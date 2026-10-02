# 04 — Payments: Keep Merchant Identity and Local State Consistent

## Definition

A payment integration connects a merchant account, provider-side payment state and local business records. Docita distinguishes clinic-owned payment configuration, patient-to-clinic collection and clinic-to-Docita SaaS billing.

The central problem is ownership: a patient's invoice payment must reach the intended clinic merchant, while a SaaS subscription payment belongs to Docita. A successful API call can still be wrong if it uses the wrong merchant credentials.

This case describes source inspected on **2 October 2026**. Intended separation is distinguished from current wiring; historical incidents and “zero mix-ups” outcomes are not asserted without evidence.

## First Principles

Merchant identity determines which account receives a provider transaction. Local tenant identity determines which clinic's records may change. Neither a dependency-injection token nor a valid signature establishes that both identities match.

Provider and local database operations also commit independently. A webhook can repeat, arrive out of order or report a payment whose local update previously failed. Correctness therefore needs identity checks, a monotonic business-state transition, durable duplicate handling and reconciliation.

## Why Separate Configuration From Collection?

| Concern | Owner or payer | Responsibility |
| -------------------------- | ----------------------- | ----------------------------------------------------------------- |
| Clinic gateway settings | Clinic owns credentials | Persist and resolve tenant-scoped provider configuration |
| Patient invoice collection | Patient pays clinic | Use the intended clinic merchant and update that clinic's invoice |
| SaaS billing | Clinic pays Docita | Use the platform merchant and update subscription state |

Clinic settings are configuration, not a third independent money-transfer rail or a requirement for three total merchant accounts. Clinics using cash, POS or their own UPI collection need not enable a hosted payment integration.

## How Current Injection Sites Separate Intent

The payment module declares `CLINIC_INVOICE_PAYMENT_LINK_PROVIDER_TOKEN` and `DOCITA_PLATFORM_PAYMENT_LINK_PROVIDER_TOKEN`. Billing and subscription callers use different tokens, which makes their intended responsibility visible.

**The current factories both call the shared factory's `getPaymentLinkProvider()` method.** The product payment-flow document explicitly identifies clinic-scoped provider resolution as technical debt. Token names alone therefore do not prove separate merchant credentials. New patient-online flows must resolve the authorized clinic's configuration or fail closed, rather than quietly substituting platform credentials.

Useful evidence includes the resolved merchant identity for a test transaction, tenant-bound credential lookup and a rejection test for missing configuration. Do not expose secrets while collecting that evidence.

## How a Webhook Becomes a Local Payment Update

```text
receive exact body bytes
  → verify provider signature with the correct webhook secret
  → validate event shape and resolve the expected payment session
  → check merchant, tenant, amount, currency and state compatibility
  → commit payment state + invoice transition + outbox intent
  → acknowledge only according to durable processing responsibility
```

