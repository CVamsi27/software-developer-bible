---
section: SDE Role
category: Interview
tags: [study-plan]
---

# 8-Week SDE Interview Study Schedule

> A focused 8-week study plan for senior full-stack engineers targeting SDE II / SDE III roles. Combines data structures, system design, behavioral preparation, and a daily checklist. Adjust the daily hours to match your schedule — 2 hours/day minimum, 6 hours/day for the intensive track.

## Definition

A weekly study plan that sequences CS fundamentals, coding practice, system design, and behavioral preparation over 8 weeks. Each week has a clear theme, daily checkpoints, and a Friday mock-interview session. Built to be aggressive but realistic for working engineers.

## Why It Matters (TL;DR)

- **8 weeks is the sweet spot** — long enough for depth, short enough to maintain urgency
- **Daily structure** — eliminates decision fatigue
- **Friday mocks** — every week ends with realistic practice
- **Adjustable intensity** — scale hours based on availability
- **Cross-references the other 31 files** — one source of navigation

## How to Use This Plan

```text
DAILY RULES:
  • Study at the same time every day (builds the habit)
  • Phones in another room
  • Use a timer (Pomodoro: 50 min focus, 10 min break)
  • Track every session in 11-Daily-Study-Timer.md
  • End each day with one paragraph: what I learned, what's unclear

WEEKLY REVIEW (Sunday, 1 hour):
  • Update 08-Progress-Tracker.md
  • Identify weakest area → next week's deep dive
  • Schedule 1-2 mock interviews for next week
```

## 8-Week Plan (4-6 hrs/day)

### Week 1 — Foundations & Big-O Refresher

**Theme:** Arrays, strings, hash maps, time/space complexity, language fluency.

