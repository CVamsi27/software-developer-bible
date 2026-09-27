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
from read_time import content_files, minutes, human  # noqa: E402
from check_template import parse_meta  # noqa: E402

OUT = os.path.join(ROOT, 'search.html')
API_OUT = os.path.join(ROOT, 'api', 'index.json')
CONFIG = os.path.join(ROOT, '_config.yml')
THEME_ASSET_RE = re.compile(r'^theme_asset:\s*(\S+)\s*$', re.M)
H1 = re.compile(r'^# (?!#)\s*(.+?)\s*$', re.M)
MAX_TAGS = 24          # chips rendered for the top tags; the rest stay searchable
MIN_TAG_COUNT = 4      # tags below this are not offered as chips


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
<title>{TITLE} — Master Search Index</title>
<script src="{THEME_SRC}"></script>
<style>
  :root, html[data-theme="light"] {{
    --theme-bg: #ffffff;
    --theme-text: #1f2937;
    --theme-text-muted: #64748b;
    --theme-heading: #0f172a;
    --theme-border: #e2e8f0;
    --theme-border-subtle: #f1f5f9;
    --theme-link: #2563eb;
    --theme-link-hover: #1d4ed8;
    --theme-accent: #3b82f6;
    --card-bg: #ffffff;
    --input-bg: #ffffff;
    --chip-bg: #f1f5f9;
    --chip-hover: #e2e8f0;
    --chip-text: #475569;
    --chip-active-bg: #2563eb;
    --chip-active-text: #ffffff;
    --row-hover: rgba(59, 130, 246, 0.05);
    --row-selected: rgba(59, 130, 246, 0.12);
    --kbd-bg: #f1f5f9;
    --kbd-border: #cbd5e1;
  }}

  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --theme-bg: #0b1114;
      --theme-text: #cbd5e1;
      --theme-text-muted: #94a3b8;
      --theme-heading: #f8fafc;
      --theme-border: #1e293b;
      --theme-border-subtle: #151e28;
      --theme-link: #60a5fa;
      --theme-link-hover: #93c5fd;
      --theme-accent: #3b82f6;
      --card-bg: #10171d;
      --input-bg: #0e151b;
      --chip-bg: #151e26;
      --chip-hover: #22303c;
      --chip-text: #cbd5e1;
      --chip-active-bg: #3b82f6;
      --chip-active-text: #ffffff;
      --row-hover: rgba(59, 130, 246, 0.08);
      --row-selected: rgba(59, 130, 246, 0.22);
      --kbd-bg: #151e26;
      --kbd-border: #334155;
    }}
  }}

  html[data-theme="dark"] {{
    --theme-bg: #0b1114;
    --theme-text: #cbd5e1;
    --theme-text-muted: #94a3b8;
    --theme-heading: #f8fafc;
    --theme-border: #1e293b;
    --theme-border-subtle: #151e28;
    --theme-link: #60a5fa;
    --theme-link-hover: #93c5fd;
    --theme-accent: #3b82f6;
    --card-bg: #10171d;
    --input-bg: #0e151b;
    --chip-bg: #151e26;
    --chip-hover: #22303c;
    --chip-text: #cbd5e1;
    --chip-active-bg: #3b82f6;
    --chip-active-text: #ffffff;
    --row-hover: rgba(59, 130, 246, 0.08);
    --row-selected: rgba(59, 130, 246, 0.22);
    --kbd-bg: #151e26;
    --kbd-border: #334155;
  }}

  ::selection {{
    background-color: rgba(59, 130, 246, 0.25);
    color: inherit;
  }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    max-width: 1140px;
    margin: 0 auto;
    padding: 1.5rem 1.5rem 4rem;
    line-height: 1.5;
    background-color: var(--theme-bg);
    color: var(--theme-text);
    -webkit-font-smoothing: antialiased;
  }}

  .top-bar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.25rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--theme-border);
  }}

  .nav-back {{
    font-size: 0.92rem;
    font-weight: 550;
  }}

  .theme-toggle-btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    border-radius: 8px;
    border: 1px solid var(--theme-border);
    background-color: var(--chip-bg);
    color: var(--theme-text);
    cursor: pointer;
    transition: all 0.2s ease;
  }}

  .theme-toggle-btn:hover {{
    background-color: var(--chip-hover);
    border-color: var(--theme-accent);
    color: var(--theme-accent);
    transform: scale(1.05);
  }}

  .theme-toggle-btn svg {{
    display: block;
    width: 17px;
    height: 17px;
  }}

  h1 {{
    font-size: 1.65rem;
    font-weight: 750;
    color: var(--theme-heading);
    margin: 0 0 0.4rem;
    letter-spacing: -0.025em;
  }}

  .sub {{
    color: var(--theme-text-muted);
    margin: 0 0 1.25rem;
    font-size: 0.92rem;
  }}

  .search-container {{
    position: relative;
    margin: 1rem 0;
  }}

  .search-box-wrapper {{
    position: relative;
    display: flex;
    align-items: center;
  }}

  .search-icon {{
    position: absolute;
    left: 14px;
    width: 18px;
    height: 18px;
    color: var(--theme-text-muted);
    pointer-events: none;
  }}

  #q {{
    width: 100%;
    box-sizing: border-box;
    font-size: 1.05rem;
    padding: 0.75rem 2.5rem 0.75rem 2.6rem;
    border: 1.5px solid var(--theme-border);
    border-radius: 10px;
    background-color: var(--input-bg);
    color: var(--theme-text);
    outline: none;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
  }}

  #q:focus {{
    border-color: var(--theme-accent);
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
  }}

  .clear-btn {{
    position: absolute;
    right: 12px;
    background: transparent;
    border: none;
    color: var(--theme-text-muted);
    cursor: pointer;
    font-size: 1rem;
    padding: 4px 8px;
    border-radius: 4px;
    display: none;
  }}

  .clear-btn:hover {{
    color: var(--theme-heading);
  }}

  .keyboard-hints {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 12px;
    margin-top: 6px;
    font-size: 0.78rem;
    color: var(--theme-text-muted);
  }}

  kbd {{
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: 0.75rem;
    background-color: var(--kbd-bg);
    border: 1px solid var(--kbd-border);
    border-radius: 4px;
    padding: 1px 5px;
    box-shadow: 0 1px 1px rgba(0, 0, 0, 0.05);
  }}

  .chips-group {{
    margin: 0.75rem 0;
  }}

  .chips-label {{
    font-size: 0.78rem;
    font-weight: 650;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--theme-text-muted);
    margin-bottom: 0.35rem;
  }}

  .chips {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
  }}

  .chips button {{
    font-size: 0.8rem;
    padding: 0.24rem 0.65rem;
    border-radius: 999px;
    border: 1px solid var(--theme-border);
    background-color: var(--chip-bg);
    cursor: pointer;
    color: var(--chip-text);
    transition: all 0.15s ease;
  }}

  .chips button:hover {{
    background-color: var(--chip-hover);
    border-color: var(--theme-accent);
  }}

  .chips button.on {{
    background-color: var(--chip-active-bg);
    border-color: var(--chip-active-bg);
    color: var(--chip-active-text);
    font-weight: 550;
  }}

  #stats {{
    font-size: 0.9rem;
    color: var(--theme-text-muted);
    margin: 1.25rem 0 0.75rem;
    font-weight: 550;
  }}

  .table-wrapper {{
    overflow-x: auto;
    border: 1px solid var(--theme-border);
    border-radius: 10px;
    background-color: var(--card-bg);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.91rem;
    margin: 0;
  }}

  th {{
    text-align: left;
    background-color: var(--theme-border-subtle);
    color: var(--theme-heading);
    font-weight: 650;
    border-bottom: 2px solid var(--theme-border);
    padding: 0.6rem 0.85rem;
    white-space: nowrap;
  }}

  td {{
    border-bottom: 1px solid var(--theme-border);
    padding: 0.55rem 0.85rem;
    vertical-align: middle;
  }}

  tr:last-child td {{
    border-bottom: none;
  }}

  tr.active-row {{
    background-color: var(--row-selected) !important;
  }}

  tr:hover {{
    background-color: var(--row-hover);
  }}

  td.m, th.m {{
    text-align: right;
    white-space: nowrap;
  }}

  .chapter-title-link {{
    font-weight: 600;
    color: var(--theme-link);
    text-decoration: none;
  }}

  .chapter-title-link:hover {{
    text-decoration: underline;
    color: var(--theme-link-hover);
  }}

  a {{
    text-decoration: none;
    color: var(--theme-link);
  }}

  a:hover {{
    text-decoration: underline;
  }}

  .tag-badge {{
    display: inline-block;
    font-size: 0.75rem;
    padding: 1px 6px;
    margin: 2px 3px 2px 0;
    border-radius: 4px;
    background-color: var(--theme-border-subtle);
    border: 1px solid var(--theme-border);
    color: var(--theme-text-muted);
  }}

  .read-badge {{
    font-size: 0.82rem;
    font-weight: 550;
    color: var(--theme-text-muted);
    font-variant-numeric: tabular-nums;
  }}

  .hidden {{
    display: none;
  }}
