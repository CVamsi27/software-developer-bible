# Frontend review ledger (10-frontend)

This file records what has actually been read in the `10-frontend` section pass,
against the [quality rubric](2026-11-quality-rubric.md). It is deliberately
separate from [the corpus coverage ledger](2026-10-25-fullstack-coverage.json):
that JSON is an exact-byte record that a file was reviewed at a point in time,
and it is not being restamped here for files this pass has not opened.

A row exists for every file in the section. `unread` means exactly that: the
file has not been read end to end in this campaign, and no verdict is claimed
for it. `read` rows carry what the read found, with the evidence:

- **R1 accuracy** — the specific version or API claim checked, and how it was
  checked (installed package, vendor page, or execution).
- **R2 depth** — whether the chapter opens on a problem or result, explains the
  mechanism, states a failure boundary and carries a worked example, or what
  was added to reach that bar.
- **R3 execution** — whether its complete examples were run, and the outcome.
  Fragments are named as fragments.
- **R4 prose** — what reading found beyond `check_prose` (gate 30).
- **R5/R6** — structure, and revision-companion consistency where one exists.
- **Notes** — anything unverifiable, plus the repair made.

Reading order is study order, so the ledger fills from the top of
`10.1-javascript` downward. A section-level roll-up appears at the end.

| File | Status | R1 accuracy | R2 depth | R3 execution | R4 prose | R5/R6 |
| -------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| [10.1.1.01-execution-context.md](../10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.01-execution-context.md) | read | Spec components (code evaluation state, Realm, LE/VE, PrivateEnvironment) checked against ECMA-262's execution-context record; parameter-vs-body example executed. | Problem-first opening, mechanism (declaration setup, LE/VE), failure boundary (blocks do not push contexts), worked example. | chooseReader() executed: ['parameter','body'] as documented. | No issues beyond gate 30. | Summary single; nav/labels correct; revision group matches chapter facts. |
| [10.1.1.02-scope.md](../10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.02-scope.md) | read | var/let boundary rule, per-iteration let bindings and `using` immutability checked; loop example executed. | Keyword-to-boundary table, lookup trace, loop mechanism, switch/catch boundaries all present. | Loop example executed: var [3,3,3], let [0,1,2] as documented. | No issues. | Read-order and revision group consistent. |
| [10.1.1.03-call-stack.md](../10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.03-call-stack.md) | read | LIFO model, no portable depth limit, frame layout hedged as implementation detail. | Opens on RangeError, traces push/pop, explains logical vs physical frames. | Console trace example is a diagnostic fragment, correctly framed; not executed as a unit. | No issues. | Nav correct. |
| [10.1.1.04-hoisting.md](../10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.04-hoisting.md) | read | Declaration-kind matrix (function/var/let/const/class/import) matches ECMA-262 instantiation rules; TDZ and typeof behaviour executed. | Three end states stated up front, instantiation vs evaluation, TDZ, V8 hole hedge. | typeof example executed as part of the scope harness; undefined vs ReferenceError reproduced. | No issues. | Revision pair on Annex B matches the chapter's hedge. |
| [10.1.1.05-lexical-environment.md](../10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.05-lexical-environment.md) | read | Environment Record family, Global composite record, module-vs-script boundary checked against spec structure. | Lookup trace first, record specialisation table, module boundary, property-access misconception. | Example read as a trace; runnable form is the closure example executed elsewhere. | No issues. | Revision group consistent. |
| [10.1.1.06-closures.md](../10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.06-closures.md) | read | [[Environment]] retention and live-binding semantics confirmed by execution. | Opening question, retention diagram, live-binding example, shared vs per-call records. | counter and live-binding examples executed: 11/11 and pending->completed as documented. | No issues. | Nav correct. |
| [10.1.1.07-v8-execution-and-optimization.md](../10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.07-v8-execution-and-optimization.md) | read | Tier names (Ignition/Sparkplug/Maglev/TurboFan-Turboshaft) and Maps/inline caches are hedged as implementation detail, correctly not spec claims. | Opens on a slow-then-fast-then-slow function; pipeline diagram; Maps and deopt explained. | No complete runnable example; diagrams only, as framed. | No issues. | Revision group consistent. |
| [INDEX.md](../10-frontend/10.1-javascript/01-execution-and-scope/INDEX.md) | read | Badge files-8 = 7 chapters + companion; chapter table lists 7. Read-order rationale matches chapter content. | — | — | Heading '## Files' lists chapters only while badge counts the companion; left as-is, noted. | Docita anchors name specific files; unverified against the checked-out revision. |
| [REVISION.md](../10-frontend/10.1-javascript/01-execution-and-scope/REVISION.md) | read | — | — | — | — | Six source-linked groups, 30 Q/A pairs, answers match the chapters including the Annex B and `using` hesitations. |
| [10.1.2.01-this.md](../10-frontend/10.1-javascript/02-objects-prototypes-this/10.1.2.01-this.md) | unread | — | — | — | — | — |
| [10.1.2.02-prototypes.md](../10-frontend/10.1-javascript/02-objects-prototypes-this/10.1.2.02-prototypes.md) | unread | — | — | — | — | — |
| [10.1.2.03-proxy-reflect.md](../10-frontend/10.1-javascript/02-objects-prototypes-this/10.1.2.03-proxy-reflect.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.1-javascript/02-objects-prototypes-this/INDEX.md) | unread | — | — | — | — | — |
| [REVISION.md](../10-frontend/10.1-javascript/02-objects-prototypes-this/REVISION.md) | unread | — | — | — | — | — |
| [10.1.3.01-event-loop.md](../10-frontend/10.1-javascript/03-async-concurrency/10.1.3.01-event-loop.md) | unread | — | — | — | — | — |
| [10.1.3.02-promises.md](../10-frontend/10.1-javascript/03-async-concurrency/10.1.3.02-promises.md) | unread | — | — | — | — | — |
| [10.1.3.03-async-await.md](../10-frontend/10.1-javascript/03-async-concurrency/10.1.3.03-async-await.md) | unread | — | — | — | — | — |
| [10.1.3.04-error-handling.md](../10-frontend/10.1-javascript/03-async-concurrency/10.1.3.04-error-handling.md) | unread | — | — | — | — | — |
| [10.1.3.05-abort-and-cancellation.md](../10-frontend/10.1-javascript/03-async-concurrency/10.1.3.05-abort-and-cancellation.md) | unread | — | — | — | — | — |
| [10.1.3.06-bounded-concurrency.md](../10-frontend/10.1-javascript/03-async-concurrency/10.1.3.06-bounded-concurrency.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.1-javascript/03-async-concurrency/INDEX.md) | unread | — | — | — | — | — |
| [REVISION.md](../10-frontend/10.1-javascript/03-async-concurrency/REVISION.md) | unread | — | — | — | — | — |
| [10.1.4.01-pass-by-value.md](../10-frontend/10.1-javascript/04-memory-and-data/10.1.4.01-pass-by-value.md) | unread | — | — | — | — | — |
| [10.1.4.02-map-set-weakmap-weakset.md](../10-frontend/10.1-javascript/04-memory-and-data/10.1.4.02-map-set-weakmap-weakset.md) | unread | — | — | — | — | — |
| [10.1.4.03-shallow-vs-deep-copy.md](../10-frontend/10.1-javascript/04-memory-and-data/10.1.4.03-shallow-vs-deep-copy.md) | unread | — | — | — | — | — |
| [10.1.4.04-debounce.md](../10-frontend/10.1-javascript/04-memory-and-data/10.1.4.04-debounce.md) | unread | — | — | — | — | — |
| [10.1.4.05-throttle.md](../10-frontend/10.1-javascript/04-memory-and-data/10.1.4.05-throttle.md) | unread | — | — | — | — | — |
| [10.1.4.06-memory-leaks.md](../10-frontend/10.1-javascript/04-memory-and-data/10.1.4.06-memory-leaks.md) | unread | — | — | — | — | — |
| [10.1.4.07-garbage-collection.md](../10-frontend/10.1-javascript/04-memory-and-data/10.1.4.07-garbage-collection.md) | unread | — | — | — | — | — |
| [10.1.4.08-hash-tables-internals.md](../10-frontend/10.1-javascript/04-memory-and-data/10.1.4.08-hash-tables-internals.md) | unread | — | — | — | — | — |
| [10.1.4.09-equality-and-coercion.md](../10-frontend/10.1-javascript/04-memory-and-data/10.1.4.09-equality-and-coercion.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.1-javascript/04-memory-and-data/INDEX.md) | unread | — | — | — | — | — |
| [REVISION.md](../10-frontend/10.1-javascript/04-memory-and-data/REVISION.md) | unread | — | — | — | — | — |
| [10.1.5.01-modules.md](../10-frontend/10.1-javascript/05-functional-patterns/10.1.5.01-modules.md) | unread | — | — | — | — | — |
| [10.1.5.02-memoization.md](../10-frontend/10.1-javascript/05-functional-patterns/10.1.5.02-memoization.md) | unread | — | — | — | — | — |
| [10.1.5.03-generators.md](../10-frontend/10.1-javascript/05-functional-patterns/10.1.5.03-generators.md) | read | Iterator protocols checked against MDN/ECMA-262 and executed on Node 24.22.1: Symbol.iterator identity, re-iterability, Iterator.from/map/take/toArray, absence of Iterator.concat and AsyncIterator. | Had no entry for the protocol key that makes an object consumable, while the interview bank assumed iterator helpers: added a worked section with runnable example and failure boundary. | New example executed: spread [1,2,3], destructuring 1/[2,3], helpers [2,4]; Iterator.concat and AsyncIterator confirmed absent on Node 24.22.1. | Removed a dangling '(as the hook example shows)' reference to an example the chapter does not contain. | Section renumbered to 1-5, definition and summary updated, three revision pairs added. |
| [10.1.5.04-currying-composition.md](../10-frontend/10.1-javascript/05-functional-patterns/10.1.5.04-currying-composition.md) | unread | — | — | — | — | — |
| [10.1.5.05-recursion-tail-call.md](../10-frontend/10.1-javascript/05-functional-patterns/10.1.5.05-recursion-tail-call.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.1-javascript/05-functional-patterns/INDEX.md) | read | Chapter table, read order and Docita anchors all consistent; generator row now also names the protocol and helper topics. | — | — | — | Badge counts chapters plus companion; heading lists chapters — same convention as the rest of the section. |
| [REVISION.md](../10-frontend/10.1-javascript/05-functional-patterns/REVISION.md) | read | New pairs cite the executed Node 24.22.1 results rather than prose claims. | — | — | — | Ten source-linked pairs for generators, including the iterable-vs-iterator and helper-availability questions the bank now asks. |
| [10.1.6.01-es2024-features.md](../10-frontend/10.1-javascript/06-modern-and-interview/10.1.6.01-es2024-features.md) | unread | — | — | — | — | — |
| [10.1.6.02-web-workers.md](../10-frontend/10.1-javascript/06-modern-and-interview/10.1.6.02-web-workers.md) | unread | — | — | — | — | — |
| [10.1.6.03-dom-events-delegation.md](../10-frontend/10.1-javascript/06-modern-and-interview/10.1.6.03-dom-events-delegation.md) | unread | — | — | — | — | — |
| [10.1.6.04-cross-tab-communication.md](../10-frontend/10.1-javascript/06-modern-and-interview/10.1.6.04-cross-tab-communication.md) | unread | — | — | — | — | — |
| [10.1.6.06-regexp-and-text.md](../10-frontend/10.1-javascript/06-modern-and-interview/10.1.6.06-regexp-and-text.md) | unread | — | — | — | — | — |
| [10.1.6.05-interview-questions.md](../10-frontend/10.1-javascript/06-modern-and-interview/10.1.6.05-interview-questions.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.1-javascript/06-modern-and-interview/INDEX.md) | unread | — | — | — | — | — |
| [REVISION.md](../10-frontend/10.1-javascript/06-modern-and-interview/REVISION.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.1-javascript/INDEX.md) | read | Counts: 41 badge = 35 chapters + 6 revision companions; category table sums 35 and now says Chapters, not Files. | Six-category flow read; sequence matches folder order and each category names a concrete trace. | — | — | Nav + cross-refs correct. |
| [10.2.1.01-types-vs-interfaces.md](../10-frontend/10.2-typescript/01-foundations/10.2.1.01-types-vs-interfaces.md) | read | `type` vs `interface`, declaration merging and excess-property checks matched to the TypeScript handbook and the Object Types chapter; no version-specific claim. | Opens on choosing a named shape, then covers unions/intersections, merging, excess-property checking and the runtime boundary. | Illustrative fragments; no standalone program. | No issues beyond gate 30. | One Summary; revision has seven source-linked pairs. |
| [10.2.1.02-keyof-typeof.md](../10-frontend/10.2-typescript/01-foundations/10.2.1.02-keyof-typeof.md) | read | `keyof`, `typeof`, indexed access and `as const` widening checked against the TypeScript handbook. | Opens on deriving keys from a runtime map; covers key unions, value-derived types, dictionary overstatement and key remapping. | Illustrative fragments; no standalone program. | No issues. | Revision pairs match the chapter's dictionary and `as const` boundaries. |
| [10.2.1.03-type-narrowing.md](../10-frontend/10.2-typescript/01-foundations/10.2.1.03-type-narrowing.md) | read | `typeof null`, discriminated-union narrowing, `assertNever` and the TypeScript 5.5 inferred-predicate conditions checked against the 5.5 release notes. | Opens on unknown input; covers `typeof`/`instanceof`/`in`/equality guards, predicates, exhaustiveness and the `void`-handler failure case. | Illustrative fragments; no standalone program. | No issues. | Seven source-linked pairs; changed-condition checks match the chapter. |
| [10.2.1.04-tsconfig-compiler-options.md](../10-frontend/10.2-typescript/01-foundations/10.2.1.04-tsconfig-compiler-options.md) | read | `node18`/`node20` module modes confirmed with local TypeScript 5.9.3 `--help --all`; `module: node20` with `moduleResolution: node16` accepted; TypeScript 6 defaults and 7 removals checked against the official release notes and 7.0 announcement. | Follows one file through roots, resolution, checking and emit, then covers loader-matched modules, `isolatedModules`, project references and the 6/7 migration boundary. | Config examples are fragments; the node20/node16 pairing was accepted by `tsc` 5.9.3. | No issues; date boundary updated to November 2026. | Revision has eight source-linked groups plus five changed-condition checks; facts match the chapter. |
| [INDEX.md](../10-frontend/10.2-typescript/01-foundations/INDEX.md) | read | Badge 5 = four chapters plus companion; table lists four; status changed to complete after this pass. | — | — | Read-order paragraph matches chapter order. | Docita anchors name specific files; unverified against the checked-out revision. |
| [REVISION.md](../10-frontend/10.2-typescript/01-foundations/REVISION.md) | read | Version claims (TypeScript 5.5 predicates, 6 defaults, 7 removals) match the chapters and cited release notes. | — | — | — | Four source-linked groups plus changed-condition checks; answers agree with the chapters. |
| [10.2.2.01-generics.md](../10-frontend/10.2-typescript/02-generics-and-inference/10.2.2.01-generics.md) | read | `const` type parameters (TypeScript 5.0) checked against the 5.0 release notes; the curriculum fixture `primitive-versus-nested-inference` compiles `identity`/`exactIdentity` with TypeScript 5.9.3 and rejects the widened case with TS2322. | Opens on a decoder result; covers input/output binding, constraints, defaults, interface/class reuse and runtime validation. | `python3 scripts/test_curriculum_examples.py` ran all three fixtures successfully, including this TypeScript case. | Added the missing module-context note for top-level `await`; no other issues. | Revision pairs cover const inference, merge semantics and the runtime boundary. |
| [10.2.2.02-infer.md](../10-frontend/10.2-typescript/02-generics-and-inference/10.2.2.02-infer.md) | read | `infer` placement, `Awaited`, `ReturnType`, `Parameters` and recursive unwrapping checked against the TypeScript handbook. | Opens on extracting a nested type; covers capture positions, tuple/constructor patterns, recursion and the terminal case. | Illustrative fragments; no standalone program. | No issues. | Seven source-linked pairs; answers match the extraction limits. |
| [10.2.2.03-advanced-generics.md](../10-frontend/10.2-typescript/02-generics-and-inference/10.2.2.03-advanced-generics.md) | read | Keyed-container encoding, recursive alias legality and variadic tuples checked against the handbook and TypeScript 4.0 release notes. | Covers keyed container encodings, nested path reads/writes, variadic pipelines, recursive transforms and runtime boundaries. | Illustrative fragments; no standalone program. | No issues. | Seven source-linked pairs, including the pipeline-compatibility failure case. |
| [10.2.2.04-type-variance.md](../10-frontend/10.2-typescript/02-generics-and-inference/10.2.2.04-type-variance.md) | read | `strictFunctionTypes` method bivariance and variance annotations checked against the TypeScript 2.6 and 4.7 release notes. | Explains producer/consumer direction, callback parameters, mutable-array holes, readonly views and explicit variance annotations. | Illustrative fragments; no standalone program. | No issues. | Seven source-linked pairs; answers agree with the array and callback examples. |
| [INDEX.md](../10-frontend/10.2-typescript/02-generics-and-inference/INDEX.md) | read | Badge 5 = four chapters plus companion; table lists four; status changed to complete after this pass. | — | — | Read-order paragraph matches chapter order. | Docita anchors unverified against the checked-out revision. |
| [REVISION.md](../10-frontend/10.2-typescript/02-generics-and-inference/REVISION.md) | read | Inference and variance answers match the chapters and the executed curriculum case. | — | — | — | Four source-linked groups plus five changed-condition checks. |
| [10.2.3.01-utility-types.md](../10-frontend/10.2-typescript/03-type-transformations/10.2.3.01-utility-types.md) | read | Utility-type definitions checked against `lib.es5.d.ts`; corrected wrong `LoadedUserRecord` comments so the `Partial`/`Required` composition matches the declared result. | Opens on public/editable/resolved views; covers `Partial`, `Required`, `Pick`, `Omit`, `Readonly` limits, function utilities and runtime projection. | Illustrative fragments; no standalone program. | Fixed the misleading comments; no other prose defects. | Eight source-linked pairs; answers match the corrected view. |
| [10.2.3.02-conditional-types.md](../10-frontend/10.2-typescript/03-type-transformations/10.2.3.02-conditional-types.md) | read | Distribution, `never`, tuple wrapping and `infer` behavior checked against the TypeScript handbook. | Opens on branch computation; covers naked-parameter distribution, tuple opt-out, inference, recursion and the runtime boundary. | Illustrative fragments; no standalone program. | Removed a dangling “(as the hook example shows)” reference. | Eight source-linked pairs; changed-condition checks match the chapter. |
| [10.2.3.03-mapped-types.md](../10-frontend/10.2-typescript/03-type-transformations/10.2.3.03-mapped-types.md) | read | Mapping modifiers, key remapping and `Reflect.ownKeys` behavior checked against the handbook and the chapter's own runtime helper. | Covers key iteration, `+?`/`-?`, `as` remapping, deep partials, symbol keys and the runtime boundary. | Illustrative fragments; no standalone program. | No issues. | Eight source-linked pairs; symbol-key answer matches the helper. |
| [10.2.3.04-template-literal-types.md](../10-frontend/10.2-typescript/03-type-transformations/10.2.3.04-template-literal-types.md) | read | TypeScript 7.0 Unicode code-point inference checked against the 7.0 announcement and executed: TypeScript 5.9.3 rejected `['😀', 'abc']`; TypeScript 7.0.2 accepted it. | Covers name construction, route parameters, key contracts, deep paths, join/split/replace, union bounds and the new Unicode boundary. | `HeadTail<'😀abc'>` compile check run under TypeScript 5.9.3 (old surrogate result) and 7.0.2 (code-point result). | Added the Unicode subsection; no other issues. | New source-linked revision pair for Unicode; the template group now has nine pairs. |
| [INDEX.md](../10-frontend/10.2-typescript/03-type-transformations/INDEX.md) | read | Badge 5 = four chapters plus companion; table lists four. | — | — | Read-order paragraph matches chapter order. | Docita anchors unverified against the checked-out revision. |
| [REVISION.md](../10-frontend/10.2-typescript/03-type-transformations/REVISION.md) | read | New Unicode pair cites the executed 5.9.3/7.0.2 results; other answers match their chapters. | — | — | — | Four source-linked groups plus changed-condition checks; Unicode pair added without removing authored questions. |
| [10.2.4.01-satisfies-operator.md](../10-frontend/10.2-typescript/04-advanced-patterns/10.2.4.01-satisfies-operator.md) | read | `satisfies` semantics and the TypeScript 4.9 release claim checked against the 4.9 notes and handbook. | Opens on preserving a route table's literal keys; covers finite/open keys, contextual inference, `as const` and the runtime boundary. | Illustrative fragments; no standalone program. | No issues. | Nine source-linked pairs; answers match the route-table examples. |
| [10.2.4.02-branded-types.md](../10-frontend/10.2-typescript/04-advanced-patterns/10.2.4.02-branded-types.md) | read | Brand assignability, `unique symbol` isolation and `NoInfer` (TypeScript 5.4) checked against the handbook and 5.4 notes. | Opens on same-representation IDs; covers opaque IDs, validated units/currency, parsers, JSON boundaries and flavoring. | Illustrative fragments; no standalone program. | No issues. | Ten source-linked pairs; parser and arithmetic boundaries match. |
| [10.2.4.03-decorators.md](../10-frontend/10.2-typescript/04-advanced-patterns/10.2.4.03-decorators.md) | read | Newer vs legacy conventions, `context.metadata` (TypeScript 5.2), accessor signatures and parameter-decorator limits checked against the 5.0/5.2 notes and TC39 proposal. | Opens on an annotation that does not dispatch a request; covers the three phases, convention choice, wrappers, accessors and metadata consumers. | Illustrative fragments; no standalone program. | No issues. | Ten source-linked pairs; ordering, binding and field-write answers match. |
| [10.2.4.04-declaration-files.md](../10-frontend/10.2-typescript/04-advanced-patterns/10.2.4.04-declaration-files.md) | read | Ambient vs external-module scope, `.d.mts`/`.d.cts` format rules, augmentation and package `exports` checked against the declaration and module-resolution handbooks. | Opens on a JavaScript implementation and its static contract; covers ambient declarations, augmentation, assets, publishing and triple-slash directives. | Illustrative fragments; no standalone package consumed. | No issues. | Ten source-linked pairs; the two-path fixture and packaging answers match. |
| [10.2.4.05-advanced-patterns.md](../10-frontend/10.2-typescript/04-advanced-patterns/10.2.4.05-advanced-patterns.md) | read | Correlated tuple-union dispatch checked against the handbook; the complete emitter compiles and runs. | Opens on a mismatched event/payload pair; derives the tuple union, contains the storage assertion, and states snapshot, cleanup and failure policy. | Emitter compiled with TypeScript 7.0.2 and executed on Node 24.22.2: logged `a1` and no second log after unsubscribe. | No issues. | Ten source-linked pairs; dispatch and disposal answers match. |
| [10.2.4.06-typescript-compiler-pipeline.md](../10-frontend/10.2-typescript/04-advanced-patterns/10.2.4.06-typescript-compiler-pipeline.md) | read | TypeScript 7.0's native/no-API boundary checked against the 7.0 announcement; 7.1 beta status and the 24 November stable target checked against the iteration plan and npm's `beta` dist-tag on 12 November 2026. | Opens on an editor/build mismatch; traces roots, parsing, resolution, binding, checking and emit, then project references and the language service. | Diagnostic commands documented; no fixture project was built for this row. | Updated the release-boundary date and status. | Six source-linked pairs; the Compiler API answer matches the 7.0 announcement. |
| [INDEX.md](../10-frontend/10.2-typescript/04-advanced-patterns/INDEX.md) | read | Badge 7 = six chapters plus companion; table lists six. | — | — | Read-order paragraph matches chapter order. | Docita anchors unverified against the checked-out revision. |
| [REVISION.md](../10-frontend/10.2-typescript/04-advanced-patterns/REVISION.md) | read | The TypeScript 7.0 API answer matches the announcement; decorator and declaration answers match their chapters. | — | — | — | Six source-linked groups, 55 pairs; changed-condition checks remain in place. |
| [10.2.5.01-interview-questions.md](../10-frontend/10.2-typescript/05-interview-prep/10.2.5.01-interview-questions.md) | read | Version claims (TypeScript 5.4+, `NoInfer`, `useUnknownInCatchVariables`) checked; six design sketches compiled with TypeScript 5.9.3 and again with 7.0.2 under `--strict`. | Fifty questions progress from shapes to senior/FAANG design; each answer names the mechanism and a runtime or lifecycle boundary. | Q22, Q31, Q32, Q37, Q39 and Q40 compiled cleanly under TypeScript 5.9.3 and 7.0.2; the canonical event emitter was also executed. | Fixed the `Question38` spacing error; no other issues. | One Summary; canonical-chapter links and anchors checked. |
| [INDEX.md](../10-frontend/10.2-typescript/05-interview-prep/INDEX.md) | read | Badge 1; table lists one file; the 50-question claim matches the bank. | — | — | Practice order and category links match. | Docita anchors unverified against the checked-out revision. |
| [INDEX.md](../10-frontend/10.2-typescript/INDEX.md) | read | Badge 23 = 19 chapters plus four revision companions; category table sums 4+4+4+6+1 chapters; read time restamped. | Study flow and the advanced-patterns row now describe the current composed-event chapter. | — | Fixed stale advanced-patterns topics and the tsconfig row; status badges for foundations and generics corrected to complete. | Navigation and category links checked. |
| [10.3.1.01-virtual-dom.md](../10-frontend/10.3-react/01-react-internals/10.3.1.01-virtual-dom.md) | unread | — | — | — | — | — |
| [10.3.1.02-fiber.md](../10-frontend/10.3-react/01-react-internals/10.3.1.02-fiber.md) | unread | — | — | — | — | — |
| [10.3.1.03-reconciliation.md](../10-frontend/10.3-react/01-react-internals/10.3.1.03-reconciliation.md) | unread | — | — | — | — | — |
| [10.3.1.04-rendering.md](../10-frontend/10.3-react/01-react-internals/10.3.1.04-rendering.md) | unread | — | — | — | — | — |
| [10.3.1.05-lifecycle.md](../10-frontend/10.3-react/01-react-internals/10.3.1.05-lifecycle.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.3-react/01-react-internals/INDEX.md) | unread | — | — | — | — | — |
| [REVISION.md](../10-frontend/10.3-react/01-react-internals/REVISION.md) | unread | — | — | — | — | — |
| [10.3.2.01-usestate.md](../10-frontend/10.3-react/02-core-hooks/10.3.2.01-usestate.md) | unread | — | — | — | — | — |
| [10.3.2.02-useeffect.md](../10-frontend/10.3-react/02-core-hooks/10.3.2.02-useeffect.md) | unread | — | — | — | — | — |
| [10.3.2.03-usememo-usecallback.md](../10-frontend/10.3-react/02-core-hooks/10.3.2.03-usememo-usecallback.md) | unread | — | — | — | — | — |
| [10.3.2.04-useref.md](../10-frontend/10.3-react/02-core-hooks/10.3.2.04-useref.md) | unread | — | — | — | — | — |
| [10.3.2.05-context-api.md](../10-frontend/10.3-react/02-core-hooks/10.3.2.05-context-api.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.3-react/02-core-hooks/INDEX.md) | unread | — | — | — | — | — |
| [REVISION.md](../10-frontend/10.3-react/02-core-hooks/REVISION.md) | unread | — | — | — | — | — |
| [10.3.3.01-suspense.md](../10-frontend/10.3-react/03-advanced-hooks-and-patterns/10.3.3.01-suspense.md) | unread | — | — | — | — | — |
| [10.3.3.02-error-boundary.md](../10-frontend/10.3-react/03-advanced-hooks-and-patterns/10.3.3.02-error-boundary.md) | unread | — | — | — | — | — |
| [10.3.3.03-custom-hooks.md](../10-frontend/10.3-react/03-advanced-hooks-and-patterns/10.3.3.03-custom-hooks.md) | unread | — | — | — | — | — |
| [10.3.3.04-usesyncexternalstore.md](../10-frontend/10.3-react/03-advanced-hooks-and-patterns/10.3.3.04-usesyncexternalstore.md) | unread | — | — | — | — | — |
| [10.3.3.05-performance.md](../10-frontend/10.3-react/03-advanced-hooks-and-patterns/10.3.3.05-performance.md) | unread | — | — | — | — | — |
| [10.3.3.06-state-management.md](../10-frontend/10.3-react/03-advanced-hooks-and-patterns/10.3.3.06-state-management.md) | unread | — | — | — | — | — |
| [10.3.3.07-tanstack-query.md](../10-frontend/10.3-react/03-advanced-hooks-and-patterns/10.3.3.07-tanstack-query.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.3-react/03-advanced-hooks-and-patterns/INDEX.md) | unread | — | — | — | — | — |
| [REVISION.md](../10-frontend/10.3-react/03-advanced-hooks-and-patterns/REVISION.md) | unread | — | — | — | — | — |
| [10.3.4.01-modern-hooks-react18-19.md](../10-frontend/10.3-react/04-modern-react/10.3.4.01-modern-hooks-react18-19.md) | unread | — | — | — | — | — |
| [10.3.4.02-web-components.md](../10-frontend/10.3-react/04-modern-react/10.3.4.02-web-components.md) | unread | — | — | — | — | — |
| [10.3.4.03-react-router.md](../10-frontend/10.3-react/04-modern-react/10.3.4.03-react-router.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.3-react/04-modern-react/INDEX.md) | unread | — | — | — | — | — |
| [REVISION.md](../10-frontend/10.3-react/04-modern-react/REVISION.md) | unread | — | — | — | — | — |
| [10.3.5.01-portals.md](../10-frontend/10.3-react/05-patterns-and-interview/10.3.5.01-portals.md) | unread | — | — | — | — | — |
| [10.3.5.02-compound-components.md](../10-frontend/10.3-react/05-patterns-and-interview/10.3.5.02-compound-components.md) | unread | — | — | — | — | — |
| [10.3.5.03-interview-questions.md](../10-frontend/10.3-react/05-patterns-and-interview/10.3.5.03-interview-questions.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.3-react/05-patterns-and-interview/INDEX.md) | unread | — | — | — | — | — |
| [REVISION.md](../10-frontend/10.3-react/05-patterns-and-interview/REVISION.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.3-react/INDEX.md) | unread | — | — | — | — | — |
| [10.4.1.01-ssr-csr-ssg-isr.md](../10-frontend/10.4-next.js/01-rendering-fundamentals/10.4.1.01-ssr-csr-ssg-isr.md) | unread | — | — | — | — | — |
| [10.4.1.02-app-router.md](../10-frontend/10.4-next.js/01-rendering-fundamentals/10.4.1.02-app-router.md) | unread | — | — | — | — | — |
| [10.4.1.03-server-components.md](../10-frontend/10.4-next.js/01-rendering-fundamentals/10.4.1.03-server-components.md) | unread | — | — | — | — | — |
| [10.4.1.04-client-components.md](../10-frontend/10.4-next.js/01-rendering-fundamentals/10.4.1.04-client-components.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.4-next.js/01-rendering-fundamentals/INDEX.md) | unread | — | — | — | — | — |
| [REVISION.md](../10-frontend/10.4-next.js/01-rendering-fundamentals/REVISION.md) | unread | — | — | — | — | — |
| [10.4.2.01-middleware.md](../10-frontend/10.4-next.js/02-routing-and-middleware/10.4.2.01-middleware.md) | unread | — | — | — | — | — |
| [10.4.2.02-route-handlers.md](../10-frontend/10.4-next.js/02-routing-and-middleware/10.4.2.02-route-handlers.md) | unread | — | — | — | — | — |
| [10.4.2.03-metadata.md](../10-frontend/10.4-next.js/02-routing-and-middleware/10.4.2.03-metadata.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.4-next.js/02-routing-and-middleware/INDEX.md) | unread | — | — | — | — | — |
| [REVISION.md](../10-frontend/10.4-next.js/02-routing-and-middleware/REVISION.md) | unread | — | — | — | — | — |
| [10.4.3.01-data-fetching-patterns.md](../10-frontend/10.4-next.js/03-data-and-caching/10.4.3.01-data-fetching-patterns.md) | unread | — | — | — | — | — |
| [10.4.3.02-server-actions.md](../10-frontend/10.4-next.js/03-data-and-caching/10.4.3.02-server-actions.md) | unread | — | — | — | — | — |
| [10.4.3.03-caching.md](../10-frontend/10.4-next.js/03-data-and-caching/10.4.3.03-caching.md) | unread | — | — | — | — | — |
| [10.4.3.04-streaming.md](../10-frontend/10.4-next.js/03-data-and-caching/10.4.3.04-streaming.md) | unread | — | — | — | — | — |
| [10.4.3.05-incremental-static-regeneration.md](../10-frontend/10.4-next.js/03-data-and-caching/10.4.3.05-incremental-static-regeneration.md) | unread | — | — | — | — | — |
| [10.4.3.06-static-exports.md](../10-frontend/10.4-next.js/03-data-and-caching/10.4.3.06-static-exports.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.4-next.js/03-data-and-caching/INDEX.md) | unread | — | — | — | — | — |
| [REVISION.md](../10-frontend/10.4-next.js/03-data-and-caching/REVISION.md) | unread | — | — | — | — | — |
| [10.4.4.01-authentication.md](../10-frontend/10.4-next.js/04-production/10.4.4.01-authentication.md) | unread | — | — | — | — | — |
| [10.4.4.02-image-optimization.md](../10-frontend/10.4-next.js/04-production/10.4.4.02-image-optimization.md) | unread | — | — | — | — | — |
| [10.4.4.03-deploying-nextjs.md](../10-frontend/10.4-next.js/04-production/10.4.4.03-deploying-nextjs.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.4-next.js/04-production/INDEX.md) | unread | — | — | — | — | — |
| [REVISION.md](../10-frontend/10.4-next.js/04-production/REVISION.md) | unread | — | — | — | — | — |
| [10.4.5.01-interview-questions.md](../10-frontend/10.4-next.js/05-interview-prep/10.4.5.01-interview-questions.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.4-next.js/05-interview-prep/INDEX.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.4-next.js/INDEX.md) | unread | — | — | — | — | — |
| [10.5.01-react-hook-form.md](../10-frontend/10.5-form-handling/10.5.01-react-hook-form.md) | unread | — | — | — | — | — |
| [10.5.02-zod.md](../10-frontend/10.5-form-handling/10.5.02-zod.md) | unread | — | — | — | — | — |
| [10.5.03-formik.md](../10-frontend/10.5-form-handling/10.5.03-formik.md) | unread | — | — | — | — | — |
| [10.5.04-tanstack-form.md](../10-frontend/10.5-form-handling/10.5.04-tanstack-form.md) | unread | — | — | — | — | — |
| [10.5.05-server-actions-and-form-patterns.md](../10-frontend/10.5-form-handling/10.5.05-server-actions-and-form-patterns.md) | unread | — | — | — | — | — |
| [10.5.06-autosave-draft-recovery.md](../10-frontend/10.5-form-handling/10.5.06-autosave-draft-recovery.md) | unread | — | — | — | — | — |
| [10.5.07-interview-questions.md](../10-frontend/10.5-form-handling/10.5.07-interview-questions.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.5-form-handling/INDEX.md) | unread | — | — | — | — | — |
| [REVISION.md](../10-frontend/10.5-form-handling/REVISION.md) | unread | — | — | — | — | — |
| [10.6.01-css-animations.md](../10-frontend/10.6-animation/10.6.01-css-animations.md) | unread | — | — | — | — | — |
| [10.6.02-framer-motion.md](../10-frontend/10.6-animation/10.6.02-framer-motion.md) | unread | — | — | — | — | — |
| [10.6.03-gsap.md](../10-frontend/10.6-animation/10.6.03-gsap.md) | unread | — | — | — | — | — |
| [10.6.04-react-spring.md](../10-frontend/10.6-animation/10.6.04-react-spring.md) | unread | — | — | — | — | — |
| [10.6.05-web-animations-api.md](../10-frontend/10.6-animation/10.6.05-web-animations-api.md) | unread | — | — | — | — | — |
| [10.6.06-view-transitions-and-scroll-driven-animations.md](../10-frontend/10.6-animation/10.6.06-view-transitions-and-scroll-driven-animations.md) | unread | — | — | — | — | — |
| [10.6.07-canvas-svg-animation.md](../10-frontend/10.6-animation/10.6.07-canvas-svg-animation.md) | unread | — | — | — | — | — |
| [10.6.08-interview-questions.md](../10-frontend/10.6-animation/10.6.08-interview-questions.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.6-animation/INDEX.md) | unread | — | — | — | — | — |
| [REVISION.md](../10-frontend/10.6-animation/REVISION.md) | unread | — | — | — | — | — |
| [10.7.01-html-fundamentals.md](../10-frontend/10.7-html-css/10.7.01-html-fundamentals.md) | unread | — | — | — | — | — |
| [10.7.02-css-fundamentals.md](../10-frontend/10.7-html-css/10.7.02-css-fundamentals.md) | unread | — | — | — | — | — |
| [10.7.03-browser-rendering.md](../10-frontend/10.7-html-css/10.7.03-browser-rendering.md) | unread | — | — | — | — | — |
| [10.7.04-seo.md](../10-frontend/10.7-html-css/10.7.04-seo.md) | unread | — | — | — | — | — |
| [10.7.05-pwa.md](../10-frontend/10.7-html-css/10.7.05-pwa.md) | unread | — | — | — | — | — |
| [10.7.06-css-architecture-styling-approaches.md](../10-frontend/10.7-html-css/10.7.06-css-architecture-styling-approaches.md) | unread | — | — | — | — | — |
| [10.7.07-theming-design-tokens.md](../10-frontend/10.7-html-css/10.7.07-theming-design-tokens.md) | unread | — | — | — | — | — |
| [10.7.08-browser-storage.md](../10-frontend/10.7-html-css/10.7.08-browser-storage.md) | unread | — | — | — | — | — |
| [10.7.09-tailwind-css.md](../10-frontend/10.7-html-css/10.7.09-tailwind-css.md) | unread | — | — | — | — | — |
| [10.7.10-interview-questions.md](../10-frontend/10.7-html-css/10.7.10-interview-questions.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.7-html-css/INDEX.md) | unread | — | — | — | — | — |
| [REVISION.md](../10-frontend/10.7-html-css/REVISION.md) | unread | — | — | — | — | — |
| [10.8.01-react-native-cross-platform.md](../10-frontend/10.8-mobile/10.8.01-react-native-cross-platform.md) | unread | — | — | — | — | — |
| [10.8.02-deep-linking-universal-links.md](../10-frontend/10.8-mobile/10.8.02-deep-linking-universal-links.md) | unread | — | — | — | — | — |
| [10.8.03-testing-react-native-apps.md](../10-frontend/10.8-mobile/10.8.03-testing-react-native-apps.md) | unread | — | — | — | — | — |
| [10.8.04-expo-eas-builds.md](../10-frontend/10.8-mobile/10.8.04-expo-eas-builds.md) | unread | — | — | — | — | — |
| [10.8.05-codepush-ota-updates.md](../10-frontend/10.8-mobile/10.8.05-codepush-ota-updates.md) | unread | — | — | — | — | — |
| [10.8.06-app-store-release-automation.md](../10-frontend/10.8-mobile/10.8.06-app-store-release-automation.md) | unread | — | — | — | — | — |
| [10.8.07-interview-questions.md](../10-frontend/10.8-mobile/10.8.07-interview-questions.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/10.8-mobile/INDEX.md) | unread | — | — | — | — | — |
| [REVISION.md](../10-frontend/10.8-mobile/REVISION.md) | unread | — | — | — | — | — |
| [INDEX.md](../10-frontend/INDEX.md) | unread | — | — | — | — | — |

