# Full Bible Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the software-developer-bible repo to a single unified numbering convention with category subfolders, complete the auth track (video parity), and author 83 missing chapters across all stacks.

**Architecture:** Spec `docs/superpowers/specs/2026-08-25-full-restructure-design.md` is the authoritative move map and chapter list. Phase 1 executes structural moves stack-by-stack with automated relink + verification. Phases 2+ author content waves via parallel subagents following contributing.md template. One commit per task.

**Tech Stack:** Markdown, bash, python3 (available at /opt/homebrew/bin/python3), git.

## Global Constraints

- Convention: category folders `NN-slug/`; files in categories `<stack>.<cat>.<seq>-slug.md` (cat = folder number sans leading zero); flat-stack files `<stack>.<seq>-slug.md`; sequences contiguous from 01; interview-questions LAST.
- Every chapter follows contributing.md template: TL;DR -> Definition -> Why -> How -> Code -> Real-world -> Mistakes -> Best practices -> Summary -> Cheat sheet -> See Also -> References. No emojis. Badges per contributing.md.
- NEVER commit/push in ~/repos/career-ops. Never touch 80-lanes-abroad-full-stack/personal/ contents (symlinks). This repo only.
- Moves are moves: preserve chapter substance when relocating; only links/headers/badges change.
- After every task: run `bash scripts/check-structure.sh` (created in Task 1) must pass before commit.
- Old file IDs never remain referenced anywhere after a task completes.

---

### Task 0: Verification tooling

**Files:**
- Create: `scripts/check_structure.py`

**Interfaces:**
- Produces: `python3 scripts/check_structure.py [--root .]` exit code 0 = pass. Checks: (1) every relative md link in every .md resolves to an existing file (skips http/mailto/anchors); (2) per directory, file numeric IDs are unique and contiguous from 01 within their prefix family; (3) no file ID appears twice anywhere in repo.

- [ ] **Step 1: Write script**

```python
#!/usr/bin/env python3
import re, sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
MD = sorted(ROOT.rglob("*.md"))
SKIP = ("/.git/", "/node_modules/", "/.archive/", "/.freebuff/", "/.sass-cache/")
MD = [p for p in MD if not any(s in str(p) for s in SKIP)]
errors = []

LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
for p in MD:
    for m in LINK.finditer(p.read_text(encoding="utf-8", errors="replace")):
        t = m.group(1)
        if t.startswith(("http", "mailto:", "#")):
            continue
        target = (p.parent / t.split("#")[0]).resolve()
        if not target.exists():
            errors.append(f"BROKEN LINK {p.relative_to(ROOT)} -> {t}")

idre = re.compile(r"^(?:\d+\.)+\d+-")
seen = {}
for p in MD:
    if idre.match(p.name):
        if p.name in seen:
            errors.append(f"DUPLICATE ID {p.name}: {seen[p.name]} & {p.relative_to(ROOT)}")
        seen[p.name] = str(p.relative_to(ROOT))

fam = {}
for p in MD:
    m2 = re.match(r"^((?:\d+\.)*\d+)\.(\d+)-", p.name)
    if not m2 or "INDEX" in p.name:
        continue
    fam.setdefault((str(p.parent), m2.group(1)), []).append(int(m2.group(2)))
for (d, pref), nums in fam.items():
    exp = list(range(1, len(nums) + 1))
    if sorted(nums) != exp:
        errors.append(f"GAPS {d} prefix {pref}: has {sorted(nums)} expected {exp}")

print("\n".join(errors) if errors else f"OK: {len(MD)} md files checked")
sys.exit(1 if errors else 0)
```

Note: contiguity check is only meaningful AFTER all moves are done - during intermediate tasks expect GAPS errors for untouched stacks (e.g. 20.5-security pre-move). For Tasks 1-8 use `--links-only` mode: add argv flag that skips the family check.

- [ ] **Step 2: Verify baseline** — Run: `python3 scripts/check_structure.py --links-only`. Expected: OK or a short list of PRE-EXISTING broken links; record them (they get fixed by relink steps).

- [ ] **Step 3: Commit** — `git add scripts/check_structure.py && git commit -m "chore(scripts): structure verification tool"`

