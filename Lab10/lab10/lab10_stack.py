from aws_cdk import (
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_ec2 as ec2, 
    aws_sns_subscriptions as subs,
    core
)

class Lab10Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        queue = sqs.Queue(
            self, "Lab10Queue",
            visibility_timeout=core.Duration.seconds(300),
        )

        topic = sns.Topic(
            self, "Lab10Topic"
        )

        topic.add_subscription(subs.SqsSubscription(queue))

        vpc = ec2.Vpc.from_lookup(self, "aws-cdk-handson-lab02-vpc",vpc_name="default")

        # The code that defines your stack goes here
        core.CfnOutput(self,"CDKMetadata",value="hello cdk")
