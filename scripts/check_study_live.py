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
import re
import sys
import time
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
FIXED_GATED_PATHS = ("/", "/INDEX.html")
# A path that certainly does not exist: the gate must answer it exactly as it
# answers a real chapter, or its redirect reveals what is on disk.
MISSING_PATH = "definitely/not/a/real/page.html"
BOGUS_TOKEN = "not-a-real-session-token"
# The probe's own credential, if the operator has set one: with it the success
# path — the half of the gate that serves a chapter — stops being the one thing
# nobody can exercise. Read from the environment, never committed.
PROBE_TOKEN_ENV = "STUDY_PROBE_TOKEN"
PROBE_COOKIE = "study_access_token"

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIDDLEWARE_SOURCE = os.path.join(REPO_ROOT, "functions", "_lib", "study-access.mjs")
PUBLIC_SET_RE = re.compile(r"PUBLIC_AUTH_PATHS = new Set\(\[(.*?)\]\)", re.S)
# The adapter that answers the OAuth callback itself, with no file behind it.
INTERCEPT_SOURCE = os.path.join(REPO_ROOT, "functions", "_middleware.ts")
INTERCEPT_PATH_RE = re.compile(r'url\.pathname === "([^"]+)"')
OK, WARN, FAIL = "PASS", "WARN", "FAIL"
Result = namedtuple("Result", "kind label name detail")
CHECKS = []
_DENSE_RECORDS = None


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
    """A status, the two headers this contract cares about, and a body prefix."""

    __slots__ = ("status", "location", "set_cookie", "error", "body")

    def __init__(self, status=None, location="", set_cookie="", error="", body=""):
        self.status = status
        self.location = location
        self.set_cookie = set_cookie
        self.error = error
        self.body = body

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
                 denial_origin=DENIAL_ORIGIN, denial_target=DENIAL_TARGET, timeout=25,
                 probe_token="", probe_sample=(), await_fresh=0, await_interval=20):
        self.scheme, self.study_host, self.pages_host = scheme, study_host, pages_host
        self.denial_origin, self.denial_target, self.timeout = (
            denial_origin, denial_target, timeout)
        self.probe_token, self.probe_sample = probe_token, list(probe_sample)
        # Seconds to wait for a deployment to land before judging its currency:
        # Pages builds in parallel with CI, so a push-triggered run can arrive
        # before the deploy it is measuring exists yet.
        self.await_fresh, self.await_interval = await_fresh, await_interval
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

    def follow_same_host(self, response, cookie=None):
        """One same-host redirect hop, for rules about the page finally served.

        Cloudflare Pages answers `/auth/login.html` with a 308 to `/auth/login`,
        so a canonical-suffix redirect is the platform working, not a routing
        failure. Returning the first hop's response instead would make this
        probe demand 200 from a URL the host deliberately never serves.
        """
        if response.status not in (301, 302, 307, 308) or not response.location:
            return response
        parsed = urllib.parse.urlparse(response.location)
        if parsed.netloc and parsed.netloc != self.study_host:
            return response  # off-host: somebody else's service, not our page
        target = parsed.path or "/"
        if parsed.query:
            target += f"?{parsed.query}"
        return self.get(self.study(target), cookie=cookie)

    def get(self, url, cookie=None, limit=20000):
        headers = dict(self.headers)
        if cookie:
            headers["Cookie"] = cookie
        request = urllib.request.Request(url, headers=headers)
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                return Response(response.status, response.headers.get("Location") or "",
                                response.headers.get("Set-Cookie") or "",
                                body=read_prefix(response, limit))
        except urllib.error.HTTPError as error:
            head = error.headers or {}
            return Response(error.code, head.get("Location") or "",
                            head.get("Set-Cookie") or "", body=read_prefix(error, limit))
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


def read_prefix(response, limit):
    """The start of a response body, decoded, for content assertions.

    Bounded on purpose: every marker asserted on sits well inside a page, and
    the one body that must be read whole (the corpus dump, ~126 KB) asks for
    the room explicitly.
    """
    try:
        return response.read(limit).decode("utf-8", "replace")
    except Exception:
        return ""


