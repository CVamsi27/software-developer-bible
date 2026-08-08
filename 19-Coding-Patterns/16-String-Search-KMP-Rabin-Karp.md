---
section: Coding Patterns
category: Interview
tags: [concept, practice]
---

# String Search — KMP & Rabin-Karp

## Definition

**String search** finds occurrences of a **pattern** `P` (length `m`) inside a **text** `T` (length `n`). Naive search is O(nm) — for each position in T, check if the pattern matches. Two interview-classical algorithms improve this:

- **Knuth-Morris-Pratt (KMP)**: builds a **failure function** (also called the prefix function or LPS — Longest Proper Prefix which is also Suffix) in O(m) time, then searches in O(n) time, total **O(n+m)** with O(m) extra space. Never re-checks characters in T.
- **Rabin-Karp**: uses **rolling hash** to compute the hash of every length-m window in T in O(1) per shift. Average case **O(n+m)**, worst case O(nm) when hash collisions cluster. Excellent for **multi-pattern search**.

## TL;DR

KMP and Rabin-Karp are the two classic **O(n+m)** string-matching algorithms. KMP uses a precomputed **failure function** to skip comparisons when a mismatch happens (similar to how KMP avoids re-reading the text). Rabin-Karp uses a **rolling hash** to compare hashes in O(1) per window, with a fallback check on actual characters when hashes match. **Use KMP for single-pattern, deterministic O(n+m)**. **Use Rabin-Karp for multi-pattern search** (e.g., find any of K patterns at once) or when you can tolerate average-case performance.

## Why it matters

String search appears in **~5% of interview problems** and is the senior-signal pattern for **DNA/protein matching, plagiarism detection, log analysis, and grep-style searching**. The senior-level question: **deriving the KMP failure function** (the LPS array, which is the heart of the algorithm), **handling hash collisions in Rabin-Karp** (always verify the actual characters on a hash match), and **choosing between KMP and Rabin-Karp** based on use case. Weak candidates re-implement the naive O(nm) search; strong candidates recognize the linear-time opportunity and code the right algorithm.

## When to Use

- **KMP**: "Find all occurrences of pattern P in text T", "Find the shortest prefix that's a suffix", "Detect pattern cycles", "Implement strStr()"
- **Rabin-Karp**: "Find all occurrences of any of K patterns in T", "Find longest palindromic substring" (Manacher-style), "Plagiarism detection"
- **Pattern signature**: substring matching, where naive O(nm) is too slow; especially when the text is large (logs, DNA, code)

## Template

```typescript
// ==================== KMP ====================
function kmpSearch(text: string, pattern: string): number[] {
  if (pattern.length === 0) return [];
  const lps = computeLPS(pattern);
  const result: number[] = [];
  let i = 0; // index in text
  let j = 0; // index in pattern

  while (i < text.length) {
    if (text[i] === pattern[j]) {
      i++;
      j++;
      if (j === pattern.length) {
        result.push(i - j); // match found at index i - j
        j = lps[j - 1];     // continue searching
      }
    } else {
      if (j !== 0) {
        j = lps[j - 1]; // fallback using LPS, don't move i
      } else {
        i++;
      }
    }
  }

  return result;
}

function computeLPS(pattern: string): number[] {
  const lps = new Array(pattern.length).fill(0);
  let length = 0; // length of previous longest prefix-suffix
  let i = 1;

  while (i < pattern.length) {
    if (pattern[i] === pattern[length]) {
      length++;
      lps[i] = length;
      i++;
    } else {
      if (length !== 0) {
        length = lps[length - 1]; // try a shorter prefix
      } else {
        lps[i] = 0;
        i++;
      }
    }
  }

  return lps;
}

// ==================== Rabin-Karp ====================
function rabinKarpSearch(text: string, pattern: string): number[] {
  if (pattern.length > text.length) return [];
  const base = 256;     // alphabet size
  const mod = 1_000_000_007; // large prime
  const m = pattern.length;

  // Compute initial hash of pattern and first window of text
  let patternHash = 0;
  let windowHash = 0;
  let h = 1; // base^(m-1) mod mod
  for (let i = 0; i < m - 1; i++) h = (h * base) % mod;

  for (let i = 0; i < m; i++) {
    patternHash = (patternHash * base + pattern.charCodeAt(i)) % mod;
    windowHash = (windowHash * base + text.charCodeAt(i)) % mod;
  }

  const result: number[] = [];
  for (let i = 0; i <= text.length - m; i++) {
    if (patternHash === windowHash) {
      // Verify character-by-character to avoid false positives
      let match = true;
      for (let k = 0; k < m; k++) {
        if (text[i + k] !== pattern[k]) { match = false; break; }
      }
      if (match) result.push(i);
    }
    // Roll the hash to the next window
    if (i < text.length - m) {
      windowHash = ((windowHash - text.charCodeAt(i) * h) * base + text.charCodeAt(i + m)) % mod;
      if (windowHash < 0) windowHash += mod; // handle negative
    }
  }

  return result;
}
```

## How It Works

### KMP — Failure Function (LPS Array)