</style>
</head>
<body>
<div class="top-bar">
  <div class="nav-back"><a href="INDEX.html">← Back to Master Index</a></div>
  <button id="theme-btn" class="theme-toggle-btn" type="button" aria-label="Toggle color theme" title="Toggle dark/light mode"></button>
</div>
<h1>{TITLE} — master index</h1>
<p class="sub">{N} chapters · {TIME} of reading · generated from enforced file
metadata by <code>scripts/gen_master_index.py</code> — do not edit by hand
(gate 14 regenerates it; run that script to refresh).</p>
<div class="search-container">
  <div class="search-box-wrapper">
    <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
    <input id="q" type="search" placeholder="Search {N} chapters by title, section, category, tags…"
           autocomplete="off" autofocus>
    <button id="clear-btn" class="clear-btn" type="button" title="Clear search">✕</button>
  </div>
  <div class="keyboard-hints">
    <span><kbd>Esc</kbd> to clear</span>
    <span><kbd>↑</kbd> <kbd>↓</kbd> to navigate</span>
    <span><kbd>Enter</kbd> to open chapter</span>
  </div>
</div>
<div class="chips-group"><div class="chips-label">Categories</div><div class="chips" id="cats"></div></div>
<div class="chips-group"><div class="chips-label">Sections</div><div class="chips" id="secs"></div></div>
<div class="chips-group"><div class="chips-label">Popular Tags</div><div class="chips" id="tags"></div></div>
<p id="stats"></p>
<div class="table-wrapper">
<table>
<thead><tr><th>Chapter</th><th>Section</th><th>Tags</th><th class="m">Read</th></tr></thead>
<tbody id="rows"></tbody>
</table>
</div>
<script>
const DATA = {DATA};
const TOP_TAGS = {TOP_TAGS};
const $ = id => document.getElementById(id);
const state = {{ q: '', cats: new Set(), secs: new Set(), tags: new Set() }};
let selectedRowIndex = -1;
let currentFilteredRows = [];

