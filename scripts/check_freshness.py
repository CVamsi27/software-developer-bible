#!/usr/bin/env python3
"""Freshness gate: flag known stale-API signatures in docs.

Born from the Sept 2026 docs modernization audit. Each rule matches a
pattern that survived the audit as "outdated content shipped in a
chapter". The gate exists so these signatures fail verify.sh instead of
waiting for the next manual audit.

Rules are deliberately scoped (fence-language, file markers, allowlists)
to avoid false positives on teaching content — e.g. `params: { id: string }`
is correct for react-router and NestJS, and generateStaticParams RETURNS
plain param objects. When a Pages Router example is intentionally shown
in the Next.js stack, keep it inside the allowlisted directory.

Usage:
  python3 scripts/check_freshness.py                # report; exit 1 on hits
  python3 scripts/check_freshness.py --check-urls   # also probe a sample of
                                                    # external links for
                                                    # liveness (network;
                                                    # NOT part of verify.sh)
"""
import argparse
import concurrent.futures
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path
import md_fences
from scan_scope import guard

SKIP_DIRS = {'.git', 'node_modules', 'vendor', '_site', '.archive', '.freebuff', '.sass-cache'}
# The Next.js stack teaches Pages Router side-by-side with App Router
# (marked "Pages Router"); legacy names are intentional there.
PAGES_ROUTER_ALLOWED = ('10-frontend/10.4-next.js',)
# Historical restructure plans are records, not living docs.
SKIP_SUBSTRINGS = ('/docs/superpowers/',)

FAKE_ARCHIVE_TS = 'web.archive.org/web/20240701000000'

# RFC 9298 specifies HTTP UDP proxying, not WebTransport. Match an active
# citation whose label makes the wrong attribution; legitimate UDP references
# and fenced demonstrations of the bad link must remain valid.
WRONG_WEBTRANSPORT_RFC = re.compile(
    r'\[[^\]\n]*webtransport[^\]\n]*\]\(https?://(?:www\.)?'
    r'(?:rfc-editor\.org|datatracker\.ietf\.org)/[^)\s]*\brfc9298'
    r'(?:\.html|/|#[^)\s]*)?\)', re.I
)

# Retired OWASP cheat-sheet URL forms. OWASP renamed the site's cheat
# directory from cheat-sheets/ to cheatsheets/ (2026-09), breaking every
# link written the old way; owasp.org/cheatsheets/ (no subdomain) is a
# short-host variant that was never a stable citation target either.
# Discovered during the dead-link remediation sweep; see
# docs/superpowers/plans/2026-09-10-dead-link-remediation.md.
RETIRED_OWASP = re.compile(
    r'cheatsheetseries\.owasp\.org/cheat-sheets/'
    # The (?<![\w.]) guard keeps this branch from matching INSIDE the good
    # form: cheatsheetseries.owasp.org/cheatsheets/ contains
    # owasp.org/cheatsheets/ as a substring, preceded by a dot.
    r'|(?<![\w.])owasp\.org/cheatsheets/'
)

# Domains confirmed dead during the Sept 2026 remediation and the CI
# warn-mining pass (DNS gone, content retired, or a never-correct typo
# domain). A citation to any of these is rot the day it is written; the
# rule fails verify.sh so the class can never silently re-enter. Each
# replacement target used at remediation time is listed in
# docs/2026-09-11-dead-link-remediation-report.md.
# The (?<!\w) guard blocks letter-extended hostnames that merely contain a
# listed domain as a suffix substring — bundlephobia.com contains
# undlephobia.com after its first letter, notweave.works contains
# weave.works. Subdomain prefixes (www.weave.works) must still match, so
# a dot before the domain is allowed — dots are not word characters.
SHUTTERED_DOMAINS = re.compile(
    r'(?<!\w)'
    r'(?:weave\.works'             # Weaveworks shut down (2024)
    r'|complexityzoo\.net'         # DNS dead (root and wiki paths)
    r'|jstherightway\.org'
    r'|dassum\.io'
    r'|gdprtoday\.com'
    r'|georgestockera\.com'
    r'|saaslogy\.com'
    r'|programminglogs\.com'
    r'|blog\.rsbuild\.dev'         # Rsbuild blog now at rspack.rs/blog
    r'|blog\.savut\.se'
    r'|blog\.usejournal\.com'      # Medium publication retired
    r'|docs\.kata-containers\.io'  # real domain: katacontainers.io
    r'|learn\.branch\.io'          # moved to docs.branch.io
    r'|undlephobia\.com'           # typo of bundlephobia.com
    r'|bluecard-network\.de'
    r'|heim\.ifi\.uio\.no'        # UIO personal pages retired (broken SSL)
    r'|tacticaledge\.co'
    r')'
)

