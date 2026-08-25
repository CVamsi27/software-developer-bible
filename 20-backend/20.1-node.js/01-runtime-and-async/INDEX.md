# Runtime & Async - Node.js

> **2 files.** How Node.js actually runs JavaScript: the libuv event loop — the most-asked topic in Node interviews — plus the modern Web Streams API and the built-in test runner.

[![Files](https://img.shields.io/badge/files-2-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Runtime%20%26%20Async-success)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Event Loop](20.1.1.01-event-loop.md) | Phases (timers, pending callbacks, idle/prepare, poll, check, close), microtasks vs macrotasks, `setImmediate` vs `nextTick`, blocking vs non-blocking | 30 min |
| 02 | [Web Streams & Test Runner](20.1.1.02-web-streams-and-test-runner.md) | ReadableStream/WritableStream/TransformStream (WHATWG, global in Node 18+), cross-runtime streams, `node:test`, mocking, watch mode, TAP output | 30 min |

---

[← Back to Node.js](../INDEX.md)
