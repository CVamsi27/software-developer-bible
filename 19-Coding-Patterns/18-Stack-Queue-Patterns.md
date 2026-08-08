---
section: Coding Patterns
category: Interview
tags: [concept, practice]
---

# Stack & Queue Patterns

## Definition

**Stacks** (LIFO) and **queues** (FIFO) are the simplest non-trivial data structures, but they power a surprising number of interview problems. Beyond basic push/pop, the senior-level interview pattern is to use a stack or queue to **maintain state** (next greater, balanced brackets, sliding-window max) or to **simulate a process** (BFS traversal, task scheduling, rate limiting). Common variants:

- **Monotonic stack/deque**: maintain elements in sorted order — covered in [Monotonic Stack](13-Monotonic-Stack.md)
- **Two-stack queue**: implement a queue using two stacks (O(1) amortized)
- **Sliding window with deque**: maintain max/min over a window in O(n)
- **BFS with queue**: shortest path in unweighted graphs

## TL;DR

Stacks are for **recursion simulation, undo, and LIFO patterns**: balanced brackets, expression evaluation, DFS iterative, next greater element, valid parentheses. Queues are for **BFS, scheduling, and FIFO patterns**: level-order traversal, sliding window max, producer-consumer, rate limiting. **Deques** (double-ended queue) extend queues to support O(1) push/pop from both ends — the right tool for sliding-window max problems. The senior signal: knowing which LIFO/FIFO problem maps to which structure, and using the right data structure to keep operations O(1) or O(log n).

## Why it matters

Stacks and queues appear in **~15-20% of interview questions** (often as the underlying data structure, not the stated problem). The senior-level question: **choosing the right data structure** for state maintenance (stack for LIFO, queue for FIFO, deque for both), **simulating recursion with a stack** (iterative DFS to avoid stack overflow on deep trees), and **monotonic structures** for amortized O(n) solutions to "next greater" or "sliding-window max". Production: undo/redo in editors, BFS in graph databases, rate-limiters (token bucket with queue), and Kafka consumer groups (queue-based).

## When to Use

### Stack

- **Balanced brackets** (matching `()`, `[]`, `{}`): push opening, pop on closing
- **Expression evaluation** (infix → postfix, calculator): push operands and operators
- **Next greater/smaller element**: see [Monotonic Stack](13-Monotonic-Stack.md)
- **Iterative DFS**: simulate recursion with explicit stack (avoid stack overflow)
- **Undo/redo**: stack of operations
- **Function call stack**: implicit; sometimes you need to simulate it

### Queue (and Deque)

- **BFS** (shortest path, level-order): see [DFS & BFS](04-DFS-BFS.md)
- **Sliding window max/min**: monotonic deque
- **Producer-consumer**: queue between threads/processes
- **Rate limiting**: token bucket, leaky bucket
- **Task scheduling**: round-robin with queue
- **LRU cache**: hashmap + doubly-linked list (or queue of keys)

## Template

```typescript
// ==================== Stack Patterns ====================

// Balanced brackets
function isBalanced(s: string): boolean {
  const stack: string[] = [];
  const pairs: Record<string, string> = { ')': '(', ']': '[', '}': '{' };

  for (const c of s) {
    if (c in pairs) {
      if (stack.length === 0 || stack.pop() !== pairs[c]) return false;
    } else {
      stack.push(c);
    }
  }
  return stack.length === 0;
}

// Iterative DFS (avoid stack overflow on deep trees)
function dfsIterative(root: TreeNode | null): number[] {
  const result: number[] = [];
  if (!root) return result;

  const stack: TreeNode[] = [root];
  while (stack.length > 0) {
    const node = stack.pop()!;
    result.push(node.val);
    if (node.right) stack.push(node.right); // right first so left is processed first
    if (node.left) stack.push(node.left);
  }
  return result;
}

// ==================== Queue Patterns ====================

// BFS (level-order traversal)
function bfsLevelOrder(root: TreeNode | null): number[][] {
  const result: number[][] = [];
  if (!root) return result;

  const queue: TreeNode[] = [root];
  while (queue.length > 0) {
    const levelSize = queue.length;
    const level: number[] = [];
    for (let i = 0; i < levelSize; i++) {
      const node = queue.shift()!;
      level.push(node.val);
      if (node.left) queue.push(node.left);
      if (node.right) queue.push(node.right);
    }
    result.push(level);
  }
  return result;
}

// Sliding window maximum (monotonic deque) — LeetCode 239
function maxSlidingWindow(nums: number[], k: number): number[] {
  const result: number[] = [];
  const deque: number[] = []; // stores indices, decreasing values

  for (let i = 0; i < nums.length; i++) {
    // Remove indices outside the window
    while (deque.length > 0 && deque[0] <= i - k) deque.shift();

    // Remove indices whose values are smaller than current
    while (deque.length > 0 && nums[deque[deque.length - 1]] < nums[i]) {
      deque.pop();
    }

    deque.push(i);

    if (i >= k - 1) {
      result.push(nums[deque[0]]);
    }
  }

  return result;
}

// LRU Cache — hashmap + doubly-linked list
class LRUCache<K, V> {
  private capacity: number;
  private cache: Map<K, V>;

  constructor(capacity: number) {
    this.capacity = capacity;
    this.cache = new Map();
  }

  get(key: K): V | -1 {
    if (!this.cache.has(key)) return -1;
    const value = this.cache.get(key)!;
    // Move to end (most recently used)
    this.cache.delete(key);
    this.cache.set(key, value);
    return value;
  }

  put(key: K, value: V): void {
    if (this.cache.has(key)) this.cache.delete(key);
    else if (this.cache.size >= this.capacity) {
      // Evict the least recently used (first inserted)
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(key, value);
  }
}
```

