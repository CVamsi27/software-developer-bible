<!-- section: Reference | category: Tooling | tags: scripts, gates, verification, restampers -->
[![Section](https://img.shields.io/badge/section-Reference-blue)](#)
[![Category](https://img.shields.io/badge/category-Tooling-orange)](#)
[![Tags](https://img.shields.io/badge/tags-scripts,%20gates,%20verification,%20restampers-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-8_min-informational)](#)

# Scripts Map — what runs, what owns what, what to reach for

> Every script in `scripts/`, arranged by the job it does inside the 21-gate
> verification suite: the gate that runs it, what it owns exclusively, the
> fixer or restamper to reach for when it fails, and the doctrine that keeps
> one concern from growing a second implementation. Gate numbers refer to
> `bash scripts/verify.sh` (labels appear in gate order in that file).

## First Principles

- **A script exists because a specific defect was real.** Every checker here
  was written after a defect actually shipped or was caught by hand — count
  drift, bank over-promising, invisible sub-stacks, fence desync. If you
  cannot name the defect a new script prevents, it does not belong yet.
- **One owner per concern.** Counts are restamped only by
  `check_counts.py --write`, fence state is parsed only by `md_fences.py`,
  the gate count lives only in `check_verify_wiring.py`'s computation. Two
  implementations of one concern *will* disagree eventually; the disagreement
  is the bug.
- **A checker that can fix should also explain**, and a fixer's output is a
  contract: pinned byte-for-byte by `test_fixers.py` (gate 17), so a fixer
  that starts repairing wrongly fails the suite instead of silently
  corrupting the corpus.

## Definition

- **Gates** are read-only checks — they fail a build; they never write.
- **Fixers** rewrite files; every fixer is idempotent and shares its
  detection logic with a gate (same parser, same thresholds).
- **Restampers** recompute *owned claims* from disk (badges, counts,
  read-times, search index). Running a restamper is how a "drifted" failure
  becomes green — legitimately, because the claim's owner recomputed it.
- **Generators** produce files whose content is fully derived (search page,
  metadata digests); `--check` mode makes the generator double as a gate.

## How It Works

### The 20 gates, in verify.sh order

| # | Script | What it owns | Fails when |
| --- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| 1 | `check_counts.py` | Every count claim on the nav surface (badges, blurb counts, table Files columns, repo-scale totals, [api-contract](api-contract.md)) | a claim disagrees with live disk |
| 2 | `check_alignment.py` | Table pipe alignment + ASCII box walls | rows/pipes misaligned vs widest cell |
| 3 | `check_structure.py` | IDs unique, sequences contiguous, banks last, one H1, unique H2 slugs, **INDEX completeness** (every numbered subdir with an INDEX is linked) | structure or navigation has a gap |
| 4 | `check_links.py` | Internal links resolve, no stale path-as-label links (fence-aware, anchor-verified) | a link is broken or lies about its target |
| 5 | `check_freshness.py` | 14 staleness rules incl. date-gated EOL tables | a known stale signature appears |
| 6 | `link_baseline.py` (diff) | Every cited external URL is in the probe-verified baseline | an unverified URL is cited |
| 6b | `check_template.py` | Template sections/order, metadata contract, empty sections, question-claim contract, 25-question floor, fence grammar | a chapter or bank violates the contract |
| 7 | `check_claims.py` | Campaign-material claims integrity (purged phrases stay purged) | a purged claim re-enters active docs |
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
| 18 | `test_gates.py` | **The suite self-test** — each sandboxable gate's canonical defect, planted in a temp tree, must still fire; clean content must still pass | a gate stops detecting its defect |

### The checker → fixer → restamper recipes

When a gate fails, run the tool it names — never hand-edit a claim it owns:

| Failure | Reach for |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Gate 1 count drift | `python3 scripts/check_counts.py --write` |
| Gate 2 misaligned tables/boxes | `python3 scripts/check_alignment.py --fix` |
| Gate 6b metadata drift | `python3 scripts/read_time.py --write` after fixing placement |
| Gate 13/14 study-time / search drift | `python3 scripts/read_time.py --write` → `python3 scripts/gen_master_index.py` → `python3 scripts/check_counts.py --write` (this order; earlier steps change what later steps read) |
| Gate 8/8b/8c hygiene | `python3 scripts/fix_code_whitespace.py --trailing-ws --paste-shift` / `fix_box_code_indent.py --fix` / `fix_box_width.py --fix` then `check_alignment.py --fix` |
| Gate 6 new external URL | probe-verify in a browser, then `python3 scripts/link_baseline.py --update`, commit the JSON with the doc |
| Gate 12 missing twin links | `python3 scripts/link_topic_twins.py` (dry-run first) |
| Gate 15 wiring broken | fix by hand — that is the point; `--write` only restamps counts |
| Gate 16/17 test failure | fix the module under test (or deliberately re-pin with a probe run + commit note) |

### Scripts that serve specific workflows (not gates)

| Script | Job |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `backfill_metadata.py` | Backfills the metadata block the template gate requires (historical import) |
| `fix_depth.py` | Rewrites relative md links after files move deeper/shallower |
| `fix_fence_labels.py` | Relabels fences mislabeled as `text`/`plain`/`output`/`console` |
| `fix_section_order.py` | One-off canonical section reorder (normalizer) |
| `insert_section.py` | Inserts a `## Definition`-style section at its canonical slot |
| `relink.py` | Bulk-rewrites links whose target basename changed (rename companion) |
| `tldr_digest.py` | Prints an authoring digest for chapters the template gate flags |
| `gen_master_index.py` | Generates search.html + api/index.json (`--check` = gate 14) |
| `drift_drill.py` | Quarterly re-probe of the 31 known staleness classes (advisory, opens tracking issues) |
| `job_board_watch.py` | Weekly JD watch (advisory workflow) |
| `md_fences.py` | The single fence parser — imported by ten scripts; pinned by gate 16 |
| `test_md_fences.py` / `test_fixers.py` / `test_gates.py` | The tooling's own test suites (gates 16/17/18) |
| `external-links-baseline.json` / `first-principles-baseline.json` | Owned data tables: probe-verified URLs; coverage floor |

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

## Cheat sheet

| You see... | You run... |
| ----------------------------------- | -------------------------------------------------------------------- |
| `COUNT DRIFT` | `python3 scripts/check_counts.py --write` |
| `misaligned boxes/tables` | `python3 scripts/check_alignment.py --fix` |
| `read_time drifted` | `python3 scripts/read_time.py --write` |
| `search.html drifted` | `python3 scripts/gen_master_index.py` |
| `de-indented lines found` | `python3 scripts/fix_box_code_indent.py --fix` |
| `over-padded boxes found` | `python3 scripts/fix_box_width.py --fix` then aligner |
| `trailing whitespace` / paste-shift | `python3 scripts/fix_code_whitespace.py --trailing-ws --paste-shift` |
| `unverified external URL` | browser-verify → `link_baseline.py --update` |
| `INDEX GAP` | add the missing link by hand (it is navigation, not a count) |
| `wiring: N problem(s)` | fix by hand — the harness must listen |
| any test gate red | fix the module, not the expectations |

## See Also

- [Verification Gates](verification-gates.md) — the narrative
  history and full contract of every gate row.
- [Gate Design Principles](gate-design-principles.md) — why the suite is
  shaped the way it is: the constraints, the method, and the layer table.
- [Corpus Health Report](2026-09-19-corpus-health-report.md) — the
  ledger this map summarizes; every defect named here is documented there.
- [Contributing](../contributing.md) — repo conventions the gates enforce.

## References

- `scripts/verify.sh` — the executable table of contents for this map.
- `scripts/test_fixers.py` / `scripts/test_md_fences.py` — the recorded
  contracts of the fixers and the fence parser.
