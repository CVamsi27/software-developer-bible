#!/usr/bin/env python3
"""Relabel code fences that are mislabeled as text/plain/output/console.

Why: a code block fenced as `text` renders unstyled and reads as sloppy
indentation even when the code inside is fine. This pass relabels a
text-labeled fence to its real language when the body is PREDOMINANTLY
code — never when it is a diagram, a dialogue, or prose.

A fence is CODE when:
  - code_lines / non-empty lines >= 0.5, where a code line either ends
    with ; { } ( ) : , or contains a strong language keyword, and
  - diagram_lines / non-empty lines < 0.3 (box-drawing characters),
  - and it is not an HTTP dialogue (>=40% of lines start with an HTTP
    verb or a header name).

Language inference (first match wins):
  json     body starts with { or [ and parses-ish (braces/brackets + quotes)
  yaml     top-level `key: value` shape with dash lists, no semicolons
  bash     lines start with $ / sudo / cd / npm / git / kubectl / curl ...
  sql      SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|WITH|EXPLAIN at line starts
  python   def /class /import /from ... import /print( patterns
  java     public class / System.out / @Override
  go       package main / func / :=
  typescript interface |: string| as | => with const/let/type
  typescript (fallback for tsx-looking code when unsure → ts)
  http     HTTP dialogue (kept as text → relabeled `http`)
Otherwise the fence is left alone.

Usage:
  python3 scripts/fix_fence_labels.py --apply
  python3 scripts/fix_fence_labels.py            (dry run)
"""

import os

from scan_scope import guard
import re
import sys

SKIP_DIRS = {'.git', 'node_modules', 'vendor', '_site', '.archive', 'venv', '__pycache__',
             '.github', 'scripts', 'projects'}
FENCE_RE = re.compile(r'^( {0,3})(`{3,}|~{3,})([A-Za-z0-9_+-]*)')
TARGET_LABELS = {'', 'text', 'txt', 'plain', 'output', 'console', 'log'}
DIAGRAM_CHARS = set('┌┐└┘├┤┬┴┼─│═║╔╗╚╝▼▲►◀◄→←↔')

CODE_END = re.compile(r'[;{}(),]$')
KEYWORDS = re.compile(
    r'\b(def |class |function |const |let |var |import |export |from |package |'
    r'public |private |return |await |async |throw |try |except |elif |'
    r'SELECT |INSERT |UPDATE |DELETE |CREATE TABLE|ALTER TABLE|EXPLAIN |'
    r'kubectl |sudo |git |npm |pnpm |yarn |curl |docker )')
# HTTP dialogue lines: a verb with a path, or a KNOWN header name.
HTTP_LINE = re.compile(
    r'^(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS) /\S'
    r'|^(HTTP/\d)'
    r'|^(Host|Content-Type|Content-Length|Accept|Authorization|Cache-Control|'
    r'Set-Cookie|Cookie|Location|User-Agent|ETag|X-[A-Za-z-]+): ')
