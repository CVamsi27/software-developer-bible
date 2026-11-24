# Full Bible Restructure Implementation Plan

> **Historical design record:** requirements, example paths, and checkboxes describe this dated plan, not current repository status or authorization to rerun it. Later [explanation-depth work](../plans/2026-10-08-explanation-depth.md), [AGENTS.md](../../../AGENTS.md), and [contributing.md](../../../contributing.md) govern current changes. Preserve stable chapter IDs; `TL;DR` and inline chapter cheat and revision sections are retired.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the `software-developer-bible` repository to a single unified numbering convention with category subfolders, complete the authentication track (video parity), and author 83 missing chapters across all stacks.

**Architecture:** Spec `docs/superpowers/specs/2026-08-25-full-restructure-design.md` is the authoritative move map and chapter list. Phase 1 executes structural moves stack by stack with automated relinking and verification, and Phases 2+ author content waves via parallel subagents following `contributing.md` templates, with one commit per task.

**Tech Stack:** Markdown, bash, `python3` (available at `/opt/homebrew/bin/python3`), and Git.

## Global Constraints

- Convention: category folders use `NN-slug/`, files in categories use `<stack>.<cat>.<seq>-slug.md` (`cat` = folder number without a leading zero), flat-stack files use `<stack>.<seq>-slug.md`, sequences are contiguous from `01`, and interview-questions files always appear last.
- Every chapter follows the `contributing.md` template: TL;DR, Definition, Why, How, Code, Real-world, Mistakes, Best practices, Summary, Cheat sheet, See Also, and References, with no emojis and badges matching `contributing.md`.
- Never commit or push in `~/repos/career-ops`, and never touch `80-lanes-abroad-full-stack/personal/` contents (symlinks); work in this repository only.
- Moves preserve chapter substance when relocating: only links, headers, and badges change.
- After every task, run `bash scripts/check-structure.sh` (created in Task 1) and verify it passes before committing.
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

### Task 2: Frontend structural moves (10.1–10.8)

**Files:** Move and rename entries per Section 3 of the spec under `10-frontend/` (all eight stacks), create a category `INDEX.md` for each new folder, and rebuild each affected stack `INDEX.md`. Do not create placeholder files for new chapters (they arrive in Wave A, Task 10), so indexes built in this task reference only files that exist at that moment.

**Interfaces:**
- Consumes: Section 3 of the spec (exact old-to-new map per stack) and Task 1 `relink.py`.
- Produces: final frontend paths such as `10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.01-execution-context.md`.
- [ ] **Step 1: Per stack, run `git mv` on every file into its new category folder and filename** (so history follows), processing `10.1`, `10.2`, `10.3`, `10.4`, and then flat compactions `10.5`–`10.8`.
- [ ] **Step 2: After each stack's moves**, run `python3 scripts/relink.py <old-basename-with-ext> <new/path/file.md>` for every moved basename.
- [ ] **Step 3: Rewrite internal headers and badges** in moved files where they self-reference old IDs (search each new folder for old basenames).
- [ ] **Step 4: Create category `INDEX.md`** per new folder (purpose, table of files with topics and read times, plus previous and next navigation).
- [ ] **Step 5: Rebuild each stack `INDEX.md`**: badge counts, category table, flow diagram, study paths, and cross-references matching only existing files.
- [ ] **Step 6: Verify** with `python3 scripts/check_structure.py --links-only` (zero new breaks versus the Task 0 baseline) and inspect `find 10-frontend -name "*.md" | sort` against the spec.
- [ ] **Step 7: Commit** — `git add -A && git commit -m "refactor(frontend): category subfolders + unified numbering per spec"`

---

### Task 3: Backend structural moves part 1 (20.1 Node, 20.2 NestJS, 20.3 REST, 20.4 Database)

Same procedure as Task 2 for stacks `20.1`–`20.4` per Section 3 of the spec. Commit message: `refactor(backend): category subfolders + numbering for node/nestjs/rest/database`.

---

### Task 4: Security restructure including auth numbering (20.5)

**Files:** Move per Section 3 of the spec under `20.5-security` (`auth/` becomes `01-auth/` with numbered files such as `auth-fundamentals` -> `20.5.1.01`, `attacks` -> `02-attacks-and-defense/`, `hardening` -> `03-hardening-and-operations/`, and `drills` -> `04-interview-drills/`).

Because the four new authentication chapters and OAuth slim-down happen in Task 9, this task numbers only existing files (`20.5.1.01`, `.04`, `.05`, `.06`, `.09`, `.10`). Temporary gaps `.02`, `.03`, `.07`, and `.08` clear in Task 9, and full `check_structure.py` mode starts from Task 14 onward.