```text
Pattern:    A  B  A  B  A  C
Index:      0  1  2  3  4  5
LPS:        0  0  1  2  3  0

LPS[i] = length of the longest proper prefix of pattern[0..i]
         that is also a suffix of pattern[0..i]

For pattern "ABABAC":
  i=0, A:               no proper prefix/suffix → 0
  i=1, AB:              "A" vs "B" → no match   → 0
  i=2, ABA:             "A" is both prefix and suffix → 1
  i=3, ABAB:            "AB" is both                → 2
  i=4, ABABA:           "ABA" is both               → 3
  i=5, ABABAC:          no proper prefix == suffix  → 0
```

### KMP — Search Walk-Through

```text
Text:    A  B  A  B  A  C  A  B  A  B  A  C
Pattern: A  B  A  B  A  C
         ↑
         i=0, j=0, A=A ✓

i=5, j=5, text[5]=C, pattern[5]=C ✓ — MATCH at index 0!

For more matches, j = LPS[4] = 3, continue scanning.
```

### Rabin-Karp — Rolling Hash

```text
Text:    A  B  A  B  A  C  A  B  A  C  ...
Pattern: A  B  A  B  A  C  (length 5)
mod = large prime, base = 256

Initial hash:
  pattern[0..4] = 65·256^4 + 66·256^3 + 65·256^2 + 66·256 + 65
  text[0..4]    = same calculation

For each shift i:
  hash(text[i+1..i+5]) = (hash(text[i..i+4]) - text[i]·base^4)·base + text[i+5]

This runs in O(1) per shift — total O(n) for the hash, plus O(m) per match for verification.
```

## Code Examples (TypeScript)

### Example 1: Implement strStr() (LeetCode 28) — KMP

```typescript
function strStr(haystack: string, needle: string): number {
  if (needle.length === 0) return 0;
  const lps = computeLPS(needle);
  let i = 0, j = 0;

  while (i < haystack.length) {
    if (haystack[i] === needle[j]) {
      i++;
      j++;
      if (j === needle.length) return i - j;
    } else {
      if (j !== 0) j = lps[j - 1];
      else i++;
    }
  }

  return -1;
}

console.log(strStr("sadbutsad", "sad")); // 0
console.log(strStr("leetcode", "leeto")); // -1
```

### Example 2: Find All Occurrences — KMP

```typescript
function findAllOccurrences(text: string, pattern: string): number[] {
  return kmpSearch(text, pattern);
}

console.log(findAllOccurrences("abababab", "abab"));
// [0, 2, 4]
```

### Example 3: Rabin-Karp Multi-Pattern Search

```typescript
function multiPatternSearch(text: string, patterns: string[]): Map<string, number[]> {
  const results = new Map<string, number[]>();
  for (const p of patterns) results.set(p, []);

  if (patterns.length === 0) return results;

  const base = 256;
  const mod = 1_000_000_007;
  const minLen = Math.min(...patterns.map(p => p.length));
  const maxLen = Math.max(...patterns.map(p => p.length));

  // Pre-compute hashes of all patterns by length
  const hashToPatterns = new Map<number, string[]>();
  for (const p of patterns) {
    const h = computeHash(p, base, mod);
    if (!hashToPatterns.has(h)) hashToPatterns.set(h, []);
    hashToPatterns.get(h)!.push(p);
  }

  // For each window length, search
  for (let len = minLen; len <= maxLen; len++) {
    const candidates = patterns.filter(p => p.length === len);
    if (candidates.length === 0) continue;

    let h = 1;
    for (let i = 0; i < len - 1; i++) h = (h * base) % mod;

    let windowHash = 0;
    for (let i = 0; i < len; i++) {
      windowHash = (windowHash * base + text.charCodeAt(i)) % mod;
    }

    for (let i = 0; i <= text.length - len; i++) {
      if (hashToPatterns.has(windowHash)) {
        for (const p of hashToPatterns.get(windowHash)!) {
          if (text.substring(i, i + len) === p) {
            results.get(p)!.push(i);
          }
        }
      }
      if (i < text.length - len) {
        windowHash = ((windowHash - text.charCodeAt(i) * h) * base + text.charCodeAt(i + len)) % mod;
        if (windowHash < 0) windowHash += mod;
      }
    }
  }

  return results;
}

function computeHash(s: string, base: number, mod: number): number {
  let h = 0;
  for (const c of s) h = (h * base + c.charCodeAt(0)) % mod;
  return h;
}

const r = multiPatternSearch("the quick brown fox jumps", ["quick", "fox", "cat"]);
console.log(r.get("quick")); // [4]
console.log(r.get("fox"));   // [16]
console.log(r.get("cat"));   // []
```

### Example 4: Repeated Substring Pattern (LeetCode 459) — Uses KMP Logic

```typescript
function repeatedSubstringPattern(s: string): boolean {
  // The string is a repetition of a substring iff
  // LPS[n-1] > 0 and n is divisible by (n - LPS[n-1])
  const n = s.length;
  const lps = computeLPS(s);
  const longest = lps[n - 1];
  return longest > 0 && n % (n - longest) === 0;
}

console.log(repeatedSubstringPattern("ababab"));     // true
console.log(repeatedSubstringPattern("aba"));        // false
console.log(repeatedSubstringPattern("abcabcabc"));  // true
```

