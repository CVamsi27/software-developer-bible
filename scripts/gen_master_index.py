#!/usr/bin/env python3
"""Generate search.html — a filterable master index over the whole corpus.

The data comes from the same metadata gate 6b enforces (check_template.
parse_meta) and the same read-time model gate 13 enforces, so the page
cannot drift from the corpus: gate 14 regenerates it in memory and fails
if the committed file differs.

Output is a static HTML file (no Jekyll front matter -> copied verbatim,
no Liquid escaping needed) with the corpus embedded as JSON and vanilla JS
filtering — no dependencies. The shared theme script is loaded through the
same `_config.yml` owner (`theme_asset`) the Jekyll include reads, emitted
document-relative so the committed page also works offline and from file://
(rule 13 in scripts/check_verify_wiring.py enforces the single owner).

Usage:
  python3 scripts/gen_master_index.py            # write search.html + api/index.json
  python3 scripts/gen_master_index.py --check    # gate: exit 1 on drift
"""
import hashlib
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from read_time import content_files, minutes  # noqa: E402
from check_template import parse_meta  # noqa: E402

OUT = os.path.join(ROOT, 'search.html')
API_OUT = os.path.join(ROOT, 'api', 'index.json')
CONFIG = os.path.join(ROOT, '_config.yml')
THEME_ASSET_RE = re.compile(r'^theme_asset:\s*(\S+)\s*$', re.M)
H1 = re.compile(r'^# (?!#)\s*(.+?)\s*$', re.M)


def collect():
    rows = []
    for rel in content_files():
        text = open(os.path.join(ROOT, rel), encoding='utf-8').read()
        meta = parse_meta(text) or {}
        m = H1.search(text)
        title = (m.group(1) if m else os.path.basename(rel)[:-3]).strip()
        tags = sorted({t.strip() for t in (meta.get('tags') or '').split(',')
                       if t.strip()})
        rows.append({
            'p': rel[:-3] + '.html',   # Jekyll renders md -> html at same path
            't': title,
            's': meta.get('section', ''),
            'c': meta.get('category', ''),
            'g': tags,
            'm': minutes(os.path.join(ROOT, rel)),
        })
    rows.sort(key=lambda r: (r['s'], r['p']))
    return rows


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Search the library — {TITLE}</title>
<script src="{THEME_SRC}"></script>
<link rel="stylesheet" href="assets/search-ui.css?v=study-flow-13">
<link rel="stylesheet" href="assets/reading-ui.css?v=study-flow-13">
<link rel="stylesheet" href="assets/reference-reader.css?v=reference-12">
<script src="assets/study-state.js" defer></script>
<script src="assets/roadmap-return.js?v=study-flow-13" defer></script>
<script src="assets/reading-ui.js?v=study-flow-13" defer></script>
<script src="assets/search-ui.js" defer></script>
</head>
<body>
<header class="site-header" role="banner">
  <div class="wrapper">
    <a class="site-title" rel="author" href="index.html">Developer Bible</a>
    <nav class="site-nav" aria-label="Main navigation">
      <input type="checkbox" id="nav-trigger" class="nav-trigger">
      <label for="nav-trigger">
          <span class="menu-icon">
            <svg viewBox="0 0 18 15" width="18px" height="15px">
              <path d="M18,1.484c0,0.82-0.665,1.484-1.484,1.484H1.484C0.665,2.969,0,2.304,0,1.484l0,0C0,0.665,0.665,0,1.484,0 h15.032C17.335,0,18,0.665,18,1.484L18,1.484z M18,7.516C18,8.335,17.335,9,16.516,9H1.484C0.665,9,0,8.335,0,7.516l0,0 c0-0.82,0.665-1.484,1.484-1.484h15.032C17.335,6.031,18,6.696,18,7.516L18,7.516z M18,13.516C18,14.335,17.335,15,16.516,15H1.484 C0.665,15,0,14.335,0,13.516l0,0c0-0.82,0.665-1.483,1.484-1.483h15.032C17.335,12.031,18,12.695,18,13.516L18,13.516z"/>
            </svg>
          </span>
        </label>
      <div class="trigger">
        <a class="page-link" href="INDEX.html">Library</a>
        <a class="page-link" href="ROADMAP.html">Roadmap</a>
      </div>
    </nav>
    <form class="header-search" action="search.html" role="search">
      <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10" cy="10" r="7"/><path d="m15 15 6 6"/></svg>
      <label class="read-aloud-status" for="header-topic">Search topics</label>
      <input id="header-topic" type="search" name="q" placeholder="Search topics, e.g. closures, APIs, system design…">
    </form>
  </div>
</header>

