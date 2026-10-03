<!-- section: CI/CD | category: Reference | tags: revision, practice| general-importance: important| general-importance: important | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-CI/CD-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# CI/CD — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## GitHub Actions

Source: [GitHub Actions](40.3.1.01-github-actions.md)

**Q:** Why should workflow token permissions be explicit?

**A:** Jobs otherwise inherit broader defaults than they may need. Grant each job only the repository/cloud capabilities required and treat untrusted pull-request input as data.

**Q:** Why does a successful PR build not automatically authorize production deployment?

**A:** PR code may be untrusted and the tested ref differs from the trusted main push. Verify without release authority, then promote the identified artifact from the intended trusted run through configured environment/cloud policy.

**Q:** What distinguishes a dependency cache from the artifact you approve for release?

**A:** A cache saves reconstructible work and can restore older/untrusted content. A release artifact needs an identified producer/run/commit and integrity verification; it must be the bytes the deployment consumes.

**Q:** Why is id-token: write insufficient to deploy to AWS?

**A:** It permits requesting an OIDC token. AWS still needs the provider, audience/subject trust conditions and a role policy granting only the intended deployment operations.

**Q:** Why can filtering a monorepo workflow to apps/web/** miss necessary verification?

**A:** Shared source, root lockfiles, build configuration or workflow changes can affect that app without matching the narrow path. Keep required checks available and select work from the full dependency graph, including merge-group runs where applicable.

**Q:** Why do PR titles belong in environment variables rather than interpolated shell source?

**A:** They are untrusted input. Environment passing plus appropriate quoting treats the value as data instead of allowing it to alter the generated script.

## GitLab CI/CD

Source: [GitLab CI/CD](40.3.1.02-gitlab-ci.md)

**Q:** When do needs and stages express different ordering?

**A:** Stages provide broad ordering barriers; needs declares particular job dependencies so independent work can run sooner. Artifact dependencies must still match the producer/consumer contract.

## Jenkins CI/CD

Source: [Jenkins CI/CD](40.3.1.03-jenkins.md)

**Q:** Why is a Jenkinsfile insufficient for a reproducible pipeline?

**A:** Agent images, plugins, credentials, tool versions, and external dependencies also influence execution. Pin and operate those inputs as part of the pipeline system.

## ArgoCD (GitOps)

Source: [ArgoCD (GitOps)](40.3.1.04-argocd.md)

**Q:** Why does a manual production hotfix drift under GitOps?

**A:** The controller may restore the declared Git state. Record the intended change in the source of truth or use an explicit incident policy before reconciliation reverses it.

**Q:** Can reverting Git safely reverse every deployment effect?

**A:** It can restore manifests/artifact references. Database migrations, writes, and external effects may require a separate forward repair or rollback procedure.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
