from aws_cdk import core


class Lab00Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # The code that defines your stack goes here
        core.CfnOutput(self,"CDKMetadata",value="hello cdk")
