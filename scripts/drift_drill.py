#!/usr/bin/env python3
"""Quarterly drift drill: re-probe the known staleness classes.

The Sept 2026 hardening session swept the corpus for dead products, EOL
pins, and deprecated idioms, fixed the hits, and gated the *recurring*
classes in check_freshness.py. The classes below are the ones a gate
cannot own — singletons and context-dependent mentions — so they decay
back silently unless re-probed. This script re-probes them on a
schedule (see .github/workflows/drift-drill.yml) the way
link_baseline.py --probe re-probes cited URLs.

Two severities, mirroring the link-rot audit's DEAD/SUSPECT/warn split:

  STALE  — the token is anomalous in current teaching docs regardless of
           context (a dead product name, a removed API call). Any hit is
           worth a tracking issue. Drives the exit code.
  REVIEW — the token can appear legitimately in migration/legacy
           teaching ("Enzyme was…; React Testing Library is the modern
           path"). Hits are listed for a human to judge; they never fail
           the run.

Exit codes: 0 = no STALE hits, 1 = at least one STALE hit (the audit
workflow turns that into a labeled tracking issue; it never fails red).

Excluded trees: docs/ (the health report and remediation reports quote
the class names *by design* — they document the sweep itself) and the
personal lane trees (private material, own genres).
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_TOP = ('80-lanes-abroad-full-stack', '81-lanes-indian-sde-faang',
            'lanes', 'projects', 'docs')
SKIP_NAMES = {'INDEX.md', 'README.md'}
SKIP_SUBDIRS = {'.git', 'node_modules', 'vendor', '_site', '.archive', '.sass-cache', 'scripts'}

# (name, severity, regex, fix-path note)
CLASSES = [
    ('dead-product-stackdriver', 'STALE',
     r'\bStackdriver\b',
     'GCP renamed it: Cloud Monitoring / Cloud Logging (2019)'),
    ('dead-product-elasticsearch-aws', 'STALE',
     r'Amazon Elasticsearch|AmazonES|awselasticsearch',
     'AWS service is OpenSearch since 2021; Elasticsearch is Elastic Cloud'),
    ('dead-product-codecommit', 'STALE',
     r'\bCodeCommit\b|\bCloud Source Repositor',
     'AWS closed new-customer access 2024-07; recommend GitHub/GitLab'),
    ('aws-sdk-v2-js', 'STALE',
     r"require\('aws-sdk'\)|from 'aws-sdk'",
     'SDK v2 entered maintenance 2023; use @aws-sdk/* v3 clients'),
    ('aws-cli-v1-get-login', 'STALE',
     r'aws ecr get-login ',
     'v1 command removed; use `aws ecr get-login-password`'),
    ('lambda-runtime-eol', 'STALE',
     r'\bnodejs(10|12|14|16)\.x\b|\bpython3\.[67]\b(?!\S)',
     'runtime deprecated by AWS; nodejs22.x / python3.13 are current'),
    ('go-ioutil', 'STALE',
     r'\bioutil\.',
     'Go 1.16+: io.ReadAll / os.ReadFile / io.Copy (io/ioutil is a shim)'),
    ('python-distutils', 'STALE',
     r'\bdistutils\b',
     'removed in Python 3.12; use setuptools or sysconfig'),
    ('react-dom-render', 'STALE',
     r'ReDOM\.render|ReactDOM\.render\(',
     'React 18+: createRoot(document.getElementById(...)).render(...)'),
    ('vue2-new-vue', 'STALE',
     r'new Vue\(',
     'Vue 2 EOL 2023-12-31; Vue 3 uses createApp'),
    ('webpack-commonschunk', 'STALE',
     r'\bCommonsChunkPlugin\b',
     'webpack 4 legacy; use optimization.splitChunks'),
    ('yarn-global', 'STALE',
     r'yarn global (add|remove)',
     'removed in Yarn 2; use yarn global add via corepack or npm i -g'),
    ('webpack-loader-chaining', 'STALE',
     r'\b[\w-]+-loader![\w-]+',
     'webpack 4 inline chaining; use module.rules use: [...]'),
    ('kubectl-generator', 'STALE',
     r'--generator=?\s',
     'flag removed in kubectl 1.15+; generator selection is automatic'),
    ('helm-init', 'STALE',
     r'\bhelm init\b',
     'Helm 2 command; Helm 3 needs no Tiller init'),
    ('terraform-template-file', 'STALE',
     r'\btemplate_file\b',
     'deprecated provider; use templatefile() function'),
    ('istio-alpha-api', 'STALE',
     r'networking\.istio\.io/v1alpha3',
     'removed in Istio 1.24 (2024-11); v1 is served, v1beta1 is the convention'),
    ('fabric-io-domain', 'STALE',
     r'fabric\.io',
     'Fabric crash-platform domain retired (Crashlytics moved to Firebase '
     '2017-2020); note Fabric the RN renderer is CURRENT — scope to the domain'),
    ('google-plus', 'STALE',
     r'Google\+|plus\.google\.com',
     'Google+ shut down April 2019; sign-in is Google Identity / OAuth2'),
    ('docker-scan', 'STALE',
     r'\bdocker scan\b',
     'retired with Docker Desktop 4.x; use `docker sbom` / Trivy / Scout'),
    # REVIEW: context-dependent, human judgment required.
    ('enzyme-mention', 'REVIEW',
     r'\bEnzyme\b', 'legitimate in migration teaching; flag only if recommended'),
    ('moment-mention', 'REVIEW',
     r'\bmoment\(', 'legacy; check the text recommends date-fns/Temporal'),
    ('node-sass-mention', 'REVIEW',
     r'\bnode-sass\b', 'deprecated; check the text recommends dart-sass'),
    ('tslint-mention', 'REVIEW',
     r'\btslint\b', 'deprecated 2019; check the text recommends ESLint'),
    ('react-unsafe-lifecycles', 'REVIEW',
     r'componentWill(ReceiveProps|Mount|Update)\b',
     'UNSAFE_-renamed; legitimate when teaching the migration'),
    ('bower-mention', 'REVIEW',
     r'\bBower\b', 'dead since 2017; legitimate only as history'),
    ('cra-mention', 'REVIEW',
     r'create-react-app|Create React App',
     'deprecated 2023-02; check the text recommends Vite/Next'),
    ('angularjs-mention', 'REVIEW',
     r'\bAngularJS\b', 'EOL 2021-12; legitimate only as history'),
    ('app-center-mention', 'REVIEW',
     r'App Center',
     'hosted CodePush retired 2025-03-31; mentions must date it (see 10.8.05)'),
    ('parse-com-mention', 'REVIEW',
     r'[Pp]arse\.com',
     'hosted Parse shut down 2017; Parse Server continues self-hosted'),
    ('heroku-free-mention', 'REVIEW',
     r'Heroku free',
     'free tier retired Nov 2022; eco/basic dynos replaced it'),
]

REVIEW_MARKERS = ('was ', 'legacy', 'deprecated', 'removed', 'renamed',
                  'replac', 'instead', 'migrat', 'EOL', 'history')


def iter_files():
    for root, dirs, files in os.walk(ROOT):
        rel_root = os.path.relpath(root, ROOT).replace(os.sep, '/')
        top = rel_root.split('/')[0]
        dirs[:] = sorted(d for d in dirs if d not in SKIP_SUBDIRS)
        if rel_root != '.' and top in SKIP_TOP:
            dirs[:] = []
            continue
        if any(part == 'personal' for part in rel_root.split('/')):
            dirs[:] = []
            continue
        for f in sorted(files):
            if f.endswith('.md') and f not in SKIP_NAMES:
                yield os.path.join(root, f), rel_root


def main() -> int:
    stale, review = [], []
    for path, rel in iter_files():
        with open(path, encoding='utf-8') as fh:
            for lineno, line in enumerate(fh, 1):
                for name, severity, pattern, note in CLASSES:
                    if re.search(pattern, line):
                        where = f"{os.path.relpath(path, ROOT)}:{lineno}"
                        entry = (name, where, line.strip()[:90], note)
                        (stale if severity == 'STALE' else review).append(entry)

    def show(entries, label):
        print(f'{label}: {len(entries)}')
        for name, where, text, note in sorted(entries):
            print(f'  {label}  [{name}] {where}')
            print(f'        {text}')
            print(f'        fix: {note}')

    show(stale, 'STALE')
    show(review, 'REVIEW')
    if not stale and not review:
        print('Drill clean — every swept class is still absent from the corpus.')
    elif not stale:
        print('No STALE hits; review items above are advisory only.')
    else:
        print('STALE hits found — verify each against live sources, fix the ')
        print('doc, and re-run. Re-gate a class that recurs (freshness rule).')
    return 1 if stale else 0


if __name__ == '__main__':
    sys.exit(main())
