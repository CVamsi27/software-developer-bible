# Node.js Production Runtime Architecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Add a senior-level Node.js learning path explaining PM2 process supervision and Watt's worker-thread application runtime, their operational boundaries, and how to investigate their failure behavior.

**Architecture:** Add two numbered teaching chapters after Node's existing process, worker, and clustering foundations. Integrate both into the process category and Node.js indexes, keep recall questions in `REVISION.md`, add distinct interview prompts, and regenerate the site's derived catalogs and count claims.

**Tech Stack:** Markdown, Jekyll with the repository-pinned Ruby 3.4.11 and locked Bundler dependencies, Python corpus gates and generators, and official Node.js, PM2, and Platformatic documentation.

## Global Constraints

- Preserve existing chapter IDs, URLs, authored examples, study order, and source material.
- Each concept chapter has a practical definition, a distinct textbook definition, First Principles, one final Summary, See Also, and References; do not add `TL;DR` or embed revision drills.
- Start with a concrete production problem, explain one new term at a time, trace cause to mechanism to observable result, and end at the decision boundary.
- Reuse the existing clustering, worker-thread, and process-lifecycle chapters as canonical homes for Node primitives; link to them instead of duplicating their code or explanations.
- Distinguish a worker process, a worker thread, an application runtime, a process supervisor, and a container orchestrator, never implying shared in-memory state, exactly-once external effects, or zero downtime without evidence.
- Verify product-specific behavior against official documentation while authoring, naming versions only for claims that cannot be stated version-neutrally.
- Keep `REVISION.md` separate, preserve every existing prompt, and add at least five fresh source-linked `**Q:**` and `**A:**` pairs across the PM2 and Watt groups.
- Update all file counts, read-time metadata, search output, and API catalog through their repository scripts rather than editing generated outputs by hand.
- Limit this implementation to Node.js PM2 and Watt runtime architecture; JVM, Kubernetes, TypeScript, Redis, and V8 remain separate future passes.

---

## File map

- Create `20-backend/20.1-node.js/03-processes-and-concurrency/20.1.3.04-pm2-process-supervision.md` for PM2's process-management model and lifecycle behavior.
- Create `20-backend/20.1-node.js/03-processes-and-concurrency/20.1.3.05-watt-runtime-architecture.md` for Watt's application, worker-thread, internal-routing, and shared-process model.
- Modify `20-backend/20.1-node.js/03-processes-and-concurrency/INDEX.md` to add both chapters and connect the reading flow.
- Modify `20-backend/20.1-node.js/INDEX.md` to clarify the process-runtime learning path and keep the category row accurate.
- Modify `20-backend/20.1-node.js/03-processes-and-concurrency/20.1.3.01-clustering.md` with a concise pointer to process supervision where PM2 is mentioned.
- Modify `20-backend/20.1-node.js/03-processes-and-concurrency/REVISION.md` with source-linked recall groups for PM2 and Watt.
- Modify `20-backend/20.1-node.js/04-security-and-operations/20.1.4.04-interview-questions.md` with four distinct senior-level prompts, numbered `Q41`–`Q44`, and update its opening count from 40 to 44.
- Regenerate `search.html`, `api/index.json`, the external-link baseline if new chapter citations are added, and count-bearing repository summaries through their owning scripts.

### Task 1: Teach PM2 process supervision

**Files:**
- Create: `20-backend/20.1-node.js/03-processes-and-concurrency/20.1.3.04-pm2-process-supervision.md`
- Modify: `20-backend/20.1-node.js/03-processes-and-concurrency/INDEX.md`
- [x] **Step 1: Open with a concrete failure and define supervision.** Explain the incident where a Node server crashes after accepting a request: PM2 can restart capacity, but cannot restore the lost response or prove a side effect did not happen; add a practical definition and a textbook definition of process supervision.
- [x] **Step 2: Derive the process topology.** Add a small diagram showing the `pm2` command-line interface (CLI), the background PM2 daemon and process list, the managed Node process or cluster workers, and the operating-system and container boundary, explaining which component starts, monitors, replaces, and persists which state.
- [x] **Step 3: Explain the execution and lifecycle decisions.** Compare PM2 fork mode with cluster mode (linking cluster mode to the clustering chapter), trace start, readiness, request admission, crash and restart, and shutdown, and explain that readiness, graceful draining, restart budgets, and startup persistence are separate behaviors rather than promising zero downtime from `reload` alone.
- [x] **Step 4: Bound the claim and link decisions.** Compare PM2's app-process responsibility with `systemd`'s service responsibility and a container orchestrator's placement and replica responsibility, add one short failure table for app exit, PM2 daemon exit, and host or container loss, and end with the operational trade-off, one Summary, See Also, and References.
- [x] **Step 5: Add the category entry and verify the file.** Place PM2 after existing process, worker, and cluster fundamentals in the category map and reading flow, then run `python3 scripts/check_template.py` and `python3 scripts/read_time.py --file 20-backend/20.1-node.js/03-processes-and-concurrency/20.1.3.04-pm2-process-supervision.md --dry-run` before continuing.

