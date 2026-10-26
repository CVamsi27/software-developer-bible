<!-- section: WebSockets | category: Reference | tags: revision, practice | role-priority: important | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-WebSockets-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../../docs/topic-importance.md)

# WebSockets — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Real-Time Architecture

Source: [Real-Time Architecture](60.1.2.01-real-time-architecture.md)

**Q:** Why is Redis Pub/Sub not a durable message history?

**A:** Disconnected subscribers miss publications. Persist replayable events in a suitable log/store and associate an authorized cursor with the client's recovery protocol.

**Q:** How do a transport acknowledgment and a committed mutation differ?

**A:** An acknowledgment can only prove the protocol's declared checkpoint. Tie business acceptance to durable commit/idempotency state if the client relies on that stronger guarantee.

## Scaling WebSockets

Source: [Scaling WebSockets](60.1.2.02-scaling-patterns.md)

**Q:** Why measure capacity by message rate and buffer growth as well as sockets?

**A:** Idle sockets, TLS work, fan-out, slow clients, and queued payloads use very different resources. One universal connections-per-node number hides overload modes.

**Q:** What must graceful drain tell a reconnecting client?

**A:** Stop accepting new work, close/retry under policy, and provide a way to recover durable session/message state. Sticky routing cannot recover memory from a failed node.

**Q:** Why can adding gateways worsen fan-out pressure?

**A:** Each subscription/node can increase broker delivery and duplicate work. Partition channels and measure downstream throughput instead of assuming gateway count is the only bottleneck.

## Commit, Publish and Recover

Source: [Real-Time Architecture](60.1.2.01-real-time-architecture.md)

**Q:** A booking and outbox record commit, then the worker crashes after publishing. Which repetition is possible?

**A:** The worker may publish the same stable event again because its publication checkpoint was not saved. Consumers deduplicate/reconcile under their effect contract; the outbox does not promise exactly-once network delivery.

**Q:** Why can a snapshot fetched before subscribing leave a screen permanently stale?

**A:** A change can occur between the snapshot and active subscription. Coordinate a versioned snapshot/replay boundary or subscribe, buffer and reconcile under an explicit version domain.

**Q:** What goes wrong when every gateway shares one work-consumer group?

**A:** The group distributes an event to one member while interested clients may be on other members. Route onward, align ownership or use independent subscription/checkpoint domains for all interested gateways.

**Q:** Does an audit outbox make current-state tables an event-sourced system?

**A:** No. Event sourcing makes domain event history authoritative for reconstructing state. An outbox can only support reliable publication beside ordinary authoritative tables.

## Fleet and Workload Boundaries

Source: [Scaling WebSockets](60.1.2.02-scaling-patterns.md)

**Q:** Why does the Redis adapter not eliminate polling affinity?

**A:** It forwards Socket.IO room events; it does not share ownership of the Engine.IO polling session. Successive requests still need its owning node.

**Q:** Estimate payload-only egress for 500-byte events at 20 per second to 2,000 clients.

**A:** 500 × 20 × 2,000 is 20,000,000 bytes/second, about 20 decimal MB/second. Framing, TLS, broker traffic and other work add to that figure.

**Q:** What must survive when reconnect reaches a different gateway?

**A:** Verified identity/current permissions, durable business state and the history/snapshot needed by recovery. An old process’s live socket cannot be transferred by changing a registry entry.

**Q:** Why can scale-out fail to help a hot auction?

**A:** One authoritative ordering/price invariant may remain serialized even with more connection gateways. Partitioning must preserve the invariant and define safe ownership transfer.

**Q:** Does an authorized Socket.IO room make a shared Redis adapter channel safe for untrusted publishers?

**A:** No. The adapter trusts its internal Pub/Sub messages. Protect Redis access and command/channel permissions; a publisher to adapter channels can inject traffic outside the client handler's room checks.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
