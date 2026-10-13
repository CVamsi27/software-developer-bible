<!-- section: System Design | category: Reference | tags: revision, retrieval-practice | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-System%20Design-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-15_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Case Studies — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## URL Shortener System Design

Source: [URL Shortener System Design](30.2.2.01-url-shortener.md)

**Q:** Why must short-code uniqueness be enforced after generation?

**A:** Random generation can collide and concurrent requests can choose the same code. A unique constraint or conditional insertion must reject collisions and retry generation.

**Q:** What if two custom-alias requests both pass an existence check?

**A:** The authoritative unique insertion admits one. The other returns a conflict or retries under policy; a lost successful response needs stable request identity, not a new alias allocation.

**Q:** Why can a CDN purge fail to enforce immediate link revocation?

**A:** A browser may already have cached the redirect and never contact the service or CDN again. The redirect's cache lifetime must fit the revocation promise, or the product must accept that a previously cached destination can remain reachable.

**Q:** What does a unique constraint guarantee for randomly generated codes, and what does it not guarantee?

**A:** It prevents two committed mappings from owning the same code and gives the creator a collision signal to retry. It does not make collisions improbable; code-space size and randomness determine collision risk, while the constraint preserves correctness.

## WhatsApp System Design

Source: [WhatsApp System Design](30.2.2.02-whatsapp.md)

**Q:** What should reconnecting chat clients use to discover missed messages?

**A:** A durable conversation sequence or cursor and a synchronization contract. A live WebSocket connection alone does not preserve history across disconnects.

**Q:** What does the sender know when the server acknowledges a message commit?

**A:** Only that the service durably accepted that message identity. A later device receipt is evidence that a recipient device stored it; a read marker is a separate client action. A socket write alone proves neither.

**Q:** Why can a database row with one `ciphertext` field be only a teaching model for encrypted multi-device delivery?

**A:** A protocol may encrypt one group payload and distribute different key envelopes to authorized devices, or store other protocol-specific state. The schema's opaque field illustrates durable message identity, not the protocol's device-key, envelope or group-epoch model.

**Q:** What does a membership-removal transaction guarantee, and what can it not undo?

**A:** It can define the authorization boundary for later accepted messages and prevent future key material from reaching the removed member under the chosen protocol. It cannot retract ciphertext or plaintext already delivered and stored on that member's device.

## Uber System Design

Source: [Uber System Design](30.2.2.03-uber.md)

**Q:** Why can driver-location reads be approximate while accepting a ride cannot be?

**A:** Location discovery can tolerate freshness error. Assigning one driver to competing riders requires an atomic claim or equivalent invariant enforcement.

**Q:** Why must a location report include a session generation and increasing sequence?

**A:** An old connection can deliver a delayed report or disconnect after a newer session has taken ownership. Rejecting stale generations and out-of-order sequence numbers within a generation prevents old state from replacing the driver's current position or availability.

**Q:** Why does the nearest geo-index result not prove the fastest pickup?

**A:** A geo index ranks or filters by straight-line distance. Road barriers, traffic, eligibility and stale positions can change the useful ranking, so route estimates should be bounded and final assignment must recheck authoritative state.

**Q:** What does `ST_DWithin` provide when a spatial index is available, and what does it not decide?

**A:** It can filter rows within a radius using an applicable spatial index. It does not estimate road travel time, prove a driver's availability, or atomically reserve that driver for a ride.

## Netflix System Design

Source: [Netflix System Design](30.2.2.04-netflix.md)

**Q:** Why does a CDN not eliminate the need to plan origin capacity?

**A:** Cold misses, purge storms, unpopular objects and failover still reach the origin. Cache-hit averages can hide burst amplification.

## Google Drive System Design

Source: [Google Drive System Design](30.2.2.05-google-drive.md)

**Q:** Why is a completed object upload not the point at which a new file version becomes visible?

**A:** Upload completion proves only that storage received an object. The service must still verify it, recheck permission, expected version and quota, then atomically publish the version pointer and change record. A failed publication stays invisible and can be retried or safely reclaimed.

## Payment Gateway System Design

Source: [Payment Gateway System Design](30.2.2.06-payment-gateway.md)

**Q:** What state should a payment timeout produce before another charge is attempted?

**A:** Keep the command unknown and reconcile it through the same provider identity. Provider idempotency can have a shorter retention window than the gateway's command record; after that window, resolve the original outcome before sending a new attempt or changing providers.