### Task 2: Teach Watt's application-runtime architecture

**Files:**
- Create: `20-backend/20.1-node.js/03-processes-and-concurrency/20.1.3.05-watt-runtime-architecture.md`
- Modify: `20-backend/20.1-node.js/03-processes-and-concurrency/INDEX.md`
- [x] **Step 1: Open with the deployment-boundary problem.** Contrast a single Node process whose modules share one event loop with separately deployed microservices that add process, network, and operational overhead; define `wattpm` as the CLI and Watt as the runtime, adding practical and textbook definitions.
- [x] **Step 2: Trace the thread-per-application topology.** Diagram the runtime main thread and application worker threads, explaining each worker's V8 isolate, heap, module registry, globals, and event loop while distinguishing this isolation from a separate process or container.
- [x] **Step 3: Follow an internal request and worker lifecycle.** Trace a `.plt.local` call through Watt's documented dispatcher and `MessagePort` path (without opening a Transmission Control Protocol (TCP) connection, while noting request and response data still crosses a thread boundary), plus dependency-aware startup, health checks, replacement, shutdown, and shared telemetry without repeating worker-thread API details.
- [x] **Step 4: State the failure and deployment boundary.** Explain that applications in one Watt runtime start, stop, and deploy together so thread-level failure isolation cannot contain process-wide native crashes, process memory exhaustion, or exit policies terminating the host process; identify when to split into separate runtimes or containers vs keeping a shared deployment unit.
- [x] **Step 5: Add a bounded observation exercise and category entry.** Ask readers to run a process-local counter and slow request, observe a worker restart, and record which state and requests survive without asking for benchmark claims; add Watt after PM2 in the category reading flow and run `python3 scripts/check_template.py` and `python3 scripts/check_structure.py`.

### Task 3: Connect the new chapters to the existing Node.js journey

**Files:**
- Modify: `20-backend/20.1-node.js/03-processes-and-concurrency/INDEX.md`
- Modify: `20-backend/20.1-node.js/INDEX.md`
- Modify: `20-backend/20.1-node.js/03-processes-and-concurrency/20.1.3.01-clustering.md`
- [x] **Step 1: Make the category flow explicit.** Start from process configuration and shutdown, revisit worker and process boundaries and clustering, then compare PM2's external process supervision with Watt's in-process application supervision while preserving child-process and cluster chapters as canonical API explanations.
- [x] **Step 2: Update the Node.js stack introduction.** Add process supervision and application-runtime architecture to the category description and reading pass while keeping the root index concise and pointing to the category `INDEX` for the full sequence.
- [x] **Step 3: Add a discoverable PM2 link from clustering.** Replace the brief PM2 mention with a human-title link to the new PM2 chapter and one See Also pointer rather than copying configuration or lifecycle details into the cluster chapter.
- [x] **Step 4: Verify numbering and navigation.** Run `python3 scripts/check_structure.py` and `python3 scripts/check_alignment.py`, confirming the two sequence IDs are contiguous and linked from the category `INDEX` while deferring count validation until Task 5.

### Task 4: Add revision and interview practice

