# AGENTS.md — Operating Rules for AI Assistants

> This file governs any AI CLI (Claude Code, Codex, OpenCode, …) working in this repository.

## 🔴 Hard rules

1. **NEVER commit or push in `~/repos/career-ops`.** It is an external fork (`santifer/career-ops`) used purely as a *tool*. All personal data there is gitignored and now **symlinked into this bible** — committing there is both wrong and unnecessary. If changes seem needed in career-ops:
   - data/content changes → they already land in `80-lanes-abroad-full-stack/personal/` (symlinks). Commit them HERE.
   - tool/code changes → leave uncommitted; surface to the user instead.

2. **Personal data is canonical in `80-lanes-abroad-full-stack/personal/`** (CV, profile.yml, portals.yml, application tracker, outreach playbook, targets, relocation plan, reports, generated outputs). Never duplicate it elsewhere; never copy it back into career-ops as real files.

3. **Never commit secrets or PII outside this private repo** (phone numbers, family details live only under `personal/`).

## ✅ Expected workflow

```bash
# after running career-ops tools (scan / contacto / tracker / pdf):
bash 80-lanes-abroad-full-stack/personal/doctor.sh   # verify symlinks + flag new dated artifacts
git add -A && git commit -m "…"                      # in THIS repo only
```

## Repo conventions

- Folders are numbered by study order; every topic lives in exactly ONE place (no duplicates).
- Every stack INDEX is a learning-flow doc (passes/stages), not just a file list.
- Content follows the chapter template: TL;DR → Definition → Why → How → Code → Real-world → Mistakes → Best practices → Summary → Cheat sheet → See Also → References.
- Run the link check before pushing (see contributing.md).
