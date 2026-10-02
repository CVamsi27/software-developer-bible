<!-- section: Git Advanced | category: Reference | tags: revision, practice -->
[![Section](https://img.shields.io/badge/section-Git%20Advanced-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

# Git Advanced — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Git Internals: Objects, Refs & Packfiles

Source: [Git Internals: Objects, Refs & Packfiles](40.6.01-git-internals-objects-refs-packfiles.md)

**Q:** Why does editing a committed file not mutate its existing Git object?

**A:** Objects are content-addressed and immutable; new content creates new objects and a new commit tree. Branch refs move to select history.

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

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
