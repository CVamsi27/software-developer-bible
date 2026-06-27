# Heap

## Definition

A heap is a specialized tree-based data structure that satisfies the heap property: in a max-heap, for any given node, its value is greater than or equal to the values of its children; in a min-heap, its value is less than or equal to its children. It's commonly used to implement priority queues.

## When to Use

- Finding the Kth largest/smallest element
- Finding the median of a stream
- Task scheduling with priorities
- Merge K sorted lists/arrays
- Top K frequent elements
- Any problem requiring efficient access to min/max

## Template

```typescript
// Min-Heap implementation
class MinHeap {
  private heap: number[] = [];

  push(val: number): void {
    this.heap.push(val);
    this.bubbleUp(this.heap.length - 1);
  }

  pop(): number {
    const min = this.heap[0];
    const last = this.heap.pop()!;
    if (this.heap.length > 0) {
      this.heap[0] = last;
      this.bubbleDown(0);
    }
    return min;
  }

  private bubbleUp(idx: number): void {
    while (idx > 0) {
      const parent = Math.floor((idx - 1) / 2);
      if (this.heap[parent] <= this.heap[idx]) break;
      [this.heap[parent], this.heap[idx]] = [this.heap[idx], this.heap[parent]];
      idx = parent;
    }
  }

  private bubbleDown(idx: number): void {
    while (true) {
      let smallest = idx;
      const left = 2 * idx + 1;
      const right = 2 * idx + 2;

      if (left < this.heap.length && this.heap[left] < this.heap[smallest]) {
        smallest = left;
      }
      if (right < this.heap.length && this.heap[right] < this.heap[smallest]) {
        smallest = right;
      }

      if (smallest === idx) break;

      [this.heap[idx], this.heap[smallest]] = [this.heap[smallest], this.heap[idx]];
      idx = smallest;
    }
  }

  peek(): number {
    return this.heap[0];
  }

  size(): number {
    return this.heap.length;
  }
}
```

## How It Works

```
Min-Heap:
        1
       / \
      3   2
     / \ / \
    7  4 5  6

Parent is always smaller than children.
Complete binary tree stored in array:
Index: 0  1  2  3  4  5  6
Value: 1  3  2  7  4  5  6

Max-Heap:
        7
       / \
      5   6
     / \ / \
    3  4 1  2

Parent is always larger than children.
```

### ASCII Diagram

```
MIN-HEAP (Priority Queue)
┌─────────────────────────────────────────┐
│              1 (min)                    │
│             / \                         │
│            3   2                        │
│           / \ / \                       │
│          7  4 5  6                      │
└─────────────────────────────────────────┘

Array representation: [1, 3, 2, 7, 4, 5, 6]

Push operation (add 0):
        1
       / \
      3   2         →    0
     / \ / \           / \
    7  4 5  6         1   2
                     / \ / \
                    7  4 5  6

Pop operation (remove 1):
        1              6 (last element)
       / \            / \
      3   2    →     3   2
     / \ / \        / \ / \
    7  4 5  6      7  4 5

Then bubble down 6:
        2
       / \
      3   6
     / \ / \
    7  4 5
```

## Code Examples (TypeScript)

### Problem 1: Kth Largest Element in a Stream

```typescript
class KthLargest {
  private minHeap: MinHeap;
  private k: number;

  constructor(k: number, nums: number[]) {
    this.k = k;
    this.minHeap = new MinHeap();

    for (const num of nums) {
      this.add(num);
    }
  }

  add(val: number): number {
    if (this.minHeap.size() < this.k) {
      this.minHeap.push(val);
    } else if (val > this.minHeap.peek()) {
      this.minHeap.pop();
      this.minHeap.push(val);
    }

    return this.minHeap.peek();
  }
}

// Example
const kthLargest = new KthLargest(3, [4, 5, 8, 2]);
console.log(kthLargest.add(3)); // 4
console.log(kthLargest.add(5)); // 5
console.log(kthLargest.add(10)); // 5
console.log(kthLargest.add(9)); // 8
```

### Problem 2: Find Median from Data Stream

