import base64
from aws_cdk import (
    core, 
    aws_ec2 as ec2, 
    aws_iam as iam
)

class Lab02Stack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        #create S3 access role for ec2 
        ec2Role = iam.Role(
            self, 
            "ec2role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
            ]
        )

        instanceProfile = iam.CfnInstanceProfile(
            self,
            "ec2Profile",
            roles=[ec2Role.role_name],
            instance_profile_name="aws-cdk-handson-ec2Profile",

        )

        #create new VPC for lab02
        vpc= ec2.Vpc(self,id="aws-cdk-handson-vpc",cidr="172.30.0.0/16",nat_gateways=0,
        subnet_configuration=[ 
             { "cidrMask": 24,"name": "subnet-1-", "subnetType": ec2.SubnetType.PUBLIC },
             { "cidrMask": 24,"name": "subnet-2-", "subnetType": ec2.SubnetType.PUBLIC },
             { "cidrMask": 24,"name": "subnet-3-", "subnetType": ec2.SubnetType.PUBLIC }, 
            ])
                
        #create new Security Group
        sg = ec2.CfnSecurityGroup(
            self,
            "ec2securitygroup",
            group_description="this is aws-cdk-handson workshop",
            group_name="ec2securitygroup",
            security_group_ingress=[
                {
                    "ipProtocol": "tcp",
                    "fromPort": 80,
                    "toPort": 80,
                    "cidrIp": "0.0.0.0/0",
                },
                {
                    "ipProtocol": "tcp",
                    "fromPort": 22,
                    "toPort": 22,
                    "cidrIp": "0.0.0.0/0",
                },
            ],
            vpc_id=vpc.vpc_id
        )

        #create Elastic Network Interface
        eni0 = ec2.CfnNetworkInterface(
            self, "eni-" + str(1), subnet_id=vpc.public_subnets[0].subnet_id,
             #group_set=["sg-08cddeaeec7392eb2"]
             group_set=[sg.attr_group_id]
        )
          
        #read and base64 encode userdata file
        data = open("../resource/httpd.sh", "rb").read()
        encodedBytes = base64.encodebytes(data)
        encodedStr = str(encodedBytes, "utf-8")

        #create ec2 instances
        ami=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2)
        instance = ec2.CfnInstance(
            self,
            "ec2-httpd-" + str(1),
            image_id=ami.get_image(self).image_id, #use Amazon Linux 2 AMI 
            instance_type="t2.micro",
            key_name="wsu-ap-northeast-1",
            network_interfaces=[
                {
                    "deviceIndex": "0", 
                    "networkInterfaceId": eni0.ref
                }
            
            ],
            tags=[core.CfnTag(key="Name", value="aws-cdk-handson-ec2")],
            iam_instance_profile=instanceProfile.ref,
            user_data=encodedStr
           
        )
           
        #associate EIP with the instance
        eip = ec2.CfnEIP(self, "eip-" + str(1))
        ec2.CfnEIPAssociation(self, "eip-ass-i" + str(1),
                                 allocation_id=eip.attr_allocation_id,
                                 network_interface_id=eni0.ref)
        
        #Export PublicIP and PublicDNSName
        core.CfnOutput(self,"PublicIP",export_name="PublicIP",value=instance.attr_public_ip)
        core.CfnOutput(self,"PublicDNSName",export_name="PublicDNSName",value=instance.attr_public_dns_name)