def dense_records():
    """The API dump's chapter records, in path order (empty if unreadable).

    Read rather than hard-coded so the probe keeps exercising files that exist
    after a restructure. The dump records the *rendered* `.html` path, which is
    what a browser — and this probe — must request.

    Cached: three probes need it and each call would otherwise re-parse the
    126 KB dump.
    """
    global _DENSE_RECORDS
    if _DENSE_RECORDS is None:
        try:
            with open(os.path.join(REPO_ROOT, "api", "index.json"),
                      encoding="utf-8") as handle:
                records = json.load(handle).get("chapters") or []
            _DENSE_RECORDS = sorted(
                [r for r in records
                 if isinstance(r, dict) and "/" in r.get("p", "") and r.get("t")],
                key=lambda record: record["p"],
            )
        except Exception:
            _DENSE_RECORDS = []
    return _DENSE_RECORDS


def chapter_path():
    """One real deep chapter path, from the committed API dump."""
    records = dense_records()
    return records[0]["p"] if records else None


def probe_sample(limit=0):
    """`(rendered path, title marker)` — deep chapters, at most one per stack.

    One chapter proves the pipeline; one per top-level stack proves it for every
    *render class* the corpus has (each stack has its own template, badge set and
    depth). Sampling the first path alphabetically instead would miss a break in
    any stack whose name sorts later — the difference between proving "the edge
    serves a chapter" and "the edge serves this corpus".
    """
    per_stack = {}
    for record in dense_records():
        path = record["p"]
        marker = render_marker(record["t"])
        if not marker:
            continue
        stack = path.split("/")[0]
        if stack not in per_stack:
            per_stack[stack] = (path, marker)
    sample = [per_stack[stack] for stack in sorted(per_stack)]
    return sample[:limit] if limit else sample


def public_paths():
    """The public surface, derived from the middleware that enforces it.

    A second hard-coded list here was the drift this repo gates against
    everywhere else and did not gate here: the probe checked three of the eight
    paths, so a path could lose its public status — or a new one could ship
    unprobed — with every check green. Read from the gate itself, so the list
    cannot be right in one place and wrong in the other.
    """
    try:
        with open(MIDDLEWARE_SOURCE, encoding="utf-8") as handle:
            block = PUBLIC_SET_RE.search(handle.read()).group(1)
        return tuple(re.findall(r'"([^"]+)"', block))
    except Exception:
        return ()


def intercepted_public_pages():
    """The paths `_middleware.ts` answers itself, before the asset layer runs.

    Read from the adapter, like `PUBLIC_AUTH_PATHS` is read from the gate that
    enforces it: a list restated here could stay green while the intercept
    moved.
    """
    try:
        with open(INTERCEPT_SOURCE, encoding="utf-8") as handle:
            return tuple(dict.fromkeys(INTERCEPT_PATH_RE.findall(handle.read())))
    except Exception:
        return ()


def direct_public_pages(paths):
    """Public paths served without the gate, so they must answer 200.

    Two mechanisms serve one directly: a file on disk (Pages resolves
    `/auth/login` to `auth/login.html`) and the middleware intercept (the OAuth
    callback, which has no file — an asset request would 308 to the clean URL
    and drop the `#access_token` fragment). Both sources are read, so removing
    a file cannot silently demote a path to "any answer will do".
    """
    intercepted = set(intercepted_public_pages())
    served = []
    for path in paths:
        rel = path.lstrip("/")
        if (path in intercepted
                or os.path.isfile(os.path.join(REPO_ROOT, rel))
                or os.path.isfile(os.path.join(REPO_ROOT, rel + ".html"))):
            served.append(path)
    return tuple(served)


def render_marker(title):
    """A 3+-word plain-prose run from a chapter title, or "" if there is none.

    A marker has to *identify* the page, not merely relate to it. One word is
    worthless — "Testing" or "WebSockets" appears in the navigation of every
    page in its section — and two words are weak, because this corpus
    cross-references chapter titles, so a fragment can appear in some other
    chapter's prose and a wrong page would pass. Only a full run of plain words
    (≥3 words, ≥12 characters) is evidence that this particular page was served.

    Punctuated runs are skipped rather than approximated: titles here mix prose
    with `—`, `:`, `/` and `&`, and matching one would mean reasoning about how
    the renderer escapes it. A title with no plain-prose run is dropped from the
    sample instead, so the assertion is never a guess.
    """
    candidates = [
        " ".join(words[:6])
        for words in (run.split() for run in re.split(r"[^A-Za-z0-9 ]+", title or ""))
        if len(words) >= 3 and sum(len(word) for word in words) >= 12
    ]
    return max(candidates, key=len, default="")