**Files:**
- Modify: `20-backend/20.1-node.js/03-processes-and-concurrency/REVISION.md`
- Modify: `20-backend/20.1-node.js/04-security-and-operations/20.1.4.04-interview-questions.md`
- [x] **Step 1: Add a source-linked PM2 revision group.** Add three fresh `**Q:**` and `**A:**` pairs testing daemon and process-list ownership, readiness versus listening, and why restart or reload does not recover an uncertain in-flight side effect.
- [x] **Step 2: Add a source-linked Watt revision group.** Add three fresh pairs testing `.plt.local` routing and its non-network cost boundary, thread versus process failure, and the deployment-independence trade-off, linking the group to the Watt chapter and official references.
- [x] **Step 3: Add four senior interview prompts.** Add `Q41`–`Q44` covering: (41) readiness and PM2 registration, (42) reload versus request-level availability guarantees, (43) PM2 cluster processes versus Watt threads and their failure domains, and (44) extracting a Watt mesh application to a network service, giving each answer a concrete trace and canonical chapter link without copying revision answers.
- [x] **Step 4: Correct and verify the interview-bank count.** Update the bank's opening claim from 40 to 44 and run `python3 scripts/check_template.py` and `python3 scripts/check_answer_depth.py` to confirm existing prompts remain and new answers meet the prose-depth gate.

### Task 5: Refresh derived catalogs and citations

**Files:**
- Modify through generators: `20-backend/20.1-node.js/**` read-time metadata, `search.html`, `api/index.json`, count-bearing summary files, `scripts/external-links-baseline.json` when new live citations are introduced.
- [x] **Step 1: Refresh read times.** Run `python3 scripts/read_time.py --write`, then `python3 scripts/read_time.py --check`.
- [x] **Step 2: Regenerate search and API output.** Run `python3 scripts/gen_master_index.py` after the read-time refresh, then `python3 scripts/gen_master_index.py --check`.
- [x] **Step 3: Review and probe the citation delta.** Run `python3 scripts/link_baseline.py`, then probe the chapter sources with the repository's checker:

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, 'scripts')
from check_freshness import probe

urls = [
    'https://nodejs.org/api/cluster.html',
    'https://nodejs.org/api/worker_threads.html',
    'https://pm2.io/docs/runtime/guide/process-management/',
    'https://pm2.io/docs/runtime/guide/load-balancing/',
    'https://pm2.io/docs/runtime/best-practices/graceful-shutdown/',
    'https://docs.platformatic.dev/docs/concepts/watt-architecture',
    'https://docs.platformatic.dev/docs/reference/runtime/multithread-architecture',
]
for url in urls:
    status, detail = probe(url)
    print(status, detail, url)
    if status != 'LIVE':
        raise SystemExit(1)
PY
```

Replace any dead citation with an official live source. Once every newly cited URL returns LIVE, run `python3 scripts/link_baseline.py --update` and verify the clean baseline diff.
- [x] **Step 4: Restamp counts and formatting.** Run `python3 scripts/check_counts.py --write`, then `python3 scripts/check_alignment.py --fix` if the generated digit changes alter table widths. Run the count, alignment and read-time checks again.

### Task 6: Run corpus, build, and rendered-page checks

**Files:**
- Verify: all files modified in Tasks 1–5, plus generated `search.html` and `api/index.json`.
- [x] **Step 1: Run the full repository gates.** Run `bash scripts/verify.sh` and resolve every reported issue across count, alignment, structure, links, freshness, metadata, duplication, revision-depth, generated-catalog, and fixed-point checks.
- [x] **Step 2: Run the required standalone link gate.** Run `python3 scripts/check_links.py`, requiring zero broken relative links and stale labels.
- [x] **Step 3: Build the production-equivalent site with the pinned Ruby.** Run `PATH=/opt/homebrew/opt/ruby@3.4/bin:$PATH BUNDLE_PATH=vendor/bundle JEKYLL_ENV=production bundle exec jekyll build --destination /tmp/bible-node-runtime-2026-10-14`.
- [x] **Step 4: Check the rendered pages.** Run `python3 scripts/test_rendered_headings.py /tmp/bible-node-runtime-2026-10-14`, inspecting both generated chapter pages and their category navigation to confirm each has one visible title, complete authored content, valid internal links, and a correct position in the reading flow.
- [x] **Step 5: Review the final change set.** Run `git diff --check` and inspect `git diff --stat` plus the full diff, confirming only the scoped Node.js chapters, companion and index updates, and generated metadata and catalog files changed while leaving the JVM, Kubernetes, TypeScript, Redis, and V8 follow-on gaps untouched.