---

### Task 1: Relink helper

**Files:**
- Create: `scripts/relink.py`

**Interfaces:**
- Produces: `python3 scripts/relink.py <old-basename> <new-path-from-repo-root>` rewrites every relative md link in the repo whose final path segment equals old-basename to point at new location, recomputing ../../ depth correctly.

- [ ] **Step 1: Write script**

```python
#!/usr/bin/env python3
import os, re, sys
from pathlib import Path

old_name, new_rel = sys.argv[1], Path(sys.argv[2])
ROOT = Path(".").resolve()
target_abs = ROOT / new_rel
LINK = re.compile(r"(\]\()([^)\s]+(\.md))(\))")
changed = 0
for p in ROOT.rglob("*.md"):
    if any(s in str(p) for s in ("/.git/", "/.archive/", "/.freebuff/")):
        continue
    txt = p.read_text(encoding="utf-8"); orig = txt
    def repl(m):
        ref = m.group(2)
        base = os.path.basename(ref.split("#")[0])
        if base != old_name: return m.group(0)
        resolved = os.path.normpath(os.path.join(os.path.dirname(p), ref.split("#")[0]))
        # rewrite even if currently stale (file already moved)
        newref = os.path.relpath(target_abs, p.parent)
        return m.group(1) + newref + m.group(4)
    txt = LINK.sub(repl, txt)
    if txt != orig:
        p.write_text(txt, encoding="utf-8"); changed += 1
print(f"rewrote links in {changed} files")
```

- [ ] **Step 2: Commit** — `git add scripts/relink.py && git commit -m "chore(scripts): bulk relink helper"`

---

### Task 2: Frontend structural moves (10.1-10.8)

**Files:** Move/rename per spec section 3 entries under `10-frontend/` (all eight stacks). Create category INDEX.md for every new folder; rebuild each affected stack INDEX.md; create NEW-chapter placeholder files? NO - placeholders forbidden; new chapters arrive in Wave A (Task 10); INDEXes built in this task reference ONLY files that exist at that moment.

**Interfaces:**
- Consumes: spec section 3 (exact old->new map per stack), Task 1 relink.py
- Produces: final FE paths like `10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.01-execution-context.md`

- [ ] **Step 1: Per stack, git mv every file into its new category folder with new name** (use `git mv` so history follows). Process stacks in order 10.1, 10.2, 10.3, 10.4, then flat compactions 10.5-10.8.
- [ ] **Step 2: After EACH stack's moves**, run relink.py for every moved basename: `python3 scripts/relink.py <old-basename-with-ext> <new/path/file.md>`
- [ ] **Step 3: Rewrite internal headers/badges** in moved files where they self-reference old IDs (grep each new folder for old basenames).
- [ ] **Step 4: Create category INDEX.md** per new folder (short: purpose, table of files with topics/read-time, prev/next nav).
- [ ] **Step 5: Rebuild each stack INDEX.md**: badges count, category table, flow diagram, study paths, cross-refs - referencing only existing files.
- [ ] **Step 6: Verify** `python3 scripts/check_structure.py --links-only` - zero new breaks vs Task 0 baseline. Also `find 10-frontend -name "*.md" | sort` eyeball against spec.
- [ ] **Step 7: Commit** - `git add -A && git commit -m "refactor(frontend): category subfolders + unified numbering per spec"`

---

### Task 3: Backend structural moves part 1 (20.1 node, 20.2 nestjs, 20.3 rest, 20.4 database)

Same procedure as Task 2, stacks 20.1-20.4 per spec section 3. Commit message: `refactor(backend): category subfolders + numbering for node/nestjs/rest/database`.

---

### Task 4: Security restructure incl. auth numbering (20.5)

**Files:** Move per spec section 3 entry `20.5-security`: auth/ -> 01-auth/ with numbered files (auth-fundamentals->20.5.1.01 etc.), attacks->02-, hardening->03-, drills->04-. NOTE: the four NEW auth chapters and oauth slim-down happen in Task 9 - this task only numbers EXISTING files (20.5.1.01, .04, .05, .06, .09, .10 present; gaps .02/.03/.07/.08 temporarily acceptable until Task 9 fills them - check_structure full-mode runs only from Task 14 onward).