## How It Works

### Monotonic Deque (Sliding Window Max)

```text
nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3

i=0, val=1:  deque=[0]                (values: [1])
i=1, val=3:  pop 0 (1<3), deque=[1]   (values: [3])
i=2, val=-1: deque=[1, 2]              (values: [3, -1])
             i >= k-1, push nums[deque[0]]=3 to result
i=3, val=-3: deque=[1, 2, 3]           (values: [3, -1, -3])
             shift if deque[0] <= 0 → 1>0, keep
             push nums[deque[0]]=3 to result
i=4, val=5:  pop 3 (-3<5), pop 2 (-1<5), pop 1 (3<5)
             deque=[4]                  (values: [5])
             push 5 to result
i=5, val=3:  deque=[4, 5]              (values: [5, 3])
             shift if deque[0] <= 2 → 4>2, keep
             push 5 to result
i=6, val=6:  pop 5 (3<6), pop 4 (5<6)
             deque=[6]                  (values: [6])
             push 6 to result
i=7, val=7:  pop 6 (6<7)
             deque=[7]                  (values: [7])
             push 7 to result

Result: [3, 3, 5, 5, 6, 7]
```

### LRU Cache Mechanism

```text
HashMap preserves insertion order in JS (and Java's LinkedHashMap)
So we can use Map as a combination of hashmap + insertion-order tracking

put(1, A): cache = {1: A}
put(2, B): cache = {1: A, 2: B}
put(3, C): cache = {1: A, 2: B, 3: C}
get(1):    move 1 to end → cache = {2: B, 3: C, 1: A}
put(4, D): evict LRU (2) → cache = {3: C, 1: A, 4: D}
```

## Code Examples (TypeScript)

### Example 1: Valid Parentheses (LeetCode 20) — Stack

```typescript
function isValid(s: string): boolean {
  const stack: string[] = [];
  const pairs: Record<string, string> = { ')': '(', ']': '[', '}': '{' };

  for (const c of s) {
    if (c in pairs) {
      if (stack.pop() !== pairs[c]) return false;
    } else {
      stack.push(c);
    }
  }
  return stack.length === 0;
}

console.log(isValid("()[]{}"));   // true
console.log(isValid("([)]"));     // false
```

### Example 2: Min Stack (LeetCode 155) — Auxiliary Stack

```typescript
class MinStack {
  private stack: number[] = [];
  private minStack: number[] = []; // parallel stack tracking current min

  push(val: number): void {
    this.stack.push(val);
    if (this.minStack.length === 0 || val <= this.minStack[this.minStack.length - 1]) {
      this.minStack.push(val);
    }
  }

  pop(): void {
    const popped = this.stack.pop()!;
    if (popped === this.minStack[this.minStack.length - 1]) {
      this.minStack.pop();
    }
  }

  top(): number { return this.stack[this.stack.length - 1]; }
  getMin(): number { return this.minStack[this.minStack.length - 1]; }
}
```

### Example 3: Evaluate Reverse Polish Notation (LeetCode 150) — Stack

