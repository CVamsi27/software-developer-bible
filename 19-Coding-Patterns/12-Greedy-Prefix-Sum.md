# Greedy & Prefix Sum

## Definition

**Greedy Algorithm**: A technique that makes the locally optimal choice at each step with the hope of finding a global optimum. It builds a solution piece by piece, always choosing the next piece that offers the most immediate benefit.

**Prefix Sum**: A technique where you precompute cumulative sums to answer range sum queries efficiently. PrefixSum[i] = sum of all elements from index 0 to i-1.

## When to Use

**Greedy:**

- When local optimal leads to global optimal
- Scheduling problems (job sequencing, activity selection)
- Huffman coding, Dijkstra's algorithm
- Minimum spanning tree (Kruskal's, Prim's)
- When you can make a choice without reconsidering

**Prefix Sum:**

- Range sum queries (subarray sum)
- Finding subarrays with specific sum
- Difference arrays
- Cumulative frequency problems
- When you need to query sums multiple times

## Template

```typescript
// Prefix Sum
function buildPrefixSum(nums: number[]): number[] {
  const prefix = new Array(nums.length + 1).fill(0);
  for (let i = 0; i < nums.length; i++) {
    prefix[i + 1] = prefix[i] + nums[i];
  }
  return prefix;
}

// Range sum query: sum of nums[left..right]
function rangeSum(prefix: number[], left: number, right: number): number {
  return prefix[right + 1] - prefix[left];
}

// Greedy template
function greedySort(items: number[][]): number {
  items.sort((a, b) => /* custom comparator */);

  let result = 0;
  for (const item of items) {
    if (/* can include */) {
      result += item[1]; // or whatever value
    }
  }
  return result;
}

```

## How It Works

```text
Prefix Sum:
Array:      [2, 4, 6, 8, 10]
Prefix: [0, 2, 6, 12, 20, 30]
Index:   0  1  2  3  4   5

Sum(1,3) = Prefix[4] - Prefix[1] = 20 - 2 = 18
          (elements 4+6+8 = 18)

Greedy Example (Activity Selection):
Activities: [(1,4), (3,5), (0,6), (5,7), (3,9), (5,9), (6,10), (8,11), (8,12), (2,14), (12,16)]

Sort by end time:
(1,4) (3,5) (0,6) (5,7) (3,9) (5,9) (6,10) (8,11) (8,12) (2,14) (12,16)

Greedy choice:

1. Pick (1,4) - ends earliest

2. Skip (3,5), (0,6) - overlap

3. Pick (5,7) - first non-overlapping

4. Skip (3,9), (5,9), (6,10) - overlap

5. Pick (8,11) - first non-overlapping

6. Pick (12,16) - first non-overlapping

Result: 4 activities

```

### ASCII Diagram

```text
PREFIX SUM:
Array:      [2, 4, 6, 8, 10]
             ├──┼──┼──┼──┤
Prefix: [0, 2, 6, 12, 20, 30]
         ├──┼──┼──┼──┼──┤

Sum(1,3) = Prefix[4] - Prefix[1]
         = 20 - 2 = 18
         (4 + 6 + 8 = 18) ✓

2D PREFIX SUM:
Matrix:     [[1, 2, 3],
             [4, 5, 6],
             [7, 8, 9]]

Prefix:     [[0, 0, 0, 0],
             [0, 1, 3, 6],
             [0, 5, 12, 21],
             [0, 12, 27, 45]]

Sum(1,1 to 2,2) = Prefix[3][3] - Prefix[1][3] - Prefix[3][1] + Prefix[1][1]
                = 45 - 6 - 12 + 1 = 28
                (5+6+8+9 = 28) ✓

GREEDY (JOB SEQUENCING):
Jobs: [(A,20,100), (B,1,19), (C,2,27), (D,1,25), (E,3,15)]

Sort by profit: A(100), D(25), C(27), B(19), E(15)

Time slots: [_][_][_][_][_][_][_][_][_][_]

1. Job A (deadline 2): [_][_][A][_][_][_][_][_][_][_]

2. Job D (deadline 1): [_][_][A][_][_][_][_][_][_][_] → [D][_][A][_][_][_][_][_][_][_]

3. Job C (deadline 2): [D][_][A][_][_][_][_][_][_][_] → [D][C][A][_][_][_][_][_][_][_]

Total profit: 100 + 25 + 27 = 152

```

