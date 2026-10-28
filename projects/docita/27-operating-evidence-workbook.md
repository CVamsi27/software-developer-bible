# 27 — Prove the Operation: A Workbook for Senior Decisions

[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)

A monthly aggregate returns the expected 26,000 appointments, yet a patient cannot retrieve the prescription. Both observations can be true. The aggregate checked rows; it did not check tenant access, document generation, object retrieval or whether the worker was running. Practice becomes useful when each exercise states which boundary its evidence can establish.

## Definition

An operating-evidence workbook turns an architecture into bounded exercises. Each exercise names its prerequisite, action, expected invariant, failure case, retained result and stop condition. It lets a learner explain a real result without confusing a source reading, stub test, synthetic experiment and live customer outcome.

> **Textbook Definition:** Operational verification evaluates observable system behavior against explicit correctness, service and recovery requirements under a declared environment and workload, retaining reproducible evidence and the limitations of each inference.

This workbook continues the **28 October 2026** source review based on Docita `f3fddffc0` and the reviewed, unpublished capacity patch. Commands added by that patch are absent from the clean base revision. The workbook itself adds no application feature, seed generator, production activation, measured capacity or customer result. [Deployment](10-deployment-infrastructure.md) owns exact setup/preflight commands, [workload modeling](23-hypothetical-clinic-metrics.md) owns the load protocol and [costs](26-monthly-operating-costs.md) owns pricing arithmetic.

## First Principles

A passing check establishes only the properties it exercised. A mock cannot establish a database lock invariant; an aggregate over projected columns cannot establish full-schema behavior; a process state cannot establish job completion. Conversely, a failed prerequisite means an exercise has not yet tested its intended property.

Follow one operation through its authoritative state and external effects, then change one constraint. Keep the result, the counterexample and the limits together. That gives an interviewer or operator something inspectable beyond a memorized explanation.

```text
Question -> prerequisite -> bounded action -> observation -> assertion
               |                                |
               +-> absent: stop, record gap      +-> changed constraint
                                                        |
                                                        v
                                              repeat and explain

Evidence scope grows only when the next boundary is actually exercised:
source -> local check -> real engine -> full application -> provider -> recovery
```

## Prepare a Practice Record Before Running Anything

Use synthetic data and a disposable local environment whose database, object storage, queue, email, messaging and payment destinations you have inspected. A loopback API can still connect to a remote database or provider. Keep the original source checkout and production maintenance state outside the experiment.

| Field | What to retain privately |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Question and invariant | One operation and the property that must remain true |
| Source | Commit, clean/dirty state, required patch availability and recoverable source snapshot; a hash alone does not preserve untracked files |
| Environment | Local/staging distinction, actual process topology, CPU/RAM limits, database engine/role/pooling, storage and provider mode |
| Fixture | Synthetic entities, relationships, history, distribution, clock/timezone, starting state and cleanup ownership |
| Action | Exact command or UI/API sequence, inputs, load shape and declared maximum duration/resource use |
| Assertions | Expected records/statuses, denied operations, side-effect count and relevant artifact checks |
| Observation | Actual outcome, sample population/count, errors/drops/unfinished work and relevant resource measurements |
| Failure and recovery | Changed constraint, detection, interrupted work, reconciliation and verified cleanup |
| Conclusion | Supported claim, unsupported inference, next gap and owner |

For shared learning material, publish only permitted sanitized aggregates and synthetic aliases. Logs, tokens, provider credentials, clinical records and raw owner snapshots do not belong in the workbook or a public evidence card.

## Know Which Commands Exist and What They Can Change

