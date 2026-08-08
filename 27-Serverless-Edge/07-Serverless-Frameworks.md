---
section: Serverless & Edge
category: DevOps
tags: [concept, reference, tool]
---

# Serverless Frameworks (SAM, CDK, SST, Serverless Framework)

> Senior full-stack interviews increasingly ask about IaC for serverless. This file covers the four dominant frameworks: AWS SAM, AWS CDK, Serverless Framework, and SST. Each has trade-offs around abstraction level, language, and ecosystem.

## Definition

Serverless frameworks are infrastructure-as-code tools purpose-built for FaaS and managed-service architectures. They abstract CloudFormation (or Terraform) with higher-level constructs for functions, APIs, queues, and event sources, letting you ship Lambda-based stacks without writing raw YAML.

## Why It Matters (TL;DR)

- **Faster iteration** — declare resources in a few lines vs hundreds of CloudFormation lines
- **Local development** — SAM and SST emulate Lambda locally with `sam local` / `sst dev`
- **Type safety** — CDK and SST give you TypeScript types for AWS resources
- **CI/CD integration** — built-in deploy, rollback, and stage management

## Framework Comparison

| Dimension | AWS SAM | AWS CDK | Serverless Framework | SST |
|-----------|---------|---------|---------------------|-----|
| Language | YAML/JSON | TypeScript, Python, Go, Java, .NET | YAML (plugins in JS) | TypeScript |
| IaC Underneath | CloudFormation | CloudFormation | CloudFormation (AWS), custom | CDK (sits on top) |
| Abstraction Level | Low–Mid | High (L2/L3 constructs) | Mid (serverless-only) | High (Live Lambda, WebSocket, etc.) |
| Local Dev | `sam local` | `cdk synth` + manual | `serverless offline` | `sst dev` (live reload over HTTPS) |
| Type Safety | No | Yes | No | Yes |
| Multi-Cloud | No (AWS) | No (AWS, but extensible) | Yes (AWS, Azure, GCP, etc.) | No (AWS) |
| Best For | Pure Lambda + API Gateway stacks | Large AWS infra beyond Lambda | Multi-cloud or quick prototypes | Modern full-stack serverless apps |
| Maturity | AWS-native, GA | AWS-native, GA | Mature, large plugin ecosystem | Newer, rapidly gaining adoption |

## Code Examples

### 1. AWS SAM — REST API + Lambda + DynamoDB

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Globals:
  Function:
    Runtime: nodejs20.x
    MemorySize: 512
    Timeout: 10
    Environment:
      Variables:
        TABLE_NAME: !Ref UsersTable

Resources:
  UsersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub "${AWS::StackName}-users"
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH

  CreateUserFn:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/users.create
      Events:
        CreateApi:
          Type: HttpApi
          Properties:
            Path: /users
            Method: POST
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref UsersTable
```

```bash
# Local invocation
sam local invoke CreateUserFn --event events/create.json

# Start API locally
sam local start-api

# Deploy
sam build && sam deploy --guided
```

### 2. AWS CDK — Same Stack in TypeScript

```typescript
// lib/users-stack.ts
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { NodejsFunction } from 'aws-cdk-lib/aws-lambda-nodejs';
import { HttpApi } from 'aws-cdk-lib/aws-apigatewayv2';
import { HttpLambdaIntegration } from 'aws-cdk-lib/aws-apigatewayv2-integrations';
import { Table, AttributeType, BillingMode } from 'aws-cdk-lib/aws-dynamodb';
import { PolicyStatement } from 'aws-cdk-lib/aws-iam';

export class UsersStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const table = new Table(this, 'UsersTable', {
      partitionKey: { name: 'id', type: AttributeType.STRING },
      billingMode: BillingMode.PAY_PER_REQUEST,
    });

    const fn = new NodejsFunction(this, 'CreateUserFn', {
      entry: 'src/handlers/users.create.ts',
      environment: { TABLE_NAME: table.tableName },
    });
    table.grantReadWriteData(fn);

    const httpApi = new HttpApi(this, 'HttpApi');
    httpApi.addRoutes({
      path: '/users',
      methods: [{ method: 'POST' }],
      integration: new HttpLambdaIntegration('CreateUserIntegration', fn),
    });
  }
}
```

```bash
# Synthesize CloudFormation
cdk synth

# Deploy
cdk deploy

# Diff against deployed
cdk diff
```

### 3. Serverless Framework — Multi-Cloud Style

```yaml
# serverless.yml
service: users-api
frameworkVersion: '3'

provider:
  name: aws
  runtime: nodejs20.x
  region: us-east-1
  environment:
    TABLE_NAME: ${self:service}-users

functions:
  createUser:
    handler: src/handlers/users.create
    events:
      - httpApi:
          path: /users
          method: post
  getUser:
    handler: src/handlers/users.get
    events:
      - httpApi:
          path: /users/{id}
          method: get

resources:
  Resources:
    UsersTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: ${self:service}-users
        BillingMode: PAY_PER_REQUEST
        AttributeDefinitions:
          - AttributeName: id
            AttributeType: S
        KeySchema:
          - AttributeName: id
            KeyType: HASH
```

```bash
# Local invoke
serverless invoke local --function createUser

# Start offline
serverless offline

# Deploy
serverless deploy

# Multi-stage (dev/staging/prod)
serverless deploy --stage prod
```

### 4. SST — Modern Live Lambda Development

```typescript
// sst.config.ts
/// <reference path="./.sst/platform/config.d.ts" />

