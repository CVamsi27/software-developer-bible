<!-- section: AI Engineering | category: Reference | tags: revision -->
[![Section](https://img.shields.io/badge/section-AI%20Engineering-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-orange)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

# AI Engineering — Revision

Explain each failure boundary before opening the source chapter. The [interview bank](20.12.07-interview-questions.md) is a separate drill for concise design answers.

## LLM App Architecture

Source: [LLM App Architecture](20.12.01-llm-app-architecture.md).

**Q:** Why must an agent preserve the assistant's tool-call message before appending the tool result?

**A:** The provider protocol associates results with call identities. A free-form result without its preceding call loses that association, especially when several calls are returned together.

**Q:** A slow SSE client makes `res.write` return false. What should the producer wait for, and what must end that wait on disconnect?

**A:** Wait for response `drain` while observing a cancellation signal. A response transport close/deadline should abort the wait and propagate to the provider adapter; request-body completion is a different event.

## Prompts, Context and Evals

Source: [Prompts, Context and Evals](20.12.02-prompts-context-evals.md).

**Q:** Why can counting only the question and document text still exceed the context window?

**A:** Message framing, instructions, tool definitions, schemas, history, and reserved output tokens also consume capacity. Count the actual serialized request for the selected model and leave a conservative output reserve.

**Q:** Why is the word “cannot” in an answer insufficient evidence of a safe refusal?

**A:** The answer may still provide the prohibited assistance. Evaluate the whole output against the task-specific refusal/forbidden-content contract, with human-calibrated adversarial cases.

## Retrieval Quality

Source: [Retrieval Quality](20.12.03-retrieval-quality-hybrid-search-reranking.md).

**Q:** Why should a vector candidate query select its ordered LIMIT before assigning fusion ranks?

**A:** The candidate set must be the nearest eligible results, not an arbitrary subset with window ranks attached. The direct distance ORDER BY/LIMIT also matters to the ANN index plan; inspect EXPLAIN and filtered recall.

**Q:** A harness reranks only six results but reports recall@10. What needs to change?

**A:** Request at least ten final candidates for that metric or report recall@6. Label the stage being evaluated, deduplicate identities, and reject cases with no relevant labels rather than dividing by zero.

## Agent Orchestration

Source: [Agent Orchestration](20.12.04-agent-orchestration-patterns.md).

**Q:** Why must invalid or repeated tool proposals consume the max-step budget?

**A:** Each proposal still requires an inference call. Counting only executed tools lets repeated/invalid turns bypass the intended loop bound and keep spending.

**Q:** Does running an MCP stdio server make its tools sandboxed?

**A:** No. It launches a subprocess with inherited permissions unless the host applies separate isolation. Review its trusted command configuration, capabilities, authorization, and filesystem/network access.

## Serving Models

Source: [Serving Models](20.12.05-serving-models-hosted-vs-self-hosted.md).

**Q:** Why does fitting a model's weights in GPU memory not prove the target concurrency fits?

**A:** Concurrent sequences also need KV cache, activations, runtime buffers, and headroom. Calculate consistent GB/GiB units, account for sharding/quantization, and load-test realistic context/output lengths.

**Q:** Is an endpoint called “EU” or “self-hosted” enough to authorize sensitive-data routing?

**A:** No. Verify the actual approved data classes, processing/access regions, subprocessors, retention, transfer obligations, and deployment controls. Apply that policy before availability-based fallback.

## Safety, Cost and Governance

Source: [Safety, Cost and Governance](20.12.06-safety-cost-governance.md).

**Q:** Why can role separation and schema-valid output still leave prompt injection dangerous?

**A:** Untrusted text can influence a model to request a well-formed but unauthorized action. Deterministic tool/data-access authorization and least privilege enforce authority; prompts and serialization only help the model interpret data.

**Q:** What race does a conditional atomic budget update avoid, and what accounting remains afterward?

**A:** It rejects admission before concurrent reservations exceed the cap, without a separate over-limit increment/compensation race. Actual-cost settlement still needs a durable request/day reservation, bounded provider usage, and exactly-once release of unused funds.

## Summary

Assess state, authority, cost, and recovery at explicit boundaries. An eval pass or a guardrail is evidence for its tested contract, not a blanket accuracy, privacy, or compliance guarantee.

## See Also

- [Reading flow](INDEX.md) — choose a workload-specific pass.
- [Interview bank](20.12.07-interview-questions.md) — explain the trade-offs aloud.

## References & Learn More

The linked source chapters contain the technical sources for these review answers.
