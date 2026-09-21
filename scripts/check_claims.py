#!/usr/bin/env python3
"""Claims-integrity gate for campaign materials.

Born from the Sept 2026 cross-repo audits (docita source vs application
materials): claim phrases that were purged as unverifiable must never
re-enter ACTIVE campaign files. Each rule carries the reason and the
source-verified replacement pattern so the fix is mechanical, not a
judgment call.

Historical sent-application reports (001-008) are allowlisted — they
record what was actually sent and must stay frozen as-is.

Usage:
    python3 scripts/check_claims.py            # gate mode (exit 1 on hit)
    python3 scripts/check_claims.py --scan     # informational, always exit 0
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from scan_scope import guard

REPO = Path(__file__).resolve().parent.parent
PERSONAL = REPO / "80-lanes-abroad-full-stack" / "personal"

# Active campaign files: application answers, outreach playbook, profile,
# CV sources, live-portfolio claims. (Interview/drill reports are reports/,
# reachable via their own docs; the answers + playbook + profile are what
# a reviewer actually receives.)
ACTIVE_GLOBS = [
    "application-outputs/application-answers-*.md",
    "outreach-playbook.md",
    "profile.yml",
    "cv.md",
    "linkedin-profile.md",
    "munich-berlin-targets.md",
]

# Historical records: what was actually sent on the dated wave. Frozen.
# reports/00N-* sent-record summaries are handled in is_frozen() below.
HISTORICAL_EXACT: set[str] = set()

# ---------------------------------------------------------------------------
# Rules. Each: pattern (regex, case-insensitive), reason, replacement hint.
# ---------------------------------------------------------------------------

RULES: list[dict] = [
    {
        "id": "NEXTJS-AT-DOCITA",
        "pattern": r"Next\.?js\s*1[45]\b(?=[^.]{0,120}\bdocita\b)|\bdocita\b[^.]{0,120}Next\.?js\s*1[45]",
        "reason": "Docita has no Next.js anywhere (audit 2026-09-14); the product "
        "frontend is React 19 + Vite SPA on Cloudflare Workers",
        "fix": "say \u201cReact 19 + Vite SPA on Cloudflare Workers\u201d; Next.js is "
        "\u201cworking depth\u201d only, never tied to Docita",
    },
    {
        "id": "NEXTJS-PRODUCTION-SURFACE",
        "pattern": r"Next\.?js[^.\n]{0,80}\b(in production|produktionserfahrung|production surface|product surface)\b",
        "reason": "production claims with Next.js as the subject are false for "
        "Docita and unsourceable elsewhere (honest form is \u201cReact product "
        "surface in production \u2026 Next.js at working depth\u201d, which this "
        "forward-only rule does not flag)",
        "fix": "\u201cApp Router working depth\u201d or name the real production stack",
    },
    {
        "id": "CELLO-FOUNDERS-TRIO",
        "pattern": r"(Twilio|Wise|Skype)[^\n.]{0,40}(Wise|Skype|Twilio)",
        "reason": "the \u201cfounding team from Twilio/Wise/Skype\u201d bio is unverifiable; "
        "verified story is payments-CRO founder DNA (audit 2026-09-14)",
        "fix": "\u201cyour CEO built Cello after years leading revenue at a payments company\u201d",
    },
    {
        "id": "STREAMING-ASSISTANT",
        "pattern": r"streaming (clinical )?assistant|assistant[^\n.]{0,40}stream(ing|s|ed)",
        "reason": "no streaming mechanism exists in docita source (audit 2026-09-14)",
        "fix": "\u201cinternal AI assistant (OpenAI-backed, feature-flagged)\u201d",
    },
    {
        "id": "INTERACTION-ANALYSIS",
        "pattern": r"(prescription[^\n.]{0,20})?interaction analysis|drug[^\n.]{0,20}interaction[^\n.]{0,20}(analysis|check)",
        "reason": "no interaction-analysis code exists in docita source (audit 2026-09-14)",
        "fix": "name the verified AI surface: assistant + OCR import workflow",
    },
    {
        "id": "ENVELOPE-ENCRYPTION",
        "pattern": r"(per-row\s+)?(DEK/KEK|envelope[^\n.]{0,20}encrypt)",
        "reason": "docita uses field-level patient-record encryption with versioned "
        "keys, not per-row DEK/KEK envelope encryption (audit 2026-09-14)",
        "fix": "\u201cfield-level encryption of patient records with versioned keys\u201d",
    },
    {
        "id": "EX-AWS-BIO",
        "pattern": r"[Ff]abian F[üu]lling[^\n.]{0,60}ex-AWS|ex-AWS[^\n.]{0,60}F[üu]lling",
        "reason": "his own LinkedIn headline is \u201cEx-Rocket | Ex-Amazon\u201d — "
        "person-bio claims must match the person's own words",
        "fix": "\u201cEx-Amazon / Ex-Rocket — exact headline per his LinkedIn\u201d",
    },
    {
        "id": "N8N-STALE-REACH",
        "pattern": r"650[,.]?000 (developers|users)|650k (developers|users)",
        "reason": "n8n publishes 204k GitHub stars / 200k+ community; the 650k "
        "figure is stale marketing (refreshed 2026-09-14)",
        "fix": "\u201c200,000-strong community\u201d",
    },
]

# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------


def iter_active_files() -> list[Path]:
    files: list[Path] = []
    for pattern in ACTIVE_GLOBS:
        files.extend(PERSONAL.glob(pattern))
    return sorted(set(files))


def is_frozen(path: Path) -> bool:
    rel = path.relative_to(PERSONAL).as_posix()
    if rel in HISTORICAL_EXACT:
        return True
    # reports/00N-* are sent-record summaries: always frozen
    if rel.startswith("reports/00") and "20" in rel:
        return True
    return False


def scan_files(mode: str) -> list[str]:
    problems: list[str] = []
    scanned = 0
    for path in iter_active_files():
        if is_frozen(path):
            continue
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for rule in RULES:
            # Strip (1) fenced code blocks and (2) double-quoted spans.
            # Quoted spans are the JD's own words (stack-match tables quote
            # requirements verbatim) or quoted titles — they are not the
            # candidate's claims, and matching across a quote/evidence cell
            # boundary produces false couples. A real claim written inside
            # quotes would be hidden too — accepted trade-off for a tripwire.
            stripped = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
            stripped = re.sub(r'"[^"\n]*"', "", stripped)
            # Strip the gate's own audit-trail lines: a "Claims audit <date>:"
            # footnote documents which phrases were purged and therefore must
            # mention them — scanning it would trip the gate forever.
            stripped = re.sub(r"(?m)^.*Claims audit \d{4}-\d{2}-\d{2}:.*$", "", stripped)
            if re.search(rule["pattern"], stripped, flags=re.IGNORECASE):
                rel = path.relative_to(REPO)
                problems.append(
                    f"  {mode}: {rel} :: rule {rule['id']}\n"
                    f"    why: {rule['reason']}\n"
                    f"    fix: {rule['fix']}"
                )
    # A claims gate over no documents finds no claims (see scan_scope).
    guard(scanned, 'active campaign documents')
    if mode == "gate" and not problems:
        print(f"OK — claims gate clean ({scanned} active files, {len(RULES)} rules).")
    elif mode == "scan" and not problems:
        print(f"Claims scan clean: {scanned} active files, {len(RULES)} rules.")
    return problems


def main() -> int:
    args = sys.argv[1:]
    scan_mode = "--scan" in args
    problems = scan_files("SCAN" if scan_mode else "CLAIM-HIT")
    if problems and not scan_mode:
        print("Claims gate FAILED:")
        print("\n".join(problems))
        return 1
    if problems:
        print("\n".join(problems))
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
