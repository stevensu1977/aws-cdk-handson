from aws_cdk import core, aws_s3 as s3


class Lab04Stack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # get region, use region as bucket postfix name
        region = self.region
        
        # init CfnBucket
        bucket = s3.CfnBucket(
            self,
            id,
            bucket_name="aws-cdk-handson-" + region+"-test",
            bucket_encryption={
                "serverSideEncryptionConfiguration": [
                    {"serverSideEncryptionByDefault": {"sseAlgorithm": "AES256"}}
                ]
            },
            versioning_configuration={"status": "Enabled"},
        )

        core.CfnOutput(
            self, "BucketArn", export_name="Lab04BucketArn", value=bucket.attr_arn
        )
        # The code that defines your stack goes here
