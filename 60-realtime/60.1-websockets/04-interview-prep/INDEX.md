# WebSockets Interview Prep

> **Study time:** ≈ 46 min of reading (1 files, ~46 min average).
> **1 file.** The curated question bank for real-time rounds — protocol trade-offs, scaling designs, authentication, reconnection semantics, and failure modes.

[![Files](https://img.shields.io/badge/files-1-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Real--Time-%2300b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## The file

| # | File | Contents | Time | Role priority | General importance |
| --: | ------ | ---------- | ------ | --- | --- |
| 01 | [Interview Questions](60.1.4.01-interview-questions.md) | 50+ curated questions with answers | 2-3 hrs | Important | Specialized |

---

## Questions you will be ready for

- "WebSocket vs SSE — when to use which?"
- "How do you scale WebSockets across multiple servers?"
- "How do you authenticate WebSocket connections?"
- "What's the difference between Socket.IO and raw WebSockets?"
- "How do you handle reconnection and message ordering?"

---

## How to use it

Real-time rounds reward the ability to explain a design as well as recall APIs. Before drilling answers, draw how one event reaches many clients: load balancer → WebSocket gateway instances → Redis adapter that shares events between instances → persistent storage.

---

## Cross-References

- [System Design case studies](../../../30-architecture/30.2-system-design/02-case-studies/INDEX.md) — WhatsApp/chat system designs.
- [Coding Patterns interview bank](../../../70-interview-toolkit/70.2-coding-patterns/INDEX.md) — the algorithmic counterpart.

---

## Navigation

[← Frameworks & Paradigms](../03-frameworks-and-paradigms/INDEX.md) · [↑ WebSockets Home](../INDEX.md)
