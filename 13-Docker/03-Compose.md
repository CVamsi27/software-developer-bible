---
section: Docker
category: DevOps
tags: [concept]
---

# Docker Compose

## Definition

**Docker Compose** is a tool for defining and running multi-container Docker applications using a declarative YAML file. It manages services, networks, and volumes as a single unit, enabling local development environments and multi-service architectures.

Key concepts:

- **Service**: A container definition with build/run configuration
- **Network**: Isolated communication layer between services
- **Volume**: Persistent storage attached to services
- **Stack**: A complete Compose application (services + networks + volumes)

## Why Do We Need It?

| Problem | Solution |
|---|---|
| Multiple `docker run` commands | Single `docker-compose.yml` |
| Manual network creation | Automatic network management |
| Service discovery configuration | Built-in DNS resolution |
| Development environment setup | One command to start everything |
| Complex multi-service apps | Declarative configuration |
| Reproducible environments | Version-controlled YAML |

## How It Works

### Architecture

```text
┌─────────────────────────────────────────────────────┐
│                  docker-compose up                    │
│                        │                              │
│                        ▼                              │
│  ┌──────────────────────────────────────────────┐   │
│  │            docker-compose.yml                 │   │
│  │                                               │   │
│  │  services:        networks:      volumes:     │   │
│  │   app             frontend       pg_data     │   │
│  │   postgres        backend        redis_data  │   │
│  │   redis                           app_data   │   │
│  └──────┬──────────────┬───────────────┬────────┘   │
│         │              │               │             │
│         ▼              ▼               ▼             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │Container │  │Container │  │Container │         │
│  │  app     │  │ postgres │  │  redis   │         │
│  └──────────┘  └──────────┘  └──────────┘         │
│       │              │              │                │
│       └──────────────┴──────────────┘                │
│                      │                               │
│               Docker Networks                        │
└─────────────────────────────────────────────────────┘

```

### Project Structure

```text
myproject/
├── docker-compose.yml
├── docker-compose.override.yml
├── .env
├── .dockerignore
├── Dockerfile
├── src/
├── config/
│   ├── nginx.conf
│   └── postgres.conf
└── scripts/
    └── init.sh

```

## Code Examples

### Basic Compose File

```yaml
# docker-compose.yml
version: "3.9"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        NODE_ENV: production
    ports:

      - "3000:3000"
    environment:

      - NODE_ENV=production
      - DATABASE_URL=postgresql://postgres:secret@postgres:5432/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:

      - frontend
      - backend
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    volumes:

      - pg_data:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
    networks:

      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:

      - redis_data:/data
    networks:

      - backend
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:

      - "80:80"
      - "443:443"
    volumes:

      - ./config/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:

      - app
    networks:

      - frontend
    restart: unless-stopped

volumes:
  pg_data:
  redis_data:

networks:
  frontend:
  backend:
    internal: true

```

### Compose Profiles

```yaml
# docker-compose.yml
version: "3.9"

services:
  app:
    build: .
    ports:

      - "3000:3000"
    profiles:

      - dev
      - prod

  debug:
    image: busybox
    profiles:

      - debug

  postgres:
    image: postgres:15
    profiles:

      - dev
      - prod

  redis:
    image: redis:7-alpine
    profiles:

      - dev
      - prod

# Usage:
# docker compose --profile dev up
# docker compose --profile debug up

```

### Environment Variable Handling

```yaml
# docker-compose.yml
version: "3.9"

services:
  app:
    build: .
    env_file:

      - .env
      - .env.local
    environment:

      - NODE_ENV=${NODE_ENV:-production}
      - LOG_LEVEL=${LOG_LEVEL:-info}
    secrets:

      - db_password
      - api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    environment: API_KEY

```

### Multi-Stage Development Setup

```yaml
# docker-compose.override.yml (auto-loaded with docker-compose up)
version: "3.9"

services:
  app:
    build:
      target: development
    volumes:

      - ./src:/app/src
      - /app/node_modules
    command: npm run dev
    environment:

      - NODE_ENV=development
      - DEBUG=app:*
    ports:

      - "3000:3000"
      - "9229:9229"  # Node.js debugger

  test:
    build:
      target: test
    volumes:

      - ./src:/app/src
      - /app/node_modules
    command: npm test
    environment:

      - NODE_ENV=test
    profiles:

      - test

```

### Dockerfile for Compose

```dockerfile
# Multi-purpose Dockerfile for Compose
FROM node:18-alpine AS base
WORKDIR /app

# Dependencies layer
FROM base AS deps
COPY package*.json ./
RUN npm ci

# Development stage
FROM base AS development
COPY --from=deps /app/node_modules ./node_modules
COPY . .
CMD ["npm", "run", "dev"]

# Build stage
FROM base AS build
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production stage
FROM base AS production
ENV NODE_ENV=production
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY package*.json ./
USER node
CMD ["node", "dist/server.js"]

```

