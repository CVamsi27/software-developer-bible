# GitHub Actions

## Definition

**GitHub Actions** is a CI/CD platform built into GitHub that automates software workflows. It uses YAML-based **workflows** triggered by events (push, PR, schedule) to execute **jobs** containing **steps** (commands or actions).

Key concepts:
- **Workflow**: Automated process defined in `.github/workflows/`
- **Job**: Group of steps running on the same runner
- **Step**: Individual task (action or shell command)
- **Runner**: Server that executes jobs (GitHub-hosted or self-hosted)
- **Action**: Reusable units of code (marketplace or custom)
- **Secret**: Encrypted environment variables

## Why Do We Need It?

| Problem | Solution |
|---|---|
| Manual CI/CD setup | Built-in GitHub integration |
| External CI/CD services | No external dependencies |
| Complex pipeline config | YAML-based workflows |
| No built-in secrets | Encrypted secrets management |
| No marketplace | Pre-built actions for common tasks |
| No matrix testing | Test across multiple configurations |

## How It Works

### Architecture

```
+----------------------------------------------------------+
|                    GitHub Actions                         |
|                                                           |
|  +------------------+    +------------------+            |
|  |    Repository     |    |    Marketplace   |            |
|  |  .github/workflows|    |  Pre-built actions|           |
|  +--------+---------+    +--------+---------+            |
|           |                      |                        |
|           +----------+-----------+                        |
|                      |                                    |
|                      v                                    |
|  +--------------------------------------------------+   |
|  |                   Workflow                        |   |
|  |  +--------------------------------------------+  |   |
|  |  |              Job: build                     |  |   |
|  |  |  Step 1: Checkout code                     |  |   |
|  |  |  Step 2: Setup Node.js                     |  |   |
|  |  |  Step 3: Install dependencies              |  |   |
|  |  |  Step 4: Run tests                         |  |   |
|  |  +--------------------------------------------+  |   |
|  |  +--------------------------------------------+  |   |
|  |  |              Job: deploy                    |  |   |
|  |  |  Step 1: Build Docker image                |  |   |
|  |  |  Step 2: Push to registry                  |  |   |
|  |  |  Step 3: Deploy to Kubernetes              |  |   |
|  |  +--------------------------------------------+  |   |
|  +--------------------------------------------------+   |
+----------------------------------------------------------+
                          |
                          v
              +-----------------------+
              |     Runner (VM)       |
              |  Ubuntu / Windows     |
              |  / macOS              |
              +-----------------------+
```

### Workflow File Structure

```
.github/
+-- workflows/
|   +-- ci.yml
|   +-- cd.yml
|   +-- release.yml
+-- actions/
|   +-- setup/
|       +-- action.yml
```

## Code Examples

### Basic Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build
```

### Matrix Builds

```yaml
name: Matrix CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [16, 18, 20]

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm ci
      - run: npm test
```

### Docker Build and Push

```yaml
name: Docker Build

on:
  push:
    tags:
      - 'v*'

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: myapp:${{ github.ref_name }}
```

### Deploy to Kubernetes

```yaml
name: Deploy to K8s

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Update kubeconfig
        run: aws eks update-kubeconfig --name my-cluster

      - name: Deploy
        run: |
          kubectl set image deployment/myapp myapp=myapp:${{ github.sha }}
          kubectl rollout status deployment/myapp
```

### Reusable Workflow

```yaml
# .github/workflows/reusable-ci.yml
name: Reusable CI

on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string
    secrets:
      NPM_TOKEN:
        required: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci
      - run: npm test
```

### Custom Action

```yaml
# .github/actions/setup-app/action.yml
name: 'Setup Application'
description: 'Setup Node.js and install dependencies'
inputs:
  node-version:
    description: 'Node.js version'
    default: '18'
runs:
  using: 'composite'
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: 'npm'
    - run: npm ci
      shell: bash
```

### Secrets Management

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Use secret
        run: echo "Deploying with ${{ secrets.DEPLOY_KEY }}"
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### Caching

```yaml
steps:
  - uses: actions/cache@v4
    with:
      path: ~/.npm
      key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
      restore-keys: |
        ${{ runner.os }}-node-
```

## Real-World Use Cases

### 1. Complete CI/CD Pipeline

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run lint

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test
      - uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage/

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker tag myapp:${{ github.sha }} myapp:latest
          docker push myapp:${{ github.sha }}
          docker push myapp:latest

  deploy-staging:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to staging
        run: |
          kubectl set image deployment/myapp myapp=myapp:${{ github.sha }} -n staging
          kubectl rollout status deployment/myapp -n staging

  deploy-production:
    runs-on: ubuntu-latest
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        run: |
          kubectl set image deployment/myapp myapp=myapp:${{ github.sha }} -n production
          kubectl rollout status deployment/myapp -n production
```

### 2. Release Workflow

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate changelog
        id: changelog
        run: |
          CHANGELOG=$(git log --pretty=format:"- %s" $(git describe --tags --abbrev=0)..HEAD)
          echo "changelog<<EOF" >> $GITHUB_OUTPUT
          echo "$CHANGELOG" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Create GitHub Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          body: ${{ steps.changelog.outputs.changelog }}
```

### 3. Security Scanning

```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:latest'
          format: 'table'
          exit-code: '1'
          severity: 'CRITICAL,HIGH'
```

## Common Mistakes

| Mistake | Fix |
|---|---|
| Hardcoding secrets | Use GitHub Secrets |
| No caching | Cache dependencies |
| No matrix testing | Test across environments |
| Blocking PRs on flaky tests | Use required checks carefully |
| No reusable workflows | Create reusable workflows |
| Ignoring runner costs | Use self-hosted runners for large workloads |

## Best Practices

```yaml
# GOOD: Production workflow
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read
  packages: write

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: build-artifacts
          path: dist/
