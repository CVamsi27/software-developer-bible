#!/usr/bin/env python3
"""Generate search.html — a filterable master index over the whole corpus.

The data comes from the same metadata gate 6b enforces (check_template.
parse_meta) and the same read-time model gate 13 enforces, so the page
cannot drift from the corpus: gate 14 regenerates it in memory and fails
if the committed file differs.

Output is a static HTML file (no Jekyll front matter -> copied verbatim,
no Liquid escaping needed) with the corpus embedded as JSON and vanilla
JS filtering — no dependencies, works offline and from file://.

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
<script>
  (function() {{
    var savedTheme = localStorage.getItem("sdb-theme");
    if (savedTheme === "dark" || savedTheme === "light") {{
      document.documentElement.setAttribute("data-theme", savedTheme);
    }}
  }})();
</script>
<style>
:root {{ color-scheme: light dark; }}
html[data-theme="light"] {{ color-scheme: light; }}
html[data-theme="dark"] {{ color-scheme: dark; }}
body {{ font-family: -apple-system, 'Segoe UI', Roboto, sans-serif;
       max-width: 1100px; margin: 0 auto; padding: 1rem 1.2rem 4rem;
       line-height: 1.45; }}
h1 {{ font-size: 1.4rem; margin-bottom: .2rem; }}
.sub {{ opacity: .7; margin: 0 0 1rem; font-size: .92rem; }}
.nav-back {{ margin-bottom: .6rem; font-size: .92rem; }}
#q {{ width: 100%; box-sizing: border-box; font-size: 1rem;
     padding: .55rem .8rem; margin: .4rem 0 1rem;
     border: 1px solid #8886; border-radius: 8px; }}
.chips {{ display: flex; flex-wrap: wrap; gap: .35rem; margin: .25rem 0; }}
.chips button {{ font-size: .8rem; padding: .18rem .6rem; border-radius: 999px;
  border: 1px solid #8886; background: transparent; cursor: pointer; color: inherit; }}
.chips button.on {{ background: #4a7dff; border-color: #4a7dff; color: #fff; }}
#stats {{ font-size: .9rem; opacity: .75; margin: .8rem 0; }}
table {{ width: 100%; border-collapse: collapse; font-size: .92rem; }}
th {{ text-align: left; border-bottom: 2px solid #8886; padding: .3rem .5rem; }}
td {{ border-bottom: 1px solid #8884; padding: .32rem .5rem; }}
td.m, th.m {{ text-align: right; white-space: nowrap; }}
a {{ text-decoration: none; color: #3b82f6; }} a:hover {{ text-decoration: underline; }}
.tag {{ opacity: .7; font-size: .8rem; }}
.hidden {{ display: none; }}
</style>
</head>
<body>
<div class="nav-back"><a href="INDEX.html">← Back to Master Index</a></div>
<h1>{TITLE} — master index</h1>
<p class="sub">{N} chapters · {TIME} of reading · generated from enforced file
metadata by <code>scripts/gen_master_index.py</code> — do not edit by hand
(gate 14 regenerates it; run that script to refresh).</p>
<input id="q" type="search" placeholder="Filter by title, section, tag…"
       autocomplete="off" autofocus>
<div class="chips" id="cats"></div>
<div class="chips" id="secs"></div>
<div class="chips" id="tags"></div>
<p id="stats"></p>
<table>
<thead><tr><th>Chapter</th><th>Section</th><th>Tags</th><th class="m">Read</th></tr></thead>
<tbody id="rows"></tbody>
</table>
<script>
const DATA = {DATA};
const TOP_TAGS = {TOP_TAGS};
const $ = id => document.getElementById(id);
const state = {{ q: '', cats: new Set(), secs: new Set(), tags: new Set() }};

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

function render() {{
  const rows = DATA.filter(match);
  const total = rows.reduce((a, r) => a + r.m, 0);
  $('stats').textContent =
    `${{rows.length}} / ${{DATA.length}} chapters · ~${{fmt(total)}} of reading`;
  $('rows').innerHTML = rows.map(r =>
    `<tr><td><a href="${{r.p}}">${{r.t}}</a></td>` +
    `<td>${{r.s}}</td>` +
    `<td class="tag">${{r.g.join(', ')}}</td>` +
    `<td class="m">${{fmt(r.m)}}</td></tr>`).join('');
}}

$('q').oninput = e => {{ state.q = e.target.value.trim().toLowerCase(); render(); syncUrl(); }};
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
