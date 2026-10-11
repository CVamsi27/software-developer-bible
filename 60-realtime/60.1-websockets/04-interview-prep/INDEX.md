# WebSockets Interview Prep

> **Study time:** ≈ 8 min of reading (1 file, ~8 min average).
> **1 file.** The curated question bank for real-time rounds — protocol trade-offs, scaling designs, authentication, reconnection semantics, and failure modes.

[![Files](https://img.shields.io/badge/files-1-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Real--Time-%2300b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## The file

| # | File | Contents | Practice time | Role priority | General importance |
| --: | ------ | ---------- | ------ | --- | --- |
| 01 | [Interview Questions](60.1.4.01-interview-questions.md) | 30 authored questions and their follow-ups | 2-3 hours for worked answers | Important | Specialized |

---

## Questions to Practice

- "WebSocket vs SSE — when to use which?"
- "How do you scale WebSockets across multiple servers?"
- "How do you authenticate WebSocket connections?"
- "What's the difference between Socket.IO and raw WebSockets?"
- "How do you handle reconnection and message ordering?"

---

## How to use it

Real-time rounds reward the ability to explain a design as well as recall APIs. Before drilling, complete the [transport revision](../01-transports/REVISION.md), [architecture revision](../02-architecture-and-scaling/REVISION.md) and [framework revision](../03-frameworks-and-paradigms/REVISION.md). Then trace an authorized command → durable state/outbox → publication → interested gateways → clients. Explain recovery and uncertain acknowledgments before naming products.

---

## Cross-References

- [System Design case studies](../../../30-architecture/30.2-system-design/02-case-studies/INDEX.md) — WhatsApp/chat system designs.
- [Coding Patterns interview bank](../../../70-interview-toolkit/70.2-coding-patterns/INDEX.md) — the algorithmic counterpart.

---

## Navigation

[← Frameworks & Paradigms](../03-frameworks-and-paradigms/INDEX.md) · [↑ WebSockets Home](../INDEX.md)
