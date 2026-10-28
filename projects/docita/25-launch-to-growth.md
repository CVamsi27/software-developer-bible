# 25 — Launch a Clinic Product and Grow Through Evidence

[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)

Consider a clinic that books its first patient while the document worker is stopped. The appointment can succeed while background document generation and scheduled reminders remain unavailable. Adding another clinic makes this failure affect more people; adding another API machine does not start the worker or resolve its unfinished work.

The launch decision must connect product behavior, people, operating cost and recovery. This chapter follows that decision from a local prototype through a proposed 25-clinic workload. Detailed resource setup belongs in [deployment](10-deployment-infrastructure.md), workload arithmetic in [capacity modeling](23-hypothetical-clinic-metrics.md), measurement definitions in [analytics](14-analytics-and-dashboards.md), and dollar estimates in [monthly operating costs](26-monthly-operating-costs.md).

## Definition

An application lifecycle is the sequence of decisions and operating work that turns a tested product into a service people can depend on, then maintains that service through releases, customer growth, failures, renewals and eventual data exit.

> **Textbook Definition:** Application lifecycle management coordinates requirements, implementation, verification, release, operation and retirement, preserving traceability between business commitments, software behavior, infrastructure capacity, operational ownership and evidence of successful execution.

**Evidence boundary, 28 October 2026:** this chapter combines a scoped inspection of Docita source based on `f3fddffc0`, the dated infrastructure observations in chapter 10 and existing operational records. It does not establish actual clinic adoption or a completed production launch. The current low-cost Fly/Neon setup remains unchanged. AWS is a future balanced reference; modeled clinic counts and proposed gates are not deployed capacity or achieved service levels.

## First Principles

A clinic needs a complete operation, not an isolated successful endpoint. A visit may require authentication, tenant access, scheduling, clinical records, files, billing and an external message. Each boundary can fail separately. The operating plan must make accepted work recoverable and make missing work visible.

Growth creates two different pressures. More operations consume resources; more customers create support, training, privacy, billing and availability obligations. A small number of busy clinics can exhaust the first budget, while many quiet clinics can exhaust the second. Clinic count is therefore a planning dimension, not a hardware-sizing rule.

Move to the next stage when its evidence exists. If a safety, restore or support gate fails, pause that promotion while fixing the specific boundary. Record a waiver only with its owner, affected promise, expiry and containment; a waiver does not turn an unverified capability into a verified one.

## Follow the Whole Lifecycle

```text
One clinic problem + bounded product promise
                    |
                    v
Stage 0: local vertical slice with synthetic data
  requirements -> implementation -> meaningful checks
                    |
          reproducible setup and workflow
                    v
Readiness review: tenancy, recovery, support, spending
                    |
             every required gate passes
                    v
Stage 1: supervised pilot and first complete clinic day
                    |
            reconciled work + trained owner
                    v
Stages 2-5: repeatable onboarding and support
                    |
           retained operating measurements
                    v
Stages 6-10: predictable release and incident handling
                    |
        tested workload + restore + cost forecast
                    v
Stages 11-25: accept the intended operating profile
                    |
             new measured constraint
                    v
25+: revise assumptions, test one change, review again

At every live stage:
  incidents -> contain -> recover -> verify -> improve
  releases  -> compatible rollout -> health -> rollback decision
  exits     -> billing close -> export/access -> retention reconciliation
```

The numbered bands describe proposed clinic counts, not observed customer cohorts or automatic hardware thresholds. The arrows are promotion decisions. They do not authorize changing provider plans, restarting a maintenance environment or enabling production schedules. A feature can move backward to supervised operation when its evidence becomes stale or its failure mode changes.

## Stage 0: Validate One Useful Workflow Locally

Start with a clinic problem stated in observable terms: staff must book a slot, identify the correct patient, complete the visit and retrieve the intended invoice and prescription. State exclusions too. An outpatient pilot does not automatically require inpatient admission, insurance, laboratory integrations, AI or every optional module.

| Work | Concrete output | Completion condition |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Product scope | One workflow, supported roles, opening hours, expected record ownership and explicit exclusions | A clinic representative can recognize the intended result and the limits of the pilot |
| Data design | Tenant identity, record relationships, audit needs, money/time units and data classes | Each write has an authoritative tenant and each external effect has a recovery decision |
| Local setup | Follow Docita `docs/ONBOARDING.md` and `docs/product/ONBOARDING.md`; install pinned dependencies, start the documented local database, configure local variables, migrate and seed | A fresh environment reaches the workflow without undocumented machine state |
| One vertical slice | Browser action through API authorization, database write, background work and retrieved artifact | Success and representative rejection/failure paths are reproducible with synthetic records |
| Verification | Tests at the real correctness boundary, type checks, build and required repository gates | Retain exact commands, revision and results; skipped or credential-blocked checks remain visible |
| Release preparation | Isolated staging configuration, migration compatibility, synthetic provider setup and rollback target | Staging is separated from production data and cannot send unintended real messages or charges |
| Operating design | Named release/incident owner, support window, recovery targets and resource budget | Promises are limited to what the next stage can verify and staff can support |

