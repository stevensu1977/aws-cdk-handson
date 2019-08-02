# Lab01
Lab01 use cdk create s3 bucket 

 * list/deploy/destroy stack
  
  ```bash
  
  cd Lab01
  pip install -r requirements.txt
  
  #list your stack
  cdk list
  #deploy stack 
  cdk deploy 
  #destory your stack 
  cdk destroy   
  
  ```
 
 * how to create s3 bucket 
 
 ```python
 #lab01/lab01_stack.py
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
 
 ```
 
 * create second s3 bucket for us-west-2 region
 
 ```bash
 #app.py
 #remove comments from line 12
 
 Lab01Stack(app, "lab01-us",env={"region":"us-west-2"})
 
 
 #deploy second s3 bucket 
 cdk deploy lab01-us
 
 ```


