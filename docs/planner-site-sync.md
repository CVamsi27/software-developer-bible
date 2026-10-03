# Bible and personal-site sync

The Bible is canonical for topic explanations, study priorities and private career documents. `repos/portfolio` publishes `personal.buildora.work`; its generated chapter catalog must be refreshed after Bible topic or priority edits. The site does not copy private CVs, applications, family information or career reports into its public bundle.

## What must agree

- Topic path/ID, title, read time, role priority and general importance come from each chapter's metadata.
- Essential core engineering and system design take precedence. Animation is Optional, HTML/CSS basics remain Essential, and Java/Indian SDE preparation is Deferred.
- The 100-day chapter inventory is a navigation backlog, not a requirement to study everything before applying.
- The private execution plan owns the timetable. Study evidence, completed work, unrelated todos and reminder choices survive reseeding.
- The shipped curriculum's content digest identifies its source bytes. It differs from the Bible API's broader corpus digest because the two inventories have different scope.

## Refresh and release

From the sibling `repos/portfolio` checkout, run `pnpm career:generate`, then `pnpm career:validate`. These read the sibling Bible checkout. In an isolated worktree, pass the absolute Bible checkout using the generator's `--bible-root` option instead.

Run the curriculum and sync-state unit tests, lint, typecheck, production build and focused roadmap browser tests. Inspect the generated diff, commit only the intended portfolio changes and push its main branch. Verify the Git-connected production deployment for that commit; a successful local build is insufficient.

For cloud planner rows, use private environment configuration to run the seed in dry-run first, then apply after validation. The seed targets one owner and five planner keys. It uses the dedicated atomic RPC when available, or one atomic bulk upsert only when the function is absent. Other failures stop the write. Readback must match every expected value, not merely counts. The published page also refreshes saved chapter metadata from its shipped catalog without moving scheduled work.

No automatic cross-repository scheduled job is configured. Every future Bible topic change needs this refresh/release step; record a blocked deployment explicitly rather than claiming the sites are in sync.

## Bible release gates

Run the count/read-time/alignment/search generators as required, then `bash scripts/verify.sh` before committing or pushing the Bible. Run the personal doctor when changing canonical personal artifacts. Keep the public portfolio checkout and its unrelated in-progress UI work separate.
