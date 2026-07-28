---
section: CI/CD
category: DevOps
tags: [concept]
---

# GitLab CI/CD

## Definition

**GitLab CI/CD** is GitLab's built-in continuous integration and continuous delivery platform. Pipelines are defined in a `.gitlab-ci.yml` file in the repository root. It features auto-scaling runners, container registry, built-in container scanning, and integrated deployment environments with review apps.

## Why Do We Need It?

1. **Single platform**: SCM, CI/CD, registry, and monitoring in one tool
2. **Auto DevOps**: Automated pipeline setup for common stacks
3. **Review Apps**: Auto-deploy feature branches as ephemeral environments
4. **Built-in security**: SAST, DAST, container scanning, dependency scanning
5. **Scale**: Auto-scaling runners for parallel job execution

## Code Examples

### Basic Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy

variables:
  NODE_VERSION: "20-alpine"
  DOCKER_DRIVER: overlay2

cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/

before_script:
  - node --version
  - npm --version

build:
  stage: build
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour

lint:
  stage: test
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run lint
  needs: []

unit-test:
  stage: test
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run test:unit
  coverage: '/Statements\s+:\s([\d.]+)%/'
  artifacts:
    reports:
      junit: reports/junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

integration-test:
  stage: test
  image: node:${NODE_VERSION}
  services:
    - postgres:15-alpine
    - redis:7-alpine
  variables:
    DATABASE_URL: "postgres://postgres:password@postgres:5432/test"
  script:
    - npm ci
    - npm run test:integration

deploy-dev:
  stage: deploy
  image: alpine:latest
  script:
    - apk add --no-cache curl
    - curl -X POST ${DEPLOY_WEBHOOK}
  environment:
    name: development
  only:
    - main

deploy-production:
  stage: deploy
  image: alpine:latest
  script:
    - apk add --no-cache kubectl
    - kubectl set image deployment/my-app app=${CI_REGISTRY_IMAGE}:${CI_COMMIT_SHORT_SHA}
  environment:
    name: production
    url: https://example.com
  when: manual
  only:
    - tags
```

### Multi-Project Pipeline

```yaml
# Trigger downstream pipeline
trigger-frontend:
  stage: deploy
  trigger:
    project: myorg/frontend
    branch: main
    strategy: depend

# Multi-project pipeline with artifacts
deploy:
  stage: deploy
  variables:
    UPSTREAM_COMMIT: ${CI_COMMIT_SHA}
  trigger:
    project: myorg/deployment
    branch: main
    strategy: depend
```

### Docker & Registry

```yaml
docker-build:
  stage: build
  image: docker:20
  services:
    - docker:20-dind
  variables:
    DOCKER_HOST: tcp://docker:2375
    DOCKER_TLS_CERTDIR: ""
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
  only:
    - main
```

## Best Practices

1. **Use `needs`** to run jobs in parallel and reduce pipeline time
2. **Cache dependencies** between runs (node_modules, gems)
3. **Use `rules`** instead of deprecated `only`/`except`
4. **Include templates** for reusable pipeline configuration
5. **Set job timeouts** to prevent runaway pipelines
6. **Use GitLab Container Registry** for storing Docker images
7. **Implement protected environments** for production deployments

---

### See Also

- [ArgoCD](../06-ArgoCD.md)
- [Docker Build & Deploy](../02-Docker-Build-Deploy.md)
- [GitHub Actions](../01-GitHub-Actions.md)
- [Jenkins](../04-Jenkins.md)

### References

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [GitLab CI YAML Reference](https://docs.gitlab.com/ee/ci/yaml/)
- [GitLab Runners](https://docs.gitlab.com/runner/)
- [GitLab Auto DevOps](https://docs.gitlab.com/ee/topics/autodevops/)
