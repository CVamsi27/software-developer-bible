# 04 — Payment Flows

> Three payment rails that must never mix — financial compliance in healthcare SaaS.

---

## Context

Docita handles money in three distinct contexts:

1. **Clinic's own payments** — a clinic configures their Razorpay account to accept patient payments
2. **Patient pays clinic** — patients pay for consultations, prescriptions, lab tests
3. **Clinic pays Docita** — clinics pay Docita for their SaaS subscription

**The risk:** If a developer accidentally uses Docita's Razorpay merchant key for a patient payment, Docita receives the patient's money instead of the clinic. This is a financial compliance issue that could result in legal action.

---

## Decision: Three Separate Injection Sites

### Flow A: Clinic's Razorpay Credentials (Optional)

Each clinic can optionally configure their own Razorpay API keys. These are stored in the clinic's settings JSON field.

```text
Clinic Settings → Razorpay Key ID + Key Secret → Used for patient payments
```

**Why optional:** Some clinics prefer at-desk payments (cash/UPI/POS) and don't need online payment integration.

### Flow B: Patient Pays Clinic

When a patient pays online, the system uses the clinic's own Razorpay credentials (Flow A). The money goes directly to the clinic's Razorpay account.

```typescript
// apps/api/src/domains/billing/application/services/razorpay-invoice-webhook.service.ts
private async handlePaymentCaptured(payload) {
  const payment = payload.payload.payment?.entity;

  // Idempotency: skip if we already processed this payment
  const existing = await this.repository.findByProviderPaymentId('razorpay', payment.id);
  if (existing) return;

  // Find the session this payment belongs to
  const session = await this.repository.findByProviderSessionId(payment.order_id);
  if (!session || !session.invoiceId || !session.patientId) throw new BadRequestException('...');

  // Process: update session + transition invoice + append outbox event
  await this.transactionRunner.run(async (tx) => {
    await this.repository.updatePaymentSession(session.id, { providerPaymentId: payment.id, ... }, tx);
    await this.invoiceRepository.transitionStatus(session.invoiceId, InvoiceStatus.PAID, tx);
    await this.outbox.append(tx, { eventName: ApplicationEvents.PAYMENT_CAPTURED, ... });
  });
}
```

**Key design decisions:**

1. **Idempotency check first** — Razorpay can send the same webhook multiple times. Check `findByProviderPaymentId` before processing.

2. **Transaction wrapping** — session update + invoice transition + outbox event happen in one transaction. If any fails, all roll back.

3. **Outbox for downstream events** — the payment event triggers receipt WhatsApp, dashboard update, and analytics. These go through the outbox for reliable delivery.

### Flow C: Docita SaaS Subscription

Clinics pay Docita for their subscription using a *separate* Razorpay merchant account. This uses different API keys and a different webhook endpoint.

```typescript
// apps/api/src/domains/subscriptions/application/webhooks/razorpay/handlers/payment-captured.webhook-handler.ts
// This handler processes Docita's own subscription payments — NOT patient payments
```

**Separation enforcement:**

| Aspect | Flow B (Patient → Clinic) | Flow C (Clinic → Docita)                                                    |
|--------|--------------------------|-------------------------                                                     |
| **Razorpay keys** | `CLINIC_INVOICE_PAYMENT_LINK_PROVIDER_TOKEN` | `DOCITA_PLATFORM_PAYMENT_LINK_PROVIDER_TOKEN` |
| **Webhook endpoint** | `/api/billing/webhooks/razorpay` | `/api/subscriptions/webhooks/razorpay`                 |
| **Domain** | `billing` | `subscriptions`                                                                         |
| **Merchant** | Clinic's Razorpay account | Docita's Razorpay account                                             |

---

## Alternatives Considered

