# 09 — Subscription System

> SaaS monetization — tier gating, overage tracking, and the referral system.

---

## Context

Docita is a SaaS product. Clinics pay monthly subscriptions based on tier:

| Tier | Price | Features |
| -------------- | --------- | --------------------------------------- |
| **Free** | ₹0 | Basic scheduling, limited patients |
| **Starter** | ₹499/mo | Full scheduling, prescriptions, billing |
| **Pro** | ₹1,499/mo | WhatsApp, analytics, multi-doctor |
| **Enterprise** | Custom | API access, custom integrations, SLA |

**The challenge:** Feature gating must be enforced at every API endpoint without duplicating logic across 29 domains.

---

## Decision 1: Feature Gates via Decorator

### What We Chose

A `@Feature()` decorator that checks clinic tier before the endpoint executes:

```typescript
@Feature(WHATSAPP_MESSAGING)
@Post('send')
async sendMessage(@Body() dto: SendWhatsAppDto) {
  // Only reaches here if clinic has WhatsApp feature
}
```

```typescript
// apps/api/src/shared/modules/auth/utils/clinic-feature-access.util.ts
export function assertClinicHasFeatureOrThrow(clinic: ClinicFeatures, feature: Feature): void {
  if (!hasFeature(clinic, feature)) {
    throw new ForbiddenException(`Feature ${feature} not available on your plan`);
  }
}
```

### Why Decorator (Not Middleware)

**The alternative:** Global middleware that checks features on every request.

**Why rejected:** Not all endpoints need feature checks. Health checks, auth endpoints, and public booking don't need tier validation. Decorators are explicit — only checked endpoints are gated.

---

## Decision 2: Overage Tracking

### What We Chose

Usage is tracked per clinic per billing period. When usage exceeds tier limits, overage charges are calculated and invoiced.

```typescript
// apps/api/src/domains/billing/core/services/usage-tracking.service.ts
async recordUsageEvent(params: { clinicId, type, quantity?, entityType?, entityId? }) {
  return this.command.recordUsageEvent(params);
}

async trackWhatsAppMessage(clinicId, messageId, type) { ... }
async trackAICredits(clinicId, feature, entityId?) { ... }
async trackPatientActivity(clinicId, patientId) { ... }
async trackAppointment(clinicId, appointmentId) { ... }
async trackPrescription(clinicId, prescriptionId) { ... }
async trackInvoice(clinicId, invoiceId) { ... }
```

**Usage types tracked:**

- WhatsApp messages (template vs session)
- AI credits (per feature)
- Patient records
- Appointments
- Prescriptions
- Invoices
- OCR pages

### Why Track Everything (Not Just Billable Items)

**The alternative:** Only track items that are explicitly billed (e.g., WhatsApp messages).

**Why rejected:** Understanding usage patterns helps with pricing decisions. If 80% of clinics hit the patient record limit, the Free tier limit might be too low. Usage data informs product decisions.

---

## Decision 3: Subscription Lifecycle State Machine

### What We Chose

```text
PENDING → ACTIVE → PAST_DUE → GRACE_PERIOD → EXPIRED
                                    ↓
                              ACTIVE (payment resumed)
```

**Key rules:**

- `PAST_DUE` → 7-day grace period for payment retry
- `GRACE_PERIOD` → 3 more days before `EXPIRED`
- `EXPIRED` → clinic features disabled, data preserved
- Payment resume → immediate reactivation

### Why Grace Period (Not Hard Cut)

**The alternative:** Payment fails → immediately disable features.

**Why rejected:** A clinic's payment might fail due to temporary bank issues. Disabling their clinic management system mid-consultation would be catastrophic. Grace period gives time to resolve payment issues.

---

## Decision 4: Referral System

### What We Chose

Clinics earn credits for referring other clinics:

```typescript
// apps/api/src/domains/subscriptions/core/services/referral.service.ts
// Referrer gets credits when referee activates subscription
// Referee gets first-month discount
```

**Why referrals:** In India's clinic market, word-of-mouth is the primary acquisition channel. A referral incentive aligns with how clinics actually discover new tools.

---

## What Worked

- **Feature gating** — zero feature leakage (Free clinics accessing Pro features)
- **Usage tracking** — data-driven pricing decisions
- **Grace period** — zero involuntary churn from temporary payment failures

## What Failed

- **Overage calculation lag** — usage aggregation runs hourly. A clinic could exceed limits by 20% before the system notices. Fix: real-time usage checks for critical limits (e.g., patient records).

- **Razorpay subscription webhooks** — Razorpay sends multiple webhook types (activated, charged, halted, pending). Each needs a dedicated handler. Initially, we missed the `subscription.halted` event, leaving clinics in an inconsistent state.

## What Could Be Better

- **Usage-based pricing** — currently tier-based. A hybrid model (base tier + usage-based overage) would better align cost with value.

- **Self-serve plan changes** — currently plan changes require support intervention. A self-serve upgrade/downgrade flow would improve UX.

- **Annual billing** — currently monthly only. Annual plans with discounts would improve retention.

---

## Code Evidence

| Claim | File |
| ------------------------- | ------------------------------------------------------------------------------------------- |
| Feature decorator | `apps/api/src/shared/modules/auth/` |
| Usage tracking | `apps/api/src/domains/billing/core/services/usage-tracking.service.ts` |
| Subscription entity | `apps/api/src/domains/subscriptions/core/entities/subscription.entity.ts` |
| Razorpay webhook handlers | `apps/api/src/domains/subscriptions/application/webhooks/razorpay/handlers/` |
| Overage billing scheduler | `apps/api/src/domains/subscriptions/infrastructure/schedulers/overage-billing.scheduler.ts` |
| Referral service | `apps/api/src/domains/subscriptions/core/services/referral.service.ts` |

---

## Interview Script (60 seconds)

> "Docita uses tier-based SaaS pricing with feature gating via a `@Feature()` decorator. Usage is tracked per clinic per billing period across 7 dimensions (WhatsApp, AI credits, patients, appointments, prescriptions, invoices, OCR pages). When usage exceeds tier limits, overage charges are calculated hourly and invoiced. The subscription lifecycle follows a state machine: ACTIVE → PAST_DUE → 7-day grace period → EXPIRED. The grace period prevents involuntary churn from temporary payment failures. A referral system incentivizes word-of-mouth — the primary acquisition channel in India's clinic market."
---

[← Previous: Billing Invoicing](08-billing-invoicing.md) · [ Back to Index](INDEX.md) · [Next: Deployment Infrastructure →](10-deployment-infrastructure.md)
