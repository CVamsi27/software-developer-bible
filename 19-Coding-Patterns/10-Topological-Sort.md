# Topological Sort

## Definition

Topological Sort is a linear ordering of vertices in a Directed Acyclic Graph (DAG) such that for every directed edge (u, v), vertex u comes before vertex v in the ordering. It's used to determine the order of tasks with dependencies.

## When to Use

- Task scheduling with dependencies
- Course prerequisites
- Build systems (make, webpack)
- Spreadsheet cell dependencies
- Any problem with dependency ordering

## Template

```typescript
// Kahn's Algorithm (BFS-based)
function topologicalSortBFS(numCourses: number, prerequisites: number[][]): number[] {
  const inDegree = new Array(numCourses).fill(0);
  const graph: Map<number, number[]> = new Map();

  for (const [course, prereq] of prerequisites) {
    if (!graph.has(prereq)) graph.set(prereq, []);
    graph.get(prereq)!.push(course);
    inDegree[course]++;
  }

  const queue: number[] = [];
  for (let i = 0; i < numCourses; i++) {
    if (inDegree[i] === 0) queue.push(i);
  }

  const result: number[] = [];

  while (queue.length > 0) {
    const course = queue.shift()!;
    result.push(course);

    for (const next of graph.get(course) || []) {
      inDegree[next]--;
      if (inDegree[next] === 0) {
        queue.push(next);
      }
    }
  }

  return result.length === numCourses ? result : [];
}

// DFS-based
function topologicalSortDFS(numCourses: number, prerequisites: number[][]): number[] {
  const graph: Map<number, number[]> = new Map();
  for (const [course, prereq] of prerequisites) {
    if (!graph.has(prereq)) graph.set(prereq, []);
    graph.get(prereq)!.push(course);
  }

  const visited = new Array(numCourses).fill(0); // 0: unvisited, 1: visiting, 2: visited
  const result: number[] = [];

  function dfs(node: number): boolean {
    if (visited[node] === 1) return false; // cycle detected
    if (visited[node] === 2) return true;

    visited[node] = 1;

    for (const next of graph.get(node) || []) {
      if (!dfs(next)) return false;
    }

    visited[node] = 2;
    result.unshift(node); // add to front
    return true;
  }

  for (let i = 0; i < numCourses; i++) {
    if (!dfs(i)) return []; // cycle detected
  }

  return result;
}
```

## How It Works

```text
DAG with dependencies:
    0 → 1 → 3
    ↓   ↓
    2 → 3

Valid topological orders:
[0, 1, 2, 3]
[0, 2, 1, 3]
[2, 0, 1, 3]

Kahn's Algorithm (BFS):
1. Find all nodes with in-degree 0: [0]
2. Remove 0, update in-degrees: [1, 2] have in-degree 0
3. Remove 1, update: [2, 3] have in-degree 0
4. Remove 2, update: [3] has in-degree 0
5. Remove 3: done!

Result: [0, 1, 2, 3]
```

### ASCII Diagram

```text
KAHN'S ALGORITHM (BFS):

Initial Graph:
┌─────────────────────────────────────────┐
│     0 → 1 → 3                          │
│     ↓   ↓                              │
│     2 → 3                              │
└─────────────────────────────────────────┘

In-degrees: [0: 0, 1: 1, 2: 1, 3: 2]
Queue: [0]

Step 1: Process 0
- Remove edges 0→1, 0→2
- In-degrees: [0: 0, 1: 0, 2: 0, 3: 2]
- Queue: [1, 2]
- Result: [0]

Step 2: Process 1
- Remove edge 1→3
- In-degrees: [0: 0, 1: 0, 2: 0, 3: 1]
- Queue: [2]
- Result: [0, 1]

Step 3: Process 2
- Remove edge 2→3
- In-degrees: [0: 0, 1: 0, 2: 0, 3: 0]
- Queue: [3]
- Result: [0, 1, 2]

Step 4: Process 3
- No edges to remove
- Queue: []
- Result: [0, 1, 2, 3]

DFS-BASED:
Visit 0: exploring → visiting
Visit 1: exploring → visiting
Visit 3: exploring → visited, add to front
Back to 1: visited, add to front
Back to 0: visit 2
Visit 2: exploring → visiting
Back to 2: visited, add to front
Back to 0: visited, add to front

Result: [3, 1, 2, 0] (reverse finish order)
```

## Code Examples (TypeScript)

### Problem 1: Course Schedule

