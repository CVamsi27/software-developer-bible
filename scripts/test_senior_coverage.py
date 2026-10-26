#!/usr/bin/env python3
"""Exact-byte review and release-enforcement regressions in disposable trees."""
import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import check_verify_wiring as wiring
from senior_coverage import inventory

ROOT = Path(__file__).resolve().parent.parent


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.chapter = self.root / 'cache.md'
        self.chapter.write_text('# Cache\n\nA concrete invariant.\n')
        self.record = {'path': 'cache.md', 'sha256': hashlib.sha256(self.chapter.read_bytes()).hexdigest(),
                       'status': 'reviewed', 'reviewer': 'fixture', 'notes': 'Scoped read'}

    def test_current(self):
        self.assertEqual(inventory(self.root, [self.record])['totals'], {'reviewed': 1})

    def test_changed_byte_is_stale(self):
        self.chapter.write_text('# Cache\n\nA changed invariant.\n')
        self.assertEqual(inventory(self.root, [self.record])['entries'][0]['status'], 'stale-review')

    def test_new_pending_and_removed_orphan(self):
        self.assertEqual(inventory(self.root, [])['totals'], {'pending-semantic-review': 1})
        self.chapter.unlink()
        self.assertEqual(inventory(self.root, [self.record])['orphanedReviewPaths'], ['cache.md'])

    def test_duplicate_and_incomplete_attestations(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            inventory(self.root, [self.record, self.record])
        for field in ('reviewer', 'notes'):
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'reviewer and scoped notes'):
                inventory(self.root, [{**self.record, field: ''}])

    def test_empty_scope_is_not_complete(self):
        self.chapter.unlink()
        scripts = self.root / 'scripts'
        scripts.mkdir()
        for name in ('senior_coverage.py', 'md_fences.py'):
            shutil.copy(ROOT / 'scripts' / name, scripts)
        result = subprocess.run(['python3', 'scripts/senior_coverage.py', '--require-complete'],
                                cwd=self.root, text=True, capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('SCOPE ERROR', result.stdout)

    def test_invalid_ledger_is_a_configuration_error(self):
        scripts = self.root / 'scripts'
        scripts.mkdir()
        for name in ('senior_coverage.py', 'md_fences.py'):
            shutil.copy(ROOT / 'scripts' / name, scripts)
        ledger = self.root / 'reviews.json'
        ledger.write_text('null')
        result = subprocess.run(['python3', 'scripts/senior_coverage.py', '--reviews=reviews.json',
                                 '--require-complete'], cwd=self.root, text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('REVIEW CONFIGURATION ERROR', result.stdout)
        self.assertNotIn('Traceback', result.stderr)

    def test_release_command_is_required_even_without_checker_prefix(self):
        problems = []
        wiring.check_review_release(problems, 'echo "manual inventory only"\n')
        self.assertTrue(any('senior_coverage.py' in p for p in problems))
        problems = []
        wiring.check_review_release(problems, (ROOT / 'scripts/verify.sh').read_text())
        self.assertEqual(problems, [])

    def test_both_events_trigger_on_each_review_input(self):
        workflow = (ROOT / '.github/workflows/code-whitespace.yml').read_text()
        for target in ('docs/2026-10-25-fullstack-review-records.json',
                       'docs/2026-10-25-fullstack-coverage.json'):
            with self.subTest(target=target):
                problems = []
                wiring.check_review_triggers(problems, workflow.replace(f"      - '{target}'\n", '', 1))
                self.assertTrue(any(target in p and 'push' in p for p in problems))
        problems = []
        wiring.check_review_triggers(problems, workflow)
        self.assertEqual(problems, [])

    def test_actual_harness_propagates_stale_review_failure(self):
        # Run the actual harness with all Python gates stubbed except coverage.
        # A stale lesson must still reach its real final exit; no real lesson changes.
        scripts = self.root / 'scripts'
        scripts.mkdir()
        shutil.copy(ROOT / 'scripts/verify.sh', scripts / 'verify.sh')
        for name in ('senior_coverage.py', 'md_fences.py'):
            shutil.copy(ROOT / 'scripts' / name, scripts)
        docs = self.root / 'docs'
        docs.mkdir()
        (docs / '2026-10-25-fullstack-review-records.json').write_text(json.dumps({'reviews': [self.record]}))
        self.chapter.write_text('# Cache\n\nA changed invariant.\n')
        bin_dir = self.root / 'bin'
        bin_dir.mkdir()
        python = shutil.which('python3')
        (bin_dir / 'python3').write_text(
            '#!/bin/sh\ncase "$1" in\n  scripts/senior_coverage.py) exec ' + python + ' "$@" ;;\n'
            '  *) exit 0 ;;\nesac\n')
        (bin_dir / 'node').write_text('#!/bin/sh\nexit 0\n')
        for command in bin_dir.iterdir():
            command.chmod(0o755)
        import os
        result = subprocess.run(['bash', 'scripts/verify.sh'], cwd=self.root,
                                env={**os.environ, 'PATH': str(bin_dir) + os.pathsep + os.environ['PATH']},
                                text=True, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('REVIEW REQUIRED cache.md', result.stdout)
        self.assertIn('One or more checks FAILED', result.stdout)


if __name__ == '__main__':
    unittest.main()
