# 13 — Inventory: Commit the Stock Change and Its Movement Together

## Definition

Inventory maintains a current stock quantity and a history explaining how it changed. In Docita, the item holds the live balance while movement records identify receipts, consumption, expiry, waste and other adjustments.

Suppose two operators each issue the last unit. Reading quantity 1 and later decrementing without a condition can let both proceed. Separately recording history can also leave a changed balance without its movement when the second write fails.

This case describes source inspected on **2 October 2026**. It explains the guarded mutation path and the other paths that limit a whole-domain guarantee.

## First Principles

Concurrent readers can observe the same balance. The database must decide which decrement remains valid at the write, and the movement explaining that change must commit with it. A stored balance is a projection: it stays consistent with history only if every mutation follows the same accounting protocol.

Atomicity within one path does not protect callers that bypass it or repeated delivery of the same business operation.

## Why Store Both a Balance and Movements?

A stored quantity supports direct reads and conditional updates. A movement history supports explanations and reconciliation. Computing every balance from the history can simplify the source-of-truth rule but adds aggregation and concurrency-design work; retaining a projection trades that read cost for an obligation to keep it aligned.

The current movement types include INITIAL, IN, OUT, ADJUSTMENT, EXPIRED and WASTE. The command treats OUT/EXPIRED/WASTE as negative deltas and the other types as positive. In particular, ADJUSTMENT currently means a positive movement here, not automatically “set balance to this value.”

## How One Guarded Mutation Works

The repository transaction constructs an item/clinic predicate. For a negative delta, it additionally requires quantity to be at least the amount removed. It atomically increments quantity and, on success, inserts the movement through the same transaction client.

```text
transaction
  conditional update: quantity >= amount → quantity -= amount
  if no item matched: reject
  insert movement explaining the accepted delta
commit both, or roll back both
```

The SQL equivalent of the decisive predicate is:

```sql
UPDATE "InventoryItem"
SET quantity = quantity - 1
WHERE id = $1 AND "clinicId" = $2 AND quantity >= 1
RETURNING quantity;
```

This is a focused illustration of the Prisma conditional update, not the complete transaction. PostgreSQL coordinates concurrent writes to the same row. If the first decrement commits quantity 0, a competing decrement's condition cannot accept another unit from that balance.

| Step | Operator A | Operator B |
| ------------------ | ----------------------- | ----------------------------------------------- |
| Starting balance | 1 | 1 |
| Conditional update | Can accept one unit | Must wait or evaluate after the competing write |
| After A commits | Balance 0, one movement | Its quantity predicate fails |

If movement insertion fails, the transaction rolls the quantity update back. If the item cannot be updated, the repository attempts a diagnostic read; that read uses item ID without an explicit clinic predicate. Verify its tenant-routing context and avoid reporting another tenant's balance through an error. “No rows matched” does not always mean insufficient stock; it can also mean absent or unauthorized scope.

## Where the Balance and Ledger Can Still Diverge

The item edit API and command still accept `quantity`. `updateItem` writes it directly without appending a movement. This bypass exists in current source, so the earlier claim that every quantity change is ledger-backed is inaccurate.

Creation uses a nested INITIAL movement when initial quantity is positive. That protects the current create path, not historical data, manual SQL, other bypasses or database immutability. Calling a movement log append-only describes the desired protocol; enforce update/delete restrictions if immutability is required.

A repair should route stock corrections through an authorized adjustment protocol that records the difference and reason, or prevent direct quantity edits. Reconciliation should derive signed deltas from movement types because the stored movement quantity is a positive magnitude at the validated HTTP boundary.

### Repeated Business Operations Need Their Own Identity

The guard prevents overselling available stock through that path. It does not prevent the same invoice line from consuming stock twice when enough quantity remains. The schema/interface's reference fields explain a movement; their mere presence does not establish a unique idempotency constraint.

Select a business operation key and enforce duplicate handling where the mutation commits. Retrying after an ambiguous response must recognize the existing accepted movement rather than blindly subtracting again.

## How Input, Units and Money Affect the Invariant

The controller DTO validates nonnegative integer item quantities and positive integer movement quantities, and limits movement types to an enum. The command normalizes the direction. Verify that internal callers also satisfy those requirements and that values fit database integer and money ranges.