- [ ] **Step 1-6:** Same as Task 2 steps but skip family-contiguity assertion; verify links-only. Update auth INDEX stage table to show planned 10 stages but link only existing files.
- [ ] **Step 7: Commit** - `refactor(security): auth numbered track + attack/hardening/drills categories`

---

### Task 5: Backend structural moves part 2 (20.6 microservices, 20.7 graphql, 20.8 caching compact, 20.12 ai-engineering)

Same as Task 2 for these four stacks per spec. Commit: `refactor(backend): categories for microservices/graphql + caching/ai compaction`.

---

### Task 6: Architecture moves (30.1 conversion, 30.2 renames, 30.3 regroup)

Per spec section 3: convert design-patterns folders/files to dotted scheme (`30.1.11-singleton.md` -> `02-creational/30.1.2.01-singleton.md`, etc.), rename system-design folders (`00-theory`->`01-theory`, `10-case-studies`->`02-case-studies` - files unchanged), regroup infra-patterns into 5 categories fixing gaps. Repair links via relink.py per basename (many INDEX cross-links inside design-patterns reference old concatenated IDs). Commit: `refactor(architecture): unified scheme for patterns/system-design/infra-patterns`.

---

### Task 7: Platform moves (40.1-40.10)

Per spec section 3: kubernetes/ci-cd/observability/build-tools gain category folders; docker/git/serverless/monorepo/cdn flat compactions (IQ last); twelve-factor unchanged; delete stray `.DS_Store` in 40.3. Commit: `refactor(platform): categories + contiguous numbering across platform stacks`.

---

### Task 8: Quality/realtime/toolkit moves (50.x, 60.x, 70.x)

Per spec section 3: testing/performance/websockets/coding-patterns gain categories; accessibility/prod-eng/behavioral/cheatsheets flat compactions. Behavioral INDEX gains note that STAR basics live in 00-strategy. Commit: `refactor(quality-toolkit): categories + contiguous numbering`.

---

### Task 9: Auth completion (video parity)

**Files:**
- Create: `20-backend/20.5-security/01-auth/20.5.1.02-http-basic-digest-auth.md`
- Create: `20-backend/20.5-security/01-auth/20.5.1.03-api-keys.md`
- Create: `20-backend/20.5-security/01-auth/20.5.1.07-sso-saml-federation.md`
- Create: `20-backend/20.5-security/01-auth/20.5.1.08-mfa-passkeys-webauthn.md`
- Modify: `.../01-auth/20.5.1.06-oauth2-oidc.md` (extract SSO/SAML/passkey sections -> replace with links to .07/.08)
- Modify: `.../01-auth/INDEX.md`, `.../20.5-security/INDEX.md`

Coverage bullets per chapter are in spec section 4 (authoritative). Author directly (not via subagent) since precision matters here; follow Global Constraints template. Rebuild auth INDEX as 10-stage flow matching video order: fundamentals -> basic/digest -> api keys -> sessions -> jwt(+access/refresh) -> oauth2/oidc -> sso/saml -> mfa/passkeys -> rbac/abac -> drills. Add video to References of INDEX.

- [ ] **Step 1: Write 4 chapters** (full template, 250+ lines each, code samples TS/NestJS-flavored like neighbors)
- [ ] **Step 2: Slim oauth2-oidc.md**, leaving See Also links to .07/.08
- [ ] **Step 3: Rebuild both INDEXes** (counts, stages, badges)
- [ ] **Step 4: Cross-link fixes**: REST authentication chapter + security interview bank reference new chapters
- [ ] **Step 5: Verify links-only check passes; commit** - `feat(security): complete auth track - basic/digest, api keys, sso/saml, mfa/passkeys`

---

### Task 10: Wave A - Frontend chapters (13)

Dispatch 2 parallel general agents (agent A1: 7 chapters, A2: 6). Each agent prompt includes: contributing.md path to read first, one neighbor chapter path per stack for tone calibration, its chapter list below with required coverage bullets, rule to ALSO append its files to the right category INDEX + stack INDEX tables and update badge counts, run links-only check before finishing.

