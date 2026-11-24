# Fresh-reader review — 5 October 2026

> **Dated review record:** counts, test results, and remaining-work statements below describe the recorded pass. Use the [current review progress](2026-10-25-fullstack-coverage-review.md) and [verification runbook](verification-gates.md) for present scope; chapter existence and passing scans do not establish complete reader review.

This records full-prose reading performed by the independent reader passes in this continuation. "Fully read" means prose outside fenced code was read from start to end; it does not imply every claim was independently source-checked. Automated gates are not a substitute for this review.

## REST API category — fully read

The reader read all non-code-fence prose in the following category files:

- `20-backend/20.3-rest-apis/INDEX.md`
- `20-backend/20.3-rest-apis/01-design-and-contract/INDEX.md`
- `20-backend/20.3-rest-apis/01-design-and-contract/REVISION.md`
- `20-backend/20.3-rest-apis/01-design-and-contract/20.3.1.01-api-design-patterns.md`
- `20-backend/20.3-rest-apis/01-design-and-contract/20.3.1.02-rest-principles.md`
- `20-backend/20.3-rest-apis/01-design-and-contract/20.3.1.03-versioning.md`
- `20-backend/20.3-rest-apis/01-design-and-contract/20.3.1.04-rest-maturity-model.md`
- `20-backend/20.3-rest-apis/01-design-and-contract/20.3.1.05-openapi-swagger.md`
- `20-backend/20.3-rest-apis/02-http-mechanics/INDEX.md`
- `20-backend/20.3-rest-apis/02-http-mechanics/REVISION.md`
- `20-backend/20.3-rest-apis/02-http-mechanics/20.3.2.01-http-methods.md`
- `20-backend/20.3-rest-apis/02-http-mechanics/20.3.2.02-status-codes.md`
- `20-backend/20.3-rest-apis/02-http-mechanics/20.3.2.03-cors.md`
- `20-backend/20.3-rest-apis/02-http-mechanics/20.3.2.04-http-caching.md`
- `20-backend/20.3-rest-apis/03-payloads-errors-integration/INDEX.md`
- `20-backend/20.3-rest-apis/03-payloads-errors-integration/REVISION.md`
- `20-backend/20.3-rest-apis/03-payloads-errors-integration/20.3.3.01-pagination.md`
- `20-backend/20.3-rest-apis/03-payloads-errors-integration/20.3.3.02-error-handling-design.md`
- `20-backend/20.3-rest-apis/03-payloads-errors-integration/20.3.3.03-long-running-api-operations.md`
- `20-backend/20.3-rest-apis/03-payloads-errors-integration/20.3.3.04-file-upload-apis.md`
- `20-backend/20.3-rest-apis/03-payloads-errors-integration/20.3.3.05-webhooks.md`
- `20-backend/20.3-rest-apis/03-payloads-errors-integration/20.3.3.06-serialization-and-wire-formats.md`
- `20-backend/20.3-rest-apis/03-payloads-errors-integration/20.3.3.07-transactional-email-and-notifications.md`
- `20-backend/20.3-rest-apis/04-edge-and-scale/INDEX.md`
- `20-backend/20.3-rest-apis/04-edge-and-scale/REVISION.md`
- `20-backend/20.3-rest-apis/04-edge-and-scale/20.3.4.01-rate-limiting.md`
- `20-backend/20.3-rest-apis/04-edge-and-scale/20.3.4.02-api-gateway.md`
- `20-backend/20.3-rest-apis/04-edge-and-scale/20.3.4.03-bff.md`
- `20-backend/20.3-rest-apis/04-edge-and-scale/20.3.4.04-authentication.md`
- `20-backend/20.3-rest-apis/05-interview-drills/INDEX.md`
- `20-backend/20.3-rest-apis/05-interview-drills/20.3.5.01-interview-questions.md`

The reader flagged, and this pass corrected, claims about Representational State Transfer (REST) statelessness, API versioning, HTTP status classes, Cross-Origin Resource Sharing (CORS), HTTP caching, and pagination totals. It also updated Request for Comments (RFC) 9457 error details, long-running operations, provider-specific webhook contracts, email rules, and authentication schemes.

