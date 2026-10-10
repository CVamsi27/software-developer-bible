<!-- section: IaC | category: Reference | tags: revision, practice | role-priority: optional | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-IaC-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Optional-lightgrey)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)

# IaC — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## 40.12.01 — Infrastructure as Code & Terraform Fundamentals

Source: [40.12.01 — Infrastructure as Code & Terraform Fundamentals](40.12.01-iac-fundamentals-terraform.md)

**Q:** Why is Terraform state sensitive even when values are marked sensitive?

**A:** Sensitive marks control presentation, not necessarily storage. State can contain secrets and resource details, so secure access, encryption, backups, and locking.

**Q:** What does a saved plan bind, and what can still change before apply?

**A:** It records the intended resource diff for known inputs/state. Provider behavior, external changes, credentials, and time-dependent conditions still require controlled application and verification.

**Q:** Why lock shared state during mutation?

**A:** Concurrent writers can race on the same resource mapping and overwrite assumptions. Locking serializes supported operations but does not replace review or backup.

**Q:** What is the difference between import and configuration reconciliation?

**A:** Import records an existing resource's identity in state. The configuration must still describe the intended settings or a later plan may change or destroy it.

**Q:** Why are remote API results necessary after a successful apply?

**A:** The command establishes what the provider reported. Service behavior, propagation, access, and readiness must be observed through deployment-specific checks.

**Q:** Plan observes an object, then someone edits it before apply. Does the saved plan stop that edit?

**A:** No. Supported state locks control Terraform operations on that state, not external console writes. Apply can encounter different conditions; verify the target, review changes and inspect actual outcomes.

**Q:** Does reading a secret-manager value keep it out of ordinary state?

**A:** Not necessarily. A provider data result can be persisted. sensitive marks redact display; use supported ephemeral/write-only contracts where needed and protect state/plans regardless.

**Q:** Which current S3 backend setting enables a native state lock?

**A:** use_lockfile = true, with the necessary lockfile permissions. Selecting S3 alone does not enable it; the older DynamoDB lock mechanism is deprecated.

**Q:** Is CDKTF a maintained new-project option?

**A:** HashiCorp deprecated it on 10 December 2025 and stopped maintaining it. Existing projects need an explicit support/migration choice. AWS CDK is a different tool and synthesizes CloudFormation.

**Q:** Why might retrying after a partial apply need import rather than another create?

**A:** The remote creation might have succeeded before its identity was persisted. Inspect remote state and ownership, recover the mapping if needed, then produce a fresh plan.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
