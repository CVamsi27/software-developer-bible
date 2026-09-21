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
# trailing parent/genre suffix: '— Index', ' - Node.js', ' — Database'
TAIL_SUFFIX = re.compile(r'\s*[—–-]\s*(?:Index|Database|Node\.js|Frontend|Backend'
                         r'|Platform|Architecture|Realtime|Real-time|Toolkit'
                         r'|[A-Z][\w.&/ ]*)\s*$')


def is_nav_footer(line: str) -> bool:
    """A nav footer carries a Previous/Next label (the generated surface)."""
    return 'Previous:' in line or 'Next:' in line


def human_title(target: str):
    """The target file's own title: H1 minus numbering and suffix, or None."""
    if not os.path.exists(target):
        return None
    with open(target, encoding='utf-8') as fh:
        for line in fh:
            m = ANY_H1.match(line.rstrip('\n'))
            if m:
                title = LEAD_NUM.sub('', m.group(1)).strip()
                stripped = TAIL_SUFFIX.sub('', title).strip()
                return stripped or title
    return None


def label_spans(line: str):
    """Yield (label_start, label_end, link_target) for nav links."""
    for m in re.finditer(r'\[([^\]]+)\]\(([^)]*)\)', line):
        label = m.group(1)
        nav = re.match(r'^(?:←\s*)?(?:Previous|Next):\s*', label)
        if nav:
            yield m.start(1) + nav.end(), m.start(1) + len(label), m.group(2)


def fix_line(line: str, base_dir: str, base_rel: str):
    """('fixed line', [(line-relative problem description), ...])."""
    if not is_nav_footer(line):
        return line, []
    changed = []

    def rewrite(seg: str, target: str):
        arrow = ' →' if seg.rstrip().endswith('→') else ''
        core = seg.rstrip()[:-1].rstrip() if arrow else seg.strip()
        if core.startswith(('./', '../')):
            path = os.path.normpath(os.path.join(base_dir, target.split('#')[0]))
            title = human_title(path)
            if title:
                changed.append(f'label is the path "{core}" — target title is '
                               f'"{title}"')
                return title + arrow
            changed.append(f'label is the path "{core}" and its target has no '
                           f'readable title — fix by hand')
            return seg.lstrip()
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
    for path in iter_files():
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
    if hits:
        verb = 'repaired' if fix else 'found'
        print(f"nav labels: {verb} {total} non-canonical token(s) in "
              f"{files_touched} file(s)\n")
        for h in hits:
            print(f"  {h}")
        if not fix:
            print("\n  fix: python3 scripts/fix_nav_labels.py --fix")
        return 1 if not fix else 0
    print(f"nav labels OK — every Previous/Next label is a canonically-cased "
          f"human title, not a path ({mode})")
    return 0


if __name__ == '__main__':
    sys.exit(main())
