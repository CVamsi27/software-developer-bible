<!-- section: Docker | category: Reference | tags: revision, practice -->
[![Section](https://img.shields.io/badge/section-Docker-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

# Docker — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Docker Images & Containers

Source: [Docker Images & Containers](40.1.01-images-containers.md)

**Q:** Why does changing an image not modify an already running container?

**A:** A container was created from a particular image and has its own writable layer; replacing a registry tag does not replace that process or its filesystem.

## Docker Volumes & Networks

Source: [Docker Volumes & Networks](40.1.02-volumes-networks.md)

**Q:** What survives when a container is removed?

**A:** Named volumes survive unless explicitly removed. The container's writable layer does not. Bind mounts refer to host-owned paths and have a separate lifecycle.

## Docker Compose

Source: [Docker Compose](40.1.03-compose.md)

**Q:** Why can a Compose dependency be started while still unusable?

**A:** Startup order is not readiness. A health condition can gate initial startup, but the application must still handle later dependency failure and reconnect.

## Docker Multi-Stage Builds

Source: [Docker Multi-Stage Builds](40.1.04-multi-stage-builds.md)

**Q:** What crosses a multi-stage build boundary?

**A:** Only explicitly copied files and selected image configuration; tools and secrets in earlier stages are not automatically needed in the runtime image.

## Dockerfile Best Practices & Security

Source: [Dockerfile Best Practices & Security](40.1.05-dockerfile-best-practices.md)

**Q:** Why copy the lockfile before application source?

**A:** Dependency installation can reuse its cached layer when only source changes. The lockfile and manifests are inputs to installation, so their changes must invalidate that layer.

## Docker Production Patterns — Security, Optimization, Multi-Stage

Source: [Docker Production Patterns — Security, Optimization, Multi-Stage](40.1.06-production-patterns.md)

**Q:** What must a production container do on SIGTERM?

**A:** Stop accepting new work, drain or safely abandon current work within the orchestrator's grace period, close resources, and exit. Merely setting a health check does not implement shutdown.

## Container Runtime Internals — Namespaces, cgroups, OverlayFS

Source: [Container Runtime Internals — Namespaces, cgroups, OverlayFS](40.1.07-container-runtime-internals-namespaces-cgroups.md)

**Q:** How do namespaces and cgroups answer different questions?

**A:** Namespaces determine the process's view of resources; cgroups account for and limit resource use. Neither alone provides a VM-style separate kernel.

## Image Signing, SBOM & Supply Chain Security

Source: [Image Signing, SBOM & Supply Chain Security](40.1.08-image-signing-sbom-supply-chain.md)

**Q:** Why is a valid image signature insufficient to approve deployment?

**A:** It authenticates a digest under an identity/key policy. Approval also needs expected provenance, source/build identity, contents, and vulnerability policy.

## Rootless Mode & Sandboxed Runtimes (gVisor, Kata)

Source: [Rootless Mode & Sandboxed Runtimes (gVisor, Kata)](40.1.09-rootless-sandboxed-runtimes.md)

**Q:** What does rootless mode leave shared with the host?

**A:** The host kernel. Removing daemon root reduces privilege but does not eliminate kernel vulnerabilities; gVisor and VM-backed runtimes introduce additional isolation with compatibility/cost trade-offs.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
