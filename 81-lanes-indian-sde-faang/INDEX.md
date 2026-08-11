# Indian SDE / FAANG Lane — The Complete Reference

> **For senior engineers (5+ YoE) targeting Indian SDE roles AND FAANG / Big Tech positions** — Microsoft, Google, Amazon, Meta, Apple, Adobe, in-country India product companies, and US-based roles with H1B/STEM-OPT sponsorship. **DSA-heavy**, 8-12 week intensive prep, 4-6 hrs/day. The bar is LeetCode mediums to hards on the phone screen.

[![Files](https://img.shields.io/badge/files-23-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Interview-red)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Table of Contents

| # | Section | Purpose |
|---|---------|---------|
| 1 | [Lane Decision](#lane-decision--is-this-the-right-lane-for-you) | When to use this lane (decision matrix with ✅/❌ per company type) |
| 2 | [Reference Topics — What You Need to Know](#reference-topics--what-you-need-to-know) | The checklist — what you need to know (3 tiers: mandatory / common / differentiator + skip list). This is the "perfect reference" part. |
| 3 | [Interview Process — Round-by-Round](#interview-process--round-by-round) | Round-by-round — what each round tests, format, duration, what gets you rejected, how to prep |
| 4 | [Strategy — How to Prep, What to Skip, When to Apply](#strategy--how-to-prep-what-to-skip-when-to-apply) | The 80/20 — what to skip, when to start applying, comp strategy (US FAANG + India in-country), visa strategy (H1B / Blue Card) |
| 5 | [Files in This Lane](#files-in-this-lane) | Current deliverables (with file counts) |
| 6 | [Cross-references to Core Sections (1-7 + 0)](#cross-references-to-core-sections-1-7 + 0) | Where to study (the 8 themed groups) |
| 7 | [FAQ](#faq) | Common questions |
| 8 | [Navigation](#navigation) | ← Previous · 🏠 Home · Sibling Lane → |

---

## Lane Decision — Is This the Right Lane for You?

| If you are targeting... | Use this lane (81)? | Or use Abroad Full-Stack (82)? |
|--------------------------|:-------------------:|:------------------------------:|
| **FAANG in the US** (Google MTV, Meta Menlo Park, Apple Cupertino) | ✅ **primary** | — |
| **FAANG in EU** (Google Zürich, Meta London, Microsoft Dublin, Apple Cork) | ✅ **primary** | secondary (for family/visa overlay) |
| **Big Tech EU** (Booking.com, Spotify, Klarna) | secondary | ✅ **primary** |
| **US Big Tech via H1B / STEM-OPT** | ✅ **primary** | secondary |
| **Indian in-country** (Bangalore, Hyderabad, NCR product companies) | ✅ **primary** | — |
| **Adobe, Oracle, Cisco, VMware, Salesforce** (India + US) | ✅ **primary** | — |
| **EU / non-Indian mid-stage startups** (n8n, SumUp, sennder, THRYVE) | secondary | ✅ **primary** |
| **Remote-first US startups** (Stripe, Linear, Vercel) | secondary | ✅ **primary** |
| **Junior roles (under 3 YoE)** | — | start with fundamentals first |

**Quick heuristic:** if the company's **phone screen has a LeetCode medium-to-hard problem**, you're in this lane. If the company is **mid-stage and uses take-homes instead**, you're in 82.

**The "both" case:** European companies like Booking.com and Spotify run FAANG-style loops. For them, **use both lanes** — start with 31 for the FAANG-DSA signal, then layer 32's family/visa/relocation overlay.

---

## Reference Topics — What You Need to Know

This is a **reference checklist** of every topic a senior Indian SDE / FAANG candidate should be ready for. It is **non-duplicative** with the core stacks 1-7 + 0 (which contain the actual deep-dive content). This is the **what to be ready for**; the core sections are **where to study it**.

### Tier 1 — Mandatory, will be asked in 90%+ of FAANG interviews

| Topic | What you need to demonstrate | Where to study |
|-------|------------------------------|----------------|
| **Data Structures & Algorithms** | Arrays, Strings, HashMaps, Trees (BST + balanced), Graphs (BFS/DFS/Union-Find), Linked Lists, Stacks, Queues, Heaps. Implement from scratch in your strongest language. | [Coding Patterns](../../interview-toolkit/coding-patterns/INDEX.md) |
| **Dynamic Programming** | 1D and 2D DP, knapsack, LCS/edit distance, coin change, climbing stairs, house robber, longest increasing subsequence. **This is the FAANG bar.** | [Coding Patterns/06 Dynamic Programming](../../interview-toolkit/coding-patterns/INDEX.md) |
| **Graphs** | BFS, DFS, topological sort, Dijkstra, Union-Find, MST (Kruskal/Prim). Code on whiteboard in 20 min. | [Coding Patterns](../../interview-toolkit/coding-patterns/INDEX.md) + [Complete Guide](complete-guide.md) |
| **Object-Oriented Design** | Design a parking lot, URL shortener, hotel booking, library management. Class diagrams, design patterns applied. | [Design Patterns](../../backend/design-patterns/INDEX.md) + [Core Cs Fundamentals](core-cs-fundamentals.md) |
| **System Design at 45 min** | URL shortener, WhatsApp, Instagram, Twitter timeline, Uber, Netflix, Dropbox. With back-of-envelope estimates. | [System Design](../../architecture/system-design/INDEX.md) |
| **Concurrency & multithreading** | Threads, locks, deadlocks, semaphores, producer-consumer, dining philosophers, rate limiters. **Asked at Meta, Google, Amazon.** | [Core Cs Fundamentals](core-cs-fundamentals.md) |
| **Operating Systems** | Process vs thread, virtual memory, paging, context switching, scheduling, file systems, IPC. | [Core Cs Fundamentals](core-cs-fundamentals.md) |
| **Database design** | Normalization, indexes, transactions, ACID, query optimization, joins, NoSQL vs SQL trade-offs. | [Database](../../backend/database/INDEX.md) + [Complete Guide](complete-guide.md) |
| **Networking basics** | HTTP, TCP/IP, DNS, TLS handshake, REST, GraphQL, gRPC. | [Core Cs Fundamentals](core-cs-fundamentals.md) + [REST API](../../backend/rest-api/INDEX.md) |
| **Coding on whiteboard / shared doc** | Can write a working solution with clear variable names, edge cases, and complexity analysis in 25-30 min. **No IDE, no autocomplete.** | Practice with timer |
| **Behavioral — STAR + company values** | 5-8 stories, lead with result, Amazon LP or Googleyness or similar. | [Behavioral](../../interview-toolkit/behavioral/INDEX.md) + your own story bank |

### Tier 2 — Asked in 60-80% of FAANG interviews (mid-senior to senior)

| Topic | What you need to demonstrate | Where to study |
|-------|------------------------------|----------------|
| **Bit manipulation** | XOR tricks, bitmask DP, popcount. Asked at Meta, Google. | [Core Cs Fundamentals](core-cs-fundamentals.md) + [Coding Patterns/15 Bit Manipulation](../../interview-toolkit/coding-patterns/INDEX.md) |
| **Segment Tree / Fenwick / BIT** | Range queries with updates. Asked at Google, occasionally Meta. Skip for Amazon/Microsoft. | [Advanced Topics](advanced-topics.md) |
| **Backtracking** | N-queens, sudoku, word search, permutations. Classic. | [Coding Patterns/05 Backtracking](../../interview-toolkit/coding-patterns/INDEX.md) |
| **Greedy algorithms** | Interval scheduling, jump game, activity selection. | [Coding Patterns/12 Greedy Prefix Sum](../../interview-toolkit/coding-patterns/INDEX.md) |
| **Tries** | Word search, autocomplete. Asked at Google. | [Coding Patterns/08 Trie](../../interview-toolkit/coding-patterns/INDEX.md) |
| **Union-Find** | Connected components, account merge, redundant connection. | [Coding Patterns/09 Union Find](../../interview-toolkit/coding-patterns/INDEX.md) |
| **Monotonic Stack** | Next greater element, largest rectangle. Asked at Amazon. | [Coding Patterns/13 Monotonic Stack](../../interview-toolkit/coding-patterns/INDEX.md) |
| **Topological Sort** | Course schedule, alien dictionary, sequence reconstruction. | [Coding Patterns/10 Topological Sort](../../interview-toolkit/coding-patterns/INDEX.md) |
| **System Design depth** | Distributed systems, CAP theorem, sharding strategies, consistent hashing, idempotency, exactly-once semantics. | [System Design](../../architecture/system-design/INDEX.md) + [Microservices](../../backend/microservices/INDEX.md) |
| **API design** | REST, GraphQL, gRPC, versioning, pagination, auth. | [REST API](../../backend/rest-api/INDEX.md) + [GraphQL](../../backend/graphql/INDEX.md) |
| **Security basics** | XSS, CSRF, SQL injection, JWT, OAuth, RBAC. | [Security](../../backend/security/INDEX.md) |
| **Containerization** | Docker basics, multi-stage builds. | [Docker](../../platform/docker/INDEX.md) |
| **Cloud basics** | AWS / GCP core services: EC2/Compute Engine, S3/Cloud Storage, RDS/Cloud SQL, Lambda/Cloud Functions, SQS/Pub-Sub. | [Devops Behavioral Career](devops-behavioral-career.md) |
| **Git workflow** | Branching strategies, rebase, merge, conflict resolution. | [Git Advanced](../../platform/git-advanced/INDEX.md) |
| **Testing strategy** | Unit, integration, E2E. When to mock vs not. | [Testing](../../quality/testing/INDEX.md) |
| **Performance + observability** | Profiling, debugging, SLI/SLO. | [Performance Monitoring](../../quality/performance-monitoring/INDEX.md) + [Observability](../../platform/observability/INDEX.md) |

### Tier 3 — Differentiator (asked 20-40%, distinguishes senior from staff)

| Topic | What you need to demonstrate | Where to study |
|-------|------------------------------|----------------|
| **Distributed systems** | Raft, Paxos, distributed locks, leader election, consensus. | [Microservices](../../backend/microservices/INDEX.md) |
| **Cost optimization at scale** | AWS cost levers, multi-region trade-offs, data egress, spot instances. | Practical experience |
| **Mentorship & influence** | How you've grown engineers, RFC process, code review as teaching. | [Behavioral](../../interview-toolkit/behavioral/INDEX.md) |
| **Engineering culture** | Postmortem culture, blameless retros, RFC templates. | [Behavioral](../../interview-toolkit/behavioral/INDEX.md) |
| **Compensation negotiation** | Base vs RSU trade-offs, sign-on vs equity, level mapping, real offer scripts. | [Compensation Benchmarking](compensation-benchmarking.md) |
| **Architecture trade-offs** | Microservices vs monolith, when to break up, when to consolidate. | [Design Patterns](../../backend/design-patterns/INDEX.md) + [Microservices](../../backend/microservices/INDEX.md) |
| **Threat modeling** | STRIDE, attack trees, secrets management. | [Security](../../backend/security/INDEX.md) |
| **Engineering productivity** | Build vs buy, internal tooling, dev experience. | Practical experience + [Build Tools](../../platform/build-tools/INDEX.md) |
| **Capacity planning** | QPS estimates, storage, bandwidth, cost at scale. | [System Design](../../architecture/system-design/INDEX.md) |

### Topics to SKIP for mid-tier Indian product companies (Adobe, Flipkart, Razorpay, etc.)

The bar is lower at Indian product companies. Skip the FAANG-hard topics:
- 2D DP (mediums are enough)
- Segment tree, BIT, KMP
- Monotonic stack, queue
- Hard graph algorithms (Tarjan's SCC, articulation points)
- Raft / Paxos
- Distributed consensus

### Topics to SKIP for in-country India SDE roles

The bar is even lower. Skip:
- Hard DP
- Segment tree, BIT
- System design beyond URL shortener + 1-2 case studies
- All Tier 3 distributed-systems topics
- Distributed systems deep-dive

**India in-country prep is ~80% of what FAANG asks, but the bar is "good enough to ship" not "good enough to optimize at scale."**

---

## Interview Process — Round-by-Round

The FAANG / Big Tech loop is **5-6 rounds**, with LeetCode at the front. Compared to EU mid-stage's 3-4 rounds, this is longer, harder, and more focused on raw problem-solving.

### Round 0: Recruiter Screen (15-30 min)

| Who | What they test | What they ask |
|------|----------------|---------------|
| Internal recruiter or university recruiter | Basic fit, motivation, comp, location, visa. | "Tell me about yourself." "Why [company]?" "What level are you targeting?" "Do you need visa sponsorship?" "Comp expectation?" |

**How to prep:** 60-second "tell me about yourself" cold. Know your target level (E4/E5 for senior, E6/E7 for staff). Have comp range in USD/INR ready.

### Round 1: Phone Screen / Online Assessment (45-90 min)

| Format | What they test | What they ask |
|--------|----------------|---------------|
| **HackerRank / CodeSignal** (Google, Amazon) | 1-2 mediums in 60-90 min, often LeetCode 1-3 difficulty. | Standard mediums, 1-2 problems, edge cases, complexity analysis. |
| **CoderPad live coding** (Meta, Stripe) | 1 medium, 45-60 min, live with interviewer. | Same problems, but the interviewer watches and asks follow-ups. |
| **Phone screen with engineer** (Apple, Microsoft) | 1-2 mediums, often easier than onsites. | Same problems, easier bar. |
| **Microsoft Teams "interview"** (Microsoft) | Sometimes a behavior + 1 coding. | Often a writing exercise. |

**The bar for Round 1 is "1-2 mediums in 60 min, edge cases, clean code."** No FAANG-hard at this stage.

**What gets you REJECTED on the phone screen:**
- Cannot solve a 2-sum variant in 15 min
- Cannot debug a small bug in your own code when prompted
- No questions asked back
- Silent for 5+ minutes when stuck

### Round 2-5: Onsite Loop (4-5 hours total, 1-2 days)

| Round | Format | What they test | Duration |
|-------|--------|----------------|----------|
| **2a: Coding 1** | 1 medium-to-hard problem on whiteboard / shared doc | Coding fluency, data structures, edge cases | 45-60 min |
| **2b: Coding 2** | 1 different medium-to-hard problem | Different pattern from Round 2a (e.g., DP in 2a, graph in 2b) | 45-60 min |
| **3: System Design** | 1 system design problem (whiteboard / shared doc) | Can you design a real system at 45 min? | 45-60 min |
| **4: Behavioral / Values** | 1-2 behavioral questions | STAR, leadership, "Why us?" | 30-60 min |
| **5: Hiring Manager** (sometimes) | Vision, ownership, motivation | Why this team? Why this level? | 30-60 min |
| **Bar Raiser** (Amazon only) | Behavioral + values + judgment | Amazon Leadership Principles deep-dive | 45-60 min |

**The bar for Round 2-5 is "1-2 FAANG-medium-to-hard problems in 45 min, plus 1 system design, plus 1-2 behavioral."** This is the FAANG bar.

**What gets you REJECTED on the coding round:**
- Cannot solve a medium in 45 min
- Cannot debug your own code
- Cannot discuss complexity (Big-O)
- No edge cases handled
- Cannot explain your approach before coding

**What gets you REJECTED on system design:**
- Start drawing before clarifying
- No estimates
- Single point of failure everywhere
- No observability
- Cannot discuss trade-offs

**What gets you REJECTED on behavioral:**
- STAR answer is just S and T, no A or R
- Cannot give a specific metric
- Cannot describe what you learned
- "Why this company?" is generic ("great products, smart people")
- "Tell me about a conflict" → "I don't really have conflicts"

### Round 6: Offer / Comp (HR / Recruiter call)

| Who | What they discuss |
|------|-------------------|
| Recruiter | Comp (base, RSU, sign-on, bonus), start date, level, location. |

**How to negotiate:** see [Compensation Benchmarking](compensation-benchmarking.md). Rule of thumb: always counter, especially on equity.

---

## Strategy — How to Prep, What to Skip, When to Apply

### The 8-12 week prep plan (4-6 hrs/day)

| Week | Focus | Hours | Deliverable |
|------|-------|------:|-------------|
| **Week 1-2** | Foundation: data structures, basic algorithms, complexity analysis | ~50-60h | All 19 patterns studied, 5-10 problems per pattern solved |
| **Week 3-4** | Pattern mastery: 100+ problems across all patterns, time-boxed | ~50-60h | 100+ problems solved, 2 mock interviews done |
| **Week 5-6** | System design + OOD | ~50-60h | 5 system designs explained cold + 3 OOD problems |
| **Week 7-8** | Company-specific prep + behavioral | ~30-40h | 8 STAR stories + 2 mock interviews per company |
| **Week 9-12** | Mock interview grind + applications | ~30-40h | 5+ mock interviews, 10-15 applications sent |

### The 80/20 — what to skip if time is short

If you have **less than 8 weeks**, drop in this order:
1. **Skip advanced system design** (URL shortener + 1-2 case studies is enough for mid-tier; FAANG wants 5+)
2. **Skip Segment Tree, BIT, KMP, monostack, union-find** (only needed for Google, Meta Staff+)
3. **Skip the 28-phase 12-week plan** (use the 8-week accelerated version)
4. **Skip the 4-6 hrs/day blocks** (2-3 hrs/day is fine, takes longer but works)

**The non-negotiable 4-week MVP:**
- 50+ LeetCode mediums across 6 patterns (HashMap, Sliding Window, Two Pointers, BFS/DFS, 1D DP, Heap)
- 1 system design case (URL shortener) explained cold
- 5 STAR stories practiced out loud
- 2 mock interviews done

If you can ship those, you can pass 70%+ of mid-tier loops.

### When to start applying

| Trigger | Apply now |
|---------|-----------|
| 50+ problems solved (across 6 patterns) | ✅ after Week 4 |
| 1 system design case explained cold | ✅ after Week 5 |
| 5 STAR stories practiced | ✅ after Week 7 |
| 2 mock interviews done | ✅ after Week 8 |

**Rule of thumb:** Apply 2-3 weeks before you feel "ready." Real interview feedback is more useful than any prep.

### Comp strategy (US-based FAANG, 2024-26 levels)

| Level | Title | Base (USD) | RSU/yr (USD) | Total Comp (USD) |
|-------|-------|------------|--------------|-----------------|
| E3 | SWE | $150K-180K | $50-80K | $200-260K |
| E4 | Senior SWE | $180-220K | $80-150K | $260-370K |
| E5 | Staff SWE | $220-280K | $150-300K | $370-580K |
| E6 | Senior Staff | $280-340K | $300-500K | $580-840K |
| E7 | Principal | $340-400K | $500-1M+ | $840K-1.4M |

**India-based SDE (product company, in-country):**

| Level | Title | Base (INR) | Total Comp (INR) | Total Comp (USD) |
|-------|-------|------------|------------------|-----------------|
| SDE-1 | Junior | 12-25 L | 15-30 L | $18-36K |
| SDE-2 | Mid | 25-45 L | 30-60 L | $36-72K |
| SDE-3 | Senior | 45-80 L | 60-120 L | $72-145K |
| SDE-4 / Staff | Lead | 80-150 L | 120-250 L | $145-300K |
| Principal | Principal | 150-300 L | 250-500 L+ | $300-600K |

**Negotiation:** Always counter on equity. RSUs are negotiable; base is usually not. Sign-on is negotiable. Use competing offers as leverage. See [Compensation Benchmarking](compensation-benchmarking.md).

### Visa strategy

| Scenario | Visa | Process time | Family |
|----------|------|--------------|--------|
| **US-based FAANG** | H1B (lottery) or STEM-OPT (if from US Masters) | H1B: 6-12 months for lottery, then 6-12 weeks for stamping. STEM-OPT: 12-36 months. | H4 dependent visa for spouse. H4 EAD requires I-140 approval. |
| **US-based Big Tech (Microsoft, Amazon)** | Same as FAANG | Same | Same |
| **EU-based (Google Zürich, Meta London, Microsoft Dublin)** | EU Blue Card or local work permit | 4-12 weeks | Spouse work permit included. |
| **UK-based (Google London, Meta London)** | Skilled Worker visa | 4-8 weeks | Spouse Dependant visa (work allowed). |

**H1B strategy:** Apply to FAANG in the lottery window (March-April). Most new grad / E3 hires get picked in the lottery. For senior, you often get hired on a "we'll transfer you later" basis (L-1 visa, intra-company transfer) or via the cap-exempt pool (if you've been on STEM-OPT).

---

## Files in This Lane

### Core Knowledge (Phases 1-28)

| # | File | Phases | Topics |
|---|------|--------|--------|
| 01 | [Complete Guide](complete-guide.md) | 1-8 | Java, DSA, Algorithms, Patterns, DP, Graphs, Trees |
| 02 | [Core CS Fundamentals](core-cs-fundamentals.md) | 9-16 | Bit Manipulation, Math, OOP, OS, Networks, Databases |
| 03 | [System Design & APIs](system-design-apis-security.md) | 17-20 | System Design, REST APIs, Security, Concurrency |
| 04 | [DevOps & Career](devops-behavioral-career.md) | 21-28 | Git, Linux, Behavioral, Resume, Testing, Cloud |
| 05 | [Advanced Topics](advanced-topics.md) | — | Segment Tree, Fenwick, AVL, DI, Repository, MVC |

### Study Tools

| # | File | Purpose |
|---|------|---------|
| 06 | [LeetCode Study Plan](leetcode-study-plan.md) | 12-week intensive plan (4-6 hrs/day) |
| 07 | [Cheat Sheet](cheat-sheet.md) | Quick reference for all 28 phases |
| 08 | [Progress Tracker](progress-tracker.md) | Weekly tracking with readiness scores |
| 09 | [Mock Interview Bank](mock-interview-question-bank.md) | 90 questions (50 Coding + 20 SD + 20 Behavioral) |
| 10 | [Spaced Repetition Schedule](spaced-repetition-schedule.md) | 12-week review calendar with mastery tracking |
| 11 | [Daily Study Timer](daily-study-timer.md) | Pomodoro tracking, productive vs review time |
| 12 | [Quick Reference Cards](quick-reference-cards.md) | One-page cards for Arrays, Trees, Graphs, DP, etc. |
| 13 | [Learning Guarantee System](learning-guarantee-system.md) | Active recall, mastery criteria, practice testing |
| 14 | [Flashcard Decks](flashcard-decks.md) | 240+ cards across 8 topics for Anki/Quizlet |
| 15 | [Resume & Negotiation](resume-negotiation.md) | Resume ATS optimization, STAR bullets, offer negotiation, comp breakdown |
| 21 | [Week study schedule](week-study-schedule.md) | Day-by-day 8-week plan with daily checklist + mastery trackers |
| 22 | [Compensation Benchmarking](compensation-benchmarking.md) | Level mapping, RSU mechanics, sign-on negotiation, real scripts |

### Company-Specific Guides

| # | File | Company | Focus |
|---|------|---------|-------|
| 16 | [Microsoft Azure Guide](microsoft-azure-interview-guide.md) | Microsoft | Growth Mindset, Azure, Plain Text Editor |
| 17 | [Google Guide](google-interview-guide.md) | Google | Googleyness, Google Docs Coding, HC Process |
| 18 | [Amazon Guide](amazon-interview-guide.md) | Amazon | Leadership Principles, Bar Raiser, AWS |
| 19 | [Meta Guide](meta-interview-guide.md) | Meta | Move Fast, CodeSignal OA, Product Architecture |
| 20 | [Apple Guide](apple-interview-guide.md) | Apple | Privacy-First, On-Demand Processing, Domain Expertise |

---

## Cross-references to Core Sections (1-7 + 0)

These are the **where to study** sections. The reference topics above are the **what to be ready for** checklist.

**Core fundamentals:** [Interview Strategy](../../strategy/INDEX.md) · [JavaScript](../../frontend/javascript/INDEX.md) · [TypeScript](../../frontend/typescript/INDEX.md) · [React](../../frontend/react/INDEX.md) · [Next.js](../../frontend/nextjs/INDEX.md)

**Backend, API & Data:** [Node.js](../../backend/nodejs/INDEX.md) · [NestJS](../../backend/nestjs/INDEX.md) · [REST API](../../backend/rest-api/INDEX.md) · [Database](../../backend/database/INDEX.md) · [GraphQL](../../backend/graphql/INDEX.md)

**Architecture & Design:** [Security](../../backend/security/INDEX.md) · [Design Patterns](../../backend/design-patterns/INDEX.md) · [System Design](../../architecture/system-design/INDEX.md) · [Microservices](../../backend/microservices/INDEX.md)

**DevOps, Observability & Tooling:** [Docker](../../platform/docker/INDEX.md) · [Kubernetes](../../platform/kubernetes/INDEX.md) · [CI/CD](../../platform/ci-cd) · [Observability](../../platform/observability/INDEX.md) · [Build Tools](../../platform/build-tools/INDEX.md) · [Git Advanced](../../platform/git-advanced/INDEX.md) · [Serverless & Edge](../../platform/serverless-edge/INDEX.md)

**Testing & Quality:** [Testing](../../quality/testing/INDEX.md) · [Accessibility](../../quality/accessibility/INDEX.md) · [Performance Monitoring](../../quality/performance-monitoring/INDEX.md)

**Real-time:** [WebSockets](../../realtime/websockets/INDEX.md)

**Interview prep:** [Behavioral](../../interview-toolkit/behavioral/INDEX.md) · [Coding Patterns](../../interview-toolkit/coding-patterns/INDEX.md)

**Reference & quick-look:** [Cheat Sheets](../../interview-toolkit/cheatsheets/INDEX.md) · [Monorepo](../../platform/monorepo/INDEX.md) · [Form Handling](../../frontend/form-handling/INDEX.md) · [Animation](../../frontend/animation/INDEX.md)

---

## FAQ

**Q: I have 4 weeks. Can I pass a Google interview?**
A: Honestly, no. Google E4/E5 expects 200+ LeetCode problems internalized, 5+ system design cases, and 5+ behavioral stories cold. 4 weeks is for mid-tier, not Google.

**Q: How many LeetCode problems do I need?**
A: For mid-tier (Adobe, Microsoft, in-country product): 100-150. For FAANG: 250-400. For FAANG Staff: 400+ with system design depth.

**Q: Java or Python or C++ for FAANG?**
A: Most common: Python (Google, Meta), Java (Amazon, Microsoft), C++ (Google, some Meta). Pick the one you can code fastest in. Python is usually fastest for interviews. **Stick to one — don't switch languages between rounds.**

**Q: How long does the FAANG process take?**
A: End-to-end: 4-12 weeks. Recruiter screen → phone screen → onsite → team match → offer. The bottleneck is usually scheduling the onsite, not the actual rounds.

**Q: Should I tell the recruiter my other offers?**
A: Yes, but only if they're real. Use them for comp negotiation, not for FAANG bar-raiser rounds (Amazon bar-raisers can ding you for "shopping around").

**Q: How do I get into FAANG as a non-US-resident?**
A: Apply from India. Most FAANG have India offices (Google Bangalore, Amazon Bangalore, Microsoft Hyderabad, Meta doesn't have India yet). You can also apply to US roles and request H1B sponsorship — most FAANG will sponsor.

**Q: My CTC is INR X, is that competitive?**
A: For the same role, US-based FAANG TC is 5-10x India-based TC. In-country India is competitive with global product companies (Flipkart, Razorpay, Atlassian India, etc.) but well below US. The "right" comp depends on your family situation, visa, and lifestyle goals.

---

## When to add to this lane

This lane is a living scaffold. As you go through interviews, add:

- **New company-specific guides** — for each FAANG you've interviewed at, add a 1-pager on the actual loop format
- **New system design case studies** — once you solve a case interview well, add the case + your answer framework
- **Updated LeetCode lists** — LeetCode problem IDs change; refresh the problem set every 6 months
- **Comp data points** — once you have an offer or strong signal, log it (anonymized) to keep the comp data fresh

---

## Navigation

[← Previous: Animation](../../frontend/animation/INDEX.md) · [🏠 Back to Index](../../INDEX.md) · [Sibling Lane: Abroad Full-Stack (82) →](../abroad-full-stack/INDEX.md)
