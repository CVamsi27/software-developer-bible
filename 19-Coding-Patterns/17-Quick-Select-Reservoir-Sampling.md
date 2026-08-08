---
section: Coding Patterns
category: Interview
tags: [concept, practice]
---

# Quick Select & Reservoir Sampling

## Definition

**Quick Select** is a selection algorithm that finds the **k-th smallest (or largest) element** in an unordered array in **average O(n)**, **worst-case O(n²)** time. It's derived from QuickSort's partition step: instead of recursing into both halves, it recurses only into the half that contains the k-th element.

**Reservoir Sampling** is a family of randomized algorithms for selecting a **uniform random sample of k items from a stream of unknown size n** in **O(n) time and O(k) space**. The classic algorithm (Algorithm R, by Jeffrey Vitter) maintains a reservoir of size k; each new item replaces a random reservoir element with probability k/i (where i is the item's 1-based position in the stream).

## TL;DR

**Quick Select** finds the k-th smallest in O(n) average by partitioning around a pivot and recursing into one side. **Reservoir Sampling** picks k uniform-random items from a stream of unknown size in O(n) time using O(k) space. Quick Select is the right tool when you need the k-th element of an **array in memory**; Reservoir Sampling is the right tool when you need k items from a **stream you can't rewind** (e.g., database cursor, log file, Kafka topic).

## Why it matters

Both patterns appear in **~3-5% of FAANG interviews** and are senior-signal patterns for **streaming/online algorithms** and **selection problems**. Quick Select is the canonical solution to **Kth Largest in Array** and **Top K Frequent Elements** (when paired with a count map). Reservoir Sampling solves **"pick a random sample from a Kafka log"**, **"uniform random shuffle of a linked list"**, and **"random sampling from a database with unknown row count"**. The senior signal: knowing Quick Select's worst-case (O(n²) on already-sorted input — fix with median-of-medians or randomized pivot) and the **math behind reservoir sampling's uniformity guarantee**.

## When to Use

### Quick Select

- **"Find the k-th smallest/largest element"** in an unsorted array
- **"Top K elements"** when paired with a hashmap (count + sort) — but Quick Select avoids the sort
- **"Find the median"** of a stream (online selection)
- **Pattern signature**: array, unsorted, need k-th or median

### Reservoir Sampling

- **"Pick k random elements from a stream of unknown size"**
- **"Shuffle a linked list"** (Fisher-Yates with reservoir)
- **"Random sample from a database cursor"**
- **"Reservoir sampling with weights"** (weighted reservoir, A-Res)
- **Pattern signature**: streaming, can't rewind, need uniform random sample

## Template

```typescript
// ==================== Quick Select ====================
function quickSelect(nums: number[], k: number): number {
  // k is 1-based: 1 = smallest, n = largest
  return quickSelectHelper(nums, 0, nums.length - 1, k);
}

function quickSelectHelper(nums: number[], left: number, right: number, k: number): number {
  if (left === right) return nums[left];

  const pivotIndex = partition(nums, left, right);

  // The pivot is at position pivotIndex in the sorted order
  // How many elements are to the left of the pivot? pivotIndex - left
  if (k - 1 < pivotIndex - left) {
    return quickSelectHelper(nums, left, pivotIndex - 1, k);
  } else if (k - 1 > pivotIndex - left) {
    return quickSelectHelper(nums, pivotIndex + 1, right, k - (pivotIndex - left + 1));
  } else {
    return nums[pivotIndex];
  }
}

function partition(nums: number[], left: number, right: number): number {
  // Randomized pivot to avoid worst case
  const randomIdx = left + Math.floor(Math.random() * (right - left + 1));
  [nums[randomIdx], nums[right]] = [nums[right], nums[randomIdx]];

  const pivot = nums[right];
  let i = left;
  for (let j = left; j < right; j++) {
    if (nums[j] < pivot) {
      [nums[i], nums[j]] = [nums[j], nums[i]];
      i++;
    }
  }
  [nums[i], nums[right]] = [nums[right], nums[i]];
  return i;
}

// ==================== Reservoir Sampling (Algorithm R) ====================
function reservoirSample<T>(stream: Iterable<T>, k: number): T[] {
  const reservoir: T[] = [];
  let i = 0;

  for (const item of stream) {
    if (i < k) {
      reservoir.push(item); // fill the reservoir
    } else {
      // Replace a random element with probability k/(i+1)
      const j = Math.floor(Math.random() * (i + 1));
      if (j < k) {
        reservoir[j] = item;
      }
    }
    i++;
  }

  return reservoir;
}

// ==================== Fisher-Yates Shuffle ====================
function shuffle<T>(arr: T[]): T[] {
  const result = [...arr];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}
```

## How It Works

### Quick Select Walk-Through

```text
Find the 3rd smallest in [3, 2, 1, 5, 4]
k=3

Step 1: pivot=4 (rightmost after randomization), partition:
  [3, 2, 1] | 4 | [5]
   < 4      pivot  > 4
  pivotIndex = 3 (0-based)
  3 elements to the left of pivot. k-1 = 2. 2 < 3? YES → recurse left [3, 2, 1]

Step 2: pivot=1, partition:
  [] | 1 | [3, 2]
  pivotIndex = 0
  0 elements to the left. k-1 = 2. 2 > 0? YES → recurse right [3, 2], k=2 (1-based "2nd smallest in [3,2]")

Step 3: pivot=2, partition:
  [] | 2 | [3]
  pivotIndex = 1
  1 element to the left. k-1 = 1. 1 == 1? YES → return pivot = 2

Answer: 2 (the 3rd smallest of [3, 2, 1, 5, 4] is 2, the sorted array is [1, 2, 3, 4, 5])
```

### Reservoir Sampling Math

```text
Goal: Pick k items from a stream of size n, each subset of size k equally likely.

Algorithm R:
  Fill reservoir with first k items
  For each i = k+1 to n:
    Pick random j in [0, i-1]
    If j < k, replace reservoir[j] with item[i]

Probability analysis (for any specific item m, m > k):
  P(item m is in reservoir) = P(m selected at step m) × P(not replaced in m+1..n)
                            = (k/m) × ((1 - 1/m) × (1 - 1/(m+1)) × ... × (1 - 1/n))
                            = (k/m) × (m/n)
                            = k/n

All items have probability k/n of being in the final reservoir → uniform random sample.
```

## Code Examples (TypeScript)

### Example 1: Kth Largest Element in an Array (LeetCode 215)

```typescript
function findKthLargest(nums: number[], k: number): number {
  // We want the (n - k)th smallest
  return quickSelect(nums, nums.length - k + 1);
}

console.log(findKthLargest([3, 2, 1, 5, 6, 4], 2)); // 5
```

### Example 2: Top K Frequent Elements (LeetCode 347) — Quick Select Variant

```typescript
function topKFrequent(nums: number[], k: number): number[] {
  const count = new Map<number, number>();
  for (const n of nums) count.set(n, (count.get(n) || 0) + 1);

  // Unique values, each with its count
  const unique = [...count.keys()];

  // Quick select by count (descending)
  return quickSelectByCount(unique, count, k);
}

function quickSelectByCount(
  unique: number[],
  count: Map<number, number>,
  k: number
): number[] {
  return quickSelectHelperCount(unique, count, 0, unique.length - 1, k);
}

function quickSelectHelperCount(
  unique: number[],
  count: Map<number, number>,
  left: number,
  right: number,
  k: number
): number[] {
  if (left > right) return [];
  if (left === right) return [unique.slice(left, left + Math.min(k, right - left + 1))].flat();

  const pivot = count.get(unique[right])!;
  let i = left;
  for (let j = left; j < right; j++) {
    if (count.get(unique[j])! >= pivot) { // descending
      [unique[i], unique[j]] = [unique[j], unique[i]];
      i++;
    }
  }
  [unique[i], unique[right]] = [unique[right], unique[i]];

  const leftCount = i - left; // number of elements with count >= pivot
  if (leftCount === k) return unique.slice(left, i);
  if (leftCount > k) return quickSelectHelperCount(unique, count, left, i - 1, k);
  return [
    ...unique.slice(left, i),
    ...quickSelectHelperCount(unique, count, i + 1, right, k - leftCount),
  ];
}

console.log(topKFrequent([1, 1, 1, 2, 2, 3], 2)); // [1, 2]
```

### Example 3: Reservoir Sampling from a Stream

```typescript
class StreamSampler<T> {
  private reservoir: T[];
  private k: number;
  private count: number = 0;

  constructor(k: number) {
    this.k = k;
    this.reservoir = [];
  }

  add(item: T): void {
    if (this.count < this.k) {
      this.reservoir.push(item);
    } else {
      const j = Math.floor(Math.random() * (this.count + 1));
      if (j < this.k) {
        this.reservoir[j] = item;
      }
    }
    this.count++;
  }

  getSample(): T[] {
    return [...this.reservoir];
  }
}

// Simulate streaming 1M numbers, sample 100 uniform-random
const sampler = new StreamSampler<number>(100);
for (let i = 0; i < 1_000_000; i++) {
  sampler.add(i);
}
console.log(sampler.getSample().length); // 100
console.log(sampler.getSample().slice(0, 5)); // e.g., [423801, 12734, ...]
```

### Example 4: Shuffle a Linked List (LeetCode 382)

```typescript
class ListNode {
  val: number;
  next: ListNode | null;
  constructor(val: number, next: ListNode | null = null) {
    this.val = val;
    this.next = next;
  }
}

function shuffleLinkedList(head: ListNode | null): ListNode | null {
  if (!head) return null;
  const arr: ListNode[] = [];
  let curr: ListNode | null = head;
  while (curr) {
    arr.push(curr);
    curr = curr.next;
  }
  // Fisher-Yates shuffle
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  // Re-link
  for (let i = 0; i < arr.length - 1; i++) {
    arr[i].next = arr[i + 1];
  }
  arr[arr.length - 1].next = null;
  return arr[0];
}
```

### Example 5: Random Pick Index (LeetCode 398) — Reservoir with k=1

```typescript
class Solution {
  private nums: number[];

  constructor(nums: number[]) {
    this.nums = nums;
  }

  pick(target: number): number {
    let count = 0;
    let result = -1;
    for (let i = 0; i < this.nums.length; i++) {
      if (this.nums[i] === target) {
        count++;
        // Reservoir with k=1: pick with probability 1/count
        if (Math.floor(Math.random() * count) === 0) {
          result = i;
        }
      }
    }
    return result;
  }
}
```

## Common Mistakes

### 1. Quick Select Worst-Case (Already-Sorted Input)

```typescript
// ❌ BAD: pivot = rightmost (or leftmost) → O(n²) on sorted input
function partition(nums, left, right) {
  const pivot = nums[right]; // deterministic — worst case
  // ...
}

// ✅ GOOD: randomize the pivot
function partition(nums, left, right) {
  const randomIdx = left + Math.floor(Math.random() * (right - left + 1));
  [nums[randomIdx], nums[right]] = [nums[right], nums[randomIdx]];
  const pivot = nums[right];
  // ...
}
```

### 2. Quick Select Off-By-One (1-based vs 0-based k)

```typescript
// ❌ BAD: confusing k=0 (smallest) vs. k=1 (1st smallest)
if (k < pivotIndex) { /* ... */ }

// ✅ GOOD: explicit 1-based k
if (k - 1 < pivotIndex - left) { /* k-th element is in the left side */ }
```

### 3. Reservoir Sampling Off-By-One

```typescript
// ❌ BAD: probability should be k/(i+1), not k/i
const j = Math.floor(Math.random() * (i)); // missing +1
if (j < k) reservoir[j] = item;

// ✅ GOOD: i is 0-based item index, probability is k/(i+1)
const j = Math.floor(Math.random() * (i + 1));
if (j < k) reservoir[j] = item;
```

### 4. Using Sort Instead of Quick Select

```typescript
// ❌ BAD: O(n log n) when O(n) is available
function kthLargest(nums, k) {
  return nums.sort((a, b) => b - a)[k - 1];
}

// ✅ GOOD: Quick Select for average O(n)
function kthLargest(nums, k) {
  return quickSelect(nums, nums.length - k + 1);
}
```

## Time/Space Complexity

### Quick Select

| Case | Time | Space |
|------|------|-------|
| Best (median pivot) | O(n) | O(log n) recursion |
| Average (random pivot) | O(n) | O(log n) recursion |
| Worst (deterministic pivot on sorted) | O(n²) | O(n) recursion stack |

**With median-of-medians** pivot selection: guaranteed O(n) worst case, but constant factor is high (rare in practice).

### Reservoir Sampling

| Algorithm | Time | Space | Notes |
|-----------|------|-------|-------|
| Algorithm R (uniform) | O(n) | O(k) | Most common |
| Algorithm A (optimized skips) | O(n + k log k) | O(k) | For sparse samples |
| Weighted reservoir (A-Res) | O(n log W) | O(k) | When items have weights |

## Interview Problems

### Quick Select

#### Easy

1. **Kth Largest Element in an Array** (LeetCode 215) — classic
2. **Kth Smallest Element in a Sorted Matrix** (LeetCode 378) — binary search variant

#### Medium

1. **Top K Frequent Elements** (LeetCode 347) — Quick Select on counts
2. **Sort an Array** (LeetCode 912) — use QuickSort (related pattern)
3. **Kth Largest Element in a Stream** (LeetCode 703) — heap or partial sort

#### Hard

1. **Wiggle Sort II** (LeetCode 324) — Quick Select + 3-way partition
2. **Kth Smallest Number in Multiplication Table** (LeetCode 668) — binary search

### Reservoir Sampling

#### Easy

1. **Random Pick Index** (LeetCode 398) — reservoir with k=1
2. **Linked List Random Node** (LeetCode 382) — reservoir or Fisher-Yates

#### Medium

1. **Random Pick with Weight** (LeetCode 528) — prefix-sum + binary search
2. **Random Flip Matrix** (LeetCode 519) — reservoir with shrinking range
3. **Shuffle an Array** (LeetCode 384) — Fisher-Yates

#### Hard

1. **Random Point in Non-Overlapping Rectangles** (LeetCode 497) — prefix-sum + binary search
2. **Implement Rand10() Using Rand7()** (LeetCode 470) — rejection sampling
3. **Sample With Size** (related, weighted reservoir)

## Summary

### Quick Select

- Quick Select finds the **k-th smallest in average O(n)** by partitioning around a pivot and recursing into one side
- **Randomized pivot** avoids the O(n²) worst case on sorted/almost-sorted input
- Use it for: k-th largest, top K frequent, median of a stream
- **Not stable** (doesn't preserve order of equal elements)
- Worst case: O(n²); average: O(n); space: O(log n) recursion stack

### Reservoir Sampling

- Reservoir sampling picks **k uniform-random items from a stream** in **O(n) time, O(k) space**
- Each new item replaces a random reservoir element with probability **k/(i+1)**
- Use it for: streaming data, log sampling, shuffling a linked list, random pick from a database cursor
- **Algorithm R** is the canonical version; **Algorithm A** optimizes for sparse samples
- **Weighted reservoir** (A-Res) extends to items with non-uniform weights

### Combined Senior Signal

- Recognize **k-th element in an array** → Quick Select (not full sort)
- Recognize **k random from a stream** → Reservoir Sampling (not collect-all-then-sample)
- Know the **mathematical guarantees** (Quick Select's O(n) average, Reservoir's uniform distribution)
- **Watch out for**: Quick Select's O(n²) on sorted input (randomize!), Reservoir's off-by-one probability (k/(i+1) not k/i)

---

## See Also
- [Binary Search](03-Binary-Search.md)
- [Coding Patterns](../19-Coding-Patterns/)
- [Dynamic Programming](06-Dynamic-Programming.md)
- [Heap](07-Heap.md)
- [Monotonic Stack](13-Monotonic-Stack.md)
- [String Search — KMP & Rabin-Karp](16-String-Search-KMP-Rabin-Karp.md)

## References & Learn More

- [Quick Select — CP Algorithms](https://cp-algorithms.com/sequences/k-th.html)
- [Quick Select — Wikipedia](https://en.wikipedia.org/wiki/Quickselect)
- [Reservoir Sampling — Wikipedia](https://en.wikipedia.org/wiki/Reservoir_sampling)
- [Kth Largest Element — LeetCode 215](https://leetcode.com/problems/kth-largest-element-in-an-array/)
- [Random Pick Index — LeetCode 398](https://leetcode.com/problems/random-pick-index/)
- [Vitter's Reservoir Sampling — Original Paper](https://www.cs.umd.edu/~samir/498/vitter.pdf)