```typescript
function evalRPN(tokens: string[]): number {
  const stack: number[] = [];
  const ops: Record<string, (a: number, b: number) => number> = {
    '+': (a, b) => a + b,
    '-': (a, b) => a - b,
    '*': (a, b) => a * b,
    '/': (a, b) => Math.trunc(a / b),
  };

  for (const token of tokens) {
    if (token in ops) {
      const b = stack.pop()!;
      const a = stack.pop()!;
      stack.push(ops[token](a, b));
    } else {
      stack.push(Number(token));
    }
  }

  return stack[0];
}

console.log(evalRPN(["2", "1", "+", "3", "*"])); // 9
console.log(evalRPN(["4", "13", "5", "/", "+"])); // 6
```

### Example 4: Sliding Window Maximum (LeetCode 239) — Monotonic Deque

```typescript
function maxSlidingWindow(nums: number[], k: number): number[] {
  const result: number[] = [];
  const deque: number[] = []; // indices, decreasing nums values

  for (let i = 0; i < nums.length; i++) {
    while (deque.length > 0 && deque[0] <= i - k) deque.shift();
    while (deque.length > 0 && nums[deque[deque.length - 1]] < nums[i]) deque.pop();
    deque.push(i);
    if (i >= k - 1) result.push(nums[deque[0]]);
  }

  return result;
}

console.log(maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3));
// [3, 3, 5, 5, 6, 7]
```

### Example 5: Design Circular Queue (LeetCode 622) — Array with Two Pointers

```typescript
class MyCircularQueue {
  private data: number[];
  private head: number = 0;
  private tail: number = 0;
  private size: number = 0;
  private capacity: number;

  constructor(k: number) {
    this.capacity = k;
    this.data = new Array(k);
  }

  enQueue(value: number): boolean {
    if (this.isFull()) return false;
    this.data[this.tail] = value;
    this.tail = (this.tail + 1) % this.capacity;
    this.size++;
    return true;
  }

  deQueue(): boolean {
    if (this.isEmpty()) return false;
    this.head = (this.head + 1) % this.capacity;
    this.size--;
    return true;
  }

  Front(): number {
    return this.isEmpty() ? -1 : this.data[this.head];
  }

  Rear(): number {
    return this.isEmpty() ? -1 : this.data[(this.tail - 1 + this.capacity) % this.capacity];
  }

  isEmpty(): boolean { return this.size === 0; }
  isFull(): boolean { return this.size === this.capacity; }
}
```

### Example 6: Implement Queue using Stacks (LeetCode 232)

```typescript
class MyQueue {
  private inStack: number[] = [];   // for enqueue
  private outStack: number[] = [];  // for dequeue/peek

  push(x: number): void {
    this.inStack.push(x);
  }

  pop(): number {
    this.peek();
    return this.outStack.pop()!;
  }

  peek(): number {
    if (this.outStack.length === 0) {
      while (this.inStack.length > 0) {
        this.outStack.push(this.inStack.pop()!);
      }
    }
    return this.outStack[this.outStack.length - 1];
  }

  empty(): boolean {
    return this.inStack.length === 0 && this.outStack.length === 0;
  }
}

// Amortized O(1) per operation: each element is moved at most twice
```

## Common Mistakes

### 1. Using Array.shift() in a Hot Loop (JS)

```typescript
// ❌ BAD: array.shift() is O(n) — kills performance for large queues
const queue: number[] = [1, 2, 3];
queue.shift(); // O(n) — re-indexes all elements

// ✅ GOOD: use a head pointer, or a proper deque
// For sliding window: use a monotonic deque with push/pop, never shift
```

### 2. Off-By-One in Circular Queue

```typescript
// ❌ BAD: confusing "tail points to next insertion" with "tail points to last element"
// Pick ONE convention and stick with it

// ✅ GOOD: tail points to the NEXT empty slot
// Front = data[head], Rear = data[(tail - 1 + capacity) % capacity]
```

### 3. Iterative DFS Without Tracking Visited

```typescript
// ❌ BAD: infinite loop on a graph with cycles
const stack = [startNode];
while (stack.length > 0) {
  const node = stack.pop()!;
  for (const neighbor of node.neighbors) {
    stack.push(neighbor); // cycles push the same node repeatedly
  }
}

// ✅ GOOD: track visited set
const visited = new Set();
while (stack.length > 0) {
  const node = stack.pop()!;
  if (visited.has(node)) continue;
  visited.add(node);
  for (const neighbor of node.neighbors) {
    if (!visited.has(neighbor)) stack.push(neighbor);
  }
}
```