```typescript
class MedianFinder {
  private maxHeap: number[]; // left half (smaller numbers)
  private minHeap: number[]; // right half (larger numbers)

  constructor() {
    this.maxHeap = []; // max-heap (negate values)
    this.minHeap = []; // min-heap
  }

  addNum(num: number): void {
    // Add to max-heap (negate for max behavior)
    this.maxHeap.push(-num);
    this.bubbleUpMax(this.maxHeap.length - 1);

    // Balance: move max from left to right
    this.minHeap.push(-this.maxHeap[0]);
    this.bubbleUpMin(this.minHeap.length - 1);
    this.popMax();

    // If right has more, move min back to left
    if (this.minHeap.length > this.maxHeap.length) {
      this.maxHeap.push(-this.minHeap[0]);
      this.bubbleUpMax(this.maxHeap.length - 1);
      this.popMin();
    }
  }

  findMedian(): number {
    if (this.maxHeap.length > this.minHeap.length) {
      return -this.maxHeap[0];
    }
    return (-this.maxHeap[0] + this.minHeap[0]) / 2;
  }

  // Helper methods for heap operations
  private bubbleUpMax(idx: number): void {
    while (idx > 0) {
      const parent = Math.floor((idx - 1) / 2);
      if (this.maxHeap[parent] >= this.maxHeap[idx]) break;
      [this.maxHeap[parent], this.maxHeap[idx]] = [this.maxHeap[idx], this.maxHeap[parent]];
      idx = parent;
    }
  }

  private bubbleUpMin(idx: number): void {
    while (idx > 0) {
      const parent = Math.floor((idx - 1) / 2);
      if (this.minHeap[parent] <= this.minHeap[idx]) break;
      [this.minHeap[parent], this.minHeap[idx]] = [this.minHeap[idx], this.minHeap[parent]];
      idx = parent;
    }
  }

  private popMax(): void {
    const max = this.maxHeap[0];
    const last = this.maxHeap.pop()!;
    if (this.maxHeap.length > 0) {
      this.maxHeap[0] = last;
      this.bubbleDownMax(0);
    }
  }

  private popMin(): void {
    const min = this.minHeap[0];
    const last = this.minHeap.pop()!;
    if (this.minHeap.length > 0) {
      this.minHeap[0] = last;
      this.bubbleDownMin(0);
    }
  }

  private bubbleDownMax(idx: number): void {
    while (true) {
      let largest = idx;
      const left = 2 * idx + 1;
      const right = 2 * idx + 2;

      if (left < this.maxHeap.length && this.maxHeap[left] > this.maxHeap[largest]) {
        largest = left;
      }
      if (right < this.maxHeap.length && this.maxHeap[right] > this.maxHeap[largest]) {
        largest = right;
      }

      if (largest === idx) break;

      [this.maxHeap[idx], this.maxHeap[largest]] = [this.maxHeap[largest], this.maxHeap[idx]];
      idx = largest;
    }
  }

  private bubbleDownMin(idx: number): void {
    while (true) {
      let smallest = idx;
      const left = 2 * idx + 1;
      const right = 2 * idx + 2;

      if (left < this.minHeap.length && this.minHeap[left] < this.minHeap[smallest]) {
        smallest = left;
      }
      if (right < this.minHeap.length && this.minHeap[right] < this.minHeap[smallest]) {
        smallest = right;
      }

      if (smallest === idx) break;

      [this.minHeap[idx], this.minHeap[smallest]] = [this.minHeap[smallest], this.minHeap[idx]];
      idx = smallest;
    }
  }
}

// Example
const medianFinder = new MedianFinder();
medianFinder.addNum(1);
medianFinder.addNum(2);
console.log(medianFinder.findMedian()); // 1.5
medianFinder.addNum(3);
console.log(medianFinder.findMedian()); // 2
```

### Problem 3: Top K Frequent Elements

```typescript
function topKFrequent(nums: number[], k: number): number[] {
  const freq = new Map<number, number>();
  for (const num of nums) {
    freq.set(num, (freq.get(num) || 0) + 1);
  }

  // Min-heap of size k
  const heap: [number, number][] = []; // [num, frequency]

  for (const [num, count] of freq) {
    if (heap.length < k) {
      heap.push([num, count]);
      heap.sort((a, b) => a[1] - b[1]);
    } else if (count > heap[0][1]) {
      heap[0] = [num, count];
      heap.sort((a, b) => a[1] - b[1]);
    }
  }

  return heap.map(([num]) => num);
}

// Example
console.log(topKFrequent([1, 1, 1, 2, 2, 3], 2)); // [1, 2]
console.log(topKFrequent([1], 1)); // [1]
```

### Problem 4: Merge K Sorted Lists

