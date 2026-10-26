#!/usr/bin/env python3
"""Inventory Markdown coverage without confusing structure with semantic review.

Added 2026-10-25: an old semantic ledger could look current after chapter
rewrites. Bind each reviewed disposition to the bytes actually inspected.

Pass explicit per-file review records with --reviews=PATH. A record applies only
to the exact bytes read by its reviewer. --require-complete fails on pending or
stale reviews; a normal inventory deliberately makes no completeness claim.
"""
import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

from md_fences import walk

SKIP = {'.git', '_site', 'node_modules', 'vendor', '.archive', '.freebuff',
        '.sass-cache', '.jekyll-cache', '__pycache__'}


def paths_for(root):
    if (root / '.git').exists():
        result = subprocess.run(
            ['git', 'ls-files', '--cached', '--others', '--exclude-standard', '*.md'],
            cwd=root, text=True, capture_output=True, check=True)
        candidates = [root / p for p in set(result.stdout.splitlines())]
    else:
        candidates = root.rglob('*.md')
    return sorted(p for p in candidates if p.is_file() and not SKIP.intersection(p.relative_to(root).parts))


def genre(path):
    if path.name == 'INDEX.md':
        return 'learning-index'
    if path.name == 'REVISION.md':
        return 'revision'
    if 'interview-questions' in path.name:
        return 'interview-bank'
    rel = path.as_posix()
    if rel.startswith(('docs/', 'projects/')) or '/' not in rel:
        return 'operational-or-project'
    if rel.startswith(('80-', '81-')):
        return 'role-guide'
    return 'learning-or-reference'


def inventory(root, records):
    known = {}
    for record in records:
        path = record['path']
        if path in known:
            raise ValueError(f'Duplicate review: {path}')
        if record.get('status') == 'reviewed' and not (record.get('reviewer') and record.get('notes')):
            raise ValueError(f'Review needs reviewer and scoped notes: {path}')
        known[path] = record
    entries = []
    for path in paths_for(root):
        rel = path.relative_to(root).as_posix()
        data = path.read_bytes()
        text = data.decode('utf-8')
        sha = hashlib.sha256(data).hexdigest()
        scanned = list(walk(text.splitlines()))
        prose = '\n'.join(line for _, line, inside, delimiter in scanned
                          if not inside and not delimiter)
        review = known.pop(rel, None)
        status = 'pending-semantic-review'
        if review and review.get('status') == 'reviewed':
            status = 'reviewed' if review.get('sha256') == sha else 'stale-review'
        elif review:
            status = review.get('status', status)
        entries.append({
            'path': rel, 'sha256': sha, 'genre': genre(Path(rel)),
            'status': status,
            'structure': {
                'headings': re.findall(r'^## (.+)$', prose, re.M),
                'code_fences': sum(1 for _, _, inside, delimiter in scanned if inside and delimiter),
                'revision_questions': len(re.findall(r'^\*\*Q:\*\*', prose, re.M)),
                'has_summary': bool(re.search(r'^## Summary\s*$', prose, re.M)),
                'has_first_principles': bool(re.search(r'^## First Principles\s*$', prose, re.M)),
            },
            **({'review': review} if review else {}),
        })
    return {
        'schemaVersion': 1,
        'scope': 'Current non-ignored Markdown, excluding generated/vendor trees',
        'method': 'Structure is machine-inspected; semantic review requires explicit exact-hash evidence.',
        'totals': dict(Counter(e['status'] for e in entries)),
        'files': len(entries), 'orphanedReviewPaths': sorted(known), 'entries': entries,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--reviews', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    # An empty checkout must fail honestly before reading a missing ledger.
    if args.require_complete and not paths_for(root):
        print('SCOPE ERROR — no current Markdown files to review')
        return 1
    try:
        payload = json.loads(args.reviews.read_text()) if args.reviews else {'reviews': []}
        if not isinstance(payload, dict) or not isinstance(payload.get('reviews'), list):
            raise ValueError('Review ledger must contain a reviews array')
        records = payload['reviews']
        result = inventory(root, records)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'REVIEW CONFIGURATION ERROR — {error}')
        return 2
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'files': result['files'], 'statuses': result['totals'],
                      'orphanedReviewPaths': result['orphanedReviewPaths']}))
    pending = [e['path'] for e in result['entries'] if e['status'] != 'reviewed']
    if args.require_complete and (pending or not result['entries'] or result['orphanedReviewPaths']):
        for path in pending:
            print(f'REVIEW REQUIRED {path}')
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
