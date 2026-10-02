<!-- section: CI/CD | category: Reference | tags: revision, practice -->
[![Section](https://img.shields.io/badge/section-CI/CD-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

# CI/CD — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Docker Build & Deploy Pipeline

Source: [Docker Build & Deploy Pipeline](40.3.2.01-docker-build-deploy.md)

**Q:** Why build an image once and promote its digest?

**A:** Rebuilding per environment can change dependencies or toolchain output. Promotion deploys the same tested bytes while environment-specific configuration remains separate.

## CI/CD Pipeline Patterns — GitHub Actions, GitLab CI, Deployment Strategies

Source: [CI/CD Pipeline Patterns — GitHub Actions, GitLab CI, Deployment Strategies](40.3.2.02-pipeline-patterns.md)

**Q:** What should a cache miss change about pipeline correctness?

**A:** Only speed. A pipeline that cannot build cleanly without cache depends on hidden state and is not reproducible.

## Artifact Registries & Release Promotion

Source: [Artifact Registries & Release Promotion](40.3.2.03-artifact-registries-release-promotion.md)

**Q:** What distinguishes an artifact tag from a digest?

**A:** A tag can be moved; a digest identifies immutable content. Release promotion and rollback evidence should record the tested digest.

## Pipeline Supply-Chain Security & SLSA

Source: [Pipeline Supply-Chain Security & SLSA](40.3.2.04-pipeline-supply-chain-security-slsa.md)

**Q:** What does provenance add beyond a successful vulnerability scan?

**A:** It records how and where an artifact was built and from which source. A scan inspects contents; it does not authenticate the build process.

**Q:** Why must verification enforce an expected identity rather than any valid signature?

**A:** An attacker can sign their own artifact. Policy must bind the signature/provenance to the approved repository, workflow, builder, and digest.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
