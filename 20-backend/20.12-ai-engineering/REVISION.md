<!-- section: AI Engineering | category: Reference | tags: revision | role-priority: important | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-AI%20Engineering-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-orange)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)

# AI Engineering — Revision

Explain each failure boundary before opening the source chapter. The [interview bank](20.12.07-interview-questions.md) is a separate drill for concise design answers.

## LLM App Architecture

Source: [LLM App Architecture](20.12.01-llm-app-architecture.md).

**Q:** Why must an agent preserve the assistant's tool-call message before appending the tool result?

**A:** The provider protocol associates results with call identities. A free-form result without its preceding call loses that association, especially when several calls are returned together.

**Q:** A slow SSE client makes `res.write` return false. What should the producer wait for, and what must end that wait on disconnect?

**A:** Wait for response `drain` while observing a cancellation signal. A response transport close or deadline should abort the wait and propagate to the provider adapter; request-body completion is a different event.

## Prompts, Context and Evals

Source: [Prompts, Context and Evals](20.12.02-prompts-context-evals.md).

**Q:** Why can counting only the question and document text still exceed the context window?

**A:** Message framing, instructions, tool definitions, schemas, history, and reserved output tokens also consume capacity. Count the actual serialized request for the selected model and leave a conservative output reserve.

**Q:** Why cap the raw model response before parsing JSON?

**A:** Schema and field limits apply only after parsing. A byte limit prevents an oversized response from consuming unbounded parsing and validation work.

**Q:** Why is the word "cannot" in an answer insufficient evidence of a safe refusal?

**A:** The answer may still provide the prohibited assistance. Evaluate the whole output against the task-specific refusal and forbidden-content contract, with human-calibrated adversarial cases.

## Retrieval Quality

Source: [Retrieval Quality](20.12.03-retrieval-quality-hybrid-search-reranking.md).

**Q:** Why should a vector candidate query select its ordered `LIMIT` before assigning fusion ranks?

**A:** The candidate set must be the nearest eligible results, not an arbitrary subset with window ranks attached. The direct distance `ORDER BY` and `LIMIT` also matters to the approximate nearest neighbor (ANN) index plan; inspect `EXPLAIN` and filtered recall.

**Q:** A harness reranks only six results but reports `recall@10`. What needs to change?

**A:** Request at least ten final candidates for that metric or report `recall@6`. Label the stage being evaluated, deduplicate identities, and reject cases with no relevant labels rather than dividing by zero.

## Agent Orchestration

Source: [Agent Orchestration](20.12.04-agent-orchestration-patterns.md).

**Q:** Why must invalid or repeated tool proposals consume the max-step budget?

**A:** Each proposal still requires an inference call. Counting only executed tools lets repeated or invalid turns bypass the intended loop bound and keep spending.

**Q:** What should an engineer verify when upgrading a Model Context Protocol (MCP) integration to a newer protocol revision?

**A:** Pin and inspect both specification and software development kit (SDK), then test transport, state, discovery, cancellation, and backward compatibility. The `2026-07-28` revision uses stateless requests over standard `stdio` or Streamable HTTP; elicitation uses a multi-round-trip `input_required` result rather than server-initiated JSON-RPC. Older peers can follow different rules. The host must authorize operations and isolate subprocesses explicitly.

## Serving Models

Source: [Serving Models](20.12.05-serving-models-hosted-vs-self-hosted.md).

**Q:** Why does fitting a model's weights in GPU memory not prove the target concurrency fits?

**A:** Concurrent sequences also need key-value (KV) cache, activations, runtime buffers, and headroom. Calculate consistent GB and GiB units, account for sharding and quantization, and load-test realistic context and output lengths.

**Q:** Is an endpoint called "EU" or "self-hosted" enough to authorize sensitive-data routing?

**A:** No. Verify the actual approved data classes, processing and access regions, subprocessors, retention, transfer obligations, and deployment controls. Apply that policy before availability-based fallback.

## Safety, Cost and Governance

Source: [Safety, Cost and Governance](20.12.06-safety-cost-governance.md).

**Q:** Why can role separation and schema-valid output still leave prompt injection dangerous?

