# Real-Time Stack

> **WebSockets, SSE, real-time architecture** — optional stack, study when a JD demands it. Shared by both lanes.

[![Files](https://img.shields.io/badge/files-8-blue)](../INDEX.md)

| Section | Files | Topics |
|---------|------:|--------|
| [WebSockets](60.1-websockets/INDEX.md) | 8 | Protocol deep-dive, Socket.IO, SSE, real-time architecture, NestJS gateways, WebTransport, scaling patterns, interview questions |

## The 60-Second Orientation

```text
Need server→client push only?        → SSE (auto-reconnect, Last-Event-ID)
Need bidirectional (chat/collab)?    → WebSockets (Socket.IO for rooms/fallbacks)
Need it behind serverless/edge?      → managed pub/sub + polling fallback first
Scaling beyond one node?             → Redis adapter / sticky sessions → pub/sub backbone
```

**Cross-references:** [Microservices & event-driven patterns](../20-backend/20.6-microservices/INDEX.md) · [NestJS](../20-backend/20.2-nestjs/INDEX.md)

---

**Lane-specific overlays:** Add interview strategy context, behavioral stories, and prep plans in [Interview Lanes](../80-lanes-abroad-full-stack/INDEX.md) — the stacks stay stack-pure.
