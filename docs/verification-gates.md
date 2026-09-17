# Verification Gates — what enforces what

> **TL;DR:** Every integrity claim in this repo is enforced by a script, and
> `bash scripts/verify.sh` runs all of them. This page maps each gate to the
> rule it enforces, the files it scans, and the canonical fix when it fails.
> Gates are cheap by design (stdlib text scans) so they run on every push,
> not on a schedule.

Run everything locally before any commit:

```bash
bash scripts/verify.sh          # all 16 gates; exit 1 blocks the push
```

CI (`.github/workflows/code-whitespace.yml`) runs the same scripts on every
push/PR — a red X means a gate your local run should have caught.

## The gates

| # | Script | Enforces | Canonical fix on FAIL |
| --- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | `check_counts.py` | Repo-total scale claims ("848 files, 360K lines") match live disk. Never hand-edit the numbers — they drifted repeatedly before this gate. | Recompute: restate the string exactly as the gate recommends, in *all* files the gate lists. |
| 2 | `check_alignment.py` | Table pipes and ASCII box walls align (screen-width safe). | `python3 scripts/check_alignment.py --fix` |
| 3 | `check_structure.py` | Unified numbering: IDs resolve, sequences contiguous, interview files last. | Rename/renumber per the gate's message; see contributing.md "Unified numbering". |
| 4 | `check_links.py` | Zero broken internal links (fence-aware, anchor-verified). | Fix the path/anchor the gate prints. |
| 5 | `check_freshness.py` | Known stale-API signatures can't ship (deprecated `url.parse`, sync Next.js `params`, fake archive timestamps, …). | Update the code/doc to the modern API; add a rule here when a modernization pass fixes a *class*. |
| 6 | `link_baseline.py` (diff) | Every cited external URL is in the probe-verified baseline. | Probe-verify each new URL in a browser, then `python3 scripts/link_baseline.py --update` and commit the JSON with the doc change. |
| 6b | `check_template.py` | Chapter template: required sections per genre, canonical order, and the file-metadata contract (comment at top, canonical category, 4 badges present and ordered). | Missing section → write it for that chapter (no boilerplate). Metadata → run `python3 scripts/read_time.py --write` after fixing placement by hand. |
| 7 | `check_claims.py` | Purged unverifiable campaign phrases (Next.js-at-Docita, invented bios, DEK/KEK specifics) don't re-enter active files. | Delete the claim or re-source it; historical sent-records are exempt. |
| 8 | `check_code_whitespace.py` | Code-block indentation hygiene (no trailing whitespace, no paste-shifted blocks). | `python3 scripts/fix_code_whitespace.py --trailing-ws --paste-shift` |
| 8b | `fix_box_code_indent.py --check` | Code inside ASCII box diagrams is de-indented consistently. | `python3 scripts/fix_box_code_indent.py --fix --json --css` |
| 8c | `fix_box_width.py --check` | ASCII boxes don't exceed screen wrap width. | `python3 scripts/fix_box_width.py --fix` then gate 2 `--fix`. |
| 9 | `check_first_principles.py --diff` | First-Principles coverage never regresses from baseline (every numbered concept chapter carries one). | Restore removed sections, or re-baseline deliberately: `--baseline`. |
| 10 | `check_cross_refs.py` | Inline `→ N.N.N.N` references resolve to real files. | Fix the ID or the file name it should point at. |
| 11 | `check_duplication.py --strict` | No chapter teaches another chapter's prose (shingle similarity on section bodies). | Rewrite the duplicated section in the chapter's own voice; route to the canonical chapter instead. |
| 12 | `check_topic_twins.py` | Twin chapters (same specific topic token, different categories) must cross-link both ways. | `python3 scripts/link_topic_twins.py` (descriptions derive from the target's own opening). |
| 13 | `read_time.py --check` | Study-time lines (INDEXes) and Read-time badges (chapters) equal the computed estimate. | `python3 scripts/read_time.py --write` (idempotent; second run is a no-op). |
| 14 | `gen_master_index.py --check` | `search.html` (the site's filterable master index) is byte-identical to what the current corpus generates. | `python3 scripts/gen_master_index.py` |

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

## Adding a gate

1. Write `scripts/check_<thing>.py`, stdlib-only, exit 0/1, deterministic
   (sort every walk — union-find over unsorted `os.walk` produced different
   twin groups on macOS vs Linux once).
2. Prove it can fire: plant the defect in a scratch file and watch it fail
   before trusting a green run.
3. Calibrate to corpus reality (both documented TL;DR styles, case-study
   genre, …) — a gate stricter than the corpus buries real signal in noise.
4. Wire it into `scripts/verify.sh` with the canonical fix in the FAIL
   message, add the CI step, and add a row here.
