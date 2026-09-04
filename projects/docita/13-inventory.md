# 14 — Inventory

> Clinic stock with a movement ledger — every quantity change is an append-only `InventoryMovement`, and decrements are atomic conditional updates that can never drive stock negative.

---

## Context

Clinics stock medicines, consumables, and supplies. Inventory in Docita must answer:

- **What do we have?** — items with quantity, unit, SKU, supplier, batch, expiry.
- **Is anything running low or about to expire?** — the stats bar clinics actually look at: `totalItems`, `totalStock`, `lowStock`, `critical` (quantity 0), `expiringSoon` (30-day window).
- **Where did stock go?** — a movement ledger: INITIAL, IN (purchase/return), OUT (sale/use), EXPIRED, WASTE.
- **Can we sell/issue this?** — never allow a decrement that would take quantity below zero.

**The problems:** (1) quantity on the item row and the movement history must never disagree; (2) two concurrent issues of the last unit must not both succeed; (3) "low stock" must be *derived*, not hand-maintained; (4) prices mix a legacy `Float` column and a newer canonical `*Cents` column that must stay in sync.

---

## Decision 1: Ledger + Derived Quantity, Updated Atomically

### What We Chose

The item row carries the live `quantity`. Every mutation goes through `addMovementAndUpdateQuantity`, which inside one `$transaction` does a **conditional increment** and, only on success, appends the movement row:

```typescript
// apps/api/src/domains/inventory/infrastructure/repositories/prisma-inventory.repository.ts
async addMovementAndUpdateQuantity(itemId, clinicId, movementData, quantityDelta) {
  return this.prisma.$transaction(async (tx) => {
    const where: Prisma.InventoryItemWhereInput = { id: itemId, clinicId };
    if (quantityDelta < 0) where.quantity = { gte: Math.abs(quantityDelta) };  // never negative

    const updateResult = await tx.inventoryItem.updateMany({ where, data: { quantity: { increment: quantityDelta } } });
    if (updateResult.count === 0) {
      const existing = await tx.inventoryItem.findUnique({ where: { id: itemId }, select: { quantity: true } });
      if (!existing) throw new NotFoundException(...);
      throw new BadRequestException(`Insufficient stock: requested ${Math.abs(quantityDelta)} but only ${existing.quantity} available`);
    }
    return tx.inventoryMovement.create({ data: { inventoryItem: { connect: { id: itemId } }, clinic: { connect: { id: clinicId } }, ...movementData } });
  });
}
```

The sign convention is normalized in the command service — `OUT/EXPIRED/WASTE` become negative, everything else positive — and each movement records `createdBy`, `type`, and optional `referenceType`/`referenceId` (e.g., which invoice consumed it).

### Why This Was Chosen

- **The ledger and the balance can't drift** — both writes commit or neither does.
- **Negative stock is structurally impossible** — `updateMany` with `quantity >= |delta|` is a compare-and-swap at the database; a concurrent decrement of the last unit loses the race with `count === 0`, and the error message reports the actual remaining stock.
- **`OUT`, `EXPIRED`, and `WASTE` are explicit movement types**, so "we wrote off 40 units of expired amoxicillin" is auditable instead of a silent quantity edit.

### Alternatives Considered

- **Event-sourced stock** (quantity = sum of movements, never stored) — heavier read path (every item detail page aggregates history); with thousands of items and a handful of clinics, a stored quantity + append-only ledger is the right cost/benefit.
- **`update` then `create` without a guard** — rejected: a lost update between two concurrent issues could oversell the last unit.

### Trade-offs

- **Quantity is denormalized** — it can only be corrected by adding a movement; a manual "fix quantity" edit needs its own movement type (see What Could Be Better).
- **Single movement per call** — there is no bulk "dispense 5 items from one prescription" API yet; each line becomes its own transaction (see What Could Be Better).

---

## Decision 2: Low-Stock Is Derived, Not Stored

### What We Chose

`low_stock` is computed at query time by comparing `quantity` against the item's own `minQuantity` column:

```typescript
if (filters.status === 'low_stock') {
  where.quantity = { lte: this.prisma.inventoryItem.fields.minQuantity };  // field-to-field comparison
}
```

Stats (counts + aggregate + low/critical/expiring-soon) run as **five parallel reads** (`Promise.all`) on the read replica via `getReadClient()`.

### Why This Was Chosen

- Field-to-field Prisma comparison keeps the threshold per item — a clinic's par level for gloves differs from its par for antibiotics — without a nightly job re-computing flags.
- Read-replica + parallel queries keep the dashboard off the primary write path.

