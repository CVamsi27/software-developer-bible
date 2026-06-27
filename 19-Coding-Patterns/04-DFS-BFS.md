# DFS & BFS

## Definition

**Depth-First Search (DFS)**: A traversal algorithm that explores as far as possible along each branch before backtracking. Uses a stack (explicit or call stack).

**Breadth-First Search (BFS)**: A traversal algorithm that explores all nodes at the present depth before moving to nodes at the next depth level. Uses a queue.

## When to Use

**DFS:**
- Finding paths between two nodes
- Detecting cycles in graphs
- Topological sorting
- Solving mazes/puzzles
- When you need to explore all possibilities

**BFS:**
- Finding shortest path in unweighted graphs
- Level-order traversal of trees
- Finding connected components
- When you need to process nodes level by level

## Template

```typescript
// DFS - Recursive
function dfs(node: TreeNode | null): void {
  if (!node) return;

  // Process current node
  console.log(node.val);

  // Recurse on children
  dfs(node.left);
  dfs(node.right);
}

// DFS - Iterative (using stack)
function dfsIterative(root: TreeNode | null): void {
  if (!root) return;

  const stack: TreeNode[] = [root];

  while (stack.length > 0) {
    const node = stack.pop()!;
    console.log(node.val);

    // Push children (right first so left is processed first)
    if (node.right) stack.push(node.right);
    if (node.left) stack.push(node.left);
  }
}

// BFS - Iterative (using queue)
function bfs(root: TreeNode | null): void {
  if (!root) return;

  const queue: TreeNode[] = [root];

  while (queue.length > 0) {
    const node = queue.shift()!;
    console.log(node.val);

    if (node.left) queue.push(node.left);
    if (node.right) queue.push(node.right);
  }
}
```

## How It Works

```
Binary Tree:
        1
       / \
      2   3
     / \   \
    4   5   6

DFS Traversal (Pre-order): 1 → 2 → 4 → 5 → 3 → 6
DFS Traversal (In-order):  4 → 2 → 5 → 1 → 3 → 6
DFS Traversal (Post-order): 4 → 5 → 2 → 6 → 3 → 1

BFS Traversal (Level-order): 1 → 2 → 3 → 4 → 5 → 6
```

### ASCII Diagram

```
DFS (Depth-First):
        1
       / \
      2   3
     / \   \
    4   5   6

Stack-based traversal:
┌─────┬─────┬─────┬─────┬─────┬─────┐
│  1  │  3  │  5  │  4  │  2  │  6  │  (order visited)
└─────┴─────┴─────┴─────┴─────┴─────┘

BFS (Breadth-First):
        1
       / \
      2   3
     / \   \
    4   5   6

Queue-based traversal:
Level 0: [1]
Level 1: [2, 3]
Level 2: [4, 5, 6]
Order: 1 → 2 → 3 → 4 → 5 → 6
```

## Code Examples (TypeScript)

### Problem 1: Number of Islands (DFS)

```typescript
function numIslands(grid: string[][]): number {
  if (!grid || grid.length === 0) return 0;

  const rows = grid.length;
  const cols = grid[0].length;
  let count = 0;

  function dfs(r: number, c: number): void {
    if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] === '0') {
      return;
    }

    grid[r][c] = '0'; // mark as visited

    dfs(r + 1, c); // down
    dfs(r - 1, c); // up
    dfs(r, c + 1); // right
    dfs(r, c - 1); // left
  }

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (grid[r][c] === '1') {
        count++;
        dfs(r, c);
      }
    }
  }

  return count;
}

// Example
const grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
];
console.log(numIslands(grid)); // 1
```

### Problem 2: Binary Tree Level Order Traversal (BFS)