- [ ] **Steps 1–6:** Same as Task 2, skipping the family-contiguity assertion and verifying links only; update the authentication `INDEX` stage table to show the planned 10 stages while linking only existing files.
- [ ] **Step 7: Commit** — `refactor(security): auth numbered track + attack/hardening/drills categories`

---

### Task 5: Backend structural moves part 2 (20.6 microservices, 20.7 GraphQL, 20.8 caching, 20.12 AI engineering)

Same as Task 2 for these four stacks per the spec. Commit: `refactor(backend): categories for microservices/graphql + caching/ai compaction`.

---

### Task 6: Architecture moves (30.1 conversion, 30.2 renames, 30.3 regrouping)

Per Section 3 of the spec, convert design-patterns folders and files to the dotted scheme (`30.1.11-singleton.md` becomes `02-creational/30.1.2.01-singleton.md`, and so on), rename system-design folders (`00-theory` to `01-theory` and `10-case-studies` to `02-case-studies`, keeping filenames unchanged), and regroup infra-patterns into five categories while closing gaps.

Repair links via `relink.py` per basename because many `INDEX` cross-links inside design patterns reference old concatenated IDs. Commit: `refactor(architecture): unified scheme for patterns/system-design/infra-patterns`.

---

### Task 7: Platform moves (40.1–40.10)

Per Section 3 of the spec, `kubernetes`, `ci-cd`, `observability`, and `build-tools` gain category folders, while `docker`, `git`, `serverless`, `monorepo`, and `cdn` get flat compactions (with interview questions last); `twelve-factor` stays unchanged, and the stray `.DS_Store` in `40.3` is deleted. Commit: `refactor(platform): categories + contiguous numbering across platform stacks`.

---

### Task 8: Quality, real-time, and toolkit moves (50.x, 60.x, 70.x)

Per Section 3 of the spec, `testing`, `performance`, `websockets`, and `coding-patterns` gain categories, while `accessibility`, `prod-eng`, `behavioral`, and `cheatsheets` get flat compactions. The behavioral `INDEX` adds a note that Situation, Task, Action, Result (STAR) basics live in `00-strategy`. Commit: `refactor(quality-toolkit): categories + contiguous numbering`.

---

### Task 9: Auth completion (video parity)

**Files:**
- Create: `20-backend/20.5-security/01-auth/20.5.1.02-http-basic-digest-auth.md`
- Create: `20-backend/20.5-security/01-auth/20.5.1.03-api-keys.md`
- Create: `20-backend/20.5-security/01-auth/20.5.1.07-sso-saml-federation.md`
- Create: `20-backend/20.5-security/01-auth/20.5.1.08-mfa-passkeys-webauthn.md`
- Modify: `20-backend/20.5-security/01-auth/20.5.1.06-oauth2-oidc.md` (extract single sign-on (SSO), SAML, and passkey sections and replace with links to `.07` and `.08`)
- Modify: `20-backend/20.5-security/01-auth/INDEX.md`, `20-backend/20.5-security/INDEX.md`

Coverage bullets per chapter follow Section 4 of the spec (authoritative). Author directly rather than via a subagent so precision stays exact, follow Global Constraints, rebuild the authentication `INDEX` as a 10-stage flow matching the video order (fundamentals, basic and digest, API keys, sessions, JWT with access and refresh, OAuth2 and OIDC, SSO and SAML, MFA and passkeys, RBAC and ABAC, and drills), and add the video to `References` of the `INDEX`.

- [ ] **Step 1: Write 4 chapters** (full template, 250+ lines each, TypeScript and NestJS code samples matching neighboring chapters).
- [ ] **Step 2: Slim `oauth2-oidc.md`**, leaving See Also links to `.07` and `.08`.
- [ ] **Step 3: Rebuild both `INDEX` files** (counts, stages, badges).
- [ ] **Step 4: Cross-link fixes**: REST authentication chapter and security interview bank reference new chapters.
- [ ] **Step 5: Verify links-only check passes and commit** — `feat(security): complete auth track - basic/digest, api keys, sso/saml, mfa/passkeys`

---

### Task 10: Wave A — Frontend chapters (13)

Dispatch two parallel general agents (Agent A1: 7 chapters; Agent A2: 6 chapters). Give each agent the `contributing.md` path to read first, one neighbor chapter path per stack for tone calibration, its chapter list below with required coverage bullets, instructions to append new files to the category `INDEX` and stack `INDEX` tables with updated badge counts, and the requirement to pass the links-only check before finishing:

