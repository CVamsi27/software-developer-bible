---
section: Coding Patterns
category: Interview
tags: [concept, practice]
---

# Segment Tree & Binary Indexed Tree (BIT)

## Definition

A **Segment Tree** is a binary tree that stores information about **array intervals (segments)** at each node. It supports **range queries** (sum, min, max, gcd) and **point/range updates** in **O(log n)** time. Each node represents an interval `[l, r]`; the root represents `[0, n-1]`, the leaves represent single elements, and each internal node represents the union of its children.

A **Binary Indexed Tree (BIT / Fenwick Tree)** is a simpler data structure that supports **prefix sum queries** and **point updates** in O(log n), using only O(n) space. It's the right tool when you need sum queries (not arbitrary range queries) and the array is static or has point updates.

## TL;DR

Segment trees and BITs solve "**dynamic range query + update**" problems: as elements change, you can answer "what's the sum/min/max in indices [l, r]?" in O(log n) per query. Segment tree is the **general-purpose** tool (any associative function, range updates via lazy propagation); BIT is the **lightweight** tool (sum only, point updates). For senior interviews, the key is recognizing when the problem is a range query, choosing the right tool, and knowing the O(log n) construction.

## Why it matters

Segment trees appear in **~5% of hard interview problems** and are common in **competitive programming**-style questions. The senior-level question: **lazy propagation** (defer range updates to children until needed — turns O(n log n) into O(log n) for range updates), **building in O(n)** instead of O(n log n) (post-order construction from leaves up), and **choosing segment tree vs. BIT** (BIT is simpler if you only need sums; segment tree handles min/max/gcd/range updates). Production: range-aggregation dashboards, sliding-window analytics over streaming data, and 2D variants for image processing.

## When to Use

- **"Range sum query with point updates"**: BIT is the simplest solution
- **"Range min/max/gcd with point updates"**: segment tree
- **"Range sum/min/max with range updates"**: segment tree with **lazy propagation**
- **"Count elements less than X in a range"**: merge-sort tree (segment tree of sorted vectors) or BIT
- **Pattern signature**: input is an array that changes over time (or you process queries offline); queries are about a contiguous range; brute force per query is O(n) but you need O(log n) per query

## Template

```typescript
// Generic Segment Tree with point update + range query
class SegmentTree {
  private n: number;
  private tree: number[];
  private merge: (a: number, b: number) => number;
  private identity: number;

  constructor(arr: number[], merge: (a: number, b: number) => number, identity: number) {
    this.n = arr.length;
    this.merge = merge;
    this.identity = identity;
    this.tree = new Array(4 * this.n).fill(identity);
    if (this.n > 0) this.build(arr, 0, 0, this.n - 1);
  }

  private build(arr: number[], node: number, l: number, r: number): void {
    if (l === r) {
      this.tree[node] = arr[l];
      return;
    }
    const mid = Math.floor((l + r) / 2);
    this.build(arr, 2 * node + 1, l, mid);
    this.build(arr, 2 * node + 2, mid + 1, r);
    this.tree[node] = this.merge(this.tree[2 * node + 1], this.tree[2 * node + 2]);
  }

  update(index: number, value: number): void {
    this.updateHelper(0, 0, this.n - 1, index, value);
  }

  private updateHelper(node: number, l: number, r: number, index: number, value: number): void {
    if (l === r) {
      this.tree[node] = value;
      return;
    }
    const mid = Math.floor((l + r) / 2);
    if (index <= mid) {
      this.updateHelper(2 * node + 1, l, mid, index, value);
    } else {
      this.updateHelper(2 * node + 2, mid + 1, r, index, value);
    }
    this.tree[node] = this.merge(this.tree[2 * node + 1], this.tree[2 * node + 2]);
  }

  query(left: number, right: number): number {
    return this.queryHelper(0, 0, this.n - 1, left, right);
  }

  private queryHelper(node: number, l: number, r: number, left: number, right: number): number {
    if (right < l || r < left) return this.identity;          // no overlap
    if (left <= l && r <= right) return this.tree[node];      // full overlap
    const mid = Math.floor((l + r) / 2);
    const leftRes = this.queryHelper(2 * node + 1, l, mid, left, right);
    const rightRes = this.queryHelper(2 * node + 2, mid + 1, r, left, right);
    return this.merge(leftRes, rightRes);
  }
}

// Binary Indexed Tree (Fenwick) for range sum
class BIT {
  private n: number;
  private tree: number[];

  constructor(n: number) {
    this.n = n;
    this.tree = new Array(n + 1).fill(0);
  }

  update(index: number, delta: number): void {
    for (let i = index + 1; i <= this.n; i += i & -i) {
      this.tree[i] += delta;
    }
  }

  query(index: number): number { // prefix sum [0, index]
    let sum = 0;
    for (let i = index + 1; i > 0; i -= i & -i) {
      sum += this.tree[i];
    }
    return sum;
  }

  rangeQuery(left: number, right: number): number {
    return this.query(right) - (left > 0 ? this.query(left - 1) : 0);
  }
}
```

