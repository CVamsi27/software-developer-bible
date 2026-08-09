---
section: Abroad Full-Stack Lane
category: Interview
tags: [study-plan, personal]
---

# 4-Week Senior Full-Stack Interview Prep Plan — Vamsi Krishna Chandaluri (Revised: v2 — take-home + DSA-lite)

> **Goal:** Land a senior full-stack TS role at n8n, SumUp, Scalable Capital, Peter Park, sennder, THRYVE, or similar EU mid-stage company
> **Time budget:** ~2-3h/day weekdays, ~4-5h/day weekends (~18-20h/week)
> **Total:** ~50-55 hours over 4 weeks (down from v1's 75-80h; dropped LeetCode grinding)
> **Style:** Take-home + system design + behavioral heavy. Light DSA (5-6 patterns at medium, 30-40 problems over 4 weeks, not 100+). No 500-problem grind.
> **Source of truth:** `cv.md`, `config/profile.yml`, `modes/_profile.md`, `interview-prep/story-bank.md`, `software-developer-bible/`

---

## What changed from v1

| | v1 (old) | v2 (this) |
|---|---|---|
| **Total time** | ~75-80h | **~50-55h** |
| **LeetCode problems** | 3-5 (light) | **30-40 (focused mediums)** |
| **LeetCode focus** | "Stay sharp" | **Defensive — phone screens at SumUp/sennder** |
| **Take-home** | One project, 5-8h | **Same — but with explicit scope and 2 variants** |
| **System design** | 5 cases, ~12h | **5 cases, ~14h (more reps)** |
| **Behavioral** | 8 stories practice | **8 stories practice (same)** |
| **Mocks** | 3-4 | **3-4 (same)** |

The trimmed time comes from dropping "exposure" LeetCode problems (where you read 5 patterns and solve 0-1 problems per pattern) and replacing with **focused medium-level practice on the 4-5 patterns that actually show up on phone screens at SumUp/sennder-style fintechs.** Real reps, not symbolic coverage.

---

## Top-level summary

This plan is **deliberately asymmetric**: **~50% system design + take-home (the real signal for n8n/SumUp/Scalable/Peter Park/sennder/THRYVE)**, ~20% behavioral (8 stories are already written — practice delivery, not new writing), ~15% light DSA (5-6 patterns at medium, defensive coverage for phone screens at fintechs), ~10% frontend depth (React/Next.js — the second signal for these companies), ~5% company research.

The single biggest differentiator for Vamsi at mid-stage EU: **ship a real take-home, then explain Docita end-to-end crisply, then design a system on a whiteboard for 45 minutes.** Everything else is secondary.

Three mocks minimum, four ideal. **No mock = no offer.** Sundays are recovery or shallow review only — burnout kills momentum faster than under-prep.

---

## DSA strategy: 5 patterns, ~30-40 problems, 25-30h total

**Why this and not "500 problems":**

SumUp and sennder have phone screens that test 1-2 mediums. The patterns they ask:
- **HashMap / Set** — most common, ~40% of phone screens
- **Sliding Window** — string/array problems, ~25%
- **Two Pointers** — array problems, ~20%
- **BFS/DFS** — tree/graph traversal, ~25%
- **Basic DP (1D only)** — climbing stairs, max subarray, ~10%
- **Heap** — top-K, merge K streams, ~10%

**Skip entirely:** Segment Tree, BIT, Bit Manipulation, KMP, Monotonic Stack, Union-Find, Topological Sort, 2D DP, hard graph algorithms. These are FAANG/LeetCode-hard, not SumUp/sennder bar.

**How to use the 5-6 patterns:**
- Week 1: First pass on the 5 core patterns. Solve 2-3 problems per pattern at medium, time-boxed to 25 min each. Goal: get familiar with the templates.
- Week 2: If a take-home is in flight, skip DSA. Otherwise, do 2-3 mediums from the patterns that feel weakest.
- Week 3: 2 mock phone screens that include 1 medium coding problem each. Use the bible's `19-Coding-Patterns/` files as templates.
- Week 4: Last-mile review. Solve 1-2 problems you've failed before, just to be sure.

**Total: 30-40 problems, ~25-30h, spread over 4 weeks. Not a grind, just defensive coverage.**

---

## Daily structure (recurring skeleton)

| Block | Time (weekday) | Time (weekend) | Purpose |
|------|---------------|---------------|---------|
| Block A — Deep work | 60-90 min | 2h | Hard skill (take-home, system design, or DSA) |
| Block B — Stories / soft skill | 30-45 min | 60 min | Behavioral practice, mock prep, reflection |
| Block C — Shallow / reading | 30-45 min | 60-90 min | Company research, blog reads, repo skims |
| Wind-down | 15 min | 15 min | Update `interview-prep/progress-log.md` (1 paragraph) |

**Rules:** No more than 3h hard focus on a weekday. One rest block per week minimum (no study Saturday afternoon OR Sunday morning — non-negotiable). Pomodoro 50/10 inside each block. Phone in another room. End each day with one sentence: "What did I learn / what's still unclear?" written into the progress log.

---

## Week 1: Foundation + Behavioral + Company Mapping

**Theme:** Get the foundation tight. Stories delivered out loud. Know the four target companies cold. Light DSA primer.

| Day | Tasks | Time |
|-----|-------|------|
| **Mon** | **Stories 1+2** — practice delivery out loud. Record Story 1 (Docita founding) and Story 2 (MAQ 30% latency) on phone, 3-4 min each, punchline-first. Review recording, note filler words. | 2.5h |
| **Tue** | **Stories 3+4** — same drill: Story 3 (25% delivery) and Story 4 (mentoring 4 engineers). Read `18-Behavioral/01-STAR-Method.md` once for the framework. | 2.5h |
| **Wed** | **Stories 5+6** — Story 5 (microservices tradeoff) and Story 6 (RBAC + audit). End-of-day: time yourself on the "Tell me about yourself" answer (target: 90 seconds, lead with Docita + a sentence on why EU). | 2.5h |
| **Thu** | **Stories 7+8** — Story 7 (85% coverage / 15% incidents) and Story 8 (observability). Then practice the **map**: for each of Stories 1-8, write 3 questions it answers. This becomes your quick-pick index. **DSA primer (30 min):** read `19-Coding-Patterns/01-Sliding-Window.md` and `19-Coding-Patterns/02-Two-Pointers.md` — no solving yet, just absorb the templates. | 3h |
| **Fri** | **DSA first-pass #1** — solve 2 mediums from HashMap pattern (top 100 frequency, two-sum variant). 25-min timer per problem. **End-of-day: schedule Mock 1 for Week 2** (friend, Pramp, or IG/Twitter #typescript peer). | 3h |
| **Sat** | **Company deep-dive #1 (n8n)** — read n8n engineering blog (last 6 months), GitHub `n8n-io/n8n` README + 2-3 recent merged PRs, product changelog. Read 1 system design case study (`11-System-Design/13-Rate-Limiter.md`) — n8n is workflow-engine, rate limiting is relevant. Take notes in `interview-prep/n8n-research.md`. | 4.5h |
| **Sun** | **REST.** Light week review (1h max): re-listen to one story recording, update progress log, look ahead at Week 2. **No study after noon.** | 1h |

**End-of-week deliverable:**
- All 8 stories delivered out loud, recorded, punchline-first
- "Tell me about yourself" at 90 seconds
- `interview-prep/n8n-research.md` populated
- Mock 1 scheduled for Week 2
- Story → question map written down
- 2 HashMap mediums solved (DSA first-pass started)

---

## Week 2: Take-Home Project (n8n-style) + DSA + First Mock

**Theme:** Ship a real take-home in 5-7 sessions, 6-10h total. This is your single most-leverage artifact for the EU mid-stage market. Plus continued DSA coverage.

| Day | Tasks | Time |
|-----|-------|------|
| **Mon** | **Take-home kickoff** — pick ONE small full-stack TS project that maps to n8n/SumUp style. Recommended: **mini workflow engine** (trigger + 3 node types + execution log + retry), OR **multi-tenant URL shortener with RBAC + audit log** (Docita-coded). Stack: NestJS + Prisma + PostgreSQL + React (Next.js). Read `06-NestJS/02-Controllers-Providers.md` and `08-Database/11-Prisma.md` if rusty. Set up repo. **DSA #2 (30 min):** solve 2 Sliding Window mediums (longest substring, min-size subarray sum). | 3h |
| **Tue** | **Take-home backend** — schema, migrations, 2-3 endpoints, RBAC guard, audit log table. Aim: working API with auth + 1 protected resource by EOD. | 3h |
| **Wed** | **Take-home backend continued** — add the core feature (workflow execution OR shortener redirect + analytics), 80%+ test coverage on the parts you build. **DSA #3 (30 min):** solve 2 Two Pointers mediums (3-sum, container with most water). | 3h |
| **Thu** | **Take-home frontend** — Next.js 15 page: list view + create + run/execute. Minimal, accessible, fast. Add 1 E2E test (Playwright). | 3h |
| **Fri** | **Mock 1 (60-75 min, scheduled earlier in week)** — Frontend deep-dive (30 min) + 1 medium coding problem (15 min — pick from HashMap/Sliding Window) + behavioral (15 min). Have a friend/peer play interviewer. Record it. **After mock: take-home polish (README, demo script, screenshots).** | 2.5h + mock |
| **Sat** | **Take-home polish + second company research** — write a clean README (problem, design decisions, what you'd do differently). Then research **SumUp**: engineering blog, careers page, recent Glassdoor reviews, 1 system design (`11-System-Design/06-Payment-Gateway.md` — SumUp is fintech, payments is core). **DSA #4 (45 min):** 2 BFS/DFS mediums (number of islands, max depth of binary tree). | 4.5h |
| **Sun** | **REST.** Optional: 1 light algo problem from `19-Coding-Patterns/07-Heap.md` for stretching. Otherwise full rest. **No study after noon.** | 0-1h |

**End-of-week deliverable:**
- Working take-home project (public GitHub repo, live demo if possible)
- `interview-prep/sumup-research.md`
- Mock 1 completed, recorded, reviewed
- 1 reflection written: "What would I do differently in the take-home if I had 24 more hours?"
- 8-10 DSA problems solved across 4 patterns (HashMap, Sliding Window, Two Pointers, BFS/DFS)

---

## Week 3: System Design + Frontend Deep-Dive + DSA

**Theme:** This is the make-or-break week. System design fluency = offer signal for senior+ at n8n/SumUp/Scalable.

| Day | Tasks | Time |
|-----|-------|------|
| **Mon** | **System design #1 — URL Shortener** (45 min timed, record yourself). Read `11-System-Design/01-URL-Shortener.md` for the answer key AFTER you finish. Use the 4-phase framework from `11-System-Design/17-How-to-Approach.md`. Then read `18-Behavioral/04-System-Design-Behavioral.md` for the soft-skill overlay. **DSA #5 (30 min):** 1 DP medium (max subarray) + 1 Heap medium (top-K). | 3h |
| **Tue** | **System design #2 — Notification Service** (45 min timed). `11-System-Design/07-Notification-Service.md`. Push the deep-dive on retry/backoff/DLQ — interviewers love that. | 3h |
| **Wed** | **System design #3 — Ticket Booking / Inventory** (45 min timed). `11-System-Design/08-Ticket-Booking.md`. Focus on consistency (strong vs eventual) and the "two users grab the last seat" problem. **Schedule Mock 2 for Friday.** | 2.5h |
| **Thu** | **Frontend deep-dive #1** — read `03-React/13-Performance.md`, `03-React/19-Modern-Hooks-React-18-19.md`, `04-NextJS/01-SSR-CSR-SSG-ISR.md`. Write 1-pager: "How I'd structure a Next.js 15 app for [SumUp / n8n]." Practice explaining out loud. **DSA #6 (30 min):** 2 more mediums from your weakest pattern (review your fail list from #2-#5). | 3h |
| **Fri** | **Mock 2 (60 min) — System design only + 1 coding problem.** Peer plays interviewer, picks one of {URL shortener, Notification, Ticket booking} you haven't practiced. Plus 1 medium from your strongest pattern. Record. Review, note 2 weaknesses. | 2h + mock |
| **Sat** | **System design #4 — Hospital Management** (45 min timed). `11-System-Design/10-Hospital-Management.md` — Vamsi already knows this domain (Docita is healthcare), use it as a confidence-builder. Then research **Scalable Capital**: blog, engineering posts, 1 case study (`11-System-Design/13-Rate-Limiter.md` is again relevant for fintech). | 4.5h |
| **Sun** | **REST.** Optional: 1 light algo problem from `19-Coding-Patterns/11-Intervals.md`. Otherwise full rest. **No study after noon.** | 0-1h |

**End-of-week deliverable:**
- 4 system designs explained end-to-end with timer, recorded
- `interview-prep/scalable-capital-research.md`
- Mock 2 completed
- 1-pager on Next.js 15 architecture
- Take-home repo polished, public
- 14-18 DSA problems solved (across 6 patterns: HashMap, Sliding Window, Two Pointers, BFS/DFS, DP, Heap)

---

## Week 4: Mocks + Final Polish + Live Applications

**Theme:** Convert prep into applications. The plan ends when applications are sent.

| Day | Tasks | Time |
|-----|-------|------|
| **Mon** | **System design #5 — Pick your weakest** of {URL Shortener, Notification, Ticket Booking, Hospital, Rate Limiter}. Re-record. **Send 2-3 applications** to target companies (n8n, SumUp, Scalable — go through `career-ops` pipeline). | 3h |
| **Tue** | **Behavioral polish session** — pick 6 hardest HR questions from `18-Behavioral/02-HR-Questions.md`. Practice out loud, time each at 2 min. | 2.5h |
| **Wed** | **Frontend deep-dive #2** — read `16-Testing/01-Overview.md`, `25-Accessibility/01-WCAG.md`, `26-Performance-Monitoring/01-Core-Web-Vitals.md`. Write 1-pager: "How I'd ship a feature at [company] — from spec to prod, including tests + observability." **DSA final review (45 min):** re-solve 2 problems you previously failed. | 3h |
| **Thu** | **Full mock 3 (90 min) — coding (1 medium) + 30 min system design + 15 min behavioral.** Self-record or peer. This is the dress rehearsal. | 2.5h + mock |
| **Fri** | **Company-specific mock 4 (60 min)** — pick the company most likely to move first (highest signal back from the application). Read `interview-prep/{company}-research.md` before. Have a friend grill you on "Why [company]?" "What would you do in your first 90 days?" | 2h + mock |
| **Sat** | **Final polish + applications push.** Update CV per `career-ops/generate-pdf.mjs` if any take-home lessons changed framing. Send remaining applications. **Schedule Mock 5** (optional, with a paid service like IGotAnOffer if budget allows) for early Week 5. | 4h |
| **Sun** | **REST.** Light review only. The hard work is done. Trust the prep. | 0-1h |

**End-of-week deliverable:**
- 5 system designs explained cold
- 3-4 mocks completed (4 if Mock 5 scheduled)
- 4-6 applications sent to n8n / SumUp / Scalable Capital / Peter Park / similar
- CV + portfolio polished
- 16-20 DSA problems solved across 6 patterns (defensive coverage, not mastery)
- Ready to start Week 5 (live interview prep) if any company moves

---

## Week 5 (Stretch / Only If Interviews Are Landing)

**Theme:** Live interview prep. Activated only if a company is scheduling a real loop.

| Day | Tasks | Time |
|-----|-------|------|
| **Mon** | **Company-specific deep-dive** — read the role's JD line by line, map every requirement to a story from `interview-prep/story-bank.md`. Write 1-pager "Why I'm a strong fit." | 2h |
| **Tue** | **System design drill on the company-adjacent domain** (e.g., if SumUp → Payment Gateway `11-System-Design/06-Payment-Gateway.md`; if n8n → Webhook delivery / event-driven). | 2.5h |
| **Wed** | **Mock 5 (paid service or strong peer)** — full loop. 90-120 min. | 2h + mock |
| **Thu** | **Final review** — re-record Story 1 cold, listen, fix any drift. | 1.5h |
| **Fri** | **INTERVIEW.** | — |
| **Sat-Sun** | **Recovery + next-prep cycle.** | rest |

**End-of-week deliverable:** Confident, on-message, on-time for the real loop.

---

## Mock Interview Schedule

The schedule is non-negotiable. Practicing out loud is the highest ROI activity in the entire plan. A senior engineer who has never said "I'll design a URL shortener" out loud will freeze at minute 8 of a real interview. Mocks de-freeze you.

| # | When | Type | Setup | Output |
|---|------|------|-------|--------|
| 1 | Week 2, Fri | Frontend deep-dive (30 min) + 1 medium coding (15 min) + behavioral (15 min) | Friend or peer (60-75 min) | Recording + 3 takeaway notes |
| 2 | Week 3, Fri | System design (45 min) + 1 medium coding (15 min) + debrief (15 min) | Friend or peer (60-75 min) | Recording + weakest-area list |
| 3 | Week 4, Thu | Full dress rehearsal: 1 medium coding + 30 min SD + 15 min behavioral | Self-record (90 min) | Recording + final fix list |
| 4 | Week 4, Fri | Company-specific (60 min) | Strong peer who knows the company | Recording + "Why this company" answer polished |
| 5 (optional) | Week 5, Wed | Full loop (90-120 min) | IGotAnOffer / Exponent / strong peer | If budget, do it. Best $200 you'll spend. |

**Mock setup checklist (each one):**
- [ ] Calendar invite sent ≥5 days ahead
- [ ] JD of the target role sent to the mock interviewer
- [ ] One specific system design case pre-assigned
- [ ] Recording (phone, Loom, or Zoom) set up
- [ ] After: write 3 things that went well + 3 things to fix in `interview-prep/mock-N-feedback.md`

---

## Pre-Interview Checklist (per company)

For each of **n8n, SumUp, Scalable Capital, Peter Park, sennder, THRYVE**, complete this 90-min block ≥48h before the interview:

- [ ] **Read the engineering blog** — last 6 months, every post. Note 1 thing that excited you, 1 thing you'd ask about.
- [ ] **Read the product changelog** — last 3 months, every release. Note 2 product bets you respect.
- [ ] **Skim 2-3 open-source repos** (if applicable) — pick recent merged PRs, read the code review comments, note the engineering bar.
- [ ] **Read the JD twice** — first time for content, second time with a pen. Map every line to a story from `interview-prep/story-bank.md`.
- [ ] **Prepare 3 questions for the interviewer** — at least one about team, one about product direction, one about how decisions get made.
- [ ] **Prepare the "Why this company" answer** — 60 seconds, specific, not generic. Must reference something concrete (a feature, a blog post, a repo).
- [ ] **Re-record Story 1 (Docita) and Story 2 (MAQ latency)** cold, listen once, fix drift.
- [ ] **Run a 25-min mock system design** on a case adjacent to the company's domain (e.g., for n8n → workflow engine, for SumUp → payment gateway, for Scalable → rate limiter).
- [ ] **DSA pre-call review (15 min):** re-solve 1 HashMap + 1 Sliding Window medium. The phone-screen warmup.
- [ ] **Logistics:** test video/audio, confirm calendar, charge phone, have water + notepad ready.
- [ ] **Family logistics:** tell wife and kid the interview window; reduce interruptions.

---

## Weekly Metrics to Track

Update `interview-prep/progress-log.md` every Sunday. If a number is below target by Week 3, escalate (add a block, don't skip recovery).

| Metric | Week 1 | Week 2 | Week 3 | Week 4 | Total Target |
|--------|-------:|-------:|-------:|-------:|-------------:|
| Stories practiced out loud (cold) | 8 | 8 (re-record) | 8 (spot-check) | 4 (polish) | 8 all, re-recorded ≥3x |
| System designs explained with timer (recorded) | 0 | 0 | 4 | 1 | **5** |
| Take-home projects shipped | 0 | 1 | 0 | 0 | **1** |
| Mocks completed | 0 | 1 | 1 | 2 | **3 (4 ideal)** |
| Company research files written | 1 (n8n) | 1 (SumUp) | 1 (Scalable) | 1 (Peter Park / sennder / 4th) | **3-4** |
| DSA mediums solved | 2 | 4 | 4 | 4 | **14-20 across 6 patterns** |
| Applications sent | 0 | 0 | 0 | 4-6 | **4-6** |
| Mock recordings reviewed | 0 | 1 | 1 | 2 | **4** |
| Hours logged | ~12-14 | ~14-16 | ~14-16 | ~12-14 | **~50-55** |

**Stop condition:** if 3+ metrics are off-target by end of Week 3, push Week 4 mocks to Week 5 and add recovery.

---

## Resource Map (bible files referenced)

### Core — used every week
- `software-developer-bible/18-Behavioral/01-STAR-Method.md` — framework, read once
- `software-developer-bible/18-Behavioral/02-HR-Questions.md` — Week 4 questions
- `software-developer-bible/18-Behavioral/04-System-Design-Behavioral.md` — Week 3 soft-skill
- `software-developer-bible/11-System-Design/17-How-to-Approach.md` — read ONCE before Week 3, then use the 4-phase framework
- `software-developer-bible/11-System-Design/INDEX.md` — case-study index, pick 5 from this

### System design case studies (Week 3 core)
- `11-System-Design/01-URL-Shortener.md`
- `11-System-Design/07-Notification-Service.md`
- `11-System-Design/08-Ticket-Booking.md`
- `11-System-Design/10-Hospital-Management.md` (domain fit — Vamsi knows healthcare)
- `11-System-Design/13-Rate-Limiter.md` (fintech / n8n workflow throttling)
- `11-System-Design/06-Payment-Gateway.md` (SumUp)

### Frontend deep-dive (Week 3-4)
- `software-developer-bible/03-React/13-Performance.md`
- `software-developer-bible/03-React/19-Modern-Hooks-React-18-19.md`
- `software-developer-bible/04-NextJS/01-SSR-CSR-SSG-ISR.md`
- `software-developer-bible/04-NextJS/02-App-Router.md`
- `software-developer-bible/16-Testing/01-Overview.md`
- `software-developer-bible/25-Accessibility/01-WCAG.md`
- `software-developer-bible/26-Performance-Monitoring/01-Core-Web-Vitals.md`

### Take-home prep (Week 2)
- `software-developer-bible/06-NestJS/02-Controllers-Providers.md`
- `software-developer-bible/06-NestJS/04-Guards-Pipes.md`
- `software-developer-bible/08-Database/11-Prisma.md`
- `software-developer-bible/09-Security/01-JWT.md`
- `software-developer-bible/09-Security/08-RBAC.md`
- `software-developer-bible/16-Testing/02-Jest.md`
- `software-developer-bible/16-Testing/06-E2E.md`

### DSA patterns (Week 1-4, defensive coverage)
Pick 2-3 mediums per pattern, 25 min timer, ~30-40 problems total. **Stick to the 5-6 core patterns below — skip the FAANG-hard ones.**

**The 5-6 patterns to use (defensive coverage for SumUp/sennder phone screens):**
- `19-Coding-Patterns/01-Sliding-Window.md`
- `19-Coding-Patterns/02-Two-Pointers.md`
- `19-Coding-Patterns/04-DFS-BFS.md`
- `19-Coding-Patterns/06-Dynamic-Programming.md` (1D only)
- `19-Coding-Patterns/07-Heap.md`
- `19-Coding-Patterns/18-Stack-Queue-Patterns.md` (basic stack/queue, not LRU/monotonic)

**The HashMap/Set pattern is so common it's worth its own ad-hoc study.** Read `19-Coding-Patterns/` introductions and solve 2-3 problems per pattern. Don't grind LeetCode; this is **defensive coverage** for the phone screen at SumUp or sennder.

**Skip entirely:** Segment Tree, BIT, Bit Manipulation, KMP, Monotonic Stack, Union-Find, Topological Sort, 2D DP, hard graph algorithms. These are FAANG/LeetCode-hard, not n8n/SumUp bar.

**Recommended problem sources (free):**
- LeetCode "Top Interview 150" (Easy + Medium) — pick 2-3 per pattern
- NeetCode 150 (https://neetcode.io) — same list, better organization
- Don't use "Blind 75" — too FAANG-heavy

### Reference (skim, don't deep-read)
- `software-developer-bible/00-Interview-Strategy/` — for the "communication" overlay
- `software-developer-bible/81-Indian-SDE-FAANG/01-Complete-Guide.md` — orientation only, this is for FAANG
- `software-developer-bible/81-Indian-SDE-FAANG/21-8-Week-Study-Schedule.md` — used to compare/contrast (this plan is the EU-mid-stage version, not the FAANG version)
- `software-developer-bible/20-CheatSheets/04-System-Design.md` — last-week review, not for learning

---

## Recovery & Anti-Burnout Rules

1. **One full rest block per week, non-negotiable.** Either Saturday afternoon OR Sunday morning, never both, but always one.
2. **No more than 3h hard focus on a weekday.** After 3h, retention collapses for senior engineers who already work full-time.
3. **Sundays after noon = phone off, no study.** Family is in `config/profile.yml` as a top-3 priority. Treat prep like a job; clock out.
4. **Two consecutive missed days = pause the plan and reset.** Don't push through. Skipping 1 day is fine, 2 is a signal to recalibrate.
5. **The plan is allowed to slip by 1 week.** If Week 2 is rough, the whole plan pushes back a week. Don't compress — 4 weeks is the minimum at the right intensity.

---

## When to deviate from this plan

- **If a real interview loop lands before Week 4:** stop the take-home (it's already done in Week 2), spend the freed time on the target company's domain case study. Move that company to Mock 4 priority.
- **If a take-home assignment comes in Week 1 from a real application:** skip the weekend company research, do the take-home instead. Real take-homes > plan tasks. Always.
- **If motivation collapses mid-Week 2:** skip Saturday's company research, take a long walk, come back Sunday. The plan will survive. Burnout won't.
- **If a friend offers a mock on short notice:** take it. A 60-min mock now is worth 3 hours of solo practice. Move the scheduled mock, don't add.
- **If a phone screen is scheduled for Week 2-3 and you're weak on a pattern:** drop the take-home polish, spend 4 hours on that pattern. Phone screens are time-sensitive.

---

## DSA problem selection (concrete)

**HashMap (8 problems)** — most common interview pattern, do this first
1. Two Sum (LC #1) — 5 min warmup
2. Top K Frequent Elements (LC #347)
3. Group Anagrams (LC #49)
4. Longest Consecutive Sequence (LC #128)
5. Valid Anagram (LC #242) — quick
6. Subarray Sum Equals K (LC #560)
7. Intersection of Two Arrays (LC #349)
8. Longest Substring Without Repeating (LC #3) — sliding window + hashmap combo

**Sliding Window (6 problems)**
1. Best Time to Buy/Sell Stock (LC #121)
2. Longest Substring Without Repeating (LC #3)
3. Minimum Size Subarray Sum (LC #209)
4. Longest Repeating Character Replacement (LC #424)
5. Permutation in String (LC #567)
6. Minimum Window Substring (LC #76) — harder, optional

**Two Pointers (6 problems)**
1. Valid Palindrome (LC #125)
2. Two Sum II - Input Array Sorted (LC #167)
3. 3Sum (LC #15)
4. Container With Most Water (LC #11)
5. Trapping Rain Water (LC #42) — harder, optional
6. Remove Duplicates from Sorted Array (LC #26) — quick

**BFS/DFS (5 problems)**
1. Number of Islands (LC #200)
2. Max Depth of Binary Tree (LC #104)
3. Same Tree (LC #100) — quick
4. Invert Binary Tree (LC #226) — quick
5. Course Schedule (LC #207) — topological sort intro

**1D DP (4 problems)**
1. Climbing Stairs (LC #70)
2. Maximum Subarray (LC #53)
3. House Robber (LC #198)
4. Coin Change (LC #322)

**Heap (3 problems)**
1. Top K Frequent Elements (already in HashMap, skip)
2. Kth Largest Element in an Array (LC #215)
3. Merge K Sorted Lists (LC #23) — optional, harder

**Total: ~30 problems across 6 patterns, ~25-30h, spread over 4 weeks.**

---

*Last updated: v2 — dropped LeetCode grinding, added 5-6 patterns at medium level with concrete problem list, kept take-home + system design + behavioral. Total time 50-55h. Review at end of Week 2 and adjust Week 3-4 focus if metrics are off.*
