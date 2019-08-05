import base64

from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    aws_elasticloadbalancingv2 as elb
)

class Lab03Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lab03_vpc=ec2.Vpc(self,"Lab03",nat_gateways=1)

        #read and base64 encode userdata file
        data = open("../resource/httpd.sh", "rb").read()
        encodedBytes = base64.encodebytes(data)
        encodedStr = str(encodedBytes, "utf-8")

        #create UserData
        httpd=ec2.UserData.for_linux()
        httpd.add_commands(str(data,'utf-8'))

        
       
        
        #create AutoScaling Group
        ami=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2) #get AMAZON Linux 2 AMI
        asg=autoscaling.AutoScalingGroup(
            self,
            "aws-cdk-asg",
            vpc=lab03_vpc,
            machine_image=ami, #use Amazon Linux 2 AMI 
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            user_data=httpd,
            min_capacity=1,
            desired_capacity=2,
            max_capacity=3,
        )

        #create Elastic Load Balancer
        lab03_alb=elb.ApplicationLoadBalancer(self,"lab03_alb",vpc=lab03_vpc,internet_facing=True)
        alb_listener=lab03_alb.add_listener("lab03_alb_listener",port=80)
        alb_listener.add_targets('Target',port=80,targets=[asg])
        
        #output ALB DNS
        core.CfnOutput(self,"Lab03ALB",export_name="Lab03ALB",value=lab03_alb.load_balancer_dns_name)
        
        
