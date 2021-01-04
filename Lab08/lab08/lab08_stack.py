from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_elasticloadbalancingv2 as elb,
    aws_elasticloadbalancingv2_targets as _targets,
     aws_ec2 as ec2,
)

import time

class Lab08Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        my_lambda = _lambda.Function(
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='hello.handler',
        )

        
        
        
        

        version01=_lambda.Version(self,"version01",lambda_=my_lambda)
        alias_beta= _lambda.Alias(self,"alias_beta",alias_name="beta",version=version01)

        #当我创建v3的时候我可以使用下面的代码,为v2创建一个新的别名alias_v2
        #v2=_lambda.Version.from_version_arn(self,"v",version_arn="arn:aws-cn:lambda:cn-northwest-1:188642756190:function:lab08-HelloHandler2E4FBA4D-1D2KNU1L6W08T:2")
        #alias_v2= _lambda.Alias(self,"alias_v2",alias_name="alias_v2",version=version01)
        
        #始终保持别名prod在最新的版本
        alias_prod= _lambda.Alias(self,"prod",alias_name="prod",version=my_lambda.current_version)


        # v5=_lambda.Version.from_version_arn(self,"v5",version_arn="arn:aws-cn:lambda:cn-northwest-1:188642756190:function:lab08-HelloHandler2E4FBA4D-1UZFGVUVZPTQJ:5")

        # alias_prod= _lambda.Alias(self,"prod",alias_name="prod",version=v5)
        
        
        
        lab03_alb=elb.ApplicationLoadBalancer(self,"lab03_alb",vpc=lab03_vpc,internet_facing=True)
        alb_listener=lab03_alb.add_listener("lab03_alb_listener",port=80)
        
        alb_listener.add_targets('Target',targets=[_targets.LambdaTarget(fn=my_lambda)])
        

        # my_lambda.add_permission("alb",principal=iam.ServicePrincipal("elasticloadbalancing.amazonaws.com"))