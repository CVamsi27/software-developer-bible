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

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
