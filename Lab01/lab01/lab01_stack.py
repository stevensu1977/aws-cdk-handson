# -*- coding: utf-8 -*-
"""
   Copyright 2019 Wei(Steven) Su
   Email: suwei007@gmail.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from aws_cdk import core, aws_s3 as s3
from datetime import datetime

class Lab01Stack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #获取region变量, 使用region 和 datetime 作为bucket的名字
        region = self.region
        now=datetime.now().strftime("%Y%M%d%H%M")
        
        #初始化 CfnBucket,设置bucket_name
        bucket = s3.CfnBucket(self,id,bucket_name="aws-cdk-handson-" + region+"-"+now)
        
        #输出Bucket名字和ARN
        core.CfnOutput(self,"BucketName",value=bucket.bucket_name
        )
        core.CfnOutput(
            self, "BucketArn", value=bucket.attr_arn
        )
        
        
