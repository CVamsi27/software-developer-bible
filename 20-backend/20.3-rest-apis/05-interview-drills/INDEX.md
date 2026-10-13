# Interview Drills - REST APIs

> **Study time:** ≈ 9 min of reading (1 file, ~9 min average).
> **1 file.** Curated Q&A to close the loop on the full REST/API stack.

[![Files](https://img.shields.io/badge/files-1-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Interview%20Drills-blue)](../INDEX.md)

---

## Practice Flow

Read the four category revision companions first: [design](../01-design-and-contract/REVISION.md), [HTTP mechanics](../02-http-mechanics/REVISION.md), [payloads and integrations](../03-payloads-errors-integration/REVISION.md), and [edge and scale](../04-edge-and-scale/REVISION.md). Then answer the ten deep-dive questions aloud and use the fifty-question bank to vary one condition per answer. Cite project evidence only after inspecting the current implementation and tests.

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| :---: | ------------------------------------------------------- | -------------------------------------------------------------------------- | ------------- | ------------------ | --------: |
| 01 | [Interview Questions](20.3.5.01-interview-questions.md) | Curated Q&A across design, HTTP mechanics, payloads/errors, edge and scale | Essential | Foundational | 9 min |

---

[← Back to REST APIs](../INDEX.md)

---

## Docita Anchor

These [Docita](https://github.com/CVamsi27/docita) healthcare-application pointers identify places to inspect before citing project evidence. They do not establish current deployment, correctness or personal ownership by themselves:

| Drill | Docita evidence |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------- |
| "Offset vs cursor pagination?" | `apps/api/src/shared/common/pagination.helper.ts` - keyset implementation to walk through |
| "Make POST retries safe" | `apps/api/src/shared/modules/idempotency/idempotency.interceptor.ts` - header-driven replay window |
| "Design webhook delivery" | `apps/api/src/shared/modules/webhooks/outgoing/outgoing-webhook.service.ts` - signing + retry/backoff in one service |

---

[← Previous: Edge & Scale](../04-edge-and-scale/INDEX.md)
