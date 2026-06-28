# Docker Multi-Stage Builds

## Definition

**Multi-stage builds** allow you to use multiple `FROM` statements in a single Dockerfile. Each `FROM` begins a new stage. Artifacts from earlier stages can be selectively copied to later stages using `COPY --from=<stage>`. The final image contains only what is needed for production, dramatically reducing size.

Key concepts:

- **Build Stage**: Contains compilers, build tools, dev dependencies
- **Production Stage**: Contains only runtime and application artifacts
- **AS alias**: Names a stage for later reference
- **COPY --from**: Copies files from a specific stage
- **Target build**: Build up to a specific stage (`docker build --target`)

## Why Do We Need It?

| Problem | Solution |
|---|---|
| Build tools in production image | Multi-stage: build in one, run in another |
| Large image sizes | Final image has only production deps |
| Security vulnerabilities | No compilers/shells in production |
| Slow CI/CD pipelines | Smaller images = faster pulls |
| Dev/prod parity issues | Same Dockerfile, different targets |
| Dependency on build cache | Isolated stages with clear boundaries |

## How It Works

### Build Process

```text
+-----------------------------------------------------+

|                Multi-Stage Build                      |
|                                                       |
|  Stage 1: builder                                    |
|  +-----------------------------------------------+  |
|  | FROM node:18-alpine AS builder              |  |
|  | WORKDIR /app                                |  |
|  | COPY package*.json ./                        |  |
|  | RUN npm ci                    <-- build deps  |  |
|  | COPY . .                                     |  |
|  | RUN npm run build             <-- compile TS  |  |
|  +---------------------+------------------------+  |
|                        |                             |
|                        |  COPY --from=builder        |
|                        v                             |
|  Stage 2: production                                 |
|  +-----------------------------------------------+  |
|  | FROM node:18-alpine                         |  |
|  | WORKDIR /app                                |  |
|  | COPY --from=builder /app/dist ./dist        |  |
|  | COPY --from=builder /app/node_modules ./    |  |
|  | RUN npm prune --production    <-- prod only   |  |
|  | USER node                                  |  |
|  | CMD ["node", "dist/server.js"]             |  |
|  +-----------------------------------------------+  |
|                                                       |
|  Result: 280MB builder --> 80MB final image           |

+-----------------------------------------------------+

```

### Image Size Comparison

```text
Single-stage:                          Multi-stage:
+------------------+                  +------------------+

| node:18-alpine   | 130 MB           |                  |
| + build deps     | +200 MB          | Final Image      |

| + prod deps      | +80 MB           | node:18-alpine   | 130 MB
| + source code    | +5 MB            | + dist folder    |  5 MB
| + dev tools      | +50 MB           | + prod deps      | 80 MB

|                  |                   |                  |

| TOTAL            | ~465 MB          | TOTAL            | ~215 MB
+------------------+                  +------------------+

```

## Code Examples

### Node.js TypeScript Application

```dockerfile
# Stage 1: Dependencies
FROM node:18-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Stage 2: Build
FROM deps AS build
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:18-alpine AS production
RUN apk add --no-cache dumb-init
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=deps /app/node_modules ./node_modules
COPY package*.json ./
RUN npm prune --production
USER node
EXPOSE 3000
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/server.js"]

```

### Go Application with Distroless

```dockerfile
# Stage 1: Build
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-s -w" -o /server ./cmd/server

# Stage 2: Production (distroless - no shell, no package manager)
FROM gcr.io/distroless/static-debian12
COPY --from=builder /server /server
USER nonroot:nonroot
ENTRYPOINT ["/server"]

```

### Python Flask Application

```dockerfile
# Stage 1: Build wheels
FROM python:3.11-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# Stage 2: Production
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels
COPY . .
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser
EXPOSE 5000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]

```

### Rust Application with Scratch

```dockerfile
FROM rust:1.72 AS builder
WORKDIR /app
COPY . .
RUN cargo build --release

FROM scratch
COPY --from=builder /app/target/release/myapp /myapp
USER 1000:1000
ENTRYPOINT ["/myapp"]

```

### Angular/Frontend Application

```dockerfile
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build -- --configuration production

FROM nginx:alpine
COPY --from=build /app/dist/myapp/browser /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80

```

### Custom Build Targets

```bash
# Build only the builder stage (for testing)
docker build --target builder -t myapp:debug .

# Build the production stage
docker build --target production -t myapp:latest .

# Build all stages
docker build -t myapp:latest .

```

## Real-World Use Cases

### 1. Monorepo with Shared Libraries

