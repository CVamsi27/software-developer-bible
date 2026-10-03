<!-- section: Cheat Sheets | category: Reference | tags: revision, practi | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Cheat%20Sheets-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
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

**A:** Persistent fetch caching defaults changed in Next.js 15. Render request memoization, route output, and Router Cache are separate mechanisms with their own invalidation scope.

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


## Summary

Check each component’s role and contract in a concrete trace. State the runtime/version, concurrent behavior, and evidence required before repeating a claimed guarantee.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
