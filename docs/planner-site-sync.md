# Bible and personal-site sync

The Bible is canonical for public topic explanations and study priorities. Career documents and account data have a separate private owner. `repos/portfolio` publishes `personal.buildora.work`; its generated chapter catalog must be refreshed after Bible topic or priority edits. The site does not copy private CVs, applications, family information or career reports into its public bundle.

## What must agree

- Topic path/ID, title, read time, role priority and general importance come from each chapter's metadata.
- Essential core engineering and system design take precedence. Animation is Optional, HTML/CSS basics remain Essential, and Java/Indian SDE preparation is Deferred.
- The 100-day chapter inventory is a navigation backlog, not a requirement to study everything before applying.
- The private execution plan owns the timetable. Study evidence, completed work, unrelated todos and reminder choices survive reseeding.
- The shipped curriculum's content digest identifies its source bytes. It differs from the Bible API's broader corpus digest because the two inventories have different scope.

## Refresh and release

From the sibling `repos/portfolio` checkout, run `pnpm career:generate`, then `pnpm career:validate`. These read the sibling Bible checkout. In an isolated worktree, pass the absolute Bible checkout using the generator's `--bible-root` option instead.

Run the curriculum and sync-state unit tests, lint, typecheck, production build and focused roadmap browser tests. Inspect the generated diff, commit only the intended portfolio changes and push its main branch. Verify the Git-connected production deployment for that commit; a successful local build is insufficient.

### Release a revised execution plan

Generate the forward plan with `pnpm career:forward:generate`, using the canonical private inputs and new output filenames documented in the portfolio runbook. Validate dates, minute caps, prerequisites, stable assignment references and preservation of existing history. Deploy the compatible application before importing its new assignment schema.

Run `scripts/sync-germany-roadmap.ts` with the exact validated payload and private environment configuration. Its default is a dry run. Inspect the owner, changed keys and final merged values before repeating that payload with `--apply`. It changes only the career and timetable rows, uses one compare-and-swap per row and verifies every owner row afterward. Each row update is atomic; the two-row release is not a transaction. A conflict stops the import and reports any applied keys. Re-read and reconcile instead of blindly restoring a backup. Backups and previews contain account data and belong only in private, mode-0600 files. A successful repeat dry run must report no changes.

The orientation guide has its own `scripts/sync-career-plan.ts` import into the career row. Keep that payload private too. Neither import enables reminders, verifies candidate readiness nor sends applications or outreach.

### Initialize an account separately

`pnpm career:seed` is an initialization workflow, not a replacement for an existing execution plan. It targets one owner and five planner keys, using the dedicated atomic RPC when available or one atomic bulk upsert only when that function is absent. Other failures stop the write. Validate its dry run and compare every expected value in readback. The published page can also refresh saved chapter metadata from its shipped catalog without moving scheduled work.

No automatic cross-repository scheduled job is configured. Every future Bible topic change needs this refresh/release step; record a blocked deployment explicitly rather than claiming the sites are in sync.

## Bible release gates

Run the count/read-time/alignment/search generators as required, then `bash scripts/verify.sh` before committing or pushing the Bible. Run the personal doctor when changing canonical personal artifacts. Keep the public portfolio checkout and its unrelated in-progress UI work separate.
