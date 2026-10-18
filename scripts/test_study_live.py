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
  - a deployment older than HEAD           -> exit 1
  - a deployment that never catches up     -> exit 1, after the wait expires
  - a deployment that predates the endpoint-> exit 1, after the wait expires
  - a version body that is not the payload -> exit 1, on the first read

The last four are the freshness class. The two "before the deploy lands"
states — a readable commit from an older build, and a deployment that predates
the endpoint (any non-200; the path is still gated there) — are waited for,
because a build in flight fixes both. A 200 whose body is not the endpoint's
payload is misconfiguration: the case pins both that it is reported as such
and that the wait budget is not spent on it.

The denial-offline case exists because the contract classifies a dead denial
host as environment state. The probe once hard-coded FAIL for an unreachable
host, which silently broke that promise; the stub only ever modelled "answers
404", so the broken branch was untested. Both halves of that are now covered.

Exits 0 when all cases pass; prints the failing case and exits 1 otherwise.

Run directly: python3 scripts/test_study_live.py
"""

import functools
import http.server
import json
import os
import socket
import subprocess
import sys
import threading
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_study_live as live  # noqa: E402

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_study_live.py")
PROBE_TOKEN = "stub-probe-credential"
AUTHORIZE = "https://proj.supabase.co/auth/v1/authorize?provider=google"
# Derived from the edge sources, like the probe derives it: a fixture that
# invents its own public surface could stay green while production's changed.
PUBLIC_DIRECT = live.direct_public_pages(live.public_paths())
SESSION_PATH = "/auth/session"
DENIAL_PATH = "/personal"
CLEARED_COOKIE = "study_access_token=; Max-Age=0; HttpOnly; Secure; SameSite=Lax"


def quote(value):
    return urllib.parse.quote(value, safe="")


class Stub(http.server.BaseHTTPRequestHandler):
    """A study host (or the `.pages.dev` fallback) with injectable violations."""

    role, violations, study_origin, denial_origin = "study", frozenset(), "", ""
    probe_token, probe_markers, all_markers_body = "", {}, ""
    live_version, stale_version = "", ""
    fresh_after, version_reads = 0, 0

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
            return (self.reply(302, f"{live.LOGIN_PATH}?next={quote(path)}")
                    if "no_canonical" in self.violations
                    else self.reply(308, f"{self.study_origin}{path}"))
        if path == "/api/version":
            # The deployment's commit, published without a session: what the
            # probe reads to prove the edge is this checkout rather than an
            # older one. `fresh_after` models a deployment still building: the
            # first N reads answer with the previous commit, then it catches up.
            if "version_gated" in self.violations:
                # A deployment older than the endpoint itself: the path is
                # still gated there, so it answers the login redirect until the
                # build in flight lands. The state this endpoint's first
                # deployment lives through.
                return self.reply(302, f"{live.LOGIN_PATH}?next={quote(path)}")
            if "version_not_json" in self.violations:
                # A 200 that is not the payload at all — misconfiguration, not a
                # build in flight, and the state a probe must not wait on.
                return self.reply(200, body="<!DOCTYPE html><html><body>Not the version</body></html>")
            type(self).version_reads += 1
            body = (self.live_version if type(self).version_reads > self.fresh_after
                    else self.stale_version)
            return self.reply(200, body=body)
        if path == DENIAL_PATH:  # the access-denied landing page
            return self.reply(404 if "denial_dead" in self.violations else 200, body="personal")
        if path in PUBLIC_DIRECT:
            return self.reply(200, body="public")
        if path == SESSION_PATH:
            # The real route is POST-only, so a GET is a 405 — public, but not a
            # page. Either way it must never answer like a protected path.
            if "session_gated" in self.violations:
                return self.reply(302, f"{live.LOGIN_PATH}?next={quote(path)}")
            return self.reply(405, body="method not allowed")
        if path == "/auth/start":
            return (self.reply(503, body="sign-in is not configured")
                    if "signin_unconfigured" in self.violations
                    else self.reply(302, AUTHORIZE))
        if path == "/auth/logout":
            return self.reply(302, live.LOGIN_PATH,
                              "" if "logout_no_cookie" in self.violations else CLEARED_COOKIE)
        if "serve_content" in self.violations:
            return self.reply(200, body="CHAPTER")
        cookie = self.headers.get("Cookie") or ""
        if self.probe_token and f"study_access_token={self.probe_token}" in cookie:
            if "probe_rejected" in self.violations:
                return self.reply(302, f"{live.LOGIN_PATH}?next={quote(path)}")
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
        return self.reply(302, f"{live.LOGIN_PATH}?next={quote(landed)}")


def stub_version(violations):
    """This checkout's commit in the endpoint's shape, or an older build's."""
    expected = live.local_build_commit()
    if not expected:
        raise RuntimeError(
            "this checkout's commit cannot be resolved, so the stub cannot "
            "model a current deployment — run the suite inside the git checkout")
    if "stale_deploy" in violations or "catching_up" in violations:
        return json.dumps({"commit": "0" * 40})
    return json.dumps({"commit": expected})


