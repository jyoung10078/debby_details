import * as cdk from 'aws-cdk-lib/core';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as path from 'path';

export class AwsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create Lambda Layer for langchain and dependencies
    const langchainLayer = new lambda.LayerVersion(this, 'LangchainLayer', {
      code: lambda.Code.fromAsset(path.join(__dirname, '../lambda/layers/langchain')),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_11],
      description: 'Langchain and dependencies layer'
    });

    // Create Lambda function with proper Python runtime
    const agentFunction = new lambda.Function(this, 'AgentKickoff', {
      runtime: lambda.Runtime.PYTHON_3_11,
      code: lambda.Code.fromAsset(path.join(__dirname, '../handlers/agentStarter')),
      handler: 'index.lambda_handler',
      layers: [langchainLayer],
      environment: {
        OPENAI_API_KEY: process.env.OPENAI_API_KEY || '',
      },
      timeout: cdk.Duration.seconds(60),
      memorySize: 512,
    });

    // Create API Gateway
    const api = new apigateway.RestApi(this, 'AgentApi', {
      restApiName: 'Agent Service API',
      description: 'API for the debby_details agent',
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS,
      },
    });

    // Create /agent resource and POST method
    const agentResource = api.root.addResource('agent');
    agentResource.addMethod('POST', new apigateway.LambdaIntegration(agentFunction));

    // Output the API endpoint
    new cdk.CfnOutput(this, 'ApiEndpoint', {
      value: api.url,
      description: 'API Gateway endpoint URL',
    });
  }
}
