import json

from aws_cdk import (
    core,
    aws_ec2 as ec2, 
    aws_s3 as s3, 
    aws_iam as iam,
    aws_dms as dms,
    aws_rds as rds,
    aws_kinesis as kinesis,
    aws_kinesisanalytics as kinesisanalytics,
    aws_kinesisfirehose as firehose,
    aws_secretsmanager as secretsmanager

)
from aws_cdk.aws_lambda import Version


class Lab11Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        
        #获取vpc
        #vpc = ec2.Vpc.from_lookup(self, 'default',is_default=True,vpc_name='default')
        vpc =ec2.Vpc.from_lookup(self,'dms-vpc',vpc_id='vpc-08b56fb6053ca2c75')


        #创建RDS参数组
        db_parameter=rds.ParameterGroup(
            self,'dms-param-mysql5.7',
            engine=rds.DatabaseInstanceEngine.mysql(version=rds.MysqlEngineVersion.VER_5_7),
            parameters={"binlog_format":"ROW"}
        )

        # sourceDB = rds.DatabaseInstanceFromSnapshot(
        #     self,'dms-rds-soruce',
        #     snapshot_identifier= 'tickets-mysql57',
        #     engine=rds.DatabaseInstanceEngine.MYSQL,
        #     instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3,ec2.InstanceSize.MEDIUM),
        #     vpc=vpc,
        #     parameter_group=db_parameter
        #     )

       

        # sourceDB = rds.DatabaseInstance(
        #     self,'dms-rds-soruce',
        #     #instance_identifier='dms-rds-soruce',
        #     engine=rds.DatabaseInstanceEngine.mysql(
        #         version=rds.MysqlEngineVersion.VER_5_7
        #     ),
        #     instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3,ec2.InstanceSize.MEDIUM),
        #     vpc=vpc,
        #     parameter_group=db_parameter,
        #     #credentials=rdsPasswordSecret
        #     )

        # sourceDB.connections.allow_default_port_internally()

        dms_rep = dms.CfnReplicationInstance(self, 'dms-replication',replication_instance_class='dms.c5.large',engine_version='3.4.0')

        stream = kinesis.Stream(self,'dms-steam')

        streamWriteRole = iam.Role(self, 'dms-stream-role', assumed_by= iam.ServicePrincipal('dms.amazonaws.com'))

        streamWriteRole.add_to_policy(
            iam.PolicyStatement(
                resources=[stream.stream_arn],
                actions=[
                    'kinesis:DescribeStream',
                    'kinesis:PutRecord',
                    'kinesis:PutRecords'
                ]
        ))

        

        source = dms.CfnEndpoint(self,'dms-source',endpoint_type='source',engine_name='mysql',username='admin',password='gjsNoihHVj9pV5s3JNv7',server_name="dms-rdssource.c7iucbqgd2xo.us-east-1.rds.amazonaws.com",port=3306)

        target = dms.CfnEndpoint(self,'dms-target', endpoint_type='target',engine_name='kinesis',kinesis_settings={"messageFormat":"JSON",'streamArn':stream.stream_arn,"serviceAccessRoleArn":streamWriteRole.role_arn})

        dmsTableMappings = {
            "rules": [
                {
                    "rule-type": "selection",
                    "rule-id": "1",
                    "rule-name": "1",
                    "object-locator": {
                        "schema-name": "dms_sample",
                        "table-name": "t_log_levelup"
                        },
                        "rule-action": "include"
                }
        ]}

        dms.CfnReplicationTask(self,'dms-stream-repTask',
        replication_instance_arn=dms_rep.ref,
        migration_type= 'full-load-and-cdc',
        source_endpoint_arn= source.ref,
        target_endpoint_arn=target.ref,
        table_mappings=json.dumps(dmsTableMappings))

        analyticsRole=iam.Role(self,'KinesisAnalyticsRole',assumed_by=iam.ServicePrincipal('kinesisanalytics.amazonaws.com'))

        kinesisanalytics.CfnApplicationV2(
            self,'KinesisAnalytics',
            application_name='dms-stream-anlytics',
            service_execution_role=analyticsRole.role_arn,
            runtime_environment='SQL-1_0',
            application_configuration={
                'sqlApplicationConfiguration': {
                    'inputs': [
                        {
                            'namePrefix': "exampleNamePrefix",
                            'inputSchema': {
                                'recordColumns': [
                                    {
                                        'name': "example",
                                        'sqlType': "VARCHAR(16)",
                                        'mapping': "$.example"
                                        }
                                ],
                            'recordFormat': {
                                'recordFormatType': "JSON",
                                'mappingParameters': {
                                    'jsonMappingParameters': {
                                        'recordRowPath': "$"
                                    }
                                }
                            }
              },
              'kinesisStreamsInput': {
                'resourceArn': stream.stream_arn
              }
            }

          ]
        },
        'applicationCodeConfiguration': {
          'codeContent': {
            'textContent': "Example Application Code"
          },
          'codeContentType': "PLAINTEXT"
        }
      })

        


    
        
