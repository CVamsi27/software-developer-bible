# Trie

## Definition

A Trie (also called a prefix tree or digital tree) is a tree-like data structure used to store a dynamic set of strings, where each node represents a character. It's particularly efficient for prefix-based operations like autocomplete, spell checking, and word search.

## When to Use

- Prefix-based searches
- Autocomplete/autosuggest features
- Spell checking
- Word games (Boggle, Word Search II)
- IP routing
- Any problem with prefix matching

## Template

```typescript
class TrieNode {
  children: Map<string, TrieNode>;
  isEnd: boolean;

  constructor() {
    this.children = new Map();
    this.isEnd = false;
  }
}

class Trie {
  private root: TrieNode;

  constructor() {
    this.root = new TrieNode();
  }

  insert(word: string): void {
    let node = this.root;
    for (const char of word) {
      if (!node.children.has(char)) {
        node.children.set(char, new TrieNode());
      }
      node = node.children.get(char)!;
    }
    node.isEnd = true;
  }

  search(word: string): boolean {
    let node = this.root;
    for (const char of word) {
      if (!node.children.has(char)) return false;
      node = node.children.get(char)!;
    }
    return node.isEnd;
  }

  startsWith(prefix: string): boolean {
    let node = this.root;
    for (const char of prefix) {
      if (!node.children.has(char)) return false;
      node = node.children.get(char)!;
    }
    return true;
  }
}

```

## How It Works

```text
Inserting: "apple", "app", "application"

        root
        /|\
       a |
      /  |
     p   |
    / \  |
   p   |
  / \  |
 l   e  (end)

 |

 i

 |

 c

 |

 a

 |

 t

 |

 i

 |

 o

 |

 n
 (end)

Words: "apple" (root→a→p→p→l→e*)
       "app" (root→a→p→p*)
       "application" (root→a→p→p→l→i→c→a→t→i→o→n*)

```

### ASCII Diagram

```text
TRIE STRUCTURE:
┌─────────────────────────────────────────┐
│              (root)                     │
│                │                        │
│                a                        │
│                │                        │
│                p                        │
│               / \                       │
│              p   p                      │
│             / \   \                     │
│            l   e*  p*                   │
│            │       │                    │
│            e*      l                    │
│            │       │                    │
│            d       i                    │
│            │       │                    │
│           (end)    c                    │
│                   │                     │
│                   a                     │
│                   │                     │
│                   t                     │
│                   │                     │
│                   i                     │
│                   │                     │
│                   o                     │
│                   │                     │
│                   n*                    │
│                   (end)                 │
└─────────────────────────────────────────┘

- marks end of word

```

## Code Examples (TypeScript)

### Problem 1: Implement Trie (Prefix Tree)

```typescript
class TrieNode {
  children: Map<string, TrieNode>;
  isEnd: boolean;

  constructor() {
    this.children = new Map();
    this.isEnd = false;
  }
}

class Trie {
  private root: TrieNode;

  constructor() {
    this.root = new TrieNode();
  }

  insert(word: string): void {
    let node = this.root;
    for (const char of word) {
      if (!node.children.has(char)) {
        node.children.set(char, new TrieNode());
      }
      node = node.children.get(char)!;
    }
    node.isEnd = true;
  }

  search(word: string): boolean {
    let node = this.root;
    for (const char of word) {
      if (!node.children.has(char)) return false;
      node = node.children.get(char)!;
    }
    return node.isEnd;
  }

  startsWith(prefix: string): boolean {
    let node = this.root;
    for (const char of prefix) {
      if (!node.children.has(char)) return false;
      node = node.children.get(char)!;
    }
    return true;
  }
}

// Example
const trie = new Trie();
trie.insert("apple");
trie.insert("app");
trie.insert("application");
console.log(trie.search("apple"));     // true
console.log(trie.search("app"));       // true
console.log(trie.startsWith("app"));   // true
console.log(trie.startsWith("apl"));   // false

```

### Problem 2: Design Add and Search Words Data Structure