@check("Signed-in",
       "with the probe credential one real chapter per stack answers 200 and "
       "contains that chapter's own title — and without one the check warns, "
       "because the success path is then verified by unit tests alone")
def signed_in_render(probe):
    if not probe.probe_token:
        return [Result(WARN, "Signed-in", "signed-in render",
                       f"{PROBE_TOKEN_ENV} is not set, so only the blocked half of the "
                       f"gate is probed. Set it in Cloudflare Pages → Settings → "
                       f"Environment variables and as a repo secret to have the edge "
                       f"prove it serves a chapter to a valid session")]
    if not probe.probe_sample:
        return [Result(WARN, "Signed-in", "signed-in render",
                       "no chapter to probe: the API dump is unreadable, so there is "
                       "no title to assert on")]
    out, bodies = [], {}
    for chapter, marker in probe.probe_sample:
        response = probe.get(probe.study(f"/{chapter}"),
                             cookie=f"{PROBE_COOKIE}={probe.probe_token}")
        matched = (response.status == 200
                   and marker in response.body
                   and LOGIN_PATH not in response.body)
        bodies[chapter] = response.body
        out.append(verdict("Signed-in", f"signed-in {chapter}", matched, response,
                           f"expected 200 containing {marker!r} — a valid session must "
                           f"reach its chapter, and the page must be that chapter rather "
                           f"than a login page"))
    # Per-chapter markers prove each page says the right thing; this proves the
    # host is reading the path at all. An edge serving one cached response for
    # every chapter would satisfy a marker check only by coincidence.
    if len(bodies) > 1:
        distinct = len(set(bodies.values())) == len(bodies)
        out.append(Result(OK if distinct else FAIL, "Signed-in", "signed-in distinct pages",
                          f"{len(bodies)} chapters returned {len(set(bodies.values()))} "
                          f"distinct responses" if distinct else
                          f"{len(bodies)} different chapters returned identical bodies — "
                          f"the edge is not serving the requested path"))
    return out


def local_corpus_digest():
    """The digest this checkout's dump carries — what a current deploy must serve."""
    try:
        with open(os.path.join(REPO_ROOT, "api", "index.json"), encoding="utf-8") as handle:
            return json.load(handle).get("corpus_digest") or ""
    except Exception:
        return ""


def read_served_digest(response):
    """`(digest, why_unreadable)` from a served `/api/index.json`.

    Only one state is a deployment in flight: a valid digest from an older
    build. A response that carries no digest — any status, a body that is not
    JSON, or JSON without the field — is not this dump at this path, and no
    amount of waiting turns it into one. Reporting that as "the edge is older
    than HEAD" would send the operator to re-run a build that was never the
    problem, so it is named as what it is.
    """
    try:
        payload = json.loads(response.body)
    except Exception:
        payload = None
    digest = payload.get("corpus_digest") if isinstance(payload, dict) else None
    if not digest:
        return "", (f"the edge served {response.describe} with no corpus_digest "
                    f"({response.body[:60]!r}…) — that is not this dump at this "
                    f"path, so waiting for a build cannot fix it; check that "
                    f"/api/index.json is deployed and gated rather than shadowed")
    return digest, ""


@check("Freshness",
       "the deployment serves this checkout's corpus — `/api/index.json` carries the "
       "same digest, so an edge left behind HEAD cannot pass as current. With "
       "`--await-fresh` it waits for a deploy still in flight instead of failing on it")
