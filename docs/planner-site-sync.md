# Bible and personal-site sync

The Bible is canonical for public topic explanations and study priorities, while career documents and account data have a separate private owner.

`repos/portfolio` publishes `personal.buildora.work`; its generated chapter catalog must be refreshed after Bible topic or priority edits. The site does not copy private CVs, applications, family information, or career reports into its public bundle.

## What must agree

- Topic path and ID, title, read time, role priority, and general importance come from each chapter's metadata.
- Essential core engineering and system design take precedence. Animation is Optional, HTML and CSS basics remain Essential, and Java and Indian Software Development Engineer (SDE) preparation is Deferred.
- The 100-day chapter inventory is a navigation backlog, not a requirement to study everything before applying.
- The private execution plan owns the timetable. Study evidence, completed work, unrelated to-dos, and reminder choices survive reseeding.
- The shipped curriculum's content digest identifies its source bytes. It differs from the Bible API's broader corpus digest because the two inventories have different scope.

## Refresh and release

From the sibling `repos/portfolio` checkout, run `pnpm career:generate`, then `pnpm career:validate`. These read the sibling Bible checkout; in an isolated worktree, pass the absolute Bible checkout using the generator's `--bible-root` option instead.

Run the curriculum and sync-state unit tests, lint, typecheck, production build, and focused roadmap browser tests. Inspect the generated diff, commit only the intended portfolio changes, and push its `main` branch. Verify the Git-connected production deployment for that commit; a successful local build is insufficient.

### Release a revised execution plan

Generate the forward plan with `pnpm career:forward:generate`, using the canonical private inputs and new output filenames documented in the portfolio runbook. Validate dates, minute caps, prerequisites, stable assignment references, and preservation of existing history, then deploy the compatible application before importing its new assignment schema.

Run `scripts/sync-germany-roadmap.ts` with the exact validated payload and private environment configuration. Its default is a dry run: inspect the owner, changed keys, and final merged values before repeating that payload with `--apply`.

It changes only the career and timetable rows, uses one compare-and-swap per row, and verifies every owner row afterward. Each row update is atomic, though the two-row release is not a single transaction.

A conflict stops the import and reports any applied keys; re-read and reconcile instead of blindly restoring a backup. Backups and previews contain account data and belong only in private, `mode-0600` files, and a successful repeat dry run must report no changes.

The orientation guide has its own `scripts/sync-career-plan.ts` import into the career row. Keep that payload private too; neither import enables reminders, verifies candidate readiness, nor sends applications or outreach.

### Initialize an account separately

`pnpm career:seed` is an initialization workflow, not a replacement for an existing execution plan. It targets one owner and five planner keys, using the dedicated atomic Remote Procedure Call (RPC) when available or one atomic bulk upsert only when that function is absent.

Other failures stop the write. Validate its dry run and compare every expected value in readback; the published page can also refresh saved chapter metadata from its shipped catalog without moving scheduled work.

No automatic cross-repository scheduled job is configured. Every future Bible topic change requires this refresh and release step; record a blocked deployment explicitly rather than claiming the sites are in sync.

## Bible release gates

Run the count, read-time, alignment, and search generators as required, then `bash scripts/verify.sh` before committing or pushing the Bible. Run the personal doctor when changing canonical personal artifacts, and keep the public portfolio checkout separate from its unrelated in-progress UI work.