```typescript
class TrieNode {
  children: Map<string, TrieNode>;
  isEnd: boolean;

  constructor() {
    this.children = new Map();
    this.isEnd = false;
  }
}

class WordDictionary {
  private root: TrieNode;

  constructor() {
    this.root = new TrieNode();
  }

  addWord(word: string): void {
    let node = this.root;
    for (const char of word) {
      if (!node.children.has(char)) {
        node.children.set(char, new TrieNode());
      }
      node = node.children.get(char)!;
    }
    node.isEnd = true;
  }

  search(word: string): boolean {
    return this.dfs(word, 0, this.root);
  }

  private dfs(word: string, index: number, node: TrieNode): boolean {
    if (index === word.length) return node.isEnd;

    const char = word[index];

    if (char === '.') {
      for (const child of node.children.values()) {
        if (this.dfs(word, index + 1, child)) return true;
      }
      return false;
    }

    if (!node.children.has(char)) return false;

    return this.dfs(word, index + 1, node.children.get(char)!);
  }
}

// Example
const wordDict = new WordDictionary();
wordDict.addWord("bad");
wordDict.addWord("dad");
wordDict.addWord("mad");
console.log(wordDict.search("pad")); // false
console.log(wordDict.search("bad")); // true
console.log(wordDict.search(".ad")); // true
console.log(wordDict.search("b..")); // true

```

### Problem 3: Word Search II

```typescript
function findWords(board: string[][], words: string[]): string[] {
  const result: string[] = [];

  // Build trie from words
  const trie = new Trie();
  for (const word of words) {
    trie.insert(word);
  }

  const rows = board.length;
  const cols = board[0].length;

  function dfs(r: number, c: number, node: TrieNode, word: string): void {
    if (node.isEnd) {
      result.push(word);
      node.isEnd = false; // avoid duplicates
    }

    if (r < 0 || r >= rows || c < 0 || c >= cols) return;

    const char = board[r][c];
    if (char === '#' || !node.children.has(char)) return;

    board[r][c] = '#'; // mark visited

    const childNode = node.children.get(char)!;
    dfs(r + 1, c, childNode, word + char);
    dfs(r - 1, c, childNode, word + char);
    dfs(r, c + 1, childNode, word + char);
    dfs(r, c - 1, childNode, word + char);

    board[r][c] = char; // restore
  }

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (trie.root.children.has(board[r][c])) {
        dfs(r, c, trie.root, '');
      }
    }
  }

  return result;
}

// Example
const board = [
  ["o","a","a","n"],
  ["e","t","a","e"],
  ["i","h","k","r"],
  ["i","f","l","v"]
];
const words = ["oath","pea","eat","rain"];
console.log(findWords(board, words)); // ["eat","oath"]

```

### Problem 4: Longest Word in Dictionary

```typescript
function longestWord(words: string[]): string {
  const trie = new Trie();
  for (const word of words) {
    trie.insert(word);
  }

  let longest = '';

  function dfs(node: TrieNode, current: string): void {
    if (current.length > longest.length) {
      longest = current;
    }

    for (const [char, childNode] of node.children) {
      if (childNode.isEnd) {
        dfs(childNode, current + char);
      }
    }
  }

  dfs(trie.root, '');
  return longest;
}

// Example
console.log(longestWord(["w","wo","wor","worl","world"])); // "world"
console.log(longestWord(["a","ap","app","appl","apple"])); // "apple"

```

### Problem 5: Replace Words

```typescript
class TrieNode {
  children: Map<string, TrieNode>;
  isEnd: boolean;

  constructor() {
    this.children = new Map();
    this.isEnd = false;
  }
}

function replaceWords(dictionary: string[], sentence: string): string {
  const trie = new TrieNode();

  // Build trie
  for (const root of dictionary) {
    let node = trie;
    for (const char of root) {
      if (!node.children.has(char)) {
        node.children.set(char, new TrieNode());
      }
      node = node.children.get(char)!;
    }
    node.isEnd = true;
  }

  // Find shortest root for each word
  function findRoot(word: string): string {
    let node = trie;
    for (let i = 0; i < word.length; i++) {
      const char = word[i];
      if (!node.children.has(char) || node.isEnd) {
        return word.substring(0, i);
      }
      node = node.children.get(char)!;
    }
    return word;
  }

  return sentence.split(' ').map(findRoot).join(' ');
}

// Example
console.log(replaceWords(
  ["cat", "bat", "rat"],
  "the cattle was rattled by the battery"
)); // "the cat was rat by the bat"

```

