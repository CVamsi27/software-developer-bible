---
section: SDE Role
category: Interview
tags: [guide]
---

# 🟠 Amazon (AWS) — Interview Guide (2025–2026)

> **Target Role:** SDE I (L4) / SDE II (L5) / Senior SDE (L6)
>
> **Teams to Consider:** AWS, Alexa, Prime, Retail, Kindle, Twitch, Ring

---

## 📋 Interview Process Overview

| Stage | Format | Duration | Focus |
|-------|--------|----------|-------|
| **Recruiter Screen** | Phone/Video | 30 min | Background, salary, team fit |
| **Technical Phone Screen** | CoderPad/HackerRank | 60 min | 1-2 problems, sometimes system design concept |
| **Onsite/Virtual Loop** | 5-6 rounds × 60 min | Full day | Coding, System Design, Behavioral |
| **Bar Raiser Round** | Special interviewer | 60 min | Cross-team evaluator, veto power |
| **Offer Decision** | Internal review | 1-2 weeks | LP evaluation, leveling |

### ⚠️ Key Differences from Other Companies
- **Bar Raiser** — One interviewer from different team has veto power
- **Leadership Principles are EVERYWHERE** — Every question maps to an LP
- **Metrics-driven** — Quantify everything (%, $, time saved)
- **Ownership expected** — Take responsibility beyond your job description
- **AWS knowledge valued** — Not required, but highly advantageous

---

## 🎯 Amazon Leadership Principles (THE MOST IMPORTANT)

### The 16 Leadership Principles

| # | Principle | What It Means | Interview Focus |
|---|-----------|---------------|-----------------|
| 1 | **Customer Obsession** | Start with customer, work backwards | Stories about user impact |
| 2 | **Ownership** | Think long-term, act on behalf of entire company | Taking responsibility beyond scope |
| 3 | **Invent and Simplify** | Innovate and find ways to simplify | Creative solutions, simplicity |
| 4 | **Are Right, A Lot** | Strong judgment, seek diverse perspectives | Decision-making stories |
| 5 | **Learn and Be Curious** | Never stop learning, explore possibilities | Learning new technologies |
| 6 | **Hire and Develop the Best** | Raise the performance bar, mentor | Mentoring, hiring decisions |
| 7 | **Insist on the Highest Standards** | Never settle for "good enough" | Quality, code review, testing |
| 8 | **Think Big** | Create bold direction, think differently | Visionary projects |
| 9 | **Bias for Action** | Speed matters, calculated risk-taking | Quick decisions, shipping fast |
| 10 | **Frugality** | Accomplish more with less | Resource optimization |
| 11 | **Earn Trust** | Listen, speak candidly, treat others respectfully | Conflict resolution, honesty |
| 12 | **Dive Deep** | Stay connected to details, audit frequently | Technical deep dives |
| 13 | **Have Backbone; Disagree and Commit** | Respectfully challenge decisions, commit fully | Disagreeing with manager |
| 14 | **Deliver Results** | Focus on key inputs, deliver with quality | Shipping, metrics, impact |
| 15 | **Strive to be Earth's Best Employer** | Create a better place to work | Team culture, mentoring |
| 16 | **Success and Scale Bring Broad Responsibility** | Think bigger, give back | Community, impact |

### Most Common LPs Tested

| LP | Frequency | Example Question |
|----|-----------|------------------|
| **Ownership** | ⭐⭐⭐⭐⭐ | Tell me about a time you took on something outside your area of responsibility |
| **Bias for Action** | ⭐⭐⭐⭐⭐ | Tell me about a time you had to make a decision quickly |
| **Dive Deep** | ⭐⭐⭐⭐ | Tell me about a time you went deep into the data to solve a problem |
| **Earn Trust** | ⭐⭐⭐⭐ | Tell me about a time you had to push back on someone |
| **Insist on Highest Standards** | ⭐⭐⭐⭐ | Tell me about a time you refused to compromise on quality |
| **Customer Obsession** | ⭐⭐⭐ | Tell me about a time you went above and beyond for a customer |

### STAR Method for Amazon

```text

Situation: Set the context (when, where, what was the challenge)
Task:      What was YOUR responsibility? (not the team's)
Action:    What did YOU do? Be specific, use "I" not "we"
Result:    What was the outcome? QUANTIFY everything

Amazon-specific tips:
- Use "I" not "we" — they want YOUR contribution
- Quantify results: "reduced latency by 60%", "saved $2M"
- Be honest about failures — focus on what you learned
- Map every story to 2-3 LPs explicitly

```

---

## 💻 Coding Interview — Recent Question Trends

### Frequency Distribution by Topic

