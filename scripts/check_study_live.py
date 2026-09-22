#!/usr/bin/env python3
"""Post-deploy smoke check for the private study host.

`scripts/verify.sh` gates the corpus offline; `site-build.yml` gates the local
render. Neither looks at what is actually served, so a deployment can sit
stale, mis-canonicalized or signed-out while every gate stays green. It did: on
2026-09-22 production served a Functions bundle one commit behind HEAD, so
`.pages.dev` never canonicalized and `/auth/start` answered 503.

Each probe owns its documented expectation — `--print-contract` renders them,
and a probe cannot run undocumented because the expectation is part of its
registration. There is no second list of promises to drift from.

A check's `kind` is the verdict for *any* non-matching outcome, including an
unreachable host, so an environment-state check cannot be escalated to a
failure by a third-party page being down.

Exit 0 = every probe matched. Exit 1 = a contract violation. Warnings never
change the exit code: they are environment state (a secret nobody has set, a
page someone else owns), not defects in this repo.

Usage:

    python3 scripts/check_study_live.py                 # probe production
    python3 scripts/check_study_live.py --verbose       # list passing probes too
    python3 scripts/check_study_live.py --print-contract
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import namedtuple

SCHEME = "https"
STUDY_HOST = "study.buildora.work"
PAGES_HOST = "software-developer-bible.pages.dev"
DENIAL_ORIGIN = "https://personal.buildora.work"
DENIAL_TARGET = DENIAL_ORIGIN + "/?study=access-denied"

LOGIN_PATH = "/auth/login.html"
PUBLIC_PATHS = ("/auth/login", "/auth/callback", "/favicon.svg")
FIXED_GATED_PATHS = ("/", "/INDEX.html")
# A path that certainly does not exist: the gate must answer it exactly as it
# answers a real chapter, or its redirect reveals what is on disk.
MISSING_PATH = "definitely/not/a/real/page.html"
BOGUS_TOKEN = "not-a-real-session-token"

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OK, WARN, FAIL = "PASS", "WARN", "FAIL"
Result = namedtuple("Result", "kind label name detail")
CHECKS = []


def check(label, expectation):
    """Register a probe; its label and expectation are the documented contract."""
    def register(function):
        function.label = label
        function.expectation = expectation
        CHECKS.append(function)
        return function
    return register


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Return the 3xx itself — the redirect target *is* the contract here."""

    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


class Response:
    """A status plus the two headers this contract cares about."""

    __slots__ = ("status", "location", "set_cookie", "error")

    def __init__(self, status=None, location="", set_cookie="", error=""):
        self.status = status
        self.location = location
        self.set_cookie = set_cookie
        self.error = error

    @property
    def ok(self):
        return self.status is not None

    @property
    def describe(self):
        if self.error:
            return self.error
        return f"{self.status} -> {self.location}" if self.location else str(self.status)

    def next_param(self):
        """The `next` a login redirect carries back to the requested path."""
        query = urllib.parse.urlparse(self.location).query
        return (urllib.parse.parse_qs(query).get("next") or [None])[0]


class Probe:
    """Host and transport configuration, so the same probes can drive a stub."""

    def __init__(self, scheme=SCHEME, study_host=STUDY_HOST, pages_host=PAGES_HOST,
                 denial_origin=DENIAL_ORIGIN, denial_target=DENIAL_TARGET, timeout=25):
        self.scheme, self.study_host, self.pages_host = scheme, study_host, pages_host
        self.denial_origin, self.denial_target, self.timeout = (
            denial_origin, denial_target, timeout)
        # Browser-shaped headers: Cloudflare's edge fingerprints bare clients.
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        self.opener = urllib.request.build_opener(_NoRedirect)

    def study(self, path):
        return f"{self.scheme}://{self.study_host}{path}"

    def pages(self, path):
        return f"{self.scheme}://{self.pages_host}{path}"

    def get(self, url, cookie=None):
        headers = dict(self.headers)
        if cookie:
            headers["Cookie"] = cookie
        request = urllib.request.Request(url, headers=headers)
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                return Response(response.status, response.headers.get("Location") or "",
                                response.headers.get("Set-Cookie") or "")
        except urllib.error.HTTPError as error:
            head = error.headers or {}
            return Response(error.code, head.get("Location") or "",
                            head.get("Set-Cookie") or "")
        except Exception as error:  # DNS, TLS, timeout, refused
            return Response(error=f"unreachable: {error.__class__.__name__}: {error}")