```dockerfile
FROM node:18-alpine AS base
WORKDIR /app

FROM base AS deps
COPY package*.json ./
RUN npm ci

FROM deps AS build-common
COPY packages/common/ ./packages/common/
RUN npm run build -w packages/common

FROM deps AS build-api
COPY --from=build-common /app/packages/common/dist ./packages/common/dist
COPY packages/api/ ./packages/api/
RUN npm run build -w packages/api

FROM node:18-alpine AS production
COPY --from=build-api /app/packages/api/dist ./dist
COPY --from=build-api /app/packages/api/node_modules ./node_modules
USER node
CMD ["node", "dist/index.js"]

```

### 2. Full-Stack Application

```dockerfile
# Frontend build
FROM node:18-alpine AS frontend-build
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Backend build
FROM node:18-alpine AS backend-build
WORKDIR /backend
COPY backend/package*.json ./
RUN npm ci
COPY backend/ .
RUN npm run build

# Production
FROM node:18-alpine
WORKDIR /app
COPY --from=backend-build /backend/dist ./backend/dist
COPY --from=backend-build /backend/node_modules ./backend/node_modules
COPY --from=frontend-build /frontend/dist ./frontend/dist
USER node
CMD ["node", "backend/dist/server.js"]

```

### 3. Java Spring Boot with GraalVM

```dockerfile
FROM ghcr.io/graalvm/native-image:17 AS builder
WORKDIR /app
COPY . .
RUN mvn package -Pnative

FROM scratch
COPY --from=builder /app/target/myapp /myapp
EXPOSE 8080
ENTRYPOINT ["/myapp"]

```

## Common Mistakes

| Mistake | Fix |
|---|---|
| Not naming stages | Always use `AS` for clarity |
| Copying entire node_modules | Copy package.json first, install, then copy source |
| Not using `--target` for dev builds | Use `--target` for debug/development stages |
| Forgetting `npm prune --production` | Remove dev deps in final stage |
| Using wrong base image for build vs runtime | Use `alpine` for build, `distroless` for runtime |
| Not cleaning up in the same layer | Combine commands to reduce layers |
| Not using BuildKit | Enable BuildKit for parallel stage builds |

## Best Practices

```dockerfile
# GOOD: Production-optimized multi-stage build
FROM node:18.17.0-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

FROM node:18.17.0-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM gcr.io/distroless/nodejs18-debian12 AS production
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=deps /app/node_modules ./node_modules
USER nonroot
EXPOSE 3000
CMD ["dist/server.js"]

```

1. **Name all stages** — improves readability and caching

2. **Use distroless for final stage** — minimal attack surface

3. **Separate dependency installation from source copy** — better caching

4. **Use `npm ci` not `npm install`** — deterministic builds

5. **Prune dev dependencies** — reduce final image size

6. **Use `--target` for dev/debug** — build specific stages

7. **Leverage BuildKit** — parallel stage execution

8. **Pin base image versions** — reproducible builds

9. **Order stages by build time** — slowest first for caching
10. **Scan each stage** — catch vulnerabilities early

## Performance Considerations

| Factor | Impact | Mitigation |
|---|---|---|
| Number of stages | Build time | Minimize stages, use BuildKit |
| Stage dependencies | Cache efficiency | Order by change frequency |
| Base image size | Pull time | Use Alpine or distroless |
| Build context | Upload time | `.dockerignore` |
| Parallel builds | Build speed | BuildKit auto-parallelizes |
| Layer size | Push/pull time | Combine small layers |

```bash
# BuildKit parallel build
DOCKER_BUILDKIT=1 docker build -t myapp .

# Build specific target
docker build --target builder -t myapp:debug .

# Build with no cache
docker build --no-cache -t myapp .

# Check image size
docker images myapp

```

## Interview Questions

### Beginner (5-10)

1. **What is a multi-stage build?**
   A Dockerfile technique using multiple `FROM` statements to build in stages, copying only needed artifacts to the final image.

2. **Why use multi-stage builds?**
   To keep production images small by excluding build tools, dev dependencies, and source code.

3. **What does `COPY --from=builder` do?**
   Copies files from the stage named `builder` into the current stage.

4. **How do you name a stage?**
   Use `AS alias` after the `FROM` instruction: `FROM node:18 AS builder`.

5. **Can you build a specific stage?**
   Yes: `docker build --target builder -t myapp:debug .`

6. **What is the difference between single-stage and multi-stage builds?**
   Single-stage: one `FROM`, everything in one image. Multi-stage: multiple `FROM`, only artifacts copied to final image.

7. **How do multi-stage builds improve security?**
   Build tools, compilers, and dev dependencies are excluded from the final image.

8. **What happens to earlier stages after the build?**
   They are not included in the final image but remain in build cache.

9. **Can you copy from any stage?**
   Yes, using `COPY --from=<stage-name-or-index>`.

10. **What is a distroless image?**
    A minimal image containing only the runtime and app—no shell, package manager, or OS utilities.