The maturity-model chapter now points to the dedicated versioning chapter instead of repeating it. The interview drill and revision answers align with those corrections.

## PostgreSQL and database category — fully read, with one sampled drill

The reader fully read all prose outside code fences in:

- `20-backend/20.4-database/INDEX.md`
- `20-backend/20.4-database/01-postgresql-foundations/INDEX.md`
- `20-backend/20.4-database/01-postgresql-foundations/REVISION.md`
- `20-backend/20.4-database/01-postgresql-foundations/20.4.1.01-postgresql.md`
- `20-backend/20.4-database/01-postgresql-foundations/20.4.1.02-normalization.md`
- `20-backend/20.4-database/01-postgresql-foundations/20.4.1.03-mvcc.md`
- `20-backend/20.4-database/01-postgresql-foundations/20.4.1.04-nosql-vs-sql.md`
- `20-backend/20.4-database/01-postgresql-foundations/20.4.1.05-postgresql-performance.md`
- `20-backend/20.4-database/01-postgresql-foundations/20.4.1.06-row-level-security.md`
- `20-backend/20.4-database/02-querying-and-optimization/INDEX.md`
- `20-backend/20.4-database/02-querying-and-optimization/REVISION.md`
- `20-backend/20.4-database/02-querying-and-optimization/20.4.2.01-indexes.md`
- `20-backend/20.4-database/02-querying-and-optimization/20.4.2.02-joins.md`
- `20-backend/20.4-database/02-querying-and-optimization/20.4.2.03-execution-plans.md`
- `20-backend/20.4-database/02-querying-and-optimization/20.4.2.04-window-functions.md`
- `20-backend/20.4-database/02-querying-and-optimization/20.4.2.05-jsonb.md`
- `20-backend/20.4-database/03-transactions-and-replication/INDEX.md`
- `20-backend/20.4-database/03-transactions-and-replication/REVISION.md`
- `20-backend/20.4-database/03-transactions-and-replication/20.4.3.01-transactions.md`
- `20-backend/20.4-database/03-transactions-and-replication/20.4.3.02-deadlocks.md`
- `20-backend/20.4-database/03-transactions-and-replication/20.4.3.03-optimistic-pessimistic-locking.md`
- `20-backend/20.4-database/03-transactions-and-replication/20.4.3.04-database-replication.md`
- `20-backend/20.4-database/04-orm-and-access/INDEX.md`
- `20-backend/20.4-database/04-orm-and-access/REVISION.md`
- `20-backend/20.4-database/04-orm-and-access/20.4.4.01-prisma.md`
- `20-backend/20.4-database/04-orm-and-access/20.4.4.02-prisma-advanced.md`
- `20-backend/20.4-database/04-orm-and-access/20.4.4.03-orm-query-builder-landscape.md`
- `20-backend/20.4-database/05-operations-and-scaling/INDEX.md`
- `20-backend/20.4-database/05-operations-and-scaling/REVISION.md`
- `20-backend/20.4-database/05-operations-and-scaling/20.4.5.01-connection-pooling.md`
- `20-backend/20.4-database/05-operations-and-scaling/20.4.5.02-migration-strategies.md`
- `20-backend/20.4-database/05-operations-and-scaling/20.4.5.03-soft-delete-and-tombstones.md`
- `20-backend/20.4-database/05-operations-and-scaling/20.4.5.04-backups-pitr-recovery.md`
- `20-backend/20.4-database/05-operations-and-scaling/20.4.5.05-search-infrastructure-at-scale.md`

`20-backend/20.4-database/05-operations-and-scaling/20.4.5.06-interview-questions.md` was sampled only. The sample found two array-query examples missing a `FROM` clause; they now name `products`.

Findings fixed in fully read chapters include row-level security (RLS) boundaries, Prisma parameterization, policy composition, NoSQL and relational distinctions, and isolation language. The edits also cover PostgreSQL indexing, window-function behavior, query-tuning heuristics, conditional erasure requirements, migration locks and recovery, and deadlock `SQLSTATE` codes.

## System-design theory — selected full reads

The reader fully read the prose outside code fences in:

