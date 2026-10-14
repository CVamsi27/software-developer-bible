<!-- section: Git Advanced | category: Reference | tags: revision, practice | role-priority: important | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Git%20Advanced-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-6_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../docs/topic-importance.md)

# Git Advanced — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Git Internals: Objects, Refs & Packfiles

Source: [Git Internals: Objects, Refs & Packfiles](40.6.01-git-internals-objects-refs-packfiles.md)

**Q:** Why does editing a committed file not mutate its existing Git object?

**A:** Objects are content-addressed and immutable; new content creates new objects and a new commit tree. Branch refs move to select history.

**Q:** Where does Git store a tracked file's executable mode, and does changing that mode change the blob?

**A:** The tree entry stores mode and filename; the blob stores file content. A mode-only change creates a different tree while the unchanged content can reuse the same blob.

**Q:** Why should a repository tool not assume every branch is a 41-byte file?

**A:** That describes a loose SHA-1 ref in the traditional files backend. References can be packed or use another backend, and object-ID length depends on repository format. Use Git's ref and object APIs rather than assuming on-disk filenames or byte lengths.

**Q:** Why can `git reflog` fail to recover work after `git reset --hard`?

**A:** A reflog records local ref movements; it does not store uncommitted file bytes. It can help locate a commit only while the entry and its objects remain available, and entries expire according to repository configuration. Preserve valuable work in a commit or verified backup. See [git-reflog](https://git-scm.com/docs/git-reflog).

**Q:** Why can deleting a large file and committing the deletion leave the repository just as large?

**A:** Earlier commits still reference the file's blob, so it remains reachable through retained history. Removing it from old history requires a coordinated rewrite, and storage is reclaimed only after all retained refs and cleanup policies allow it. See [Git at Scale](40.6.08-git-at-scale-lfs-partial-clones.md).

**Q:** Why might `.git` be a file in a linked worktree, and where are its objects?

**A:** A linked worktree uses a gitfile that points to per-worktree metadata. Its HEAD and index are separate, while the common Git directory holds shared objects and most repository metadata. Ask Git for paths with `git rev-parse --git-dir --git-common-dir`; see [repository layout](https://git-scm.com/docs/gitrepository-layout) and [git-worktree](https://git-scm.com/docs/git-worktree).

## Branching Strategies

Source: [Branching Strategies](40.6.02-branching-strategies.md)

**Q:** What should determine a branching strategy?

**A:** Start with integration frequency, number of versions still supported, release timing, and required review/CI controls. GitHub Flow describes a pull-request loop; trunk-based development describes frequent integration, so short reviewed branches can satisfy both. See [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow) and [short-lived trunk branches](https://trunkbaseddevelopment.com/short-lived-feature-branches/).

**Q:** A tested fix is on the trunk, but versions 2.4 and 2.5 are still supported. How should it reach them?

**A:** Backport only the fix to each affected release line, then run that line's tests and release checks; the trunk result cannot validate older dependencies. Record the source and destination commits, owner, and artifact released. See the [release-branch guidance](https://trunkbaseddevelopment.com/branch-for-release/) and [Rebase & Cherry-Pick](40.6.03-rebase-cherry-pick.md).

**Q:** Why does deleting a merged topic branch not identify what is deployed?

**A:** A branch name is a movable reference and may be deleted after review. A release must record its exact source commit and artifact digest; deployment and rollback use those immutable identities rather than a branch label.

## Rebase & Cherry-Pick

Source: [Rebase & Cherry-Pick](40.6.03-rebase-cherry-pick.md)

**Q:** After rebasing a private feature branch, how do you check that the intended patch series survived?

**A:** Save the old tip and base before replay, compare the old and new ranges with `git range-diff`, then run the feature tests on the new base. Rebase can omit patches already present upstream or flatten merges unless merge preservation is requested. See [git-rebase](https://git-scm.com/docs/git-rebase) and [git-range-diff](https://git-scm.com/docs/git-range-diff).

**Q:** A fix must be backported to a maintained release. What does cherry-pick carry over, and what must you verify?

**A:** Cherry-pick reapplies the selected commit's change relative to its parent; it does not bring prerequisite commits or original ancestry. Use `-x` for a clean cross-branch pick, check dependencies, and run the destination release's tests. See [git-cherry-pick](https://git-scm.com/docs/git-cherry-pick).

**Q:** Why does `git cherry-pick -m 1 <merge>` not reproduce the original merge?

**A:** `-m 1` computes the merge commit's change relative to its first parent and applies that patch to the current branch. It neither preserves the original merge ancestry nor guarantees the selected diff is limited to the desired fix. See the [git-cherry-pick manual](https://git-scm.com/docs/git-cherry-pick).

**Q:** After rewriting a branch that already exists on the remote, what makes the update safer, and what does it not make safe?

**A:** Coordinate because collaborators may depend on the old IDs. Capture the expected remote tip and use an explicit `--force-with-lease` so a concurrent remote update is rejected; this does not authorize rewriting a shared branch or bypass server policy. See [git-push](https://git-scm.com/docs/git-push).

## Git Hooks

Source: [Git Hooks](40.6.04-git-hooks.md)

**Q:** Why are local hooks not a complete policy enforcement mechanism?

**A:** They can be absent or bypassed. Enforce required checks and access policy at the shared integration boundary while using hooks for quick local feedback.

**Q:** Why can a passing worktree formatter fail to validate the snapshot a commit will contain?

**A:** The index is the commit snapshot; partially staged files can also contain unstaged worktree changes. Run the tool against staged content, then inspect the final index because formatters can modify what will be committed. See [lint-staged](https://github.com/lint-staged/lint-staged).

**Q:** A push updates `main` and a feature ref. How do `pre-receive` and `update` differ if policy rejects `main`?

**A:** `pre-receive` runs once for the receive operation, and a nonzero exit rejects every ref in that push. With a normal non-atomic push, `update` runs for each ref and can reject `main` while allowing the feature ref; `--atomic` makes the set all-or-nothing. See the [Git Hooks manual](https://git-scm.com/docs/githooks).

**Q:** A deployment notifier fails after a push succeeds. Did Git reject or roll back the push?

**A:** No. `post-receive` runs after refs are updated and cannot change the result. Treat downstream work as a separately monitored, retryable operation; do not report the accepted push as rejected. See the [post-receive hook](https://git-scm.com/docs/githooks).

## Git Advanced Commands

Source: [Git Advanced Commands](40.6.05-git-advanced-commands.md)

**Q:** When is revert safer than reset on a shared branch?

**A:** Revert adds a compensating commit without removing shared history. Reset moves a ref and can discard or require rewriting commits others already use.

**Q:** What must remain true for `git bisect` to identify the first commit that changed a property?

**A:** The good and bad endpoints must be correct, and every tested revision must be classified against the same observable test. If the test setup fails for an unrelated reason, skip that revision instead of calling it bad; skips near the transition can leave multiple candidates. See the [git-bisect manual](https://git-scm.com/docs/git-bisect).

**Q:** What can a reflog recover after a reset, and what evidence should you check before relying on it?

**A:** A reflog can name a previous local ref value. Inspect whether its object still exists, then create a rescue branch before changing the checkout. Reflog entries expire and do not contain uncommitted file bytes. See the [git-reflog manual](https://git-scm.com/docs/git-reflog).

**Q:** When is a stash a better fit than a worktree, and what does each preserve?

**A:** A stash is a local snapshot for briefly clearing one checkout; include untracked or ignored files explicitly and inspect the result before dropping it. A linked worktree gives a second checkout with its own index and `HEAD`, but shares repository storage and is not a backup. See the [git-stash](https://git-scm.com/docs/git-stash) and [git-worktree](https://git-scm.com/docs/git-worktree) manuals.

**Q:** How does `git submodule update --remote` differ from the default update?

**A:** The default restores the commit recorded by the superproject’s gitlink. `--remote` selects a configured remote-tracking tip, which can change the gitlink and therefore requires review and a parent-repository commit. See the [git-submodule manual](https://git-scm.com/docs/git-submodule).

**Q:** Why does reset’s `--hard` mode require more care than revert on a published branch?

**A:** `reset --hard` moves the current branch and replaces the index and tracked working files with the target, potentially overwriting untracked paths. Revert records a new inverse-change commit, so collaborators can keep using the published ancestry. A merge revert also needs an intentional mainline choice. See the [git-reset](https://git-scm.com/docs/git-reset) and [git-revert](https://git-scm.com/docs/git-revert) manuals.

## Git Patch, Bundle & Archive

Source: [Git Patch, Bundle & Archive](40.6.06-patch-and-bundle.md)

**Q:** What does applying a `format-patch` series preserve, and why do the resulting commit IDs differ?

**A:** Each mail carries a commit’s author/message and patch. `git am` replays it on the recipient’s base and creates a commit from the result. Its ID commonly changes when the parent or committer metadata changes; the original commit object and signature are not transferred. See the [git-format-patch](https://git-scm.com/docs/git-format-patch) and [git-am](https://git-scm.com/docs/git-am) manuals.

**Q:** Why must an incremental bundle be verified in the receiving repository?

**A:** Its excluded base commits are prerequisites. The sender already has them, so verification there proves nothing about the recipient. Verify in the actual target, then fetch and inspect the offered ref before integrating it. See the [git-bundle manual](https://git-scm.com/docs/git-bundle).

**Q:** What does a bundle created with `--all` fail to preserve?

**A:** It carries selected refs and reachable commits, not the index, working tree, reflogs, hooks or repository configuration. A bundle clone does not reliably reconstruct the stash list. Git 2.51 added `stash export`/`import` for explicit transfer; confirm both ends run 2.51+ and test the restore. LFS payloads and submodule repositories need separate backups. See the [git-bundle](https://git-scm.com/docs/git-bundle) and [Git 2.51 release notes](https://github.blog/open-source/git/highlights-from-git-2-51/).

**Q:** When should a release use `git archive` rather than a bundle?

**A:** Use an archive when the build needs the files from a specific tree but not Git history. It cannot restore refs or commits, and `export-ignore` or `export-subst` attributes can change its contents. Check LFS payload requirements separately. See [git-archive](https://git-scm.com/docs/git-archive) and [Git at Scale](40.6.08-git-at-scale-lfs-partial-clones.md).

**Q:** What does a `Signed-off-by` trailer establish, and how does it differ from a commit signature?

**A:** A sign-off is a contributor’s textual declaration required by some project policies; it is not cryptographic proof. A verified commit signature depends on a trusted key and policy. `format-patch --signature` is only a message footer. See [git-format-patch](https://git-scm.com/docs/git-format-patch) and [signed commits](40.6.09-signed-commits-repository-security.md).

## Git Code Archaeology

Source: [Git Code Archaeology](40.6.07-code-archaeology.md)

**Q:** What does `git blame` establish, and what evidence is needed before you explain a behavior change?

**A:** Blame attributes each current line to a recorded change. It does not identify the behavior-changing commit when a later refactor touched the line, and its author fields do not prove identity or intent. Inspect the candidate diff, tests and linked review/incident records. See the [git-blame](https://git-scm.com/docs/git-blame) and [git-show](https://git-scm.com/docs/git-show) manuals.

**Q:** When should you use `git log -S` instead of `git log -G`?

**A:** `-S` finds commits that change the number of occurrences of an exact string. `-G` finds commits whose added or removed patch lines match a regular expression, even when the match count stays the same. Inspect the patch before treating a match as causal. See the [git-log manual](https://git-scm.com/docs/git-log).

**Q:** How do `git blame -M`, `-C`, and `git log --follow` differ?

**A:** `-M` detects moved or copied lines within a file; `-C` also searches other files, with repeated `-C` widening the search. `--follow` continues one file's log across detected renames and accepts only a single path. These are heuristics, so inspect the resulting commits. See the [git-blame](https://git-scm.com/docs/git-blame) and [git-log](https://git-scm.com/docs/git-log) manuals.

**Q:** What does `git log -L` show, and what limits should shape its use?

**A:** It traces and prints patches for one line range or function in a file. The range must exist at the starting revision; the walk starts from at most one positive revision and cannot be combined with path limiters. See the [git-log manual](https://git-scm.com/docs/git-log).

**Q:** Why can `git log --all` still miss the history you need?

**A:** `--all` searches refs already present in the local repository. It cannot retrieve deleted or unfetched remote refs, and a shallow clone stops at its history boundary. Fetch relevant refs or deepen/unshallow the repository, then verify that the required objects are available. See the [git-log](https://git-scm.com/docs/git-log) and [partial-clone](https://git-scm.com/docs/partial-clone) manuals.

## Git at Scale: LFS & Partial Clones

Source: [Git at Scale: LFS & Partial Clones](40.6.08-git-at-scale-lfs-partial-clones.md)

**Q:** What do partial clone and sparse checkout reduce separately?

**A:** Partial clone can omit objects until needed; sparse checkout limits checked-out paths. A small working tree does not by itself shrink downloaded history.

**Q:** Why should a CI job use an explicit destination refspec when it deepens the branch used by `git merge-base`?

**A:** `git fetch origin main` always records the fetched commit in `FETCH_HEAD`, while updating `origin/main` depends on the remote's configured ref mapping. An explicit source-to-destination refspec guarantees the intended tracking ref is refreshed; then check the merge-base result. See the [git-fetch manual](https://git-scm.com/docs/git-fetch).

## Signed Commits & Repository Security

Source: [Signed Commits & Repository Security](40.6.09-signed-commits-repository-security.md)

**Q:** What does a valid commit signature establish about a person?

**A:** It binds commit content to control of a trusted signing identity/key under a verification policy. It does not independently prove that the author field's human wrote or reviewed the code.

## Recovery and verification cases

Source: [Advanced commands](40.6.05-git-advanced-commands.md), [bundles](40.6.06-patch-and-bundle.md), [scale](40.6.08-git-at-scale-lfs-partial-clones.md), and [signing](40.6.09-signed-commits-repository-security.md).

**Q:** A reflog names a commit whose object is missing. Does creating a branch recover its bytes?

**A:** No. The ref can name history only if the necessary objects exist. Preserve the damaged store and obtain verified missing objects from a complete backup or trusted remote; reflog is not an object backup.

**Q:** Why can an incremental bundle pass verification in its creator but fail on an empty receiver?

**A:** Its prerequisite commits exist in the creator. The empty receiver lacks them. Restore the base bundle first and verify the incremental bundle in the actual receiver.

**Q:** Why did a sparse build pass despite a required package being absent?

**A:** A discovery-only script tested present directories instead of required targets. Decide the job's required targets first and reject an incomplete checkout.

**Q:** Does a signed LFS pointer prove the file bytes can be restored offline?

**A:** No. It binds the content identity/size recorded in Git, but the binary bytes are stored separately. Back up and verify LFS content as well as Git objects and refs.

**Q:** Can a contribution provide its own allowed-signers file for a required signature check?

**A:** That would let the contribution redefine who is trusted. Provision the verification policy through a separate reviewed trust path.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
