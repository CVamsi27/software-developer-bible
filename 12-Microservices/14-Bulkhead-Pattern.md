# Bulkhead Pattern

[![Category: Architecture](https://img.shields.io/badge/category-Architecture-800080)](.)

## Definition

The **Bulkhead Pattern** is a resilience design pattern that isolates failures within a system by partitioning resources into separate pools (bulkheads). Named after the watertight compartments on ships that prevent flooding from sinking the entire vessel, the pattern ensures that a failure in one part of the system does not cascade to other parts. In microservices, bulkheads can be implemented at various levels: thread pools, connection pools, semaphores, queues, and even physical infrastructure.

## Why Do We Need It?

1. **Failure isolation** — A slow/down dependency only affects its own bulkhead, not the entire system
2. **Resource exhaustion protection** — Prevent one service from consuming all threads, connections, or memory
3. **Fair resource allocation** — Guarantee each tenant/customer gets a minimum level of service
4. **Graceful degradation** — Non-critical features can fail without taking down critical ones
5. **Cascading failure prevention** — Stop failures from propagating through the system

## How It Works

### Bulkhead Types

```text
Bulkhead Architecture:
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────┐
│                    BULKHEAD PATTERN TYPES                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Thread Pool Bulkhead:                                           │
│  ┌─────────────────────────┐   ┌─────────────────────────┐      │
│  │  Service A Pool         │   │  Service B Pool         │      │
│  │  ┌───┬───┬───┬───┐    │   │  ┌───┬───┬───┐         │      │
│  │  │ T │ T │ T │ T │    │   │  │ T │ T │ T │         │      │
│  │  └───┴───┴───┴───┘    │   │  └───┴───┴───┘         │      │
│  │  Max: 4 threads         │   │  Max: 3 threads         │      │
│  └─────────────────────────┘   └─────────────────────────┘      │
│                                                                  │
│  Semaphore Bulkhead:                                             │
│  ┌─────────────────────────┐   ┌─────────────────────────┐      │
│  │  Critical Endpoint      │   │  Non-Critical Endpoint  │      │
│  │  Permits: 10            │   │  Permits: 5             │      │
│  │  ┌──┬──┬──┬──┬──┬──┐  │   │  ┌──┬──┬──┬──┐         │      │
│  │  │P │P │P │P │P │P │  │   │  │P │P │P │P │         │      │
│  │  └──┴──┴──┴──┴──┴──┘  │   │  └──┴──┴──┴──┘         │      │
│  └─────────────────────────┘   └─────────────────────────┘      │
│                                                                  │
│  Connection Pool Bulkhead:                                       │
│  ┌─────────────────────────┐   ┌─────────────────────────┐      │
│  │  Database Pool          │   │  External API Pool      │      │
│  │  Max: 20 connections    │   │  Max: 5 connections     │      │
│  └─────────────────────────┘   └─────────────────────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

```

### With vs Without Bulkhead

```text
Without Bulkhead:
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│  ALL services share one thread pool                          │
│                                                              │
│  1 request to /slow-api (5s) → occupies 1 thread            │
│  10 requests to /slow-api → 10 threads occupied              │
│  /fast-api request → Queues... waits for /slow-api          │
│                                                              │
│  Result: Slow API consumes ALL threads → Fast API is DEAD   │
└─────────────────────────────────────────────────────────────┘

With Bulkhead:
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│  Fast API has its OWN thread pool                            │
│  Slow API has its OWN thread pool                            │
│                                                              │
│  /slow-api pool exhausted (10 requests)                     │
│  /fast-api pool still has available threads                  │
│                                                              │
│  Result: Slow API is degraded, Fast API works perfectly     │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### 1. Thread Pool Bulkhead (Generic)

```typescript
// bulkhead.ts — Thread pool bulkhead
class BulkheadPool {
  private active = 0;
  private queue: Array<{
    task: () => Promise<any>;
    resolve: (value: any) => void;
    reject: (reason: any) => void;
  }> = [];

  constructor(
    private maxConcurrent: number,
    private maxQueue: number,
    private name: string,
  ) {}

  async execute<T>(task: () => Promise<T>): Promise<T> {
    if (this.active < this.maxConcurrent) {
      return this.runTask(task);
    }

    if (this.queue.length >= this.maxQueue) {
      throw new Error(`Bulkhead [${this.name}]: Queue full (${this.maxQueue})`);
    }

    return new Promise<T>((resolve, reject) => {
      this.queue.push({ task: task as () => Promise<any>, resolve, reject });
    });
  }

  private async runTask<T>(task: () => Promise<T>): Promise<T> {
    this.active++;
    try {
      return await task();
    } finally {
      this.active--;
      this.processQueue();
    }
  }

  private processQueue(): void {
    if (this.queue.length > 0 && this.active < this.maxConcurrent) {
      const next = this.queue.shift()!;
      this.runTask(next.task).then(next.resolve).catch(next.reject);
    }
  }

  get stats() {
    return {
      name: this.name,
      active: this.active,
      queued: this.queue.length,
      maxConcurrent: this.maxConcurrent,
      maxQueue: this.maxQueue,
    };
  }
}
```

### 2. Service-Level Bulkheads

```typescript
// service-bulkheads.ts — Bulkhead configuration per service
import { BulkheadPool } from './bulkhead';

// Define bulkheads for each downstream service
const servicePools = {
  // Critical services get larger pools
  database: new BulkheadPool(10, 50, 'database'),
  paymentGateway: new BulkheadPool(5, 20, 'payment'),

  // Non-critical services get smaller pools
  analytics: new BulkheadPool(2, 10, 'analytics'),
  emailService: new BulkheadPool(3, 10, 'email'),
  recommendations: new BulkheadPool(2, 5, 'recommendations'),
};

// Usage in service calls
async function processOrder(order: Order) {
  const [customer, payment, invoice] = await Promise.all([
    // Each call goes through its own bulkhead
    servicePools.database.execute(() => db.getCustomer(order.customerId)),
    servicePools.paymentGateway.execute(() =>
      payment.charge(order.total, order.paymentMethod)),
    servicePools.database.execute(() => db.createInvoice(order)),
  ]);

  // Non-critical: if analytics fails, order still processes
  servicePools.analytics.execute(() =>
    analytics.track('order_placed', { orderId: order.id })
  ).catch(() => log.warn('Analytics failed, continuing'));

  return { customer, payment, invoice };
}

// Monitoring bulkhead health
function getBulkheadHealth() {
  const stats: Record<string, any> = {};
  for (const [name, pool] of Object.entries(servicePools)) {
    const s = pool.stats;
    stats[name] = {
      ...s,
      utilizationPercent: Math.round((s.active / s.maxConcurrent) * 100),
      queueUtilizationPercent: Math.round((s.queued / s.maxQueue) * 100),
    };
  }
  return stats;
}
```

### 3. Semaphore Bulkhead (Resilience4j style)

```typescript
// semaphore-bulkhead.ts
class SemaphoreBulkhead {
  private permits: number;
  private totalPermits: number;
  private queue: Array<{
    resolve: () => void;
    reject: (reason: any) => void;
  }> = [];
  private maxQueue: number;

  constructor(maxConcurrent: number, maxQueue: number = 0) {
    this.permits = maxConcurrent;
    this.totalPermits = maxConcurrent;
    this.maxQueue = maxQueue;
  }

  async execute<T>(task: () => Promise<T>): Promise<T> {
    await this.acquire();
    try {
      return await task();
    } finally {
      this.release();
    }
  }

  private acquire(): Promise<void> {
    if (this.permits > 0) {
      this.permits--;
      return Promise.resolve();
    }

    if (this.maxQueue > 0 && this.queue.length >= this.maxQueue) {
      return Promise.reject(new Error('Semaphore queue full'));
    }

    return new Promise<void>((resolve, reject) => {
      this.queue.push({ resolve, reject });
    });
  }

  private release(): void {
    if (this.queue.length > 0) {
      const next = this.queue.shift()!;
      next.resolve();
    } else {
      this.permits++;
    }
  }

  get availablePermits() { return this.permits; }
  get waitingCount() { return this.queue.length; }
}

// Usage with circuit breaker integration
class ResilientService {
  private bulkhead = new SemaphoreBulkhead(5, 10);

  async callExternalApi(request: Request): Promise<Response> {
    return this.bulkhead.execute(async () => {
      const response = await fetch('https://api.example.com', {
        method: 'POST',
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      return response.json();
    });
  }
}
```

### 4. Tenancy-Based Bulkheads

```typescript
// tenant-bulkheads.ts — Per-tenant resource isolation
class TenantBulkheadRegistry {
  private tenantPools = new Map<string, BulkheadPool>();

  // Each tenant gets an isolated pool
  getPool(tenantId: string): BulkheadPool {
    let pool = this.tenantPools.get(tenantId);

    if (!pool) {
      const maxConcurrent = this.getTenantLimit(tenantId);
      pool = new BulkheadPool(maxConcurrent, maxConcurrent * 5, `tenant-${tenantId}`);
      this.tenantPools.set(tenantId, pool);
    }

    return pool;
  }

  private getTenantLimit(tenantId: string): number {
    const tier = this.getTenantTier(tenantId);
    // Premium tenants get more resources
    switch (tier) {
      case 'premium': return 20;
      case 'business': return 10;
      case 'free': return 3;
      default: return 5;
    }
  }

  private getTenantTier(tenantId: string): string {
    // Look up tenant tier from database or cache
    return 'business';
  }
}

// Usage
const tenantBulkheads = new TenantBulkheadRegistry();

async function handleTenantRequest(tenantId: string, request: Request) {
  const pool = tenantBulkheads.getPool(tenantId);

  return pool.execute(async () => {
    // Process request for this tenant
    const data = await db.query(request.query);
    return { tenant: tenantId, data };
  });
}
```

### 5. Connection Pool Bulkhead

```typescript
// connection-pool-bulkhead.ts
import { Pool } from 'pg';

const databasePools = {
  // Separate connection pools for different workloads
  reads: new Pool({ max: 20, idleTimeoutMillis: 30000 }),
  writes: new Pool({ max: 10, idleTimeoutMillis: 30000 }),
  reporting: new Pool({ max: 5, idleTimeoutMillis: 60000 }),
};

// Queries are routed to the appropriate pool
async function queryRead(sql: string, params?: any[]) {
  return databasePools.reads.query(sql, params);
}

async function queryWrite(sql: string, params?: any[]) {
  return databasePools.writes.query(sql, params);
}

async function queryReport(sql: string, params?: any[]) {
  return databasePools.reporting.query(sql, params);
}
```

### 6. Web Server Bulkhead with Express

```typescript
import express from 'express';
import { BulkheadPool } from './bulkhead';

const app = express();

// Separate bulkheads for different API groups
const pools = {
  critical: new BulkheadPool(20, 100, 'critical'),
  background: new BulkheadPool(5, 20, 'background'),
  admin: new BulkheadPool(10, 30, 'admin'),
};

// Middleware to assign bulkhead based on path
app.use('/api/orders', (req, res, next) => {
  pools.critical.execute(() => new Promise<void>((resolve) => {
    next();
    resolve();
  })).catch(err => {
    res.status(503).json({ error: 'Too many requests - try later' });
  });
});

app.use('/api/analytics', (req, res, next) => {
  pools.background.execute(() => new Promise<void>((resolve) => {
    next();
    resolve();
  })).catch(err => {
    res.status(503).json({ error: 'Analytics unavailable' });
  });
});

// Metrics endpoint
app.get('/health/bulkheads', (req, res) => {
  res.json({
    critical: pools.critical.stats,
    background: pools.background.stats,
    admin: pools.admin.stats,
  });
});
```

## Real-World Use Cases

| Scenario | Bulkhead Type | Benefit |
|----------|--------------|---------|
| **API rate limiting per client** | Semaphore per API key | One client can't overload the system |
| **Database read vs write pools** | Connection pool separation | Write-heavy queries don't starve reads |
| **Multi-tenant SaaS** | Tenant-based thread pools | Noisy neighbor isolation |
| **Command vs Query (CQRS)** | Separate thread pools | Commands don't block queries |
| **Critical vs non-critical endpoints** | Resource budgets | Monitoring can fail, orders still process |
| **External dependency isolation** | Per-service bulkheads | Slow payment API doesn't block recommendations |

## Common Mistakes

### 1. Too Many Bulkheads

```typescript
// ❌ BAD: Over-partitioning creates management overhead
const pools = {
  userService: new BulkheadPool(3, 10),
  productService: new BulkheadPool(3, 10),
  cartService: new BulkheadPool(3, 10),
  searchService: new BulkheadPool(3, 10),
  reviewService: new BulkheadPool(3, 10),
  // ... 20 more services
};

// ✅ GOOD: Group by criticality
const pools = {
  critical: new BulkheadPool(15, 50),
  standard: new BulkheadPool(10, 30),
  background: new BulkheadPool(5, 15),
};
```

### 2. Bulkhead Without Queuing

```typescript
// ❌ BAD: No queue — requests are immediately rejected
class StrictBulkhead {
  async execute(task) {
    if (this.active >= this.max) {
      throw new Error('Bulkhead full'); // Immediate rejection
    }
    // ...
  }
}

// ✅ GOOD: Queue requests with backpressure
class QueueingBulkhead {
  async execute(task) {
    if (this.queue.length >= this.maxQueue) {
      throw new Error('Queue full'); // Only reject when queue is full
    }
    // Queue the task...
  }
}
```

### 3. Not Monitoring Bulkhead Saturation

```typescript
// ❌ BAD: No monitoring — you don't know when bulkheads are near capacity

// ✅ GOOD: Monitor and alert on saturation
function checkBulkheadHealth(pools: Map<string, BulkheadPool>) {
  for (const [name, pool] of pools) {
    const stats = pool.stats;
    const utilization = stats.active / stats.maxConcurrent;

    if (utilization > 0.8) {
      logger.warn(`Bulkhead ${name} at ${utilization * 100}% capacity`);
    }

    if (stats.queued > 0) {
      logger.info(`Bulkhead ${name} has ${stats.queued} queued requests`);
    }
  }
}
```

## Best Practices

1. **Group by criticality** — Critical (orders), Standard (profiles), Background (analytics)
2. **Size pools empirically** — Monitor actual usage and adjust pool sizes
3. **Always include queuing** — Reject only when queue is full, not immediately
4. **Combine with Circuit Breaker** — Bulkhead isolates, circuit breaker stops repeated failures
5. **Add timeouts** — Don't let queue items wait forever
6. **Monitor and alert** — Track pool utilization and queue depth
7. **Test failure scenarios** — Chaos engineering: simulate bulkhead exhaustion
8. **Document pool sizes** — Why each pool is sized the way it is

## Bulkhead + Circuit Breaker Integration

| Pattern | Purpose | Together |
|---------|---------|----------|
| **Bulkhead** | Isolates resources | Limits concurrent calls |
| **Circuit Breaker** | Stops repeated failures | Prevents wasted capacity |
| **Combined** | Resilient calling pattern | Bulkhead → CB → Task |

```typescript
// Combined bulkhead + circuit breaker
async function resilientCall<T>(service: string, task: () => Promise<T>): Promise<T> {
  const pool = bulkheads.get(service);
  const cb = circuitBreakers.get(service);

  return pool.execute(async () => {
    return cb.call(task);
  });
}
```

## Summary

- Bulkhead isolates resources into separate pools to prevent cascading failures
- Common implementations: thread pools, semaphore, connection pools, tenant-based
- Size pools based on criticality: critical services get more resources
- Always include queuing with a max queue size to handle bursts
- Combine with Circuit Breaker and Timeout patterns for comprehensive resilience

## Cheat Sheet

```typescript
// Thread pool bulkhead
class BulkheadPool {
  constructor(maxConcurrent: number, maxQueue: number, name: string) {}
  async execute<T>(task: () => Promise<T>): Promise<T> {}
  get stats(): { active: number; queued: number; maxConcurrent: number; maxQueue: number }
}

// Semaphore bulkhead
class SemaphoreBulkhead {
  constructor(maxConcurrent: number, maxQueue: number) {}
  async execute<T>(task: () => Promise<T>): Promise<T> {}
}

// Usage pattern
const pools = {
  critical: new BulkheadPool(15, 50, 'critical'),
  standard: new BulkheadPool(10, 30, 'standard'),
  background: new BulkheadPool(5, 15, 'background'),
};

const result = await pools.critical.execute(() => db.query(sql));
```

```text
Bulkhead Key Points:
├── Isolate: Separate pools per service/criticality/tenant
├── Protect: One failing component can't take down others
├── Size: Monitor actual usage, adjust empirically
├── Queue: Always queue (don't immediately reject)
├── Combine: Bulkhead + Circuit Breaker + Timeout
├── Monitor: Track utilization and queue depth
└── Test: Chaos engineering to validate isolation
```

---

## See Also

- [API Gateway](02-API-Gateway.md)
- [Circuit Breaker](04-Circuit-Breaker.md)
- [Distributed Transactions](11-Distributed-Transactions.md)
- [Interview Questions](08-Interview-Questions.md)
- [Rate Limiting](../07-REST-API/07-Rate-Limiting.md)
- [Resilience Patterns](09-gRPC.md)

## References & Learn More

- [Resilience4j: Bulkhead](https://resilience4j.readme.io/docs/bulkhead)
- [Microsoft: Bulkhead Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead)
- [Netflix: Bulkhead Patterns](https://netflixtechblog.com/bulkhead-patterns-for-resilient-systems-1a8f1e3c4e3a)
- [Build Resilient Microservices](https://www.oreilly.com/library/view/building-microservices/9781491950340/)