**Q:** What should happen when a caller reuses an idempotency key with a different request fingerprint?

**A:** Return a conflict and preserve the original command. The key identifies one intended operation; interpreting it again with a different amount, target or token can produce a charge the caller did not intend.

## Notification Service System Design

Source: [Notification Service System Design](30.2.2.07-notification-service.md)

**Q:** Why should notification delivery have a stable per-message identity?

**A:** Retries and provider uncertainty can repeat sends. Carry identity to providers that deduplicate and distinguish accepted, delivered and user-observed states. A repeated producer event with changed meaning must conflict rather than silently reuse its old intent.

**Q:** Does a final consent check guarantee that no notification is sent after an opt-out?

**A:** No. The external request can race with the opt-out after the service authorizes dispatch. Define the cutoff, stop unsent retries and use cancellation only where the provider supports it; do not promise recall of an accepted message.

**Q:** Why store an IANA timezone for quiet hours instead of a UTC offset?

**A:** Offsets can change with daylight-saving rules and legislation. An IANA zone lets the scheduler apply date-specific transitions, but skipped and repeated local times still need an explicit delivery policy.

## Ticket Booking System Design

Source: [Ticket Booking System Design](30.2.2.08-ticket-booking.md)

**Q:** Why should ticket holds expire conditionally on their current owner/version?

**A:** A late cleanup task must release a seat only if it is still held by that exact hold and its authoritative deadline has passed. Event scope and the copied seat deadline must match the hold record; renewal updates both under the same transaction so stale cleanup cannot release a newer owner.

## E-Commerce System Design

Source: [E-Commerce System Design](30.2.2.09-e-commerce.md)

**Q:** Why is a shopping cart a different consistency problem from inventory reservation?

**A:** The cart expresses mutable intent and can tolerate stale availability. A reservation conditionally decrements authoritative stock and records a stable order/SKU identity; a retry returns that outcome, while a competing buyer cannot allocate the same final unit.

## Hospital Management System Design

Source: [Hospital Management System Design](30.2.2.10-hospital-management.md)

**Q:** Why must tenant filtering cover exports and workers as well as HTTP reads?

**A:** Those paths access the same sensitive objects outside ordinary request handlers. Restored authorized tenant context and scoped queries must constrain every path.

**Q:** What does the appointment exclusion constraint guarantee, and what does it not guarantee?

**A:** It serializes conflicting active intervals for the resource keys and policy encoded in the constraint, even when two requests race. It does not establish staff eligibility, patient-care authorization, schedule hours, or retry identity; validate those separately.

**Q:** How should a booking endpoint handle the same idempotency key arriving concurrently?

**A:** Claim a tenant- and actor-scoped key inside the booking transaction, bind it to a canonical request fingerprint, and commit its appointment ID with the appointment and outbox row. A matching retry returns that appointment after authorization is checked again; a different fingerprint conflicts.

**Q:** Why must the scheduling zone be stored separately from a PostgreSQL `timestamptz`?

**A:** `timestamptz` preserves the instant, not the original zone or offset. The facility's IANA zone supplies local calendar rules; an explicit offset resolves a repeated daylight-saving time, while nonexistent local times must be rejected.

**Q:** Why keep the partner's FHIR or HL7 representation at an adapter boundary?

**A:** A wire standard defines an exchange contract, not the application's entire persistence model. A versioned adapter can translate partner profiles, identifiers, terminology, acknowledgments, and corrections without making external message shape the authority for internal workflow state.

**Q:** Why is a FHIR `Appointment` not evidence that a clinical encounter happened?

**A:** Appointment represents a planned booking; the visit and clinical documentation follow a separate lifecycle. Treating a scheduled resource as completed care can create false clinical and billing state.

## Live Betting System Design

Source: [Live Betting System Design](30.2.2.11-live-betting.md)

**Q:** What makes odds versioning essential when accepting a bet?

**A:** The acceptance records the exact offered terms under which the stake was committed. A later price update must not silently change an accepted bet.

**Q:** Why does the baseline keep the market version, wallet debit, wager and journal in one transactional authority?

**A:** The service must not accept a price while failing the debit, or debit funds without a durable wager. Local database commits cannot make two service-owned databases atomic; a split design needs explicit reservations, expiry, compensation and recovery.

**Q:** How does the service distinguish a retried wager from a second intentional wager with identical terms?

