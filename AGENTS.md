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
- Content follows the chapter template: TL;DR → Definition → Why → How → Code → Real-world → Mistakes → Best practices → Summary → Cheat sheet → See Also → References.
- Run the link check before pushing: `python3 scripts/check_links.py` (fence-aware; exits 1 on a broken link).
- **Run the verification gates before any commit or push**: `bash scripts/verify.sh` (count guard → alignment → structure → links → freshness → link-baseline diff). The count guard (`scripts/check_counts.py`) exists because repo-scale numbers drifted repeatedly — never hand-edit the "808 files, 346K lines" claims; recompute and restamp them together. The link gate (`scripts/check_links.py`) scripts the "0 broken links" footer claim — run it standalone with `python3 scripts/check_links.py`. The freshness gate (`scripts/check_freshness.py`, added Sept 2026) catches known stale-API signatures (e.g. fake web.archive.org timestamps, deprecated `url.parse()`, sync Next.js `params`, citations to shuttered domains) so outdated code can't silently ship again — when a new modernization pass fixes a class of staleness, add a rule there so it can't regress. The link-baseline gate (`scripts/link_baseline.py` diff mode, added Sept 2026) fails the build when a doc cites an external URL missing from `scripts/external-links-baseline.json` — probe-verify new citations, then `--update` and commit the JSON with the doc change; human-browser verification steps live in `docs/residential-verification-checklist.md`.
- **Unified numbering** — every stack folder `NN.N-slug/` holds either category subfolders `NN-slug/` (2-digit study order, each with its own INDEX.md) for larger stacks, or flat numbered files. Files in categories: `<stack>.<cat>.<seq>-slug.md` (cat = folder number sans leading zero, e.g., `20.5-security/01-auth/20.5.1.01-auth-fundamentals.md`). Flat-stack files: `<stack>.<seq>-slug.md`. Sequences contiguous from 01; interview-questions files always last. Verify with `python3 scripts/check_structure.py`.
