<!-- section: Reference | category: Tooling | tags: review, coverage, verification -->

# Full-stack coverage review — 25–26 October 2026

A green documentation build can still teach a false cache guarantee or an unavailable framework option. This review keeps machine checks and a reader's technical review as separate evidence. It starts with resume-relevant full-stack mechanisms, while every current Markdown path receives a visible disposition.

## What the ledger establishes

[The current inventory](2026-10-25-fullstack-coverage.json) records each non-ignored Markdown file's path, hash, genre, and review status. [Review records](2026-10-25-fullstack-review-records.json) contain the scoped reasoning and evidence for inspected files. The inventory includes learning chapters, INDEX learning flows, revision companions, interview banks, and operational records, and a source change invalidates the matching review.

`reviewed` means the named reviewer read that version and recorded the checks described in its notes. It does not imply that every code block ran, that a deployment was validated, or that a learner independently demonstrated the skill. `pending-semantic-review` and `stale-review` remain unfinished work, and earlier dated ledgers preserve historical evidence whose old completion totals do not certify this tree.

```bash
python3 scripts/senior_coverage.py \
  --reviews=docs/2026-10-25-fullstack-review-records.json \
  --output=docs/2026-10-25-fullstack-coverage.json

# Release requires every current file to have a current review:
python3 scripts/senior_coverage.py \
  --reviews=docs/2026-10-25-fullstack-review-records.json --require-complete
```

## Corrections in this batch

| Area | Corrected boundary |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TanStack Query | Query-key identity instead of normalized entities; staleness versus refetch triggers; active and inactive invalidation; cancellation, concurrent writes, and request-scoped hydration |
| JavaScript execution and scope | Specification contexts versus physical frames; module and global lookup, retained bindings, declaration instantiation, shallow freezing, and synchronous work inside async functions |
| TypeScript inference | Explicit index signatures versus mapped `Record` keys; primitive literal inference versus nested `const`-like inference; finite event-name unions versus capitalization patterns |
| V8 | Tiering is conditional implementation behavior; object maps, specialization, and deoptimization do not promise fixed timing or universal shape thresholds |
| Tailwind | Version 4 CSS-first configuration and complete source candidates; dynamic input and the normal CSS cascade retain their own contracts |
| Next.js | Cache Components begins in 16.0; the separate Partial Prefetching flag begins in 16.3; installed minor versions matter |
| Playwright | Browser-context isolation does not isolate backend records; a mocked reload checks a client contract, while persistence needs a real backend fixture |
| Transactional messaging | Source evidence distinguishes durable intent, broker acceptance, duplicate-safe effects, and the actual manual recovery path |
| Retry identity | A lost response can follow a committed mutation; provider formats and retention remain contractual even while the Internet Engineering Task Force (IETF) proposal evolves |
| Admission control | A disconnected response does not finish database or provider work; retain the work permit until the protected operation and cleanup settle |
| Java and database tooling | Testcontainers 2 PostgreSQL class is non-generic; Java Virtual Machine (JVM) stages and PostgreSQL `EXPLAIN` option introduction versions are explicit |
| Platform | OpenTelemetry direct dependency, conditional profiling support, Nx affected defaults, and Lambda trigger and capacity timeout ceilings |
| Edge and deployment | Next.js 16.3 no longer selects the Edge runtime for routes or pages; runtime placement and actual data authority stay separate |
| Testing | k6 checks can be thresholded; a failed check alone does not set a failing exit code; Vitest runtime and restore behavior follows the installed version |
| Coding patterns | Safe-integer recursion inputs, graph direction, and canonical priority metadata agree with the algorithms' conditions |
| Project evidence | Current tenant routing uses child async scope; manual dead-letter recovery and missing-listener refusal are distinguished from older implementations |

Companion revision questions follow the corrected canonical examples. The topic-priority CSV resolves current chapter paths and metadata, and catalog generation reads those current IDs rather than a separately maintained list.

## Evidence and verification limits

Targeted behavior checks cover TanStack cache identity and deduplication, invalidation, stale expiry without polling, and hydration; Tailwind compilation checks complete candidates and an absent candidate. Review records state the library versions and test boundaries, and source inspection, static compilation, synthetic checks, and live integration remain distinct results.

Additional checks execute extracted JavaScript examples, strict TypeScript inference fixtures, JavaScript Object Notation for Linked Data (JSON-LD) script-boundary escaping, local HTTP retry and drain cases, and error-budget arithmetic. A failing admission-control reproduction demonstrates the old disconnect bug, while the corrected operation-owned permit passes normal, failure, disconnect, and cooperative-abort cases. Lesson navigation tests cover legacy and forward campaign task formats, including invalid dates and task mismatches.

The review read learning chapters alongside their INDEX, REVISION, and interview companions. It checked the concrete problem, definitions, first-principles argument, state transition, authority, failure and recovery boundaries, changed constraints, and example limitations.

Canonical mechanisms remain in one home. Changing claims were checked against primary documentation, and per-file notes distinguish executed fixtures from source inspection.

The normal repository verification suite remains mandatory for release, checking structure, links, citations, freshness, example formatting, and generated navigation. Gate 29 requires exact-hash completeness on the final tree, including metadata changes.

Gate 18 proves stale reviews fail through the harness and replays three [canonical examples](scripts-map.md#canonical-example-replay) with named mutations: nested microtask order, generic literal inference, and operation-owned bulkhead permits. Those fixtures add reproducible local evidence without rerunning every historical check; source inspection and executable behavior remain distinct, and passing the suite does not certify that every error was found.

## Summary

The review covers the current Markdown inventory with scoped, exact-byte records. The repaired mechanisms retain their conditions and failure boundaries; changed or unreviewed content fails the completeness check, and learning and independently demonstrating skills remain separate work.

## See Also

- [Scripts map](scripts-map.md) — chooses the checker or generator for a named defect
- [Contribution guide](../contributing.md) — teaching, revision, and release requirements
- [Topic importance](topic-importance.md) — reading priorities without making them mastery claims

## References & Learn More

The repaired chapters link the primary technical sources. Per-file notes and validation limits are in the linked review records.
