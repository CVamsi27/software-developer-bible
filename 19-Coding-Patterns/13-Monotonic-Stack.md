---
section: Coding Patterns
category: Interview
tags: [concept, practice]
---

# Monotonic Stack

## Definition

A **monotonic stack** is a stack that maintains its elements in **strictly increasing or strictly decreasing order** as you push and pop. It's the right pattern for "next greater/smaller element" problems, because when a new element arrives, you can **pop all elements that are no longer valid** in O(1) amortized. The two flavors:

- **Monotonic increasing stack** (bottom to top: increasing): the top is always the **smallest** element seen so far; useful for "next smaller element"
- **Monotonic decreasing stack** (bottom to top: decreasing): the top is always the **largest** element seen so far; useful for "next greater element"

## TL;DR

A monotonic stack solves "for each element, find the next greater/smaller element" in **O(n) total** instead of O(n²). As you traverse, you pop elements that have found their answer, then push the current element. Each element is pushed and popped at most once → amortized O(1) per element. Variants: next greater (decreasing stack), next smaller (increasing stack), previous greater/smaller (pop from one end, look at the other), and "circular array" (traverse twice with modulo).

## Why it matters

Monotonic stack appears in **~5% of FAANG interview questions** and is the canonical solution to **"Daily Temperatures," "Largest Rectangle in Histogram," "Trapping Rain Water," and "Next Greater Element"** problems. The senior signal: understanding *why* the amortized O(n) bound holds (each element pushed and popped exactly once), and applying the pattern to variants (next greater in a circular array, stock span, asteroid collision). Weak candidates reach for O(n²) brute force; strong candidates recognize the "next greater" signature and code the stack-based solution in 5 minutes.

## When to Use

- **"Next greater/smaller element"**: for each element, find the nearest element to its right that is greater/smaller
- **Largest rectangle in histogram**: for each bar, find the nearest smaller bar on each side (using monotonic stack)
- **Trapping rain water**: monotonic stack of bar heights, pop when current is taller, compute trapped water
- **Stock span**: for each day's price, count consecutive days with price ≤ today
- **Asteroid collision / removing K digits**: simulate with a stack that maintains a monotonic property
- **Pattern signature**: input is an array; output is per-element information about a "neighbor" relationship; brute force is O(n²)

## Template

```typescript
// Next Greater Element (decreasing stack)
function nextGreaterElements(nums: number[]): number[] {
  const n = nums.length;
  const result = new Array(n).fill(-1);
  const stack: number[] = []; // stores INDICES of elements waiting for their "next greater"

  for (let i = 0; i < n; i++) {
    // Pop elements that have found their next greater element (current num)
    while (stack.length > 0 && nums[stack[stack.length - 1]] < nums[i]) {
      const idx = stack.pop()!;
      result[idx] = nums[i];
    }
    stack.push(i);
  }

  return result;
}

// Largest Rectangle in Histogram (increasing stack)
function largestRectangleArea(heights: number[]): number {
  const stack: number[] = []; // stores indices, increasing heights
  let maxArea = 0;

  for (let i = 0; i <= heights.length; i++) {
    const currentHeight = i < heights.length ? heights[i] : 0; // sentinel for flush

    while (stack.length > 0 && heights[stack[stack.length - 1]] > currentHeight) {
      const height = heights[stack.pop()!];
      const width = stack.length === 0 ? i : i - stack[stack.length - 1] - 1;
      maxArea = Math.max(maxArea, height * width);
    }
    stack.push(i);
  }

  return maxArea;
}
```

## How It Works

```text
INPUT: [2, 1, 2, 4, 3]      GOAL: next greater element for each index

Step-by-step with decreasing stack (top = index of "next greater" answer pending):

i=0, val=2  |  stack=[]              → push 0  | stack=[0]
            |  No popped (stack empty)
i=1, val=1  |  stack=[0], top has 2  → 2 < 1 ? NO (1 < 2, but we want next GREATER, so keep 0)
            |  (we only pop if top's val < current val)
            |  push 1                | stack=[0,1]
i=2, val=2  |  stack=[0,1], top is 1 → 1 < 2? YES → pop 1, result[1] = 2
            |  stack=[0], top is 0   → 2 < 2? NO (not strict)
            |  push 2                | stack=[0,2]
i=3, val=4  |  stack=[0,2]           → 2 < 4? YES → pop 2, result[2] = 4
            |                        → 0 < 4? YES → pop 0, result[0] = 4
            |  push 3                | stack=[3]
i=4, val=3  |  stack=[3], top is 3   → 4 < 3? NO
            |  push 4                | stack=[3,4]
End: indices 3 and 4 still in stack → result[3] = -1, result[4] = -1

RESULT: [4, 2, 4, -1, -1]
```