## Code Examples (TypeScript)

### Problem 1: Prefix Sum - Range Sum Query

```typescript
class NumArray {
  private prefix: number[];

  constructor(nums: number[]) {
    this.prefix = new Array(nums.length + 1).fill(0);
    for (let i = 0; i < nums.length; i++) {
      this.prefix[i + 1] = this.prefix[i] + nums[i];
    }
  }

  sumRange(left: number, right: number): number {
    return this.prefix[right + 1] - this.prefix[left];
  }
}

// Example
const numArray = new NumArray([-2, 0, 3, -5, 2, -1]);
console.log(numArray.sumRange(0, 2)); // 1 (-2+0+3)
console.log(numArray.sumRange(2, 5)); // -1 (3-5+2-1)
console.log(numArray.sumRange(0, 5)); // -3 (sum of all)

```

### Problem 2: Subarray Sum Equals K

```typescript
function subarraySum(nums: number[], k: number): number {
  const prefixCount = new Map<number, number>();
  prefixCount.set(0, 1);

  let prefixSum = 0;
  let count = 0;

  for (const num of nums) {
    prefixSum += num;

    if (prefixCount.has(prefixSum - k)) {
      count += prefixCount.get(prefixSum - k)!;
    }

    prefixCount.set(prefixSum, (prefixCount.get(prefixSum) || 0) + 1);
  }

  return count;
}

// Example
console.log(subarraySum([1, 1, 1], 2)); // 2
console.log(subarraySum([1, 2, 3], 3)); // 2

```

### Problem 3: Product of Array Except Self (Prefix Product)

```typescript
function productExceptSelf(nums: number[]): number[] {
  const n = nums.length;
  const result = new Array(n).fill(1);

  // Left prefix products
  let leftProduct = 1;
  for (let i = 0; i < n; i++) {
    result[i] = leftProduct;
    leftProduct *= nums[i];
  }

  // Right prefix products
  let rightProduct = 1;
  for (let i = n - 1; i >= 0; i--) {
    result[i] *= rightProduct;
    rightProduct *= nums[i];
  }

  return result;
}

// Example
console.log(productExceptSelf([1, 2, 3, 4])); // [24, 12, 8, 6]
console.log(productExceptSelf([-1, 1, 0, -3, 3])); // [0, 0, 9, 0, 0]

```

### Problem 4: Maximum Subarray Sum (Kadane's Algorithm - Greedy)

```typescript
function maxSubArray(nums: number[]): number {
  let maxSum = nums[0];
  let currentSum = nums[0];

  for (let i = 1; i < nums.length; i++) {
    currentSum = Math.max(nums[i], currentSum + nums[i]);
    maxSum = Math.max(maxSum, currentSum);
  }

  return maxSum;
}

// Example
console.log(maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4])); // 6
console.log(maxSubArray([1])); // 1
console.log(maxSubArray([5, 4, -1, 7, 8])); // 23

```

### Problem 5: Jump Game (Greedy)

```typescript
function canJump(nums: number[]): boolean {
  let maxReach = 0;

  for (let i = 0; i < nums.length; i++) {
    if (i > maxReach) return false;
    maxReach = Math.max(maxReach, i + nums[i]);
  }

  return true;
}

// Example
console.log(canJump([2, 3, 1, 1, 4])); // true
console.log(canJump([3, 2, 1, 0, 4])); // false

```

### Problem 6: Gas Station (Greedy)

```typescript
function canCompleteCircuit(gas: number[], cost: number[]): number {
  let totalGas = 0;
  let currentGas = 0;
  let start = 0;

  for (let i = 0; i < gas.length; i++) {
    const diff = gas[i] - cost[i];
    totalGas += diff;
    currentGas += diff;

    if (currentGas < 0) {
      start = i + 1;
      currentGas = 0;
    }
  }

  return totalGas >= 0 ? start : -1;
}

// Example
console.log(canCompleteCircuit([1,2,3,4,5], [3,4,5,1,2])); // 3
console.log(canCompleteCircuit([2,3,4], [3,4,3])); // -1

```

