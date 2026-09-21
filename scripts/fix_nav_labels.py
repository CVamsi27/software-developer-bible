#!/usr/bin/env python3
"""Restore navigation-foot labels: canonical casing, and human titles.

The corpus's `[← Previous: X](...) · [Back to Index](INDEX.md) · [Next: Y](...)`
footers were minted by a pass that *humanized the target slug* — title-casing
its words. Two uniform-and-wrong signatures survived in the navigation
surface, exactly the generator-defect pattern the 2026-09 cheat-sheet
forensics documented:

  Rule 1 (casing). Acronyms and brand names have fixed casing that
title-casing destroys, so readers were told about "Mvcc", "Cqrs Di", "Sli Slo
Sla", "Cap Theorem", "Iac Fundamentals", "Rabbitmq", "Webrtc Peer To Peer",
"Typescript Cheat Sheet" — 57 wrong-cased tokens across 45 files. Nothing
caught it: gate 4's stale-label rule rejects only *spaceless* path labels, and
gate 11's duplication check compares prose bodies, not footers.

  Rule 2 (paths as labels). 55 labels were still raw relative paths —
`[Next: ../03 Transactions And Replication/index →](../…)` — because gate 4's
rule required the label to contain no space. They resolve, so the link works,
but the reader sees a filesystem path where a title belongs. The fix derives
the title from the source of truth: the target file's own H1, with its
numbering prefix and trailing parent/genre suffix (`— Index`, `- Node.js`)
stripped. Deriving beats inventing — the label can never drift from the file
it points at.

  Rule 3 (slug-humanized labels). The same generator's most common failure:
a label that is the target's title *with its punctuation and case flattened*
— `Useeffect` for `useEffect`, `Usesyncexternalstore` for
`useSyncExternalStore`, `Bff` for `BFF`, `Statefulsets Daemonsets` for
`StatefulSets & DaemonSets`, `Tanstack Form` for `TanStack Form`,
`Socket Io` for `Socket.io`, `Graphql` for `GraphQL`, `Async Await` for
`Async/Await`, `SLI SLO SLA` for `SLI, SLO & SLA`. 132 labels. The signature
is deliberately tight — the label equals the title once every non-alphanumeric
character is dropped and case is folded — so a label that merely *shortens* a
title (`Fiber` for `React Fiber`, `Performance` for `React Performance
Optimization`) is left alone: shortening is an editorial choice, flattening is
an artifact. Rule 2's derivation is the repair.

This tool is both the fixer and the gate, matching fix_box_width.py:

--check  exit 1 listing every offending label (either rule)
--fix    rewrite them in place (idempotent; only label text changes)

Scope is deliberately the footer line: in nav labels a capitalized "Cap" is
always the CAP theorem, while in body prose a sentence may legitimately begin
"Cap the retries …". Prose elsewhere is clean because prose is written by
hand; the defect lives only in generated labels, so only labels are gated.

Code spans are skipped even inside a label (`\`Transport.GRPC\`` is the real
NestJS API name, not a casing error) — the same fence/span discipline the rest
of the suite uses.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import md_fences
from scan_scope import guard

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'node_modules', '.archive', 'personal', 'docs', 'scripts'}
EXEMPT_PREFIXES = ('80-lanes-abroad-full-stack', '81-lanes-indian-sde-faang',
                   'projects')

# Wrong casing -> canonical form. Keys are the shapes title-casing a slug
# produces; every one was observed in the corpus at the fix's birth (2026-09-21)
# and the list is closed — a new shape is a new defect and fails until mapped.
CANONICAL = {
    'Mvcc': 'MVCC', 'Cqrs': 'CQRS', 'Di': 'DI', 'Ddd': 'DDD',
    'Solid': 'SOLID', 'Oop': 'OOP', 'Orm': 'ORM', 'Http': 'HTTP',
    'Https': 'HTTPS', 'Json': 'JSON', 'Yaml': 'YAML', 'Xml': 'XML',
    'Html': 'HTML', 'Css': 'CSS', 'Dom': 'DOM', 'Url': 'URL', 'Uri': 'URI',
    'Dns': 'DNS', 'Cdn': 'CDN', 'Cpu': 'CPU', 'Ttl': 'TTL', 'Uuid': 'UUID',
    'Oltp': 'OLTP', 'Olap': 'OLAP', 'Crdt': 'CRDT', 'Mvc': 'MVC',
    'Acid': 'ACID', 'Cap': 'CAP', 'Jvm': 'JVM', 'Tls': 'TLS', 'Aes': 'AES',
    'Rsa': 'RSA', 'Pii': 'PII', 'Sla': 'SLA', 'Slo': 'SLO', 'Sli': 'SLI',
    'Cicd': 'CI/CD', 'Iac': 'IaC', 'Rbac': 'RBAC', 'Grpc': 'gRPC',
    'Graphql': 'GraphQL', 'Nestjs': 'NestJS', 'Postgresql': 'PostgreSQL',
    'Typescript': 'TypeScript', 'Javascript': 'JavaScript',
    'Github': 'GitHub', 'Nextjs': 'Next.js', 'Nodejs': 'Node.js',
    'Webrtc': 'WebRTC', 'Rabbitmq': 'RabbitMQ', 'Oauth': 'OAuth',
    'Jwt': 'JWT', 'Nosql': 'NoSQL', 'Cors': 'CORS', 'Csrf': 'CSRF',
    'Xss': 'XSS', 'Sse': 'SSE', 'Ssr': 'SSR', 'Isr': 'ISR', 'Ssg': 'SSG',
    'Csr': 'CSR', 'Kmp': 'KMP', 'Wasm': 'WASM', 'Etl': 'ETL',
    'Apis': 'APIs', 'Api': 'API', 'Rest': 'REST', 'Crud': 'CRUD',
    'Sre': 'SRE', 'Elk': 'ELK', 'Ide': 'IDE', 'Jdbc': 'JDBC', 'Jpa': 'JPA',
    'Openapi': 'OpenAPI', 'Saas': 'SaaS', 'Paas': 'PaaS', 'Iaas': 'IaaS',
    'Cidr': 'CIDR', 'Ux': 'UX', 'Ui': 'UI',
}
TOKEN = re.compile(r'[A-Za-z][A-Za-z0-9.+/-]*')
CODESPAN = re.compile(r'`[^`]*`')


ANY_H1 = re.compile(r'^#\s+(.+?)\s*$')
LEAD_NUM = re.compile(r'^\d+(?:\.\d+)*\s*[—–-]\s*')
# Titles carry an optional trailing "— <suffix>". Two kinds exist in the
# corpus (measured): the parent stack/genre ("— JavaScript", "— Database",
# "— Index") and a genuine subtitle ("— KMP & Rabin-Karp", "— Aggregates &
# Value Objects"). Only the first is not part of the name, and it is derivable
# from the file's own path rather than guessable from a word list: the ancestor
# directory names ARE the parent stacks (`10.1-javascript` -> JavaScript).
# An earlier version stripped any trailing capitalised phrase and silently
# destroyed real titles ("The Twelve-Factor App" -> "The Twelve"), which also
# masked 27 label defects by making the identity comparison fail. `index` is
# included because "<Thing> — Index" is the INDEX genre, not a subtitle.
GENERIC_SUFFIXES = {'index'}
NUM_PREFIX = re.compile(r'^\d+(?:\.\d+)*[-_]?')


def allowed_suffixes(target: str):
    """Parent-stack and genre names a title may legitimately end with."""
    names = set(GENERIC_SUFFIXES)
    for part in os.path.abspath(target).split(os.sep)[:-1]:
        base = NUM_PREFIX.sub('', part)
        if base:
            names.add(norm_key(base))
    return names


def is_nav_footer(line: str) -> bool:
    """A nav footer carries a Previous/Next label (the generated surface)."""
    return 'Previous:' in line or 'Next:' in line


def norm_key(s: str) -> str:
    """Title/label identity key: punctuation- and case-insensitive."""
    return re.sub(r'[^a-z0-9]', '', s.lower())


def human_title(target: str):
    """The target file's own title: H1 minus numbering and parent suffix.

    A link may point at a category *directory* (`../40.3-ci-cd`) rather than
    its INDEX.md; the directory's INDEX carries the title in that layout.
    """
    if os.path.isdir(target):
        target = os.path.join(target, 'INDEX.md')
    if not os.path.exists(target):
        return None
    allowed = allowed_suffixes(target)
    with open(target, encoding='utf-8') as fh:
        for line in fh:
            m = ANY_H1.match(line.rstrip('\n'))
            if m:
                title = LEAD_NUM.sub('', m.group(1)).strip()
                sm = re.search(r'\s+[—–-]\s+(.+)$', title)
                if sm and norm_key(sm.group(1)) in allowed:
                    title = title[:sm.start()].strip()
                return title or None
    return None


def label_spans(line: str):
    """Yield (label_start, label_end, link_target) for nav links.

    Two footer styles exist in the corpus (measured: 1,186 inside, 3 outside):
    the dominant `[Next: Label](target)` puts the marker inside the brackets,
    and a rare `Next: [Label](target)` puts it before them. Both are the same
    generated surface, so both are inspected — a style the scanner skipped
    would be a label the gate cannot defend.
    """
    for m in re.finditer(r'\[([^\]]+)\]\(([^)]*)\)', line):
        label = m.group(1)
        nav = re.match(r'^(?:←\s*)?(?:Previous|Next):\s*', label)
        if nav:
            yield m.start(1) + nav.end(), m.start(1) + len(label), m.group(2)
        elif re.search(r'(?:←\s*)?(?:Previous|Next):\s*$',
                       line[:m.start()]):
            yield m.start(1), m.start(1) + len(label), m.group(2)


def fix_line(line: str, base_dir: str, base_rel: str):
    """('fixed line', [(line-relative problem description), ...])."""
    if not is_nav_footer(line):
        return line, []
    changed = []

    def rewrite(seg: str, target: str):
        arrow = ' →' if seg.rstrip().endswith('→') else ''
        core = seg.rstrip()[:-1].rstrip() if arrow else seg.strip()
        path = os.path.normpath(os.path.join(base_dir, target.split('#')[0]))
        title = human_title(path)
        if core.startswith(('./', '../')):
            if title:
                changed.append(f'label is the path "{core}" — target title is '
                               f'"{title}"')
                return title + arrow
            changed.append(f'label is the path "{core}" and its target has no '
                           f'readable title — fix by hand')
            return seg.lstrip()
        if title and core != title and norm_key(core) == norm_key(title):
            changed.append(f'label "{core}" is the slug-humanized form of its '
                           f'target title "{title}"')
            return title + arrow
        masked = CODESPAN.sub(lambda m: '\0' * len(m.group(0)), core)
        out, last = [], 0
        for m in TOKEN.finditer(masked):
            tok = m.group(0)
            if tok in CANONICAL and CANONICAL[tok] != tok:
                out.append(core[last:m.start()])
                out.append(CANONICAL[tok])
                last = m.end()
                changed.append(f'nav label says "{tok}" — canonical form is '
                               f'"{CANONICAL[tok]}"')
        out.append(core[last:])
        return ''.join(out) + arrow

    pieces, prev = [], 0
    for start, end, target in label_spans(line):
        pieces.append(line[prev:start])
        pieces.append(rewrite(line[start:end], target))
        prev = end
    pieces.append(line[prev:])
    return ''.join(pieces), changed


def iter_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        rel = os.path.relpath(dirpath, ROOT)
        if rel.startswith(EXEMPT_PREFIXES):
            continue
        for name in sorted(filenames):
            if name.endswith('.md'):
                yield os.path.join(dirpath, name)


def main() -> int:
    fix = '--fix' in sys.argv
    hits, total, files_touched = [], 0, 0
    scanned = 0
    for path in iter_files():
        scanned += 1
        with open(path, encoding='utf-8') as fh:
            lines = fh.read().splitlines()
        # Only prose lines can hold a footer (a fenced 'Previous:' is content).
        fenced = [in_fence for _, _, in_fence, _ in md_fences.walk(lines)]
        out, file_changes = [], []
        for i, line in enumerate(lines):
            if fenced[i]:
                out.append(line)
                continue
            new, changed = fix_line(line, os.path.dirname(path), path)
            out.append(new)
            if changed:
                file_changes.append((i + 1, changed))
        if file_changes:
            files_touched += 1
            rel = os.path.relpath(path, ROOT)
            for ln, changed in file_changes:
                for problem in changed:
                    total += 1
                    hits.append(f"{rel}:{ln}: {problem}")
            if fix:
                with open(path, 'w', encoding='utf-8') as fh:
                    fh.write('\n'.join(out) + '\n')

    mode = 'fixed' if fix else 'check'
    # A nav scanner that read no chapters has not checked a single footer
    # (see scan_scope) — and 0 files touched would have said "all clean".
    guard(scanned, 'markdown files', ROOT)
    if hits:
        verb = 'repaired' if fix else 'found'
        print(f"nav labels: {verb} {total} non-canonical token(s) in "
              f"{files_touched} file(s)\n")
        for h in hits:
            print(f"  {h}")
        if not fix:
            print("\n  fix: python3 scripts/fix_nav_labels.py --fix")
        return 1 if not fix else 0
    print(f"nav labels OK — every Previous/Next label in {scanned} files is a "
          f"canonically-cased human title, not a path ({mode})")
    return 0


if __name__ == '__main__':
    sys.exit(main())
