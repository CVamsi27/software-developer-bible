---
section: Coding Patterns
category: Interview
tags: [concept, practice]
---

# Bit Manipulation

## Definition

**Bit manipulation** uses **bitwise operators** (`&`, `|`, `^`, `~`, `<<`, `>>`) to operate on the binary representation of integers. It can turn O(n) or O(n²) problems into O(1) or O(n) by exploiting properties of bits: every integer is a 32-bit (or 64-bit) vector, and you can pack, mask, count, and shift bits in constant time. Common techniques: bitmasks (represent sets as integers), bit counting (Hamming weight / popcount), and bitwise tricks (XOR for finding uniques, AND for masking).

## TL;DR

Bit manipulation is a **constant-time toolkit** for problems involving small finite sets, parity, uniqueness, and binary encoding. A 32-bit integer can represent a set of up to 32 elements; an `int` is a bitmask. The 5 must-know operators: `&` (AND — mask), `|` (OR — set bits), `^` (XOR — toggle / find unique), `~` (NOT — flip all bits), `<<` / `>>` (shift — multiply/divide by 2). The 3 must-know tricks: **XOR of a number with itself = 0**, **XOR of a number with 0 = itself**, and **`n & (n-1)` removes the lowest set bit** (used in popcount, finding power of 2).

## Why it matters

Bit manipulation appears in **~5-10% of interview questions** and is the senior-signal pattern for **low-level optimization, embedded systems, and competitive programming**. Interviewers test the **"find the unique number"** problem (XOR all elements, duplicates cancel), **bit counting** (popcount, number of 1 bits), **subsets via bitmask** (enumerate 2^n subsets of n elements), and **single-number problems**. The senior signal: knowing when bit packing saves space (e.g., permission flags as a single int), when to use **`n & (n-1)`** for O(1) bit-counting, and **avoiding signed-shift bugs** in languages where `>>` is arithmetic vs. logical shift.

## When to Use

- **"Find the unique element"**: XOR all elements; duplicates cancel, unique remains
- **"Count set bits" / Hamming weight**: Brian Kernighan's algorithm `n & (n-1)` runs in O(popcount)
- **"Power of 2 check"**: `n & (n-1) == 0` and `n > 0`
- **"Generate all subsets"**: iterate 0 to 2^n - 1, use bitmask to pick elements
- **"Permission flags / set operations"**: store as int, use bitwise ops for union/intersection
- **"Reverse bits"**: bit-shift + mask
- **Pattern signature**: small finite set, binary decisions, or "find what's different" / "find what's missing" problems

## Template

```typescript
// ==================== Bit Building Blocks ====================

// Check if bit i is set
function isSet(num: number, i: number): boolean {
  return (num & (1 << i)) !== 0;
}

// Set bit i
function setBit(num: number, i: number): number {
  return num | (1 << i);
}

// Clear bit i
function clearBit(num: number, i: number): number {
  return num & ~(1 << i);
}

// Toggle bit i
function toggleBit(num: number, i: number): number {
  return num ^ (1 << i);
}

// Count set bits — Brian Kernighan's algorithm
function popcount(n: number): number {
  let count = 0;
  while (n !== 0) {
    n &= n - 1; // remove lowest set bit
    count++;
  }
  return count;
}

// Check if n is a power of 2
function isPowerOfTwo(n: number): boolean {
  return n > 0 && (n & (n - 1)) === 0;
}

// ==================== Common Patterns ====================

// Find the unique number (others appear twice) — XOR
function findUnique(nums: number[]): number {
  return nums.reduce((acc, n) => acc ^ n, 0);
}

// Find two unique numbers (others appear twice)
function findTwoUniques(nums: number[]): [number, number] {
  let xor = 0;
  for (const n of nums) xor ^= n;          // XOR of all = a ^ b (a, b are uniques)
  const rightmostSetBit = xor & -xor;       // isolate lowest set bit
  let a = 0, b = 0;
  for (const n of nums) {
    if ((n & rightmostSetBit) === 0) a ^= n; // group 1
    else b ^= n;                              // group 2
  }
  return [a, b];
}

// Generate all subsets via bitmask
function subsets<T>(nums: T[]): T[][] {
  const result: T[][] = [];
  const n = nums.length;
  for (let mask = 0; mask < (1 << n); mask++) {
    const subset: T[] = [];
    for (let i = 0; i < n; i++) {
      if ((mask & (1 << i)) !== 0) subset.push(nums[i]);
    }
    result.push(subset);
  }
  return result;
}
```

## How It Works

### XOR Properties (Foundation)

```text
XOR (^) returns 1 if bits differ, 0 if same

a ^ a = 0       (a number XOR itself is 0)
a ^ 0 = a       (a number XOR 0 is itself)
a ^ b = b ^ a   (commutative)
a ^ (b ^ c) = (a ^ b) ^ c   (associative)

APPLICATION: "Find the unique number" in [2, 3, 5, 3, 2]
  0 ^ 2 = 2
  2 ^ 3 = 1
  1 ^ 5 = 4
  4 ^ 3 = 7
  7 ^ 2 = 5  ← unique!
```

