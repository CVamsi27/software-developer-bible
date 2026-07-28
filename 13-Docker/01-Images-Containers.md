---
section: Docker
category: DevOps
tags: [concept]
---

# Docker Images & Containers

## Definition

A **Docker image** is a read-only template containing instructions for creating a container. It consists of layered filesystem changes. A **Docker container** is a runnable instance of an image—lightweight, isolated, and ephemeral. Images are built from a **Dockerfile**, a declarative script of build instructions.

Key terms:

- **Image**: Immutable blueprint (e.g., `nginx:1.25`)
- **Container**: Running process with isolated CPU, memory, filesystem, network
- **Layer**: Each Dockerfile instruction produces an immutable layer
- **Registry**: Central repository for images (Docker Hub, ECR, GCR, ACR)
- **Tag**: Version identifier appended to image name (`node:18-alpine`)

## Why Do We Need It?

| Problem | Solution |
|---|---|
| "Works on my machine" | Consistent environment via images |
| Manual server setup | Declarative Dockerfile |
| Dependency conflicts | Per-container isolation |
| Slow deployments | Lightweight containers vs VMs |
| Difficult rollbacks | Immutable image tags |
| Resource waste | Shared kernel, no hypervisor overhead |

## How It Works

### Image Layering

Every instruction in a Dockerfile creates a layer. Layers are cached and stacked. When you rebuild, only changed layers are regenerated.

```dockerfile
FROM node:18-alpine          # Layer 0: base OS
WORKDIR /app                 # Layer 1: set working dir
COPY package*.json ./        # Layer 2: copy dep manifest
RUN npm ci --production      # Layer 3: install deps
COPY . .                     # Layer 4: copy source
EXPOSE 3000                  # Layer 5: metadata
CMD ["node", "server.js"]    # Layer 6: default command

```

### Container Lifecycle

```text
  docker build

       |

       v
  [Image] --docker run--> [Container] --docker stop--> [Stopped]

                              |                              |

                              v                              v
                          [Running]                   [docker rm]

                              |                              |

                              v                              v
                         docker pause              [Removed from disk]

```

### Image Architecture

```text
┌─────────────────────────────────────────────┐
│              Docker Image                   │
├─────────────────────────────────────────────┤
│  Layer 5: CMD ["node", "server.js"]         │  ← ~0 bytes (metadata)
│  Layer 4: COPY . .                          │  ← varies
│  Layer 3: RUN npm ci --production           │  ← ~150 MB
│  Layer 2: COPY package*.json ./             │  ← ~0.05 MB
│  Layer 1: WORKDIR /app                      │  ← ~0 bytes
│  Layer 0: node:18-alpine (base)             │  ← ~130 MB
├─────────────────────────────────────────────┤
│  Total image: ~280 MB                       │
└─────────────────────────────────────────────┘

```

## Code Examples

### Basic Dockerfile

```dockerfile
# Use specific version, never 'latest'
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy dependency manifests first (layer caching)
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

# Run as non-root user
USER node

# Start application
CMD ["node", "server.js"]

```

### Building and Running

```bash
# Build image with tag
docker build -t myapp:1.0.0 .

# Build with build arguments
docker build --build-arg NODE_ENV=production -t myapp:1.0.0 .

# Run container
docker run -d -p 3000:3000 --name myapp myapp:1.0.0

# Run with environment variables
docker run -d -p 3000:3000 \
  -e DATABASE_URL="postgres://db:5432/mydb" \
  -e REDIS_URL="redis://cache:6379" \
  --name myapp myapp:1.0.0

# Run interactively
docker run -it -p 3000:3000 myapp:1.0.0 sh

```

### Multi-Stage Build

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./
USER node
CMD ["node", "dist/server.js"]

```

### Inspecting Images and Containers

```bash
# Inspect image layers
docker history myapp:1.0.0

# Inspect image details
docker inspect myapp:1.0.0

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# View container logs
docker logs myapp

# Execute command in running container
docker exec -it myapp sh

# Copy files from container
docker cp myapp:/app/logs ./logs

# Remove stopped containers
docker rm myapp

# Remove image
docker rmi myapp:1.0.0