### Problem 7: Maximum Product Subarray

```typescript
function maxProduct(nums: number[]): number {
  let maxProd = nums[0];
  let minProd = nums[0];
  let result = nums[0];

  for (let i = 1; i < nums.length; i++) {
    const temp = maxProd;
    maxProd = Math.max(nums[i], maxProd * nums[i], minProd * nums[i]);
    minProd = Math.min(nums[i], temp * nums[i], minProd * nums[i]);
    result = Math.max(result, maxProd);
  }

  return result;
}

// Example
console.log(maxProduct([2, 3, -2, 4])); // 6
console.log(maxProduct([-2, 0, -1])); // 0

```

## Common Mistakes

1. **Not verifying greedy choice**: Ensure local optimal leads to global optimal

2. **Wrong prefix sum indexing**: Off-by-one errors in range queries

3. **Forgetting negative numbers**: In max subarray, current sum can reset

4. **Not handling edge cases**: Empty arrays, single elements

5. **Greedy doesn't always work**: Some problems require DP instead

## Time/Space Complexity

| Algorithm | Time | Space |
|-----------|------|-------|
| Prefix Sum | O(n) build, O(1) query | O(n) |
| Range Sum Query | O(n) build, O(1) query | O(n) |
| Kadane's | O(n) | O(1) |
| Jump Game | O(n) | O(1) |
| Gas Station | O(n) | O(1) |

## Interview Problems

### Easy

1. **Maximum Subarray** (LeetCode 53)

2. **Best Time to Buy and Sell Stock** (LeetCode 121)

3. **Range Sum Query - Immutable** (LeetCode 303)

4. **Jump Game** (LeetCode 55)

### Medium

1. **Subarray Sum Equals K** (LeetCode 560)

2. **Product of Array Except Self** (LeetCode 238)

3. **Jump Game II** (LeetCode 45)

4. **Gas Station** (LeetCode 134)

5. **Maximum Product Subarray** (LeetCode 152)

6. **Hand of Straights** (LeetCode 846)

7. **Task Scheduler** (LeetCode 621)

### Hard

1. **Wildcard Matching** (LeetCode 44)

2. **Sliding Window Maximum** (LeetCode 239)

3. **Frog Jump** (LeetCode 403)

4. **Russian Doll Envelopes** (LeetCode 354)

## Summary

Greedy algorithms make locally optimal choices at each step. Prefix sum enables efficient range queries. Together, they solve many optimization and query problems efficiently.

## Cheat Sheet

```text
Pattern: Greedy + Prefix Sum
Use when: Optimization, range queries, local optimal → global optimal
Time: O(n) | Space: O(n) for prefix, O(1) for greedy

Greedy:
┌─────────────────────────────────────────┐
│ 1. Sort by relevant criteria            │
│ 2. Make locally optimal choice          │
│ 3. Never reconsider (no backtracking)   │
│ 4. Prove correctness if possible        │
└─────────────────────────────────────────┘

Prefix Sum:
┌─────────────────────────────────────────┐
│ Build: prefix[i+1] = prefix[i] + nums[i]│
│ Query: sum(left,right) = prefix[right+1] - prefix[left] │
│                                         │
│ For subarray sum = k:                   │
│   Use Map to count prefix sums          │
│   count += map.get(prefixSum - k)       │
└─────────────────────────────────────────┘

When to use greedy:

- Activity selection
- Job scheduling
- Huffman coding
- Coin change (canonical systems)

When to use prefix sum:

- Range sum queries
- Subarray sum problems
- Difference arrays
- 2D range queries

```

---

## References & Learn More

- [LeetCode Greedy](https://leetcode.com/tag/greedy/)
- [NeetCode Greedy](https://neetcode.io/)
- [CP-Algorithms](https://cp-algorithms.com/)
- [Algorithm Design by Kleinberg & Tardos](https://www.amazon.com/Algorithm-Design-Kleinberg-Jon/dp/0321295358)
- [GeeksforGeeks Greedy](https://www.geeksforgeeks.org/greedy-algorithms/)
