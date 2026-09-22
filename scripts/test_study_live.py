#!/usr/bin/env python3
"""Characterization tests for scripts/check_study_live.py.

The live probe is the only thing between a drifted Cloudflare deployment and a
silent green board: on 2026-09-22 production served a Functions bundle one
commit behind HEAD — `.pages.dev` never canonicalized and `/auth/start` answered
503 — while all 26 corpus gates stayed green. That makes the probe's
*classification* load-bearing, and its dangerous failure mode is a check that
can only ever report success.

So each behaviour case starts a local stub study host, runs the real CLI
against it over real HTTP via a subprocess, and asserts the exit code:

  - the full contract satisfied        -> exit 0, zero warnings
  - a protected chapter served         -> exit 1
  - `.pages.dev` not canonicalizing    -> exit 1
  - a login redirect that drops `next` -> exit 1
  - a logout that keeps the session    -> exit 1
  - an unconfigured sign-in (503)      -> exit 0 with a warning, never red
  - a dead access-denied page          -> exit 0 with a warning

Plus one consistency case that needs no server: every probe must claim a
documented contract label, and every documented label must have a probe — so
the contract cannot quietly drift away from what actually runs.

Exits 0 when all cases pass; prints the failing case and exits 1 otherwise.

Run directly: python3 scripts/test_study_live.py
"""

import functools
import http.server
import os
import subprocess
import sys
import threading
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_study_live as live  # noqa: E402

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_study_live.py")
AUTHORIZE = "https://proj.supabase.co/auth/v1/authorize?provider=google"
PUBLIC = ("/auth/login", "/auth/callback", "/favicon.svg")
DENIAL_PATH = "/personal"


def quote(value):
    return urllib.parse.quote(value, safe="")


class Stub(http.server.BaseHTTPRequestHandler):
    """A study host (or the `.pages.dev` fallback) with injectable violations."""

    role = "study"
    violations = frozenset()
    study_origin = ""
    denial_origin = ""

    def log_message(self, *args):  # keep the suite's output readable
        pass

    def reply(self, status, location="", set_cookie="", body=""):
        self.send_response(status)
        if location:
            self.send_header("Location", location)
        if set_cookie:
            self.send_header("Set-Cookie", set_cookie)
        payload = body.encode()
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        if payload:
            self.wfile.write(payload)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path

        if self.role == "pages":
            if "no_canonical" in self.violations:
                return self.reply(302, location=f"/auth/login.html?next={quote(path)}")
            return self.reply(308, location=f"{self.study_origin}{path}")

        if path == DENIAL_PATH:  # the access-denied landing page
            return self.reply(404 if "denial_dead" in self.violations else 200, body="personal")
        if path in PUBLIC:
            return self.reply(200, body="public")
        if path == "/auth/start":
            if "signin_unconfigured" in self.violations:
                return self.reply(503, body="Study sign-in is not configured.")
            return self.reply(302, location=AUTHORIZE)
        if path == "/auth/logout":
            cookie = ("" if "logout_no_cookie" in self.violations else
                      "study_access_token=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0")
            return self.reply(302, location="/auth/login.html", set_cookie=cookie)

        if "serve_content" in self.violations:
            return self.reply(200, body="CHAPTER")
        if "study_access_token=" in (self.headers.get("Cookie") or ""):
            # Absolute, like the middleware's accessDeniedRedirect(): the
            # denial target is a different host in production.
            return self.reply(302, location=f"{self.denial_origin}/?study=access-denied")
        landed = "/" if "drop_next" in self.violations else path
        return self.reply(302, location=f"/auth/login.html?next={quote(landed)}")


def start(role, violations, study_origin="", denial_origin=""):
    handler = type("Handler", (Stub,), {
        "role": role,
        "violations": frozenset(violations),
        "study_origin": study_origin,
        "denial_origin": denial_origin,
    })
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"


def run_cli(*violations):
    """Run the real CLI against stubbed hosts. Returns (exit code, output)."""
    study, study_origin = start("study", violations)
    # In production the denial target is a different host; the stub plays both,
    # so it can only learn its own origin once the port is bound.
    study.RequestHandlerClass.denial_origin = study_origin
    pages, _ = start("pages", violations, study_origin=study_origin)
    try:
        command = [
            sys.executable, SCRIPT, "--verbose", "--scheme", "http",
            "--study-host", f"127.0.0.1:{study.server_address[1]}",
            "--pages-host", f"127.0.0.1:{pages.server_address[1]}",
            "--denial-origin", study_origin,
            "--denial-target", f"{study_origin}{DENIAL_PATH}",
            "--timeout", "10",
        ]
        done = subprocess.run(command, capture_output=True, text=True, timeout=120)
        return done.returncode, done.stdout + done.stderr
    finally:
        study.shutdown()
        pages.shutdown()


# (name, stub violations, expected exit code, output must contain)
BEHAVIOURS = [
    ("a satisfied contract exits 0", (), 0, ("0 failed", "0 warning")),
    ("a served chapter exits 1", ("serve_content",), 1, ("no-leak",)),
    ("a non-canonical fallback exits 1", ("no_canonical",), 1, ("canonicalizing",)),
    ("a dropped deep-link `next` exits 1", ("drop_next",), 1, ("next=/INDEX.html",)),
    ("an uncleared logout exits 1", ("logout_no_cookie",), 1, ("session cookie",)),
    ("an unconfigured sign-in warns only", ("signin_unconfigured",), 0,
     ("NOT configured", "1 warning")),
    ("a dead denial target warns only", ("denial_dead",), 0,
     ("denial target reachable",)),
]


def case_behaviour(name, violations, want_code, needles):
    code, output = run_cli(*violations)
    if code != want_code:
        return f"expected exit {want_code}, got {code}:\n{output}"
    gaps = [n for n in needles if n not in output]
    if gaps:
        return f"output is missing {gaps}:\n{output}"
    return None


def case_probes_and_contract_agree():
    documented = {label for label, _ in live.CONTRACT}
    claimed = {function.label for function in live.CHECKS}
    if documented != claimed:
        return (f"probes claim {sorted(claimed)} but the contract documents "
                f"{sorted(documented)} — a probe would run undocumented, or a "
                f"documented expectation would never be checked")
    return None


CASES = [(
    f"{name}", functools.partial(case_behaviour, name, violations, code, needles)
) for name, violations, code, needles in BEHAVIOURS]
CASES.append(("probes and contract agree", case_probes_and_contract_agree))


def main() -> int:
    failures = 0
    for name, case in CASES:
        problem = case()
        if problem:
            failures += 1
            print(f"FAIL {name}\n  {problem}")
        else:
            print(f"ok   {name}")
    if failures:
        print(f"\n{failures} case(s) failed — check_study_live.py's contract drifted; "
              f"fix the check, not these expectations.")
        return 1
    n = len(CASES)
    print(f"\nstudy_live: {n}/{n} cases pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
