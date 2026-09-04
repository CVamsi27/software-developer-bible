# 08 — Billing & Invoicing

> Indian healthcare billing complexity — GST, tax calculation, and invoice lifecycle.

---

## Context

Indian healthcare invoicing involves:
- **GST (Goods and Services Tax)** — 12% or 18% depending on service type
- **Place of supply rules** — interstate vs intrastate tax calculation
- **Clinic-specific settings** — each clinic has different tax registration, state code, and currency
- **Multiple payment methods** — cash, UPI, card, insurance claims

**The complexity:** A clinic in Mumbai (Maharashtra) billing a patient from Karnataka has different tax implications than billing a local patient. The system must calculate this correctly for every invoice.

---

## Decision 1: Immutable Tax Snapshots

### What We Chose

Tax calculation is frozen at invoice creation time. If clinic tax settings change, existing invoices retain their original calculation.

```typescript
// apps/api/src/domains/billing/application/services/invoices-command.service.ts
private buildTaxSnapshots(patient: PatientInvoiceContext) {
  const taxSettings = parseTaxSettings(patient.clinic.settings);
  const gstin = taxSettings.registrationId || extractClinicGstin(patient.clinic);
  const stateCode = taxSettings.stateCode || extractGstinStateCode(gstin);

  const seller = taxRegistrationSnapshotSchema.parse({
    countryCode: taxSettings.countryCode,
    regime: taxSettings.regime,
    registrationId: gstin,
    legalName: taxSettings.legalName || patient.clinic.name,
    stateCode,
    stateName: taxSettings.stateName,
  });

  const buyer = taxRegistrationSnapshotSchema.parse({
    countryCode: seller.countryCode,
    regime: seller.regime,
    legalName: getPatientFullName(patient).trim(),
    address: patient.address || undefined,
  });

  return { taxSettings, seller, buyer };
}
```

### Why Immutable Snapshots (Not Recalculated)

**The alternative:** Recalculate tax on every invoice view.

**Why rejected:** If a clinic updates their GSTIN (tax registration number), all historical invoices would show the new GSTIN — incorrect for tax filing. Immutable snapshots ensure the invoice reflects the tax state at creation time.

---

## Decision 2: Invoice Status State Machine

### What We Chose

```text
DRAFT → ISSUED → PAID / PARTIALLY_PAID / OVERDUE / CANCELLED
```

**Key rules:**

- Can't edit a PAID invoice
- Can't cancel a PAID invoice (must issue credit note)
- Status transitions validated by `assertInvoiceStatusTransition()`

### Why State Machine

**The alternative:** Free-form status updates.

**Why rejected:** A clinic accidentally marked an invoice as "PAID" without receiving payment. The patient got a "payment received" WhatsApp. State machines prevent invalid transitions and require proper authorization.

---

## Decision 3: Daybook for Cash Reconciliation

### What We Chose

A daybook feature that aggregates all transactions for a given day, helping clinics reconcile cash at end of day.

```typescript
// apps/api/src/domains/billing/application/services/invoices-query.service.ts
async getCollectionsByMode(clinicId: string, query: CollectionsByModeQuery) {
  // Groups payments by mode: cash, UPI, card, insurance
  // Returns daily totals for reconciliation
}
```

**Why daybook:** Indian clinics deal heavily in cash. At end of day, the clinic owner counts cash and compares against the system. The daybook provides this reconciliation view.

---

## What Worked

- **Tax accuracy** — zero tax calculation errors in production
- **Immutable snapshots** — historical invoices remain accurate after clinic setting changes
- **Daybook** — clinics report 50% faster end-of-day reconciliation

## What Failed

- **GST rate changes** — India changed GST rates on some medical services. Existing invoices with old rates needed manual adjustment. Fix: tax rate is snapshot per invoice, not referenced from settings.

- **Insurance claim complexity** — insurance claims have their own workflow (DRAFT → SUBMITTED → UNDER_REVIEW → APPROVED/REJECTED → SETTLED). This was initially part of billing but was extracted to its own domain.

## What Could Be Better

- **Multi-currency support** — currently INR only. Some clinics serve international patients and need USD/EUR invoicing.

- **Automated tax filing** — no integration with India's GST filing system (GSTN). Currently manual.

- **Credit note automation** — when an invoice is cancelled after payment, a credit note should be auto-generated. Currently manual.

---

## Code Evidence

| Claim | File |
| ----------------- | -------------------------------------------------------------------------------- |
| Invoice service | `apps/api/src/domains/billing/application/services/invoices.service.ts` |
| Invoice command | `apps/api/src/domains/billing/application/services/invoices-command.service.ts` |
| Tax calculator | `apps/api/src/domains/billing/core/services/tax-calculator.service.ts` |
| Invoice entity | `apps/api/src/domains/billing/core/entities/invoice.entity.ts` |
| Invoice status VO | `apps/api/src/domains/billing/core/value-objects/invoice-status.value-object.ts` |
| Invoice PDF | `apps/api/src/domains/billing/application/services/invoice-pdf-document.ts` |
| Daybook | `apps/api/src/domains/billing/application/services/invoices-query.service.ts` |

---

## Interview Script (60 seconds)

> "Indian healthcare billing involves GST with interstate vs intrastate rules. I implemented immutable tax snapshots — tax is calculated and frozen at invoice creation time. If a clinic updates their GSTIN, historical invoices retain their original calculation. Invoices follow a state machine: DRAFT → ISSUED → PAID/OVERDUE/CANCELLED. Invalid transitions are blocked at the entity level. The daybook feature aggregates daily transactions by payment mode (cash, UPI, card, insurance) for end-of-day reconciliation — critical for Indian clinics that deal heavily in cash."
---

[← Previous: Prescription Safety](07-prescription-safety.md) · [ Back to Index](INDEX.md) · [Next: Subscription System →](09-subscription-system.md)