# --- EOL base-image pins (2026-09-19) ---------------------------------------
# ~55 Dockerfile examples pinned node majors that had passed end-of-life
# (18 EOL 2025-04, 20 EOL 2026-04); the corpus had even drifted against
# itself, with newer chapters on 20 and older ones on 18. This is a DATA
# table, not a regex list: when a pinned major reaches EOL, add its date
# here and every pin to it starts failing the same day. Date-gated, so
# adding a future EOL entry early is harmless — it stays silent until the
# date arrives. Extend the dict with other base images the same way.
# Keys are version STRINGS: bare major for single-number schemes (node),
# 'major.minor' for semver schemes (golang, python, rust) — go 1.21 and
# python 3.11 are different beasts from their bare majors.
EOL_BASE_IMAGES = {
    'node': {
        '14': date(2023, 4, 30),
        '16': date(2023, 9, 11),
        '18': date(2025, 4, 30),
        '20': date(2026, 4, 30),
    },
    # Go supports the last two majors; 1.21 lost support when 1.23 shipped
    # (2024-08-13). The corpus pinned it in the Go distroless examples.
    'golang': {
        '1.20': date(2024, 2, 6),
        '1.21': date(2024, 8, 13),
        '1.22': date(2025, 8, 12),
        '1.23': date(2026, 2, 10),
    },
    'python': {
        '3.8': date(2024, 10, 7),
        '3.9': date(2025, 10, 31),
        # 3.10 goes EOL 2026-10-31 — deliberately listed; the date gate
        # keeps it silent until then, which is the table's whole point.
        '3.10': date(2026, 10, 31),
    },
    'rust': {
        # Rust has no LTS: each minor is supported until the NEXT minor
        # ships (~6 weeks). Dates here are approximations for illustration
        # pins only; the real maintenance cost of exact per-minor dates is
        # not worth it, so rust pins carry a deliberately loose floor.
        '1.70': date(2024, 1, 1),
        '1.71': date(2024, 2, 1),
        '1.72': date(2024, 3, 1),
    },
    'ghcr.io/graalvm/native-image': {
        # GraalVM for JDK 17 reached Oracle Premier end (2026-06) and the
        # community line moved to JDK 21+; the old ghcr tag family is
        # effectively unmaintained for new work.
        '17': date(2026, 6, 1),
    },
}
EOL_NODE_RUNTIMES = {
    '18': date(2025, 4, 30),
    '20': date(2026, 4, 30),
}
NODE_RUNTIME_PIN = re.compile(
    r'''(?ix)\b(?:node-version\s*:\s*|NODE_VERSION\s*[:=]\s*|'''
    r'''nodeVersion\s*(?:\?:|=)\s*|Runtime\s*:\s*|runtime\s*:\s*|'''
    r'''nodejs|node:)['"]?(18|20)'''
    r'''(?:\.x|(?:\.\d+){1,2}|-[\w.]+)?(?=[\s'"),#]|$)'''
)
FROM_PIN = re.compile(
    r'\bFROM\s+((?:[a-z0-9/_.-]+)?(?:golang|node|python|rust|ghcr\.io/graalvm/native-image))'
    r':(\d+)(\.(\d+))?(?:[\s-]|$)')

# --- EOL GitHub Action pins (2026-09-23) ------------------------------------
# GitHub removed the Node 20 action runner on this date. These releases bundle
# Node 20 and therefore need upgrading even if their action major is otherwise
# supported. Older retired majors remain listed as well. Unlisted majors stay
# silent (unknown, not wrong).
EOL_GITHUB_ACTIONS = {
    'actions/checkout': {'v2': date(2022, 8, 15), 'v3': date(2024, 8, 15), 'v4': date(2026, 9, 23)},
    'actions/setup-node': {'v2': date(2022, 8, 15), 'v3': date(2024, 8, 15), 'v4': date(2026, 9, 23)},
    'actions/cache': {'v2': date(2022, 8, 15), 'v3': date(2024, 8, 15)},
    'actions/upload-artifact': {'v2': date(2022, 8, 15), 'v3': date(2024, 8, 15), 'v4': date(2026, 9, 23), 'v5': date(2026, 9, 23)},
    'actions/upload-pages-artifact': {'v3': date(2026, 9, 23), 'v4': date(2026, 9, 23)},
    'actions/deploy-pages': {'v4': date(2026, 9, 23)},
    'docker/build-push-action': {'v5': date(2026, 9, 23), 'v6': date(2026, 9, 23)},
    'docker/login-action': {'v3': date(2026, 9, 23)},
    'docker/metadata-action': {'v5': date(2026, 9, 23)},
    'aws-actions/configure-aws-credentials': {'v4': date(2026, 9, 23), 'v5': date(2026, 9, 23)},
    'codecov/codecov-action': {'v3': date(2024, 8, 1), 'v4': date(2026, 9, 23), 'v5': date(2026, 9, 23)},
    'github/codeql-action': {'v2': date(2024, 8, 15), 'v3': date(2026, 9, 23)},
    'googleapis/release-please-action': {'v4': date(2026, 9, 23)},
    'slsa-framework/slsa-github-generator': {'v1': date(2026, 9, 23)},
    'treosh/lighthouse-ci-action': {'v11': date(2026, 9, 23)},
}
USES_PIN = re.compile(r'\buses:\s*([\w.-]+/[\w.-]+)@v(\d+)\b')
MUTABLE_ACTION_REF = re.compile(
    r'\buses:\s*[\w.-]+/[\w.-]+@(master|main|develop|dev|trunk)\b', re.I)

# --- Obsolete Compose version: key (2026-09-19) -----------------------------
# Compose V2 ignores the top-level version field and warns "the attribute
# version is obsolete" on every run; the Compose Spec removed it. Two guards
# keep the rule off everything else: the key must sit at column 0 (top-level
# — Helm chart version: lives nested under the chart root) and the value must
# match the historical Compose file scheme (bare major 2/3, major.minor, or
# major.minor.patch — Helm pins like "12.x.x" and app/package versions like
# "1.0.0" never match the scheme).
COMPOSE_VERSION_KEY = re.compile(
    r'^version: ["\']([23](?:\.\d+){0,2})["\']\s*(?:#.*)?$')

