<!-- section: Git Advanced | category: Reference | tags: revision, practice | role-priority: important | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Git%20Advanced-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)
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

## Git Patch & Bundle

Source: [Git Patch & Bundle](40.6.06-patch-and-bundle.md)

**Q:** How do a patch and a bundle transfer different information?

**A:** A patch describes changes, often replayed onto existing history. A bundle can carry Git objects and refs with prerequisites, enabling offline repository/history transfer.

## Git Code Archaeology

Source: [Git Code Archaeology](40.6.07-code-archaeology.md)

**Q:** Why should blame be followed by the introducing commit and its context?

**A:** The last line edit may be formatting or refactoring. The relevant change's diff, message, surrounding code, and tests explain intent better than author attribution alone.

## Git at Scale: LFS & Partial Clones

Source: [Git at Scale: LFS & Partial Clones](40.6.08-git-at-scale-lfs-partial-clones.md)

**Q:** What do partial clone and sparse checkout reduce separately?

**A:** Partial clone can omit objects until needed; sparse checkout limits checked-out paths. A small working tree does not by itself shrink downloaded history.

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