**A:** A durable command ID identifies one user operation, while a canonical fingerprint detects changed terms under that ID. Two intentional bets use different command IDs even when account, selection and stake match.

**Q:** Why is the cash-out calculation based on accepted return divided by current odds?

**A:** Decimal odds encode the potential total return. Dividing that return by the new odds raises the idealized value when the chance of winning rises; a real offer then applies margin, exposure, fees and limits.

**Q:** How should an operator represent a corrected final result after settlement?

**A:** Preserve the original posting and add an auditable reversal or adjustment linked to it. Editing history or replaying the original payout can hide the reason for the balance change or pay twice.

## Twitter Feed System Design

Source: [Twitter Feed System Design](30.2.2.12-twitter-feed.md)

**Q:** Why do high-fanout accounts often need a different feed strategy?

**A:** Writing a copy into every follower's feed can dominate cost and latency. A hybrid may read-merge large accounts while precomputing ordinary fanout.

**Q:** Why is a cached feed candidate not proof that the reader may see its post?

**A:** Blocking, unfollowing, protected-account changes, moderation and deletion can invalidate a copied pointer. Hydration must check current visibility before returning post text or media.

**Q:** What does a chronological cursor need when two posts share a timestamp?

**A:** The complete ordering tuple, such as `(created_at, post_id)`, is required for both sorting and the next-page predicate. A timestamp-only cursor can skip or repeat posts tied at the boundary.

**Q:** Why does a push-to-pull migration need a watermark and temporary dual reads?

**A:** Some posts may already be copied while others are still served from author history. A transition watermark and deduplication let readers consult both paths without losing or duplicating posts during the change.

**Q:** How does a deletion tombstone stop a delayed create event from restoring a post?

**A:** Derived consumers compare monotonic object versions and retain the delete version. A stale create with an earlier version is discarded instead of replacing the tombstone.

**Q:** Why is lifetime hashtag volume a poor definition of a trend?

**A:** It rewards old popularity instead of recent acceleration. A trend needs a defined time window or decay model, event-time lateness handling, deduplication and abuse controls.

## Rate Limiter System Design

Source: [Rate Limiter System Design](30.2.2.13-rate-limiter.md)

**Q:** Why must a distributed rate limiter define whether it fails open or closed?

**A:** When its shared store is unavailable, that choice trades service access against overload or abuse. The policy depends on the endpoint and its protected resource.

**Q:** How can a quota of two be exceeded when the stored count is one?

**A:** Two separate readers can both see one, both admit, and increment to three. The check and update must be one atomic admission operation.

**Q:** Why might a service need a concurrency limit in addition to a rate limit?

**A:** A rate limit bounds arrivals over time, but slow requests can keep all workers busy and exhaust connections. A concurrency limit caps in-flight work; a queue or bounded admission policy then controls what happens when those slots are occupied.

**Q:** What can go wrong when account and endpoint quotas are checked in separate atomic operations?

**A:** The first quota may be consumed before the second rejects the request. Decide whether partial consumption is intentional; if the policy requires one all-or-none decision, the keys need a shared transactional boundary or a different model.

**Q:** When is `Retry-After` useful in a 429 response?

**A:** It is useful when the limiter can give a defensible retry delay. A policy reset timestamp and a delay are different values, so return the header only with the meaning and units the API contract promises.

## Web Crawler System Design

Source: [Web Crawler System Design](30.2.2.14-web-crawler.md)

**Q:** Why must a crawler validate destinations again after redirects and DNS resolution?

**A:** A URL may lead to internal or otherwise prohibited addresses through redirects or rebinding. Initial string validation alone does not constrain the final connection.

**Q:** Why keep URL identity, response-body deduplication and revisit scheduling as separate records or decisions?

**A:** Distinct URLs can return equal bytes, and one URL can return new bytes later. Shared body storage may save space, but each URL still needs its own provenance, outgoing-link coverage and next-visit policy.

**Q:** Why does a positive Bloom-filter result need exact confirmation before a crawler skips a URL?

**A:** A Bloom filter can report a false positive, meaning an unseen URL may look present. Confirming against exact storage avoids silently losing coverage; skipping on the approximate result is an explicit recall trade-off.

**Q:** What does a lease generation protect when a URL claim expires and is reassigned?

**A:** The old worker may finish after a new worker owns the URL. A monotonically increasing generation fences that stale completion so it cannot overwrite the newer claim's result.

