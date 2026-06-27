# Dynamic Programming

## Definition

Dynamic Programming (DP) is an algorithmic technique for solving optimization problems by breaking them down into simpler subproblems and storing the results of subproblems to avoid redundant computations. It's applicable when the problem has overlapping subproblems and optimal substructure.

## When to Use

- Optimization problems (min/max)
- Counting problems
- Problems with overlapping subproblems
- Problems with optimal substructure
- When brute force is exponential

## Template

```typescript
// Memoization (Top-Down)
function dpMemo(n: number, memo: Map<number, number> = new Map()): number {
  if (n <= 1) return n;
  if (memo.has(n)) return memo.get(n)!;

  const result = dpMemo(n - 1, memo) + dpMemo(n - 2, memo);
  memo.set(n, result);
  return result;
}

// Tabulation (Bottom-Up)
function dpTab(n: number): number {
  if (n <= 1) return n;

  const dp = new Array(n + 1).fill(0);
  dp[0] = 0;
  dp[1] = 1;

  for (let i = 2; i <= n; i++) {
    dp[i] = dp[i - 1] + dp[i - 2];
  }

  return dp[n];
}
```

## How It Works

```
Fibonacci Sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21...

Naive Recursion:          Memoization:
f(5)                      f(5)
├── f(4)                  ├── f(4)
│   ├── f(3)              │   ├── f(3)
│   │   ├── f(2)          │   │   ├── f(2)
│   │   │   ├── f(1)      │   │   │   ├── f(1)
│   │   │   └── f(0)      │   │   │   └── f(0)
│   │   └── f(1)          │   │   └── f(1)
│   └── f(2)              │   └── f(2)
│       ├── f(1)          └── f(3) [cached!]
│       └── f(0)
└── f(3)
    ├── f(2)
    │   ├── f(1)
    │   └── f(0)
    └── f(1)

Tabulation (Bottom-Up):
dp[0] = 0
dp[1] = 1
dp[2] = dp[1] + dp[0] = 1
dp[3] = dp[2] + dp[1] = 2
dp[4] = dp[3] + dp[2] = 3
dp[5] = dp[4] + dp[3] = 5
```

### ASCII Diagram

```
0/1 KNAPSACK PROBLEM:

Items: [(w=2, v=3), (w=3, v=4), (w=4, v=5)]
Capacity: 5

DP Table:
       Capacity
       0  1  2  3  4  5
Item 0  0  0  3  3  3  3
Item 1  0  0  3  4  4  7
Item 2  0  0  3  4  5  7

Answer: 7 (items 0 and 1)

LCS TABLE:
       ""  A  B  C  B
  ""    0  0  0  0  0
  A     0  1  1  1  1
  B     0  1  2  2  2
  C     0  1  2  3  3
  B     0  1  2  3  4

Answer: 4 (ABCB)
```

## Code Examples (TypeScript)

### Problem 1: Fibonacci Number

```typescript
// Memoization
function fibMemo(n: number): number {
  const memo = new Map<number, number>();

  function dp(n: number): number {
    if (n <= 1) return n;
    if (memo.has(n)) return memo.get(n)!;

    memo.set(n, dp(n - 1) + dp(n - 2));
    return memo.get(n)!;
  }

  return dp(n);
}

// Tabulation
function fibTab(n: number): number {
  if (n <= 1) return n;

  let prev = 0;
  let curr = 1;

  for (let i = 2; i <= n; i++) {
    const next = prev + curr;
    prev = curr;
    curr = next;
  }

  return curr;
}

// Example
console.log(fibMemo(10)); // 55
console.log(fibTab(10));  // 55
```

### Problem 2: 0/1 Knapsack

```typescript
function knapsack(weights: number[], values: number[], capacity: number): number {
  const n = weights.length;
  const dp = Array(n + 1).fill(null).map(() => Array(capacity + 1).fill(0));

  for (let i = 1; i <= n; i++) {
    for (let w = 0; w <= capacity; w++) {
      if (weights[i - 1] <= w) {
        dp[i][w] = Math.max(
          dp[i - 1][w],
          dp[i - 1][w - weights[i - 1]] + values[i - 1]
        );
      } else {
        dp[i][w] = dp[i - 1][w];
      }
    }
  }

  return dp[n][capacity];
}

// Example
console.log(knapsack([2, 3, 4, 5], [3, 4, 5, 6], 5)); // 7
```

### Problem 3: Longest Common Subsequence

```typescript
function longestCommonSubsequence(text1: string, text2: string): number {
  const m = text1.length;
  const n = text2.length;

  const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));

  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (text1[i - 1] === text2[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }

  return dp[m][n];
}

// Example
console.log(longestCommonSubsequence("abcde", "ace")); // 3
console.log(longestCommonSubsequence("abc", "abc"));   // 3
console.log(longestCommonSubsequence("abc", "def"));   // 0
```

### Problem 4: Longest Increasing Subsequence

