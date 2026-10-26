<!-- section: CI/CD | category: Reference | tags: revision, practice | role-priority: important | general-importance: important -->
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

**Q:** What must a cloud provider verify before trusting a GitLab job ID token?

**A:** Match the configured issuer and audience, then restrict trust to the intended project and protected ref or deployment environment. A valid token proves job identity; it does not make unreviewed pipeline code trustworthy or grant a role by itself.

## Jenkins CI/CD

Source: [Jenkins CI/CD](40.3.1.03-jenkins.md)

**Q:** Why is a Jenkinsfile insufficient for a reproducible pipeline?

**A:** Agent images, plugins, credentials, tool versions, and external dependencies also influence execution. Pin and operate those inputs as part of the pipeline system.

## Argo CD (GitOps)

Source: [Argo CD (GitOps)](40.3.1.04-argocd.md)

**Q:** Why can an unrecorded live-cluster hotfix be overwritten under GitOps?

**A:** If the edited fields belong to an Argo-tracked resource and self-heal is enabled, reconciliation may restore the declared Git state. Record the repair in the source of truth or follow an explicit incident policy before resuming reconciliation.

**Q:** Can reverting Git safely reverse every deployment effect?

**A:** It can restore manifests/artifact references. Database migrations, writes, and external effects may require a separate forward repair or rollback procedure.

**Q:** If Argo CD reports Synced, what must you still check before calling the release successful?

**A:** Desired configuration matches live configuration, but workload health and user-visible behavior can still fail. Inspect readiness, resource health and application checks separately.

**Q:** Why must a release that depends on a PreSync migration avoid selective sync?

**A:** Hooks do not run during selective sync. A normal ordered synchronization can execute the migration; it still needs compatible, safely repeatable database behavior.

**Q:** An ApplicationSet object is accepted in `default`, but no Applications are generated. What controller boundary should you inspect?

**A:** ApplicationSets normally belong in the Argo CD control-plane namespace. Watching other namespaces requires explicit ApplicationSet controller configuration and matching allowed Application namespaces; API acceptance alone does not establish reconciliation.

**Q:** Does a SyncFail hook automatically reverse a database migration?

**A:** No. It can run configured remediation, but database/external effects are not a transaction with manifest synchronization. Establish a compatible repair procedure.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
