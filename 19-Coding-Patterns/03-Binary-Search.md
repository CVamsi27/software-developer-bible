# Binary Search

## Definition

Binary search is a search algorithm that finds the position of a target value within a sorted array by repeatedly dividing the search interval in half. It compares the target value to the middle element of the array and eliminates the half where the target cannot exist.

## When to Use

- Searching in a sorted array
- Finding boundary conditions (first/last occurrence)
- Searching on a sorted/monotonic function
- Finding minimum/maximum value satisfying a condition
- Search space problems where answer can be guessed and verified

## Template

```typescript
// Standard Binary Search
function binarySearch(nums: number[], target: number): number {
  let left = 0;
  let right = nums.length - 1;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);

    if (nums[mid] === target) {
      return mid;
    } else if (nums[mid] < target) {
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }

  return -1; // not found
}
```

## How It Works

```
Sorted Array: [2, 5, 8, 12, 16, 23, 38, 56, 72, 91], Target = 23

Step 1: left=0, right=9, mid=4
        [2, 5, 8, 12, |16|, 23, 38, 56, 72, 91]
                       mid
        16 < 23, so search right half

Step 2: left=5, right=9, mid=7
        [23, 38, |56|, 72, 91]
               mid
        56 > 23, so search left half

Step 3: left=5, right=6, mid=5
        [|23|, 38]
         mid
        23 = 23, found at index 5!
```

### ASCII Diagram

```
STANDARD BINARY SEARCH
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│ 2 │ 5 │ 8 │12 │16 │23 │38 │56 │72 │91 │
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
  L                       M               R
                    (16 < 23, move L)
                          L           M   R
                         (23 found!)

LEFT BOUND SEARCH (first occurrence)
┌───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 2 │ 2 │ 3 │ 3 │  target = 2
└───┴───┴───┴───┴───┴───┘
  L           M       R
            (found 2, but keep searching left)
              L   M   R
            (left bound found at index 1)

RIGHT BOUND SEARCH (last occurrence)
┌───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 2 │ 2 │ 3 │ 3 │  target = 2
└───┴───┴───┴───┴───┴───┘
  L           M       R
            (found 2, keep searching right)
              L       M
                    R (right bound found at index 3)
```

## Code Examples (TypeScript)

### Problem 1: Standard Binary Search

```typescript
function binarySearch(nums: number[], target: number): number {
  let left = 0;
  let right = nums.length - 1;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);

    if (nums[mid] === target) {
      return mid;
    } else if (nums[mid] < target) {
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }

  return -1;
}

// Example
console.log(binarySearch([-1, 0, 3, 5, 9, 12], 9)); // 4
console.log(binarySearch([-1, 0, 3, 5, 9, 12], 2)); // -1
```

### Problem 2: Left Bound Binary Search (First Occurrence)

```typescript
function searchLeftBound(nums: number[], target: number): number {
  let left = 0;
  let right = nums.length - 1;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);

    if (nums[mid] === target) {
      right = mid - 1; // keep searching left
    } else if (nums[mid] < target) {
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }

  return left < nums.length && nums[left] === target ? left : -1;
}

// Example
console.log(searchLeftBound([5, 7, 7, 8, 8, 10], 8)); // 3 (first 8)
console.log(searchLeftBound([5, 7, 7, 8, 8, 10], 6)); // -1
```

### Problem 3: Right Bound Binary Search (Last Occurrence)

```typescript
function searchRightBound(nums: number[], target: number): number {
  let left = 0;
  let right = nums.length - 1;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);

    if (nums[mid] === target) {
      left = mid + 1; // keep searching right
    } else if (nums[mid] < target) {
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }

  return right >= 0 && nums[right] === target ? right : -1;
}

// Example
console.log(searchRightBound([5, 7, 7, 8, 8, 10], 8)); // 4 (last 8)
console.log(searchRightBound([5, 7, 7, 8, 8, 10], 6)); // -1
```

### Problem 4: Search in Rotated Sorted Array

```typescript
function searchRotated(nums: number[], target: number): number {
  let left = 0;
  let right = nums.length - 1;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);

    if (nums[mid] === target) return mid;

    // Left half is sorted
    if (nums[left] <= nums[mid]) {
      if (target >= nums[left] && target < nums[mid]) {
        right = mid - 1;
      } else {
        left = mid + 1;
      }
    }
    // Right half is sorted
    else {
      if (target > nums[mid] && target <= nums[right]) {
        left = mid + 1;
      } else {
        right = mid - 1;
      }
    }
  }

  return -1;
}

// Example
console.log(searchRotated([4, 5, 6, 7, 0, 1, 2], 0)); // 4
console.log(searchRotated([4, 5, 6, 7, 0, 1, 2], 3)); // -1
```

