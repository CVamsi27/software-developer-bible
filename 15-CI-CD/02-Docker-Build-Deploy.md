# Docker Build & Deploy Pipeline

## Definition

A **Docker build pipeline** automates the process of building, testing, and deploying Docker images. It includes image building, registry storage, versioning, and deployment strategies. The pipeline ensures consistent, reproducible deployments across environments.

Key concepts:
- **Build Pipeline**: Automated build, test, and deploy workflow
- **Container Registry**: Storage for Docker images (Docker Hub, ECR, GCR)
- **Image Tagging**: Version identification for images
- **Deployment Strategy**: How updates are applied (rolling, blue-green, canary)
- **Image Scanning**: Vulnerability detection in images

## Why Do We Need It?

| Problem | Solution |
|---|---|
| Manual image builds | Automated CI/CD pipelines |
| Inconsistent deployments | Reproducible image builds |
| No version control | Semantic versioning and tags |
| Security vulnerabilities | Automated image scanning |
| No rollback capability | Immutable image versions |
| Environment drift | Same image across environments |

## How It Works

### Pipeline Architecture

```
+----------------------------------------------------------+
|                  Docker Build Pipeline                     |
|                                                           |
|  +------------------+    +------------------+            |
|  |   Source Code     |    |   Dockerfile     |            |
|  |   (Git push)      |    |   (Build spec)   |            |
|  +--------+---------+    +--------+---------+            |
|           |                      |                        |
|           +----------+-----------+                        |
|                      |                                    |
|                      v                                    |
|  +--------------------------------------------------+   |
|  |              CI/CD Pipeline                       |   |
|  |  1. Build Docker image                           |   |
|  |  2. Run tests in container                       |   |
|  |  3. Scan image for vulnerabilities               |   |
|  |  4. Push to registry                             |   |
|  |  5. Deploy to staging                            |   |
|  |  6. Run integration tests                        |   |
|  |  7. Deploy to production                         |   |
|  +--------------------------------------------------+   |
|                      |                                    |
|                      v                                    |
|  +--------------------------------------------------+   |
|  |              Container Registry                    |   |
|  |  myapp:1.0.0, myapp:1.0.1, myapp:latest         |   |
|  +--------------------------------------------------+   |
+----------------------------------------------------------+
                          |
                          v
              +-----------------------+
              |    Kubernetes/VMs     |
              |    (Deployment)       |
              +-----------------------+
```

### Image Tagging Strategy

```
Git Tags:              Docker Tags:              Registry:
v1.0.0        --->     myapp:1.0.0       --->  myapp:1.0.0
v1.0.1        --->     myapp:1.0.1       --->  myapp:1.0.1
main          --->     myapp:latest      --->  myapp:latest
abc1234       --->     myapp:abc1234     --->  myapp:abc1234
```

## Code Examples

### GitHub Actions Docker Pipeline

```yaml
name: Docker Build & Deploy

on:
  push:
    branches: [main]
    tags: ['v*']

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=semver,pattern={{version}}
            type=sha,prefix=

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}

      - name: Scan image
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: 'table'
          exit-code: '1'
          severity: 'CRITICAL,HIGH'
```

### AWS ECR Pipeline

```yaml
name: Deploy to ECR

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

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build, tag, and push image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: myapp
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:latest .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest

      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster my-cluster \
            --service my-service \
            --force-new-deployment
```

### Multi-Stage Build Pipeline

```yaml
name: Multi-Stage Build

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build builder stage
        run: docker build --target builder -t myapp:builder .

      - name: Run tests in builder
        run: docker run myapp:builder npm test

      - name: Build production image
        run: docker build --target production -t myapp:latest .

      - name: Push to registry
        run: |
          docker tag myapp:latest registry.example.com/myapp:${{ github.sha }}
          docker push registry.example.com/myapp:${{ github.sha }}
```

### Deployment to Kubernetes

