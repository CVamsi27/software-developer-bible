#!/usr/bin/env python3
"""Characterization tests for scripts/check_study_live.py.

The live probe is the only thing between a drifted Cloudflare deployment and a
silent green board: on 2026-09-22 production served a Functions bundle one
commit behind HEAD — `.pages.dev` never canonicalized and `/auth/start` answered
503 — while all 26 corpus gates stayed green. That makes the probe's
classification load-bearing, and its two dangerous failure modes are a check
that can only ever report success and one that goes red on environment state.

So each case starts a local stub study host, runs the real CLI against it over
real HTTP in a subprocess, and asserts the exit code:

  - the full contract satisfied            -> exit 0, zero warnings
  - a protected chapter served             -> exit 1
  - `.pages.dev` not canonicalizing        -> exit 1
  - a login redirect that drops `next`     -> exit 1
  - a logout that keeps the session cookie -> exit 1
  - an unconfigured sign-in (503)          -> exit 0 with a warning
  - a denial page that answers 404         -> exit 0 with a warning
  - a denial page that does not answer     -> exit 0 with a warning

The last case exists because the contract classifies a dead denial host as
environment state. The probe once hard-coded FAIL for an unreachable host, which
silently broke that promise; the stub only ever modelled "answers 404", so the
broken branch was untested. Both halves of that are now covered.

Exits 0 when all cases pass; prints the failing case and exits 1 otherwise.

Run directly: python3 scripts/test_study_live.py
"""

import functools
import http.server
import os
import socket
import subprocess
import sys
import threading
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_study_live as live  # noqa: E402

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_study_live.py")
PROBE_TOKEN = "stub-probe-credential"
AUTHORIZE = "https://proj.supabase.co/auth/v1/authorize?provider=google"
PUBLIC = ("/auth/login", "/auth/callback", "/favicon.svg")
DENIAL_PATH = "/personal"
CLEARED_COOKIE = "study_access_token=; Max-Age=0; HttpOnly; Secure; SameSite=Lax"


def quote(value):
    return urllib.parse.quote(value, safe="")


class Stub(http.server.BaseHTTPRequestHandler):
    """A study host (or the `.pages.dev` fallback) with injectable violations."""

    role, violations, study_origin, denial_origin = "study", frozenset(), "", ""
    probe_token, probe_markers, all_markers_body = "", {}, ""

    def log_message(self, *args):  # keep the suite's output readable
        pass

    def reply(self, status, location="", cookie="", body=""):
        self.send_response(status)
        if location:
            self.send_header("Location", location)
        if cookie:
            self.send_header("Set-Cookie", cookie)
        payload = body.encode()
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        if payload:
            self.wfile.write(payload)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if self.role == "pages":
            return (self.reply(302, f"/auth/login.html?next={quote(path)}")
                    if "no_canonical" in self.violations
                    else self.reply(308, f"{self.study_origin}{path}"))
        if path == DENIAL_PATH:  # the access-denied landing page
            return self.reply(404 if "denial_dead" in self.violations else 200, body="personal")
        if path in PUBLIC:
            return self.reply(200, body="public")
        if path == "/auth/start":
            return (self.reply(503, body="sign-in is not configured")
                    if "signin_unconfigured" in self.violations
                    else self.reply(302, AUTHORIZE))
        if path == "/auth/logout":
            return self.reply(302, "/auth/login.html",
                              "" if "logout_no_cookie" in self.violations else CLEARED_COOKIE)
        if "serve_content" in self.violations:
            return self.reply(200, body="CHAPTER")
        cookie = self.headers.get("Cookie") or ""
        if self.probe_token and f"study_access_token={self.probe_token}" in cookie:
            if "probe_rejected" in self.violations:
                return self.reply(302, f"/auth/login.html?next={quote(path)}")
            if "probe_wrong_body" in self.violations:
                return self.reply(200, body="<html><h1>Not the chapter</h1></html>")
            if "probe_same_body" in self.violations:
                # Every marker present on every path: each per-chapter assertion
                # passes and only the distinctness net can catch it.
                return self.reply(200, body=self.all_markers_body)
            marker = self.probe_markers.get(path.lstrip("/"), "")
            return self.reply(200, body=f"<html><h1>{marker}</h1></html>")
        if "study_access_token=" in cookie:
            # Absolute, like the middleware's accessDeniedRedirect(): the denial
            # target is a different host in production.
            return self.reply(302, f"{self.denial_origin}/?study=access-denied")
        landed = "/" if "drop_next" in self.violations else path
        return self.reply(302, f"/auth/login.html?next={quote(landed)}")


def start(role, violations, study_origin="", probe_token="", probe_markers=None):
    markers = dict(probe_markers or {})
    handler = type("Handler", (Stub,), {
        "role": role, "violations": frozenset(violations), "study_origin": study_origin,
        "probe_token": probe_token, "probe_markers": markers,
        "all_markers_body": "".join(f"<h1>{marker}</h1>" for marker in markers.values()),
    })
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"


