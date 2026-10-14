<!-- section: Serverless & Edge | category: Reference | tags: revision, practice | role-priority: important | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Serverless%20%26%20Edge-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-6_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)

# Serverless & Edge — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Serverless Overview

Source: [Serverless Overview](40.7.01-serverless-overview.md)

**Q:** What capacity remains your responsibility in serverless?

**A:** Concurrency quotas, downstream connection/request budgets, cold-start behavior, scaling limits, and cost. Provider-managed servers do not eliminate those constraints.

**Q:** A queue worker writes a resized image, then crashes before acknowledging the message. How do you prevent a retry from creating the wrong or duplicate result?

**A:** Give the input an immutable identity such as object key plus version, include the transform version, and make the output/status operation idempotent or conditional. Let the queue retry, and acknowledge only after durable completion. If the effect is an external API call, reuse a receiver-enforced idempotency key or reconcile its result first.

## AWS Lambda

Source: [AWS Lambda](40.7.02-aws-lambda.md)

**Q:** Why initialize reusable clients outside a Lambda handler?

**A:** A warm execution environment can reuse them, reducing repeated setup. Reuse is opportunistic; reconnect, timeout, and idempotency behavior still need explicit handling.

**Q:** Why can code that is safe under standard Lambda become unsafe on Lambda Managed Instances?

**A:** Managed Instances can run multiple invocations concurrently inside one environment. Mutable globals and shared clients therefore need thread-safety and request-context isolation; the standard one-invocation-per-environment assumption no longer applies.

**Q:** Does Lambda Durable Functions simply raise the timeout for an ordinary handler?

**A:** No. It is a checkpointed workflow model with a separate total execution timeout: completed steps can resume from saved results and waits can release compute. Each invocation still has its own limit, and an event-source mapping can impose a shorter overall ceiling. External side effects still need stable idempotency because a checkpoint cannot atomically commit a remote provider's effect.

**Q:** Why can retrying immediately after a Managed Instances timeout duplicate an effect?

**A:** Lambda reports the invocation failure without forcibly stopping the handler. The original code can continue to commit an effect while the caller retries. Check remaining time, stop at a safe boundary, and use a stable idempotency key or reconcile the authoritative result before retrying.

## Vercel Deployments

Source: [Vercel Deployments](40.7.03-vercel-deployments.md)

**Q:** Why place a managed function near its database rather than only near users?

**A:** Repeated cross-region database round trips can dominate end-to-end latency. Measure the whole dependency path and choose the deployment region accordingly.

**Q:** A preview has its own URL and deployment protection. Is it isolated from production effects?

**A:** Not automatically. The preview can still hold production credentials or call production services. Scope its database, secrets, webhooks, and scheduled work separately; deployment protection controls who can reach the preview, not what systems its code can reach.

**Q:** What should a Vercel cron handler do after missing a scheduled run or receiving the same run twice?

