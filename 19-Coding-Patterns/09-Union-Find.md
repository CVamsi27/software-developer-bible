# Union-Find

## Definition

Union-Find (also called Disjoint Set Union or DSU) is a data structure that tracks a set of elements partitioned into a number of disjoint (non-overlapping) subsets. It supports two operations: `find` (determine which set an element belongs to) and `union` (merge two sets into one).

## When to Use

- Detecting cycles in undirected graphs
- Finding connected components
- Dynamic connectivity problems
- Kruskal's minimum spanning tree algorithm
- Problems involving merging groups/sets

## Template

```typescript
class UnionFind {
  private parent: number[];
  private rank: number[];
  private components: number;

  constructor(n: number) {
    this.parent = new Array(n);
    this.rank = new Array(n).fill(0);
    this.components = n;

    for (let i = 0; i < n; i++) {
      this.parent[i] = i;
    }
  }

  find(x: number): number {
    if (this.parent[x] !== x) {
      this.parent[x] = this.find(this.parent[x]); // path compression
    }
    return this.parent[x];
  }

  union(x: number, y: number): boolean {
    const rootX = this.find(x);
    const rootY = this.find(y);

    if (rootX === rootY) return false;

    // Union by rank
    if (this.rank[rootX] < this.rank[rootY]) {
      this.parent[rootX] = rootY;
    } else if (this.rank[rootX] > this.rank[rootY]) {
      this.parent[rootY] = rootX;
    } else {
      this.parent[rootY] = rootX;
      this.rank[rootX]++;
    }

    this.components--;
    return true;
  }

  connected(x: number, y: number): boolean {
    return this.find(x) === this.find(y);
  }

  getComponents(): number {
    return this.components;
  }
}
```

## How It Works

```
Initial: [0, 1, 2, 3, 4] (5 separate sets)

Union(0, 1):
  0 ← 1    (1's root becomes 0)
  2  3  4

Union(2, 3):
  0 ← 1    2 ← 3
  4

Union(1, 3):
  0 ← 1 ← 2 ← 3
  4

find(4) = 4
find(3) = 0 (with path compression)

connected(0, 3) = true
connected(0, 4) = false
```

### ASCII Diagram

```
UNION-FIND WITH PATH COMPRESSION:

Before path compression:
    0
    |
    1
    |
    2
    |
    3

find(3) traverses: 3 → 2 → 1 → 0

After path compression:
    0
  / | \
 1  2  3

find(3) now goes directly to 0

UNION BY RANK:

Union(0, 1):     Union(2, 3):     Union(1, 2):
  0                 2                 0
  |                 |               / | \
  1                 3              1  2  3

rank[0] = 1       rank[2] = 1     rank[0] = 2
```

## Code Examples (TypeScript)

### Problem 1: Number of Islands II (Dynamic Connectivity)

```typescript
class UnionFind {
  private parent: number[];
  private rank: number[];
  private count: number;

  constructor(n: number) {
    this.parent = new Array(n);
    this.rank = new Array(n).fill(0);
    this.count = 0;

    for (let i = 0; i < n; i++) {
      this.parent[i] = i;
    }
  }

  find(x: number): number {
    if (this.parent[x] !== x) {
      this.parent[x] = this.find(this.parent[x]);
    }
    return this.parent[x];
  }

  union(x: number, y: number): boolean {
    const rootX = this.find(x);
    const rootY = this.find(y);

    if (rootX === rootY) return false;

    if (this.rank[rootX] < this.rank[rootY]) {
      this.parent[rootX] = rootY;
    } else if (this.rank[rootX] > this.rank[rootY]) {
      this.parent[rootY] = rootX;
    } else {
      this.parent[rootY] = rootX;
      this.rank[rootX]++;
    }

    this.count--;
    return true;
  }

  addIsland(): void {
    this.count++;
  }

  getCount(): number {
    return this.count;
  }
}

function numIslands2(m: number, n: number, positions: number[][]): number[] {
  const uf = new UnionFind(m * n);
  const grid = new Array(m * n).fill(0);
  const result: number[] = [];
  const directions = [[0, 1], [0, -1], [1, 0], [-1, 0]];

  for (const [r, c] of positions) {
    const id = r * n + c;

    if (grid[id] === 1) {
      result.push(uf.getCount());
      continue;
    }

    grid[id] = 1;
    uf.addIsland();

    for (const [dr, dc] of directions) {
      const nr = r + dr;
      const nc = c + dc;
      const nid = nr * n + nc;

      if (nr >= 0 && nr < m && nc >= 0 && nc < n && grid[nid] === 1) {
        uf.union(id, nid);
      }
    }

    result.push(uf.getCount());
  }

  return result;
}

// Example
console.log(numIslands2(3, 3, [[0,0],[0,1],[1,2],[2,1]]));
// [1, 1, 2, 3]
```

### Problem 2: Accounts Merge

```typescript
function accountsMerge(accounts: string[][]): string[][] {
  const emailToId = new Map<string, number>();
  const emailToName = new Map<string, string>();
  let id = 0;

  for (const account of accounts) {
    const name = account[0];
    for (let i = 1; i < account.length; i++) {
      const email = account[i];
      emailToName.set(email, name);
      if (!emailToId.has(email)) {
        emailToId.set(email, id++);
      }
    }
  }

  const uf = new UnionFind(id);

  for (const account of accounts) {
    const firstEmailId = emailToId.get(account[1])!;
    for (let i = 2; i < account.length; i++) {
      const emailId = emailToId.get(account[i])!;
      uf.union(firstEmailId, emailId);
    }
  }

  const merged = new Map<number, string[]>();
  for (const [email] of emailToId) {
    const root = uf.find(emailToId.get(email)!);
    if (!merged.has(root)) {
      merged.set(root, []);
    }
    merged.get(root)!.push(email);
  }

  const result: string[][] = [];
  for (const [root, emails] of merged) {
    const name = emailToName.get(emails[0])!;
    result.push([name, ...emails.sort()]);
  }

  return result;
}

// Example
console.log(accountsMerge([
  ["John","johnsmith@mail.com","john_newyork@mail.com"],
  ["John","johnsmith@mail.com","john00@mail.com"],
  ["Mary","mary@mail.com"],
  ["John","johnnybravo@mail.com"]
]));
// [["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],
//  ["Mary","mary@mail.com"],
//  ["John","johnnybravo@mail.com"]]
```