A1: dom-events-delegation (bubbling/capturing/delegation, synthetic-event contrast), cross-tab-communication (BroadcastChannel/storage events/SharedWorker vs postMessage, logout-sync pattern), tsconfig-compiler-options (strict matrix, moduleResolution bundler/nodenext, isolatedModules, incremental), type-variance (co/contra, function bivariance, in/out), usesyncexternalstore (tearing, zustand/redux integration), react-router (v6/v7 data routers, loaders/actions, protected routes), deploying-nextjs (standalone Docker, Vercel vs self-host, edge runtime limits, multi-zone)
A2: autosave-draft-recovery (debounced saves, IndexedDB/localStorage drafts, dirty guards), canvas-svg-animation (rAF loop, stroke-dashoffset, canvas-vs-DOM perf), css-architecture-styling-approaches (BEM/CUBE, CSS Modules vs CSS-in-JS vs Tailwind decision, cascade layers), theming-design-tokens (tokens, prefers-color-scheme, FOUC avoidance), deep-linking-universal-links (schemes, deferred links, cold/warm start), testing-react-native-apps (Detox/Maestro, device farms)

- [ ] **Step 1: Dispatch agents, wait, review outputs** (template compliance, no emojis, links resolve)
- [ ] **Step 2: Run links-only check; fix any breaks; commit** - `feat(frontend): wave A - 13 new chapters`

---

### Task 11: Wave B - Backend chapters (20)

3 parallel agents.
B1 (node/nest): debugging-profiling-nodejs (--inspect/--prof, heap snapshots, CPU vs memory bound), express-fastify-internals (middleware chain, error middleware semantics, fastify hooks/encapsulation, why faster), lifecycle-hooks-graceful-shutdown (OnModuleInit/Bootstrap/Destroy, enableShutdownHooks, SIGTERM ordering), scheduling-background-jobs (@nestjs/schedule crons, BullMQ, idempotent handlers), swagger-openapi-nestjs (@nestjs/swagger DTO mapping, DocumentBuilder, codegen)
B2 (rest/db/sec-vuln/micro/graphql): long-running-api-operations (202 + status endpoint, polling vs callbacks), file-upload-apis (multipart limits, presigned S3, resumable/tus, AV gates), orm-query-builder-landscape (Drizzle/Knex/TypeORM vs Prisma decision tree), backups-pitr-recovery (WAL archiving, pgBackRest, RPO/RTO, restore drills), search-infrastructure-at-scale (when ES/OpenSearch/Meilisearch beats GIN FTS, CDC sync, relevance), vulnerability-management-patch-governance (CVE triage, patch SLAs, SBOM response), decomposing-monolith-database (service-owned schemas, shared-table hazards, transition sync), codegen-schema-safety-ci (GraphQL Codegen, typed documents, CI schema-check)
B3 (auth 4 + ai 3): http-basic-digest-auth, api-keys, sso-saml-federation, mfa-passkeys-webauthn per spec section 4 IF Task 9 not done by main worker (else skip); retrieval-quality-hybrid-search-reranking (hybrid BM25+vector, rerankers, HNSW/IVF, recall@k evals), agent-orchestration-patterns (plan-act loops, state machines/graphs, stop criteria, cost guards), serving-models-hosted-vs-self-hosted (vLLM basics, quantization, latency/cost/residency matrix)

NOTE: If Task 9 completed first, B3 = AI trio only (3 chapters).

- [ ] **Step 1-2:** Dispatch, review, verify, commit - `feat(backend): wave B - backend/AI/auth-support chapters`

---

### Task 12: Wave C - Architecture chapters (14)

2 parallel agents.
C1 (patterns 5 + infra 4): null-object, ddd-tactical-patterns-aggregates-value-objects, anti-corruption-layer, service-locator-vs-dependency-injection, presentation-patterns-mvc-mvp-mvvm, feature-flags-kill-switches (flag stores, targeting, kill-switch SLAs), backup-strategy-restore-drills (drill cadence, game days - mechanics live in 20.4.5.04, link it), cost-engineering-finops (rightsizing, tiers, spot), data-retention-archival (policies, tiering, cold storage)
C2 (case studies 5, follow existing case-study format e.g. url-shortener): typeahead-autocomplete (trie, geo-sharding, freshness), metrics-monitoring-pipeline (TSDB ingestion, downsampling, cardinality), distributed-job-scheduler (cron-at-scale, leases, visibility timeouts), distributed-id-generator (snowflake, clock skew, k-sortability), ad-click-aggregator (streaming dedup, windowed agg, exactly-once sinks)