### Intermediate (5-10)

11. **How does BuildKit improve multi-stage builds?**
    BuildKit builds independent stages in parallel, significantly reducing build time.

12. **How would you optimize a Node.js multi-stage build?**
    Copy package.json first, install deps, copy source, build, then create production stage with only dist and production node_modules.

13. **What is the `--target` flag used for?**
    Builds up to a specific named stage, useful for dev/test/debug builds.

14. **How do you handle secrets in multi-stage builds?**
    Use `--mount=type=secret` with BuildKit to avoid leaking secrets in layers.

15. **What is the best base image for production?**
    Distroless or Alpine for minimal size and security.

16. **How do you test a multi-stage build locally?**
    Build with `--target` to intermediate stages and run tests there.

17. **What is `npm prune --production`?**
    Removes devDependencies from node_modules, reducing image size.

18. **How do you handle monorepos with multi-stage builds?**
    Build shared libraries in early stages, copy artifacts to application stages.

19. **What is the difference between `COPY --from` and volume mounts?**
    `COPY --from` bakes files into the image. Volume mounts overlay at runtime.

20. **How do you debug a failed multi-stage build?**
    Build with `--target` up to the failing stage, or use `docker run -it <stage-image> sh`.

### Senior (10-15)

21. **Design a multi-stage Dockerfile for a microservices monorepo.**
    Use base stage for shared configs, dependency stages per service, build stages for compilation, production stages with distroless. Leverage BuildKit cache mounts.

22. **How would you implement build caching across CI/CD pipelines?**
    Use BuildKit cache mounts for npm/yarn, registry-based caching, or Docker layer cache in CI.

23. **What is the security implication of leaving build tools in production?**
    Increased attack surface—compilers and shells can be used to exploit vulnerabilities.

24. **How do you handle native dependencies in multi-stage builds?**
    Build native modules in a full base image, copy compiled binaries to Alpine/distroless final stage.

25. **Explain BuildKit cache mounts for package managers.**
    `RUN --mount=type=cache,target=/root/.npm npm ci` caches npm's download cache across builds.

### FAANG-style (5-10)

26. **Design a Docker build pipeline for 100+ microservices.**
    Use shared base images, BuildKit cache imports/exports, registry caching, and parallel builds. Implement image promotion across environments.

27. **How would you optimize Docker build times from 30 minutes to under 5 minutes?**
    BuildKit parallel stages, cache mounts, minimal context, layer ordering, remote cache, and pre-built base images.

28. **Describe a strategy for managing base image updates across services.**
    Use a base image repository with automated updates, dependency scanning, and coordinated rollouts.

29. **How would you implement reproducible builds across different architectures?**
    Use multi-arch builds (`docker buildx build --platform linux/amd64,linux/arm64`), pin exact base image digests.

30. **Design a security scanning pipeline for multi-stage builds.**
    Scan each stage independently, block critical CVEs, maintain allowlists, integrate with CI/CD gates.

### Follow-ups (5-10)

31. **What happens if a stage fails during a multi-stage build?**
    The entire build fails. Docker does not cache failed stages.

32. **Can you use multi-stage builds with `docker compose`?**
    Yes, Compose supports multi-stage builds via the `target` build option.

33. **How do you copy SSH keys in multi-stage builds?**
    Use `--mount=type=ssh` with BuildKit: `RUN --mount=type=ssh ssh git@github.com`.

34. **What is the difference between `COPY --from` and `ADD --from`?**
    Both copy from previous stages. `ADD` can also extract tarballs and fetch URLs.

35. **How do you handle Docker layer caching with multi-stage builds?**
    Order instructions by change frequency. Use BuildKit cache mounts for package managers.

## Summary

Multi-stage builds separate build-time and run-time concerns, producing minimal, secure production images. They improve caching, reduce image sizes, and enable consistent dev/prod environments using a single Dockerfile with different target stages.

## Cheat Sheet

```bash
# Build specific stage
docker build --target builder -t myapp:debug .

# Build production
docker build --target production -t myapp:latest .

# BuildKit
DOCKER_BUILDKIT=1 docker build -t myapp .

# Build with cache mounts
RUN --mount=type=cache,target=/root/.npm npm ci

# Copy from stage
COPY --from=builder /app/dist ./dist

# Multi-arch build
docker buildx build --platform linux/amd64,linux/arm64 -t myapp .

# Check image size
docker images myapp
docker scout quickview myapp:latest

```

---

## References & Learn More

- [Docker Documentation](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Deep Dive by Nigel Poulton](https://www.amazon.com/Docker-Deep-Dive-Nigel-Poulton/dp/1098130235)
- [Docker Curriculum](https://docker-curriculum.com/)
- [Play with Docker](https://labs.play-with-docker.com/)