```typescript
function canFinish(numCourses: number, prerequisites: number[][]): boolean {
  const inDegree = new Array(numCourses).fill(0);
  const graph: Map<number, number[]> = new Map();

  for (const [course, prereq] of prerequisites) {
    if (!graph.has(prereq)) graph.set(prereq, []);
    graph.get(prereq)!.push(course);
    inDegree[course]++;
  }

  const queue: number[] = [];
  for (let i = 0; i < numCourses; i++) {
    if (inDegree[i] === 0) queue.push(i);
  }

  let count = 0;

  while (queue.length > 0) {
    const course = queue.shift()!;
    count++;

    for (const next of graph.get(course) || []) {
      inDegree[next]--;
      if (inDegree[next] === 0) {
        queue.push(next);
      }
    }
  }

  return count === numCourses;
}

// Example
console.log(canFinish(2, [[1,0]])); // true
console.log(canFinish(2, [[1,0],[0,1]])); // false (cycle)
```

### Problem 2: Course Schedule II

```typescript
function findOrder(numCourses: number, prerequisites: number[][]): number[] {
  const inDegree = new Array(numCourses).fill(0);
  const graph: Map<number, number[]> = new Map();

  for (const [course, prereq] of prerequisites) {
    if (!graph.has(prereq)) graph.set(prereq, []);
    graph.get(prereq)!.push(course);
    inDegree[course]++;
  }

  const queue: number[] = [];
  for (let i = 0; i < numCourses; i++) {
    if (inDegree[i] === 0) queue.push(i);
  }

  const result: number[] = [];

  while (queue.length > 0) {
    const course = queue.shift()!;
    result.push(course);

    for (const next of graph.get(course) || []) {
      inDegree[next]--;
      if (inDegree[next] === 0) {
        queue.push(next);
      }
    }
  }

  return result.length === numCourses ? result : [];
}

// Example
console.log(findOrder(2, [[1,0]])); // [0, 1]
console.log(findOrder(4, [[1,0],[2,0],[3,1],[3,2]])); // [0, 1, 2, 3]
```

### Problem 3: Alien Dictionary

```typescript
function alienOrder(words: string[]): string {
  const graph = new Map<string, Set<string>>();
  const inDegree = new Map<string, number>();

  // Initialize
  for (const word of words) {
    for (const char of word) {
      if (!graph.has(char)) graph.set(char, new Set());
      if (!inDegree.has(char)) inDegree.set(char, 0);
    }
  }

  // Build graph
  for (let i = 0; i < words.length - 1; i++) {
    const word1 = words[i];
    const word2 = words[i + 1];

    // Check for invalid case: longer word comes before shorter
    if (word1.length > word2.length && word1.startsWith(word2)) {
      return '';
    }

    for (let j = 0; j < Math.min(word1.length, word2.length); j++) {
      const char1 = word1[j];
      const char2 = word2[j];

      if (char1 !== char2) {
        if (!graph.get(char1)!.has(char2)) {
          graph.get(char1)!.add(char2);
          inDegree.set(char2, (inDegree.get(char2) || 0) + 1);
        }
        break;
      }
    }
  }

  // Topological sort
  const queue: string[] = [];
  for (const [char, degree] of inDegree) {
    if (degree === 0) queue.push(char);
  }

  const result: string[] = [];

  while (queue.length > 0) {
    const char = queue.shift()!;
    result.push(char);

    for (const next of graph.get(char) || []) {
      inDegree.set(next, inDegree.get(next)! - 1);
      if (inDegree.get(next) === 0) {
        queue.push(next);
      }
    }
  }

  return result.length === inDegree.size ? result.join('') : '';
}

// Example
console.log(alienOrder(["wrt","wrf","er","ett","rftt"]));
// "wertf"
console.log(alienOrder(["z","x"]));
// "zx"
console.log(alienOrder(["z","x","z"]));
// "" (cycle)
```

### Problem 4: Parallel Courses

```typescript
function minimumSemesters(n: number, relations: number[][]): number {
  const inDegree = new Array(n + 1).fill(0);
  const graph: Map<number, number[]> = new Map();

  for (const [prev, next] of relations) {
    if (!graph.has(prev)) graph.set(prev, []);
    graph.get(prev)!.push(next);
    inDegree[next]++;
  }

  const queue: number[] = [];
  for (let i = 1; i <= n; i++) {
    if (inDegree[i] === 0) queue.push(i);
  }

  let semesters = 0;
  let count = 0;

  while (queue.length > 0) {
    const size = queue.length;
    semesters++;

    for (let i = 0; i < size; i++) {
      const course = queue.shift()!;
      count++;

      for (const next of graph.get(course) || []) {
        inDegree[next]--;
        if (inDegree[next] === 0) {
          queue.push(next);
        }
      }
    }
  }

  return count === n ? semesters : -1;
}

// Example
console.log(minimumSemesters(3, [[1,3],[2,3]])); // 2
console.log(minimumSemesters(3, [[1,2],[2,3],[3,1]])); // -1 (cycle)
```

