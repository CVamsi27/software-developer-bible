---
section: Database
category: Backend
tags: [concept]
---

# Database Migrations & Zero-Downtime Schema Changes

> **TL;DR:** Migrations are how you evolve a live database without taking the app offline. The senior pattern is **expand → backfill → contract**: add the new column/table in a non-breaking way, write the data, then drop the old shape. Lock-free migrations, batched backfills, and a feature-flag gate are the three tools that keep the production database from becoming a hostage.
>
> **Why it matters:** This is a Backend interview topic you will be asked about at the senior level (5+ YoE) — not for definition recall, but for tradeoffs, production failure modes, and the ability to compare it against alternatives.

## Definition

A **migration** is a versioned, ordered, reversible change to the database schema (DDL) and sometimes data (DML). **Zero-downtime migration** is the practice of evolving a live, high-traffic database without locking tables for long, without dropping data, and without taking the app offline — using the **expand → backfill → contract** pattern. Senior engineers know the difference between a one-shot migration (fine for a small greenfield app) and a multi-phase deployment (mandatory for any production database serving real traffic).

## Why Do We Need It?

1. **Reproducibility** — Every environment (dev, staging, prod) has the same schema; a new database is one command away.
2. **Auditability** — Migrations are committed, reviewed, and rolled back — the schema change history is a git log.
3. **Coordination** — Multiple engineers and multiple deploys per day need a single source of truth for schema state.
4. **Zero downtime** — A long `ALTER TABLE` on a large table blocks writes; senior engineers avoid it.
5. **Rollback safety** — A bad migration must be reversible; a destructive migration (DROP) without a backup is a resume-generating event.
6. **Backward compatibility** — Old app versions must keep working until they are fully rolled over — schema and code in lockstep.
7. **Data integrity** — Backfills must be idempotent and resumable; a half-finished backfill is worse than no backfill.

## How It Works

### Expand → Backfill → Contract

```text
Phase 1: EXPAND
  - Add new column (nullable or with default)
  - Add new table
  - App writes to BOTH old and new
  - Backward compatible: old app version still works

Phase 2: BACKFILL
  - Batched copy of old → new (e.g. 10k rows at a time)
  - Idempotent: rerunnable
  - Progress: log rows remaining; resumable from cursor
  - Run during low-traffic window if expensive

Phase 3: SWITCH READS
  - App reads from new shape
  - Old app version still works (reads/writes both)
  - Cutover: feature flag, dual-read dual-write validation

Phase 4: CONTRACT
  - Drop old column, drop old table
  - Remove dual-write code
  - Update tests
  - Now you can require the new app version
```

### Migration Tooling

| Tool | Style | Notes |
|------|-------|-------|
| Prisma Migrate | Declarative, schema-first | Generates SQL; drift detection; good for greenfield |
| Drizzle / Kysely | Type-safe query builder with migrations | Strong TS inference; explicit SQL |
| Flyway / Liquibase | SQL/XML/YAML files, versioned | Java-heavy, mature, used in enterprise |
| Alembic | SQLAlchemy migrations (Python) | Autogenerate, branch and merge |
| golang-migrate | Plain SQL files | Library only; no ORM lock-in |
| Rails Active Record | DSL in Ruby | `add_column`, `add_index`; convention over config |
| `pgroll` | Expand/contract for Postgres | Open-source; native zero-downtime |

## Code Examples

### Prisma Migration

```bash
# Edit schema.prisma
# model User { id String @id email String name String? newColumn String? }
npx prisma migrate dev --name add_user_new_column
# creates ./prisma/migrations/20250115_add_user_new_column/migration.sql
npx prisma migrate deploy   # production
```

```sql
-- generated SQL
ALTER TABLE "User" ADD COLUMN "newColumn" TEXT;
```

### Knex.js Migration

```typescript
// migrations/20250115_add_user_new_column.ts
import { Knex } from 'knex';

export async function up(knex: Knex): Promise<void> {
  await knex.schema.alterTable('User', (t) => {
    t.string('newColumn').nullable();
  });
}

export async function down(knex: Knex): Promise<void> {
  await knex.schema.alterTable('User', (t) => {
    t.dropColumn('newColumn');
  });
}
```

### Zero-Downtime: Expand → Backfill → Contract

