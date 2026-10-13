<!-- section: CI/CD | category: Reference | tags: revision, practice | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-CI/CD-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

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

**A:** A tag can be reassigned unless the registry prevents it. A digest identifies exact manifest bytes, but a registry may delete those bytes; retain deployed digests for the required rollback window.

## Pipeline Supply-Chain Security & SLSA

Source: [Pipeline Supply-Chain Security & SLSA](40.3.2.04-pipeline-supply-chain-security-slsa.md)

**Q:** What does provenance add beyond a successful vulnerability scan?

**A:** It records how and where an artifact was built and from which source. A scan inspects contents; it does not authenticate the build process.

**Q:** Why must verification enforce an expected identity rather than any valid signature?

**A:** An attacker can sign their own artifact. Policy must bind the signature/provenance to the approved repository, workflow, builder, and digest.

**Q:** Why must a SLSA claim name its track as well as its level?

**A:** The Build and Source tracks describe different controls and have different levels. For example, Build L2 concerns authentic provenance from a hosted builder, while Source L2 concerns preserved change history and source provenance; one does not establish the other.

**Q:** What can a consumer conclude from Build L1 provenance?

**A:** The build generated and distributed provenance, but L1 does not require its authenticity or accuracy. Verify the builder and provenance against the applicable requirements before treating it as trusted evidence.

Source: [Docker build and deploy](40.3.2.01-docker-build-deploy.md)

**Q:** Why can a local image ID not substitute for a registry manifest digest?

**A:** They identify different objects: the local ID names image configuration, while the registry digest names the manifest or multi-platform index consumed by deployment. Record the intended registry reference after publication.

**Q:** Why does a filesystem scan not prove the release image passed an image scan?

**A:** The scan targets differ. Runtime layers and image packages can differ from the checked source tree; bind the scan evidence to the actual candidate image identity.

Source: [Artifact registries and promotion](40.3.2.03-artifact-registries-release-promotion.md)

**Q:** Does an ECR lifecycle rule know which untagged digests workloads still use?

**A:** No. Its selection uses registry metadata. Inventory deployed/recovery references and preview deletion policy before allowing collection.

Source: [Supply-chain security](40.3.2.04-pipeline-supply-chain-security-slsa.md)

**Q:** What remains stealable after migrating CI cloud access to OIDC?

**A:** Identity tokens and temporary cloud credentials can leak and be abused until expiry within their scope. Narrow trust/permissions, safe logging and revocation remain necessary.

Source: [Pipeline patterns](40.3.2.02-pipeline-patterns.md)

**Q:** Why can automatically reverting an image be the wrong response to a failed release?

**A:** The release may have changed data incompatibly or completed external effects. Define recovery from compatibility and authoritative state; rehearse rollback when safe and forward repair when reverting cannot restore a valid state.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