### Brian Kernighan's Algorithm (Count Set Bits)

```text
n = 12 = 1100

n & (n-1):
  1100 & 1011 = 1000  (lowest set bit cleared)
  1000 & 0111 = 0000  (lowest set bit cleared)

Each iteration removes the lowest set bit → runs in O(popcount) time.
For 32-bit ints: at most 32 iterations.
```

### Bitmask as a Set

```text
Set {a, c} of {a, b, c, d}  →  bitmask 0101
  bit 0 (a) = 1
  bit 1 (b) = 0
  bit 2 (c) = 1
  bit 3 (d) = 0

Union:  0101 | 0011 = 0111
Intersect: 0101 & 0011 = 0001
Difference: 0101 & ~0011 = 0100
Toggle: 0101 ^ 0010 = 0111
```

## Code Examples (TypeScript)

### Example 1: Single Number (LeetCode 136)

```typescript
function singleNumber(nums: number[]): number {
  return nums.reduce((acc, n) => acc ^ n, 0);
}

console.log(singleNumber([4, 1, 2, 1, 2])); // 4
```

### Example 2: Number of 1 Bits / Hamming Weight (LeetCode 191)

```typescript
function hammingWeight(n: number): number {
  let count = 0;
  while (n !== 0) {
    n &= n - 1; // remove lowest set bit
    count++;
  }
  return count;
}

console.log(hammingWeight(0b1011)); // 3 (binary 1011 has three 1s)
```

### Example 3: Subsets (LeetCode 78) — Bitmask Enumeration

```typescript
function subsets(nums: number[]): number[][] {
  const result: number[][] = [];
  const n = nums.length;
  for (let mask = 0; mask < (1 << n); mask++) {
    const subset: number[] = [];
    for (let i = 0; i < n; i++) {
      if ((mask & (1 << i)) !== 0) {
        subset.push(nums[i]);
      }
    }
    result.push(subset);
  }
  return result;
}

console.log(subsets([1, 2, 3]));
// [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]
```

### Example 4: Reverse Bits (LeetCode 190)

```typescript
function reverseBits(n: number): number {
  let result = 0;
  for (let i = 0; i < 32; i++) {
    result = (result << 1) | (n & 1); // shift result left, add current LSB
    n >>>= 1; // unsigned right shift
  }
  return result >>> 0; // force unsigned 32-bit
}

console.log(reverseBits(0b00000010100101000001111010011100));
// 964176192 (binary: 00111001011110000010100101000000)
```

### Example 5: Power of Two (LeetCode 231)

```typescript
function isPowerOfTwo(n: number): boolean {
  // Powers of 2 have exactly one bit set; n-1 flips that bit and sets all lower bits
  // e.g., 8 = 1000, 7 = 0111 → 1000 & 0111 = 0
  return n > 0 && (n & (n - 1)) === 0;
}
```

### Example 6: Missing Number (LeetCode 268) — XOR Trick

```typescript
function missingNumber(nums: number[]): number {
  // XOR of [0..n] XOR XOR of nums = missing number
  // (because all values present in both cancel out)
  const n = nums.length;
  let xor = n;
  for (let i = 0; i < n; i++) {
    xor ^= i ^ nums[i];
  }
  return xor;
}

console.log(missingNumber([3, 0, 1])); // 2
console.log(missingNumber([0, 1, 2, 3, 4, 5, 6, 7, 9])); // 8
```

### Example 7: Permission System with Bitmasks

```typescript
// Permissions as bit flags
const Permission = {
  READ:    1 << 0,  // 0b0001
  WRITE:   1 << 1,  // 0b0010
  DELETE:  1 << 2,  // 0b0100
  ADMIN:   1 << 3,  // 0b1000
} as const;

class User {
  private perms: number = 0;

  grant(perm: number): void { this.perms |= perm; }
  revoke(perm: number): void { this.perms &= ~perm; }
  has(perm: number): boolean { return (this.perms & perm) === perm; }
  hasAny(perms: number): boolean { return (this.perms & perms) !== 0; }
  hasAll(perms: number): boolean { return (this.perms & perms) === perms; }
}

const alice = new User();
alice.grant(Permission.READ | Permission.WRITE);

console.log(alice.has(Permission.READ));        // true
console.log(alice.has(Permission.DELETE));     // false
console.log(alice.hasAll(Permission.READ | Permission.WRITE)); // true
```

## Common Mistakes

### 1. Signed vs. Unsigned Right Shift

```typescript
// ❌ BAD: `>>` is arithmetic shift (preserves sign bit) in JS/Java
let x = -1;
x >> 1;  // -1 (sign bit propagated)

// ✅ GOOD: `>>>` is unsigned right shift (fills with 0)
let x = -1;
x >>> 1; // 2147483647 (MAX_INT for 32-bit)

// Use >>> for bit manipulation in JS to avoid sign bugs
```

