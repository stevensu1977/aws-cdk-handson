import base64
from aws_cdk import (
    core, 
    aws_ec2 as ec2, 
    aws_iam as iam
)

class Lab02Stack(core.Stack):
    def __init__(self, scope: core.Construct, id: str,custom:dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        region = self.region

        #create S3 access role for ec2 
        ec2Role = iam.Role(
            self, 
            "aws-cdk-handson-lab02-ec2role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
            ]
        )

        instanceProfile = iam.CfnInstanceProfile(
            self,
            "aws-cdk-handson-lab02-ec2Profile",
            roles=[ec2Role.role_name],
            instance_profile_name="aws-cdk-handson-lab02-ec2Profile",

        )

        #create new VPC for lab02
        #vpc = ec2.Vpc.from_lookup(self, "aws-cdk-handson-lab02-vpc",vpc_name="default") #使用默认的vpc

        #创建新的vpc
        vpc= ec2.Vpc(self,id="aws-cdk-handson-lab02-vpc",cidr="172.30.0.0/16",nat_gateways=0,
        subnet_configuration=[ 
             { "cidrMask": 24,"name": "subnet-1-", "subnetType": ec2.SubnetType.PUBLIC },
             { "cidrMask": 24,"name": "subnet-2-", "subnetType": ec2.SubnetType.PUBLIC },
             { "cidrMask": 24,"name": "subnet-3-", "subnetType": ec2.SubnetType.PUBLIC }, 
            ])

        
        
                
        
        #使用已有的安全组
        #sg=ec2.SecurityGroup.from_security_group_id(self,"nodeSG",security_group_id='sg-0dd53aaa5c9eb8324')

        #创建新的安全组
        sg = ec2.CfnSecurityGroup(
            self,
            "aws-cdk-handson-lab02-ec2securitygroup",
            group_description="this is aws-cdk-handson workshop",
            group_name="aws-cdk-handson-lab02-ec2securitygroup",
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
                {
                    "ipProtocol": "tcp",
                    "fromPort": 8080,
                    "toPort": 8080,
                    "cidrIp": "0.0.0.0/0",
                },
            ],
            vpc_id=vpc.vpc_id
        )


        
          
        #read and base64 encode userdata file
        data = open("../resource/httpd.sh", "rb").read()
        encodedBytes = base64.encodebytes(data)
        encodedStr = str(encodedBytes, "utf-8")

        #create ec2 instances
        ami=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2)

        #创建2台EC2
        ec2Count = 2

        
        
        for i in range(ec2Count):
            
            eni0=ec2.CfnNetworkInterface(
            self, "eni-" + str(i), subnet_id=vpc.public_subnets[0].subnet_id,
            group_set=[sg.attr_group_id]
            )
            #group_set=[sg.security_group_id]
            instance = ec2.CfnInstance(
            self,
            "ec2-httpd-" + str(i),
            image_id=ami.get_image(self).image_id, #use Amazon Linux 2 AMI 
            instance_type="t3.micro",
            key_name="wsu-cn-northwest-1",#这个是keypair的名字非常重要
            tags=[core.CfnTag(key="Name", value="aws-cdk-lab02-ec2-"+str(i))], #加上标签
            iam_instance_profile=instanceProfile.ref,
            user_data=encodedStr,
            network_interfaces=[{
                    'deviceIndex': '0',
                    'networkInterfaceId': eni0.ref,
            }])

            core.CfnOutput(self,"PublicIP-"+str(i),export_name="PublicIP-"+str(i),value=instance.attr_public_ip)
            core.CfnOutput(self,"PublicDNSName-"+str(i),export_name="PublicDNSName-"+str(i),value=instance.attr_public_dns_name)
            

        

        

       

       
       