def closed_port():
    """A port nothing listens on, so connecting to it is refused."""
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def run_cli(*violations, signed_in=False):
    """Run the real CLI against stubbed hosts. Returns (exit code, output).

    `signed_in` supplies the probe credential, whose absence is itself one of
    the classifications under test. The child's environment is pinned rather
    than inherited, so a developer's own STUDY_PROBE_TOKEN cannot decide which
    case passes.
    """
    token = PROBE_TOKEN if signed_in else ""
    markers = dict(live.probe_sample()) if signed_in else {}
    study, study_origin = start("study", violations,
                                probe_token=token, probe_markers=markers)
    # In production the denial target is a different host; the stub plays both,
    # so it can only learn its own origin once the port is bound.
    study.RequestHandlerClass.denial_origin = study_origin
    pages, _ = start("pages", violations, study_origin=study_origin)
    denial = (f"http://127.0.0.1:{closed_port()}{DENIAL_PATH}"
              if "denial_offline" in violations else f"{study_origin}{DENIAL_PATH}")
    try:
        command = [
            sys.executable, SCRIPT, "--verbose", "--scheme", "http",
            "--study-host", f"127.0.0.1:{study.server_address[1]}",
            "--pages-host", f"127.0.0.1:{pages.server_address[1]}",
            "--denial-origin", study_origin, "--denial-target", denial,
            "--timeout", "10", "--probe-token", token,
        ]
        done = subprocess.run(command, capture_output=True, text=True, timeout=120,
                              env={**os.environ, "STUDY_PROBE_TOKEN": token})
        return done.returncode, done.stdout + done.stderr
    finally:
        study.shutdown()
        pages.shutdown()


# (name, stub violations, expected exit code, output must contain)
# Needles are the probe's own name plus the short head of its expectation, not
# free prose from the message body: rewording an explanation must not break the
# suite, but losing the named probe it belongs to must.
BEHAVIOURS = [
    ("a satisfied contract exits 0", (), 0, ("0 failed", "0 warning"), True),
    ("a served chapter exits 1", ("serve_content",), 1,
     ("no-leak", "expected a redirect"), True),
    ("a non-canonical fallback exits 1", ("no_canonical",), 1,
     ("canonical /", "expected 308"), True),
    ("a dropped deep-link `next` exits 1", ("drop_next",), 1,
     ("gate /INDEX.html", "next=/INDEX.html"), True),
    ("an uncleared logout exits 1", ("logout_no_cookie",), 1,
     ("logout /auth/logout", "session cookie"), True),
    ("an unconfigured sign-in warns only", ("signin_unconfigured",), 0,
     ("sign-in /auth/start", "NOT configured", "1 warning"), True),
    ("a denial page answering 404 warns only", ("denial_dead",), 0,
     ("denial target reachable", "1 warning"), True),
    ("a denial page that does not answer warns only", ("denial_offline",), 0,
     ("denial target reachable", "unreachable", "1 warning"), True),
    # The success path. With a credential the probe asserts a real chapter is
    # served *and that it is that chapter*; without one it must warn, because
    # the join it covers is then unverified.
    ("a rejected probe credential exits 1", ("probe_rejected",), 1,
     ("signed-in ", "expected 200"), True),
    ("a page without the chapter's title exits 1", ("probe_wrong_body",), 1,
     ("signed-in ", "expected 200"), True),
    ("one response for every chapter exits 1", ("probe_same_body",), 1,
     ("distinct pages", "identical bodies"), True),
    ("an unconfigured probe credential warns only", (), 0,
     ("signed-in render", "STUDY_PROBE_TOKEN", "1 warning"), False),
]


def case_behaviour(name, violations, want_code, needles, signed_in):
    code, output = run_cli(*violations, signed_in=signed_in)
    if code != want_code:
        return f"expected exit {want_code}, got {code}:\n{output}"
    gaps = [n for n in needles if n not in output]
    if gaps:
        return f"output is missing {gaps}:\n{output}"
    return None


def case_probes_declare_their_contract():
    labels = [function.label for function in live.CHECKS]
    if len(set(labels)) != len(labels):
        return f"duplicate probe labels: {sorted(labels)}"
    silent = [f.__name__ for f in live.CHECKS if not (getattr(f, "expectation", "") or "").strip()]
    if silent:
        return (f"probes with no documented expectation: {silent} — a probe that "
                f"cannot be described is a probe nobody can review")
    return None


CASES = [(name, functools.partial(case_behaviour, name, violations, code, needles, signed_in))
         for name, violations, code, needles, signed_in in BEHAVIOURS]
CASES.append(("probes declare their contract", case_probes_declare_their_contract))


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
        print(f"\n{failures} case(s) failed — check_study_live.py's classification "
              f"drifted; fix the check, not these expectations.")
        return 1
    n = len(CASES)
    print(f"\nstudy_live: {n}/{n} cases pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
