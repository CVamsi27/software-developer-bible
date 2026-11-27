# Final Performance and Reader UX Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task with checkpoints.

**Goal:** Reduce avoidable repeated page payload, make page-weight enforcement use gzip transport size, and improve search loading and error user experience (UX) without changing authored study content or reader navigation contracts.

**Architecture:** The existing inline reader shell becomes two static, versioned assets loaded by the shared Jekyll head. The generated search page loads a relative generated JavaScript catalog from `api/`, preserving offline `file://` previews while removing the large inline metadata blob; search consumes the explicit `window.__SDB_SEARCH_DATA__` interface and exposes loading and failure status, while page-weight reporting retains raw and gzip measurements as `--check` enforces the portable gzip budget.

**Tech Stack:** Jekyll 3.10.0, Ruby 3.4.11, Python 3.15, vanilla JavaScript, Node.js 26, Node test runner, optional `jsdom` 26.1.0, and repository verification scripts.

## Global Constraints

- Preserve all authored prose, question-and-answer (Q&A) pairs, code, heading IDs, anchors, and file identities.
- Do not split or renumber long pages merely to lower raw HTML bytes.
- Do not expose private lane or personal data in generated search assets.
- Do not claim browser coverage when the browser dependency is unavailable.
- Do not change authentication, deployment, or Cloudflare behavior.
- Keep generated files synchronized through repository-owned writers.
- Preserve relative URL and `file://` behavior for the generated search page.

---

## File Map

| File | Responsibility in this pass |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `_includes/head-custom.html` | Load the extracted reader-shell CSS and JavaScript and retain small Jekyll-owned configuration values. |
| `assets/reader-shell.css` | Cacheable copy of the shared inline reader stylesheet. |
| `assets/reader-shell.js` | Cacheable copy of the shared inline reader behavior. |
| `scripts/gen_master_index.py` | Generate and validate `api/search-index.js`, `search.html`, and `api/index.json`. |
| `api/search-index.js` | Generated browser-readable catalog assigned to `window.__SDB_SEARCH_DATA__`. |
| `search.html` | Generated search page with external catalog loading and accessible status and error markup. |
| `assets/search-ui.js` | Consume the external catalog and render loading and failure states without losing URL state. |
| `assets/search-ui.css` | Style the actionable search failure state without changing existing result layout. |
| `assets/study-ui.test.cjs` | Regression tests for external catalog data, failure UX, and the extracted reader shell. |
| `scripts/measure_page_weight.py` | Report raw diagnostics and enforce the gzip transport budget. |
| `docs/corpus-review/README.md` | Document raw-versus-gzip measurement and the enforced budget. |
| `docs/scripts-map.md` | Keep the measurement workflow description accurate. |
| `docs/corpus-review/page-weight.json` | Generated post-build raw and gzip measurements. |
| `docs/review-ledger.json` | Restamp `fast` evidence for reviewed files after rendered weights change. |

## Task 1: Add failing regression coverage

**Files:**
- Modify: `assets/study-ui.test.cjs:118-139, 248-260`

**Interfaces:**
- Consumes: `window.__SDB_SEARCH_DATA__` as an array of rows with `p`, `t`, `s`, `c`, `g`, and `m` fields.
- Produces: tests that fail until the generated catalog, failure state, and extracted `assets/reader-shell.js` exist.
- [ ] **Step 1: Change the search fixture to inject the future external catalog interface**

Replace the two test fixtures that append `#study-search-data` with setup callbacks that assign the same rows to the window:

```javascript
const rows = [
  {p: chapter.slice(1), t: 'Scope lesson', s: 'JavaScript', c: 'Core', g: ['concept'], m: 15},
  {p: revision.slice(1), t: 'Scope revision', s: 'JavaScript', c: 'Reference', g: ['revision'], m: 4},
  {p: 'other.html', t: 'Other topic', s: 'Node.js', c: 'Core', g: [], m: 5},
];
const dom = boot(searchHtml, '/search.html?q=scope', ['search-ui.js'], w => {
  w.__SDB_SEARCH_DATA__ = rows;
});
```