<main class="search-main wrapper">
  <p class="eyebrow">THE STUDY LIBRARY</p>
  <h1>Search the library</h1>
  <p class="search-intro">Find explanations, revision questions, and interview practice.</p>
  <form id="search-form" role="search">
    <label for="q">Topic or keyword</label>
    <div class="query-row"><input type="search" id="q" placeholder="Try closures, APIs, or system design" autocomplete="off"><button type="button" id="clear-query">Clear search</button></div>
    <div class="search-filters">
      <label for="sec">Stack<select id="sec" aria-label="Stack"><option value="">All stacks</option></select></label>
      <label for="material">Material<select id="material" aria-label="Material"><option value="">All material</option><option value="learn">Learn</option><option value="revision">Revision</option><option value="interview">Interview practice</option><option value="reference">Reference</option></select></label>
      <details class="advanced-filters"><summary>More filters</summary><div><label for="cat">Category<select id="cat" aria-label="Category"><option value="">All categories</option></select></label><label for="tag">Tag<select id="tag" aria-label="Tag"><option value="">All tags</option></select></label></div></details>
    </div>
  </form>
  <div id="selected-filters" class="selected-filters" aria-label="Selected filters"></div>
  <div class="result-heading"><p id="result-count" role="status" aria-live="polite"></p><button type="button" data-clear-filters hidden>Clear filters</button></div>
  <ol id="results" class="search-results"></ol>
  <section id="empty-state" hidden><h2>No topics match your search</h2><p>Try a shorter topic name or clear the selected filters.</p><a href="INDEX.html">Browse the library</a></section>
  <noscript><p>Search needs JavaScript. <a href="INDEX.html">Browse the full learning index</a>.</p></noscript>
  <p class="search-note">Searches titles, stack, category and tags · {N} chapters · <a href="INDEX.html">Browse the library</a></p>
</main>
<script id="study-search-data" type="application/json">{DATA}</script>
</body>
</html>
"""

def theme_src():
    """The theme script's `src`, read from its single owner in `_config.yml`.

    Rule 13 (scripts/check_verify_wiring.py) keeps the path in one place: the
    Jekyll include resolves `theme_asset` with `relative_url`, and this page
    gets it document-relative — no leading slash — because an absolute
    `/assets/...` resolves against the filesystem root under file:// and would
    silently drop the saved theme and the toggle wiring.
    """
    try:
        with open(CONFIG, encoding='utf-8') as handle:
            config_text = handle.read()
            declared = THEME_ASSET_RE.search(config_text)
            version = re.search(r'^theme_version:\s*([a-zA-Z0-9_-]+)\s*$', config_text, re.M)
    except OSError:
        declared = None
        version = None
    if declared is None:
        sys.exit('_config.yml must define theme_asset: <path> '
                 '(rule 13 owns the theme load path there)')
    return declared.group(1).lstrip('/') + ('?v=' + version.group(1) if version else '')


def render(rows):
    # Substitute only the owned placeholders; script data is escaped separately.
    page = PAGE.replace('{{', '{').replace('}}', '}')
    return (page
            .replace('{TITLE}', 'Software Developer Bible')
            .replace('{THEME_SRC}', theme_src())
            .replace('{N}', str(len(rows)))
            .replace('{DATA}', json.dumps(rows, ensure_ascii=False,
                                          separators=(',', ':')).replace('<', '\\u003c')))


def corpus_digest():
    """A digest of the corpus this dump describes.

    sha256 over each content file's own sha256, keyed by path and taken in
    `content_files()` order (sorted, so it is stable): any change to any
    chapter's bytes changes it, and — like the rest of this file — it carries
    no timestamp.

    Why it exists: the live probe can prove the *contract* holds at a stale
    deployment, because a stale deployment is still a working site. On
    2026-09-22 production served a bundle a commit behind HEAD for fifteen
    hours with every gate green. This field is what turns "the site is up"
    into "the site is this commit".
    """
    digest = hashlib.sha256()
    for rel in content_files():
        digest.update(rel.encode('utf-8'))
        digest.update(b'\0')
        with open(os.path.join(ROOT, rel), 'rb') as handle:
            digest.update(hashlib.sha256(handle.read()).digest())
    return digest.hexdigest()


def api_json(rows):
    """Machine-readable corpus API (docs/api-contract.md consumers).

    Deliberately timestamp-free: the freshness gate compares bytes, and a
    wall-clock field would make every run differ.
    """
    return json.dumps({
        'source': 'generated by scripts/gen_master_index.py from enforced file metadata (gate 6b) and read times (gate 13); do not edit',
        'consumers': ['repos/resume-generator', 'repos/docita'],
        'corpus_digest': corpus_digest(),
        'totals': {
            'chapters': len(rows),
            'sections': len({r['s'] for r in rows if r['s']}),
            'categories': len({r['c'] for r in rows if r['c']}),
            'read_minutes': sum(r['m'] for r in rows),
        },
        'chapters': sorted(rows, key=lambda r: r['p']),
    }, ensure_ascii=False, indent=1, separators=(',', ': ')) + '\n'


def main():
    rows = collect()
    html = render(rows)
    api = api_json(rows)
    if '--check' in sys.argv:
        problems = []
        if not os.path.exists(OUT):
            problems.append('search.html missing')
        elif open(OUT, encoding='utf-8').read() != html:
            problems.append('search.html drifted from the corpus')
        if not os.path.exists(API_OUT):
            problems.append('api/index.json missing')
        elif open(API_OUT, encoding='utf-8').read() != api:
            problems.append('api/index.json drifted from the corpus')
        if problems:
            print('; '.join(problems) + ' — run: python3 scripts/gen_master_index.py')
            return 1
        print(f'search.html + api/index.json in sync ({len(rows)} chapters)')
        return 0
    os.makedirs(os.path.dirname(API_OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(html)
    open(API_OUT, 'w', encoding='utf-8').write(api)
    print(f'search.html ({len(html) // 1024} KB) + api/index.json '
          f'({len(api) // 1024} KB) written ({len(rows)} chapters)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
