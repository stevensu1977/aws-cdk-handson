# Lab01
Lab01 使用CDK创建S3 bucket

 * 初始化项目

  ```bash
  
  cd Lab01
  pip install -r requirements.txt
  
  #列出当前Stack
  cdk list
  #部署s3 bucket
  cdk deploy 
  #删除stack 
  cdk destroy   
  
  ```
 
 * 代码说明
 ```python
 #lab01/lab01_stack.py
 #get region, use region and datetime as bucket postfix name
 region=self.region
 now=datetime.datetime.now().strftime("%Y%M%d%H%M")
 #初始化 CfnBucket,设置bucke_name
 s3.CfnBucket(self,id,bucket_name="aws-cdk-handson-"+region+"-"+now)
 ```
 
 ```python
 #如果要部署到东京region请删除以下注释
 #region="ap-northeast-1"
 #重新执行 cdk deploy
 ```



