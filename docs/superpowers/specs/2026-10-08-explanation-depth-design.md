# Explanation Depth — Design and Review Plan

Status: approved by the user on 2026-10-08; implementation in progress.

## Problem and outcome

The reader should be able to explain a topic from its chapter, follow its example and predict what happens when a condition changes. A correct definition and a catalog of names do not establish that understanding. The previous pass improved definitions and shared UI, but its targeted semantic review did not establish adequate explanation throughout every chapter.

The lexical-environment chapter demonstrates the remaining defect. Its record-kind table introduces Declarative, Function, Module, Object and Global records without developing their relationships or tracing their distinct behavior. The surrounding explanation of bindings and outer links is useful and should remain. The missing detail belongs beside the table, connected to the mechanism already introduced.

Preserve concise, distraction-free reading by removing repetition and adding the reasoning needed to understand an example. There is no target word count, fixed number of examples or requirement to fill every template heading.

## Evidence gathered for this plan

The baseline inventory was generated from tracked Markdown paths before creating this proposal. It contains 1,014 documents, including teaching material, indexes, revision companions, operational documents and private career records.

A fence-aware advisory scan found 810 sections with at least four table lines and fewer than 40 reasoning-prose words, across 423 documents. The scan used the existing `md_fences.walk` and `prose_scan.prose_words` helpers. These are review candidates, not confirmed defects: an effective recap or mistakes table can legitimately contain little standalone prose. The heuristic also misses prose-heavy jargon, unexplained diagrams and examples with hidden assumptions.

The reported LE record-kind passage did not trigger that heuristic. Its surrounding prose supplies enough words to clear the threshold while leaving the reader's questions unanswered. This is direct evidence that the full review must not be limited to automatically flagged passages.

Initial inspection established these concrete review cases:

| Source | Finding | Required review |
| ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| [Lexical environment](../../../10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.05-lexical-environment.md) | Record types receive one-line descriptions; LE versus VE is absent | Develop the model, relationships and observable differences in a readable sequence |
| [Execution context](../../../10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.01-execution-context.md) | Active environments are mentioned without explaining their distinct jobs | Own execution-context state and declaration-setup details here; connect the LE chapter without repeating its lookup example |
| [MVCC](../../../20-backend/20.4-database/01-postgresql-foundations/20.4.1.03-mvcc.md) | Improved prose coexists with diagrams and a two-session example that omit critical isolation/visibility conditions | Reconcile the entire chapter, including old diagrams, code comments and outputs |
| [Web workers](../../../10-frontend/10.1-javascript/06-modern-and-interview/10.1.6.02-web-workers.md) | Worker kinds are compressed into a table before a detailed dedicated-worker example | Check whether each variant's owner, communication and lifetime are understandable without prior familiarity |
| [HPA scaling](../../../40-platform/40.2-kubernetes/03-scaling/40.2.3.01-hpa-scaling.md) | Formula, architecture diagram and configuration introduce several interacting components | Trace metrics, resource requests, desired replicas, scheduling and readiness before comparing scaling mechanisms |

The MVCC issue is substantive: its SQL starts Session 2 with plain `BEGIN`, then expects an unchanged value after another transaction commits. PostgreSQL's default Read Committed isolation takes a new snapshot for each statement. The chapter must explicitly choose the intended isolation and explain its consequences. [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html).