- **Agent A1:** `dom-events-delegation` (bubbling, capturing, delegation, synthetic-event contrast), `cross-tab-communication` (`BroadcastChannel`, storage events, `SharedWorker` vs `postMessage`, logout-sync pattern), `tsconfig-compiler-options` (`strict` matrix, `moduleResolution` `bundler` and `nodenext`, `isolatedModules`, `incremental`), `type-variance` (covariance, contravariance, function bivariance, `in` and `out`), `usesyncexternalstore` (tearing, Zustand and Redux integration), `react-router` (v6 and v7 data routers, loaders and actions, protected routes), and `deploying-nextjs` (standalone Docker, Vercel vs self-hosting, Edge runtime limits, multi-zone).
- **Agent A2:** `autosave-draft-recovery` (debounced saves, IndexedDB and `localStorage` drafts, dirty guards), `canvas-svg-animation` (`requestAnimationFrame` (rAF) loop, `stroke-dashoffset`, Canvas vs DOM performance), `css-architecture-styling-approaches` (BEM, CUBE, CSS Modules vs CSS-in-JS vs Tailwind decision, cascade layers), `theming-design-tokens` (tokens, `prefers-color-scheme`, flash of unstyled content (FOUC) avoidance), `deep-linking-universal-links` (schemes, deferred links, cold and warm starts), and `testing-react-native-apps` (Detox, Maestro, device farms).
- [ ] **Step 1: Dispatch agents, wait, and review outputs** (template compliance, no emojis, resolving links).
- [ ] **Step 2: Run links-only check, fix any breaks, and commit** — `feat(frontend): wave A - 13 new chapters`

---

### Task 11: Wave B — Backend chapters (20)

Dispatch three parallel agents:

- **Agent B1 (Node and NestJS):** `debugging-profiling-nodejs` (`--inspect` and `--prof`, heap snapshots, CPU vs memory bound), `express-fastify-internals` (middleware chain, error middleware semantics, Fastify hooks and encapsulation, performance drivers), `lifecycle-hooks-graceful-shutdown` (`OnModuleInit`, `Bootstrap`, `Destroy`, `enableShutdownHooks`, `SIGTERM` ordering), `scheduling-background-jobs` (`@nestjs/schedule` crons, BullMQ, idempotent handlers), and `swagger-openapi-nestjs` (`@nestjs/swagger` DTO mapping, `DocumentBuilder`, codegen).
- **Agent B2 (REST, Database, Security, Microservices, and GraphQL):** `long-running-api-operations` (`202` plus status endpoint, polling vs callbacks), `file-upload-apis` (multipart limits, presigned S3, resumable `tus`, antivirus gates), `orm-query-builder-landscape` (Drizzle, Knex, TypeORM vs Prisma decision tree), `backups-pitr-recovery` (WAL archiving, `pgBackRest`, recovery point and time objectives (RPO and RTO), restore drills), `search-infrastructure-at-scale` (when Elasticsearch, OpenSearch, or Meilisearch beats GIN full-text search (FTS), change data capture (CDC) sync, relevance), `vulnerability-management-patch-governance` (Common Vulnerabilities and Exposures (CVE) triage, patch service-level agreements (SLAs), Software Bill of Materials (SBOM) response), `decomposing-monolith-database` (service-owned schemas, shared-table hazards, transition sync), and `codegen-schema-safety-ci` (GraphQL Codegen, typed documents, continuous integration (CI) schema checks).
- **Agent B3 (Auth 4 plus AI 3):** `http-basic-digest-auth`, `api-keys`, `sso-saml-federation`, and `mfa-passkeys-webauthn` per Section 4 of the spec if Task 9 was not completed by the main worker (otherwise skip), plus `retrieval-quality-hybrid-search-reranking` (hybrid BM25 plus vector search, rerankers, Hierarchical Navigable Small World (HNSW) and inverted file index (IVF), `recall@k` evaluations), `agent-orchestration-patterns` (plan-act loops, state machines and graphs, stop criteria, cost guards), and `serving-models-hosted-vs-self-hosted` (vLLM basics, quantization, latency, cost, and residency matrix).

Note: if Task 9 completed first, B3 covers only the AI trio (3 chapters).

- [ ] **Steps 1–2:** Dispatch, review, verify, and commit — `feat(backend): wave B - backend/AI/auth-support chapters`

---

### Task 12: Wave C — Architecture chapters (14)

Dispatch two parallel agents:

- **Agent C1 (Patterns 5 plus Infra 4):** `null-object`, `ddd-tactical-patterns-aggregates-value-objects`, `anti-corruption-layer`, `service-locator-vs-dependency-injection`, `presentation-patterns-mvc-mvp-mvvm`, `feature-flags-kill-switches` (flag stores, targeting, kill-switch SLAs), `backup-strategy-restore-drills` (drill cadence and game days — mechanics live in `20.4.5.04`, link it), `cost-engineering-finops` (rightsizing, tiers, spot instances), and `data-retention-archival` (policies, tiering, cold storage).
- **Agent C2 (Case studies 5, matching `url-shortener` format):** `typeahead-autocomplete` (trie, geo-sharding, freshness), `metrics-monitoring-pipeline` (time-series database (TSDB) ingestion, downsampling, cardinality), `distributed-job-scheduler` (cron at scale, leases, visibility timeouts), `distributed-id-generator` (Snowflake, clock skew, k-sortability), and `ad-click-aggregator` (streaming deduplication, windowed aggregation, exactly-once sinks).
- [ ] **Steps 1–2:** Dispatch, review, verify, and commit — `feat(architecture): wave C - patterns + case studies + ops chapters`

