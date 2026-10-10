# Dead-Link Remediation & Wayback Pass Implementation Plan

> **Historical design record:** requirements, example paths and checkboxes describe this dated plan, not current repository status or authorization to rerun it. Later [explanation-depth work](../plans/2026-10-08-explanation-depth.md), [AGENTS.md](../../../AGENTS.md) and [contributing.md](../../../contributing.md) govern current changes. Preserve stable chapter IDs; TL;DR and inline chapter cheat/revision sections are retired.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eliminate every confirmed-dead external citation in the bible docs by probe-verified replacement (live URL or exact Wayback snapshot), closing the "~200 dead links remain open" item in `docs/2026-09-10-modernization-changelog.md` §5.

**Architecture:** The freshness gate (`scripts/check_freshness.py --check-urls`) is the single source of truth for what is dead. Workflow per cluster: regenerate the authoritative dead list → re-probe each candidate with curl GET (sweep3 predates several fix batches, so its list over-counts) → find each dead URL's citing files with grep → for each, `web_search` a replacement candidate → verify the candidate returns HTTP 200 via curl GET with browser headers → `str_replace` in the citing file → gates → commit. URLs that are iconic-but-dead (High Scalability architectures, the LinkedIn log paper) get exact-timestamp Wayback citations instead of replacements.

**Tech Stack:** python3 (available at `/opt/homebrew/bin/python3`), `scripts/check_freshness.py` (7 rules + `--check-urls N` liveness mode), curl, `web_search` + `read_url` for candidate discovery/verification, `str_replace` for edits, `bash scripts/verify.sh` as the gate.

## Global Constraints

- **Never cite an unverified URL.** Every replacement must return HTTP 200 from `curl -s -o /dev/null -w "%{http_code}" -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36" "$URL"` (GET — never judge by HEAD; PortSwigger-class sites 404 on HEAD but serve GET).
- **Never guess a URL from memory.** Discover candidates via `web_search`, then verify with the curl command above. If a candidate 404s, search again — do not "fix" a 404 with another 404.
- **WARN is not DEAD.** `HTTP 403`/`429`/bot-blocks (LeetCode, LinkedIn, Cloudflare-challenged hosts) mean leave the URL alone.
- **By-design exclusions (never replace):** `github.com/CVamsi27/docita` (private repo; 404 only for unauthenticated probes), any URL under `80-lanes-abroad-full-stack/personal/` (historical job-application records), badge hosts (`img.shields.io`).
- **Wayback citations** must use the exact snapshot URL returned by `https://archive.org/wayback/available?url=<orig>` and be verified 200. Never fabricate or hand-write a snapshot timestamp. Cite format: `[Title (archived)](https://web.archive.org/web/<TIMESTAMP>/<original-url>)`.
- **Citations only.** No content restructuring, no prose rewrites beyond the link line and, if needed, one clause noting the archived status. Follow existing file conventions.
- **Never edit** `80-lanes-abroad-full-stack/personal/` contents (symlinks). Never commit/push in `~/repos/career-ops`. This repo only.
- **Gates before every commit:** `bash scripts/verify.sh` must print 5/5 PASS (structure may print baseline lane-80.x GAPS — that is intentional). If the count guard fails after edits, recompute and restamp the scale string in all four sites together (root `INDEX.md`, `80-lanes-abroad-full-stack/INDEX.md`, `contributing.md`, `AGENTS.md`) using the exact string `check_counts.py` prints — never hand-invent it.
- **Commit style** (matches repo history): `docs: <imperative summary>` — e.g. `docs: replace dead freecodecamp citations with verified live URLs`. Never push.
- If a "dead" URL turns out LIVE on re-probe, drop it from the work list silently — sweep3 contains false deads (pre-hardening HEAD-probe results, pre-paren-repair Wikipedia truncations, one transient PortSwigger outage).

---

### Task 1: Regenerate the authoritative dead-URL list

**Files:**
- Create (scratch, not committed): `/tmp/dead_final.txt`
- Read: `scripts/check_freshness.py` (no changes)

**Interfaces:**
- Consumes: `scripts/check_freshness.py --check-urls N` (exit 0 = all probed links alive or warn; exit 1 = dead links or malformed links found; output lines match `  DEAD  HTTP 404  <url>` or `  MALFORMED  <url>`).
- Produces: `/tmp/dead_final.txt` — one URL per line, sorted, deduped (the authoritative work list every later task consumes). Also `/tmp/malformed.txt` for the Task 10 artifact.

- [ ] **Step 1: Run the full liveness sweep with the hardened checker**

```bash
python3 scripts/check_freshness.py --check-urls 3000 > /tmp/sweep_final.txt 2>&1; echo "exit=$?"
```

Note: `--check-urls 3000` exceeds the external-link count (~2,300), so every link is probed (the checker probes all when `N >= len(urls)`). This takes several minutes. Expected: `exit=1` with a few dozen-to-~200 DEAD lines — far fewer than sweep3's 234 because the session already fixed ~30 citations and the checker now repairs Wikipedia-style parens and retries transient 404s.

- [ ] **Step 2: Extract the dead and malformed work lists**

```bash
grep "  DEAD  " /tmp/sweep_final.txt | sed 's/.*  \(https\?:[^ ]*\)$/\1/' | sort -u > /tmp/dead_final.txt
grep "  MALFORMED  " /tmp/sweep_final.txt | sed 's/.*MALFORMED  //' | sort -u > /tmp/malformed.txt
grep "  DEAD  \|  MALFORMED  " /tmp/sweep_final.txt | grep -v "  WARN  " | head -30
wc -l /tmp/dead_final.txt /tmp/malformed.txt
```

- [ ] **Step 3: Remove by-design exclusions from the work list**