function chips(el, values, set) {{
  el.innerHTML = '';
  for (const v of values) {{
    const b = document.createElement('button');
    b.textContent = v;
    b.onclick = () => {{ set.has(v) ? set.delete(v) : set.add(v);
                        b.classList.toggle('on'); render(); syncUrl(); }};
    el.appendChild(b);
  }}
}}

function match(r) {{
  if (state.cats.size && !state.cats.has(r.c)) return false;
  if (state.secs.size && !state.secs.has(r.s)) return false;
  if (state.tags.size && !r.g.some(t => state.tags.has(t))) return false;
  if (state.q) {{
    const hay = (r.t + ' ' + r.s + ' ' + r.c + ' ' + r.g.join(' ')).toLowerCase();
    if (!hay.includes(state.q)) return false;
  }}
  return true;
}}

function fmt(m) {{ const h = Math.floor(m / 60);
  return h ? `${{h}}h ${{m % 60}}m` : `${{m}}m`; }}

function updateRowSelection() {{
  const trs = $('rows').querySelectorAll('tr');
  trs.forEach((tr, i) => {{
    if (i === selectedRowIndex) {{
      tr.classList.add('active-row');
      tr.scrollIntoView({{ block: 'nearest', behavior: 'smooth' }});
    }} else {{
      tr.classList.remove('active-row');
    }}
  }});
}}

function render() {{
  currentFilteredRows = DATA.filter(match);
  selectedRowIndex = -1;
  const total = currentFilteredRows.reduce((a, r) => a + r.m, 0);
  $('stats').textContent =
    `${{currentFilteredRows.length}} / ${{DATA.length}} chapters · ~${{fmt(total)}} of reading`;
  $('rows').innerHTML = currentFilteredRows.map((r, i) =>
    `<tr data-idx="${{i}}"><td><a class="chapter-title-link" href="${{r.p}}">${{r.t}}</a></td>` +
    `<td>${{r.s}}</td>` +
    `<td>${{r.g.map(tag => `<span class="tag-badge">${{tag}}</span>`).join('')}}</td>` +
    `<td class="m"><span class="read-badge">${{fmt(r.m)}}</span></td></tr>`).join('');
  $('clear-btn').style.display = state.q ? 'block' : 'none';
}}

