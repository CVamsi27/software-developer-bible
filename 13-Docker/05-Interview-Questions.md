# Docker Interview Questions

## 30 Most Asked Docker Interview Questions with Detailed Answers

---

### Question 1: What is Docker and how does it differ from a virtual machine?

**Answer:**

Docker is a containerization platform that packages applications with their dependencies into lightweight, portable containers. Containers share the host OS kernel, unlike VMs which each run a full guest OS.

**Key Differences:**

| Aspect | Docker Container | Virtual Machine |
|---|---|---|
| OS | Shares host kernel | Full guest OS |
| Size | MBs | GBs |
| Startup | Seconds | Minutes |
| Isolation | Process-level | Hardware-level |
| Performance | Near-native | Hypervisor overhead |
| Density | 100s per host | 10s per host |

**Architecture:**

```
VM Architecture:
+------------------+  +------------------+
|     App B        |  |     App A        |
|     Bins/Libs    |  |     Bins/Libs    |
|     Guest OS     |  |     Guest OS     |
+------------------+  +------------------+
|        Hypervisor                   |
+-------------------------------------+
|        Host OS                      |
+-------------------------------------+
|        Hardware                     |
+-------------------------------------+

Docker Architecture:
+------------------+  +------------------+
|     App B        |  |     App A        |
|     Bins/Libs    |  |     Bins/Libs    |
+------------------+  +------------------+
|     Docker Engine (Shared Kernel)    |
+-------------------------------------+
|        Host OS                      |
+-------------------------------------+
|        Hardware                     |
+-------------------------------------+
```

---

### Question 2: What is a Docker image and how is it structured?

**Answer:**

A Docker image is a read-only template with instructions for creating a container. It uses a union filesystem with layers, each representing a Dockerfile instruction.

**Layer Structure:**

```
+-------------------------------+
| Layer N: CMD ["app"]          |  <-- ~0 bytes (metadata)
+-------------------------------+
| Layer N-1: COPY dist/         |  <-- varies
+-------------------------------+
| Layer N-2: RUN npm ci         |  <-- ~150 MB
+-------------------------------+
| Layer N-3: COPY package.json  |  <-- ~0.05 MB
+-------------------------------+
| Layer N-4: WORKDIR /app       |  <-- ~0 bytes
+-------------------------------+
| Layer 0: node:18-alpine       |  <-- ~130 MB
+-------------------------------+
```

Each layer is content-addressable (SHA256 hash). Layers are cached and shared across images.

---

### Question 3: What is the difference between COPY and ADD in Dockerfile?

**Answer:**

| Feature | COPY | ADD |
|---|---|---|
| Basic copy | Yes | Yes |
| URL download | No | Yes |
| Auto-extract tar | No | Yes |
| Control | Predictable | Less predictable |

**Best Practice:** Use `COPY` unless you specifically need tar extraction or URL downloading. `COPY` is explicit and easier to understand.

```dockerfile
# Preferred
COPY package*.json ./
COPY dist/ ./dist/

# Only use ADD when needed
ADD archive.tar.gz /app/
ADD https://example.com/file.txt /app/
```

---

### Question 4: Explain Docker layer caching and how to optimize it.

**Answer:**

Docker caches each layer. If a layer and its context haven't changed, Docker reuses the cached version. Only changed layers rebuild.

**Optimization Strategy:**

```dockerfile
# BAD: Changes to source code invalidate dependency cache
COPY . .
RUN npm ci

# GOOD: Dependencies cached separately
COPY package*.json ./
RUN npm ci
COPY . .
```

**Cache Hierarchy (least to most changeable):**
1. Base image (rarely changes)
2. System dependencies (occasionally)
3. Application dependencies (weekly)
4. Application code (daily)

---

### Question 5: What is a multi-stage build and why use it?

**Answer:**

Multi-stage builds use multiple `FROM` statements to build in stages. Only artifacts from later stages are included in the final image.

**Benefits:**
- Smaller production images (no build tools)
- Better security (no compilers/shells)
- Faster CI/CD (smaller images)
- Single Dockerfile for dev/prod

```dockerfile
FROM node:18 AS builder
WORKDIR /app
COPY . .
RUN npm ci && npm run build

FROM node:18-alpine
COPY --from=builder /app/dist ./dist
USER node
CMD ["node", "dist/server.js"]
```

---

### Question 6: How do you handle secrets in Docker?

**Answer:**

Never hardcode secrets in Dockerfiles or images.

**Methods:**

```bash
# 1. Environment variables (runtime only)
docker run -e DB_PASSWORD=secret myapp

# 2. Docker secrets (Swarm mode)
docker secret create db_pass password.txt

# 3. BuildKit secrets (build time)
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci

# 4. External secrets (Vault, AWS SSM)
# Use entrypoint scripts to fetch secrets
```

