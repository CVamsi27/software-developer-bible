# Interview Prep — Design Patterns

> **Study time:** ≈ 26 min of reading (1 files, ~26 min average).
> **1 file, 50+ curated questions with answers.** The pattern catalog is only useful if you can recall and apply it under pressure. This is the drill.

[![Files](https://img.shields.io/badge/files-1-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## What's here

A curated Q&A bank covering the patterns in [creational](../02-creational/INDEX.md), [structural](../03-structural/INDEX.md), [behavioral](../04-behavioral/INDEX.md), and [architectural](../05-architectural/INDEX.md) — plus classic LLD design problems you solve by applying patterns.

---

## File Index

### [Design Pattern Interview Questions](30.1.6.01-interview-questions.md)
50+ questions across three difficulty levels:
- **Easy** (10-15 Qs): definition, intent, when to use
- **Medium** (20-25 Qs): tradeoffs, comparisons, code-level decisions
- **Hard** (15-20 Qs): apply patterns to LLD scenarios, anti-patterns, production failure modes

Includes a final section on **classic LLD problems** (parking lot, URL shortener, elevator system, chess, hotel reservation) and which patterns each one calls for.

---

## How to use this

1. **First pass:** read the question, say the answer out loud in 30 seconds.
2. **Second pass:** write a 2-paragraph answer in your own words.
3. **Third pass:** with a peer, time-box yourself at 2 min per question.

If you can answer the Hard section cold, you are ready for a senior-level patterns interview.

---

## Navigation

[← Architectural Patterns](../05-architectural/INDEX.md) · [↑ Design Patterns Home](../INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS (NestJS monorepo) — gives me true stories for these answers.

| Topic | Docita evidence |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| "Design a plugin system" → Strategy + Registry | `search-strategy.registry.ts`, `bulk-import-strategy.registry.ts` with per-entity strategy files |
| "Builder for complex documents" → Builder | `fhir/factories/observations/builders/*.builder.ts` composing FHIR observations |
| "Factory families" → Factory Method | `fhir/factories/*`, `analytics/core/factories/*`, `payment-gateway.factory.ts` |
| "Template Method pipeline" → base-class skeleton | `base-pdf.service.ts` PDF generation, `base-websocket.gateway.ts` realtime, `base-pdf.processor.ts` queue jobs |
| "Facade over a subsystem" → Facade | `ocr-facade.service.ts` (OCR pipeline), `templates-facade.service.ts` (WhatsApp templates) |
| "Repository + DI for testability" → Repository | `base.repository.ts` + DI-token binding enforced by `check-repository-di-tokens.mjs` |
