# Connection Pooling

## Definition

Connection pooling is a technique that maintains a cache of database connections for reuse by applications. Instead of creating a new connection for each request, the application borrows a connection from the pool, uses it, and returns it. This reduces the overhead of establishing connections and improves application performance.

## Why Do We Need It?

- **Reduced Overhead**: Avoid TCP handshake, authentication for each query
- **Better Performance**: Reuse existing connections instead of creating new ones
- **Resource Management**: Limit maximum concurrent connections
- **Scalability**: Handle more concurrent users with fewer connections
- **Reliability**: Connection health checks and automatic recovery

## How It Works

### Connection Pool Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Connection Pool Architecture              │
│                                                             │
│  Application Servers                                        │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐                      │
│  │ Server 1│ │ Server 2│ │ Server 3│                      │
│  └────┬────┘ └────┬────┘ └────┬────┘                      │
│       │           │           │                             │
│       └───────────┼───────────┘                             │
│                   ▼                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Connection Pool                         │   │
│  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐        │   │
│  │  │Conn │ │Conn │ │Conn │ │Conn │ │Conn │ ...     │   │
│  │  │  1  │ │  2  │ │  3  │ │  4  │ │  5  │        │   │
│  │  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘        │   │
│  │                                                     │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │  Pool Manager                                │   │   │
│  │  │  • Min connections                           │   │   │
│  │  │  • Max connections                           │   │   │
│  │  │  • Idle timeout                              │   │   │
│  │  │  • Connection validation                     │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
│                   │                                         │
│                   ▼                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              PostgreSQL Server                       │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │  Max Connections: 100                        │   │   │
│  │  │  Active: 45    Idle: 10    Waiting: 5       │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Pool States

```
┌─────────────────────────────────────────────────────────────┐
│                    Connection Pool States                     │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ACTIVE: Connection in use by application            │   │
│  │  • Borrowed from pool                              │   │
│  │  • Counted against max connections                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  IDLE: Connection available for reuse               │   │
│  │  • In pool waiting for request                      │   │
│  │  • May be closed after idle timeout                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  WAITING: Request waiting for connection             │   │
│  │  • All connections in use                           │   │
│  │  • Will timeout after connection timeout            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  CLOSED: Connection removed from pool               │   │
│  │  • Exceeded idle timeout                           │   │
│  │  • Failed validation                               │   │
│  │  • Server closed connection                        │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### PgBouncer Configuration

```ini
; pgbouncer.ini
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
; Pool mode
pool_mode = transaction  ; or session, statement

; Connection settings
max_client_conn = 1000
default_pool_size = 25
min_pool_size = 5
reserve_pool_size = 5
reserve_pool_timeout = 3

; Timeouts
server_idle_timeout = 600
client_idle_timeout = 0
query_timeout = 0

; Logging
log_connections = 1
log_disconnections = 1
log_pooler_errors = 1

; Authentication
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
```

### Prisma Connection Pool

```prisma
// schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  // Connection pool settings
  relationMode = "prisma"
}

// Or in environment
// DATABASE_URL="postgresql://user:pass@host:5432/db?connection_limit=20&pool_timeout=10"
```

```typescript
import { PrismaClient } from '@prisma/client';

// Prisma automatically manages connection pool
const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL,
    },
  },
  // Log queries for debugging
  log: ['query', 'info', 'warn', 'error'],
});

// Prisma handles connection pooling internally
// Each PrismaClient instance has its own pool
```

### Node.js pg Pool

```typescript
import { Pool } from 'pg';

// Create connection pool
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,                    // Maximum connections
  min: 5,                     // Minimum connections
  idleTimeoutMillis: 30000,   // Close idle connections after 30s
  connectionTimeoutMillis: 5000,  // Fail after 5s if no connection
  allowExitOnIdle: true,      // Allow process to exit when idle
});

// Use pool
async function getUser(id: number) {
  const client = await pool.connect();
  try {
    const result = await client.query('SELECT * FROM users WHERE id = $1', [id]);
    return result.rows[0];
  } finally {
    client.release();  // Return connection to pool
  }
}

// Or use pool.query directly (auto-releases)
async function getUserAuto(id: number) {
  const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
  return result.rows[0];
}

// Pool events
pool.on('connect', (client) => {
  console.log('New client connected');
});

pool.on('error', (err) => {
  console.error('Unexpected error on idle client', err);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  pool.end();
});
```

### Connection Pool Monitoring

```sql
-- Check PostgreSQL connections
SELECT
    datname,
    state,
    COUNT(*) AS count