```typescript
class ListNode {
  val: number;
  next: ListNode | null;
  constructor(val?: number, next?: ListNode | null) {
    this.val = val ?? 0;
    this.next = next ?? null;
  }
}

function mergeKLists(lists: (ListNode | null)[]): ListNode | null {
  const heap: ListNode[] = [];

  for (const node of lists) {
    if (node) {
      heap.push(node);
      heap.sort((a, b) => a.val - b.val);
    }
  }

  const dummy = new ListNode();
  let current = dummy;

  while (heap.length > 0) {
    const node = heap.shift()!;
    current.next = node;
    current = current.next;

    if (node.next) {
      heap.push(node.next);
      heap.sort((a, b) => a.val - b.val);
    }
  }

  return dummy.next;
}
```

### Problem 5: Task Scheduler

```typescript
function leastInterval(tasks: string[], n: number): number {
  const freq = new Map<string, number>();
  for (const task of tasks) {
    freq.set(task, (freq.get(task) || 0) + 1);
  }

  // Max-heap of frequencies
  const heap = Array.from(freq.values()).sort((a, b) => b - a);

  let time = 0;

  while (heap.length > 0) {
    let i = 0;
    const temp: number[] = [];

    while (i <= n && heap.length > 0) {
      const freq = heap.shift()!;
      if (freq > 1) {
        temp.push(freq - 1);
      }
      time++;
      i++;
    }

    // Add back remaining tasks
    for (const f of temp) {
      heap.push(f);
    }
    heap.sort((a, b) => b - a);

    // If there are still tasks, add idle time
    if (heap.length > 0) {
      time += n - i + 1;
    }
  }

  return time;
}

// Example
console.log(leastInterval(["A","A","A","B","B","B"], 2)); // 8
```

## Common Mistakes

1. **Wrong heap property**: Max-heap vs min-heap, negate values for max behavior
2. **Not maintaining heap after operations**: Always bubble up/down after push/pop
3. **Using wrong comparison**: For max-heap in JS, negate values or use custom comparator
4. **Not handling edge cases**: Empty heap, single element, all same values
5. **Forgetting to sort after batch operations**: Heap property must be maintained

## Time/Space Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Insert | O(log n) | O(1) |
| Delete | O(log n) | O(1) |
| Peek | O(1) | O(1) |
| Build Heap | O(n) | O(n) |
| Heap Sort | O(n log n) | O(1) |

## Interview Problems

### Easy

1. **Kth Largest Element in a Stream** (LeetCode 703)
2. **Last Stone Weight** (LeetCode 1046)

### Medium

1. **Top K Frequent Elements** (LeetCode 347)
2. **Task Scheduler** (LeetCode 621)
3. **Reorganize String** (LeetCode 767)
4. **Kth Smallest Element in a Sorted Matrix** (LeetCode 378)
5. **Find K Pairs with Smallest Sums** (LeetCode 373)

### Hard

1. **Find Median from Data Stream** (LeetCode 295)
2. **Merge K Sorted Lists** (LeetCode 23)
3. **Smallest Range Covering Elements from K Lists** (LeetCode 632)
4. **IPO** (LeetCode 502)

## Summary

Heaps are essential for problems requiring efficient access to minimum or maximum elements. They're commonly used for top K problems, merging sorted data, and scheduling.

## Cheat Sheet

```
Pattern: Heap / Priority Queue
Use when: Top K, median, merge sorted, scheduling
Time: O(log n) insert/delete | O(1) peek

Min-Heap:
┌─────────────────────────────────────────┐
│ - Parent ≤ Children                     │
│ - Root is minimum                       │
│ - Use for: "find kth smallest"          │
└─────────────────────────────────────────┘

Max-Heap:
┌─────────────────────────────────────────┐
│ - Parent ≥ Children                     │
│ - Root is maximum                       │
│ - Use for: "find kth largest"           │
│ - In JS: negate values                  │
└─────────────────────────────────────────┘

Key operations:
- push(val): O(log n)
- pop(): O(log n)
- peek(): O(1)

When to use heap:
- Need min/max frequently
- Top K elements
- Merge K sorted streams
- Median finding
```

---

## References & Learn More
- [LeetCode Heap](https://leetcode.com/tag/heap/)
- [NeetCode Heap](https://neetcode.io/)
- [CP-Algorithms](https://cp-algorithms.com/)
- [Algorithm Design by Kleinberg & Tardos](https://www.amazon.com/Algorithm-Design-Kleinberg-Jon/dp/0321295358)
- [GeeksforGeeks Heap](https://www.geeksforgeeks.org/heap-data-structure/)