| Topic | Frequency | Amazon Focus |
|-------|-----------|--------------|
| Arrays & Strings | ~30% | Two Pointers, Sliding Window |
| Trees & Graphs | ~25% | BFS/DFS, Serialization |
| HashMap & Sets | ~15% | Frequency, Grouping |
| Dynamic Programming | ~12% | 1D DP, Knapsack |
| Linked Lists | ~8% | Reverse, Cycle Detection |
| Concurrency | ~5% | Thread-safe, Producer-Consumer |

### 🔥 Most Asked Amazon Questions (2024–2025)

#### Tier 1: Must-Know (Very Frequent)
| # | Problem | Difficulty | Pattern | Link |
|---|---------|------------|---------|------|
| 1 | Two Sum | Easy | HashMap | [LC #1](https://leetcode.com/problems/two-sum/) |
| 2 | Valid Parentheses | Easy | Stack | [LC #20](https://leetcode.com/problems/valid-parentheses/) |
| 3 | Merge Two Sorted Lists | Easy | Linked List | [LC #21](https://leetcode.com/problems/merge-two-sorted-lists/) |
| 4 | Best Time to Buy and Sell Stock | Easy | Array | [LC #121](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) |
| 5 | LRU Cache | Medium | Design | [LC #146](https://leetcode.com/problems/lru-cache/) |
| 6 | Number of Islands | Medium | DFS/BFS | [LC #200](https://leetcode.com/problems/number-of-islands/) |
| 7 | Course Schedule | Medium | Topological Sort | [LC #207](https://leetcode.com/problems/course-schedule/) |
| 8 | Product of Array Except Self | Medium | Prefix Sum | [LC #238](https://leetcode.com/problems/product-of-array-except-self/) |
| 9 | Group Anagrams | Medium | HashMap | [LC #49](https://leetcode.com/problems/group-anagrams/) |
| 10 | Trapping Rain Water | Hard | Two Pointers | [LC #42](https://leetcode.com/problems/trapping-rain-water/) |

#### Tier 2: High Probability
| # | Problem | Difficulty | Pattern | Link |
|---|---------|------------|---------|------|
| 11 | Serialize and Deserialize Binary Tree | Hard | Design | [LC #297](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) |
| 12 | Find Median from Data Stream | Hard | Two Heaps | [LC #295](https://leetcode.com/problems/find-median-from-data-stream/) |
| 13 | Minimum Window Substring | Hard | Sliding Window | [LC #76](https://leetcode.com/problems/minimum-window-substring/) |
| 14 | Binary Tree Level Order Traversal | Medium | BFS | [LC #102](https://leetcode.com/problems/binary-tree-level-order-traversal/) |
| 15 | Word Break | Medium | DP | [LC #139](https://leetcode.com/problems/word-break/) |
| 16 | Clone Graph | Medium | DFS | [LC #133](https://leetcode.com/problems/clone-graph/) |
| 17 | Task Scheduler | Medium | Greedy + Heap | [LC #621](https://leetcode.com/problems/task-scheduler/) |
| 18 | Longest Substring Without Repeating Characters | Medium | Sliding Window | [LC #3](https://leetcode.com/problems/longest-substring-without-repeating-characters/) |
| 19 | Kth Largest Element in an Array | Medium | Quickselect | [LC #215](https://leetcode.com/problems/kth-largest-element-in-an-array/) |
| 20 | Rotting Oranges | Medium | Multi-source BFS | [LC #994](https://leetcode.com/problems/rotting-oranges/) |

### 📝 Coding Round Tips for Amazon

```text

✅ DO:
  • Talk through your approach BEFORE coding
  • Start with brute force, then optimize
  • Handle edge cases explicitly (null, empty, single element)
  • Write clean, testable code
  • Ask clarifying questions about constraints
  • Mention time/space complexity before and after optimizing
  • Think about thread safety when relevant

❌ DON'T:
  • Jump straight to coding without discussing approach
  • Stay silent while thinking
  • Ignore edge cases
  • Forget to mention test cases
  • Give up when stuck — ask for hints

```

---

## 🏗️ System Design — Amazon Focus Areas

### Level Expectations

| Level | Expected Scope | Example Questions |
|-------|---------------|-------------------|
| **SDE I** | Single service/feature | Design a URL Shortener, Design a Rate Limiter |
| **SDE II** | Multiple services, clear requirements | Design a Chat System, Design a Notification Service |
| **Senior SDE** | Full architecture, complex trade-offs | Design Amazon Prime, Design a Marketplace |

### Classic Amazon System Design Questions

| Question | Key Components | AWS Services |
|----------|---------------|--------------|
| Design Amazon.com | Product catalog, Cart, Checkout, Payments | DynamoDB, S3, SQS, Lambda |
| Design Prime Video | Streaming, CDN, Recommendations | CloudFront, S3, DynamoDB |
| Design Alexa | Voice processing, NLP, Skills | Lambda, Polly, Lex |
| Design a Package Tracking System | Real-time updates, Notifications | SQS, SNS, DynamoDB |
| Design a Review System | Ratings, Moderation, Search | Elasticsearch, DynamoDB |
| Design a Recommendation Engine | Collaborative filtering, ML | SageMaker, DynamoDB |

### System Design Framework for Amazon

```text

Step 1: Requirements (5 min)
  - Functional: What does the system do?
  - Non-functional: Scale, latency, availability
  - Amazon context: Customer-obsessed, metrics-driven

Step 2: Estimation (5 min)
  - QPS (queries per second)
  - Storage requirements
  - Cost considerations (AWS pricing)

Step 3: High-Level Design (15 min)
  - Draw components using AWS services
  - Show data flow
  - Mark bottlenecks

Step 4: Deep Dive (20 min)
  - Pick 2-3 components to elaborate
  - Discuss AWS-specific implementations
  - Address scaling strategies
  - Handle failure scenarios

Step 5: Wrap-up (5 min)
  - Summarize key decisions
  - Discuss trade-offs
  - Mention monitoring (CloudWatch)
  - Cost optimization strategies

```

---

## 🧠 Amazon-Specific Technical Questions

### AWS Services You MUST Know

| Category | Services | Use Case |
|----------|----------|----------|
| **Compute** | EC2, Lambda, ECS, EKS | Virtual machines, serverless, containers |
| **Storage** | S3, EBS, EFS | Object storage, block storage, file storage |
| **Database** | DynamoDB, RDS, Aurora, ElastiCache | NoSQL, SQL, caching |
| **Messaging** | SQS, SNS, Kinesis, EventBridge | Queues, pub/sub, streaming |
| **Networking** | VPC, CloudFront, Route 53 | Isolation, CDN, DNS |
| **Security** | IAM, KMS, WAF | Access control, encryption, firewall |

### Distributed Systems

```text

Q: Design a distributed lock service.
A:
  - Option 1: DynamoDB with condition expressions
  - Option 2: ElastiCache (Redis) with SETNX
  - Option 3: SQS with visibility timeout
  - Consider: Lock renewal, failure handling, clock skew
  - Amazon equivalent: DynamoDB TTL + condition expressions

Q: How would you handle eventual consistency in a distributed system?
A:
  - Use version numbers or timestamps for conflict detection
  - Implement retry logic with exponential backoff
  - Consider read-repair or anti-entropy protocols
  - AWS: DynamoDB offers eventually consistent reads by default

```

---

## 📊 Behavioral Questions — Amazon Specific

### Must-Have Stories (Prepare 7-8)

```text

1. A time you took ownership beyond your job description (Ownership)
2. A time you made a decision quickly with incomplete information (Bias for Action)
3. A time you went deep into data to solve a problem (Dive Deep)
4. A time you pushed back on someone respectfully (Earn Trust)
5. A time you refused to compromise on quality (Insist on Highest Standards)
6. A time you went above and beyond for a customer (Customer Obsession)
7. A time you failed and what you learned (Learn and Be Curious)
8. A time you mentored someone (Hire and Develop the Best)

```

### Common Amazon Behavioral Questions

| Question | LP Being Assessed |
|----------|------------------|
| Tell me about a time you took on something outside your responsibility | Ownership |
| Describe a time you had to make a decision quickly | Bias for Action |
| Tell me about a time you went deep into the data | Dive Deep |
| How do you handle disagreements with teammates? | Earn Trust |
| Tell me about a time you refused to compromise on quality | Insist on Highest Standards |
| Describe a time you went above and beyond for a customer | Customer Obsession |
| How do you prioritize when everything is urgent? | Deliver Results |
| Tell me about a time you had to learn something new quickly | Learn and Be Curious |

### "Why Amazon?" — Answer Framework

```text

1. Customer Obsession: "Amazon's principle of starting with the customer
   and working backwards resonates deeply with how I approach engineering."

2. Scale: "Amazon handles millions of requests per second. I want to work
   on systems that operate at this scale."

3. Ownership Culture: "Amazon empowers engineers to own their services
   end-to-end. I thrive in this kind of environment."

4. Specific Team: "I'm particularly interested in [specific team] because
   [specific reason about their technical challenges/products]."

```

---

## 📅 2-Week Amazon-Specific Prep Plan

### Week 1: Technical + LP Deep Dive
| Day | Focus | Activities |
|-----|-------|------------|
| **Mon** | Coding | Solve 10 Amazon-tagged LeetCode problems |
| **Tue** | AWS Services | Review all AWS services listed above |
| **Wed** | System Design | Practice 2 designs (Amazon.com, Prime Video) |
| **Thu** | Leadership Principles | Write 8 STAR stories mapped to LPs |
| **Fri** | Coding | Solve 10 more problems, focus on clean code |
| **Sat** | Behavioral | Practice telling STAR stories aloud |
| **Sun** | Review | Review all notes, identify weak areas |

### Week 2: Interview Simulation
| Day | Focus | Activities |
|-----|-------|------------|
| **Mon** | Mock Coding #1 | 2 problems in 60 min (CoderPad) |
| **Tue** | Mock System Design | Design Amazon-scale system in 45 min |
| **Wed** | Mock Behavioral | Practice all 8 STAR stories |
| **Thu** | Weak Areas | Re-solve problems you struggled with |
| **Fri** | Final Review | Read cheat sheet, review LPs |
| **Sat** | Rest | Light review only, good sleep |
| **Sun** | Interview Day | Review notes morning of, stay calm |

---

## 🎯 Final Checklist Before Amazon Interview

```text

Technical:
  [ ] Can solve Medium problems in 20-25 minutes
  [ ] Can solve Hard problems in 35-45 minutes
  [ ] Can design Amazon-scale systems with AWS services
  [ ] Understand distributed systems fundamentals
  [ ] Know key AWS services and their use cases

Behavioral:
  [ ] Have 8 STAR stories prepared (mapped to LPs)
  [ ] Can explain "Why Amazon?" authentically
  [ ] Can demonstrate every LP through stories
  [ ] Practiced telling stories aloud (2 min each)
  [ ] Have metrics ready for every story

Logistics:
  [ ] Test CoderPad setup for coding
  [ ] Know interviewer names and their teams
  [ ] Have questions prepared for interviewers
  [ ] Research the specific team you're interviewing for

```

---

> **Pro Tip:** Amazon interviewers WILL ask follow-up questions about your stories. Be prepared to go deeper on the "Action" part. They want specifics, not generalities. Use "I" not "we" — they want YOUR contribution.

> **Remember:** The Bar Raiser is looking for candidates who raise the bar. They're not just checking if you're good enough — they're checking if you're better than 50% of current employees in the role. Show exceptional impact!

---

*Last updated: July 2026*

---

## 🔗 Related Files

| File | Description |
|------|-------------|
| [Complete Guide](01-Complete-Guide.md) | Phases 1-8: Java, DSA, Algorithms |
| [Core CS Fundamentals](02-Core-CS-Fundamentals.md) | Phases 9-16: CS Fundamentals, NoSQL |
| [System Design & APIs](03-System-Design-APIs-Security.md) | Phases 17-20: System Design, REST, Security |
| [DevOps & Career](04-DevOps-Behavioral-Career.md) | Phases 21-28: Git, Linux, Behavioral, Cloud |
| [Advanced Topics](05-Advanced-Topics.md) | Segment Tree, DI, Repository, MVC |
| [LeetCode Study Plan](06-LeetCode-Study-Plan.md) | 12-week intensive study plan |
| [Cheat Sheet](07-Cheat-Sheet.md) | Last-minute review for all 28 phases |
| [Microsoft Guide](16-Microsoft-Azure-Interview-Guide.md) | Microsoft Azure team-specific prep |
| [Progress Tracker](08-Progress-Tracker.md) | Track your weekly progress |
| [Mock Interview Bank](09-Mock-Interview-Question-Bank.md) | 90 questions (Coding + SD + Behavioral) |
| [Google Guide](17-Google-Interview-Guide.md) | Google-specific interview prep |
| [Amazon Guide](18-Amazon-Interview-Guide.md) | Amazon Leadership Principles prep |
| [Meta Guide](19-Meta-Interview-Guide.md) | Meta-specific interview prep |
| [Apple Guide](20-Apple-Interview-Guide.md) | Apple-specific interview prep |
---


## Summary

This guide covers Amazon's interview process with a focus on Amazon's Leadership Principles, bar raiser rounds, system design expectations, and strategies for demonstrating customer obsession and ownership.

## References & Learn More

- [LeetCode](https://leetcode.com/)
- [NeetCode](https://neetcode.io/)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [Levels.fyi](https://www.levels.fyi/)
- [Cracking the Coding Interview](http://www.crackingthecodinginterview.com/)

## See Also
- [JavaScript](../01-JavaScript/)
- [TypeScript](../02-TypeScript/)
- [React](../03-React/)
- [System Design](../11-System-Design/)
- [Behavioral](../18-Behavioral/)
- [Coding Patterns](../19-Coding-Patterns/)
