# Lab02
 Lab02 使用CDK创建一个自动安装apache/httpd的EC2实例(自定义VPC、 安全组、 userdata, ENI、EIP、 设置角色)

 * deploy/destroy stack
  
  ```bash
  
  cd Lab02
  pip install -r requirements.txt
  
  #部署ec2实例,通过outputs里面的信息可以访问apache web server 
  cdk deploy 

  Outputs:
  lab02.PublicDNSName = <ec2>.<region>.compute.amazonaws.com
  lab02.PublicIP = <ip地址>
 
 #清除ec2实例 
  cdk destroy   
  
  ```
 
 * 创建VPC
 
 ```python
 vpc = ec2.Vpc(self,id="aws-cdk-handson-vpc",cidr="172.30.0.0/16",nat_gateways=0,
        subnet_configuration=[ 
             { "cidrMask": 24,"name": "subnet-1-", "subnetType": ec2.SubnetType.PUBLIC },
             { "cidrMask": 24,"name": "subnet-2-", "subnetType": ec2.SubnetType.PUBLIC },
             { "cidrMask": 24,"name": "subnet-3-", "subnetType": ec2.SubnetType.PUBLIC }, 
            ]) 
 ```
 
 * 创建安全组
 
 ```bash
 sg = ec2.CfnSecurityGroup(....
 
 ```
 
 * 创建Elastic Network Interface
 
 ```python
 
 eni0 = ec2.CfnNetworkInterface(
            self, "eni-" + str(1), subnet_id=vpc.public_subnets[0].subnet_id,
             #group_set=["sg-08cddeaeec7392eb2"]
             group_set=[sg.attr_group_id]
        )
 ```

 * 读取/加载 userdata 自定义启动脚本 
 
 ```python
 #httpd.sh install httpd as service
 data = open("httpd.sh", "rb").read()
 encodedBytes = base64.encodebytes(data)
 encodedStr = str(encodedBytes, "utf-8")
 
 ```
 * create ec2 instance
 
 ```python
 #create ec2 instances
 instance = ec2.CfnInstance(....
 
  key_name="wsu-ap-northeast-1",#这个是keypair的名字非常重要,请更换你设置的keypair name

 ```
 
 * 为ec2实例分配固定EIP

 ```python
 eip = ec2.CfnEIP(self, "eip-" + str(1))
 ec2.CfnEIPAssociation(self, "eip-ass-i" + str(1),
                       allocation_id=eip.attr_allocation_id,
                       network_interface_id=eni0.ref)
 
 ```