```yaml
name: Deploy to Kubernetes

on:
  push:
    tags: ['v*']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build and push image
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: myapp:${{ github.ref_name }}

      - name: Deploy to staging
        run: |
          kubectl set image deployment/myapp \
            myapp=myapp:${{ github.ref_name }} \
            -n staging
          kubectl rollout status deployment/myapp -n staging

      - name: Run integration tests
        run: npm run test:integration

      - name: Deploy to production
        run: |
          kubectl set image deployment/myapp \
            myapp=myapp:${{ github.ref_name }} \
            -n production
          kubectl rollout status deployment/myapp -n production
```

### Docker Compose Pipeline

```yaml
name: Docker Compose Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build and deploy
        run: |
          docker compose build
          docker compose up -d

      - name: Health check
        run: |
          sleep 30
          curl -f http://localhost:3000/health
```

## Real-World Use Cases

### 1. Complete CI/CD with Image Scanning

```yaml
name: Full Pipeline

on: [push, pull_request]

jobs:
  build-test-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t myapp:test .

      - name: Run tests
        run: docker run myapp:test npm test

      - name: Scan with Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:test
          severity: CRITICAL,HIGH
          exit-code: 1

  push:
    needs: build-test-scan
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Push to registry
        run: |
          docker build -t registry.example.com/myapp:${{ github.sha }} .
          docker push registry.example.com/myapp:${{ github.sha }}
          docker tag registry.example.com/myapp:${{ github.sha }} registry.example.com/myapp:latest
          docker push registry.example.com/myapp:latest
```

### 2. Multi-Environment Deployment

```yaml
name: Multi-Environment Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to staging
        run: ./deploy.sh staging

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        run: ./deploy.sh production
```

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using `latest` tag | Use SHA or semantic version |
| No image scanning | Integrate Trivy/Clair |
| No caching | Cache Docker layers |
| No health checks | Add health check endpoints |
| Hardcoding tags | Use dynamic tagging |
| No rollback strategy | Implement automated rollback |
| Not using multi-stage builds | Separate build and production stages |

## Best Practices

```yaml
# GOOD: Production pipeline
name: Production Deploy

on:
  push:
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: |
            myapp:${{ github.ref_name }}
            myapp:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Scan image
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          severity: CRITICAL
          exit-code: 1
```

1. **Use semantic versioning** — tag images with version numbers
2. **Never use `latest` in production** — use specific tags
3. **Scan images for vulnerabilities** — block critical CVEs
4. **Use multi-stage builds** — minimize image size
5. **Cache Docker layers** — speed up builds
6. **Use health checks** — verify deployment success
7. **Implement rollback** — automated rollback on failure
8. **Use image signing** — verify image integrity
9. **Monitor image size** — prevent bloat
10. **Use registry replication** — distribute images globally

## Performance Considerations

| Factor | Impact | Mitigation |
|---|---|---|
| Build context size | Build time | `.dockerignore`, minimize context |
| Layer count | Build time | Combine layers, use BuildKit |
| Registry location | Pull time | Use regional registries |
| Image size | Pull/deploy time | Multi-stage builds, Alpine |
| Caching strategy | Build speed | Layer caching, BuildKit cache |

```bash
# Optimize build
DOCKER_BUILDKIT=1 docker build --cache-from type=registry,ref=myapp:cache -t myapp .

# Check image size
docker images myapp

# Scan image
trivy image myapp:latest

# Push with multiple tags
docker tag myapp:latest myapp:1.0.0
docker push myapp:1.0.0
docker push myapp:latest
```

## Interview Questions

### Beginner (5-10)

1. **What is a Docker build pipeline?**
   Automated workflow for building, testing, and deploying Docker images.

2. **What is a container registry?**
   Storage system for Docker images (Docker Hub, ECR, GCR).

3. **What is image tagging?**
   Version identification for Docker images (e.g., `myapp:1.0.0`).

4. **Why not use `latest` tag in production?**
   It's ambiguous and can lead to unexpected deployments.

5. **What is image scanning?**
   Analyzing images for security vulnerabilities.

6. **What is a multi-stage build?**
   Using multiple `FROM` statements to build and production in separate stages.

7. **How do you push an image to a registry?**
   `docker push registry.example.com/myapp:tag`

