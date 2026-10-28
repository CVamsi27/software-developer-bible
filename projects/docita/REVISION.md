# Docita Case Studies — Category Revision

[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../docs/topic-importance.md)



Read the relevant case study first. Distinguish inspected source, executable checks and deployment evidence in each answer.

## [Tenant Isolation](02-multi-tenancy-rls.md)

**Q:** What must connect a request’s clinic identity to its row-policy evaluation?

**A:** Trusted identity and authorization must lead to scope settings and the actual query on the same appropriately privileged database transaction.

**Q:** Why is the existence of an RLS policy insufficient in the inspected implementation?

**A:** Its staged condition permits rows when the enable setting is absent or not on. Role privileges, table coverage and query routing also govern enforcement.

**Q:** Do timers always lose AsyncLocalStorage context after a request?

**A:** No. Work started inside an existing request can inherit its context, while delayed work can retain a reference to a transaction that has already ended. Independently scheduled work needs its own explicitly supplied and validated clinic or user scope.

**Q:** What changed between the historical overlapping-query failure and the current routing probe?

**A:** The earlier router cleared a sibling-visible transaction reference. The current router creates a child async scope with tx:null for the delegate, leaving the parent transaction visible to siblings. The 26 October extracted-helper check routed both overlapping calls through their transaction delegates; it did not establish database policy enforcement or production isolation.

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

**A:** The 2 October probe showed synchronous `emit` returning before an async listener completed. The 9 October recheck shows the relay now awaits `emitAsync`; extracted-source checks confirmed delayed fulfillment and rejection-driven retry. Its marker still depends on the registered listener returning and propagating the required work.

**Q:** What happens if the required event listener was never registered?

**A:** An unguarded `emitAsync` can fulfill with no listener results. The 15 October source has a `hasListeners` guard that throws instead, leaving retryable intent. One registered listener still does not prove that every required handler exists or propagates failure; verify registration and the actual Nest wiring.

**Q:** Does a dispatch timeout stop the listener's side effect?

**A:** No. It stops waiting, not the underlying promise. The first attempt can complete after a retry begins, so stable operation keys and effect-level idempotency remain necessary.

**Q:** Why can a Nest listener failure fail to trigger an outbox retry?

**A:** Its default `suppressErrors: true` can log the error rather than rethrow it. A required listener must return its work promise and propagate failures; test the actual Nest wiring, not only an emitter stub.

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

## Patient Identity and OTP Finalization

Source: [Patient portal](16-patient-portal.md).

**Q:** How many codes does randomInt(100000, 1_000_000) generate?

**A:** 900,000; the upper bound is exclusive and leading-zero codes are excluded.

**Q:** Does atomic attempt counting prove a successful OTP can only be used once?

**A:** No. Success needs a separate conditional finalization that checks unused and still-valid state and returns one winner.

**Q:** Why does a generic request response not eliminate enumeration by itself?

**A:** Timing, exceptional paths and delivery side effects can still differ when an account exists.

**Q:** What should a prescription detail lookup combine with its requested ID?

**A:** The authenticated patient's derived scope and clinic ownership, including nested and file access.

**Q:** Why is endpoint throttle metadata not proof of per-phone protection?

**A:** Effective enforcement depends on the installed guard, tracker key and storage; IP limits and phone cooldowns protect different boundaries.

**Q:** What model supports a guardian safely?

**A:** An explicit revocable delegation with patient scope and audit evidence, rather than accepting arbitrary patient IDs.

## Claim Concurrency and Historical Evidence

Source: [Insurance claims](11-insurance-claims.md).

**Q:** Why do a transition table and version predicate solve different problems?

**A:** The table rejects invalid moves; the predicate rejects stale decisions made against an earlier row version.

**Q:** What does the transition transaction guarantee about its event?

**A:** The accepted state change and event insert commit or roll back together through that path.

**Q:** Why is the claim event table not automatically immutable?

**A:** Database permissions and retention are separate, and the current schema cascades events when their claim is deleted.

**Q:** Is readiness rechecked for resubmission to SUBMITTED?

**A:** Yes, the command checks any requested SUBMITTED transition with a linked invoice, not only the draft edge.

**Q:** What gap remains in preliminary idempotency lookup plus a unique key?

**A:** Concurrent requests can both miss the lookup; uniqueness prevents duplicate rows but conflict handling must still provide the promised API result.

**Q:** Does an invoice ID prove a reimbursement references a finalized invoice?

**A:** No. The inspected shape check requires the ID; finalized-state and amount/currency validation need separate enforcement.

## Bed Allocation and Admission Races

Source: [Inpatient management](12-ipd-inpatient.md).

**Q:** Why can two transactions both create an active admission after finding none?

**A:** A transactional absence read does not itself lock a unique resource; a constraint or serialization protocol must protect that invariant.

**Q:** What does a conditional AVAILABLE bed update protect?

**A:** It gives one transaction the bed claim when one affected row is required, but does not alone enforce one admission per patient across different beds.

**Q:** Why must discharge verify current allocation ownership?

**A:** An earlier bed snapshot can be stale after transfer, so freeing it by ID can release the wrong allocation.

**Q:** Is the current post-operation audit in the allocation transaction?

**A:** No. The service invokes it after repository completion, so required history needs a recoverable commit boundary.

**Q:** Why should active uniqueness exclude discharged history?

**A:** Patients and beds legitimately appear in later admissions; only overlapping active allocation should conflict.

**Q:** Can append-to-notes preserve concurrent history reliably?

**A:** Not when each writer rebuilds from an earlier string; individual versioned events avoid lost appends.

## Enterprise Membership and Issued Terms

Source: [Enterprise contracts](18-enterprise-contracts.md).

**Q:** Does current member removal restore the previous subscription?

**A:** No. The inspected method marks membership removed and records a revision, without restoring subscription fields.

**Q:** Why is a payment/invoice upsert not necessarily immutable issuance?

**A:** Its update branch can change amount, currency and metadata; issued terms need a frozen version and correction policy.

**Q:** Does a random adjustment invoice number deduplicate retries?

**A:** No. Each retry can create another adjustment unless stable operation identity is enforced.

**Q:** Why can current estimates and true-up disagree?

**A:** They use different current quantities, accumulated events, usage summaries, membership periods and comparison baselines. They do not calculate from one identical ledger with the same definitions.

**Q:** What must an enterprise exit snapshot retain?

**A:** The approved prior entitlement state and effective dates, or another explicit policy for the post-contract plan.

**Q:** What makes one alert per contract/period reliable under concurrency?

**A:** A unique period identity and transactional creation with durable notification work, rather than only a prior lookup.

## Credential Freshness and Public Request Boundaries

Source: [Doctors and public booking](15-doctors-verification-and-public-booking.md).

**Q:** What happens when no automated verification provider is configured?

**A:** The inspected service leaves verification pending for manual administration rather than proving registry verification.

**Q:** Why must a provider result identify the credential version it checked?

**A:** A delayed result must not mark newer edited registration facts verified.

**Q:** Does taking 500 records establish periodic verification of every doctor?

**A:** No. Coverage needs a fair due-time selection or cursor and completion evidence.

**Q:** Why are implicit opening hours risky?

**A:** Missing configuration can become apparent availability even when the clinic has not approved those hours.

**Q:** Does an appointment request reserve the displayed slot?

**A:** No. Staff confirmation must revalidate and atomically claim current capacity.

**Q:** What gaps can separate patient creation, consent and request creation leave?

**A:** Partial records and duplicate intake; stable operation identity and recovery must span the required steps.

## Health Exchange Trust and Evidence

Source: [ABDM integration](17-abdm-integration.md).

**Q:** Does an existing care-context reference authenticate its callback?

**A:** No. Correlation and sender authentication are separate, and consent authorization is another requirement.

**Q:** What callback authentication already exists in the inspected source?

**A:** A shared webhook verifier configured for shared-secret-header authentication with replay/timestamp inputs; this is not evidence of asymmetric published-key verification.

**Q:** Does marking a context SHARE_REQUESTED prove an HTTP exchange was dispatched?

**A:** No. The inspected link/share helper records intent and local state without dispatching the external request itself.

**Q:** Why are encryptedContent fields insufficient proof of correct encryption?

**A:** The pipeline must demonstrate that authorized local records were encrypted under the negotiated protocol and can be decrypted and validated by the intended receiver.