# Two verified frontend API regressions (2026-10-01). The hydration
# matcher is anchored to the options object of the actual call, so a
# user-defined onHydrated callback elsewhere remains legitimate.
HYDRATION_OPTIONS = re.compile(
    r'\bhydrateRoot\s*\(\s*[^,\n]+,\s*[^,\n]+,\s*\{'
    r'[^}]*?\bonHydrated\s*:'
)
NEXT_GEO = re.compile(r'\b(?:request|req)\.geo\b')

# MSW v2 replaced the v1 rest API with http/HttpResponse. Only match
# executable import declarations, preserving prose about migration.
MSW_REST_IMPORT = re.compile(
    r"\bimport\s*\{[^}]*\brest\b[^}]*\}\s*from\s*['\"]msw['\"]"
)

NEST_LAZY_IMPORT = re.compile(
    r"\bimport\s*\{[^}]*\bLazyModule\b[^}]*\}\s*from\s*['\"]@nestjs/core['\"]"
)

# API regressions verified against current upstream docs (2026-10-07).
# PubSub matches only receivers constructed by the built-in implementation;
# third-party adapters can legitimately retain asyncIterator.
BUILTIN_PUBSUB = re.compile(r"\b(?:const|let)\s+(\w+)\s*=\s*new\s+PubSub(?:<[^;]+?>)?\s*\(")
GSAP_CSS_EASE = re.compile(r"\bease\s*:\s*['\"]cubic-bezier\s*\(")
FABRICATED_WS_IMPORT = re.compile(r"\bfrom\s*['\"]ws\.use/server['\"]")
# Zod 4 moves string format validators to the top-level namespace. The
# chained forms continue to work but are deprecated; examples should use
# z.email(), z.uuid(), and their peers.
ZOD4_DEPRECATED_STRING_FORMAT = re.compile(
    r"\bz\.string\(\)\.(?:email|uuid|url|datetime|date|time|ip|cidr)\s*\(")

# RFC9745 defines a Structured Field Date, not the older boolean examples.
BOOLEAN_DEPRECATION_HEADER = re.compile(r'^\s*Deprecation\s*:\s*true\s*$', re.I)
# Current teaching cites Revision2. Historical records outside teaching stacks
# may retain their then-current sources; a fenced citation is an illustration.
WITHDRAWN_NIST_SANITIZATION = re.compile(
    r'\]\(https?://csrc\.nist\.gov/pubs/sp/800/88/r1/final(?:#[^)]*)?\)', re.I)

# Minimum versions checked against the versioned PostgreSQL manuals on
# 2026-10-25. Availability on 18 is valid; claiming introduction there is not.
WRONG_PG_EXPLAIN_INTRODUCTION = re.compile(
    r'(?:PostgreSQL\s+18\s+(?:introduced|introduces|adds|added)\s+'
    r'(?:support\s+for\s+)?`?(?:GENERIC_PLAN|SERIALIZE)\b|'
    r'`?(?:GENERIC_PLAN|SERIALIZE)`?\s+(?:was\s+)?(?:introduced|added|new)\s+'
    r'(?:in|with)\s+PostgreSQL\s+18\b)', re.I)