**Q:** Why normalize a trailing DNS dot while preserving path and query distinctions?

**A:** `example.com.` and `example.com` name the same DNS host and should share politeness state. Paths and query components can identify different resources, so removing their meaningful differences can collapse distinct crawl targets.

## Chat System Design

Source: [Chat System Design](30.2.2.15-chat-system.md)

**Q:** How can message ordering differ from server arrival order?

**A:** Concurrent senders, retries and multiple servers race. Define an authoritative conversation sequence and distinguish it from client timestamps and transport order.

**Q:** How does a conversation-local sequence avoid an off-by-one or duplicate allocation?

**A:** Define the stored counter as the next unallocated value, reserve it under the conversation row lock, and commit that value with the message and outbox row. A failed transaction rolls back the reservation; a retry returns the existing sequence.

**Q:** Why should a chat receipt name the device and the level of evidence it represents?

**A:** One device receiving a message does not prove that all of a user's devices received it, and receipt does not prove a human read or understood it. Define whether a badge means one eligible device, all devices or a separate read event.

**Q:** Why does reconnect need a change cursor in addition to a message sequence cursor?

**A:** Edits, deletions and reactions can change messages whose original sequence is already below the device cursor. A retained change stream or versioned delta cursor lets the device recover those updates or request a fresh snapshot when retention has expired.

**Q:** What must happen when a caller retries an accepted command after its message body has expired?

**A:** Keep the operation ID and payload fingerprint for the supported retry period, even if the body is gone. A tombstone or separate command ledger can return the original acceptance and prevent a late retry from creating a second message.

**Q:** Why do an outbox and device deduplication solve different delivery failures?

**A:** The outbox prevents a committed message from losing its delivery intent; device deduplication makes redelivery safe when a worker crashes after sending but before recording a receipt. Both are required for recoverable at-least-once delivery.

## Instagram System Design

Source: [Instagram System Design](30.2.2.16-instagram.md)

**Q:** Why should image variants have versioned object identities?

**A:** Changing bytes under a cached URL can leave stale renditions in the CDN. Versioned references make updates and cache behavior explicit.

**Q:** Why does media upload finish before a post becomes visible?

**A:** The upload transfer proves only that bytes arrived. The service still has to verify the owner, object, size and checksum, then decode and generate safe renditions. Publishing a post after those steps prevents a feed from exposing missing or unvalidated media.

**Q:** Why pair a processing lease with a generation number?

**A:** The lease lets another worker recover after a crash. Recovery increments the generation, so the old worker's conditional publish affects no row even if it later finishes. A timeout alone is not a fence against stale work.

**Q:** What makes retrying post creation safe after a client timeout?

**A:** Scope an idempotency key to the owner and compare a canonical request fingerprint. The same request returns its original post; changed input under that key is a conflict. Commit the ready-upload consumption, post and outbox event together so a retry cannot create another post or lose the event.

**Q:** Why are unique likes canonical while displayed like counts may be approximate?

**A:** A unique `(user_id, post_id)` record decides whether the user liked the post and makes retries harmless. Counts are projections for fast display; consumers must deduplicate stable events or rebuild the projection so redelivery does not inflate totals.

**Q:** Why recheck visibility after reading IDs from a feed cache?

**A:** The cache is a candidate list, not an authorization grant. A user may have blocked the author, lost follower access, or encountered a deleted or expired post after the list was built. Hydration and media delivery must enforce current policy.

**Q:** What does a short-lived signed media URL guarantee, and what does it not guarantee?

**A:** It grants whoever holds it access until its expiry. Short lifetimes bound the delay before revocation takes effect; an already issued URL is not immediately revoked just because the post metadata changed.

**Q:** When should feed generation push posts to followers and when should it merge at read time?

**A:** Push works when the active follower fan-out is affordable and gives readers a prepared candidate list. Pull avoids enormous write amplification for high-fan-out authors but adds read work. Choose the boundary from measured active-follower cost and read latency, then bound and rank the merged candidates.

**Q:** How does the design enforce a 24-hour story lifetime if cleanup is delayed?

**A:** Reads reject a story once `expires_at` has passed; cleanup only reclaims storage. Cache hits, search results and signed media delivery must follow the same expiry decision, or a stale copy can outlive the record's intended visibility.

## YouTube System Design

Source: [YouTube System Design](30.2.2.17-youtube.md)

**Q:** Why is transcoding modeled as retryable work rather than one synchronous upload call?

