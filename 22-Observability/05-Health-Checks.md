[![Category: DevOps](https://img.shields.io/badge/category-DevOps-ff7f00)](.)

# Health Checks

## Definition

Health checks are endpoints or mechanisms that report whether a service is alive and able to handle requests. They are the most basic form of observability — a binary signal (healthy/unhealthy) that load balancers, orchestrators, and monitoring systems use to route traffic and manage service lifecycle.

There are two distinct types:

- **Liveness check**: Is the process alive? (Can it be restarted?)
- **Readiness check**: Can it serve traffic? (Is it ready to handle requests?)

## Why Do We Need It?

1. **Orchestration**: Kubernetes uses health checks to decide when to restart pods and when to send traffic

2. **Load balancing**: Load balancers use health checks to exclude unhealthy instances

3. **Dependency verification**: Confirm database, cache, and external service connectivity

4. **Graceful shutdown**: Signal when a service is draining and should stop receiving new requests

5. **Alerting**: Health check failures trigger alerts before users notice

6. **Auto-scaling**: Combined with metrics, health checks inform scaling decisions

## How It Works

```text
┌─────────────────────────────────────────────────────────────────┐
│               HEALTH CHECK TYPES IN KUBERNETES                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  LIVENESS PROBE (Is the process alive?)                        │
│  ─────────────────────────────────────                         │
│  GET /health/live → 200 OK = alive                             │
│  Failure → Container RESTARTED                                  │
│                                                                 │
│  Use case: Deadlock detection, infinite loops, memory leaks    │
│                                                                 │
│  ┌─────────┐   health/live    ┌─────────┐                     │
│  │  Kubelet │ ──────────────▶ │   Pod   │  200 OK = alive     │
│  └─────────┘                  └─────────┘  timeout = restart   │
│                                                                 │
│                                                                 │
│  READINESS PROBE (Can it serve traffic?)                       │
│  ──────────────────────────────────────                        │
│  GET /health/ready → 200 OK = ready                            │
│  Failure → Removed from SERVICE ENDPOINTS (no traffic)         │
│                                                                 │
│  Use case: Waiting for DB connection, warm-up, dependencies    │
│                                                                 │
│  ┌─────────┐   health/ready   ┌─────────┐                     │
│  │  Kubelet │ ──────────────▶ │   Pod   │  200 = in service   │
│  └─────────┘                  └─────────┘  503 = out of svc    │
│                                                                 │
│                                                                 │
│  STARTUP PROBE (Is the container started?)                     │
│  ────────────────────────────────────────                      │
│  GET /health/startup → 200 OK = started                        │
│  Failure → Container KILLED and restarted                      │
│                                                                 │
│  Use case: Slow-starting apps (JVM, large datasets)           │
│  Disables liveness/readiness until startup succeeds            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  HEALTH CHECK RESPONSE FORMAT                               │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  200 OK (healthy)                                          │
  │  {                                                         │
  │    "status": "healthy",                                    │
  │    "timestamp": "2024-01-15T10:30:45Z",                   │
  │    "version": "1.2.3",                                    │
  │    "uptime": 86400,                                        │
  │    "checks": {                                             │
  │      "database": "healthy",                                │
  │      "redis": "healthy",                                   │
  │      "external-api": "healthy"                             │
  │    }                                                       │
  │  }                                                         │
  │                                                             │
  │  503 Service Unavailable (unhealthy)                       │
  │  {                                                         │
  │    "status": "unhealthy",                                  │
  │    "error": "Database connection failed",                  │
  │    "checks": {                                             │
  │      "database": "unhealthy",                              │
  │      "redis": "healthy"                                    │
  │    }                                                       │
  │  }                                                         │
  └─────────────────────────────────────────────────────────────┘

```

## Code Examples

### Basic Health Check Server

```typescript
import express from "express";
import http from "http";

const healthApp = express();

interface HealthStatus {
  status: "healthy" | "unhealthy" | "degraded";
  timestamp: string;
  version: string;
  uptime: number;
  checks: Record<string, { status: string; latencyMs?: number; error?: string }>;
}

// Dependency check functions
async function checkDatabase(): Promise<{ status: string; latencyMs: number }> {
  const start = Date.now();
  try {
    await db.query("SELECT 1");
    return { status: "healthy", latencyMs: Date.now() - start };
  } catch (err) {
    return { status: "unhealthy", latencyMs: Date.now() - start, error: (err as Error).message };
  }
}

async function checkRedis(): Promise<{ status: string; latencyMs: number }> {
  const start = Date.now();
  try {
    await redis.ping();
    return { status: "healthy", latencyMs: Date.now() - start };
  } catch (err) {
    return { status: "unhealthy", latencyMs: Date.now() - start, error: (err as Error).message };
  }
}

async function checkExternalAPI(): Promise<{ status: string; latencyMs: number }> {
  const start = Date.now();
  try {
    const res = await fetch("https://api.stripe.com/health", {
      signal: AbortSignal.timeout(3000),
    });
    return { status: res.ok ? "healthy" : "degraded", latencyMs: Date.now() - start };
  } catch (err) {
    return { status: "unhealthy", latencyMs: Date.now() - start, error: (err as Error).message };
  }
}

// Liveness: Is the process alive?
healthApp.get("/health/live", (_req, res) => {
  res.status(200).json({ status: "alive" });
});

// Readiness: Can it serve traffic?
healthApp.get("/health/ready", async (_req, res) => {
  const checks = {
    database: await checkDatabase(),
    redis: await checkRedis(),
    stripe: await checkExternalAPI(),
  };

  const allHealthy = Object.values(checks).every((c) => c.status === "healthy");
  const anyUnhealthy = Object.values(checks).some((c) => c.status === "unhealthy");

  const status: HealthStatus["status"] = allHealthy
    ? "healthy"
    : anyUnhealthy
      ? "unhealthy"
      : "degraded";

  const statusCode = status === "healthy" ? 200 : 503;

  res.status(statusCode).json({
    status,
    timestamp: new Date().toISOString(),
    version: process.env.APP_VERSION || "unknown",
    uptime: process.uptime(),
    checks,
  });
});

// Startup: Has the app finished initializing?
let isStarted = false;

healthApp.get("/health/startup", (_req, res) => {
  if (isStarted) {
    res.status(200).json({ status: "started" });
  } else {
    res.status(503).json({ status: "starting" });
  }
});

// Mark as started after initialization
async function initializeApp() {
  await connectDatabase();
  await connectRedis();
  await warmCache();
  isStarted = true;
  console.log("Application started and ready");
}

// Start health check server on separate port
const healthServer = healthApp.listen(8081, () => {
  console.log("Health check server running on :8081");
});

export { healthApp, healthServer, initializeApp, isStarted };

```

### Kubernetes Deployment with Health Checks

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:

        - name: order-service
          image: order-service:1.2.3
          ports:

            - containerPort: 3000
              name: http

            - containerPort: 8081
              name: health

          # Startup probe: Give app time to initialize
          startupProbe:
            httpGet:
              path: /health/startup
              port: health
            initialDelaySeconds: 5
            periodSeconds: 5
            failureThreshold: 30  # 5 * 30 = 150s max startup time

          # Liveness probe: Restart if deadlocked
          livenessProbe:
            httpGet:
              path: /health/live
              port: health
            periodSeconds: 10
            failureThreshold: 3   # 30s before restart
            timeoutSeconds: 5

          # Readiness probe: Remove from service if not ready
          readinessProbe:
            httpGet:
              path: /health/ready
              port: health
            periodSeconds: 5
            failureThreshold: 2   # 10s before removed from endpoints
            timeoutSeconds: 3
            successThreshold: 1   # Must succeed once to be ready

          resources:
            requests:
              cpu: 100m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi

          lifecycle:
            preStop:
              exec:
                command: ["/bin/sh", "-c", "sleep 10"]

```

### Graceful Shutdown Health Check

```typescript
import { healthServer } from "./health";

let isShuttingDown = false;

// Mark as not ready during shutdown
function updateReadiness() {
  // Override readiness to return 503 during shutdown
  healthServer.removeAllListeners("request");
  healthServer.on("request", (req, res) => {
    if (req.url === "/health/ready") {
      res.writeHead(503);
      res.end(JSON.stringify({ status: "shutting_down" }));
      return;
    }
    // Forward other requests (health/live still works)
    healthApp(req, res);
  });
}

// Graceful shutdown
async function gracefulShutdown(signal: string) {
  console.log(`Received ${signal}, starting graceful shutdown`);
  isShuttingDown = true;
  updateReadiness();

  // Wait for in-flight requests to complete
  const maxWaitMs = 30_000;
  const start = Date.now();

  // Stop accepting new connections
  const mainServer = getMainServer();
  mainServer.close(() => {
    console.log("Main server closed");
  });

  // Wait for existing connections to drain
  while (mainServer.connections > 0 && Date.now() - start < maxWaitMs) {
    console.log(`Waiting for ${mainServer.connections} connections to drain...`);
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  // Close health server
  healthServer.close();

  // Close database connections
  await db.end();
  await redis.quit();

  console.log("Shutdown complete");
  process.exit(0);
}

process.on("SIGTERM", () => gracefulShutdown("SIGTERM"));
process.on("SIGINT", () => gracefulShutdown("SIGINT"));

```

### Health Check with Circuit Breaker

```typescript
import CircuitBreaker from "opossum";

interface DependencyHealth {
  name: string;
  status: "healthy" | "unhealthy" | "circuit_open";
  latencyMs: number;
  circuitState: string;
  error?: string;
}

// Circuit breaker for each dependency
const dbBreaker = new CircuitBreaker(checkDatabase, {
  timeout: 5000,
  errorThresholdPercentage: 50,
  resetTimeout: 30000,
  rollingCountTimeout: 10000,
  rollingCountBuckets: 10,
});

const redisBreaker = new CircuitBreaker(checkRedis, {
  timeout: 3000,
  errorThresholdPercentage: 50,
  resetTimeout: 30000,
});

dbBreaker.on("open", () => console.warn("DB circuit breaker OPEN"));
dbBreaker.on("halfOpen", () => console.info("DB circuit breaker HALF_OPEN"));
dbBreaker.on("close", () => console.info("DB circuit breaker CLOSED"));

async function checkWithCircuitBreaker(
  breaker: CircuitBreaker,
  name: string
): Promise<DependencyHealth> {
  const start = Date.now();
  const circuitState = breaker.open ? "circuit_open" : breaker.halfOpen ? "half_open" : "closed";

  try {
    await breaker.fire();
    return {
      name,
      status: "healthy",
      latencyMs: Date.now() - start,
      circuitState,
    };
  } catch (err) {
    if (circuitState === "circuit_open") {
      return {
        name,
        status: "circuit_open",
        latencyMs: Date.now() - start,
        circuitState,
        error: "Circuit breaker is open — dependency unavailable",
      };
    }
    return {
      name,
      status: "unhealthy",
      latencyMs: Date.now() - start,
      circuitState,
      error: (err as Error).message,
    };
  }
}

app.get("/health/ready", async (_req, res) => {
  const checks = await Promise.all([
    checkWithCircuitBreaker(dbBreaker, "database"),
    checkWithCircuitBreaker(redisBreaker, "redis"),
  ]);

  const results = Object.fromEntries(checks.map((c) => [c.name, c]));

  const anyUnhealthy = checks.some((c) => c.status !== "healthy");
  res.status(anyUnhealthy ? 503 : 200).json({
    status: anyUnhealthy ? "unhealthy" : "healthy",
    checks: results,
  });
});

```

### Docker Health Check

```dockerfile
# Dockerfile
FROM node:20-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY dist/ ./dist/

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8081/health/live || exit 1

EXPOSE 3000 8081
CMD ["node", "dist/server.js"]

```

## Real-World Use Cases

1. **Kubernetes orchestration**: Liveness restarts deadlocked pods, readiness controls traffic routing

2. **Load balancer health**: AWS ALB/NLB use health checks to route only to healthy targets

3. **Service mesh**: Istio/Linkerd use health checks for traffic management and circuit breaking

4. **Blue-green deployments**: New environment passes health checks before traffic is switched

5. **Canary analysis**: Health check failure in canary triggers automatic rollback

6. **Database failover**: Health checks detect primary DB failure and trigger promotion

## Common Mistakes

| Mistake | Why It Hurts | Fix |
|---------|-------------|-----|
| Liveness check depends on external services | Pod restarts when DB is down (cascading failure) | Liveness should only check process state |
| No startup probe for slow apps | Liveness kills pod before it's ready | Add startup probe with generous timeout |
| Health endpoint does too much work | Health check itself causes timeouts | Keep checks lightweight (<100ms) |
| 200 OK always (even when unhealthy) | Load balancer keeps routing to broken instances | Return 503 when dependencies are down |
| No readiness drain time | In-flight requests dropped during scale-down | Use preStop hook with sleep |
| Health check port exposed publicly | Attackers can probe internal dependencies | Use separate port, restrict via network policy |

## Best Practices

1. **Separate liveness and readiness** — they serve different purposes

2. **Liveness = process only** — check memory, event loop, no external deps

3. **Readiness = dependencies** — check DB, cache, queues, external APIs

4. **Startup probe for slow starters** — prevents premature liveness kills

5. **Lightweight checks** — <100ms response time, no heavy queries

6. **Include version in response** — helps verify correct version is deployed

7. **Include dependency status** — so operators can see what's broken

8. **Monitor health check failure rate** — alert on readiness drops

9. **Use separate port** — health checks on port 8081, app on 3000
10. **Graceful shutdown** — mark not ready, drain connections, then exit

## Performance Considerations

- **Health check overhead** — each check makes DB/cache calls; keep total <100ms
- **Check caching** — cache health status for 5-10s to avoid hammering dependencies
- **Parallel checks** — `Promise.all()` for independent dependency checks
- **Timeout per check** — set 2-3s max per dependency to prevent health check hangs
- **Startup probe interval** — set longer intervals (5-10s) to avoid flooding during startup

## Summary

Health checks are the foundation of service reliability. Implement liveness (process state), readiness (dependency state), and startup (initialization) probes. Keep liveness independent of external services. Monitor health check failure rates and include dependency status in responses.

---

## See Also
- [Kubernetes](../14-Kubernetes/)
- [Performance Monitoring](../26-Performance-Monitoring/)
- [Serverless & Edge](../27-Serverless-Edge/)

## References & Learn More

- [Kubernetes Health Check Guide](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [Spring Boot Health Checks](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html)
- [AWS ALB Health Checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)
- [Istio Health Checks](https://istio.io/latest/docs/tasks/traffic-management/health-checks/)
- [Docker HEALTHCHECK](https://docs.docker.com/engine/reference/builder/#healthcheck)
- [Microservices Patterns - Health Check](https://microservices.io/patterns/observability/health-check-api.html)