- [ ] **Step 1-2:** Dispatch, review, verify, commit - `feat(architecture): wave C - patterns + case studies + ops chapters`

---

### Task 13: Wave D - Platform chapters (19)

3 parallel agents.
D1 (docker/k8s 6): container-runtime-internals-namespaces-cgroups, image-signing-sbom-supply-chain (cosign, SBOM, SLSA provenance), rootless-sandboxed-runtimes (gVisor/Kata), node-autoscaling-cluster-capacity (cluster-autoscaler, Karpenter), kustomize-overlays-packaging-tradeoffs, crds-operators-controller-patterns (reconcile loops)
D2 (ci-cd/obs/build 6): artifact-registries-release-promotion, pipeline-supply-chain-security-slsa (action pinning, OIDC, attestation), dora-metrics-delivery-performance, continuous-profiling (Pyroscope/Parca), ebpf-observability (Hubble/Pixie), asset-pipelines-css-images-fonts (PostCSS/Tailwind build, image/font optimization)
D3 (git/serverless/monorepo/cdn 7): git-internals-objects-refs-packfiles, git-at-scale-lfs-partial-clones, signed-commits-repository-security, durable-execution-temporal-inngest, versioning-publishing-strategies (changesets in practice), multi-cdn-traffic-steering, media-optimization-at-the-edge

- [ ] **Step 1-2:** Dispatch, review, verify, commit - `feat(platform): wave D - 19 platform chapters`

---

### Task 14: Wave E - Quality/Realtime/Toolkit chapters (17)

2 parallel agents.
E1 (quality/realtime 9): test-data-management-anonymization (GDPR-safe fixtures), accessible-charts-data-viz, accessibility-design-systems, http2-http3-performance-effects (HOL blocking, coalescing), production-readiness-reviews, on-call-without-burnout, graphql-subscriptions-live-queries, webrtc-peer-to-peer (SFU vs mesh), testing-realtime-systems (Artillery WS, churn)
E2 (toolkit 8): stakeholder-management-stories, judgment-calls-ambiguity, behavioral-anti-patterns-checklist (self-audit rubric), shortest-paths-dijkstra-bellman-ford, linked-list-manipulation-patterns, matrix-traversal-simulation, docker-kubernetes-cicd-cheat-sheet, sql-data-modeling-cheat-sheet

- [ ] **Step 1-2:** Dispatch, review, verify, commit - `feat(quality-realtime-toolkit): wave E - 17 chapters`

---

### Task 15: Root docs + full verification

- [ ] **Step 1: Update root INDEX.md / README.md / ROADMAP.md** - stack counts, structure trees, totals (83 new chapters reflected).
- [ ] **Step 2: Update AGENTS.md** design-patterns convention paragraph -> unified convention text. Update contributing.md Directory Structure + File Naming sections likewise.
- [ ] **Step 3: Full check** - `python3 scripts/check_structure.py` (NO flags): zero broken links, zero duplicate IDs, ALL families contiguous.
- [ ] **Step 4: Doctor** - `bash 80-lanes-abroad-full-stack/personal/doctor.sh` still clean.
- [ ] **Step 5: Final commit** - `docs: root indexes + conventions updated for unified structure; full verification green`

## Self-Review Notes

- Spec coverage: spec sections 2 (Tasks 15 conventions), 3 (Tasks 2-8), 4 (Task 9), 5 (Tasks 10-14), 6 (INDEX steps inside every task), 7 (Task 0/15 checks), 8 (order preserved). All covered.
- Type consistency: scripts' CLI contracts fixed in Tasks 0-1 and consumed identically later.
- Known sequencing dependency: family-contiguity full check only valid after Task 8; Tasks 2-8 use --links-only.
