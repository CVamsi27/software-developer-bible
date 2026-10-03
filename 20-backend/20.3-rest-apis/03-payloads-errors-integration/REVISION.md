<!-- section: REST APIs | category: Reference | tags: revisi | role-priority: essential | general-importance: foundational -->
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

**Q:** What core constraint explains why collections grow; responses cannot. governs api pagination?

**A:** A table with 10M rows cannot be serialized "in full" — memory, time, and client rendering all fail at different scales. The API must expose a *cursor into the collection* — which is all any pagination scheme is.

**Q:** What core constraint explains why offset and cursor trade two failure modes. governs api pagination?

**A:** Offset pages (`?page=50`) are cheap to build but shift under concurrent inserts (duplicates/skips) and cost O(skipped) rows server-side. Cursor pages (keyset: `?after=id_123`) are stable and O(log n) but can only walk the sort order. The senior choice is per-collection: mutable data → cursor; small/admin sets → offset.

**Q:** What core constraint explains why the client needs total-knowledge signals governs api pagination?

**A:** — total count or a `next` link — otherwise "am I done?" is unanswerable. That's why pagination metadata isn't decoration.

## API Error Handling & Response Design

Source: [API Error Handling & Response Design](20.3.3.02-error-handling-design.md)

**Q:** What core constraint explains why every error has a audience: machine or human. governs api error handling & response design?

**A:** The status code and machine-readable `code` field drive client branching (retry? redirect? show form error?); the human-readable `message` is for the developer debugging their integration. Conflating them — leaking stack traces to clients, or returning only prose with no code — serves neither.

**Q:** What core constraint explains why errors must be predictable shapes. governs api error handling & response design?

**A:** A client cannot handle what it can't parse; one error envelope across all endpoints (RFC 7807/9457 style) is what makes centralized handling possible.

**Q:** What core constraint explains why the error budget is part of the contract. governs api error handling & response design?

**A:** Which failures are retryable, which are permanent, which carry correlation IDs for support — these are designed decisions. An error that a client can't distinguish "wait and retry" from "give up" has failed at its one job.

## Long-Running API Operations (202 Accepted Pattern)

Source: [Long-Running API Operations (202 Accepted Pattern)](20.3.3.03-long-running-api-operations.md)

**Q:** What core constraint explains why a request-response call assumes the answer arrives before something times out. governs long-running api operations (202 accepted pattern)?

**A:** Any operation beyond ~30s violates that assumption at some layer (LB idle timeout, client timeout, connection reset) — no amount of tuning makes 2-hour jobs request-shaped.

**Q:** What core constraint explains why the fix is decoupling acceptance from completion. governs long-running api operations (202 accepted pattern)?

**A:** Return `202 Accepted` + a status resource immediately (`/operations/{id}`); completion is discovered by polling or pushed by callback/webhook. The operation becomes a *resource* — which is the REST way of representing "work in progress.".

**Q:** What core constraint explains why idempotency moves to creation. governs long-running api operations (202 accepted pattern)?

**A:** Since the client can't know if the create-request landed (timeout before response), creation needs idempotency keys; the operation itself needs checkpointing so a crashed worker resumes rather than restarts.

## File Upload APIs

Source: [File Upload APIs](20.3.3.04-file-upload-apis.md)

**Q:** What core constraint explains why app servers are the wrong place for large bytes. governs file upload apis?

**A:** They're sized for request handling, not throughput; streaming 2GB through one ties a worker for minutes. The scalable shape routes bytes *around* the app: presigned URLs direct-to-object-storage, server only brokers authorization.

**Q:** What core constraint explains why integrity needs both directions. governs file upload apis?

**A:** Client → server needs checksums (hash before upload, verify after) because TCP checksums don't catch application-level corruption; server → client needs Content-Length/Range so partial transfers are detectable and resumable.

**Q:** What core constraint explains why upload size must be a designed limit governs file upload apis?

**A:** , not an accident of framework defaults — body-size caps, storage quotas, and virus scanning are boundary controls. Every "unlimited" upload endpoint becomes an attacker's free storage.

## Webhooks

Source: [Webhooks](20.3.3.05-webhooks.md)

**Q:** What core constraint explains why the server can't hold the connection, so it calls you back. governs webhooks?

**A:** "Notify me when X happens" over request-response requires the provider to become an HTTP *client* to your endpoint — which means your endpoint is now a public surface with all the security that implies.

**Q:** What core constraint explains why delivery is at-least-once, by construction. governs webhooks?

**A:** The provider cannot know if your endpoint received its POST (your ack may be lost), so it retries — duplicates are guaranteed. Therefore consumer idempotency (event IDs) isn't optional hardening; it's the core protocol requirement.

**Q:** What core constraint explains why the consumer must verify the caller. governs webhooks?

**A:** Anyone who finds your webhook URL can POST to it — HMAC signatures over the raw body (and timestamp to block replay) are how trust is established — verified *before* processing, not after. ack fast, process async, or the provider's timeout turns your slow handler into false failures.

## Serialization & Wire Formats

Source: [Serialization & Wire Formats](20.3.3.06-serialization-and-wire-formats.md)

**Q:** What core constraint explains why bytes are the only interface. governs serialization & wire formats?

**A:** Everything else — language, runtime, ORM, type system — stops at the socket. So a serialization boundary is where type information is *lost* by default and must be re-established explicitly (a schema, a type declaration, or defensive parsing).

**Q:** What core constraint explains why a format is a position on a fixed triangle: size, speed, opacity. governs serialization & wire formats?

**A:** Optimizing size costs readability (binary), optimizing readability costs size (JSON), and no format wins all three — which is why every mature system ends up with more than one.

**Q:** What core constraint explains why every field you ship is a contract you must keep. governs serialization & wire formats?

**A:** Once a client parses `created_at`, its name, type and nullability are public API; renaming is a breaking change whether or not a schema exists.

## Transactional Email & Notification Delivery

Source: [Transactional Email & Notification Delivery](20.3.3.07-transactional-email-and-notifications.md)

**Q:** What core constraint explains why you do not control the receiving server. governs transactional email & notification delivery?

**A:** Delivery is a *negotiation* between mail servers; the final inbox/ spam decision is made by someone else's reputation system, using signals you can only influence (authentication, complaint rate, engagement).

**Q:** What core constraint explains why the failure arrives later, and out of band. governs transactional email & notification delivery?

**A:** SMTP acceptance is not delivery, and delivery is not read receipt. So the sending call cannot return the truth — which means "email sent" can only ever mean "handed to the provider".

**Q:** What core constraint explains why retries are guaranteed, deduplication is your job. governs transactional email & notification delivery?

**A:** Any at-least-once pipeline (queue, provider retry, our own retry) will duplicate work; the only defense is an idempotency key derived from the business event, not from the attempt.

## Summary

Use these prompts after the reading pass to recall the payloads errors integration mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
