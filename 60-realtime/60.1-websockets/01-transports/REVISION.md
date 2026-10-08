<!-- section: WebSockets | category: Reference | tags: revision, practice | role-priority: important | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-WebSockets-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../../docs/topic-importance.md)

# WebSockets — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## WebSockets Overview

Source: [WebSockets Overview](60.1.1.01-websockets-overview.md)

**Q:** What delivery does a live WebSocket provide, and what recovery is missing?

**A:** Frames ride an ordered reliable live transport, but reconnects do not automatically replay missed application messages or deduplicate effects. Define IDs, acknowledgments, retention, and replay where needed.

**Q:** Does the HTTP upgrade establish a TCP connection that did not previously exist?

**A:** No. The HTTP/1.1 upgrade happens on an existing connection. A successful protocol handshake is also not user authentication; authorization remains a separate application decision.

**Q:** Why does the echo fixture check both readyState and pending bytes before replying?

**A:** Sending requires an open channel, and pending work must remain bounded. The send callback describes local progress/error, not a durable business acknowledgment. A slow peer triggers the fixture's termination policy.

**Q:** Why can an origin allowlist not identify a trusted user?

**A:** Browsers supply an Origin header, but non-browser clients can supply their own. Validate the application session and authorize rooms/actions independently; do not equate origin acceptance with permission.

## Server-Sent Events (SSE)

Source: [Server-Sent Events (SSE)](60.1.1.02-server-sent-events.md)

**Q:** Why does Last-Event-ID not itself recover a missed SSE event?

**A:** It gives the server a cursor. The server must retain events, authorize replay, detect expired cursors, and send the right continuation or resynchronization response.

**Q:** Trace the local SSE fixture after the browser applies ID 2, the connection closes and ID 3 is published before reconnection.

**A:** The same EventSource reconnects with Last-Event-ID 2. The server validates that cursor and replays retained records greater than 2, then subscribes the response to live publications without an asynchronous gap in this single-process fixture.

**Q:** What changes when that cursor is older than retained history?

**A:** The server emits reset instead of silently skipping updates. The client closes the source and requests a reload for current state. This temperature display can use a latest snapshot; an every-event consumer needs a durable recovery contract.

**Q:** Why does a false Node response write not justify an unbounded pending queue?

**A:** It indicates local buffered pressure, not a client acknowledgment. The fixture disconnects the slow consumer; recovery remains limited to retained history. Waiting for drain, coalescing or durable replay require explicit bounded policies.

**Q:** Does the browser's remembered event ID prove the application applied a database effect?

**A:** No. It is a transport replay cursor. Handler validation, application processing and durable acknowledgment are separate. The display validates and applies before updating its own deduplication cursor.

## Socket.io

Source: [Socket.io](60.1.1.03-socket-io.md)

**Q:** Why does Socket.IO polling need affinity while a WebSocket-only session does not?

**A:** Polling spans separate HTTP requests that must reach the node owning the Engine.IO session. A single live WebSocket remains on its selected backend after the handshake.

**Q:** What do acknowledgments still leave unspecified?

**A:** Define limits on retries, where messages are stored safely, how duplicates are recognized, how clients recover after reconnecting, and whether an acknowledgment means the business operation committed. The application must state these rules explicitly.

**Q:** A write commits, but its acknowledgment is lost. What happens if the client retries?

**A:** The server can receive the command again. Use a durable operation identity and an atomic duplicate-effect check, or reconcile the authoritative result. Socket.IO's ordering and reconnection features do not make the business write execute exactly once.

## WebTransport

Source: [WebTransport](60.1.1.04-webtransport.md)

**Q:** When do WebTransport datagrams solve a problem reliable streams cannot?

**A:** When obsolete data should be discarded rather than retransmitted, such as fresh game positions. Reliable ordered streams remain useful for commands/state that must arrive intact.

**Q:** Why does receiving position 4 after losing position 3 work only for some protocols?

**A:** A full snapshot replaces older state without needing position 3. A delta based on position 3 cannot reconstruct the same result; it needs recovery or reliable delivery.

**Q:** Why can a reliable stream return half a JSON record in one read?

**A:** It preserves an ordered byte sequence, not the sender’s write boundaries. Buffer and decode incrementally until the application’s bounded framing rule identifies a complete record.

**Q:** Does QUIC migration cause transport.ready to fire again?

**A:** No. ready is a promise for establishment, not a repeated event. If the session actually closes, create a new one and restore state within a new epoch or cursor domain.

**Q:** Does a successful stream write prove a chat message was stored?

**A:** No. It reports the local write operation, not a durable server effect. Define and observe an acknowledgment whose meaning includes the required business result.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