**Q:** What must be checked before a callback-selected data push?

**A:** Trusted participant/destination, tenant and patient scope, valid unexpired/unrevoked consent, authorized data and retry identity.

**Q:** Does RETRYABLE in an inbox automatically recover an operation?

**A:** No. A durable worker or explicit operator process must own retry, correlation and completion evidence.

## Lab Release and Catalog Coverage

Source: [Clinical lab and coding](20-clinical-lab-and-medical-coding.md).

**Q:** Why can two releaseIfReady calls both send a result?

**A:** Eligibility is read before sending, and the final update does not atomically claim release ownership.

**Q:** Does a caught WhatsApp failure keep the local order unreleased?

**A:** Not in the inspected path; it can still mark completion, so released, notified and delivered need separate states.

**Q:** Does paidAt prove a provider collected the matching invoice amount?

**A:** No. The current lab verification records a local action and reference; financial reconciliation is separate.

**Q:** What does mapping HCPCS Level II into CptCode lose?

**A:** The distinction between code systems unless source/system/version are retained and displayed explicitly.

**Q:** Why can a resolved sync still be partial?

**A:** The NLM stream catches a fetch failure and returns; the caller can report seen counts without a completion watermark.

**Q:** What must a catalog fallback tell its consumer?

**A:** Active source, system/version, coverage and degraded status rather than pretending interchangeable semantics.

## Smaller Domains: Boundaries and Recovery

Source: [Smaller domains](21-long-tail-domains.md).

**Q:** Why does sent-history lookup not guarantee one reminder send?

**A:** Two runners can read the same absence before either sends or records its result; an atomic intent/claim is required.

**Q:** Does custom-field definition CRUD prove patient values are validated?

**A:** No. Patient writes must explicitly validate values against authorized definitions and their versions.

**Q:** What concrete outbound webhook gaps does the inspected path expose?

**A:** Recipient selection lacks a clinic predicate, tick uses a placeholder signing secret, and markFailed leaves claimed rows IN_FLIGHT without scheduling their next attempt.

**Q:** Does a ten-minute replay claim prove webhook business processing completed?

**A:** No. It records acceptance within a transport window; durable processing state and business idempotency must handle crashes and later retries.

**Q:** Does Role.LAB at login establish every subsequent resource permission?

**A:** No. Worklists, uploads and result reads still need tenant, lab and order authorization.

**Q:** Why is transactional leave approval insufficient to prevent conflicting transitions?

**A:** The re-read does not own the state and the final update lacks a conditional PENDING/version predicate; competing actions can pass their earlier checks.

**Q:** What distinguishes feedback status labels from a workflow?

**A:** Labels constrain possible values; a workflow also constrains transitions from the current state and records authorized decisions.

**Q:** What does account deletion actually change before erasure completes?

**A:** It soft-deletes and disables login, then separately creates a clinic-bound request. Those writes are not proof of session revocation or completed erasure.

## Hypothetical 25-Clinic Metrics and Measurement

Source: [Workload model and outcome definitions](23-hypothetical-clinic-metrics.md). All numerical samples in this group are invented study inputs or calculations, not observed Docita results.

**Q:** How does the scenario obtain 26,000 monthly completed appointments?

**A:** It assumes 25 clinics, 40 completed appointments per clinic-day and 26 operating days: 25 × 40 × 26. It does not count cancellations or prove that real clinics exist.

**Q:** Why does the model's 0.69 requests/second average not demonstrate enough capacity?

**A:** It spreads the assumed 20,000 daily requests over eight hours. Concentrating 30% into 30 minutes gives 3.33 requests/second, and the proposed brief stress burst is 33.3. Handler cost, concurrency, dataset and shared database work still need measurement.

**Q:** Why can the queue's two-second poll setting undermine a fast burst-completion goal?

**A:** One idle job-name lane starts at most roughly one job per two seconds in the idealized model. Starting 1,000 jobs takes about 33 minutes even before execution overhead. Other names and instances change capacity but do not prove safe repeated effects.

**Q:** Is the outbox's 200-row batch every five seconds a measured delivery rate of 40 events/second?

**A:** No. It is a theoretical selection-rate calculation from settings. Dispatch, lock holding, downstream work and asynchronous-listener acknowledgment affect actual outcomes.

**Q:** How would you explain the invented 800-to-350 ms p95 example?

**A:** The absolute decrease is 450 ms and the relative decrease is 56.25% of the 800 ms baseline. I would explicitly call it a synthetic example. An actual claim needs comparable endpoint, load, dataset, cache conditions, deployment and request distributions.

**Q:** Can per-clinic p95 values simply be averaged into a platform p95?

**A:** No. Calculate the combined percentile from all eligible observations, or from compatible summaries that can be merged while preserving the distribution. Averaging per-clinic percentiles loses the underlying values and gives clinics the wrong weight when their sample counts differ.

**Q:** Why cannot a 90-second reduction in median booking time establish 650 saved staff-hours?

**A:** Total labor depends on mean task time and actual task counts. The chapter's 650-hour example separately assumes a 90-second mean saving over 26,000 tasks. Median differences do not justify that total.

**Q:** What does 50,960 out of 52,000 messages mean in the example?

**A:** An invented 98% delivery fraction within 24 hours of each eligible message intent, if those are unique eligible logical messages with provider delivery receipts. Enqueue success and provider acceptance are earlier states, and retries must not inflate the denominator.

**Q:** Can 5,200 estimated payment attempts serve as the denominator for captured-payment reconciliation?

**A:** No. Failed or abandoned attempts need not produce captured payments. The synthetic reconciliation example independently assumes 5,200 eligible captured payments, of which 5,174 are matched within five minutes of capture. Actual provider records must establish that population.

**Q:** What is the time-based budget for a proposed 99.9% availability target over 30 days?

**A:** 43.2 minutes unavailable: 30 × 24 × 60 × 0.001. It is a proposed time-based target, not an observed uptime claim or a substitute for a request-based error budget.

**Q:** What must accompany a PDF-completion p95 under 60 seconds?

**A:** Durable enqueue and artifact-availability timestamps, workload and observation window, plus outstanding work and terminal failure counts. Measuring only completed jobs can hide missing or indefinitely stuck work.

**Q:** Why does zero unauthorized effects in a fixture not mean the product has never leaked data?

**A:** The result covers the exercised matrix of tenants, roles, queries and failure paths. It cannot establish unobserved production history or every possible access path; database privilege and scope wiring remain important.

**Q:** What distinguishes RPO from RTO in the proposed restore exercise?

**A:** RPO bounds the accepted data-loss interval; RTO bounds time to verified restoration. A backup configuration supports neither an executed recovery-time claim nor proof of restored integrity by itself.

**Q:** How should I describe the scenario in a system-design interview?

**A:** “Assuming 25 clinics completing 40 appointments on 26 operating days, I model 26,000 monthly visits, then test bursts, tenant isolation and effect recovery separately.” Keep the assumption explicit rather than presenting adoption as personal operating history.

**Q:** When can an invented improvement be moved into the resume?

**A:** It cannot be moved as an achievement. Replace it with an actual measurement or documented reasonable estimate, record personal contribution, and preserve whether the result came from production, a pilot or a controlled benchmark.

**Q:** What turns the 25-clinic model into benchmark evidence?

**A:** Execute a versioned synthetic fixture under a stated arrival schedule, retain correctness checks and raw outcomes, and reproduce the comparison. The resulting claim describes that benchmark's actual observations; the assumed clinic count still does not describe customers.

**Q:** Why report offered load as well as achieved throughput?

**A:** A generator that waits for responses may slow down as the server slows down. A low error rate at that reduced rate can hide overload. State the arrival model, actual request count, failures, timeouts and unfinished work before interpreting latency.

**Q:** Which evidence would establish a real active-clinic count instead?

**A:** A dated, privacy-safe aggregate from operational records using an explicit completed-appointment definition, distinct clinic identities, reporting cutoff and synthetic/demo exclusions. A seeded fixture, a public case study or a metric row entered to match the desired number cannot establish adoption.

## Current Resume Bullet Walkthrough

Source: [Five-bullet walkthrough](24-resume-claim-walkthrough.md).

**Q:** What should lead my 90-second Docita overview?

