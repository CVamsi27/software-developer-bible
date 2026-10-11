# Interview Prep — Design Patterns

> **Study time:** ≈ 7 min of reading (1 file, ~7 min average).
> **1 file, 50 curated questions with answers.** The pattern catalog is only useful if you can recall and apply it under pressure. This is the drill.

[![Files](https://img.shields.io/badge/files-1-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## What's here

A curated Q&A bank covering the patterns in [creational](../02-creational/INDEX.md), [structural](../03-structural/INDEX.md), [behavioral](../04-behavioral/INDEX.md), and [architectural](../05-architectural/INDEX.md), plus low-level design (LLD) problems about classes and their interactions. Define the behavior first, then apply a pattern where its contract helps.

---

## Practice in passes

1. Start with the contract questions. Explain one operation before naming its class roles.
2. Compare neighboring intentions, then reason about lifetime, failures and performance.
3. Use the system scenarios to add persistence, concurrency and delivery mechanisms to the local pattern choices.
4. Defend the design against one changed requirement, using the follow-up questions.

The [question bank](30.1.6.01-interview-questions.md) supplies prompts and concise answers. Category `REVISION.md` files check recall of their learning chapters; this bank is the separate interview drill. Review weak answers through their source chapter, then try a fresh scenario rather than treating a completed bank as an interview-readiness guarantee.

---

## Navigation

[← Architectural Patterns](../05-architectural/INDEX.md) · [↑ Design Patterns Home](../INDEX.md)

---

## Docita Anchor

Concrete source pointers in [docita](https://github.com/CVamsi27/docita) — the hospital-management NestJS monorepo — supply examples to inspect. A registry is not an untrusted-plugin sandbox, and the pointers do not establish production readiness.

| Topic | Docita evidence |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| "Design a plugin system" → Strategy + Registry | `search-strategy.registry.ts`, `bulk-import-strategy.registry.ts` with per-entity strategy files |
| "Builder for complex documents" → Builder | `fhir/factories/observations/builders/*.builder.ts` composing FHIR observations |
| "Product creation" → factory techniques | `fhir/factories/*`, `analytics/core/factories/*`, `payment-gateway.factory.ts` |
| "Template Method pipeline" → base-class skeleton | `base-pdf.service.ts` PDF generation, `base-websocket.gateway.ts` realtime, `base-pdf.processor.ts` queue jobs |
| "Facade over a subsystem" → Facade | `ocr-facade.service.ts` (OCR pipeline), `templates-facade.service.ts` (WhatsApp templates) |
| "Repository + DI for testability" → Repository | `base.repository.ts` + DI-token binding checked by `check-repository-di-tokens.mjs` |