```typescript
// Phase 1: EXPAND — add new column (safe, no lock)
await knex.schema.alterTable('orders', (t) => {
  t.decimal('total_cents', 10, 0).nullable();   // new column
});

// Phase 2: BACKFILL — batched copy of old → new
async function backfillOrders(batchSize = 5000) {
  let lastId = 0;
  for (;;) {
    const rows = await knex('orders')
      .where('id', '>', lastId)
      .whereNull('total_cents')
      .orderBy('id')
      .limit(batchSize)
      .select('id', 'total');                 // old column: 'total' is a decimal

    if (rows.length === 0) break;

    await knex.transaction(async (trx) => {
      for (const r of rows) {
        await trx('orders')
          .where({ id: r.id })
          .update({ total_cents: Math.round(Number(r.total) * 100) });
      }
    });
    lastId = rows[rows.length - 1].id;
    console.log(`Backfilled up to id=${lastId}`);
  }
}

// Phase 3: SWITCH — app reads from total_cents (dual-write code path)
// Phase 4: CONTRACT — drop the old column
await knex.schema.alterTable('orders', (t) => {
  t.dropColumn('total');
});
```

### Lock-Free Index Creation in Postgres

```sql
-- ❌ Blocks writes for the duration of the build
CREATE INDEX idx_orders_created_at ON orders (created_at);

-- ✅ Concurrent build; takes longer, but doesn't lock
CREATE INDEX CONCURRENTLY idx_orders_created_at ON orders (created_at);
```

### Safe Default Backfill (Postgres 11+)

```sql
-- Adding a NOT NULL column with a non-volatile default used to rewrite the table.
-- Postgres 11+ stores the default in the catalog and backfills lazily.
ALTER TABLE orders ADD COLUMN status TEXT NOT NULL DEFAULT 'pending';
-- For a 100M-row table this is still expensive to backfill on first read;
-- the lazy backfill is the trick, not zero work.
```

### Feature-Flag Gated Cutover

```typescript
// orders.service.ts
async createOrder(dto: CreateOrderDto) {
  if (this.flags.isEnabled('orders.write_to_new_table')) {
    return this.newTable.create(dto);
  }
  return this.legacyTable.create(dto);
}

async getOrder(id: string) {
  if (this.flags.isEnabled('orders.read_from_new_table')) {
    return this.newTable.findById(id);
  }
  return this.legacyTable.findById(id);
}
```

### Reversible, Resumable Backfill Job

```typescript
// jobs/backfill-orders.ts
@Injectable()
export class BackfillOrdersJob {
  @Cron('*/5 * * * *')   // every 5 min
  async run() {
    const cursor = await this.cursorStore.get('backfill:orders');
    const rows = await this.ordersOld.find({ id: { $gt: cursor } }).limit(1000);
    if (rows.length === 0) return this.cursorStore.delete('backfill:orders');

    await this.ordersNew.insertMany(rows.map(transform));   // idempotent via PK
    await this.cursorStore.set('backfill:orders', rows[rows.length - 1].id);
  }
}
```

## Real-World Use Cases

1. **Renaming a column** — Add new column, dual-write, backfill, switch reads, drop old column. 4 deploys minimum.
2. **Splitting a table** — Create new table, dual-write, backfill, switch reads, deprecate old table.
3. **Adding a NOT NULL column** — Add nullable, backfill in batches, set NOT NULL after the backfill is verified complete.
4. **Adding an index on a hot table** — `CREATE INDEX CONCURRENTLY` to avoid blocking writes.
5. **Migrating a primary key type** — Add new column, dual-write, switch reads, drop old — usually 6+ deploys.
6. **Changing a JSON shape** — Add new field with version key, backfill from old, switch readers, deprecate old field.
7. **Multi-tenant schema split** — New schema/DB, dual-write, migrate tenants one at a time, drop old.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `ALTER TABLE ADD COLUMN NOT NULL` without default | Always add nullable first, backfill, then `SET NOT NULL` after |
| `CREATE INDEX` (not CONCURRENTLY) on a hot table | Use `CREATE INDEX CONCURRENTLY` |
| One big migration in one deploy | Expand → backfill → contract across 4+ deploys |
| Backfill that locks rows | Batch with explicit cursor; never `UPDATE` every row in one statement |
| Backfill that isn't idempotent | Use primary key + `ON CONFLICT DO NOTHING` so reruns are safe |
| Dropping a column in the same deploy as the new column is in use | Wait at least one full release cycle before contracting |
| Destructive change without a backup | Snapshot the table or take a `pg_dump` before any destructive migration |
| Long-running migration in a single transaction | Batch in chunks; commit per chunk; resumable on failure |
| Schema and code deploy out of order | Schema first (backward compatible), then code, then schema contract |
| No rollback migration | Every `up` must have a tested `down`; if it can't be reversed, that's a flag |

