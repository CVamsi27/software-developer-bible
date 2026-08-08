---
section: Git Advanced
category: Reference
tags: [concept, reference, guide]
---

# Git Patch & Bundle

## Definition

**`git format-patch`** and **`git am`** are Git's email-based patch workflow — the way Linux kernel maintainers, OSS maintainers, and many enterprise teams collaborate. A patch is a unified diff with commit metadata; a bundle is a single-file archive of an entire repository's history. Both allow Git changes to be transferred over email, USB drives, or any text channel that Git's HTTP/SSH transport can't reach.

Patches are the lingua franca of OSS contribution. Every Linux kernel commit has gone through `git format-patch` → email → `git am` on the maintainer's side. Understanding this workflow is essential for contributing to large open-source projects.

## Why Do We Need It?

1. **OSS contribution**: Most large projects (Linux kernel, Git itself, QEMU) accept patches via mailing lists
2. **Offline sharing**: Transfer changes via email when VPN/SSH is unavailable
3. **Review without platform**: Some teams review `.patch` files in email clients instead of GitHub/GitLab
4. **Bundle whole history**: `git bundle` creates a single-file repository snapshot for transfer via removable media
5. **Reproducible changes**: Patches are exact, signed, and reviewable in any diff tool

## How It Works

### Patch Flow

```text
CONTRIBUTOR                              MAINTAINER
─────────────                            ──────────
  │                                        │
  │ 1. Make commits on a branch            │
  │                                        │
  │ 2. git format-patch -3 main            │
  │    → Creates 0001-Add-foo.patch        │
  │      0002-Fix-bar.patch                │
  │      0003-Refactor-baz.patch           │
  │                                        │
  │ 3. Send patches via email              │
  │ ─────────────────────────────────────► │
  │                                        │
  │                                        │ 4. git am 0001-*.patch
  │                                        │    git am 0002-*.patch
  │                                        │    git am 0003-*.patch
  │                                        │
  │                                        │ 5. Review, test, push
  │                                        │
```

### Bundle Flow

```text
MACHINE A (no network)                 MACHINE B (no network)
──────────────                         ──────
  │                                       │
  │ 1. git bundle create repo.bundle \    │
  │       --all                           │
  │                                       │
  │ 2. Copy via USB / scp / sneakernet    │
  │ ────────────────────────────────────► │
  │                                       │
  │                                       │ 3. git clone repo.bundle
  │                                       │    git remote add origin ...
  │                                       │    git push origin main
```

## Code Examples

### Creating Patches

```bash
# Create patch for the last 3 commits on current branch (vs main)
git format-patch main -3
# Output: 0001-Add-foo.patch, 0002-Fix-bar.patch, 0003-Refactor-baz.patch

# Create patch for a single commit
git format-patch -1 <sha>

# Create patch for a range
git format-patch <start-sha>..<end-sha>

# Output to a directory
git format-patch main -3 -o ~/patches/

# Include cover letter (commit 0000)
git format-patch main -3 --cover-letter

# With signature (signoff)
git format-patch main -3 --signoff

# With cryptographic signature
git format-patch main -3 --signoff --signature="John Doe <john@example.com>"
```

### Patch File Format

```text
From abc123def456... Mon Sep 17 00:00:00 2024
Subject: [PATCH 1/3] feat: add user authentication

User authentication adds a JWT-based login flow with
refresh tokens. This is the foundation for the
user dashboard feature.

Signed-off-by: Jane Developer <jane@example.com>
---
 src/auth/login.ts        | 45 +++++++++++++++++++++++
 src/auth/jwt.ts          | 78 +++++++++++++++++++++++++++++++++++
 src/auth/middleware.ts   | 23 ++++++++++++
 3 files changed, 146 insertions(+)

diff --git a/src/auth/login.ts b/src/auth/login.ts
new file mode 100644
index 0000000..abc1234
--- /dev/null
+++ b/src/auth/login.ts
@@ -0,0 +1,45 @@
+export async function login(email: string, password: string) {
+  // implementation
+}
```

