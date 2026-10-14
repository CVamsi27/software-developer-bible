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

Source: [The Twelve-Factor App](40.9.01-the-twelve-factor-app.md) · [Original factor text](https://12factor.net/) · [Community refresh announcement](https://12factor.net/blog/open-source-announcement) · [Manifesto repository](https://github.com/twelve-factor/twelve-factor)

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

**Q:** Can a stateless process have a connection pool or local cache?

**A:** Yes. Those are reconstructible optimization state; accepted business effects must remain correct if they disappear. Warm-up time still affects readiness and scale-out.

**Q:** Does redeploying release R−1 undo the database migration from R?

**A:** No. It restores code/configuration identity, not external effects. Check backward-compatible schema/data behavior and the recovery path before rollback.

**Q:** Must every web process start within five seconds and stop within thirty?

**A:** No. The methodology favors fast start and graceful stop; measure workload readiness and configure the runtime deadline. Sudden death still requires durable recovery.

**Q:** What is the current status of the original Twelve-Factor text?

**A:** It was published in 2011, and the original pages state they were last updated in 2017. A community refresh began in 2024; its repository says the working updates remain on `next` until maintainers agree the round is complete. Treat the original as a useful baseline and describe adaptations without presenting later proposals as a finalized replacement.

**Q:** Is a secret fetched into memory safe from crash dumps?

**A:** No. Delivery avoids embedding it in the artifact but does not remove its in-memory value. Control diagnostics, lifetime, access and redaction.

## Deployment Prompts Moved from the Learning Chapter

Source: [The Twelve-Factor App](40.9.01-the-twelve-factor-app.md) · [Original factor text](https://12factor.net/)

**Q:** Walk me through your deployment pipeline.

**A:** Identify the built artifact, release configuration, compatibility/migration gate, rollout and observed outcome. Use your actual pipeline; separating the stages does not make rollback of external state automatic.

**Q:** How do you handle config?

**A:** Explain deployment-varying inputs, validation, credential delivery and audit. The original factor recommends independent env vars; identify any mounted-config or runtime-service adaptation and its exposure boundary.

**Q:** What about stateful operations like database migrations?

**A:** Run compatible release tooling under an explicit owner and recoverable one-off execution policy. Prevent unsafe overlap, preserve supported old/new schema behavior and verify the result before admitting dependent code.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