**A:** Untrusted text can influence a model to request a well-formed but unauthorized action. Deterministic tool and data-access authorization and least privilege enforce authority; prompts and serialization only help the model interpret data.

**Q:** What race does a conditional atomic budget update avoid, and what accounting remains afterward?

**A:** It rejects admission before concurrent reservations exceed the cap, without a separate over-limit increment and compensation race. Actual-cost settlement still needs a durable per-request reservation, bounded provider usage, and exactly-once release of unused funds.

## Trace and Vary the Boundary

Source: [Architecture](20.12.01-llm-app-architecture.md), [evaluation trace](20.12.02-prompts-context-evals.md#one-deterministic-evaluation-trace), [fusion](20.12.03-retrieval-quality-hybrid-search-reranking.md#trace-fusion-independently-of-any-provider), [local loop](20.12.04-agent-orchestration-patterns.md#an-executable-control-loop-with-injected-read-tools), [sizing](20.12.05-serving-models-hosted-vs-self-hosted.md#vram-sizing-calculator), and [budget admission](20.12.06-safety-cost-governance.md).

**Q:** An answer cites a permitted document but contradicts it. Which check passes, and which must fail?

**A:** Source-id membership passes. Claim-support grading must fail; a structural validator cannot establish factual grounding.

**Q:** A relevant document is absent from both candidate lists. Can reciprocal rank fusion (RRF) or a reranker recover it?

**A:** No. Improve retrieval, eligibility or indexing; later stages only reorder the selected candidates.

**Q:** A model proposes an unknown tool every turn. Can it avoid the local loop's ceiling?

**A:** No. Each inference consumes a turn and each proposal a call, even if no tool executes. A provider spend ceiling still requires separate reservations.

**Q:** The declared GPU capacity is negative or concurrency fractional. Should a sizing formula return a plausible fit?

**A:** No. Reject invalid inputs before arithmetic. A valid lower-bound estimate still requires a real runtime load test.

**Q:** A regex misses a patient's name. May the routing detector downgrade a known health-data class?

**A:** No. Authoritative classification remains binding; detection can tighten a policy but cannot prove anonymization.

**Q:** A cache prefix is reused but writing it also has a charge. Is a hit automatically free?

**A:** No. Measure eligible reuse and the provider's current input, cached-input, cache-write and output categories; prompt caching is distinct from reusing an answer.

Source: [Prompts, Context & Evals](20.12.02-prompts-context-evals.md)

**Q:** Why does placing a current timestamp or retrieved chunks ahead of static system instructions and tool schemas defeat provider prompt caching?

**A:** Prompt caching reuses KV state only along the longest identical token prefix starting from index zero. Any volatile field early in the request breaks prefix matching on every call, so static instructions and tool definitions must come first.

Source: [Agent Orchestration Patterns](20.12.04-agent-orchestration-patterns.md)

**Q:** How does MCP tool-description poisoning ("rug pulls") exploit `tools/list`, and how should hosts guard against it?

**A:** A compromised remote server can alter tool descriptions or parameter schemas across sessions to inject hidden instructions steering model arguments. Hosts should pin approved manifests or hash-verify `tools/list` definitions on connect before accepting diffs.

Source: [Serving Models](20.12.05-serving-models-hosted-vs-self-hosted.md)

**Q:** Why do high-scale LLM fleets disaggregate prefill workers from decode workers?

**A:** Prefill is compute-bound while token decoding is memory-bandwidth-bound; mixing long-prompt prefills into active decode batches spikes inter-token latency (TPOT). Separating prefill and decode pools and shipping KV caches across fast interconnects lets each tier meet its own latency SLO.

## Summary

Assess state, authority, cost, and recovery at explicit boundaries. An eval pass or a guardrail is evidence for its tested contract, not a blanket accuracy, privacy, or compliance guarantee.

## See Also

- [Reading flow](INDEX.md) — choose a workload-specific pass.
- [Interview bank](20.12.07-interview-questions.md) — explain the trade-offs aloud.

## References & Learn More

The linked source chapters contain the technical sources for these review answers.
