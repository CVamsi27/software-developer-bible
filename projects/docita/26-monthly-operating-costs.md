# 26 — Monthly Costs: Price the Promise Before Adding Clinics

[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)

A suspended API can make the compute bill look small while a stopped worker misses every reminder. At the other extreme, two messages per visit can cost more than the application machines. A useful budget starts with the service being promised, then prices the resources and external effects needed to deliver it.

## Definition

An operating-cost model translates application activity into provider billing units: running hours, database compute, retained bytes, requests, delivered messages and successful payment value. For Docita, it also records who pays each bill and which service obligations remain unfunded.

> **Textbook Definition:** Application operating cost is the recurring expense of delivering and maintaining a defined service, including compute, persistence, networking, external providers, recovery, observation and human operation, measured over a stated period and workload.

Prices below were checked against official sources on **28 October 2026**. Calculations use **720 hours**, US dollars unless marked INR, public on-demand rates and no promotional credits. A 31-day month has 744 hours. These are reproducible **planning scenarios**, not Docita invoices or evidence that a topology has met the [25-clinic workload](23-hypothetical-clinic-metrics.md). The actual Neon tier, utilization, storage, provider contracts and monthly bill have not been inspected. No paid resource change is implied.

## First Principles

A clinic is a customer boundary, not a billing unit. Two clinics can produce very different traffic, retained images, message deliveries and support demand. Some costs continue when requests stop; other costs appear only when a provider delivers an effect.

Derive the budget in this order:

```text
Service promise: opening hours, background work, recovery and support
      |
      v
Workload: visits, request classes, documents, retained history, messages
      |
      v
Resource use: runtime/CU-hours, bytes, operations, successful money flow
      |
      v
Provider units and account-wide allowances -> infrastructure subtotal
      |
      +-> messaging/email/payment fees, allocated to the correct payer
      +-> recovery, staging, monitoring, domain, support and incident work
      v
Tax + invoice-currency conversion + explicitly chosen contingency
      |
      v
Reconcile actual invoice and service outcomes; revise next month's model
```

Keep three views: **cash paid**, **usage consumed** and **fully loaded cost** including labor. Buying email credits affects cash before all credits are used. A prepaid annual domain belongs in monthly economics as annual price divided by twelve. Unpaid founder time is still work.

## Establish the Current Baseline Before Estimating Growth

The 28 October inventory recorded one stopped Singapore API machine, 1 shared vCPU/512 MiB, and one stopped worker, 1 shared vCPU/256 MiB. Neon is the current temporary database provider; AWS RDS is a future reference. [Deployment](10-deployment-infrastructure.md) owns configuration, CPU/RAM/heap distinctions and recovery boundaries.

The present invoice cannot be reconstructed from that snapshot. Collect machine running seconds, stopped-rootfs sizes, IP allocations, volumes, regional transfer, Neon plan/CU-hours/storage/history, R2 usage, edge plan, provider balances and account-wide allowances. A stopped machine can still have rootfs charges. The worker must run whenever its scheduled work is promised; waking the API does not start that worker.

For each environment, keep a private resource register with resource ID, region, purpose, payer, plan, unit rate, usage, retention, budget owner and removal date. Publish only sanitized totals. Production, previews, staging, restore drills and abandoned resources all belong in the register.

## Translate the Infrastructure Into Billing Units

### Fly: running time and the region both matter