### Applying Patches

```bash
# Apply a single patch (creates commit)
git am 0001-Add-foo.patch

# Apply multiple patches in order
git am 0001-*.patch 0002-*.patch 0003-*.patch

# Apply patch without committing (use 'apply' instead of 'am')
git apply 0001-Add-foo.patch   # working tree only, no commit

# Apply with 3-way merge (handles conflicts)
git am --3way 0001-Add-foo.patch

# Apply and resolve conflicts
git am 0001-Add-foo.patch
# CONFLICT, resolve in editor
git add <resolved-files>
git am --continue

# Abort if it goes wrong
git am --abort
```

### Creating Bundles

```bash
# Bundle entire repository (all branches)
git bundle create repo.bundle --all

# Bundle specific branches
git bundle create repo.bundle main feature/auth

# Bundle last N commits on a branch
git bundle create recent.bundle main --not main~10

# Verify a bundle
git bundle verify repo.bundle

# Clone from a bundle
git clone repo.bundle cloned-repo

# Add bundle as a remote and fetch
git remote add bundle-repo repo.bundle
git fetch bundle-repo
```

### Signed Patches (for Linux Kernel style)

```bash
# Generate GPG-signed patch
git format-patch -1 --signoff <sha>

# Apply and verify signature
git am --verify-signature 0001-*.patch

# Maintainer requires PGP-signed patches
git config format.signature true
git config user.signingkey <gpg-key-id>
```

## Real-World Use Cases

### 1. Contributing to Linux Kernel

```bash
# Develop on your fork's branch
git checkout -b driver/v2

# Make commits, sign off
git commit -s -m "drivers: net: add support for new device"

# Generate patch series
git format-patch main -3 --cover-letter -o ~/patches/

# Send via git send-email (uses SMTP)
git send-email --to="netdev@vger.kernel.org" \
  --cc="maintainer@example.com" \
  ~/patches/0000-*.patch
```

### 2. Offline Repository Transfer (Air-Gapped Networks)

```bash
# Create a bundle of the whole repo
git bundle create full-history.bundle --all

# Transfer via USB / sneakernet
# On target machine:
git clone full-history.bundle my-clone
cd my-clone
git remote set-url origin git@internal-git:repo.git
git push --mirror origin
```

### 3. Code Review via Email (Some Enterprise Teams)

```text
1. Developer makes commits
2. git format-patch main -3 > review.patch
3. Email patch to team lead
4. Team lead reviews in email client
5. git am review.patch on integration branch
```

### 4. Backporting a Fix via Patch

```bash
# On newer branch, create the fix
git checkout feature/new-api
git commit -m "fix: handle null user in getProfile"

# Generate patch and apply to old release branch
git format-patch -1 HEAD -o /tmp/fix.patch
git checkout release/v1.x
git am /tmp/fix.patch
```

## Common Mistakes

### 1. Forgetting `--signoff` for Kernel-Style Projects

Many projects (Linux kernel, Git itself) require `Signed-off-by` lines. Use `-s` or `--signoff`:

```bash
git format-patch -3 -s
```

### 2. Sending Out-of-Order Patches

```bash
# ❌ Bad: send 0001 and 0003, forget 0002
git am 0001-*.patch 0003-*.patch
# error: 0003 depends on 0002, can't apply

# ✅ Good: keep all patches in one directory, send in order
```

### 3. Patches with Merge Commits

```text
❌ Bad: format-patch from a merged branch (creates confusing history)
✅ Good: rebase before format-patch for a clean series
```

```bash
# Rebase before sending
git rebase -i main
git format-patch main -3
```

### 4. Editing Patches Manually

```text
❌ Bad: opening patch in editor, breaking headers
✅ Good: use git rebase -i to fix, then regenerate patches
```

## Best Practices

