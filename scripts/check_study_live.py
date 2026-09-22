#!/usr/bin/env python3
"""Post-deploy smoke check for the private study host.

`scripts/verify.sh` gates the corpus *offline*; `site-build.yml` gates the
*local* render. Neither looks at what is actually served, so a deployment can
sit stale, mis-canonicalized, or signed-out indefinitely while every gate
stays green. That is not hypothetical: on 2026-09-22 the live host was serving
the middleware from one commit *before* HEAD (the canonical-host redirect
added in `8dc0604d` had never reached production) and `/auth/start` answered
503 because the Supabase variables were never set in the Cloudflare dashboard.
Both were invisible to 26 green gates.

This check encodes the contract in docs/deployment.md as executable probes:

  1. GATE            every protected path 302s to `/auth/login.html?next=…`
                     with the requested path preserved — deep links included.
  2. NO-LEAK         a protected chapter path never returns 200 + body, and
                     the answer is identical for a path that exists and one
                     that does not (gating must not reveal what is on disk).
  3. PUBLIC-AUTH     `/auth/login`, `/auth/callback`, `/favicon.svg` are the
                     only unauthenticated 200s.
  4. CANONICAL       `software-developer-bible.pages.dev` 308s to
                     `study.buildora.work` (docs/deployment.md §2.7) — the
                     platform fallback must not be a second entry point.
  5. SIGN-IN         `/auth/start` 302s to the Supabase authorize endpoint.
                     A 503 means "not configured": reported as a WARNING with
                     the exact dashboard fix, because it depends on a secret
                     only the operator can set.
  6. LOGOUT          `/auth/logout` clears the session cookie (Max-Age=0).
  7. DENIAL-TARGET   the access-denied landing page is reachable.

Exit 0 = every probe matched. Exit 1 = at least one contract violation.
Warnings never change the exit code; they are environment state, not defects.

Usage:

    python3 scripts/check_study_live.py            # probe production
    python3 scripts/check_study_live.py --verbose  # print every probe
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

STUDY_HOST = "study.buildora.work"
PAGES_HOST = "software-developer-bible.pages.dev"
DENIAL_TARGET = "https://personal.buildora.work/"

LOGIN_PATH = "/auth/login.html"
PUBLIC_PATHS = ("/auth/login", "/auth/callback", "/favicon.svg")
FIXED_GATED_PATHS = ("/", "/INDEX.html")
# A path that certainly does not exist: the gate must answer it exactly as it
# answers a real chapter, or the redirect reveals what is on disk.
MISSING_PATH = "definitely/not/a/real/page.html"

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Browser-shaped headers: the Pages gate sits behind Cloudflare's edge, which
# fingerprints bare clients. See scripts/link_baseline.py for the same policy.
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)
HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}
TIMEOUT = 25

OK, WARN, FAIL = "PASS", "WARN", "FAIL"
RESULTS = []


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Return the 3xx itself — the redirect target *is* the contract here."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def record(kind, name, detail):
    RESULTS.append((kind, name, detail))


def probe(url):
    """GET without following redirects. Returns (status, headers)."""
    request = urllib.request.Request(url, headers=HEADERS)
    try:
        with OPENER.open(request, timeout=TIMEOUT) as response:
            return response.status, response.headers
    except urllib.error.HTTPError as error:
        return error.code, error.headers
    except Exception as error:  # DNS, TLS, timeout — reported as unreachable
        record(FAIL, url, f"unreachable: {error.__class__.__name__}: {error}")
        return None, None


def location_of(headers):
    return (headers.get("Location") or "") if headers is not None else ""


def next_param(location):
    """The `next` value a login redirect carries back to the requested path."""
    query = urllib.parse.urlparse(location).query
    values = urllib.parse.parse_qs(query).get("next") or []
    return values[0] if values else None


def chapter_path():
    """A real deep chapter path, read from the committed API dump.

    Read rather than hard-coded so the probe keeps exercising a file that
    actually exists after a restructure. Returns None if the dump is
    unreadable, in which case the gated-path set falls back to the fixed two.
    """
    api = os.path.join(REPO_ROOT, "api", "index.json")
    try:
        with open(api, encoding="utf-8") as handle:
            records = json.load(handle).get("chapters") or []
        deep = [r["p"] for r in records if isinstance(r, dict) and "/" in r.get("p", "")]
        return sorted(deep)[0] if deep else None
    except Exception:
        return None


def gated_paths():
    """Protected paths the gate must intercept: the root, INDEX, a chapter."""
    paths = list(FIXED_GATED_PATHS)
    chapter = chapter_path()
    if chapter and chapter not in paths:
        paths.append(chapter)
    return tuple(paths)


# ---------------------------------------------------------------- 1. gating


def check_gate_preserves_deep_link():
    for path in gated_paths():
        url = f"https://{STUDY_HOST}/{path.lstrip('/')}"
        status, headers = probe(url)
        if status is None:
            continue
        location = location_of(headers)
        if status != 302:
            record(FAIL, f"gate {path}", f"expected 302 to login, got {status}")
            continue
        if not location.startswith(LOGIN_PATH):
            record(FAIL, f"gate {path}", f"302 landed on {location or '(no Location)'}")
            continue
        wanted = "/" + path.lstrip("/")
        if next_param(location) != wanted:
            record(
                FAIL,
                f"gate {path}",
                f"`next` is {next_param(location)!r}, not {wanted!r} — a deep link "
                f"would not return to where it started",
            )
            continue
        record(OK, f"gate {path}", f"302 -> {location}")


# ------------------------------------------------------------- 2. no leaking


def check_no_unauthenticated_content():
    """A protected chapter must not be served, and existence must not leak."""
    chapter = chapter_path()
    if not chapter:
        record(WARN, "no-leak", "could not read a chapter path from api/index.json")
        return

    probed = {chapter: None, MISSING_PATH: None}
    for path in probed:
        status, headers = probe(f"https://{STUDY_HOST}/{path}")
        probed[path] = status
        if status is None:
            continue
        if status == 200:
            record(
                FAIL,
                f"no-leak {path}",
                "served unauthenticated with 200 — static asset reachable "
                "without the access gate",
            )
        elif status in (302, 308):
            record(OK, f"no-leak {path}", f"{status} -> {location_of(headers)}")
        else:
            record(FAIL, f"no-leak {path}", f"unexpected status {status}")

    real, fake = probed[chapter], probed[MISSING_PATH]
    if real is not None and fake is not None and real != fake:
        record(
            FAIL,
            "no-leak existence",
            f"a real chapter answers {real} while a missing path answers {fake} "
            f"— the gate reveals what exists on disk",
        )


# ---------------------------------------------------------- 3. public surface


def check_public_auth_surface():
    for path in PUBLIC_PATHS:
        status, headers = probe(f"https://{STUDY_HOST}{path}")
        if status is None:
            continue
        if status == 200:
            record(OK, f"public {path}", "200")
        else:
            record(
                FAIL,
                f"public {path}",
                f"expected 200, got {status} -> {location_of(headers)} "
                f"(the sign-in flow is unreachable)",
            )


# -------------------------------------------------------------- 4. canonical


def check_canonical_host():
    for path in ("/", "/INDEX.html"):
        status, headers = probe(f"https://{PAGES_HOST}{path}")
        if status is None:
            continue
        location = location_of(headers)
        expected = f"https://{STUDY_HOST}{'' if path == '/' else path}"
        if status == 308 and location == expected:
            record(OK, f"canonical {path}", f"308 -> {location}")
        elif status in (301, 308) and location.startswith(f"https://{STUDY_HOST}"):
            record(OK, f"canonical {path}", f"{status} -> {location}")
        else:
            record(
                FAIL,
                f"canonical {path}",
                f"expected 308 -> {expected}, got {status} -> {location or '(none)'} — "
                f"the platform fallback serves the gated site instead of "
                f"canonicalizing. Either the Pages production deployment predates "
                f"the middleware host check (re-run the Pages build) or the "
                f"account-level redirect is missing (docs/deployment.md §2.7).",
            )


# --------------------------------------------------------------- 5. sign-in


def check_signin_readiness():
    status, headers = probe(f"https://{STUDY_HOST}/auth/start")
    if status is None:
        return
    location = location_of(headers)
    if status == 302 and "/auth/v1/authorize" in location and "provider=google" in location:
        record(OK, "sign-in /auth/start", f"302 -> {urllib.parse.urlparse(location).netloc}")
    elif status == 503:
        record(
            WARN,
            "sign-in /auth/start",
            "503 — sign-in is NOT configured. Set SUPABASE_URL and either "
            "SUPABASE_ANON_KEY or SUPABASE_JWKS_URL in Cloudflare Pages → "
            "Settings → Environment variables (production), then re-deploy "
            "(docs/deployment.md §2.3)",
        )
    else:
        record(
            FAIL,
            "sign-in /auth/start",
            f"expected 302 to the Supabase authorize endpoint, got {status} -> "
            f"{location or '(none)'}",
        )


# ---------------------------------------------------------------- 6. logout


def check_logout_clears_session():
    status, headers = probe(f"https://{STUDY_HOST}/auth/logout")
    if status is None:
        return
    cookie = (headers.get("Set-Cookie") or "") if headers is not None else ""
    if status != 302:
        record(FAIL, "logout /auth/logout", f"expected 302, got {status}")
    elif "study_access_token=" not in cookie or "Max-Age=0" not in cookie:
        record(
            FAIL,
            "logout /auth/logout",
            f"302 but the session cookie is not cleared (Set-Cookie: {cookie or '(none)'})",
        )
    else:
        record(OK, "logout /auth/logout", "302 + session cookie cleared")


# ---------------------------------------------------------- 7. denial target


def check_denial_target():
    status, headers = probe(DENIAL_TARGET)
    if status is None:
        return
    if 200 <= status < 400:
        record(OK, "denial target", f"{DENIAL_TARGET} -> {status}")
    else:
        record(
            WARN,
            "denial target",
            f"{DENIAL_TARGET} -> {status}; a non-owner who signs in with a "
            f"Google account lands on a dead page",
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--verbose", action="store_true",
                        help="print passing probes too (they are summarised otherwise)")
    args = parser.parse_args()

    for check in (
        check_gate_preserves_deep_link,
        check_no_unauthenticated_content,
        check_public_auth_surface,
        check_canonical_host,
        check_signin_readiness,
        check_logout_clears_session,
        check_denial_target,
    ):
        check()

    if not RESULTS:
        print("Study live check: no probe produced a result — is the host reachable?")
        return 1

    failures = [r for r in RESULTS if r[0] == FAIL]
    warnings = [r for r in RESULTS if r[0] == WARN]
    passes = [r for r in RESULTS if r[0] == OK]

    print(f"Study live check — https://{STUDY_HOST}\n")
    for kind, name, detail in RESULTS:
        if kind == OK and not args.verbose:
            continue
        print(f"  {kind}  {name}: {detail}")
    if passes and not args.verbose:
        print(f"\n  ({len(passes)} probe(s) passed; --verbose lists them)")

    print(
        f"\n{len(passes)} passed · {len(warnings)} warning(s) · {len(failures)} failed"
    )
    if warnings:
        print("\nWarnings are environment state, not defects — they need dashboard "
              "action, so they do not fail the check.")
    if failures:
        print("\nThe deployment does not match its documented contract "
              "(docs/deployment.md §2/§3). Fix forward and re-deploy, or "
              "roll back from the Pages dashboard.")
        return 1
    print("\nEvery probed contract matches the live deployment.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