**A:** It is expensive, may produce many variants and can fail independently. Persist progress and stable job identities before exposing a playable version.

**Q:** Why must a version-one transcoder not publish ready after a replacement upload?

**A:** Its outputs belong to a superseded source version. Publication checks the current source/processing version and only exposes a complete validated manifest for that version.

**Q:** Why keep `ready_version` separate from `source_version` during replacement processing?

**A:** `source_version` names the input currently being processed; `ready_version` and its manifest name the bytes viewers can actually play. The service may keep the old ready version available by policy while a newer source is processed, then atomically switch only if the worker's source version is still current.

**Q:** What must be true before the service publishes an HLS or DASH manifest?

**A:** Every required playlist and referenced segment must exist, pass validation and belong to the same source/rendition generation. A manifest that points to partial or mixed-version objects turns a successful database update into a broken playback path.

## Dropbox System Design

Source: [Dropbox System Design](30.2.2.18-dropbox.md)

**Q:** Why does content hashing not resolve concurrent file edits by itself?

**A:** It identifies bytes, not which version should win. The sync protocol still needs versions, conflict detection and a user-visible reconciliation policy.

**Q:** Why persist a change cursor after applying its page rather than before?

**A:** A crash before application with an advanced cursor skips changes. Applying first may replay a page after a crash, so application must be idempotent under stable change identity.

**Q:** What does the namespace sequence add beyond a `committed_at` timestamp?

**A:** A sequence assigned under the namespace-head transaction gives a committed cursor order even when clocks tie or differ. It also makes the serialization cost visible: one hot namespace has a single ordering point and may need a partition-aware cursor design to scale further.

**Q:** Why bind the current file revision to a row in `file_versions` with a deferred foreign key?

**A:** A version update changes the current pointer and inserts its manifest record in one transaction. Deferral permits either write order inside that transaction while rejecting a commit whose pointer has no corresponding version.

**Q:** Why keep a sync-operation result separate from the change cursor?

**A:** The operation record answers whether a retried command already committed and returns its original result. The cursor answers which namespace changes a device has applied. A notification or cursor cannot resolve an unknown write response by itself.

## Lyft / Ride-Sharing System Design

Source: [Lyft / Ride-Sharing System Design](30.2.2.19-lyft.md)

**Q:** What prevents two dispatch workers from assigning the same driver?

**A:** A shared atomic claim or transactional state transition. Independent local decisions based on location snapshots cannot enforce the assignment invariant.

**Q:** Why does locking only a ride leave driver double-booking possible?

**A:** Two different rides can each accept the same driver. Claim the driver and ride together under one authoritative transaction and recheck the current unexpired offer.

**Q:** Why is the nearest grid cell not necessarily the fastest pickup?

**A:** Straight-line distance ignores road topology, traffic and barriers such as rivers or one-way roads. Use cells to bound candidate discovery, then compare a limited set with road-time estimates and keep a clear fallback if routing is unavailable.

## Distributed Counter / Metrics Aggregation System Design

Source: [Distributed Counter / Metrics Aggregation System Design](30.2.2.20-distributed-counter.md)

**Q:** Why can a sharded counter be scalable yet unsuitable for a hard inventory cap?

**A:** Summing eventually visible shards gives an approximate or delayed total. Enforcing a strict cap requires coordinated admission or preallocated bounded rights.

**Q:** Which G-Counter operation is idempotent, and which business action is not automatically deduplicated?

**A:** State merge takes the maximum per writer slot, so repeated state exchange changes nothing. Repeating a new local increment for one client retry can still count the business event twice.

**Q:** Why must each G-Counter writer keep its identity unique across concurrent writers and restarts?