### Problem 3: Redundant Connection

```typescript
function findRedundantConnection(edges: number[][]): number[] {
  const n = edges.length;
  const uf = new UnionFind(n + 1);

  for (const [u, v] of edges) {
    if (!uf.union(u, v)) {
      return [u, v];
    }
  }

  return [];
}

// Example
console.log(findRedundantConnection([[1,2],[1,3],[2,3]])); // [2,3]
console.log(findRedundantConnection([[1,2],[2,3],[3,4],[1,4],[1,5]])); // [1,4]
```

### Problem 4: Number of Connected Components in an Undirected Graph

```typescript
function countComponents(n: number, edges: number[][]): number {
  const uf = new UnionFind(n);

  for (const [u, v] of edges) {
    uf.union(u, v);
  }

  return uf.getComponents();
}

// Example
console.log(countComponents(5, [[0,1],[1,2],[3,4]])); // 3
console.log(countComponents(5, [[0,1],[1,2],[2,3],[3,4]])); // 1
```

### Problem 5: Surrounded Regions (Union-Find approach)

```typescript
function solve(board: string[][]): void {
  if (!board || board.length === 0) return;

  const rows = board.length;
  const cols = board[0].length;
  const uf = new UnionFind(rows * cols + 1);
  const dummy = rows * cols;

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (board[r][c] === 'O') {
        const id = r * cols + c;

        // Connect to dummy if on border
        if (r === 0 || r === rows - 1 || c === 0 || c === cols - 1) {
          uf.union(id, dummy);
        }

        // Connect to adjacent O's
        if (r > 0 && board[r - 1][c] === 'O') uf.union(id, (r - 1) * cols + c);
        if (c > 0 && board[r][c - 1] === 'O') uf.union(id, r * cols + (c - 1));
      }
    }
  }

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (board[r][c] === 'O' && !uf.connected(r * cols + c, dummy)) {
        board[r][c] = 'X';
      }
    }
  }
}

// Example
const board = [
  ["X","X","X","X"],
  ["X","O","O","X"],
  ["X","X","O","X"],
  ["X","O","X","X"]
];
solve(board);
console.log(board);
// [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]
```

## Common Mistakes

1. **Not using path compression**: Makes find operations O(n) instead of O(α(n))
2. **Not using union by rank**: Can lead to unbalanced trees
3. **Forgetting to check if already connected**: Union should return false if roots are same
4. **Wrong index handling**: Ensure 0-indexed or 1-indexed consistently
5. **Not updating component count**: Keep track of number of components

## Time/Space Complexity

| Operation | Time (with optimizations) | Space |
|-----------|---------------------------|-------|
| Find | O(α(n)) amortized | O(1) |
| Union | O(α(n)) amortized | O(1) |
| Connected | O(α(n)) amortized | O(1) |

- **α(n)**: Inverse Ackermann function (nearly constant, < 5 for all practical n)
- **Space**: O(n) for parent and rank arrays

## Interview Problems

### Easy

1. **Number of Provinces** (LeetCode 547)
2. **Max Area of Island** (LeetCode 695)

### Medium

1. **Accounts Merge** (LeetCode 721)
2. **Number of Connected Components in an Undirected Graph** (LeetCode 323)
3. **Redundant Connection** (LeetCode 684)
4. **Redundant Connection II** (LeetCode 685)
5. **Number of Islands II** (LeetCode 305)
6. **Surrounded Regions** (LeetCode 130)

### Hard

1. **Smallest String With Swaps** (LeetCode 1202)
2. **Accounts Merge** (LeetCode 721)
3. **Number of Islands II** (LeetCode 305)

## Summary

Union-Find is a powerful data structure for dynamic connectivity problems. With path compression and union by rank, it achieves nearly constant time per operation.

## Cheat Sheet

```
Pattern: Union-Find (DSU)
Use when: Connected components, cycle detection, merging sets
Time: O(α(n)) amortized | Space: O(n)

Key operations:
┌─────────────────────────────────────────┐
│ find(x): Find root of x                │
│   - Use path compression                │
│                                         │
│ union(x, y): Merge sets containing x,y │
│   - Use union by rank                   │
│   - Return false if already connected   │
│                                         │
│ connected(x, y): Check if same set     │
│   - find(x) === find(y)                │
└─────────────────────────────────────────┘

Optimizations:
1. Path compression: flatten tree during find
2. Union by rank: attach smaller tree to larger

Common patterns:
- Grid problems: id = row * cols + col
- Track component count: increment on union
- Detect cycle: union returns false
```

---

## References & Learn More
- [LeetCode Union Find](https://leetcode.com/tag/union-find/)
- [NeetCode Union Find](https://neetcode.io/)
- [CP-Algorithms](https://cp-algorithms.com/)
- [Algorithm Design by Kleinberg & Tardos](https://www.amazon.com/Algorithm-Design-Kleinberg-Jon/dp/0321295358)
- [GeeksforGeeks Union Find](https://www.geeksforgeeks.org/union-find/)