### Problem 6: Map Sum Pairs

```typescript
class TrieNode {
  children: Map<string, TrieNode>;
  value: number;

  constructor() {
    this.children = new Map();
    this.value = 0;
  }
}

class MapSum {
  private root: TrieNode;
  private map: Map<string, number>;

  constructor() {
    this.root = new TrieNode();
    this.map = new Map();
  }

  insert(key: string, val: number): void {
    const delta = val - (this.map.get(key) || 0);
    this.map.set(key, val);

    let node = this.root;
    for (const char of key) {
      if (!node.children.has(char)) {
        node.children.set(char, new TrieNode());
      }
      node = node.children.get(char)!;
      node.value += delta;
    }
  }

  sum(prefix: string): number {
    let node = this.root;
    for (const char of prefix) {
      if (!node.children.has(char)) return 0;
      node = node.children.get(char)!;
    }
    return node.value;
  }
}

// Example
const mapSum = new MapSum();
mapSum.insert("apple", 3);
console.log(mapSum.sum("ap"));     // 3
mapSum.insert("app", 2);
console.log(mapSum.sum("ap"));     // 5

```

## Common Mistakes

1. **Not handling edge cases**: Empty strings, single characters

2. **Forgetting to mark end of word**: Always set `isEnd = true` after inserting

3. **Not cleaning up after removal**: If implementing deletion, handle all cases

4. **Using array instead of Map**: Map is more flexible for character storage

5. **Not checking for null**: Always verify node exists before accessing children

## Time/Space Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Insert | O(m) | O(m) |
| Search | O(m) | O(1) |
| StartsWith | O(m) | O(1) |

- **m**: length of the word
- **Space**: O(N × m) total for N words, but often less due to shared prefixes

## Interview Problems

### Easy

1. **Implement Trie (Prefix Tree)** (LeetCode 208)

2. **Maximum Depth of N-ary Tree** (LeetCode 559)

### Medium

1. **Design Add and Search Words Data Structure** (LeetCode 211)

2. **Word Search II** (LeetCode 212)

3. **Longest Word in Dictionary** (LeetCode 720)

4. **Map Sum Pairs** (LeetCode 677)

5. **Replace Words** (LeetCode 648)

6. **Search Suggestions System** (LeetCode 1268)

### Hard

1. **Palindrome Pairs** (LeetCode 336)

2. **Word Search II** (LeetCode 212) — uses Trie + DFS

3. **Stream of Characters** (LeetCode 1032)

## Summary

Trie is a powerful data structure for prefix-based operations. It's essential for autocomplete, spell checking, and word games. The key insight is sharing common prefixes to save space.

## Cheat Sheet

```text
Pattern: Trie (Prefix Tree)
Use when: Prefix matching, autocomplete, word search
Time: O(m) per operation | Space: O(N × m)

Structure:
┌─────────────────────────────────────────┐
│ Each node contains:                     │
│ - Map of children (char → node)         │
│ - isEnd flag (marks end of word)        │
└─────────────────────────────────────────┘

Operations:

- insert(word): O(m) time
- search(word): O(m) time
- startsWith(prefix): O(m) time

Key insight:

- Share common prefixes
- Use isEnd to distinguish words from prefixes
- For '.' matching, use DFS/backtracking

Common patterns:

- Build trie from dictionary
- Search with DFS
- Check prefixes efficiently

```

---

## References & Learn More

- [LeetCode Trie](https://leetcode.com/tag/trie/)
- [NeetCode Trie](https://neetcode.io/)
- [CP-Algorithms](https://cp-algorithms.com/)
- [Algorithm Design by Kleinberg & Tardos](https://www.amazon.com/Algorithm-Design-Kleinberg-Jon/dp/0321295358)
- [GeeksforGeeks Trie](https://www.geeksforgeeks.org/trie-insert-and-search/)
