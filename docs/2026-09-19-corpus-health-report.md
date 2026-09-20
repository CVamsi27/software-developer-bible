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

### Gate inventory after the session (21 gates, all CI-enforced)

| Gate | Enforces | Session change |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1 `check_counts.py` | Every count claim on the nav surface | +4 owned claims: gates-page walker scope, api-contract totals (sourced from the gate-14-locked JSON), freshness rule count, drill class counts |
| 2 `check_alignment.py` | Table alignment + header rows exist | — |
| 3 `check_structure.py` | Numbering, single-H1, dup-H2 slugs, **banks-last**, **INDEX completeness**, **doc reachability** | +banks-last rule with two documented exemptions; +INDEX-completeness (no invisible sub-stacks — caught the 60-realtime omission on first run) and orphan-doc reachability (BFS from entry points; born from the 7-of-10 docs/ orphan scan) |
| 4 `check_links.py` | Internal links + honest link labels | — |
| 5 `check_freshness.py` | **14 rules**, incl. two date-gated EOL tables + Compose | +EOL-BASE-IMAGE, +EOL-GITHUB-ACTION, +OBSOLETE-COMPOSE-VERSION |
| 6 `link_baseline.py` | Cited URLs probe-verified (2379) | +verified SRE/broker URLs |
| 6b `check_template.py` | Template, metadata, **question-count claims**, **bank floor**, **fence grammar** | +count-claim contract (claims read only from intro blockquote/TL;DR); +25-question floor with one named-format exemption; +closing-fence rule with full CommonMark nesting semantics |
| 7–15 | Claims, whitespace, first-principles, cross-refs, duplication, twins, read-time, search byte-lock, self-wiring | — (gate 15 enforced throughout) |
| 16 `test_md_fences.py` | The fence owner's semantics, pinned by 16 characterization tests | +gate born from writing the tests: `is_fence_line` flagged regex-matching content lines as delimiters (now true only on real open/close); `read_time` had been silently miscounting nested-fence content as reading text |
| 17 `test_fixers.py` | The fixers' repair output, pinned by planted-defect round trips (byte-exact, idempotent, no-mangle negative) | +closes the repair-wrongly failure mode the session demonstrated twice — corrupted repair pass, silently-skipping box fixer — by asserting each fixer's recorded contract in a temp-tree sandbox |
| 18 `test_gates.py` | **The suite self-test**: each sandboxable gate's canonical defect planted in a temp tree must still fire; clean content (incl. a real passing chapter) must still pass | +closes the last unwatched layer — detection itself; the two-sided design caught the wiring checker's check/write word-count asymmetry past twenty gates before landing |
| drift drill | 31 staleness classes, quarterly + issue-tracking | — |

### Day-one catch ledger

Five rules found real defects on their first baseline run — the empirical
argument for the whole method:

| Rule | Caught | Why the manual pass missed it |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
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
- fence parsing unified: ten scripts' naive `in_fence` toggles replaced by one `md_fences.walk` owner; the unified parser immediately found **20 over-padded boxes in 17 files** the desyncing old parser had silently skipped
- **new: 20.9-message-brokers stack** — 4 chapters + INDEX in the reserved-but-empty slot; brokers had 50+ example mentions corpus-wide but no canonical home; includes the Docita Anchor whose honest verdict is "zero brokers, deliberately" (the 20.9.01 when-not-to lesson shipped)
- **20.9 wired into 31 sites** — See Also links with per-site reason phrases from all 12 system-design case studies, the heavy broker-mention chapters, and both system-design INDEXes; the top INDEX's missing table row restored
- **docs layer made reachable** — 7 of 10 docs/ files were linked from nowhere; entry points repaired (README, health-report See Also, scripts map) and the property gate-enforced

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

The corpus is now 560 study chapters, 40 interview banks — every one at or
above the 25-question floor the gate now enforces — 2379 probe-verified
external links, 14 freshness rules across two date-gated data tables, and 21
CI-enforced gates whose harness audits its own wiring, whose markdown
parsing has a single fence owner, and whose detection itself is plant-tested
every run. Every count a reader can see is recomputed
from disk; every product pin ages forward against a date table. Everything
below lands as reviewed commits on `main`, nothing pushed.

## Cheat Sheet

```bash
bash scripts/verify.sh                    # all 21 gates; exit 1 blocks push
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