Keep the existing filter, clear, Back-state and repeated-revision-title assertions.

- [ ] **Step 2: Add the actionable catalog-failure test**

Add a test after the successful search tests:

```javascript
test('search exposes an actionable failure when the generated catalog is unavailable', () => {
  const searchHtml = fs.readFileSync(path.join(root, 'search.html'), 'utf8')
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/g, '');
  const dom = boot(searchHtml, '/search.html', ['search-ui.js'], w => {
    w.__SDB_SEARCH_DATA__ = null;
  });
  const d = dom.window.document;
  assert.match(d.querySelector('#result-count').textContent, /could not load/i);
  assert.equal(d.querySelector('#search-error').hidden, false);
  assert.equal(d.querySelector('#search-error a').getAttribute('href'), 'INDEX.html');
  dom.window.close();
});
```

- [ ] **Step 3: Point the copy-control test at the extracted shell asset**

Replace the current `head-custom.html` substring extraction in the copy test with:

```javascript
const shell = fs.readFileSync(path.join(root, 'assets/reader-shell.js'), 'utf8');
w.eval(shell);
```

- [ ] **Step 4: Run the focused test and confirm the expected pre-implementation failure**

Run:

```bash
UI_DEPS=$(mktemp -d)
npm install --prefix "$UI_DEPS" --no-audit --no-fund jsdom@26.1.0
NODE_PATH="$UI_DEPS/node_modules" /opt/homebrew/bin/node --test assets/study-ui.test.cjs
```

Expected: the external-data and extracted-shell tests fail because the current page still owns `#study-search-data` and `assets/reader-shell.js` does not exist. Remove the temporary dependency directory after the run.

## Task 2: Extract the shared reader shell without changing behavior

**Files:**
- Create: `assets/reader-shell.css`
- Create: `assets/reader-shell.js`
- Modify: `_includes/head-custom.html:12-1214`

**Interfaces:**
- Consumes: the exact current Liquid-protected stylesheet and DOMContentLoaded reader-shell handler from `_includes/head-custom.html`.
- Produces: `/assets/reader-shell.css?v=reader-shell-1` and `/assets/reader-shell.js?v=reader-shell-1`, loaded before the existing deferred reader modules.
- [ ] **Step 1: Copy the existing raw stylesheet into the static CSS asset**

Copy the bytes inside the current Liquid-protected `<style>` block into `assets/reader-shell.css`, removing only the `<style>` wrapper and preserving selectors, declarations, comments, media queries and ordering. The new file must contain no Liquid tags.

- [ ] **Step 2: Copy the current reader-shell handler into the static JavaScript asset**

Copy the current `document.addEventListener("DOMContentLoaded", function() { ... });` block into `assets/reader-shell.js` unchanged. Do not move the later `reading-ui.js`, `read-aloud.js`, `revision-ui.js` or `study-resume.js` logic into this file.

- [ ] **Step 3: Replace the inline blocks with versioned asset links**

Replace the large raw/style/script region with:

```liquid
<link rel="stylesheet" href="{{ '/assets/reader-shell.css' | relative_url }}?v=reader-shell-1">
<script src="{{ '/assets/reader-shell.js' | relative_url }}?v=reader-shell-1" defer></script>
```

Keep the Jekyll-owned favicon, font preload, search URL, theme script, read-aloud stylesheet and existing deferred module order intact.

- [ ] **Step 4: Run syntax and source checks**

Run:

```bash
/opt/homebrew/bin/node --check assets/reader-shell.js
python3 scripts/check_code_whitespace.py
python3 scripts/test_md_fences.py
```

Expected: all commands pass, with no code-fence or whitespace changes caused by the extraction.

## Task 3: Generate an external search catalog and accessible state

**Files:**
- Modify: `scripts/gen_master_index.py:9-18, 32-34, 60-127, 152-161, 206-229`
- Modify: `assets/search-ui.js:1-118`
- Modify: `assets/search-ui.css:147-153`
- Generated: `api/search-index.js`
- Generated: `search.html`