$('q').oninput = e => {{
  state.q = e.target.value.trim().toLowerCase();
  render();
  syncUrl();
}};

$('clear-btn').onclick = () => {{
  $('q').value = '';
  state.q = '';
  render();
  syncUrl();
  $('q').focus();
}};

// Keyboard navigation
document.addEventListener('keydown', e => {{
  if (e.key === 'ArrowDown') {{
    if (currentFilteredRows.length > 0) {{
      e.preventDefault();
      selectedRowIndex = Math.min(selectedRowIndex + 1, currentFilteredRows.length - 1);
      updateRowSelection();
    }}
  }} else if (e.key === 'ArrowUp') {{
    if (currentFilteredRows.length > 0) {{
      e.preventDefault();
      selectedRowIndex = Math.max(selectedRowIndex - 1, 0);
      updateRowSelection();
    }}
  }} else if (e.key === 'Enter') {{
    if (selectedRowIndex >= 0 && selectedRowIndex < currentFilteredRows.length) {{
      e.preventDefault();
      window.location.href = currentFilteredRows[selectedRowIndex].p;
    }}
  }} else if (e.key === 'Escape') {{
    if (state.q || $('q').value) {{
      e.preventDefault();
      $('q').value = '';
      state.q = '';
      render();
      syncUrl();
    }}
  }}
}});

chips($('cats'), {CATS}, state.cats);
chips($('secs'), {SECS}, state.secs);
chips($('tags'), TOP_TAGS, state.tags);

// Deep links: ?q=&cat=&sec=&tag= restore state, every change syncs the URL.
function syncUrl() {{
  const p = new URLSearchParams();
  if (state.q) p.set('q', state.q);
  if (state.cats.size) p.set('cat', [...state.cats].join(','));
  if (state.secs.size) p.set('sec', [...state.secs].join(','));
  if (state.tags.size) p.set('tag', [...state.tags].join(','));
  try {{ history.replaceState(null, '', p.toString() ? '?' + p : location.pathname); }}
  catch (e) {{ /* file:// may block replaceState — filtering still works */ }}
}}

const params = new URLSearchParams(location.search);
if (params.get('q')) {{ state.q = params.get('q').toLowerCase(); $('q').value = params.get('q'); }}
for (const k of (params.get('cat') || '').split(',')) if (k) state.cats.add(k);
for (const k of (params.get('sec') || '').split(',')) if (k) state.secs.add(k);
for (const k of (params.get('tag') || '').split(',')) if (k) state.tags.add(k);
for (const b of document.querySelectorAll('.chips button'))
  if (state.cats.has(b.textContent) || state.secs.has(b.textContent) ||
      state.tags.has(b.textContent)) b.classList.add('on');
render();
</script>
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
            declared = THEME_ASSET_RE.search(handle.read())
    except OSError:
        declared = None
    if declared is None:
        sys.exit('_config.yml must define theme_asset: <path> '
                 '(rule 13 owns the theme load path there)')
    return declared.group(1).lstrip('/')


def render(rows):
    from collections import Counter
    cats = sorted({r['c'] for r in rows if r['c']})
    secs = sorted({r['s'] for r in rows if r['s']})
    tag_n = Counter(t for r in rows for t in r['g'])
    top = [t for t, n in tag_n.most_common() if n >= MIN_TAG_COUNT][:MAX_TAGS]
    total = sum(r['m'] for r in rows)
    # PAGE is written with doubled braces for readability; substitution is
    # plain .replace (not str.format), so undouble before placeholders.
    page = PAGE.replace('{{', '{').replace('}}', '}')
    return (page
            .replace('{TITLE}', 'Software Developer Bible')
            .replace('{THEME_SRC}', theme_src())
            .replace('{N}', str(len(rows)))
            .replace('{TIME}', human(total))
            .replace('{DATA}', json.dumps(rows, ensure_ascii=False,
                                          separators=(',', ':')))
            .replace('{TOP_TAGS}', json.dumps(top))
            .replace('{CATS}', json.dumps(cats))
            .replace('{SECS}', json.dumps(secs)))


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
