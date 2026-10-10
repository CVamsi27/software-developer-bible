<!-- section: Git Advanced | category: Reference | tags: revision, practice | role-priority: important | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Git%20Advanced-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
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

## Branching Strategies

Source: [Branching Strategies](40.6.02-branching-strategies.md)

**Q:** What should determine a branching strategy?

**A:** Release cadence, integration frequency, support branches, and review/deployment controls. A named strategy cannot resolve those product constraints by itself.

## Rebase & Cherry-Pick

Source: [Rebase & Cherry-Pick](40.6.03-rebase-cherry-pick.md)

**Q:** Why does rebasing change commit identities?

**A:** The rewritten commit's parents or metadata/content change, producing different object IDs. Coordinate before rewriting history others have based work on.

## Git Hooks

Source: [Git Hooks](40.6.04-git-hooks.md)

**Q:** Why are local hooks not a complete policy enforcement mechanism?

**A:** They can be absent or bypassed. Enforce required checks and access policy at the shared integration boundary while using hooks for quick local feedback.

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
