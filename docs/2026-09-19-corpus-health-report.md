<!-- section: Meta | category: Reference | tags: health-report, verification-gates, session-retrospective -->
[![Section](https://img.shields.io/badge/section-Meta-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-800080)](#)
[![Tags](https://img.shields.io/badge/tags-health--report,%20verification--gates,%20session--retrospective-lightgrey)](#)

> **Dated review record:** test results and remaining-work statements below describe the recorded pass. Repo-scale and freshness-rule counts are restamped by the current count tool rather than preserved historical totals. Use the [current review progress](2026-10-25-fullstack-coverage-review.md) and [verification runbook](verification-gates.md) for present scope; chapter existence and passing scans do not establish complete reader review.

# Corpus Health Report — September 2026

> A multi-commit hardening session (see `git log` for the running total),
> organized around one recurring method: **measure first, fix what the
> measurement proves, then gate the class so it cannot regress.**
>
> This report is the ledger — what each gate enforces, which rules caught real
> defects on their first run, which sweeps came back clean, and what remains
> unexamined.

## Definition

- **Drift class** — a category of defect that recurs structurally (for example,
  "claims outrun content" or "newer chapters current, older siblings stale").
- **Owned claim** — a number in docs and `INDEX.md` files that a script
  restamps from the same computation it checks (`--write`); an unowned claim
  is a drift waiting to happen.
- **Date-gated data table** — a freshness-gate table keyed on *dates*, not
  banned strings: an entry starts failing the day reality changes, with no
  rule edit needed.
- **Day-one catch** — a gate rule that found a real corpus defect on its very
  first baseline run, before any planted test.

## First Principles

1. **A doc is a claim about the world; gates are how claims stay true.**
   Every drift found this session was a claim (a count, a promise, a pin, a
   version) whose referent moved. The fix is never "edit the number" — it is
   "give the number an owner that recomputes it."
2. **Sweeps decay; gates don't.** A manual sweep is true the day it runs and
   less true every day after, whereas converting a finding into a gate rule
   establishes a standing property.

   Classes a gate cannot own (singletons and context-dependent mentions) decay
   silently unless re-probed, which is what the quarterly **drift drill**
   (`scripts/drift_drill.py` + `.github/workflows/drift-drill.yml`) handles:
   20 STALE classes that open a tracking issue, 11 REVIEW classes listed for
   human judgment.
3. **The gate must be calibrated to reality, then proven both ways.** A rule
   that fires on the corpus as it stands buries signal; a rule never proven to
   fire may be dead code (one rule here was unreachable after `return`, and
   only the plant test exposed it).
4. **Drift concentrates where content was extended without revisiting
   siblings.** Four separate finds (Node pins, Actions pins, Istio
   `apiVersions`, and Compose keys) showed newer content current and older
   content stale *within the same stack*.

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
| 5 `check_freshness.py` | **46 rules**, incl. two date-gated EOL tables + Compose | +EOL-BASE-IMAGE, +EOL-GITHUB-ACTION, +OBSOLETE-COMPOSE-VERSION |
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
- **answer-quality arc: 247 answers deepened across 11 banks** — the question-count floor passed banks holding flashcard bullets and code-only answers; a fence-aware, label-agnostic depth scan found TypeScript (29), security (36), NestJS (32), microservices (27), Node.js (31), CI/CD (23), Kubernetes (19), Docker (14), REST (6), auth (5), and AI engineering (25). Each received a hand-authored senior-depth prose block (mechanism, trade-off, and failure mode), leaving zero answers under 40 words corpus-wide.
- **the probe that falsified the arc's own scanner: 27 table-only answers** — the first depth scan counted table words, so a comparison table plus one `**Answer:**` label line read as healthy. A prose-only re-scan (fences, tables, headings, quotes, and badges excluded) found Docker (10), Kubernetes (7), CI/CD (5), NestJS (2), REST (1), auth (1), and security (1); every one gained mechanism and trade-off prose, REST Q10 (pure code) was repaired, and zero answers sit under 25 prose words corpus-wide.
- **gate 19 `check_answer_depth.py`** — makes that property permanent: `>=25` fence- and table-aware prose words per answer, question headings require the digit (so `### Question Categories` never false-triggers), the suite relabeled `21 -> 22` gates cleanly, and the canonical plant is pinned two ways in the self-test (12/12).
- **rule 2, the chapter sweep: the same failure mode in study chapters** — a survey of 2,028 sections confirmed Best Practices and How It Works sections use an H3-title-plus-code genre (exempt by decision), while 9 chapter Definitions were table-only, diagram-only, or thin intros. All 9 gained definitional prose, and gate 19 rule 2 makes chapter Definitions `>= 25` prose words permanent (self-test 13/13).
- **the duplicate-example audit: 10 code blocks re-taught across sibling chapters, trimmed to pointers (2026-09-22)** — language-tagged fenced blocks tokenized cross-file (preserving strings) found 8 raw-identical blocks in 4 pairs out of 7,476 fenced blocks and 27 structural pairs `>= 20` lines.

  Ten real re-teaches were trimmed to canonical pointers (`useeffect.md`, `caching.md`, `apollo-client.md`, `scope.md`, `gc.md`, `closures.md`), while 17 were classified and kept (deliberate contrasts, interview-recap compilations, and Docita defense quotes). Gate 26 (`check_code_dup.py`) tracks that census against `identical: 2, near: 16`.
- **the See Also pilot: zero bare See Also entries corpus-wide (2026-09-23)** — across nine progressive pilots on the same day, every bare See Also entry across all study stacks, lanes, strategy, and docs gained a hand-authored reason connecting source chapter to target with zero echo defects:

  - Pilots 1–2 tightened `10.1-javascript` (92 entries) and `10.3-react` (120 entries).
  - Pilots 3–6 reasoned `20.6-microservices` (91), `20.2-nestjs` (68), `20.4-database` (57), and all of `40-platform` (379 total across Kubernetes and sibling stacks).
  - Pilots 7–9 finished `60-realtime` (29), `00-strategy` (8), `docs/` (5), `20.8`/`20.9`/`20.13`/`30.3`/`10.8` (31), `10.2-typescript` (87), `10.4-next.js` (85), and the remaining stacks (~750 entries), plus repairing 76 mispointed case-study footer targets and 7 placeholder `(#)` links. Gate 27's baseline is now `0` across every stack.

### Measured non-actions (the boundary findings)

- **39 interview banks, 741 pairs**: zero true cross-stack duplicates; similarity came from shared form (section skeleton and question framing).
- **00-strategy vs. lanes**: maximum shingle overlap `J=0.005`, confirming a clean ownership boundary.
- **Enzyme, `getServerSideProps`, Swarm, and `@babel/polyfill` mentions**: all teach migrating *away*; left alone.
- **Cloud staleness sweep (12 classes)**: Stackdriver, Amazon ES, CodeCommit, SDK v2, `get-login`, dead Lambda runtimes, EC2-Classic, GCE, `--generator`, `helm init`, `template_file`, and Ansible `include:` returned zero genuine hits.
- **JS ecosystem sweep (14 classes)**: CRA, `moment`, `node-sass`, `request`, `tslint`, `ReactDOM.render`, removed lifecycles, Vue 2, Bower, `CommonsChunkPlugin`, `yarn global`, `npm --save`, and webpack v4 shapes returned zero genuine hits. Two consecutive clean sweeps show the hunt saturating.
- **See Also reasons: 72% bare-entry class measured and not bulk-generated (2026-09-22)** — across 2,727 entries (1,958 bare across 438 files), 1,874 of 1,888 title-derivable entries collapsed into four boilerplate templates ("the X topic index", "derives X from first principles"). Rather than minting another boilerplate signature, entries were authored per link and progressive hygiene recorded under Common Mistakes in `gate-design-principles.md`.
- **Prose dilution, measured four ways and found absent (2026-09-22)** — across 776 chapter files, adjacent-sentence restatement (`Jaccard >= 0.34`), partial overlap (`0.20–0.34`), intra-chapter near-duplicate paragraphs (`>= 20` lines apart), and `TL;DR`-versus-Summary overlap (median `0.00`, max `<= 0.25`) all came back clean. Eighteen empty discourse openers remain gated as rule 4 of `prose_hygiene.py`, while `essentially` (10 uses) and `the fact that` (6 uses) stay excluded because all 16 do technical work.

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

At the close of this pass the corpus held 988 study chapters and 40 interview
banks, every one at or above the 25-question floor the gate enforced. After the
answer-quality arc (2026-11-14 review) and the table-only probe that falsified
its scanner, no answer and no chapter Definition fell under the 25-prose-word
floor gate 19 enforced — its rule 2 having measured and deliberately exempted
the H3-plus-code genres.

The sweeps below are the session's ledger, each one a fix-then-gate pair:

- **One scanner owner (`prose_scan.py` + gate 20):** reasoning-prose classification moved out of copy-pasted snippets into one module (following `md_fences`), consumed by gate 19 and pinned by gate 20; `read_time.py` keeps its separate reading-weight model.
- **Code-sample audit, first arc (24 collapsed cheat sheets repaired and gated):** scanning 7,844 fences showed 24 Cheat Sheets shared a stray close plus empty-open pair that spilled failure tables and code outside the blocks. All 24 were deterministically repaired, and gate 6b rule 3 now fails any empty fence (self-test 14/14).
- **Forensics on the collapse (`2535a0b4`):** commit history showed the 6-fence defect shipped on 2026-07-28 and survived 8 weeks of alignment and fence sweeps untouched; zero unclosed sheets remain across `0:92, 2:400, 4:16, 6:3`.
- **Jul–Aug bulk-pass sweep:** frontmatter, badge (`read--time`), and heading sweeps confirmed gates 1, 4, and 6b already own those surfaces; the sole title-only cheat sheet (`30.2.2.20` distributed counter) was populated, with `README.md`'s empty sheet kept exempt.
- **Sheet-forensics epilogue (rule 4, gate 6b):** requiring a Cheat Sheet's first fence to hold `>= 5` content lines caught 9 truncated case-study sheets and 3 stub sheets in `70.2`, all repaired and calibrated cleanly against supplementary small fences.
- **Reference-integrity sweep (53 dead prose paths repaired):** `human_title` gained path-aware suffix stripping (catching 28 masked label defects plus `Next: [Label](...)`), and 53 unlinked prose paths across three numbering generations in `80.13` and `80.29` were repaired and gated under gate 4 (plus `section: CheatSheets` -> `Cheat Sheets` across 8 files).
- **Navigation-surface sweep (74 + 125 files repaired, gate 21):** `fix_nav_labels.py` catches wrong-cased tokens (`Mvcc`, `Cqrs Di`, etc.), 55 raw path labels, and 132 flattened titles (`Useeffect`, `Bff`) by deriving replacements from each target file's H1 — bringing **19 gates** to two-way proof.
- **Scope-floor sweep (gate 23):** testing every gate against an empty tree saw 15 of 19 exit 0 silently; all 19 now guard discovery via `scan_scope.guard` (verified for `exit 1` and `SCOPE ERROR`, bringing **23 gates** to two-way proof and the suite to **26 gates**).
- **Writer audit (gate 22):** `check_fixpoint.py` runs every repair and restamp tool over a copy of the tree and requires zero byte diffs after catching layout-fence trailing-whitespace edits in `fix_code_whitespace.py` and mixed-fence relabeling proposals in `fix_fence_labels.py`.
- **Probe-clean sweep (four measured exemptions + gate 3 duplicate check):** unlabeled diagram fences (235), H3-plus-code sections (`Why It Matters`, `Real-World Use Cases`, `Common Mistakes`, tabular `Summary`), two historical version notes (Postgres 11+, Java 8+), and valid nested `##`/`###` sections remain exempt, while an adjacent-duplicate heading pair in the security drills bank and a duplicate number in `20-backend/INDEX.md` were fixed and gated (**16 gates** proven both ways at that checkpoint).

The historical citation checkpoint contained 2,379 probe-verified external links. The current tool-maintained count is 46 freshness rules across two date-gated
data tables — alongside the 29 CI-enforced gates listed above, whose harness audits its own wiring, whose Markdown parsing has a single fence owner, and whose detection is plant-tested every run. Every count a reader sees is recomputed from disk, every product pin ages against a date table, and everything landed as reviewed commits on `main`.

## Cheat Sheet

```bash
bash scripts/verify.sh                    # all 29 gates at this report's checkpoint; exit 1 blocks push
# Restamp order matters when several drift: read_time → gen_master_index →
# check_counts (it copies the generated JSON totals into the api-contract).
python3 scripts/read_time.py --write      # restamp read-time badges
python3 scripts/gen_master_index.py       # regen search + api/index.json
python3 scripts/check_counts.py --write   # restamp every owned count
python3 scripts/check_freshness.py        # the 35 staleness rules at this report's checkpoint
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
