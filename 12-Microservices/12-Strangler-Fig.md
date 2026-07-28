---
section: Microservices
category: Architecture
tags: [concept]
---

# Strangler Fig Pattern

## Definition

The **Strangler Fig Pattern** (also called the Strangler Pattern) is a strategy for incrementally migrating a legacy monolithic application to a modern architecture — typically microservices. Named after strangler fig vines that gradually envelop a host tree, the pattern works by creating a new system alongside the old one, routing functionality to the new system piece by piece, and eventually retiring the legacy system entirely when the migration is complete.

## Why Do We Need It?

1. **Risk reduction** — Incremental migration reduces blast radius of failures
2. **Business continuity** — The legacy system keeps running during the migration
3. **Incremental value** — New features can be delivered during the migration
4. **Parallel running** — Both systems coexist until migration is complete
5. **Rollback capability** — Easy rollback by switching traffic back to legacy
6. **Team autonomy** — Different teams can migrate different modules independently

## How It Works

### Basic Flow

```text
Strangler Fig Migration Phases:
═══════════════════════════════════════════════════════════════

Phase 1: Initial State (Monolith)
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  User → [Legacy Monolith] → Database                        │
│                                                              │
│  All functionality lives in the monolith                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘

Phase 2: Strangle Layer Introduced
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  User → [Strangler Facade/Gateway]                          │
│                  │                                           │
│          ┌───────┴────────┐                                  │
│          ▼                ▼                                   │
│  [Legacy Monolith]  [New Microservice A]                    │
│          │                │                                   │
│          └───────┬────────┘                                  │
│                  ▼                                           │
│             [Database]                                       │
│                                                              │
│  Some routes go to new microservice, rest go to monolith     │
│                                                              │
└─────────────────────────────────────────────────────────────┘

Phase 3: Gradual Migration
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  User → [Strangler Facade/Gateway]                          │
│                  │                                           │
│          ┌───────┬───────┬────────┐                          │
│          ▼       ▼       ▼        ▼                          │
│  [Legacy]   [Svc A]  [Svc B]  [Svc C]                      │
│  (shrinking)                                                │
│                                                              │
│  More features migrated over time as microservices           │
│                                                              │
└─────────────────────────────────────────────────────────────┘

Phase 4: Complete Migration
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  User → [API Gateway]                                       │
│                  │                                           │
│          ┌───────┬───────┬────────┐                          │
│          ▼       ▼       ▼        ▼                          │
│       [Svc A]  [Svc B]  [Svc C]  [Svc D]                   │
│                                                              │
│  Legacy monolith is retired/decommissioned                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

### Migration Strategies

```text
Migration Approaches:
═══════════════════════════════════════════════════════════════