Each element is **pushed exactly once** and **popped at most once** → O(2n) = O(n) total work.

## Code Examples (TypeScript)

### Example 1: Daily Temperatures (LeetCode 739)

```typescript
/**
 * Given daily temperatures, return an array answer such that
 * answer[i] is the number of days until a warmer temperature.
 * If no future day is warmer, answer[i] = 0.
 */
function dailyTemperatures(temperatures: number[]): number[] {
  const n = temperatures.length;
  const result = new Array(n).fill(0);
  const stack: number[] = []; // indices of days waiting for a warmer day

  for (let i = 0; i < n; i++) {
    while (stack.length > 0 && temperatures[stack[stack.length - 1]] < temperatures[i]) {
      const prevDay = stack.pop()!;
      result[prevDay] = i - prevDay; // days until warmer
    }
    stack.push(i);
  }

  return result;
}

// Example
console.log(dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]));
// [1, 1, 4, 2, 1, 1, 0, 0]
```

### Example 2: Largest Rectangle in Histogram (LeetCode 84)

```typescript
function largestRectangleArea(heights: number[]): number {
  const stack: number[] = []; // increasing stack of indices
  let maxArea = 0;

  for (let i = 0; i <= heights.length; i++) {
    // Sentinel value 0 at the end forces the stack to flush
    const h = i < heights.length ? heights[i] : 0;

    while (stack.length > 0 && heights[stack[stack.length - 1]] > h) {
      const height = heights[stack.pop()!];
      // Width = distance to the new stack top (left boundary) or 0 (no left boundary)
      const width = stack.length === 0 ? i : i - stack[stack.length - 1] - 1;
      maxArea = Math.max(maxArea, height * width);
    }

    stack.push(i);
  }

  return maxArea;
}

// Example
console.log(largestRectangleArea([2, 1, 5, 6, 2, 3]));
// 10 (the rectangle of height 5 spanning [2,5] = 5*2)
```

### Example 3: Trapping Rain Water II — 2D version uses heap, but 1D uses stack

```typescript
function trap1D(height: number[]): number {
  const stack: number[] = [];
  let totalWater = 0;
  let i = 0;

  while (i < height.length) {
    while (stack.length > 0 && height[stack[stack.length - 1]] < height[i]) {
      const bottom = stack.pop()!;
      if (stack.length === 0) break;
      const left = stack[stack.length - 1];
      const width = i - left - 1;
      const boundedHeight = Math.min(height[left], height[i]) - height[bottom];
      totalWater += width * boundedHeight;
    }
    stack.push(i);
    i++;
  }

  return totalWater;
}

console.log(trap1D([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]));
// 6
```

### Example 4: Next Greater Element in Circular Array (LeetCode 503)

```typescript
function nextGreaterElementsCircular(nums: number[]): number[] {
  const n = nums.length;
  const result = new Array(n).fill(-1);
  const stack: number[] = [];

  // Traverse twice to handle circular wrap-around
  for (let i = 0; i < 2 * n; i++) {
    const idx = i % n;

    while (stack.length > 0 && nums[stack[stack.length - 1]] < nums[idx]) {
      const prevIdx = stack.pop()!;
      result[prevIdx] = nums[idx];
    }

    // Only push the first n indices (avoid double-pushing)
    if (i < n) stack.push(idx);
  }

  return result;
}

console.log(nextGreaterElementsCircular([1, 2, 1]));
// [2, -1, 2]
```

## Common Mistakes

### 1. Forgetting the Sentinel Value (Histogram Variant)

```typescript
// ❌ BAD: stack never flushes for ascending heights
for (let i = 0; i < heights.length; i++) {
  while (stack.length > 0 && heights[stack[stack.length - 1]] > heights[i]) {
    // pop and compute
  }
  stack.push(i);
}

// ✅ GOOD: add sentinel (i = heights.length, height = 0) to flush
for (let i = 0; i <= heights.length; i++) {
  const h = i < heights.length ? heights[i] : 0;
  // ...
}
```

### 2. Wrong Stack Direction

