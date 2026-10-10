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

1. **Prose has no compiler.** Invalid syntax or types may fail a build, but wrong behavior can still compile; a document that
   lies can render perfectly. In a hand-maintained corpus every claim — a count,
   a pin, a link, a promise — is unchecked by default, so verification must
   be made explicit. That is the entire justification for the suite's
   existence, and it is why gates are cheap stdlib scans that run on every
   push rather than expensive audits that run occasionally.

2. **A claim without an owner drifts.** Given one number quoted in three
   places and a corpus that changes daily, the number is already wrong; the
   only question is when anyone notices. Two complementary controls are: give the claim a single *writer* that recomputes it from
   disk (a restamper with `--write`), or give it a constant *reader* that
   fails when reality disagrees (a gate). Hand-editing an owned claim is not
   maintenance — it is re-introducing the drift on a delay.

3. **Manual sweeps decay; rules do not.** A sweep is true the day it runs
   and less true every day after. Converting a sweep's finding into a gate
   rule converts a point-in-time audit into a standing property. The residue
   — defect classes too singular or context-dependent to gate — decays back
   silently unless re-probed on a schedule, which is what the drift drill is
   for. The corollary sets the boundary: *do not gate singletons*. A rule
   needs a recurring class to guard; a rule for a one-off is noise that
   trains contributors to ignore failures.

4. **A gate is only as blocking as its wiring.** Every gate script can exit 1
   correctly and still be worth nothing if the harness never listens — the
   real false green here was a failure branch writing a variable the summary
   never read, skipping four gates and exiting 0. So the harness needs a gate
   of its own, and in CI the same audit applies one level up: a workflow step
   that runs a gate under `set +e` and drops the status is the same lie,
   again invisible from the inside.

5. **Detection rots like content does.** A gate that stops firing — after a
   refactor, a rename, an over-eager cleanup — stays green forever, and
   nothing about green distinguishes "verified" from "never ran." Wiring
   checks cannot see this; they prove a failure *can* reach the exit, not
   that detection *still works*. Gates therefore need gates: plant each
   canonical defect and require non-zero (fire side), run on clean content
   and require zero (clean side), and pin the tooling's own parsers and
   fixers with characterization suites. An unrealistic plant that "passes"
   proves nothing — the gates are calibrated against real corpus shape, and
   the plants must be too.

6. **Calibrate to reality, then prove both ways.** A rule that fires on the
   corpus as it stands buries signal in baseline noise; a rule never proven
   to fire may be dead code (one rule here was — unreachable after a
   `return`, caught only by the plant). Both proofs are mandatory before a
   rule is trusted, and the honest record of what a rule caught on its first
   baseline run — the day-one ledger — is the empirical argument that the
   method finds what manual passes miss.

## Why Do We Need It?

Because every layer added here answered a failure that actually happened:
counts drifted by double digits before the count guard existed; a bank
promised 30 questions and held 20; a repair pass built on a naive fence
toggle corrupted three files; ten scripts each carried a fence parser that
desynced on nested fences; the box fixer silently skipped whole files; a red
build passed CI through a wiring gap; a rule was dead code until a plant
proved it could fire. None of these were hypothetical. The suite is the
shape it is because each shape was forced by an incident — and the incidents
are all recorded, with dates, in the [health report](2026-09-19-corpus-health-report.md).

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

| Layer | Watches | Watched by |
| --------------- | ----------------------------------------------------------- | ----------- |
| Corpus content | counts, links, structure, claims, staleness | gates 1–14 |
| Harness | failure branches, gate count, CI enforcement, trigger paths | gate 15 |
| Tooling parsers | fence semantics, gate detection, fixer output | gates 16–18 |
| Navigation | sub-stacks, chapters, docs — nothing invisible | gates 3, 15 |

The design property this table encodes: **every layer that can be wrong has
something that watches it**, and the watchers are themselves watched — down
to the self-test that re-proves detection every run.

## Real-world Application

The method transfers to any corpus or codebase where generated or hand-kept
claims must stay true: API docs quoting counts, runbooks quoting endpoints,
READMEs quoting versions. Start by inventorying claims and sorting them into
owned vs unowned; convert unowned live-count claims to restampers first
(cheapest, highest yield); sweep defect classes only where a gate can be
built from the wreckage; and keep the day-one ledger from the beginning —
it is what converts "we added checks" into "we know the checks work."

## Common Mistakes

- **Mass-applying a derivation because the numbers look large.** The See
  Also surface measured 1958 bare entries (72%) — a big, uniform-looking
  class, and exactly the shape the nav-label and cheat-sheet defects had. But
  drafting the derivation before applying it showed what readers would
  actually get: 1874 of the 1888 derivable entries collapse into four
  boilerplate templates ("the X topic index", "derives X from first
  principles") repeated hundreds of times each — the bare link with extra
  words, and a new uniform-and-wrong signature minted by the fix itself. A
  reason phrase is a judgment about *why this link helps this reader here*;
  it can be assisted, checked for hygiene (resolves, not a duplicate of the
  label), and progressively improved — but not mass-generated. The measured
  non-action and its numbers are recorded in the health-report ledger.

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
- Treat baseline JSONs (link baselines, coverage floors) as append-only audit
  trails; their diffs are the citation history.
- When a sweep comes back clean twice, stop sweeping and write the ledger —
  saturation is a result, not a failure.

## Summary

The suite combines corpus checks, parser/fixer tests, a harness auditor and a drift drill. Its checks arose from observed defects and are tested with defect and clean controls. They cover named failure classes, not every possible technical or editorial error. The design fits in
one sentence: **make the corpus a system whose lies are detectable, whose
detection is wired, and whose wiring is itself tested** — then write down
how, so the next maintainer inherits the reasoning and not just the rules.

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
