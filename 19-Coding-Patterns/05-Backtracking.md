# Backtracking

## Definition

Backtracking is an algorithmic technique for solving problems recursively by trying to build a solution incrementally, one piece at a time, removing those solutions that fail to satisfy the constraints of the problem. It explores all possible solutions and backtracks when it finds a dead end.

## When to Use

- Finding all permutations/combinations/subsets
- Constraint satisfaction problems (N-Queens, Sudoku)
- Path finding with specific constraints
- Problems where you need to explore all possibilities
- When brute force with pruning is needed

## Template

```typescript
function backtrack(path: number[], choices: number[]): void {
  // Base case: if the current path satisfies a condition
  if (/* reached end */) {
    result.push([...path]); // make a copy
    return;
  }

  for (const choice of choices) {
    // Skip invalid choices
    if (/* choice is invalid */) continue;

    // Make a choice
    path.push(choice);

    // Recurse with updated path
    backtrack(path, choices);

    // Undo the choice (backtrack)
    path.pop();
  }
}
```

## How It Works

```
Permutations of [1, 2, 3]:

                        []
                   /    |    \
                 [1]   [2]   [3]
                / \    / \    / \
             [1,2][1,3][2,1][2,3][3,1][3,2]
              |    |    |    |    |    |
           [1,2,3][1,3,2][2,1,3][2,3,1][3,1,2][3,2,1]

Backtracking prunes invalid branches early.
```

### ASCII Diagram

```
SUBSETS OF [1, 2, 3]:

Level 0:         []
               / | \
Level 1:     [1] [2] [3]
            / \   |
Level 2: [1,2][1,3][2,3]
           |
Level 3: [1,2,3]

N-QUEENS (4x4):
Q . . .      Column 0: Q at row 0
. . Q .      Column 1: Q at row 2
. Q . .      Column 2: Q at row 1
. . . Q      Column 3: Q at row 3

No two queens attack each other!
```

## Code Examples (TypeScript)

### Problem 1: Subsets

```typescript
function subsets(nums: number[]): number[][] {
  const result: number[][] = [];

  function backtrack(start: number, current: number[]): void {
    result.push([...current]);

    for (let i = start; i < nums.length; i++) {
      current.push(nums[i]);
      backtrack(i + 1, current);
      current.pop();
    }
  }

  backtrack(0, []);
  return result;
}

// Example
console.log(subsets([1, 2, 3]));
// [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]
```

### Problem 2: Permutations

```typescript
function permute(nums: number[]): number[][] {
  const result: number[][] = [];

  function backtrack(current: number[], remaining: number[]): void {
    if (remaining.length === 0) {
      result.push([...current]);
      return;
    }

    for (let i = 0; i < remaining.length; i++) {
      current.push(remaining[i]);
      backtrack(current, [...remaining.slice(0, i), ...remaining.slice(i + 1)]);
      current.pop();
    }
  }

  backtrack([], nums);
  return result;
}

// Example
console.log(permute([1, 2, 3]));
// [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

### Problem 3: Combination Sum

```typescript
function combinationSum(candidates: number[], target: number): number[][] {
  const result: number[][] = [];
  candidates.sort((a, b) => a - b);

  function backtrack(start: number, current: number[], remaining: number): void {
    if (remaining === 0) {
      result.push([...current]);
      return;
    }

    for (let i = start; i < candidates.length; i++) {
      if (candidates[i] > remaining) break;

      current.push(candidates[i]);
      backtrack(i, current, remaining - candidates[i]);
      current.pop();
    }
  }

  backtrack(0, [], target);
  return result;
}

// Example
console.log(combinationSum([2, 3, 6, 7], 7));
// [[2,2,3], [7]]
```

### Problem 4: N-Queens

```typescript
function solveNQueens(n: number): string[][] {
  const result: string[][] = [];

  function backtrack(row: number, queens: number[]): void {
    if (row === n) {
      const board: string[] = [];
      for (let i = 0; i < n; i++) {
        let rowStr = '';
        for (let j = 0; j < n; j++) {
          rowStr += queens[i] === j ? 'Q' : '.';
        }
        board.push(rowStr);
      }
      result.push(board);
      return;
    }

    for (let col = 0; col < n; col++) {
      if (isSafe(queens, row, col)) {
        queens.push(col);
        backtrack(row + 1, queens);
        queens.pop();
      }
    }
  }

  function isSafe(queens: number[], row: number, col: number): boolean {
    for (let i = 0; i < row; i++) {
      if (queens[i] === col) return false;
      if (Math.abs(queens[i] - col) === Math.abs(i - row)) return false;
    }
    return true;
  }

  backtrack(0, []);
  return result;
}

// Example
console.log(solveNQueens(4));
// [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
```

### Problem 5: Sudoku Solver

```typescript
function solveSudoku(board: string[][]): void {
  function isValid(row: number, col: number, num: string): boolean {
    for (let i = 0; i < 9; i++) {
      if (board[row][i] === num) return false;
      if (board[i][col] === num) return false;
    }

    const boxRow = Math.floor(row / 3) * 3;
    const boxCol = Math.floor(col / 3) * 3;

    for (let i = boxRow; i < boxRow + 3; i++) {
      for (let j = boxCol; j < boxCol + 3; j++) {
        if (board[i][j] === num) return false;
      }
    }

    return true;
  }

  function solve(): boolean {
    for (let row = 0; row < 9; row++) {
      for (let col = 0; col < 9; col++) {
        if (board[row][col] === '.') {
          for (let num = 1; num <= 9; num++) {
            if (isValid(row, col, num.toString())) {
              board[row][col] = num.toString();

              if (solve()) return true;

              board[row][col] = '.';
            }
          }
          return false;
        }
      }
    }
    return true;
  }

  solve();
}