The setup guides onboard developers; they are not a clinic go-live checklist. Keep real patient records, production credentials and customer contracts out of seeds, screenshots, fixtures and public learning artifacts. A clean build establishes executable code, while the live-service review below establishes a different boundary.

### Sequence Features Around the Pilot's Actual Work

| Feature group | Proposed sequence and release condition | Canonical mechanism |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Identity, roles and tenant access | Mandatory before patient work: staff authentication, authorized clinic membership, least privilege and cross-clinic denial | [Architecture](01-architecture-decisions.md) and [tenant isolation](02-multi-tenancy-rls.md) |
| Appointment and completed visit | Mandatory pilot slice: supported booking/check-in/consultation states, conflicts, timezone and relevant clinical record | [Clinic workflows](05-clinic-workflows.md) |
| Prescription and invoice | Mandatory for the proposed outpatient pilot: correct records, retrievable prescribed document, invoice state and explicit exception handling | [Prescription safety](07-prescription-safety.md), [billing](08-billing-invoicing.md) and [documents](19-documents-and-uploads.md) |
| Subscription and paid access | Define trial/paid/cancellation policy before offering it; release only the plans and transitions whose entitlement and reconciliation paths pass | [Subscriptions](09-subscription-system.md) |
| Messaging and online payment | Bounded additions: enable only the required channel/merchant flow after consent, provider setup, cost and failure/replay checks | [WhatsApp](06-whatsapp-integration.md), [payments](04-payment-flows.md) and [async work](03-async-processing.md) |
| Inventory, inpatient and insurance | Optional: add only for an identified clinic need, trained users and independently verified domain transitions | [Inventory](13-inventory.md), [inpatient](12-ipd-inpatient.md) and [insurance](11-insurance-claims.md) |
| ABDM, laboratories and optional AI | Optional: verify integration readiness, applicable permission/data flow, clinical review boundary, provider cost and failure handling before enabling | [ABDM](17-abdm-integration.md), [clinical/lab domains](20-clinical-lab-and-medical-coding.md) and [prescription safety](07-prescription-safety.md) |

The mandatory slice is a proposed scope for this outpatient pilot, not a claim that every clinic must adopt every feature. Revise the scope deliberately when discovery identifies a different workflow. Feature presence in the repository is not its launch approval; optional modules should not delay proving the agreed core journey or bypass their own readiness gates.

## Stage 1: Make the First Clinic a Supervised Pilot

Entry requires the local workflow and readiness evidence. The pilot adds real operating responsibility, even if access is free. Define who can stop a workflow, who receives an incident, and which manual fallback the clinic can use while the service is unavailable.

| Launch gate | Evidence before enabling clinic work | Hold condition |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| Service hours and processes | API readiness and first-request behavior under the chosen warm/idle policy; worker heartbeat and schedule ownership for promised background work | API traffic can wake an existing API machine but the required worker remains stopped |
| Tenant access | App-role tests against relevant tenant policies, including cross-clinic denial and privileged bootstrap boundaries | Owner/BYPASSRLS credentials or unverified policy coverage are treated as proof of isolation |
| Core workflow | Booking conflict handling, correct patient/clinic records, document retrieval and invoice state verified in the intended environment | Only mocks, SQL count fixtures or GET requests have passed |
| Provider boundary | Appropriate merchant/account configuration, signature verification, sandbox reconciliation and applicable patient communication consent | A message attempt or payment order is described as delivery or captured revenue |
| Recovery | Usable backup of required data classes, object/key custody, restore verification and measured recovery scope | A synthetic empty-table drill or prepared backup script is the only evidence |
| Release safety | Current mandatory checks, schema-compatible rollback target and supervised health window | Missing latency baseline or an unrelated failing gate is silently marked green |
| Support and fallback | Named owner during agreed hours, reachable escalation, clinic training and a documented outage procedure | An always-on promise depends on an unavailable sole operator |
| Spending and security | Approved active profile, current provider limits, access review, secret custody and alerts with known enforcement limits | A budget email is treated as a hard spending cap or a low-cost plan as a security guarantee |

