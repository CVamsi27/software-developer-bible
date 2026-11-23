# AI Engineering — Index

> **Study time:** ≈ 1 h 31 m of reading (8 files, ~11 min average).
> **Building products with language models** — this track focuses on application architecture, retrieval, evaluation, serving, and governance rather than model training. Learn the mechanisms in order, then practice explaining their trade-offs with evidence from systems you have actually worked on.

[![Files](https://img.shields.io/badge/files-8-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Read the track in this order

Start by framing the model as a probabilistic dependency inside an ordinary application. Then follow a request through context selection, retrieval, orchestration, serving, and governance. Each chapter adds a boundary the previous one relies on.

| Step | Read | Be ready to explain |
| ---- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| 1 | [LLM App Architecture](20.12.01-llm-app-architecture.md) | When a problem calls for prompting, retrieval, or tuning; where validation and authorization belong |
| 2 | [Prompts, Context & Evals](20.12.02-prompts-context-evals.md) | How to budget a serialized request and measure quality, refusal, cost, and latency |
| 3 | [Retrieval Quality: Hybrid Search & Reranking](20.12.03-retrieval-quality-hybrid-search-reranking.md) | How lexical/vector candidates, fusion, reranking, chunking, and tenant filters shape evidence quality |
| 4 | [Agent Orchestration Patterns](20.12.04-agent-orchestration-patterns.md) | How application code bounds tool use, state, side effects, and recovery |
| 5 | [Serving Models: Hosted vs Self-Hosted](20.12.05-serving-models-hosted-vs-self-hosted.md) | How quality, total cost, latency, data handling, and operations decide the serving path |
| 6 | [Safety, Cost & Governance](20.12.06-safety-cost-governance.md) | How to enforce egress, authorization, budget, review, and audit controls |
| — | [Revision](REVISION.md) | Recall the mechanism and failure boundary for each chapter before timed practice |
| 7 | [Interview Questions](20.12.07-interview-questions.md) | How to state a design decision, its failure boundary, and the evidence that would change it |

## Choose Your First Pass

For an interactive document assistant, begin with architecture → prompts/evals → retrieval. Add orchestration when the feature needs tools or multi-step work. Before designing provider egress or fallback chains, read governance and serving. Use the [separate Revision](REVISION.md) to retrieve mechanisms from memory, then practice trade-offs in the interview bank.

## The Production Stack in One Diagram

```text
Client ──► API gateway ──► AI service layer ──► Provider SDK (streaming)
                │               ├── prompt assembly (+ RAG context)
                │               ├── controls: data-class policy · cost budget · rate limit
                │               ├── fallback: cached response → smaller model → graceful degrade
                │               └── observability: token/cost/latency metrics, trace per call
                └── feature flag / kill switch (tested for every provider egress path)
```

---

## Docita Anchor

Inspect these [Docita](https://github.com/CVamsi27/docita) modules to see how the patterns in this track look inside a real codebase (verify current deployed configuration and tests before citing production behavior):

| Topic | Docita evidence |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Kill-switched provider access | `apps/api/src/shared/modules/ai/openai.service.ts` — `AI_EXTERNAL_ENABLED=false` skips constructing any client; responses cached |
| Structured clinical output | `apps/api/src/shared/modules/ai/clinical-ai.service.ts` — prescription analysis normalized through typed normalizers |
| OCR extraction pipeline | `apps/api/src/shared/modules/ai/ocr-extraction.service.ts` — local OCR path available; optional cloud vision is configuration-gated |
| Cost governance | `apps/api/src/shared/modules/ai/ai-credit-guard.service.ts` — per-clinic credit allotment and exhaustion enforcement |
| Streaming chat | `apps/api/src/shared/modules/ai/ask-ai.service.ts` — history-aware streamed responses |

## Cross-references

- Your working example: Docita AI module — env kill-switch (`AI_EXTERNAL_ENABLED`), response caching, streaming generators, credit guard ([80.21 §Q22](../../80-lanes-abroad-full-stack/80.21-docita-google-level-prep.md))
- [Microservices resilience](../20.6-microservices/INDEX.md) applies directly (circuit breakers and timeouts around external providers)
- For a domain-specific AI role (such as geospatial or clinical AI), map these mechanisms onto the role's actual data pipeline and product constraints

---

## Navigation

[← Previous: Microservices](../20.6-microservices/INDEX.md) · [ Back to Index](../../INDEX.md)
