# AGENTS.md — Operating Rules for AI Assistants

> This file governs any AI CLI (Claude Code, Codex, OpenCode, …) working in this repository.

## Hard rules

1. **NEVER commit or push in `~/repos/career-ops`.** It is an external fork (`santifer/career-ops`) used purely as a *tool*. All personal data there is gitignored and now **symlinked into this bible** — committing there is both wrong and unnecessary. If changes seem needed in career-ops:
   - data/content changes → they already land in `80-lanes-abroad-full-stack/personal/` (symlinks). Commit them HERE.
   - tool/code changes → leave uncommitted; surface to the user instead.

2. **Personal data is canonical in `80-lanes-abroad-full-stack/personal/`** (CV, profile.yml, portals.yml, application tracker, outreach playbook, targets, relocation plan, reports, generated outputs). Never duplicate it elsewhere; never copy it back into career-ops as real files.

3. **Never commit secrets or PII outside this private repo** (phone numbers, family details live only under `personal/`).

## Expected workflow

```bash
# after running career-ops tools (scan / contacto / tracker / pdf):
bash 80-lanes-abroad-full-stack/personal/doctor.sh # verify symlinks + flag new dated artifacts
bash scripts/verify.sh                            # count + alignment + structure + link gates (see contributing.md)
git add -A && git commit -m "…" # in THIS repo only
```

## Repo conventions

- Folders are numbered by study order; every topic lives in exactly ONE place (no duplicates).
- Every stack INDEX is a learning-flow doc (passes/stages), not just a file list.
- Teaching chapters follow Definition → First Principles → Why → How → Examples → Real-world decisions → Mistakes → Best practices → Summary → See Also → References. **TL;DR is retired** (2026-10-01): introduce the concept once, then explain it. First Principles derives the topic from unavoidable constraints; it must not restate the definition or list benefits. Every mechanism/example has one canonical home; adjacent sections add new reasoning rather than repeat code. Optional sections may be omitted when they add no distinct teaching value.
- **Reading flow:** motivate a concrete problem, explain its mechanism, trace one focused example, then compare decisions and boundaries. Define terms before relying on them. When introducing a component, explain how it fits inside the whole before listing its variants. Headings should state the relationship or question being explained, not merely name unfamiliar jargon followed by “in detail”. Use short topic-specific headings and small diagrams/tables when they resolve confusion; do not mechanically fill template headings or repeat an overview in several forms.
- **Revision is separate:** each category has a `REVISION.md` companion; flat stacks place it at stack level. Learning chapters link to it under See Also and end their content with one Summary. The category INDEX puts revision after the learning chapters and before interview practice. Companions preserve existing authored questions and contain at least five fresh-worded `**Q:**`/`**A:**` pairs overall, with at least one source-linked group/question per concept or case study. Interview banks remain their own drill. `REVISION.md` is an explicitly named companion exempt from numbered chapter sequences; existing chapter IDs stay stable. Do not put a Cheat Sheet or revision drill inside a concept chapter.
- Run the link check before pushing: `python3 scripts/check_links.py` (fence-aware; exits 1 on a broken link).
- **Run the verification gates before any commit or push**: `bash scripts/verify.sh` (count guard → alignment → structure → links → freshness → link-baseline diff). The count guard (`scripts/check_counts.py`) exists because repo-scale numbers drifted repeatedly — never hand-edit a `files`/`K lines` claim, an INDEX `Files` badge, an INDEX `> **N files**` blurb or a navigation-table count; run `python3 scripts/check_counts.py --write` to recompute and restamp them all from disk together. The link gate (`scripts/check_links.py`) scripts the "0 broken links" footer claim — run it standalone with `python3 scripts/check_links.py`. The freshness gate (`scripts/check_freshness.py`, added Sept 2026) catches known stale-API signatures (e.g. fake web.archive.org timestamps, deprecated `url.parse()`, sync Next.js `params`, citations to shuttered domains) so outdated code can't silently ship again — when a new modernization pass fixes a class of staleness, add a rule there so it can't regress. The link-baseline gate (`scripts/link_baseline.py` diff mode, added Sept 2026) fails the build when a doc cites an external URL missing from `scripts/external-links-baseline.json` — probe-verify new citations, then `--update` and commit the JSON with the doc change; human-browser verification steps live in `docs/residential-verification-checklist.md`.
- **Unified numbering** — every stack folder `NN.N-slug/` holds either category subfolders `NN-slug/` (2-digit study order, each with its own INDEX.md) for larger stacks, or flat numbered files. Files in categories: `<stack>.<cat>.<seq>-slug.md` (cat = folder number sans leading zero, e.g., `20.5-security/01-auth/20.5.1.01-auth-fundamentals.md`). Flat-stack files: `<stack>.<seq>-slug.md`. Sequences contiguous from 01; interview-questions files always last. Verify with `python3 scripts/check_structure.py`.