**Interfaces:**
- Consumes: the existing `collect()` row list.
- Produces: `api/search-index.js` containing `window.__SDB_SEARCH_DATA__ = <JSON>;` and a generated page that loads it with a document-relative `api/search-index.js` script.
- [ ] **Step 1: Add the generated catalog output and serializer**

Add:

```python
SEARCH_DATA_OUT = os.path.join(ROOT, 'api', 'search-index.js')

def search_data_js(rows):
    data = json.dumps(rows, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    return f'window.__SDB_SEARCH_DATA__ = {data};\n'
```

Keep `api/index.json` as the machine-readable JSON API; the JavaScript catalog is a browser transport artifact, not a replacement for that API.

- [ ] **Step 2: Replace the inline search data in the generated page**

Change `PAGE` to:

```html
<script src="api/search-index.js" defer></script>
<script src="assets/search-ui.js?v=study-flow-23" defer></script>
```

Replace the inline data element with:

```html
<p id="search-status" role="status" aria-live="polite">Loading the library…</p>
<section id="search-error" class="search-error" hidden>
  <h2>Search is temporarily unavailable</h2>
  <p>Browse the library directly while the search catalog reloads.</p>
  <a href="INDEX.html">Browse the library</a>
</section>
```

Keep the existing `#result-count` status, results list, empty state, `noscript` fallback and topic count.

- [ ] **Step 3: Validate and write the new generated artifact**

In `main()`:

```python
rows = collect()
html = render(rows)
search_data = search_data_js(rows)
api = api_json(rows)
```

In check mode, fail if `api/search-index.js` is missing or differs. In write mode, write it beside `api/index.json` and include its path in the success message. Keep the existing `search.html` and `api/index.json` drift checks.

- [ ] **Step 4: Consume the global catalog and make failure explicit**

At the start of the DOMContentLoaded handler, replace the inline-element lookup with:

```javascript
var rows = Array.isArray(window.__SDB_SEARCH_DATA__)
  ? window.__SDB_SEARCH_DATA__
  : null;
var status = document.getElementById('search-status');
var error = document.getElementById('search-error');
if (!rows) {
  document.getElementById('result-count').textContent =
    'Search could not load. Browse the library or reload to try again.';
  status.textContent = 'Search catalog unavailable.';
  error.hidden = false;
  return;
}
status.hidden = true;
```

Retain the current `state`, `restore`, `sync`, `render`, filter, keyboard,
roadmap-context and Back-state logic. Remove the old `study-search-data` JSON
parse and the duplicate dynamic `study-catalog.js` loading branch.

- [ ] **Step 5: Add only the failure-state styling**

Add a compact rule beside `#empty-state`:

```css
.search-error {
  padding: 24px;
  margin-top: 24px;
  border: 1px solid var(--theme-border);
  border-radius: 12px;
  background: var(--card-bg);
}
.search-error h2 { margin: 0 0 8px; font-size: 1.25rem; }
.search-error p { margin: 0 0 12px; color: var(--theme-text-muted); }
```

- [ ] **Step 6: Regenerate and run focused search tests**

Run:

```bash
python3 scripts/gen_master_index.py
python3 scripts/gen_master_index.py --check
UI_DEPS=$(mktemp -d)
npm install --prefix "$UI_DEPS" --no-audit --no-fund jsdom@26.1.0
NODE_PATH="$UI_DEPS/node_modules" /opt/homebrew/bin/node --test assets/study-ui.test.cjs
```

Expected: the generated search page has no `study-search-data` element, the
external catalog contains all current rows, filter/Back behavior passes, and
the unavailable-catalog test exposes the library link. Remove the temporary
dependency directory after the run.

## Task 4: Make page-weight enforcement transport-realistic

**Files:**
- Modify: `scripts/measure_page_weight.py:9-18, 35-38, 149-197`
- Modify: `docs/corpus-review/README.md:27-65`
- Modify: `docs/scripts-map.md:108-112`

