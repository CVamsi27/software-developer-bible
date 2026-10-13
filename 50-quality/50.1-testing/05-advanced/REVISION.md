<!-- section: Testing | category: Reference | tags: revision, practice | role-priority: important | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Testing-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../../docs/topic-importance.md)

# Testing — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Performance & Load Testing

Source: [Performance & Load Testing](50.1.5.01-performance-load-testing.md)

**Q:** Why can a fixed-VU test hide overload?

**A:** In a fixed virtual-user (VU) test, each simulated user waits for a response before sending more work, so a slower service receives fewer requests. An arrival-rate model sends work at the intended rate independently of response time and can expose capacity limits.

**Q:** Why run a soak after a short throughput test passes?

**A:** Leaks, pool exhaustion, periodic jobs, and accumulating buffers may appear only over sustained time. Measure resource trends as well as request latency.

**Q:** What proves the load generator is not the bottleneck?

**A:** Its CPU/network/resource usage, achieved arrival rate, dropped iterations, and connection limits must show that it supplied the intended workload throughout the measurement.

## Chaos Engineering & Game Days

Source: [Chaos Engineering & Game Days](50.1.5.02-chaos-engineering.md)

**Q:** What makes fault injection an experiment rather than random breakage?

**A:** A falsifiable hypothesis, known baseline, bounded fault/blast radius, measurements, abort criteria, and recorded findings distinguish an experiment.

**Q:** Why start a new chaos scenario in staging?

**A:** It validates the fault, instrumentation, and stop mechanism before accepting production risk. Production experiments can add realism when explicitly governed; they are not the only valid experiments.

## Load contract and metric population

Source: [Performance & Load Testing](50.1.5.01-performance-load-testing.md)

**Q:** Why does the runnable catalog example add both good and bad attempts to its failure Rate?

**A:** The denominator must be all observed attempts. Adding only failures makes one failure look like a 100% failure population and cannot express the actual ratio.

**Q:** Can HTTP 200 still fail the example's process-level gate?

**A:** Yes. The semantic check verifies the expected item and price; its result feeds a custom `semantic_failures` Rate with a zero-failure threshold. The built-in `checks` metric records outcomes but cannot itself be thresholded. A wrong price can fail the process gate while `http_req_failed` remains zero.

**Q:** What boundary does Little's Law require?

**A:** Use the same stable work population for average throughput, average time and average in-flight work. Include queue time when waiting work is in the population; a p99 multiplied by all registered users is not that relationship.

## Fault layer and application behavior

Source: [Chaos Engineering & Game Days](50.1.5.02-chaos-engineering.md)

**Q:** Does a 150 ms downstream latency toxic generate a 50% HTTP error rate?

**A:** No. It delays selected server-to-client data. HTTP errors require an appropriate application or protocol-aware failure scenario; toxicity selects links and is not a business error percentage.

**Q:** What does the local delay example establish about a circuit breaker?

**A:** Nothing about its state transitions. It verifies delayed correct responses and recovery through the proxy. A breaker test must observe the actual application contract, opening, rejection and recovery probes.

**Q:** Why verify that the application uses the proxy before interpreting a passing chaos test?

**A:** An active fault on an unused route changes nothing. Confirm the routing and injection while the required user operation runs, then check both fault removal and service recovery.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md) — set a workload and recovery hypothesis before interpreting experiment results

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