1. **Sign off patches** (`-s`) for projects that require `Signed-off-by`
2. **Use cover letters** (`--cover-letter`) for series of 3+ patches
3. **Rebase before format-patch** for a clean series
4. **Test patches apply cleanly** before sending (clone into a fresh dir and `git am`)
5. **Use `git send-email`** for SMTP delivery to mailing lists
6. **Add a `---` divider** in commit message for review notes (excluded from log)
7. **Keep patches focused** — one logical change per commit
8. **Use `--subject-prefix="PATCH v2"`** for revisions of previously sent series
9. **Bundle entire history with `--all`** when transferring a full repo offline
10. **Verify bundles** with `git bundle verify` before relying on them

## Patch Conventions for Mailing Lists

```text
Subject: [PATCH v2 1/5] component: short summary
        ↓                       ↓
   [tag]                  [seq/total]  [scope: area]

Body:
  - What changed
  - Why
  - How tested

  Signed-off-by: Name <email>
  ---
  v2: address feedback from previous review
      - fixed off-by-one in edge case
      - added test for ...
```

## Performance Considerations

| Operation | Size | Time |
|-----------|------|------|
| format-patch of 1 commit | 1-10 KB | < 1s |
| format-patch of 100 commits | 1-5 MB | < 5s |
| bundle of 1000-commit repo | 5-50 MB | 5-30s |
| bundle of 100K-commit repo | 100-500 MB | 1-5 min |
| am of 1 patch | — | < 1s |
| am of 100 patches with conflicts | — | 5-30 min |

## Summary

- `git format-patch` creates email-ready patches with commit metadata
- `git am` applies patches and creates commits
- `git bundle` creates single-file repository snapshots
- Patches are the lingua franca of OSS contribution (Linux kernel style)
- Always sign off (`-s`) for projects that require it
- Use cover letters for series of 3+ patches
- Use bundles for offline repo transfer

---

## Cheat Sheet
```text
GIT PATCH & BUNDLE CHEAT SHEET
============================================================

FORMAT PATCH:
  git format-patch main -3              # last 3 commits
  git format-patch -1 <sha>             # single commit
  git format-patch <start>..<end>       # range
  git format-patch main -3 -o ~/patches/ # output dir
  git format-patch -3 --cover-letter     # 0000-cover.patch
  git format-patch -3 -s                 # signoff

APPLY PATCH:
  git am 0001-*.patch                   # commit
  git apply 0001-*.patch                # working tree only
  git am --3way 0001-*.patch            # merge if conflict
  git am --continue                     # after conflict resolution
  git am --abort                        # bail

BUNDLE:
  git bundle create repo.bundle --all   # full history
  git bundle create recent.bundle main --not main~10
  git bundle verify repo.bundle        # check valid
  git clone repo.bundle cloned-repo     # restore

SEND EMAIL:
  git send-email --to="ml@example.org" \
    --cc="reviewer@example.com" \
    ~/patches/0000-*.patch

CONVENTIONS:
  Subject: [PATCH v2 1/5] component: summary
  Body: what, why, how tested
  Signed-off-by: Name <email>

INTERVIEW TIPS:
  • Explain the Linux kernel contribution workflow
  • Discuss when to use format-patch vs git push + PR
  • Show how to maintain a patch series through revisions
```
---

## See Also
- [Branching Strategies](01-Branching-Strategies.md)
- [CI/CD](../15-CI-CD/)
- [Git Advanced Commands](04-Git-Advanced-Commands.md)
- [Monorepo](../28-Monorepo/)
- [Rebase & Cherry-Pick](02-Rebase-Cherry-Pick.md)

## References & Learn More

- [git-format-patch Documentation](https://git-scm.com/docs/git-format-patch)
- [git-am Documentation](https://git-scm.com/docs/git-am)
- [git-bundle Documentation](https://git-scm.com/docs/git-bundle)
- [Linux Kernel Submitting Patches](https://www.kernel.org/doc/html/latest/process/submitting-patches.html)
- [git send-email](https://git-scm.com/docs/git-send-email)
- [Signed-off-by Line (DCO)](https://developercertificate.org/)
