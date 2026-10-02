<!-- section: Serverless & Edge | category: Reference | tags: revision, practice -->
[![Section](https://img.shields.io/badge/section-Serverless%20%26%20Edge-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

# Serverless & Edge — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Serverless Overview

Source: [Serverless Overview](40.7.01-serverless-overview.md)

**Q:** What capacity remains your responsibility in serverless?

**A:** Concurrency quotas, downstream connection/request budgets, cold-start behavior, scaling limits, and cost. Provider-managed servers do not eliminate those constraints.

## AWS Lambda

Source: [AWS Lambda](40.7.02-aws-lambda.md)

**Q:** Why initialize reusable clients outside a Lambda handler?

**A:** A warm execution environment can reuse them, reducing repeated setup. Reuse is opportunistic; reconnect, timeout, and idempotency behavior still need explicit handling.

## Vercel Deployments

Source: [Vercel Deployments](40.7.03-vercel-deployments.md)

**Q:** Why place a managed function near its database rather than only near users?

**A:** Repeated cross-region database round trips can dominate end-to-end latency. Measure the whole dependency path and choose the deployment region accordingly.

## Edge Functions

Source: [Edge Functions](40.7.04-edge-functions.md)

**Q:** Why does running at the edge not guarantee a fixed latency?

**A:** Cache misses, remote data access, network conditions, and compute still contribute. Runtime/API limits and actual dependencies determine the useful latency gain.

## Serverless Patterns

Source: [Serverless Patterns](40.7.05-serverless-patterns.md)

**Q:** Why persist an idempotency decision with the side effect?

**A:** A crash between the business write and a separate processed flag allows replay to duplicate the effect. Use an atomic transaction or a recoverable operation protocol.

## Serverless Frameworks (SAM, CDK, SST, Serverless Framework)

Source: [Serverless Frameworks (SAM, CDK, SST, Serverless Framework)](40.7.06-serverless-frameworks.md)

**Q:** Why is local emulation insufficient for release verification?

**A:** Provider IAM, event delivery, network paths, quotas, and managed service behavior can differ. Combine fast local tests with targeted deployed integration checks.

## Durable Execution: Temporal & Inngest

Source: [Durable Execution: Temporal & Inngest](40.7.07-durable-execution-temporal-inngest.md)

**Q:** Which code may be replayed in a durable workflow?

**A:** Deterministic workflow logic can replay against recorded history. External effects belong in supported activities/steps and still need idempotency across retries.

## Fly.io Deployment Patterns

Source: [Fly.io Deployment Patterns](40.7.09-flyio-deployment.md)

**Q:** Why should a stateful Fly application not rely on process memory after scaling or deploy?

**A:** Machines are replaceable and requests can reach different instances. Store durable/shared state deliberately and account for per-machine storage placement.

## Vite SPA on Cloudflare Workers

Source: [Vite SPA on Cloudflare Workers](40.7.10-vite-spa-cloudflare-workers.md)

**Q:** Why must an API proxy request run before a SPA fallback?

**A:** Otherwise an unmatched API request can receive index.html and appear to succeed with the wrong content. Route API paths explicitly and reserve HTML fallback for navigation.

**Q:** Which Worker bundle measurement should be compared with the current platform limit?

**A:** As verified on 2026-10-02, compare uncompressed Total Upload with the 64 MiB limit for either plan. The gzip number is informational; static asset limits and browser bundle budgets are separate.

**Q:** Why can a same-origin API proxy still have an authentication or CSRF defect?

**A:** It changes the browser's request origin path but does not enforce backend identity, tenant authorization, cookie scope, Origin policy or CSRF defenses. Those contracts still need explicit implementation and tests.

**Q:** Why might middleware in the Worker never protect the static application shell?

**A:** Asset-first requests can bypass the script. Protect the relevant asset paths through the intended access/routing policy and test deployed responses; backend data authorization remains its own boundary.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
