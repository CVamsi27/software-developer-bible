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

```
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

```
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

## Interview Questions

### Beginner (5-10)

1. **What is Docker Compose?**
   A tool for defining and running multi-container Docker applications with a YAML file.

2. **What is the difference between `docker run` and `docker-compose up`?**
   `docker run` manages single containers; Compose manages multiple services, networks, and volumes together.

3. **What is the `depends_on` directive?**
   Controls service startup order and can wait for health checks.

4. **How do you stop a Compose application?**
   `docker compose down` stops and removes containers; `docker compose down -v` also removes volumes.

5. **What is a Compose profile?**
   A way to define optional services that only start when the profile is activated.

6. **How do you pass environment variables?**
   Via `.env` file, `environment` section, or `env_file` directive.

7. **What is the default network created by Compose?**
   A bridge network named `<project_name>_default`.

8. **How do you view logs?**
   `docker compose logs -f [service]`

9. **What is the difference between `docker-compose` and `docker compose`?**
   `docker-compose` is the standalone v1 binary; `docker compose` is the v2 plugin.

10. **How do you rebuild images?**
    `docker compose build --no-cache` or `docker compose up --build`

### Intermediate (5-10)

11. **How does Compose handle service discovery?**
    Services are accessible by their service name as DNS entries on shared networks.

12. **What is `docker-compose.override.yml`?**
    Automatically loaded alongside `docker-compose.yml` to override or extend configuration.

13. **How do you run a one-off command in a service?**
    `docker compose run <service> <command>` or `docker compose exec <service> <command>`.

14. **What is the difference between `run` and `exec`?**
    `run` creates a new container; `exec` runs in an existing running container.

15. **How do you scale services?**
    `docker compose up --scale <service>=<count>` (limited to single host).

16. **How do you handle different environments?**
    Use multiple Compose files: `docker compose -f docker-compose.yml -f docker-compose.prod.yml up`.

17. **What is the `build` context?**
    The directory sent to the Docker daemon for building the image.

18. **How do you mount secrets in Compose?**
    Use the `secrets` top-level element with `file:` or `environment:` sources.

19. **What is `docker compose watch`?**
    A feature that watches for file changes and rebuilds/restarts services automatically.

20. **How do you configure resource limits?**
    Under `deploy.resources.limits` (Compose v3) or `mem_limit`/`cpus` (Compose v2).

### Senior (10-15)

21. **How would you structure Compose files for a microservices architecture?**
    Use base file + environment-specific overrides. Separate network definitions per service boundary. Use profiles for optional services (debug, monitoring).

22. **How do you handle database migrations in Compose?**
    Use a migration service with `depends_on` health checks, or run migrations in the app's entrypoint script.

23. **Explain Compose's networking model.**
    Compose creates a default bridge network. Services communicate via DNS names. You can define custom networks for isolation.

24. **How do you implement zero-downtime deployment with Compose?**
    Use `docker compose up --no-deps --scale app=N` with a load balancer, or rolling updates via Swarm mode.

25. **How do you handle secrets securely in Compose?**
    Use Docker secrets (Swarm), `env_file` for local dev, or external secret management (Vault, AWS SSM).

### FAANG-style (5-10)

26. **Design a production Compose setup for a high-availability application.**
    Multiple replicas behind a load balancer, health checks, resource limits, logging to centralized system, volume backups, network isolation.

27. **How would you migrate from Compose to Kubernetes?**
    Map Compose services to Deployments, volumes to PVs, networks to Services, and use Kompose or manual YAML conversion.

28. **Describe a multi-host Compose deployment strategy.**
    Use Docker Swarm mode or orchestrate Compose with remote Docker contexts. For true multi-host, migrate to Kubernetes.

29. **How would you debug a Compose application with 20+ services?**
    Use `docker compose logs --tail=100`, check health status, verify network connectivity, use debug profiles.

30. **Design a Compose-based development environment for a team of 50 engineers.**
    Use `.env` files with sensible defaults, mount host SSH keys, cache node_modules as named volumes, provide scripts for common tasks.

### Follow-ups (5-10)

31. **What is the `init` directive in Compose?**
    Runs an init process (tini) inside the container to handle PID 1 responsibilities.

32. **How do you handle file permissions with bind mounts?**
    Use `user` directive, create matching UID/GID, or use named volumes.

33. **Can Compose work with Docker Swarm?**
    Yes — `docker stack deploy -c docker-compose.yml` deploys to Swarm.

34. **What is the `external` keyword for volumes/networks?**
    References resources created outside Compose that shouldn't be removed by `docker compose down`.

35. **How do you configure HTTPS in Compose with nginx?**
    Mount certificate files and configure nginx.conf with SSL directives.

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

## References & Learn More
- [Docker Documentation](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Deep Dive by Nigel Poulton](https://www.amazon.com/Docker-Deep-Dive-Nigel-Poulton/dp/1098130235)
- [Docker Curriculum](https://docker-curriculum.com/)
- [Play with Docker](https://labs.play-with-docker.com/)