## Common Mistakes

### 1. Off-By-One in the LPS Array

```typescript
// ❌ BAD: setting lps[0] = 1 instead of 0
// (lps[i] is the LENGTH of the prefix, not including the current char)

// ✅ GOOD: lps[0] is always 0 (single character has no proper prefix that equals its suffix)
const lps = new Array(pattern.length).fill(0);
```

### 2. Forgetting to Verify on Hash Match (Rabin-Karp)

```typescript
// ❌ BAD: trusting hash equality
if (patternHash === windowHash) result.push(i);

// ✅ GOOD: verify character-by-character to handle collisions
if (patternHash === windowHash) {
  let match = true;
  for (let k = 0; k < m; k++) {
    if (text[i + k] !== pattern[k]) { match = false; break; }
  }
  if (match) result.push(i);
}
```

### 3. Negative Hash Values in Rolling Update

```typescript
// ❌ BAD: windowHash can go negative in JS/Java
windowHash = ((windowHash - text.charCodeAt(i) * h) * base + text.charCodeAt(i + m)) % mod;

// ✅ GOOD: fix negative values
if (windowHash < 0) windowHash += mod;
```

### 4. Using O(nm) When KMP/Rabin-Karp is Needed

```typescript
// ❌ BAD: naive search — O(nm)
function naiveSearch(text, pattern) {
  for (let i = 0; i <= text.length - pattern.length; i++) {
    let j = 0;
    while (j < pattern.length && text[i + j] === pattern[j]) j++;
    if (j === pattern.length) return i;
  }
  return -1;
}

// ✅ GOOD: KMP for guaranteed O(n+m) on single pattern
function kmpSearch(text, pattern) { /* ... */ }
```

## Time/Space Complexity

| Algorithm | Time (avg) | Time (worst) | Space |
|-----------|------------|--------------|-------|
| Naive | O(nm) | O(nm) | O(1) |
| **KMP** | O(n+m) | O(n+m) | O(m) |
| **Rabin-Karp (single pattern)** | O(n+m) | O(nm) | O(1) |
| **Rabin-Karp (K patterns)** | O(n + Km + matches) | O(nm) | O(K) |
| Z-algorithm | O(n+m) | O(n+m) | O(n+m) |

## Interview Problems

### Easy

1. **Implement strStr()** (LeetCode 28) — basic KMP
2. **Repeated Substring Pattern** (LeetCode 459) — KMP LPS trick
3. **Detect Capital** (LeetCode 520) — string, not really search

### Medium

1. **Longest Happy Prefix** (LeetCode 1392) — KMP LPS
2. **Shortest Palindrome** (LeetCode 214) — KMP on reverse
3. **Find the Index of the First Occurrence in a String** (LeetCode 28) — same as strStr
4. **Count Substrings With Only 1s** (related, not strict search)
5. **String Matching in an Array** (LeetCode 1408) — multi-pattern

### Hard

1. **Longest Duplicate Substring** (LeetCode 1044) — Rabin-Karp with binary search
2. **Distinct Subsequences** (LeetCode 115) — DP, not strict search
3. **Minimum Number of K Consecutive Bit Flips** (LeetCode 995) — sliding window
4. **Shortest Palindrome** (LeetCode 214) — KMP on the reverse

## Summary

- **KMP**: build LPS (failure function) in O(m), search in O(n) — total **O(n+m)**, no re-checks
- **Rabin-Karp**: rolling hash for O(1) window updates — **O(n+m) avg, O(nm) worst** for collisions
- **Use KMP** for single-pattern, deterministic linear time
- **Use Rabin-Karp** for multi-pattern search (e.g., grep-style "find any of K patterns")
- **Always verify on hash match** — collisions are rare but possible
- **Senior signal**: derive the LPS array, debug off-by-one in failure function, choose right algorithm
- Production: DNA/protein alignment (BLAST uses similar ideas), log search (grep uses Boyer-Moore), plagiarism detection (Winnowing, MOSS)
- The LPS array is reusable: same `computeLPS` for strStr, repeated substring, shortest palindrome prefix

---

## See Also
- [Binary Search](03-Binary-Search.md)
- [Coding Patterns](../19-Coding-Patterns/)
- [Dynamic Programming](06-Dynamic-Programming.md)
- [Sliding Window](01-Sliding-Window.md)
- [Trie](08-Trie.md)

## References & Learn More

- [KMP Algorithm — CP Algorithms](https://cp-algorithms.com/string/prefix-function.html)
- [Rabin-Karp — CP Algorithms](https://cp-algorithms.com/string/rabin-karp.html)
- [Rolling Hash — USACO Guide](https://usaco.guide/plat/strings-hash)
- [Implement strStr() — LeetCode 28](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/)
- [Longest Duplicate Substring — LeetCode 1044](https://leetcode.com/problems/longest-duplicate-substring/)