FROM pg_stat_activity
GROUP BY datname, state;

-- Check connection limits
SELECT
    datname,
    numbackends AS current,
    max_conn AS max_connections
FROM pg_stat_database
JOIN (SELECT setting::int AS max_conn FROM pg_settings WHERE name = 'max_connections') s ON true
WHERE datname = current_database();

-- Check PgBouncer stats
SHOW POOLS;
SHOW CLIENTS;
SHOW SERVERS;
SHOW STATS;
```

## Real-World Use Cases

### Web Application

```typescript
// NestJS with Prisma
import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class DatabaseService extends PrismaClient
  implements OnModuleInit, OnModuleDestroy {
  async onModuleInit() {
    await this.$connect();
  }

  async onModuleDestroy() {
    await this.$disconnect();
  }
}

// In your service
@Injectable()
export class UsersService {
  constructor(private prisma: DatabaseService) {}

  async findAll() {
    return this.prisma.user.findMany();
  }
}
```

### Microservices

```typescript
// Each microservice has its own pool
// Service A
const poolA = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 10,
});

// Service B
const poolB = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 10,
});

// With PgBouncer in front
// PgBouncer manages connections to PostgreSQL
// Each service connects to PgBouncer
```

### Connection Pool Sizing

```typescript
// Calculate optimal pool size
// Rule of thumb: connections = (2 * CPU cores) + disk_spindles

// For a 4-core server with SSD:
const optimalPoolSize = 2 * 4 + 1;  // = 9 connections

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: optimalPoolSize,
  min: 2,
  idleTimeoutMillis: 30000,
});
```

## Common Mistakes

### 1. Not Using Connection Pooling

```typescript
// BAD: Creating new connection per query
async function getUser(id: number) {
  const client = new Client({ connectionString: process.env.DATABASE_URL });
  await client.connect();
  const result = await client.query('SELECT * FROM users WHERE id = $1', [id]);
  await client.end();
  return result.rows[0];
}

// GOOD: Using connection pool
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

async function getUser(id: number) {
  const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
  return result.rows[0];
}
```

### 2. Pool Exhaustion

```typescript
// BAD: Long-running queries exhaust pool
async function generateReport() {
  const result = await pool.query('SELECT * FROM large_table');  // Takes 30s
  return result.rows;
}

// GOOD: Use separate pool for long queries
const reportPool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 5,  // Separate pool for reports
});

async function generateReport() {
  const result = await reportPool.query('SELECT * FROM large_table');
  return result.rows;
}
```

### 3. Not Handling Connection Errors

```typescript
// BAD: No error handling
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

// GOOD: Handle errors
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
});

pool.on('error', (err) => {
  console.error('Pool error:', err);
  // Implement recovery logic
});
```

## Best Practices

```typescript
// 1. Configure pool size appropriately
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,                    // Max connections
  min: 5,                     // Min connections
  idleTimeoutMillis: 30000,   // Close idle connections
  connectionTimeoutMillis: 5000,  // Connection timeout
});

// 2. Always release connections
async function query(text: string, params?: any[]) {
  const client = await pool.connect();
  try {
    return await client.query(text, params);
  } finally {
    client.release();
  }
}

// 3. Use connection timeout
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  connectionTimeoutMillis: 5000,  // Fail after 5s
});

// 4. Monitor pool health
setInterval(() => {
  console.log('Pool stats:', {
    total: pool.totalCount,
    idle: pool.idleCount,
    waiting: pool.waitingCount,
  });
}, 30000);

// 5. Graceful shutdown
process.on('SIGTERM', async () => {
  await pool.end();
  process.exit(0);
});