## Section roll-up

- Files with a read-backed row: **43 of 179**.
- Range covered so far: `10.1-javascript/INDEX.md`, all of `10.1-javascript/01-execution-and-scope/`, `10.1-javascript/05-functional-patterns/` (index, Generators chapter, revision), and the complete TypeScript stack (`10.2-typescript/`, 29 documents including the stack and category indexes and all four revision companions).
- Topic gap closed: the Generators chapter never named `Symbol.iterator`/`Symbol.asyncIterator` or the iterator helpers, although the interview bank teaches both; a new section, three revision pairs and a runtime caveat in the bank now cover them. `Iterator.concat` and `AsyncIterator` were confirmed absent on Node 24.22.1 and are labeled accordingly.
- TypeScript gaps closed: the template-literal chapter now covers TypeScript 7.0's code-point inference and its disagreement with runtime UTF-16 indexing; the generics chapter states the ES-module requirement for its top-level `await`; the compiler-pipeline chapter's release boundary was refreshed to 12 November 2026 (7.1 beta, stable target 24 November) and the stack index's stale advanced-patterns and tsconfig topics were corrected.
- Edited but not yet fully read: `10.1.6.05-interview-questions.md` (one answer corrected), so its row stays `unread` and no full-read claim is made for it.
- Everything else is `unread` in this ledger and is not claimed as reviewed.
- Defects found in this range: none in the seven JavaScript chapters; the section-level count-scope defect in `10.1-javascript/INDEX.md` (a `Files` column that counted chapters while the badge counted companions) was fixed in the same pass across the five stack indexes that carried it. In TypeScript: two wrong utility-type comments, one dangling example reference, one spacing error in the interview bank, two stale index topic rows, two malformed `wip` status badges, and the missing TypeScript 7.0 Unicode boundary.