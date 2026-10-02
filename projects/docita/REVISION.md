# Docita Case Studies — Category Revision

Read the relevant case study first. Distinguish inspected source, executable checks and deployment evidence in each answer.

## [Tenant Isolation](02-multi-tenancy-rls.md)

**Q:** What must connect a request’s clinic identity to its row-policy evaluation?

**A:** Trusted identity and authorization must lead to scope settings and the actual query on the same appropriately privileged database transaction.

**Q:** Why is the existence of an RLS policy insufficient in the inspected implementation?

**A:** Its staged condition permits rows when the enable setting is absent or not on. Role privileges, table coverage and query routing also govern enforcement.

**Q:** Do timers always lose AsyncLocalStorage context after a request?

**A:** No. Descendant work can inherit context; delayed work can instead retain an expired transaction reference. Independently scheduled work needs explicit validated scope.

**Q:** What did the overlapping-query routing probe establish?

**A:** The source-extracted routing core permits a second operation to take the base-client fallback while a first operation clears the shared tx. It did not establish live database behavior or a production leak.

**Q:** Does a worker necessarily need unrestricted access because it lacks HTTP context?

**A:** No. Tenant work can receive validated identity and run in a scoped transaction. Cross-tenant privilege should be justified for a specific operation.

**Q:** When does the inspected patient policy enforce doctor assignment?

**A:** For a plain DOCTOR when the resource requires assignment; it is not an unconditional check on every doctor operation.

## Architecture Boundaries

Source: [Architecture decisions](01-architecture-decisions.md).

**Q:** Why can DDD and ports and adapters appear in the same design?

**A:** DDD organizes business concepts and rules; ports and adapters control dependencies. They address related but different concerns.

**Q:** Does a pre-save overlap query prevent two concurrent bookings?

**A:** No. Both requests can pass the check. Persistence must enforce the invariant through a suitable constraint or transaction protocol.

**Q:** What does inferring a TypeScript type from Zod establish?

**A:** A type derived from the schema, not runtime validation of an arbitrary request. The boundary must parse input, and database and permission rules remain separate.

**Q:** Why is “all unexpected fields are rejected” inaccurate for an ordinary Zod object?

**A:** It normally strips unknown keys. Rejection requires a deliberately selected strict policy.

**Q:** Does a separate worker solve duplicate delivery?

**A:** No. It isolates execution and lifecycle; durable delivery and idempotency require a separate protocol.

**Q:** Why does one monorepo commit not make deployment atomic?

**A:** Application versions and migrations can roll out at different times. Contracts must remain compatible during overlap.

## Durable Work and Repeated Effects

Source: [Async processing](03-async-processing.md).

**Q:** What gap does a transactional outbox close?

**A:** A committed business change losing its event intent because a separate emission fails. Both database writes must use the same transaction.

**Q:** Why does SKIP LOCKED not establish exactly-once processing?

**A:** It coordinates claims while locks are held. A crash after an effect but before completion can cause another attempt.

**Q:** Can a recent-completed-job lookup prevent concurrent duplicate effects?

**A:** No. Both jobs may see no completed predecessor. Idempotency must protect the effect itself.

**Q:** What risk remains when recovering a stale ACTIVE job?

**A:** Its first worker may still be running. A lease or timeout needs ownership checks and, where appropriate, fencing.

**Q:** What did the local EventEmitter2 probe show?

**A:** Synchronous emit returned before an async listener completed. A relay processed marker after emit does not prove the side effect completed.

**Q:** Why is using PostgreSQL insufficient to prove transactional enqueue?

**A:** The business and intent writes still have to share one transaction. Separate calls can retain a dual-write gap.

## Payment Ownership and Acknowledgments

Source: [Payment flows](04-payment-flows.md).

**Q:** Why do two injection tokens not prove merchant isolation?

**A:** Their factories may return the same adapter and credentials. Verify tenant-scoped resolution and the actual merchant identity.

**Q:** What does webhook signature validation establish, and what remains?

**A:** Authenticity under the signature protocol. Expected merchant, tenant, amount, currency and permitted business transition still need validation.

**Q:** Why is checking for an existing provider payment before writing insufficient?

**A:** Concurrent deliveries can both pass the lookup. Enforce the business transition and effect idempotency within a suitable persistence protocol.

**Q:** What does the payment capture transaction cover?

**A:** The local payment-session update, invoice update and outbox append through the transaction client—not the provider's external operation or downstream effect.

**Q:** What must be true before returning 200 after a processing failure?

**A:** Durable recovery responsibility must already exist. Logging an error alone does not prove replay or reconciliation.

**Q:** Why distinguish event ID, provider payment ID and invoice identity?

**A:** Multiple deliveries or event types can refer to one business payment. Transport duplicate detection and business transition idempotency solve different problems.

## Compatible Deployment and Recovery

Source: [Deployment and infrastructure](10-deployment-infrastructure.md).

**Q:** What does a successful schema drift check fail to establish?

**A:** Compatibility with old application versions that remain during rollout. Schema alignment and release compatibility are different checks.

**Q:** Why does one warm machine not guarantee no cold starts or errors?