**Interfaces:**
- Consumes: built HTML rows with `rawBytes` and `gzipBytes`.
- Produces: `--check` failures based on `gzipBytes`, with raw-size diagnostics and a generated `budgetGzipBytes` field.
- [ ] **Step 1: Change the default budget constant and CLI name**

Use:

```python
RAW_DIAGNOSTIC_BUDGET_BYTES = 120_000
BUDGET_GZIP_BYTES = 64 * 1024
```

Keep `--budget` as a backwards-compatible alias for the enforced gzip budget, updating its help text to say "gzip transport budget", and add `--budget-gzip` with the same destination if the parser needs an explicit descriptive name.

- [ ] **Step 2: Keep raw diagnostics and enforce gzip**

Compute both reports:

```python
raw_over = [r for r in built if r["rawBytes"] > RAW_DIAGNOSTIC_BUDGET_BYTES]
over = [r for r in built if r["gzipBytes"] > args.budget_gzip]
```

Print the raw exception count as diagnostic information, print the enforced gzip
budget and offending gzip rows, and return failure only when `over` is non-empty.

- [ ] **Step 3: Update generated metadata and documentation**

Write:

```python
"rawDiagnosticBudgetBytes": RAW_DIAGNOSTIC_BUDGET_BYTES,
"budgetGzipBytes": args.budget_gzip,
```

Document that gzip is the enforced portable transfer floor, raw HTML remains a
DOM/diagnostic signal, and long-form interview/revision pages can remain raw-size
exceptions when their compressed transfer is within budget.

- [ ] **Step 4: Run the measurement check before a full build**

Run:

```bash
python3 -m py_compile scripts/measure_page_weight.py
python3 scripts/measure_page_weight.py --check
```

Expected: the command uses the new gzip metric; before the asset extraction
build it may still report any page above 64 KB gzip, but it must no longer report
the nine raw-byte-only exceptions as failures.

## Task 5: Build, refresh measurements, and restamp review evidence

**Files:**
- Generated: `docs/corpus-review/page-weight.json`
- Modify: `docs/review-ledger.json` fast evidence only

**Interfaces:**
- Consumes: the production `_site` produced by the pinned Jekyll bundle.
- Produces: current rendered byte measurements and exact fast-axis strings for every read-backed ledger row.
- [ ] **Step 1: Build with the pinned toolchain**

Run:

```bash
PATH=/opt/homebrew/opt/ruby@3.4/bin:$PATH \
BUNDLE_PATH=vendor/bundle \
JEKYLL_ENV=production \
bundle exec jekyll build
```

Expected: the build succeeds with only the existing non-fatal Faraday retry
middleware notice.

- [ ] **Step 2: Regenerate page weights**

Run:

```bash
python3 scripts/measure_page_weight.py --write
python3 scripts/measure_page_weight.py --check
```

Expected: every built page is within the enforced gzip budget; raw-size
exceptions, if any, are printed as diagnostics rather than failures.

- [ ] **Step 3: Restamp only fast evidence for reviewed files**

Generate a temporary batch from `docs/review-ledger.json` that copies each read row's `current`, `readable`, `concise`, `focused`, and `best` values unchanged and replaces only `fast` with:

```text
<raw KB> KB raw / <gzip KB> KB gzip built page; the shared Jekyll shell is included.
```

Apply the batch with `python3 scripts/review_ledger.py --date 2026-11-18 apply <batch>`. Confirm that no Markdown hash changed and that the ledger audit has
zero axis failures.

## Task 6: Run reader UX and rendered-site verification

**Files:**
- Modify only files exposed by a failing check; do not make speculative visual changes.
- Test: `assets/study-ui.test.cjs`, `scripts/test_rendered_headings.py`, `scripts/check_rendered_links.py`

**Interfaces:**
- Consumes: the rebuilt `_site` and generated search and catalog assets.
- Produces: evidence for search states, reader controls, responsive structure, links, and accessibility behavior.
- [ ] **Step 1: Run the Document Object Model (DOM) regression suite**

