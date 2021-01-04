# Lab03
准备环境


##Lab03 is AutoScalingGroup , Elastic Load Balancer example, you create web servers used CDK.

 * deploy/destroy stack

  ```bash
  
  cd Lab03
  pip install -r requirements.txt
  
  #deploy stack 
  cdk deploy 
  
  #destory your stack 
  cdk destroy   
  
  ```

 * create  AutoScaling Group

 ```python
    #create AutoScaling Group
    ami=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2) #get AMAZON Linux 2 AMI
    asg=autoscaling.AutoScalingGroup(
            self,
            "aws-cdk-asg",
            vpc=lab03_vpc,
            machine_image=ami, #use Amazon Linux 2 AMI 
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            user_data=httpd,
            min_capacity=1,
            desired_capacity=2,
            max_capacity=3,
        )
        
 ```

 * create Elastic Load balancer

 ```bash
    #create Elastic Load Balancer
    lab03_alb=elb.ApplicationLoadBalancer(self,"lab03_alb",vpc=lab03_vpc,internet_facing=True)
    alb_listener=lab03_alb.add_listener("lab03_alb_listener",port=80)
    alb_listener.add_targets('Target',port=80,targets=[asg])
 
 ```
