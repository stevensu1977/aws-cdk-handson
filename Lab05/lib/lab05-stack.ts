import cdk = require('@aws-cdk/core');
import ec2 = require('@aws-cdk/aws-ec2');
import rds = require('@aws-cdk/aws-rds');

export class Lab05Stack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    
    const vpc=ec2.Vpc.fromLookup(this,"defaultVPC",{vpcId:'vpc-704ac70a'})
    const sourceInstance = new rds.DatabaseInstance(this, 'Instance', {
      engine: rds.DatabaseInstanceEngine.MYSQL,
      instanceClass: ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
      masterUsername: 'admin',
      vpc
    });

    // WHEN
    new rds.DatabaseInstanceReadReplica(this, 'ReadReplica', {
      sourceDatabaseInstance: sourceInstance,
      engine: rds.DatabaseInstanceEngine.MYSQL,
      instanceClass: ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.LARGE),
      vpc
    });

  }
}