```bash
grep -v "github.com/CVamsi27/docita" /tmp/dead_final.txt > /tmp/dead_work.txt && mv /tmp/dead_work.txt /tmp/dead_final.txt
grep -c "personal/" /tmp/dead_final.txt   # must print 0 — checker already skips /personal/
```

- [ ] **Step 4: Sanity-check the size**

Run: `wc -l /tmp/dead_final.txt`
Expected: 0 < N ≤ 210. If N > 220, stop and debug (likely a network outage mass-failing probes — re-run Step 1 before proceeding). If N = 0, skip to Task 10.

- [ ] **Step 5: No commit**

This task produces only scratch files. Nothing to commit.

---

### Task 2: freecodecamp cluster (15 candidate URLs)

**Files:**
- Modify (grep will confirm the exact set — one References-section line each):
  - `10-frontend/10.3-react/03-advanced-hooks-and-patterns/10.3.3.05-performance.md`
  - `10-frontend/10.3-react/03-advanced-hooks-and-patterns/10.3.3.01-suspense.md`
  - `10-frontend/10.3-react/03-advanced-hooks-and-patterns/10.3.3.02-error-boundary.md`
  - `10-frontend/10.3-react/02-core-hooks/10.3.2.05-context-api.md`
  - `10-frontend/10.3-react/02-core-hooks/10.3.2.01-usestate.md`
  - `10-frontend/10.3-react/02-core-hooks/10.3.2.04-useref.md`
  - `10-frontend/10.3-react/02-core-hooks/10.3.2.02-useeffect.md`
  - `10-frontend/10.3-react/01-react-internals/10.3.1.03-reconciliation.md`
  - `10-frontend/10.3-react/01-react-internals/10.3.1.01-virtual-dom.md`
  - `10-frontend/10.1-javascript/02-objects-prototypes-this/10.1.2.01-this.md`
  - `10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.03-call-stack.md`
  - `10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.06-closures.md`
  - `10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.04-hoisting.md`
  - `10-frontend/10.1-javascript/04-memory-and-data/10.1.4.01-pass-by-value.md`
  - `10-frontend/10.1-javascript/04-memory-and-data/10.1.4.07-garbage-collection.md`
  - `10-frontend/10.1-javascript/04-memory-and-data/10.1.4.04-debounce.md`
  - `10-frontend/10.1-javascript/03-async-concurrency/10.1.3.03-async-await.md`
  - `10-frontend/10.1-javascript/05-functional-patterns/10.1.5.02-memoization.md`
  - `20-backend/20.1-node.js/02-io-and-data/20.1.2.02-buffers.md`

**Interfaces:**
- Consumes: `/tmp/dead_final.txt` from Task 1.
- Produces: all surviving freecodecamp citations replaced with verified live URLs; commit `docs: replace dead freecodecamp citations with verified live URLs`.