- `30-architecture/30.2-system-design/01-theory/INDEX.md`
- `30-architecture/30.2-system-design/01-theory/REVISION.md`
- `30-architecture/30.2-system-design/01-theory/30.2.1.01-cap-theorem.md`
- `30-architecture/30.2-system-design/01-theory/30.2.1.02-consistency-models.md`
- `30-architecture/30.2-system-design/01-theory/30.2.1.05-caching-patterns.md`
- `30-architecture/30.2-system-design/01-theory/30.2.1.06-queues-and-async.md`
- `30-architecture/30.2-system-design/01-theory/30.2.1.08-rate-limiting.md`
- `30-architecture/30.2-system-design/01-theory/30.2.1.12-capacity-planning.md`
- `30-architecture/30.2-system-design/01-theory/30.2.1.13-backpressure-and-flow-control.md`
- `30-architecture/30.2-system-design/01-theory/30.2.1.18-outbox-and-cdc.md`

Corrections cover delivery guarantees and retention conditions, cache source-of-truth and invalidation races, push versus pull flow control, and queue recovery options. They also address rate-limit scope, capacity units, Little's Law, and change data capture (CDC) log-retention limits. Other system-design chapters and the hospital-management case remain open for full-prose review.

## Additional full reads — distributed data and routing

The primary reviewer subsequently read all prose and examples in `30.2.1.03-sharding-and-replication.md`, `30.2.1.04-load-balancing.md`, `30.2.1.07-distributed-transactions.md`, and `30.2.1.09-consensus-and-leader-election.md`.

- **Sharding (`30.2.1.03`):** describes storage as well as write scaling, distinguishes PostgreSQL table partitioning from distributing data across database servers, and explains why consensus alone does not fence stale writes at an external resource.
- **Load balancing (`30.2.1.04`):** defines proxy and client-side routing, qualifies per-request versus per-connection behavior, clarifies Layer 4 (L4) handling of gRPC, and removes default claims about round-robin fairness, latency routing, and least-connections. It also distinguishes instance readiness from broader dependency health and states that traffic routing cannot restore a failed dependency.
- **Consensus and transactions (`30.2.1.07`, `30.2.1.09`):** ties replica agreement to deterministic state-machine behavior and removes a dated KRaft-readiness milestone; the distributed-transaction chapter's atomic-commit and saga boundaries were confirmed in a full read.

Other system-design chapters and the broader corpus still need full-prose review.

## Additional full reads — failure handling and architecture choices

The primary reviewer read all prose and examples in `30.2.1.10-failure-modes.md` and `30.2.1.11-architecture-patterns.md`.

The failure guide now makes timeout budgets illustrative rather than fixed and distinguishes Transport Layer Security (TLS) certificate expiry from retired Secure Sockets Layer (SSL) terminology. It also adds freshness and authorization conditions to a search fallback, defines recovery objectives clearly, removes repeated backup warnings, and trims vendor lists that did not explain the concepts.

The architecture guide now distinguishes deployment boundaries from communication and internal dependency patterns. It removes the unsupported "four patterns" claim and clarifies that module boundaries can help a later extraction without guaranteeing one. The remaining system-design chapters and broader corpus are still open for full-prose review.

## Remaining scope

These finished batches do not constitute a full-corpus review. The corpus-wide inventory still covers hundreds of Markdown pages that have not had a full fresh-reader pass. Continue recording actual path coverage and unresolved content, and do not treat passing automated checks as a readability certification.

## Targeted hospital case-study follow-up — 5 October

The primary reviewer revisited the booking, tenancy, audit, cache, queue, scaling, failure, monitoring, and capacity sections in `30-architecture/30.2-system-design/02-case-studies/30.2.2.10-hospital-management.md`. The example now uses a database overlap constraint for concurrent bookings, tenant-scoped foreign keys, offset-aware appointment times, durable notification events, minimal audit metadata, and failure behavior that does not bypass key controls. Malformed ASCII diagrams and duplicate implementation snippets were replaced with shorter relationships and a single flow diagram.

This was a targeted correction pass, not an independent full-prose read or a validation that the illustrative architecture meets a particular organization's legal obligations. Other case studies and the remaining corpus still need review.

## Additional system-design theory corrections — 5 October

