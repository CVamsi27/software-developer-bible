#!/usr/bin/env python3
"""The review ledger's lie detector, pinned.

The 2026-11-14 ledger passed because the gate only asked whether an evidence
string was non-empty. 805 rows then shared one "manual scan" paragraph, and
the ledger reported 988/988 read-backed. These tests pin the replacement:
the row must name the file's real line count, the prose word count, the
measured page weight, and a check or an explicit no-claim boundary.
"""
import contextlib
import hashlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import review_ledger
import prose_scan


class ReviewLedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.path = '10-frontend/example.md'
        example = self.root / self.path
        example.parent.mkdir(parents=True)
        example.write_text(
            '# Example\n\n'
            'A request arrives without a tenant and fails at the database boundary.\n\n'
            'The handler resolves the tenant before it opens the connection.\n'
            'The test shows the failure and the repaired path.\n'
        )
        self.lines = example.read_text().count('\n')
        self.words = prose_scan.prose_words(example.read_text().splitlines())
        self.page = self.root / 'page-weight.json'
        self.page.write_text(json.dumps({
            'rows': [{
                'path': self.path,
                'genre': 'chapter',
                'status': 'built',
                'rawBytes': 50000,
                'gzipBytes': 14000,
                'assets': {'scripts': 1, 'stylesheets': 1, 'images': 0, 'iframes': 0, 'videos': 0},
            }]
        }))
        self.ledger = self.root / 'review-ledger.json'
        self.ledger.write_text(json.dumps({
            'schemaVersion': 1,
            'files': {},
            'pending': [],
        }))
        patches = [
            mock.patch.object(review_ledger, 'ROOT', str(self.root)),
            mock.patch.object(review_ledger, 'PAGE_WEIGHT', str(self.page)),
            mock.patch.object(review_ledger, 'LEDGER', str(self.ledger)),
        ]
        for patcher in patches:
            patcher.start()
            self.addCleanup(patcher.stop)
        review_ledger._PAGE_CACHE = None
        self.addCleanup(setattr, review_ledger, '_PAGE_CACHE', None)

    def valid_evidence(self):
        return {
            'current': "No version-sensitive claim; the mechanism was checked against the chapter's own example.",
            'readable': f'Full read of {self.lines} lines. It opens on a tenant failure and traces one causal path.',
            'concise': f'{self.words} words. The example carries the mechanism and the Summary names the boundary.',
            'focused': 'The mechanism has one canonical home and links out for the rest.',
            'fast': '48.8 KB raw / 13.7 KB gzip on the shared shell; text only.',
            'best': 'Genre: chapter. It names a failure boundary; the remaining limit is runtime-specific behavior.',
        }

    def write_row(self, evidence):
        row = {
            'sha256': hashlib.sha256((self.root / self.path).read_bytes()).hexdigest(),
            'lines': self.lines,
            'genre': 'chapter',
            'status': 'read',
            'reviewed': '2026-11-15',
            'evidence': evidence,
        }
        self.ledger.write_text(json.dumps({
            'schemaVersion': 1,
            'files': {self.path: row},
            'pending': [],
        }))

    def test_valid_row_passes(self):
        self.assertEqual(review_ledger.evidence_problems(self.path, self.valid_evidence()), [])

    def test_manual_scan_template_fails(self):
        evidence = self.valid_evidence()
        evidence['readable'] = 'Manual scan found a coherent title, complete HN outline and Summary; the text reviewed at those levels was clear.'
        problems = review_ledger.evidence_problems(self.path, evidence)
        self.assertTrue(any('structural-scan template' in p for p in problems), problems)

    def test_source_weight_is_not_page_speed(self):
        evidence = self.valid_evidence()
        evidence['fast'] = 'Source 6.6 KB over 87 lines with 3 Markdown links; the scan found no unrelated preamble in the title or Summary.'
        problems = review_ledger.evidence_problems(self.path, evidence)
        self.assertTrue(any('measured value' in p for p in problems), problems)

    def test_wrong_line_count_fails(self):
        evidence = self.valid_evidence()
        evidence['readable'] = 'Full read of 999 lines. It opens on a tenant failure.'
        problems = review_ledger.evidence_problems(self.path, evidence)
        self.assertTrue(any('line count says 999' in p for p in problems), problems)

    def test_wrong_word_count_fails(self):
        evidence = self.valid_evidence()
        evidence['concise'] = '999 words. The example carries the mechanism.'
        problems = review_ledger.evidence_problems(self.path, evidence)
        self.assertTrue(any('word count says 999' in p for p in problems), problems)

    def test_missing_current_check_fails(self):
        evidence = self.valid_evidence()
        evidence['current'] = 'The chapter is accurate and has no issues.'
        problems = review_ledger.evidence_problems(self.path, evidence)
        self.assertTrue(any('current evidence names no check' in p for p in problems), problems)

    def test_check_rejects_template_row(self):
        evidence = self.valid_evidence()
        evidence['readable'] = 'Manual scan found a coherent title, complete HN outline and Summary; the text reviewed at those levels was clear.'
        self.write_row(evidence)
        with mock.patch.object(review_ledger, 'tracked_md', return_value=[self.path]):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = review_ledger.cmd_check(mock.Mock())
        self.assertEqual(code, 1)
        self.assertIn('structural-scan template', output.getvalue())

    def test_check_accepts_valid_row(self):
        self.write_row(self.valid_evidence())
        with mock.patch.object(review_ledger, 'tracked_md', return_value=[self.path]):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = review_ledger.cmd_check(mock.Mock())
        self.assertEqual(code, 0, output.getvalue())


if __name__ == '__main__':
    unittest.main()