**Candidate inventory** (from sweep3 — re-confirmed live/dead by Task 1's list; skip any not present in `/tmp/dead_final.txt`):

```
https://www.freecodecamp.org/news/optimize-react-app-performance/
https://www.freecodecamp.org/news/react-suspense-and-error-boundaries/
https://www.freecodecamp.org/news/error-handling-react/
https://www.freecodecamp.org/news/context-api-in-react/
https://www.freecodecamp.org/news/usestate-hook-in-react/
https://www.freecodecamp.org/news/useref-hook-in-react/
https://www.freecodecamp.org/news/useeffect-hook-in-react/
https://www.freecodecamp.org/news/react-reconciliation-algorithm/
https://www.freecodecamp.org/news/what-is-the-virtual-dom-in-react/
https://www.freecodecamp.org/news/what-is-this-in-javascript/
https://www.freecodecamp.org/news/understanding-the-javascript-call-stack/
https://www.freecodecamp.org/news/lets-learn-javascript-closures/
https://www.freecodecamp.org/news/understanding-hoisting-in-javascript/
https://www.freecodecamp.org/news/javascript-pass-by-value-and-pass-by-reference/
https://www.freecodecamp.org/news/javascript-garbage-collection/
https://www.freecodecamp.org/news/debouncing-and-throttling-in-javascript/
https://www.freecodecamp.org/news/async-await-in-javascript/
https://www.freecodecamp.org/news/javascript-memoization/
https://www.freecodecamp.org/news/node-js-streams/
```

- [ ] **Step 1: Re-probe the whole cluster in one loop**

```bash
grep "freecodecamp" /tmp/dead_final.txt | while read -r u; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36" "$u")
  echo "$code $u"
done
```

Expected: mostly `404` (freecodecamp renamed its news slugs site-wide) — plus possibly a few `200` (false deads; drop those). Work only the `404` list.

- [ ] **Step 2: Find replacements (worked example — repeat the pattern for every 404)**

For each dead URL, search by the page title, not the slug. Worked example for the call-stack link:

1. `web_search` for `freecodecamp news javascript call stack`
2. Take the top freecodecamp.org result whose title matches the citation's subject.
3. Verify before writing:

```bash
curl -s -o /dev/null -w "%{http_code}" -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36" "<candidate-url>"
```

Expected: `200`. If `404`, search again with different phrasing.

4. Keep the citation's existing link text unless the article title differs materially (then update the text to the real title).

- [ ] **Step 3: Apply the edits**

One `str_replace` per citing file. Worked example (call-stack chapter, line ~802):

- oldString: `- [FreeCodeCamp: Understanding the JavaScript Call Stack](https://www.freecodecamp.org/news/understanding-the-javascript-call-stack/)`
- newString: `- [FreeCodeCamp: Understanding the JavaScript Call Stack](<verified-url>)`

If grep finds a URL cited in more than one file, fix every occurrence (same oldString, one `str_replace` per file).

- [ ] **Step 4: Verify zero freecodecamp URLs remain dead**

```bash
grep -rn "freecodecamp.org/news/" --include="*.md" . | grep -v ".archive" | grep -v node_modules | sed 's/.*(\(https[^)]*\)).*/\1/' | sort -u | while read -r u; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36" "$u")
  [ "$code" != "200" ] && echo "STILL BAD $code $u"
done; echo "freecodecamp scan done"
```

Expected: only `freecodecamp scan done` (no STILL BAD lines).

- [ ] **Step 5: Run gates**

Run: `bash scripts/verify.sh`
Expected: 5/5 PASS (structure baseline GAPS allowed).

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "docs: replace dead freecodecamp citations with verified live URLs"
```

---

### Task 3: Developer-education blog cluster

**Files:**
- Modify (exact set confirmed by `grep -rln` per URL):
  - `blog.logrocket.com` ×3 — cited in: error-boundary (`10.3.3.02`), bundler chapters (`40-frontend-tooling`), module chapters (`10.1.2.x` / `40.2.x`)
  - `dev.to` ×3 — scope chapter (`10.1.1.x`), TS `infer` chapter (`10.2.x`), branded-types chapter (`10.2.x`)
  - `dmitripavlutin.com` ×2 — usestate/useref chapters (`10.3.2.01`, `10.3.2.04`)
  - `www.robinwieruch.de`, `www.joshwcomeau.com`, `www.akshaykhot.com`, `www.udacity.com`, `www.simplilearn.com`, `www.geeksforgeeks.org` ×3, `www.interviewbit.com`, `www.ambysoft.com`, `www.sadalage.com`, `www.vertabelo.com` — one citation each; locate with Step 1's grep

**Interfaces:**
- Consumes: `/tmp/dead_final.txt` from Task 1.
- Produces: verified replacements for all blog-cluster URLs; commit `docs: replace dead dev-blog citations with verified live URLs`.

- [ ] **Step 1: Enumerate citing files for every cluster URL**

```bash
for u in $(grep -E "logrocket|dev\.to|dmitripavlutin|robinwieruch|joshwcomeau|akshaykhot|udacity|simplilearn|geeksforgeeks|interviewbit|ambysoft|sadalage|vertabelo" /tmp/dead_final.txt); do
  echo "== $u"; grep -rln --include="*.md" "$u" . | grep -v ".archive" | grep -v node_modules
done
```

Expected: one to two files per URL. A URL with zero citing files was already fixed — drop it.

- [ ] **Step 2: Re-probe each URL, keep only confirmed 404s**

```bash
for u in $(grep -E "logrocket|dev\.to|dmitripavlutin|robinwieruch|joshwcomeau|akshaykhot|udacity|simplilearn|geeksforgeeks|interviewbit|ambysoft|sadalage|vertabelo" /tmp/dead_final.txt); do
  code=$(curl -s -o /dev/null -w "%{http_code}" -A "Mozilla/5.0" "$u"); echo "$code $u"
done
```

(Note: the short `-A "Mozilla/5.0"` is fine here — these are personal blogs, not bot-walled. For any host that 403s, switch to the full Chrome header string from Global Constraints and re-test; if it still 403s, treat as WARN and skip.)

- [ ] **Step 3: Search, verify, and apply one replacement per URL**

Same loop as Task 2 Steps 2–3: search by page title (`web_search` with the article subject + site name), curl-verify 200, then `str_replace` the exact citation line. Example (dev.to scope article in the scope chapter):

- oldString: `- [Understanding JavaScript Scope](https://dev.to/boywithnohorns/understanding-javascript-scope-1h83)`
- newString: `- [<Real Title>](<verified-url>)`

If no good replacement exists (article subject niche), prefer the most authoritative stable alternative covering the same subject (e.g., for TS branded types: the totaltypescript.com or TS handbook page; for logrocket error-handling-react: react.dev's error-boundary docs) — always curl-verified first.

- [ ] **Step 4: Run gates and commit**

```bash
bash scripts/verify.sh
git add -A && git commit -m "docs: replace dead dev-blog citations with verified live URLs"
```

Expected: 5/5 PASS, commit succeeds.

---

### Task 4: Framework/vendor docs cluster (largest — AWS, Google, Next/Vercel, Node, MDN, web.dev, GraphQL, DBs)

**Files:**
- Modify (grep-confirmed per URL; expected files include):
  - `30-architecture/30.3-infra-patterns/04-data-at-scale/30.3.4.03-cdn-architecture.md`
  - `20-backend/20.6-microservices/**` (saga, strangler-fig leftovers)
  - `20-backend/20.4-database/**` (cassandra ×2, redis ×2, RDS-proxy)
  - `10-frontend/10.4-next.js/**` (nextjs.org ×3, vercel ×3)
  - `20-backend/20.1-node.js/**` (nodejs.org ×4)
  - MDN ×5 + web.dev ×4 + developer.chrome — a11y, performance, tooling chapters across `10-frontend/`, `50-quality/`
  - Apollo ×4, the-guild, relay, remix, reactrouter, reactnavigation, reactnative, react.dev — GraphQL/React chapters

**Interfaces:**
- Consumes: `/tmp/dead_final.txt` from Task 1.
- Produces: verified vendor-docs replacements; commit `docs: replace dead vendor-doc citations with verified live URLs`.

**Candidate inventory by sub-domain (re-confirm against Task 1 list):**

```
docs.aws.amazon.com/whitepapers/latest/aws-disaster-recovery/aws-disaster-recovery-workloads.html
docs.aws.amazon.com/prescriptive-guidance/latest/{strangler-fig-pattern,right-to-be-forgotten,multi-tenant-saas,multi-tenant-saas/postgresql-rls,microservices-choreography/saga-pattern}
aws.amazon.com/blogs/database/fundamentals-of-optimizing-amazon-rds-proxy/
aws.amazon.com/nosql/sql-vs-nosql/
cloud.google.com/architecture/idempotency-patterns
cloud.google.com/architecture/identity/checklist-reviews-enterprise-authentication
learn.microsoft.com/en-us/azure/architecture/patterns/transactional-outbox
learn.microsoft.com/en-us/archive/blogs/johngossman/introduction-to-modelviewviewmodel-pattern-for-wpf
nextjs.org/docs/app/building-your-application/data-fetching/fetching-caching-on-demand
nextjs.org/docs/app/building-your-application/configuring/multi-zones
nextjs.org/blog/partial-prerendering-with-next-components
vercel.com/docs/deployments/{static-deployments,isr}
vercel.com/blog/next-js-app-router-data-fetching
nodejs.org/api/stream_web.html
nodejs.org/en/learn/{diagnostics,manipulating-files/working-with-file-streams-in-nodejs,asynchronous-work/streams}
developer.mozilla.org/.../{Glossary/Execution_context,Glossary/Currying,Web/Accessibility/ARIA/Reference/forms,Web/API/ReactDOM/createPortal,Learn/Tools_and_testing/Client_side_tooling/TypeScript}
web.dev/articles/{synthetic-vs-real-user-monitoring,patterns/optimize-images,edge-computing,contrast-and-color-accessibility}
developer.chrome.com/docs/devtools/rendering-performance/js-execution
redis.io/docs/operate/oss_and_stack/management/best-practices/
redis.com/redis-best-practices/rate-limiting/
cassandra.apache.org/doc/latest/cassandra/{data_modeling/,operating/counters.html}
debezium.io/documentation/reference/stable/transformations/tombstones.html
docs.bullmq.io/guide/patterns
www.apollographql.com/docs/apollo-server/security/
www.apollographql.com/blog/graphql/{security/5-ways-to-secure-your-graphql-api,caching/fixing-the-n-1-problem-in-graphql,basics/the-top-5-ways-to-use-mutations}
the-guild.dev/graphql/graphql-ws
relay.dev/docs/tutorial/mutations/
remix.run/docs/en/main/guides/forms
reactrouter.com/how-to/custom-router
reactnavigation.org/docs/linking/
reactnative.dev/docs/jest
react.dev/learn/profiling-react-performance
```

- [ ] **Step 1: Map every candidate to its citing file(s)**

```bash
for u in $(grep -E "aws\.amazon|cloud\.google|learn\.microsoft|nextjs\.org|vercel\.com|nodejs\.org|developer\.mozilla|web\.dev|developer\.chrome|redis|cassandra|debezium|bullmq|apollographql|the-guild|relay\.dev|remix\.run|reactrouter|reactnavigation|reactnative\.dev|react\.dev" /tmp/dead_final.txt); do
  echo "== $u"; grep -rln --include="*.md" "$u" . | grep -v ".archive" | grep -v node_modules
done
```

- [ ] **Step 2: Re-probe; drop false deads**

Same curl loop pattern as Task 3 Step 2 (full Chrome header for AWS/Mozilla/web.dev — those bot-wall aggressively). Keep only `404`.

- [ ] **Step 3: Replace from canonical doc roots, verifying each**

Vendor-doc replacements should go to the vendor's current canonical page for the same subject — search `web_search` with the subject + vendor name (e.g. `aws prescriptive guidance strangler fig pattern site:aws.amazon.com`, `MDN ARIA forms`, `web.dev optimize images`), then curl-verify. Known-good canonical patterns from this session (verify again before reuse — vendors keep reorganizing):

- AWS prescriptive-guidance pages now live under `docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/...` (e.g. `transactional-outbox.html` — verified live earlier).
- Stripe's `api/idempotency_keys` → `docs.stripe.com/api/idempotent_requests` (verified live earlier).
- Node webstreams → `nodejs.org/api/webstreams.html` (verified live earlier).
- Next.js on-demand fetching → `nextjs.org/docs/app/guides/data-caching` (verify).

- [ ] **Step 4: Run gates and commit**

```bash
bash scripts/verify.sh
git add -A && git commit -m "docs: replace dead vendor-doc citations with verified live URLs"
```

---

### Task 5: Security cluster (OWASP, NIST, PortSwigger, Auth0)

**Files:**
- Modify (grep-confirmed): auth/JWT/RBAC/CSRF/SSRF/file-upload/de-identification chapters under `20-backend/20.7-security/**`, `50-quality/**`, and the RBAC history citation in the auth chapters.

**Interfaces:**
- Consumes: `/tmp/dead_final.txt` from Task 1.
- Produces: verified security-doc replacements; commit `docs: replace dead security-doc citations with verified live URLs`.

**Candidate inventory:**

```
cheatsheetseries.owasp.org/cheatsheets/Configuration_Cheat_Sheet.html        # NEVER EXISTED (Google-index-verified) — cite OWASP's real Cheat_Series index instead
cheatsheetseries.owasp.org/cheatsheets/Data_De-identification_and_Anomymization_Cheat_Sheet.html  # typo'd name ("Anomymization") — find real sheet
cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet_for_Java.html
cheatsheetseries.owasp.org/cheatsheets/Unrestricted_File_Upload_Cheat_Sheet.html
owasp.org/www-community/attacks/{csrf,Session_hijacking_attack,Server_Side_Request_Forgery,SQL_Injection}
csrc.nist.gov/pubs/legacy/ir/1992/sandhu-ferraiolo-kuhn-rbac.pdf
nvlpubs.nist.gov/nistpubs/ir/2015/NIST.IR.8053.pdf
portswigger.net/web-security/api-security
auth0.com/blog/{four-types-of-memory-leaks-and-how-to-avoid-them,json-web-tokens-and-security,saml-vs-oauth-which-one-should-you-use}
auth0.com/docs/secure/tokens/json-web-tokens/json-web-token-best-practices
workos.com/blog/idp-initiated-sso-what-it-is-and-when-to-use-it
www.pingidentity.com/en/company/blog/posts/posts/2023/role-based-access-control-vs-attribute-based-access-control.html
```

- [ ] **Step 1: Re-probe the cluster**

```bash
for u in $(grep -E "owasp|nist|portswigger|auth0|workos|pingidentity" /tmp/dead_final.txt); do
  code=$(curl -s -o /dev/null -w "%{http_code}" -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36" "$u"); echo "$code $u"
done
```

Expected: OWASP cheat-sheet series 404s (filenames changed); the four `owasp.org/www-community/attacks/...` may 404 or 200 (they moved into the new OWASP site structure); NIST PDFs need the new `csrc.nist.gov/pubs/ir/YYYY/NN-...` path scheme. PortSwigger was transient-404 once before — trust the fresh probe.

- [ ] **Step 2: Search and verify replacements**

- OWASP sheets: `web_search` `OWASP cheat sheet <subject>` — cite the current `cheatsheetseries.owasp.org/cheatsheets/<Real_Name>.html` (e.g. the JWT sheet's current name, the real de-identification sheet name). Verify each with curl.
- `owasp.org/www-community/attacks/...` → the same attacks now live under `owasp.org/www-community/attacks/` reorganized paths or the cheat sheets; verify whatever the search returns.
- NIST RBAC paper (Sandhu–Ferraiolo–Kuhn): search `NIST IR 1992 Sandhu Ferraiolo Kuhn RBAC` → current `csrc.nist.gov` pubs path; NIST IR 8053 likewise.
- Auth0 blog posts → auth0's current blog/docs equivalents (auth0 reorganized docs into `auth0.com/docs` new IA); if the exact post is gone, cite auth0's current JWT article.

- [ ] **Step 3: Apply, gate, commit**

```bash
# str_replace per citing file, then:
bash scripts/verify.sh
git add -A && git commit -m "docs: replace dead security-doc citations with verified live URLs"
```

---

### Task 6: Engineering-blog cluster + Wayback pass (High Scalability, LinkedIn log paper, etc.)

**Files:**
- Modify (grep-confirmed): distributed-systems and scalability chapters under `30-architecture/30.2-system-design/**`, `30-architecture/30.3-infra-patterns/**`, `20-backend/20.5-queues/**` (feature-toggles, cache-invalidation, pagination, consistency chapters), plus `docs.bullmq.io`-adjacent queue chapters as grep directs.

**Interfaces:**
- Consumes: `/tmp/dead_final.txt` from Task 1; the Wayback availability API.
- Produces: either live replacements or **exact-timestamp Wayback citations** for each; commit `docs: replace dead engineering-blog citations with live URLs or verified Wayback snapshots`.

**Wayback-worthy (iconic primaries — cite the snapshot, not a stand-in):**

```
http://highscalability.com/blog/2011/3/14/tech-talk-dropbox-architecture.html
http://highscalability.com/blog/2012/2/6/youtube-architecture-1-billion-viewsday.html
http://highscalability.com/blog/2012/4/9/the-instagram-architecture-facebook-bought-for-1-billion.html
http://highscalability.com/blog/2013/7/8/the-architecture-twitter-uses-to-process-over-100000-tweets-p.html
https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying
```

**Remaining inventory (replace with live equivalents where one exists):**

```
blog.cloudflare.com/announcing-webtransport
brandur.org/articles/mysql-pagination
blog.thepete.net/blog/2020/07/01/feature-toggles-are-one-of-the-worst-kinds-of-technical-debt/
danielcwilson.com/blog/2018/02/spring-physics-with-javascript/
timber.io/blog/promql-for-humans/                      # already replaced with prometheus.io docs once — re-check current state
stripe.com/blog/{online-payments,api-design-best-practices}
www.fastly.com/blog/5-tips-for-supercharging-your-caching-strategy
www.cockroachlabs.com/blog/the-cost-of-cache-invalidation/
www.everythingsysadmin.com/2017/11/consistency-models.html
timkadlec.com/remembers/2018-08-09-implementing-a-performance-budget/
www.brendangregg.com/latency.html
www.joyent.com/node-js/production/design/errors        # already replaced with nodejs.org/api/errors — confirm in Task 1 list
philcalcado.com/2015/09/18/the-back-end-for-front-end-pattern.html
jimmybogard.com/who-needs-the-repository-pattern/
staffeng.com/books/staff-engineer
youtube-eng.googleblog.com/
research.google/pubs/large-scale-monorepo-development-...
engineering.fb.com/2023/08/03/core-infra/messenger/
martinfowler.com/articles/2023/transactional-outbox.html
martinfowler.com/articles/patterns-of-distributed-systems/reliable-real-time-communication.html
martinfowler.com/eaaCatalog/{workflow,softDelete,nullObject}.html
```

- [ ] **Step 1: Fetch exact Wayback snapshots for the five iconic posts**

```bash
for u in \
  "http://highscalability.com/blog/2011/3/14/tech-talk-dropbox-architecture.html" \
  "http://highscalability.com/blog/2012/2/6/youtube-architecture-1-billion-viewsday.html" \
  "http://highscalability.com/blog/2012/4/9/the-instagram-architecture-facebook-bought-for-1-billion.html" \
  "http://highscalability.com/blog/2013/7/8/the-architecture-twitter-uses-to-process-over-100000-tweets-p.html" \
  "https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying"
do
  curl -s --max-time 20 "https://archive.org/wayback/available?url=$u"
  echo
  sleep 3
done
```

Expected per URL: JSON `{"url": "...", "closest": {"url": "https://web.archive.org/web/<TS>/<orig>", "status": "200", ...}}`. If rate-limited (`{"available": false}` or empty), wait 60s and retry once; do not proceed with unverified timestamps.

- [ ] **Step 2: Verify each snapshot URL serves 200**

```bash
curl -s -o /dev/null -w "%{http_code}" -A "Mozilla/5.0" "https://web.archive.org/web/<TS>/<orig>"
```

Expected: `200` for each of the five.

- [ ] **Step 3: Apply Wayback citations**

For each of the five, `str_replace` in the citing file (grep the URL first). Format — keep original link text, add "(archived)":

- oldString: `- [Dropbox Architecture](http://highscalability.com/blog/2011/3/14/tech-talk-dropbox-architecture.html)`
- newString: `- [Dropbox Architecture (archived)](https://web.archive.org/web/<TS>/http://highscalability.com/blog/2011/3/14/tech-talk-dropbox-architecture.html)`

- [ ] **Step 4: Replace the remaining live-replaceable URLs**

Same search→verify→str_replace loop as Tasks 2–5 for the remaining inventory. Martin Fowler specifics (verify first — his site shuffles article paths): the transactional-outbox 2023 article was already retired once; if dead again, cite `martinfowler.com/articles/transactional-outbox.html` or the AWS cloud-design-patterns page already used in Task 4. `eaaCatalog` entries: if the catalog root (verified live earlier: `martinfowler.com/eaaCatalog/index.html`) still 200s but per-pattern pages 404, cite the catalog root.

- [ ] **Step 5: Run gates and commit**

```bash
bash scripts/verify.sh
git add -A && git commit -m "docs: replace dead engineering-blog citations with live URLs or verified Wayback snapshots"
```

---

### Task 7: CS-paper / algorithm cluster

**Files:**
- Modify (grep-confirmed): hash-tables, bloom-filter, probabilistic-structures, sorting/queue internals under `10-frontend/10.1-javascript/04-memory-and-data/**`, `30-architecture/30.2-system-design/01-theory/**`, DSA-adjacent chapters.

**Interfaces:**
- Consumes: `/tmp/dead_final.txt` from Task 1.
- Produces: verified paper/article citations; commit `docs: replace dead CS-paper citations with verified live URLs`.

**Candidate inventory:**

```
vigna.di.unimi.it/ftp/papers/BroadKernel.pdf
www.cs.princeton.edu/courses/archive/spring14/cos226/lectures/bloom.pdf
people.eecs.berkeley.edu/~brewer/cs262b-2004/PODC-keynote.pdf
cp-algorithms.com/data_structures/{stack,queue}.html
lemire.me/blog/2017/07/07/bloom-filters/
probablydance.com/2019/12/05/trie-hash-maps-are-really-really-fast/
usaco.guide/plat/strings-hash
www.akshaykhot.com/tags/probabilistic-data-structures/   # if not already handled in Task 3
```

- [ ] **Step 1: Re-probe and split into "moved" vs "gone"**

```bash
for u in $(grep -E "vigna|princeton|berkeley|cp-algorithms|lemire|probablydance|usaco" /tmp/dead_final.txt); do
  code=$(curl -s -o /dev/null -w "%{http_code}" -A "Mozilla/5.0" "$u"); echo "$code $u"
done
```

Note: `probablydance.com` was fixed to a verified-live URL earlier this session — if it appears here, the sweep3 entry is stale; drop it.

- [ ] **Step 2: Search and verify replacements**

- University course PDFs: search the paper title (`web_search` `Brewer PODC keynote PDF`, `Princeton cos226 bloom filter lecture PDF`) → verify the new host serves 200. If a professor moved slides, their faculty page or a stable mirror (e.g. `www.cs.cornell.edu`, course-archive sites) is acceptable.
- `cp-algorithms.com` restructured its data-structure paths — search `cp-algorithms stack queue` and verify the new slugs.
- `vigna.di.unimi.it` BroadKernel paper: search `Vigna Broad Kernel paper PDF`; if gone, cite his publications index.

- [ ] **Step 3: Apply, gate, commit**

```bash
bash scripts/verify.sh
git add -A && git commit -m "docs: replace dead CS-paper citations with verified live URLs"
```

---

### Task 8: Tooling/K8s/misc-docs cluster

**Files:**
- Modify (grep-confirmed): platform/observability/monorepo/mobile chapters under `40-platform/**`, `30-architecture/**`, `10-frontend/10.8-mobile/**`, `20-backend/**` as grep directs.

**Interfaces:**
- Consumes: `/tmp/dead_final.txt` from Task 1.
- Produces: verified tooling-doc citations; commit `docs: replace dead tooling citations with verified live URLs`.

**Candidate inventory:**

```
blog.kubernetes.io/blog/2017/12/08/introducing-kustomize-template-free-configuration-customization-for-kubernetes/
kubernetes.io/docs/concepts/workloads/pods/podpreset/          # PodPreset was REMOVED from K8s — replace with a removal-note or kustomize docs
kubectl.docs.kubernetes.io/guides/kustomize/
kyverno.io/docs/writing-policies/verify-images/
istio.io/latest/docs/tasks/traffic-management/health-checks/
linkerd.io/2.15/concepts/service-mesh-performance/
docs.cilium.io/en/latest/security/network/observability/
docs.datadoghq.com/tracing/otel_collector/
grafana.com/docs/tempo/latest/trace-integrations/profiles-in-traces/
opentelemetry.io/community/sigs/profiles/
zipkin.io/pages/references.html
docs.sigstore.dev/cosign/overview/
docs.temporal.io/encyclopedia/high-level-production-architecture
temporal.io/blog/temporal-vs-cadence
fly.io/docs/about/machines/
devcenter.heroku.com/{categories/how-heroku-works,articles/multi-tenant-applications}
www.jenkins.io/doc/book/pipeline/best-practices/
nx.dev/{extending-nx/recipes/local-generators,ci/affected}
lerna.js.org/docs/concepts/how-lerna-works
www.rspack.dev/guide/{start/benchmark,migrate-from-webpack,features/module-federation}
amzn.github.io/style-dictionary/
ballerina.io/learn/by-example/backends-for-frontends/
www.artillery.io/docs/guides/test-types/websocket-testing
blog.dreamfactory.com/websockets-vs-server-sent-events/
developers.cloudflare.com/workers/{frameworks/framework-guides/vite,examples/handle-webhooks}
seemann.github.io/plato/
yeun.github.io/otplib/
www.highcharts.com/demo/sonification
en.bem.info/methodology/
www.deque.com/aria/
www.a11yproject.com/posts/accessible-forms/
www.radix-ui.com/primitives/docs/guides/accessibility
use-the-index-luke.com/window-functions
staffeng.com/books/staff-engineer                               # if not handled in Task 6
```

- [ ] **Step 1: Map, re-probe, drop false deads**

Same grep + curl loop pattern as Task 4 Steps 1–2 (full Chrome header for kubernetes.io/istio.io/datadoghq — they bot-wall).

- [ ] **Step 2: Replace with current canonical docs, verifying each**

Vendor-specific notes: K8s blog post URLs moved to `kubernetes.io/blog/<new-slug>/` (search `Kubernetes blog introducing kustomize`); PodPreset is an **alpha feature removed in v1.26+** — replace the citation with the Kustomize docs or an archive note, and if the surrounding prose teaches PodPreset, add one sentence "(removed in Kubernetes 1.26; see Kustomize for the modern equivalent)". Istio dropped `latest` versioned paths → current version path via search. Rspack moved to `rspack.dev` new IA. Heroku devcenter reorganized → `devcenter.heroku.com` search for the same subjects.

- [ ] **Step 3: Apply, gate, commit**

```bash
bash scripts/verify.sh
git add -A && git commit -m "docs: replace dead tooling citations with verified live URLs"
```

---

### Task 9: Long-tail cluster (marketplace, GitHub repos, misc)

**Files:**
- Modify (grep-confirmed): wherever grep locates these — book/ASIN links in reading lists, GitHub repo links in tool chapters, misc singles.

**Interfaces:**
- Consumes: `/tmp/dead_final.txt` from Task 1.
- Produces: zero unclassified URLs left in `/tmp/dead_final.txt`; commit `docs: replace dead long-tail citations with verified live URLs`.

**Candidate inventory:**

```
www.amazon.com/UML-Distilled-Brief-Standard-Modeling/dp/0321193681
www.amazon.com/System-Design-Interview-insiders-Second/dpB08CMF2PY      # MALFORMED ASIN (missing /dp/) — search the book, cite its real /dp/ page or publisher page
www.oreilly.com/library/view/programming-kubernetes/9781492047096/
www.overleaf.com/latex/templates/jakes-resume/syzfjbzcjxzx              # likely irrelevant single — if cited oddly, propose removal to user in task report
www.herthabsc.com/jugend                                                 # likely irrelevant — same treatment
www.linkedin.com/salary/                                                 # bot-walled; WARN → leave alone unless 404 with browser headers
www.aboutamazon.com/news/company-news/2015-letter-to-shareholders
github.com/substack/stream-handbook
github.com/rafaykhattak/CountMinSketch
github.com/privatenumber/tsx-bundler-comparison
github.com/oxeye-nl/sre-checklist
github.com/nicktraz/node-error-handling
github.com/git-lfs/git-lfs/blob/main/docs/man/git-lfs.1.ronn
github.com/getify/You-Dont-Know-JS/blob/2nd-ed/async-performance/README.md
github.com/davidyaha/graphql-rate-limit
github.com/changesets/changesets/blob/main/docs/intro-to-changesets.md
github.com/Shopify/graphql-tools-web/tree/main/packages/graphql-depth-limit
github.com/GoogleChrome/lighthouse-ci/blob/main/docs/budgets.md
github.com/DefinitelyTyped/DefinitelyTyped/blob/master/Contributors.md
eloquentjavascript.net/3rd_edition/chapter5.html                          # chapter renumbered — verify current edition structure
docs.libuv.org/en/latest/guide/design.html
www.enterprisedb.com/blog/postgresql-vacuuming-part-1-vacuum-essentials
www.cybertec-postgresql.com/en/{postgresql-multiversion-concurrency-control,postgresql-indexing-choosing-the-right-index,postgresql-execution-plans}/
wiki.postgresql.org/wiki/{VACUUM,Deadlock,Row-Level_Security}            # NEVER EXISTED — already replaced with postgresql.org/docs/current/* once; confirm gone from citing files
www.postgresql.org/docs/current/logical-replication-slots.html           # already replaced with logical-replication — confirm
v8.dev/{features/temporal,blog/hash-map}                                  # NEVER EXISTED / moved — cite v8.dev current paths
```

- [ ] **Step 1: Map, re-probe, drop false deads and already-fixed items**

Same grep + curl pattern as Task 4. The last four groups have session fix-history — expect them absent from `/tmp/dead_final.txt`; if present, the fix didn't cover every citing file (grep finds stragglers).

- [ ] **Step 2: Fix GitHub blob links by rebasing onto the repo default branch**

For each `github.com/<org>/<repo>/blob/...` 404: fetch `https://github.com/<org>/<repo>` (200 expected), find the file's current path via `web_search` or the repo's tree, verify the new blob URL 200s, then cite it. For deleted repos (`rafaykhattak/CountMinSketch`, `oxeye-nl/sre-checklist`, `davidyaha/graphql-rate-limit`, `nicktraz/node-error-handling`, `Shopify/graphql-tools-web`): search for the canonical successor (e.g. `graphql-depth-limit` moved to `graphql-compose/graphql-depth-limit`? — verify whatever search returns) or a maintained fork; if none, keep the citation only if a Wayback snapshot exists (same procedure as Task 6 Steps 1–3), else remove the citation line and note the removal in the task report.

- [ ] **Step 3: Fix book/ASIN links**

Search each book by title + author; cite the publisher's page or a verified live store page (Amazon URLs verified by curl — Amazon bot-walls aggressively; if curl gets 503 but the search result is a plain `amazon.com/dp/<ASIN>` listing, prefer the publisher page instead).

- [ ] **Step 4: Apply, gate, commit**

```bash
bash scripts/verify.sh
git add -A && git commit -m "docs: replace dead long-tail citations with verified live URLs"
```

---

### Task 10: Malformed-link artifact + final verification + changelog update

**Files:**
- Modify: citing file for the `http-transaction` artifact (locate in Step 1)
- Modify: `docs/2026-09-10-modernization-changelog.md` (§5 open-items update)
- Possibly restamp: `INDEX.md`, `80-lanes-abroad-full-stack/INDEX.md`, `contributing.md`, `AGENTS.md` (only if count guard demands)

**Interfaces:**
- Consumes: `/tmp/malformed.txt` (Task 1), `/tmp/dead_final.txt` (must be empty of actionable items after Tasks 2–9), `bash scripts/verify.sh`.
- Produces: the close-out commit; changelog §5 marked resolved; final sweep green.

- [ ] **Step 1: Locate and fix the malformed link**

```bash
cat /tmp/malformed.txt
grep -rn --include="*.md" "http-transaction" . | grep -v ".archive" | grep -v node_modules
```

Expected: the artifact is a truncated or mis-written link (sweep3 shows a bare `http-transaction` string). Read the citing line, fix the URL to its intended target (verify with curl), or convert it to inline code if it was never a real link.

- [ ] **Step 2: Full final sweep**

```bash
python3 scripts/check_freshness.py --check-urls 3000 > /tmp/sweep_close.txt 2>&1; echo "exit=$?"
grep -c "  DEAD  " /tmp/sweep_close.txt; grep "  DEAD  \|  MALFORMED  " /tmp/sweep_close.txt | grep -v "CVamsi27/docita"
```

Expected: `exit=0`, or a DEAD/MALFORMED list consisting **only** of by-design exclusions (docita). Any other residual goes back through the Task 2–9 loop.

- [ ] **Step 3: Update the changelog's open-items section**

In `docs/2026-09-10-modernization-changelog.md` §5, replace the two dead-link bullets with a closed-status note. Exact edit:

- oldString: `- **~200 dead links in the blog/tutorial long tail** (freecodecamp ×15,\n  patterns.dev, auth0, basarat gitbook, dev.to, logrocket). Each needs a\n  search-verified replacement; URL guessing is explicitly off-limits.`
- newString: `- ~~Dead links in the blog/tutorial long tail~~ — resolved by the plan in\n  \`docs/superpowers/plans/2026-09-10-dead-link-remediation.md\` (cluster-by-cluster\n  verified replacements; see git log).`

Also update the Wayback bullet:

- oldString: `- **Wayback snapshot pass** for the iconic dead posts (High Scalability's\n  Dropbox/Twitter architecture write-ups, the LinkedIn log paper) — the\n  archive.org availability API was rate-limited after the full sweep; one\n  clean run is owed, and unverified snapshot timestamps will not be written.`
- newString: `- ~~Wayback snapshot pass~~ — done: the five iconic posts now cite exact-timestamp\n  snapshots verified live at citation time.`

(If the section's exact wording has drifted by execution time, read the file and adapt the oldStrings — the intent is: mark both items resolved and reference this plan.)

- [ ] **Step 4: Run the full gate suite**

Run: `bash scripts/verify.sh`
Expected: 5/5 PASS. If the count guard fails (line-count changes moved the totals), restamp all four scale sites with the exact string `check_counts.py` prints:

```bash
python3 scripts/check_counts.py   # prints: recommended scale string: "NNN files, NNK lines"
# then str_replace the old string with the new one in all four sites, exactly
```

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "docs: close dead-link remediation, cite verified Wayback snapshots, update changelog"
```

---

## Self-Review (completed at plan time)

1. **Spec coverage:** Changelog §5 has four open items — long-tail dead links (Tasks 2–9), Wayback pass (Task 6), docita link (Global Constraints: by-design exclusion, documented in changelog §5 already — nothing to do), commit itself (all task commits; note the user asked for these commits by approving plan execution). Coverage complete.
2. **Placeholder scan:** No TBDs; every step has exact commands; every cluster has its literal URL inventory; the replacement workflow is given as a fully worked example plus the mechanical loop. Replacement target URLs are necessarily discovered at execution time by search+verify — that constraint is itself stated (never guess), so it is not a placeholder but the core discipline.
3. **Type consistency:** Scratch-file names (`/tmp/dead_final.txt`, `/tmp/malformed.txt`, `/tmp/sweep_final.txt`, `/tmp/sweep_close.txt`) consistent across tasks; checker exit semantics stated once in Task 1 Interfaces and consumed everywhere; commit messages follow the repo's `docs:` style throughout.
