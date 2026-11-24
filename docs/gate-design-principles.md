<!-- section: Meta | category: Reference | tags: gate-design, verification, methodology, first-principles -->
[![Section](https://img.shields.io/badge/section-Meta-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-800080)](#)
[![Tags](https://img.shields.io/badge/tags-gate--design,%20verification,%20methodology,%20first--principles-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-9_min-informational)](#)

# Gate Design Principles — why the verification suite is shaped the way it is

> The [gate inventory](verification-gates.md) records *what* each
> of the current gates enforces; the [scripts map](scripts-map.md) records *how to
> route* around a failure. This doc records the *why*: six constraints of a
> hand-maintained corpus, the design each constraint forces, and the method —
> measure, fix, gate, prove both ways, write it down — that produced every
> rule in the suite. Nothing here was designed up front; each principle was
> earned by a defect.

## Definition

A verification gate checks a named condition and returns a failing result when the condition is violated. The build or release harness must propagate that result for the check to block anything.

**Textbook definition:** a verification gate is an acceptance predicate evaluated at a workflow boundary, with progression contingent on its result. Its assurance is limited by the predicate, inputs, and enforcement path.

- **Gate** — a read-only check that fails a build. Never writes.
- **Fixer** — rewrites files; idempotent; shares its detection logic with a
  gate so the two cannot disagree; its output is pinned byte-for-byte.
- **Restamper** — the single writer of an owned claim, recomputing it from
  the same data the gate reads.
- **Generator** — produces files whose content is fully derived; `--check`
  mode makes it double as a gate (byte-lock).
- **Owned claim** — a number whose truth is recomputed, not asserted.
- **Drift class** — a defect category that recurs structurally, and is
  therefore gateable.
- **Day-one catch** — a real defect a new rule found on its first baseline
  run, before any planted test. The ledger of these is the method's evidence.

## First Principles

1. **Prose has no compiler.** Invalid syntax or types may fail a build, whereas
   wrong behavior can compile cleanly and a document that lies can render
   perfectly. In a hand-maintained corpus, a count, an Application Programming
   Interface (API) signature, a path, or a guarantee can look plausible and
   still be wrong.

   The suite makes specific, repeatable properties explicit. Structural checks,
   semantic review, and live-source verification answer different questions and
   cannot substitute for one another; bounded local checks run routinely, while
   remote drift and judgment calls require separate evidence.

2. **A claim without an owner drifts.** A number quoted independently in three
   places becomes inconsistent as the corpus evolves. Two complementary
   controls stop this: give each claim a single *writer* that recomputes it from
   disk (a restamper with `--write`), or give it a constant *reader* that fails
   when reality disagrees (a gate). Hand-editing an owned claim re-introduces
   drift on a delay.

3. **A repeatable rule makes a check reusable.** A sweep is true the day it
   runs and less true every day after, whereas converting a finding into a gate
   checks that property on every subsequent run. The detector still needs
   regression controls and updated inputs, while singular or context-dependent
   classes stay in the scheduled drift drill. The corollary sets the boundary:
   *do not gate singletons*, because a one-off rule produces noise that trains
   contributors to ignore failures.

4. **A gate is only as blocking as its wiring.** Every gate script can exit 1
   correctly and still block nothing if the harness ignores it — the real
   false green here wrote a variable the summary never read, skipping four
   gates and exiting 0. Continuous Integration (CI) needs the same audit one
   level up, because a workflow step running under `set +e` and dropping its
   exit code is an invisible lie from the inside.

5. **Detection rots like content does.** A gate that stops firing after a
   refactor or cleanup stays green forever, and green alone never distinguishes
   "verified" from "never ran." Wiring checks prove a failure *can* reach the
   exit, not that detection *still works*.

   Gates therefore need gates: plant each canonical defect and require non-zero
   (fire side), run on clean content and require zero (clean side), and pin
   parsers and fixers with characterization suites. Because gates are
   calibrated against real corpus shape, planted defects must match that shape
   too.

6. **Calibrate to reality, then prove both ways.** A rule firing on the live
   corpus buries signal in baseline noise, while a rule never proven to fire
   may be dead code (one rule here was unreachable after a `return`, caught
   only by the plant). Both proofs are mandatory before trusting a rule, and the
   day-one ledger records empirically what rules find that manual passes miss.

## Why Do We Need It?

Every layer added here answered an observed failure: counts drifted by double
digits before the count guard existed, an interview bank promised 30 questions
and held 20, and a repair pass built on a naive fence toggle corrupted three
files. Ten scripts once carried separate fence parsers that desynced on nested
fences, the box fixer silently skipped whole files, a red build passed CI
through a wiring gap, and one rule was dead code until a plant proved it could
fire.

None of those failures were hypothetical. The suite has its current shape
because each check was forced by an incident recorded with dates in the
[health report](2026-09-19-corpus-health-report.md).

## How It Works

### The method loop

1. **Hunt** with a measurement calibrated against its own false positives
   first — a counter blind to `### 1.` headings, a grep blind to single
   quotes: each was fixed *before* its output was trusted.
2. **Verify every hit against the live world** before editing; honest
   history stays honest.
3. **Fix, biasing toward deepening** — finish the promise rather than shrink
   it.
4. **Gate the class** in the same session: an unfixed class re-accumulates;
   an ungated fix decays.
5. **Prove both ways** — fires on the plant, silent on the corpus, wired so
   the failure reaches the exit.
6. **Write it down** — gate row, script map entry, health-report ledger. A
   rule whose rationale lives only in a commit message will be misjudged by
   whoever reads it next.

### The layers, and what watches each

| Concern | Examples | Checks (labels can overlap) |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------ |
| Corpus claims and learning content | counts, links, structure, staleness, answer depth, spelling, repeated prose, topic links, and generated reading metadata | gates 1–14, 19, 24–27 |
| Harness and workflow wiring | failure propagation, gate inventory, CI enforcement, and trigger coverage | gate 15 |
| Shared parsers and repair tools | fence and prose parsing, planted gate defects, writer output, empty-scope behavior, and fixed points | gates 16–18, 20, 22–23 |
| Navigation and teaching flow | reachable chapters, readable previous and next labels, and related-reading guidance | gates 3–4, 21, 27 |

These rows group concerns rather than claiming complete coverage, and each gate
checks only its named property on its declared inputs. Parser, writer, and
harness tests exercise selected failure and control cases, so passing tests
still leave other behavior for review.

## Real-world Application

The method transfers to any corpus or codebase where generated or hand-kept
claims must stay true: API docs quoting counts, runbooks quoting endpoints, and
READMEs quoting versions.

Start by inventorying claims and sorting them into owned versus unowned,
convert unowned live-count claims to restampers first (cheapest, highest yield),
sweep defect classes only where a gate can catch regressions, and keep the
day-one ledger from the start to show the checks work.

## Common Mistakes

- **Mass-applying a derivation because the numbers look large.** The See
  Also surface measured 1958 bare entries (72%) — a big, uniform-looking class
  matching the shape of the nav-label and cheat-sheet defects. Yet drafting
  the derivation showed 1874 of 1888 derivable entries collapsed into four
  boilerplate templates ("the X topic index", "derives X from first
  principles") repeated hundreds of times each — a bare link with extra words
  and a new wrong signature minted by the fix itself.

  A reason phrase judges *why this link helps this reader here*; it can be
  assisted, checked for hygiene (resolves without echoing the label), and
  improved progressively, never mass-generated. That measured non-action and its
  numbers live in the health-report ledger.

| Mistake | Why it bites | Instead |
| ---------------------------------------------- | -------------------------------------------------------------------- | --------------------------- |
| Hand-editing an owned number | Reverted by the next restamp, or worse, gates and prose disagree | Run the owner's `--write` |
| A second implementation of one concern | The two drift; the disagreement is the bug | One owner, shared module |
| Banning strings instead of dates for EOL rules | Fires forever on not-yet-EOL pins, then goes stale itself | Date-gated data tables |
| Planting an unrealistic defect | Gates calibrated to corpus shape pass it silently — proof of nothing | Plant real corpus shape |
| Proving only the script, not the suite | The wiring gap class: red tool, green build | Prove the suite fails |
| Gating a singleton | Noise trains people to ignore red | Schedule a re-probe instead |
| Exemptions as folklore | Undocumented skips get "fixed" later, breaking real cases | Named, reasoned, in code |

## Best Practices

- Fix-then-gate in the same session; the fix without the gate decays, the
  gate without the fix buries signal on day one.
- Keep exemption lists *named and reasoned* inside the gate code, never in a
  side document that can drift.
- Review baseline JSON changes deliberately. A snapshot may legitimately remove an old citation or revise a scoped floor; Git history retains those changes. Never reset a baseline just to silence an unexplained failure.
- When a sweep comes back clean twice, stop sweeping and write the ledger —
  saturation is a result, not a failure.

## Summary

The suite combines corpus checks, parser and fixer tests, a harness auditor, and a drift drill. Its checks arose from observed defects and are tested with defect and clean controls covering named failure classes rather than every possible technical or editorial error.

The design fits in one sentence: **make the corpus a system whose lies are detectable, whose detection is wired, and whose wiring is itself tested** — then write down how, so the next maintainer inherits the reasoning and not just the rules.

## See Also

- [Verification Gates](verification-gates.md) — the complete gate inventory
  and each rule's contract.
- [Scripts Map](scripts-map.md) — every script, its gate, and the routing
  table for failures.
- [Corpus Health Report](2026-09-19-corpus-health-report.md) — the ledger of
  defects, catches, and fixes this design was derived from.

## References

- `scripts/verify.sh` — the suite as an executable artifact.
- `scripts/test_gates.py` — the self-test that proves detection still works.
- `scripts/check_verify_wiring.py` — the harness auditor (rules 1–10).