```typescript
function lengthOfLIS(nums: number[]): number {
  const n = nums.length;
  const dp = new Array(n).fill(1);

  for (let i = 1; i < n; i++) {
    for (let j = 0; j < i; j++) {
      if (nums[j] < nums[i]) {
        dp[i] = Math.max(dp[i], dp[j] + 1);
      }
    }
  }

  return Math.max(...dp);
}

// Example
console.log(lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18])); // 4 ([2,3,7,101])
```

### Problem 5: Coin Change

```typescript
function coinChange(coins: number[], amount: number): number {
  const dp = new Array(amount + 1).fill(Infinity);
  dp[0] = 0;

  for (let i = 1; i <= amount; i++) {
    for (const coin of coins) {
      if (i >= coin && dp[i - coin] !== Infinity) {
        dp[i] = Math.min(dp[i], dp[i - coin] + 1);
      }
    }
  }

  return dp[amount] === Infinity ? -1 : dp[amount];
}

// Example
console.log(coinChange([1, 2, 5], 11)); // 3 (5 + 5 + 1)
console.log(coinChange([2], 3));         // -1
```

### Problem 6: Edit Distance

```typescript
function minDistance(word1: string, word2: string): number {
  const m = word1.length;
  const n = word2.length;

  const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));

  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;

  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (word1[i - 1] === word2[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1];
      } else {
        dp[i][j] = 1 + Math.min(
          dp[i - 1][j],     // delete
          dp[i][j - 1],     // insert
          dp[i - 1][j - 1]  // replace
        );
      }
    }
  }

  return dp[m][n];
}

// Example
console.log(minDistance("horse", "ros")); // 3
console.log(minDistance("intention", "execution")); // 5
```

## Common Mistakes

1. **Not identifying overlapping subproblems**: Use memoization to avoid redundant work
2. **Wrong recurrence relation**: Carefully define the relationship between subproblems
3. **Incorrect base case**: Always define base cases before recurrence
4. **Not considering all options**: In knapsack, consider both including and excluding items
5. **Space optimization not needed**: Sometimes O(n) space is sufficient, don't over-optimize

## Time/Space Complexity

| Problem | Time | Space | Optimized Space |
|---------|------|-------|-----------------|
| Fibonacci | O(n) | O(n) | O(1) |
| Knapsack | O(n×W) | O(n×W) | O(W) |
| LCS | O(m×n) | O(m×n) | O(min(m,n)) |
| LIS | O(n²) | O(n) | O(n log n) |
| Coin Change | O(n×amount) | O(amount) | O(amount) |
| Edit Distance | O(m×n) | O(m×n) | O(min(m,n)) |

## Interview Problems

### Easy

1. **Climbing Stairs** (LeetCode 70)
2. **House Robber** (LeetCode 198)
3. **Min Cost Climbing Stairs** (LeetCode 746)

### Medium

1. **Coin Change** (LeetCode 322)
2. **Longest Increasing Subsequence** (LeetCode 300)
3. **Word Break** (LeetCode 139)
4. **Unique Paths** (LeetCode 62)
5. **Maximum Product Subarray** (LeetCode 152)
6. **Decode Ways** (LeetCode 91)
7. **Longest Common Subsequence** (LeetCode 1143)

### Hard

1. **Edit Distance** (LeetCode 72)
2. **Burst Balloons** (LeetCode 312)
3. **Regular Expression Matching** (LeetCode 10)
4. **Wildcard Matching** (LeetCode 44)
5. **Longest Valid Parentheses** (LeetCode 32)

## Summary

Dynamic Programming is a powerful technique for solving optimization problems with overlapping subproblems and optimal substructure. Choose between memoization (top-down) and tabulation (bottom-up) based on the problem.

## Cheat Sheet

```
Pattern: Dynamic Programming
Use when: Optimization, counting, overlapping subproblems
Time: O(n) to O(n²) | Space: O(n) to O(n²)

Types:
┌─────────────────────────────────────────┐
│ 1. Memoization (Top-Down)               │
│    - Recursive with caching             │
│    - Only compute needed subproblems    │
│                                         │
│ 2. Tabulation (Bottom-Up)               │
│    - Iterative with table               │
│    - Computes all subproblems           │
│                                         │
│ 3. Space Optimized                      │
│    - Only keep last row/column          │
│    - Reduces space complexity           │
└─────────────────────────────────────────┘

Steps to solve DP:
1. Define state: what does dp[i] represent?
2. Base case: what are the simplest cases?
3. Recurrence: how to compute dp[i] from smaller subproblems?
4. Answer: where is the final answer in the table?
```

---

## References & Learn More
- [LeetCode Dynamic Programming](https://leetcode.com/tag/dynamic-programming/)
- [NeetCode Dynamic Programming](https://neetcode.io/)
- [CP-Algorithms](https://cp-algorithms.com/)
- [Algorithm Design by Kleinberg & Tardos](https://www.amazon.com/Algorithm-Design-Kleinberg-Jon/dp/0321295358)
- [GeeksforGeeks Dynamic Programming](https://www.geeksforgeeks.org/dynamic-programming/)