The 28 October Fly observation in [chapter 10](10-deployment-infrastructure.md#trace-the-deployment-before-choosing-a-machine) found the API and worker stopped. The worker has no HTTP wake path in its checked-in configuration. Existing `docs/operations/ENCRYPTED_DATABASE_BACKUPS.md` records production backups as disabled on 20 October; backup activation and full clinical recovery remained unverified there. Those dated records require a fresh operational check before launch. Writing this plan does not change those states.

Before promising always-on clinic operation, verify the actual process lifecycle, maintenance policy, alert coverage, operator availability, provider dependencies and recovery procedure together. Two API guests alone cannot establish that promise. Use a narrower supervised service window until the broader promise is supported.

### Provision One Clinic Across the Actual Boundaries

The onboarding code already provides meaningful mechanisms. It persists an onboarding session with a 24-hour expiry; completion validates input and payment before creating the clinic records. The following diagram shows the boundary inspected in source, rather than a proposed distributed transaction.

```text
Clinic operator
  |
  +--> persisted onboarding session, expires after 24 hours
  |      clinic + administrator + plan + payment + SLA + consent + staff
  |
  v
Validate input and payment evidence
  |
  v
Privileged bootstrap: one database transaction
  +---------------------------------------------------------------+
  | clinic, timezone/settings, medical-record-number sequence      |
  | administrator or eligible existing user linkage               |
  | subscription and applicable plan state                         |
  | SLA acceptance and consent configuration                       |
  | optional staff, default settings and weekly schedules          |
  +---------------------------------------------------------------+
  |
  +--> transaction failure: database changes roll back
  |
  v
COMMIT: clinic records now exist
  |
  +--> clear onboarding session
  +--> success audit/compliance work
  +--> optional referral event: in-process, not durable outbox
  +--> create authentication response and return success
          |
          +--> failure here does not undo the committed clinic
```

The source calls these follow-up steps after the database transaction. A timeout or error response can therefore coexist with a created clinic. Reconcile clinic identity, administrator linkage, subscription/payment state and session state before repeating completion. A duplicate-email check is useful, but does not by itself provide a complete retry-safe onboarding protocol.

The SLA acceptance method also generates and uploads a proof PDF while the database transaction is open. That object-storage operation does not join the database transaction: database rollback cannot be assumed to remove an already-uploaded object. Include proof-object reconciliation and the time spent holding the transaction in the onboarding review; the database box above is not an atomic boundary around every external effect.

The referral notification is explicitly an in-process event after commit. A crash between commit and emission can lose that follow-up. A future durable intent recorded with provisioning would close that boundary; it is not implemented by this documentation. The exact payment and entitlement mechanisms remain in [payment flows](04-payment-flows.md) and [subscriptions](09-subscription-system.md).

### Train Staff and Reconcile Imported Records

| Step | Operator action | Exit evidence |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Establish ownership | Confirm the clinic administrator, staff roles, doctor identity, timezone, weekly hours and applicable notice/processing terms | Authorized administrator approves configuration and can remove staff access |
| Preview old data | Inventory source formats and entities, map columns, inspect a small synthetic/redacted sample, define duplicate handling and exceptions | Clinic understands what will be imported, excluded or manually corrected |
| Authorize import | Use an authorized import role/tier and required patient-import attestation; retain source and access in protected storage | Audit context identifies operator and applicable notice version; no patient file enters public artifacts |
| Run a bounded import | Perform one supervised small batch during a controlled window; monitor progress and record errors | Source rows reconcile to successful, failed and skipped rows; check meaningful records and relationships |
| Resolve interruption | Inspect job status and already-created records before retrying or correcting rows | Avoid blanket reimport after a restart; explain and resolve duplicates and partial results |
| Train by role | Reception books/checks in; clinician completes a visit; administrator reviews an invoice, access and an exception | Each role completes its work and demonstrates an unavailable-service fallback |
| Close the first day | Reconcile visits, prescriptions/artifacts, invoices and relevant provider outcomes | Administrator accepts exceptions and knows how to raise a ticket |

The bulk-import registry supports patients, doctors, prescriptions, lab tests and inventory. That list does not establish complete migration of historical appointments, invoices, attachments or every legacy field.

The current import implementation persists job metadata, parses rows into memory and starts processing with `setImmediate`. Its stored `inline:<jobId>` marker is not a durable payload in object storage. Progress is written during processing, but a process restart can interrupt the accepted job; the import cooldown is also a process-local map. A database job row therefore does not prove recoverable background execution or a global import rate limit.

Until restart-safe payloads, claims/checkpoints and reconciliation are implemented and tested, the operational mitigation is supervised, bounded imports with retained source and row-level reconciliation. Avoid a deploy during the supervised import, but do not pretend that an uninterrupted process is guaranteed. Never advertise unattended restart-safe migration on the strength of a queued status label.

## Acquire Clinics Through a Measurable Learning Funnel

Start with a proposed ideal segment: a small outpatient clinic whose booking, visit, prescription and invoice work matches the verified pilot scope, with an available administrator and a clinician willing to review the workflow. This is a segment hypothesis to test in discovery. A large hospital with complex claims, inpatient or integration requirements may need a different product/readiness plan before a pilot is suitable.

A design partner is a clinic that agrees to test a bounded workflow and provide feedback. It is not automatically a customer, a paid account, a public reference or permission to use its name. Start discovery with the clinic's present process, the recurring problem, who owns a buying decision, a realistic data migration and what successful daily use would mean. Demonstrate the agreed workflow with synthetic data before accepting a qualified pilot.

```text
Permitted conversation -> discovery -> relevant synthetic demo
                                          |
                              fit + owner + agreed scope
                                          v
Qualified pilot -> readiness-approved setup -> activation
                                              |
                               complete intended clinic work
                                              v
                              agreed paid conversion
                                              |
                               successful renewal/use
                                              v
                          optional consented referral

At every step: record next action, owner, result or reason to stop.
```

Use clinics that have agreed to the conversation, or channels where the specific contact is permitted, and retain the applicable permission. Respect channel restrictions, opt-outs and suppression lists; never put patient details in prospecting material. A referral introduction needs the relevant parties' agreement, and a testimonial or case study needs separate authorization. This roadmap prepares messages and next actions for human review; it does not authorize automated contact or send any outreach.

| Proposed operating band | Acquisition and retention work | Stage owner and next action | Gate before widening the band |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| 0: discovery | Test the ideal segment with permitted discovery conversations; document pain, buyer/champion, current tools, objections and fit; recruit a willing design partner | Product/founder owns the segment hypothesis; schedule the next agreed conversation or close a poor-fit lead | A bounded problem, an accountable clinic champion and a pilot scope the product can support |
| 1: design partner/pilot | Give a relevant demo, qualify migration/support needs, agree the pilot and activation milestone, train staff and review the first clinic day | Onboarding owner and clinic champion own setup; resolve the next blocking task before requesting payment or another pilot | Readiness and reconciliation pass; the clinic reaches the agreed useful workflow and can explain its unresolved issues |
| 2–5: repeatable fit | Add qualified clinics in small supervised cohorts; compare setup, activation and objections; convert to paid only under agreed terms and review ongoing use | Product owns qualification; onboarding owns activation; billing owns the next trial/paid decision and renewal date | The checklist works repeatedly, paid/access states reconcile and support demand fits coverage |
| 6–10: retention | Review each cohort's continued use, reasons for nonactivation/cancellation, repeated tickets and first renewal; request introductions only after useful results and consent | Support/customer-success owner reviews the next at-risk clinic; product owns the recurring cause; finance owns reconciliation | Retention and service evidence support the promise, with owned recovery for churn or support bottlenecks |
| 11–25: controlled expansion | Continue cohorts sized to onboarding/support capacity; compare acquisition effort, conversion, retained use and contribution after provider costs | Growth owner proposes the next cohort using operating and cost evidence; release owner confirms readiness | No unresolved safety/recovery blocker, tested intended load, acceptable support burden and an approved forecast |
| 25+: revise segment/channel | Recheck clinic mix, channel quality, retention and economics; choose whether to deepen the segment, change the offer or expand it | Product/growth owner records one next experiment, owner, review date and stop condition | The next hypothesis and operating change are reviewable; growth remains optional if the economics or service fail |

These bands describe the proposed total participating clinic count; they are an experiment sequence, not a guaranteed calendar or forecast of customers. A measurement cohort is a fixed group entering a specified funnel step in a defined period, such as clinics starting a pilot in the same month. Record that membership once and compare its outcomes over time rather than mixing it with the changing operating band. Store identifiable prospect/customer records in an appropriately protected system. Keep public study material limited to definitions and anonymized or explicitly hypothetical examples.

### Keep Funnel and Retention Denominators Visible

For every rate, count numerator outcomes only within the stated denominator population and observation period. Keep clinics whose full measurement window has not elapsed in a separate pending group; an early success in that group must not enter a mature-cohort numerator without its denominator.

| Measure | Explicit population and interpretation | Decision it informs |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Discovery/demo/pilot progression | Count distinct clinics reaching the next step within a defined cohort; divide by clinics that reached the preceding step and have had the full agreed progression window; report still-pending clinics separately | Whether the segment, problem, demo or qualification needs correction; never divide unrelated lead and pilot totals |
| Activation | Activated clinics divided by eligible onboarded clinics whose full agreed observation window has elapsed; use one declared milestone and report newer pending clinics separately | Setup/training/product friction; registering an account is not a completed clinical workflow |
| Paid conversion | Clinics that become paid divided by the eligible pilot/trial cohort whose conversion window has elapsed | Offer/value and commercial fit; exclude unelapsed trials from a mature-cohort comparison |
| Retention and churn | Continued active or paid clinics divided by the matching starting cohort, using a declared definition; report cancellations/nonrenewals and reasons separately | Whether the product keeps delivering value; newly added clinics must not hide losses in the original cohort |
| Renewal | Successful renewed clinics divided by clinics actually due for renewal in that period | Billing failure versus value/support problems; not every active clinic has reached renewal yet |
| Support burden | Tickets, severe incidents and operator hours per active clinic, with common causes and the reporting window | Cohort size, training improvements and staffing; few cloud resources do not imply low operating effort |
| Acquisition and contribution | Attribute actual channel/onboarding effort and expenses to the acquired cohort; compare agreed revenue with payment/message/other variable costs and support allocation | Whether expansion is affordable; report the costing scope and link the [cost model](26-monthly-operating-costs.md) rather than inventing margin |
| Referral outcome | Agreed introductions, qualified pilots and activated/paid results as separate stages; retain source and permission | Channel quality; an introduction is not an acquired clinic or endorsement |

Keep the next action small and owned: demonstrate one agreed workflow, reconcile one import, resolve a recurring ticket or review one renewal. If clinics do not activate or remain, improve that boundary before buying more acquisition volume. This is a proposed operating process; no conversion, retention or customer-acquisition result is asserted here.

## Stages 2–5: Make Onboarding Repeatable

Enter this stage after the pilot completes a reconciled clinic day. Repeat the same checklist for the next clinic instead of copying arbitrary production rows or sharing administrator accounts. Record the time spent in setup, data correction, training and support; a cheap cloud bill can hide an expensive manual service.

| Responsibility | Repeatable procedure | Evidence to move forward |
| -------------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Setup | Version the supported configuration template, roles, hours, plan, provider prerequisites and feature decisions | A second operator follows the checklist without private local knowledge |
| Activation | Define the intended first value, such as a completed visit with retrievable clinical/billing artifacts | Eligible onboarding cohort, completed milestone and time window are retained; sign-up alone is not activation |
| Import quality | Reuse mapping and reconciliation rules while recording clinic-specific exceptions | Accepted/rejected/skipped counts agree with inspected records and clinic sign-off |
| Support | Classify access failures, booking issues, document delays, payment uncertainty and product requests | Tickets have impact, owner, next action, status and resolution evidence |
| Product correction | Review repeated friction and fix the highest-impact cause | Fewer repeat tickets or faster task completion is measured before claiming improvement |
| Commercial operation | Reconcile trial start/end, paid activation, renewal, failed payment, cancellation date and access policy | Subscription, payment-provider and invoice state agree or have an owned exception |

A proposed entry into the 6–10 stage requires repeatable onboarding plus retained operating measurements, not five fictional customers. Keep the existing topology if it satisfies its measured budgets. Do not add a cache, replica or separate service merely because another clinic joins.

### Keep Consent, Features and Commercial Access Separate

| Boundary | What must be checked | What it does not establish |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| Clinic agreement | Captured SLA, processing/privacy acceptance and authorized signer; compare service text with actual operating capability | A generated agreement PDF does not verify its backup or uptime promises |
| Patient communication | Current applicable consent/withdrawal state, purpose, channel and minimum necessary content | A clinic feature toggle or imported phone number does not authorize every message |
| Payment account | Correct merchant ownership, amounts/currency, verified provider events and reconciliation | Checkout/order creation does not mean collection, refund or settlement |
| Entitlement | Plan, billing/access policy, caller permission and applicable feature flag | A paid tier does not override tenant or patient authorization |
| Optional AI/integrations | Applicable processing permission, provider terms/data flow, key scope and usage budget | Disabling a UI control does not establish server enforcement or erase prior provider data |
| Data locality | Actual database/object/provider regions and contractual processing decisions | Saving `dataResidency` or operating-country settings does not relocate infrastructure |

Docita has per-clinic/global feature primitives. Use a named canary clinic and an explicit rollback/disable decision for optional changes. The global flag cache is process-local with a nominal 60-second expiry configuration and a shared expiry field; a write invalidates the writing process's cache, not every process. A guaranteed global kill-switch deadline therefore needs separate verification. Feature flags also need real server-side enforcement at the affected operation.

## Stages 6–10: Make Operations Predictable

Enter when repeatable onboarding produces enough observation to identify normal work and exceptions. Formalize the following operating cadence before widening promises; the opening checks, support and recovery responsibilities already apply to the first live clinic. The roles can belong to one person initially, but coverage and handoff must be explicit.

| Cadence or trigger | Owner and action | Retained result |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| Before clinic opening | Operations checks intended process state, API readiness, worker heartbeat, oldest pending job, provider condition, backup freshness and open incidents | Dated status; named operator and fallback for each failed check |
| During clinical hours | Support triages patient-safety impact, access/tenant failures, booking conflicts and blocked workflows before cosmetic issues | Ticket with impact, first observation, affected scope, owner and next update |
| End of clinic day | Clinic administrator reconciles completed visits, missing artifacts, invoice/payment exceptions and failed communications | Unresolved work remains visible with a responsible owner; no attempt/delivery conflation |
| Every release | Release owner follows the canonical release checklist, records compatible images/schema/config and supervises the health window | Exact checks, deployment/version IDs, business smoke result and deliberate rollback-window close |
| Weekly | Product/engineering reviews onboarding delays, repeated tickets, deployment failures, provider exceptions, access changes and capacity trends | Prioritized corrective work with owner and completion evidence |
| Monthly | Operations/finance compares resource usage with provider invoices, retention growth, support effort, plan renewals and cohort activity | Actual-versus-forecast cost, variance explanation, next-month budget and unresolved billing exceptions |
| Backup or alert test | Recovery owner verifies custody, completed backup/readback, alert delivery and the declared restore scope; follows alert containment limits | Real operating evidence kept distinct from synthetic canaries and prepared scripts |
| Dependency/security change | Engineering checks affected runtime paths, updates or contains the risk, rotates access when required and verifies compatibility | Reviewed change, appropriate checks and documented residual risk |

Use [analytics](14-analytics-and-dashboards.md) to define observation windows and denominators. Track user-visible completion, endpoint errors/tails, database waits and connection usage, worker lag, memory/restarts, provider outcomes and storage growth. Keep useful correlation IDs while excluding patient details and credentials from general telemetry. A retained SQL latency sample does not establish end-to-end availability.

### Trace One Complete Clinic Day

The following sequence is the operating journey to verify, using only the features enabled for that clinic. Each arrow is a boundary with its own success/failure evidence; it does not imply one transaction or universal durable delivery across the whole day.

```text
Before opening
  Operations -> service: readiness, worker heartbeat, pending work, backup age
  Operations -> clinic: supported hours, incidents and fallback confirmed
                    |
                    v
Booking and arrival
  Reception -> browser/API: authenticate; use authorized clinic and staff role
  API -> database: identify/register patient; validate and store booking
  Reception -> API/database: check in; allocate queue/workflow state
                    |
                    v
Consultation
  Clinician -> API/database: open correct patient; record intended visit work
  Clinician -> API/database: save prescription/complete applicable visit state
  API/background lane -> object storage: generate and store intended document
  Authorized user -> API/object storage: retrieve correct clinic/patient artifact
                    |
                    v
Billing and optional provider work
  Staff -> API/database: create/review invoice and correct financial state
  Optional payment -> provider -> verified callback/reconciliation -> local state
  Consented message -> provider -> recorded acceptance/delivery/failure evidence
  Pending/failed work -> operator: inspect, reconcile, deliberately retry if safe
                    |
                    v
Day close
  Administrator -> records: visits, documents, invoices and provider exceptions
  Support -> ticket owner: unfinished work, next action and clinic communication
  Operations -> next opening: process/recovery status and unresolved incident handoff
```

Follow the canonical [clinic workflow](05-clinic-workflows.md), [prescription](07-prescription-safety.md), [billing](08-billing-invoicing.md), [payment](04-payment-flows.md), [messaging](06-whatsapp-integration.md) and [async](03-async-processing.md) chapters for their actual transitions. A created appointment does not prove reminder enrollment; a saved prescription does not prove a generated PDF; an invoice does not prove payment. At day close, classify each unfinished item by the missing boundary and assign its recovery action rather than counting earlier acknowledgments as completion.

### Handle an Incident Without Losing the Recovery Boundary

| Step | Action | Decision or proof |
| ----------------- | ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Detect and assess | Confirm the signal; identify affected workflow, start time and tenant/provider scope | Severity reflects blocked care, wrong access or lost work as well as request errors |
| Contain | Stop the affected feature or new onboarding; preserve records and compatible rollback options | Named owner chooses the narrowest useful containment; flags alone are not a proven immediate global stop |
| Communicate | Use the agreed clinic support channel and update cadence | Authorized communication states known impact and next update without leaking patient data |
| Recover | Roll back compatible code, forward-correct schema or reconcile jobs/provider effects using the applicable runbook | A code rollback does not reverse migrations, restore secrets or cancel an external effect |
| Verify | Check representative reads/writes, pending work, provider state and tenant access | Resumed traffic is not the sole proof; inspect the affected business operation |
| Learn | Record cause, timeline, missed detection and one owned preventive change | A review distinguishes observed facts from hypotheses and verifies the corrective action |

The canonical Docita `docs/operations/RELEASE_EVIDENCE_CHECKLIST.md` requires a retained API latency baseline, migration evidence, deployment/image identifiers, a supervised health window and rollback compatibility. Use that artifact rather than inventing a second release checklist here. A failure elsewhere in the required verification pipeline remains a failure even when focused checks pass.

## Stages 11–25: Accept the Intended Operating Profile

Enter after monitoring, support and recovery procedures produce usable evidence. Apply the [chapter 23 workload](23-hypothetical-clinic-metrics.md) to the intended topology. Its example assumes 25 clinics, 26,000 completed visits and 520,000 appointment-linked requests per month. These totals are calculations from assumptions, not current adoption or proven throughput.

| Promotion gate | Required experiment or record | Insufficient substitute |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| User-visible correctness | Authenticated booking/clinical/billing writes, conflicts, pagination and tenant denials on the relevant schema | Metric aggregation fixtures or a successful public health probe |
| Busy-window behavior | Retained normal and burst arrivals, latency distributions, errors, waiting, admission/drop outcomes and representative tenant skew | Monthly averages or an invented P95/P99 sample |
| Background completion | Worker availability, realistic document/provider tasks, backlog age, retry behavior and restart/recovery evidence | Idealized poll frequency or a database claim count |
| Process failure | API replacement, worker shutdown, interrupted import, provider timeout and duplicate-event exercises | An orderly happy-path test alone |
| Database budget | Measured query/pool/transaction pressure; include every API/worker/maintenance connection and rollout overlap | Assuming horizontal API scaling creates database capacity |
| Recovery | Timed restore of relevant database rows, referenced objects and recoverable keys; reconcile erased/held records before access | Matching zero counts from copied empty clinical tables |
| Economics and staffing | Stage-specific forecast, provider limits, retained-data growth, support coverage and agreed spending policy | Treating free allowances or omitted support work as unlimited capacity |

Record a promotion decision with revision, environment, topology, dataset, traffic mix, start/end time, target, achieved result, unresolved limitation, owner and next review. Choose explicit targets from the product promise and [measurement/capacity acceptance protocol](23-hypothetical-clinic-metrics.md#run-a-capacity-experiment-with-a-declared-boundary). Current proposed latency budgets are not achieved results.

The future balanced reference in [chapter 10](10-deployment-infrastructure.md#keep-the-cheap-deployment-and-future-balanced-reference-distinct) is a test candidate. Database connections, worker completion and process-local behavior can limit a two-API deployment even when CPU looks quiet. More API guests require checking global rate limits, cache/flag propagation, socket routing and event ownership; an unused Redis configuration is not a wired shared adapter.

## Beyond 25: Change the Bottleneck That Was Measured

| Observed constraint | First investigation | Change only when its test and cost justify it |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Slow database-bound requests | Query plan, indexes, selected columns, pagination, locks and whole-request transaction time | Resize compute/storage or redesign the operation after preserving correctness |
| API memory pressure | Resident memory, heap, buffers, concurrency, object lifetimes and restart pattern | Adjust memory/concurrency or isolate heavy work; swap is not equivalent to RAM |
| Old document/provider backlog | Handler duration, polling/claim behavior, effective outbox batch, rate limits and repeat-safe effects | Tune/scale the appropriate worker lane with a bounded database connection budget |
| One noisy clinic | Per-tenant contribution, expensive reports/imports and fairness | Tenant-aware admission and job limits rather than globally worsening every clinic's experience |
| Analytics harming visits | Query cost, scan windows, aggregation and freshness requirements | A separate read model, replica or warehouse after confirming actual read-pressure and consistency needs |
| Support workload exceeds coverage | Tickets per active clinic, repetitive setup, training and escalation gaps | Better product flow/documentation or staffed support before promising a broader service window |
| Regional or recovery requirement changes | Actual users, provider locality, data-flow constraints and tested recovery | Regional architecture or provider migration with a new failure and cost model |

Database size grows with retained history and indexes, not only the current month's visits. Object revisions, audit/telemetry retention, backup copies, egress and provider messages can grow differently. Recompute [monthly costs](26-monthly-operating-costs.md) from actual measurements rather than extrapolating one provider allowance forever.

## Move From Neon to AWS With a Cutover Decision

The current provider is temporarily Neon; AWS remains a future option. Start the migration review when a measured capacity, recovery/control, locality or commercial requirement supports it. A clinic count alone does not require the move. The resource and dollar proposals stay in chapters [10](10-deployment-infrastructure.md) and [26](26-monthly-operating-costs.md).

| Cutover phase | Work and exit evidence |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Inventory | Confirm actual source compute, storage, extension/version compatibility, connection routes, encryption keys, object references, job/provider state and applicable retention scope |
| Rehearse | Use a protected isolated target, representative encrypted records and relevant tenant roles; measure copy, restore, checks and rollback decision time |
| Choose transfer method | Select an explicit maintenance/write-freeze procedure or a tested replication/catch-up method; prove what happens to writes and schema changes during transfer |
| Prepare target | Verify runtime role/policies, pool budget, TLS/network access, backups, monitoring, worker connectivity and secret custody without exposing values |
| Reconcile state | Compare authoritative records and relationships, migration state, required objects/decryption, pending jobs and captured provider outcomes; raw total row counts alone are insufficient |
| Cut over | Named operator changes the approved connection/configuration path, resumes one controlled workflow and monitors errors, tails and worker progress |
| Decide rollback | Set a deadline and compatibility condition; once the new primary accepts writes, returning to the old primary requires explicit reverse reconciliation to avoid lost/divergent records |
| Close | Retain the source for the approved recovery window, restrict access, account for temporary dual-running cost, then remove resources only after data/retention and billing sign-off |

Avoid two writable primaries without a designed conflict/reconciliation protocol. A successful DNS or connection-string change is not a complete database migration, and a database migration does not automatically move object storage or external provider state.

## Close the Customer Lifecycle Deliberately

| Event | Required handoff | Completion evidence |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Renewal fails | Billing owner reconciles provider evidence, grace/hardlock policy, administrator access and customer notice | Explicit access decision and payment/invoice exception resolution; no improvised data deletion |
| Downgrade/cancel | Confirm effective date, plan limits, refunds/credits if applicable, queued costly work and end-of-access expectations | Subscription and financial records agree with the documented terms |
| Clinic requests export | Authorize the requester, define entities/formats/object inclusion and deliver through protected access | Verified completeness and recipient acknowledgement; patient JSON portability is not automatically a full clinic export |
| Staff member leaves | Administrator removes role/membership and revokes access according to session policy | Previously issued access is tested against the intended revocation boundary |
| Patient erasure or clinic exit | Reconcile authorized anonymization/erasure with applicable record obligations, legal hold, provider copies, logs and stored objects | Per-data-class action and exceptions are recorded; cancellation alone is not evidence that all data was erased |
| Restore after an exit | Quarantine restored data until deletion/hold state and keys/object references are reconciled | Erased records are not silently reintroduced to active access |
| Resource shutdown | Confirm remaining tenants, billing/export work, retention locks and recovery custody before stopping/deleting infrastructure | Approved maintenance/retirement state and subsequent provider bill/readback |

Distinguish request handling from erasure completion. A response can explain an approved retention exception or an outstanding provider action, but cannot mark every copy erased. Record the exact completed scope, retained classes, reason, owner and next review; label physical deletion/anonymization complete only for the scope whose actions and verification actually finished.

Docita's ADR 0016 and compliance documents own data-class and recovery decisions. Existing runbooks explicitly mark the historical `export:tenant` command as nonexistent; do not treat it as a working selective-restore tool. A future operator-facing clinic export/restore procedure requires its own implementation and verification.

## Record What Is Ready Before Saying What Comes Next

Maintain one dated readiness record with three columns: required capability, inspected implementation and executed operating evidence. For example, “backup tooling exists; production schedule disabled in the dated record; activation/clinical restore unverified” is more useful than a green backup badge. Apply the same distinction to customer adoption, provider delivery, feature rollout, support coverage and measured monthly spend.

The next action should close the highest-impact incomplete boundary: establish non-owner tenant enforcement, prove complete recovery, make interrupted work recoverable, retain the required latency baseline or resolve the release gate. A new clinic can proceed only within an explicitly supported scope. A proposed architecture and a long checklist do not expand that scope on their own.

## Summary

Grow a clinic service by proving complete workflows and assigning ownership for what happens when they fail. Begin with reproducible local work, launch a supervised pilot only after its readiness gates pass, then make onboarding, support, release, recovery and cost review repeatable. Use measured constraints to select infrastructure changes; keep hypothetical demand, source mechanisms and achieved operating evidence distinct through every stage.

## See Also

- [Operating-evidence workbook](27-operating-evidence-workbook.md) — executable availability checks, a clinic-day acceptance sheet, diagnosis and promotion records.
- [Category revision](REVISION.md) — lifecycle and growth recall after the learning cases.
- [Deployment and infrastructure](10-deployment-infrastructure.md) — hardware, setup, process lifecycle, releases and recovery topology.
- [Monthly operating costs](26-monthly-operating-costs.md) — provider estimates, fixed/variable cost, usage forecasts and budget boundaries.
- [25-clinic workload](23-hypothetical-clinic-metrics.md) — demand assumptions, resource budgets and experiment acceptance.
- [Analytics and dashboards](14-analytics-and-dashboards.md) — metric scope, time windows and retained evidence.
- [Tenant isolation](02-multi-tenancy-rls.md), [async processing](03-async-processing.md) and [documents](19-documents-and-uploads.md) — correctness and recovery boundaries.
- [Subscriptions](09-subscription-system.md) and [long-tail domains](21-long-tail-domains.md) — access policy, reminders and user lifecycle.

## References

Scoped source inspection on 28 October 2026 used a Docita working tree based on canonical revision `f3fddffc0`; the following relative paths identify mechanisms, not deployment/adoption evidence. Dated operational records below retain their own verification dates and limitations.

- `apps/api/src/domains/clinics/application/services/onboarding/onboarding-data.service.ts` — persisted sessions, expiry, steps and completion cleanup.
- `apps/api/src/domains/clinics/application/services/onboarding/onboarding.service.ts` and `onboarding-workflow.service.ts` — validation, bootstrap transaction, created records and postcommit work.
- `apps/api/src/domains/clinics/application/services/onboarding/onboarding-compliance.service.ts` — SLA/processing/privacy acceptance and signature proof.
- `apps/api/src/shared/modules/imports/imports.controller.access.ts` and `bulk-import-strategy.registry.ts` — import authorization, patient attestation and supported entity types.
- `apps/api/src/shared/modules/imports/bulk-import-orchestrator.service.ts` and `bulk-import-job-processor.service.ts` — process-local cooldown, inline payload, scheduled execution and partial results.
- `apps/api/src/shared/modules/services/feature-flag.service.ts` — global/per-clinic values, local cache and invalidation boundary.
- `docs/ONBOARDING.md` and `docs/product/ONBOARDING.md` — developer environment setup, not clinic launch certification.
- `docs/operations/RELEASE_EVIDENCE_CHECKLIST.md` and `docs/operations/STABILITY_RUNBOOK.md` — release ownership, verification, health and incident/capacity procedures.
- `docs/operations/ENCRYPTED_DATABASE_BACKUPS.md`, `DR_RUNBOOK.md` and `ZERO_HOSTING_SPEND.md` in the same directory — dated preparation, recovery and maintenance/spending boundaries.
- `docs/architecture/decisions/0016-patient-data-lifecycle-and-recovery.md`, `docs/compliance/DPDP_READINESS.md` and `DPDP_SUBPROCESSORS.md` in the compliance directory — data lifecycle decisions, operational gaps and provider data flows; verify current obligations before making external commitments.
- [Case-study index](INDEX.md) — canonical learning order and source-evidence scope.
