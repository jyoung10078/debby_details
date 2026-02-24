import * as cdk from 'aws-cdk-lib/core';
import { Construct } from 'constructs';
import * as llambda from 'aws-cdk-lib/aws-lambda';

export class AwsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    new llambda.Function(this, 'AgentKickoff', {
      runtime: llambda.Runtime.NODEJS_20_X,
      code: llambda.Code.fromAsset('lambda'),
      handler: 'index.handler'
    });
  }
}
