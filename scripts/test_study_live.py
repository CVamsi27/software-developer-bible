#!/usr/bin/env python3
"""Characterization tests for scripts/check_study_live.py.

The live probe is the only thing standing between a drifted Cloudflare
deployment and a silent green board: on 2026-09-22 the production Functions
bundle was a commit behind HEAD and sign-in returned 503 while all 26 corpus
gates stayed green. That makes the probe's *classification* load-bearing, and
its failure modes are the dangerous ones:

  - a protected chapter answering 200 must be a FAIL (the security assertion
    — if this ever degrades to a warning, a leak ships as "environment
    state");
  - gating that answers differently for a real and a missing path must be a
    FAIL (existence leak);
  - a login redirect that drops `next` must be a FAIL (silent deep-link loss);
  - a 503 from `/auth/start` must be a WARN, never a FAIL — it needs a
    dashboard secret, and a check that goes red while nobody can act on it is
    a check that gets muted. The exit code is the contract.

Every case drives the real check functions with a stubbed `probe`, so the
assertions run offline in milliseconds and pin what a passing live run means.
Exits 0 when all cases pass; prints the failing case and exits 1 otherwise.

Run directly: python3 scripts/test_study_live.py
"""

import contextlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_study_live as live  # noqa: E402


class Headers:
    """Minimal stand-in for the response headers the checks read."""

    def __init__(self, **fields):
        self._fields = {k.lower(): v for k, v in fields.items()}

    def get(self, name, default=None):
        return self._fields.get(name.lower(), default)


LOGIN = "/auth/login.html"
STUDY = f"https://{live.STUDY_HOST}"
PAGES = f"https://{live.PAGES_HOST}"
# The probe reads the chapter path from api/index.json, so the test asks the
# script for it too — hard-coding one here would break on the next restructure
# and, worse, could pass while probing a path that no longer exists.
GATED = live.chapter_path()
MISSING = live.MISSING_PATH


def answer(value):
    """A route value -> a probe result.

    `(status, location)` covers redirect routes; `(status, {...})` supplies raw
    headers instead, for the logout cookie.
    """
    status, extra = value
    if isinstance(extra, dict):
        return status, Headers(**extra)
    return status, (Headers(Location=extra) if extra else Headers())


def serve(routes):
    """A `probe` whose answers come from an exact URL -> (status, Location) table.

    Exact keys, not prefixes: `/` as a prefix would swallow every other route
    and make a green case pass for the wrong reason.
    """

    def probe(url):
        if url in routes:
            return answer(routes[url])
        return 404, Headers()

    return probe


def collect(routes, checks):
    """Run `checks` against a stubbed probe; return the recorded results."""
    live.RESULTS.clear()
    live.probe = serve(routes)
    for check in checks:
        check()
    return list(live.RESULTS)


def kinds(results):
    return {(kind, name) for kind, name, _ in results}


def failed_names(results):
    return {name for kind, name, _ in results if kind == live.FAIL}


def login(next_path):
    wanted = next_path.replace("/", "%2F")
    return 302, f"{LOGIN}?next={wanted}"


def gated_routes():
    """Every protected path answering the way a working gate does."""
    return {
        f"{STUDY}/": login("/"),
        f"{STUDY}/INDEX.html": login("/INDEX.html"),
        f"{STUDY}/{GATED}": login(f"/{GATED}"),
        f"{STUDY}/{MISSING}": login(f"/{MISSING}"),
    }


# ------------------------------------------------------------------ cases


def case_contract_passes_clean():
    """The documented contract, fully satisfied, records no failures."""
    routes = dict(gated_routes())
    routes.update({
        f"{PAGES}/": (308, f"{STUDY}/"),
        f"{PAGES}/INDEX.html": (308, f"{STUDY}/INDEX.html"),
        f"{STUDY}/auth/login": (200, None),
        f"{STUDY}/auth/callback": (200, None),
        f"{STUDY}/favicon.svg": (200, None),
        f"{STUDY}/auth/start": (
            302,
            "https://proj.supabase.co/auth/v1/authorize?provider=google",
        ),
        f"{STUDY}/auth/logout": (
            302,
            {"Set-Cookie": "study_access_token=; Path=/; HttpOnly; Secure; "
                           "SameSite=Lax; Max-Age=0"},
        ),
        live.DENIAL_TARGET: (200, None),
    })
    results = collect(routes, (
        live.check_gate_preserves_deep_link,
        live.check_no_unauthenticated_content,
        live.check_public_auth_surface,
        live.check_canonical_host,
        live.check_signin_readiness,
        live.check_logout_clears_session,
        live.check_denial_target,
    ))
    failures = [r for r in results if r[0] == live.FAIL]
    if failures:
        return f"expected no failures, got {failures}"
    if len(results) < 10:
        return f"expected the checks to record >=10 results, got {len(results)}"
    return None


