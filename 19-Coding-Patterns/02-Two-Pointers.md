# Two Pointers

## Definition

Two pointers is a technique that uses two variables to iterate through a data structure, typically from different positions or at different speeds. It's used to solve problems involving pairs, comparisons, or when you need to examine relationships between elements at different positions.

## When to Use

- Finding pairs in a sorted array that sum to a target
- Comparing elements from both ends
- Detecting cycles in linked lists
- Problems requiring comparison of two sequences
- When brute force uses nested loops and can be optimized

## Template

```typescript
// Two pointers moving toward each other
function twoPointers(arr: number[]): number {
  let left = 0;
  let right = arr.length - 1;

  while (left < right) {
    const sum = arr[left] + arr[right];

    if (sum === target) {
      return [left, right];
    } else if (sum < target) {
      left++;
    } else {
      right--;
    }
  }

  return -1;
}
```

## How It Works

```text
Opposite Direction:
Sorted Array: [2, 7, 11, 15, 20], Target = 22

Step 1: [2, 7, 11, 15, 20]  sum = 2+20 = 22 ✓
         L                R

Step 2: (found at L=0, R=4)

Same Direction (Fast/Slow):
[1, 2, 3, 4, 5]
 S
 F

Step 1: S=0, F=0
Step 2: S=1, F=2
Step 3: S=2, F=4  (fast reaches end first)
```

### ASCII Diagram

```text
OPPOSITE DIRECTION (Two Sum II)
┌───┬───┬───┬───┬───┬───┐
│ 2 │ 7 │ 11│ 15│ 20│ 25│  sorted array
└───┴───┴───┴───┴───┴───┘
  ▲                   ▲
  L                   R  sum=27 > 22 → R--
     ▲               ▲
     L               R  sum=27 > 22 → R--
        ▲         ▲
        L         R  sum=22 ✓ found!

FAST/SLOW POINTER (Cycle Detection)
     ┌───┐
     │ 1 │──→┌───┐
     └───┘   │ 2 │
       ↑     └───┘
       │       │
       │     ┌─▼─┐
       │     │ 3 │
       │     └─┬─┘
       │       │
       │     ┌─▼─┐
       └─────│ 4 │
             └───┘

Slow moves 1 step, Fast moves 2 steps
They will meet at node 3 if cycle exists
```

## Code Examples (TypeScript)

### Problem 1: Two Sum II - Input Array is Sorted

```typescript
function twoSumSorted(numbers: number[], target: number): number[] {
  let left = 0;
  let right = numbers.length - 1;

  while (left < right) {
    const sum = numbers[left] + numbers[right];

    if (sum === target) {
      return [left + 1, right + 1]; // 1-indexed
    } else if (sum < target) {
      left++;
    } else {
      right--;
    }
  }

  return [-1, -1];
}

// Example
console.log(twoSumSorted([2, 7, 11, 15], 9)); // [1, 2]
```

### Problem 2: Container With Most Water

```typescript
function maxArea(height: number[]): number {
  let left = 0;
  let right = height.length - 1;
  let maxArea = 0;

  while (left < right) {
    const width = right - left;
    const h = Math.min(height[left], height[right]);
    const area = width * h;

    maxArea = Math.max(maxArea, area);

    // Move the pointer with smaller height
    if (height[left] < height[right]) {
      left++;
    } else {
      right--;
    }
  }

  return maxArea;
}

// Example
console.log(maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7])); // 49
// Container between index 1 (height 8) and index 8 (height 7)
```

### Problem 3: Trapping Rain Water

```typescript
function trap(height: number[]): number {
  if (height.length === 0) return 0;

  let left = 0;
  let right = height.length - 1;
  let leftMax = height[left];
  let rightMax = height[right];
  let water = 0;

  while (left < right) {
    if (leftMax < rightMax) {
      left++;
      leftMax = Math.max(leftMax, height[left]);
      water += leftMax - height[left];
    } else {
      right--;
      rightMax = Math.max(rightMax, height[right]);
      water += rightMax - height[right];
    }
  }

  return water;
}

// Example
console.log(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])); // 6
```

### Problem 4: Valid Palindrome

```typescript
function isPalindrome(s: string): boolean {
  const cleaned = s.toLowerCase().replace(/[^a-z0-9]/g, '');

  let left = 0;
  let right = cleaned.length - 1;

  while (left < right) {
    if (cleaned[left] !== cleaned[right]) {
      return false;
    }
    left++;
    right--;
  }

  return true;
}

// Example
console.log(isPalindrome("A man, a plan, a canal: Panama")); // true
```

