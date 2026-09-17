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
  python3 scripts/gen_master_index.py            # write search.html
  python3 scripts/gen_master_index.py --check    # gate: exit 1 on drift
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from read_time import content_files, minutes, human  # noqa: E402
from check_template import parse_meta  # noqa: E402

OUT = os.path.join(ROOT, 'search.html')
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
<title>{TITLE} — master index</title>
<style>
:root {{ color-scheme: light dark; }}
body {{ font-family: -apple-system, 'Segoe UI', Roboto, sans-serif;
       max-width: 1100px; margin: 0 auto; padding: 1rem 1.2rem 4rem;
       line-height: 1.45; }}
h1 {{ font-size: 1.4rem; margin-bottom: .2rem; }}
.sub {{ opacity: .7; margin: 0 0 1rem; font-size: .92rem; }}
#q {{ width: 100%; box-sizing: border-box; font-size: 1rem;
     padding: .55rem .8rem; margin: .4rem 0 1rem;
     border: 1px solid #8886; border-radius: 8px; }}
.chips {{ display: flex; flex-wrap: wrap; gap: .35rem; margin: .25rem 0; }}
.chips button {{ font-size: .8rem; padding: .18rem .6rem; border-radius: 999px;
  border: 1px solid #8886; background: transparent; cursor: pointer; }}
.chips button.on {{ background: #4a7dff; border-color: #4a7dff; color: #fff; }}
#stats {{ font-size: .9rem; opacity: .75; margin: .8rem 0; }}
table {{ width: 100%; border-collapse: collapse; font-size: .92rem; }}
th {{ text-align: left; border-bottom: 2px solid #8886; padding: .3rem .5rem; }}
td {{ border-bottom: 1px solid #8884; padding: .32rem .5rem; }}
td.m, th.m {{ text-align: right; white-space: nowrap; }}
a {{ text-decoration: none; }} a:hover {{ text-decoration: underline; }}
.tag {{ opacity: .7; font-size: .8rem; }}
.hidden {{ display: none; }}
</style>
</head>
<body>
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
                        b.classList.toggle('on'); render(); }};
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

$('q').oninput = e => {{ state.q = e.target.value.trim().toLowerCase(); render(); }};
chips($('cats'), {CATS}, state.cats);
chips($('secs'), {SECS}, state.secs);
chips($('tags'), TOP_TAGS, state.tags);
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


def main():
    html = render(collect())
    if '--check' in sys.argv:
        if not os.path.exists(OUT):
            print('search.html missing — run: python3 scripts/gen_master_index.py')
            return 1
        if open(OUT, encoding='utf-8').read() != html:
            print('search.html drifted from the corpus — '
                  'run: python3 scripts/gen_master_index.py')
            return 1
        print(f'search.html in sync ({len(json.loads(html.split("const DATA = ")[1].split("];")[0] + "]"))} chapters)')
        return 0
    open(OUT, 'w', encoding='utf-8').write(html)
    print(f'search.html written ({len(html) // 1024} KB)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