**Never:**
```dockerfile
# BAD: Secrets baked into image
ENV API_KEY=sk_live_abc123
COPY secrets.json /app/
```

---

### Question 7: What is Docker Compose and when would you use it?

**Answer:**

Docker Compose is a tool for defining and running multi-container applications using YAML configuration.

**Use Cases:**
- Local development environments
- Multi-service applications
- Integration testing
- CI/CD pipelines

```yaml
version: "3.9"
services:
  app:
    build: .
    ports: ["3000:3000"]
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15
    volumes: ["pg_data:/var/lib/postgresql/data"]
    healthcheck:
      test: ["CMD", "pg_isready"]

volumes:
  pg_data:
```

---

### Question 8: What are Docker networks and their types?

**Answer:**

Docker networks enable container-to-container communication.

| Network | Description | Use Case |
|---|---|---|
| bridge | Default, single host | Most common |
| host | Shares host network | Performance-critical |
| overlay | Multi-host (Swarm) | Clusters |
| macvlan | Assigns MAC address | Legacy apps |
| none | No networking | Isolated workloads |

```bash
# Create custom bridge network
docker network create --driver bridge mynet

# Run containers on network
docker run --network mynet --name api myapp
docker run --network mynet --name db postgres

# Containers communicate via name
# Inside api: curl http://db:5432
```

---

### Question 9: How do you reduce Docker image size?

**Answer:**

| Technique | Impact |
|---|---|
| Use Alpine base | ~130MB vs ~900MB |
| Multi-stage builds | Remove build tools |
| .dockerignore | Exclude unnecessary files |
| npm ci --only=production | No devDependencies |
| Combine RUN commands | Fewer layers |
| Use distroless | Minimal runtime |
| Remove caches | Clean npm/pip cache |

**Example:**

```dockerfile
# ~900MB
FROM node:18
COPY . .
RUN npm install

# ~150MB
FROM node:18-alpine
COPY package*.json ./
RUN npm ci --only=production
COPY dist/ ./dist
USER node
```

---

### Question 10: What is the difference between CMD and ENTRYPOINT?

**Answer:**

| Aspect | CMD | ENTRYPOINT |
|---|---|---|
| Purpose | Default arguments | Main executable |
| Override | `docker run myapp arg` | `docker run myapp --entrypoint` |
| Multiple | Last one wins | Can be combined with CMD |

```dockerfile
# ENTRYPOINT defines the executable
ENTRYPOINT ["node"]

# CMD provides default arguments
CMD ["server.js"]

# Result: node server.js
# Override args: docker run myapp app.js  -->  node app.js
```

---

### Question 11: Explain Docker volume types.

**Answer:**

| Type | Description | Persistence |
|---|---|---|
| Named volume | Docker-managed | Yes |
| Bind mount | Host path mapping | Yes |
| tmpfs | Memory only | No |

```bash
# Named volume
docker run -v mydata:/data myapp

# Bind mount
docker run -v /host/path:/container/path myapp

# tmpfs
docker run --tmpfs /tmp:rw,size=100m myapp

# Read-only
docker run -v /data:/app/data:ro myapp
```

---

### Question 12: How do you debug a container that keeps crashing?

**Answer:**

```bash
# 1. Check logs
docker logs <container>
docker logs --tail 100 <container>

# 2. Inspect container
docker inspect <container>

# 3. Check exit code
docker inspect --format='{{.State.ExitCode}}' <container>

# 4. Run with shell override
docker run --entrypoint sh -it myapp

# 5. Check health status
docker inspect --format='{{.State.Health.Status}}' <container>

# 6. View resource usage
docker stats <container>
```

---

### Question 13: What is a .dockerignore file?

**Answer:**

`.dockerignore` excludes files from the build context, reducing build time and preventing sensitive files from entering the image.

```
node_modules
npm-debug.log
.git
.gitignore
.env
.env.*
Dockerfile
docker-compose.yml
*.md
coverage
.nyc_output
.vscode
.idea
```

**Impact:** A project with `node_modules` (200MB) vs without (2MB) significantly affects build context upload time.

---

### Question 14: How do you handle database migrations in Docker?

**Answer:**

**Option 1: Init Container Pattern**

```yaml
services:
  migrations:
    image: myapp
    command: npm run migrate
    depends_on:
      db:
        condition: service_healthy
    restart: "no"

  app:
    image: myapp
    command: npm start
    depends_on:
      migrations:
        condition: service_completed_successfully
```

**Option 2: Entrypoint Script**

```bash
#!/bin/sh
set -e
npm run migrate
exec node server.js
```

**Option 3: Kubernetes Jobs**
Use a Job resource that runs migrations before the Deployment.

---

### Question 15: What is Docker BuildKit?

