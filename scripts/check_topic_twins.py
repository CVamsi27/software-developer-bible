#!/usr/bin/env python3
"""Topic-twin gate: chapters that teach the same topic must cross-link.

The prose-shingle duplicate detector (`check_duplication.py`) catches
copy-paste. It does *not* catch the failure this repo actually hit: the same
topic taught twice in different words (chaos engineering in 50.1.5.02 and
50.4.03, caching in 30.2.1.05 and 20.8.01). Those show up in the *titles*,
not the prose.

This gate:
  1. Derives each content file's topic tokens from its slug (generic words
     such as patterns/advanced/deep-dive/architecture stripped).
  2. Groups files whose topic-token sets overlap strongly — the twins.
  3. Requires every pair inside a group to reference each other, so a reader
     landing on either half is routed to the other.

A twin group whose members do not link to each other is drift: one of them
will grow into a second copy of the other (which is exactly how the chaos
pair reached ~250 overlapping lines).
"""
import os
import re
import sys
from collections import defaultdict
from itertools import combinations

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'node_modules', '.archive', 'personal', 'docs', '.freebuff'}
SKIP_FILES = {'INDEX.md', 'README.md', 'AGENTS.md', 'contributing.md', 'ROADMAP.md'}
EXEMPT_PREFIXES = ('80-lanes-abroad-full-stack', '81-lanes-indian-sde-faang', 'projects')

# Slug words that describe the *form* of a chapter, not its topic.
GENERIC = {
    'patterns', 'pattern', 'architecture', 'design', 'system', 'systems',
    'advanced', 'basics', 'fundamentals', 'internals', 'deep', 'dive',
    'overview', 'guide', 'full', 'practice', 'practical', 'deepdive',
    'the', 'a', 'an', 'and', 'or', 'of', 'in', 'for', 'with', 'vs',
    'interview', 'questions', 'strategies', 'strategy', 'concepts',
    'production', 'at', 'scale', 'how', 'to', 'cheat', 'sheet', 'sheets',
}

# Pairs that share topic tokens but are *not* the same topic — recorded
# deliberately so the heuristic cannot force a meaningless link.
NOT_TWINS = {
    ('40-platform/40.2-kubernetes/01-core-workloads/40.2.1.02-deployments.md',
     '40-platform/40.7-serverless-edge/40.7.03-vercel-deployments.md'),
    # Same slug word, different concept. A link here would mislead a reader
    # who wants the other meaning of the word.
    ('10-frontend/10.1-javascript/05-functional-patterns/10.1.5.01-modules.md',
     '20-backend/20.2-nestjs/01-core-architecture/20.2.1.01-modules.md'),
    ('10-frontend/10.3-react/03-advanced-hooks-and-patterns/10.3.3.05-performance.md',
     '20-backend/20.4-database/01-postgresql-foundations/20.4.1.05-postgresql-performance.md'),
    ('30-architecture/30.1-design-patterns/04-behavioral/30.1.4.04-state.md',
     '10-frontend/10.3-react/03-advanced-hooks-and-patterns/10.3.3.06-state-management.md'),
    ('10-frontend/10.4-next.js/03-data-and-caching/10.4.3.04-streaming.md',
     '20-backend/20.6-microservices/02-communication-and-messaging/20.6.2.02-grpc-streaming.md'),
    ('10-frontend/10.6-animation/10.6.01-css-animations.md',
     '10-frontend/10.7-html-css/10.7.02-css-fundamentals.md'),
    ('20-backend/20.1-node.js/02-io-and-data/20.1.2.04-http-module.md',
     '30-architecture/30.1-design-patterns/03-structural/30.1.3.05-module-pattern.md'),
    ('20-backend/20.3-rest-apis/01-design-and-contract/20.3.1.03-versioning.md',
     '40-platform/40.8-monorepo/40.8.05-versioning-publishing-strategies.md'),
    ('30-architecture/30.3-infra-patterns/04-data-at-scale/30.3.4.01-database-scaling.md',
     '60-realtime/60.1-websockets/02-architecture-and-scaling/60.1.2.02-scaling-patterns.md'),
    ('20-backend/20.2-nestjs/04-quality-and-operations/20.2.4.02-testing.md',
     '60-realtime/60.1-websockets/03-frameworks-and-paradigms/60.1.3.04-testing-realtime-systems.md'),
    ('10-frontend/10.3-react/02-core-hooks/10.3.2.05-context-api.md',
     '20-backend/20.3-rest-apis/01-design-and-contract/20.3.1.01-api-design-patterns.md'),
}
THRESHOLD = 0.5

