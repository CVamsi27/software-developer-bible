# AI Engineering — Index

> **Building products WITH LLMs** — not model training. This is the 2025+ interview differentiator: RAG architecture, streaming, structured output, evals, and production governance (cost + safety). Every senior full-stack loop now touches this; your Docita AI-kill-switch story lives here.

[![Files](https://img.shields.io/badge/files-5-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Topic Categories

The 4 content files classify into 3 conceptual categories + drills — the "GoF classification" of AI engineering.

| Category | Files | Why it matters |
|----------|------:|----------------|
| **Architecture** | 1 | LLM app architecture — RAG vs fine-tuning vs prompting, streaming, function calling |
| **Quality** | 1 | Prompts, context budgeting, evals — how you *prove* the thing works |
| **Governance** | 1 | Safety, cost, PII, kill-switches — the regulated-domain story |
| **Interview Drills** | 1 | 25+ Q&A with follow-up traps |

---

## Study Order

| # | File | You can defend… |
|---|------|-----------------|
| 1 | [LLM App Architecture](20.12.01-llm-app-architecture.md) | RAG vs fine-tuning vs prompting; embeddings; streaming; function calling |
| 2 | [Prompts, Context & Evals](20.12.02-prompts-context-evals.md) | Prompt structure, context-window budgeting, how to prove quality (evals) |
| 3 | [Safety, Cost & Governance](20.12.03-safety-cost-governance.md) | Kill-switches, spend guards, PII redaction, human-in-the-loop — the regulated-domain story |
| 4 | [Interview Questions](20.12.04-interview-questions.md) | 25+ Q&A with follow-up traps |

## The Decision Map (memorize)

```text
Task needs world knowledge you don't have? → RAG (retrieval + grounding)
Task is narrow/repetitive/format-fixed? → Prompting + structured output
Task needs a behavior/style no model has? → Fine-tune LAST (data + cost + ops burden)
Output feeds code/DB/UI? → JSON schema / function calling — never parse prose
Regulated data involved? → Governance layer FIRST (see file 3)
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

## Cross-references

- Your working example: Docita AI module — env kill-switch (`AI_EXTERNAL_ENABLED`), response caching, streaming generators, credit guard ([80.21 §Q22](../../80-lanes-abroad-full-stack/80.21-docita-google-level-prep.md))
- [Microservices resilience](../20.6-microservices/INDEX.md) applies directly (circuit breakers around providers)
- LiveEO angle: GeoAI/optical-SAR fusion is their SPRIND frontier — architecture literacy transfers

---

## Navigation

[← Previous: Microservices](../20.6-microservices/INDEX.md) · [ Back to Index](../../INDEX.md)