Targeted reviews corrected the resharding explanation and mixed content delivery network (CDN) and global-routing diagram in `30-architecture/30.2-system-design/01-theory/30.2.1.03-sharding-and-replication.md` and `30-architecture/30.2-system-design/01-theory/30.2.1.04-load-balancing.md`. `30.2.1.07-distributed-transactions.md` now has concise, non-duplicated references that distinguish the atomic-commit discussion from microservice recovery patterns.

`30.2.1.09-consensus-and-leader-election.md` now distinguishes the agreement problem from leader election, qualifies majority assumptions, and removes duplicated explanations. It also explains timeouts, fencing, and Kafka and Redlock behavior with current references.

These were targeted correction passes, not a certification that every paragraph and code sample in these chapters has had an independent full-prose review. Their companion revision links and cross-reference gates were also checked. The remaining system-design theory and other corpus sections are still open.

## Failure and architecture-pattern corrections — 5 October

Targeted edits in `30-architecture/30.2-system-design/01-theory/30.2.1.10-failure-modes.md` remove repeated category tables and repeated examples, replace fixed retry and failover values with bounded policies, and distinguish provider timeouts from confirmed failures. The examples avoid unsafe automatic payment-provider fallback, blind database promotion, static-IP Domain Name System (DNS) fallback, and unguarded production fault injection. They add explicit data-corruption, deployment, configuration, and external-provider recovery cases.

`30.2.1.11-architecture-patterns.md` now uses a short boundary-and-cost comparison and corrects categorical team-size and latency claims. It distinguishes event-driven delivery from event sourcing and ordering guarantees, replaces malformed ASCII figures with small flow diagrams, and removes repeated interview-selection tables and invented team metrics. These are targeted correction passes; the broader architecture corpus and all remaining chapters have not been fully read.

## Distributed locks and interview-flow corrections — 5 October

`30-architecture/30.2-system-design/01-theory/30.2.1.14-distributed-locks.md` is now organized around the invariant, the expiry failure, resource-side fencing, choosing a database or coordination primitive, and safe worker patterns. It removes unsafe unconditional Redis release and the claim that a DynamoDB time to live (TTL) deletion acts as an immediate lease, and it distinguishes lock ownership from exactly-once work. Official Redis, ZooKeeper, etcd, PostgreSQL, and DynamoDB material plus the Redlock critique were checked and linked.

`30.2.1.15-how-to-approach.md` replaces the large ASCII interview chart and repeated schedule with a four-row flow, labels its timing as a suggestion for a 45-minute interview, makes the URL-shortener numbers explicitly hypothetical, and removes redundant and echoing See Also labels. The theory index now describes this as an adaptable flow. These are targeted corrections; remaining theory chapters and the broader corpus still need full fresh-reader review.

## Resilience and probabilistic-structure corrections — 5 October

`30.2.1.19-resilience-patterns-deep-dive.md` removes unsupported hedging gains, fixed shedding percentages, and universal wrapper and threshold claims. It distinguishes 503 capacity responses from 429 rate-policy responses, explains singleflight as process-local, makes cancellation and deadline limits explicit, and fixes the example's double-release bug. The companion questions now ask about attempt independence and duplicate-work cost.

`30.2.1.17-probabilistic-data-structures.md` now distinguishes approximate sketches from Merkle trees, corrects false-positive and Count-Min semantics, and removes unsupported vendor-use claims and benchmark numbers. It also repairs incomplete comparison tables and clarifies Merkle-tree compatibility requirements. New Bloom, Count-Min, Merkle, and Envoy references were checked and added to the external-link baseline. These two chapters received a targeted prose and claim audit; the other system-design chapters and remaining corpus still need review.

## Multi-region and transport corrections — 5 October

`30.2.1.20-multi-region-deployment.md` defines recovery point objective (RPO) and recovery time objective (RTO), removes unsupported availability, cost, DNS recovery, and failover-time promises, and distinguishes deployment topology from consistency behavior. It replaces a handwritten PostgreSQL promotion script with a guarded failover outline and corrects DynamoDB Global Tables and quorum descriptions. It also narrows conflict-free replicated data type (CRDT) and operational transformation (OT) claims, avoids presenting data-residency law as a blanket in-country storage rule, and leaves provider, database, and jurisdictional adaptation to the reader.