The pasted elaboration is evidence of unanswered learner questions, not a verified replacement. Environment Records describe language behavior rather than a required engine memory layout. [ECMAScript Environment Records](https://tc39.es/ecma262/multipage/executable-code-and-execution-contexts.html#sec-environment-records).

## Approach

Use a complete per-document review, delivered in dependency-ordered batches. Start with the lexical-environment family as the reference treatment, then apply the same comprehension criteria across the corpus. Existing scanners prioritize investigation and protect structure; editorial reasoning decides whether an explanation is sufficient.

Two alternatives were considered. Expanding only flagged tables would be faster but miss incomplete prose, diagrams and code. Rewriting every page into an identical long template would create repetition and obscure differences between learning chapters, revision, interview drills and operational records. The selected approach reviews every authored Markdown file in its own genre and changes passages with a specific explanatory need.

## Review contract for a teaching chapter

For each introduced concept, mechanism or consequential variant, check:

1. **Meaning:** Can the reader say what it is in ordinary language? Define terms and acronyms before relying on them.
2. **Place in the system:** What contains it, creates it, uses it or communicates with it? Explain that relationship before cataloging variants.
3. **Necessity:** Which concrete problem or constraint requires it? Derive the mechanism instead of repeating its benefits.
4. **Operation:** What changes, in what order, and who owns the relevant state? Trace the operation through one focused example.
5. **Observable result:** Explain the expected output, state transition or failure. State the runtime, setup and assumptions that make the result valid.
6. **Distinction:** Explain how a consequential variant changes the trace, rather than supplying only a name and a benefit.
7. **Boundary:** Where does the explanation stop being valid? Include relevant failure, concurrency, security, lifecycle and recovery conditions.
8. **Judgment:** Give the reader a real decision and its trade-off, including when to avoid the mechanism.

A table compares concepts the chapter has already made understandable. A diagram has surrounding prose that explains its arrows and state. A code block has its setup, essential execution steps, result and limitation. Small annotations can supply that reasoning where they are clearer than a separate paragraph.

Keep an advanced distinction when it changes correctness or an interview answer. Put specification notation and engine details after the basic mechanism. Do not replace missing explanation with a link; use links to deepen a concept whose immediate role is already clear.

## Lexical-environment reference treatment

Rewrite this family first, preserving correct existing definitions and examples:

- Begin with the practical question: two scopes can use the same name, so how does a read find the intended variable?
- Explain identifier, binding, initialization, record and outer link through the existing nested-function trace.
- Introduce record kinds as adaptations of this one lookup model. Show their relationship, including the specialization of Function and Module records and the Global record's combined responsibilities.
- For Declarative records, trace a block binding, shadowing and initialization. Explain the visible consequence before adding internal terminology.
- For Function records, separate a fresh call's local bindings from the function's captured enclosing environment. Explain ordinary/arrow `this` and `arguments` ownership; link the existing `this` chapter for its complete call rules.
- For Module records, use a small two-file example to explain a live imported binding, importing-side assignment restrictions and module-local declarations.
- For Object records, explain resolving a name through object properties and where this participates in global lookup. Describe legacy `with` only to explain the model and its restrictions, not as recommended application code.
- For Global records, trace browser classic-script `var` versus `let`/`const`, then contrast module declarations. Explain `globalThis` before asking the reader to interpret its properties. Do not imply browser results apply unchanged to Node CommonJS.
- Explain LE and VE as execution-context references with different jobs: current identifier lookup versus the environment used for `var` declarations. They are not separate memory buckets for two declaration lists. The execution-context chapter owns the complete setup/block-entry/block-exit trace and its strictness/default-parameter qualifications; the LE chapter includes the distinction needed for its own examples.
- Review the pasted claims before reuse: no unsupported ES6 origin story, universal fixed-root assertion, memory-offset guarantee or claim that block exit alone establishes garbage collection. Explain retained access through a closure where it affects the trace.

Learning examples remain in their canonical chapter. Add changed-condition questions to category `REVISION.md`, preserve existing authored questions, and update the interview bank's answers only where they teach a contradictory or incomplete model.

## Delivery sequence

Each batch has its own review notes and verification. Finish the whole chapter and affected companions before moving on; a revised introduction must not leave an old diagram or example contradicting it.

- [ ] **1. Inventory and review ledger.** Enumerate tracked and newly authored Markdown outside dependencies/build output. Record file path, genre, content hash, review state, section findings, disposition and validation evidence. Account for every path; a scanner pass does not set a file to reviewed. Produce `docs/2026-10-08-explanation-depth-review.json` and a short progress report.
- [ ] **2. JavaScript scope pilot.** Review lexical environment, execution context, scope, hoisting, closures and their revision/interview companions together. Verify explanations against primary language sources and execute the observable cases below. Publish the reference treatment and record the criteria used to assess it.
- [ ] **3. Core frontend foundations.** Review the rest of JavaScript, TypeScript, HTML/CSS/browser behavior, React and forms in prerequisite order. Follow with Next.js, animation and mobile. Resolve glossary-only descriptions, lifecycle diagrams, unexplained code and ownership gaps.
- [ ] **4. Backend foundations and application boundaries.** Review Node.js, database, HTTP/API, authentication/authorization and NestJS. Prioritize complete transaction/MVCC traces. Continue through caching, brokers, microservices, GraphQL, AI and Java; optional/deferred role priority affects sequence, not review coverage.
- [ ] **5. Architecture and platform.** Review design-pattern responsibilities and collaboration before variants; derive system-design decisions from requirements and failure cases. Review platform tooling from input through controller/runtime behavior to observable deployment/operations results.
- [ ] **6. Quality, real-time and interview toolkit.** Review what each measurement or guarantee actually observes; explain race, retry and recovery conditions. Ensure interview answers contain reasoning for follow-up questions and revision companions refer to the actual source mechanisms.
- [ ] **7. Strategy, lanes, navigation and project material.** Review learner prerequisites, study order and project traces. Keep factual experience and hypothetical designs distinct. Fix missing explanations in operational documents according to their genre. Review personal and historical records for clarity/cross-references while preserving their facts, dates, decisions and canonical location.
- [ ] **8. Whole-corpus reconciliation and release evidence.** Check the ledger for unreviewed or unresolved files, reconcile changed terminology and example contracts across companions, regenerate owned metadata, and run the repository/build/browser checks below. Report semantic coverage separately from automated coverage.

Do not stop after role-essential pages or the 423 candidate documents. Every authored Markdown path receives a recorded review disposition. A correct passage can remain unchanged, with a reason; a historical record can retain its original context, with that genre decision recorded.

## Evidence and acceptance

For the scope pilot, execute and explain these observable cases:

- A nested function resolves its defining scope even when called from a differently named caller scope.
- Separate factory calls retain independent state; later calls read the retained binding rather than a copied initial value.
- A shadowing uninitialized binding throws instead of falling through to an outer value.
- A `var` declared inside a block remains available at its containing function level, while its block's `let` does not.
- An ordinary method's receiver differs from an arrow's captured `this`; an arrow does not create its own `arguments` binding.
- In an isolated classic browser script, a fresh top-level `var` is a global-object property while a fresh top-level `let` is not. Run a separate module to establish its different declaration boundary.
- A two-file module example observes an exported binding's later change and rejects direct reassignment of its import.
- A strict-function trace and a default-parameter closure case prevent the simplified LE/VE picture from becoming a universal allocation claim.

These examples test externally observable language behavior, not invisible specification objects. Check the written trace against the specification separately. For database concurrency, use actual PostgreSQL sessions with explicit isolation; SQLite is not evidence for PostgreSQL MVCC visibility. For a platform controller, distinguish a documented algorithm calculation from an executed cluster integration.

For each reviewed chapter, write two short questions in the ledger: one asks the reader to trace the main mechanism, and one changes a consequential condition. The chapter or an explicitly introduced prerequisite must support both answers. Put learner-facing retrieval questions in revision/interview companions, not a new drill inside every learning chapter.

Automation protects objective properties and generates investigation leads. It cannot certify that a beginner understands a term or that a senior answer shows judgment. Do not use prose length as a new universal release gate. If a deterministic regression rule is added, pin a real failing case, a valid compact explanation and nested-fence behavior before enabling it.

After each substantive batch, run affected structure/template, alignment, freshness, link and duplication checks. Before a requested commit or push, run `bash scripts/verify.sh`. Regenerate read-time/count/search/API output with the existing writers rather than editing badges. Probe new primary-source citations and update the external-link baseline through its established workflow.

Build the site after the complete pass and inspect newly expanded chapters on narrow and wide screens, in both themes. Rerun reader, navigation and read-aloud browser suites. Inspect new diagrams/tables for overflow, code outputs for clarity and the heading outline for a usable reading sequence.

Acceptance requires every inventory entry to have a completed review disposition, every confirmed issue to be resolved or explicitly blocked with its reason, the LE reference cases to pass, and required verification to pass. The final report must name any outstanding source/runtime limitation; a green structural check must not be described as complete semantic proof.

## Boundaries

Keep chapter IDs and canonical topic homes stable. Preserve the practical/formal definition pair where correct, one final Summary, separate revision, source-linked authored questions, existing role-priority semantics and private-data boundaries. Do not duplicate personal data, alter job-history claims, or commit/push in `career-ops`.

The current request calls for a plan before the rewrite. This proposal defines the review and acceptance criteria; chapter edits and implementation tooling begin after design review. Commit/push and deployment are separate actions from drafting this plan.