**A:** Replacement, failure and regional disruption still occur. The minimum setting also applies only in the primary region.

**Q:** Does Fly autostart create more machines under load?

**A:** No. It manages existing machines; creating capacity is a separate operation.

**Q:** What does the inspected worker canary's started-state check show?

**A:** Process stability for its settling window, not successful jobs, correct tenant scope or duplicate-safe effects.

**Q:** Why distinguish Worker executable size from browser assets?

**A:** They are different deployment artifacts with different constraints. The current Worker limit is uncompressed, not the old gzip comparison.

**Q:** Why might an application-image rollback be insufficient?

**A:** Migrations, data writes and external effects may already have occurred. Recovery must address those changes separately.

## Upload Capabilities and Stored Objects

Source: [Documents and uploads](19-documents-and-uploads.md).

**Q:** Why are repeated readiness checks insufficient for single-use uploads?

**A:** Concurrent callers can both observe an unused session before either updates it. Consumption needs an atomic ownership transition.

**Q:** What did the source-extracted upload probe establish?

**A:** Controlled overlapping calls both uploaded and updated the same session. It did not establish a production exploit.

**Q:** What protection does a random-secret hash provide?

**A:** The stored hash cannot directly serve as the bearer secret. Plaintext delivery, issuance permissions and target binding still matter.

**Q:** Does the local provider's generateSignedUrl method create an expiring signature?

**A:** No. It checks TTL input but returns a public local URL and advertises supportsSignedUrls false.

**Q:** Why do opaque keys not make a provider migration automatic?

**A:** The bytes and access policy must migrate too. Legacy paths and provider semantics can differ.

**Q:** Does signed-URL expiry revoke downloaded copies?

**A:** No. It limits future access under that signature, not already-obtained bytes.

**Q:** Why can controller logging miss a later file download?

**A:** A direct presigned-URL fetch can reach object storage without passing through the application controller.

## Workflow State and Scheduling

Source: [Clinic workflows](05-clinic-workflows.md).

**Q:** Why distinguish queue progress from appointment status?

**A:** A reservation can exist before arrival, and arrival does not necessarily mean consultation has begun. Their lifecycles differ.

**Q:** What allocation risk does lastNumber + 1 introduce?

**A:** Concurrent callers can read the same last number. An atomic counter or constrained retry protocol must coordinate allocation.

**Q:** Does incrementing version prevent a stale update?

**A:** No. The write must compare the expected version or permitted persisted state and handle a failed match.

**Q:** Why can adjacent half-open appointments coexist?

**A:** The end is excluded, so one ending exactly when another starts does not overlap. A buffer is a separate policy.

**Q:** Which boundary can protect overlapping bookings after both preflight checks pass?

**A:** An applied exclusion constraint or another suitable concurrent persistence protocol, under the intended clinic/doctor/status scope.

**Q:** Why is Date.getHours unsuitable as an implicit clinic-hour check?

**A:** It uses process-local timezone. Clinic policy needs explicit timezone conversion, including calendar boundaries.

## Retrospective Decisions

