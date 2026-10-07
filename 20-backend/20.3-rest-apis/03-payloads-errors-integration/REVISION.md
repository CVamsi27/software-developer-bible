<!-- section: REST APIs | category: Reference | tags: revision | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-REST%20APIs-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# REST APIs — Payloads Errors Integration Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## API Pagination

Source: [API Pagination](20.3.3.01-pagination.md)

**Q:** Why must an API bound the size of collection responses?

**A:** Large responses consume server memory, transfer time and client resources. Return a bounded subset and a documented continuation rule; offset and cursor schemes implement different rules.

**Q:** How do offset and cursor pagination behave differently during concurrent changes?

**A:** Offset positions shift as rows are inserted or removed. Keyset cursors avoid positional skipping for a stable indexed order, but mutable sort values and filters can still cause omissions; neither alone guarantees a snapshot.

**Q:** How can a client discover that another page exists without an exact total?

**A:** A next cursor or hasMore flag can indicate another page. Return an exact total only when its cost and consistency behavior serve a product requirement.

**Q:** Three rows share one timestamp and the first page contains only two. What must its continuation contain?

**A:** The timestamp and a unique tie-breaker from the last returned row. Use the same pair in ORDER BY and the continuation predicate; a timestamp-only strict comparison would skip the third row. Preserve the database values without losing timestamp precision or large identifier digits.

**Q:** Does an opaque or signed cursor authorize the next page?

**A:** No. Validate its size, fields, version and query binding, then enforce the caller's current authorization and tenant scope on every page. Encoding obscures data and signing detects tampering; neither grants access.

**Q:** Why reject a limit such as `20junk` rather than passing it to parseInt?

**A:** parseInt accepts a numeric prefix, so malformed input can become a plausible page size. Validate the complete parameter and bound it before querying; distinguish an absent value from an invalid one.

## API Error Handling & Response Design

Source: [API Error Handling & Response Design](20.3.3.02-error-handling-design.md)

**Q:** How do machine-readable error fields and human messages serve different needs?

**A:** Stable codes and structured fields drive client decisions. Human messages explain the failure; keep them safe for their audience and retain sensitive diagnostics in protected logs.

**Q:** Why should errors have stable, documented response shapes?

**A:** A predictable representation supports centralized handling. RFC 9457 defines Problem Details; custom extensions still need stable meanings and documented validation.

**Q:** How should an error contract communicate retryability and diagnostic context?

**A:** Document which conditions can change, whether retry is safe and which delay or limit applies. Include a correlation identifier for support without exposing secrets or internal stack traces.

## Long-Running API Operations (202 Accepted Pattern)

Source: [Long-Running API Operations (202 Accepted Pattern)](20.3.3.03-long-running-api-operations.md)

**Q:** Why can long-running work outlive a synchronous request's timeout budget?

**A:** The expected work may exceed client, proxy or deployment budgets, and a broken connection does not establish that work stopped. No universal duration threshold determines the design.

**Q:** What does separating acceptance from completion change for a client?

**A:** The client receives acceptance plus an operation resource and checks progress later. Persist queued, running and terminal states so acceptance is distinguishable from successful completion.

**Q:** Why does creating a long-running operation need an idempotency policy?

**A:** A response can be lost after creation, causing the client to submit the same work again. Deduplicate creation and define worker recovery through restart or checkpointing according to the task.

## File Upload APIs

Source: [File Upload APIs](20.3.3.04-file-upload-apis.md)

**Q:** When does direct object-storage upload help avoid an application-server bottleneck?

**A:** Large byte transfers can consume application connections and bandwidth for long periods. A signed direct-upload grant moves the byte path to storage while the API retains authorization and publication decisions.

**Q:** Which checks establish that uploaded bytes match the authorized upload?

**A:** Check the authorized object key, size, content rules and checksum where supported, then inspect the stored object before publishing it. Client-supplied metadata alone does not establish content safety.

**Q:** Why should an upload API define explicit size and resource limits?

**A:** Explicit body limits, quotas, deadlines and scanning budgets prevent accidental resource exhaustion. Apply limits to both proxy and direct-upload flows.

## Webhooks

Source: [Webhooks](20.3.3.05-webhooks.md)

**Q:** When can a webhook replace polling for an event outcome?

**A:** The provider calls a receiver when an event occurs, avoiding repeated status reads. The receiver must be reachable and own acknowledgment, authentication and failure handling.

**Q:** Why must a webhook receiver handle repeated deliveries?

**A:** A lost acknowledgment can trigger another delivery; providers can also retry failed attempts. Delivery guarantees vary by provider, so use stable event identity and duplicate-safe handling.

**Q:** How should a webhook receiver verify that a delivery came from its provider?

**A:** Apply the provider's documented signature scheme to the required raw bytes and signed metadata. Validate time or replay conditions when specified, then durably accept work before returning a success acknowledgment.

## Serialization & Wire Formats

Source: [Serialization & Wire Formats](20.3.3.06-serialization-and-wire-formats.md)

**Q:** Why do independently running systems need an agreed byte representation?

**A:** A receiver observes bytes rather than the sender's in-memory types. Both sides need an encoding contract and validation that restores the expected value semantics.

**Q:** How should payload size, encoding cost and inspectability influence a wire-format choice?

**A:** Measure representative payloads and encoding costs alongside tooling, schema evolution and debugging needs. Binary formats are not always smaller or faster for every value distribution.

**Q:** Why do serialized fields need an evolution policy?

**A:** Consumers depend on field names, value meaning, type and nullability. Additions, removals and changed meanings need compatibility rules even without a formal schema file.

## Transactional Email & Notification Delivery

Source: [Transactional Email & Notification Delivery](20.3.3.07-transactional-email-and-notifications.md)

**Q:** Why does provider acceptance not establish recipient delivery?

**A:** Acceptance means an intermediate server accepted responsibility under its contract. Later delivery can fail, and successful mail-server delivery does not establish inbox placement or reading.

**Q:** How should a service handle failures reported after the send request succeeds?

**A:** Process provider delivery and bounce events, correlate them with the notification and update its durable state. Classify permanent failures before retrying and avoid misleading success labels.

**Q:** Where should a notification system enforce retry and deduplication rules?

**A:** Deduplicate by business event at the enqueue/effect boundary and use provider idempotency when available. A new key for each retry defeats deduplication; provider acknowledgment uncertainty still needs an explicit policy.

## Summary

Use these prompts after the reading pass to recall the payloads errors integration mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