1. URL/Route-Based Strangling
├── Identify URL patterns that map to specific functionality
├── Route /api/users/* → New User Service
├── Route /api/orders/* → New Order Service
└── Route /api/* (remaining) → Legacy monolith

2. Feature-Based Strangling
├── Identify features/domains to migrate
├── Extract feature with bounded context
├── Route feature-specific calls to new service
└── Repeat for each feature

3. Database-Driven Strangling
├── Identify database schema domains
├── Extract schema tables to new service's DB
├── Implement dual-write during migration
└── Cut over reads to new service

```

## Code Examples

### 1. Strangler Facade (Gateway)

```typescript
// strangler-facade.ts — API Gateway routing logic
import express from 'express';

const app = express();

// Configuration — which routes go to which service
const serviceMap = {
  // Migrated to new microservice
  '/api/v2/users': { target: 'http://user-service:3001', migrated: true },
  '/api/v2/products': { target: 'http://product-service:3002', migrated: true },
  '/api/v2/orders': { target: 'http://order-service:3003', migrated: true },

  // Still in legacy monolith
  '/api/v2/inventory': { target: 'http://legacy-monolith:8080', migrated: false },
  '/api/v2/reports': { target: 'http://legacy-monolith:8080', migrated: false },
};

// Proxy middleware
app.all('/api/v2/*', async (req, res) => {
  // Find the matching service
  const matchedRoute = Object.entries(serviceMap)
    .find(([route]) => req.path.startsWith(route));

  if (!matchedRoute) {
    return res.status(404).json({ error: 'Route not found' });
  }

  const [route, config] = matchedRoute;

  try {
    // Proxy the request
    const targetUrl = `${config.target}${req.path.replace('/api/v2', '')}`;
    const response = await fetch(targetUrl, {
      method: req.method,
      headers: req.headers as HeadersInit,
      body: req.method !== 'GET' ? JSON.stringify(req.body) : undefined,
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (error) {
    // If new service fails, fall back to legacy
    if (config.migrated) {
      console.warn(`Service failed, falling back to legacy: ${req.path}`);
      const legacyUrl = `http://legacy-monolith:8080${req.path}`;
      const fallback = await fetch(legacyUrl, {
        method: req.method,
        headers: req.headers as HeadersInit,
        body: req.method !== 'GET' ? JSON.stringify(req.body) : undefined,
      });
      const fallbackData = await fallback.json();
      return res.status(fallback.status).json(fallbackData);
    }

    res.status(500).json({ error: 'Service unavailable' });
  }
});
```

### 2. Feature Flag Integration

```typescript
// feature-flags.ts — Control migration percentage
interface FeatureFlag {
  name: string;
  enabled: boolean;
  percentage: number; // 0-100
  newServiceUrl: string;
}

const featureFlags: Record<string, FeatureFlag> = {
  'user-search': {
    name: 'User Search',
    enabled: true,
    percentage: 50, // 50% of traffic goes to new service
    newServiceUrl: 'http://user-search-service:3004',
  },
  'order-history': {
    name: 'Order History',
    enabled: false, // Not yet ready for production traffic
    percentage: 0,
    newServiceUrl: 'http://order-history-service:3005',
  },
};

// Migration router with feature flags
async function migrationRouter(req: Request): Promise<Response> {
  const featureName = extractFeatureName(req.url);
  const flag = featureFlags[featureName];

  // If feature not flagged, route to legacy
  if (!flag || !flag.enabled) {
    return proxyToLegacy(req);
  }

  // Percentage-based routing
  const userId = extractUserId(req);
  const userHash = hashUserId(userId);

  if (userHash < flag.percentage) {
    // Route to new service
    try {
      return await proxyToNewService(req, flag.newServiceUrl);
    } catch (error) {
      // Fall back to legacy on failure
      console.warn(`New service failed for ${featureName}, falling back`);
      return proxyToLegacy(req);
    }
  }

  // Route to legacy
  return proxyToLegacy(req);
}
```

### 3. Database Migration (Dual Write)

```typescript
// database-migration.ts — Dual-write pattern
import { db as legacyDb } from './legacy-database';
import { db as newDb } from './new-database';

class OrderMigrationService {
  async createOrder(orderData: Order) {
    // Write to both databases during migration
    const [legacyOrder, newOrder] = await Promise.all([
      legacyDb.orders.create({ data: orderData }),
      newDb.orders.create({ data: orderData }),
    ]);

    return newOrder;
  }

  async getOrder(orderId: string) {
    // Read from new service first, fall back to legacy
    try {
      return await newDb.orders.findUnique({ where: { id: orderId } });
    } catch {
      const legacyOrder = await legacyDb.orders.findUnique({
        where: { id: orderId },
      });

      // Sync to new database (backfill)
      if (legacyOrder) {
        await newDb.orders.create({ data: legacyOrder }).catch(() => {});
      }

      return legacyOrder;
    }
  }

  async migrateBatch(limit: number = 1000) {
    // Backfill existing data from legacy to new
    const orders = await legacyDb.orders.findMany({
      take: limit,
      orderBy: { createdAt: 'asc' },
      where: {
        migratedAt: null, // Not yet migrated
      },
    });

    for (const order of orders) {
      await newDb.orders.upsert({
        where: { id: order.id },
        create: order,
        update: order,
      });

      await legacyDb.orders.update({
        where: { id: order.id },
        data: { migratedAt: new Date() },
      });
    }

    return orders.length;
  }

  async verifyConsistency() {
    // Compare counts between old and new databases
    const [legacyCount, newCount] = await Promise.all([
      legacyDb.orders.count(),
      newDb.orders.count(),
    ]);

    const discrepancy = Math.abs(legacyCount - newCount);
    const isConsistent = discrepancy === 0;

    return {
      consistent: isConsistent,
      legacyCount,
      newCount,
      discrepancy,
    };
  }
}
```

### 4. Parallel Run with Comparison

```typescript
// parallel-run.ts — Run both systems and compare results
import { logger } from './observability';

class ParallelRunValidator {
  async validateAndCompare(feature: string, request: Request) {
    // Run both systems simultaneously
    const [legacyResult, newResult] = await Promise.all([
      this.callLegacy(feature, request),
      this.callNewService(feature, request),
    ]);

    // Compare results
    const match = this.deepCompare(legacyResult, newResult);

    if (!match) {
      // Log discrepancy for investigation
      logger.warn('Parallel run mismatch detected', {
        feature,
        request: request.url,
        legacyResult: legacyResult,
        newResult: newResult,
        timestamp: new Date().toISOString(),
      });

      // Return legacy result to avoid breaking users
      return legacyResult;
    }

    logger.info('Parallel run match', {
      feature,
      responseTime: {
        legacy: legacyResult.responseTime,
        new: newResult.responseTime,
      },
    });

    // Return either result (they match)
    return newResult;
  }

  private deepCompare(a: any, b: any): boolean {
    try {
      return JSON.stringify(a) === JSON.stringify(b);
    } catch {
      return false;
    }
  }

  private async callLegacy(feature: string, request: Request) {
    const start = Date.now();
    const response = await fetch(`http://legacy-monolith/${feature}`, {
      method: request.method,
      headers: request.headers,
      body: request.body,
    });
    return {
      status: response.status,
      data: await response.json(),
      responseTime: Date.now() - start,
    };
  }

  private async callNewService(feature: string, request: Request) {
    const start = Date.now();
    const response = await fetch(`http://new-service/${feature}`, {
      method: request.method,
      headers: request.headers,
      body: request.body,
    });
    return {
      status: response.status,
      data: await response.json(),
      responseTime: Date.now() - start,
    };
  }
}
```

### 5. Migration Orchestrator

```typescript
// migration-orchestrator.ts
interface MigrationStep {
  feature: string;
  status: 'pending' | 'in-progress' | 'validating' | 'completed' | 'rolled-back';
  startDate?: Date;
  completionDate?: Date;
  percentage: number; // Current traffic percentage
}

class MigrationOrchestrator {
  private migrations: MigrationStep[] = [];

  async startMigration(feature: string): Promise<void> {
    console.log(`Starting migration for: ${feature}`);

    // Phase 1: Extract and isolate (2 weeks)
    await this.extractService(feature);
    console.log(`  ✅ Extracted ${feature} as independent service`);

    // Phase 2: Shadow traffic (1 week)
    await this.runShadowTraffic(feature);
    console.log(`  ✅ Shadow traffic validated for ${feature}`);

    // Phase 3: Percentage rollout (2 weeks)
    await this.gradualRollout(feature);
    console.log(`  ✅ ${feature} at 100% traffic`);

    // Phase 4: Legacy cleanup (1 week)
    await this.cleanupLegacy(feature);
    console.log(`  ✅ Legacy ${feature} decommissioned`);

    this.migrations.push({
      feature,
      status: 'completed',
      completionDate: new Date(),
      percentage: 100,
    });
  }

  private async extractService(feature: string): Promise<void> {
    // Extract code, data, and deploy as new service
    console.log(`  📦 Extracting ${feature} codebase...`);
    console.log(`  🗄️  Migrating ${feature} data...`);
    console.log(`  🚀 Deploying ${feature} service...`);
  }

  private async runShadowTraffic(feature: string): Promise<void> {
    // Run both systems, compare results, don't serve new
    console.log(`  👻 Running shadow traffic for ${feature}...`);
    console.log(`  📊 Comparing ${feature} response accuracy...`);
  }

  private async gradualRollout(feature: string): Promise<void> {
    const percentages = [1, 5, 10, 25, 50, 75, 90, 100];

    for (const pct of percentages) {
      console.log(`  🔄 Routing ${pct}% of ${feature} traffic to new service`);
      await this.monitorForErrors(feature, pct);

      if (await this.hasErrors(feature)) {
        console.log(`  ⚠️  Rolling back ${feature} from ${pct}%`);
        await this.rollback(feature);
        return;
      }
    }
  }

  private async cleanupLegacy(feature: string): Promise<void> {
    console.log(`  🧹 Removing ${feature} from legacy monolith`);
    console.log(`  📝 Updating documentation for ${feature}`);
    console.log(`  ✅ ${feature} migration complete`);
  }

  private async monitorForErrors(feature: string, percentage: number): Promise<void> {
    // Wait and observe error rates
    await new Promise(resolve => setTimeout(resolve, 1000));
  }

  private async hasErrors(feature: string): Promise<boolean> {
    // Check error rates from monitoring
    return false;
  }

  private async rollback(feature: string): Promise<void> {
    console.log(`  ↩️  Rolling back ${feature} to legacy system`);
  }
}
```

## Real-World Use Cases

| Scenario | Migration Pattern | Key Considerations |
|----------|-------------------|-------------------|
| **E-commerce monolith** | Route-based strangling | Start with catalog (read-heavy), then cart/checkout |
| **Banking system** | Feature-based strangling | Audit trail, regulatory compliance, dual-write for 6+ months |
| **SaaS platform** | Database-driven strangling | Tenant isolation, backfill schedule, zero-downtime cutover |
| **Legacy CRM** | Facade/API gateway | Handle custom integrations, report parity |
| **Payment processing** | Parallel run + comparison | Exact financial matching, reconciliation |

## Common Mistakes

### 1. Big Bang Cutover

```text
// ❌ BAD: Trying to migrate everything at once
Risk:
├── Massive blast radius
├── Difficult to roll back
├── Teams overwhelmed
└── Users impacted for extended period

// ✅ GOOD: Incremental migration
Benefits:
├── Small blast radius
├── Easy rollback (one feature at a time)
├── Teams can focus
└── Users see continuous improvement
```

### 2. Not Having a Rollback Plan

```text
// ❌ BAD: No rollback strategy
Issue:
├── New service has bug
├── Old code already removed
├── No way to go back
└── Outage!

// ✅ GOOD: Always keep legacy running
Benefits:
├── Instant rollback to legacy
├── Feature flag toggle
├── Canary deployments
└── Zero downtime rollback
```

### 3. Ignoring Data Consistency

```typescript
// ❌ BAD: Eventual consistency without verification
// No reconciliation between old and new databases

// ✅ GOOD: Implement verification
async function reconcileData() {
  const discrepancies = await findDiscrepancies();
  if (discrepancies.length > 0) {
    await resolveDiscrepancies(discrepancies);
  }
}
```

### 4. Premature Optimization

```text
// ❌ BAD: Migrating everything to microservices
Issue:
├── High upfront cost
├── Team not ready for operational complexity
├── Many modules work fine as-is
└── Increased latency from over-splitting

// ✅ GOOD: Migrate only what needs to scale
Benefits:
├── Lower risk
├── Lower cost
├── Team learns incrementally
└── Focus on high-value migrations
```

## Best Practices

1. **Start with read-heavy, low-risk features** — Reporting, search, catalog

2. **Keep the strangler facade simple** — It's a temporary routing layer

3. **Implement feature flags** — Gradual traffic shifting with instant rollback

4. **Run both systems in parallel** — Validate correctness before cutting over

5. **Monitor aggressively** — Track error rates, latency, and data consistency

6. **Backfill data progressively** — Don't try to migrate all data at once

7. **Document the migration** — Keep a clear map of what's migrated and what's pending

8. **Set migration milestones** — Each migrated feature is a win

9. **Plan for legacy decommissioning** — Don't let the legacy system linger forever

10. **Communicate with stakeholders** — Track progress and impacts transparently

## Summary

- The Strangler Fig Pattern enables incremental migration from monolithic to microservices architecture
- A strangler facade/gateway routes traffic between legacy and new systems during migration
- Start with low-risk, read-heavy features and gradually increase traffic percentage
- Always keep the legacy system running until migration is fully validated
- Feature flags, parallel runs, and dual-write patterns help ensure safe migrations

## Cheat Sheet

```text
Strangler Fig Pattern Key Points:
├── What: Incrementally migrate monolith to microservices
├── How: Strangler facade routes traffic to new services
├── When: Modernizing legacy systems without downtime
├── Risk: Low — incremental, reversible
└── Duration: Months to years (not days)

Migration Phases:
├── Phase 1: Introduce strangler facade
├── Phase 2: Extract first feature as microservice
├── Phase 3: Route feature traffic to new service
├── Phase 4: Validate, increase traffic percentage
├── Phase 5: Decommission legacy feature
└── Repeat for each feature

Key Patterns:
├── URL-based routing → Simple, clean separation
├── Feature flags → Gradual rollouts, instant rollback
├── Dual-write → Database consistency during migration
├── Parallel run → Compare results before cutover
└── Shadow traffic → Test new service without impacting users

Common Mistakes:
├── Big bang migration
├── No rollback plan
├── Ignoring data consistency
├── Premature over-splitting
└── Not decommissioning legacy

Best Practices:
├── Start with read-heavy, low-risk features
├── Feature flags for gradual rollout
├── Monitor error rates and latency
├── Validate data consistency
├── Backfill data progressively
├── Document migration progress
├── Plan for legacy decommission
└── Communicate with stakeholders
```

---

## See Also

- [API Gateway](02-API-Gateway.md)
- [Circuit Breaker](04-Circuit-Breaker.md)
- [Distributed Transactions](11-Distributed-Transactions.md)
- [Event Sourcing](07-Event-Sourcing.md)
- [Interview Questions](08-Interview-Questions.md)
- [Service Discovery](01-Service-Discovery.md)
- [Service Mesh](10-Service-Mesh.md)

## References & Learn More

- [Martin Fowler: Strangler Fig Application](https://martinfowler.com/bliki/StranglerFigApplication.html)
- [Amazon: Strangler Fig Pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/strangler-fig-pattern/welcome.html)
- [Microsoft: Strangler Fig Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig)
- [Building Microservices by Sam Newman](https://www.amazon.com/Building-Microservices-designing-Systems/dp/1491950358)
- [Monolith to Microservices by Sam Newman](https://www.amazon.com/Monolith-Microservices-Evolutionary-Patterns-Transform/dp/1492047848)