RULES = [
    ('UNQUALIFIED-LAMBDA-TIMEOUT',
     'Default-capacity Lambda has a fifteen-minute ceiling; supported Managed '
     'Instances triggers allow up to ninety minutes'),
    ('GENERIC-TESTCONTAINERS2-POSTGRES',
     'The Testcontainers 2 org.testcontainers.postgresql.PostgreSQLContainer '
     'class is non-generic; old-package generic examples remain valid'),
    ('FALSE-K6-CHECKS-LIMITATION',
     'The k6 checks metric supports thresholds; bare failed checks alone '
     'do not change the process exit status'),
    ('WRONG-PG-EXPLAIN-INTRODUCTION',
     'GENERIC_PLAN starts in PostgreSQL16 and SERIALIZE in17; '
     'neither was introduced in18'),
    ('UNSAFE-JSONLD-UNICODE-ESCAPE',
     'A JavaScript Unicode escape evaluates back to <; JSON-LD serialization '
     'needs a literal backslash-u sequence to protect the script boundary'),
    ('FABRICATED-TANSTACK-QUERY-API',
     'TanStack Query uses onSettled and hydrate/HydrationBoundary; '
     'onSettle and rehydrate are not its mutation/hydration APIs'),
    ('BOOLEAN-DEPRECATION-HEADER',
     'RFC9745 Deprecation uses a Structured Field Date such as @1790812800, not true'),
    ('WITHDRAWN-NIST-SANITIZATION-CITATION',
     'Current media-sanitization teaching must cite NIST SP800-88 Revision2; Revision1 was withdrawn'),
    ('FABRICATED-PAGE-HEAP-COMMAND',
     'Heap snapshots require DevTools or a debugging-protocol session; '
     'window.chrome.sendCommand is not a page API'),
    ('FABRICATED-LHCI-FUNCTION-API',
     'Lighthouse CI exposes its documented CLI commands, not start/upload '
     'function exports from @lhci/cli'),
    ('REMOVED-LIGHTHOUSE-INTERACTIVE',
     'Standard Lighthouse removed Time to Interactive in version 10; '
     'use supported audit IDs and separate field INP measurement'),
    ('AXE-PLAYWRIGHT-CONTEXT',
     'AxeBuilder needs an explicit Playwright browser context; create a '
     'context with browser.newContext(), then context.newPage()'),
    ('FABRICATED-RECHARTS-ACCESSIBILITY-COMPONENT',
     'Recharts exposes accessibilityLayer as a chart prop, not an '
     'AccessibilityLayer component export'),
    ('FABRICATED-K6-MEMORY-METRIC',
     'k6 has no builtin vus_memory metric; observe application memory '
     'through real telemetry or explicitly define and populate a custom metric'),
    ('WRONG-WEBTRANSPORT-RFC',
     'RFC 9298 defines HTTP UDP proxying, not WebTransport; cite the '
     'WebTransport specification or its HTTP/3 draft'),
    ('INSTANCE-TEMPORAL-REPLAY', 'Temporal replay helpers are static Worker methods; use Worker.runReplayHistory or consume Worker.runReplayHistories'),
    ('STATIC-SCROLLTRIGGER-KILL', 'kill() belongs to a ScrollTrigger instance; revert the owned context or kill the owned trigger'),
    ('GSAP-CSS-EASE-STRING', 'GSAP needs a registered CustomEase or a supported easing name, not a raw CSS cubic-bezier string'),
    ('OBSOLETE-BUILTIN-PUBSUB-ITERATOR', 'graphql-subscriptions v3 built-in PubSub uses asyncIterableIterator; check third-party adapter APIs separately'),
    ('FABRICATED-GRAPHQL-WS-IMPORT', 'useServer comes from graphql-ws/use/ws, not ws.use/server'),
    ('FABRICATED-NEST-LAZY-MODULE',
     'Nest exposes LazyModuleLoader, not a LazyModule decorator from @nestjs/core'),
    ('OBSOLETE-MSW-REST',
     'MSW v1 rest import; use current http and HttpResponse APIs'),
    ('DEPRECATED-ZOD4-STRING-FORMAT',
     'Zod 4 deprecates chained string format validators; use top-level z.email(), z.uuid(), z.url(), or z.iso.*()'),
    ('UNSUPPORTED-HYDRATION-CALLBACK',
     'hydrateRoot has no onHydrated option; use documented error callbacks '
     'and a component effect for mount-related work'),
    ('REMOVED-NEXT-GEO',
     'NextRequest.geo was removed in Next.js 15; use trusted hosting '
     'provider headers or an explicit geolocation service'),
    ('FAKE-ARCHIVE-TS',
     'fabricated web.archive.org timestamp (20240701000000); cite the live URL instead'),
    ('RETIRED-OWASP-CHEATSHEET',
     'retired OWASP cheat-sheet URL form (cheat-sheets/ or short host); '
     'cite cheatsheetseries.owasp.org/cheatsheets/<Name>.html'),
    ('SHUTTERED-DOMAIN',
     'cites a domain confirmed dead in the Sept 2026 remediation; '
     're-cite a live home (replacements listed in '
     'docs/2026-09-11-dead-link-remediation-report.md)'),
    ('STALE-GOOGLE-WEB-TREE',
     'developers.google.com/web/ is retired; cite web.dev or developer.chrome.com'),
    ('LEGACY-PAGES-ROUTER-EXPORT',
     'getStaticProps/getServerSideProps export outside the Next.js stack; '
     'move into 10.4-next.js or rewrite with App Router APIs'),
    ('SYNC-PARAMS',
     'sync params type in a Next.js context; params/searchParams are Promises '
     'since Next.js 15 — use Promise<{...}> and await'),
    ('DEPRECATED-URL-PARSE',
     'url.parse() is legacy; use new URL() and searchParams'),
    ('NEW-BUFFER',
     'new Buffer() is deprecated; use Buffer.from/alloc/allocUnsafe'),
    ('SETTIMEOUT-CHUNKING',
     'old setTimeout chunking pattern; prefer scheduler.yield() time-slicing'),
    ('DUPLICATE-FOOTER',
     'file carries more than one "[ Back to Index]" footer — an old merge '
     'grafted repeated tails; keep exactly one footer at EOF'),
    ('STRAY-GRAFT-HEADER',
     'a "# Phase/Part/Section N" H1 grafted into a chapter file (chapters '
     'structure with ##; only the 81-lanes guides use # Phase at top level) — '
     'delete the stray header'),
    ('EOL-BASE-IMAGE',
     'base-image pin past its end-of-life (data table EOL_BASE_IMAGES, '
     'compared against today); bump to a supported LTS major'),
    ('EOL-NODE-RUNTIME',
     'Node.js runtime pin past its end-of-life (data table EOL_NODE_RUNTIMES, '
     'compared against today); upgrade the CI, container or hosted runtime'),
    ('EOL-GITHUB-ACTION',
     'GitHub Action release uses a removed runner or is retired upstream '
     '(data table EOL_GITHUB_ACTIONS, compared against today); bump to a '
     'Node 24-compatible release'),
    ('MUTABLE-GITHUB-ACTION-REF',
     'GitHub Action is pinned to a moving branch; use a reviewed full commit SHA'),
    ('OBSOLETE-COMPOSE-VERSION',
     'top-level version: key in a Compose file (Compose V2 ignores it and '
     'warns "the attribute version is obsolete"); delete the line — the '
     'Compose Spec has no version field'),
]

