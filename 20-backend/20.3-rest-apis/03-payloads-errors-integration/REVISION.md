<!-- section: REST APIs | category: Reference | tags: revision | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-REST%20APIs-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)
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

## Changed-Condition Checks

Source: [Error contracts](20.3.3.02-error-handling-design.md)

**Q:** A database exception includes a password and SQL query. Which fields reach the client?

**A:** A safe generic problem with consistent HTTP status and an opaque occurrence URI. Retain redacted diagnostics in protected records; wrapping the exception's message as a public domain error would break that boundary.

**Q:** A matching creation key is submitted twice after a lost response. Is a 409 always the correct second result?

**A:** No. Recover the original response or operation for the same scoped key and fingerprint. A different request under that key is a conflict. Enforce the key atomically; a pre-insert lookup races.

Source: [Long-running operations](20.3.3.03-long-running-api-operations.md)

**Q:** The operation row committed, but the process stopped before enqueueing. How does accepted work recover?

**A:** Commit a dispatch outbox row in the same transaction and let a recoverable relay publish it. A standalone operation insert followed by a queue call leaves a gap.

**Q:** A client stops polling or requests cancellation while completion commits. What follows?

**A:** Stopping polling does not stop server work. Cancellation is a conditional request; if completion wins, return the current terminal state. Remote effects already completed need a separate compensation policy.

Source: [Uploads](20.3.3.04-file-upload-apis.md)

**Q:** A file passed scanning, then a still-valid upload URL replaced its key. Is serving that key safe?

**A:** The old verdict applies only to the inspected bytes. Bind publication to an immutable version, enforced write-once identity or protected published copy so the served object cannot silently change.

**Q:** Two resumable PATCH requests carry the same offset. Can both append independently?

**A:** No. Compare and update the authoritative offset under serialized ownership or an atomic condition. A stale tus offset returns 409 without modifying the resource; a header alone does not implement recovery.

Source: [Webhooks](20.3.3.05-webhooks.md)

**Q:** An inbox row commits and its acknowledgment is lost. What must the repeated delivery do?

**A:** Verify the delivery, compare its durable identity and payload, acknowledge the existing acceptance and avoid adding new work. The business worker still needs duplicate-safe transitions and separate handling of remote effects.

**Q:** What is wrong with adding a “seen” record before a queue send and returning success immediately?

**A:** A crash can lose the send while suppressing the recovery delivery. Commit inbox and processing intent together, then acknowledge after durable acceptance.

Source: [Wire formats](20.3.3.06-serialization-and-wire-formats.md)

**Q:** A JSON identifier has 9007199254740993 as an unquoted number. Why can a JavaScript consumer receive a different value?

**A:** Its ordinary decoder uses a number representation that rounds that integer. Publish and decode the identifier as a decimal string before precision is lost; JSON grammar itself does not require every language to round it.

**Q:** Does a protobuf rename preserve every contract?

**A:** A retained field number can preserve binary identity, but ProtoJSON names and generated language APIs may break. Reserve removed numbers/names and test the actual old/new consumer paths.

Source: [Notifications](20.3.3.07-transactional-email-and-notifications.md)

**Q:** The provider accepted a receipt, but the response timed out. Does a local sent-at guard prevent the next worker from duplicating it?

**A:** No. Persist ownership and reuse the provider's stable effect key within its documented window, or reconcile the unknown outcome. Local uniqueness cannot atomically include the external send.

**Q:** SPF fails but a valid DKIM signature aligns with the visible From domain. Can DMARC pass?

**A:** Yes. An aligned passing SPF or DKIM path can satisfy DMARC. Its requested policy does not guarantee inbox placement or override every receiver's local policy.

## Summary

Use these prompts after the reading pass to recall the payloads errors integration mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md) — return to prerequisites and learning stages for validated data, errors and integration outcomes

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
