<!-- section: System Design | category: Reference | tags: revision, retrieval-practice| general-importance: important| general-importance: important | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-System%20Design-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Case Studies — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## URL Shortener System Design

Source: [URL Shortener System Design](30.2.2.01-url-shortener.md)

**Q:** Why must short-code uniqueness be enforced after generation?

**A:** Random generation can collide and concurrent requests can choose the same code. A unique constraint or conditional insertion must reject collisions and retry generation.

## WhatsApp System Design

Source: [WhatsApp System Design](30.2.2.02-whatsapp.md)

**Q:** What should reconnecting chat clients use to discover missed messages?

**A:** A durable conversation sequence or cursor and a synchronization contract. A live WebSocket connection alone does not preserve history across disconnects.

## Uber System Design

Source: [Uber System Design](30.2.2.03-uber.md)

**Q:** Why can driver-location reads be approximate while accepting a ride cannot be?

**A:** Location discovery can tolerate freshness error. Assigning one driver to competing riders requires an atomic claim or equivalent invariant enforcement.

## Netflix System Design

Source: [Netflix System Design](30.2.2.04-netflix.md)

**Q:** Why does a CDN not eliminate the need to plan origin capacity?

**A:** Cold misses, purge storms, unpopular objects and failover still reach the origin. Cache-hit averages can hide burst amplification.

## Google Drive System Design

Source: [Google Drive System Design](30.2.2.05-google-drive.md)

**Q:** What should a file update commit besides uploaded bytes?

**A:** The metadata/version identity that makes those bytes visible. Coordinate partial uploads, retries and garbage collection so a visible version does not point to missing data.

## Payment Gateway System Design

Source: [Payment Gateway System Design](30.2.2.06-payment-gateway.md)

**Q:** What state should a payment timeout produce before another charge is attempted?

**A:** An uncertain outcome that is reconciled by stable provider identity. Repeating the charge with a new key can double-charge after a lost response.

## Notification Service System Design

Source: [Notification Service System Design](30.2.2.07-notification-service.md)

**Q:** Why should notification delivery have a stable per-message identity?

**A:** Retries and provider uncertainty can repeat sends. Carry identity to providers that deduplicate and distinguish accepted, delivered and user-observed states.

## Ticket Booking System Design

Source: [Ticket Booking System Design](30.2.2.08-ticket-booking.md)

**Q:** Why should ticket holds expire conditionally on their current owner/version?

**A:** A late cleanup task for an old hold must not release a renewed or purchased seat. The state transition needs atomic ownership and expiry checks.

## E-Commerce System Design

Source: [E-Commerce System Design](30.2.2.09-e-commerce.md)

**Q:** Why is a shopping cart a different consistency problem from inventory reservation?

**A:** The cart expresses intent and may tolerate stale product data. Reservation or purchase commits scarce inventory under an invariant that concurrent buyers cannot violate.

## Hospital Management System Design

Source: [Hospital Management System Design](30.2.2.10-hospital-management.md)

**Q:** Why must tenant filtering cover exports and workers as well as HTTP reads?

**A:** Those paths access the same sensitive objects outside ordinary request handlers. Restored authorized tenant context and scoped queries must constrain every path.

## Live Betting System Design

Source: [Live Betting System Design](30.2.2.11-live-betting.md)

**Q:** What makes odds versioning essential when accepting a bet?

**A:** The acceptance records the exact offered terms under which the stake was committed. A later price update must not silently change an accepted bet.

## Twitter Feed System Design

Source: [Twitter Feed System Design](30.2.2.12-twitter-feed.md)

**Q:** Why do high-fanout accounts often need a different feed strategy?

**A:** Writing a copy into every follower's feed can dominate cost and latency. A hybrid may read-merge large accounts while precomputing ordinary fanout.

## Rate Limiter System Design

Source: [Rate Limiter System Design](30.2.2.13-rate-limiter.md)

**Q:** Why must a distributed rate limiter define whether it fails open or closed?

**A:** When its shared store is unavailable, that choice trades service access against overload or abuse. The policy depends on the endpoint and its protected resource.

## Web Crawler System Design

Source: [Web Crawler System Design](30.2.2.14-web-crawler.md)

**Q:** Why must a crawler validate destinations again after redirects and DNS resolution?

**A:** A URL may lead to internal or otherwise prohibited addresses through redirects or rebinding. Initial string validation alone does not constrain the final connection.

## Chat System Design

Source: [Chat System Design](30.2.2.15-chat-system.md)

**Q:** How can message ordering differ from server arrival order?

**A:** Concurrent senders, retries and multiple servers race. Define an authoritative conversation sequence and distinguish it from client timestamps and transport order.

## Instagram System Design

Source: [Instagram System Design](30.2.2.16-instagram.md)

**Q:** Why should image variants have versioned object identities?

**A:** Changing bytes under a cached URL can leave stale renditions in the CDN. Versioned references make updates and cache behavior explicit.