export default $config({
  app(input) {
    return { name: 'users-api', removal: input.stage === 'prod' ? 'retain' : 'remove' };
  },
  async run() {
    const table = new sst.aws.Dynamo('UsersTable', {
      fields: { id: 'string' },
      primaryKey: 'id',
    });

    const api = new sst.aws.ApiGatewayV2('Api');
    api.route('POST /users', 'src/handlers/users.create', {
      environment: { TABLE_NAME: table.name },
      link: [table],
    });

    return { api: api.url };
  },
});
```

```bash
# sst dev — Live Lambda development with instant reload over HTTPS
# 1. Start the dev environment
sst dev

# 2. Save any file in src/ — the function is replaced instantly.
# 3. Hit the printed URL — changes are live in seconds.
```

### 5. Local Development Trade-offs

```text
LOCAL EMULATION COMPARISON:
┌─────────────────────────────────────────────────────────────────┐
│  AWS SAM                                                       │
│  • Pros: closest to prod; supports event payloads              │
│  • Cons: slow startup; Docker required                         │
│                                                                 │
│  SST                                                           │
│  • Pros: live reload, no Docker, real AWS env (Live Lambda)    │
│  • Cons: requires AWS account; needs deployed stack            │
│                                                                 │
│  Serverless Framework                                          │
│  • Pros: fast offline mode; mature plugins                     │
│  • Cons: not 100% AWS-accurate for edge cases                  │
│                                                                 │
│  CDK                                                           │
│  • Pros: full TypeScript, rich constructs                      │
│  • Cons: no native local emulation; pair with SAM or SST       │
└─────────────────────────────────────────────────────────────────┘
```

## When to Choose What

| Scenario | Recommended |
|----------|-------------|
| Pure Lambda + API Gateway + DynamoDB | **SAM** (simple, AWS-native) |
| Large multi-service infra beyond Lambda | **CDK** (full type safety, L2/L3 constructs) |
| Quick multi-cloud prototype | **Serverless Framework** |
| Modern full-stack with WebSockets, Cron, Auth | **SST** (Live Lambda, WebSocket constructs) |
| Team mostly writes Java/Python and wants IaC | **CDK** |
| Single-purpose serverless API, smallest cognitive load | **SAM** |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Mixing SAM with raw CloudFormation in the same stack | Use SAM `Globals` for shared config; keep custom CFN minimal |
| Not using `NodejsFunction` / `PythonFunction` constructs (CDK) | They auto-bundle with esbuild; smaller packages, faster cold starts |
| Forgetting to set CloudFormation stack termination protection | Enable on production stacks to prevent accidental deletion |
| Treating SST dev as a replacement for unit tests | SST dev hits real AWS; use unit tests with mocked handlers for CI |
| Choosing Serverless Framework for large AWS-only infra | CDK is better — typed, more AWS services, better DX |

## Best Practices

1. **Pick one framework per repo** — mixing causes drift
2. **Use environment variables and SSM** — never hardcode secrets in template files
3. **Pin versions** — SAM `Transform` version, CDK `lib` version, SST version
4. **Test locally before deploy** — `sam local invoke`, `sst dev`, `serverless offline`
5. **Use stages** — dev / staging / prod, with separate stacks for isolation
6. **CI/CD** — `sam pipeline` (SAM), `cdk deploy` in GitHub Actions, `serverless deploy` in CI
7. **Drift detection** — `cdk diff` before every deploy

## Summary

- SAM, CDK, Serverless Framework, and SST are the four dominant serverless frameworks
- Choose SAM for pure Lambda + API Gateway stacks; CDK for large infra; SST for modern full-stack; Serverless Framework for multi-cloud
- Local dev tools (`sam local`, `sst dev`, `serverless offline`) trade fidelity for speed — pair with unit tests for CI
- Pin versions, use stages, and integrate with CI/CD for predictable deploys

---

## Cheat Sheet

```text
SERVERLESS FRAMEWORKS CHEAT SHEET
═══════════════════════════════════════════════════════════════

CHOOSE BY TEAM:
  • Small team, simple stacks       → SAM
  • TypeScript-first org           → CDK or SST
  • Multi-cloud needs              → Serverless Framework
  • WebSocket / Live Lambda / Cron → SST

KEY CLI COMMANDS:
  SAM:                 sam build && sam deploy --guided
  CDK:                 cdk synth && cdk deploy
  Serverless:          sls deploy (or serverless deploy)
  SST:                 sst deploy

INTERVIEW ANSWER:
  1. What problem the framework solves vs raw CloudFormation
  2. Type safety / abstraction level
  3. Local dev story
  4. When to reach for it (real example)
```

---

## See Also

- [AWS Lambda](05-AWS-Lambda.md)
- [CI/CD](../15-CI-CD/)
- [Docker](../13-Docker/)
- [Edge Functions](02-Edge-Functions.md)
- [Serverless Overview](01-Serverless-Overview.md)
- [Serverless Patterns](03-Serverless-Patterns.md)


## References & Learn More

- [Awesome CDK](https://github.com/kolomied/awesome-cdk)
- [AWS CDK](https://aws.amazon.com/cdk/)
- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)
- [CDK Patterns](https://cdkpatterns.com/)
- [Serverless Framework](https://www.serverless.com/)
- [SST (Serverless Stack)](https://sst.dev/)
