<!-- section: Message Brokers | category: Reference | tags: revision | role-priority: important | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Message%20Brokers-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-orange)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)

# Message Brokers — Revision

Use these questions after the three concept chapters. Keep the [interview bank](20.9.04-interview-questions.md) for spoken drills after the failure mechanisms are clear.

## Message Brokers

Source: [Message Brokers](20.9.01-message-brokers.md).

**Q:** Why is a publish acknowledgment not proof that a consumer completed its work?

**A:** It acknowledges the broker acceptance/durability contract. Consumer processing and its acknowledgment happen later, across another failure boundary.

**Q:** Which retained history disappears when a keyed Kafka topic is compacted?

**A:** Superseded values for each key may be removed. A rebuild can recover retained current state, while a complete event/audit history needs uncompacted retention or an external archive.

## Kafka Internals & Operations

Source: [Kafka Internals & Operations](20.9.02-kafka-internals-and-operations.md).

**Q:** With replication factor five, ISR size three, and minimum ISR two, how many current ISR copies does `acks=all` wait for?

**A:** The current ISR of three, including the leader. Minimum ISR two is the acceptance floor; it is not a fixed majority or the number waited for.

**Q:** Does an offset distance of 1000 imply a particular end-to-end delay?

**A:** No. It is an offset distance affected by processing/commit rate and log gaps. Measure event-to-effect latency and oldest-unprocessed age alongside lag.

**Q:** Why does a consumer heartbeat inside a loop not make an arbitrarily slow chunk safe?

**A:** The heartbeat runs only after the chunk yields. A long chunk can exceed the session budget or block JavaScript from sending it. Bound/chunk the work and keep effects idempotent across reassignment.

## Event-Driven Patterns

Source: [Event-Driven Patterns](20.9.03-event-driven-patterns.md).

**Q:** What happens if the consumer advances the source offset after its dead-letter publish fails?

**A:** It loses the only durable record of that failed work. Quarantine must succeed before progress advances; a crash between quarantine and source commit can instead create duplicates that need deduplication.

**Q:** Why is a one-day dedup TTL unsafe when operators may replay a year of archived events?

**A:** Old duplicate identities can arrive after their markers expire. The dedup/effect contract must cover the supported replay horizon or make the effect inherently idempotent.

**Q:** What ordering decision is hidden in moving one entity event to a DLQ and continuing?

**A:** Later entity events can be processed without the failed predecessor. Decide whether that gap is allowed or whether the entity/partition must remain blocked until repaired.

## Failure Traces

Sources: [broker model](20.9.01-message-brokers.md), [Kafka operations](20.9.02-kafka-internals-and-operations.md), and [event patterns](20.9.03-event-driven-patterns.md).

**Q:** A provider charged once but the worker crashed before its offset commit. What must the retry reuse?

**A:** The same effect idempotency key, within the provider's supported window. A new key can charge again; an in-memory dedup marker cannot survive the crash.

**Q:** Why can increasing partitions break the order assumed for one customer?

**A:** Hash-based mapping can move that key to a new partition. Older records remain in the original partition, so parallel readers need a migration barrier or entity-version enforcement.

**Q:** What does a committed offset of 115 mean when the log end is 120?

**A:** Recovery starts at 115, giving an offset distance of five. It does not prove five retained records or a particular delay; an invalid/reset position must remain unknown rather than zero.

**Q:** Does upgrading the broker to Kafka 4.3 put every consumer on KIP-848?

**A:** No. A compatible client explicitly selects the consumer protocol. Server heartbeat/session settings then apply, but Java poll-progress limits still matter; check each client's protocol support instead of assuming API compatibility implies KIP-848 support.

**Q:** When should a Kafka Share Group replace a classic consumer group?

**A:** When individual records can be distributed and acknowledged independently, and strict per-partition processing order is unnecessary. A classic group remains the fit for partition ownership, ordered stream processing and offset-based replay.

**Q:** Why can a claim-check event become impossible to replay after its first successful delivery?

**A:** Its referenced object may have been deleted. Blob retention and authorization must cover every independent consumer and the entire supported retry/replay horizon, with corruption/missing-object handling.

**Q:** Does adding an optional field prove every older consumer will accept the event?

**A:** No. Compatibility depends on format, defaults, validation and semantics. A strict unknown-field reader can reject it, and changing a money unit can break meaning without changing the type.

## Next Step

Return to the [reading flow](INDEX.md), then answer an interview question with one concrete failure boundary and one trade-off.

## Summary

Explain the failure boundary before naming the technique. Return to the source chapter when an answer omits the race, recovery path, or durability assumption.

## See Also

- [Stack reading flow](INDEX.md) — return to the mechanism that needs another pass.

## References & Learn More

The source chapters linked above contain the technical references for these review answers.
