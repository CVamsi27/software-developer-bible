<!-- section: Platform | category: Reference | tags: revision, practice | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Platform-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../docs/topic-importance.md)

# Platform — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## The Twelve-Factor App

Source: [The Twelve-Factor App](40.9.01-the-twelve-factor-app.md)

**Q:** What separates a build from a release?

**A:** A build produces an artifact; a release combines that artifact with configuration for an environment. Running it should not mutate the build artifact.

**Q:** Why keep a process disposable?

**A:** Replacement, scale-out, and deploys must not require recovering hidden in-memory business state. Start quickly and terminate gracefully while persisting durable state externally.

**Q:** What does treating a database as an attached resource enable?

**A:** Its connection/configuration is injected rather than hard-coded into the artifact, so environments can attach different resources under the same application contract.

**Q:** Why are logs an event stream instead of an application-managed file rotation job?

**A:** The runtime/platform can collect, route, retain, and query stdout/stderr events consistently across replaceable processes. Sensitive data policy still applies to their contents.

**Q:** Why do one-off admin jobs use the release's code and configuration?

**A:** They need the same dependency/schema/environment contract as the service. Ad-hoc laptop scripts create untracked versions and privilege drift.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
