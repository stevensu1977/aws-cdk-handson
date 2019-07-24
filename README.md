# aws-cdk-handson
This is hands-on lab for aws cdk, cdk support typescript,javascript,java,.net, python , this lab only cover python and typescript.


## Set your environment
  [Prerequisites](https://github.com/stevensu1977/aws-cdk-handson/blob/master/prerequisites.md)
  
  
## Lab 

 Lab01 create your first stack 

 * init empty stack
  
  ```bash
  #linux or macOS
  cdk init app --language python
  source .env/bin/activate
  pip install -r requirements.txt
  
  
  #use region parameter 
  cdk deploy --region ap-northeast-1
  
  cdk destroy --region ap-norheast-1
  
  ```
 
 * add s3 bucket to stack
 
 ```bash
 pip install aws-cdk.aws_s3
 
 ``` 
 
 * code comments
 
 ```python
 #
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
  