## Real-World Use Cases

### 1. Full-Stack Development Environment

```yaml
version: "3.9"

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      target: development
    volumes:

      - ./frontend/src:/app/src
    ports:

      - "3001:3000"
    environment:

      - REACT_APP_API_URL=http://localhost:3002

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: development
    volumes:

      - ./backend/src:/app/src
    ports:

      - "3002:3000"
    environment:

      - DATABASE_URL=postgres://postgres:secret@db:5432/mydb
      - REDIS_URL=redis://redis:6379

  db:
    image: postgres:15-alpine
    volumes:

      - pg_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: mydb
      POSTGRES_PASSWORD: secret

  redis:
    image: redis:7-alpine

  mailhog:
    image: mailhog/mailhog
    ports:

      - "1025:1025"
      - "8025:8025"

volumes:
  pg_data:

```

### 2. CI/CD Pipeline Services

```yaml
version: "3.9"

services:
  test-runner:
    build:
      context: .
      target: test
    environment:

      - DATABASE_URL=postgres://test:test@test-db:5432/testdb
    depends_on:
      test-db:
        condition: service_healthy

  test-db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: testdb
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U test -d testdb"]
      interval: 5s
      timeout: 3s
      retries: 10

  lint:
    build:
      context: .
      target: development
    command: npm run lint
    profiles:

      - lint

```

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using `docker-compose` (v1) | Use `docker compose` (v2 plugin) |
| No `depends_on` health checks | Use `condition: service_healthy` |
| Hardcoding secrets in YAML | Use `.env` files or `secrets` |
| Not using `.env` for config | Use environment variable substitution |
| Using `latest` tag | Pin specific image versions |
| No restart policy | Add `restart: unless-stopped` |
| Missing health checks | Add health checks for all services |
| Not cleaning up | Use `docker compose down -v` |

## Best Practices

```yaml
# GOOD: Production-ready Compose file
version: "3.9"

services:
  app:
    build:
      context: .
      target: production
      args:

        - NODE_ENV=production
    ports:

      - "${APP_PORT:-3000}:3000"
    environment:

      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
    secrets:

      - db_password
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:3000/health', r => process.exit(r.statusCode === 200 ? 0 : 1))"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "0.5"
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    networks:

      - frontend
      - backend

secrets:
  db_password:
    file: ./secrets/db_password.txt

networks:
  frontend:
  backend:
    internal: true

```

1. **Use Compose v2** — `docker compose` CLI, not `docker-compose`

2. **Use profiles** — separate dev/test/prod configurations

3. **Pin image versions** — never use `latest`

4. **Add health checks** — enable `depends_on` conditions

5. **Use `.env` files** — never hardcode secrets

6. **Set resource limits** — prevent container resource exhaustion

7. **Use `restart: unless-stopped`** — automatic recovery

8. **Configure logging** — limit log file sizes

9. **Use secrets** — for passwords and API keys
10. **Use `internal` networks** — for backend isolation

## Performance Considerations

| Factor | Impact | Mitigation |
|---|---|---|
| Build context size | Build time | `.dockerignore`, minimize context |
| Service startup order | App readiness | Health checks + `depends_on` |
| Volume mount type | I/O performance | Use named volumes, not bind mounts |
| Resource limits | Stability | Set memory/CPU limits |
| Log size | Disk usage | Configure log rotation |
| Network isolation | Security | Use `internal` networks |

```bash
# Build with cache
docker compose build --parallel

# Start only needed services
docker compose up app postgres

# Use watch mode (Compose v2)
docker compose watch

# Scale a service
docker compose up --scale worker=3

```


## Summary

Docker Compose simplifies multi-container application management through declarative YAML configuration. It provides service discovery, network management, volume orchestration, and environment variable handling. Essential for local development, testing, and simple deployments.

## Cheat Sheet
```bash
# Lifecycle
docker compose up -d
docker compose down -v
docker compose restart
docker compose stop
docker compose start

# Build
docker compose build
docker compose build --no-cache
docker compose up --build

# Logs
docker compose logs -f
docker compose logs app --tail=100

# Execute
docker compose exec app sh
docker compose run --rm app npm test

# Scale
docker compose up --scale worker=3

# Watch
docker compose watch

# Profiles
docker compose --profile debug up

# Environment
docker compose config  # validate and view resolved config

```

---

---

## See Also
- [Kubernetes](../14-Kubernetes/)
- [CI/CD](../15-CI-CD/)
- [Microservices](../12-Microservices/)

## References & Learn More

- [Docker Documentation](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Deep Dive by Nigel Poulton](https://www.amazon.com/Docker-Deep-Dive-Nigel-Poulton/dp/1098130235)
- [Docker Curriculum](https://docker-curriculum.com/)
- [Play with Docker](https://labs.play-with-docker.com/)
