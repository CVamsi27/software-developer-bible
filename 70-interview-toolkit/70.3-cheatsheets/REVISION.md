<!-- section: Cheat Sheets | category: Reference | tags: revision, practice | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Cheat%20Sheets-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../docs/topic-importance.md)

# Cheat Sheets — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## JavaScript Cheat Sheet

Source: [JavaScript Cheat Sheet](70.3.01-javascript-cheat-sheet.md)

**Q:** What should you verify before quoting a JavaScript output under pressure?

**A:** Scope, call order, queue boundaries, coercion rules, and the runtime contract. A remembered slogan cannot replace tracing the exact program.

## TypeScript Cheat Sheet

Source: [TypeScript Cheat Sheet](70.3.02-typescript-cheat-sheet.md)

**Q:** Why does TypeScript assignability not validate an incoming payload?

**A:** Type annotations do not create runtime checks. Parse external data as unknown and validate its required fields before exposing a domain type.

**Q:** Can a callback typed to return void still return a value?

**A:** Yes. A contextual callback type returning void means its caller ignores the return value. It does not force every accepted implementation to return undefined.


## React & Next.js Cheat Sheet

Source: [React & Next.js Cheat Sheet](70.3.03-react-nextjs-cheat-sheet.md)

**Q:** Which Next.js caching claim must be qualified by version?

**A:** In the previous cache model, Next.js 15+ fetch is not persistent by default; explicit fetch and route settings govern reuse. With Next.js 16 Cache Components enabled, route-segment `revalidate` and `fetchCache` exports are removed and cached scopes use `'use cache'`, `cacheLife`, and `cacheTag`. Render request memoization, route output, and browser Router Cache remain distinct mechanisms.

**Q:** Does marking a state update as a transition let React interrupt a long synchronous calculation inside the event handler?

**A:** No. React can prioritize and interrupt its render work, but the handler’s JavaScript still runs synchronously. Break up or move expensive computation using an appropriate execution mechanism.


## Backend Cheat Sheet

Source: [Backend Cheat Sheet](70.3.04-backend-cheat-sheet.md)

**Q:** Why use atomic idempotency handling on a retryable write endpoint?

**A:** Concurrent/replayed requests can perform the business effect twice if checking a key and writing are separate. Bind the decision to the mutation transaction or a recoverable operation protocol.

**Q:** Why can a read followed by a debit overdraw an account even inside a transaction?

**A:** Two default-isolation transactions can both observe the old sufficient balance before either writes. Protect the decision with locks, a conditional write, or serializable execution with bounded whole-transaction retries.


## System Design Cheat Sheet

Source: [System Design Cheat Sheet](70.3.05-system-design-cheat-sheet.md)

**Q:** What should a system-design answer state before choosing a database?

**A:** The workload, access patterns, consistency/durability needs, failure budget, data size, and growth assumptions determine the relevant trade-offs.

**Q:** Why is publishing a failed record to a dead-letter destination not enough to safely commit its Kafka offset?

**A:** Publication must be durably acknowledged before skipping the record, and the committed offset must not skip unprocessed records in that partition. A crash between publication and commit can still cause duplicates, so retain event identity and deduplicate.


## Docker, Kubernetes & CI/CD Cheat Sheet

Source: [Docker, Kubernetes & CI/CD Cheat Sheet](70.3.06-docker-kubernetes-cicd-cheat-sheet.md)

**Q:** What does a PDB protect without controlling a Deployment rollout?

**A:** It constrains disruptions requested through the Eviction API, such as eligible drain evictions. Direct pod deletion, workload-controller rollouts, and node-pressure eviction do not use that guarantee. Rollout strategy and readiness govern rollout behavior separately.

**Q:** What evidence distinguishes an OOM termination from another exit with code 137?

**A:** Inspect the runtime’s termination reason and relevant memory/node events. Code 137 reflects SIGKILL and alone does not establish that a memory limit caused it.


## SQL & Data Modeling Cheat Sheet

Source: [SQL & Data Modeling Cheat Sheet](70.3.07-sql-data-modeling-cheat-sheet.md)

**Q:** Why can an index improve reads while making writes more expensive?

**A:** Each write must also maintain index structures and their storage. Choose indexes for measured access paths and verify query plans instead of indexing every column.

**Q:** Why does an inner join not behave like a set intersection?

**A:** It emits a row for each matching pair and preserves multiplicity. A left row matching two right rows contributes two result rows; select an aggregate, distinct operation, or existence test only when that matches the intended semantics.


## Trace the Missing Boundary

### JavaScript

Source: [JavaScript](70.3.01-javascript-cheat-sheet.md)

**Q:** Does this reference emitter wait for an async listener?

**A:** No. It calls listeners synchronously, propagates a synchronous throw and ignores returned promises. A rejected async result needs a separate observed policy; this helper supplies neither durable delivery nor awaited completion.

### TypeScript

Source: [TypeScript](70.3.02-typescript-cheat-sheet.md)

**Q:** What fact does the user type predicate establish beyond an assertion?

**A:** It executes checks that id and name are strings on a non-null object. An as assertion changes only the checker view. Neither establishes authorization or every domain invariant.

### React and Next.js

Source: [React and Next.js](70.3.03-react-nextjs-cheat-sheet.md)

**Q:** Why can an optimistic todo disappear after a successful server action?

**A:** The temporary optimistic projection settles back to the authoritative props. If the parent never refreshes those props after persistence, the new item is absent there. Persist and refresh the baseline, rather than treating a temporary render as the source of truth.

### Backend

Source: [Backend](70.3.04-backend-cheat-sheet.md)

**Q:** What does locking both accounts leave outside the transfer example?

**A:** It protects the local balance operation under the stated currency and numeric rules. Caller ownership, durable request idempotency and audit records still need implementation; a local transaction cannot atomically include a remote payment provider.

### System Design

Source: [System Design](70.3.05-system-design-cheat-sheet.md)

**Q:** What is the missing guarantee when a Redis lease expires while its old owner is paused?

**A:** A token-checked release prevents deleting a newer lease but does not stop the old owner from resuming its work. A protected resource must enforce a fencing or version condition if stale work would violate the invariant.

### Platform

Source: [Platform](70.3.06-docker-kubernetes-cicd-cheat-sheet.md)

**Q:** Can the probe fragment be applied as a standalone Kubernetes resource?

**A:** No. It belongs under a container in a Pod template and lacks its own kind and metadata. The deployment strategy fragment has a different location; syntax alone does not verify the workload and metrics dependencies.

### SQL and Modeling

Source: [SQL and Modeling](70.3.07-sql-data-modeling-cheat-sheet.md)

**Q:** Does a filtered view prevent every caller from reading soft-deleted rows?

**A:** Only callers restricted to that interface receive its filtering contract. Direct base-table access can bypass it. Enforce privileges and appropriate row policies, and consider owner/bypass-role behavior and restore uniqueness conflicts.

## Summary

Check each component’s role and contract in a concrete trace. State the runtime/version, concurrent behavior, and evidence required before repeating a claimed guarantee.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