`30.2.1.21-tcp-udp-transport-fundamentals.md` states TCP and TLS round-trip time (RTT) assumptions, separates TCP setup from TLS and request-response time, treats UDP congestion and delivery as application-protocol concerns, and explains QUIC 0-RTT replay limits. It corrects DNS, game and media, `TIME_WAIT`, and pool examples, removes the misleading toy UDP retry protocol, and moves interview drills to the separate category revision companion. RFC 9293, RFC 9000, RFC 9001, RFC 8446, RFC 4786, and current AWS and Google references were checked; these chapters received targeted passes rather than a full review of all remaining system-design material or the broader corpus.

## DNS, TLS, and adjacent interview-bank follow-up — 5 October

`30.2.1.22-dns-and-name-resolution.md` introduces lookups in plain language, explains resolver roles and TTL behavior without fixed cutover promises, distinguishes DNS Security Extensions (DNSSEC) from encrypted DNS, and qualifies Kubernetes search behavior. It also corrects Node.js `resolve*()` cache assumptions and moves its drills into the theory revision companion.

`30.2.1.23-tls-https-and-certificates.md` clarifies TLS over TCP versus HTTP/3 over QUIC, limits forward-secrecy and 0-RTT claims to their actual modes, distinguishes Automatic Certificate Management Environment (ACME) from Let's Encrypt, qualifies revocation behavior, and corrects the manual DNS challenge example. Their source links were checked and added to the citation baseline.

The adjacent 1,759-line system-design interview bank was sampled by heading and representative early examples only. Its opening contained unsupported popularity and difficulty claims, unlabeled workload assumptions, fixed cache-hit and connection-capacity numbers, and misleading recommendations such as MD5-based short-code generation and treating redirect status as an analytics control. A full question-by-question review remained outstanding at that checkpoint; the two networking chapters received a targeted content pass rather than a full system-design or corpus review.

## System-design drill sample correction — 5 October

The opening of `30-architecture/30.2-system-design/01-theory/30.2.1.16-interview-questions.md` describes the set as practice prompts, labels supplied figures as exercise assumptions, and gives a repeatable way to work through a design. The URL-shortener answer removes unsupported MD5, default-sharding, and cache-hit claims and explains uniqueness, redirect caching, and analytics trade-offs.

The rate-limiter answer distinguishes local from distributed state, labels its Python token bucket as single-process teaching code, and explains why a non-atomic Redis pipeline is insufficient. The remaining 28 answers were still unaudited at that point.

Prompts 3–7 were rewritten around requirement clarification, a small design flow, and explicit failure cases:

- **Notifications, chat, and key-value stores:** notification separates provider acceptance from delivery and includes durable intent and retry behavior; chat scopes ordering and reconnect cursors; key-value qualifies quorum assumptions and removes the toy hash ring.
- **Web crawler and autocomplete:** crawler distinguishes `robots.txt` guidance from access authorization and calls out URL deduplication loss and Server-Side Request Forgery (SSRF); autocomplete covers ranking freshness and deletion.

RFC 9309 was checked and added to the citation baseline. Prompts 8–30 were reviewed in the follow-up notes below; higher-numbered prompts and other corpus sections remained outstanding at that time.

The interview-bank pass continued through prompts 8–10. Analytics defines event IDs and timestamps, duplicates and late data, bounded ingestion, and deletion across derived stores, while the CDN answer removes invented edge counts and latency tiers and explains cache keys, private-response boundaries, origin behavior, and invalidation.

The ID-generator answer separates uniqueness from ordering, covers universally unique identifier (UUID) v4, UUIDv7, sequence, and Snowflake-style trade-offs, and calls out worker allocation, clock rollback, and security boundaries. RFC 9562 was checked and added to the external-link baseline, leaving prompts 11–30 unaudited then.

Prompts 11–14 also received a focused rewrite:

- **Ride sharing and social feed:** ride sharing separates approximate candidate search from atomic, durable driver and trip assignment; social feed removes broken sample code and an arbitrary celebrity threshold, then explains projection lag, visibility checks, and pagination.
- **Video streaming and payments:** video streaming separates upload, processing, publishing, CDN delivery, and recommendations, with resumable uploads and recoverable processing states; payments replaces the unsafe Redis check-then-charge example with durable operation identity, provider idempotency, ambiguous-timeout handling, duplicate and out-of-order webhooks, and reconciliation (provider-specific links were checked against Stripe documentation).

