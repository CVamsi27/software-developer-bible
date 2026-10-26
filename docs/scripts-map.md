<!-- section: Reference | category: Tooling | tags: scripts, gates, verification, restampers -->
[![Section](https://img.shields.io/badge/section-Reference-blue)](#)
[![Category](https://img.shields.io/badge/category-Tooling-orange)](#)
[![Tags](https://img.shields.io/badge/tags-scripts,%20gates,%20verification,%20restampers-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-8_min-informational)](#)

# Scripts Map — what runs, what owns what, what to reach for

`roadmap-return.test.cjs` exercises safe dated return links and chapter/revision context; it runs with the JavaScript checks in `verify.sh`.

> The main verification and maintenance scripts, arranged by the job they do inside the 31-gate
> verification suite: the gate that runs it, what it owns exclusively, the
> fixer or restamper to reach for when it fails, and the doctrine that keeps
> one concern from growing a second implementation. Gate numbers refer to
> `bash scripts/verify.sh` (labels appear in gate order in that file).

## First Principles

- **A script exists to prevent a named defect.** Checkers here cover concrete
  failure classes such as count drift, bank over-promising, invisible
  sub-stacks and fence desynchronization. Before adding one, name the defect
  it detects and the behavior that proves it catches that defect.
- **One owner per concern.** Counts are restamped only by
  `check_counts.py --write`, fence state is parsed only by `md_fences.py`,
  the gate count lives only in `check_verify_wiring.py`'s computation. Two
  implementations of one concern *will* disagree eventually; the disagreement
  is the bug.
- **A checker that can fix should also explain.** Repair writers listed by
  `check_fixpoint.py` must leave a clean corpus unchanged. `test_fixers.py`
  pins representative repair output byte-for-byte, so an incorrect repair
  fails verification instead of silently corrupting the corpus.

## Definition

- **Gates** are read-only checks — they fail a build; they never write.
- **Repair writers** rewrite files to correct detected defects. The repeatable
  repair and restamp tools listed by `check_fixpoint.py` must be idempotent;
  one-shot authoring helpers such as `insert_section.py` have a different
  contract and are not run as corpus-wide repair passes.
- **Restampers** recompute *owned claims* from disk (badges, counts,
  read-times, search index). Running a restamper is how a "drifted" failure
  becomes green — legitimately, because the claim's owner recomputed it.
- **Generators** produce files whose content is fully derived (search page,
  metadata digests); `--check` mode makes the generator double as a gate.

## How It Works

### The 31 gates, in verify.sh order

| # | Script | What it owns | Fails when |
| --- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| 1 | `check_counts.py` | Every count claim on the nav surface (badges, blurb counts, table Files columns, repo-scale totals, [api-contract](api-contract.md)) | a claim disagrees with live disk |
| 2 | `check_alignment.py` | Table pipe alignment, surrounding blank lines + ASCII box walls | rows/pipes misaligned or a table boundary fails to render |
| 3 | `check_structure.py` | IDs unique, sequences contiguous, banks last, one H1, unique H2 slugs, **INDEX completeness** (every numbered subdir with an INDEX is linked) | structure or navigation has a gap |
| 4 | `check_links.py` | Source Markdown links, anchors, visible path labels and unambiguous prose code paths resolve (fence-aware; generated `_site/` output and vendored `vendor/` dependencies are excluded) | a link is broken or presents a path that no longer exists |
| 5 | `check_freshness.py` | Known stale API signatures and date-gated EOL tables | a known stale signature appears |
| 6 | `link_baseline.py` (diff) | Every cited external URL is in the probe-verified baseline | an unverified URL is cited |
| 6b | `check_template.py` | Template sections/order, metadata contract, empty sections, question-claim contract, 25-question floor, fence grammar | a chapter or bank violates the contract |
| 7 | `check_private_refs.py` | No references back into the private workspace (retired in-repo path, private-repo links; dated records exempt) | a public doc points back at private campaign material |
| 8 | `check_code_whitespace.py` | Trailing WS + paste-shift bases inside fenced code | code hygiene regresses |
| 8b | `fix_box_code_indent.py --check` | Code embedded in box walls keeps indentation | box code renders flat |
| 8c | `fix_box_width.py --check` | Boxes stay within screen width | a box wraps on laptop screens |
| 9 | `check_first_principles.py --diff` | First-Principles coverage must not regress | coverage drops below baseline |
| 10 | `check_cross_refs.py` | `→ N.N.N` refs resolve to real files | a ref points nowhere |
| 11 | `check_duplication.py --strict` | No chapter teaches another chapter's prose | near-duplicate sections appear |
| 12 | `check_topic_twins.py` | Twin chapters cross-link both ways | twins stop linking |
| 13 | `read_time.py --check` | Declared study/read times equal computed estimates | times drift from word counts |
| 14 | `gen_master_index.py --check` | search.html + api/index.json byte-identical to corpus | generated files stale |
| 15 | `check_verify_wiring.py` | The harness itself: failure branches, gate count in 3 files, CI enforcement, trigger paths | the harness stops listening |
| 16 | `test_md_fences.py` | The fence owner's semantics (16 characterization cases) | `md_fences.walk` drifts |
| 17 | `test_fixers.py` | The fixers' repair output (7 planted-defect round trips, byte-exact) | a fixer repairs wrongly |
| 18 | `test_gates.py`, `test_read_time.py` | **The suite self-test** — each sandboxable gate's canonical defect must fire, clean content must pass, and generated study-time text must use correct singular/plural grammar | gate detection drifts or an index says `1 files` |
| 19 | `check_answer_depth.py` | Interview answers AND chapter Definitions carry ≥25 prose words (fence- and table-aware); H3-title-plus-code genres deliberately exempt | an answer is table-only or one-line prose; a Definition is a bare table |
| 20 | `test_prose_scan.py` | The prose scanner's classification contract (11 characterization cases) | `prose_scan` starts counting tables/fences or drops exclusions |
| 21 | `fix_nav_labels.py --check` | Previous/Next nav labels are canonically-cased human titles, not paths | a label is a raw path or a slug-humanized acronym (`Mvcc`, `Cicd`) |
| 22 | `check_fixpoint.py` | A clean corpus is a byte-for-byte no-op for every repair/restamp writer | a writer edits what its checker calls clean (an edit no gate can flag) |
| 23 | `check_scope_floor.py` | Every corpus gate exits 1 with a SCOPE ERROR on an empty tree (list derived from verify.sh) | a gate reports compliance while scanning nothing |
| 24 | `prose_hygiene.py` | Spelling convention (10 measured pairs), glued ATX headings, GFM table cell counts, empty-filler register (rule 4 check-only) | a minority spelling, a heading that renders as literal text, a table row with a broken cell grid |
| 25 | `check_dilution.py` | A chapter must not restate itself — ceiling baseline over the measured 0/0 state (within-chapter, sentence granularity; gate 11 owns cross-chapter) | a paragraph restated 20+ lines apart exceeds the baseline |
| 26 | `check_code_dup.py` | A chapter must not re-teach another chapter's code — cross-file fenced-block pairs (identical token streams ≥ 10 lines; near ≥ 0.85) against a ceiling baseline of classified keeps | an example duplicated from a sibling chapter exceeds the baseline |
| 27 | `check_see_also.py` | See Also hygiene — per-stack bare ceilings, label echoes, clipped endings and copied heading/table fragments; uses the shared fence reader | a new bare entry, label echo or unfinished description |
| 28 | `check_readability.py` | The outline names the mechanism: no retired generic heading (`How It Works`, `Explanation`, `Overview`, …) and no numbered mechanism step left under one, in learning chapters (`--write` removes the label and promotes its `### N.` children to `##`, preserving every heading text so anchors survive) | a chapter files its argument under a generic label |
| — | `scan_scope.py` | The scope floor itself: one owner for "a checker that finds nothing must not pass" (imported by every corpus gate) | — |

### The checker → fixer → restamper recipes

When a gate fails, identify the reported defect and use its matching repair. Metadata placement, category and tag errors need an authored correction; the read-time writer only computes read times. Never hand-edit an owned count:

| Failure | Reach for |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Gate 1 count drift | `python3 scripts/check_counts.py --write` |
| Gate 2 misaligned tables/boxes | `python3 scripts/check_alignment.py --fix` |
| Gate 6b metadata drift | `python3 scripts/read_time.py --write` after fixing placement |
| Gate 13/14 study-time / search drift | `python3 scripts/read_time.py --write` → `python3 scripts/gen_master_index.py` → `python3 scripts/check_counts.py --write` (this order; earlier steps change what later steps read) |
| Gate 28 generic section label | `python3 scripts/check_readability.py --write` (mechanical: promotes the umbrella's own children, touches no prose) |
| Gate 8/8b/8c hygiene | `python3 scripts/fix_code_whitespace.py --trailing-ws --paste-shift` / `fix_box_code_indent.py --fix` / `fix_box_width.py --fix` then `check_alignment.py --fix` |
| Gate 6 new external URL | probe-verify in a browser, then `python3 scripts/link_baseline.py --update`, commit the JSON with the doc |
| Gate 12 missing twin links | `python3 scripts/link_topic_twins.py` (dry-run first) |
| Gate 15 wiring broken | fix by hand — that is the point; `--write` only restamps counts |
| Gate 16/17 test failure | fix the module under test (or deliberately re-pin with a probe run + commit note) |

### Scripts that serve specific workflows (not gates)

| Script | Job |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `backfill_metadata.py` | Backfills the metadata block the template gate requires (historical import) |
| `check_study_live.py` | Post-deploy contract probe of the private study host — gating, canonicalization, the public surface, sign-in, denial, freshness; run by `study-live.yml`, pinned offline by `test_study_live.py` |
| `test_study_live.py` | Characterization tests for the live probe against stub hosts (19 cases) — the hermetic job that must pass before the live probe judges a deployment |
| `test_rendered_headings.py` | Checks the Minima page and post layouts keep one article H1; runs unit fixtures and scans the built site in `site-build.yml` |
| `fix_depth.py` | Rewrites relative md links after files move deeper/shallower |
| `fix_fence_labels.py` | Relabels fences mislabeled as `text`/`plain`/`output`/`console` |
| `fix_section_order.py` | One-off canonical section reorder (normalizer) |
| `insert_section.py` | Inserts a `## Definition`-style section at its canonical slot |
| `relink.py` | Bulk-rewrites links whose target basename changed (rename companion) |
| `tldr_digest.py` | Prints an authoring digest for chapters the template gate flags |
| `gen_master_index.py` | Generates search.html + api/index.json (`--check` = gate 14) |
| `senior_coverage.py` | Inventories current Markdown by genre and binds semantic review records to exact source hashes; `--require-complete` fails on pending/stale records instead of treating structural checks as an accuracy review |
| `drift_drill.py` | Quarterly re-probe of the 31 known staleness classes (advisory, opens tracking issues) |
| `job_board_watch.py` | Weekly JD watch (advisory workflow) |
| `md_fences.py` | The single fence parser — imported by ten scripts; pinned by gate 16 |
| `prose_scan.py` | The single reasoning-prose classifier (fence/table/heading/quote/badge exclusions) — imported by gate 19; pinned by gate 20. `read_time.py` deliberately keeps its own reading-weight model; the two classifiers answer different questions |
| `test_md_fences.py` / `test_fixers.py` / `test_gates.py` / `test_read_time.py` | The tooling's own test suites (gates 16/17/18) |
| `external-links-baseline.json` / `first-principles-baseline.json` | Owned data tables: probe-verified URLs; coverage floor |

### Rendered-page checks

The optional Playwright suites exercise the built site served at `http://127.0.0.1:4337`:

- `test_reading_ui_browser.cjs` checks chapter width, theme behavior, contrast and reader controls.
- `test_read_aloud_browser.cjs` checks speech extraction and playback; set `STUDY_TEST_URL` to a built chapter.
- `test_reading_pages_browser.cjs` checks navigation routes, one visible title, separate mobile touch targets, pointer/keyboard menus, expanded state/focus, local overflow, homepage/table/hover contrast and clipboard text.
- `test_rendered_headings.py` checks that a rendered Markdown H1 suppresses Minima's generated title across page and post layouts, including the built README.

Run these with `@playwright/test` and its Chromium browser available to Node. On a case-insensitive preview filesystem, `INDEX.html` and `index.html` collide. Render the authored homepage output to a temporary preview alias and set `STUDY_HOME_ROUTE` to that alias for the navigation suite; the production routes stay unchanged. A successful static build does not replace these browser checks.

### Doctrine: adding a script

1. Name the defect it prevents in its docstring — with the date and the
   incident.
2. Reuse `md_fences.walk()` for any fence-state need; never write a toggle.
3. If it recomputes a claim, make it the **only** writer of that claim and
   add `--write`; gate mode and write mode share one computation.
4. If it fixes, prove idempotence and pin its output in `test_fixers.py`.
5. Wire it: a gate row in `verify.sh` (failure branch sets `FAIL=1`),
   a `paths:` trigger, and a row in `docs/verification-gates.md` —
   `check_verify_wiring.py` enforces all three.

## Real-world Application

Any doc corpus or codebase with generated claims hits this wall: prose says
one number, reality another, and nobody can tell which is stale. The map's
value is the *routing*: a contributor who sees "FAIL" knows within one table
row whether to hand-fix, run a fixer, or restamp an owned claim — and knows
which failures are always hand-fix by design.

## Common Mistakes

| Mistake | Why it bites | Instead |
| ---------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------ |
| Hand-editing an owned count | The restamper will overwrite you — or worse, the gates will disagree | Run the owner's `--write` |
| Restamping in the wrong order | read_time → gen_master_index → check_counts, each reads the previous | Follow the recipe table |
| A second fence toggle | Desyncs on nested fences; corrupts whole files downstream | Import `md_fences.walk` |
| Copying gate logic into a fixer | The two drift apart; the fixer "fixes" things the gate then rejects | Shared module, shared thresholds |
| Treating `is_fence_line` as "line matched the regex" | Nested-fence content lines match too | Trust the pinned tests; read gate 16 |
| Adding a gate without wiring | Gate 15 fails: unwired gates are green in CI by definition | Follow doctrine step 5 |

## Best Practices

- Run `bash scripts/verify.sh` before every commit; capture the exit code,
  not the vibe.
- When a restamper changes files you did not expect, read the diff before
  staging — restampers own *claims*, not your prose.
- Keep the baseline JSONs append-only in review; their diffs are an audit
  trail of every new external citation and coverage change.

## Summary

The scripts form three legible layers — **gates** that judge, **fixers** that
repair, **restampers/generators** that recompute owned claims — with one
owner per concern and test suites pinning the two layers most able to do
silent damage. When something fails, the recipe table routes you to the one
correct tool; when you add a tool, the doctrine tells you what wiring makes
it real.

## See Also

- [Verification Gates](verification-gates.md) — the narrative
  history and full contract of every gate row.
- [Gate Design Principles](gate-design-principles.md) — why the suite is
  shaped the way it is: the constraints, the method, and the layer table.
- [Corpus Health Report](2026-09-19-corpus-health-report.md) — the ledger of clean sweeps and boundary findings
  ledger this map summarizes; every defect named here is documented there.
- [Contributing](../contributing.md) — repo conventions the gates enforce.

## References

- `scripts/verify.sh` — the executable table of contents for this map.
- `scripts/test_fixers.py` / `scripts/test_md_fences.py` — the recorded
  contracts of the fixers and the fence parser.
- `scripts/test_read_time.py` — regression checks for singular/plural file
  counts in generated study-time lines.
