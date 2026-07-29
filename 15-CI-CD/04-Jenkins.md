# Jenkins CI/CD

[![Category: DevOps](https://img.shields.io/badge/category-DevOps-ff7f00)](.)

## Definition

**Jenkins** is an open-source automation server for building, testing, and deploying software. It supports declarative and scripted pipelines, distributed builds, extensive plugin ecosystem, and integration with virtually all DevOps tools. Jenkins pipelines are defined in a `Jenkinsfile` using Groovy-based DSL.

## Why Do We Need It?

1. **Pipeline as Code**: Define entire CI/CD pipeline in version-controlled `Jenkinsfile`
2. **Extensibility**: 1,800+ plugins for every tool in the DevOps ecosystem
3. **Distributed builds**: Master/agent architecture for scaling build capacity
4. **Mature ecosystem**: Battle-tested in enterprise environments for decades
5. **Flexibility**: Support for any SCM, build tool, or deployment target

## Code Examples

### Declarative Pipeline

```groovy
// Jenkinsfile (Declarative Pipeline)
pipeline {
    agent any

    parameters {
        choice(name: 'ENV', choices: ['dev', 'staging', 'prod'], description: 'Deploy environment')
        string(name: 'VERSION', defaultValue: '1.0.0', description: 'Release version')
    }

    environment {
        DOCKER_REGISTRY = 'registry.example.com'
        APP_NAME = 'my-app'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'npm ci'
            }
        }

        stage('Lint') {
            steps {
                sh 'npm run lint'
            }
        }

        stage('Test') {
            steps {
                sh 'npm run test:ci'
            }
            post {
                always {
                    junit 'reports/**/*.xml'
                }
            }
        }

        stage('Build') {
            steps {
                sh 'npm run build'
            }
        }

        stage('Docker Build & Push') {
            when {
                branch 'main'
            }
            steps {
                sh """
                    docker build -t ${DOCKER_REGISTRY}/${APP_NAME}:${VERSION} .
                    docker push ${DOCKER_REGISTRY}/${APP_NAME}:${VERSION}
                """
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
                    if (params.ENV == 'prod') {
                        input message: 'Deploy to production?', ok: 'Deploy'
                    }
                }
                sh "kubectl set image deployment/${APP_NAME} app=${DOCKER_REGISTRY}/${APP_NAME}:${VERSION}"
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        failure {
            slackSend(
                channel: '#deployments',
                message: "Build failed: ${env.BUILD_URL}"
            )
        }
        success {
            slackSend(
                channel: '#deployments',
                message: "Build succeeded: ${env.BUILD_URL}"
            )
        }
    }
}
```

### Scripted Pipeline

```groovy
// Jenkinsfile (Scripted Pipeline)
node('linux') {
    stage('Checkout') {
        checkout scm
    }

    stage('Build') {
        docker.image('node:20-alpine').inside {
            sh 'npm ci'
            sh 'npm run build'
        }
    }

    stage('Test') {
        parallel(
            unit: {
                sh 'npm run test:unit'
            },
            integration: {
                sh 'npm run test:integration'
            }
        )
    }

    stage('Deploy') {
        if (env.BRANCH_NAME == 'main') {
            build job: 'deploy-to-prod', parameters: [
                string(name: 'BUILD_TAG', value: env.BUILD_TAG)
            ]
        }
    }
}
```

### Shared Library

```groovy
// vars/buildNodeApp.groovy
def call(Map config = [:]) {
    pipeline {
        agent any
        environment {
            NODE_VERSION = config.nodeVersion ?: '20'
        }
        stages {
            stage('Setup') {
                steps {
                    sh "node --version"
                    sh "npm ci"
                }
            }
            stage('Quality') {
                parallel {
                    stage('Lint') {
                        steps { sh 'npm run lint' }
                    }
                    stage('Test') {
                        steps {
                            sh 'npm run test:ci'
                            junit 'reports/**/*.xml'
                        }
                    }
                }
            }
            stage('Build') {
                steps { sh 'npm run build' }
            }
        }
    }
}

// Jenkinsfile using shared library
@Library('my-shared-library') _

buildNodeApp(nodeVersion: '20')
```

## Best Practices

1. **Use Declarative Pipeline** over Scripted for readability
2. **Store credentials** in Jenkins Credentials Store, never in code
3. **Use Shared Libraries** for reusable pipeline code
4. **Clean workspace** in `post { always { cleanWs() } }` block
5. **Parallelize stages** for faster feedback
6. **Use when conditions** to skip unnecessary stages
7. **Implement approval gates** for production deployments

## Summary

- Jenkins is a self-hosted automation server for building, testing, and deploying software
- Pipeline as Code (Jenkinsfile) defines CI/CD workflows using Declarative or Scripted pipeline syntax
- Master-agent architecture distributes build workloads across multiple worker nodes
- Extensive plugin ecosystem integrates with SCM, build tools, test frameworks, and cloud providers
- Blue Ocean provides a modern UI for pipeline visualization and monitoring

---

## Cheat Sheet
```text
JENKINS CI/CD CHEAT SHEET
============================================================

INTERVIEW TIPS:
  - Understand the core concepts and trade-offs
  - Be ready to explain with real-world examples
  - Discuss performance implications and best practices
  - Show awareness of common pitfalls

```
## See Also
- [ArgoCD](06-ArgoCD.md)
- [Docker](../13-Docker/)

## References & Learn More

- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Jenkins Best Practices](https://www.jenkins.io/doc/book/pipeline/best-practices/)
