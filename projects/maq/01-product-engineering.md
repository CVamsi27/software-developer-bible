# 01 — Reconstruct the Product Engineering Behind the MAQ Resume

[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../docs/topic-importance.md)



An interviewer asks how an API became faster. A remembered percentage cannot explain the request, query pattern or personal contribution. Begin with one actual workflow and identify which details can be supported.

## Definition

An experience reconstruction connects a recorded responsibility to a real project, personal actions, technical decisions and available outcomes. This chapter prepares the four MAQ bullets in the current resume without inventing a project, incident, measurement or client.

> **Textbook Definition:** Experience reconstruction organizes available records of past work into a specific problem, personal contribution, engineering decisions and supported outcomes, keeping later practice distinct from employer history.

The available source is the candidate's previously authored CV. No MAQ source repository, ticket history or performance report was supplied. The technical exercises below teach how to discuss the recorded work; they do not independently verify that it happened. Keep confidential employer material private and use approved sanitized examples.

## First Principles

A team outcome and an individual contribution are different. A reusable pattern may improve maintenance without a measured delivery-speed percentage. A tuned query can improve one endpoint without establishing a platform-wide latency claim. Reconstruct the actual operation and contribution before choosing the wording of an outcome.

## Bullet 1: Explain One Recruitment or Internal Workflow

**Resume scope:** TypeScript, React, Node.js, reusable services, input validation and module boundaries.

Choose an actual workflow you worked on and identify its users, initial friction, existing constraints and your responsibility. Trace UI input → runtime validation → authentication/authorization → service rule → persistence → response → UI update. State which layers you changed and who owned adjacent work.

Explain a concrete service boundary: request parsing belongs at an input boundary; business rules must remain enforceable independently of one UI; storage details should not leak into every caller. A reusable helper is valuable when it centralizes a stable rule, not merely because it decreases line count.

For the historical delivery-time percentage, first identify what was measured: time from request to delivery (lead time), time from starting work to finishing it (cycle time), or engineering effort. Changes in release frequency and ticket complexity can also affect the result. The current resume omits that unconfirmed figure. Discuss a concrete change and its observed qualitative effect when the original calculation cannot be recovered.

**Practice exercise:** build a synthetic approval workflow with a PENDING-to-approved transition, authorized roles and a conditional version check. Two competing requests must not silently overwrite each other. This demonstrates learning; do not describe it as the implementation of an unnamed MAQ system.

## Bullet 2: Show How You Diagnosed an API Bottleneck

**Resume scope:** profiling, REST APIs, PostgreSQL indexing/pagination, caching and N+1 elimination.

Select an actual endpoint from your recollection. Establish what users experienced, how you localized the bottleneck and what you changed. Distinguish application execution, database time, network delay and downstream dependencies. Name the evidence you truly had; do not supply invented profiler output.

A useful investigation starts with request traces and query counts, then a query plan on a safe representative dataset. N+1 occurs when a parent list triggers additional per-row queries; batching or an appropriate join can reduce round trips but alter payload size and query cost. An index must fit predicates and ordering and incurs write/storage cost.

### Follow the Cost of One List Request

Consider a **practice scenario**, not a recovered MAQ incident: a recruitment page displays 50 candidate rows and each row needs its latest status. The first implementation fetches the page once, then requests status separately for each candidate. That creates `1 + 50 = 51` database calls. A batch fetch can reduce this to two calls: one for the page and one for the statuses of only those 50 candidates.

The important change is the access pattern. Fifty parallel calls still create 50 queries and pressure the connection pool. Fetching every candidate's status in one huge query avoids round trips but may increase memory and unauthorized data exposure. Scope both queries to the allowed records, project only the required fields, and preserve one latest-status result per candidate.

| Observation | What it suggests | What to inspect next |
| --------------------------------------------- | --------------------------------------- | ---------------------------------------------------- |
| Query count grows with page size | Per-row lookup or lazy relation loading | The loop and ORM relation access |
| Two queries remain slow | Each query may scan/sort too much | Query plans, selectivity and index ordering |
| Database time is low but request time is high | Another stage dominates | Pool wait, external calls, serialization and network |
| Fast responses contain wrong/stale rows | Optimization changed correctness | Authorization, cardinality, ordering and cache scope |

Compare equivalent responses before quoting a speedup. Record the same fields, ordering, permissions, dataset and workload, then observe request latency and errors. Fewer queries explain a mechanism; they do not independently establish a latency percentage.

Offset pagination can degrade at deeper pages; cursor pagination needs stable ordering and a tie-breaker. Caching needs scope, expiry and invalidation. Authorization-sensitive results must not share keys across users or tenants incorrectly. State whether you implemented each technique or are explaining an alternative.

**Practice exercise:** create a synthetic list endpoint and compare N+1 against a batched implementation with identical fixtures. Record query count, request distribution, p50/p95, failures, hardware, cache state and revisions. Use the observed benchmark result, qualified as a benchmark. Do not rename it a recovered MAQ production measurement.

The historical 30% figure lacked a confirmed statistic and original records. It is absent from the current resume. A credible explanation of the investigation does not require that number.

## Bullet 3: Explain Reuse Without Hiding Product Behavior

**Resume scope:** React/TypeScript components, loading/validation/error states, responsive behavior and accessibility.

Pick one component or form you actually changed. Explain its consumers and which contract was stable: props, controlled/uncontrolled state, error presentation, keyboard behavior and semantic markup. Separate reusable behavior from business-specific rules.

### Keep Reuse at the Interaction Boundary

A reusable field can own its label, error association, disabled/pending presentation and focus behavior. A recruitment approval rule belongs in the workflow and server, not inside a generic text field. This keeps reuse understandable while preserving the product's rules.

