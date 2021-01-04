import * as cdk from '@aws-cdk/core';

import * as lambda from '@aws-cdk/aws-lambda';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as iam from '@aws-cdk/aws-iam';
import * as elbv2 from '@aws-cdk/aws-elasticloadbalancingv2';
import * as targets from '@aws-cdk/aws-elasticloadbalancingv2-targets';

export class Lab09Stack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
  }
}


export class ImportedLambdaTarget implements elbv2.IApplicationLoadBalancerTarget {

  constructor(private readonly fn: lambda.IFunction) {
  }

  public attachToApplicationTargetGroup(targetGroup: elbv2.IApplicationTargetGroup): elbv2.LoadBalancerTargetProps {
    const permission = new lambda.CfnPermission(cdk.Stack.of(this.fn), 'GrantInvoke', {
      action: 'lambda:InvokeFunction',
      principal: 'elasticloadbalancing.amazonaws.com',
      functionName: this.fn.functionArn,
    });
    targetGroup.node.addDependency(permission)
    
    return {
      targetType: elbv2.TargetType.LAMBDA,
      targetJson: { id: this.fn.functionArn },
    };
  }
}


function getOrCreateVpc(scope: cdk.Construct): ec2.IVpc {
  // use an existing vpc or create a new one
  return scope.node.tryGetContext('use_default_vpc') === '1' ?
    ec2.Vpc.fromLookup(scope, 'Vpc', { isDefault: true }) :
    scope.node.tryGetContext('use_vpc_id') ?
      ec2.Vpc.fromLookup(scope, 'Vpc', { vpcId: scope.node.tryGetContext('use_vpc_id') }) :
      new ec2.Vpc(scope, 'Vpc', { maxAzs: 3, natGateways: 1 });
}