```

### .dockerignore

```text
node_modules
npm-debug.log
.git
.gitignore
.env
.env.*
Dockerfile
docker-compose.yml
*.md
.vscode
.idea
coverage
.nyc_output

```

## Real-World Use Cases

### 1. Node.js Microservice

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY dist/ ./dist/
USER 1001
EXPOSE 8080
CMD ["node", "dist/index.js"]

```

### 2. Python Django App

```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]

```

### 3. Go Binary (Distroless)

```dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /server ./cmd/server

FROM gcr.io/distroless/static-debian12
COPY --from=builder /server /server
USER nonroot:nonroot
ENTRYPOINT ["/server"]

```

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using `latest` tag | Pin specific versions (`node:18.17.0-alpine`) |
| Copying everything before `npm install` | Copy `package*.json` first for layer caching |
| Running as root | Use `USER node` or create custom user |
| No `.dockerignore` | Exclude `node_modules`, `.git`, etc. |
| No multi-stage builds | Separate build deps from production |
| Not cleaning caches in same layer | Combine `RUN apt-get update && apt-get install -y` |
| Not using `HEALTHCHECK` | Add health checks for orchestrators |
| Large image size | Use Alpine, distroless, or slim variants |

## Best Practices

```dockerfile
# GOOD: Pinned versions, Alpine, multi-stage, non-root, health check
FROM node:18.17.0-alpine AS builder
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
  CMD node -e "require('http').get('http://localhost:3000/health', r => { process.exit(r.statusCode === 200 ? 0 : 1) })"
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/server.js"]

```

1. **Pin base image versions** — avoid `:latest`

2. **Use multi-stage builds** — minimize final image size

3. **Order instructions by change frequency** — deps before source

4. **Run as non-root** — security best practice

5. **Use `.dockerignore`** — exclude unnecessary files

6. **Leverage layer caching** — copy dependency files first

7. **Add HEALTHCHECK** — enables orchestrator health monitoring

8. **Use specific distroless/alpine images** — smaller attack surface

9. **Combine RUN commands** — reduce layer count
10. **Scan images** — use `docker scout` or Trivy

## Performance Considerations

| Factor | Impact | Mitigation |
|---|---|---|
| Image size | Pull time, storage | Alpine, multi-stage, `.dockerignore` |
| Layer count | Build time, caching | Combine RUN commands |
| Build context size | Upload time to daemon | `.dockerignore`, minimize context |
| Cache invalidation | Full rebuild | Order Dockerfile instructions carefully |
| Registry latency | CI/CD speed | Use local cache or mirror registry |
| Container startup | Deployment speed | Use `dumb-init`, minimal base |

```bash
# Build with minimal context
docker build -t myapp . -f Dockerfile --no-cache

# Use buildkit for parallel builds
DOCKER_BUILDKIT=1 docker build -t myapp .

# Check image size
docker images myapp

# Scan image for vulnerabilities
docker scout cves myapp:1.0.0

```

## Summary

Docker images are immutable, layered templates. Containers are ephemeral runtime instances. Mastering Dockerfiles, layer caching, multi-stage builds, and security practices is essential for any senior engineer. Images should be minimal, scanned, non-root, and reproducible.

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
docker ps -a
docker logs -f app
docker exec -it app sh
docker inspect app
docker history name:tag

# Cleanup
docker rm $(docker ps -aq)
docker rmi name:tag
docker system prune -af

# Multi-stage build
FROM builder AS stage1
COPY --from=stage1 /app/dist ./dist

# Secrets in build
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci

```

---

---

## See Also
- [CI/CD](../15-CI-CD/)
- [Kubernetes](../14-Kubernetes/)
- [Kubernetes Jobs](../14-Kubernetes/10-Jobs-CronJobs.md)
- [Kubernetes StatefulSets](../14-Kubernetes/09-StatefulSets-DaemonSets.md)
- [Microservices](../12-Microservices/)

## References & Learn More

- [Docker Documentation](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Deep Dive by Nigel Poulton](https://www.amazon.com/Docker-Deep-Dive-Nigel-Poulton/dp/1098130235)
- [Docker Curriculum](https://docker-curriculum.com/)
- [Play with Docker](https://labs.play-with-docker.com/)