Source: [What I'd do differently](22-what-id-do-differently.md).

**Q:** What makes a useful improvement proposal reviewable?

**A:** A concrete invariant, threatening trace, enforcement boundary, meaningful check and compatible rollout plan.

**Q:** Do domain events remove all cross-domain coupling?

**A:** No. They replace or supplement synchronous dependencies with event contracts, delivery semantics and projection-consistency obligations.

**Q:** Why does an event schemaVersion need more than a new column?

**A:** Consumers must validate supported versions, handle unsupported ones and safely process retained events during mixed-version rollout.

**Q:** Why can broader health probes harm availability?

**A:** Unnecessary dependency calls can amplify outages or reject healthy capacity. Separate liveness, readiness and business monitoring.

**Q:** What should follow an already-configured build cache?

**A:** Validate task inputs/outputs and environment keys, then measure representative cold/warm builds and shared changes.

**Q:** Why can a validation schema not determine the whole form UI?

**A:** Accessible labels, grouping, widgets and workflow meaning require design information beyond the data shape.

## Stock, Movements and Read Freshness

Source: [Inventory](13-inventory.md).

**Q:** Why put a decrement and its movement in one transaction?

**A:** Either both commit or neither does. Otherwise history and balance can diverge after failure.

**Q:** Why does the guarded last-unit update reject a competing decrement?

**A:** The database coordinates row writes and the quantity condition must remain true when the write is accepted.

**Q:** What current bypass prevents a whole-domain ledger guarantee?

**A:** updateItem still permits directly writing quantity without a movement.

**Q:** Does a safe decrement make repeated invoice consumption idempotent?

**A:** No. When stock remains, the same business operation can subtract again unless its identity is uniquely enforced.

**Q:** What do parallel read-client queries fail to guarantee?

**A:** A common snapshot or immediate visibility of primary writes. Configured replica routing may add lag.

**Q:** Why can a sum of stock quantities be misleading?

**A:** Items may use incompatible units. A mixed count is not a shared physical stock measure.

## Metric Meaning and Historical Snapshots

Source: [Analytics and dashboards](14-analytics-and-dashboards.md).

**Q:** Why must calendar range and bucket identity agree?

**A:** The range decides inclusion and the bucket assigns a period. Different calendars can mislabel correctly selected records.

**Q:** What error did the weekly source probe reproduce?

**A:** Distinct January and February weeks map to the same key because the helper uses day-of-month logic.

**Q:** How should two revenue buckets with 100 total and 10 invoices be combined?

**A:** Sum invoice counts and divide 100 by 10. Dividing by two buckets gives the wrong average invoice amount.

**Q:** Does a daily period argument restrict source data to one day?

**A:** No. It may only select grouping granularity; an explicit date range is still required.

**Q:** Why is current catalog price times procedure count not necessarily collected revenue?

**A:** Historical charges, payment status, discounts, tax and refunds can differ, and current prices can change.

**Q:** Can rerunning today's snapshot method heal a missed historical date?

**A:** Not without a defined historical input window and correction/version protocol.

## Invoice Context and Collections

Source: [Billing and invoicing](08-billing-invoicing.md).

**Q:** What does a retained tax snapshot establish?

**A:** The stored calculation context, not that its classification or inputs were legally or numerically correct.

**Q:** Why do allowed invoice edits need an explicit historical policy?

**A:** Recalculation or missing-snapshot fallback can change context. Define finalization, correction and legacy handling.

**Q:** Does the local PAID state prove actual provider collection?

**A:** No. Its transition must be connected to verified amount and provider evidence, including duplicates and failures.

**Q:** How does filtering payment sessions by createdAt differ from paidAt?

**A:** A late capture can be reported under the session's creation date rather than the date money was received.

**Q:** Why must a daybook separate currencies?

**A:** Adding incompatible amounts and labeling the sum with the last session's currency is not a valid financial total.

**Q:** Which calculation identities are useful checks?

**A:** Subtotal minus discount plus tax equals grand total, and component amounts sum to tax total, under the chosen rounding policy.

## Subscription Entitlements and Usage

Source: [Subscription system](09-subscription-system.md).

**Q:** What does RequireFeature actually do?

**A:** It adds route metadata. TierGuard must read that metadata and enforce clinic entitlement.

**Q:** Why does a paid plan not authorize access to another clinic?

**A:** Entitlement grants a feature; caller permission and tenant scope still constrain the resources it can operate on.

**Q:** Can post-action usage tracking enforce the last remaining unit?

**A:** No. Concurrent work requires an atomic reservation when overshoot is unacceptable.

**Q:** Why can the current daily aggregation double-count a rerun?

**A:** It sums a day's events and increments the same monthly record again without identifying an already-applied contribution.

**Q:** What billing fields do month/year setters leave unresolved?

**A:** Month-end behavior, timezone and the intended period anchor need explicit policy and boundary tests.

**Q:** Does logging a failed referral reward eventually award it?

**A:** No. Non-fatal orchestration needs durable retry or reconciliation if the reward must be completed.

## Messaging Delivery and Reply Processing

Source: [WhatsApp integration](06-whatsapp-integration.md).

**Q:** What gap remains when provider send happens before saving the local message?

**A:** A database failure can lose correlation after acceptance; a retry may send a duplicate.

**Q:** Does persisting an inbound message ID establish completed appointment processing?

**A:** No. Downstream failure needs a retryable processing state separate from receipt identity.

**Q:** Why does the six-hour pending-delay lookup need conversational context?

**A:** A bare number can be a duration or menu choice, and another turn can make an old pending response misleading.

**Q:** What does the stale-delivery sweep actually recover?

**A:** It recovers visibility through counts and alerts, not delivery status or missing provider receipts.

**Q:** Does a delay conflict warning reserve another slot?

**A:** No. It compares expected arrival to the next appointment start; reservation and full overlap rules are separate.

**Q:** Why is fallback text not automatically allowed after template rejection?

**A:** Provider window and consent rules still apply; outside the service window an approved template is required.

## Prescription Checks and Document Evidence

Source: [Prescription validation](07-prescription-safety.md).

**Q:** What does an empty recorded allergy list establish?

**A:** Only that no recorded allergies were available to this check, not that the patient has none.

**Q:** Why does comparing a parsed dose number leave unit safety unresolved?

**A:** The implementation does not convert units before comparing against the configured numeric range.

**Q:** Does the general dose validator prove daily exposure is within a limit?

**A:** No. The inspected call does not combine frequency with the maximum-daily field.

**Q:** Why should consultation context come from an authoritative record?

**A:** A caller override can change whether the context-sensitive policy blocks an item.

**Q:** What can change when a prescription PDF is regenerated?

**A:** Current render date, live doctor/signature data and template behavior can differ unless inputs and document versions are retained.

**Q:** What failure remains after upload but before metadata persistence?

**A:** The object can exist without a stored prescription reference; retries and cleanup need ownership and version rules.

## Summary

Reconstruct the operation and its boundaries. Qualify every outcome according to the evidence actually obtained.

## See Also

- [Case-study index](INDEX.md) — reading stages and source-linked cases.