### Trade-offs

- **Expiry is a snapshot of "next 30 days from now"** — `expiringSoon` is computed with `now` injected via the clock port, so tests can pin time; there is no background job to *alert* on expiring stock, only the stats view.

---

## Decision 3: Cents as Canonical, Float Kept for Compatibility

### What We Chose

Create/update writes both `purchasePrice`/`sellingPrice` (legacy Float) and the canonical `purchasePriceCents`/`sellingPriceCents`, derived through `toCents`:

```typescript
// Write both the legacy Float and the canonical cents columns (G3).
purchasePrice: data.purchasePrice, sellingPrice: data.sellingPrice,
purchasePriceCents: toCents(data.purchasePrice), sellingPriceCents: toCents(data.sellingPrice),
```

This is the same money-handling rule the billing/payments domains follow (never store float currency as the source of truth).

### Why This Was Chosen

- **Consistency with the repo-wide money policy** — inventory value reports must match billing's cent-based math.
- **The Float columns remain for legacy callers** while the cents columns become the trustworthy basis for sums.

### Trade-offs

- **Dual-write is a migration hazard** — if a caller updates one pair and not the other, columns drift. The repository centralizes both write paths today (create + updateItem both sync cents), so the risk is contained to future bypasses.

---

## What Worked

- **Zero negative-stock incidents** — the conditional decrement held under concurrent use; the descriptive `Insufficient stock: requested X but only Y available` message made UI handling straightforward.
- **The movement ledger gave clinics real answers** — "where did the paracetamol go" is a filterable list, not a shrug.
- **Stats stay cheap** — read-replica parallel queries kept the dashboard snappy as item counts grew.

## What Failed

- **Item edit allowed direct quantity mutation** — `updateItem` accepts `quantity` in its data shape and writes it without a movement row. A staff member "fixing" a quantity that way silently breaks ledger continuity — the balance no longer equals the sum of movements. It was tolerated as an admin escape hatch, but it violates the domain's own invariant.
- **The initial `INITIAL` movement type was added late** — early items were created with quantity but no movement, so seed data lacked history. `createItem` now emits `INITIAL` when `quantity > 0`.

## What Could Be Better

- **Remove `quantity` from `updateItem` or route it through a `STOCK_ADJUST` movement** — the single biggest correctness hole in the domain (see What Failed).
- **Bulk consumption API** — dispensing a 6-line prescription is 6 sequential transactions today; a single `consumeMany` (one transaction, all-or-nothing) would match how clinics actually work and halve lock contention.
- **Per-batch expiry tracking** — expiry is on the item, not on each received batch; a clinic that buys the same medicine at different expiry dates can't issue oldest-first (FEFO) properly.
- **Reorder alerts** — `minQuantity` exists but nothing pushes a WhatsApp/notification when stock crosses it; the async queue + WhatsApp templates from other domains are ready to carry it.

---

## Code Evidence

| Claim | File |
| -------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Command service (create/update/movement) | `apps/api/src/domains/inventory/application/services/inventory-command.service.ts` |
| Query service + stats | `apps/api/src/domains/inventory/application/services/inventory-query.service.ts` |
| Facade | `apps/api/src/domains/inventory/application/services/inventory.service.ts` |
| Atomic ledger transaction | `apps/api/src/domains/inventory/infrastructure/repositories/prisma-inventory.repository.ts` |
| Repository interface (types) | `apps/api/src/domains/inventory/core/repositories/inventory.repository.interface.ts` |
| HTTP surface (`/inventory`, `:id/movements`) | `apps/api/src/domains/inventory/presentation/controllers/inventory.controller.ts` |

---

## Interview Script (60 seconds)

> "Inventory is a ledger, not a CRUD table. The item row carries a live quantity, but every change flows through one transactional method that does a conditional increment — for decrements the WHERE clause requires `quantity >= amount`, so stock can never go negative and two concurrent issues of the last unit can't both succeed — and only on success appends an immutable movement row recording type, user, and reference. Balance and history are written in the same transaction, so they can't drift. Low stock is derived per item against its own `minQuantity` at query time, stats run as parallel read-replica queries, and prices are dual-written with canonical cent columns matching the billing domain. The gap I'd fix first: `updateItem` can still mutate quantity directly, bypassing the ledger — that should become a `STOCK_ADJUST` movement so the invariant 'balance equals sum of movements' always holds."
---

[← Previous: IPD Inpatient](12-ipd-inpatient.md) · [ Back to Index](INDEX.md) · [Next: Analytics And Dashboards →](14-analytics-and-dashboards.md)