```typescript
class TreeNode {
  val: number;
  left: TreeNode | null;
  right: TreeNode | null;
  constructor(val?: number, left?: TreeNode | null, right?: TreeNode | null) {
    this.val = val ?? 0;
    this.left = left ?? null;
    this.right = right ?? null;
  }
}

function levelOrder(root: TreeNode | null): number[][] {
  if (!root) return [];

  const result: number[][] = [];
  const queue: TreeNode[] = [root];

  while (queue.length > 0) {
    const levelSize = queue.length;
    const currentLevel: number[] = [];

    for (let i = 0; i < levelSize; i++) {
      const node = queue.shift()!;
      currentLevel.push(node.val);

      if (node.left) queue.push(node.left);
      if (node.right) queue.push(node.right);
    }

    result.push(currentLevel);
  }

  return result;
}

// Example
const root = new TreeNode(3,
  new TreeNode(9),
  new TreeNode(20, new TreeNode(15), new TreeNode(7))
);
console.log(levelOrder(root)); // [[3], [9, 20], [15, 7]]
```

### Problem 3: Clone Graph (DFS with Memoization)

```typescript
class Node {
  val: number;
  neighbors: Node[];
  constructor(val?: number, neighbors?: Node[]) {
    this.val = val ?? 0;
    this.neighbors = neighbors ?? [];
  }
}

function cloneGraph(node: Node | null): Node | null {
  if (!node) return null;

  const visited = new Map<Node, Node>();

  function dfs(n: Node): Node {
    if (visited.has(n)) {
      return visited.get(n)!;
    }

    const clone = new Node(n.val);
    visited.set(n, clone);

    for (const neighbor of n.neighbors) {
      clone.neighbors.push(dfs(neighbor));
    }

    return clone;
  }

  return dfs(node);
}
```

### Problem 4: Number of Provinces (Union-Find + DFS)

```typescript
function findCircleNum(isConnected: number[][]): number {
  const n = isConnected.length;
  let provinces = 0;

  function dfs(city: number, visited: boolean[]): void {
    visited[city] = true;

    for (let neighbor = 0; neighbor < n; neighbor++) {
      if (isConnected[city][neighbor] === 1 && !visited[neighbor]) {
        dfs(neighbor, visited);
      }
    }
  }

  const visited = new Array(n).fill(false);

  for (let i = 0; i < n; i++) {
    if (!visited[i]) {
      provinces++;
      dfs(i, visited);
    }
  }

  return provinces;
}

// Example
const isConnected = [
  [1, 1, 0],
  [1, 1, 0],
  [0, 0, 1]
];
console.log(findCircleNum(isConnected)); // 2
```

### Problem 5: Rotting Oranges (BFS)

```typescript
function orangesRotting(grid: number[][]): number {
  const rows = grid.length;
  const cols = grid[0].length;
  const queue: [number, number][] = [];
  let fresh = 0;

  // Initialize queue with all rotten oranges
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (grid[r][c] === 2) {
        queue.push([r, c]);
      } else if (grid[r][c] === 1) {
        fresh++;
      }
    }
  }

  if (fresh === 0) return 0;

  let minutes = 0;
  const directions = [[0, 1], [0, -1], [1, 0], [-1, 0]];

  while (queue.length > 0) {
    const size = queue.length;
    let rotten = false;

    for (let i = 0; i < size; i++) {
      const [r, c] = queue.shift()!;

      for (const [dr, dc] of directions) {
        const nr = r + dr;
        const nc = c + dc;

        if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] === 1) {
          grid[nr][nc] = 2;
          queue.push([nr, nc]);
          fresh--;
          rotten = true;
        }
      }
    }

    if (rotten) minutes++;
  }

  return fresh === 0 ? minutes : -1;
}

// Example
const oranges = [
  [2, 1, 1],
  [1, 1, 0],
  [0, 1, 1]
];
console.log(orangesRotting(oranges)); // 4
```

### Problem 6: Word Ladder (BFS)

