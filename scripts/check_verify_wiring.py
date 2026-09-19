#!/usr/bin/env python3
"""Audit `scripts/verify.sh`'s own wiring — the one thing no gate ever watched.

Born from a real false green (Sept 2026): gate 10's failure branch read and
wrote a variable named `FAILURES` that nothing else in the file ever declared
or consulted. The intent was `FAIL=1`. Because `verify.sh` runs under
`set -u`, that unbound arithmetic aborts the shell *before* the trailing
`exit $FAIL` statement is reached — so a genuinely broken cross-reference made
verify.sh print "FAIL", skip gates 11-14 entirely, and still exit 0. CI would
have reported success on a red build.

The lesson generalizes: **a gate is only as blocking as its wiring.** Every
individual gate script exited 1 correctly throughout; nothing measured whether
verify.sh *listened*. So this checks the harness, not the corpus:

  1. Every gate's failure branch sets the same variable the summary reads.
     (Catches the `FAILURES` class — a failure that cannot reach the exit.)
  2. No `X=$((X+1))` on a variable that was never initialized (the `set -u`
     landmine that produced the silent abort in the first place).
  3. Every script a gate actually invokes exists on disk.
  4. Gate labels are unique, gap-free and in monotonic order — the harness
     says "the label order in this file is the gate order a reader should
     follow", so that claim is checked rather than assumed.
  5. Every `N/M` denominator equals the real number of gates, and the
     spelled-out count in the header comment agrees.
  6. The gate count as quoted in `contributing.md` and
     `docs/verification-gates.md` agrees too — the count lives in three
     files and was hand-maintained in all of them.
  7. **The CI layer can still fail.** A workflow step that runs a gate under
     `set +e` without propagating the exit status cannot fail the job — the
     same false green one level up, where nobody looks because the local run
     is green. Workflows that are *audits* rather than gates are listed in
     `ADVISORY_WORKFLOWS` with the reason they deliberately never fail.
  8. **Every gate is actually enforced by CI**, either through a
     `bash scripts/verify.sh` step or by naming the script itself. Eight gates
     had no CI step at all, so count drift, broken numbering, broken links and
     First-Principles regressions were all green in CI.
  9. **A gate's own inputs trigger the workflow that runs it.** The trigger
     list is hand-maintained and had already drifted: it named 11 scripts and
     omitted `verify.sh` plus nine gate scripts, so editing the harness did not
     even run the harness check.

`--write` restamps 5 and 6 from the same count this check computes, so the
number has one owner and cannot drift (the `check_counts.py` / `read_time.py`
pattern).

Exit 0 = the harness describes itself accurately and every failure can reach
the exit code. Exit 1 = it cannot.
"""
import fnmatch
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERIFY = os.path.join(ROOT, 'scripts', 'verify.sh')
CONTRIB = os.path.join(ROOT, 'contributing.md')
GATEDOC = os.path.join(ROOT, 'docs', 'verification-gates.md')

# `echo "6b/17 check_template.py — template compliance (…)"` — the space count
# after the label varies (some labels are 2 chars, some 4), so allow any run.
GATE_HEADER = re.compile(r'^echo "(\d+[a-z]?)/(\d+)\s+(\S+\.py|link_baseline\.py)(.*)"$')
LABEL_RE = re.compile(r'^(\d+)([a-z]?)$')
SCRIPT_REF = re.compile(r'scripts/([\w./-]+\.(?:py|sh|json))')
SELF_INC = re.compile(r'^([A-Za-z_]\w*)=\$\(\(\s*\1\b')
INIT_RE = r'^\s*%s='

WORKFLOW_DIR = os.path.join(ROOT, '.github', 'workflows')
STEP_RE = re.compile(r'^      - (name|uses):')
RUN_RE = re.compile(r'^\s+run:')
PATHS_ENTRY_RE = re.compile(r"^\s+- '([^']+)'", re.M)
SUITE_RE = re.compile(r'bash\s+scripts/verify\.sh')
PROPAGATE_RE = re.compile(r'^\s+exit\s+"?(?:\$code|\$\{PIPESTATUS\[0\]\})', re.M)
SET_PLUS_E_RE = re.compile(r'^\s+set \+e\s*$', re.M)