Run [the read-only availability preflight](10-deployment-infrastructure.md#reproduce-the-local-checks-before-a-release) first. It checks script/file availability; it does not verify source identity, dependency installation or environment isolation.

| Path | Availability and behavior | Evidence boundary |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `pnpm --filter @workspace/db run db:generate` | Existing base script; generates the Prisma client | Generated client, not an applied schema or usable database |
| `pnpm --filter @workspace/db run db:migrate:dry-run` | Existing base script; inspect its behavior and actual database target first; it may create local logs/artifacts | Review/diff work is not migration application or a read-only inventory guarantee |
| `pnpm --filter @workspace/db run db:migrate` | Existing base script invokes `prisma migrate dev`; mutates a database and may propose a reset | Only for an explicitly owned disposable development target, with migration prompts reviewed |
| `pnpm db:seed:local` | Existing base script writes developer sample data; its environment loader matters | Not a 25-clinic full-application workload generator |
| Filtered API/app/internal/worker `dev` scripts | Existing scripts; processes can connect to their configured destinations | Inspect every destination and scheduler owner before starting; worker is a separate profile |
| `pnpm capacity:plan` | Requires unpublished capacity patch; dry-run reads no credentials and makes no HTTP requests | Workload/model and harness availability only |
| `pnpm test:capacity` | Requires that patch; starts local test stubs and exercises the harness | Harness behavior, not clinical API capacity |
| Dedicated operational-metrics Jest configuration | Requires that patch; creates/removes owned projected fixture schemas on a guarded local database | SQL aggregate selection/arithmetic at stated synthetic row counts |
| `pnpm check:api-latency-budget --require-baseline` | Existing base script; reads a baseline and fails on missing/invalid required evidence | Baseline acceptance, not a fresh live measurement or load test |
| General API E2E setup | Existing setup performs force-reset/schema push and table truncation | Destructive; do not run against an arbitrary URL or a shared development database |
| Tenant-isolation integration suite | Existing suite can skip when its explicit admin fixture URL is absent; creates a cluster-wide `docita_app` role | Requires a separately owned disposable PostgreSQL cluster and actual non-skipped results |

The umbrella `pnpm dev` currently invokes a port-killing helper before startup. Follow the corrected Docita developer guide's explicit filtered commands after inspecting occupied ports. It also omits the standalone worker. An in-process memory queue is suitable for a bounded single-process exercise; it cannot share jobs with a separately started worker. For that profile, both processes need the same PostgreSQL queue, database/key/storage decisions and explicit scheduler ownership.

For document practice, inspect storage as well as the queue. The local storage provider defaults to the process working directory plus `uploads`; the API serves its own directory. Separate API and worker working directories can therefore write and serve different locations even when both select `local`. Prove the intended shared artifact path or use an explicitly isolated supported storage profile before claiming worker-generated PDF retrieval.

Prisma and seed/preflight tooling read the root environment; API and worker have their own ordered environment-file resolution. Copying only an API example is insufficient. Higher-priority production files or exported shell variables can change the target. Local Compose `db` and `db_test` both declare host port 5434: they cannot be assumed to coexist on that port. A database name alone does not isolate cluster-wide roles.

## What the Local Continuation Actually Executed

A later **28 October 2026** run moved several prerequisites from source inspection to executed local evidence. It reused installed dependencies in the reviewed working tree, Node 24.22.1 and newly initialized PostgreSQL 16.15 clusters. It did not use a clean dependency install, hosted database, real customer records or provider credentials.

| Executed check | Observed result | Limit of the conclusion |
| ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Existing migration chain on a fresh owned database | All **175 migrations** applied; the canonical schema diff reported **no difference** | Schema installation/alignment, not application behavior on every historical upgrade |
| Metrics SQL and service | **Six PostgreSQL aggregate cases, nine target guards and four service tests** pass, including the [nonempty all-invalid timing case](14-analytics-and-dashboards.md#keep-the-error-rate-when-every-timing-is-invalid) | Projected aggregate correctness; no API performance or capture-completeness claim |
| Tenant-probe contract on its own cluster | **15 passed**, with zero failures, cancellations or skips; fixture roles/tables/schemas/connections cleaned up | Non-owner fixture/probe behavior, not full-schema production policy coverage or two-clinic HTTP enforcement |
| Four PDF-playbook SELECTs on the fully migrated schema | Synthetic state produced **5, 3, 3 and 5 grouped rows**; the recent-failure group retained two rows/one reason, and one completed invoice record lacked an object reference; fixture cleanup returned zero rows | Real enum/column/foreign-key and diagnostic-state checks, not rendering, upload or worker completion |
| API build and existing developer seed | Build/seed exit zero; the synthetic seed contains **one clinic, 25 patients, 90 appointments, 10 prescriptions and 15 invoices** | A developer fixture, not 25 clinics, actual customers, generated business activity or the modeled month |
| Bounded real HTTP checks | Liveness/readiness **200**; anonymous patient list **401**; synthetic staff login **201**; session and authenticated bounded patient list **200**, returning five rows | One local authenticated read path; no browser, clinical writes, cross-tenant API test, provider effect or load verdict |
| Process cleanup | Both API runs exit zero after SIGTERM; both owned PostgreSQL clusters and the experiment API listener are stopped afterward | Local graceful cleanup, not crash recovery, a restore result or production availability |

The API profile deliberately used development configuration, an owner database role with RLS disabled, a memory queue, schedulers off, local storage and fresh local keys. A private OS network policy constrained connections to the tested local boundary. The source API still requests a wildcard bind, so an experiment-only preload forced the listener to loopback and the actual bound address was independently checked. This was a controlled test deviation, not an application bind fix or a deployed control. The local policy's wildcard-bind limitation and untested IPv6/general sandbox behavior remain explicit; no internet-address probe was needed or performed.

At readiness, this macOS development process reported **696,352,768 bytes of resident memory, approximately 664 MiB**. Resident set size (RSS) includes memory beyond the JavaScript heap. This single startup observation does not validate the cost model's proposed 512 MiB API or 256 MiB worker envelopes, establish steady-state consumption or justify changing production resources. Keep those cost inputs provisional until the intended deployment profile has measured memory and soak evidence; no standalone worker ran here.

### Preserve the Failed Prerequisite as Well as the Passing Run

The first tenant-suite attempt shared a cluster with the migration experiment. The migrations created the cluster-wide `docita_app` role, so the suite's before-hook encountered an existing role. Its **15 cases were cancelled before their assertions ran**. That was a fixture-isolation failure, not 15 demonstrated tenant-policy failures. Cleanup could not safely drop a role with privileges in another database; those dependencies were preserved.

The corrected run used a separate new PostgreSQL cluster, not just another database name. All 15 cases then passed and its roles and scratch objects were removed. Retaining both attempts explains the failure mechanism and the correction. Erasing the failed log or forcing the migrated role to disappear would weaken the evidence and could damage unrelated work in the shared cluster.

The compiled seed also writes its sample PDFs beneath `apps/api/uploads`, while the controlled API run used a fresh working directory. Successful seeding therefore does not prove those files are served from that experiment's local-storage root. At that stage, PDF retrieval and standalone-worker completion had not been exercised. The full clinic-day worksheet and 25-tenant workload below remain separate acceptance work.

## Follow a Created Record Beyond Its HTTP Status

A further **28 October** experiment used one synthetic staff session to create a patient, appointment, prescription and pending invoice. Each POST returned **201**; all four authorized GET readbacks returned **200**, and the new invoice and prescription each downloaded as a parseable one-page PDF. The first relational check still failed: the prescription's direct `clinicId` was null, although its patient, appointment and doctor associations were correct.

```text
201 response -> read the returned ID -> inspect the authoritative row
                                           |
                      related patient/visit/doctor agree
                                           |
                         direct clinic stamp is null -> fail
```

The command service had validated its clinic context but omitted it when calling the repository. The repository also omitted the Prisma clinic connection. This is why an HTTP success counter and a plausible document are insufficient acceptance criteria. Correcting one layer alone would still lose the value at the other boundary. Historical nullable rows require a separately reviewed reconciliation/backfill; a new-create fix does not repair them automatically.

### Make Fixture Controls Explicit

This run used the earlier development owner-role/RLS-disabled profile and network boundary. The seeded doctor began unverified. The owned synthetic fixture explicitly enabled its verified status for the create exercise and disabled the fixture clinic's WhatsApp automation; original values were retained for restoration. This is test preparation, not a real clinician-verification result. Schedulers-off alone cannot suppress immediate appointment, prescription or invoice event listeners.

The patient included the date of birth and phone required by persistence, even though the request contract marks those fields optional. Its phone was a synthetic fixture input under disabled outbound delivery; a numeric pattern does not prove that a number is unassigned. No patient contact value or authentication token belongs in the public evidence card.

The initial readback confirmed one medication, one active notice consent and its successful audit, and one invoice line. The pending invoice and line each retained **50,000 paise**, with zero tax, discount and paid amounts under the declared exempt-healthcare calculation. The observer found zero related payment sessions, WhatsApp logs/messages, PDF jobs or outbox events. Invoice creation logged a failed payment-link setup attempt; that does not become successful settlement or a durable provider retry. Staff in-app notifications and usage writes are different effects.

### Test the Document Boundary You Intend to Claim

The initial seeded invoice generated and downloaded successfully, with anonymous access denied and missing-record access returning 404. The seeded prescription returned **400** because its required doctor-name snapshot was absent. A separate real-provider read found that the sample file existed and its canonical object key worked, while its persisted browser URL produced `ENOENT` even under a matching storage root.

The seed correction therefore stores canonical object keys and snapshots the actual fixture doctor's name on create and update, failing when that doctor/name is absent. It does not change provider authorization or introduce a new storage-root setting. Keep the [synchronous download, stored-object and worker boundaries](03-async-processing.md) separate when evaluating the corrected result.

The first private harness attempt had used the wrong login response field after a successful login. It stopped before PDF assertions; the corrected harness uses the documented `access_token` contract. Preserve that prerequisite failure alongside application failures and passing reruns, with credentials excluded.

### Verify the Correction Against the Engine Again

Focused prescription tests first reproduced four failing assertions at the service/repository boundaries, then passed **nine tests across two suites** after the clinic propagation correction. The existing eight seed suites passed **44 tests**; these are fixture/unit checks, separate from the HTTP and PostgreSQL observations. Focused lint, combined API typecheck, Prisma boundary and the corrected API build passed.

Re-running the full developer seed on the used database failed at a lab-test deletion because seeded lab orders still referenced those rows. A before-correction database dump and the failure were retained. That seed is therefore not established as an idempotent refresh. A separate fresh owned database accepted the **175 migrations** and corrected seed; dependency installation was still reused.

On that new fixture, a fresh four-POST sequence, four GET readbacks and both document downloads passed again. This time the authoritative row check confirmed **all direct clinic and patient/appointment/doctor associations**, alongside the same consent, medication and 50,000-paise invoice invariants. The failed first row remains historical evidence; no production or historical backfill ran.

The corrected seeded invoice and prescription also passed protected staff download checks: anonymous **401**, authorized **200** PDF and missing record **404**. For a distinct stored-object check, only the two synthetic seed files were copied into the fresh API working directory's existing upload tree. Capability-authorized requests then returned **200** with bytes exactly equal to those files, `application/pdf` and `private, no-store`. Malformed/tampered capabilities returned **400**; wrong document type and a correctly signed nonexistent document returned **404**. These application capabilities use HMAC, with no expiry field/check in the inspected source; they are not the expiring R2 presigned URLs. This test does not establish expiry behavior or a new revocation policy.

Both databases' temporary fixture settings were restored. All five API runs exited zero after SIGTERM, the restarted owned PostgreSQL cluster stopped and the declared experiment ports were closed. The second earlier tenant-test cluster remained stopped. Database dumps were retained, but no restore was tested. These results establish local linked creation, rendering and controlled stored retrieval, with owner/RLS-disabled access and explicit file placement; standalone workers, cross-clinic HTTP enforcement, a full clinic day, 25-tenant load, provider delivery, production memory/SLOs and recovery remain separate work.

## Work Through the Boundary, Then Change One Constraint

These are an exercise sequence, not another daily calendar. Use an existing project, debugging, system-design or interview block; finish one bounded case before widening it. A future implementation task stays planned until its code and result exist.

| Exercise | Prerequisite and action | Retained result and stop condition |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0: establish the checkout | Inspect revision, dirty files and command availability; identify base versus unpublished additions | Explain exactly why a fresh base clone can or cannot reproduce the selected command; stop on missing source |
| 1: make local configuration coherent | Inspect loaders, target database and ports; choose basic single-process or explicit API/worker profile; follow source setup in an owned local environment | One target/role map and process/scheduler map; stop on an unknown remote/provider destination or a destructive shared target |
| 2: enforce two identities | Prepare two synthetic clinics and ordinary staff identities; prove one allowed operation and cross-clinic denial at the API and actual database role | Expected own-clinic records and rejected foreign access; owner-role bypass or a skipped fixture test cannot pass this case |
| 3: complete a clinic day | Perform the acceptance worksheet below with the enabled feature scope | Correct records, document access, financial/provider exceptions and day-close reconciliation; stop on wrong patient/tenant association |
| 4: race one invariant | Submit a controlled overlapping booking or repeated payment callback with synthetic/sandbox effects | Reconcile final allocation/effect count and conflicts; do not accept only successful HTTP counts |
| 5: interrupt background work | Use a disposable PostgreSQL-queue profile; interrupt at a declared claim/effect/acknowledgment boundary | Oldest work, retry/claim ownership, effect identity and recovery; stop on unbounded replay or a real provider destination |
| 6: verify metric meaning | Run the dedicated SQL fixture on its positively guarded local database, if the reviewed patch is present | Exact eligible counts and percentile arithmetic; keep supplied durations separate from measured API timings |
| 7: exercise offered load | Verify real 25-tenant application fixtures/tokens first, then run one bounded protocol from chapter23 | Offered/started/completed/error/dropped work and per-route samples plus server observations; absent full fixtures means this case is not ready |
| 8: diagnose before resizing | Pick one symptom from the diagnostic matrix; collect the next discriminating observation | A hypothesis, predicted observation, actual result and rejected alternative; stop if the chosen change loses correctness |
| 9: prove an alert path | Define an eligible metric/window and use a bounded synthetic signal in an approved test channel | Detection, owner delivery, first action and resolved-state readback; a dashboard rule alone is not delivered notification proof |
| 10: restore and roll forward/back | Use protected synthetic database/object/key copies and a compatible old/new application boundary | Restored business invariants, recovered cutoff, elapsed recovery, pending-effect and erasure/hold reconciliation; process startup alone cannot pass |
| 11: fund the next promise | Reconcile actual runtime/retention/provider units with the chapter26 worksheet; change one input | Forecast, payer, variance, next bottleneck and funded recovery/support; no clinic-count-only upgrade |

The existing critical-flow E2E source covers patient, appointment, prescription and invoice creation. That is valuable partial coverage. Its existence does not establish document retrieval, standalone-worker completion, external settlement/delivery, full role denial or complete restoration. The 25-clinic application fixture and credential preparation are also specifications rather than a supplied turnkey generator. Record those prerequisites honestly and implement them separately when that is the next authorized task.

## Accept One Complete Synthetic Clinic Day

Capture aliases and outcome evidence rather than copying patient content into general logs. For every row, record actual status, exception owner and source/runtime revision.

| Action | Expected authoritative state or artifact | Changed case and verification |
| --------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| Staff signs in and selects clinic | Intended active user/membership/role; authorized clinic context | Disabled/foreign membership denied at the operation, not merely hidden in navigation |
| Identify or register patient | Correct clinic-patient relationship and duplicate-handling outcome | Similar patient names or repeated registration cannot silently select the wrong patient |
| Book and check in | Intended slot/status/timezone and applicable queue state | Two overlapping requests produce the declared conflict/serialization result |
| Record visit/prescription | Intended clinical record linked to that patient and clinic | Validation/error or retry preserves the declared invariant; unrelated records remain unchanged |
| Request/retrieve the document | Correct linked artifact is readable through authorized access | Pending worker, failed render, missing object or wrong-tenant access remains distinguishable; a URL field alone is insufficient |
| Create/review invoice | Correct amounts/currency, lines, patient/clinic link and invoice state | Repeated submission or correction follows the declared financial transition, not an extra unintended invoice |
| Optional payment | Correct merchant order, captured/failed/refunded evidence and reconciled local state | Timeout/repeated callback reconciles provider identity before another effect |
| Optional message | Applicable permission/purpose, intended recipient and provider outcome | Accepted, delivered, failed and suppressed are distinct; replay does not silently create an uncounted duplicate |
| Day close | Visits, clinical records/artifacts, invoices and provider exceptions reconcile | Source totals and exceptions agree; unresolved work has an owner/next action and is not counted as complete |
| Next opening or restore | Required state/artifacts/keys remain available under the same authority | Restored deletion/hold state and pending effects are reconciled before active access |

## Diagnose the Layer That Can Explain the Symptom

| Symptom | Next observation that separates hypotheses | Decision after that evidence |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| First request is slow; warm requests are fast | Separate API resume/startup/readiness, database wake, connection establishment and application-query timings | Change the relevant lifecycle/connection path; a warm API alone cannot eliminate database wake |
| Tail latency rises while CPU stays low | Compare pool wait, active/idle-in-transaction work, lock waits, query plans and dependency time | Shorten the identified hold/query or bound concurrency before adding API replicas and connections |
| Heap settles but resident memory grows | Compare heap, RSS, external buffers, PDF sizes/concurrency, native allocations, swap and garbage collection over a declared interval | Bound or repair the relevant allocation/lifetime; do not describe the PDFKit process as a browser renderer |
| API is healthy but PDFs are old | Check worker process/heartbeat, queue backend, eligible waiting/delayed work, failures, effective claim batch and object-storage outcome | Restore the approved worker path or repair one failure; API availability is not worker progress |
| A counter improves after an apparent slowdown | Check capture coverage, invalid samples, success-only filtering, client drops and start/end window selection | Repair denominator/measurement interpretation before claiming a speedup |
| One clinic slows everyone | Compare per-tenant share of expensive queries/imports/jobs and fairness limits | Bound the noisy work while preserving tenant authority; average traffic cannot reveal skew |
| A retry causes another external effect | Correlate logical intent, provider identity, callback and local acknowledgment | Reconcile before replay; a local transaction cannot undo a delivered message or captured payment |
| Provider invoice grows faster than visits | Reconcile delivered category/market, duplicates, account allowances, merchant value and retention/runtime | Correct the identified meter/contract allocation; intent counts alone do not explain a bill |

In the inspected onboarding path, proof-PDF upload can hold a database transaction open. In imports, work can remain process-local after job metadata is saved. These are source-backed hypotheses to investigate in the relevant exercise; they are not claimed causes of an observed production incident. [Launch](25-launch-to-growth.md) owns those exact boundaries.

### Read Queue State Without Exposing Payloads

The schema uses `QueueJob`, not `Job`; PDF handler names are `generate-invoice-pdf` and `generate-prescription-pdf`. The following aggregate is for an **authorized owned local fixture**. The timeout bounds query effort; it does not make an arbitrary production query harmless. Verify the actual schema first. The local continuation executed the four canonical playbook queries against synthetic records in the migrated schema; this shorter teaching aggregate remains a separate diagnostic example.

```sql
BEGIN READ ONLY;
SET LOCAL statement_timeout = '3s';
SELECT name, status, count(*) AS jobs,
       EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - min("createdAt")))
         AS oldest_seconds_since_enqueue
FROM "QueueJob"
WHERE name IN ('generate-invoice-pdf', 'generate-prescription-pdf')
  AND status IN ('WAITING', 'ACTIVE', 'DELAYED', 'DEAD_LETTERED')
GROUP BY name, status
ORDER BY name, status;
ROLLBACK;
```

Age since original enqueue is not a P95 queue wait or handler duration. A delayed retry may not be eligible yet; inspect `delayedUntil` under authorized access before calling it overdue. Dead-lettered work is terminal pending an explicit replay decision, not active backlog. `PdfJob` tracks document-level status separately, so reconcile the intended document and accessible object with generic queue execution. Raw `data` and `failedReason` can expose sensitive content; keep detailed investigation in approved protected tools.

## Define an Alert With a Real Error Budget

A service-level indicator (SLI) needs an eligible population and a good-event predicate. For example, define an eligible CRUD request as a particular customer route class observed within a UTC window, and a good latency event as an eligible completed successful request within its chosen threshold. Handle timeouts, invalid durations and missing capture explicitly; excluded unknown work cannot silently become good work.

An availability objective of 99.9% allows a bad-event fraction of 0.001. With exactly 1,000,000 eligible observed requests, that permits 1,000 bad requests. If a recent window contains 10,000 requests and 100 are bad, its bad fraction is 1% and its **burn rate is 10×** the allowed fraction. Those 100 events consume 10% of that declared million-request budget. Real total-period traffic and capture coverage must be known before reporting consumed budget.

A time-based 99.9% objective over exactly 30 days permits **43 minutes 12 seconds** of bad time. That does not automatically translate into the same request-based budget. A P95 threshold also does not create “100 ms of error budget”: define the permitted bad-event fraction and population instead. Percentile headroom, a fixed debit for every breach and unexplained discarded short incidents cannot replace that definition.

| Alert-card field | Example to specify before testing |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Population and good event | Customer route/class, tenant inclusion/exclusion, success/error/latency predicate and capture coverage |
| Window and minimum evidence | Short/long observation windows, minimum eligible count, and treatment of zero traffic/unknown capture |
| Trigger | Proposed bad fraction/burn or queue-age bound derived from a user promise; no alert is claimed active here |
| Severity and owner | Impact on clinic work, reachable primary/backup and approved test destination |
| First diagnostic action | One discriminating check from the matrix and its runbook |
| Recovery | Correct business probe plus sustained resolved metric; pending effects reconciled |
| Delivery proof | Bounded synthetic signal, actual received notification, recovery notification/acknowledgment and cleanup of the test rule |

Keep threshold design distinct from alert activation and delivery. The dated operational record includes disabled schedules/backup alerts; a synthetic test must preserve its containment rules. A missing baseline, insufficient samples, zero traffic or an absent provider token is an unknown/blocked condition, not evidence of healthy user work.

## Make a Promotion Decision From the Evidence Bundle

Use one record per changed promise, such as adding a clinic cohort, making reminders available outside supervised hours, adding an API replica or moving the database. Link the [growth gates](25-launch-to-growth.md) and [funded cost worksheet](26-monthly-operating-costs.md).

| Required field | Decision content |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Current and requested promise | Supported workflow/hours/tenant scope and the exact extension |
| Correctness | Role/tenant, clinical, booking, financial and provider invariants actually exercised |
| Load and operations | Actual topology, data/history/skew, resource pressure, latency/error/backlog populations and operator coverage |
| Recovery | Verified data/object/key scope, recovered cutoff, elapsed service restoration and rollout compatibility |
| Funding | Distinct fixed/usage/labor lines, payer, allowances, retention, current/forecast bill and cap owner |
| Result | Pass, fail or blocked for each required gate; actual artifacts and scope, with no invented success |
| Next action | Named owner, one correction/experiment, review date, expiry of evidence and rollback/stop condition |

The record is an output template, not a supplied production result. Existing source/tests can justify a narrow statement while a broader promotion remains blocked. Preserve that distinction when turning a completed exercise into an interview explanation or a future product commitment.

## Summary

Practice one complete operation, change a failure condition and retain the evidence at the boundary actually exercised. Verify command availability and configuration before running it, diagnose the limiting layer before resizing, define alerts over real populations, and fund recovery/support alongside compute. Promotion requires completed evidence, not a worksheet with every box prefilled.

## See Also

- [Category revision](REVISION.md) — retrieve setup, diagnosis, budget and evidence distinctions after practice.
- [Deployment](10-deployment-infrastructure.md) — canonical availability preflight and setup/release boundaries.
- [Workload protocol](23-hypothetical-clinic-metrics.md) — fixtures, offered load, tail populations and recovery experiments.
- [Launch through growth](25-launch-to-growth.md) — product, onboarding, support and customer lifecycle.
- [Monthly costs](26-monthly-operating-costs.md) — calendar/runtime sensitivity, retention funding and payer allocation.
- [Analytics](14-analytics-and-dashboards.md) and [background processing](03-async-processing.md) — canonical metric and job mechanisms.

## References

Scoped source review on 28 October used a Docita working tree based on `f3fddffc0`; capacity script/SQL additions require the reviewed unpublished patch.

- `package.json`, `packages/db/package.json` and `apps/{api,worker}/package.json` — actual script behavior and process selection.
- `packages/db/prisma.config.ts`, `apps/api/src/app.module.ts`, `apps/worker/src/main.ts`, `scripts/db/db-check.mjs` and `scripts/kill-ports.js` — environment loading, startup side effects and local target assumptions.
- `docs/ONBOARDING.md` and `docs/product/ONBOARDING.md` — source setup guides; corrections do not establish a completed clean-environment application run.
- `apps/api/test/setup.ts`, `apps/api/test/e2e/smoke/critical-user-flow.e2e-spec.ts` and `packages/db/scripts/check-tenant-isolation.integration.test.mjs` — destructive/fixture setup, partial flow assertions and conditional integration tests.
- `packages/db/prisma/schema.prisma`, `apps/api/src/shared/modules/queue/queue.interface.ts` and `postgres-queue.service.ts` — queue/document state, handler names and retry/claim evidence.
- `scripts/checks/check-api-latency-budget.mjs`, `docs/operations/STABILITY_RUNBOOK.md` and `docs/operations/playbooks/pdf-queue-backlog.md` — baseline behavior and operating diagnostics.
- `loadtest/README.md` and `apps/api/test/metrics/README.md` — unpublished harness/SQL fixture scope and target restrictions.
