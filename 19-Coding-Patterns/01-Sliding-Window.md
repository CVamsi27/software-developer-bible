# Sliding Window

## Definition

The sliding window pattern is a technique that uses a "window" (a subset of elements) that slides over a data structure to solve problems involving contiguous sequences. It maintains a window of elements and adjusts the window boundaries as it traverses the input, avoiding redundant recalculations.

## When to Use

- Finding a subarray/substring with a specific property (max sum, target sum)
- Problems involving contiguous sequences of elements
- When brute force would use nested loops (O(n²) or O(n³))
- Problems asking for maximum/minimum of a subarray of fixed or variable size
- String permutation or anagram problems

## Template

```typescript
function slidingWindow(nums: number[], k: number): number {
  let windowSum = 0;
  let maxSum = -Infinity;

  // Phase 1: Build the initial window
  for (let i = 0; i < k; i++) {
    windowSum += nums[i];
  }
  maxSum = windowSum;

  // Phase 2: Slide the window
  for (let i = k; i < nums.length; i++) {
    windowSum += nums[i] - nums[i - k]; // slide right
    maxSum = Math.max(maxSum, windowSum);
  }

  return maxSum;
}
```

## How It Works

```
Array: [2, 1, 5, 1, 3, 2], k = 3

Fixed Window (k=3):
Step 1: [2, 1, 5] 1, 3, 2  → sum = 8
Step 2:  2, [1, 5, 1] 3, 2  → sum = 7
Step 3:  2, 1, [5, 1, 3] 2  → sum = 9  ← max
Step 4:  2, 1, 5, [1, 3, 2] → sum = 6

Variable Window:
Target sum = 7
[2, 1, 5] 1, 3, 2     → sum = 8 (too big, shrink)
 2 [1, 5] 1, 3, 2     → sum = 6 (too small, expand)
 2, [1, 5, 1] 3, 2    → sum = 7 ✓ found!
```

### ASCII Diagram

```
FIXED WINDOW                    VARIABLE WINDOW
┌─────────┐                    ┌─────────┐
│ Window  │                    │ Window  │
│ (k=3)   │                    │ (target)│
└────┬────┘                    └────┬────┘
     │                              │
     ▼                              ▼
┌───┬───┬───┬───┬───┐         ┌───┬───┬───┬───┬───┐
│ 2 │ 1 │ 5 │ 1 │ 3 │         │ 2 │ 1 │ 5 │ 1 │ 3 │
└───┴───┴───┴───┴───┘         └───┴───┴───┴───┴───┘
  ▲                           ▲               ▲
  L                           L               R
  (left)                      (left)          (right)
```

## Code Examples (TypeScript)

### Problem 1: Maximum Sum Subarray of Size K (Fixed Window)

```typescript
function maxSumSubarray(nums: number[], k: number): number {
  let windowSum = 0;
  let maxSum = -Infinity;

  for (let i = 0; i < nums.length; i++) {
    windowSum += nums[i];

    if (i >= k) {
      windowSum -= nums[i - k];
    }

    if (i >= k - 1) {
      maxSum = Math.max(maxSum, windowSum);
    }
  }

  return maxSum;
}

// Example
console.log(maxSumSubarray([2, 1, 5, 1, 3, 2], 3)); // 9
// Explanation: [5, 1, 3] has the maximum sum
```

### Problem 2: Longest Substring Without Repeating Characters (Variable Window)

```typescript
function lengthOfLongestSubstring(s: string): number {
  const charMap = new Map<string, number>();
  let maxLength = 0;
  let left = 0;

  for (let right = 0; right < s.length; right++) {
    const char = s[right];

    if (charMap.has(char) && charMap.get(char)! >= left) {
      left = charMap.get(char)! + 1;
    }

    charMap.set(char, right);
    maxLength = Math.max(maxLength, right - left + 1);
  }

  return maxLength;
}

// Example
console.log(lengthOfLongestSubstring("abcabcbb")); // 3 ("abc")
console.log(lengthOfLongestSubstring("bbbbb"));     // 1 ("b")
console.log(lengthOfLongestSubstring("pwwkew"));    // 3 ("wke")
```

### Problem 3: Minimum Window Substring (Variable Window with Shrink)