**A:** Reconcile durable work by a stable period or item identity so the next run can catch up safely. Vercel Cron delivery is best effort, may miss or duplicate a trigger, and does not automatically retry a failed invocation. Use a lock for overlapping work and idempotent effects for replay safety. See [Vercel's Cron delivery and recovery guidance](https://vercel.com/docs/cron-jobs/manage-cron-jobs).

**Q:** Does an instant rollback return the system to its previous state?

**A:** It restores an earlier application deployment by changing the production routing target; it does not reverse database migrations, external effects, or current environment-variable changes. Verify schema compatibility and compensate irreversible effects separately. See [Vercel's promotion and rollback behavior](https://vercel.com/docs/deployments/promoting-a-deployment).

## Edge Functions

Source: [Edge Functions](40.7.04-edge-functions.md)

**Q:** Why does running at the edge not guarantee a fixed latency?

**A:** Cache misses, remote data access, network conditions, and compute still contribute. Runtime/API limits and actual dependencies determine the useful latency gain.

**Q:** Why can a single-threaded Durable Object still lose an invariant between an `await` and the next write?

**A:** Awaiting external I/O yields the event loop, allowing another request to interleave before the first resumes. Put the invariant inside a storage transaction or an input gate; if a successful write can be retried after its response is lost, also persist a stable operation identity. See Cloudflare's [Durable Object concurrency guidance](https://developers.cloudflare.com/durable-objects/best-practices/rules-of-durable-objects/).

**Q:** Why is Workers KV a poor authority for immediate session revocation?

**A:** KV is eventually consistent, and both present and missing reads can be cached. Another location may therefore keep accepting an old value after a write. Use an authority with the consistency required by the security decision or define a bounded token lifetime and its risk window. See Cloudflare's [KV consistency model](https://developers.cloudflare.com/kv/concepts/how-kv-works/).

**Q:** When is `ctx.waitUntil()` sufficient, and when should work go to a queue?

**A:** Use it for short, bounded work that can be lost without violating the user's operation, such as analytics. Cloudflare currently cancels HTTP `waitUntil()` work after 30 seconds beyond response completion. Work that must retry or survive runtime failure belongs in a durable queue. See the [Worker context lifecycle](https://developers.cloudflare.com/workers/runtime-apis/context/).

## Serverless Patterns

Source: [Serverless Patterns](40.7.05-serverless-patterns.md)

**Q:** Why persist an idempotency decision with the side effect?

**A:** A crash between the business write and a separate processed flag allows replay to duplicate the effect. Use an atomic transaction or a recoverable operation protocol.

**Q:** In a Standard SQS batch, A succeeds and B fails. What does a partial-batch response save, and what can still repeat?

**A:** With `ReportBatchItemFailures` enabled on the event-source mapping, report B so successfully completed records need not be retried with it. If the invocation crashes before its response is accepted, A may still be delivered again. Make the business effect idempotent using a stable command identity; the SQS message ID identifies a transport record, not the business operation.

**Q:** What failure does a transactional outbox prevent, and why can it still publish twice?

**A:** Writing the business row and the outbox row in one database transaction prevents a committed change from losing its publication intent. A relay can publish, crash before marking the row delivered, and publish again. Consumers still need the same stable business operation identity and idempotent effects. See AWS's [transactional outbox guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html).

**Q:** Why is `FailedEntryCount === 0` not sufficient evidence that EventBridge received an event?

**A:** It reports entry-level publishing errors, but publishing to a nonexistent bus can return status 200 and silently drop the event. Verify the bus and rule/target path, then monitor delivery after the producer call. See AWS's [`PutEvents` behavior](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-putevents.html).

**Q:** When would you choose Step Functions Standard instead of Express, and what does its execution guarantee cover?

**A:** Standard fits long-running, auditable workflows up to one year and executes a task once by default unless a `Retry` is configured. Express runs for up to five minutes; asynchronous execution is at-least-once, while synchronous execution is at-most-once. These workflow contracts do not make a remote provider's side effect atomic with workflow history, so task retries still need idempotency or reconciliation. See AWS's [workflow-type comparison](https://docs.aws.amazon.com/step-functions/latest/dg/choosing-workflow-type.html).

## Serverless Frameworks (SAM, CDK, SST, Serverless Framework)

Source: [Serverless Frameworks (SAM, CDK, SST, Serverless Framework)](40.7.06-serverless-frameworks.md)

**Q:** Why is local emulation insufficient for release verification?

**A:** Provider IAM, event delivery, network paths, quotas, and managed service behavior can differ. Combine fast local tests with targeted deployed integration checks.

**Q:** What does `cdk synth` establish, and what must still be checked before a production deploy?

**A:** It runs the CDK app and emits a CloudFormation cloud assembly, including templates and deployment artifacts. Review the resulting resources and permissions, compare the planned change with the deployed stack, and verify the package and live event path in an isolated environment. Synthesis cannot prove that production IAM, routing, or runtime behavior is correct. See AWS's [CDK deployment lifecycle](https://docs.aws.amazon.com/cdk/v2/guide/deploy.html).

**Q:** Why does a valid SAM template not prove the function can serve its intended HTTP route?

**A:** Validation checks the template shape. The build artifact still needs the expected handler and dependencies, while the deployed stack needs the generated route, invocation permission, and supported runtime. Test a representative event locally, then verify the live route and permissions after deployment. See AWS's [`sam validate` reference](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-validate.html).

**Q:** What must a team check before adopting Serverless Framework v4 for a service?

**A:** Confirm that AWS is the target provider, plan for the CLI's required authentication and applicable license terms, and verify that installed plugins support the selected version. The v4 AWS deployment path packages the service and updates its CloudFormation stack; a v3 configuration or provider claim should not be assumed to carry forward. See the [v4 upgrade guide](https://www.serverless.com/framework/docs/guides/upgrading-v4) and [AWS deployment model](https://www.serverless.com/framework/docs/providers/aws/guide/deploying).

**Q:** What does SST resource linking provide, and what security review remains necessary?

**A:** Linking can make declared resource configuration available to supported application components and add the required permissions. Review the generated scope, isolate development credentials from production data, and verify the provider resources created by the installed SST version. See SST's [resource-linking contract](https://sst.dev/docs/linking/).

## Durable Execution: Temporal & Inngest

Source: [Durable Execution: Temporal & Inngest](40.7.07-durable-execution-temporal-inngest.md)

**Q:** Which code may be replayed in a durable workflow?

**A:** Deterministic workflow logic can replay against recorded history. External effects belong in supported activities/steps and still need idempotency across retries.

**Q:** A payment Activity charged the provider, but the Worker crashed before reporting completion. What should its next attempt do?

**A:** Reuse the same receiver-enforced operation key or query the provider's authoritative result before creating another charge. Durable workflow history cannot atomically commit an external provider effect; a timeout is an uncertain outcome, not proof of failure.

**Q:** Does a timed approval wait mean the order was approved when the wait returns?

**A:** Check whether the condition became true or the timeout expired. A timeout must enter an explicit expiry path. Signals arrive asynchronously, and a status query should report the actual workflow phase rather than infer completion from the presence of approval.

**Q:** Must TypeScript Temporal Workflows move every call to `Date.now()` or `Math.random()` into an Activity?

**A:** No. The TypeScript Workflow sandbox replaces them with replay-safe implementations. External I/O and unsupported APIs remain separate concerns. Apply the rules for the actual SDK, and replay recorded histories against changed code.

## Fly.io Deployment Patterns

Source: [Fly.io Deployment Patterns](40.7.09-flyio-deployment.md)

**Q:** Why should a stateful Fly application not rely on process memory after scaling or deploy?

**A:** Machines are replaceable and requests can reach different instances. Store durable/shared state deliberately and account for per-machine storage placement.

**Q:** Does Fly Proxy autostart create more Machines when all configured Machines are busy?

**A:** It starts existing stopped or suspended Machines. Provisioning additional Machines is a separate capacity action. A minimum running count keeps capacity warm in the primary region, so check other regions and failure recovery separately.

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

## Delivery and version-change cases

Source: [Lambda](40.7.02-aws-lambda.md), [patterns](40.7.05-serverless-patterns.md), [frameworks](40.7.06-serverless-frameworks.md), and [durable execution](40.7.07-durable-execution-temporal-inngest.md).

**Q:** Does a successful EventBridge HTTP request prove every entry was published?

**A:** No. Inspect the failed-entry count and entry errors, retry eligible entries with stable identities, and verify the target/bus configuration and delivery evidence.

**Q:** Why does a FIFO handler stop after the first failed record instead of processing later records anyway?

**A:** Continuing can overtake the failed ordered work. Report the failed and unprocessed records under the mapping's partial-batch contract; their business effects still need safe retry identity.

**Q:** Does current SST synthesize CDK constructs because historical SST used CDK?

**A:** No. Current SST uses Pulumi and provider integration, including bridged Terraform providers. Check the installed version and generated resources rather than mixing generations of APIs.

**Q:** Where is an Inngest SDK v4 trigger declared?

**A:** In the createFunction configuration's triggers field. The handler is the second argument; historical three-argument v3 examples need explicit version labels.

**Q:** If a workflow Activity times out, is it safe to dispatch a second shipment immediately?

**A:** No. Timeout does not prove the first remote effect failed. Use receiver-enforced stable identity or reconcile authoritative shipment state before creating another effect.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