Razorpay documents signature verification over the raw request body, duplicate events and potentially different event ordering. Keep webhook-secret verification separate from checkout-signature verification and API credential use. [Razorpay validation documentation](https://razorpay.com/docs/webhooks/validate-test/).

### Current Ingress Verification

The billing controller declares `webhooks/payments/razorpay` beneath the application's configured global prefix. It calls the shared `assertVerifiedRazorpayWebhook` helper with the raw body, supplied signature, configured secret and verifier. The helper rejects missing bytes/signatures and failed verification; a replay result becomes a conflict response.

These checks authenticate the request according to the verifier's protocol. They do not establish that a body represents the correct merchant or expected invoice amount. A valid request can still repeat, and replay protection must distinguish an already completed effect from an attempt that failed before completion.

### Trace the Inspected Capture Handler

For `payment.captured`, the service first looks for an existing record by provider and payment ID. It then resolves a session by provider order ID and requires invoice and patient identifiers. For `payment_link.paid`, it resolves the link session and uses a synthetic `payment_link:<id>` payment identifier.

Inside `runInTransaction`, the common capture method:

1. Updates the clinic's payment session to `CAPTURED`, including provider ID, paid time, amount and provider payload.
2. Updates the clinic's invoice to `PAID`.
3. Appends a `PAYMENT_CAPTURED` outbox event through the same transaction client.

This is evidence of a local atomic write boundary, provided the repositories use the passed transaction. It is not an atomic commit with the provider or proof that all downstream consumers finish; see the [outbox case](03-async-processing.md).

## Where Duplicate Handling and State Validation Need Care

The schema has a unique constraint on `(provider, providerPaymentId)`. It helps stop the same provider payment ID from being assigned to multiple session rows. A preflight lookup is still racy: two simultaneous deliveries can both observe no existing record. Updating the same row also does not necessarily cause a unique-constraint violation.

The two supported event shapes use different identifier forms. An event identifier, a payment identifier and an invoice's business transition are different identities. Define how they converge on one completed payment rather than assuming a single lookup deduplicates every equivalent notification.

The inspected capture method writes the supplied amount and sets the invoice to paid without showing an explicit expected-amount, currency, merchant or allowed-state comparison there. Such checks may exist elsewhere; this method alone is insufficient evidence. Partial payments, already-paid invoices, refunds and competing captures need defined transition rules and concurrency tests.

The outbox's unique intent key adds another boundary, but downstream idempotency remains necessary. Do not describe a removed, unsupported double-crediting incident as proven history or claim a preflight lookup makes duplicates harmless.

## What an HTTP Acknowledgment Means

The billing controller catches a processing failure, records it and still returns HTTP **200** with an error description. Razorpay treats non-2xx responses as delivery failures and documents retry behavior. A 200 therefore acknowledges receipt even if the local payment update failed. [Razorpay webhook best practices](https://razorpay.com/docs/webhooks/best-practices/).

This can be a valid ingress design when the event has already been durably accepted for independent recovery. Error logging alone does not establish a durable inbox, replay worker or successful reconciliation. Verify who now owns recovery before asserting eventual processing.

A timeout is another ambiguous outcome: the local commit may have succeeded while the provider did not receive its acknowledgment. A retry must safely recognize that committed result.

## Real-World Decisions

| Situation | Required decision | Evidence to seek |
| ---------------------------------------------------- | --------------------------------------------------------------------- | ---------------------------------------------- |
| Clinic lacks online configuration | Reject hosted collection or offer an explicitly supported desk method | No fallback to platform merchant |
| Same event arrives twice | Return the established result without repeating its effect | Concurrent delivery and crash tests |
| Two event types describe one payment | Resolve a common business identity and allowed transition | Payment/link identifiers and invoice state |
| Amount or currency differs from the expected invoice | Reject or enter an explicit exception workflow | Stored expected values and comparison |
| Local handling fails after receipt | Retain durable recovery responsibility or permit retry | Inbox/replay/reconciliation evidence |
| Refund occurs after capture | Model an additional financial transition | Ledger consistency and provider reconciliation |

Provider abstractions already exist in the current payment ports and adapter factories. The remaining question is whether those abstractions preserve merchant identity, permissions and provider-specific semantics—not whether an interface has been introduced at all. Reconciliation and refunds must be evaluated against actual source and operational evidence rather than labeled absent from an old snapshot.

## Mistakes

- Equating separate injection tokens with separate merchant accounts.
- Treating a valid HMAC as authorization to update any invoice.
- Trusting a preflight lookup as a concurrent idempotency mechanism.
- Marking an invoice paid without defining amount, currency and permitted transition checks.
- Returning 200 on failure while assuming provider retries will recover it.
- Recording full payment payloads or errors without checking sensitive-data handling and retention.

## Best Practices

Test each merchant boundary with controlled test accounts. Exercise simultaneous duplicates, both event shapes, incorrect scope/amount/currency, out-of-order transitions and crashes around acknowledgment. Record provider identity and local reconciliation status without leaking credentials or payment data. In interviews, explain the local transaction's exact scope and name the recovery boundary that remains.

## Current Assessment and Recommended Design

| Assessment | What it means here |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Current strengths | Provider signatures, local session state and transactional updates establish a useful payment boundary. |
| Current limitations | Acknowledging handler failure, incomplete contextual validation and duplicate effect handling can leave financial state unreconciled. |
| Recommended design | Persist verified ingress before acknowledgement; validate merchant, order, amount and currency; apply monotonic transitions and unique business-effect keys; reconcile unsettled operations against provider evidence. |
| Evidence needed | Duplicate, reordered and wrong-context fixtures cannot double-credit or activate the wrong clinic; a handler crash leaves durable retryable work and a reconcilable ledger. |

The recommended design is a proposal, not an implemented or production-verified claim. Apply it incrementally, beginning with a reproduced failure or explicit invariant; preserve working behavior and verify each migration boundary.

## Summary

Payment correctness depends on matching merchant and tenant identity, accepting only valid state transitions, handling repeated delivery and retaining recovery responsibility. Current Docita source shows separate intent tokens, ingress verification and transactional local updates; those mechanisms do not independently prove merchant isolation or end-to-end idempotency.

## See Also

- [Category revision](REVISION.md) — recall and failure scenarios after the cases.
- [Async processing](03-async-processing.md) — durable intent and acknowledgments.
- [Billing and invoicing](08-billing-invoicing.md) — financial records and invoice behavior.
- [Subscription system](09-subscription-system.md) — platform billing state.
- [Case-study index](INDEX.md) — reading order.

## References

- [Razorpay webhook validation](https://razorpay.com/docs/webhooks/validate-test/).
- [Razorpay webhook best practices](https://razorpay.com/docs/webhooks/best-practices/).

Docita source inspected on 2 October 2026:

- `docs/product/PAYMENT_FLOWS.md`
- `apps/api/src/domains/payments/payments.module.ts`
- `apps/api/src/domains/billing/presentation/controllers/webhooks.controller.ts`
- `apps/api/src/shared/modules/webhooks/razorpay-webhook-verification.helper.ts`
- `apps/api/src/domains/billing/application/services/razorpay-invoice-webhook.service.ts`
- `packages/db/prisma/schema.prisma` — `PaymentSession` model.