## How It Works

### Segment Tree Layout

```text
Array: [1, 3, 5, 7, 9, 11]
                    Range [0, 5] sum=36
                   /                       \
            [0, 2] sum=9              [3, 5] sum=27
            /       \                  /        \
        [0,1]=4  [2,1]=5          [3,4]=16  [5,1]=11
        /    \                   /     \
    [0,1]=1 [1,1]=3          [3,1]=7  [4,1]=9

Each internal node = merge of its children
Query [1, 4] = ?
  - [0, 2] intersects → recurse left → [0,1] ∩ → [1,1] full → 3
  - [2, 2] full → 5
  - [3, 5] intersects → recurse right → [3, 4] full → 16
  - sum = 3 + 5 + 16 = 24 ✓
```

### Binary Indexed Tree (BIT)

```text
tree[i] stores the sum of a specific "responsibility range" based on i's lowest set bit

index (1-based) | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8
LSB             | 1  | 2  | 1  | 4  | 1  | 2  | 1  | 8
range           |[1] |[1,2]|[3] |[1,4]|[5] |[5,6]|[7] |[1,8]

Update index 3: add to tree[3], tree[4], tree[8]
Query prefix 5:  sum tree[5] + tree[4] + tree[0]  =  a[5] + (a[1]+a[2]+a[3]+a[4])
```

## Code Examples (TypeScript)

### Example 1: Range Sum Query — Mutable (LeetCode 307) with BIT

```typescript
class NumArray {
  private bit: BIT;

  constructor(nums: number[]) {
    this.bit = new BIT(nums.length);
    for (let i = 0; i < nums.length; i++) {
      this.bit.update(i, nums[i]);
    }
  }

  update(index: number, val: number): void {
    // Need delta — assume we have access to original array
    // (simplified: caller passes delta, not new value)
    this.bit.update(index, val);
  }

  sumRange(left: number, right: number): number {
    return this.bit.rangeQuery(left, right);
  }
}
```

### Example 2: Range Min Query — Segment Tree

```typescript
function rangeMin(nums: number[], queries: Array<[number, number]>): number[] {
  const segTree = new SegmentTree(nums, Math.min, Infinity);
  return queries.map(([l, r]) => segTree.query(l, r));
}

console.log(rangeMin([1, 3, -1, 7, 2], [[0, 2], [1, 4]])); // [-1, -1]
```

### Example 3: Lazy Propagation — Range Add + Range Sum