8. **What is layer caching?**
   Reusing unchanged Docker layers to speed up builds.

9. **What is a health check?**
   An endpoint to verify container health.

10. **What is a rollback?**
    Reverting to a previous version after a failed deployment.

### Intermediate (5-10)

11. **How do you implement CI/CD for Docker?**
    Use GitHub Actions, GitLab CI, or Jenkins to build, test, and deploy images.

12. **What is the difference between `docker build` and `docker compose build`?**
    `docker build` builds a single image. `docker compose build` builds multiple services.

13. **How do you handle secrets in Docker builds?**
    Use BuildKit secret mounts or external secret management.

14. **What is image signing?**
    Cryptographic signing to verify image integrity and source.

15. **How do you implement blue-green deployment with Docker?**
    Run two environments and switch traffic between them.

16. **What is a canary deployment?**
    Gradually rolling out changes to a small subset of users.

17. **How do you handle database migrations in Docker?**
    Run migrations as init containers or separate jobs.

18. **What is the difference between `docker pull` and `docker push`?**
    `pull` downloads images. `push` uploads images.

19. **How do you optimize Docker build speed?**
    Use BuildKit, cache layers, and minimize build context.

20. **What is a Dockerfile best practice?**
    Use multi-stage builds, pin versions, and run as non-root.

### Senior (10-15)

21. **Design a Docker build pipeline for a microservices architecture.**
    Use path-based triggers, matrix builds, and shared base images. Implement caching and scanning.

22. **How would you handle image promotion across environments?**
    Use registry tags, image scanning gates, and automated promotion.

23. **What is the difference between rolling, blue-green, and canary deployments?**
    Rolling: gradual replacement. Blue-green: two environments. Canary: small subset.

24. **How do you implement zero-downtime deployments with Docker?**
    Use health checks, readiness probes, and graceful shutdown.

25. **Design a disaster recovery strategy for Docker images.**
    Use registry replication, image backup, and cross-region distribution.

### FAANG-style (5-10)

26. **Design a Docker build pipeline for 100+ microservices.**
    Use shared base images, BuildKit cache, and matrix builds. Implement automated scanning and promotion.

27. **How would you optimize Docker build times from 30 minutes to under 5?**
    BuildKit parallel builds, cache mounts, minimal context, and remote cache.

28. **Design a multi-region Docker deployment strategy.**
    Use regional registries, edge caching, and automated failover.

29. **How would you implement image governance?**
    Use image signing, vulnerability scanning, and compliance policies.

30. **Describe a Docker image management strategy.**
    Implement lifecycle policies, automated cleanup, and retention rules.

### Follow-ups (5-10)

31. **What is the difference between `docker save` and `docker export`?**
    `save` preserves layers and metadata. `export` flattens to a tarball.

32. **How do you handle Docker image cleanup?**
    Use `docker system prune` and implement registry retention policies.

33. **What is the difference between a Docker image and a Docker container?**
    Image: read-only template. Container: running instance.

34. **How do you handle Docker image versioning?**
    Use semantic versioning, Git SHA, and build numbers.

35. **What is the impact of image size on deployment?**
    Larger images take longer to pull and deploy.

## Summary

A Docker build pipeline automates image creation, testing, and deployment. Key components include CI/CD workflows, container registries, image tagging, and deployment strategies. Proper implementation ensures consistent, secure, and efficient deployments.

## Cheat Sheet

```bash
# Build
docker build -t myapp:1.0.0 .
docker build --no-cache -t myapp:1.0.0 .

# Tag
docker tag myapp:1.0.0 registry.example.com/myapp:1.0.0

# Push
docker push registry.example.com/myapp:1.0.0

# Pull
docker pull registry.example.com/myapp:1.0.0

# Scan
trivy image myapp:1.0.0

# Compose
docker compose build
docker compose up -d
docker compose down
```

---

## References & Learn More
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [CI/CD Pipeline Design Patterns](https://martinfowler.com/articles/continuousIntegration.html)
- [The Phoenix Project](https://www.amazon.com/Phoenix-Project-DevOps-Helping-Business/dp/0991538429)