```typescript
function ladderLength(
  beginWord: string,
  endWord: string,
  wordList: string[]
): number {
  const wordSet = new Set(wordList);
  if (!wordSet.has(endWord)) return 0;

  const queue: [string, number][] = [[beginWord, 1]];
  const visited = new Set<string>();
  visited.add(beginWord);

  while (queue.length > 0) {
    const [word, length] = queue.shift()!;

    for (let i = 0; i < word.length; i++) {
      for (let c = 97; c <= 122; c++) { // 'a' to 'z'
        const newWord = word.substring(0, i) + String.fromCharCode(c) + word.substring(i + 1);

        if (newWord === endWord) return length + 1;

        if (wordSet.has(newWord) && !visited.has(newWord)) {
          visited.add(newWord);
          queue.push([newWord, length + 1]);
        }
      }
    }
  }

  return 0;
}

// Example
console.log(ladderLength("hit", "cog", ["hot","dot","dog","lot","log","cog"])); // 5
```

## Common Mistakes

1. **Not marking visited nodes**: Leads to infinite loops in graphs with cycles
2. **Wrong traversal order**: DFS uses stack (LIFO), BFS uses queue (FIFO)
3. **Forgetting base case**: Always check for null/empty before recursing
4. **Modifying input**: Be careful when modifying the grid/graph during traversal
5. **Not handling disconnected components**: Always iterate through all nodes

## Time/Space Complexity

| Complexity | DFS | BFS |
|------------|-----|-----|
| Time       | O(V + E) | O(V + E) |
| Space      | O(V) for recursion stack | O(V) for queue |

- **V**: Number of vertices/nodes
- **E**: Number of edges
- **DFS Space**: Can be O(V) in worst case (skewed tree)
- **BFS Space**: Can be O(V) in worst case (complete binary tree)

## Interview Problems

### Easy

1. **Binary Tree Inorder Traversal** (LeetCode 94)
2. **Maximum Depth of Binary Tree** (LeetCode 104)
3. **Same Tree** (LeetCode 100)
4. **Symmetric Tree** (LeetCode 101)

### Medium

1. **Number of Islands** (LeetCode 200)
2. **Binary Tree Level Order Traversal** (LeetCode 102)
3. **Clone Graph** (LeetCode 133)
4. **Course Schedule** (LeetCode 207)
5. **Rotting Oranges** (LeetCode 994)
6. **Flood Fill** (LeetCode 733)
7. **Max Area of Island** (LeetCode 695)

### Hard

1. **Word Ladder** (LeetCode 127)
2. **Alien Dictionary** (LeetCode 269)
3. **Longest Increasing Path in a Matrix** (LeetCode 329)
4. **Critical Connections in a Network** (LeetCode 1192)

## Summary

DFS and BFS are fundamental graph/tree traversal algorithms. DFS goes deep before wide (stack/recursion), while BFS goes wide before deep (queue). Choose based on whether you need depth-first exploration or level-by-level processing.

## Cheat Sheet

```
Pattern: DFS / BFS
Use when: Graphs, trees, mazes, connected components
Time: O(V + E) | Space: O(V)

DFS:
┌─────────────────────────────────────────┐
│ - Uses stack or recursion               │
│ - Goes deep before wide                 │
│ - Good for: paths, cycles, topological  │
│ - Mark visited before pushing           │
└─────────────────────────────────────────┘

BFS:
┌─────────────────────────────────────────┐
│ - Uses queue                            │
│ - Goes wide before deep                 │
│ - Good for: shortest path, level order  │
│ - Mark visited when pushing to queue    │
└─────────────────────────────────────────┘

When to use which?
- Shortest path → BFS
- All paths → DFS
- Level order → BFS
- Cycle detection → DFS
- Topological sort → DFS
```

---

## References & Learn More
- [LeetCode DFS/BFS](https://leetcode.com/tag/breadth-first-search/)
- [NeetCode Graphs](https://neetcode.io/)
- [CP-Algorithms](https://cp-algorithms.com/)
- [Algorithm Design by Kleinberg & Tardos](https://www.amazon.com/Algorithm-Design-Kleinberg-Jon/dp/0321295358)
- [GeeksforGeeks DFS/BFS](https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/)