FOOTER_LINK = '[ Back to Index](INDEX.md)'
STRAY_PHASE_HEADER = re.compile(r'^# (Phase|Part|Section) \d', re.M)
# Whole-document guides legitimately structured as # Phase N sections.
PHASE_GUIDE_ALLOWED = ('81-lanes-indian-sde-faang',)

SYNC_PARAMS = re.compile(r'params:\s*\{\s*\w+:\s*string\s*\}\s*\}')
NEXT_MARKERS = re.compile(
    r"from 'next|next/navigation|next/headers|generateStaticParams|"
    r"generateMetadata|use cache|app/\w|'use client'"
)

MD_LINK_URL = re.compile(r'\]\((https?://[^)\s]+)\)')


def repair_url(text: str, m) -> str:
    """Re-attach trailing ')' belonging to URLs like Wikipedia's
    ...Closure_(computer_programming) that the regex truncates."""
    u = m.group(1)
    end = m.end(1)
    while u.count('(') > u.count(')') and end < len(text) and text[end] == ')':
        u += ')'
        end += 1
    return u
# Hosts/domains that are badges or illustrative examples — never probe.
URL_SKIP = ('img.shields.io', 'example.com', 'example.org', 'example.net',
            'localhost', '127.0.0.1')
HEADERS = {
    'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'),
    'Accept': 'text/html,application/xhtml+xml',
}
# Second-chance headers for 403/429/503: WAFs (Cloudflare, Akamai) reject
# requests that lack the full browser fingerprint even with a browser UA.
# One retry with the standard header set converts most bot-wall false
# warns into correct LIVE verdicts; hosts that still block (O'Reilly,
# ACM) are genuinely bot-walled and stay WARN — that is signal, not noise.
BROWSER_FALLBACK_HEADERS = {
    **HEADERS,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}


def collect_external_urls(root: Path):
    urls = set()
    malformed = set()
    for p, rel in iter_md_files(root):
        # Job applications and personal targets are historical records —
        # expired listings there are expected, not doc rot.
        if '/personal/' in f'/{rel}':
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        for m in MD_LINK_URL.finditer(text):
            u = repair_url(text, m)
            if any(s in u for s in URL_SKIP):
                continue
            if not u.isascii():
                # Non-ASCII in a URL is invalid (HTTP headers are latin-1);
                # these are broken doc links, not probe targets.
                malformed.add(u)
                continue
            urls.add(u)
    return sorted(urls), sorted(malformed)


def probe(url: str):
    """Return (status, detail). Status: LIVE | DEAD | WARN.

    GET-first: many sites (PortSwigger, etc.) return 404 for HEAD but
    serve GET fine, so HEAD-first produced mass false DEADs. The body is
    never read — the connection is closed immediately. Retry policy:
    404/410 is retried as-is once (absorbs transient site outages like
    OWASP mid-deploy); 403/429/503 is retried once with full browser
    headers (absorbs WAF fingerprinting), honoring Retry-After on 429.
    """
    last = ('WARN', 'no response')
    for attempt, headers in enumerate((HEADERS, BROWSER_FALLBACK_HEADERS)):
        try:
            req = urllib.request.Request(url, headers=headers, method='GET')
            with urllib.request.urlopen(req, timeout=10) as resp:
                resp.read(1)  # touch the stream; do not download the body
                return 'LIVE', f'HTTP {resp.status}'
        except urllib.error.HTTPError as e:
            code = e.code
            if code == 429:
                ra = e.headers.get('Retry-After') if e.headers else None
                time.sleep(min(int(ra), 6) if (ra or '').isdigit() else 4)
                continue
            if code in (403, 503):
                time.sleep(0.5)
                continue
            if code in (404, 410):
                if attempt == 0:
                    time.sleep(0.5)
                    continue
                return 'DEAD', f'HTTP {code}'
            return 'WARN', f'HTTP {code} (bot-blocked or rate-limited?)'
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            reason = getattr(e, 'reason', e)
            last = ('WARN', f'unreachable: {reason}')
    return last


