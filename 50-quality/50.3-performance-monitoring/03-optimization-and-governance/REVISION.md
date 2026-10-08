<!-- section: Performance Monitoring | category: Reference | tags: revision, practice | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Performance%20Monitoring-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Performance Monitoring — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Bundle Analysis

Source: [Bundle Analysis](50.3.3.01-bundle-analysis.md)

**Q:** Why is 170 KB not a universal TCP congestion-window budget?

**A:** A transport congestion window concerns bytes/segments on a connection and varies by implementation/path. A compressed JavaScript budget additionally needs measured device, parse, and execution costs.

**Q:** What does esbuild metafile true return instead of automatically writing a report?

**A:** Build-result metadata. Persist result.metafile or feed it to an analyzer explicitly; enabling the option alone does not create the JSON file named in a later command.

**Q:** Why can sideEffects false create a functional regression?

**A:** It asserts unused module evaluation is safe to omit. If CSS, registrations, or required initialization has side effects, the bundler may remove behavior the app needs.

**Q:** In the esbuild fixture, does destructuring a dynamic import guarantee the same unused-export removal as an eager named import?

**A:** No. The tested eager build omits the unused export while its dynamic chunk retains both exports. Inspect emitted assets and runtime requests; lazy loading and export elimination are separate changes.

**Q:** What happens if the lazy report chunk cannot be fetched?

**A:** The import rejects, the fixture reports a failure and re-enables the button for retry. A deployment needs compatible retained chunks or an explicit recovery policy; smaller initial bytes do not remove that requirement.

## Performance Budgets

Source: [Performance Budgets](50.3.3.02-performance-budgets.md)

**Q:** Why set both a route budget and an aggregate budget?

**A:** An acceptable total can hide a large initial route or lazy feature. Each budget constrains a different user journey and loading boundary.

**Q:** How should a necessary feature exceeding a budget be handled?

**A:** Show the measured cost, affected users, mitigation choices, and explicit exception/adjustment policy. Silently raising the threshold removes the gate's decision value.

**Q:** Two assets are individually below 120,000 gzip bytes but sum to 220,000. Does the example gate pass?

**A:** No. The aggregate limit is 200,000. The opposite case also matters: one 130,000-byte asset fails the individual bound even if the total is below 200,000. Equality passes under the declared inclusive bounds.

**Q:** Why must a missing file or empty manifest fail instead of counting as zero?

**A:** The input contract is invalid, so no useful measurement exists. A zero result would certify absent evidence. The fixture rejects both conditions, duplicate assets and invalid byte thresholds.

**Q:** What changes if an initial asset becomes a preloaded lazy chunk?

**A:** It may still be fetched before the feature is used. Derive the actual journey's request set before crediting a byte reduction; chunk naming alone does not identify initial load.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md) — connect module ownership, journey requests and budget enforcement

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