```typescript
class LazySegmentTree {
  private n: number;
  private tree: number[];      // segment tree
  private lazy: number[];      // pending lazy updates

  constructor(arr: number[]) {
    this.n = arr.length;
    this.tree = new Array(4 * this.n).fill(0);
    this.lazy = new Array(4 * this.n).fill(0);
    this.build(arr, 0, 0, this.n - 1);
  }

  // Range add: add `val` to every element in [l, r]
  rangeAdd(l: number, r: number, val: number): void {
    this.rangeAddHelper(0, 0, this.n - 1, l, r, val);
  }

  // Range sum query
  rangeSum(l: number, r: number): number {
    return this.rangeSumHelper(0, 0, this.n - 1, l, r);
  }

  private build(arr: number[], node: number, l: number, r: number): void {
    if (l === r) {
      this.tree[node] = arr[l];
      return;
    }
    const mid = (l + r) >> 1;
    this.build(arr, 2 * node + 1, l, mid);
    this.build(arr, 2 * node + 2, mid + 1, r);
    this.tree[node] = this.tree[2 * node + 1] + this.tree[2 * node + 2];
  }

  private pushDown(node: number, l: number, r: number): void {
    if (this.lazy[node] !== 0) {
      const mid = (l + r) >> 1;
      this.lazy[2 * node + 1] += this.lazy[node];
      this.lazy[2 * node + 2] += this.lazy[node];
      this.tree[2 * node + 1] += this.lazy[node] * (mid - l + 1);
      this.tree[2 * node + 2] += this.lazy[node] * (r - mid);
      this.lazy[node] = 0;
    }
  }

  private rangeAddHelper(node: number, l: number, r: number, ql: number, qr: number, val: number): void {
    if (qr < l || r < ql) return;
    if (ql <= l && r <= qr) {
      this.tree[node] += val * (r - l + 1);
      this.lazy[node] += val;
      return;
    }
    this.pushDown(node, l, r);
    const mid = (l + r) >> 1;
    this.rangeAddHelper(2 * node + 1, l, mid, ql, qr, val);
    this.rangeAddHelper(2 * node + 2, mid + 1, r, ql, qr, val);
    this.tree[node] = this.tree[2 * node + 1] + this.tree[2 * node + 2];
  }

  private rangeSumHelper(node: number, l: number, r: number, ql: number, qr: number): number {
    if (qr < l || r < ql) return 0;
    if (ql <= l && r <= qr) return this.tree[node];
    this.pushDown(node, l, r);
    const mid = (l + r) >> 1;
    return this.rangeSumHelper(2 * node + 1, l, mid, ql, qr) +
           this.rangeSumHelper(2 * node + 2, mid + 1, r, ql, qr);
  }
}
```

### Example 4: Count of Smaller Numbers After Self (LeetCode 315) — BIT

```typescript
function countSmaller(nums: number[]): number[] {
  // Coordinate compression: map values to 1..n
  const sorted = [...new Set(nums)].sort((a, b) => a - b);
  const ranks = new Map<number, number>();
  sorted.forEach((v, i) => ranks.set(v, i + 1));

  const bit = new BIT(sorted.length);
  const result: number[] = [];

  // Iterate right to left; query how many smaller-or-equal values we've seen
  for (let i = nums.length - 1; i >= 0; i--) {
    const rank = ranks.get(nums[i])!;
    result.unshift(bit.query(rank - 1)); // count of values with rank < current
    bit.update(rank, 1);
  }

  return result;
}

console.log(countSmaller([5, 2, 6, 1]));
// [2, 1, 1, 0]
```

## Common Mistakes

### 1. Building in O(n log n) Instead of O(n)

```typescript
// ❌ BAD: O(n log n) — point-update for each element
constructor(arr: number[]) {
  this.tree = new Array(4 * arr.length).fill(0);
  for (let i = 0; i < arr.length; i++) {
    this.update(i, arr[i]); // O(log n) per update
  }
}

// ✅ GOOD: O(n) — single recursive build
constructor(arr: number[]) {
  this.tree = new Array(4 * arr.length).fill(0);
  this.build(arr, 0, 0, arr.length - 1); // O(n) post-order
}
```

### 2. Forgetting Lazy Propagation

```typescript
// ❌ BAD: range update is O(n) without lazy propagation
rangeAdd(l, r, val) {
  for (let i = l; i <= r; i++) this.update(i, val); // O(n log n)!
}

// ✅ GOOD: lazy propagation makes range update O(log n)
rangeAdd(l, r, val) {
  this.rangeAddHelper(0, 0, this.n - 1, l, r, val);
}
```