An inventory item carries a unit. Summing “quantity” across boxes, tablets and bottles yields a count with mixed units, not a physically meaningful stock volume. Report totals with their interpretation or group by compatible units.

The repository writes legacy floating-point prices and canonical `purchasePriceCents`/`sellingPriceCents` together through `toCents`, including price updates. Integer minor units support consistent calculations, but conversion still needs an agreed currency, scale, rounding and range. The name cents does not itself establish universal two-decimal currency behavior. Bypassing the centralized writer can leave the pairs inconsistent.

## How Low-Stock and Expiry Views Are Derived

The item list's low-stock filter compares quantity to the item's `minQuantity` field. The stats path performs five parallel reads through `getReadClient()`:

| Metric | Inspected definition |
| ------------- | --------------------------------------------------------- |
| Total items | Active item count |
| Total stock | Sum of active quantities; interpret mixed units carefully |
| Low stock | Positive quantity at or below the item's minimum |
| Critical | Quantity exactly zero |
| Expiring soon | Expiry after now and within 30 × 24 hours |

Zero-stock items can therefore appear in the list filter while being counted separately as critical in stats. Expiring-soon excludes already-expired stock. Its duration window is not the same definition as thirty clinic-calendar days.

`getReadClient()` permits configured read routing; it does not prove a replica exists in every deployment. Replica lag can delay a just-written balance, and parallel queries do not provide a shared snapshot. Use primary or suitable snapshot semantics when a decision requires current, internally consistent figures. Derived flags reduce stale materialized status fields but do not make all reads current.

## Real-World Decisions

| Requirement | Mechanism to evaluate | Remaining boundary |
| -------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------- |
| Last unit cannot be issued twice | Guarded row update | Other writers must preserve nonnegative stock |
| Balance matches movement history | Same-transaction update and movement | Direct edits and historical inconsistencies |
| Retry cannot consume twice | Unique business-operation identity | Ambiguous response and replay behavior |
| Multiple prescription lines succeed together | One multi-item transaction with stable lock ordering | Deadlocks, retries and transaction duration |
| Oldest-expiring batch issued first | Batch-level quantities and expiry policy | Item-level expiry cannot express multiple batches |
| Low stock alerts are reliable | Defined threshold-crossing event and delivery | Duplicate alerts and notification failures |

A bulk-consumption operation can express all-or-nothing issuance. It does not automatically halve contention: workload, lock ordering and transaction duration determine the result. Per-batch tracking and threshold alerts add distinct state and operational responsibilities rather than cosmetic UI improvements.

## Mistakes

- Presenting one guarded repository method as proof that all stock writers are safe.
- Calling a movement record immutable without enforced write restrictions.
- Assuming reference fields alone provide idempotency.
- Summing incompatible item units as if they represent one stock measure.
- Treating parallel replica reads as a consistent or immediately current snapshot.
- Quoting zero incidents or improved dashboard speed without measured evidence.

## Best Practices

Exercise concurrent last-unit decrements, failed movement insertion, duplicate business references, direct quantity edits and cross-tenant diagnostic paths. Reconcile the stored quantity with signed movement history and preserve an audit reason for repairs. Define bulk-operation atomicity, numerical bounds and read freshness before advertising the resulting guarantees.

## Summary

The guarded movement path protects its decrement and history in one transaction. Whole-domain correctness additionally requires closing direct-edit bypasses, enforcing business-operation idempotency, respecting units and money ranges, and choosing suitable read freshness.

## See Also

- [Category revision](REVISION.md) — stock and ledger questions after learning.
- [Clinic workflows](05-clinic-workflows.md) — concurrent state transitions.
- [Billing](08-billing-invoicing.md) — money and invoice records.
- [Analytics](14-analytics-and-dashboards.md) — read consistency and aggregation.
- [Case-study index](INDEX.md) — learning stages.

## References

Docita source inspected on 2 October 2026:

- `apps/api/src/domains/inventory/application/services/inventory-command.service.ts`
- `apps/api/src/domains/inventory/infrastructure/repositories/prisma-inventory.repository.ts`
- `apps/api/src/domains/inventory/application/dto/inventory.dto.ts`
- `apps/api/src/domains/inventory/presentation/controllers/inventory.controller.ts`
- `packages/db/prisma/schema.prisma` — inventory models.
- `packages/utils/src/billing/money-cents.ts` — price conversion boundary.