## YouTube System Design

Source: [YouTube System Design](30.2.2.17-youtube.md)

**Q:** Why is transcoding modeled as retryable work rather than one synchronous upload call?

**A:** It is expensive, may produce many variants and can fail independently. Persist progress and stable job identities before exposing a playable version.

## Dropbox System Design

Source: [Dropbox System Design](30.2.2.18-dropbox.md)

**Q:** Why does content hashing not resolve concurrent file edits by itself?

**A:** It identifies bytes, not which version should win. The sync protocol still needs versions, conflict detection and a user-visible reconciliation policy.

## Lyft / Ride-Sharing System Design

Source: [Lyft / Ride-Sharing System Design](30.2.2.19-lyft.md)

**Q:** What prevents two dispatch workers from assigning the same driver?

**A:** A shared atomic claim or transactional state transition. Independent local decisions based on location snapshots cannot enforce the assignment invariant.

## Distributed Counter / Metrics Aggregation System Design

Source: [Distributed Counter / Metrics Aggregation System Design](30.2.2.20-distributed-counter.md)

**Q:** Why can a sharded counter be scalable yet unsuitable for a hard inventory cap?

**A:** Summing eventually visible shards gives an approximate or delayed total. Enforcing a strict cap requires coordinated admission or preallocated bounded rights.

## Workflow Engine — System Design Case Study

Source: [Workflow Engine — System Design Case Study](30.2.2.21-workflow-engine.md)

**Q:** What must a workflow engine persist before scheduling a step?

**A:** Its durable execution state and the stable identity of the intended work. Workers may repeat after crashes, so steps need appropriate deduplication or reconciliation.

## Real-Time Collaboration — System Design Case Study

Source: [Real-Time Collaboration — System Design Case Study](30.2.2.22-real-time-collaboration.md)

**Q:** Why does CRDT convergence not automatically preserve a business invariant?

**A:** The merge rules guarantee particular state convergence properties. Invariants such as limited stock or permission enforcement may require additional coordination.

## Typeahead / Autocomplete System Design

Source: [Typeahead / Autocomplete System Design](30.2.2.23-typeahead-autocomplete.md)

**Q:** Why should autocomplete rank candidates after applying access constraints?

**A:** A fast suggestion can still leak private document names or identities. Authorization and tenant boundaries apply to search indexes and caches too.

## Metrics & Monitoring Pipeline System Design

Source: [Metrics & Monitoring Pipeline System Design](30.2.2.24-metrics-monitoring-pipeline.md)

**Q:** Why must a metrics pipeline distinguish event time from ingestion time?

**A:** Late and reordered samples affect windows and alerts differently. Define watermark, lateness and correction policies rather than treating arrival as occurrence.

## Distributed Job Scheduler System Design

Source: [Distributed Job Scheduler System Design](30.2.2.25-distributed-job-scheduler.md)

**Q:** Why does electing one scheduler not guarantee one execution of a job?

**A:** Leases can expire, workers can restart and acknowledgments can be lost. Use stable run identities plus effect-side deduplication or fencing.

## Distributed ID Generator System Design

Source: [Distributed ID Generator System Design](30.2.2.26-distributed-id-generator.md)

**Q:** What should an ID generator do when the clock moves backward?

**A:** Follow an explicit policy such as waiting, a logical clock or refusing generation. Reusing a timestamp/worker/sequence range can violate uniqueness.

## Ad Click Aggregator System Design

Source: [Ad Click Aggregator System Design](30.2.2.27-ad-click-aggregator.md)

**Q:** Why must the click's exact dedup state update even when a Bloom filter says absent?

**A:** If it does not, the next duplicate may find no exact record and be counted again. Commit deduplication and the aggregate effect atomically.

## Parking Lot System Design

Source: [Parking Lot System Design](30.2.2.28-parking-lot.md)

**Q:** What should make releasing a parking space safe to retry?

**A:** A ticket/session identity and conditional transition ensure that repeating an old release cannot free a space currently occupied by a newer session.

## Distributed Cache System Design

Source: [Distributed Cache System Design](30.2.2.29-distributed-cache.md)

**Q:** What can consistent hashing solve without solving cache consistency?

**A:** It limits key remapping as nodes change. It does not supply invalidation, replication ordering, durable storage or protection against hot keys.

## Message Queue System Design

Source: [Message Queue System Design](30.2.2.30-message-queue.md)

**Q:** Why does visibility timeout require consumer deduplication?

**A:** A worker may commit an effect but fail to acknowledge before the timeout. The broker can then deliver the same message again.

## API Gateway System Design

Source: [API Gateway System Design](30.2.2.31-api-gateway.md)

**Q:** Why should an API gateway preserve the caller's end-to-end deadline?

**A:** Independent full timeouts at each hop let work continue after the client gives up. Propagate the remaining budget and cancel where supported.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