**A:** A user operation and my actual responsibility, then how frontend, API, database and background work connect. Name technologies after establishing the problem; identify source existence separately from personal contribution and production outcomes.

**Q:** Does a monorepo mean one atomic release?

**A:** No. Shared source can coordinate contracts, but migrations and application versions can deploy at different times. Explain compatibility during overlap.

**Q:** What should I trace for the React form bullet?

**A:** Local editing state, runtime validation, authorized mutation, pending/error behavior and the server-cache update. Demonstrate a failure and stale result rather than only the happy path.

**Q:** How do I explain RLS policies without promising universal isolation?

**A:** Describe their intended coverage and the actual enable settings, roles and transaction routing. The inspected staged policies and fallback paths require verification; application authorization and RLS are separate layers.

**Q:** What does the background-work bullet deliberately avoid promising?

**A:** Exactly-once effects or universal atomic enqueue. Producer transactions, claim recovery, duplicate-effect handling and relay acknowledgment have distinct current limitations.

**Q:** Why is a signed payment webhook not sufficient for a correct payment outcome?

**A:** Signature verification establishes a payload/secret relationship. Merchant ownership, business state, duplicate effects, event ordering and reconciliation still need validation.

**Q:** Does schema-valid AI output establish a safe clinical answer?

**A:** No. Shape validation does not establish clinical truth. Keep review with a clinician and explain actual data, quota, timeout and fallback controls on the selected call path.

**Q:** What can I claim from deployment configuration versus a restore drill?

**A:** Configuration shows the intended integration. A timed, integrity-checked restore supplies recovery evidence for its environment and scenario. Neither proves unobserved availability history.

**Q:** How do I demonstrate personal ownership from a repository?

**A:** Select actual changes and explain what I designed, implemented, reviewed or operated, with their context and collaborators. Finding a source file or learning its mechanism is not itself authorship evidence.

**Q:** What can I demonstrate for the operational-dashboard resume bullet?

**A:** Trace the authorized API, shared schema, PostgreSQL aggregate and frontend states. Explain the reporting window, sample population and unavailable measurements. The implementation is evidence of engineering work; retained samples alone do not establish customer adoption, availability or improvement against a baseline.

**Q:** What is a practical completion criterion for this preparation?

**A:** Explain one operation without notes, demonstrate a failure, justify an alternative and answer changed constraints. Keep production, benchmark, hypothetical and unexecuted evidence labels intact.

## Actual Production Metrics and Their Limits