// 6. Use PgBouncer for production
// PgBouncer manages connections efficiently
// Supports transaction-level pooling
```

## Performance Considerations

```
┌─────────────────────────────────────────────────────────────┐
│                    Pool Size Guidelines                      │
│                                                             │
│  Formula: connections = (2 * CPU cores) + disk_spindles     │
│                                                             │
│  Example: 4-core server with SSD                            │
│  connections = (2 * 4) + 1 = 9                             │
│                                                             │
│  Considerations:                                            │
│  • Each connection uses ~10MB RAM                           │
│  • Too many connections = context switching overhead        │
│  • Too few connections = request queuing                    │
│                                                             │
│  PgBouncer Pool Modes:                                      │
│  • Session: Connection held for entire session              │
│  • Transaction: Connection held for transaction             │
│  • Statement: Connection held for single statement          │
└─────────────────────────────────────────────────────────────┘
```

## Interview Questions

### Beginner (5)

1. **What is connection pooling?**
   Maintaining a cache of database connections for reuse.

2. **Why use connection pooling?**
   Reduces connection overhead, improves performance.

3. **What is PgBouncer?**
   Lightweight connection pooler for PostgreSQL.

4. **What is the difference between max and min pool size?**
   Max: upper limit of connections; Min: connections kept in pool.

5. **What is idle timeout?**
   Time after which idle connections are closed.

### Intermediate (5)

6. **What are PgBouncer pool modes?**
   Session, Transaction, Statement; each holds connection differently.

7. **How do you size a connection pool?**
   Based on CPU cores, workload, and response time.

8. **What is connection leak?**
   When connections are not returned to pool; causes exhaustion.

9. **What is connection validation?**
   Checking if connection is still alive before use.

10. **What is the difference between connection pool and thread pool?**
    Connection pool: manages DB connections; Thread pool: manages threads.

### Senior (10)

11. **How do you handle connection pool exhaustion?**
    Increase pool size, optimize queries, use separate pools.

12. **What is connection multiplexing?**
    Multiple logical connections over fewer physical connections.

13. **How does PgBouncer improve performance?**
    Reduces PostgreSQL connection overhead, enables transaction pooling.

14. **What is the impact of connection pool size on performance?**
    Too small: queuing; Too large: context switching, memory.

15. **How do you monitor connection pool health?**
    Track active, idle, waiting connections; alert on thresholds.

16. **What is connection timeout vs query timeout?**
    Connection timeout: time to get connection; Query timeout: time to execute.

17. **How do you handle connection failures in a pool?**
    Retry logic, health checks, automatic reconnection.

18. **What is the difference between connection pooling and query caching?**
    Connection pooling: reuses connections; Query caching: caches results.

19. **How do you implement connection pooling in Prisma?**
    Prisma manages pool internally; configure via DATABASE_URL parameters.

20. **What is the relationship between connection pool and transaction isolation?**
    Isolation level affects lock duration; impacts connection reuse.

### FAANG-style (5)

21. **Design a connection pool for 1 million concurrent users.**
    PgBouncer, multiple pools, read replicas, connection multiplexing.

22. **How do you handle connection pooling across regions?**
    Regional pools, connection routing, failover.

23. **Design a connection pool monitoring system.**
    Metrics, alerting, dashboards, auto-scaling.

24. **How do you optimize connection pool for microservices?**
    Service-specific pools, circuit breakers, bulkheads.

25. **Design a connection pool for serverless applications.**
    PgBouncer, connection proxies, stateless design.

### Follow-ups (5)

26. **What is the difference between connection pooling and connection reuse?**
    Pooling: manages connections; Reuse: uses same connection multiple times.

27. **How do you handle database failover with connection pooling?**
    PgBouncer health checks, automatic reconnection, DNS failover.

28. **What is the impact of connection pooling on ACID transactions?**
    Transaction mode: connection held for transaction; Session mode: held longer.

29. **How do you debug connection pool issues?**
    Monitor pool stats, check for leaks, analyze query performance.

30. **What is the difference between PgBouncer and PgPool-II?**
    PgBouncer: lightweight, fast; PgPool-II: more features, heavier.

## Summary

Connection pooling is essential for database performance. Use PgBouncer for production PostgreSQL. Configure pool size based on workload. Monitor pool health and handle connection failures. Prisma manages connection pooling internally.

## Cheat Sheet

```ini
# PgBouncer configuration
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
```

```typescript
// Node.js pg Pool
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  min: 5,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});

// Prisma
DATABASE_URL="postgresql://...?connection_limit=20&pool_timeout=10"
```

```sql
-- Monitor connections
SELECT * FROM pg_stat_activity;
SELECT * FROM pg_stat_database;
SHOW POOLS;  -- PgBouncer
```

## References & Learn More

- [PgBouncer Official Documentation](https://www.pgbouncer.org/config.html)
- [Prisma Connection Management](https://www.prisma.io/docs/concepts/components/prisma-client/working-with-prismaclient/connection-management)
- [Connection Pooling in PostgreSQL - PgPool-II](https://www.pgpool.net/)
- [Database Connection Pooling Best Practices - AWS](https://aws.amazon.com/blogs/database/fundamentals-of-optimizing-amazon-rds-proxy/)
- [Node.js PostgreSQL Connection Pooling - node-postgres](https://node-postgres.com/features/pooling)
