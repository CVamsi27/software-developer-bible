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

**A:** A `sensitive` mark redacts output; it does not by itself omit the value from state or saved plans. Ephemeral values and write-only arguments can avoid persistence when their supported contexts fit. Protect the remaining artifacts. See [managing sensitive data](https://developer.hashicorp.com/terraform/language/manage-sensitive-data).

**Q:** What does a saved plan bind, and what can still change before apply?

**A:** It stores the configuration and planned values with the selected actions, so protect it as a potentially secret-bearing artifact and apply only to the reviewed target. Terraform can reject it if state changed, but it does not re-plan against every external edit after planning. Regenerate the plan when its assumptions are no longer current. See [plan files](https://developer.hashicorp.com/terraform/cli/commands/plan).

**Q:** Why lock shared state during mutation?

**A:** Concurrent writers can race on the same resource mapping and overwrite assumptions. Locking serializes supported Terraform operations but not console edits or another state; see [state locking](https://developer.hashicorp.com/terraform/language/state/locking).

**Q:** What is the difference between import and configuration reconciliation?

**A:** Import binds an existing remote ID to a Terraform address. The configuration must still describe the intended settings or a later plan may change or destroy it. A `moved` block handles an address refactor for an object already tracked by Terraform. See [import](https://developer.hashicorp.com/terraform/language/import) and [refactoring](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring).

**Q:** Why are remote API results necessary after a successful apply?

**A:** The command establishes which provider operations reported success. Service behavior, propagation, access, and readiness need deployment-specific checks; Terraform apply is not a transaction or service-level health test.

**Q:** Plan observes an object, then someone edits it before apply. Does the saved plan stop that edit?

**A:** No. Supported state locks control Terraform operations on that state, not external console writes. Apply can encounter different conditions; verify the target, review changes and inspect actual outcomes.

**Q:** Does reading a secret-manager value keep it out of ordinary state?

**A:** Not necessarily. A provider data result can be persisted. `sensitive` redacts display; supported ephemeral/write-only contracts can omit values from plan and state files. Protect the remaining artifacts. See [sensitive data handling](https://developer.hashicorp.com/terraform/language/manage-sensitive-data).

**Q:** Which Amazon S3 backend setting enables native state locking?

**A:** `use_lockfile = true` opts into S3 lock files and requires read/write/delete permissions on the `.tflock` object. S3 does not enable locking by default; DynamoDB locking is deprecated. See the [S3 backend requirements](https://developer.hashicorp.com/terraform/language/backend/s3).

**Q:** Is the Cloud Development Kit for Terraform (CDKTF) maintained for new projects?

**A:** HashiCorp deprecated it on 10 December 2025 and stopped maintaining it. Existing projects need an explicit support/migration choice. AWS CDK is a different tool and synthesizes CloudFormation.

**Q:** Why might retrying after a partial apply need import rather than another create?

**A:** A remote create may succeed before Terraform records its identity. Inspect the provider and state, recover or import the binding if necessary, then create and review a fresh plan instead of blindly retrying.

**Q:** What does `.terraform.lock.hcl` pin, and what must you pin separately?

**A:** It records selected provider versions and checksums. It does not select and remember remote module versions, so declare constraints separately and use exact versions or immutable revisions when reproducibility requires them. See the [dependency lock file reference](https://developer.hashicorp.com/terraform/language/files/dependency-lock).

**Q:** Does Terraform's command-line interface (CLI) continuously repair drift after apply?

**A:** No. The CLI plans when invoked; a scheduled run service can add cadence. A GitOps controller continuously reconciles its declared resources, so define one owner for each resource or field to prevent competing writers.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
