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

**Q:** Why does a KafkaJS heartbeat inside a loop not make an arbitrarily slow chunk safe?

**A:** The heartbeat runs only after the chunk yields. A long chunk can exceed the session budget or block JavaScript from sending it. Bound/chunk the work and keep effects idempotent across reassignment.

## Event-Driven Patterns

Source: [Event-Driven Patterns](20.9.03-event-driven-patterns.md).

**Q:** What happens if the consumer advances the source offset after its dead-letter publish fails?

**A:** It loses the only durable record of that failed work. Quarantine must succeed before progress advances; a crash between quarantine and source commit can instead create duplicates that need deduplication.

**Q:** Why is a one-day dedup TTL unsafe when operators may replay a year of archived events?

**A:** Old duplicate identities can arrive after their markers expire. The dedup/effect contract must cover the supported replay horizon or make the effect inherently idempotent.

**Q:** What ordering decision is hidden in moving one entity event to a DLQ and continuing?

**A:** Later entity events can be processed without the failed predecessor. Decide whether that gap is allowed or whether the entity/partition must remain blocked until repaired.

## Next Step

Return to the [reading flow](INDEX.md), then answer an interview question with one concrete failure boundary and one trade-off.

## Summary

Explain the failure boundary before naming the technique. Return to the source chapter when an answer omits the race, recovery path, or durability assumption.

## See Also

- [Stack reading flow](INDEX.md) — return to the mechanism that needs another pass.

## References & Learn More

The source chapters linked above contain the technical references for these review answers.