**Answer:**

BuildKit is the modern build engine for Docker, providing:

- Parallel stage builds
- Cache mount support
- Secret mounts
- SSH forwarding
- Better output formatting

```bash
# Enable BuildKit
DOCKER_BUILDKIT=1 docker build -t myapp .

# Use cache mounts
RUN --mount=type=cache,target=/root/.npm npm ci

# Use secret mounts
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci

# Use SSH mounts
RUN --mount=type=ssh ssh git@github.com
```

---

### Question 16: Explain Docker health checks.

**Answer:**

Health checks verify container health status.

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
```

| Parameter | Description |
|---|---|
| interval | Time between checks |
| timeout | Max time per check |
| start-period | Grace period for startup |
| retries | Failed checks before unhealthy |

**Status:** `healthy`, `unhealthy`, `starting`

---

### Question 17: How do you manage Docker in production?

**Answer:**

| Aspect | Solution |
|---|---|
| Orchestration | Kubernetes, Docker Swarm |
| Registry | ECR, GCR, ACR, Docker Hub |
| Monitoring | Prometheus, cAdvisor, Datadog |
| Logging | ELK Stack, Fluentd, Loki |
| Security | Trivy, Clair, Docker Scout |
| Secrets | Vault, AWS SSM, K8s Secrets |
| CI/CD | GitHub Actions, GitLab CI, Jenkins |

**Production Checklist:**
- Non-root user
- Health checks
- Resource limits
- Log rotation
- Image scanning
- Secrets management
- Backup strategy

---

### Question 18: What is the difference between docker stop and docker kill?

**Answer:**

| Command | Signal | Behavior |
|---|---|---|
| `docker stop` | SIGTERM, then SIGKILL | Graceful shutdown (10s default) |
| `docker kill` | SIGKILL (default) | Immediate termination |

```bash
# Graceful stop with timeout
docker stop --time=30 mycontainer

# Kill with specific signal
docker kill --signal=SIGTERM mycontainer

# Stop all running containers
docker stop $(docker ps -q)
```

---

### Question 19: How do you copy files between host and container?

**Answer:**

```bash
# Copy from host to container
docker cp ./config.json mycontainer:/app/config.json

# Copy from container to host
docker cp mycontainer:/app/logs ./logs

# During build (better approach)
COPY ./config.json /app/config.json

# Using volumes (best for development)
docker run -v $(pwd)/config:/app/config myapp
```

---

### Question 20: What is the difference between docker-compose up and docker-compose run?

**Answer:**

| Command | Purpose |
|---|---|
| `up` | Start all services defined in compose file |
| `run` | Start a specific service for one-off commands |

```bash
# Start entire application
docker compose up -d

# Run one-off command
docker compose run --rm app npm test

# Run with service overrides
docker compose run --rm -e DEBUG=true app sh
```

---

### Question 21: How do you handle different environments (dev/staging/prod)?

**Answer:**

**Option 1: Multiple Compose Files**

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

**Option 2: Profiles**

```yaml
services:
  app:
    profiles: ["dev", "prod"]

  debug:
    profiles: ["dev"]
```

**Option 3: Environment Variables**

```bash
# .env.dev
NODE_ENV=development
DATABASE_URL=postgres://localhost/dev

# .env.prod
NODE_ENV=production
DATABASE_URL=postgres://prod-db/prod
```

---

### Question 22: What is the difference between an image and a container?

**Answer:**

| Concept | Image | Container |
|---|---|---|
| State | Immutable | Mutable |
| Storage | Registry | Local filesystem |
| Creation | `docker build` | `docker run` |
| Analogy | Class | Instance |
| Persistence | Permanent | Ephemeral |

An image is a template. A container is a running instance of that image with added writable layers.

---

### Question 23: How do you implement logging in Docker containers?

**Answer:**

**Option 1: stdout/stderr (Recommended)**

```dockerfile
# Application logs to stdout
CMD ["node", "server.js"]
# In app: console.log("Request processed")
```

**Option 2: Docker Logging Drivers**

```bash
# JSON file (default)
docker run --log-driver=json-file --log-opt max-size=10m myapp

# syslog
docker run --log-driver=syslog myapp

# fluentd
docker run --log-driver=fluentd myapp
```

**Option 3: Compose Configuration**

```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

### Question 24: What is Docker context?

**Answer:**

Docker contexts allow managing multiple Docker hosts.

```bash
# List contexts
docker context ls

# Create context for remote host
docker context create remote --docker "host=ssh://user@remote-host"

# Use remote context
docker context use remote

# Run commands on remote host
docker ps
```

---

### Question 25: How do you handle resource limits in Docker?

**Answer:**

```bash
# Memory limit
docker run -m 512m myapp

# CPU limit
docker run --cpus=1.5 myapp

# CPU shares (relative weight)
docker run --cpu-shares=512 myapp

# GPU access
docker run --gpus all myapp
```