Trace one failed submission: the user enters a value, local parsing identifies a field error, the server may reject an otherwise valid request, and the UI keeps the entered values while explaining the failure. For a slow request, expose pending state without moving focus unexpectedly. For a successful request, update the relevant server-state query; do not blindly copy an entire cached record into independent local state.

Evaluate the change by behavior: can another screen use the contract without copying validation markup, can a keyboard user reach and correct the field, and does a server error stay associated with the right action? A smaller component file alone does not answer these questions.

Discuss server state versus local form state, stale results, failed submissions and unnecessary rendering. Use an actual accessibility issue if you remember one; otherwise demonstrate the principles in an exercise. Native elements, explicit labels, focus order and useful validation feedback require verification, not just an accessibility prop or library name.

**Practice exercise:** build a reusable form field and a searchable list. Test keyboard-only use, pending/error/empty states, stale search responses and one screen-reader interaction. Measure performance before optimizing; memoization does not automatically improve every component.

The older UI-duplication and load-time percentages are historical authored claims without provided calculations. They are not present in the current application resume. Explain the concrete reuse and user-visible behavior you can substantiate.

## Bullet 4: Describe Delivery and Mentoring With One Example Each

**Resume scope:** GitHub Actions, Jest, release checks, code review, debugging and design discussions.

Draw one actual delivery path: pull request → checks → artifact → deployment → smoke check → recovery. Identify the pipeline steps you authored or maintained and the controls supplied by other teams. A successful unit check cannot prove every integration, migration or release safe.

Explain one valuable assertion, one failure it caught and why a different test layer was needed elsewhere. Coverage reports count executed lines/branches according to their configuration; they do not prove meaningful assertions or customer outcomes. The unconfirmed 85% figure has been removed from the application resume.

For mentoring, select a real review, pairing session or design discussion. Describe the other engineer's problem without personal details, the reasoning you offered, their decision and the outcome you observed. Avoid assigning a sprint-predictability percentage without a definition and records.

**Practice exercise:** review a synthetic API change for missing authorization, error mapping and a migration compatibility hazard. Write a focused review comment and a test that exposes one actual fault. This practices judgment without manufacturing an employer incident.

## Assemble Real Stories Before Memorizing Answers

Prepare four story cards corresponding to the bullets. Each card needs a real project context, approximate period, your task, implementation action, alternative considered, observed outcome and limitation. Exact client names or proprietary artifacts may be unnecessary; state when details are sanitized.

Label each detail as recalled experience, available artifact, reconstructed estimate or practice exercise. Separate “I implemented” from “the team delivered” and “I would propose.” If you cannot recall a technique attributed to you in the current resume, narrow or remove that phrase rather than learning a fictional ownership story.

### Choose Strong Wording From the Evidence You Have

For the list-request example above, the claim changes as evidence becomes available. A synthetic result never becomes an employer result by copying its number into a story.

| Available evidence | Supported statement and next check |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Recalled personal investigation, without original timing records | Describe the actual request, bottleneck investigation and change you remember. Use a qualitative outcome; do not infer a percentage or percentile. |
| An authorized source diff or review record | Identify the access pattern changed, the relevant scope and your contribution. A diff can support a mechanism or ownership statement, but cannot alone prove runtime speed. |
| Original before/after observations | State endpoint, statistic, population, periods, sample counts and exclusions. Compare equivalent permissions, fields, workload and deployment conditions before calculating a change. |
| A newly executed synthetic recreation | Name it as a current benchmark, retain its fixtures and raw output, and explain the observed result. Keep it separate from the date and outcome of the historical work. |

A useful accomplishment sentence contains the action, concrete scope and supported result. For example, if personally substantiated: “Reworked the authorized list endpoint's data access to remove per-row status lookups while preserving pagination and returned fields.” This gives a reviewer a mechanism to examine without inventing a latency improvement. The 51-to-two query calculation remains the practice example above until a real trace records those counts for a named environment.

When original timing records exist, retain the baseline and changed observations together with the calculation. Check failure rate and returned data as well as speed; excluding failed requests or changing the response can create a misleading improvement. Record other simultaneous changes that prevent attributing the entire difference to one engineer or index. Private employer evidence stays private; use approved sanitized descriptions in interviews.

Add behavioral examples only from real experience: ambiguous requirements, disagreement, a failed approach, deadline trade-offs and helping a teammate. The factual story should stay stable under follow-up questions even as your technical explanation becomes deeper.

## Prepare in an Observable Order

1. Explain one real workflow without notes and identify your contribution.
2. Implement the synthetic API performance exercise and retain reproducible results.
3. Demonstrate a React form with failure states and keyboard interaction.
4. Review a pipeline/migration and identify which checks can detect which faults.
5. Reconstruct one mentoring example and one technical disagreement.
6. Answer the [separate revision questions](REVISION.md), then repeat with a changed constraint.

Use the existing [role-focused study route](../../80-lanes-abroad-full-stack/80.29-topic-brushup-roadmap.md) for fundamentals. Do not expand into the deferred Java or Indian SDE tracks just because an older role involved Java.

## Summary

The MAQ preparation path builds technical depth around recorded work while requiring actual personal examples. Practice supplies understanding and new benchmark evidence; it does not supply missing employer history or historical measurements.

## See Also

- [Category revision](REVISION.md) — follow-ups and answer boundaries.
- [MAQ learning index](INDEX.md) — reconstruction before practice.
- [Docita claim walkthrough](../docita/24-resume-claim-walkthrough.md) — source-backed implementation study kept distinct from MAQ.

## References

- Candidate's canonical CV — authored experience, not independently verified employer evidence.
- Historical metric discussion — definitions and missing measurement records.