```typescript
function minWindow(s: string, t: string): string {
  if (s.length < t.length) return "";

  const need = new Map<string, number>();
  const window = new Map<string, number>();

  for (const char of t) {
    need.set(char, (need.get(char) || 0) + 1);
  }

  let left = 0;
  let right = 0;
  let valid = 0;
  let minLen = Infinity;
  let minStart = 0;

  while (right < s.length) {
    const char = s[right];
    window.set(char, (window.get(char) || 0) + 1);

    if (need.has(char) && window.get(char) === need.get(char)) {
      valid++;
    }

    while (valid === need.size) {
      if (right - left + 1 < minLen) {
        minLen = right - left + 1;
        minStart = left;
      }

      const leftChar = s[left];
      window.set(leftChar, window.get(leftChar)! - 1);

      if (need.has(leftChar) && window.get(leftChar)! < need.get(leftChar)!) {
        valid--;
      }

      left++;
    }

    right++;
  }

  return minLen === Infinity ? "" : s.substring(minStart, minStart + minLen);
}

// Example
console.log(minWindow("ADOBECODEBANC", "ABC")); // "BANC"
```

### Problem 4: Longest Repeating Character Replacement

```typescript
function characterReplacement(s: string, k: number): number {
  const count = new Map<string, number>();
  let maxCount = 0; // max frequency in current window
  let left = 0;
  let maxLength = 0;

  for (let right = 0; right < s.length; right++) {
    const char = s[right];
    count.set(char, (count.get(char) || 0) + 1);
    maxCount = Math.max(maxCount, count.get(char)!);

    // If we need to replace more than k characters, shrink window
    while (right - left + 1 - maxCount > k) {
      const leftChar = s[left];
      count.set(leftChar, count.get(leftChar)! - 1);
      left++;
    }

    maxLength = Math.max(maxLength, right - left + 1);
  }

  return maxLength;
}

// Example
console.log(characterReplacement("AABABBA", 1)); // 4 ("AABA")
```

## Common Mistakes

1. **Off-by-one errors**: Forgetting that the window size starts at 0 and needs `i >= k - 1` check
2. **Not resetting window state**: When the problem requires independent windows
3. **Forgetting to update left pointer**: In variable window, always shrink when condition is met
4. **Using wrong data structure**: Use a Map or array for character frequency, not a Set
5. **Not handling edge cases**: Empty strings, single elements, k > array length

## Time/Space Complexity

| Complexity | Fixed Window | Variable Window |
|------------|--------------|-----------------|
| Time       | O(n)        | O(n)            |
| Space      | O(1)        | O(k) or O(n)    |

- **Time O(n)**: Each element is visited at most twice (once by right pointer, once by left)
- **Space O(1) or O(k)**: For fixed window, we only store k elements. For variable, depends on the window size.

## Interview Problems

### Easy

1. **Maximum Average Subarray I** (LeetCode 643)
   - Find max average of subarray of size k
   
2. **Best Time to Buy and Sell Stock** (LeetCode 121)
   - Find max profit with one transaction

3. **Maximum Profit in Job Scheduling** (related pattern)

### Medium

1. **Longest Substring Without Repeating Characters** (LeetCode 3)
2. **Longest Repeating Character Replacement** (LeetCode 424)
3. **Minimum Size Subarray Sum** (LeetCode 209)
4. **Permutation in String** (LeetCode 567)
5. **Fruit Into Baskets** (LeetCode 904)

### Hard

1. **Minimum Window Substring** (LeetCode 76)
2. **Substring with Concatenation of All Words** (LeetCode 30)
3. **Sliding Window Maximum** (LeetCode 239) — uses deque
4. **Longest Substring with At Most K Distinct Characters** (LeetCode 340)

## Summary

The sliding window pattern is essential for problems involving contiguous subarrays or substrings. It reduces time complexity from O(n²) to O(n) by maintaining and updating the window instead of recalculating from scratch.

## Cheat Sheet

```
Pattern: Sliding Window
Use when: Contiguous subarray/substring problems
Time: O(n) | Space: O(1) to O(n)

Template:
┌─────────────────────────────────────────┐
│ 1. Initialize left=0, window variables  │
│ 2. Loop right from 0 to n:             │
│    a. Add element at right to window    │
│    b. While window invalid:             │
│       - Remove element at left          │
│       - left++                          │
│    c. Update result                     │
│ 3. Return result                        │
└─────────────────────────────────────────┘

Key operations:
- Expand: right++
- Shrink: left++
- Update: when window is valid
```

---

## References & Learn More
- [LeetCode Sliding Window](https://leetcode.com/tag/sliding-window/)
- [NeetCode Sliding Window](https://neetcode.io/)
- [CP-Algorithms](https://cp-algorithms.com/)
- [Algorithm Design by Kleinberg & Tardos](https://www.amazon.com/Algorithm-Design-Kleinberg-Jon/dp/0321295358)
- [GeeksforGeeks Sliding Window](https://www.geeksforgeeks.org/window-sliding-technique/)