### Problem 5: Find Minimum in Rotated Sorted Array

```typescript
function findMin(nums: number[]): number {
  let left = 0;
  let right = nums.length - 1;

  while (left < right) {
    const mid = Math.floor((left + right) / 2);

    if (nums[mid] > nums[right]) {
      left = mid + 1;
    } else {
      right = mid;
    }
  }

  return nums[left];
}

// Example
console.log(findMin([3, 4, 5, 1, 2])); // 1
console.log(findMin([4, 5, 6, 7, 0, 1, 2])); // 0
```

### Problem 6: Search a 2D Matrix

```typescript
function searchMatrix(matrix: number[][], target: number): boolean {
  if (matrix.length === 0) return false;

  const m = matrix.length;
  const n = matrix[0].length;
  let left = 0;
  let right = m * n - 1;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);
    const midValue = matrix[Math.floor(mid / n)][mid % n];

    if (midValue === target) {
      return true;
    } else if (midValue < target) {
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }

  return false;
}

// Example
const matrix = [
  [1, 3, 5, 7],
  [10, 11, 16, 20],
  [23, 30, 34, 60]
];
console.log(searchMatrix(matrix, 3)); // true
console.log(searchMatrix(matrix, 13)); // false
```

## Common Mistakes

1. **Infinite loops**: Always ensure `left` and `right` move toward each other
2. **Off-by-one with mid**: Use `Math.floor((left + right) / 2)` or `left + (right - left) / 2`
3. **Wrong boundary**: `left <= right` vs `left < right` depends on the problem
4. **Not handling duplicates**: When duplicates exist, you may need to handle them explicitly
5. **Integer overflow**: Use `left + (right - left) / 2` instead of `(left + right) / 2`

## Time/Space Complexity

| Complexity | Standard | Left/Right Bound | Rotated Array |
|------------|----------|------------------|---------------|
| Time       | O(log n) | O(log n)         | O(log n)      |
| Space      | O(1)     | O(1)             | O(1)          |

- **Time O(log n)**: Each iteration halves the search space
- **Space O(1)**: Only using a few pointers

## Interview Problems

### Easy

1. **Binary Search** (LeetCode 704)
2. **First Bad Version** (LeetCode 278)
3. **Valid Perfect Square** (LeetCode 367)

### Medium

1. **Search in Rotated Sorted Array** (LeetCode 33)
2. **Find First and Last Position of Element in Sorted Array** (LeetCode 34)
3. **Search in Rotated Sorted Array II** (LeetCode 81)
4. **Find Minimum in Rotated Sorted Array** (LeetCode 153)
5. **Capacity To Ship Packages Within D Days** (LeetCode 1011)
6. **Koko Eating Bananas** (LeetCode 875)
7. **Search a 2D Matrix** (LeetCode 74)

### Hard

1. **Median of Two Sorted Arrays** (LeetCode 4)
2. **Find in Mountain Array** (LeetCode 1095)
3. **Split Array Largest Sum** (LeetCode 410)
4. **Aggressive Cows** (SPOJ)

## Summary

Binary search is a fundamental algorithm for searching in sorted data. The key insight is to reduce the search space by half each iteration, achieving O(log n) time complexity.

## Cheat Sheet

```
Pattern: Binary Search
Use when: Sorted arrays, monotonic functions, search space
Time: O(log n) | Space: O(1)

Variants:
┌─────────────────────────────────────────┐
│ 1. Standard: left <= right              │
│    - Find exact target                  │
│                                         │
│ 2. Left Bound: left < right             │
│    - Find first occurrence              │
│    - Move right = mid                   │
│                                         │
│ 3. Right Bound: left < right            │
│    - Find last occurrence               │
│    - Move left = mid + 1                │
│                                         │
│ 4. Search Space:                        │
│    - Binary search on answer            │
│    - Verify if mid works                │
└─────────────────────────────────────────┘

Key: Always ensure left and right converge
```

---

## References & Learn More
- [LeetCode Binary Search](https://leetcode.com/tag/binary-search/)
- [NeetCode Binary Search](https://neetcode.io/)
- [CP-Algorithms](https://cp-algorithms.com/)
- [Algorithm Design by Kleinberg & Tardos](https://www.amazon.com/Algorithm-Design-Kleinberg-Jon/dp/0321295358)
- [GeeksforGeeks Binary Search](https://www.geeksforgeeks.org/binary-search/)
