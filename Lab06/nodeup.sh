#!/bin/bash
# Copyright 2016 The Kubernetes Authors All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash
    set -x
    set -e
    
    function mount_docker(){
        if sudo fdisk -l | grep -q /dev/nvme1n1 ; then
            local DEVICE=/dev/nvme1n1
        elif sudo fdisk -l | grep -q /dev/xvdb ; then
            local DEVICE=/dev/xvdb
        else
            echo "mount data failed" | tee /tmp/userdata.err
            exit 1
        fi
        sudo mkfs.xfs -n ftype=1 ${DEVICE}
        sudo systemctl stop docker || true
        sudo mv /var/lib/docker  /var/lib/docker.old
        sudo mkdir -p /var/lib/docker
    
        DOCKER_VOLUME_UUID=$(sudo blkid -o value ${DEVICE} | head -n 1)
        DOCKER_VOLUME_FS=$(sudo blkid -o value ${DEVICE} | tail -n 1)
        sudo grep -q ${DOCKER_VOLUME_UUID} /etc/fstab || echo "UUID=${DOCKER_VOLUME_UUID}     /var/lib/docker           ${DOCKER_VOLUME_FS}    defaults,noatime  1   1" | sudo tee -a /etc/fstab
        sudo mount -a
    
        sudo bash -c 'cp -ra /var/lib/docker.old/* /var/lib/docker'
        sudo systemctl start docker || true
    }
    
    function mount_data(){
        if sudo fdisk -l | grep -q /dev/nvme2n1 ; then
            local DEVICE=/dev/nvme2n1
        elif sudo fdisk -l | grep -q /dev/xvdc ; then
            local DEVICE=/dev/xvdc
        else
            echo "mount data failed" | tee /tmp/userdata.err
            exit 1
        fi
        sudo mkfs.xfs -n ftype=1 ${DEVICE}
        sudo mkdir -p /data
        DATA_VOLUME_UUID=$(sudo blkid -o value ${DEVICE} | head -n 1)
        DATA_VOLUME_FS=$(sudo blkid -o value ${DEVICE} | tail -n 1)
        sudo grep -q ${DATA_VOLUME_UUID} /etc/fstab || echo "UUID=${DATA_VOLUME_UUID}     /data           ${DATA_VOLUME_FS}    defaults,noatime  1   1" | sudo tee -a /etc/fstab
        sudo mount -a
    }
    

function try-download-release() {
  # TODO(zmerlynn): Now we REALLY have no excuse not to do the reboot
  # optimization.

  local -r nodeup_urls=( $(split-commas "${NODEUP_URL}") )
  local -r nodeup_filename="${nodeup_urls[0]##*/}"
  if [[ -n "${NODEUP_HASH:-}" ]]; then
    local -r nodeup_hash="${NODEUP_HASH}"
  else
  # TODO: Remove?
    echo "Downloading sha1 (not found in env)"
    download-or-bust "" "${nodeup_urls[@]/%/.sha1}"
    local -r nodeup_hash=$(cat "${nodeup_filename}.sha1")
  fi

  echo "Downloading nodeup (${nodeup_urls[@]})"
  download-or-bust "${nodeup_hash}" "${nodeup_urls[@]}"

  chmod +x nodeup
}

function download-release() {
  # In case of failure checking integrity of release, retry.
  until try-download-release; do
    sleep 15
    echo "Couldn't download release. Retrying..."
  done

  echo "Running nodeup"
  # We can't run in the foreground because of https://github.com/docker/docker/issues/23793
  ( cd ${INSTALL_DIR}; ./nodeup --install-systemd-unit --conf=${INSTALL_DIR}/kube_env.yaml --v=8  )
}
    
mount_docker
mount_data
    

sudo /etc/eks/bootstrap.sh --apiserver-endpoint 'https://90DE993B96561C12DF63FD40F281ECC7.gr7.us-east-1.eks.amazonaws.com' --b64-cluster-ca 'LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUN5RENDQWJDZ0F3SUJBZ0lCQURBTkJna3Foa2lHOXcwQkFRc0ZBREFWTVJNd0VRWURWUVFERXdwcmRXSmwKY201bGRHVnpNQjRYRFRFNU1USXhOREF5TXpJeE5Gb1hEVEk1TVRJeE1UQXlNekl4TkZvd0ZURVRNQkVHQTFVRQpBeE1LYTNWaVpYSnVaWFJsY3pDQ0FTSXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBSlF1CjhFRDNIMFBjb1NXM040TE0xM3FrbkdCaFhJVVRDREc3TTFyMFFCYmk1WU1NVHZvVDc4Ky9ScHJveGhnalplRjMKUFc2S3pYcnpib2RaaVEveWhtTTRSZmlWcDRjM1NETzNsZWZQam9aYVJJYkRCdG5HOUhTVXA0cVp1NExYU2YydQpDVVhLOE5kMENkeWdObHE2eXV6NzNndHBoZWp0V0wxVEw3Q2FuN1dvOFFLNEVlNnJvQkVtMGtsMGNZNDZ4RU5pCjg0MG5PVGpvOFJJblROY0dyaXZKOGh0UWx3OXJZYno0L3l6QU53UFJtUWF1ckVSazVCSGRnYVU0c3cxbGxkYjQKcTVJbWJnUW9zam0rME8yV0MxRTVjK25BTkdjV08xRGJsdXl6bnZuenVxMkhIK2pnNUFDTm5mMjliR3I2dWltTgpoNzNkZFpRZXBWc2hWbHpiRXlNQ0F3RUFBYU1qTUNFd0RnWURWUjBQQVFIL0JBUURBZ0trTUE4R0ExVWRFd0VCCi93UUZNQU1CQWY4d0RRWUpLb1pJaHZjTkFRRUxCUUFEZ2dFQkFKUEljNXZUWlJkbjFSb3ZsalpOK2dZQXhsTmcKb1VIOVJSTmNiSmRKbjR1QlhRNXRCR1IrQWxKazlKbGdHVEpwRFNnNXJrVmNaR20wK2JYbDNhc3pjRit6cFdkRgpja3NncFVvaGZWVUEwOHcvVTdlQWdFM3RyN0VENjk1OXNyQWRLLzJoRThDV3dZSksvNDZnWkNKbVh4THNTd3NmCmd0bmVTcmpJQ0ovQzdCSFd0allOMitmcmM2MDlvczZtZWpCOFpsRjVoZjRpeVpzZXk4SkIvZnRqOWpNOUg3VnYKd1d2NjFpMnN2TG1SenlRcU1GV0xWRWZ5bFI3dktzU0pieFBlYlJRYjhubTAwTUFrSjkrSlo5VkRERGM1cDM5LwpNRmViUDlHdWhLMEp3eUxZQk1UdkFscVZ5YzNHVHhWbjJDbTlEbS91MnV1Kyt0ZVNoWGptMVhHcVVWOD0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=' 'eks-asgfleet-01'


#download-release
echo "== nodeup node config done =="
