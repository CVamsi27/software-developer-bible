---
section: Docker
category: DevOps
tags: [concept, reference]
---

# Dockerfile Best Practices & Security

## Definition

**Dockerfile Best Practices** encompass the patterns, optimizations, and security measures for creating efficient, secure, and maintainable container images. Key principles include minimizing image size, leveraging layer caching, running with least privilege, and eliminating vulnerabilities.

## Why Do We Need It?

1. **Smaller images**: Faster deployments, less storage, lower bandwidth
2. **Faster builds**: Proper layer ordering maximizes cache utilization
3. **Security**: Fewer attack vectors with minimal dependencies and non-root users
4. **Compliance**: Meeting security standards (PCI-DSS, SOC2) for containerized apps
5. **Reproducibility**: Deterministic builds with pinned versions

## Best Practices

### 1. Leverage Multi-Stage Builds

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine
RUN addgroup -g 1001 app && adduser -u 1001 -G app -s /bin/sh -D app
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER app
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

### 2. Optimize Layer Caching

```dockerfile
# ❌ BAD: Cache invalidated on every code change
COPY . .
RUN npm ci
RUN npm run build

# ✅ GOOD: Copy only what's needed, layer strategically
COPY package*.json ./
RUN npm ci                           # Cached unless package.json changes
COPY tsconfig.json ./
COPY src/ ./src/
RUN npm run build                    # Cached unless src/ changes
COPY public/ ./public/               # Static files rarely change
```

### 3. Use Distroless or Slim Base Images

```dockerfile
# ❌ BAD: Full OS with unnecessary tools
FROM node:20

# ✅ GOOD: Slim variant
FROM node:20-slim

# ✅ BEST: Distroless (no shell, no package manager)
FROM gcr.io/distroless/nodejs20-debian12
COPY --from=builder /app /app
CMD ["/app/dist/main.js"]
```

### 4. Run as Non-Root User

```dockerfile
# Add user and group
RUN addgroup -g 1001 app && \
    adduser -u 1001 -G app -s /bin/sh -D app

# Set ownership
COPY --chown=app:app . /app

# Switch to non-root
USER app
```

### 5. Pin Base Image Versions

```dockerfile
# ❌ BAD: Unpinned version
FROM node:20

# ❌ BAD: 'latest' tag
FROM node:latest

# ✅ GOOD: Pinned digest
FROM node:20-alpine@sha256:1234abcd...

# ✅ GOOD: Specific minor version
FROM node:20.11.0-alpine
```

### 6. Minimize Layers

```dockerfile
# ❌ BAD: Many separate RUN commands
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get clean

# ✅ GOOD: Combine related commands
RUN apt-get update && \
    apt-get install -y curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### 7. Use .dockerignore

```
# .dockerignore
.git
node_modules
dist
.env
*.md
Dockerfile
docker-compose.yml
.gitignore
coverage
test
```

### 8. Add Healthcheck

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
```

### 9. Set Metadata Labels

```dockerfile
LABEL org.opencontainers.image.title="My App"
LABEL org.opencontainers.image.description="Production application"
LABEL org.opencontainers.image.version="1.2.3"
LABEL org.opencontainers.image.created="2025-01-15T10:00:00Z"
LABEL org.opencontainers.image.source="https://github.com/org/repo"
```

### 10. Security Scanning

```bash
# Scan with Trivy
trivy image myapp:latest

# Scan with Docker Scout
docker scout cves myapp:latest

# Scan with Snyk
snyk container test myapp:latest
```

## Summary

Dockerfile best practices reduce image size, improve build speed, and enhance security. Use multi-stage builds, optimize layer order, run as non-root, pin versions, and scan for vulnerabilities in CI/CD.

## Cheat Sheet

```dockerfile
# Optimized Dockerfile Template
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-slim
RUN addgroup -g 1001 app && adduser -u 1001 -G app -s /bin/sh -D app
COPY --from=builder /app/dist /app
COPY --from=builder /app/node_modules /app/node_modules
USER app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:3000/health || exit 1
LABEL org.opencontainers.image.version="1.0.0"
CMD ["node", "app/main.js"]
```

---

### See Also

- [Docker Security](../09-Security/)
- [Images & Containers](../01-Images-Containers.md)
- [Multi-Stage Builds](../04-Multi-Stage-Builds.md)

### References

- [Dockerfile Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [Snyk Container Security](https://snyk.io/learn/container-security/)
