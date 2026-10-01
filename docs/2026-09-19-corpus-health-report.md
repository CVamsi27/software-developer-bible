<!-- section: Meta | category: Reference | tags: health-report, verification-gates, session-retrospective -->
[![Section](https://img.shields.io/badge/section-Meta-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-800080)](#)
[![Tags](https://img.shields.io/badge/tags-health--report,%20verification--gates,%20session--retrospective-lightgrey)](#)

# Corpus Health Report — September 2026

> **TL;DR:** A multi-commit hardening session (see `git log` for the running
total), organized around one
> recurring method: **measure first, fix what the measurement proves, then
> gate the class so it cannot regress.** This report is the ledger — what
> each gate now enforces, which rules caught real defects on their first
> run, which sweeps came back clean, and what remains unexamined.

## Definition

- **Drift class** — a category of defect that recurs structurally (e.g.
  "claims outrun content", "newer chapters current, older siblings stale").
- **Owned claim** — a number in docs/INDEXes that a script restamps from the
  same computation it checks (`--write`); an unowned claim is a drift waiting
  to happen.
- **Date-gated data table** — a freshness-gate table keyed on *dates*, not
  banned strings: an entry starts failing the day reality changes, with no
  rule edit needed.
- **Day-one catch** — a gate rule that found a real corpus defect on its very
  first baseline run, before any planted test.

## First Principles

1. **A doc is a claim about the world; gates are how claims stay true.**
   Every drift found this session was a claim (a count, a promise, a pin, a
   version) whose referent had moved. The fix is never "edit the number" —
   it is "give the number an owner that recomputes it."
2. **Sweeps decay; gates don't.** A manual sweep is true the day it runs and
   less true every day after. Converting the sweep's finding into a gate rule
   converts a point-in-time audit into a standing property — and the classes a
   gate cannot own (singletons, context-dependent mentions) decay back
   silently unless re-probed, which is what the quarterly **drift drill**
   (`scripts/drift_drill.py` + `.github/workflows/drift-drill.yml`) does:
   20 STALE classes that open a tracking issue, 11 REVIEW classes listed for
   human judgment.
3. **The gate must be calibrated to reality, then proven both ways.** A rule
   that fires on the corpus as it is buries signal; a rule never proven to
   fire may be dead code (one rule here was — unreachable after `return` —
   and only the plant-test exposed it).
4. **Drift concentrates where content was extended without revisiting
   siblings.** Four separate finds (node pins, Actions pins, Istio
   apiVersions, Compose keys) showed newer content current and older content
   stale *within the same stack*.

## How It Works

### The method, applied

Each round followed the same loop:

1. **Hunt** with a grep/measurement calibrated against its own false
   positives first (a question counter that couldn't see `### 1.` headings,
   a regex blind to words between number and noun, a double-quote-only grep
   — each fixed before trusting its output).
2. **Verify every hit against the live world** — primary docs, dated
   secondary sources — before editing. Honest history ("X was…; Y is the
   modern path") was left alone every time it was actually honest.
3. **Fix confirmed defects** — bias toward deepening content over shrinking
   claims (Java bank 20→30 written rather than "30"→"20"; mobile bank
   19→30).
4. **Gate the class** so the fix is permanent.
5. **Prove the gate both ways**: fires on the planted defect, silent on all
   real files, and *wired* — the failure branch reaches the exit.

### Gate inventory after the session (29 gates, all CI-enforced)

| Gate | Enforces | Session change |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 `check_counts.py` | Every count claim on the nav surface | +4 owned claims: gates-page walker scope, api-contract totals (sourced from the gate-14-locked JSON), freshness rule count, drill class counts |
| 2 `check_alignment.py` | Table alignment + header rows exist | — |
| 3 `check_structure.py` | Numbering, single-H1, dup-H2 slugs, **adjacent-duplicate headings**, **banks-last**, **INDEX completeness**, **doc reachability**, **chapter reachability** | +banks-last rule with two documented exemptions; +INDEX-completeness (no invisible sub-stacks — caught the 60-realtime omission on first run), +orphan-doc reachability (BFS from entry points; born from the 7-of-10 docs/ orphan scan), +chapter reachability (556/556 linked at baseline; a chapter without its INDEX row now fails the build), +adjacent-duplicate headings (a heading followed by its own twin with only blank lines between — the paste artifact a promotion pass leaves; found once on disk, ignored once proven narrow enough to have no legitimate form) |
| 4 `check_links.py` | Internal links, honest link labels, **inline repo paths resolve** | +inline-path rule (2026-09-21): a prose code span naming a file must resolve — the lane study docs carried 53 relics from three generations of renumbering (`software-developer-bible/16-Testing/01-Overview.md` → `30.2-system-design/13-Rate-Limiter.md` → today), invisible to any link checker because they are not links; scope calibrated over three rounds (a design doc's planned folders and a reader's own project paths are not defects) |
| 5 `check_freshness.py` | **16 rules**, incl. two date-gated EOL tables + Compose | +EOL-BASE-IMAGE, +EOL-GITHUB-ACTION, +OBSOLETE-COMPOSE-VERSION |
| 6 `link_baseline.py` | Cited URLs probe-verified (2379) | +verified SRE/broker URLs |
| 6b `check_template.py` | Template, metadata, **question-count claims**, **bank floor**, **fence grammar** | +count-claim contract (claims read only from intro blockquote/TL;DR); +25-question floor with one named-format exemption; +closing-fence rule with full CommonMark nesting semantics |
| 7–15 | Claims, whitespace, first-principles, cross-refs, duplication, twins, read-time, search byte-lock, self-wiring | +gate 15 rule 10: no unwired checkers — a check_*/test_* script nothing invokes is invisible to the suite (the tooling-level invisible-sub-stack) |
| 16 `test_md_fences.py` | The fence owner's semantics, pinned by 16 characterization tests | +gate born from writing the tests: `is_fence_line` flagged regex-matching content lines as delimiters (now true only on real open/close); `read_time` had been silently miscounting nested-fence content as reading text |
| 17 `test_fixers.py` | The fixers' repair output, pinned by planted-defect round trips (byte-exact, idempotent, no-mangle negative) | +closes the repair-wrongly failure mode the session demonstrated twice — corrupted repair pass, silently-skipping box fixer — by asserting each fixer's recorded contract in a temp-tree sandbox |
| 18 `test_gates.py` | **The suite self-test**: each sandboxable gate's canonical defect planted in a temp tree must still fire; clean content (incl. a real passing chapter) must still pass | +closes the last unwatched layer — detection itself; the two-sided design caught the wiring checker's check/write word-count asymmetry past twenty gates before landing; now 12 gates proven both ways, incl. gate 19's table-only-answer plant |
| 19 `check_answer_depth.py` | **≥25 prose words per interview answer**, fence- and table-aware — tables and code cannot substitute for reasoning | born from the probe that falsified the arc's own table-counting scanner (27 table-only answers); the `### Question Categories` false positive is designed out by requiring the digit in question headings |
| 21 `fix_nav_labels.py` | **Previous/Next nav labels are canonically-cased human titles, not paths**: 57 wrong-cased tokens (`Mvcc`, `Cqrs Di`, `Sli Slo Sla`, `Cap Theorem`, `Iac`, `Rabbitmq`, `Webrtc`, `Typescript`, `Cicd`) plus **55 labels left as raw relative paths** and **132 labels as slug-humanized forms of their targets** (`Useeffect`, `Bff`, `Tanstack Form`, `Socket Io`, `SLI SLO SLA`) — an entire class that no gate watched, because gate 4's stale-label rule required the label to be *spaceless* and gate 11 compares prose bodies, not footers | born from the 2026-09-21 navigation-surface probe: the same generator that humanized target slugs also skipped humanizing 55 of them; rule 2 derives the fix from the target file's own H1, so a label cannot drift from what it links to. Two-sided plant (path label + acronym casing) |
| 22 `check_fixpoint.py` | **A clean corpus is a no-op for every writer** — every repair/restamp writer run over a copy of the tree must leave it byte-identical | born from the 2026-09-21 writer audit, which asked the question the rest of the suite structurally cannot: *what if a writer edits files its checker calls clean?* Then no gate can ever flag the edit. Two live instances found by hand — `fix_code_whitespace.py` stripping trailing whitespace inside layout fences the checker deliberately exempts, and `fix_fence_labels.py` proposing `typescript` for mixed cheat-sheet fences (title bar + code + tips, which would have rendered as broken code) |
| 23 `check_scope_floor.py` | **Every corpus gate fails honestly when its scope is empty** — exit 1 *and* the words `SCOPE ERROR`, on every corpus gate, with the list derived from `verify.sh` so a new gate must carry a floor or be exempt by name | born from the 2026-09-21 probe that ran every checker against an empty tree: **15 of 19 exited 0** (`OK — 0 links checked`, `template compliance OK`), two died in a traceback, and four more vacuous passes hid behind those (`--diff` with 0 stacks, `read_time` over 0 INDEXes, `link_baseline` with 0 citations, and `check_fixpoint` itself, since an empty copy is a fixed point of everything). The floor is one owner (`scan_scope.guard`, imported by every corpus gate) + this gate proving the property for all of them |
| drift drill | 31 staleness classes, quarterly + issue-tracking | — |

| 24 `prose_hygiene.py` | **The prose convention the corpus already follows**, plus two markdown rendering breaks — spelling, glued ATX headings, GFM table cell counts | born from the 2026-09-22 quality probe: 13 spelling pairs carried *both* forms in a corpus that is American by 845 to 26 (`behaviour` beside `behavior`), one heading had no space after its hashes (CommonMark renders it as literal text, so the section lost its structure), and two table rows held unescaped pipes inside a code span (GFM splits on the pipe before inline parsing, so the rows rendered with extra columns and the table stopped lining up). Pairs the corpus keeps consistently (`cancelled` 25 / `canceled` 0) or genuinely splits (`grey` 3 / `gray` 4) are excluded by recorded decision; proper nouns a word rule cannot know — `Colour Contrast Analyser`, `aria-labelledby`, `Sopra Steria Defence` — are named exemptions. Two-sided plants for all three rules; the writer is a fixed point (gate 22) |
| 20 `test_prose_scan.py` | The prose scanner's classification contract (feeds gate 19's depth arithmetic) | — |
| 25 `check_dilution.py` | **A chapter must not restate itself** — ceiling baseline over the measured 0/0 state (adjacent-sentence restatement, intra-chapter near-duplicates ≥ 20 lines apart; gate 11 owns cross-chapter prose) | born from the 2026-09-22 dilution measurement: all four probes returned zero, so the measurement became a standing ceiling instead of a one-day verdict; check-only, no writer |
| 26 `check_code_dup.py` | **A chapter must not re-teach another chapter's code** — cross-file fenced-block pairs (identical token streams ≥ 10 lines; near ≥ 0.85) against a ceiling baseline of the classified keeps (identical 2, near 16) | born from the 2026-09-22 duplicate-example audit: 27 candidate pairs ≥ 20 lines, 10 real re-teaches trimmed to pointers (see Fix ledger), 17 kept by classification; strings preserved in the tokenizer after the first normalizer scored prose-in-object-literals as duplicates |

### Day-one catch ledger

Five rules found real defects on their first baseline run — the empirical
argument for the whole method:

| Rule | Caught | Why the manual pass missed it |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| inline-path rule (4) | 53 dead prose paths in the two lane study docs, from three renumbering generations | the paths are code spans, not links — a link checker is structurally blind to them |
| nav-label rules (21) | 57 wrong-cased tokens, 55 path-shaped labels, then 132 slug-humanized labels across 125 files | no gate watched footers: gate 4 only rejected *spaceless* path labels, gate 11 compares prose bodies |
| question-count contract (6b) | mobile bank "30+ curated questions" vs 19 held | sweep regex allowed no words between number and noun |
| EOL-GITHUB-ACTION | `setup-node@v3`, `upload-artifact@v3`, a stray `checkout@v3` | sweep grepped only the actions it thought of |
| OBSOLETE-COMPOSE-VERSION | three single-quoted `version:` keys | sweep grep matched double quotes only |
| fence grammar (6b) | 38 labeled closes (+1 prose-glued) — renderers merge following headings into the code block | naive greps treat fences as pairs; CommonMark treats only bare same-length fences as closes |
| INDEX completeness (3) | `60-realtime/INDEX.md` deep-linked all 11 websocket chapters but never linked the `60.1-websockets/` stack INDEX itself | the computed files badge was right; only the hand-written navigation was silent — omission, not a wrong number |

Plus one process catch: the first version of the api-contract count rule was
unreachable dead code (appended after `return`); the plant-test caught it —
proof-after-fix is the only proof.

### Fix ledger (defects repaired in the corpus)

- ~55 EOL base-image pins (node:18/20 → 22; golang:1.21 → 1.26 — **two years
  past EOL**; rust:1.72; graalvm:17 tag family)
- 7 retired GitHub Action pins (checkout/setup-node/codecov @v3 → v4)
- 3 more Action pins + 3 single-quoted Compose keys caught by the new rules
- 11 obsolete Compose `version:` keys across 6 files
- 2 writer scopes aligned with their checkers: `fix_code_whitespace.py
  --trailing-ws` now honors the checker's layout-fence exemption (`text`,
  `csv`, `tsv`, `anki`, `diff`, `mermaid` — in a csv/anki fence a trailing tab
  is an empty field), and `fix_fence_labels.py` no longer proposes a language
  for mixed cheat-sheet fences. Neither was a corpus defect: both were
  *invisible edits* waiting to happen, which is why gate 22 now runs every
  writer over a corpus copy and requires zero byte differences
- 2 Istio `v1alpha3` resources (removed in Istio 1.24) → `v1beta1`
- Java bank +10 Spring questions (its own Summary already promised the arc);
  mobile bank +11 (crash reporting, storage matrix, push, OTA-crash)
- CodePush hosted-service shutdown (Mar 31 2025) stated in the OTA chapter
- Azure AD → Microsoft Entra ID; TypeScript bank "50+" → "50"
- 226 lane-guide headings re-leveled to one H1 per document
- Spring Boot chapter deepened 1→7 code blocks
- 3 new interview banks (nginx, twelve-factor, infra-patterns category) —
  closing the last stack with zero bank coverage
- 2 doc-vs-artifact drifts (api-contract totals, walker scope) now owned
- **8 interview banks completed to the 25-question standard** (+103 questions: HTML/CSS, production engineering, CDN & edge, caching, IaC, infra-patterns, nginx, twelve-factor); the REST bank measured as 60 real questions in an older mixed format — exempted with a reason, not thinned
- **10 thin chapters deepened to corpus depth** (StatefulSets/DaemonSets, Jobs/CronJobs, GitLab CI, Babel, esbuild/SWC, ArgoCD, Jenkins, RBAC/NetworkPolicies, Dockerfile practices, service mesh) — depth-sweep verdict: no true gaps remain above the 900-word line
- 38 closing fences carrying info strings repaired (a fixer sharing the gate's exact parser — one owner, so fixer and gate cannot disagree)
- fence parsing unified: ten scripts' naive `in_fence` toggles replaced by one `md_fences.walk` owner; the unified parser immediately found **20 over-padded boxes in 17 files** the desyncing old parser had silently skipped — and a later audit found **three more toggles in check_template itself** (the gate that owns fence grammar) plus one in the fix_section_order fixer: fourteen retired in total across twelve scripts. Migrating check_template closed a live honesty gap: the question-count contract had counted a literal Q-marker inside a nested-fence example, masking a 26-for-25 over-claim (pinned both ways in the suite self-test)
- **new: 20.9-message-brokers stack** — 4 chapters + INDEX in the reserved-but-empty slot; brokers had 50+ example mentions corpus-wide but no canonical home; includes the Docita Anchor whose honest verdict is "zero brokers, deliberately" (the 20.9.01 when-not-to lesson shipped)
- **20.9 wired into 31 sites** — See Also links with per-site reason phrases from all 12 system-design case studies, the heavy broker-mention chapters, and both system-design INDEXes; the top INDEX's missing table row restored
- **docs layer made reachable** — 7 of 10 docs/ files were linked from nowhere; entry points repaired (README, health-report See Also, scripts map) and the property gate-enforced
- **answer-quality arc: 247 answers deepened across 11 banks** — the question-count floor passed banks holding flashcard bullets and code-only answers; a fence-aware, label-agnostic depth scan (all prose between question heading and next heading) found them: TypeScript 29, security 36, NestJS 32, microservices 27, Node.js 31, CI/CD 23, Kubernetes 19, Docker 14, REST 6, auth 5, AI engineering 25 — each a hand-authored senior-depth prose block (mechanism, tradeoff, failure mode) written against the existing content; re-scan verdict: zero answers under 40 words corpus-wide
- **the probe that falsified the arc's own scanner: 27 table-only answers** — the arc's depth scan counted table words, so a comparison table plus one `**Answer:**` label line read as healthy; a prose-only re-scan (fences, tables, headings, quotes, badges excluded) found Docker 10, K8s 7, CI/CD 5, NestJS 2, REST 1, auth 1, security 1 — every one now carries the mechanism/trade-off prose the table couldn't show, and REST Q10 (pure code, masked by a lax section boundary) was caught by the new gate's stricter scan; verdict: zero answers under 25 prose words corpus-wide
- **gate 19 `check_answer_depth.py`** — makes that property permanent: ≥25 fence- and table-aware prose words per answer, question headings require the digit (the `### Question Categories` false positive burned the manual scans twice), the suite relabeled 21→22 gates with wiring/contributing/gates-doc restamped from one computation, and the canonical plant (a table-only answer) is pinned two ways in the self-test (12/12)
- **rule 2, the chapter sweep: the same failure mode in study chapters** — a measured survey of 2028 core sections showed the 0-word Best Practices/How It Works sections are a deliberate H3-title-plus-code genre (explanations live in headings and annotated code; exempt by decision, not omission), but 9 chapter Definitions were table-only or thin (4 bare tables — hash-tables-internals, auth-fundamentals, and two 20.9 chapters written that week — plus a diagram-only and 4 marginal intros); all 9 now carry definitional prose, and gate 19 rule 2 makes chapter Definitions >= 25 prose words permanent, pinned as a second plant (self-test 13/13)
- **the duplicate-example audit: 10 code blocks re-taught across sibling chapters, trimmed to pointers (2026-09-22)** — the prose dilution probes came back clean, so the last unmeasured class was examples: language-tagged fenced blocks tokenized cross-file (strings preserved — the first normalizer discarded them and scored prose-in-object-literals as shape-alike). Ground truth: 8 raw-identical blocks in 4 pairs out of 7,476 fenced blocks, and 27 structural pairs ≥ 20 lines. Each pair classified: **10 real re-teaches** trimmed to a pointer at the canonical home — React `FilteredList` in three files → `useeffect.md`, the Next.js revalidate handler in three blocks → `caching.md`, GraphQL loading states → `apollo-client.md`, `hoisting.md`'s copy of `scope.md`'s best-practices snippets, `this.md`'s `ObjectPool` → `gc.md`, `memoization.md`'s basic `memoize` → `closures.md` — versus **17 kept by classification**: deliberate contrasts (debounce-vs-throttle on the same hook, ISR-vs-static-export on the same page, `apply(this)` variants), interview-recap compilations, and docita defense quotes. Gate 26 `check_code_dup.py` makes the census standing with a ceiling baseline of the classified keeps (identical 2, near 16); hits count as pairs, so a 5-way copy-paste contributes 10
- **the See Also pilot: 10.1-javascript's 92 bare entries carry hand-authored reasons, gate 27 makes the hygiene standing (2026-09-23)** — the progressive-improvement plan recorded under the non-action below executed its first stack: all 92 bare entries in 10.1-javascript (84% bare, the worst core study stack) now carry per-pair reasons, including the stamped footer triple (Coding Patterns / Node.js / TypeScript) where the connecting mechanism genuinely differs per chapter (`this` → TS is `ThisType<T>`, the event loop → Node is libuv phases). Two rules made standing: a per-stack bare ceiling (a stack may improve freely; regressing above its committed maximum fails the build) and the label-echo rule, which fired on 3 real defects in the existing corpus — including a house-style sample written earlier in this very report. Corpus bare count 1893 → 1803; the remaining 72%-surface improves stack by stack, never bulk-derived. Pilot #2 (same day): 10.3-react's 120 bare entries — the worst remaining core sub-stack — now carry per-pair reasons (corpus 1803 → 1683, 10-frontend ceiling 415 → 295); the two-class decomposition held exactly (footer-target entries whose mechanism varies per source chapter + real intra-stack cross-links). Pilot #3 (same day): 20.6-microservices' 91 bare entries — the worst backend sub-stack — plus one honest relabel (bulkhead's "Resilience Patterns" entry actually targeted the gRPC chapter) (corpus 1683 → 1592, 20-backend ceiling 416 → 325). Pilot #4 (same day): 20.2-nestjs (68) + 20.4-database (57) together — 125 reasons, corpus 1592 → 1467, 20-backend ceiling 325 → 200. Pilot #5 (same day): 40.2-kubernetes' 95 bare entries — the worst platform sub-stack (PDBs negotiate scale-in, presets are admission-time mutation, configMapGenerator's hash-suffix triggers rollouts) — corpus 1467 → 1372, 40-platform ceiling 379 → 284. Pilot #6 (same day): the remaining 40-platform sub-stacks in one pass (docker, cdn, ci-cd, observability, build-tools, git-advanced, serverless-edge, monorepo — 284 reasons) — corpus 1372 → 1088, 40-platform fully reasoned; six pilots, zero echo defects across 807 authored reasons. Pilot #7 (same day): 60-realtime (29), 00-strategy (8), and docs (5) fully reasoned (all three dropping off the bare list entirely), plus 20.8-caching (7), 20.9-message-brokers (2), 20.13-java (7), 30.3-infra-patterns (8), and 10.8-mobile (7) — 73 hand-authored reasons, zero echo defects across 880 cumulative reasons, corpus bare count 1088 → 1015; WebTransport MTU backpressure and Redis Streams durability deepened. Pilot #8 (same day): 10.2-typescript (87) and 10.4-next.js (85) — the two largest remaining 10-frontend sub-stacks — fully reasoned in one pass; the TS stamped footer triple and Next.js footer quintuple got per-chapter mechanisms (narrowing → discriminated unions are the type-level `if`; `keyof` → mapped types are its constraint vocabulary; streaming SSR → Suspense boundaries are where the stream splits; PPR → the static shell is caching's fastest variant), corpus 1015 → 843, 10-frontend ceiling 288 → 116, 880 → 1052 cumulative reasons. Pilot #9 (same day): the final pass — the corpus is now at **zero bare See Also entries**. Two link-integrity defects surfaced first and were repaired before authoring: 76 case-study/theory footer entries labeled Database/Microservices/REST APIs/WebSockets pointed at the local `INDEX.md` (a reader clicking "Database" landed on the case-study list), now repointed to the true stacks with reasons; and 7 `(#)` placeholder links in the interview toolkit, now real targets. Then the remaining stacks in one sweep: 20-backend remainder (184), 30-architecture (150), 50-quality (133), 10-frontend remainder (116), 70-interview-toolkit (152), 81-lanes (108) — ~750 hand-authored reasons, zero echo defects. Gate 27's baseline is now 0 across every stack: any future bare entry fails the build.

### Measured non-actions (the boundary findings)

- **39 interview banks, 741 pairs**: zero true cross-stack duplicates; the
  similarity was shared *form* (section skeleton, question phrasing). The
  only genuine overlap is border topics covered once per border.
- **00-strategy vs lanes**: max shingle overlap J=0.005 — the ownership
  boundary is real.
- **Enzyme / `getServerSideProps` / Swarm / `@babel/polyfill` mentions**: all
  teach the migration *away*; left alone.
- **Cloud staleness sweep (12 classes)**: Stackdriver, Amazon ES, CodeCommit,
  SDK v2, `get-login`, dead Lambda runtimes, EC2-Classic, GCE, `--generator`,
  `helm init`, `template_file`, Ansible `include:` — zero genuine hits.
- **JS ecosystem sweep (14 classes)**: CRA, moment, node-sass, request,
  tslint, `ReactDOM.render`, removed lifecycles, Vue 2, Bower,
  `CommonsChunkPlugin`, `yarn global`, `npm --save`, webpack v4 shapes — zero
  genuine hits. Two consecutive clean sweeps say the hunt is saturating.
- **See Also reasons: the 72% bare-entry class measured, and deliberately
  NOT mass-repaired (2026-09-22)** — 2727 See Also entries, 1958 bare, 438
  files: a class whose shape (uniform, large, mechanical) matched the nav-label
  and collapsed-sheet defects, so the derivation was drafted before any
  bulk edit. The draft settled it: of 1888 entries a title-derivation could
  reach (1098 INDEX targets, 786 chapter targets; 14 unresolved are `#`
  placeholders and two stale contributing paths), 1874 collapse into four
  templates — "the X topic index" ×1098, "derives X from first principles"
  ×776 — where X is the target's own title. That is not a reason phrase; it
  is the bare link with extra words, repeated hundreds of times, and it would
  be the fourth uniform-and-wrong signature this corpus has had to repair —
  minted this time by the repair pass itself. The honest statement: a reason
  is a per-link judgment that can be *assisted* (derivation proposes, human
  disposes), *hygiene-checked* (resolves, not a label duplicate, not
  boilerplate-identical to its siblings) and *progressively* improved, but
  1958 judgments do not compress into a template. No fix arc; the constraint
  is written down in `gate-design-principles.md` under Common Mistakes.
- **prose dilution, measured four ways and found absent (2026-09-22)**: the
  recurring reader complaint is that a corpus repeats itself and buries its
  main point, so the question was measured instead of assumed, over the 776
  chapter files. Adjacent-sentence restatement (Jaccard ≥ 0.34 on 4-word
  shingles, both sides ≥ 8 content words): **0**. The partial band a reader
  would still notice (0.20–0.34): **0**. Intra-chapter near-duplicate
  paragraphs, 5-word shingles, J ≥ 0.40, at least 20 lines apart: **0**.
  TL;DR-versus-Summary overlap, the two template sections whose restatement
  would be designed in rather than accidental: **median 0.00**, and no chapter
  above 0.25 — the sections summarize different things. What the sweep did
  surface was a scanner artifact, worth recording so it is not re-hunted: 142
  "wall-of-text paragraphs" turned out to be consecutive numbered-list and
  table-of-contents lines, which my run-length heuristic read as one sentence
  because list items do not end in a period. The one durable residue is the
  register itself — eighteen empty openers (`it is important to note`,
  `needless to say`, `at the end of the day`, `let's dive into`, …) of which
  the corpus uses **zero** — now gated as rule 4 of `prose_hygiene.py`, with
  `essentially` and `the fact that` deliberately excluded because all 16 of
  their occurrences do real work.

## Real-world Application

Running the equivalent pass on any large doc corpus: inventory the claims,
sort them into *owned* vs *unowned*, convert the unowned live-count ones to
restampers first (cheapest, highest yield), then sweep defect classes only
where a gate can be built from the wreckage. Skip gate rules for singletons
— a rule needs a recurring class to guard.

## Common Mistakes

- Planting a defect and testing only the script — gate 10's failure branch
  once wrote the wrong variable name and a red build passed CI. Prove the
  *suite* fails, not just the tool.
- Banning strings instead of dates in EOL rules (fires forever on not-yet-EOL
  versions, goes stale itself later).
- Hand-editing numbers the restampers own — they will be reverted by the next
  `--write` run.
- Trusting a sweep regex before calibrating it against known-answer corpus
  files.

## Best Practices

- Fix-then-gate in the same session: an unfixed class re-accumulates, an
  ungated fix decays.
- Bias content edits toward *deepening* — finish the promise rather than
  shrink it.
- When a sweep comes back clean twice, stop sweeping and write the ledger.
- Keep exemption lists *named and reasoned* inside the gate code, not in a
  side doc.

## Summary

The corpus is now 560 study chapters and 40 interview banks, every one at or
above the 25-question floor the gate enforces. After the answer-quality arc and
the table-only probe that falsified its scanner, no answer and no chapter
Definition falls under the 25-prose-word floor gate 19 enforces — its rule 2
having measured and deliberately exempted the H3-plus-code genres.

The sweeps below are the session's ledger, each one a fix-then-gate pair:

- **one scanner owner: `prose_scan.py` + gate 20** — the reasoning-prose classification that lived as copy-pasted snippets now has a single module (the md_fences move applied to prose), consumed by gate 19 and pinned by a new characterization suite wired as gate 20; read_time keeps its own reading-weight model by recorded decision (weight vs. reasoning are different questions)
- **code-sample audit, first arc: 24 collapsed cheat sheets repaired, the class gated** — a fence-landscape survey (7,844 fences) found the unlabeled-fence and 1-line-fence classes benign after calibration (diagram/output genres, deliberate), but 24 files shared an identical 6-fence signature in their Cheat Sheet: a stray close+empty-open pair had collapsed the fence structure, spilling failure tables and code outside the blocks; deterministic repair (keep first/last, delete the middle four) with per-file assertions, and gate 6b rule 3 now fails any empty fence (blank-only included) — pinned in the self-test on an isolated plant (14/14)
- **forensics: the corruption was born with the sheets, not a later pass** — commit archaeology (following the rename 11-System-Design/04-Netflix.md to 30.2.2.04) shows the collapsed 6-fence shape present from the first commit that carried a sheet: 2535a0b4 2026-07-28 'Add missing ## Cheat Sheet and ## See Also' emitted it at birth, and every subsequent bulk pass — including the entire Sept pipe-alignment saga and the fence-parser unification itself — preserved it faithfully for ~8 weeks. Lesson: a generator with no fence-structure test mints defects that later correct tools then dutifully conserve. Latent-sibling scan: 0 unclosed sheets corpus-wide (distribution 0:92, 2:400, 4:16, 6:3 — the three 6-fence sheets are legitimate multi-block sheets with labeled opens); the 2535a0b4 class has no survivors
- **the Jul–Aug bulk-pass sweep: the surfaces are already owned** — fingerprint scans for the window's known pass outputs (frontmatter remnants, malformed badges, heading skips, blank-line artifacts, link rewrites) came back clean or naive-scanner false positives: gates 1/4/6b already own every surface those passes touched, and 'read--time' badges are valid shields escaping (a dash literal), not truncation; the one real find was a **title-only cheat sheet** (30.2.2.20 distributed counter — sheet added, content generation failed, the last survivor of the 2535a0b4 generator-gap family), populated from the chapter's own tiers and flush rules; meta exemption noted: README.md's empty sheet is a deliberate placeholder
- **sheet-forensics epilogue: the generator-gap family closed at every level** — a corpus-wide sheet sweep (rule 4, gate 6b: first fence must hold ≥5 content lines) surfaced 12 more survivors the empty-fence rule could not see, splitting into two sub-classes: **9 truncated sheets** in the case studies (ticket-booking anatomy: title bar + `COMMON PATTERNS:` then close — the failure table spilled, tips orphaned in the tail fence; same stray-pair family, minus the empty pair, so fence grammar alone is blind to it) and **3 pure stubs** in the 70.2 toolkit (title bar only). All 9 repaired with the established surgery, all 3 populated from their chapters' own patterns; the rule's first cut fired 13 false positives on legitimate small supplementary fences — calibrated to only the sheet's first fence, which is the honest contract
- **the reference-integrity sweep: 53 dead prose paths repaired, and the nav fixer corrected itself twice** — extending the navigation probe to *every* markdown link showed the other generated surfaces (INDEX tables, badges) do not carry the slug artifact, but it exposed two deeper things. First, my own fixer was wrong twice: its title-suffix stripper was greedy enough to truncate real titles (`The Twelve-Factor App` → `The Twelve`), which **masked 28 label defects** by making the identity comparison fail, and it handled only the dominant footer style — extending `human_title` to derive allowed suffixes from the file's own path, and the label scanner to the rarer `Next: [Label](…)` form, found those 28 and the last one hiding in the other style. Second, the lane study docs (80.13, 80.29) told the reader to open files from **three numbering generations** — `software-developer-bible/16-Testing/01-Overview.md`, then `30.2-system-design/13-Rate-Limiter.md` before the case studies moved under `02-case-studies/`, then `70.2.01-sliding-window.md` — 53 dead references that no link gate could see, because prose paths are not links. Every one now resolves (resolver matched slug tokens against the live tree; 7 needed judgment, e.g. `70.3.03-nestjs-cheatsheet.md` → the backend cheat sheet), and gate 4 enforces the rule from now on — calibrated over three rounds (123 → 92 → 0) because a design doc's planned folders and a reader's own project layout (`scripts/checks/…mjs`, `.github/workflows/…`) are illustrations, not defects. The one glued metadata name in the corpus (`section: CheatSheets` in 8 files) is now `Cheat Sheets`, badges re-encoded as `%20`, and the nav label followed via the gate
- **the navigation-surface sweep: 74 files repaired, and the generator's own lesson applied** — scanning prose for hand-written defects found almost none (jargon-free prose is clean), but the *generated* navigation footers carried a whole class nothing watched: one slug-humanizing pass had title-cased acronyms and brand names into wrong fixed casing (`Mvcc`, `Cqrs Di`, `Sli Slo Sla`, `Cap Theorem`, `Iac Fundamentals`, `Rabbitmq`, `Webrtc Peer To Peer`, `Typescript Cheat Sheet` — 57 tokens, 45 files) and left **55 labels as raw relative paths** (`[Next: ../03 Transactions And Replication/index →](…)`) — they resolve, so no link gate fired, but the reader is handed a filesystem path where a title belongs. Both are uniform-and-wrong signatures of that one generator, the same family as the collapsed cheat sheets; the sweep's own first probe *lied* (an inverted `in_fence` predicate scanned fence content instead of prose, reporting 210 'duplicated words' that were all Tailwind classes and `[object Object]`), and re-measuring prose correctly found zero duplicated words. New gate 21 (`fix_nav_labels.py`, check + fix in one tool like `fix_box_width.py`): rule 1 canonical casing, rule 2 **derives** the replacement label from the target file's own H1 (numbering and parent/genre suffix stripped) rather than inventing one, so labels cannot drift from their targets. then the follow-up probe found the family's largest member: **132 labels were the target's title with punctuation and case flattened** (`Useeffect`, `Usesyncexternalstore`, `Bff`, `Statefulsets Daemonsets`, `Tanstack Form`, `Socket Io`, `Async Await`, `SLI SLO SLA`) — rule 3, with a deliberately tight signature (identity once non-alphanumerics are dropped and case folded) so that *shortening* a title (`Fiber` for `React Fiber`) stays an editorial choice, not a defect; the same H1 derivation repairs them. 125 files repaired, three rules pinned by two-sided plants — **19 gates now proven both ways**
- **the scope-floor sweep: the checker side of the false-green family, closed** — the writer audit asked "what if a writer edits what its checker calls clean?"; the same question one level down is "what if a checker scans nothing?" — and the answer was measured by running every checker against an empty tree: **15 of 19 exited 0**, printing the same compliance sentence they print every day (`OK — 0 links checked`, `template compliance OK`, `0 file(s) with misaligned boxes/tables`, `every answer >= 25 prose words` over zero banks). Two more (`check_counts`, `check_verify_wiring`) failed only by traceback — not an honest failure either, and in check_counts' case the *traceback* turned out to be what the suite's own gate-1 plant had been passing on all along, not the drifted badge. Probing further found four vacuous passes behind the first fifteen: `check_first_principles --diff` (0 stacks → "no regressions"), `read_time --check` ("consistent across 0 INDEX files"), `link_baseline` (0 citations → every baseline URL reported REMOVED, exit 0) and `check_fixpoint` — the gate added earlier the same session, since an empty copy is a fixed point of *everything*. All 19 now assert their own reach through one owner (`scan_scope.guard`, mirroring `md_fences` for fences and `prose_scan` for prose), and gate 23 proves the property for all of them at once: copy the scripts into an empty tree, run each gate, require **exit 1 _and_ `SCOPE ERROR` on stdout** (both halves — a crash also exits 1, and a crash is what hides a broken walk behind noise). The gate list is *derived* from `verify.sh` via check_verify_wiring's parser, so a new gate must carry a floor or be named in `EXEMPT` with a reason. Writing the gate found its own two bugs by being run: it recursed into itself (the sandbox still contains verify.sh, so a nested run never ended — a hang, not a failure), and with the recursion closed its own list floor (`MIN_GATES`) keeps a broken parse from "proving" the property for one script. The suite self-test gained the matching two-sided plant (20 synthetic gates, one of which lies) — **23 gates now proven both ways**, suite at **26 gates**
- **the writer audit: the suite's own blind spot, gated** — the nav fixer's two bugs were both *scope* errors (over-greedy stripping, a single footer style), which raised the question the rest of the suite structurally cannot answer: **what if a writer edits files its checker calls clean?** Then no gate can ever flag the edit — the change is invisible by construction, because the only tool that would see it is the one that made it. The audit tested the property directly: run every writer over a copy of the corpus and diff. Two live instances, both real: `fix_code_whitespace.py --trailing-ws` stripped trailing whitespace inside *layout* fences (`text`, `csv`, `tsv`, `anki`, `diff`, `mermaid`) while `check_code_whitespace.py` deliberately exempts them — 'any layout IS content', and in a csv/anki fence a trailing tab is an empty *field* — so it was quietly rewriting a box diagram it must not touch; and `fix_fence_labels.py`, which nothing invokes, proposed relabeling four mixed cheat-sheet fences `text` → `typescript`, which would have rendered their title bars and tips prose as broken code (the collapse arc's genre, in a loaded gun). Both scopes fixed, both boundaries pinned in `test_fixers.py`, and the property itself is now **gate 22** (`check_fixpoint.py`): every writer, a corpus copy, zero byte differences allowed. Also worth recording: the first fixed-point run found the corpus was *already* a fixed point of the seven wired writers — the two findings sat in the unwired and flag-asymmetric corners, which is exactly where a self-audit should expect to find them
- **the probe-clean sweep: four measured dimensions, kept as exemptions** — the sheet arc's forensic method (assume a past bulk pass minted a uniform-wrong signature, then scan for it) was turned on the remaining unmeasured surfaces, and the honest outcome was four *negative* results, each now recorded so a future pass doesn't 'fix' a deliberate convention: **fence labels** — the 235 unlabeled fences are diagram/output genres, and the 84 'mislabeled' hits were heuristic naivety (TypeScript containing `Result<` reads as rust, `interface X { ... }` with `"key":` reads as json) — a language-ID heuristic is not a defensible gate; **prose-only chapter sections** — `Why It Matters` holds (n=229, median 81, one sub-floor at 22 words), while `Real-World Use Cases` (184 zero-prose of 340) and `Common Mistakes` (283 of 407) are the same H3-title-plus-annotated-code genre already exempt for Best Practices, and `Summary`-as-decision-table is legitimate compression — no fix-arc for 467 sections; **prose version claims** — only 2 currency-framed mentions corpus-wide, both correct historical facts (Postgres 11+ lazy default backfill, Java 8+ default methods), so version drift is not a class (the freshness gate's EOL tables own the code side); **empty sections** — zero truly empty H2/H3 sections once my scanner's nesting artifact was calibrated out (an H2 immediately followed by its own H3 is normal), and gate 6b already owns the rule. The one residue the sweep did find came from the archaeology prediction itself: a **paste-artifact heading pair** (`## Example Answer Format` immediately followed by `### Example Answer Format` in the security drills bank — a promotion pass that added the H2 and left the H3) plus a duplicated list number in `20-backend/INDEX.md`; both fixed, and gate 3 gained a narrow adjacent-duplicate-heading rule (blank-lines-between only, so the legitimate same-label-under-a-different-parent case is untouched) with a two-sided plant — **16 gates now proven both ways**

On top of that sit 2379 probe-verified external links and 16 freshness rules across two date-gated
data tables — plus 27 CI-enforced gates whose harness audits its own wiring, whose markdown
parsing has a single fence owner, and whose detection is itself plant-tested every run. Every
count a reader can see is recomputed from disk; every product pin ages forward against a date
table. Everything here landed as reviewed commits on `main`.

## Cheat Sheet

```bash
bash scripts/verify.sh                    # all 27 gates; exit 1 blocks push
# Restamp order matters when several drift: read_time → gen_master_index →
# check_counts (it copies the generated JSON totals into the api-contract).
python3 scripts/read_time.py --write      # restamp read-time badges
python3 scripts/gen_master_index.py       # regen search + api/index.json
python3 scripts/check_counts.py --write   # restamp every owned count
python3 scripts/check_freshness.py        # the 14 staleness rules standalone
python3 scripts/link_baseline.py --update # after probe-verifying new URLs
```

## See Also

- [Verification Gates](verification-gates.md) — the gate map this report summarizes
- [Contributing](../contributing.md) — repo conventions and the verify workflow
- [Residential Verification Checklist](residential-verification-checklist.md) — human-browser verification
- [Modernization Changelog 1](2026-09-10-modernization-changelog.md), [Dead-Link Remediation Report](2026-09-11-dead-link-remediation-report.md), [Modernization Changelog 2](2026-09-14-modernization-changelog-2.md) — the passes whose findings this report builds on
- [Reference Coverage Audit](reference-coverage-audit.md) — the video-reference gap analysis (2026-09-16)

## References

- [Docker Docs — version and name top-level elements](https://docs.docker.com/reference/compose-file/version-and-name/)
- [endoflife.date — Go](https://endoflife.date/go)
- [endoflife.date — Rust](https://endoflife.date/rust)
- [Microsoft App Center retirement](https://learn.microsoft.com/en-us/appcenter/retirement)
- [Istio 1.24 release notes](https://istio.io/latest/news/releases/1.24.x/announcing-1.24/)
