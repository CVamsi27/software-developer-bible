#!/usr/bin/env python3
"""Per-file review ledger: one hash-pinned row per tracked Markdown file.

The older coverage ledger (docs/2026-10-25-fullstack-coverage.json) records
*that* a file was inspected at exact bytes. It cannot say what standard the
file was held to: a row can be complete while the page is stale, dull or
padded. This ledger is the 2026-11 quality pass's evidence store, keyed to the
seven checks in docs/2026-11-quality-rubric.md but reporting the six axes a
reader can act on:

  current   - version/API claims checked, or "no version-sensitive claim"
  readable  - the file was read end to end; the opening, term order and causal
              flow were judged, not merely scanned
  concise   - word count against the genre's budget; filler/repetition removed
  focused   - no second treatment of a mechanism that has a canonical home
  fast      - measured page/source weight; shared shell noted; no claim of a
              Lighthouse score that was never run
  best      - genre-specific verdict: what this file is for, and whether it
              does that job better than the obvious alternative

A row is valid only while its `sha256` matches the file on disk. Editing a
reviewed file therefore invalidates the review in the same commit, which is the
point: evidence is about the bytes that exist, not the bytes someone once saw.

Ratchet, not cliff
------------------
A corpus-wide pass takes multiple sessions. The gate must stay green for the
sections already finished without pretending the rest are reviewed. So
unreviewed files live in `pending`, and the gate enforces:

  * every tracked .md file has a row (new files cannot appear unreviewed);
  * every `read` row's hash matches and carries non-empty evidence on all six
    axes;
  * `pending` is exactly the set of `unread` rows (the queue cannot silently
    grow, and a finished file cannot be left in it);
  * deleting a row is a failure, not a shortcut.

`apply` moves rows from unread to read and shrinks `pending` atomically.

Usage
-----
  python3 scripts/review_ledger.py init
  python3 scripts/review_ledger.py apply docs/review-batch.json
  python3 scripts/review_ledger.py status [--section 10-frontend]
  python3 scripts/review_ledger.py check
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, 'docs', 'review-ledger.json')
AXES = ('current', 'readable', 'concise', 'focused', 'fast', 'best')
MIN_EVIDENCE = 24
PLACEHOLDERS = ('todo', 'tbd', 'unread', 'not reviewed', 'placeholder', 'n/a')


def read_text(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def tracked_md():
    out = subprocess.run(
        ['git', 'ls-files', '*.md'], cwd=ROOT, capture_output=True,
        text=True, check=True,
    ).stdout
    return sorted(line for line in out.splitlines() if line.strip())


def sha256(rel):
    digest = hashlib.sha256()
    with open(os.path.join(ROOT, rel), 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest()


def line_count(rel):
    with open(os.path.join(ROOT, rel), 'rb') as fh:
        return sum(1 for _ in fh)


def genre_of(rel):
    name = os.path.basename(rel)
    if name == 'INDEX.md':
        return 'index'
    if name == 'REVISION.md':
        return 'revision'
    if 'interview-questions' in name:
        return 'interview'
    if rel.startswith('docs/'):
        return 'doc'
    if rel.startswith('projects/'):
        return 'project'
    if rel.startswith(('80-lanes-', '81-lanes-', 'lanes/')):
        return 'lane'
    if '/' not in rel:
        return 'meta'
    return 'chapter'


def section_of(rel):
    return rel.split('/', 1)[0] if '/' in rel else '(root)'


def load():
    if not os.path.exists(LEDGER):
        return {
            'schemaVersion': 1,
            'rubric': 'docs/2026-11-quality-rubric.md',
            'axes': list(AXES),
            'files': {},
            'pending': [],
        }
    with open(LEDGER, encoding='utf-8') as fh:
        return json.load(fh)


def save(data):
    data['pending'] = sorted(
        rel for rel, row in data['files'].items() if row['status'] == 'unread'
    )
    with open(LEDGER, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, indent=1, sort_keys=False)
        fh.write('\n')


def cmd_init(_args):
    data = load()
    rows = data['files']
    disk = tracked_md()
    disk_set = set(disk)
    added = removed = stale = 0
    for rel in disk:
        if rel not in rows:
            rows[rel] = {
                'sha256': sha256(rel),
                'lines': line_count(rel),
                'genre': genre_of(rel),
                'status': 'unread',
            }
            added += 1
        elif rows[rel]['status'] == 'read' and rows[rel]['sha256'] != sha256(rel):
            stale += 1
    for rel in sorted(set(rows) - disk_set):
        del rows[rel]
        removed += 1
    save(data)
    print(f'ledger initialised: {len(rows)} tracked Markdown files '
          f'({added} added, {removed} removed)')
    if stale:
        print(f'WARNING: {stale} read row(s) no longer match their file on disk; '
              f're-read those files and re-apply before committing')
    return 0


def cmd_apply(args):
    data = load()
    with open(args.batch, encoding='utf-8') as fh:
        payload = json.load(fh)
    entries = payload.get('files') if isinstance(payload, dict) else payload
    if not isinstance(entries, list) or not entries:
        print('apply: batch must be a non-empty list or {"files": [...]}')
        return 1
    errors = []
    accepted = 0
    for entry in entries:
        rel = entry.get('path', '')
        if rel not in data['files']:
            errors.append(f'{rel or "(missing path)"}: not a tracked Markdown file')
            continue
        missing = [axis for axis in AXES if not str(entry.get(axis, '')).strip()]
        if missing:
            errors.append(f'{rel}: missing evidence for {", ".join(missing)}')
            continue
        short = [axis for axis in AXES
                 if len(str(entry[axis]).strip()) < MIN_EVIDENCE]
        if short:
            errors.append(f'{rel}: evidence under {MIN_EVIDENCE} chars for '
                          f'{", ".join(short)}')
            continue
        row = data['files'][rel]
        row.update({
            'sha256': sha256(rel),
            'lines': line_count(rel),
            'genre': entry.get('genre') or row.get('genre') or genre_of(rel),
            'status': 'read',
            'reviewed': entry.get('reviewed') or args.date,
            'evidence': {axis: str(entry[axis]).strip() for axis in AXES},
        })
        if entry.get('defects'):
            row['defects'] = entry['defects']
        else:
            row.pop('defects', None)
        if entry.get('notes'):
            row['notes'] = str(entry['notes']).strip()
        else:
            row.pop('notes', None)
        accepted += 1
    if errors:
        print(f'apply REFUSED: {len(errors)} problem(s); no rows changed')
        for err in errors:
            print(f'  - {err}')
        return 1
    save(data)
    read = sum(1 for row in data['files'].values() if row['status'] == 'read')
    print(f'applied {accepted} row(s); read-backed {read}/{len(data["files"])}, '
          f'{len(data["pending"])} pending')
    return 0


def cmd_status(args):
    data = load()
    rows = data['files']
    sections = {}
    for rel, row in rows.items():
        sec = section_of(rel)
        bucket = sections.setdefault(sec, [0, 0, 0])
        bucket[0] += 1
        if row['status'] == 'read':
            bucket[1] += 1
        else:
            bucket[2] += 1
    total_read = sum(1 for row in rows.values() if row['status'] == 'read')
    print(f'read-backed {total_read}/{len(rows)} files '
          f'({100 * total_read / len(rows) if rows else 0:.1f}%)')
    print(f'{"section":30s} {"read":>5s} {"total":>6s} {"pending":>8s}')
    for sec in sorted(sections):
        if args.section and args.section not in sec:
            continue
        total, read, pending = sections[sec]
        print(f'{sec:30s} {read:5d} {total:6d} {pending:8d}')
    return 0


def cmd_check(_args):
    data = load()
    rows = data['files']
    try:
        disk = set(tracked_md())
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f'SCOPE ERROR — tracked Markdown files could not be listed: {exc}')
        return 1
    if not disk:
        print('SCOPE ERROR — no tracked Markdown files; run from the repository root')
        return 1
    problems = []

    missing = sorted(disk - set(rows))
    extra = sorted(set(rows) - disk)
    if missing:
        problems.append(f'{len(missing)} tracked file(s) have no ledger row: '
                        + ', '.join(missing[:8]))
    if extra:
        problems.append(f'{len(extra)} ledger row(s) name files that no longer '
                        f'exist: ' + ', '.join(extra[:8]))

    unread = {rel for rel, row in rows.items() if row['status'] == 'unread'}
    pending = set(data.get('pending', []))
    if unread != pending:
        grew = sorted(unread - pending)
        stale = sorted(pending - unread)
        if grew:
            problems.append(f'{len(grew)} unread file(s) are not in pending: '
                            + ', '.join(grew[:8]))
        if stale:
            problems.append(f'{len(stale)} pending entr(ies) are not unread: '
                            + ', '.join(stale[:8]))

    for rel, row in sorted(rows.items()):
        if row['status'] == 'read':
            if row.get('sha256') != sha256(rel):
                problems.append(f'{rel}: reviewed bytes changed since the review '
                                f'(re-read and re-apply)')
            evidence = row.get('evidence') or {}
            for axis in AXES:
                text = str(evidence.get(axis, '')).strip()
                if len(text) < MIN_EVIDENCE:
                    problems.append(f'{rel}: {axis} evidence missing or under '
                                    f'{MIN_EVIDENCE} characters')
                elif any(token in text.lower() for token in PLACEHOLDERS):
                    problems.append(f'{rel}: {axis} evidence contains a '
                                    f'placeholder token')
            if not row.get('reviewed'):
                problems.append(f'{rel}: read row has no review date')
        elif row['status'] != 'unread':
            problems.append(f'{rel}: unknown status {row["status"]!r}')

    if problems:
        print(f'review ledger: {len(problems)} problem(s)')
        for problem in problems:
            print(f'  - {problem}')
        print('\nThe ledger is evidence, not a checklist: a row must describe '
              'what the read found and stay pinned to the bytes on disk.')
        return 1

    read = sum(1 for row in rows.values() if row['status'] == 'read')
    print(f'review ledger OK: {read}/{len(rows)} files read-backed with '
          f'current hashes; {len(pending)} pending in the ratchet')
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--date', default='2026-11-14',
                    help='review date recorded on applied rows')
    sub = ap.add_subparsers(dest='command', required=True)
    p_init = sub.add_parser('init', help='add rows for new files, prune deleted')
    p_init.set_defaults(func=cmd_init)
    p_apply = sub.add_parser('apply', help='record read-backed verdicts')
    p_apply.add_argument('batch')
    p_apply.set_defaults(func=cmd_apply)
    p_status = sub.add_parser('status', help='coverage by section')
    p_status.add_argument('--section')
    p_status.set_defaults(func=cmd_status)
    p_check = sub.add_parser('check', help='gate: rows, hashes, evidence, queue')
    p_check.set_defaults(func=cmd_check)
    args = ap.parse_args()
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