| Option | Pros | Cons                                                                                 |
|--------|------|------                                                                                |
| **Single Razorpay account** | Simple | All payments mixed, can't separate clinic vs Docita revenue   |
| **Three separate accounts (chosen)** | Clear separation | More configuration, more webhook endpoints |
| **Stripe instead of Razorpay** | Better DX, global | Not popular in India, higher fees for INR       |
| **Payment abstraction layer** | Could swap providers | Over-engineering at current scale             |

### Why Razorpay

- **India-focused** — Razorpay is the dominant payment gateway in India
- **UPI support** — patients pay via UPI (most common method in Indian clinics)
- **Subscription support** — Razorpay supports recurring payments for SaaS subscriptions
- **Webhook reliability** — at-least-once delivery with signature verification

### Why Three Separate Accounts (Not One)

**The alternative:** Use one Razorpay account for everything. Simpler configuration.

**Why rejected:** If Docita uses one account, patient payments and subscription payments are mixed in the same dashboard. When a clinic disputes a charge, Docita can't easily separate "patient paid clinic" from "clinic paid Docita." Tax reporting becomes a nightmare. Separate accounts provide clean separation.

---

## What Worked

- **Zero payment mix-ups** — naming conventions + separate injection sites prevent accidental cross-flow usage
- **Idempotent webhook processing** — duplicate webhooks are harmlessly ignored
- **Transaction safety** — payment + invoice update + outbox event are atomic

## What Failed

- **Invoice double-crediting** — Razorpay sent the same `payment.captured` webhook twice within 5 seconds. The second webhook created a duplicate payment record and double-credited the clinic's wallet. Fixed by checking `findByProviderPaymentId` before processing and adding a unique constraint on `(provider, providerPaymentId)`.

- **Flow B technical debt** — Flow B still delegates to a shared adapter instead of resolving a clinic-scoped provider from Flow A settings. This means if a clinic hasn't configured their Razorpay keys, the system falls back to a default adapter. This should be resolved by dynamically resolving the provider from clinic settings.

## What Could Be Better

- **Payment provider abstraction** — currently tightly coupled to Razorpay. A `PaymentProvider` interface would allow swapping to Stripe or other providers.

- **Webhook signature verification** — we verify Razorpay signatures but don't have a generic HMAC verification middleware for other webhook sources.

- **Payment reconciliation dashboard** — no automated reconciliation between Razorpay dashboard and Docita's invoice records. Manual process currently.

- **Refund handling** — refunds are initiated through Razorpay dashboard, not through Docita's API. An in-app refund flow would improve UX.

---

## Code Evidence

| Claim | File                                                                                                       |
|-------|------                                                                                                      |
| Razorpay webhook handler | `apps/api/src/domains/billing/application/services/razorpay-invoice-webhook.service.ts` |
| Invoice command service | `apps/api/src/domains/billing/application/services/invoices-command.service.ts`          |
| Payment session repository | `apps/api/src/domains/billing/core/repositories/payment-session.repository.ts`        |
| Subscription webhook handlers | `apps/api/src/domains/subscriptions/application/webhooks/razorpay/handlers/`       |
| Payment flow docs | `docs/product/PAYMENT_FLOWS.md`                                                                |
| Payment gateway adapter | `apps/api/src/domains/payments/infrastructure/adapters/razorpay/`                        |

---

## Interview Script (60 seconds)

> "Docita handles three distinct payment flows that must never mix. Flow B: patients pay clinics using the clinic's own Razorpay credentials. Flow C: clinics pay Docita for subscriptions using Docita's separate Razorpay account. The separation is enforced through naming conventions (`CLINIC_INVOICE_PAYMENT_LINK_PROVIDER_TOKEN` vs `DOCITA_PLATFORM_PAYMENT_LINK_PROVIDER_TOKEN`), separate webhook endpoints, and separate domain modules. The key challenge was idempotency — Razorpay sends webhooks at-least-once, so we check for existing payment records before processing. A payment + invoice transition + outbox event happen in one transaction for atomicity. We hit a production issue where duplicate webhooks double-credited a clinic's wallet — fixed with a unique constraint on `(provider, providerPaymentId)`."