```typescript
// ❌ BAD: using increasing stack for "next greater" (wrong direction)
while (stack.length > 0 && stack[stack.length - 1] > current) { ... }

// ✅ GOOD: use DECREASING stack for "next greater" (pop when top is smaller)
while (stack.length > 0 && stack[stack.length - 1] < current) { ... }
```

### 3. Confusing Strict vs. Non-Strict Inequality

```typescript
// For "next greater or equal" — use <= to pop on equal
while (stack.length > 0 && stack[stack.length - 1] <= current) { ... }

// For "strictly next greater" — use < to keep equal
while (stack.length > 0 && stack[stack.length - 1] < current) { ... }
```

### 4. Pushing Duplicate Values

```typescript
// For "unique next greater" — fine to push duplicates
// For "next greater with distinct elements" — track unique values

// Generally, push INDICES not values — the index is unique
```

## Time/Space Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Next greater/smaller element | O(n) | O(n) |
| Largest rectangle in histogram | O(n) | O(n) |
| Trapping rain water (1D) | O(n) | O(n) |
| Stock span | O(n) | O(n) |
| Next greater in circular array | O(n) | O(n) |

The amortized O(n) bound comes from the fact that each element is pushed exactly once and popped at most once across the entire traversal.

## Interview Problems

### Easy

1. **Next Greater Element I** (LeetCode 496) — basic pattern
2. **Daily Temperatures** (LeetCode 739) — classic "next greater with distance"
3. **Next Greater Element in Circular Array** (LeetCode 503) — circular wrap variant
4. **Asteroid Collision** (LeetCode 735) — uses stack with conditional pops
5. **Remove All Adjacent Duplicates in String II** (LeetCode 1209) — count-based stack

### Medium

1. **Largest Rectangle in Histogram** (LeetCode 84) — the canonical problem
2. **Trapping Rain Water** (LeetCode 42) — 1D stack solution
3. **Online Stock Span** (LeetCode 901) — next greater on the left
4. **Sum of Subarray Minimums** (LeetCode 907) — count contributions per element
5. **Maximum Width Ramp** (LeetCode 962) — decreasing stack
6. **Remove K Digits** (LeetCode 402) — monotonic stack with deletion budget

### Hard

1. **Maximum Rectangle in Binary Matrix** (LeetCode 85) — applies histogram to each row
2. **Trapping Rain Water II** (LeetCode 407) — 2D variant uses min-heap, not stack
3. **Longest Valid Parentheses** (LeetCode 32) — uses stack with index tracking
4. **Basic Calculator** (LeetCode 224) — stack of operators and operands
5. **Shortest Subarray with Sum at Least K** (LeetCode 862) — monotonic deque

## Summary

- Monotonic stack solves **"next greater/smaller"** problems in **O(n) total** by maintaining elements in sorted order
- Two flavors: **decreasing stack** for next greater; **increasing stack** for next smaller
- Each element is pushed once and popped at most once → amortized O(1) per element
- Canonical problems: **Daily Temperatures, Largest Rectangle in Histogram, Trapping Rain Water, Next Greater Element**
- For circular array: traverse **2n times** with `i % n`, only push the first n indices
- For histogram: use **sentinel value 0** at the end to force the stack to flush
- Senior signal: recognize the "next greater" signature in 30 seconds, code the stack in 5 minutes
- **Avoid**: wrong direction (increasing vs. decreasing), strict vs. non-strict inequality, missing sentinel for histogram

---

## See Also
- [Backtracking](05-Backtracking.md)
- [Coding Patterns](../19-Coding-Patterns/)
- [DFS & BFS](04-DFS-BFS.md)
- [Dynamic Programming](06-Dynamic-Programming.md)
- [Heap](07-Heap.md)
- [Sliding Window](01-Sliding-Window.md)
- [Stack & Queue Patterns](18-Stack-Queue-Patterns.md)
- [Two Pointers](02-Two-Pointers.md)

## References & Learn More

- [Monotonic Stack — LeetCode Explore Card](https://leetcode.com/explore/learn/card/queue-stack/230/usage-of-stack/)
- [Largest Rectangle in Histogram — LeetCode 84](https://leetcode.com/problems/largest-rectangle-in-histogram/)
- [Next Greater Element I — LeetCode 496](https://leetcode.com/problems/next-greater-element-i/)
- [Daily Temperatures — LeetCode 739](https://leetcode.com/problems/daily-temperatures/)
- [NeetCode Monotonic Stack Roadmap](https://neetcode.io/roadmap)