# Cheat-sheet / Q&A structure: label lines, Q:/A:, numbered lists, ALL-CAPS titles.
# The ASCII underline matters as much as the box-drawing one: the corpus's
# sheets rule their titles with `=` (JEST CHEAT SHEET / ======…), and an early
# version only matched `═`, so a sheet's title bar never counted and four mixed
# cheat-sheet fences were proposed for relabeling to `typescript` — which would
# have rendered their title bars and tips prose as broken code.
SHEET_LINE = re.compile(
    r'^(Q:|A:|\d+\.\s|\d+\)\s)'
    r'|^[A-Z][A-Z0-9 /&+.\'-]{2,}:?\s*$'
    r'|^[A-Z][A-Z0-9 /&+.\'-]{2,}:\s'
    r'|^•'
    r'|^\[!\['
    r'|^[═=]{3,}\s*$'
    r'|^\s{2,}[-*]\s+\S'
    r'|^[A-Za-z].*:$'
    r'|^\[x?\]\s')

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def classify(body):
    """Return inferred language label or None if this is not code."""
    ne = [l for l in body if l.strip()]
    if len(ne) < 3:
        return None
    n = len(ne)
    code = sum(1 for l in ne if CODE_END.search(l.rstrip()) or KEYWORDS.search(l))
    diag = sum(1 for l in ne if set(l) & DIAGRAM_CHARS)
    http = sum(1 for l in ne if HTTP_LINE.match(l.strip()))
    sheet = sum(1 for l in ne if SHEET_LINE.match(l.strip()))
    if diag / n >= 0.3 or sheet / n >= 0.25:
        return None
    if http / n >= 0.5:
        # 'GET /x: 10 req/sec' limit lists read as http dialogues; require
        # at least one header-ish or HTTP-version line to confirm.
        has_http_marker = any(re.match(r'^(HTTP/\d|Host:|Content-Type:|Authorization:|Set-Cookie:)', l.strip()) for l in ne)
        if not has_http_marker:
            return None
        return 'http'
    # Homogeneity, not a bare majority: a cheat sheet mixes a title bar, code
    # snippets and tips prose, and at a 0.6 threshold four such sheets cleared
    # the bar (code lines outnumbered the rest) and were proposed for relabeling.
    # A fence that is *really* mislabeled code is code all the way down.
    if code / n < 0.9:
        return None
    joined = '\n'.join(ne)
    ls = [l.strip() for l in ne]
    if re.match(r'^[\[{"]', ls[0]) and (joined.count('{') + joined.count('[')) >= 2:
        return 'json'
    if any(re.match(r'^(SELECT|INSERT|UPDATE|DELETE|CREATE TABLE|ALTER TABLE|WITH|EXPLAIN)\b', l, re.I) for l in ls):
        return 'sql'
    if any(re.match(r'^(def |class |import \w|from \w+ import|print\()', l) for l in ls):
        return 'python'
    if any(re.match(r'^(public |private ).*class |System\.out|@Override', l) for l in ls):
        return 'java'
    if any(re.match(r'^(package \w+|\w+ :=)', l) for l in ls):
        return 'go'
    if any(re.match(r'^\$', l) for l in ls) or any(
            re.match(r'^(sudo |cd |npm |pnpm |yarn |kubectl |curl |docker |git |echo )', l) for l in ls):
        return 'bash'
    if any(re.match(r'^(interface |type \w+ =|const \w+|let \w+|function \w+|export )', l) for l in ls) or re.search(r':\s*(string|number|boolean|void)\b', joined):
        return 'typescript'
    if '=>' in joined or '?. ' in joined or '.map(' in joined:
        return 'javascript'
    return None


def process(path, apply):
    with open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')
    relabeled = []
    in_f, lang, body, start = False, '', [], 0
    for i, line in enumerate(lines):
        m = FENCE_RE.match(line)
        if m:
            if not in_f:
                in_f, lang, body, start = True, m.group(3).lower(), [], i
            elif m.group(2)[0] == line.lstrip()[0]:
                if lang in TARGET_LABELS and lang != 'anki' and lang != 'tsv':
                    new = classify(body)
                    if new and new != lang:
                        lines[start] = FENCE_RE.sub(
                            lambda mm: mm.group(1) + mm.group(2) + new,
                            lines[start], count=1)
                        relabeled.append((start + 1, lang or '(none)', new))
                in_f = False
            continue
        if in_f:
            body.append(line)
    if apply and relabeled:
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    return relabeled


def main():
    apply = '--apply' in sys.argv
    total = 0
    n_files = 0
    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if not fn.endswith('.md'):
                continue
            n_files += 1
            p = os.path.join(root, fn)
            for lineno, old, new in process(p, apply):
                total += 1
                if not apply or total <= 40:
                    print(f"  {os.path.relpath(p, repo_root)}:{lineno}  {old} -> {new}")
    # A labeler that read no fences has not validated the corpus's labels
    # (see scan_scope) — 0 relabeled would otherwise read as "all correct".
    guard(n_files, 'markdown files', repo_root)
    print(f"\n{'RELABELED' if apply else 'WOULD RELABEL'}: {total} fence(s) "
          f"across {n_files} files")
    if not apply:
        print("(dry run — add --apply to write)")


if __name__ == '__main__':
    main()
