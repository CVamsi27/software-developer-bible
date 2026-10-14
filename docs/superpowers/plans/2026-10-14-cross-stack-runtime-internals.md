# Cross-Stack Runtime Internals — Implementation Plan

## Goal

Complete the approved internals sequence after the Node.js PM2/Watt chapters. Give senior developers an accurate, concise model of the JVM, Kubernetes control plane, TypeScript compiler, Redis server, and V8 execution pipeline. Each topic should explain one end-to-end mechanism, its observable behavior, and the boundary that changes an engineering decision.

## Repository constraints

- Preserve existing chapter IDs and keep interview banks last.
- Extend the canonical chapter when a stack is flat or the topic fits an existing learning path; add a numbered chapter only where the category has room before its separate interview category.
- Preserve practical and textbook definitions, First Principles, one Summary, See Also, and References.
- Keep implementation-specific behavior distinct from language or API guarantees.
- Add source-linked revision questions and update category learning-flow indexes.
- Never hand-edit generated counts; restamp them with `scripts/check_counts.py --write`.

## Topic decisions

1. **Java / JVM:** expand the existing Java fundamentals runtime boundary into a source-to-execution trace: class loading, linking and initialization; runtime memory areas; interpretation and tiered compilation; GC and safepoints. Mark HotSpot details as implementation behavior and keep Java language contracts separate. Add a compact revision drill and update the chapter/index description without adding a file that would follow the interview bank.
2. **Kubernetes control plane:** deepen the existing Pods & ReplicaSets reconciliation trace, the canonical place where a Pod request becomes a running process. Explain API validation/admission and persistence, controller watches and desired state, scheduling/binding, kubelet/CRI execution, and status/readiness feedback. Keep control-plane ownership and failure signals attached to each step; do not create a duplicate controller chapter.
3. **TypeScript compiler:** add one advanced learning chapter for the pipeline from source files to diagnostics and JavaScript/declarations: `Program`/`CompilerHost`, parse, bind, check, emit, module resolution, incremental state, and language-service boundary. The file belongs before the existing interview category. Add it to the advanced-patterns index and revision companion.
4. **Redis internals:** expand Redis Fundamentals with a command-to-reply trace and the distinct execution, in-memory representation, persistence, replication/failover, and cluster boundaries. Explain how slow commands and unbounded work affect tail latency. Do not reimplement the existing cache, lease, rate-limit, or Streams patterns.
5. **V8 execution:** add a chapter to JavaScript Execution & Scope after the language execution-model chapters. Trace source through parsing/bytecode and tiered execution, explain feedback/inline caches and speculative optimization/deoptimization, and connect hidden classes/object shapes to measured hot paths. Mark all engine details as V8-specific and avoid promising a stable tier sequence. Add category/global index links, revision questions, and cross-links from execution and GC chapters.

## Work sequence

1. Verify current chapter/category IDs, links, relevant companion questions, and current uncommitted work. Preserve the already completed Node.js implementation.
2. Verify time-sensitive technical claims against primary sources: official Java/JVM specifications and JEPs, Kubernetes documentation, TypeScript handbook/compiler documentation, Redis documentation/source documentation, and V8 documentation.
3. Update each canonical chapter in the approved sequence. Introduce terminology with one concrete trace before adding implementation details. Remove or merge repeated explanations rather than growing generic section lists.
4. Update category and stack INDEX files, REVISION companions, See Also links, references, and generated counts. Preserve all existing authored interview questions and chapter IDs.
5. Review the final diff for factual precision, reading flow, duplicate headings, accidental unrelated edits, and complete topic coverage.
6. Run `python3 scripts/check_counts.py --write`, `python3 scripts/check_links.py`, and `bash scripts/verify.sh`; fix every failure and report exact results. Do not commit or push without a current explicit request.

## Acceptance criteria

- Each of the five topics has a correct end-to-end mechanism trace, operational consequences, relevant failure/trade-off boundaries, and current primary references.
- New material has a practical explanation, textbook definition, First Principles derivation, one final Summary, See Also, and References.
- Existing chapter IDs and interview-bank ordering remain valid.
- Indexes and revision companions lead a reader through the material without listing content in place of teaching it.
- Count, structure, link, freshness, alignment, and verification gates pass.
