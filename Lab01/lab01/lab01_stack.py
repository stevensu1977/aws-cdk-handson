from aws_cdk import (
    core,
    aws_s3 as s3
)

class Lab01Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #get region, use region as bucket postfix name
        region=self.region
        #init CfnBucket
        s3.CfnBucket(self,id,
                    bucket_name="stevensu-cdk-"+region,
                    bucket_encryption={
                         'serverSideEncryptionConfiguration':[
                               {'serverSideEncryptionByDefault':
                                 {'sseAlgorithm':'AES256'}
                               }
                             ]
                         }
                    )
        # The code that defines your stack goes here