def check_urls(root: Path, sample: int):
    urls, malformed = collect_external_urls(root)
    if malformed:
        print(f'{len(malformed)} malformed (non-ASCII) link(s) — fix in source doc:')
        for u in malformed:
            print(f'  MALFORMED  {u}')
        print()
    # Deterministic stride sampling — same set every run on the same tree.
    picked = urls if len(urls) <= sample else urls[:: len(urls) // sample][:sample]
    print(f'--check-urls: probing {len(picked)} of {len(urls)} external links '
          f'(deterministic sample)...\n')
    dead = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for url, (status, detail) in zip(picked, ex.map(probe, picked)):
            mark = {'LIVE': 'ok', 'DEAD': 'DEAD', 'WARN': 'warn'}[status]
            print(f'  {mark:4}  {detail:40}  {url}')
            if status == 'DEAD':
                dead.append(url)
    print()
    if dead:
        print(f'{len(dead)} dead link(s) — fix or re-cite in the source doc.')
        return 1
    if malformed:
        print('All sampled links answered, but malformed links must be fixed.')
        return 1
    print('All sampled links answered (warnings are usually bot-blocks, not rot).')
    return 0


def iter_md_files(root: Path):
    for p in sorted(root.rglob('*.md')):
        rel = p.relative_to(root).as_posix()
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if any(s in f'/{rel}' for s in SKIP_SUBSTRINGS):
            continue
        yield p, rel


def check(p: Path, rel: str):
    hits = []
    text = p.read_text(encoding='utf-8', errors='replace')
    in_code = False
    lang = ''
    code_rows = []
    for lineno, line, inf, isf in md_fences.walk(text.splitlines()):
        lineno += 1  # md_fences.walk emits zero-based offsets; diagnostics use source lines.
        stripped = line.lstrip()
        if isf:
            if not inf and code_rows:
                source = '\n'.join(row for _, row in code_rows)
                if lang == 'java' and re.search(
                        r'\bimport\s+org\.testcontainers\.postgresql\.PostgreSQLContainer\s*;', source):
                    for match in re.finditer(r'\bPostgreSQLContainer\s*<', source):
                        offset = source.count('\n', 0, match.start())
                        hits.append((code_rows[offset][0], 'GENERIC-TESTCONTAINERS2-POSTGRES',
                                     code_rows[offset][1].strip()[:100]))
                for match in re.finditer(
                        r"\bchrome\s*(?:\?\.)?\s*\.?\s*sendCommand\s*(?:\?\.)?\s*\(\s*['\"]HeapProfiler\.takeHeapSnapshot['\"]", source):
                    offset = source.count('\n', 0, match.start())
                    hits.append((code_rows[offset][0], 'FABRICATED-PAGE-HEAP-COMMAND',
                                 code_rows[offset][1].strip()[:100]))
                for match in re.finditer(
                        r"\bimport\s*\{[^}]*?\b(?:start|upload)\b[^}]*?\}\s*from\s*['\"]@lhci/cli['\"]", source):
                    offset = source.count('\n', 0, match.start())
                    hits.append((code_rows[offset][0], 'FABRICATED-LHCI-FUNCTION-API',
                                 code_rows[offset][1].strip()[:100]))
                if ('Lighthouse CI' in text or 'lighthouserc' in text) and 'assertions' in source:
                    for match in re.finditer(r"(?:['\"]interactive['\"]|\binteractive)\s*:\s*\[", source):
                        offset = source.count('\n', 0, match.start())
                        hits.append((code_rows[offset][0], 'REMOVED-LIGHTHOUSE-INTERACTIVE',
                                     code_rows[offset][1].strip()[:100]))
                if '@axe-core/playwright' in source:
                    for match in re.finditer(
                            r'\b(?:const|let)\s+(\w+)\s*=\s*await\s+browser\.newPage\s*\(', source):
                        page = re.escape(match.group(1))
                        axe_page = re.search(
                            r'new\s+AxeBuilder\s*\(\s*\{[^}]*?'
                            r'(?:\bpage\s*:\s*' + page + r'\b|\b' + page + r'(?=\s*[,}]))', source)
                        if axe_page:
                            offset = source.count('\n', 0, match.start())
                            hits.append((code_rows[offset][0], 'AXE-PLAYWRIGHT-CONTEXT',
                                         code_rows[offset][1].strip()[:100]))
                for match in re.finditer(
                        r"\bimport\s*\{[^}]*?\bAccessibilityLayer\b[^}]*?\}\s*from\s*['\"]recharts['\"]", source):
                    offset = source.count('\n', 0, match.start())
                    hits.append((code_rows[offset][0], 'FABRICATED-RECHARTS-ACCESSIBILITY-COMPONENT',
                                 code_rows[offset][1].strip()[:100]))
                memory_threshold = re.search(r"(?:['\"]vus_memory['\"]|\bvus_memory)\s*:", source)
                custom_memory = re.search(
                    r"new\s+(?:[\w$.]+\.)?(?:Rate|Trend|Gauge|Counter)\s*\(\s*['\"]vus_memory['\"]", source)
                if memory_threshold and not custom_memory and re.search(r"from\s*['\"]k6(?:/[^'\"]*)?['\"]", text):
                    offset = source.count('\n', 0, memory_threshold.start())
                    hits.append((code_rows[offset][0], 'FABRICATED-K6-MEMORY-METRIC',
                                 code_rows[offset][1].strip()[:100]))
                if re.search(r"from\s*['\"]@temporalio/worker['\"]", source):
                    receivers = re.findall(r'\b(?:const|let)\s+(\w+)\s*=\s*await\s+Worker\.create\s*\(', source)
                    for receiver in receivers:
                        for match in re.finditer(r'\b' + re.escape(receiver) + r'\.runReplayHistor(?:y|ies)\s*\(', source):
                            offset = source.count('\n', 0, match.start())
                            hits.append((code_rows[offset][0], 'INSTANCE-TEMPORAL-REPLAY', code_rows[offset][1].strip()[:100]))
                for match in FABRICATED_WS_IMPORT.finditer(source):
                    offset = source.count('\n', 0, match.start())
                    hits.append((code_rows[offset][0], 'FABRICATED-GRAPHQL-WS-IMPORT', code_rows[offset][1].strip()[:100]))
                if re.search(r"from\s*['\"]graphql-subscriptions['\"]", source):
                    for receiver in BUILTIN_PUBSUB.findall(source):
                        for match in re.finditer(r'\b' + re.escape(receiver) + r'\.asyncIterator\s*\(', source):
                            offset = source.count('\n', 0, match.start())
                            hits.append((code_rows[offset][0], 'OBSOLETE-BUILTIN-PUBSUB-ITERATOR', code_rows[offset][1].strip()[:100]))
                for match in NEST_LAZY_IMPORT.finditer(source):
                    offset = source.count('\n', 0, match.start())
                    hits.append((code_rows[offset][0], 'FABRICATED-NEST-LAZY-MODULE',
                                 code_rows[offset][1].strip()[:100]))
                for match in MSW_REST_IMPORT.finditer(source):
                    offset = source.count('\n', 0, match.start())
                    hits.append((code_rows[offset][0], 'OBSOLETE-MSW-REST',
                                 code_rows[offset][1].strip()[:100]))
                for match in HYDRATION_OPTIONS.finditer(source):
                    offset = source.count('\n', 0, match.end())
                    hits.append((code_rows[offset][0], 'UNSUPPORTED-HYDRATION-CALLBACK',
                                 code_rows[offset][1].strip()[:100]))
            code_rows = []
            # inf is the state after this fence line: True means it opened.
            in_code = inf
            lang = stripped.lstrip('`~').strip() if inf else ''
            continue

        if in_code and lang.lower() in ('http', 'https') and BOOLEAN_DEPRECATION_HEADER.match(line):
            hits.append((lineno, 'BOOLEAN-DEPRECATION-HEADER', line.strip()[:100]))
        if (not in_code and rel.startswith(('20-backend/', '30-architecture/', '40-platform/'))
                and WITHDRAWN_NIST_SANITIZATION.search(line)):
            hits.append((lineno, 'WITHDRAWN-NIST-SANITIZATION-CITATION', line.strip()[:100]))
        if (not in_code and rel.startswith(('20-backend/', '30-architecture/'))
                and WRONG_PG_EXPLAIN_INTRODUCTION.search(line)):
            hits.append((lineno, 'WRONG-PG-EXPLAIN-INTRODUCTION', line.strip()[:100]))
        if (not in_code and rel.startswith('50-quality/50.1-testing/') and re.search(
                r'\bbuilt-in\s+`?checks`?\s+metric\s+cannot\s+(?:itself\s+)?be\s+'
                r'(?:used\s+in\s+a\s+threshold|thresholded)', line, re.I)):
            hits.append((lineno, 'FALSE-K6-CHECKS-LIMITATION', line.strip()[:100]))

        if (not in_code and rel.startswith('40-platform/40.7-serverless-edge/')
                and re.search(r'^(?:\*\*(?:A|Answer):\*\*\s*)?Lambda\s+'
                              r'(?:has|always has)\s+a\s+15-minute\s+invocation\s+maximum',
                              line, re.I)):
            hits.append((lineno, 'UNQUALIFIED-LAMBDA-TIMEOUT', line.strip()[:100]))

        if not in_code and WRONG_WEBTRANSPORT_RFC.search(line):
            hits.append((lineno, 'WRONG-WEBTRANSPORT-RFC', line.strip()[:100]))

        if FAKE_ARCHIVE_TS in line:
            hits.append((lineno, 'FAKE-ARCHIVE-TS', line.strip()[:100]))
        m_owasp = RETIRED_OWASP.search(line)
        if m_owasp:
            hits.append((lineno, 'RETIRED-OWASP-CHEATSHEET', line.strip()[:100]))
        if SHUTTERED_DOMAINS.search(line):
            hits.append((lineno, 'SHUTTERED-DOMAIN', line.strip()[:100]))
        if 'developers.google.com/web/' in line:
            hits.append((lineno, 'STALE-GOOGLE-WEB-TREE', line.strip()[:100]))
        # EOL base-image pins: date-compared against the data table. The
        # regex anchors on the FROM instruction and requires a delimiter
        # after the major (./-/space/EOL), so node:22-alpine matches but
        # node:2 (a truncated pin) and node:2x never do — and unversioned
        # majors (no entry in the table) stay silent.
        m_pin = FROM_PIN.search(line)
        if m_pin:
            image = m_pin.group(1)
            # Semver-style images (golang, rust, python) key on MAJOR.MINOR —
            # go 1.21 and go 1.2 are different releases — so the lookup key
            # carries the minor when present, the bare major otherwise (node).
            minor = m_pin.group(4)
            version = f'{m_pin.group(2)}.{minor}' if minor else m_pin.group(2)
            eol = EOL_BASE_IMAGES.get(image, {}).get(version)
            if eol and date.today() >= eol:
                hits.append((lineno, 'EOL-BASE-IMAGE',
                             f'{image}:{version} EOL since {eol.isoformat()} — '
                             f'{line.strip()[:70]}'))
        m_node_runtime = NODE_RUNTIME_PIN.search(line)
        if m_node_runtime:
            version = m_node_runtime.group(1)
            eol = EOL_NODE_RUNTIMES[version]
            # Dockerfile FROM pins already produce the more specific
            # EOL-BASE-IMAGE finding above.
            is_node_from = bool(re.search(r'\bFROM\s+node:(?:18|20)\b', line, re.I))
            if date.today() >= eol and not is_node_from:
                hits.append((lineno, 'EOL-NODE-RUNTIME',
                             f'Node.js {version} EOL since {eol.isoformat()} — '
                             f'{line.strip()[:70]}'))
        m_use = USES_PIN.search(line)
        if m_use:
            action, vmajor = m_use.group(1), 'v' + m_use.group(2)
            eol = EOL_GITHUB_ACTIONS.get(action, {}).get(vmajor)
            if eol and date.today() >= eol:
                hits.append((lineno, 'EOL-GITHUB-ACTION',
                             f'{action}@{vmajor} runner unsupported since '
                             f'{eol.isoformat()} — {line.strip()[:60]}'))
        if in_code and lang.lower() in ('yaml', 'yml') and MUTABLE_ACTION_REF.search(line):
            hits.append((lineno, 'MUTABLE-GITHUB-ACTION-REF', line.strip()[:100]))
        if COMPOSE_VERSION_KEY.match(line):
            hits.append((lineno, 'OBSOLETE-COMPOSE-VERSION',
                         f'obsolete top-level version key — {line.strip()[:70]}'))

        if in_code and lang in ('json', 'java'):
            code_rows.append((lineno, re.sub(r'//.*$', '', line) if lang == 'java' else line))

        if in_code and lang in ('typescript', 'tsx', 'javascript', 'js'):
            # Strip line comments so explanatory notes like
            # "// url.parse() is deprecated" don't self-trigger.
            # (?<!:) avoids https://, (?!/) avoids protocol-relative //.
            code_line = re.sub(r'(?<!:)//(?!/).*$', '', line)
            code_rows.append((lineno, code_line))
            if 'application/ld+json' in text and re.search(
                    r"\.replace\(\s*/</g,\s*(['\"])\\u003[cC]\1", code_line):
                hits.append((lineno, 'UNSAFE-JSONLD-UNICODE-ESCAPE', line.strip()[:100]))
            if ('TanStack Query' in text or '@tanstack/react-query' in text) and re.search(
                    r'\bonSettle\s*:|\brehydrate\s*\(', code_line):
                hits.append((lineno, 'FABRICATED-TANSTACK-QUERY-API', line.strip()[:100]))
            if ZOD4_DEPRECATED_STRING_FORMAT.search(code_line):
                hits.append((lineno, 'DEPRECATED-ZOD4-STRING-FORMAT', line.strip()[:100]))
            if re.search(r'\bScrollTrigger\.kill\s*\(', code_line):
                hits.append((lineno, 'STATIC-SCROLLTRIGGER-KILL', line.strip()[:100]))
            if ('gsap' in rel.lower() or re.search(r'\bgsap\.', text)) and GSAP_CSS_EASE.search(code_line):
                hits.append((lineno, 'GSAP-CSS-EASE-STRING', line.strip()[:100]))
            if rel.startswith('10-frontend/10.4-next.js/') and NEXT_GEO.search(code_line):
                hits.append((lineno, 'REMOVED-NEXT-GEO', line.strip()[:100]))
            is_next_context = rel.startswith(PAGES_ROUTER_ALLOWED) or bool(
                NEXT_MARKERS.search(text)
            )
            if re.search(r'export\s+(async\s+)?(const\s+)?(getStaticProps|getServerSideProps|'
                         r'GetStaticProps|GetServerSideProps)', code_line):
                if not rel.startswith(PAGES_ROUTER_ALLOWED):
                    hits.append((lineno, 'LEGACY-PAGES-ROUTER-EXPORT', line.strip()[:100]))
            if SYNC_PARAMS.search(code_line) and is_next_context:
                hits.append((lineno, 'SYNC-PARAMS', line.strip()[:100]))
            if re.search(r'\burl\.parse\s*\(', code_line):
                hits.append((lineno, 'DEPRECATED-URL-PARSE', line.strip()[:100]))
            if re.search(r'new\s+Buffer\s*\(', code_line):
                hits.append((lineno, 'NEW-BUFFER', line.strip()[:100]))
            if 'setTimeout(processChunk, 0)' in code_line:
                hits.append((lineno, 'SETTIMEOUT-CHUNKING', line.strip()[:100]))

    # Structural grafts (found Sept 2026): an old automated merge pasted
    # repeated page tails and Phase headers into chapter files.
    if text.count(FOOTER_LINK) > 1:
        second = text.find(FOOTER_LINK, text.find(FOOTER_LINK) + 1)
        ln = text.count('\n', 0, second) + 1
        hits.append((ln, 'DUPLICATE-FOOTER',
                     f'{text.count(FOOTER_LINK)} footers; keep exactly one'))
    if '## Summary' in text and not rel.startswith(PHASE_GUIDE_ALLOWED):
        m = STRAY_PHASE_HEADER.search(text)
        if m:
            ln = text.count('\n', 0, m.start()) + 1
            hits.append((ln, 'STRAY-GRAFT-HEADER',
                         text[m.start():m.end()] + ' — top-level Phase header '
                         'inside a chapter file'))
    return hits


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--check-urls', nargs='?', const=15, type=int, metavar='N',
                        help='probe a deterministic sample of N external links '
                             '(default 15) for liveness; requires network')
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    if args.check_urls is not None:
        sys.exit(check_urls(root, args.check_urls))

    all_hits = []
    n_files = 0
    for p, rel in iter_md_files(root):
        n_files += 1
        for lineno, rule, detail in check(p, rel):
            all_hits.append(f'STALE {rel}:{lineno} [{rule}] {detail}')

    # A stale-API scan over no files finds no stale APIs (see scan_scope).
    guard(n_files, 'markdown files', str(root))

    if all_hits:
        print(f'{len(all_hits)} freshness violation(s) found:\n')
        for h in all_hits:
            print(f'  {h}')
        print('\nRules: ' + '; '.join(f'{name} — {why}' for name, why in RULES))
        sys.exit(1)

    print(f'OK — freshness scan clean ({n_files} md files, {len(RULES)} rules).')
    sys.exit(0)


if __name__ == '__main__':
    main()