def verdict(label, name, matched, response, expected, kind=FAIL):
    """`kind` is the verdict for every non-match, reachable or not.

    Hard-coding FAIL for an unreachable host would quietly contradict the
    documented promise that a dead third-party page is a warning.
    """
    if matched:
        return Result(OK, label, name, response.describe)
    return Result(kind, label, name, f"{expected} — got {response.describe}")


def chapter_path():
    """A real deep chapter path, from the committed API dump.

    Read rather than hard-coded so the probe keeps exercising a file that
    exists after a restructure; None if the dump is unreadable.
    """
    try:
        with open(os.path.join(REPO_ROOT, "api", "index.json"), encoding="utf-8") as handle:
            records = json.load(handle).get("chapters") or []
        deep = [r["p"] for r in records if isinstance(r, dict) and "/" in r.get("p", "")]
        return sorted(deep)[0] if deep else None
    except Exception:
        return None


def gated_paths():
    """Protected paths the gate must intercept: the root, INDEX, a chapter."""
    paths = [f"/{p.lstrip('/')}" for p in FIXED_GATED_PATHS]
    chapter = chapter_path()
    return tuple(paths + [f"/{chapter}"] if chapter and f"/{chapter}" not in paths else paths)


@check("Gating",
       "every protected path — `/`, `/INDEX.html` and a real chapter — 302s to "
       "`/auth/login.html` with `next` preserved, so a deep link returns where it started")
def gate_preserves_deep_link(probe):
    out = []
    for path in gated_paths():
        response = probe.get(probe.study(path))
        matched = (response.status == 302
                   and response.location.startswith(LOGIN_PATH)
                   and response.next_param() == path)
        out.append(verdict("Gating", f"gate {path}", matched, response,
                           f"expected 302 -> {LOGIN_PATH}?next={path}"))
    return out


@check("No leak",
       "a protected chapter never answers 200, and a missing path answers exactly "
       "like a real one — the gate must not reveal what is on disk")
def protected_paths_never_serve_content(probe):
    chapter = chapter_path()
    if not chapter:
        return [Result(WARN, "No leak", "chapter discovery",
                       "could not read a chapter path from api/index.json")]
    responses = {p: probe.get(probe.study(f"/{p}")) for p in (chapter, MISSING_PATH)}
    out = [verdict("No leak", f"no-leak {path}", r.status in (302, 308), r,
                   "expected a redirect, never chapter content")
           for path, r in responses.items()]
    real, missing = responses[chapter], responses[MISSING_PATH]
    if real.ok and missing.ok:
        same = real.status == missing.status
        out.append(Result(OK if same else FAIL, "No leak", "no-leak existence",
                          f"a real chapter and a missing path both answer {real.status}"
                          if same else
                          f"a real chapter answers {real.status} while a missing path "
                          f"answers {missing.status} — the gate reveals what exists on disk"))
    return out


@check("Denial",
       "a present-but-invalid session cookie is redirected to the access-denied page, "
       "which is itself reachable; content is never served")
def invalid_session_goes_to_denial(probe):
    response = probe.get(probe.study("/"), cookie=f"study_access_token={BOGUS_TOKEN}")
    matched = response.status == 302 and response.location.startswith(probe.denial_origin)
    target = probe.get(probe.denial_target)
    alive = target.ok and 200 <= target.status < 400
    return [
        verdict("Denial", "denial branch", matched, response,
                f"invalid-session requests must redirect to {probe.denial_origin}, "
                f"never serve content or bounce to login"),
        verdict("Denial", "denial target reachable", alive, target,
                f"{probe.denial_target} does not answer — a non-owner who signs in "
                f"with a Google account lands on a dead page", kind=WARN),
    ]


@check("Public surface",
       "only `/auth/login`, `/auth/callback` and `/favicon.svg` answer 200 unauthenticated")
