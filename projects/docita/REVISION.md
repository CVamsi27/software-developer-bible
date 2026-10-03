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

**A:** They use different stocks, events, rollups, membership windows and denominator semantics rather than one identical ledger calculation.

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

**A:** No. The combined quantile must represent eligible pooled observations or compatible mergeable distributions; averages of quantiles lose the distribution and population weighting.

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

## Current Resume Bullet Walkthrough

Source: [Seven-bullet walkthrough](24-resume-claim-walkthrough.md).

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

Source: [Actual-record dashboard](14-analytics-and-dashboards.md#a-dashboard-built-from-actual-records-and-retained-telemetry).

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

## Summary

Reconstruct the operation and its boundaries. Qualify every outcome according to the evidence actually obtained.

## See Also

- [Case-study index](INDEX.md) — reading stages and source-linked cases.