**Compose:**

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "1.5"
        reservations:
          memory: 256M
          cpus: "0.5"
```

---

### Question 26: What is a Docker registry and how does it work?

**Answer:**

A registry stores and distributes Docker images.

| Registry | Description |
|---|---|
| Docker Hub | Public, default |
| AWS ECR | AWS managed |
| Google GCR | GCP managed |
| Azure ACR | Azure managed |
| Harbor | Self-hosted |

```bash
# Tag and push to registry
docker tag myapp:latest registry.example.com/myapp:1.0.0
docker push registry.example.com/myapp:1.0.0

# Pull from registry
docker pull registry.example.com/myapp:1.0.0
```

---

### Question 27: How do you secure Docker containers?

**Answer:**

**Image Security:**
- Use minimal base images (Alpine, distroless)
- Scan for vulnerabilities (Trivy, Clair)
- Sign images (Docker Content Trust)
- Don't run as root

**Runtime Security:**
- Read-only filesystem
- Drop capabilities
- No new privileges
- Resource limits

**Network Security:**
- Internal networks for backend services
- TLS for all connections
- Network policies

```bash
# Security best practices
docker run \
  --read-only \
  --cap-drop ALL \
  --cap-add NET_BIND_SERVICE \
  --security-opt no-new-privileges \
  --user 1000:1000 \
  myapp
```

---

### Question 28: What is the difference between docker-compose and Kubernetes?

**Answer:**

| Aspect | Docker Compose | Kubernetes |
|---|---|---|
| Scale | Single host | Multi-host |
| Complexity | Simple | Complex |
| Use case | Development | Production |
| Self-healing | Limited | Full |
| Auto-scaling | No | Yes |
| Learning curve | Low | High |

**When to use Compose:** Local dev, testing, simple deployments
**When to use K8s:** Production, large scale, microservices, multi-tenant

---

### Question 29: How do you handle persistent data in Docker?

**Answer:**

```bash
# Named volume (recommended for production)
docker volume create mydata
docker run -v mydata:/app/data myapp

# Bind mount (development only)
docker run -v $(pwd)/src:/app/src myapp

# Backup volume
docker run --rm -v mydata:/data -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz -C /data .

# Restore volume
docker run --rm -v mydata:/data -v $(pwd):/backup \
  alpine tar xzf /backup/backup.tar.gz -C /data
```

---

### Question 30: What are the best practices for writing Dockerfiles?

**Answer:**

1. **Use specific image versions** — `node:18.17.0-alpine`
2. **Use multi-stage builds** — separate build and runtime
3. **Order instructions by change frequency** — deps before source
4. **Use .dockerignore** — exclude unnecessary files
5. **Run as non-root** — `USER node`
6. **Add health checks** — enable orchestration monitoring
7. **Minimize layers** — combine RUN commands
8. **Use BuildKit** — better caching and security
9. **Scan images** — check for vulnerabilities
10. **Document with LABELs** — metadata for maintainability

```dockerfile
# GOOD Dockerfile example
FROM node:18.17.0-alpine AS builder
LABEL maintainer="team@example.com"
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force
COPY . .
RUN npm run build

FROM node:18.17.0-alpine
RUN apk add --no-cache dumb-init
WORKDIR /app
COPY --from=builder --chown=node:node /app/dist ./dist
COPY --from=builder --chown=node:node /app/node_modules ./node_modules
USER node
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD node -e "require('http').get('http://localhost:3000/health')"
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/server.js"]
```

---

## Summary

Docker interview questions typically cover:
- Core concepts (images, containers, Dockerfile)
- Best practices (multi-stage builds, security, optimization)
- Production concerns (logging, monitoring, orchestration)
- Debugging and troubleshooting
- Compose and multi-container applications

Focus on understanding the **why** behind each concept, not just the **how**.

## Cheat Sheet

```bash
# Build
docker build -t name:tag .
docker build --no-cache -t name:tag .

# Run
docker run -d -p 3000:3000 --name app name:tag
docker run -it --rm name:tag sh

# Inspect
docker ps
docker logs -f app
docker inspect app
docker history name:tag

# Cleanup
docker system prune -af
docker volume prune

# Compose
docker compose up -d
docker compose down -v
docker compose logs -f

# Multi-stage
FROM builder AS stage1
COPY --from=stage1 /app/dist ./dist
```

---

## References & Learn More
- [Docker Documentation](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Deep Dive by Nigel Poulton](https://www.amazon.com/Docker-Deep-Dive-Nigel-Poulton/dp/1098130235)
- [Docker Curriculum](https://docker-curriculum.com/)
- [Play with Docker](https://labs.play-with-docker.com/)