### Problem 5: Linked List Cycle Detection (Fast/Slow)

```typescript
class ListNode {
  val: number;
  next: ListNode | null;
  constructor(val?: number, next?: ListNode | null) {
    this.val = val ?? 0;
    this.next = next ?? null;
  }
}

function hasCycle(head: ListNode | null): boolean {
  if (!head || !head.next) return false;

  let slow = head;
  let fast = head;

  while (fast && fast.next) {
    slow = slow.next!;
    fast = fast.next.next;

    if (slow === fast) {
      return true;
    }
  }

  return false;
}
```

### Problem 6: Three Sum

```typescript
function threeSum(nums: number[]): number[][] {
  nums.sort((a, b) => a - b);
  const result: number[][] = [];

  for (let i = 0; i < nums.length - 2; i++) {
    if (i > 0 && nums[i] === nums[i - 1]) continue; // skip duplicates

    let left = i + 1;
    let right = nums.length - 1;

    while (left < right) {
      const sum = nums[i] + nums[left] + nums[right];

      if (sum === 0) {
        result.push([nums[i], nums[left], nums[right]]);

        while (left < right && nums[left] === nums[left + 1]) left++;
        while (left < right && nums[right] === nums[right - 1]) right--;

        left++;
        right--;
      } else if (sum < 0) {
        left++;
      } else {
        right--;
      }
    }
  }

  return result;
}

// Example
console.log(threeSum([-1, 0, 1, 2, -1, -4]));
// [[-1, -1, 2], [-1, 0, 1]]
```

## Common Mistakes

1. **Forgetting to check boundaries**: Always verify `left < right` before accessing elements
2. **Not handling duplicates**: In problems requiring unique results, skip duplicate values
3. **Moving wrong pointer**: In container problems, always move the smaller height
4. **Off-by-one with indices**: Remember array indexing when returning results
5. **Not considering all cases**: Empty arrays, single element, all same values

## Time/Space Complexity

| Complexity | Opposite Direction | Same Direction |
|------------|-------------------|----------------|
| Time       | O(n)              | O(n)           |
| Space      | O(1)              | O(1)           |

- **Time O(n)**: Each pointer moves at most n times
- **Space O(1)**: Only using two pointers, no extra data structures

## Interview Problems

### Easy

1. **Valid Palindrome** (LeetCode 125)
2. **Merge Sorted Array** (LeetCode 88)
3. **Remove Duplicates from Sorted Array** (LeetCode 26)

### Medium

1. **Two Sum II - Input Array is Sorted** (LeetCode 167)
2. **Container With Most Water** (LeetCode 11)
3. **3Sum** (LeetCode 15)
4. **3Sum Closest** (LeetCode 16)
5. **4Sum** (LeetCode 18)

### Hard

1. **Trapping Rain Water** (LeetCode 42)
2. **Shortest Unsorted Continuous Subarray** (LeetCode 581)
3. **3Sum Smaller** (LeetCode 259)
4. **Count of Range Sum** (LeetCode 327)

## Summary

Two pointers is a fundamental pattern that reduces time complexity by avoiding nested loops. It's most effective when the input is sorted or when comparing elements from different positions.

## Cheat Sheet

```text
Pattern: Two Pointers
Use when: Sorted arrays, pairs, cycles, comparisons
Time: O(n) | Space: O(1)

Types:
┌─────────────────────────────────────────┐
│ 1. Opposite Direction (toward each other)│
│    - Sorted array problems               │
│    - Two sum variants                    │
│                                         │
│ 2. Same Direction (same direction)      │
│    - Fast/Slow pointers                  │
│    - Cycle detection                     │
│    - Finding middle of linked list       │
│                                         │
│ 3. Fast/Slow Pointer                    │
│    - Cycle detection                     │
│    - Finding cycle start                 │
│    - Middle of linked list               │
└─────────────────────────────────────────┘

Key insight: If sum too small, move left pointer right
            If sum too big, move right pointer left
```

---

## References & Learn More
- [LeetCode Two Pointers](https://leetcode.com/tag/two-pointers/)
- [NeetCode Two Pointers](https://neetcode.io/)
- [CP-Algorithms](https://cp-algorithms.com/)
- [Algorithm Design by Kleinberg & Tardos](https://www.amazon.com/Algorithm-Design-Kleinberg-Jon/dp/0321295358)
- [GeeksforGeeks Two Pointers](https://www.geeksforgeeks.org/two-pointers-technique/)