def public_auth_surface(probe):
    out = []
    for path in PUBLIC_PATHS:
        response = probe.get(probe.study(path))
        out.append(verdict("Public surface", f"public {path}", response.status == 200,
                           response, "expected 200; the sign-in flow is unreachable"))
    return out


@check("Canonical",
       "`software-developer-bible.pages.dev` 308s to `study.buildora.work` — the "
       "platform fallback is not a second entry point")
def canonical_host(probe):
    out = []
    for path in FIXED_GATED_PATHS:
        expected = probe.study(path)
        response = probe.get(probe.pages(path))
        matched = response.status in (301, 308) and response.location == expected
        out.append(verdict("Canonical", f"canonical {path}", matched, response,
                           f"expected 308 -> {expected}; either the Pages deployment is "
                           f"older than the middleware host check (re-run the build) or "
                           f"the account-level redirect is missing"))
    return out


@check("Sign-in",
       "`/auth/start` 302s to the Supabase authorize endpoint; a 503 is a warning, not "
       "a failure, because it needs a dashboard secret")
def signin_readiness(probe):
    response = probe.get(probe.study("/auth/start"))
    if response.status == 503:
        return [Result(WARN, "Sign-in", "sign-in /auth/start",
                       "503 — sign-in is NOT configured. Set SUPABASE_URL and either "
                       "SUPABASE_ANON_KEY or SUPABASE_JWKS_URL in Cloudflare Pages → "
                       "Settings → Environment variables (production), then re-deploy")]
    matched = (response.status == 302 and "/auth/v1/authorize" in response.location
               and "provider=google" in response.location)
    return [verdict("Sign-in", "sign-in /auth/start", matched, response,
                    "expected 302 to the Supabase authorize endpoint")]


@check("Logout",
       "`/auth/logout` 302s and clears the session cookie (`Max-Age=0`)")
def logout_clears_session(probe):
    response = probe.get(probe.study("/auth/logout"))
    cleared = ("study_access_token=" in response.set_cookie
               and "Max-Age=0" in response.set_cookie)
    return [verdict("Logout", "logout /auth/logout",
                    response.status == 302 and cleared, response,
                    "expected 302 with the session cookie cleared "
                    f"(Set-Cookie: {response.set_cookie or 'none'})")]


def run_checks(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--verbose", action="store_true", help="list passing probes too")
    parser.add_argument("--print-contract", action="store_true",
                        help="print the documented contract and exit")
    parser.add_argument("--scheme", default=SCHEME, help="scheme to probe (tests use http)")
    parser.add_argument("--study-host", default=STUDY_HOST)
    parser.add_argument("--pages-host", default=PAGES_HOST)
    parser.add_argument("--denial-origin", default=DENIAL_ORIGIN)
    parser.add_argument("--denial-target", default=DENIAL_TARGET)
    parser.add_argument("--timeout", type=float, default=25)
    args = parser.parse_args(argv)

    if args.print_contract:
        print("\n".join(f"  {c.label}: {c.expectation}" for c in CHECKS))
        return 0

    probe = Probe(args.scheme, args.study_host, args.pages_host,
                  args.denial_origin, args.denial_target, args.timeout)
    results = [result for function in CHECKS for result in function(probe)]
    failures = [r for r in results if r.kind == FAIL]
    warnings = [r for r in results if r.kind == WARN]
    passes = [r for r in results if r.kind == OK]

    print(f"Study live check — {probe.scheme}://{probe.study_host}\n")
    for result in results:
        if result.kind != OK or args.verbose:
            print(f"  {result.kind}  {result.name}: {result.detail}")
    if passes and not args.verbose:
        print(f"\n  ({len(passes)} probe(s) passed; --verbose lists them)")
    print(f"\n{len(passes)} passed · {len(warnings)} warning(s) · {len(failures)} failed")
    if warnings:
        print("\nWarnings are environment state, not defects: they need dashboard "
              "action, so they do not fail the check.")
    if failures:
        print("\nThe deployment does not match its documented contract "
              "(docs/deployment.md §2/§3). Fix forward and re-deploy, or roll back "
              "from the Pages dashboard.")
        return 1
    print("\nEvery probed contract matches.")
    return 0


def main(argv=None):
    return run_checks(argv)


if __name__ == "__main__":
    sys.exit(main())