### 2. Operator Precedence

```typescript
// ❌ BAD: `&` has lower precedence than `==`
if (n & 1 == 1) { } // evaluates as (n & (1 == 1)) = n & 1 — confusing

// ✅ GOOD: use parentheses
if ((n & 1) === 1) { }
```

### 3. Off-By-One in Bit Position

```typescript
// ❌ BAD: confusing bit position 0 vs. "bit 1"
const LSB = 1 << 0; // bit 0 (the rightmost bit)

// ✅ GOOD: use clear names
const FLAG_ENABLED = 1 << 0;  // bit 0
const FLAG_VISIBLE = 1 << 1;  // bit 1
```

### 4. JS Number Precision (32-bit Limitation)

```typescript
// ❌ BAD: shifting by 32+ bits in JS is `% 32`
1 << 32; // 1 (not 2^32) — JS treats shift amount modulo 32

// ✅ GOOD: use BigInt for > 32-bit, or accept the 32-bit limit
// For typical interview problems (int32), no issue
```

## Time/Space Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Bit count (Brian Kernighan) | O(popcount) ≤ O(32) | O(1) |
| Check / set / clear / toggle bit | O(1) | O(1) |
| Find unique (XOR) | O(n) | O(1) |
| Generate all subsets (bitmask) | O(n × 2^n) | O(n × 2^n) |
| Reverse bits | O(32) | O(1) |
| Permission system | O(1) per op | O(1) |

## Interview Problems

### Easy

1. **Single Number** (LeetCode 136) — XOR of duplicates cancels
2. **Number of 1 Bits** (LeetCode 191) — Brian Kernighan
3. **Reverse Bits** (LeetCode 190) — shift and mask
4. **Power of Two** (LeetCode 231) — `n & (n-1) == 0`
5. **Missing Number** (LeetCode 268) — XOR or sum formula
6. **Hamming Distance** (LeetCode 461) — XOR then popcount
7. **Sum of Two Integers** (LeetCode 371) — full adder in bitwise

### Medium

1. **Single Number II** (LeetCode 137) — every other appears 3 times
2. **Single Number III** (LeetCode 260) — two unique numbers
3. **Subsets** (LeetCode 78) — bitmask enumeration
4. **Bitwise AND of Numbers Range** (LeetCode 201) — find common prefix
5. **Maximum Product of Word Lengths** (LeetCode 318) — bitmask for character sets
6. **Counting Bits** (LeetCode 338) — DP + bit trick
7. **Find the Difference** (LeetCode 389) — XOR trick
8. **UTF-8 Validation** (LeetCode 393) — bit-level parsing

### Hard

1. **Minimum Number of K Consecutive Bit Flips** (LeetCode 995) — sliding window + bit flip
2. **Maximum XOR With an Element From Array** (LeetCode 1707) — bit trie
3. **Find K-th Smallest Pair Distance** (LeetCode 719) — binary search + bit
4. **Shortest Path to Get All Keys** (LeetCode 864) — bitmask BFS
5. **Maximum Score Words Formed by Letters** (LeetCode 1255) — bitmask DP

## Summary

- Bit manipulation uses **bitwise operators** to operate on integers as binary vectors
- 5 must-know operators: `&` (mask), `|` (set), `^` (XOR/toggle), `~` (NOT), `<<` `>>` `>>>` (shift)
- 3 must-know XOR properties: `a ^ a = 0`, `a ^ 0 = a`, XOR is commutative and associative
- **Brian Kernighan** `n & (n-1)` removes the lowest set bit → O(popcount) bit counting
- Bitmask as a set: 32-bit int = 32-element set with O(1) union/intersection/toggle
- Senior signal: choose bitmasks for permission systems, use XOR for "find the unique", recognize bit-counting opportunities
- **Watch out for**: signed vs. unsigned shift (`>>` vs. `>>>`), operator precedence, JS 32-bit limit
- Canonical problems: **Single Number, Number of 1 Bits, Subsets, Reverse Bits, Power of Two, Missing Number**

---

## See Also
- [Coding Patterns](../19-Coding-Patterns/)
- [Dynamic Programming](06-Dynamic-Programming.md)
- [Heap](07-Heap.md)
- [Monotonic Stack](13-Monotonic-Stack.md)
- [Trie](08-Trie.md)
- [Two Pointers](02-Two-Pointers.md)

## References & Learn More

- [Bit Manipulation — LeetCode Explore Card](https://leetcode.com/explore/learn/card/bit-manipulation/)
- [Bit Hacks — Stanford Bit Twiddling Hacks](https://graphics.stanford.edu/~seander/bithacks.html)
- [Brian Kernighan's Algorithm](https://leetcode.com/problems/number-of-1-bits/solution/)
- [Single Number — LeetCode 136](https://leetcode.com/problems/single-number/)
- [Bitmask DP — AtCoder](https://atcoder.jp/contests/dp/tasks)