---

### Task 13: Wave D — Platform chapters (19)

Dispatch three parallel agents:

- **Agent D1 (Docker and Kubernetes 6):** `container-runtime-internals-namespaces-cgroups`, `image-signing-sbom-supply-chain` (`cosign`, SBOM, Supply-chain Levels for Software Artifacts (SLSA) provenance), `rootless-sandboxed-runtimes` (gVisor and Kata), `node-autoscaling-cluster-capacity` (`cluster-autoscaler`, Karpenter), `kustomize-overlays-packaging-tradeoffs`, and `crds-operators-controller-patterns` (reconcile loops).
- **Agent D2 (CI/CD, Observability, and Build 6):** `artifact-registries-release-promotion`, `pipeline-supply-chain-security-slsa` (action pinning, OIDC, attestation), `dora-metrics-delivery-performance`, `continuous-profiling` (Pyroscope and Parca), `ebpf-observability` (Hubble and Pixie), and `asset-pipelines-css-images-fonts` (PostCSS and Tailwind build, image and font optimization).
- **Agent D3 (Git, Serverless, Monorepo, and CDN 7):** `git-internals-objects-refs-packfiles`, `git-at-scale-lfs-partial-clones`, `signed-commits-repository-security`, `durable-execution-temporal-inngest`, `versioning-publishing-strategies` (Changesets in practice), `multi-cdn-traffic-steering`, and `media-optimization-at-the-edge`.
- [ ] **Steps 1–2:** Dispatch, review, verify, and commit — `feat(platform): wave D - 19 platform chapters`

---

### Task 14: Wave E — Quality, real-time, and toolkit chapters (17)

Dispatch two parallel agents:

- **Agent E1 (Quality and real-time 9):** `test-data-management-anonymization` (GDPR-safe fixtures), `accessible-charts-data-viz`, `accessibility-design-systems`, `http2-http3-performance-effects` (head-of-line (HOL) blocking, connection coalescing), `production-readiness-reviews`, `on-call-without-burnout`, `graphql-subscriptions-live-queries`, `webrtc-peer-to-peer` (Selective Forwarding Unit (SFU) vs mesh), and `testing-realtime-systems` (Artillery WebSockets, connection churn).
- **Agent E2 (Toolkit 8):** `stakeholder-management-stories`, `judgment-calls-ambiguity`, `behavioral-anti-patterns-checklist` (self-audit rubric), `shortest-paths-dijkstra-bellman-ford`, `linked-list-manipulation-patterns`, `matrix-traversal-simulation`, `docker-kubernetes-cicd-cheat-sheet`, and `sql-data-modeling-cheat-sheet`.
- [ ] **Steps 1–2:** Dispatch, review, verify, and commit — `feat(quality-realtime-toolkit): wave E - 17 chapters`

---

### Task 15: Root docs + full verification

- [ ] **Step 1: Update root `INDEX.md`, `README.md`, and `ROADMAP.md`** — update stack counts, structure trees, and totals (83 new chapters reflected).
- [ ] **Step 2: Update `AGENTS.md` and `contributing.md`** — replace design-patterns convention text in `AGENTS.md` with unified convention text, and update Directory Structure and File Naming sections in `contributing.md`.
- [ ] **Step 3: Full check** — run `python3 scripts/check_structure.py` (no flags) and verify zero broken links, zero duplicate IDs, and all families contiguous.
- [ ] **Step 4: Doctor** — confirm `bash 80-lanes-abroad-full-stack/personal/doctor.sh` stays clean.
- [ ] **Step 5: Final commit** — `docs: root indexes + conventions updated for unified structure; full verification green`

## Self-Review Notes

- Spec coverage: Spec Sections 2 (Task 15 conventions), 3 (Tasks 2–8), 4 (Task 9), 5 (Tasks 10–14), 6 (`INDEX` steps inside every task), 7 (Tasks 0 and 15 checks), and 8 (order preserved) are all covered.
- Type consistency: scripts' CLI contracts are fixed in Tasks 0 and 1 and consumed identically afterward.
- Known sequencing dependency: full family-contiguity check is only valid after Task 8; Tasks 2–8 use `--links-only`.