### 4. Monotonic Deque Direction Confusion

```typescript
// ❌ BAD: deque stores values, but you need indices to track the window
const deque: number[] = []; // values

// ✅ GOOD: store INDICES, look up values
const deque: number[] = []; // indices
while (deque.length > 0 && nums[deque[deque.length - 1]] < nums[i]) {
  deque.pop();
}
```

## Time/Space Complexity

| Operation | Stack | Queue | Deque |
|-----------|-------|-------|-------|
| Push/Enqueue | O(1) | O(1) | O(1) |
| Pop/Dequeue | O(1) | O(1) | O(1) |
| Peek | O(1) | O(1) | O(1) |
| Search | O(n) | O(n) | O(n) |
| Build | O(n) | O(n) | O(n) |

| Pattern | Time | Space |
|---------|------|-------|
| Balanced brackets | O(n) | O(n) |
| Sliding window max/min | O(n) | O(k) |
| Min stack | O(1) per op | O(n) |
| BFS | O(V+E) | O(V) |
| Iterative DFS | O(V+E) | O(V) |
| LRU cache | O(1) per op | O(capacity) |

## Interview Problems

### Easy

1. **Valid Parentheses** (LeetCode 20) — basic stack
2. **Min Stack** (LeetCode 155) — auxiliary stack
3. **Implement Queue using Stacks** (LeetCode 232) — two-stack trick
4. **Implement Stack using Queues** (LeetCode 225) — single-queue or two-queue
5. **Design Circular Queue** (LeetCode 622) — array with two pointers

### Medium

1. **Evaluate Reverse Polish Notation** (LeetCode 150) — stack with operators
2. **Sliding Window Maximum** (LeetCode 239) — monotonic deque
3. **Daily Temperatures** (LeetCode 739) — monotonic stack
4. **LRU Cache** (LeetCode 146) — hashmap + linked list
5. **Binary Tree Level Order Traversal** (LeetCode 102) — BFS
6. **Decode String** (LeetCode 394) — stack with count + string
7. **Asteroid Collision** (LeetCode 735) — stack with conditional pops

### Hard

1. **Sliding Window Maximum** (advanced) — multi-array
2. **Maximal Rectangle** (LeetCode 85) — stack of heights
3. **Longest Valid Parentheses** (LeetCode 32) — stack with sentinel
4. **Basic Calculator** (LeetCode 224) — stack of operators
5. **LFU Cache** (LeetCode 460) — doubly-linked list + frequency map
6. **Shortest Subarray with Sum at Least K** (LeetCode 862) — monotonic deque

## Summary

- **Stack (LIFO)**: balanced brackets, expression evaluation, next greater element, undo/redo, iterative DFS
- **Queue (FIFO)**: BFS, level-order traversal, producer-consumer, rate limiting, task scheduling
- **Deque**: sliding window max/min (monotonic), BFS in 2D grids
- **LRU Cache**: hashmap + doubly-linked list (or `Map` in JS for insertion-order)
- **Senior signal**:
  - Use **monotonic structures** for amortized O(n) on "next greater" and "sliding window max"
  - Use **iterative DFS with explicit stack** to avoid stack overflow on deep trees
  - Use **two-pointer circular buffer** for fixed-size queues (no shift overhead)
  - Use **two-stack queue** when you can't use a native queue
- **Watch out for**: array.shift() in hot loops (O(n) in JS), visited-set on graphs with cycles, deque direction confusion
- Production: undo/redo, BFS in graph databases, rate limiters, Kafka consumer groups, LRU caches in DBs

---

## See Also
- [BFS & DFS](04-DFS-BFS.md)
- [Coding Patterns](../19-Coding-Patterns/)
- [Dynamic Programming](06-Dynamic-Programming.md)
- [Heap](07-Heap.md)
- [Monotonic Stack](13-Monotonic-Stack.md)
- [Sliding Window](01-Sliding-Window.md)

## References & Learn More

- [Stack — CP Algorithms](https://cp-algorithms.com/data_structures/stack.html)
- [Queue — CP Algorithms](https://cp-algorithms.com/data_structures/queue.html)
- [Sliding Window Maximum — LeetCode 239](https://leetcode.com/problems/sliding-window-maximum/)
- [LRU Cache — LeetCode 146](https://leetcode.com/problems/lru-cache/)
- [JavaScript Map insertion order](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map)