def deployed_corpus_is_current(probe):
    if not probe.probe_token:
        return [Result(WARN, "Freshness", "deployed corpus",
                       f"{PROBE_TOKEN_ENV} is not set, so the digest cannot be read "
                       f"(/api/index.json is gated). Until it is, a deployment behind "
                       f"HEAD is indistinguishable from a current one — the exact state "
                       f"production sat in for fifteen hours on 2026-09-22")]
    expected = local_corpus_digest()
    if not expected:
        return [Result(WARN, "Freshness", "deployed corpus",
                       "api/index.json carries no corpus_digest — regenerate it with "
                       "python3 scripts/gen_master_index.py")]
    url = probe.study("/api/index.json")
    cookie = f"{PROBE_COOKIE}={probe.probe_token}"
    waited, deadline = 0, time.monotonic() + probe.await_fresh
    while True:
        response = probe.get(url, cookie=cookie, limit=1 << 21)
        served, unreadable = read_served_digest(response)
        caught_up = served == expected
        # Wait only on a valid digest from another build — the one state a
        # deploy in flight produces. An unreadable body is not that state, and
        # polling it for the full budget would stall the run before reporting
        # the misconfiguration it could have named on the first read.
        if caught_up or unreadable or time.monotonic() >= deadline:
            break
        waited += 1
        print(f"  … waiting for the deployment to reach this corpus "
              f"(served {served[:12]}, want {expected[:12]})", flush=True)
        time.sleep(min(probe.await_interval, max(0.0, deadline - time.monotonic())))
    if caught_up:
        why = ""
    elif unreadable:
        why = f" — {unreadable}"
    else:
        why = (f" carrying {served[:12]}… — the edge is older than HEAD"
               + (f" (waited {waited} time(s) for the deploy to land)" if waited else "")
               + ", so re-run the Pages build before trusting anything else here")
    return [verdict("Freshness", "deployed corpus",
                    response.status == 200 and caught_up, response,
                    f"expected 200 carrying corpus_digest {expected[:12]}… (this "
                    f"checkout); got {response.describe}" + why)]


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
       "every path the middleware lists as public answers as public — the static "
       "entry pages with 200, the rest with anything but the gated redirect")
def public_auth_surface(probe):
    paths = public_paths()
    if not paths:
        return [Result(WARN, "Public surface", "public surface source",
                       "could not read PUBLIC_AUTH_PATHS from "
                       "functions/_lib/study-access.mjs, so the public surface is "
                       "unverified — check the middleware source is where this probe "
                       "expects it")]
    direct = direct_public_pages(paths)
    out = []
    for path in paths:
        response = probe.get(probe.study(path))
        # A public path answers like a protected one only if the gate hands back
        # the login redirect that names *this* path as the deep link to return to.
        gated = (response.status == 302 and response.location.startswith(LOGIN_PATH)
                 and response.next_param() == path)
        if gated:
            out.append(Result(FAIL, "Public surface", f"public {path}",
                              f"{response.describe} — the gate is treating a path the "
                              f"middleware lists as public like a protected one, which "
                              f"breaks the flow that path belongs to"))
        elif path in direct:
            settled = probe.follow_same_host(response)
            detail = (f"{response.describe} -> {settled.describe}"
                      if settled is not response else response.describe)
            out.append(Result(OK if settled.status == 200 else FAIL,
                              "Public surface", f"public {path}",
                              f"served ({detail})" if settled.status == 200 else
                              f"a static entry page must reach 200 — got {detail}"))
        else:
            out.append(Result(OK, "Public surface", f"public {path}", response.describe))
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
    parser.add_argument("--probe-token", default=os.environ.get(PROBE_TOKEN_ENV, ""),
                        help=f"session credential for the success path (default: "
                             f"${PROBE_TOKEN_ENV})")
    parser.add_argument("--await-fresh", type=float, default=0,
                        help="seconds to wait for the deployment to reach this "
                             "checkout's corpus digest before judging it (0 = judge "
                             "immediately)")
    parser.add_argument("--await-interval", type=float, default=20,
                        help="seconds between polls while waiting")
    parser.add_argument("--probe-sample", type=int, default=0,
                        help="cap the sampled chapters (0 = one per stack) — for a "
                             "quick manual check of a single render class")
    args = parser.parse_args(argv)

    if args.print_contract:
        print("\n".join(f"  {c.label}: {c.expectation}" for c in CHECKS))
        return 0

    probe = Probe(args.scheme, args.study_host, args.pages_host,
                  args.denial_origin, args.denial_target, args.timeout,
                  args.probe_token, probe_sample(args.probe_sample),
                  args.await_fresh, args.await_interval)
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