def case_chapter_served_is_a_failure():
    """A 200 on a protected chapter is a leak — it must FAIL, not warn."""
    routes = dict(gated_routes())
    routes[f"{STUDY}/{GATED}"] = (200, None)
    results = collect(routes, (live.check_no_unauthenticated_content,))
    if (live.FAIL, f"no-leak {GATED}") not in kinds(results):
        return f"an unauthenticated 200 on a chapter was not a FAIL: {results}"
    return None


def case_existence_leak_is_a_failure():
    """Real and missing paths must answer identically, or gating leaks disk state."""
    routes = {
        f"{STUDY}/{GATED}": login(f"/{GATED}"),
        f"{STUDY}/{MISSING}": (404, None),
    }
    results = collect(routes, (live.check_no_unauthenticated_content,))
    if (live.FAIL, "no-leak existence") not in kinds(results):
        return f"a real/missing status difference was not a FAIL: {results}"
    return None


def case_dropped_next_is_a_failure():
    """Landing on login is not enough; the requested deep link must survive."""
    routes = {
        f"{STUDY}/": login("/"),
        f"{STUDY}/INDEX.html": login("/"),
        f"{STUDY}/{GATED}": login("/"),
    }
    results = collect(routes, (live.check_gate_preserves_deep_link,))
    if f"gate {GATED}" not in failed_names(results):
        return f"a dropped `next` on a deep link was not a FAIL: {results}"
    return None


def case_non_canonical_fallback_is_a_failure():
    """The `.pages.dev` host answering with its own login is a contract violation."""
    routes = {
        f"{PAGES}/": (302, f"{LOGIN}?next=%2F"),
        f"{PAGES}/INDEX.html": (302, f"{LOGIN}?next=%2FINDEX.html"),
    }
    results = collect(routes, (live.check_canonical_host,))
    if "canonical /" not in failed_names(results):
        return f"a non-canonical fallback host was not a FAIL: {results}"
    return None


def case_unconfigured_signin_is_only_a_warning():
    """503 depends on a dashboard secret: warning, never a failure."""
    results = collect({f"{STUDY}/auth/start": (503, None)}, (live.check_signin_readiness,))
    if (live.WARN, "sign-in /auth/start") not in kinds(results):
        return f"a 503 was not a WARN: {results}"
    if any(kind == live.FAIL for kind, _, _ in results):
        return f"a 503 failed the check; it must stay actionable-not-red: {results}"
    return None


def case_logout_must_clear_the_cookie():
    """A 302 that does not clear the session cookie is a FAIL."""
    live.RESULTS.clear()
    live.probe = lambda url: (302, Headers(Set_Cookie="other=1"))
    live.check_logout_clears_session()
    if (live.FAIL, "logout /auth/logout") not in kinds(live.RESULTS):
        return f"an uncleared session cookie was not a FAIL: {live.RESULTS}"
    return None


def exit_code_for(results):
    """The exit code main() would return, with the live probes stubbed out."""
    live.RESULTS[:] = results
    saved = {n: getattr(live, n) for n in dir(live) if n.startswith("check_")}
    for name in saved:
        setattr(live, name, lambda: None)
    argv = sys.argv
    sys.argv = ["check_study_live.py"]
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return live.main()
    finally:
        sys.argv = argv
        for name, fn in saved.items():
            setattr(live, name, fn)


def case_warnings_never_change_the_exit_code():
    """The whole point of the WARN class: it must not turn a run red."""
    if exit_code_for([(live.WARN, "sign-in /auth/start", "503")]) != 0:
        return "a warning-only run exited non-zero"
    if exit_code_for([(live.OK, "gate /", "302"), (live.FAIL, "canonical /", "302")]) != 1:
        return "a run containing a FAIL exited zero"
    return None


CASES = [
    ("the documented contract passes clean", case_contract_passes_clean),
    ("an unauthenticated 200 on a chapter is a FAIL", case_chapter_served_is_a_failure),
    ("a real/missing status difference is a FAIL", case_existence_leak_is_a_failure),
    ("a dropped deep-link `next` is a FAIL", case_dropped_next_is_a_failure),
    ("a non-canonical .pages.dev host is a FAIL", case_non_canonical_fallback_is_a_failure),
    ("an unconfigured sign-in is only a WARN", case_unconfigured_signin_is_only_a_warning),
    ("logout must clear the session cookie", case_logout_must_clear_the_cookie),
    ("warnings never change the exit code", case_warnings_never_change_the_exit_code),
]


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