// Example usage
const sudoku = [
  ["5","3",".",".","7",".",".",".","."],
  ["6",".",".","1","9","5",".",".","."],
  [".","9","8",".",".",".",".","6","."],
  ["8",".",".",".","6",".",".",".","3"],
  ["4",".",".","8",".","3",".",".","1"],
  ["7",".",".",".","2",".",".",".","6"],
  [".","6",".",".",".",".","2","8","."],
  [".",".",".","4","1","9",".",".","5"],
  [".",".",".",".","8",".",".","7","9"]
];
solveSudoku(sudoku);
console.log(sudoku);
```

### Problem 6: Word Search

```typescript
function exist(board: string[][], word: string): boolean {
  const rows = board.length;
  const cols = board[0].length;

  function backtrack(row: number, col: number, index: number): boolean {
    if (index === word.length) return true;

    if (row < 0 || row >= rows || col < 0 || col >= cols ||
        board[row][col] !== word[index]) {
      return false;
    }

    const temp = board[row][col];
    board[row][col] = '#'; // mark as visited

    const found = backtrack(row + 1, col, index + 1) ||
                  backtrack(row - 1, col, index + 1) ||
                  backtrack(row, col + 1, index + 1) ||
                  backtrack(row, col - 1, index + 1);

    board[row][col] = temp; // restore

    return found;
  }

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (backtrack(r, c, 0)) return true;
    }
  }

  return false;
}

// Example
const board = [
  ["A","B","C","E"],
  ["S","F","C","S"],
  ["A","D","E","E"]
];
console.log(exist(board, "ABCCED")); // true
console.log(exist(board, "SEE"));    // true
console.log(exist(board, "ABCB"));   // false
```

## Common Mistakes

1. **Forgetting to backtrack**: Always undo the choice after recursion
2. **Not pruning early**: Add conditions to skip invalid branches
3. **Modifying reference instead of copy**: When adding to result, always push a copy
4. **Wrong base case**: Ensure base case covers all valid solutions
5. **Not handling duplicates**: Sort input and skip duplicates when needed

## Time/Space Complexity

| Complexity | Permutations | Combinations | Subsets |
|------------|--------------|--------------|---------|
| Time       | O(n! × n)    | O(n! × n)    | O(2^n × n) |
| Space      | O(n)         | O(n)         | O(n)    |

- **Permutations**: n! possible orderings
- **Combinations**: C(n, k) combinations
- **Subsets**: 2^n possible subsets
- **Space**: Recursion stack depth

## Interview Problems

### Easy

1. **Subsets** (LeetCode 78)
2. **Letter Combinations of a Phone Number** (LeetCode 17)
3. **Generate Parentheses** (LeetCode 22)

### Medium

1. **Permutations** (LeetCode 46)
2. **Permutations II** (LeetCode 47)
3. **Combination Sum** (LeetCode 39)
4. **Combination Sum II** (LeetCode 40)
5. **Word Search** (LeetCode 79)
6. **Palindrome Partitioning** (LeetCode 131)
7. **Subsets II** (LeetCode 90)

### Hard

1. **N-Queens** (LeetCode 51)
2. **N-Queens II** (LeetCode 52)
3. **Sudoku Solver** (LeetCode 37)
4. **Expression Add Operators** (LeetCode 282)
5. **Palindrome Permutation II** (LeetCode 267)

## Summary

Backtracking systematically explores all possible solutions by building candidates incrementally and abandoning a candidate ("backtracking") as soon as it determines the candidate cannot lead to a valid solution.

## Cheat Sheet

```
Pattern: Backtracking
Use when: All solutions, permutations, combinations, constraint satisfaction
Time: O(2^n) to O(n!) | Space: O(n)

Template:
┌─────────────────────────────────────────┐
│ 1. Start with empty path                │
│ 2. For each choice:                     │
│    a. If valid, add to path             │
│    b. Recurse                           │
│    c. Remove from path (backtrack)      │
│ 3. When path is complete, add to result │
└─────────────────────────────────────────┘

Key operations:
- Choose: path.push(choice)
- Explore: backtrack()
- Un-choose: path.pop()

Pruning techniques:
- Sort and break early
- Skip duplicates
- Validate before recursing
```

---

## References & Learn More
- [LeetCode Backtracking](https://leetcode.com/tag/backtracking/)
- [NeetCode Backtracking](https://neetcode.io/)
- [CP-Algorithms](https://cp-algorithms.com/)
- [Algorithm Design by Kleinberg & Tardos](https://www.amazon.com/Algorithm-Design-Kleinberg-Jon/dp/0321295358)
- [GeeksforGeeks Backtracking](https://www.geeksforgeeks.org/backtracking-algorithms/)