Prompts 15–30 remained to be audited beyond that checkpoint.

Prompts 15–18 were rewritten to surface concurrency, stale-data, and recovery boundaries. Ticket booking makes the durable reservation authoritative and treats Redis TTL as an aid rather than the sale record, while search separates the source from its lagging index and enforces access control on result reads.

Distributed caching distinguishes eviction from TTL and documents invalidation races, stampedes, and cache-loss behavior. The scheduler defines occurrence identity, leases, time-zone and misfire policy, and retry semantics without claiming exactly-once external effects; prompts 19–30 remained outstanding then.

Prompts 19–20 were rewritten around data lifecycle and operational use. File sync separates object bytes from metadata and change notifications, defines conflict and deletion handling, and treats chunking and deduplication as optional trade-offs with privacy costs. Metrics monitoring covers label cardinality, metric types, retention, missing telemetry, and actionable service-level objective (SLO) alerting instead of implying a specific vendor or threshold is universal, leaving prompts 21–30 unaudited at that step.

## System-design interview bank completion — 5 October

Prompts 21–25 were revised to distinguish local transactions, two-phase commit, and sagas; define event time, replay, and duplicate handling for streams; and make multi-region consistency and recovery goals explicit. They also separate recommendation candidates from ranking and bound graph traversal while enforcing authorization.

Prompts 26–30 were revised across distributed infrastructure and financial workflows:

- **Service mesh and multi-tenant isolation:** service mesh separates the request-path data plane from policy distribution and explains retry risks; multi-tenant isolation covers identity propagation, tenant isolation across derived stores, and transaction-scoped PostgreSQL context with connection pools.
- **Event-driven design, chaos, and payments:** event-driven messaging separates delivery from event sourcing, Command Query Responsibility Segregation (CQRS), and sagas, replacing the unsafe publish-before-durable-commit example with a transactional outbox; chaos engineering replaces unsafe fault-injection snippets with scoped hypotheses, pre-checks, abort controls, rollback, and recovery evidence; global payments distinguishes authorization, ledger state, provider and rail outcomes, reconciliation, clearing, and settlement while treating timeouts as ambiguous outcomes.

This completed the question-by-question rewrite of all 30 prompts in that bank. It did not complete the repository-wide review: the broad corpus still contained 1,009 Markdown files, and coverage above was limited to the named REST API, database, and system-design areas plus the recorded networking and sample passes.

The adjacent system-design theory index was also checked against the chapters: its interview-bank count matches the 30 prompts, the Merkle-tree row no longer labels that structure probabilistic, and its "why it matters" text describes decisions and constraints instead of prescribing a universal default. This was a focused consistency read of that index, not a new body-by-body read of every linked chapter.

## Case-study index and URL shortener — 5 October

The case-study index was checked against its numbered catalog. It reflects the 31 listed designs, includes Notification Service in its tier, removes unsupported claims about which prompts are "always asked," and prioritizes cases by the candidate's target role.

The primary reviewer read the URL Shortener case study end to end and replaced its 570-line collection of incompatible snippets and unsupported scale claims with one request-flow design covering requirements, code generation and uniqueness, redirect status and cache behavior, mapping storage, analytics durability and privacy, scale estimates from explicit inputs, abuse controls, and failure cases.

It removes unsafe MD5 and non-atomic Redis examples, invented cluster sizes and latency targets, redundant vendor choices, and out-of-scope infrastructure. RFC 9110 was verified for redirect semantics and added to the external-link baseline, while the rate-limiter case study waited for its own full read.

The rate-limiter case study was then read end to end and reduced from 910 lines of overlapping code and diagrams to one coherent design. It distinguishes policy configuration from live counters, requires atomic shared decisions, explains local and multi-region overshoot, and states explicit failure, identity, API response, and capacity trade-offs.

It removes an allow-result cache that bypassed enforcement, timestamp-as-member sliding-window undercounting, incorrect `Retry-After` units, unbounded or fixed latency assumptions, and redundant queue and cache implementations. Redis and Stripe reference links were checked; the case-study revision companion remains separate.
