<!-- section: Node.js | category: Reference | tags: revision | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Node.js-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Node.js — Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Streams

Source: [Streams](20.1.2.01-streams.md)

**Q:** Does a false write return mean the chunk was rejected?

**A:** No. The write accepted that chunk; stop issuing more writes until the destination drains. Retrying the same chunk would duplicate it.

**Q:** Why does JSON.parse(chunk) fail on a TCP stream that carries valid NDJSON?

**A:** Transport chunks can split or combine records and UTF-8 sequences. Decode incrementally, frame lines, enforce record limits, then parse each complete record.

**Q:** A chunk ends with {"id": and the next contains 1} plus a newline. When may the NDJSON parser produce a record?

**A:** After incremental decoding finds the complete line, not on the first chunk boundary. It retains partial input, validates the record bound and yields the parsed object under downstream demand; malformed/oversized input rejects and closes a started owned source.

**Q:** What changes if one queued object is enormous or the consumer ignores a false write result?

**A:** highWaterMark is a pressure threshold, not a hard memory cap. Object count does not bound object size, and ignoring pressure grows pending work. Bound both records and concurrent flows; finish still does not prove durable storage or remote receipt.

## Buffers

Source: [Buffers](20.1.2.02-buffers.md)

**Q:** Why can a two-byte view keep a much larger allocation alive?

**A:** The view shares its backing storage. Keeping the view retains that allocation or pooled slab; an independent copy can establish a smaller ownership boundary.

**Q:** Why does converting a Uint16Array directly to Buffer differ from sharing its ArrayBuffer?

**A:** Direct conversion takes element values as bytes and can truncate them. Sharing the ArrayBuffer exposes the host-endian raw bytes and requires the correct byteOffset and byteLength.

**Q:** Trace type 7 with UTF-8 payload hé split within its length header and payload.

**A:** The parser retains incomplete bytes until it has the four-byte length and complete frame. The length 4 includes one type byte plus the three payload bytes. It yields one owned copied payload; a zero length or truncated final header fails rather than being silently accepted.

**Q:** What changes when a retained two-byte subarray is copied with Buffer.from?

**A:** The subarray shares mutations and backing lifetime with the original; Buffer.from(view) copies the selected bytes, so later copy mutation does not alter the original. Validate offsets/lengths separately from establishing independent ownership.

## File System

Source: [File System](20.1.2.03-file-system.md)

**Q:** Which guarantee does staging then renaming add, and which does it leave open?

**A:** On the supported same-filesystem rename contract it can replace a pathname atomically. It does not serialize read-modify-write updates or by itself prove crash durability.

**Q:** Why does a lexical path-containment check not stop every filesystem escape?

**A:** A symlink or changed parent directory can resolve outside the root after validation. Use controlled identifiers/directories and the required platform-specific opening policy.

**Q:** What remains after replacing an owned JSON file twice, and after a serialization error before staging?

**A:** Successful same-filesystem replacement names the second complete document and cleans its temporary path. A serialization error before opening/staging leaves the prior target. Concurrent read-modify-write still needs version/serialization, and power-loss durability needs the actual filesystem protocol.

**Q:** What changes if the checked path is a symlink controlled by another actor?

**A:** Lexical containment no longer establishes the resolved file boundary. A realpath check can also race with later opening; control names/directories and use the deployed platform's required safe-open policy.

## HTTP Module

Source: [HTTP Module](20.1.2.04-http-module.md)

**Q:** Why does a raw async HTTP handler need a rejection path outside its initial call?

**A:** Its promise may reject after the callback returns. The server does not automatically await it and write an error response; the caller must own the promise and check response state.

**Q:** Why is requestTimeout not enough to bound a database query after body parsing?

**A:** It limits receipt of the incoming request. Business processing needs its own deadline and cancellation policy, with cleanup of the underlying operation.

**Q:** Trace the raw route for a valid name, malformed JSON, wrong media type and an oversized received body.

**A:** The fixture echoes only name with 200 and no persistence. The rejected route promise reaches the handler's response-owner path: malformed/non-object input gets 400, wrong content type 415 and bytes beyond the bound 413. It closes rejected connections and does not begin a second body after headers/destruction.

**Q:** What changes if an outbound URL is HTTPS but resolves to a private destination or redirects there?

**A:** TLS secures transport to the chosen destination; it does not authorize that destination. Apply the service's URL/DNS/private-network/redirect policy and byte/deadline limits at egress. Incoming requestTimeout is a separate receive limit.

## Summary

Use these prompts after the reading pass to recall the mechanism and its limits.

## See Also

- [Category reading flow](INDEX.md) — trace byte framing and parser boundaries before handling failures

## References & Learn More

The linked source chapters provide the API documentation and further reading.
