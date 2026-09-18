# Verification Gates — what enforces what

> **TL;DR:** Every integrity claim in this repo is enforced by a script, and
> `bash scripts/verify.sh` runs all of them. This page maps each gate to the
> rule it enforces, the files it scans, and the canonical fix when it fails.
> Gates are cheap by design (stdlib text scans) so they run on every push,
> not on a schedule.

Run everything locally before any commit:

```bash
bash scripts/verify.sh          # all 18 gates; exit 1 blocks the push
```

CI (`.github/workflows/code-whitespace.yml`) runs the same scripts on every
push/PR — a red X means a gate your local run should have caught.

## The gates

| # | Script | Enforces | Canonical fix on FAIL |
| --- | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `check_counts.py` | Every count in the navigation surface matches live disk: repo-scale strings ("854 files, 362K lines"), each INDEX's `Files` badge **and** its `> **N files** …` opening blurb, the `N files in M sub-stacks` stack headers, the `Files` column of every navigation table, and the prose counts that quote one (interview banks, cheat-sheet formats, `{% raw %}` files). It also owns ROADMAP's structural claims — case-study total, `20-backend` sub-stack count, and the real `30.2-system-design` subfolder names — which were ungated and had drifted (`Case studies ×20` against 31 on disk, `9 sub-stacks` against 10, `00-theory + 10-case-studies` against renumbered folders). Never hand-edit the numbers — 15 of 159 badges and 7 blurbs had drifted from the folder they point at before the scope was widened. | `python3 scripts/check_counts.py --write` (restamps digits only; re-run `check_alignment.py --fix` if a digit count changed) |
| 2 | `check_alignment.py` | Table pipes and ASCII box walls align (screen-width safe), **and every table has a header row**. A separator row with no header above it renders with a blank header, silently deleting the column labels — three chapters shipped that way (one generation pass left a duplicated separator), because alignment only ever checked *pipe* consistency, never that a header existed. Headerless tables are reported but never auto-fixed: the header text is content, and inventing it would be worse than failing (`--fix` still exits 1 while any remain). | `python3 scripts/check_alignment.py --fix` (headerless tables must be repaired by hand) |
| 3 | `check_structure.py` | Unified numbering: IDs resolve, sequences contiguous, interview files last. Also **no two H2 sections in one file may share a slug** — a duplicate means two identically-named outline entries and an ambiguous anchor, and it is the tell that repeated sub-structures were written as *siblings* rather than nested under their section. `80.12-story-bank.md` presented 13 stories as 65 sibling H2s with no story titles at all, and `81.05-advanced-topics.md` declared "Segment Tree" twice in a row while mixing topic titles with their own subsections. Repeats belong at `###` or deeper, where the same label under a different parent is legitimate (the 13 per-story `### Situation` blocks). Deliberately **not** gated: "one H1 per document" — several lane guides use `# Phase N:` / `# Wave N:` as document stubs, which is internally consistent there and would cascade every heading level in four large files. | Rename/renumber per the gate's message; for a duplicate H2, nest the repeats as `###` (and see contributing.md "Unified numbering"). |
| 4 | `check_links.py` | Zero broken internal links (fence-aware, anchor-verified) **and zero stale link *labels***. Every relative prose link must resolve, and a visible label that is itself a relative path (`../../2-Backend-Stack/12-Microservices/03-Saga-Pattern.md`) must point at a path that exists — those are pre-renumbering relics where the *target* was updated but the *label* was not, so a target-only checker never sees them while the reader is shown archaeology from a folder layout that no longer exists. The Sept 2026 redundancy audit fixed 10 such lines in 2 files; ~18 more survived in 10 files undetected, including two links that displayed a dead path *and* pointed at the wrong destination (Observability and Microservices both silently resolved to the local theory INDEX). Spaced labels (the generated `← Previous: ../02 Io And Data/index` footers) are humanized titles, not paths, and are not judged; post-mortem reports under `personal/` are exempt because they quote dead paths as documentation. | Fix the path/anchor the gate prints; for a stale label, rewrite it as the target's human title (a reader should never see a folder path). |
| 5 | `check_freshness.py` | Known stale-API signatures can't ship (deprecated `url.parse`, sync Next.js `params`, fake archive timestamps, …). | Update the code/doc to the modern API; add a rule here when a modernization pass fixes a *class*. |
| 6 | `link_baseline.py` (diff) | Every cited external URL is in the probe-verified baseline. | Probe-verify each new URL in a browser, then `python3 scripts/link_baseline.py --update` and commit the JSON with the doc change. |
| 6b | `check_template.py` | Chapter template: required sections per genre, canonical order, and the file-metadata contract (comment at top, canonical category, 4 badges present and **ordered and correctly targeted** — content-file badges must link to `#` per contributing.md's "File Metadata"; only INDEX/README Files badges point at the central INDEX. Twelve newly authored chapters had drifted to `INDEX.md`/`../../INDEX.md` because only presence and order were ever checked). It also rejects **empty sections** — a heading immediately followed by a heading at the *same or shallower* level, which renders as a dead entry in the outline with its apparent children sitting beside it (`## Remediation Strategies` → `## Strangler Fig Pattern`, `## Consensus Algorithms` → `## Raft`). The rule is deliberately narrow: a heading followed by a *deeper* heading is the normal shape of every `## How It Works`, so a naive heading-after-heading test fires on 1765 legitimate places. | Missing section → write it for that chapter (no boilerplate). Metadata → run `python3 scripts/read_time.py --write` after fixing placement by hand. |
| 7 | `check_claims.py` | Purged unverifiable campaign phrases (Next.js-at-Docita, invented bios, DEK/KEK specifics) don't re-enter active files. | Delete the claim or re-source it; historical sent-records are exempt. |
| 8 | `check_code_whitespace.py` | Code-block indentation hygiene (no trailing whitespace, no paste-shifted blocks) **and fence balance**. A closing fence may not carry an info string, so a fenced block containing *same-length* nested fences ends at the first bare fence — `50.4.01-incident-response.md` shipped that way, leaking two runbook headings out as real document headings and swallowing its final ~30 lines into an unclosed code block. Every fence-aware gate missed it because they all toggled on fence character alone; nesting legitimately requires a longer outer fence (```` around ```). UNCLOSED-FENCE is reported but never auto-fixed. | `python3 scripts/fix_code_whitespace.py --trailing-ws --paste-shift` (UNCLOSED-FENCE excepted — lengthen the outer fence by hand) |
| 8b | `fix_box_code_indent.py --check` | Code inside ASCII box diagrams is de-indented consistently. | `python3 scripts/fix_box_code_indent.py --fix --json --css` |
| 8c | `fix_box_width.py --check` | ASCII boxes don't exceed screen wrap width. | `python3 scripts/fix_box_width.py --fix` then gate 2 `--fix`. |
| 9 | `check_first_principles.py --diff` | First-Principles coverage never regresses from baseline (every numbered concept chapter carries one). | Restore removed sections, or re-baseline deliberately: `--baseline`. |
| 10 | `check_cross_refs.py` | Inline `→ N.N.N.N` references resolve to real files. | Fix the ID or the file name it should point at. |
| 11 | `check_duplication.py --strict` | No chapter teaches another chapter's prose (shingle similarity on section bodies). | Rewrite the duplicated section in the chapter's own voice; route to the canonical chapter instead. |
| 12 | `check_topic_twins.py` | Twin chapters (same specific topic token, different categories) must cross-link both ways. | `python3 scripts/link_topic_twins.py` (descriptions derive from the target's own opening). |
| 13 | `read_time.py --check` | Study-time lines (INDEXes) and Read-time badges (chapters) equal the computed estimate. | `python3 scripts/read_time.py --write` (idempotent; second run is a no-op). |
| 14 | `gen_master_index.py --check` | `search.html` (the site's filterable master index) is byte-identical to what the current corpus generates. | `python3 scripts/gen_master_index.py` |
| 15 | `check_verify_wiring.py` | **The harness audits itself, and so does CI.** Locally: every gate's failure branch sets the same variable the trailing summary reads; no `X=$((X+1))` on an uninitialized variable (the `set -u` abort); every script a gate invokes exists; gate labels are unique, gap-free and monotonic; and the gate count quoted in `verify.sh`, `contributing.md` and this page all agree. In CI: every workflow step that runs a gate under `set +e` must propagate its exit status (the same false green one level up — `job-board-watch.yml` and `link-rot-audit.yml` are exempt **by name, with the reason**, because they are audits that deliberately turn a non-zero exit into a tracking issue); every gate must actually be enforced by CI; and every script a workflow references must be in its `paths:` trigger filter. Born from a real **false green**: gate 10's failure branch wrote `FAILURES` instead of `FAIL`, so under `set -u` the unbound arithmetic aborted `verify.sh` *before* its trailing `exit $FAIL` — a genuinely broken cross-reference printed `FAIL`, skipped gates 11–14 entirely, and still exited **0**, so CI reported success on a red build. Every gate *script* was correct throughout; nothing measured whether the harness listened. | `python3 scripts/check_verify_wiring.py --write` restamps the count from the same computation it checks. Wiring defects (a failure branch that cannot reach the exit, a CI step that drops its status, a gate missing from CI, a trigger filter that omits a script) must be fixed by hand — that is the whole point. |

## Scope: what each gate scans

Two walks exist, and knowing which is which explains most "why wasn't this
flagged?" surprises:

**Filename-numbered concept chapters** — gate 9 (`check_first_principles.py`)
walks every top-level dir starting with a digit and selects files matching
`N(.N)+-` that aren't interview/cheat/quick-reference. This *includes* the
80-lanes trees (their planning docs carry First-Principles sections too) and
*excludes* INDEX files and interview banks by name.

**All content markdown** — gates 6b, 10–13 walk every `*.md` outside
`INDEX.md`/`README.md` and the exempt prefixes (`80-lanes-*`, `81-lanes-*`,
`projects/`, and for 6b `docs/`), i.e. today's 550 content files. Lanes and
projects are exempt *here* on purpose: they are personal campaign/planning
material with their own genres (phase guides, trackers), not chapter-shaped
teaching documents. Gate 7 (`check_claims.py`) covers their campaign-content
risk separately.

**Whole-tree** — gates 1–5, 8–8c (counts, alignment, structure, links,
freshness, whitespace) scan everything including lanes and docs, because
broken links and misaligned tables are genre-independent defects. Gate 14
regenerates `search.html` from gates 6b+13 data, so it inherits their scope.

**Not content at all** — gate 15 (`check_verify_wiring.py`) never reads a
chapter. It reads only `scripts/verify.sh`, `contributing.md` and this page,
checking the harness's own wiring and self-description. It is the only gate
whose subject is the gate system, and it exists because a gate can be
perfectly correct and still not block anything.


## Adding a gate

1. Write `scripts/check_<thing>.py`, stdlib-only, exit 0/1, deterministic
   (sort every walk — union-find over unsorted `os.walk` produced different
   twin groups on macOS vs Linux once). Prefer giving the gate a `--write`
   that *restamps* the claim from the same computation it checks (the
   `check_counts.py` / `read_time.py` pattern): a claim with one owner and a
   rewriter cannot drift, and the fix command is never guesswork.
2. Prove it can fire — **both halves**. Plant the defect in a scratch file and
   watch the *script* fail, then run `bash scripts/verify.sh` and confirm it
   fails too. The second half is not ceremony: gate 10's failure branch wrote a
   variable named `FAILURES` instead of `FAIL`, so its own correct `exit 1`
   never reached the suite's exit code and a broken cross-reference passed CI
   for as long as the bug existed. Gate 15 now checks that wiring statically —
   run it after touching `verify.sh`, and remember that planting a defect
   manually leaves the tree dirty if the script you test aborts early (use a
   scratch copy and restore in a `finally`).
3. Calibrate to corpus reality (both documented TL;DR styles, case-study
   genre, …) — a gate stricter than the corpus buries real signal in noise.
4. Wire it into `scripts/verify.sh` with the canonical fix in the FAIL
   message, add the CI step, and add a row here. Use `FAIL=1` in the failure
   branch — gate 15 enforces that, along with the label order and the gate
   count quoted in all three files (`--write` restamps the count). If you add
   a CI step, make it propagate its exit status (`exit "$code"` after
   `set +e`) and make sure the workflow's `paths:` filter covers the script;
   gate 15 enforces both, so a gate that cannot fail the job and a gate that
   no push can trigger are caught before they ship.
