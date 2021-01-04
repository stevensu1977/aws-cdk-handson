#!/usr/bin/env python3



from aws_cdk import (
    core
)



from lab02.lab02_stack import Lab02Stack



app = core.App()

#special region
region="cn-northwest-1"

#如果需要加载已有的资源需要设置账号, 比如ec2.Vpc.from_lookup(self, "aws-cdk-handson-lab02-vpc",vpc_name="default")
#account ="111111111111" #替换成你自己的账号 
#Lab02Stack(app, "lab02-"+region,env={"region":region,"account":account})

Lab02Stack(app, "lab02-"+region,env={"region":region})



app.synth()
