<!-- section: Abroad Full-Stack Lane | category: Interview | tags: story-bank, personal -->
[![Section](https://img.shields.io/badge/section-Abroad%20Full-Stack%20Lane-blue)](.)
[![Category](https://img.shields.io/badge/category-Interview-red)](.)
[![Tags](https://img.shields.io/badge/tags-story-bank%20%C2%B7%20personal-lightgrey)](.)

# Story Bank — Master STAR+R Stories

> **Vamsi Krishna Chandaluri — Senior Full-Stack / Founding Engineer (5+ YoE)**
> Target roles: Senior SWE (TS/Node + React), Founding/Lead Engineer, Senior Backend (Node/NestJS), Platform/SaaS Engineer
> Target companies: n8n, SumUp, Scalable Capital + other EU senior engineering roles

## How to use this bank

This is a **story library, not a script.** You don't memorize and recite these. You adapt them.

- **For each behavioral question**, pick the story whose core punchline best matches what the interviewer is testing — not the story with the most impressive number. "Tell me about a time you disagreed with a teammate" wants Story 4 (mentoring/patience), not Story 1 (Docita).
- **Compress to fit the question.** A 60-second recruiter screen wants the S/T/A/R skeleton and one number. A 10-minute panel deep-dive can include the architecture detail and the reflection. Same story, different depth.
- **Lead with the punchline, not the setup.** "I cut API latency 30% by removing N+1s and adding indexes" beats "So there was this recruitment module at MAQ...". The setup goes in the second sentence.
- **Always end with the reflection.** That's the senior signal — juniors describe what happened, seniors extract lessons. If you can't articulate what you learned, the story reads junior.
- **Map questions → stories** in the per-audience pack in `interview-prep/{company}-{role}.md` (Step 5 of `modes/interview-prep.md`). Don't reuse the same story for two slots in the same panel — vary the angle.
- **Keep numbers exact.** Every metric in the Result section is pulled directly from `cv.md`. Don't round, don't exaggerate, don't add detail that isn't there.

**The Big Three:**
- "Tell me about yourself" → Story 1 (Docita founding) + Story 2 (MAQ perf track record) + a sentence on why EU/why now
- "Tell me about your most impactful project" → Story 1 (Docita) or Story 6 (RBAC + compliance)
- "Tell me about a conflict / mentoring / hard tradeoff" → Story 4 (mentoring) or Story 5 (microservices tradeoff in reflection)

---

## Stories

---

# Story 1: 0→1 founding engineering at Docita

> **Use when asked:** "Tell me about a time you built something from scratch." / "Describe a project you owned end-to-end." / "Have you ever been a founding engineer?" / "Tell me about your most impactful project." / "How do you handle scope when you're the only engineer?"
> **One-line summary:** As the sole founding engineer of a healthcare SaaS for Indian clinics, I designed and shipped a production multi-tenant system solo — backend, frontend, infra, the lot.
> **Companies/roles it fits:** Founding/Lead Engineer, Senior Full-Stack, Platform/SaaS, Senior Backend at a smaller EU company, n8n (full ownership archetype)

## Situation
Indian clinics run on paper prescriptions, handwritten registers, and WhatsApp messages. There's no affordable, multi-tenant SaaS that handles the full clinic workflow — check-in, OPD queue, consultation, digital prescription, billing, invoice, admin reporting. I joined Docita as the **sole founding engineer** in August 2025 to build that platform. No prior codebase, no team, no reference implementation to copy.

## Task
My responsibility was end-to-end: own the system architecture, design the multi-tenant data model, build the backend and the frontend, ship to paying clinics, and keep it running in production. There was no one to delegate to and no spec to follow — I had to make the architecture calls and the deadline calls myself.

## Action
- **Backend:** Built a multi-tenant NestJS service with Prisma ORM on PostgreSQL. Designed the schema for clinics-as-tenants with strict row-level isolation, set up migrations, added input validation, query optimization, indexing, and connection pooling so the system wouldn't fall over once multiple clinics were live.
- **Auth + security:** Implemented JWT authentication, role-based access control (receptionist, doctor, admin), and an immutable audit log for every sensitive healthcare and billing action. Healthcare data has regulatory weight, so this wasn't optional.
- **Frontend:** Built the clinic workflows in React + Next.js 15 — patient check-in, OPD queue, consultation view, digital prescription, billing, invoice generation, admin reporting dashboards. Responsive, accessible, fast.
- **Integrations:** Email automation, WhatsApp notifications, structured logging with production monitoring and observability wired in from day one.
- **DevOps:** CI/CD pipelines, containerized deployments, production infrastructure managed by me. I was the on-call too.

## Result
Docita shipped to paying Indian clinics and is running in production. End-to-end ownership of system → database → API → frontend → deploy, by one person. The platform handles real clinic workflows (patient check-in through invoice) for real users, and the audit + RBAC foundations are in place to grow into a larger customer base.

## Reflection
If I were doing it again, I'd do three things differently: **bring in a co-founder or first engineering hire earlier** — past month 3, the solo model stops scaling and the bus factor becomes a real risk; **write more E2E tests before the first clinic went live** — I leaned on manual smoke tests and paid for it in the first month of production bugs; **instrument observability from day 1, not week 6** — when something broke at 2am in week 2, I was guessing instead of looking. The big lesson: "shipping fast" and "ship fast with the safety net already in place" feel like opposite choices when you're solo, but the second one is faster in total.

---

# Story 2: Cut API latency 30% at MAQ Software

> **Use when asked:** "Tell me about a time you optimized performance." / "Describe a time you made a system faster." / "How do you debug a slow system?" / "Tell me about a technical decision driven by data."
> **One-line summary:** I diagnosed slow recruitment-module APIs at MAQ, then cut response times 30% by removing N+1 access patterns, adding indexes, and tuning queries.
> **Companies/roles it fits:** Senior Backend, Senior Full-Stack, Platform, n8n (perf-critical workflows), SumUp/Scalable Capital (latency-sensitive fintech)

## Situation
At MAQ Software I was working on recruitment and internal workflow modules — the kind of systems that get hammered all day by recruiters who notice every extra second. The recruitment module's API response times had grown to the point where recruiters were complaining, and the team was treating it as "just how it is." Performance reviews flagged it as a top-three user pain.

## Task
My responsibility was to make the recruitment APIs fast again without a rewrite and without breaking the dozens of features layered on top of them.

## Action
- **Profiled first, didn't guess.** Spent a day reproducing the slow paths in staging with logging and a query profiler, so I knew which endpoints were actually slow and which queries inside them were the bottleneck.
- **Removed N+1 access patterns.** The biggest win came from a list endpoint that was looping over a result set and firing a separate query for each row's related data. Replaced with a single batched query (two queries + in-memory join, not 200+).
- **Added indexes on the hot lookup columns** that the recruitment filters were hitting on every request but the schema had missed.
- **Tuned the remaining slow queries** (rewrote one as a single SQL with a subquery, simplified joins in two others).
- **Caching** for the most-hit read paths that didn't need to be live — the dashboard's "today's stats" endpoint, recruitment filter dropdowns.

## Result
**30% reduction in API response times** for the recruitment module, measured before/after on the same endpoints with the same traffic pattern. The N+1 fix alone was most of it — the lesson being that the dumbest problems are sometimes the biggest wins.

## Reflection
I should have started with APM-style observability *before* optimizing, not after. I was symptom-driven ("this endpoint is slow, why?") when I could have been measurement-driven ("here are the top-10 slowest endpoints by p95, ranked by traffic, here's where to spend the day"). Symptom-driven optimization works but it means you find out late that you fixed the wrong thing on a different endpoint. Now I want a profiler or a slow-query log running on day one of any system I touch.

---

# Story 3: Cut delivery time 25% at MAQ Software

> **Use when asked:** "Tell me about a time you improved team velocity." / "How do you balance speed and quality?" / "Describe a refactor that paid off." / "Tell me about a time you paid a short-term cost for a long-term win."
> **One-line summary:** I refactored the MAQ recruitment + workflow modules around reusable TypeScript patterns and a shared component library, and the team shipped 25% faster with 20% less UI duplication.
> **Companies/roles it fits:** Senior Full-Stack, Tech Lead, any role that touches team velocity, SumUp (delivery speed at scale)

## Situation
At MAQ Software, the recruitment and internal workflow modules had grown organically over a couple of years. Each new feature meant new code, not necessarily new *patterns* — there were three slightly-different ways to do the same thing, and UI was the worst offender (each form/table was hand-rolled, often with subtle differences in validation, error display, and loading states). Sprint planning was honest: "this is a 3-week story" really meant "we'll get to it eventually."

## Task
My responsibility was to break this cycle without grinding the team to a halt. I needed to make the codebase faster to work in, not just faster on the wire (that's Story 2). I was tech lead on the modules, so the refactor decisions and the on-time-delivery outcomes were both mine.

## Action
- **Identified the highest-leverage refactors** by looking at where the team kept writing the same code. Top hits: form components, table components, API client wrappers, auth guards, error boundaries. These were duplicated across 5+ feature areas each.
- **Established a shared TypeScript component library** (React + TypeScript) for the UI layer. I picked the abstraction level carefully — too generic and nobody uses it, too specific and it just becomes a fork. I aimed for the middle: opinionated defaults, escape hatches where needed.
- **Refactored service boundaries in the backend** — clearer module seams, fewer cross-module imports, and a small set of reusable service patterns (validation, error shape, pagination) that new endpoints could plug into instead of reinventing.
- **Wrote the new patterns once and migrated the high-traffic surfaces first** so the team could see the new pattern pay off in production before we asked them to adopt it for new code.
- **Coached the team through code review** to use the new patterns — the refactor only stuck because the next 10 PRs followed it.

## Result
**25% faster delivery** on recruitment and workflow module work, **20% less UI duplication** measured by component-import reuse and a manual audit of duplicated JSX. Sprint predictability improved (related: Story 4).

## Reflection
Refactoring always feels like a tax while you're doing it. The temptation is to skip it — "we'll just write the new feature on top of the old code, debt later." What I learned is that the tax is paid once and the dividend comes back over the next 6–12 months. The pattern I now default to: every time I write the same code for the third time, I stop and extract. Two repetitions is fine. Three is a signal. Also: refactors only work if the team adopts them — the migration is the work, not the abstraction.

---

# Story 4: Mentored 4 engineers, lifted sprint predictability 20%

> **Use when asked:** "Tell me about a time you mentored someone." / "How do you grow engineers on your team?" / "Describe a leadership challenge." / "How do you balance your own delivery with helping others?" / "Tell me about a conflict you resolved."
> **One-line summary:** At MAQ I grew 4 mid-level engineers to senior through code reviews, design sessions, and pair programming — and the team got 20% more predictable on sprint commitments along the way.
> **Companies/roles it fits:** Senior Full-Stack, Tech Lead, Senior Backend at EU companies that emphasize mentorship (SumUp, n8n culture fit), any role at a company that values engineering culture

## Situation
At MAQ Software, the recruitment and workflow modules were staffed by 4 mid-level engineers who were capable but inconsistent — they shipped, but design decisions varied wildly from PR to PR, code review was rubber-stamped, and sprint commitments were missed more often than not. I was the most senior engineer on the modules and the de facto tech lead.

## Task
My job was to get those 4 engineers to senior level without tanking my own delivery. The team had a roadmap, and the company wasn't going to slow down so I could run a mentoring program — the mentoring had to happen *inside* the work.

## Action
- **Code review as the primary mentoring surface.** Not nitpicks — focused, written feedback on the design choices in each PR: why one approach scales and another doesn't, what the failure modes look like, what the test gaps are. I treated each review as a 5-minute teaching moment.
- **Weekly system design sessions.** Pulled one or two of them into 30-minute design chats before they started non-trivial work. Not me designing and them watching — I'd ask the questions and let them drive the design, then push back where it was weak.
- **Pair programming for the hard bugs** — when a senior-level engineer would have unblocked the same bug in 20 minutes, I'd pair instead and let the engineer drive. Slower that day, faster for the next 10.
- **Structured 1:1s** for career growth — where do they want to be in 12 months, what's blocking them, what stretch work can I route their way.
- **Made the mentoring visible to my own manager** so it counted in performance reviews, not just my output.

## Result
All 4 engineers grew meaningfully — three were promoted to senior within ~12 months, and the fourth pivoted into a backend-specialist role that better matched his strengths. **Sprint predictability improved 20%** (commitment vs delivery rate over the next 4 quarters). I also noticed I was happier at work — the team was operating at a level I couldn't reach alone.

## Reflection
The hardest part of mentoring as a senior engineer is **being patient when I could just do the task myself in half the time.** The short-term cost is real and it's tempting to skip. The compounding return is that the team carries more weight, makes better decisions without me, and the things I'm uniquely good at become the things only I do — which is where a senior engineer should be spending their time. The second lesson: mentoring that happens inside the work (PRs, design sessions, pairing on real bugs) beats mentoring that happens in scheduled "learning time" — engineers learn the patterns they need, not the patterns I think they need.

---

# Story 5: Built a microservices platform at Cognizant

> **Use when asked:** "Describe a system you built from scratch." / "Have you worked with microservices?" / "Tell me about a time you had to make an architectural tradeoff." / "How do you decide between monolith and microservices?"
> **One-line summary:** As a Programmer Analyst Trainee at Cognizant, I built the Spring Boot microservices backbone for an e-commerce platform — Product, Vendor, Retail Shop, Proceed-to-Buy — with Eureka discovery, Zuul gateway, and JWT auth.
> **Companies/roles it fits:** Senior Backend, Platform, n8n (workflow services), any role that asks "have you actually built a distributed system"

## Situation
At Cognizant, the team was breaking an e-commerce monolith into a microservices platform. I was early in my career — a Programmer Analyst Trainee — but I was assigned to the foundational services because the work needed to ship. The monolith had coupling problems: every release was high-risk, and scaling one product area meant scaling the whole app.

## Task
I was responsible for building the core services and the cross-cutting infrastructure that would let other teams ship features on top. That meant the catalog (Product), the supplier side (Vendor), the storefront (Retail Shop), and the checkout step (Proceed-to-Buy) — plus the discovery and routing layer that tied them together.

## Action
- **Built four Spring Boot services** — Product, Vendor, Retail Shop, Proceed-to-Buy — each with its own bounded data model and REST API. Kept the contracts clean and explicit because inter-service calls were now over the network.
- **Set up Eureka Discovery Server** as the service registry so services could find each other without hardcoded URLs (which is a non-starter the moment you have more than 3 services).
- **Built a Zuul Gateway** for API routing, load balancing, and a single ingress point for clients. Centralized concerns like auth and rate limiting here instead of every service.
- **Implemented JWT-based authentication** in a dedicated Authorization Service with role-based access control, so the gateway could verify tokens without calling the user service on every request.
- **Centralized configuration** so deployment-time changes didn't require rebuilding every service.

## Result
The platform shipped into production. The four services handled real catalog, vendor, storefront, and checkout traffic, with discovery + gateway + JWT auth wiring them together. The team was able to deploy services independently — the operational goal of the break-up.

## Reflection
The operational complexity of microservices is a **real cost** that nobody talks about enough in the "let's break up the monolith" pitch. Service discovery, distributed tracing, inter-service auth, network failures, partial outages, deployment ordering — all of this is new surface area that didn't exist in the monolith. I wouldn't recommend microservices for a small team or a young product; the cost outweighs the benefit until you have a real scaling or team-boundary reason. The thing I now look for in candidates is whether they can articulate *when not* to use microservices, not just *how* to build them.

---

# Story 6: RBAC + audit logging for healthcare compliance

> **Use when asked:** "Tell me about a time you had to build for a regulated domain." / "Describe a security or compliance problem you solved." / "How do you think about access control?" / "Tell me about a project where the stakes were high."
> **One-line summary:** At Docita I designed role-based access control for receptionists, doctors, and admins, plus an immutable audit log for every sensitive action — so Indian clinics could control who-sees-what and stay regulator-ready.
> **Companies/roles it fits:** Founding/Lead, Platform/SaaS, Senior Backend, any role that mentions compliance/regulated data, n8n (multi-tenant permissions), Scalable Capital (RBAC + audit)

## Situation
At Docita, every clinic has at least three distinct user types — receptionists who handle check-in and billing, doctors who see patient records and write prescriptions, and admins who manage the clinic itself. Patient data is healthcare data, which means regulatory scrutiny and real liability if it leaks. The off-the-shelf auth approach (everyone is an admin, hide the buttons they shouldn't click) was not an option.

## Task
My responsibility was to design and implement a role-based access control system that *actually* enforced the boundary between roles, plus an immutable audit log of every sensitive action so we could answer "who looked at this patient record and when" if a regulator — or the clinic owner — ever asked.

## Action
- **Modeled roles and permissions explicitly** — receptionist, doctor, admin — and built a permission system that checked the role on every protected endpoint, not just on the UI. The UI hides controls the role can't use; the backend refuses the request even if the UI is bypassed.
- **Built an immutable audit log** that recorded actor, action, target, timestamp, and a snapshot of the relevant data for every sensitive healthcare and billing action: viewing a patient record, writing a prescription, changing a billing record, exporting data, logging in.
- **Implemented JWT-based authentication** as the session layer, with role claims that the RBAC layer consumed. Tokens were short-lived, refresh was explicit, secrets never lived in the repo.
- **Made the audit log append-only at the database level** — no UPDATE or DELETE grants on the table for the application user, so even a bug in the app couldn't rewrite history.
- **Reviewed the design with a clinic owner** before launch to make sure the role boundaries matched how Indian clinics actually operate (e.g., a single doctor often also acts as their own admin in small clinics).

## Result
The RBAC + audit logging shipped and is in production at paying clinics. The system passed early compliance-style reviews, clinic owners could see exactly who did what, and the regulator-question "show me every prescription Doctor X wrote in March" is a one-query answer instead of a forensic exercise.

## Reflection
In retrospect, I would have used a managed identity provider (Auth0, Clerk, WorkOS) for the auth + RBAC layer instead of building it myself. The reason I didn't was cost and a 2025-era concern about PHI leaving the local region — but a well-configured Auth0/Clerk with the right region pinning is probably the right call today, and the time I spent on session management, password reset flows, and MFA plumbing is time I should have spent on the clinic workflows themselves. The audit log, on the other hand, I would absolutely build in-house — it's domain-specific and the off-the-shelf options don't model healthcare actions well.

---

# Story 7: Lifted test coverage to 85%+, cut production incidents 15%

> **Use when asked:** "How do you think about testing?" / "Tell me about a time you reduced bugs in production." / "Describe how you've improved engineering processes." / "How do you balance shipping fast with quality?"
> **One-line summary:** At MAQ I tightened the CI/CD pipeline with automated tests, structured error handling, and release gates — driving coverage above 85% and cutting production incidents 15%.
> **Companies/roles it fits:** Senior Full-Stack, Senior Backend, Platform, any role that asks about engineering rigor, Scalable Capital (regulated fintech demands this)

## Situation
At MAQ Software, production incidents were the team's biggest tax. Something was breaking in prod every week or two, the on-call rotation was draining, and customer trust was eroding. The team had tests but coverage was patchy, the CI pipeline didn't catch the regressions that mattered, and error handling was inconsistent — some services threw, some returned nulls, some logged and continued. The fix wasn't "write more tests" — it was a process problem disguised as a quality problem.

## Task
My responsibility was to reduce the incident rate without slowing the team's delivery. The team had a roadmap and a deadline — I couldn't add two weeks of "stabilization" to every sprint. The improvements had to be incremental and visibly pay for themselves.

## Action
- **CI/CD pipeline hardening** — every PR runs lint, type-check, unit tests, and integration tests. Failing CI blocks merge. No more "I'll fix it in the next PR."
- **Coverage gates** with a moving target: started by enforcing coverage on changed files, then on the modules with the highest incident history, then raising the bar quarter by quarter. Got to 85%+ on the actively-developed modules without a freeze.
- **Structured error handling** — picked a single error shape across services (typed errors with codes and messages), wrapped external calls consistently, and made sure errors were caught, logged with context, and surfaced. No more silent failures.
- **Release checks** — a short pre-deploy checklist that ran automatically: migrations applied, feature flags toggled correctly, smoke tests passed against staging. Caught the dumb stuff before it hit prod.
- **Made the team's incident postmortems a learning input**, not a blame session — every incident fed back into a test or a guardrail that would catch the next one.

## Result
**85%+ test coverage** maintained on the modules I owned. **15% reduction in production incidents** quarter-over-quarter. On-call load dropped enough that the team stopped dreading the rotation.

## Reflection
Testing is a **culture problem, not a tooling problem.** I could have set up the best CI/CD pipeline in the world and the team would still have skipped the tests if the culture treated tests as a tax. What actually moved the needle: making tests the path of least resistance (fast, in-editor feedback), making the team see the link between "we added a test for X" and "X didn't break in prod this quarter," and getting leaders to celebrate the catch-not-the-bug moments. The pipeline was the necessary substrate. The culture was the actual lever.

---

# Story 8: Production observability and incident response

> **Use when asked:** "Tell me about a time you dealt with a production incident." / "How do you debug systems in production?" / "Describe how you've improved observability." / "What's your on-call philosophy?"
> **One-line summary:** At MAQ I built out structured logging, failure monitoring, and incident triage workflows — and cut the time-to-diagnose on production issues from "hours of guess-and-check" to "minutes, with the right log line."
> **Companies/roles it fits:** Senior Backend, Platform, Senior Full-Stack, any role that mentions SRE/on-call/observability, n8n + SumUp (both operate at scale), Scalable Capital (fintech reliability)

## Situation
At MAQ Software, when something broke in production, the on-call engineer's first hour was archaeology. Logs were unstructured (or absent), there was no consistent monitoring, and triage meant scrolling through noise looking for the one error that mattered. The mean time to diagnose a production issue was high, and the team's confidence in shipping anything new was low because they couldn't tell what was happening in the system.

## Task
My responsibility was to make production issues diagnosable in minutes instead of hours. Not to eliminate incidents — that's a different problem — but to make the response cheap, the postmortem fast, and the team confident that when something broke, we'd know what.

## Action
- **Structured logging everywhere** — every service emitted JSON logs with consistent fields (request ID, user ID, service, action, duration, status). Replaced free-form `console.log("got here")` style logs with logs that could be queried.
- **Failure monitoring** wired up to the logs — alerts on error rate spikes, latency regressions, and specific exception types. Alerts had to be actionable; the rule was "if the alert fires and you can't do anything, it's not an alert, it's noise."
- **Incident triage workflow** — when something fired, the first action was always "check the structured logs for the failing service in the last N minutes," not "scroll through CloudWatch." The workflow was documented, taught to the team, and run through in incident drills.
- **Request tracing** for cross-service issues — a request ID that flowed from the gateway through every service, so a single slow request could be followed end-to-end.
- **Post-incident review** — every P1/P2 got a 30-minute blameless review, the output was a list of follow-ups, and the follow-ups had owners and dates.

## Result
Diagnosis time for production issues dropped significantly — most P2s were diagnosed inside the structured-log query that fired, not after hours of grep. The team went from dreading incidents to handling them as a normal part of the job. Production deployment confidence went up; we shipped faster *because* we could see what was happening, not despite it.

## Reflection
The lesson I took from this: **observability must be designed in, not bolted on.** When I started the work, I was trying to add logging to a system that wasn't built for it, and it was a tax on every change. When I built it into new services from day one (which I did at Docita), it was almost free. The second lesson: **on-call rotations only work if the alerting is meaningful.** A rotation with noisy alerts is a human-rights violation; people burn out and quit, and the rotation fails. A rotation with a small number of well-tuned alerts and good runbooks is sustainable. I'd rather have three alerts I trust than thirty I ignore.
