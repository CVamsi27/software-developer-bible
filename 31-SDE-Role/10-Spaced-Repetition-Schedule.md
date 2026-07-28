[![Category: Interview](https://img.shields.io/badge/category-Interview-1f7a8a)](.)

# 🔄 Spaced Repetition Schedule

> **Maximize retention with scientifically-backed review intervals**
>
> Based on the Ebbinghaus forgetting curve — review just before you forget!

---

## 🧠 How Spaced Repetition Works

```text

Day 0:  Learn new material
Day 1:  First review (1 day later)
Day 3:  Second review (3 days later)
Day 7:  Third review (1 week later)
Day 14: Fourth review (2 weeks later)
Day 30: Fifth review (1 month later)

```

**Key Principle:** Each successful review extends the interval. If you struggle, restart from a shorter interval.

---

## 📅 12-Week Spaced Repetition Calendar

### Week 1: Arrays & Strings

| Day | New Material | Reviews Due |
|-----|--------------|-------------|
| Mon | Arrays basics, Two Sum pattern | - |
| Tue | Kadane's algorithm, Merge Intervals | Day 1: Arrays basics |
| Wed | Sort Colors, Dutch National Flag | Day 1: Kadane's, Day 3: Arrays basics |
| Thu | Prefix Sum, Product of Array | Day 1: Sort Colors, Day 3: Kadane's |
| Fri | Interval Merging patterns | Day 1: Prefix Sum, Day 3: Sort Colors |
| Sat | Review Day | Day 1: Interval, Day 3: Prefix Sum, Day 7: Arrays basics |
| Sun | Rest | Day 3: Interval, Day 7: Kadane's |

---

### Week 2: Two Pointers & Sliding Window

| Day | New Material | Reviews Due |
|-----|--------------|-------------|
| Mon | Two Pointers basics, Valid Palindrome | Day 1: Interval, Day 3: Prefix Sum, Day 7: Kadane's |
| Tue | Container With Most Water, 3Sum | Day 1: Two Ptrs basics, Day 3: Interval, Day 7: Prefix Sum |
| Wed | Sliding Window basics, Longest Substring | Day 1: Container, Day 3: Two Ptrs basics, Day 7: Interval |
| Thu | Minimum Window Substring | Day 1: Sliding Window, Day 3: Container, Day 7: Two Ptrs |
| Fri | Fixed vs Variable Window patterns | Day 1: Min Window, Day 3: Sliding Window, Day 7: Container |
| Sat | Review Day | Day 1: Fixed Window, Day 3: Min Window, Day 7: Sliding Window |
| Sun | Rest | Day 3: Fixed Window, Day 7: Min Window |

---

### Week 3: Hash Maps & Sets

| Day | New Material | Reviews Due |
|-----|--------------|-------------|
| Mon | HashMap basics, Group Anagrams | Day 1: Fixed Window, Day 3: Min Window, Day 7: Sliding Window |
| Tue | Frequency counting, Top K Elements | Day 1: HashMap basics, Day 3: Fixed Window, Day 7: Min Window |
| Wed | Prefix Sum + HashMap, Subarray Sum K | Day 1: Frequency, Day 3: HashMap basics, Day 7: Fixed Window |
| Thu | LRU Cache design | Day 1: Prefix+HashMap, Day 3: Frequency, Day 7: HashMap basics |
| Fri | Design patterns (Rate Limiter, etc.) | Day 1: LRU Cache, Day 3: Prefix+HashMap, Day 7: Frequency |
| Sat | Review Day | Day 1: Design, Day 3: LRU Cache, Day 7: Prefix+HashMap |
| Sun | Rest | Day 3: Design, Day 7: LRU Cache |

---

### Week 4: Binary Search

| Day | New Material | Reviews Due |
|-----|--------------|-------------|
| Mon | Binary Search basics, Classic template | Day 1: Design, Day 3: LRU Cache, Day 7: Prefix+HashMap |
| Tue | Boundary search, First/Last position | Day 1: BS basics, Day 3: Design, Day 7: LRU Cache |
| Wed | Rotated Array search | Day 1: Boundary, Day 3: BS basics, Day 7: Design |
| Thu | Search on Answer pattern | Day 1: Rotated, Day 3: Boundary, Day 7: BS basics |
| Fri | Advanced Binary Search problems | Day 1: Search Answer, Day 3: Rotated, Day 7: Boundary |
| Sat | Review Day | Day 1: Advanced BS, Day 3: Search Answer, Day 7: Rotated |
| Sun | Rest | Day 3: Advanced BS, Day 7: Search Answer |

---

### Week 5: Linked Lists & Stacks

| Day | New Material | Reviews Due |
|-----|--------------|-------------|
| Mon | Linked List basics, Reverse, Cycle detection | Day 1: Advanced BS, Day 3: Search Answer, Day 7: Rotated |
| Tue | Merge Lists, Remove Nth Node | Day 1: LL basics, Day 3: Advanced BS, Day 7: Search Answer |
| Wed | Stack basics, Valid Parentheses | Day 1: Merge Lists, Day 3: LL basics, Day 7: Advanced BS |
| Thu | Monotonic Stack, Next Greater Element | Day 1: Stack basics, Day 3: Merge Lists, Day 7: LL basics |
| Fri | Advanced Stack problems | Day 1: Monotonic, Day 3: Stack basics, Day 7: Merge Lists |
| Sat | Review Day | Day 1: Adv Stack, Day 3: Monotonic, Day 7: Stack basics |
| Sun | Rest | Day 3: Adv Stack, Day 7: Monotonic |

---

### Week 6: Trees - Traversal & BST

| Day | New Material | Reviews Due |
|-----|--------------|-------------|
| Mon | Tree basics, DFS (Pre/In/Post order) | Day 1: Adv Stack, Day 3: Monotonic, Day 7: Stack basics |
| Tue | BFS, Level Order Traversal | Day 1: Tree DFS, Day 3: Adv Stack, Day 7: Monotonic |
| Wed | BST basics, Validate BST | Day 1: Tree BFS, Day 3: Tree DFS, Day 7: Adv Stack |
| Thu | LCA, Path Sum problems | Day 1: BST basics, Day 3: Tree BFS, Day 7: Tree DFS |
| Fri | Tree construction, Serialization | Day 1: LCA, Day 3: BST basics, Day 7: Tree BFS |
| Sat | Review Day | Day 1: Serialization, Day 3: LCA, Day 7: BST basics |
| Sun | Rest | Day 3: Serialization, Day 7: LCA |

---

### Week 7: Trees - Advanced & Heaps

| Day | New Material | Reviews Due |
|-----|--------------|-------------|
| Mon | Trie, Implement Trie | Day 1: Serialization, Day 3: LCA, Day 7: BST basics |
| Tue | Heap basics, Kth Largest | Day 1: Trie, Day 3: Serialization, Day 7: LCA |
| Wed | Two Heaps, Find Median | Day 1: Heap basics, Day 3: Trie, Day 7: Serialization |
| Thu | Merge K Sorted Lists | Day 1: Two Heaps, Day 3: Heap basics, Day 7: Trie |
| Fri | Advanced Heap problems | Day 1: Merge K, Day 3: Two Heaps, Day 7: Heap basics |
| Sat | Review Day | Day 1: Adv Heap, Day 3: Merge K, Day 7: Two Heaps |
| Sun | Rest | Day 3: Adv Heap, Day 7: Merge K |

---

### Week 8: Graphs - BFS/DFS

| Day | New Material | Reviews Due |
|-----|--------------|-------------|
| Mon | Graph basics, BFS/DFS | Day 1: Adv Heap, Day 3: Merge K, Day 7: Two Heaps |
| Tue | Island problems, Flood Fill | Day 1: Graph BFS/DFS, Day 3: Adv Heap, Day 7: Merge K |
| Wed | Course Schedule, Topological Sort | Day 1: Islands, Day 3: Graph BFS/DFS, Day 7: Adv Heap |
| Thu | Clone Graph, Union-Find | Day 1: Course Schedule, Day 3: Islands, Day 7: Graph BFS/DFS |
| Fri | Advanced Graph problems | Day 1: Clone Graph, Day 3: Course Schedule, Day 7: Islands |
| Sat | Review Day | Day 1: Adv Graph, Day 3: Clone Graph, Day 7: Course Schedule |
| Sun | Rest | Day 3: Adv Graph, Day 7: Clone Graph |

---

### Week 9: Graphs - Advanced

| Day | New Material | Reviews Due |
|-----|--------------|-------------|
| Mon | Dijkstra, Shortest Path | Day 1: Adv Graph, Day 3: Clone Graph, Day 7: Course Schedule |
| Tue | Bellman-Ford, Floyd-Warshall | Day 1: Dijkstra, Day 3: Adv Graph, Day 7: Clone Graph |
| Wed | MST (Prim, Kruskal) | Day 1: Bellman-Ford, Day 3: Dijkstra, Day 7: Adv Graph |
| Thu | Advanced Graph algorithms | Day 1: MST, Day 3: Bellman-Ford, Day 7: Dijkstra |
| Fri | Graph review and practice | Day 1: Adv Algorithms, Day 3: MST, Day 7: Bellman-Ford |
| Sat | Review Day | Day 1: Graph Review, Day 3: Adv Algorithms, Day 7: MST |
| Sun | Rest | Day 3: Graph Review, Day 7: Adv Algorithms |

---

### Week 10: Dynamic Programming - Basics

| Day | New Material | Reviews Due |
|-----|--------------|-------------|
| Mon | DP basics, Fibonacci, Climbing Stairs | Day 1: Graph Review, Day 3: Adv Algorithms, Day 7: MST |
| Tue | 1D DP, House Robber | Day 1: DP basics, Day 3: Graph Review, Day 7: Adv Algorithms |
| Wed | Knapsack (0/1, Unbounded) | Day 1: 1D DP, Day 3: DP basics, Day 7: Graph Review |
| Thu | LIS, LCS | Day 1: Knapsack, Day 3: 1D DP, Day 7: DP basics |
| Fri | Grid DP, Unique Paths | Day 1: LIS/LCS, Day 3: Knapsack, Day 7: 1D DP |
| Sat | Review Day | Day 1: Grid DP, Day 3: LIS/LCS, Day 7: Knapsack |
| Sun | Rest | Day 3: Grid DP, Day 7: LIS/LCS |

---

### Week 11: Dynamic Programming - Advanced & Backtracking

| Day | New Material | Reviews Due |
|-----|--------------|-------------|
| Mon | 2D DP, Edit Distance | Day 1: Grid DP, Day 3: LIS/LCS, Day 7: Knapsack |
| Tue | Interval DP, Burst Balloons | Day 1: 2D DP, Day 3: Grid DP, Day 7: LIS/LCS |
| Wed | Backtracking basics, Combinations | Day 1: Interval DP, Day 3: 2D DP, Day 7: Grid DP |
| Thu | Permutations, N-Queens | Day 1: Backtracking, Day 3: Interval DP, Day 7: 2D DP |
| Fri | Greedy algorithms | Day 1: Permutations, Day 3: Backtracking, Day 7: Interval DP |
| Sat | Review Day | Day 1: Greedy, Day 3: Permutations, Day 7: Backtracking |
| Sun | Rest | Day 3: Greedy, Day 7: Permutations |

---

### Week 12: Hard Problems & Mock Interviews

| Day | New Material | Reviews Due |
|-----|--------------|-------------|
| Mon | Hard mixed problems | Day 1: Greedy, Day 3: Permutations, Day 7: Backtracking |
| Tue | Hard mixed problems | Day 1: Hard Mix, Day 3: Greedy, Day 7: Permutations |
| Wed | Mock Interview 1 | Day 1: Hard Mix 2, Day 3: Hard Mix, Day 7: Greedy |
| Thu | Mock Interview 2 | Day 1: Mock 1, Day 3: Hard Mix 2, Day 7: Hard Mix |
| Fri | Weak areas review | Day 1: Mock 2, Day 3: Mock 1, Day 7: Hard Mix 2 |
| Sat | Final Review | Day 1: Weak Areas, Day 3: Mock 2, Day 7: Mock 1 |
| Sun | Rest | Day 3: Weak Areas, Day 7: Mock 2 |

---

## 📋 Daily Review Checklist

### Morning Review (30 min)
- [ ] Review yesterday's new material
- [ ] Complete any Day 1 reviews due
- [ ] Mark topics as "Reviewed" in tracker

### Evening Review (30 min)
- [ ] Complete any Day 3 reviews due
- [ ] Practice 1-2 problems from reviewed topics
- [ ] Update progress tracker

### Weekly Review (Saturday, 1-2 hours)
- [ ] Complete all Day 7 reviews due
- [ ] Review weak areas identified during the week
- [ ] Update readiness scores
- [ ] Plan next week's focus areas

---

## 🎯 Review Intervals by Topic Mastery

| Mastery Level | Review Interval | Action |
|---------------|-----------------|--------|
| **New** | Daily | Just learned, review tomorrow |
| **Learning** | Every 3 days | Getting familiar, review in 3 days |
| **Familiar** | Weekly | Understand well, review in 1 week |
| **Mastered** | Bi-weekly | Can solve confidently, review in 2 weeks |
| **Expert** | Monthly | Can teach others, review in 1 month |

### How to Determine Mastery Level

```text

New:      Can't solve without help
Learning: Can solve with hints, takes >30 min
Familiar: Can solve independently, 20-30 min
Mastered: Can solve quickly, <20 min, explain clearly
Expert:   Can solve in <15 min, can teach, know variations

```

---

## 📊 Review Tracking Template

### Daily Review Log

| Date | Topic | Interval | Mastery Level | Time Spent | Notes |
|------|-------|----------|---------------|------------|-------|
| ___/___ | | Day 1/3/7/14 | New/Learning/Familiar/Mastered/Expert | ___min | |

### Weekly Review Summary

| Week | Topics Reviewed | Total Reviews | Weak Areas | Next Focus |
|------|-----------------|---------------|------------|------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |
| 7 | | | | |
| 8 | | | | |
| 9 | | | | |
| 10 | | | | |
| 11 | | | | |
| 12 | | | | |

---

## 🔧 Spaced Repetition Tools

### Manual Method (Paper/Spreadsheet)
- Use the tracking templates above
- Mark topics with colored sticky notes (Red=New, Yellow=Learning, Green=Mastered)
- Review based on intervals

### Digital Tools
- [Anki](https://apps.ankiweb.net/) — Free flashcard app with built-in spaced repetition
- [Quizlet](https://quizlet.com/) — Create custom flashcard decks
- [Notion](https://www.notion.so/) — Create databases with review schedules
- [Google Sheets](https://sheets.google.com/) — Custom tracking spreadsheet

### Anki Setup for Interview Prep

```text

1. Create a new deck: "SDE Interview Prep"
2. Add cards for each concept/pattern
3. Tag cards by topic (Arrays, Trees, DP, etc.)
4. Use built-in spaced repetition scheduler
5. Review daily (10-15 min)

```

---

## 📈 Expected Retention Curve

```text

Without Spaced Repetition:
Day 1:  100% retention
Day 3:  60% retention
Day 7:  40% retention
Day 14: 25% retention
Day 30: 15% retention

With Spaced Repetition:
Day 1:  100% → Review → 100%
Day 3:  95% → Review → 100%
Day 7:  90% → Review → 100%
Day 14: 85% → Review → 100%
Day 30: 80% → Review → 100%

```

**Result:** Instead of forgetting 85% in a month, you retain 80%+ with regular review!

---

## 🎯 Integration with Study Plan

### How to Use This Schedule

1. **Week 1-4:** Learn new material + follow review schedule
2. **Week 5-8:** Continue learning + maintain reviews
3. **Week 9-12:** Focus on weak areas + heavy review

### Daily Time Allocation (4-6 hours)

```text

Morning (2-3 hours):
├── 30 min: Review yesterday's material
├── 2 hours: Solve new problems
└── 30 min: Document patterns

Afternoon (1.5-2 hours):
├── 30 min: Learn new pattern concepts
├── 1 hour: Solve pattern-specific problems
└── 30 min: Update notes

Evening (1-1.5 hours):
├── 30 min: System Design / Behavioral
└── 30 min: Complete remaining reviews

```

---

## 💡 Tips for Success

1. **Be Consistent** — Review every day, even if just for 10 minutes
2. **Don't Skip Intervals** — The schedule is designed for optimal retention
3. **Adjust Based on Mastery** — Move faster if you master topics quickly
4. **Track Everything** — Use the templates to monitor your progress
5. **Focus on Weak Areas** — Spend more time on topics you struggle with
6. **Teach Others** — Explaining concepts reinforces your understanding
7. **Use Active Recall** — Don't just re-read; try to solve problems from memory

---

> **Remember:** Spaced repetition is about working smarter, not harder. By reviewing at the right intervals, you'll retain more information with less total study time!

> **Pro Tip:** Combine spaced repetition with interleaving — mix different topics in your practice sessions rather than focusing on one topic for hours. This improves your ability to identify which pattern to apply!
---

## Summary

This schedule provides a structured 12-week spaced repetition plan for interview preparation, balancing topic review, problem-solving practice, and mock interviews to maximize long-term retention.

## See Also
- [Behavioral](../18-Behavioral/)
- [Coding Patterns](../19-Coding-Patterns/)
- [JavaScript](../01-JavaScript/)
- [React](../03-React/)
- [System Design](../11-System-Design/)
- [TypeScript](../02-TypeScript/)

## References & Learn More

- [LeetCode](https://leetcode.com/)
- [NeetCode](https://neetcode.io/)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [Levels.fyi](https://www.levels.fyi/)
- [Cracking the Coding Interview](http://www.crackingthecodinginterview.com/)
