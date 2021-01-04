from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    core,
)

import base64


key_name='wsu-us-east-1'
vpc_id='vpc-03d1d3531a36fa1fc'
region='us-east-1'
nodes_role_arn='arn:aws:iam::596030579944:instance-profile/eksworkshop-admin'
ami_id='ami-0392bafc801b7520f'

class EksWorkerNodesStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # get vpc used vpc-id
        vpc = ec2.Vpc.from_lookup(self, "EKSNode",vpc_id=vpc_id)
        
        subnets=[]
        if len(vpc.private_subnets)>0:
            subnets.extend(vpc.private_subnets)
        elif len(vpc.public_subnets)>0:
            subnets.extend(vpc.public_subnets)
        else:
            print("Not any subnets found,")
            return 
            
        
        # add a worker node role
        workerRole =iam.Role.from_role_arn(self,'nodeRole',role_arn=nodes_role_arn)
       
        #node_sg=ec2.SecurityGroup.from_security_group_id(self,"nodeSG",security_group_id='sg-0461d7bdfb942d0ef')

        # add iam instance profile
        instanceProfile = iam.CfnInstanceProfile(self, 'kopsNodeProfile', roles=[workerRole.role_name],
                                                 instance_profile_name='eks-cluster-workerNodeProfile')

        # read and base64 encode userdata file
        data = open('nodeup.sh', 'rb').read()
        encodedBytes = base64.encodebytes(data)
        encodedStr = str(encodedBytes, "utf-8")
        
       
        # add worker instances and associate EIPs
        for i in range(0, 1):
            # add a network interface
            eni0 = ec2.CfnNetworkInterface(
                self, 'eni-' + str(i), subnet_id='subnet-040455b57b16a4cc9',group_set=['sg-0461d7bdfb942d0ef','sg-0b3ae225b27e04679'])
           
            # add worker instances 
            instance = ec2.CfnInstance(self,
                                       "kops-node-" + str(i),
                                       image_id=ami_id,
                                       instance_type="t2.medium",
                                       block_device_mappings=[
                                        {
                                            'deviceName': '/dev/xvda',
                                            'ebs': {
                                                'deleteOnTermination': True,
                                                'volumeSize': 40,
                                                'volumeType': 'gp2',
                                                'encrypted': False,
                                            },
                                        },
                                        {
                                            'deviceName': '/dev/sdb',  # for /var/lib/docker
                                            'ebs': {
                                                'deleteOnTermination': True,
                                                'volumeSize': 100,
                                                'volumeType': 'gp2',
                                                'encrypted': False,
                                            },
                                        },
                                        {
                                            'deviceName': '/dev/sdc',  # for data volume
                                            'ebs': {
                                                'deleteOnTermination': True,
                                                'volumeSize': 200,
                                                'volumeType': 'gp2',
                                                'encrypted': False,
                                            },
                                        },
                                    ],
                                       key_name=key_name,
                                       network_interfaces=[{
                                            'deviceIndex': '0',                              
                                            'networkInterfaceId': eni0.ref,
                                       }],
                                       iam_instance_profile=instanceProfile.ref,
                                       #iam_instance_profile=nodes_role_arn,
                                       tags=[
                                           core.CfnTag(
                                           key="KubernetesCluster", 
                                           value="eks-asgfleet-01"),
                                           core.CfnTag(key="Name", 
                                           value="test-01"),
                                           core.CfnTag(key="k8s.io/role/node", 
                                           value="1"),
                                           core.CfnTag(key="CDK/manual", 
                                           value="singlenode"),
                                           ],
                                       user_data=encodedStr
                                       )

            #associate EIP with the instance
            eip = ec2.CfnEIP(self, "eip-" + str(i))
            ec2.CfnEIPAssociation(self, "eip-ass-i" + str(i), 
                                 allocation_id=eip.attr_allocation_id, 
                                 network_interface_id=eni0.ref)