The [Fly pricing page](https://docs.fly.io/about/pricing) lists regional machine rates. Its lowest-region headline is not Singapore's rate. The public calculator's Singapore multiplier is `1.269230769`; the base shared-CPU charge is `$0.0000008465/second`, including 256 MiB, and additional RAM is `$0.000002316/GB-second` with the calculator's `MB / 1024` conversion.

| Singapore machine, one shared vCPU | Estimated hourly runtime | 720 running hours |
| ---------------------------------- | ------------------------ | ----------------- |
| 256 MiB | $0.00386785 | $2.78 |
| 512 MiB | $0.00651344 | $4.69 |
| 1 GiB | $0.01180461 | $8.50 |

Calculate before rounding each displayed component. Add stopped/suspended rootfs at **$0.15/GB-month**, provisioned volumes at **$0.15/GB-month**, and Singapore internet egress at **$0.04/GB**. A dedicated inbound IPv4 is **$2/month** when allocated; shared inbound IPv4/IPv6 does not require that allocation. Optional static outbound IP allocation costs **$0.005/hour**. These resources have separate lifecycles; destroying a machine does not necessarily release its IP allocation. [Billing](https://docs.fly.io/about/billing), [egress IP scope](https://docs.fly.io/networking/egress-ips).

### Neon: compute is integrated over time

From the [official plan table](https://neon.com/docs/introduction/plans), Launch compute is **$0.106/CU-hour**, PostgreSQL storage **$0.35/GB-month**, and instant-restore history **$0.20/GB-month**. Launch has no monthly minimum. A compute unit (CU) represents a compute envelope; approximately 4 GB RAM per CU is memory, not allocated database disk.

```text
Launch compute = sum(actual CU size × active hours) × $0.106
0.25 CU × 720h = $19.08; 0.5 CU = $38.16; 1 CU = $76.32
```

Include every active branch/replica and autoscaling interval. Idle suspension can reduce hours, while probes, polling and jobs can keep the database awake. Measure that interaction rather than assuming a five-minute suspend setting produces a particular bill. Launch includes 500 GB/project public transfer, then $0.10/GB; additional branches and enabled features have their own charges.

Free is a separate plan: **100 CU-hours/project/month**, **1 GB PostgreSQL storage/project**, **20 GB account total**, **5 GB public transfer/project**, and mandatory five-minute idle suspension. Do not subtract those allowances from Launch charges. At 0.25 CU, 260 active hours uses 65 CU-hours; at 720 hours it uses 180. Exhausting compute/transfer can suspend service; storage exhaustion blocks storage-increasing operations. Free is a constrained pilot option only if its limits and recovery capabilities fit the promise. It is not a production-readiness finding.

### Cloudflare: edge requests and retained files are different meters

[Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/) has a **$5/account/month** Paid minimum including 10 million requests and 30 million CPU milliseconds; extra requests cost $0.30/million and CPU $0.02/million milliseconds. Free has 100,000 requests/day and 10 ms CPU/invocation. Static assets and dynamic proxy work must be classified correctly. A monthly request average cannot establish compliance with a daily or per-invocation limit. Share account allowances once across all deployed applications.

[R2 Standard pricing](https://developers.cloudflare.com/r2/pricing/) includes 10 GB-month storage, 1 million Class A operations and 10 million Class B operations per account/month. Overages are **$0.015/GB-month**, **$4.50/million Class A** and **$0.36/million Class B**. Usage rounds up to whole billing units. Storage uses average daily peaks; internet egress from R2 is free. An API proxying the same bytes can still incur Fly egress. Infrequent Access has different allowances, retrieval and retention rules; it is not used below.

## Compare Concrete Monthly Infrastructure Scenarios

These are example envelopes for the [growth stages](25-launch-to-growth.md), not automatic upgrades at a clinic count. All active rows need the launch/recovery gates in that chapter. Always-on rows intentionally cost both proposed API machines as warm; the deployment reference may instead suspend the spare, in which case calculate its running time and stopped rootfs separately.

| Scenario | Fly API + worker, running hours each | Database input | Edge, R2, transfer and network assumptions | Infrastructure subtotal/month |
| ------------------------------ | ---------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------- |
| 0: parked development | Existing sizes; 0 running hours | Neon Free within limits | Example only: two 1 GB rootfs all month; no paid IP/volume; edge/R2 within Free | **$0.30**, conditional on those inputs |
| 1: supervised pilot on Free | 512 MiB API + 256 MiB worker, each 260h | 0.25 CU ×260h; Free, ≤1 GB data and all other Free limits | Edge/R2 Free; 1 GB Fly egress; two 1 GB rootfs stopped for remaining 460h | **$2.93** |
| 1: same pilot on Launch | Same 260h pattern | 0.25 CU ×260h +1 GB storage; no restore-history charge assumed | Same edge/R2/network/rootfs assumptions | **$10.17** |
| 2–5: repeatable active service | 512 MiB API +256 MiB worker, each 720h | Launch 0.25 CU ×720h +5 GB storage | Workers Paid $5; R2 within allowance; 5 GB Fly egress $0.20; no separate IP/volume | **$33.50** |
| 6–10: measured warm service | 1 GiB API +512 MiB worker, each 720h | Launch 0.5 CU ×720h +10 GB data +5 GB-month restore history | Workers $5; R2 within allowance; 10 GB Fly egress $0.40 | **$61.25** |
| 11–25: Neon comparison | Two 1 GiB APIs +512 MiB worker, all 720h | Launch 0.5 CU ×720h +20 GB data +5 GB-month history | Workers $5; R2 steady inventory below $1.16; 25 GB Fly egress $1; no dedicated/static IP assumed | **$75.00** |
| 11–25: future AWS comparison | Same two APIs +worker, all 720h | RDS Single-AZ `db.t4g.medium`, 720h +50 GiB gp3 | Same Workers/R2/25 GB Fly egress; two app-scoped static Fly egress allocations $7.20; one billable RDS public IPv4 $3.60 | **$119.98** |

The pilot schedule is an explicit 260-hour **total**, not evidence that 26 ten-hour days matches actual appointments or that work can stop at closing. Include late callbacks, pending PDFs, reminders, maintenance and recovery. Pilot totals include $0.1917 stopped-rootfs cost and $0.04 Fly egress. Unverified rootfs sizes make those example totals conditional. Existing account plan minimums still apply; selecting a row does not cancel a paid plan.

The active rows exclude independent backups, additional monitoring, email, WhatsApp, payment fees, AI, domain, staging, taxes and labor; price them below. Neon history allocations are stated assumptions, not a guarantee that seven days of writes occupies 5 GB or that independent backup is covered. The R2 illustration holds document inventory constant for comparison, not because every growth stage accumulates the same history. Count and paid tier do not establish an achieved service-level objective (SLO).

At 25 active clinics, the Neon infrastructure example is about **$3.00/clinic/month** or **$0.002885/completed visit** at 26,000 visits. Those denominators must be real active clinics and completed visits in the same period when reporting actual economics. Low infrastructure cost alone does not establish profitability.

### What the future AWS row buys and leaves open

The official [Singapore RDS price catalog](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRDS/current/ap-southeast-1/index.json), publication `2026-10-26T21:47:16Z`, quotes PostgreSQL Single-AZ `db.t4g.medium` at **$0.102/hour**: SKU `MRHX8CSFGNNN9JPV`, usage `APS1-InstanceUsage:db.t4g.medium`. Its 2 vCPU/4 GiB class costs $73.44/720h. GP3 storage SKU `FXXDJWB23UZKQHCN` is **$0.138/GB-month**, making **50 GiB provisioned** **$6.90**: 50 provider storage units at the catalog's $0.138 `GB-Mo` rate. AWS [storage documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Storage.html) specifies the allocation in GiB. Instance plus provisioned storage is **$80.34**. Do not accidentally select the catalog's unused-capacity-reservation SKU. [RDS pricing](https://aws.amazon.com/rds/postgresql/pricing/).

The row models one **public endpoint protected by strict source allowlisting and TLS**, not an open database. Fly API and worker are different apps, so each needs its own app-scoped static egress allocation in Singapore: $3.60 ×2. Permit only their verified outbound addresses, validate the database certificate/hostname, use limited runtime roles and keep migration credentials separate. One AWS public IPv4 at [$0.005/hour](https://aws.amazon.com/vpc/pricing/) adds $3.60. Verify actual IP count, routing and provider support before choosing this path. Private connectivity is an alternative requiring its own design and quote; a NAT gateway is not automatically required by this public-endpoint example.

This row is **not high availability**. Price Multi-AZ, any read replica, extra storage/IOPS, surplus burst CPU credits (currently $0.075/vCPU-hour for PostgreSQL T4g/T3), backup storage beyond the included allowance, snapshots retained after deletion, AWS outbound transfer, monitoring/log retention, support and migration overlap separately. A Single-AZ instance does not become resilient because two API machines exist. Use region-specific service pricing and account-wide transfer allowances before assigning an AWS network total. No AWS outbound amount is assumed in the subtotal.

The comparison places Fly and RDS in Singapore. A move to another AWS region needs a new regional instance/storage quote, network path and data-locality review; the Singapore total cannot price Mumbai. If API and database regions differ, measure round trips per operation and their latency as well as billed transfer in both directions. Compare placements using the same workload, recovery promise and operating hours before calling one cheaper.

## Retained Data Grows Even When Clinic Count Does Not

The chapter23 example generates 20,800 prescription PDFs and 26,000 invoice PDFs monthly. At **150 KiB each**, 46,800 objects add **7.18848 decimal GB**, or **6.6948 GiB**. R2 bills decimal GB; mixing those units understates the input.

Twelve retained monthly cohorts contain **86.26176 GB** before versions, images, uploads, regenerated documents and backups. An inventory held constant at that size for a month rounds to 87 GB-month; after the 10 GB allowance, **77 ×$0.015 = $1.155**. This is a steady-inventory comparison. During accumulation, use each day's peak inventory; do not bill the final annual inventory for every earlier month. A rolling deletion policy changes the inventory curve and requires approved retention rules.

One write and three reads per PDF would be 46,800 writes and 140,400 reads/month, within the stated free operation allowances **if no other account usage consumes them**. Count HEAD/list requests, retries, multipart operations, other products and backups as applicable. Document-generation CPU is paid on Fly and is not included by R2 storage pricing.

Database disk is a different estimate. Twenty thousand clinic-patient pairs seen in a month does not mean twenty thousand new patients every month. Measure table/index sizes, new/updated rows, audit and telemetry retention, queue cleanup, WAL, temporary space and maintenance headroom. A 20 GB Neon data assumption and a 50 GiB RDS allocation are scenario inputs, not inferred row-size proofs.

### Carry the history through a growth ramp

Keep one row per actual billing month, rather than assigning the mature 25-clinic workload to every early period. Record opening active clinics, activations/reactivations, exits and closing active clinics. Separately count billable clinic-days and service-active clinic-days: a free pilot consumes resources, and a clinic activated late in a month does not contribute a full month of either usage or revenue.

| Monthly ledger input | Calculation or retained evidence |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Effective service volume | Sum each clinic's observed visits and provider work; for an initial homogeneous forecast only, service-active clinic-days divided by days in the period gives equivalent full clinic-months |
| Retained cohorts | Opening objects/bytes + new objects/bytes − authorized deletions; compute the provider's daily storage meter rather than charging only the closing inventory |
| Revenue and collection | Record invoice date, net revenue period, trial/discount, renewal, due date, refund and actual settlement; annual cash collection is not twelve new monthly collections |
| Prepaid provider balance | Opening usable emails + purchased capacity − recipient emails consumed − capacity expired; retain purchase batches and expiry dates |
| Cash and funding | Opening bank cash + net settlements/other funding − cash payments, refunds and taxes not already netted; reconcile gateway deductions once |
| Forecast versus actual | Retain forecast quantity/rate, observed quantity, invoiced charge and variance reason for each environment/payer; a modeled request count is not observed billable usage |

For a bounded arithmetic exercise, suppose three consecutive, undated practice periods have **1, 5 and 25 equivalent full clinic-months** at the chapter23 per-clinic workload. This is an input sequence, not a customer forecast or growth deadline. It totals **31 clinic-months**, 32,240 completed visits and 58,032 new PDFs. At 150 KiB each and with no deletions or other files, closing inventory is **8.9137152 GB**; it is not the twelve-cohort 86.26176 GB comparison above. Storage during each period still depends on daily accumulation and other account use.

If, independently, each practice clinic-month consumes 2,080 recipient emails, the three periods consume 2,080, 10,400 and 52,000. Starting with no credits, buying only enough and assuming no intervening expiry requires **1, 1 and 5 credits**: **$2.50, $2.50 and $12.50 cash**. The final 5,520-email balance makes total purchases $17.50 versus $16.12 of consumption. Carry that balance forward instead of buying six credits again in every month. Actual cash may also include annual renewals, one-time onboarding, overdue collections and migration overlap.

The largest cumulative forecast cash deficit, plus a deliberately chosen reserve, determines starting funding need. A month with positive modeled contribution does not remove an earlier cash deficit or prove that receivables will settle on time.

## Budget Messages, Email and Payments Against Their Actual Units

### WhatsApp: intent, category and billable delivery differ

The public official calculator returned the following India/INR quotes on 28 October. They are **dated rate inputs**; reconcile the account rate card, template classification, customer-service window, delivered status, exemptions, volume tier, taxes and any Business Solution Provider (BSP) markup before treating them as a bill.

| Category | INR per quoted delivered message | Illustration if 52,000 messages are all billable at that rate |
| -------------------------------------------------- | -------------------------------- | ------------------------------------------------------------- |
| Utility | ₹0.115 | ₹5,980 |
| Authentication, first tier | ₹0.115 | ₹5,980 |
| Marketing | ₹0.8631 | ₹44,881.20 |
| Authentication international, only when applicable | ₹2.4971 | ₹129,849.20 |
| Service | ₹0.115 calculator quote | Apply verified per-phone allowance and current terms first |

There is an important source conflict: the [pricing narrative](https://whatsappbusiness.com/products/platform-pricing/) describes free service replies within the service window, while the [official FAQ](https://whatsappbusiness.com/resources/faq/) says service messages become charged from 1 October 2026, with 1,000 free service messages/business phone/month. Record this conflict instead of promising permanently free service traffic. Do not multiply a per-phone allowance by clinic count unless that many eligible business numbers actually exist. The INR rate card is not a conversion from the USD rate card.

The workload's 52,000 message **intents** are not 52,000 billed deliveries. Suppressed messages, consent failures, retries, accepted-but-undelivered attempts and duplicate deliveries must reconcile against provider billing. Each billable duplicate may cost money even if the application counts one logical notification. [Messaging mechanisms](06-whatsapp-integration.md) own identity, consent and reconciliation.

If Docita pays for all 52,000 billable utility deliveries, the example is ₹5,980 before tax/BSP. If the clinic owns and pays the provider account, record that as clinic expense rather than silently adding it to Docita's bill. A BSP may charge a markup, platform fee or minimum; using direct Meta access does not automatically eliminate all other provider costs.

### Email: distinguish credit purchase from consumption

Zoho's transactional email offering publishes **$2.50/credit of 10,000 recipient emails**, with paid credits expiring after **six months**, no monthly minimum and one-credit purchases allowed. [Explicit rate](https://www.zoho.com/cpaas/transition-guides/mailchannels.html), [credit rules](https://www.zoho.com/zeptomail/subscription.html).

At 52,000 recipient emails, six credits cost **$15 cash** if the opening balance is zero; 8,000 remain. Usage-equivalent cost is $13 before expiry/tax. Include all recipients according to provider rules, not just API call count. Do not amortize expired unused credits as successful deliveries. Signup allowances and temporary promotions do not belong in steady-state budgets. Domain verification, account approval, bounces, complaint handling and unsubscribe/consent boundaries still need an operator.

### Payments: amount and merchant ownership decide the fee

[Razorpay standard pricing](https://razorpay.com/pricing/) quotes **2% of successful eligible payment value**, plus applicable GST on the fee, with no setup/annual maintenance charge. A fee taxed at 18% gives `successful value ×0.02 ×1.18`; verify the contracted payment method/rate and invoice treatment. This is an arithmetic example, not tax advice or a claim that every method/contract is identical.

```text
₹100,000 successful eligible value -> ₹2,000 fee + ₹360 GST = ₹2,360
Docita subscriptions: use successful Docita merchant collections
Clinic patient payments: use successful clinic merchant collections
```

The workload's 5,200 payment attempts cannot determine charges without successful amounts, method, refunds and enabled extras. Patient collections are not Docita subscription revenue. Keep settlements, refunds, disputes and optional products as separate reconciliation lines; never assume a refund reverses every provider fee. [Payment ownership](04-payment-flows.md) and [subscriptions](09-subscription-system.md) own the application transitions.

## Complete the Budget Beyond the Infrastructure Table

| Cost line | Input and calculation | What must be checked |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Independent encrypted backups | Retained compressed GB ×chosen store rate +operations/transfer +restore compute | Provider history is not the independent copy; include keys, integrity readback and complete restore drills |
| Staging and previews | Runtime +database branches/storage +objects +edge usage | Isolation, expiry/cleanup and whether production allowances are shared |
| Error/log/trace monitoring | Plan minimum +retained/ingested units above quotas | Scrubbing, sample rate, retention and alert delivery; one request is not one error |
| Domain and business email | Annual renewals/12 +mailbox plan | Renewal price, taxes, DNS/TLS needs and cash-renewal date |
| CI and build systems | Billable minutes/storage/runner capacity after actual allowances | Private/public repository treatment, artifacts, image retention and concurrency |
| Security and connectivity | Extra IPs, private connection, secrets/KMS, scanning and audit storage | Necessary control, payer, region and retention; a free certificate does not operate the service |
| AI/OCR/transcription | Actual input/output tokens, pages, images or seconds ×selected model rate | No AI usage price assumed here; check provider, clinical scope, consent, quota and human review |
| Support and operations | Onboarding +training +support +on-call/incident +maintenance hours ×loaded hourly cost | Include unpaid operator time in economics, owner coverage and clinic opening hours |
| Customer acquisition | Monthly campaign/referral/travel spend +attributed sales labor; calculate acquisition cost per new paying clinic separately | A per-clinic acquisition metric is not a monthly expense; count paying conversion, refunds and time lag without duplicating sales hours |
| Taxes and currency | Invoice-specific tax, settled FX and card/bank fees | USD and INR totals stay separate until a dated rate is selected; no fixed exchange-rate claim |
| Contingency | Explicitly chosen percentage or cash reserve | A planning allowance is not a provider quote or proof that unknown costs are covered |

For a concrete monitoring option, [Sentry](https://sentry.io/pricing/) currently lists Developer at $0 and Team at $29/month, or $26/month billed annually. The latter implies $312 annual base cash before tax/extras, not a $26 monthly cash payment. Team's base includes 50,000 errors; [logs](https://sentry.io/changelog/logs-are-generally-available/) include 5 GB then $0.50/GB. Other product quotas/overages remain separate. These are alternatives to price, not evidence Docita currently has an active paid plan. A $0 account must still fit its user, event and monitoring limits.

The dated repository recovery record reports production backups disabled and only bounded synthetic Neon recovery evidence. A backup cost of zero in the comparison is an **unfunded readiness item**, not a recommended production policy. Give independent backup, complete restoration and delivered missed-run alert evidence a funded line before onboarding real clinical use. [Launch gates](25-launch-to-growth.md) explain the stop conditions.

Backup frequency can dominate its storage line. As a hypothetical sensitivity, hourly **full** archives retained for 31 days create 744 copies in steady inventory. If each encrypted compressed archive is 1 decimal GB, that is 744 GB; once other account usage has consumed R2's free storage, the incremental storage is **$11.16/month** at $0.015/GB-month. At 20 GB per archive it is **$223.20** before operations, readback/restore compute, transfer and labor. Neither archive size is inferred from the database's used bytes. First-month accumulation differs from steady inventory; retention locks, failed attempts and cleanup can also retain additional bytes. The recovery owner must fund measured archive size × frequency × retention and its verification work explicitly; the $20 allocation below is not a backup quote.

### A funding example with every assumed addition visible

Start with the **$75.00 Neon comparison**, not a claim about the live bill. Suppose a planning budget adds **$20/month** for domain amortization, independent backup, staging/restore usage and other small tooling, plus **$29 Sentry Team** and **$15 email credit purchase**. The $20 is an allocation to validate with quotes, not a statement those items necessarily fit. This gives **$139.00 USD/month** before tax, additional usage, labor and contingency, plus **₹5,980** if all 52,000 utility messages are billable and paid by Docita. Replacing the infrastructure line with the AWS comparison gives **$183.98 USD +₹5,980** under the same additions and omissions.

Count every ledger line once: the example already includes the $20 allocation and $15 email purchase. Replace those inputs with actual itemized costs when known; add only previously unfunded usage or work.

For fully loaded planning, add actual support hours ×hourly cost, the eligible Docita subscription gateway fee, chosen acquisition spend, and any AI/extra data transfer. Convert each foreign-currency invoice at a selected dated rate, then apply a stated reserve, for example **20% as a planning assumption**. Keep patient-merchant fees separate unless Docita contractually absorbs them. This formula exposes missing inputs instead of presenting an unjustified all-inclusive bill.

```text
Monthly funding need (sum of distinct ledger lines, no duplicated allocations) =
  converted infrastructure and tooling invoices
  + Docita-paid messaging/email/payment/AI usage
  + independent recovery + staging + operating labor + acquisition
  + applicable taxes/fees + explicitly chosen reserve
```

### Find the price and payer boundary before calculating break-even

Use one invoice currency and period. Let `F` be funded fixed operating cost, `R` net subscription revenue per paying clinic after discounts/refunds and excluding taxes owed, `B` the eligible subscription amount processed per paying clinic, `g` the applicable gateway-fee fraction, `V` variable service/support cost per paying clinic, and `U` additional cost of nonpaying pilots or other nonpaying use not already in `F`. Convert foreign-currency inputs at a selected dated rate. Under a homogeneous workload and stable cost profile:

```text
contribution per paying clinic = R − g × B − V
paying clinics needed = ceil((F + U) / contribution per paying clinic)
```

If contribution is zero or negative, adding the same kind of paying clinic cannot cover fixed cost. Recompute after a capacity step, workload mix or staffing change. With the illustrated 2% fee plus 18% GST on that fee, `g = 0.0236` for the cash-fee calculation; use the actual tax/contract treatment and processed base. `B` need not equal revenue `R`, particularly with invoice taxes, annual collections and refunds. The formula does not assume an actual SaaS price or promise an achieved margin.

For scale, the 25-clinic scenario allocates 2,080 billable utility deliveries to each full clinic-month: **₹239.20** before tax/BSP if Docita pays. The separate email exercise consumes **$0.52/clinic-month**. These are variable inputs only under their stated workload, not total cost per clinic. Clinic-paid messaging moves the payer boundary; it does not remove the clinic's cost. If 25 clinics consume service but only five pay, use five revenue contributors and include all 25 clinics' costs. Do not use $139 as `F` without removing its variable/prepaid lines and replacing the unverified allocation with a funded ledger.

### Test the assumption that changes the decision

The following increments use only the dated rates above. They are separate sensitivities, not a prediction that all will occur together.

| Changed input, holding other inputs fixed | Increment and decision |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Neon runs at 1 CU instead of 0.5 CU for 10% of a 720h month | Extra `0.5 × 72 × $0.106 = $3.816`, or **$3.82**; the $75.00 comparison becomes **$78.82** before excluded costs. Measure time at each compute size rather than billing every hour at the maximum or minimum |
| Another 100 GB traverses the billable Singapore Fly internet-egress meter | **+$4.00** at $0.04/GB. A direct R2 download and an API-proxied download can have different Fly costs |
| 10% of 52,000 previously utility deliveries are classified as marketing | **+₹3,890.12**, using `5,200 × (₹0.8631 − ₹0.115)` before tax/BSP. Verify category and intended purpose rather than selecting the cheaper label |
| Utility traffic has 5,200 additional billable duplicate deliveries | **+₹598** before tax/BSP; reconcile delivery identities and idempotency rather than treating logical intents as the invoice count |

A database/provider change needs both a normal forecast and a downside case. Use the same payer, service hours, recovery scope and volume in each; include migration overlap, failed-payment cash timing and support load. A reserve is a funding choice applied after identifying those costs, not a substitute for them.

## Reproduce the Infrastructure Arithmetic

This standalone Python example has no network access and changes no infrastructure. Inputs are the dated quotes above. The repeated workload is a model; it is not a measurement generator or actual billing importer.

```python
from decimal import Decimal as D, ROUND_CEILING, ROUND_HALF_UP

def fly(mib, hours):
    seconds = D(hours) * 3600
    base = D("0.0000008465")
    extra_ram = D("0.000002316") * (D(mib) / 1024 - D("0.25"))
    return (base + extra_ram) * D("1.269230769") * seconds

def usd(value):
    return value.quantize(D("0.01"), rounding=ROUND_HALF_UP)

def neon_compute(cu, hours):
    return D(cu) * D(hours) * D("0.106")

def scenarios(month_hours):
    hours = D(month_hours)
    pilot_hours = D(260)  # held fixed, not scaled with calendar length
    assert hours >= pilot_hours
    pdf_gb = D(46800) * 150 * 1024 / D(10**9)
    held_gb_month = pdf_gb * 12  # held inventory, not growing-month storage
    r2_units = held_gb_month.to_integral_value(rounding=ROUND_CEILING)
    r2 = max(D(0), r2_units - 10) * D("0.015")
    stopped_rootfs = D(2) * D("0.15") * (hours - pilot_hours) / hours
    pilot = (fly(512, pilot_hours) + fly(256, pilot_hours)
             + stopped_rootfs + D("0.04"))
    warm_small = fly(512, hours) + fly(256, hours)
    warm_medium = fly(1024, hours) + fly(512, hours)
    warm_two = fly(1024, hours) * 2 + fly(512, hours)
    rds_compute = D("0.102") * hours
    fly_static_egress = D(2) * D("0.005") * hours
    rds_public_ipv4 = D("0.005") * hours
    return {
        "parked_example": D("0.30"),
        "pilot_free": pilot,
        "pilot_launch": pilot + neon_compute("0.25", pilot_hours) + D("0.35"),
        "2_to_5": warm_small + neon_compute("0.25", hours)
                  + D("1.75") + 5 + D("0.20"),
        "6_to_10": warm_medium + neon_compute("0.5", hours)
                   + D("3.50") + 1 + 5 + D("0.40"),
        "11_to_25_neon": warm_two + neon_compute("0.5", hours)
                         + 7 + 1 + 5 + r2 + 1,
        "11_to_25_aws": warm_two + rds_compute + 50 * D("0.138")
                        + 5 + r2 + 1 + fly_static_egress + rds_public_ipv4,
    }

expected = {
    720: ["0.30", "2.93", "10.17", "33.50", "61.25", "75.00", "119.98"],
    744: ["0.30", "2.93", "10.17", "34.39", "62.96", "77.00", "123.51"],
}
for hours, amounts in expected.items():
    totals = scenarios(hours)
    assert [usd(value) for value in totals.values()] == [D(x) for x in amounts]
    print(hours, {name: str(usd(value)) for name, value in totals.items()})
```

The assertions preserve all seven **720h** totals: `$0.30`, `$2.93`, `$10.17`, `$33.50`, `$61.25`, `$75.00` and `$119.98`. At **744h**, they are `$0.30`, `$2.93`, `$10.17`, `$34.39`, `$62.96`, `$77.00` and `$123.51`, in the same order. Every hourly charge scales: Fly runtime, Neon compute, RDS compute and the three modeled hourly IP allocations. This comparison holds monthly storage inventory, the quoted monthly storage/rootfs charge basis, traffic and account minimums fixed. The pilot stays at 260 active hours and normalizes its stopped fraction by the selected month length. It is a calendar sensitivity exercise, not verified 31-day invoice arithmetic: actual GB-month normalization and per-second billing must follow each provider's usage statement. An extra day can also create additional real usage. Updating a price, region, schedule or retention input requires updating the comparison and its evidence date together.

## Let Usage and Service Risk Trigger the Next Change

At zero clinics, instrument the meters and set account budgets before a pilot. At the first clinic, record cold starts, business-hour runtime, reminder completion and support effort. At 2–5, make onboarding and cost allocation repeatable. At 6–10, compare forecast with invoices and inspect pool wait, tail latency, worker age, memory and retained-data growth. At 11–25, accept a measured workload and recovery profile before promising capacity. Beyond 25, forecast the busiest tenant and history growth, not just another average clinic.

Use a monthly worksheet: opening balances; usage by meter/environment/payer; included allowance consumed across the account; calculated charge; actual invoice; variance explanation; closing prepaid balance; forecast; owner/action. Alert on both rate of spend and service risk, for example a chosen 80% budget warning and a forecast above the approved cap. These are proposed thresholds. Verify that alerts reach the operator; do not stop a live database automatically to save money without a clinical continuity plan.

Before a Neon-to-AWS move, price the overlap month: both databases, migration transfer/compute, test environment, backup verification, operator time and retained snapshots. Move for measured capacity, recovery/control, locality or economics requirements. Clinic count alone does not justify the migration, Redis, replicas or microservices. Use the [Neon-to-AWS cutover sequence](25-launch-to-growth.md#move-from-neon-to-aws-with-a-cutover-decision) with the schema/release compatibility process in [deployment](10-deployment-infrastructure.md).

## Summary

The smallest machine price is only one part of a service budget. These scenarios make runtime, database, retained-object and network assumptions explicit, then add provider effects and operational obligations. Reconcile them with actual usage and invoices before treating the totals as Docita's costs or choosing the next growth profile.

## See Also

- [Operating-evidence workbook](27-operating-evidence-workbook.md) — turn resource/cost assumptions into bounded checks and a promotion record.
- [Launch through growth](25-launch-to-growth.md) — sequence, ownership, readiness and growth decisions.
- [Deployment and infrastructure](10-deployment-infrastructure.md) — actual configuration and future topology.
- [Workload and evidence model](23-hypothetical-clinic-metrics.md) — monthly counts, bursts and experiment scope.
- [Analytics definitions](14-analytics-and-dashboards.md) — event populations and measurement lineage.
- [Category revision](REVISION.md) — explain the cost and growth trade-offs without memorizing totals.

## References

- [Fly regional pricing](https://docs.fly.io/about/pricing), [billing](https://docs.fly.io/about/billing) and [static egress allocations](https://docs.fly.io/networking/egress-ips).
- [Neon plan limits and metered rates](https://neon.com/docs/introduction/plans).
- [Cloudflare Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/) and [R2 pricing](https://developers.cloudflare.com/r2/pricing/).
- [RDS PostgreSQL pricing](https://aws.amazon.com/rds/postgresql/pricing/), [Singapore price catalog](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRDS/current/ap-southeast-1/index.json) and [AWS public IPv4 pricing](https://aws.amazon.com/vpc/pricing/).
- Official India/INR WhatsApp calculator quotes: [utility](https://whatsappbusiness.com/wp-json/wab/v1/pricing?market=IN&currency=INR&category=Utility), [authentication](https://whatsappbusiness.com/wp-json/wab/v1/pricing?market=IN&currency=INR&category=Authentication), [marketing](https://whatsappbusiness.com/wp-json/wab/v1/pricing?market=IN&currency=INR&category=Marketing), [service](https://whatsappbusiness.com/wp-json/wab/v1/pricing?market=IN&currency=INR&category=Service) and [authentication international](https://whatsappbusiness.com/wp-json/wab/v1/pricing?market=IN&currency=INR&category=Authentication+International); read with the [FAQ](https://whatsappbusiness.com/resources/faq/) and [pricing narrative](https://whatsappbusiness.com/products/platform-pricing/).
- [Zoho explicit email rate](https://www.zoho.com/cpaas/transition-guides/mailchannels.html) and [credit rules](https://www.zoho.com/zeptomail/subscription.html).
- [Razorpay payment pricing](https://razorpay.com/pricing/).
- [Sentry plan pricing](https://sentry.io/pricing/) and [logs billing](https://sentry.io/changelog/logs-are-generally-available/).