Run the pinned Continuous Integration (CI)-compatible `jsdom` test using a temporary dependency prefix:

```bash
UI_DEPS=$(mktemp -d)
npm install --prefix "$UI_DEPS" --no-audit --no-fund jsdom@26.1.0
NODE_PATH="$UI_DEPS/node_modules" /opt/homebrew/bin/node --test assets/study-ui.test.cjs
```

Expected: existing reader, search, and resume tests plus the external-catalog and failure-state tests pass. If the optional dependency cannot be installed, record that limitation and rely on the source and rendered checks below without claiming DOM coverage.

- [ ] **Step 2: Run rendered heading and link checks**

Run:

```bash
python3 scripts/test_rendered_headings.py _site
python3 scripts/check_rendered_links.py _site --json /private/var/folders/4l/696h29515gs3chrdfjzkqrq40000gn/T/rendered-links-final.json
```

Expected: one article `<h1>` per page, the authored JavaScript index title stays correct, and all published links, assets, and fragments resolve.

- [ ] **Step 3: Run focused generated-page assertions**

Use a read-only Python assertion over `_site/search.html` and `api/search-index.js` to verify:

```python
assert 'study-search-data' not in search_html
assert 'api/search-index.js' in search_html
assert 'window.__SDB_SEARCH_DATA__' in search_index
assert search_index.count('"p":') == 680
```

Also verify every generated Representational State Transfer (REST) page has one `<h1>` and no leaked Liquid markers. If Playwright is installed later, run `scripts/test_reading_ui_browser.cjs`; otherwise report it as unavailable rather than inferring browser behavior.

## Task 7: Run the complete gates and prepare delivery

**Files:**
- Generated or modified files from Tasks 2–5.
- Create: `docs/superpowers/plans/2026-11-18-performance-ui-implementation.md` (this plan)

**Interfaces:**
- Consumes: all phase outputs and verification reports.
- Produces: one implementation commit on a feature branch, a pushed branch, a fast-forward merge into `main`, pushed `main`, and a verified remote commit.
- [ ] **Step 1: Run repository-wide verification**

Run:

```bash
git diff --check
python3 scripts/check_links.py
bash scripts/verify.sh
```

Expected: all 34 repository gates pass, including the generated-index fixed point, senior coverage, review-ledger hashes, and no external-link drift.

- [ ] **Step 2: Inspect the final diff**

Run:

```bash
git status --short
git diff --stat
git diff --check
git diff --name-only
```

Confirm that the diff contains only the approved asset extraction, generated search transport, search failure UX, gzip measurement semantics, generated metadata, ledger fast-evidence restamp, tests, docs, and this plan, with no personal data, secrets, or unrelated chapter edits present.

- [ ] **Step 3: Create the implementation branch and commit**

Starting from the clean design commit, create the branch and commit:

```bash
git switch -c fix/final-performance-ui
git add _includes/head-custom.html assets/reader-shell.css assets/reader-shell.js \
  assets/search-ui.js assets/search-ui.css assets/study-ui.test.cjs \
  scripts/gen_master_index.py scripts/measure_page_weight.py \
  docs/corpus-review/README.md docs/scripts-map.md \
  api/search-index.js search.html api/index.json \
  docs/corpus-review/page-weight.json docs/review-ledger.json \
  docs/superpowers/plans/2026-11-18-performance-ui-implementation.md
git commit -m "perf(reader): optimize shared shell and search loading"
```

- [ ] **Step 4: Push and merge into main**

Run:

```bash
git push -u origin fix/final-performance-ui
git fetch origin
git switch main
git merge --ff-only fix/final-performance-ui
git push origin main
```

If `origin/main` advances before the merge, stop the fast-forward sequence,
bring the feature branch up to date with the fetched `origin/main`, rerun the
complete gates, and then repeat the fast-forward merge. Do not force-push or
discard unrelated remote work.

- [ ] **Step 5: Verify delivery**

Run:

```bash
git status --short
git log -2 --oneline --decorate
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

Expected: the working tree is clean and the local `HEAD` hash equals the
remote `main` hash.
