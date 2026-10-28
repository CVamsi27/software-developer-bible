# Docita — Architecture Decision Deep Dives

> Source-backed implementation assessments: what works, where the boundaries fail, and the recommended design with evidence needed to accept it.

[![Files](https://img.shields.io/badge/files-27-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Projects-purple)](#)

---

## Reading Flow

Start with one operation and trace identity, state and failure boundaries. These cases support explanations of full-stack TypeScript SaaS work; a source path supports a specific implementation claim, while production results require separate dated evidence. All 22 cases now distinguish current behavior from proposed improvements. The inspection used the local Docita working tree on 2 October 2026, with HEAD at c4eec265a and uncommitted changes present; it is not a clean-revision or production audit. A targeted 9 October recheck at local HEAD `dc5a97dc3`, also with unrelated working-tree changes present, updates the outbox acknowledgment in case 03 and its companion discussions. A scoped 26 October check at clean revision `4e3032c2d0fd9d2ee74e7c74536fefef454d5a65` updates case 02 and revision: recursion prevention now uses a child async scope, and the controlled overlapping-query probe preserves sibling transaction routing. These checks do not refresh every case into a production audit. Source details can change, so recheck the cited paths before presenting an implementation claim.

### Stage 1 — Follow an Operation Through the System

1. [Architecture decisions](01-architecture-decisions.md) — where rules, contracts and execution responsibilities belong.
2. [Tenant isolation](02-multi-tenancy-rls.md) — carry trusted identity to the actual database operation.
3. [Clinic workflows](05-clinic-workflows.md) — connect scheduling and product state to those boundaries.
4. [Patient portal](16-patient-portal.md) — apply identity and authorization to patient-facing access.

### Stage 2 — Make Work and Money Survive Failures

1. [Async processing](03-async-processing.md) — durable intent, claims, retries and repeated effects.
2. [Payment flows](04-payment-flows.md) — merchant ownership and local state transitions.
3. [Billing and invoicing](08-billing-invoicing.md) — financial records and invoice lifecycle.
4. [Subscription system](09-subscription-system.md) — subscription and entitlement behavior.
5. [Enterprise contracts](18-enterprise-contracts.md) — group billing and override boundaries.
6. [WhatsApp integration](06-whatsapp-integration.md) — provider delivery and user-facing communication.

### Stage 3 — Protect Files, Resources and Domain Transitions

1. [Documents and uploads](19-documents-and-uploads.md) — storage access and file lifecycle.
2. [Inventory](13-inventory.md) — stock movements and concurrent changes.
3. [Inpatient workflows](12-ipd-inpatient.md) — admission, transfer and resource allocation.
4. [Prescription safety](07-prescription-safety.md) — clinical decision boundaries and document output.
5. [Insurance claims](11-insurance-claims.md) — audited transitions and version checks.
6. [Clinical, lab and medical coding](20-clinical-lab-and-medical-coding.md) — results, codes and dependencies.

### Stage 4 — Operate the Product and Evaluate Integrations

1. [Deployment and infrastructure](10-deployment-infrastructure.md) — compatible versions, schema, rollout and recovery.
2. [Analytics and dashboards](14-analytics-and-dashboards.md) — historical and timezone correctness.
3. [Doctors, verification and public booking](15-doctors-verification-and-public-booking.md) — anonymous entry points and verification.
4. [ABDM integration](17-abdm-integration.md) — consent and asynchronous callbacks.
5. [Smaller domains](21-long-tail-domains.md) — reminder claims, webhook trust, reversible leave and user lifecycle.
6. [What I'd do differently](22-what-id-do-differently.md) — evaluate improvements after understanding the cases.

### Stage 5 — Model Workload and Define Outcome Evidence

First read the refreshed [deployment/resource profile](10-deployment-infrastructure.md#trace-the-deployment-before-choosing-a-machine) and [measurement lineage](14-analytics-and-dashboards.md#a-dashboard-built-from-actual-records-and-retained-telemetry). Then derive the [25-clinic workload](23-hypothetical-clinic-metrics.md): monthly counts, busy arrivals, connection budgets, storage and local experiment acceptance. The diagrams separate current low-cost operation, a future balanced AWS reference and actual tests. Modeled volume and published latency targets remain separate from customer adoption or achieved production outcomes.

### Stage 6 — Connect the Current Resume to Actual Work

Use [the five-bullet resume walkthrough](24-resume-claim-walkthrough.md) to explain the product, personal contribution, implementation and evidence behind each claim. Then rehearse one changed constraint.

### Stage 7 — Launch, Grow and Fund the Service

Follow [launch through growth](25-launch-to-growth.md) from local setup to a supervised pilot, repeatable onboarding, daily operations, incidents, customer exit and measured growth beyond 25 clinics. Use [monthly operating costs](26-monthly-operating-costs.md) alongside each promotion decision: price the service hours, database use, retained files, provider deliveries and recovery/support obligations. Its dated scenarios compare low-cost Neon operation with a future AWS reference; they are proposals rather than the live bill or capacity proof.

### Revision, Then Interview Practice

Use [category revision](REVISION.md) after the learning cases. Reconstruct a mechanism and its failure boundary before checking an answer. Each case has a source-linked revision group; questions remain outside the learning chapters.

Then use the interview guides below to connect an implementation decision to its evidence and limits. Keep business outcomes, source inspection and executed checks distinct; do not memorize an unsupported incident or metric as personal experience.

---

## Cross-References

- **Interview defense guide:** [80.36-docita-complete-interview-defense.md](../../80-lanes-abroad-full-stack/80.36-docita-complete-interview-defense.md)
- **Resume defense Q&A:** [80.16-docita-resume-defense.md](../../80-lanes-abroad-full-stack/80.16-docita-resume-defense.md)
- **Resume evidence pack:** [80.17-docita-interview-evidence-pack.md](../../80-lanes-abroad-full-stack/80.17-docita-interview-evidence-pack.md)
- **Tech topic mapping:** [80.22-docita-tech-topic-mapping.md](../../80-lanes-abroad-full-stack/80.22-docita-tech-topic-mapping.md)
- **Google-level prep:** [80.21-docita-google-level-prep.md](../../80-lanes-abroad-full-stack/80.21-docita-google-level-prep.md)

---

## Evidence to Bring to an Interview

For one selected case, record the inspected source revision, your own contribution, a representative operation, a meaningful verification result and an unresolved limitation. Obtain workload, adoption, latency and reliability metrics from their dated operational evidence before quoting them. Do not infer those outcomes from framework versions or source-folder counts.