| Day | Focus | Hours | Resources |
|-----|-------|------:|-----------|
| 1 | Arrays (prefix sum, kadane's) | 5 | 01-Complete-Guide (Phases 1-3) |
| 2 | Strings (palindromes, anagrams, sliding window) | 5 | 19-Coding-Patterns/Sliding-Window |
| 3 | Hash maps (two-sum, frequency counters) | 5 | 19-Coding-Patterns/Hash-Map |
| 4 | Two pointers | 5 | 19-Coding-Patterns/Two-Pointers |
| 5 | Binary search intro | 5 | 19-Coding-Patterns/Binary-Search |
| 6 | Mock: 2 medium + 1 behavioral | 3 | 09-Mock-Interview-Bank |
| 7 | Review week's problems + rest | 2 | 08-Progress-Tracker |

**Goal:** Solve 25-30 problems. P95 < 25 min per medium.

### Week 2 — Trees & Graphs Intro

**Theme:** Tree traversal, BST, BFS, DFS, graph basics.

| Day | Focus | Hours | Resources |
|-----|-------|------:|-----------|
| 1 | Tree BFS / DFS | 5 | 19-Coding-Patterns/Tree-BFS, Tree-DFS |
| 2 | BST operations | 5 | 19-Coding-Patterns/Tree-DFS |
| 3 | Graph BFS / DFS | 5 | 19-Coding-Patterns/Graphs |
| 4 | Topological sort | 4 | 19-Coding-Patterns/Topological-Sort |
| 5 | Union-Find | 4 | 19-Coding-Patterns/Union-Find |
| 6 | Mock: 1 hard tree + 2 mediums | 3 | 09-Mock-Interview-Bank |
| 7 | Review + study 1 system design (URL shortener) | 3 | 11-System-Design/01-URL-Shortener |

**Goal:** 20 problems. Solve 1 tree problem in < 20 min.

### Week 3 — Dynamic Programming Intro

**Theme:** 1D DP, 2D DP, knapsack, LCS.

| Day | Focus | Hours | Resources |
|-----|-------|------:|-----------|
| 1 | DP fundamentals (memoization vs tabulation) | 4 | 19-Coding-Patterns/DP |
| 2 | 1D DP (climbing stairs, house robber) | 5 | 19-Coding-Patterns/DP |
| 3 | 2D DP (grid paths, longest common subsequence) | 5 | 19-Coding-Patterns/DP |
| 4 | Knapsack pattern | 5 | 19-Coding-Patterns/DP |
| 5 | DP on strings (edit distance) | 4 | 19-Coding-Patterns/DP |
| 6 | Mock: 1 hard DP + 2 mediums | 3 | 09-Mock-Interview-Bank |
| 7 | Review + 1 system design (rate limiter) | 3 | 11-System-Design/02-Rate-Limiter |

**Goal:** 15 problems. Identify and explain 3 DP patterns cold.

### Week 4 — Advanced Data Structures + CS Fundamentals

**Theme:** Heaps, tries, intervals, bit manipulation, OS/networking/Databases refresh.

| Day | Focus | Hours | Resources |
|-----|-------|------:|-----------|
| 1 | Heap (top K, merge K lists) | 4 | 19-Coding-Patterns/Heap |
| 2 | Trie (autocomplete) | 4 | 19-Coding-Patterns/Trie |
| 3 | Intervals (merge, meeting rooms) | 4 | 19-Coding-Patterns/Intervals |
| 4 | Bit manipulation | 3 | 02-Core-CS-Fundamentals (Bit Manip) |
| 5 | OS, networking, DB refresh | 4 | 02-Core-CS-Fundamentals (Phases 12-14) |
| 6 | Mock: 2 mediums + 1 OS/networking Q | 3 | 09-Mock-Interview-Bank |
| 7 | Review + 1 system design (chat system) | 3 | 11-System-Design/06-Chat-System |

**Goal:** 20 problems + can explain TCP/IP, ACID, MVCC, deadlocks cold.

### Week 5 — System Design Deep Dive

**Theme:** URL shortener → Twitter → rate limiter → chat system. Capacity, sharding, caching.

| Day | Focus | Hours | Resources |
|-----|-------|------:|-----------|
| 1 | URL shortener deep dive (write it out) | 5 | 11-System-Design/01-URL-Shortener |
| 2 | Twitter timeline (fan-out, caching) | 5 | 11-System-Design/04-Twitter |
| 3 | Rate limiter (token bucket, Redis) | 4 | 11-System-Design/02-Rate-Limiter |
| 4 | Notification system (pub/sub, retries) | 4 | 11-System-Design/07-Notification-Service |
| 5 | WebSockets + chat (presence, scaling) | 4 | 21-WebSockets + 11-System-Design/06 |
| 6 | Mock: 1 system design (45 min) | 2 | 09-Mock-Interview-Bank |
| 7 | Review + weak system design redo | 2 | 11-System-Design |

**Goal:** Can design URL shortener, Twitter, rate limiter in 45 min each.

### Week 6 — Behavioral + Soft Skills

**Theme:** STAR stories, company research, why-questions.

| Day | Focus | Hours | Resources |
|-----|-------|------:|-----------|
| 1 | Write 5 STAR stories (leadership, conflict, fail) | 4 | 18-Behavioral/01-STAR-Method |
| 2 | Write 5 STAR stories (impact, technical, mentoring) | 4 | 18-Behavioral/02-Leadership-Questions |
| 3 | HR questions (why company, why leaving, weakness) | 3 | 18-Behavioral/03-HR-Questions |
| 4 | Company research: values, products, recent news | 3 | 16-20 company guides |
| 5 | Mock behavioral (30 min, peer or Pramp) | 2 | 09-Mock-Interview-Bank |
| 6 | Mock: 1 system design + 2 STAR stories | 2 | 09-Mock-Interview-Bank |
| 7 | Rest + light review | 1 | 08-Progress-Tracker |

**Goal:** 10 polished STAR stories, 2-min pitch, can answer any "tell me about a time" in 2 min.

### Week 7 — Company-Specific Prep + Mock Sprints

**Theme:** Target 1-2 companies. Mock interviews daily.

| Day | Focus | Hours | Resources |
|-----|-------|------:|-----------|
| 1 | Target company guide (read fully) | 3 | 16-20 company guides |
| 2 | Process, format, values, recent news | 3 | Company blog, LinkedIn, Glassdoor |
| 3 | Mock coding (1 hard) | 3 | 09-Mock-Interview-Bank |
| 4 | Mock system design (45 min) | 2 | Pramp / Interviewing.io |
| 5 | Mock behavioral (30 min) | 2 | Pramp / Interviewing.io |
| 6 | Mock loop: coding + SD + behavioral (3 hours) | 3 | 09-Mock-Interview-Bank |
| 7 | Review weak areas + rest | 2 | 08-Progress-Tracker |

**Goal:** Score 7/10+ on every mock. Identify the 2-3 patterns you still miss.

### Week 8 — Final Polish + Logistics

**Theme:** Light review, logistics, rest, confidence.

| Day | Focus | Hours |
|-----|-------|------:|
| 1 | Review 07-Cheat-Sheet — full pass | 2 |
| 2 | Top 10 weak problems — re-solve | 3 |
| 3 | Top 3 system designs — re-do | 3 |
| 4 | One full mock loop (coding + SD + behavioral) | 3 |
| 5 | Logistics: dress, route, laptop, snacks, sleep | 1 |
| 6 | Rest + light walk | 0 |
| 7 | **INTERVIEW** | — |

## Daily Checklist (Template)

```text
Date: ____________

□ 3-5 LeetCode problems (track pattern, time, mistakes)
□ 30 min CS fundamentals refresh (review 1 phase)
□ 30 min system design (read 1 case study or design 1 system)
□ 20 min behavioral (write or refine 1 STAR story)
□ 1 paragraph journal: what I learned, what's unclear

Total focus: ____ hours
Pattern of the day: __________
Mistakes made: __________
Plan to fix: __________
```

## Patterns Checklist (Mastery Tracker)

| Pattern | Confident | Notes |
|---------|:---------:|-------|
| Sliding Window | ☐ | |
| Two Pointers | ☐ | |
| Binary Search | ☐ | |
| Hash Map | ☐ | |
| Tree BFS / DFS | ☐ | |
| Graph BFS / DFS | ☐ | |
| Topological Sort | ☐ | |
| Union-Find | ☐ | |
| Heap / Priority Queue | ☐ | |
| Trie | ☐ | |
| Dynamic Programming | ☐ | |
| Backtracking | ☐ | |
| Greedy | ☐ | |
| Intervals | ☐ | |
| Bit Manipulation | ☐ | |
| Monotonic Stack | ☐ | |

## CS Fundamentals Checklist

| Topic | Confident | Notes |
|-------|:---------:|-------|
| Big-O time / space | ☐ | |
| Arrays / hash maps | ☐ | |
| Linked lists | ☐ | |
| Stacks / queues | ☐ | |
| Trees / BST | ☐ | |
| Heaps | ☐ | |
| Graphs (BFS / DFS / Dijkstra) | ☐ | |
| Sorting algorithms | ☐ | |
| Recursion / backtracking | ☐ | |
| Dynamic programming | ☐ | |
| Bit manipulation | ☐ | |
| OOP / design patterns | ☐ | |
| Operating systems (processes, threads, sync) | ☐ | |
| Networking (TCP/IP, HTTP, DNS) | ☐ | |
| Databases (SQL, ACID, indexes, MVCC) | ☐ | |
| Distributed systems (CAP, consensus) | ☐ | |

## System Design Checklist

| System | Designed in 45 min? | Notes |
|--------|:-------------------:|-------|
| URL shortener | ☐ | |
| Twitter / Instagram feed | ☐ | |
| Rate limiter | ☐ | |
| Chat system (WhatsApp) | ☐ | |
| Notification system | ☐ | |
| Uber / Lyft | ☐ | |
| YouTube / Netflix | ☐ | |
| Dropbox / Google Drive | ☐ | |
| Payment gateway | ☐ | |
| Ticket booking | ☐ | |

## Behavioral Stories Checklist (10 Required)

| # | Theme | Story | Polished? |
|---|-------|-------|:---------:|
| 1 | Technical leadership | | ☐ |
| 2 | Conflict resolution | | ☐ |
| 3 | Failure / learning | | ☐ |
| 4 | Big impact / metric | | ☐ |
| 5 | Cross-team collaboration | | ☐ |
| 6 | Mentoring / growth | | ☐ |
| 7 | Disagreement with manager | | ☐ |
| 8 | Speed vs quality tradeoff | | ☐ |
| 9 | Stakeholder management | | ☐ |
| 10 | Innovation / invention | | ☐ |

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| "I'll do 10 problems today, then 0 for 3 days" | 2-3 problems/day, every day, for 8 weeks |
| Skipping the fundamentals phase | Week 4 CS fundamentals often reveals gaps that doom Week 5 system design |
| Memorizing solutions | Explain the pattern out loud, derive the solution from first principles |
| Only LeetCode, no system design | Coding is 50% — system design is 25%, behavioral is 25% |
| No mock interviews | Mocks reveal problems you can't see on your own; aim for 8-10 mocks |
| Burnout | Take Sunday afternoons off; sleep 7+ hours; daily 30-min walk |

## See Also

- 01-Complete-Guide — DSA phases
- 02-Core-CS-Fundamentals — OS / networks / DBs
- 03-System-Design-APIs-Security — system design primer
- 04-DevOps-Behavioral-Career — behavioral primer
- 06-LeetCode-Study-Plan — 12-week alternative
- 07-Cheat-Sheet — last-minute review
- 08-Progress-Tracker — weekly tracking
- 09-Mock-Interview-Bank — 90 mock questions
- 10-Spaced-Repetition-Schedule — review calendar
- 11-Daily-Study-Timer — Pomodoro tracking
- 13-Learning-Guarantee-System — mastery criteria
- 14-Flashcard-Decks — Anki/Quizlet decks
- 15-Resume-Negotiation — resume + offer negotiation


## Summary

- 8 weeks is the sweet spot for senior full-stack interview prep
- Daily checklist: 3-5 problems + 30 min fundamentals + 30 min system design + 20 min behavioral
- Friday: mock interview (coding or system design)
- Sunday: 1-hour review, update tracker
- The plan scales: 2 hrs/day minimum, 6 hrs/day intensive
- Mastery = explain the pattern, derive the solution, write code in 25 min

---

## Cheat Sheet

```text
8-WEEK PLAN AT A GLANCE
═══════════════════════════════════════════════════════════════

WEEK 1: Arrays, strings, hash, two pointers, binary search
WEEK 2: Trees (BFS/DFS), graphs, topological sort
WEEK 3: Dynamic programming (1D, 2D, knapsack)
WEEK 4: Heaps, tries, intervals + CS fundamentals refresh
WEEK 5: System design deep dive (5 systems end-to-end)
WEEK 6: Behavioral (10 STAR stories, company research)
WEEK 7: Company-specific prep + daily mocks
WEEK 8: Final polish, logistics, rest

DAILY:
  3-5 problems → 30 min fundamentals → 30 min system design → 20 min behavioral
```

---

## References & Learn More

- [Blind 75 / Grind 75](https://www.techinterviewhandbook.org/grind75) — essential problem sets
- [Grokking the Coding Interview](https://www.educative.io/courses/grokking-the-coding-interview) — pattern-based prep
- [Interviewing.io](https://interviewing.io/) — anonymous mocks with engineers
- [LeetCode](https://leetcode.com/) — primary practice platform
- [NeetCode Roadmap](https://neetcode.io/roadmap) — curated problem list by pattern
- [Pramp](https://www.pramp.com/) — free peer mock interviews
- [Spaced Repetition for Anki](https://docs.ankiweb.net/deck-options.html) — review schedule settings
- [System Design Primer](https://github.com/donnemartin/system-design-primer) — GitHub repo with case studies
- [Tech Interview Handbook](https://www.techinterviewhandbook.org/) — comprehensive prep guide
