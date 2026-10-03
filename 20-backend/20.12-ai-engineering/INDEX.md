# AI Engineering — Index

> **Study time:** ≈ 1 h 29 m of reading (8 files, ~11 min average).
> **Building products WITH LLMs** — not model training. This is the 2025+ interview differentiator: RAG architecture, streaming, structured output, evals, and production governance (cost + safety). Relevant interviews may probe these mechanisms; your Docita AI-kill-switch story lives here.

[![Files](https://img.shields.io/badge/files-8-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Topic Categories

The 7 content files classify into 4 conceptual categories + drills — a route through architecture, quality, orchestration, and governance.

| Category | Files | Why it matters |
| -------------------- | ----: | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Architecture** | 2 | LLM app architecture (RAG vs fine-tuning vs prompting, streaming, function calling) + serving strategy (hosted vs self-hosted, vLLM, quantization) |
| **Orchestration** | 1 | Agent orchestration — ReAct loops, budgets/guards, multi-agent topologies, trajectory evals |
| **Quality** | 2 | Prompts/context/evals + retrieval quality (hybrid search, reranking) — how you *prove* the thing works |
| **Governance** | 1 | Safety, cost, PII, kill-switches — the regulated-domain story |
| **Interview Drills** | 1 | 25+ Q&A with follow-up traps |

---

## Study Order

| # | File | You can defend… | Role priority | General importance |
| --- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ------------------ |
| 1 | [LLM App Architecture](20.12.01-llm-app-architecture.md) | RAG vs fine-tuning vs prompting; embeddings; streaming; function calling | Important | Specialized |
| 2 | [Prompts, Context & Evals](20.12.02-prompts-context-evals.md) | Prompt structure, context-window budgeting, how to prove quality (evals) | Important | Specialized |
| 3 | [Retrieval Quality: Hybrid Search & Reranking](20.12.03-retrieval-quality-hybrid-search-reranking.md) | Why pure vector fails; hybrid BM25+vector fusion (RRF); rerankers; HNSW/IVF; chunking; recall@k/MRR harness; pgvector hybrid example | Important | Specialized |
| 4 | [Agent Orchestration Patterns](20.12.04-agent-orchestration-patterns.md) | ReAct plan-act-observe loops; state machines vs graph orchestration; tool-calling (parallel/chained); step/token budgets + circuit breakers; supervisor/debate/handoff topologies; memory tiers; trajectory evals | Important | Specialized |
| 5 | [Serving Models: Hosted vs Self-Hosted](20.12.05-serving-models-hosted-vs-self-hosted.md) | Decision matrix (cost/latency/residency/control); vLLM PagedAttention + continuous batching; quantization ladder; VRAM math; TTFT/TPOT; provider routing/fallback; EU-GDPR hybrid pattern | Important | Specialized |
| 6 | [Safety, Cost & Governance](20.12.06-safety-cost-governance.md) | Kill-switches, spend guards, PII redaction, human-in-the-loop — the regulated-domain story | Important | Specialized |
| 7 | [Interview Questions](20.12.07-interview-questions.md) | 25+ Q&A with follow-up traps | Important | Specialized |

## Choose Your First Pass

For an interactive docs feature, read architecture → prompts/evals → retrieval. For tool-driven workflows, add orchestration. Before any provider egress, read governance and serving policy. Then use the [separate Revision](REVISION.md) to explain mechanisms from memory and the interview bank for spoken trade-off answers.

## The Decision Map

```text
Task needs world knowledge you don't have? → RAG (retrieval + grounding)
Task is narrow/repetitive/format-fixed? → Prompting + structured output
Task needs a behavior/style no model has? → Fine-tune LAST (data + cost + ops burden)
Output feeds code/DB/UI? → JSON schema / function calling — never parse prose
Regulated data involved? → Governance layer FIRST (see file 6)
```

## The Production Stack in One Diagram

```text
Client ──► API gateway ──► AI service layer ──► provider SDK (streaming)
                │ │ ├── prompt assembly (+RAG context)
                │ │ ├── guardrails: PII gate · cost meter · rate limit
                │ │ └── fallback: cached response → smaller model → degrade gracefully
                │ └── observability: token/cost/latency metrics, trace per completion
                └── feature flag / KILL SWITCH (default-off for regulated data)
```

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Kill-switched provider access | `apps/api/src/shared/modules/ai/openai.service.ts` - `AI_EXTERNAL_ENABLED=false` constructs no client at all; responses cached |
| Structured clinical output | `apps/api/src/shared/modules/ai/clinical-ai.service.ts` - prescription analysis normalized through typed normalizers |
| OCR extraction pipeline | `apps/api/src/shared/modules/ai/ocr-extraction.service.ts` - vision-based field extraction with per-field confidence |
| Cost governance | `apps/api/src/shared/modules/ai/ai-credit-guard.service.ts` - per-clinic credit allotment/exhaustion enforcement |
| Streaming chat | `apps/api/src/shared/modules/ai/ask-ai.service.ts` - history-aware streamed responses |

RAG/vector retrieval: _no direct docita implementation yet_ — governance-first AI is the pattern this stack teaches.

## Cross-references

- Your working example: Docita AI module — env kill-switch (`AI_EXTERNAL_ENABLED`), response caching, streaming generators, credit guard ([80.21 §Q22](../../80-lanes-abroad-full-stack/80.21-docita-google-level-prep.md))
- [Microservices resilience](../20.6-microservices/INDEX.md) applies directly (circuit breakers around providers)
- LiveEO angle: GeoAI/optical-SAR fusion is their SPRIND frontier — architecture literacy transfers

---

## Navigation

[← Previous: Microservices](../20.6-microservices/INDEX.md) · [ Back to Index](../../INDEX.md)
