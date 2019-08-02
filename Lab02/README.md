# Lab02
 Lab02 is ec2 instance example, include vpc, security group , userdata, ENI,EIP, assume role for ec2

 * list/deploy/destroy stack
  
  ```bash
  
  cd Lab02
  pip install -r requirements.txt
  
  #deploy stack 
  cdk deploy 
  #destory your stack 
  cdk destroy   
  
  ```
 
 * create vpc
 
 ```python
 vpc = ec2.Vpc(self,id="aws-cdk-handson-vpc",cidr="172.30.0.0/16",nat_gateways=0,
        subnet_configuration=[ 
             { "cidrMask": 24,"name": "subnet-1-", "subnetType": ec2.SubnetType.PUBLIC },
             { "cidrMask": 24,"name": "subnet-2-", "subnetType": ec2.SubnetType.PUBLIC },
             { "cidrMask": 24,"name": "subnet-3-", "subnetType": ec2.SubnetType.PUBLIC }, 
            ]) 
 ```
 
 * create new Security Group
 
 ```bash
 sg = ec2.CfnSecurityGroup(....
 
 
 #deploy second s3 bucket 
 cdk deploy lab01-us
 
 ```
 
 * create Elastic Network Interface
 
 ```python
 
 eni0 = ec2.CfnNetworkInterface(
            self, "eni-" + str(1), subnet_id=vpc.public_subnets[0].subnet_id,
             #group_set=["sg-08cddeaeec7392eb2"]
             group_set=[sg.attr_group_id]
        )
 ```

 * read and base64 encode userdata file 
 
 ```python
 #httpd.sh install httpd as service
 data = open("httpd.sh", "rb").read()
 encodedBytes = base64.encodebytes(data)
 encodedStr = str(encodedBytes, "utf-8")
 
 ```
 * create ec2 instance
 
 ```python
 #create ec2 instances
 instance = ec2.CfnInstance(....
 
 ```
 
 * associate EIP with the instance

 ```python
 eip = ec2.CfnEIP(self, "eip-" + str(1))
 ec2.CfnEIPAssociation(self, "eip-ass-i" + str(1),
                       allocation_id=eip.attr_allocation_id,
                       network_interface_id=eni0.ref)
 
 ```