### Problem 5: Longest Path in DAG

```typescript
function longestPath(n: number, edges: number[][]): number[] {
  const graph: Map<number, [number, number][]> = new Map(); // node -> [(neighbor, weight)]
  const inDegree = new Array(n).fill(0);

  for (const [from, to, weight] of edges) {
    if (!graph.has(from)) graph.set(from, []);
    graph.get(from)!.push([to, weight]);
    inDegree[to]++;
  }

  const dist = new Array(n).fill(0);
  const queue: number[] = [];

  for (let i = 0; i < n; i++) {
    if (inDegree[i] === 0) queue.push(i);
  }

  while (queue.length > 0) {
    const node = queue.shift()!;

    for (const [next, weight] of graph.get(node) || []) {
      dist[next] = Math.max(dist[next], dist[node] + weight);
      inDegree[next]--;
      if (inDegree[next] === 0) {
        queue.push(next);
      }
    }
  }

  return dist;
}

// Example
console.log(longestPath(5, [[0,1,3],[0,2,2],[1,3,1],[2,3,4],[1,4,2]]));
// [0, 3, 2, 4, 5]
```

## Common Mistakes

1. **Not detecting cycles**: Topological sort only works on DAGs
2. **Wrong edge direction**: Ensure edges represent dependencies correctly
3. **Not handling all nodes**: Some nodes may have no edges
4. **Forgetting to check if valid**: Result length must equal number of nodes
5. **Not initializing in-degree**: Set all nodes with no incoming edges to 0

## Time/Space Complexity

| Algorithm | Time | Space |
|-----------|------|-------|
| Kahn's (BFS) | O(V + E) | O(V + E) |
| DFS-based | O(V + E) | O(V + E) |

- **V**: Number of vertices
- **E**: Number of edges
- Both algorithms have the same complexity

## Interview Problems

### Easy

1. **Course Schedule** (LeetCode 207)
2. **Minimum Height Trees** (LeetCode 310)

### Medium

1. **Course Schedule II** (LeetCode 210)
2. **Alien Dictionary** (LeetCode 269)
3. **Parallel Courses** (LeetCode 1136)
4. **Longest Path in DAG** (custom problem)
5. **Sort Items by Groups Respecting Dependencies** (LeetCode 1203)

### Hard

1. **All Anagrams from a Dictionary** (LeetCode 212)
2. **Parallel Courses III** (LeetCode 2050)
3. **Critical Connections in a Network** (LeetCode 1192)

## Summary

Topological sort provides a linear ordering of vertices in a DAG. It's essential for problems involving dependencies and ordering constraints. Two main approaches: Kahn's (BFS) and DFS-based.

## Cheat Sheet

```text
Pattern: Topological Sort
Use when: Dependencies, ordering, DAG processing
Time: O(V + E) | Space: O(V + E)

Algorithms:
┌─────────────────────────────────────────┐
│ 1. Kahn's Algorithm (BFS)               │
│    - Use in-degree array                │
│    - Process nodes with in-degree 0     │
│    - Decrease in-degree of neighbors    │
│    - Add to queue if in-degree becomes 0│
│                                         │
│ 2. DFS-based                            │
│    - Use visited states (0, 1, 2)       │
│    - Detect cycles with state 1         │
│    - Add to result on finish            │
│    - Reverse result for correct order   │
└─────────────────────────────────────────┘

When to use:
- Task scheduling → Kahn's
- Detecting cycles → DFS
- Need order → Kahn's
- Need to detect all cycles → DFS
```

---

## References & Learn More
- [LeetCode Topological Sort](https://leetcode.com/tag/topological-sort/)
- [NeetCode Graphs](https://neetcode.io/)
- [CP-Algorithms](https://cp-algorithms.com/)
- [Algorithm Design by Kleinberg & Tardos](https://www.amazon.com/Algorithm-Design-Kleinberg-Jon/dp/0321295358)
- [GeeksforGeeks Topological Sort](https://www.geeksforgeeks.org/topological-sorting/)