### 3. Wrong Tree Size

```typescript
// ❌ BAD: tree size is n (too small)
// A segment tree can have up to 4n nodes in the worst case (sparse)

// ✅ GOOD: always use 4n
this.tree = new Array(4 * n).fill(0);
```

### 4. BIT Off-By-One (1-based vs 0-based)

```typescript
// ❌ Confusing 0-based and 1-based indices
// BIT internally is 1-based; queries use index+1, updates use index+1

// ✅ Use a wrapper class to hide the conversion
class BIT {
  update(index, delta) {
    for (let i = index + 1; i <= this.n; i += i & -i) { ... }
  }
}
```

## Time/Space Complexity

| Operation | Segment Tree | BIT | Naive |
|-----------|--------------|-----|-------|
| Build | O(n) | O(n) | O(n) |
| Point update | O(log n) | O(log n) | O(1) |
| Range query | O(log n) | O(log n) | O(n) |
| Range update (lazy) | O(log n) | O(n log n) | O(n) |
| Space | O(4n) | O(n) | O(1) |

## Interview Problems

### Easy

1. **Range Sum Query — Immutable** (LeetCode 303) — prefix sum
2. **Range Sum Query — Mutable** (LeetCode 307) — BIT or segment tree
3. **Count of Smaller Numbers After Self** (LeetCode 315) — BIT with coordinate compression

### Medium

1. **Range Sum Query 2D — Mutable** (LeetCode 308) — 2D BIT
2. **My Calendar I** (LeetCode 729) — sweep line or segment tree
3. **Longest Increasing Subsequence** (LeetCode 300) — can be solved with BIT (O(n log n))
4. **Queue Reconstruction by Height** (LeetCode 406) — BIT for efficient insertion
5. **Range Module** (LeetCode 715) — segment tree with lazy propagation

### Hard

1. **The Skyline Problem** (LeetCode 218) — sweep line + priority queue
2. **Falling Squares** (LeetCode 699) — segment tree with lazy
3. **Count of Range Sum** (LeetCode 327) — BIT + coordinate compression
4. **My Calendar III** (LeetCode 732) — segment tree with delta propagation
5. **Reverse Pairs** (LeetCode 493) — BIT or merge sort

## Summary

- Segment trees and BITs solve **dynamic range query + update** in **O(log n)** per operation
- **BIT (Fenwick)**: simpler, less code, prefix sums only, point updates
- **Segment tree**: general-purpose, any associative merge, range updates via lazy propagation
- Build in **O(n)** with post-order recursion (not O(n log n) point updates)
- **Lazy propagation**: defer range updates to children → O(log n) instead of O(n)
- Tree size: always **4n** (worst case for sparse)
- Coordinate compression: map large values to 1..k for BIT
- Senior signal: recognize the "dynamic range query" signature; choose BIT vs. segment tree; code lazy propagation correctly
- Production: range-aggregation dashboards, sliding-window analytics, 2D image processing

---

## See Also
- [Binary Search](03-Binary-Search.md)
- [Coding Patterns](../19-Coding-Patterns/)
- [DFS & BFS](04-DFS-BFS.md)
- [Dynamic Programming](06-Dynamic-Programming.md)
- [Heap](07-Heap.md)
- [Monotonic Stack](13-Monotonic-Stack.md)

## References & Learn More

- [Segment Tree — CP Algorithms](https://cp-algorithms.com/data_structures/segment_tree.html)
- [Binary Indexed Tree — TopCoder](https://www.topcoder.com/thrive/articles/Binary%20Indexed%20Trees)
- [Lazy Propagation — CP Algorithms](https://cp-algorithms.com/data_structures/segment_tree.html#lazy-propagation)
- [Range Sum Query — Mutable (LeetCode 307)](https://leetcode.com/problems/range-sum-query-mutable/)
- [AtCoder Library — segtree](https://github.com/atcoder/ac-library)