# Workflows that are *audits*, not gates: their scripts exit non-zero as a
# signal (actionable job-board findings, dead external links) and the
# workflow deliberately turns that into a tracking issue instead of a failed
# run. A weekly red X for external link rot would be noise, not signal -- so
# these are exempt from the propagation rule, by name and with the reason.
# Do not "fix" them into blocking steps.
ADVISORY_WORKFLOWS = {
    'job-board-watch.yml': 'exit 1 means actionable signals; opens a tracking issue',
    'link-rot-audit.yml': 'the probe never fails the workflow; bot-wall warns are noise',
    'drift-drill.yml': 'STALE hits open a tracking issue; a scheduled red X for doc staleness is noise',
}

WORDS = {}
for _n, _w in enumerate(
    'zero one two three four five six seven eight nine ten eleven twelve '
    'thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty'.split()
):
    WORDS[_n] = _w


def read(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def summary_start(text):
    """0-based line index of the trailing `if [ "$FAIL" -eq 0 ]` block.

    The last gate's body must stop here: the summary's own `else` sets no
    VAR=1 (it exits), and swallowing it would report the summary as a gate
    whose failure branch cannot reach the exit.
    """
    m = re.search(r'^if \[ "\$(\w+)" -eq 0 \]; then\s*$', text, re.M)
    return None if m is None else text[:m.start()].count('\n')


def parse_gates(text, stop_line=None):
    """Split verify.sh into gate blocks: header line index -> next header."""
    lines = text.splitlines()
    heads = []
    for i, line in enumerate(lines):
        m = GATE_HEADER.match(line)
        if m:
            label = m.group(1)
            lm = LABEL_RE.match(label)
            heads.append({
                'line': i + 1,
                'label': label,
                'base': int(lm.group(1)),
                'letter': lm.group(2),
                'denom': int(m.group(2)),
                'script': m.group(3),
                'i': i,
            })
    for idx, head in enumerate(heads):
        if idx + 1 < len(heads):
            end = heads[idx + 1]['i']
        else:
            end = len(lines)
            if stop_line is not None:
                end = min(end, stop_line)
        head['body'] = lines[head['i']:end]
    return heads


def failure_regions(body):
    """Lines inside each `else` … `fi` block of a gate body."""
    regions, start = [], None
    for line in body:
        if start is None and re.match(r'^\s*else\s*$', line):
            start = []
        elif start is not None and re.match(r'^fi\s*$', line):
            regions.append(start)
            start = None
        elif start is not None:
            start.append(line)
    return regions


def check(problems, text, lines, gates, summary_line):
    # --- 1. every failure branch must reach the exit -----------------------
    fail_vars = set()
    for g in gates:
        regions = failure_regions(g['body'])
        if not regions:
            problems.append(
                f"gate {g['label']} ({g['script']}) has no else/fi failure branch"
            )
            continue
        for region in regions:
            joined = '\n'.join(region)
            assigns = re.findall(r'^\s*([A-Za-z_]\w*)=1\s*$', joined, re.M)
            if not assigns:
                problems.append(
                    f"gate {g['label']} ({g['script']}) failure branch sets no "
                    f"`VAR=1` — its FAIL output cannot reach the exit code "
                    f"(line ~{g['line']})"
                )
            fail_vars.update(assigns)

    summary = re.search(
        r'if \[ "\$(\w+)" -eq 0 \]; then(.*?)^fi\s*$', text, re.M | re.S
    )
    if not summary or summary_line is None:
        problems.append('no trailing `if [ "$FAIL" -eq 0 ]` summary block found')
    else:
        summary_var = summary.group(1)
        body = summary.group(2)
        if 'exit 0' not in body or 'exit 1' not in body:
            problems.append(
                'the summary block must `exit 0` / `exit 1` — otherwise a '
                'failure can be printed without changing the build result'
            )
        extra = fail_vars - {summary_var}
        if extra:
            problems.append(
                f'failure branches write {sorted(extra)} but the summary only '
                f'reads ${summary_var} — those failures are silently ignored'
            )
        if summary_var not in fail_vars:
            problems.append(
                f'no failure branch ever sets ${summary_var}, so the summary '
                f'can never fail the build'
            )

    # --- 2. the set -u landmine -------------------------------------------
    for i, line in enumerate(lines):
        m = SELF_INC.match(line.strip())
        if not m:
            continue
        name = m.group(1)
        earlier = '\n'.join(lines[:i])
        if not re.search(INIT_RE % re.escape(name), earlier, re.M):
            problems.append(
                f'line {i + 1}: `{name}=$(({name}+1))` reads {name} before it '
                f'is ever set — under `set -u` this aborts verify.sh with an '
                f'unbound-variable error, skipping every later gate while the '
                f'process still exits 0'
            )

    # --- 3. invoked scripts exist -----------------------------------------
    seen_scripts = set()
    for i, line in enumerate(lines):
        if line.lstrip().startswith('#'):
            continue                      # comments name superseded scripts
        for name in SCRIPT_REF.findall(line):
            seen_scripts.add(name)
            if not os.path.exists(os.path.join(ROOT, 'scripts', name)):
                problems.append(f'line {i + 1}: verify.sh invokes missing scripts/{name}')

    # --- 4. labels unique, gap-free, monotonic ----------------------------
    labels = [g['label'] for g in gates]
    dupes = {x for x in labels if labels.count(x) > 1}
    if dupes:
        problems.append(f'duplicate gate labels: {sorted(dupes)}')
    keys = [(g['base'], g['letter']) for g in gates]
    if keys != sorted(keys):
        problems.append(
            f'gate labels are not in monotonic order: {labels} — the file '
            f'claims "the label order in this file is the gate order"'
        )
    bases = sorted({g['base'] for g in gates})
    if bases and bases != list(range(1, bases[-1] + 1)):
        missing = sorted(set(range(1, bases[-1] + 1)) - set(bases))
        problems.append(f'gate numbering has gaps at {missing}')

    # --- 5/6. the count claim, in all three files -------------------------
    count = len(gates)
    for g in gates:
        if g['denom'] != count:
            problems.append(
                f"gate {g['label']} label says /{g['denom']} but there are "
                f"{count} gates"
            )
    hdr = re.search(r'^# Runs all (\w+) checks', text, re.M)
    word = WORDS.get(count)
    if not hdr:
        problems.append('header comment no longer states how many checks run')
    elif hdr.group(1).lower() != word:
        problems.append(
            f'header comment says "all {hdr.group(1)} checks" but {count} run'
        )

    for path, label in ((CONTRIB, 'contributing.md'), (GATEDOC, 'docs/verification-gates.md')):
        doc = read(path)
        for num, den in re.findall(r'Gate (\d+[a-z]?)/(\d+)', doc):
            if int(den) != count:
                problems.append(
                    f'{label}: "Gate {num}/{den}" — the suite has {count} gates'
                )
        for num in re.findall(r'(?:all|the) (\d+) gates', doc):
            if int(num) != count:
                problems.append(f'{label}: says "all {num} gates" but {count} run')


def workflow_steps(text):
    """Split a workflow file into steps; return name + run body for each."""
    lines = text.splitlines()
    starts = [i for i, l in enumerate(lines) if STEP_RE.match(l)]
    starts.append(len(lines))
    out = []
    for k in range(len(starts) - 1):
        blk = lines[starts[k]:starts[k + 1]]
        name = re.sub(r'^\s*- (?:name|uses):\s*', '', blk[0]).strip()
        run_i = next((j for j, l in enumerate(blk) if RUN_RE.match(l)), None)
        if run_i is None:
            out.append({'name': name, 'run': ''})
            continue
        # `run: |` starts a block; `run: cmd` is an inline single command. Both
        # shapes appear in this repo, and handling only the block form made the
        # suite-runner step (and gate 14's step) invisible to the checks below.
        inline = re.sub(r'^\s+run:\s*', '', blk[run_i]).strip()
        body = [] if inline in ('', '|', '>', '|-', '>-') else [inline]
        body += blk[run_i + 1:]
        out.append({'name': name, 'run': '\n'.join(body)})
    return out


def command_lines(body):
    """A step's executed lines, minus echo/comment text.

    FAIL messages name the script a human should run next (`echo "FAIL - run:
    python3 scripts/check_alignment.py --fix"`). That is guidance, not
    execution, and must not count as CI enforcing the gate.
    """
    keep = []
    for line in body.splitlines():
        s = line.strip()
        if s.startswith('echo') or s.startswith('#'):
            continue
        keep.append(line)
    return '\n'.join(keep)


def workflow_paths(text):
    """Trigger path filters, from the `on:` block only."""
    m = re.search(r'^on:.*?(?=^[a-z]|\Z)', text, re.M | re.S)
    return PATHS_ENTRY_RE.findall(m.group(0)) if m else []


def covered(entry, target):
    """Does a trigger path filter `entry` match `target`?"""
    if entry == target:
        return True
    if entry.endswith('/**') and target.startswith(entry[:-2]):
        return True
    return fnmatch.fnmatch(target, entry)


def check_ci(problems, gate_scripts):
    """Rules 7-9: the CI layer must be able to fail, cover every gate, and
    be triggered by the files those gates read."""
    if not os.path.isdir(WORKFLOW_DIR):
        problems.append('.github/workflows/ is missing — nothing runs the gates in CI')
        return
    suite_wf, invoked = None, set()
    # Only a workflow that can actually go red counts as *enforcing* a gate.
    # link-rot-audit.yml runs `link_baseline.py --probe`, but that step never
    # fails the job by design, so crediting it would mark a gate as covered
    # when nothing would ever turn red for it.
    enforced = set()
    for path in sorted(glob.glob(os.path.join(WORKFLOW_DIR, '*.yml'))):
        wf = os.path.basename(path)
        text = read(path)
        blocking = wf not in ADVISORY_WORKFLOWS
        for step in workflow_steps(text):
            cmds = command_lines(step['run'])
            names = SCRIPT_REF.findall(cmds)
            invoked.update(names)
            if blocking:
                enforced.update(names)
            if SUITE_RE.search(cmds):
                suite_wf = wf
            # 7. a failing gate must be able to fail the job
            if SET_PLUS_E_RE.search(step['run']) and not PROPAGATE_RE.search(step['run']):
                if wf not in ADVISORY_WORKFLOWS:
                    problems.append(
                        f'{wf}: step "{step["name"]}" runs under `set +e` but never '
                        f'exits on the captured status — a failing gate there is a '
                        f'green build (advisory workflows are exempt, but this one '
                        f'is not)'
                    )
        # 9. trigger coverage
        paths = workflow_paths(text)
        if paths:
            needed = {p for p in gate_scripts if p in invoked}
            if SUITE_RE.search(text):
                needed.add('verify.sh')
            for name in sorted(needed):
                # the gate file itself
                if not any(covered(e, f'scripts/{name}') for e in paths):
                    problems.append(
                        f'{wf}: runs scripts/{name} but its `paths:` filter does not '
                        f'include it, so a change to that file would not trigger the '
                        f'workflow on push/PR'
                    )

    # 8. every gate must be enforced by CI
    if suite_wf:
        return
    missing = sorted(set(gate_scripts) - enforced)
    if missing:
        problems.append(
            'no workflow runs `bash scripts/verify.sh`, and these gates are not '
            'enforced by any workflow that can go red: ' + ', '.join(missing) +
            ' — their failures are green in CI'
        )


def write(text):
    """Restamp the count claims from the single computed gate count."""
    gates = parse_gates(text)
    count = len(gates)
    word = WORDS.get(count, str(count))
    changed = []

    out = re.sub(r'^(echo "\d+[a-z]?)/\d+', lambda m: f'{m.group(1)}/{count}', text, flags=re.M)
    out = re.sub(r'^(# Runs all )\w+( checks)', lambda m: f'{m.group(1)}{word}{m.group(2)}',
                 out, flags=re.M)
    if out != text:
        with open(VERIFY, 'w', encoding='utf-8') as fh:
            fh.write(out)
        changed.append('scripts/verify.sh')

    for path, rel in ((CONTRIB, 'contributing.md'), (GATEDOC, 'docs/verification-gates.md')):
        doc = read(path)
        new = re.sub(r'(Gate \d+[a-z]?)/\d+', lambda m: f'{m.group(1)}/{count}', doc)
        new = re.sub(r'((?:all|the) )\d+( gates)', lambda m: f'{m.group(1)}{count}{m.group(2)}', new)
        if new != doc:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(new)
            changed.append(rel)
    return changed


def main() -> int:
    text = read(VERIFY)
    lines = text.splitlines()
    stop = summary_start(text)
    gates = parse_gates(text, stop)
    if '--write' in sys.argv:
        changed = write(text)
        if changed:
            print('restamped gate count in: ' + ', '.join(changed))
        else:
            print('gate count already consistent — nothing to restamp')
        return 0

    problems = []
    check(problems, text, lines, gates, stop)
    check_ci(problems, sorted({g['script'] for g in gates}))
    if problems:
        print(f'verify.sh wiring: {len(problems)} problem(s)')
        for p in problems:
            print(f'  - {p}')
        print('\nThis is a defect in the harness itself, not the corpus: a gate '
              'whose failure cannot reach the exit code does not block anything.')
        return 1
    print(
        f'verify.sh wiring OK ({len(gates)} gates, every failure branch reaches '
        f'the exit, all count claims agree, and CI enforces every gate in a job '
        f'that can fail)'
    )
    return 0


if __name__ == '__main__':
    sys.exit(main())