**A:** Merge compares values within the same writer slot. Two concurrent writers sharing a slot can overwrite one another, while resetting a slot can make the merged state forget prior increments. Use durable identity or a new epoch and a safe protocol before compacting old slots. See the [CRDT counter model](https://dsf.berkeley.edu/cs286/papers/crdt-tr2011.pdf).

## Workflow Engine — System Design Case Study

Source: [Workflow Engine — System Design Case Study](30.2.2.21-workflow-engine.md)

**Q:** What must a workflow engine persist before scheduling a step?

**A:** Its durable execution state and the stable identity of the intended work. Workers may repeat after crashes, so steps need appropriate deduplication or reconciliation.

**Q:** Why is a completed-step lookup insufficient before an external charge?

**A:** Two attempts can pass the lookup, and a charge can succeed before its result is saved. Stable downstream action identity, ownership checks, and uncertain-outcome reconciliation cover those gaps.

**Q:** Why must replayed workflow decisions be deterministic in Temporal?

**A:** Temporal reconstructs workflow state by replaying its event history. Incompatible code can produce different commands for old history, so external I/O belongs in activities and in-flight workflow changes need a compatible versioning strategy. See [Temporal's workflow-definition guidance](https://docs.temporal.io/workflow-definition).

## Real-Time Collaboration — System Design Case Study

Source: [Real-Time Collaboration — System Design Case Study](30.2.2.22-real-time-collaboration.md)

**Q:** Why does CRDT convergence not automatically preserve a business invariant?

**A:** The merge rules guarantee particular state convergence properties. Invariants such as limited stock or permission enforcement may require additional coordination.

**Q:** Why should an editor snapshot preserve CRDT state rather than just the displayed string?

**A:** The string discards identifiers and relationships required to merge offline edits. Persist compatible CRDT state at a known checkpoint and retain later missing updates.

**Q:** What does a Yjs state vector establish during reconnect, and what does it leave unproven?

**A:** It summarizes the replica state so a peer can compute missing updates. It does not prove those updates were durably committed or that the caller is authorized to apply them. See [Yjs document updates](https://docs.yjs.dev/api/document-updates).

## Typeahead / Autocomplete System Design

Source: [Typeahead / Autocomplete System Design](30.2.2.23-typeahead-autocomplete.md)

**Q:** Why should autocomplete rank candidates after applying access constraints?

**A:** A fast suggestion can still leak private document names or identities. Authorization and tenant boundaries apply to search indexes and caches too.

**Q:** How can an older autocomplete response overwrite a newer query even after cancellation?

**A:** Cancellation races with response completion. Render only a response whose request generation still matches current input; keep private cache scope separate from that UI rule.

**Q:** Why must the index builder and serving path use the same normalization policy?

**A:** A query normalized differently from the built keys can miss a valid prefix or collide with another key. Pin the normalization form and version, and reject collisions before publication. See [Unicode normalization](https://unicode.org/reports/tr15/).

## Metrics & Monitoring Pipeline System Design

Source: [Metrics & Monitoring Pipeline System Design](30.2.2.24-metrics-monitoring-pipeline.md)

**Q:** Why must a metrics pipeline distinguish event time from ingestion time?

**A:** Late and reordered samples affect windows and alerts differently. Define watermark, lateness and correction policies rather than treating arrival as occurrence.

**Q:** Why cannot a Bloom-filter match prove series quota admission?

**A:** It may be a false positive for a new series. Confirm exact tenant-scoped identity and atomically reserve quota; use the filter only to optimize lookup.

**Q:** How does delta temporality change counter or histogram rate processing?

**A:** Each delta covers a non-overlapping interval, while cumulative points cover an interval from a start time. Preserve those boundaries and detect gaps/resets before aggregation; applying cumulative reset logic to deltas can double-count or lose samples. See the [OpenTelemetry metrics data model](https://opentelemetry.io/docs/specs/otel/metrics/data-model/).

## Distributed Job Scheduler System Design

Source: [Distributed Job Scheduler System Design](30.2.2.25-distributed-job-scheduler.md)

**Q:** Why does electing one scheduler not guarantee one execution of a job?

**A:** Leases can expire, workers can restart and acknowledgments can be lost. Use stable run identities plus effect-side deduplication or fencing.

**Q:** Why retain occurrence uniqueness after a scheduled job succeeds?

**A:** A delayed scanner or replay can revisit its scheduled timestamp. A live-only unique key disappears after success and would allow the same occurrence to be created again.

**Q:** What does the unique live-run index protect, and what does it leave to the scheduler transaction?

**A:** It prevents two current runs from owning the same job occurrence. The transaction must still verify the schedule version, insert the run, advance the next-fire cursor, and write publication intent together. See [PostgreSQL partial indexes](https://www.postgresql.org/docs/current/indexes-partial.html).

## Distributed ID Generator System Design

Source: [Distributed ID Generator System Design](30.2.2.26-distributed-id-generator.md)

**Q:** What should an ID generator do when the clock moves backward?

**A:** Follow an explicit policy such as waiting, a logical clock or refusing generation. Reusing a timestamp/worker/sequence range can violate uniqueness.

**Q:** Why can writing last timestamp every few seconds fail after restart?

**A:** Issued timestamp/sequence combinations inside the unsaved interval can be reused. Persist a safe reservation before issuance or restore a protocol that skips all possibly issued values and preserves exclusive identity.

**Q:** Does a worker ID make a Snowflake-style generator safe after its lease expires?

**A:** No. If an old process keeps issuing after the identity is reassigned, both owners can emit the same worker/time/sequence tuple. The old process must stop at a conservative lease deadline, or identities must not be reused under the chosen protocol.

## Ad Click Aggregator System Design

Source: [Ad Click Aggregator System Design](30.2.2.27-ad-click-aggregator.md)

**Q:** Why must the click's exact dedup state update even when a Bloom filter says absent?

**A:** If it does not, the next duplicate may find no exact record and be counted again. Commit deduplication and the aggregate effect atomically.

**Q:** Why does nightly replay not by itself prove an invoice exact?

**A:** The log may miss source events or retain outdated fraud/price policy. Reconcile defined event sets and versions, settle an auditable revision, and record later adjustments rather than overwrite issued billing.

**Q:** What does a one-percent Bloom-filter false-positive rate describe?

**A:** It describes the chance that a previously unseen identity tests positive. It does not mean one percent of all positive checks are false, and it cannot authorize dropping exact deduplication. Repeated events can make most lookups positive because they are genuine repeats.

## Parking Lot System Design

Source: [Parking Lot System Design](30.2.2.28-parking-lot.md)

**Q:** What should make releasing a parking space safe to retry?

**A:** A ticket/session identity and conditional transition ensure that repeating an old release cannot free a space currently occupied by a newer session.

**Q:** Why must payment and physical exit remain separate facts?

**A:** A paid car may still occupy a space, and a sent barrier command may not have executed. Reconcile controller/passage/occupancy evidence under the facility policy before releasing authoritative ownership.

**Q:** Why are `assigned_at` and `entered_at` separate timestamps?

**A:** A database can reserve a space before the car crosses the barrier. Recording entry only after passage keeps the software decision distinct from physical evidence; a lost acknowledgment needs reconciliation rather than a fabricated arrival time.

## Distributed Cache System Design

Source: [Distributed Cache System Design](30.2.2.29-distributed-cache.md)

**Q:** What can consistent hashing solve without solving cache consistency?

**A:** It limits key remapping as nodes change. It does not supply invalidation, replication ordering, durable storage or protection against hot keys.

**Q:** How can delete-after-write still leave an old cached value?

**A:** An in-flight reader loaded version seven before a version-eight write and invalidation, then populates seven afterward. Version/generation-aware population or an explicit stale-window policy handles the race.

**Q:** Does a five-minute TTL guarantee the cached value is at most five minutes old?

**A:** No. TTL measures time since insertion. A slow loader can insert an old origin snapshot just before insertion and keep it for another five minutes; record source version/observation time when source age matters.

## Message Queue System Design

Source: [Message Queue System Design](30.2.2.30-message-queue.md)

**Q:** Why does visibility timeout require consumer deduplication?

**A:** A worker may commit an effect but fail to acknowledge before the timeout. The broker can then deliver the same message again.

**Q:** Why can partition-ordered reads still produce out-of-order business effects?

**A:** Parallel handlers, retries, producer races, and delayed external calls can complete in another order. Enforce aggregate versions or serialized processing where business ordering is required.

**Q:** What does SQS FIFO producer deduplication guarantee beyond the deduplication window?

**A:** Nothing about a later retry after its five-minute window, and nothing about an external database or payment effect. Persist a stable business idempotency key at the consumer boundary as well. See [SQS FIFO deduplication](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-exactly-once-processing.html).

## API Gateway System Design

Source: [API Gateway System Design](30.2.2.31-api-gateway.md)

**Q:** Why should an API gateway preserve the caller's end-to-end deadline?

**A:** Independent full timeouts at each hop let work continue after the client gives up. Propagate the remaining budget and cancel where supported.

**Q:** Why are identity headers not safe merely because a gateway sets them?

**A:** A caller can spoof them unless the gateway strips inbound values and the backend authenticates the protected gateway context/channel. The backend still checks resource and tenant authorization.

**Q:** Where should the final decision to read `/orders/7` be made?

**A:** The orders service should authorize the authenticated principal against order 7 and its tenant or ownership policy. The gateway can authenticate and admit the request, but route access alone does not grant object access.

## Additional case traces

Source: [30.2.2.02-whatsapp](30.2.2.02-whatsapp.md)

**Q:** Why does a socket send fail to prove delivery?

**A:** Only an authenticated recipient receipt after durable device storage establishes that device delivery. Socket acceptance proves neither receipt nor user reading.

Source: [30.2.2.03-uber](30.2.2.03-uber.md)

**Q:** Why can the nearest driver arrive later?

**A:** Straight-line distance ignores road barriers and traffic. Use bounded fresh eligible candidates and a road ETA budget, then let the authoritative transaction claim both driver and ride.

Source: [30.2.2.04-netflix](30.2.2.04-netflix.md)

**Q:** Why cannot a license outage create an offline license?

**A:** Offline rights must be provisioned in advance under expiry/device policy. An outage cannot safely manufacture authorization; existing valid licenses may continue while new starts fail.

Source: [30.2.2.05-google-drive](30.2.2.05-google-drive.md)

**Q:** Why does parent_id referencing files fail to prevent a folder cycle?

**A:** A foreign key only proves existence. The move authority must check folder type, scope, ancestry and concurrent moves under suitable coordination; otherwise two individually checked moves can create a cycle.

Source: [30.2.2.06-payment-gateway](30.2.2.06-payment-gateway.md)

**Q:** Why must a timed-out charge retain its provider identity?

**A:** The provider may have succeeded before the response was lost. Another provider has a separate deduplication namespace and can charge again. Reconcile/retry the existing identity before changing route.

Source: [30.2.2.07-notification-service](30.2.2.07-notification-service.md)

**Q:** Why recheck preferences after scheduling?

**A:** A recipient may opt out or lose a valid channel target while a job waits. Acceptance-time consent is stale; dispatch rechecks purpose/channel policy, quiet hours and expiry before provider work.

Source: [30.2.2.16-instagram](30.2.2.16-instagram.md)

**Q:** Why is a cached feed ID insufficient to show a post?

**A:** It is derived shortlist data. Current visibility, blocking, expiry and deletion must still be checked during hydration and media access, including cache hits.


Source: [Ticket booking](30.2.2.08-ticket-booking.md)

**Q:** Why must a late successful payment not reclaim an expired hold's seats?

**A:** Another buyer may already hold or own those seats. Confirmation must recheck the exact current hold and expiry. Reconcile/cancel/refund the payment under the compensation policy instead of taking another buyer's inventory.

Source: [E-commerce](30.2.2.09-e-commerce.md)

**Q:** Why can a duplicate inventory-release command create oversell risk?

**A:** Incrementing available stock on every retry invents additional units. Claim active-to-released once and restore that reservation's quantity in the same transaction; subsequent retries return the recorded outcome without another increment.

Source: [Hospital management](30.2.2.10-hospital-management.md)

**Q:** Why does an overlap exclusion constraint fail to implement booking retry identity?

**A:** It rejects competing active time intervals, but cannot tell whether a repeated request is the same already committed booking. A scoped stable command ID with a matching payload returns the existing appointment after a lost response; resource authorization is rechecked independently.

Source: [Live betting](30.2.2.11-live-betting.md)

**Q:** Why must cash-out and settlement share a terminal-state decision?

**A:** Both can credit the same open wager. Compare the authoritative wager state/version and post the winning transition and journal atomically; a competing retry retrieves the recorded result rather than crediting it again.

Source: [Twitter feed](30.2.2.12-twitter-feed.md)

**Q:** Why does a chronological cursor include the post ID as well as time?

**A:** Two posts can share a timestamp. Ordering and filtering by the same complete tuple preserve the boundary; time-only filtering can skip a tied post. Ranked feeds additionally need a session/snapshot contract.

Source: [Web crawler](30.2.2.14-web-crawler.md)

**Q:** Why can a locally delayed fetch still overwhelm one origin?

**A:** Other workers can independently pass the same timing check. Reserve origin capacity and next-start time atomically under shared ownership, bound request lifetimes and account for overlap during expired-claim recovery.

Source: [Chat system](30.2.2.15-chat-system.md)

**Q:** Why does a new-message cursor miss offline edits?

**A:** An edit changes an existing sequence rather than creating a later message. Retain a separate change/delta cursor with a snapshot watermark, apply changes before advancing it, and require resynchronization when retention removed needed deltas.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