## Best Practices

1. **Migrations are code** — Reviewed in PRs, versioned in git, runnable in CI; never one-off SQL run against prod.
2. **Backward compatible schema only** — Never break a running app; if you need to, you need a multi-phase plan.
3. **Expand → backfill → contract** — Default pattern for any non-trivial change.
4. **Batch backfills** — 1k–10k rows per batch; commit per batch; resumable on failure; log progress.
5. **Use `CREATE INDEX CONCURRENTLY`** — Never lock writes for an index build on a hot table.
6. **Add nullable first, `SET NOT NULL` after** — Avoid table rewrites for `NOT NULL` defaults where possible.
7. **Dual-write + dual-read** — Validate the new shape with shadow reads before cutting over.
8. **Feature-flag the cutover** — `orders.read_from_new_table` so you can flip back in seconds.
9. **Snapshot before destructive ops** — `pg_dump` or DB snapshot; test the restore.
10. **Track schema drift in CI** — Prisma `migrate diff`, Flyway `validate`, or a shadow DB; catch "the migration ran on staging but not prod" before it ships.
11. **Run migrations separately from app deploys** — `migrate deploy` is its own step; app deploys can roll back independently.
12. **Have a kill switch** — A way to stop the backfill job if it hammers the database; throttle, not abort.

## Performance Considerations

- `ALTER TABLE ADD COLUMN` on a billion-row table is minutes-to-hours of write lock; never do it.
- `CREATE INDEX CONCURRENTLY` takes 2–10× longer than `CREATE INDEX` but is non-blocking.
- Backfill batches of 1k–10k rows balance throughput and lock duration; tune for your workload.
- Use `LIMIT` + cursor; never `UPDATE` every row in one statement.
- Schedule heavy backfills during low-traffic windows; throttle, monitor, alert.
- Postgres autovacuum will be aggressive during a backfill; tune `maintenance_work_mem` if you have headroom.
- The "lazy default" trick in Postgres 11+ avoids the table rewrite but still has a small per-row cost on first read; benchmark on a representative sample.

## Summary

- Migrations are versioned, ordered, reversible schema changes committed with the code.
- Zero-downtime is the **expand → backfill → contract** pattern across 4+ deploys.
- Always `CREATE INDEX CONCURRENTLY` on hot tables; always add nullable first, `SET NOT NULL` after backfill.
- Dual-write + dual-read with a feature flag is the safe cutover.
- Every destructive op needs a backup, a tested rollback, and a kill switch.

## Cheat Sheet

| Concept | Description |
|---------|-------------|
| Migration | Versioned, ordered, reversible schema change |
| `up` / `down` | Forward and reverse migration functions |
| Expand | Add new column/table; backward compatible with old app version |
| Backfill | Batched, idempotent, resumable copy of old → new |
| Contract | Drop the old column/table once the new shape is the source of truth |
| `CREATE INDEX CONCURRENTLY` | Non-blocking index build; takes longer but doesn't lock writes |
| `ALTER TABLE ... ADD COLUMN ... NULL` | Safe; no table rewrite if no default |
| `SET NOT NULL` after backfill | Promote a nullable column after all rows are filled |
| Dual-write | App writes to both old and new during cutover |
| Dual-read | App reads from both and compares during validation |
| Feature flag | Cutover is a flag flip, not a deploy |
| `pg_dump` snapshot | Mandatory before any destructive migration |
| `migrate deploy` | Run pending migrations; never auto-run in app boot |
| Schema drift | Schema in DB ≠ schema in code; catch in CI |

---

## See Also
- [Microservices](../12-Microservices/) (migrations across services)
- [REST APIs](../07-REST-API/) (API versioning pairs with DB versioning)
- [System Design](../11-System-Design/) (migrations in zero-downtime deploys)
- [Performance Monitoring](../26-Performance-Monitoring/) (migration performance impact)

## References & Learn More

- [Prisma Migrate](https://www.prisma.io/docs/orm/prisma-migrate)
- [Flyway](https://flywaydb.org/)
- [Liquibase](https://www.liquibase.org/)
- [pgroll — Zero-downtime Postgres migrations](https://github.com/xataio/pgroll)
- [Strong Migrations — Rails](https://github.com/ankane/strong_migrations)
- [PostgreSQL — ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html)
- [Expand and Contract Pattern — Pramod Sadalage](https://www.sadalage.com/blog/2014/12/16/expand-and-contract-pattern-for-database-migration/)
- [Refactoring Databases — Scott Ambler](https://www.ambysoft.com/books/refactoringDatabases.html)