def start(role, violations, study_origin="", probe_token="", probe_markers=None):
    markers = dict(probe_markers or {})
    handler = type("Handler", (Stub,), {
        "role": role, "violations": frozenset(violations), "study_origin": study_origin,
        "probe_token": probe_token, "probe_markers": markers,
        "all_markers_body": "".join(f"<h1>{marker}</h1>" for marker in markers.values()),
        # `fresh_after` is how many reads answer with the previous commit before
        # the deployment catches up; infinite means it never does.
        "live_version": stub_version([]),
        "stale_version": stub_version(["stale_deploy"]),
        "fresh_after": (float("inf") if "stale_deploy" in violations
                        else 1 if "catching_up" in violations else 0),
        "version_reads": 0,
    })
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"


def closed_port():
    """A port nothing listens on, so connecting to it is refused."""
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def run_cli(*violations, signed_in=False, await_fresh=0, await_interval=20):
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
            "--await-fresh", str(await_fresh), "--await-interval", str(await_interval),
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
    # The path the probe used to skip: it is public in the middleware, and the
    # old three-path check never looked at it.
    ("a public path answering as gated exits 1", ("session_gated",), 1,
     ("public /auth/session", "lists as public"), True),
    # Nothing else here can see the stale-deploy class; this case pins the
    # failure the wait exists for, so a regression cannot turn the budget
    # expiring into a pass. Its budget comes from AWAIT_ARGS below.
    ("a deployment that never lands exits 1", ("stale_deploy",), 1,
     ("deployed build", "older than HEAD", "waited"), True),
    # The stale-deploy class: a site whose whole contract holds but whose build
    # is an older commit. Nothing else here can see it.
    ("a deployment older than HEAD exits 1", ("stale_deploy",), 1,
     ("deployed build", "older than HEAD"), True),
    # This endpoint's own first deployment: until it lands, the path is still
    # gated on the running edge (non-200), which the freshness check must wait
    # on — judging it as misconfiguration would fail the very push that ships
    # the endpoint.
    ("a deployment that predates the endpoint exits 1", ("version_gated",), 1,
     ("deployed build", "never served", "waited"), True),

    # The one credential-dependent check warns; it may never become a failure.
    ("an unconfigured probe credential warns only", (), 0,
     ("signed-in render", "STUDY_PROBE_TOKEN", "1 warning", "0 failed"), False),
]

# Cases that must exercise `--await-fresh` need a budget short enough to keep the
# suite instant. Every other case is a single read, which is what await_fresh=0
# means, so the table above stays uniform and the exception lives in one place.
AWAIT_ARGS = {
    "a deployment that never lands exits 1": {"await_fresh": 2, "await_interval": 0.2},
    "a deployment that predates the endpoint exits 1": {"await_fresh": 2, "await_interval": 0.2},
}


def case_behaviour(name, violations, want_code, needles, signed_in,
                   await_fresh=0, await_interval=20):
    code, output = run_cli(*violations, signed_in=signed_in,
                           await_fresh=await_fresh, await_interval=await_interval)
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


CASES = [(name, functools.partial(case_behaviour, name, violations, code, needles, signed_in,
                                  **AWAIT_ARGS.get(name, {})))
         for name, violations, code, needles, signed_in in BEHAVIOURS]
# The reason a push-triggered probe is safe: while a deploy is still building,
# the check waits for it rather than failing on the previous commit — or worse,
# passing on it. The stub answers the first read with the old commit and the
# second with this checkout's, which is exactly a deploy landing mid-run.
CASES.append((
    "a deployment still catching up is waited for",
    functools.partial(case_behaviour, "a deployment still catching up is waited for",
                      ("catching_up",), 0,
                      ("deployed build", "waiting for the deployment", "0 failed"), True,
                      await_fresh=2, await_interval=0.2),
))


def case_misconfigured_version_fails_fast():
    """A 200 that is not the endpoint's payload is misconfiguration, not a build in flight.

    Pins both halves so neither can regress alone: the verdict names the cause
    instead of blaming an old commit, and the probe does not spend its whole
    `--await-fresh` budget on a state that waiting cannot change. No credential
    is supplied, because judging freshness without one is the point of the
    endpoint.
    """
    started = time.monotonic()
    code, output = run_cli("version_not_json", await_fresh=30, await_interval=5)
    elapsed = time.monotonic() - started
    if code != 1:
        return f"expected exit 1, got {code}:\n{output}"
    gaps = [n for n in ("deployed build", "no commit identity") if n not in output]
    if gaps:
        return f"output is missing {gaps}:\n{output}"
    if "waiting for the deployment" in output:
        return f"waited on an unreadable body:\n{output}"
    if elapsed > 15:
        return (f"took {elapsed:.1f}s to report a state the first read already "
                f"settled:\n{output}")
    return None


CASES.append(("a version body that is not the payload fails fast",
              case_misconfigured_version_fails_fast))
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