# A twin group is only actionable if the members are in *different* files;
# same-topic files inside one category are usually deliberate siblings
# (e.g. debounce vs throttle), so the gate reports them but requires a link
# only across categories/stacks.
FENCE = re.compile(r'^\s*(```|~~~)')
LINK = re.compile(r'\[[^\]]*\]\(([^)]+)\)')


def topic_tokens(path):
    slug = os.path.basename(path)
    slug = re.sub(r'^(?:\d+\.)*\d+[a-z]?-', '', slug) if re.match(r'^(?:\d+\.)*\d', slug) else slug
    slug = slug[:-3] if slug.endswith('.md') else slug
    toks = [t for t in slug.split('-') if t and t not in GENERIC and not t.isdigit()]
    return set(toks)


def iter_files():
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        rel = os.path.relpath(root, ROOT)
        if rel.startswith(EXEMPT_PREFIXES):
            continue
        for f in sorted(files):
            if f.endswith('.md') and f not in SKIP_FILES and 'interview' not in f.lower():
                yield os.path.join(root, f)


def links(path):
    """Relative link targets mentioned outside fences."""
    out = set()
    in_fence = False
    for line in open(path, encoding='utf-8'):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in LINK.finditer(line):
            t = m.group(1)
            if not t.startswith(('http://', 'https://', '#')):
                out.add(os.path.basename(t))
    return out


def analyse():
    """Return (twin_groups, topics, missing_links).

    Shared by the checker and `link_topic_twins.py` so both always agree on
    what a twin is.
    """
    files = list(iter_files())
    topics = {os.path.relpath(p, ROOT): topic_tokens(p) for p in files}

    groups = defaultdict(list)
    for rel, toks in topics.items():
        if toks:
            groups[frozenset(toks)].append(rel)

    # Merge overlapping topic sets into twin groups (Jaccard >= THRESHOLD).
    keys = [k for k in groups if groups[k]]
    merged = []
    for k in keys:
        placed = False
        for grp in merged:
            j = len(k & grp) / max(1, len(k | grp))
            if j >= THRESHOLD:
                grp |= set(k)
                placed = True
                break
        if not placed:
            merged.append(set(k))

    members = defaultdict(list)
    for k in keys:
        for grp in merged:
            if len(k & grp) / max(1, len(k | grp)) >= THRESHOLD:
                members[frozenset(grp)].extend(groups[k])
                break

    twin_groups = {g: sorted(v) for g, v in members.items() if len(v) > 1}

    missing = []
    for g, files_in in sorted(twin_groups.items(), key=lambda kv: kv[1][0]):
        if len(files_in) < 2:
            continue
        for a, b in combinations(files_in, 2):
            la, lb = topics[a], topics[b]
            if len(la & lb) / max(1, len(la | lb)) < THRESHOLD:
                continue
            # Siblings inside one category are already presented together by
            # the category INDEX; a mutual link adds nothing. Drift happens
            # across categories, where the two halves cannot see each other.
            if os.path.dirname(a) == os.path.dirname(b):
                continue
            if (a, b) in NOT_TWINS or (b, a) in NOT_TWINS:
                continue
            a_links, b_links = links(os.path.join(ROOT, a)), links(os.path.join(ROOT, b))
            if os.path.basename(b) not in a_links:
                missing.append((a, b))
            if os.path.basename(a) not in b_links:
                missing.append((b, a))
    return twin_groups, topics, missing


def main() -> int:
    twin_groups, _topics, missing = analyse()
    print(f"topic-twin groups: {len(twin_groups)}")
    for g, files_in in sorted(twin_groups.items(), key=lambda kv: kv[1][0]):
        print(f"\n[{' '.join(sorted(g))}]  {len(files_in)} chapters")
        for f in files_in:
            print(f"    {f}")

    if missing:
        print(f"\nMISSING TWIN LINKS ({len(missing)}):  the first file does not link to the second")
        for a, b in missing:
            print(f"   {a}\n     -> {b}")
        return 1
    print("\nevery topic twin cross-links its counterpart")
    return 0


if __name__ == '__main__':
    sys.exit(main())
