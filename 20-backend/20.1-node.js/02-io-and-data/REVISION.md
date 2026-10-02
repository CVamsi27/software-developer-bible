<!-- section: Node.js | category: Reference | tags: revision -->
[![Section](https://img.shields.io/badge/section-Node.js-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

# Node.js — Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Streams

Source: [Streams](20.1.2.01-streams.md)

**Q:** Does a false write return mean the chunk was rejected?

**A:** No. The write accepted that chunk; stop issuing more writes until the destination drains. Retrying the same chunk would duplicate it.

**Q:** Why does JSON.parse(chunk) fail on a TCP stream that carries valid NDJSON?

**A:** Transport chunks can split or combine records and UTF-8 sequences. Decode incrementally, frame lines, enforce record limits, then parse each complete record.

## Buffers

Source: [Buffers](20.1.2.02-buffers.md)

**Q:** Why can a two-byte view keep a much larger allocation alive?

**A:** The view shares its backing storage. Keeping the view retains that allocation or pooled slab; an independent copy can establish a smaller ownership boundary.

**Q:** Why does converting a Uint16Array directly to Buffer differ from sharing its ArrayBuffer?

**A:** Direct conversion takes element values as bytes and can truncate them. Sharing the ArrayBuffer exposes the host-endian raw bytes and requires the correct byteOffset and byteLength.

## File System

Source: [File System](20.1.2.03-file-system.md)

**Q:** Which guarantee does staging then renaming add, and which does it leave open?

**A:** On the supported same-filesystem rename contract it can replace a pathname atomically. It does not serialize read-modify-write updates or by itself prove crash durability.

**Q:** Why does a lexical path-containment check not stop every filesystem escape?

**A:** A symlink or changed parent directory can resolve outside the root after validation. Use controlled identifiers/directories and the required platform-specific opening policy.

## HTTP Module

Source: [HTTP Module](20.1.2.04-http-module.md)

**Q:** Why does a raw async HTTP handler need a rejection path outside its initial call?

**A:** Its promise may reject after the callback returns. The server does not automatically await it and write an error response; the caller must own the promise and check response state.

**Q:** Why is requestTimeout not enough to bound a database query after body parsing?

**A:** It limits receipt of the incoming request. Business processing needs its own deadline and cancellation policy, with cleanup of the underlying operation.

## Summary

Use these prompts after the reading pass to recall the mechanism and its limits.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide the API documentation and further reading.
