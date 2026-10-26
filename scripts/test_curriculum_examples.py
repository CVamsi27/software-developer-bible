#!/usr/bin/env python3
"""Replay a bounded pack extracted from canonical fences, including mutations.

No packages are fetched here. Set CURRICULUM_NODE and CURRICULUM_TSC to
preinstalled pinned tools, or put their executables on PATH. Only Node and the
declared TypeScript compiler are executed; snippets receive no inherited secrets.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from md_fences import walk

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / 'scripts/fixtures/curriculum-cases.json'


def extract(case, root=ROOT):
    path = root / case['path']
    lines = path.read_text().splitlines()
    blocks, current, language = [], [], None
    for _, line, inside, delimiter in walk(lines):
        if delimiter and inside:
            language = line.strip().lstrip('`~').strip()
            current = []
        elif delimiter:
            blocks.append((language, '\n'.join(current) + '\n'))
        elif inside:
            current.append(line)
    selected = []
    for fence in case['fences']:
        matches = [body for lang, body in blocks
                   if lang == case['language'] and body.startswith(fence['startsWith'])]
        if len(matches) != 1 or hashlib.sha256(matches[0].encode()).hexdigest() != fence['sha256']:
            raise AssertionError(f"{case['path']}: stale or ambiguous canonical fence {fence['startsWith']!r}")
        selected.append(matches[0])
    return '\n'.join(selected)


def command(args, work):
    # An allowlisted executable is assembled by replay, never read as a shell
    # command from the fixture. No network clients, shell or inherited tokens.
    return subprocess.run(args, cwd=work, capture_output=True, text=True, timeout=10,
                          env={'PATH': os.environ.get('PATH', ''), 'LANG': 'C.UTF-8', 'TZ': 'UTC'})


def tools(case):
    node = os.environ.get('CURRICULUM_NODE') or shutil.which('node')
    if not node:
        raise AssertionError('Install the pinned Node runtime from the scripts map')
    observed = command([node, '--version'], ROOT).stdout.strip().removeprefix('v')
    if observed != case['runtime']['node']:
        raise AssertionError(f"{case['path']}: Node {case['runtime']['node']} required; observed {observed}")
    if case['language'] != 'typescript':
        return node, None
    compiler = os.environ.get('CURRICULUM_TSC') or shutil.which('tsc')
    if not compiler:
        raise AssertionError('Install TypeScript 5.9.3 and set CURRICULUM_TSC to its bin/tsc')
    compiler = str(Path(compiler).resolve())
    version = command([node, compiler, '--version'], ROOT).stdout.strip()
    if version != 'Version ' + case['runtime']['typescript']:
        raise AssertionError(f"{case['path']}: TypeScript pin mismatch: {version}")
    return node, compiler


def replay(case, source, mutation=False):
    node, compiler = tools(case)
    if mutation:
        change = case['mutation']
        if source.count(change['before']) != 1:
            raise AssertionError(f"{case['id']}: mutation boundary is not unique")
        source = source.replace(change['before'], change['after'], 1)
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        if case['language'] == 'typescript':
            path = work / 'case.ts'
            path.write_text(source + '\n' + case['wrapper']['accepted'])
            accepted = command([node, compiler, *case['arguments'], path.name], work)
            if (accepted.returncode, accepted.stdout, accepted.stderr) != (0, '', ''):
                raise AssertionError(f"{case['path']}: accepted compile failed: {accepted.stdout}{accepted.stderr}")
            path.write_text(source + '\n' + case['wrapper']['accepted'] + '\n' + case['wrapper']['rejected'])
            rejected = command([node, compiler, *case['arguments'], path.name], work)
            codes = re.findall(r'error (TS\d+):', rejected.stdout)
            if rejected.returncode != case['expected']['negativeExit'] or codes != case['expected']['negativeCodes']:
                raise AssertionError(f"{case['path']}: rejected compile gave {rejected.returncode}/{codes}: {rejected.stdout}")
        else:
            path = work / 'case.cjs'
            path.write_text(source + '\n' + case['wrapper']['suffix'])
            result = command([node, *case['arguments'], path.name], work)
            actual = {'exit': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
            if actual != case['expected']:
                raise AssertionError(f"{case['path']}: observed {actual!r}; expected {case['expected']!r}")


class CurriculumExamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads(MANIFEST.read_text())['cases']

    def test_canonical_mechanisms(self):
        self.assertTrue(1 <= len(self.cases) <= 3)
        for case in self.cases:
            with self.subTest(case=case['id']):
                replay(case, extract(case))

    def test_named_mutations_are_detected(self):
        for case in self.cases:
            with self.subTest(case=case['id'], mutation=case['mutation']['name']):
                source = extract(case)
                # Tool/setup errors cannot serve as the mutation's failure.
                tools(case)
                with self.assertRaisesRegex(AssertionError, re.escape(case['path'])):
                    replay(case, source, mutation=True)

    def test_stale_fence_refuses_execution(self):
        case = self.cases[0]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / case['path']
            path.parent.mkdir(parents=True)
            start = case['fences'][0]['startsWith']
            path.write_text((ROOT / case['path']).read_text().replace(start, start + '\nconsole.log("changed");', 1))
            with self.assertRaisesRegex(AssertionError, 'stale or ambiguous'):
                extract(case, root)


if __name__ == '__main__':
    unittest.main()