Source: [Actual-record dashboard](14-analytics-and-dashboards.md#a-dashboard-built-from-actual-records-and-retained-telemetry). This group preserves the scoped 2 October legacy-query observation; it is not a new version-2 customer-traffic result.

**Q:** Can 158 retained requests with zero recorded server errors establish 100% availability?

**A:** No. The sample set has partial coverage and can omit requests when persistence fails. Availability needs an independently defined observation period, denominator and outage detection.

**Q:** What does the measured 2 ms p95 describe?

**A:** The nonnegative persisted request durations in that specific production sample set. It can include health checks and excludes client/network/render time. I need route-specific, representative traffic before describing user-facing latency.

**Q:** Why does a completed-appointment count use both time and status?

**A:** The time selects appointments scheduled in the window; current status selects those now completed. Without a completion event timestamp, it does not count completions that happened during the window.

**Q:** Why avoid a new table filled with the desired metrics?

**A:** A dashboard should derive its current counts from authoritative operational records. Invented metric rows would break provenance; versioned snapshots are useful only when their real inputs, cutoff and correction policy are preserved.

**Q:** What production result can I currently explain without inventing adoption?

**A:** The dated read-only aggregate returned 158 retained request samples and no appointment, invoice or retained job activity in its selected window. I can explain the query and its limits; it does not substantiate a 25-clinic customer claim.

## Read a Fly Machine Before Describing Its Capacity

Sources: [Deployment and infrastructure](10-deployment-infrastructure.md), [capacity model](23-hypothetical-clinic-metrics.md).

**Q:** What can the 28 October machine inventory tell me about the current deployment?

**A:** It identifies one configured API Machine and one worker Machine in Singapore, with one shared CPU each and 512 MiB/256 MiB RAM respectively. Both were stopped at the observation time. That snapshot describes provisioned shape and state; resource utilization and active-service latency require observations while the processes actually run.

**Q:** Why does one virtual CPU (vCPU) not make every Node.js request run in parallel?

**A:** Asynchronous I/O can overlap while the JavaScript event loop schedules callbacks, but CPU-heavy work can delay those callbacks. Inspect event-loop delay and profiles under representative requests; a configured core count does not reveal the work each request performs or establish its achievable throughput.

**Q:** How should shared CPU capacity affect an explanation of a benchmark?

**A:** State the CPU kind as well as its count. A shared CPU allocation does not imply the same sustained compute as a dedicated core. Keep resource contention and repeated-run variation in the report before attributing a changed tail latency entirely to application code.

**Q:** Is a 384 MiB V8 heap ceiling a safe total-memory budget inside a 512 MiB API Machine?

**A:** The heap is only one part of resident memory. Buffers, native allocations, stacks, the database driver and runtime overhead consume additional space. Measure peak resident set size (RSS), heap and garbage-collection behavior together; setting the heap below the VM limit alone does not establish enough headroom.

**Q:** What makes the worker's 192 MiB heap setting worth testing inside its 256 MiB Machine?

**A:** PDFKit generation, fonts, image buffers, concurrent jobs and database work share the worker process and its memory envelope. The current PDF path does not launch a browser subprocess. Measure representative documents and peak RSS; an idle worker's small heap use cannot predict a burst of complex files.

**Q:** Do Fly's request soft limit of 60 and hard limit of 100 describe requests per second?

**A:** They describe concurrent in-flight requests for the configured service. A long request occupies that allowance longer than a short request. Measure arrival rate, response duration and accepted/rejected work together, rather than treating a concurrency setting as a throughput benchmark.

**Q:** What must be reviewed before adding another API Machine behind a scaling controller?

**A:** Identify state that currently lives inside one process: caches, rate-limit counters, socket rooms, in-flight work and scheduled ownership. A second Machine may create inconsistent views or separate limits. Verify cross-instance behavior and the database connection envelope before interpreting more Machines as safe capacity.

**Q:** Why will an API request not necessarily wake a stopped worker?

**A:** Fly Proxy routes the API's HTTP service, while the separately deployed worker has no equivalent HTTP wake path in its checked-in configuration. A newly queued database job is not itself a proxy request. Define and test how the worker remains available or is explicitly started.

## Choose a Database Profile Without Inventing Its Hardware

Sources: [Deployment and infrastructure](10-deployment-infrastructure.md), [capacity model](23-hypothetical-clinic-metrics.md).

**Q:** Which database facts can I state about the temporary deployment without guessing a Neon tier?

**A:** The owner-confirmed current provider is Neon, used as the temporary cost-conscious database. Its exact project limits, compute allocation, region, storage and recovery settings need separate inventory. A PostgreSQL connection string or repository pool setting cannot supply those provider-side hardware facts.

**Q:** Why distinguish Neon compute allocation from stored data size?

**A:** Compute executes queries and holds active memory, while stored relations and indexes occupy persistent storage. Their scaling and billing controls are different. Record provider compute limits and database-size observations separately; a small stored dataset can still create expensive joins, sorts or connection pressure.

**Q:** How can an inexpensive suspended setup produce a slow first request even with fast warm queries?

**A:** The API may need to resume and the database compute may need to become available before the request's normal work begins. Measure the whole cold path and the warm path separately. Tuning a warm SQL query cannot remove every delay introduced before it is executed.

**Q:** Why does the database region matter when the Fly API is in Singapore?

**A:** Each sequential database exchange adds network latency to the critical path. Several individually cheap statements can therefore produce a slow response when the database is distant. Record actual region placement and round trips, then compare query batching and placement using the same workflow.

**Q:** How should a future AWS database profile appear in an interview answer?

**A:** Identify it as a proposed reference profile, with the workload, availability objective and observations that would justify it. Describe its CPU, memory, storage and recovery decisions together. Do not describe the proposal as the current database or imply that its capacity has already been measured.

**Q:** Why might a pooled endpoint suit application traffic while a migration uses a direct endpoint?

**A:** Application traffic benefits from bounded connection reuse, while migration and administrative operations may need session behavior or locks that a transaction pooler changes. Verify the provider's mode, driver compatibility and transaction-local RLS behavior. Keep endpoint selection explicit rather than swapping URLs without a compatibility check.

**Q:** What evidence would justify moving from the temporary database profile to the balanced reference profile?

**A:** Compare measured query time, pool wait, input/output (I/O) pressure, cold-start behavior, recovery needs and cost over a representative workload. Identify the binding constraint and the expected benefit. A clinic-count milestone alone cannot establish that a different provider or larger instance solves the observed problem.

## Budget Connections, Memory and Storage Together

Sources: [Capacity model](23-hypothetical-clinic-metrics.md), [tenant isolation](02-multi-tenancy-rls.md), [deployment](10-deployment-infrastructure.md).

**Q:** What does a production Prisma pool maximum of 15 mean when both API and worker run?

**A:** It is a per-process limit. One API and one worker can allocate up to 30 connections through those pools, before other clients and administrative reserves. During an old/new API overlap that envelope can reach 45. Inventory every actual pool and compare the total with the provider's effective budget.

**Q:** Why is the RLS-enabled outbox batch normally capped at 13 rather than 200 in the production source profile?

**A:** Each tenant-scoped dispatch holds a connection. The relay takes the smaller of 200 and the configured 15-connection pool minus two reserved connections for coordination and acknowledgment. Thirteen is an admission bound under that configuration, not a measured delivery rate or a universal worker setting.

**Q:** Can SHOW shared_buffers reveal the database instance's physical RAM?

**A:** It reveals one PostgreSQL memory setting. The provider also needs memory for processes, working operations, caches and other services, and serverless allocation can have its own controls. Obtain the effective compute profile from the provider and correlate it with database observations rather than treating one setting as total RAM.

**Q:** Why is pg_database_size different from provisioned disk capacity?

**A:** It reports database storage usage within its defined scope, while provider capacity and free-space metrics describe a different resource envelope. Record relation/index sizes and provider storage together. Do not infer spare capacity, WAL retention or recovery storage solely from the size of one database.

**Q:** What storage headroom can a row-count estimate miss?

**A:** Indexes, large-value storage, row versions awaiting cleanup, write-ahead logs, temporary spills and maintenance operations can add space beyond live row payloads. Measure a representative fixture and observe growth during writes and maintenance. A payload-only estimate cannot serve as a disk-exhaustion threshold.

**Q:** Why can an index improve a list endpoint while increasing the system's cost?

**A:** The index can reduce reads for a selected predicate and ordering, but consumes storage and must be maintained on writes. Inspect actual plans, selectivity, write latency and index size together. Retain the benefit for the important workload rather than adding every plausible index without measurement.

**Q:** When would partitioning be a useful next experiment instead of a clinic-count rule?

**A:** Start from a measured large-table problem such as retention deletion, expensive pruning or maintenance pressure. Check whether the query predicates match a useful partition key and how uniqueness and migrations change. Partitioning adds operational work and does not automatically isolate tenants or accelerate every query.

**Q:** Does the modeled 2.98 GiB of prescription PDFs per month describe PostgreSQL growth?

**A:** That calculation assumes 20,800 documents at 150 KiB each and describes object payloads. PostgreSQL stores separate clinical data and document metadata, while indexes and operational records add their own growth. Estimate those stores independently and include retention, revisions and backups in the intended capacity boundary.

## Derive Traffic Before Selecting a Machine Count

Sources: [25-clinic workload](23-hypothetical-clinic-metrics.md), [deployment](10-deployment-infrastructure.md).

**Q:** How can 520,000 monthly requests produce both a 0.2 and a 0.69 requests-per-second average?

**A:** The first spreads traffic over all seconds of a 30-day month; the second spreads it across 26 eight-hour operating days. State which clock matches the workload. Neither average describes a synchronized clinic burst, offered stress load or the maximum sustainable capacity of the deployment.

**Q:** What additional assumption produces 20,000 distinct clinic-patients from 26,000 visits?

**A:** The model assumes 1.3 visits per distinct clinic-patient during the period and divides 26,000 by that value. It must be checked against a distinct-patient query for actual reporting. The appointment count alone cannot determine how many visits were repeat visits or new registrations.

**Q:** Why should a capacity model test sensitivity to its assumed 20 API requests per visit?

**A:** Autosave, pagination, polling, retries, invalidation and user navigation can change the number and cost of requests. Trace representative visits and vary the mix. Doubling cheap cached reads and doubling expensive report requests create different pressure even when the total request count changes by the same factor.

**Q:** Which response-time statistic belongs in a Little's Law concurrency calculation?

**A:** Use compatible long-run means for arrival rate and time in a stable, defined system. A P95 is not the mean. Align the system boundary, include waiting where appropriate and verify stability; substituting a tail percentile can produce a plausible-looking concurrency value without the law's conditions.

**Q:** How does the modeled busy window change the workload without changing its daily total?

**A:** Moving 30 percent of 20,000 daily requests into 30 minutes creates 6,000 arrivals, about 3.33 per second, and leaves 14,000 elsewhere. A separate 33.3-request-per-second stress exercise adds artificial demand. Keep those schedules distinct so the same daily population is not counted twice.

**Q:** What does a high 429 rate during a capacity experiment require me to distinguish?

**A:** Check intended rate-limit rejection, the identity/IP distribution of the generator and backend saturation separately. Report offered, accepted and rejected work. Bypassing production throttles to obtain a larger throughput number changes the contract and can conceal the resource protections the test should evaluate.

**Q:** Why can 200 staff accounts not determine a concurrent-user test?

**A:** Accounts describe provisioned identities. Simultaneous sessions depend on shifts, clinic behavior, think time and actions per session. Model those choices explicitly, including overlapping active work and long requests. A count of database user rows cannot supply the actual arrival schedule or in-flight concurrency.

## Interpret P95 and P99 With Their Population

Sources: [Percentile methods](14-analytics-and-dashboards.md#match-the-percentile-method-before-comparing-two-runs), [request observations](14-analytics-and-dashboards.md#preserve-the-observation-time-through-a-delayed-flush).

**Q:** Why can continuous and nearest-rank P95 disagree on identical observations?

**A:** Continuous percentiles interpolate between sorted values, while nearest rank selects an observed value. For the synthetic set 10, 20, 30, 40 and 50 ms, their P95 values are 48 and 50 ms respectively. Preserve the algorithm when comparing results so a method change is not mistaken for a performance change.

**Q:** What happens to a monthly traffic report if a delayed flush uses ingestion time instead of observation time?

**A:** Requests that happened earlier can appear in the later persistence window, changing both traffic and latency distributions. Select the original observation timestamp and retain ingestion time for capture diagnostics. Test an observation outside the range that is flushed inside it to expose this mistake.

**Q:** Why can a fast health probe make the customer-facing percentile look misleadingly good?

**A:** Frequent, short probes add many small samples to a pooled distribution. Classify the request population before aggregation and report customer traffic separately. A customer-only result can still need route-level breakdowns; removing probes does not make every remaining endpoint equally represented or equally costly.

**Q:** Why does an invalid duration not remove the request from the server-error denominator?

**A:** Duration validity and HTTP outcome are different properties. Keep the customer's observed response outcome while excluding its unusable timing from the latency distribution. Report both valid and invalid sample counts; otherwise a timing-instrumentation failure could make actual failed requests disappear from the error fraction.

**Q:** What makes a P99 based on a small sample unstable?

**A:** Very few observations determine the upper tail, so one slow or missing request can move the result sharply. Retain sample counts, repeated representative runs and timeouts. A producer's minimum-sample check guards basic completeness; it does not guarantee that the sample is large or independent enough for a precise tail estimate.

**Q:** Why report a cold-start distribution separately from warm steady-state latency?

**A:** Resuming the API, waking database compute and building caches can add work absent from warm requests. Their relative frequency can also change between runs. Report both experiences and their workload proportions so a faster warm path does not hide an unacceptable first request after idle time.

**Q:** Can a pooled customer P95 hide a problem after health checks have been excluded?

**A:** Yes. A high-volume cheap route can dominate lower-volume expensive operations, and one busy clinic can dominate others. Break down endpoint class and relevant workload dimensions, retain sample sizes and control label cardinality. Use the breakdown to investigate rather than average the resulting percentiles together.

**Q:** Which checks protect a before/after latency comparison from a cheaper but incorrect response?

**A:** Confirm the same authorization, fields, ordering, pagination and business result under the same dataset and request mix. Include failures and unfinished work alongside valid durations. A change that skips required work or rejects expensive requests cannot be interpreted solely as a faster implementation of the previous operation.

## Count the Workflow Rather Than Borrowing a Dashboard Label

Sources: [Business counter lineage](14-analytics-and-dashboards.md#follow-the-business-record-to-its-counter), [retained-data limits](14-analytics-and-dashboards.md#retained-samples-do-not-form-an-availability-monitor).

**Q:** Why can a completed-appointment total change when the same old reporting window is queried again?

**A:** The query selects appointments by scheduled start and their current COMPLETED status. Later corrections can change that status even though the selected dates stay fixed. A historical completion-event metric needs an authoritative event timestamp and correction policy rather than assuming a current-row query freezes history.

**Q:** How would I verify unique patients treated without reusing the new-registration counter?

**A:** Select the eligible completed visits and count distinct clinic/patient pairs in the same window. Repeat visits inside one clinic contribute once, while separate clinic identities remain distinct. Test those cases explicitly and state whether the product requires a separate global-person identity for another question.

**Q:** Which extra evidence is needed after counting 20,800 prescription records?

**A:** Identify whether the intended outcome is authoring, clinician review, document generation or authorized delivery. Each has a separate state and timestamp. A prescription row may have no generated PDF, and its existence cannot establish clinical correctness or that a patient received the document.

**Q:** Why must an invoice-created count stay separate from a collected-money metric?

**A:** An invoice can remain unpaid, be cancelled or be corrected, while provider capture, refunds and settlement follow their own lifecycle. Select the authoritative money events and currency rules for financial reporting. Multiplying an invoice count by a catalog price does not reconcile cash received.

**Q:** How should an empty request window appear on the dashboard?

**A:** Show zero retained request samples and unavailable percentiles/error percentage. There is no observed timing distribution or nonzero denominator to calculate those rates. Preserve a capture failure as an error or explicit coverage gap rather than displaying an empty result as measured healthy traffic.

**Q:** Why are new metric fields optional during the response-contract transition?

**A:** Old and new API/frontend versions can overlap. Version 2 emits explicit customer scope, P99 and new activity fields, while an older response lacks that evidence. The client must display unknown or unavailable rather than infer those fields, preserving compatibility without silently strengthening the older result's meaning.

**Q:** What does one SQL statement solve, and what does it leave unresolved for a dashboard snapshot?

**A:** Its subqueries share one statement snapshot, reducing inconsistencies from separate reads during concurrent changes. It does not make mutable source rows historical events, repair missing observations or choose correct business definitions. Record the cutoff and metric version, and test those semantic questions separately.

## Explain the Worker at the Effect Boundary

Sources: [Async processing](03-async-processing.md), [prescription documents](07-prescription-safety.md), [capacity model](23-hypothetical-clinic-metrics.md).

**Q:** Why does the default five-attempt queue setting not describe every PDF and outbox operation?

**A:** Producers can supply their own budgets: the PDF path requests three attempts, while the outbox has an eight-attempt policy. Trace the actual producer and relay before describing recovery. Also inspect which backoff options the selected queue backend honors; an option object alone does not establish the execution schedule.

**Q:** Why cannot a report-ingress P95 establish the time until a prescription PDF is ready?

**A:** The request can return after durable enqueue while the job still waits, renders and uploads its artifact. Measure from accepted durable intent to authorized artifact availability, and include failed or outstanding jobs. A quick HTTP acknowledgment can coexist with a long document backlog.

**Q:** Would doubling worker CPU necessarily double starts in a two-second polling lane?

**A:** A scheduler that claims one job per name per poll still has that admission pattern, even if execution becomes faster. Measure handler time, overlap rules and backlog age before choosing a remedy. More compute may help expensive rendering but cannot by itself remove a polling or coordination limit.

**Q:** How do claim tokens protect a job after its old worker becomes slow rather than dead?

**A:** A newly claimed attempt receives a new token, and acknowledgment must match the current owner. The previous worker cannot then mark the newer claim complete through a stale token. Effect-level idempotency remains necessary because fencing a database acknowledgment does not cancel already-started remote work.

**Q:** What should a retry do after a provider accepted work but the worker lost the response?

**A:** Preserve the uncertain outcome and use a stable provider-supported idempotency key or a reconciliation lookup when available. A new attempt without those semantics can repeat the external effect. A locally unique job record cannot prove what the remote provider already performed.

**Q:** Why must shutdown drain active work before disconnecting Prisma?

**A:** An in-flight handler can still need its scoped transaction, acknowledgment and outcome writes. Stop new claims, wait within a bounded grace period and close database resources in the intended order. Test shutdown during real work; a process that exits cleanly while idle does not exercise this boundary.

**Q:** How should a persistent provider outage influence the retry design and its dashboard?

**A:** Bound retries and backoff, preserve terminal or uncertain outcomes and expose queue age and remaining work. Repeated attempts consume shared database and worker capacity without guaranteeing delivery. Recovery should identify which operations are safe to replay and which require reconciliation or operator action.

## Diagnose the Resource That Actually Delays the Operation

Sources: [Observation lineage](14-analytics-and-dashboards.md), [production setup](10-deployment-infrastructure.md), [capacity experiments](23-hypothetical-clinic-metrics.md).

**Q:** Which observations help separate a CPU bottleneck from garbage-collection pressure?

**A:** Correlate request latency with CPU use, event-loop delay, heap growth, collection pauses and RSS over the same interval. Capture a profile for the expensive path. High CPU and a large heap are symptoms with several causes; increasing memory without locating retained objects can merely postpone a leak.

**Q:** Why can server-side duration look good while the user's action remains slow?

**A:** Browser work, network exchanges, proxy waits, retries and time before the server's timer begins can sit outside the measured duration. Compare client and server boundaries using safe correlation identifiers. Instrument the missing segment rather than assuming one fast server percentile represents the complete interaction.

**Q:** How can API latency satisfy its budget while the clinic still waits too long for a document?

**A:** Interactive requests and background completion have separate queues and deadlines. Enqueue can remain fast as the worker backlog grows. Inspect oldest-job age, enqueue-to-artifact delay, failures and worker activity together; increasing API instances would not address a worker or provider bottleneck identified by those observations.

**Q:** What should I investigate when recorded 5xx responses fall to zero during a database incident?

**A:** Verify that request observations continued to persist and that capture-gap events are visible. A logger that cannot write can leave an apparently clean retained set. Compare independent probes and application outcomes, and preserve the missing interval instead of interpreting the absence of recorded failures as recovery.

**Q:** How can a request be correlated with its later job without copying clinical payloads into logs?

**A:** Carry a bounded, authorized operation identifier through the request, durable intent and outcome records. Log state transitions and timing rather than patient content or provider secrets. Review identifier sensitivity and access controls; a correlation key remains capable of revealing relationships even when names are omitted.

**Q:** Why can pool wait rise even when database CPU is low?

**A:** Connections may be held by long transactions, idle scopes or blocked work, leaving new callers waiting before their statements reach execution. Compare pool acquisition time, transaction duration and database activity/locks. A bigger database CPU allocation cannot directly repair an application that holds scarce connections unnecessarily.

**Q:** How would I test whether one large clinic harms the others without weakening tenant checks?

**A:** Run a controlled mixed-tenant workload and compare per-tenant latency, accepted work, pool use and queue age under the same authorization rules. Add suitable admission or resource bounds for the demonstrated shared bottleneck. An isolated cross-tenant denial test establishes a different property from noisy-neighbor fairness.

## Release, Restore and Cost Need Separate Acceptance Checks

Sources: [Deployment and recovery](10-deployment-infrastructure.md), [capacity model](23-hypothetical-clinic-metrics.md).

**Q:** Why must a blue-green release appear in the database-capacity calculation?

**A:** Old and new application versions can hold separate pools while both remain alive, and migration/admin work may overlap. Budget that temporary maximum before rollout. Verify schema and job-payload compatibility as well as connection availability; a green process starting does not establish either property.

**Q:** Which three health questions should a production setup answer independently?

**A:** Ask whether the process is alive, whether it is ready for its defined traffic and whether an important business operation succeeds. Keep dependency-heavy checks from destroying liveness semantics. A database outage, an unavailable provider and a stuck worker can require different routing and operator responses.

**Q:** What makes a backup-restoration drill support an RTO claim?

**A:** Time the complete recovery to verified service, including database restoration, secrets/configuration, compatible application startup and integrity/business checks. Record the recovered cutoff for RPO separately. The presence of scheduled backups or a successful download does not establish the time or correctness of restoration.

**Q:** What should happen when the required latency-baseline gate has no artifact?

**A:** Keep the performance acceptance result blocked and run a complete controlled capture before declaring the budget met. Do not replace the artifact with the SLO numbers themselves. The gate's ability to reject absent evidence is useful behavior, but it supplies no achieved latency measurement.

**Q:** How should the low-cost and balanced resource profiles be compared?

**A:** Keep the application revision, data distribution, request mix and correctness checks equivalent, then record cost and resource pressure alongside outcomes. Test cold behavior and failure recovery as separate cases. A cheaper idle configuration and a stronger proposed profile cannot be compared using assumed throughput alone.

**Q:** Why are a Multi-AZ standby and a read replica different design choices in a future AWS setup?

**A:** Their intended availability, read-routing, replication and failover roles differ, and neither removes consistency or recovery decisions from the application. Verify the chosen service's behavior and costs. Do not count a standby as extra read capacity without confirming that the selected topology actually serves those reads.

## Reproduce the Capacity Claim Safely

Sources: [Benchmark procedure](23-hypothetical-clinic-metrics.md#turn-the-model-into-a-reproducible-benchmark), [known-fixture reconciliation](14-analytics-and-dashboards.md#reconcile-a-small-fixture-before-generating-a-large-one).

**Q:** What must a 25-tenant fixture contain beyond 25 clinic rows?

**A:** Include realistic patient/visit distributions, prescription and invoice relationships, permissions, historical rows, document shapes and a reproducible seed. Record which counts are inputs and which are generated outcomes. Empty tenant rows cannot exercise the data access, contention or background work implied by the workload model.

**Q:** Which protections should isolate a destructive capacity fixture from real clinical data?

**A:** Use an explicitly designated test database, verified connection identity, synthetic records and guarded cleanup. Disable real provider sends and payment effects. Fail closed when the environment is ambiguous, and record the tested revision and reset procedure so another engineer can repeat the experiment without touching production.

**Q:** What should a PDF capacity check assert besides a completion status?

**A:** Verify a readable generated artifact, its expected document association, storage availability and authorized access. Exercise representative content sizes and missing assets. Keep synthetic clinical content and simulated delivery; a success flag alone can hide an empty file, the wrong document or a broken access path.

**Q:** Why do passing mocked unit tests not replace the isolated database experiment?

**A:** Mocks can pin branching, contracts and error handling while bypassing real locks, indexes, roles, network exchanges and transaction behavior. Retain those useful tests, then exercise the relevant invariant against the actual database engine and resource profile. State the scope of each result rather than promoting one into another.

**Q:** Why should a growth experiment retain old data while testing a recent-month report?

**A:** Historical rows and indexes can affect plan choice, cache fit and maintenance even when the response selects a recent window. Seed a stated history and compare plans/resource use as it grows. Recreating only one clean month can hide the conditions that change the production bottleneck.

**Q:** How should a failed rollout experiment be checked after returning to the previous application version?

**A:** Reconcile existing records, queued payloads and external outcomes under the resulting schema, then run the representative business probes. An old image can be incompatible with new writes or migrations. Record what was restored and what still requires a forward repair rather than stopping at the process version.

**Q:** What should stop a capacity run before it produces a misleading headline throughput?

**A:** Define limits for correctness failures, unacceptable latency/error rates, growing backlog, resource exhaustion and generator overload before starting. Retain the offered and rejected work when a limit is reached. A high count of fast successful responses cannot compensate for dropped operations or an unbounded recovery debt.

## Explain the Executed Monthly Aggregate Fixture

Source: [Known-volume SQL verification](14-analytics-and-dashboards.md#verify-the-sql-at-a-known-monthly-row-volume).

**Q:** Which part of the 25-clinic model was actually checked at its stated row volume?

**A:** The real operational aggregate ran on projected PostgreSQL fixture tables with 26,000 appointments, 20,800 prescriptions, 26,000 invoices, 20,000 distinct clinic-patient pairs and 520,000 customer observation rows. Exact counts were asserted. This does not replay clinical operations or establish how the full schema, RLS role, API and worker behave together.

**Q:** Why are P95 470 ms and P99 494 ms from the regression not API performance achievements?

**A:** They are continuous percentile calculations over supplied values 100, 200 and 500 ms. The test proves eligible-row selection and arithmetic, including delayed persistence and invalid samples. No HTTP operation took those measured times. A real performance claim needs actual operation timings, load, resources, errors and capture coverage.

## Operate From the First Clinic Through Growth

Sources: [Launch and growth](25-launch-to-growth.md), [deployment profile](10-deployment-infrastructure.md).

**Q:** What changes when the first clinic joins even if the machine is mostly idle?

**A:** The service now needs defined opening hours, support, data responsibilities, complete workflows, recoverable records and a fallback. Resource pressure and customer obligations grow differently. A small CPU bill cannot establish that those obligations are met.

**Q:** Why does a working appointment endpoint not establish a usable clinic day?

**A:** The patient/tenant identity, booking state, clinical record, prescription or invoice artifact and relevant provider outcome must agree. Follow the whole operation and retain unresolved exceptions. A stopped document worker can leave an otherwise successful interactive action incomplete.

**Q:** How can onboarding return an error after creating a clinic?

**A:** Provisioning commits before some session cleanup, audit/event and authentication-response work. A later failure does not undo the database commit. Reconcile clinic, administrator, subscription and payment state before repeating completion.

**Q:** Why is the SLA proof PDF outside the database's atomic guarantee?

**A:** Its generation/upload occurs while the database transaction is open, but the object store does not join that transaction. A rollback can leave an uploaded orphan and an upload can lengthen connection hold time. Reconcile those effects rather than calling the entire procedure atomic.

**Q:** What makes an accepted bulk import vulnerable to process restart?

**A:** The inspected implementation persists job metadata but keeps parsed rows in memory and uses process-local execution. The inline marker is not a durable recoverable payload. Supervised bounded imports and row reconciliation contain the current boundary; durable payloads, checkpoints and restart tests are separate work.

**Q:** What evidence moves onboarding from one pilot to repeatable operation?

**A:** Another operator can follow the versioned checklist, reconcile imported rows, configure roles/providers and train the clinic without undocumented knowledge. Define activation as a completed useful workflow in an eligible cohort, then measure it. Sign-ups and demonstrations alone do not establish activation or paid retention.

**Q:** Which checks should precede every clinic opening?

**A:** Verify intended API/worker availability, readiness, oldest pending work, provider condition, backup freshness, open incidents and reachable escalation. Record failed checks and the clinic fallback. A successful health route does not establish background completion or usable restoration.

**Q:** Why are feature flags not a guaranteed instant global stop?

**A:** The inspected global cache and invalidation are process-local; a nominal expiry setting is not a tested replica-wide deadline. Verify enforcement at the actual operation and propagation behavior. Plan incident containment that remains effective when a process has a stale value.

**Q:** What decides whether to add a machine at ten or twenty-five clinics?

**A:** Retained measurements of request tails, memory, database waits, worker age, tenant skew and support coverage identify the limiting promise. Test the smallest relevant change with its connection/cost/rollback budget. Clinic count alone cannot identify the bottleneck or justify a shared cache or service split.

**Q:** What makes a Neon-to-AWS rollback unsafe after cutover?

**A:** New writes on the target can diverge from the old source. Returning to the source needs an explicit reconciliation or reverse-transfer plan and a bounded decision window. Changing the connection string alone can lose accepted work or replay provider effects.

**Q:** Why does cancellation not mean every clinical record is immediately deleted?

**A:** Financial close, access revocation, authorized export, retention/hold decisions, provider/object copies and restored-data reconciliation are separate actions. Record the completed scope and remaining exceptions. Do not claim physical erasure for actions that have not been executed and verified.

**Q:** Why is a design partner not automatically a paid clinic or public reference?

**A:** Agreement to test a bounded workflow does not establish successful paid conversion, continuing use or permission to publish the clinic's name. Record these separately and obtain the relevant authorization before using an endorsement. Advance the next cohort only when service and support evidence allow it.

**Q:** How can a growth chart hide churn?

**A:** New clinics can offset losses in an older cohort while total accounts rise. Measure active/paid retention against the matching starting cohort and report cancellation/nonrenewal reasons separately. Use the same maturity window when comparing paid conversion; unelapsed trials should not lower a mature-cohort conversion rate.

**Q:** Why should optional inpatient, insurance or AI features wait during an outpatient pilot?

**A:** They add domain transitions, training, data-flow and provider costs beyond the agreed core slice. Enable them for an identified need only after their own readiness checks pass. Repository presence does not establish operating readiness, and adding optional modules cannot repair a failed appointment-to-document workflow.

## Explain Monthly Costs and Their Boundaries

Source: [Monthly operating costs](26-monthly-operating-costs.md).

**Q:** What is missing from a statement that a stopped application costs nothing?

**A:** Stopped root filesystems, provisioned volumes, allocated IPs, database storage, plan minimums and retained objects can continue billing. Inventory actual resource states and billing units. A stopped API also cannot establish completion of promised scheduled work.

**Q:** Why can a Singapore machine estimate differ from Fly's headline machine price?

**A:** The headline can use the lowest-priced region. Use the intended region's multiplier/rate, runtime seconds and memory allocation, then add independent resources and transfer. A global list price is not necessarily the rate of the deployed resource.

**Q:** Why does 0.25 CU not mean a database with 0.25 GB of storage?

**A:** A compute unit describes compute/memory, while retained PostgreSQL storage has its own meter. Launch compute integrates actual CU size over active time. At the quoted rate, 0.25 CU for 720 hours costs $19.08 before storage and history.

**Q:** Can Launch subtract the Free plan's first 100 CU-hours?

**A:** No. Those are different plans. Price Launch at its quoted CU-hour rate and apply only the allowances belonging to that plan. Similarly, do not silently multiply account-wide object/edge allowances by clinic count.

**Q:** Why can a paid edge plan be appropriate below ten million monthly requests?

**A:** Free limits can apply per day or per invocation, and plan selection can depend on enabled features and operational needs. Check peak daily requests and CPU work as well as totals. A monthly average cannot prove the Free limits or the service promise fit.

**Q:** How do 46,800 files at 150 KiB become different GB and GiB numbers?

**A:** Divide their bytes by one billion for decimal GB or by 1,073,741,824 for GiB. The result is 7.18848 GB or about 6.6948 GiB. Use the provider's billing unit and actual time-weighted inventory, rather than treating those numbers as interchangeable.

**Q:** Why is the twelve-cohort R2 example not the bill for every month of the first year?

**A:** Earlier months contain fewer accumulated objects and R2 uses average daily peak inventory. The $1.155 storage comparison holds twelve cohorts constant for a whole month. Actual accumulation, versions, uploads, backup copies and account-wide allowance consumption change the charge.

**Q:** Why does a public-RDS allowlist example need two Fly egress allocations?

**A:** The API and worker are separate Fly applications. The proposed app-scoped static egress allocation is shared within an app/region, not automatically across both apps. Price both allocations and the chosen AWS public IP, enforce the actual addresses and TLS, and quote private connectivity separately if chosen.

**Q:** What does the $80.34 RDS example include?

**A:** It includes 720 hours of Singapore PostgreSQL Single-AZ db.t4g.medium at $0.102/hour and 50 GiB provisioned gp3, priced as 50 provider storage units at $0.138/GB-month. It excludes connectivity, surplus credits, extra backup/transfer, monitoring, support and tax. It does not buy Multi-AZ availability or prove workload capacity.

**Q:** Can 52,000 WhatsApp intents be multiplied directly by a delivery price?

**A:** Only as an explicitly conditional illustration that all become billable deliveries in the specified market/category. Actual charges depend on delivery, exemptions, rate tier, provider agreement and duplicate effects. Reconcile the current account rate card when official source narratives conflict.

**Q:** Why do 52,000 recipient emails cost $15 cash but $13 of usage in the example?

**A:** Six 10,000-email credits at $2.50 are needed from a zero balance, leaving 8,000 emails unused. Usage consumes 5.2 credits. Retain the opening/closing balance and expiry; expired unused credits still cost cash.

**Q:** What extra information is needed to price 5,200 payment attempts?

**A:** Successful eligible payment amounts, payment method and contracted rate, fee tax, refund/dispute/optional-service treatment and merchant ownership. Attempts alone lack both the successful-value denominator and payer. Clinic patient collections must not become Docita subscription revenue.

**Q:** Why is the $75 Neon comparison not an all-inclusive monthly bill?

**A:** It prices declared runtime/database/edge/object/transfer inputs only. Add actual recovery, staging, monitoring, email/messages, payment/AI, domain, tax and labor. Keep any planning allowance visibly separate from quoted provider rates and reconcile the complete result with invoices.

**Q:** What belongs in a monthly budget variance review?

**A:** Compare actual units and prices by environment and payer, account-wide allowances, prepaid balances, tax/currency and invoice charges against the forecast. Explain the difference and assign a next action. Check the service outcomes too, so cost savings do not hide missing reminders, retention or recovery work.

## Produce Operating Evidence, Not Just More Output

Sources: [Operating workbook](27-operating-evidence-workbook.md), [availability preflight](10-deployment-infrastructure.md#reproduce-the-local-checks-before-a-release), [calendar/cost arithmetic](26-monthly-operating-costs.md#reproduce-the-infrastructure-arithmetic).

**Q:** What does a passing command-availability preflight establish?

**A:** Required files and script entries exist in that checkout. It does not verify their revision, dependencies, target isolation or behavior. The clean base lacks capacity additions, so identify the reviewed unpublished patch before offering its commands as a fresh-clone recipe.

**Q:** Why can migrations, seed and the running API target different databases despite one copied example file?

**A:** Their loaders and working directories differ, and exported variables or higher-priority files can override the intended target. Inspect root and process-specific configuration and explicitly verify the same owned target before any write. A loopback HTTP address alone says nothing about the backend's database/provider destinations.

**Q:** Why do PostgreSQL queues not solve every separate-worker setup issue?

**A:** They share queued work, while process environment, scheduler ownership, decryption keys and object paths remain separate. Local storage defaults to each process's working directory. Prove that the API can retrieve the intended worker artifact rather than equating a completed job with accessible output.

**Q:** What can the ordinary critical-flow E2E leave unverified?

**A:** Creation of patient/appointment/prescription/invoice records does not establish document retrieval, standalone-worker completion, cross-clinic denial, provider settlement/delivery or full restoration. Its general setup can reset/truncate a database, so use only a positively identified owned target and retain the exact assertion scope.

**Q:** How can a tenant integration suite appear harmless while affecting another local project?

**A:** Its fixture role can be cluster-wide even if tables are confined to a test database. Use a separately owned cluster, inspect cleanup and verify a non-skipped execution. A missing environment prerequisite that skips the suite supplies no tenant-isolation evidence.

**Q:** Why is an old QueueJob row not automatically a long queue-wait measurement?

**A:** It may be delayed until a future retry, currently active or terminally dead-lettered. Age since initial enqueue is a different observation from ready-to-start wait or handler duration. Reconcile generic queue state with the intended PdfJob/document/object result.

**Q:** How should a diagnosis begin when latency rises while CPU looks quiet?

**A:** Select an observation that separates pool wait, locks, long transactions, query execution and external dependency time. Retain the predicted and actual result. Adding API replicas before identifying connection pressure can make the same constraint worse.

**Q:** What is the 30-day time budget for a 99.9% objective?

**A:** Exactly 43 minutes 12 seconds over a 30-day window. A request-based objective instead counts eligible good/bad events. Do not turn percentile headroom in milliseconds or a fixed charge per incident into an error budget.

**Q:** How does a 1% observed bad fraction relate to a 99.9% good-event objective?

**A:** Its burn rate is 10 times the allowed 0.1% bad fraction. Consumption of the complete period's budget also needs that period's eligible population and capture coverage; a burn rate alone does not supply those counts. Define windows, minimum evidence and zero-traffic/unknown handling before alerting.

**Q:** What should change when the calculator moves from 720 to 744 hours?

**A:** Every modeled hourly meter: Fly runtime, Neon CU-hours, RDS instance-hours and allocated hourly IPs. The current comparison intentionally holds monthly storage/traffic/minimums fixed. It is a sensitivity comparison rather than a statement that another day creates no additional real usage.

**Q:** Why can an hourly full-backup policy overwhelm a small tooling allowance?

**A:** Retention multiplies archive size by copies kept. One GB per hourly full archive retained 31 days holds 744 GB in steady inventory, before other data and verification work. Measure compressed size and cleanup/lock behavior, fund the line explicitly and keep database-used bytes separate from archive size.

**Q:** Why is acquisition cost per clinic not the month's acquisition expense?

**A:** Monthly spend and attributed labor are expenses; dividing by newly acquired paying clinics produces a unit metric. Keep the units and period separate and do not add the same sales labor twice. A zero-conversion month still has cash costs even when a per-acquired-clinic ratio is undefined.

**Q:** When does the break-even formula stop supporting a growth decision?

**A:** If contribution is nonpositive, or if the workload, payer, paid fraction, fixed capacity or staffing assumptions change. Include the cost of nonpaying pilots and distinguish revenue from successfully processed amounts. A modeled positive month does not remove an earlier cash deficit or establish actual collections.

**Q:** What is required before a promotion record can say pass?

**A:** Actual scoped evidence for correctness, operations/load, recovery, funding and owner coverage. A template, source path or missing prerequisite is not a successful experiment. Record fail/blocked outcomes and the next owned action rather than filling every field with assumed success.

## Explain the Executed Local Boundary

Sources: [Executed local checks](27-operating-evidence-workbook.md#what-the-local-continuation-actually-executed), [all-invalid metrics](14-analytics-and-dashboards.md#keep-the-error-rate-when-every-timing-is-invalid).

**Q:** Why can an error rate remain known when every percentile is unavailable?

**A:** Request outcomes and timing validity are different properties. In the synthetic three-request case, two server errors give a 66.67% retained-request error rate, while zero valid durations leave P50/P95/P99 null. That still does not prove the retained rows cover every real request.

**Q:** What did the cancelled tenant-suite attempt establish?

**A:** Its setup collided with a cluster-wide role before any of its 15 test cases ran. It established an isolation prerequisite failure, not failed tenant guarantees. The corrected separate-cluster run passed all 15 cases; keep both attempts and preserve the other database's role dependencies.

**Q:** What do successful migrations and a zero schema diff leave untested?

**A:** They establish that the current chain installs and matches its declared schema on that local database. They do not establish safe upgrades from every old state, complete API authorization, clinical transitions, provider effects, performance or recovery. Those need their own runtime evidence.

**Q:** Why is the successful local API read not a production tenant-isolation verdict?

**A:** That profile used a development owner role with RLS disabled and exercised one synthetic staff identity. Its anonymous denial, login/session and list results are useful HTTP evidence, while the non-owner tenant suite is a different fixture boundary. Neither becomes complete cross-clinic API coverage by combining their pass counts.

**Q:** What must remain visible about the experiment-only listener shim?

**A:** It forced the built API's wildcard bind to loopback for this controlled run, whose actual listener was checked. The production source was not changed by it. Report that deviation and the tested network-policy limits rather than claiming a deployed fix or universal sandbox isolation.

**Q:** Why can the developer seed pass while PDF retrieval remains unverified?

**A:** It can create metadata and write sample files in its own known directory while a separately launched API serves another working directory. Reconcile the actual storage root, intended artifact and authorized retrieval. The seed's one synthetic clinic and sample counts also do not become a 25-clinic workload or adoption result.

## Explain the Clinical and Document Readback

Sources: [Created-record evidence](27-operating-evidence-workbook.md#follow-a-created-record-beyond-its-http-status), [corrected engine checks](27-operating-evidence-workbook.md#verify-the-correction-against-the-engine-again), [PDF paths](03-async-processing.md#a-downloaded-pdf-does-not-prove-worker-completion).

**Q:** How could four successful creates still fail the clinic-association check?

**A:** The prescription related to the intended patient, appointment and doctor, but its direct clinic field was null. The service dropped clinic context and the repository omitted the clinic connection. Both boundaries needed correction, followed by a new real API write and database readback. Existing historical null rows require separate reviewed reconciliation.

**Q:** Why did the local write exercise change two fixture settings explicitly?

**A:** Prescription creation requires a verified signed doctor, while the synthetic seed starts unverified. Immediate event handlers can also run with schedulers off. The owned fixture temporarily used VERIFIED status and disabled clinic WhatsApp automation; both original settings were restored. That does not establish real verification, production RLS or provider delivery.

**Q:** What did an invoice total of 50,000 paise establish in this exercise?

**A:** Its pending record and one line reconciled to the server's exempt-healthcare calculation, with zero tax, discount and paid amounts. Consent and its audit also existed. Zero payment sessions and the failed payment-link attempt did not establish settlement or a durable retry, even though invoice creation returned 201.

**Q:** Why must a stored PDF check compare the returned bytes with an existing object?

**A:** A protected local staff route can regenerate a PDF while ignoring the stored reference. The capability proxy's existing-key path reads the object instead. Matching the returned bytes to the deliberately placed synthetic file establishes that stored-read branch; it still says nothing about standalone-worker completion or a different storage-root mapping.

**Q:** Does a valid document capability prove that its expiry was checked?

**A:** No. The inspected application capability uses HMAC over document type and identity and has no expiry field or check. Its malformed/tampered and wrong-type denials establish those boundaries only. R2 presigned URLs have a different lifetime contract; do not transfer that expiry claim to every document link.

**Q:** What did the failed full-seed rerun change about the setup conclusion?

**A:** Existing lab orders blocked deletion of their referenced tests. The run did not establish an idempotent refresh, even though bootstrap had worked on a fresh database. Retain the failed state and its snapshot, then distinguish a successful new-database seed from a repaired rerun. A stored dump also is not a tested restore.

## Explain the Separate Worker Boundary

Sources: [Worker clinic context](03-async-processing.md#a-separate-worker-must-enter-the-jobs-clinic), [separate-worker evidence](27-operating-evidence-workbook.md#make-the-separate-worker-own-the-effect).

**Q:** Why did a worker consume valid queued jobs yet fail both PDFs?

**A:** HTTP request context does not travel into another process. The worker's domain reads lacked an AsyncLocalStorage clinic scope, so the tenant guard rejected them. After three attempts each, the queue rows were dead-lettered and PDF rows failed. The correction scopes awaited read/render/store work to the queued clinic without a broad domain bypass.

**Q:** Why must a worker replace an inherited caller's context and restore it afterward?

**A:** A caller may carry another clinic or an unrestricted marker. Reusing it would apply the wrong authority to the job. A fresh job scope spans each awaited operation, then restores its caller after completion or error. Narrow status-update bypasses remain separate from ordinary document queries. Application context still does not prove SQL RLS setup or non-owner enforcement.

**Q:** How can a completed queue row show zero `attemptsMade`?

**A:** This implementation increments that field on failures. A successful first execution leaves it zero, while the execution-history row records COMPLETED at attempt 1. Reconcile status, history, document metadata and actual bytes; do not interpret one counter as evidence that the handler never ran.

**Q:** What closes the separate-process PDF proof beyond a 202 response?

**A:** Pending rows with the worker stopped, then successful worker execution, completed queue/PDF rows, canonical document references, newly generated files and byte-equal downloads. Protected status and capability reads exercise different boundaries. A synchronous staff PDF response can regenerate bytes and cannot substitute for this chain.

**Q:** What did the shared-directory profile and scheduler census leave unproved?

**A:** One filesystem and CWD aligned local API/worker files; it did not share disks across Fly machines or validate R2. Enabling worker PDF handlers also enabled the wider cron graph. Controlled fixture settings and observed row counts bounded that experiment; they did not prove every scheduler path, restart recovery, provider effect, production memory limit or 25-tenant workload.

## Summary

Reconstruct the operation and its boundaries. Qualify every outcome according to the evidence actually obtained.

## See Also

- [Case-study index](INDEX.md) — reading stages and source-linked cases.