```

1. **Use specific action versions** — `actions/checkout@v4`, not `@main`
2. **Cache dependencies** — speed up builds
3. **Use matrix builds** — test across environments
4. **Use reusable workflows** — reduce duplication
5. **Use environments** — protect deployments
6. **Use secrets** — never hardcode credentials
7. **Use permissions** — follow least privilege
8. **Use concurrency groups** — prevent redundant runs
9. **Use status badges** — track workflow status
10. **Monitor costs** — use self-hosted runners when needed

## Performance Considerations

| Factor | Impact | Mitigation |
|---|---|---|
| Workflow file size | Parse time | Keep workflows focused |
| Runner selection | Build speed | Use appropriate runner |
| Caching | Build time | Cache dependencies |
| Parallel jobs | Total time | Run independent jobs in parallel |
| Artifact size | Upload/download time | Minimize artifacts |
| Marketplace actions | Security | Pin to specific versions |

```bash
# View workflow runs
gh run list

# View workflow run details
gh run view <run-id>

# Cancel a run
gh run cancel <run-id>

# Re-run a workflow
gh run rerun <run-id>
```

## Interview Questions

### Beginner (5-10)

1. **What is GitHub Actions?**
   A CI/CD platform built into GitHub for automating software workflows.

2. **What is a workflow?**
   An automated process defined in `.github/workflows/`.

3. **What is a job?**
   A group of steps running on the same runner.

4. **What is a step?**
   An individual task (action or shell command).

5. **What is a runner?**
   A server that executes jobs (GitHub-hosted or self-hosted).

6. **What is an action?**
   A reusable unit of code from the marketplace or custom.

7. **How do you trigger a workflow?**
   Via events (push, PR, schedule, manual).

8. **What is the `uses` keyword?**
   Specifies an action to use in a step.

9. **How do you access secrets?**
   `${{ secrets.SECRET_NAME }}`

10. **What is the default workflow directory?**
    `.github/workflows/`

### Intermediate (5-10)

11. **What is matrix strategy?**
    Run jobs across multiple configurations (OS, versions).

12. **What is a reusable workflow?**
    A workflow called from another workflow via `workflow_call`.

13. **What are artifacts?**
    Files produced by a workflow, downloadable or passed between jobs.

14. **What are environments?**
    Deployment targets with protection rules and secrets.

15. **What is concurrency?**
    Prevents multiple workflow runs from running simultaneously.

16. **What is the `needs` keyword?**
    Defines job dependencies.

17. **What is the `if` keyword?**
    Conditional execution of jobs or steps.

18. **How do you cache dependencies?**
    Use `actions/cache` or built-in caching in setup actions.

19. **What is the `outputs` keyword?**
    Pass data between jobs or workflows.

20. **What is the `workflow_dispatch` event?**
    Manual workflow trigger from the GitHub UI.

### Senior (10-15)

21. **How would you design a CI/CD pipeline for a monorepo?**
    Use path filters, reusable workflows, and matrix builds per service.

22. **How do you handle secrets in GitHub Actions?**
    Use GitHub Secrets, environment secrets, and OIDC for cloud providers.

23. **What is OIDC in GitHub Actions?**
    OpenID Connect for passwordless authentication with cloud providers.

24. **How do you optimize GitHub Actions workflows?**
    Cache dependencies, parallelize jobs, and use matrix builds.

25. **How do you handle deployment approvals?**
    Use environment protection rules with required reviewers.

### FAANG-style (5-10)

26. **Design a CI/CD pipeline for 100+ microservices.**
    Use path-based triggers, reusable workflows, and matrix builds. Implement caching and parallelization.

27. **How would you handle GitHub Actions costs?**
    Use self-hosted runners, optimize workflow duration, and implement caching.

28. **Design a security scanning pipeline.**
    Integrate Trivy, Snyk, and CodeQL. Block PRs on critical vulnerabilities.

29. **How would you implement GitOps with GitHub Actions?**
    Use Argo CD or Flux with GitHub Actions for image updates.

30. **Design a multi-environment deployment pipeline.**
    Use environments with protection rules, manual approvals, and rollback strategies.

### Follow-ups (5-10)

31. **What is the difference between `runs-on: ubuntu-latest` and self-hosted?**
    GitHub-hosted: managed by GitHub. Self-hosted: your own infrastructure.

32. **How do you handle workflow file syntax errors?**
    Use `actionlint` or GitHub's workflow validation.

33. **What is the `GITHUB_TOKEN`?**
    A default token for authentication with GitHub API.

34. **How do you debug workflow failures?**
    Enable debug logging, use `tmate` action, and check workflow logs.

35. **What is the difference between `push` and `pull_request` events?**
    `push`: code pushed to branch. `pull_request`: PR opened/updated.

## Summary

GitHub Actions provides a powerful, integrated CI/CD platform. Workflows are defined in YAML, triggered by events, and executed on runners. Key features include matrix builds, caching, secrets management, and reusable workflows.

## Cheat Sheet

```bash
# Workflow file location
.github/workflows/ci.yml

# Key syntax
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test

# Secrets
${{ secrets.MY_SECRET }}

# Matrix
strategy:
  matrix:
    node: [16, 18, 20]

# Artifacts
- uses: actions/upload-artifact@v4
  with:
    name: build
    path: dist/

# Reusable workflow
on:
  workflow_call:
```

---

## References & Learn More
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [CI/CD Pipeline Design Patterns](https://martinfowler.com/articles/continuousIntegration.html)
- [The Phoenix Project](https://www.amazon.com/Phoenix-Project-DevOps-Helping-Business/dp/0991538429)
