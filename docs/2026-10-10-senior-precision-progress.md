# Senior technical precision pass — 10 October 2026

This pass corrects concepts that could lead to the wrong engineering decision: consistency and commit boundaries, behavioral substitution, domain ownership, security credentials, cache freshness and platform resource guarantees. It uses original explanations informed by the supplied books, with current specifications and official documentation for runtime behavior.

## Fresh review coverage

The current inventory contains **1,023 authored Markdown documents**. This pass completely read **27 revised documents** and **11 retained/review-report documents**. **985 documents remain pending a new complete semantic review**. The earlier explanation-depth review remains historical evidence; it does not close this new accuracy pass.

Header or narrowly scoped companion repairs also touched **89 pending documents**. Those changes do not certify their remaining content. The internal audit records each path, baseline/current hash, concrete claims checked, source and disposition. A scanner or structural gate cannot establish technical accuracy.

## Corrected engineering boundaries

- **Distributed data:** sequential versus real-time ordering; serializability versus strict serializability; quorum assumptions; atomic commit versus locking; prepared outcomes and partial-failure uncertainty. DDIA references now identify the supplied 2017 edition and the correct chapters.
- **Coordination and routing:** one consensus decision versus a replicated log, quorum configuration, Zab scope, retry identity, stale-writer fences and hot-key limits. Queue acceptance, deferred completion, priority and aggregate routing now carry their actual conditions.
- **Design:** stakeholder-driven responsibility, actual behavioral substitution, source dependencies versus runtime calls, domain-service/aggregate boundaries, and language-specific access controls. Removed universal method-count, hierarchy and interface rules.
- **Security:** identity evidence, hash/MAC/signature distinctions, intended token recipients, OAuth/OIDC roles and callback traces, cookie credential attachment, authenticated encryption and key lifecycle. Broken auth diagrams were replaced with readable mechanisms.
- **Caching:** installed-entry TTL versus source-data age, delayed fills, namespace versions, normal misses versus stampedes, capacity/byte budgets, authoritative Redis state and partial-write recovery. All authored caching interview questions remain, with conditional and concise model answers.
- **Platform:** namespace quota admission versus actual resource usage or reserved capacity; priority/QoS boundaries carried into the companion and interview guidance.
- **Reading experience:** repaired 64 malformed Tags badge URLs and added checker regression cases. Removed repeated unsupported promises about interview coverage. Unbroken prose now wraps within mobile paragraphs while code blocks retain their scrolling. Paragraph width and theme behavior are checked on rendered pages.

## Books used for substantive reasoning

*Designing Data-Intensive Applications* (2017), *Clean Architecture*, *Fundamentals of Software Architecture* (2020), *Domain-Driven Design Quickly* (2006), and the supplied first edition of *Head First Design Patterns*. Edition-sensitive chapter references were checked against the local books. Front-matter inventory of another book is not treated as reading its technical advice. Extracted book text stays outside the repository.

## Validation and limits

Executed checks cover PostgreSQL 16.15 transfer, savepoint, prepared-state recovery, snapshot visibility, write skew, serialization rejection, lease renewal/replacement, stale epochs, conflict-row waits and outbox claim ordering; Node/browser lexical environment, promise, OAuth transaction and cache examples; value-object/account invariants; and Redis 7.4 transaction/script error retention, lease release and ACL enumeration. Five complete OOP examples also pass strict TypeScript 5.9.3 checking.

These checks establish the stated local traces. They do not establish managed-service failover, live provider OAuth exchange, cloud database behavior, Kubernetes admission on a real cluster or every integration sketch. The internal validation record retains outcomes, environment versions and unresolved execution boundaries. Full repository gates and rendered-page checks are reported only after their final run.

## Remaining work

Follow the ordered book-informed section of the explanation-depth plan. Continue complete reads through the remaining system-design theory and database/microservice material, then design/runtime/frontend/platform, quality/realtime/interview material and supporting guides. Reconcile companion answers at each contract change. Keep a document pending until its full meaning and examples have been assessed; do not replace this work with a bulk template or an arbitrary length requirement.
