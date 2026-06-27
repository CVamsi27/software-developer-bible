# Intervals

## Definition

Interval problems involve working with ranges defined by start and end points (e.g., [start, end]). They typically require merging, inserting, or checking overlaps between intervals. Common operations include merging overlapping intervals, inserting new intervals, and finding non-overlapping intervals.

## When to Use

- Merging overlapping ranges
- Inserting intervals into a sorted list
- Checking if intervals overlap
- Finding minimum number of intervals to remove
- Meeting room problems
- Any problem involving time ranges or number lines

## Template

```typescript
function merge(intervals: number[][]): number[][] {
  intervals.sort((a, b) => a[0] - b[0]);
  const merged: number[][] = [];
  let current = intervals[0];

  for (let i = 1; i < intervals.length; i++) {
    if (intervals[i][0] <= current[1]) {
      current[1] = Math.max(current[1], intervals[i][1]);
    } else {
      merged.push(current);
      current = intervals[i];
    }
  }
  merged.push(current);
  return merged;
}
```

## How It Works

```
Intervals: [[1,3], [2,6], [8,10], [15,18]]

Sort by start: [[1,3], [2,6], [8,10], [15,18]]

Step 1: current = [1,3]
        [2,6] overlaps (2 <= 3), merge to [1,6]

Step 2: current = [1,6]
        [8,10] doesn't overlap (8 > 6), add [1,6]

Step 3: current = [8,10]
        [15,18] doesn't overlap (15 > 10), add [8,10]

Step 4: Add [15,18]

Result: [[1,6], [8,10], [15,18]]
```

### ASCII Diagram

```
MERGE INTERVALS:
Original:     [1,3]  [2,6]      [8,10]         [15,18]
              |-----|  |--------|
                          |---------|             |--------|

After sort:   [1,3]  [2,6]      [8,10]         [15,18]

Merge:        [1,6]            [8,10]         [15,18]
              |-----------|
                                |---------|
                                                  |--------|

INSERT INTERVAL:
Original:     [1,3]  [6,9]
              |-----|
                        |---------|

Insert [2,5]: [1,5]           [6,9]
              |----------|
                        |---------|

MEETING ROOMS:
Room 1:  [0,30]  [5,10]  [15,20]
         |-------------------------------|
              |----|
                   |---------|

Overlap exists! Need multiple rooms.

Room 2:  [5,10] [15,20] [30,40]
              |----|
                   |---------|
                                |---------|

No overlaps! One room enough.
```

## Code Examples (TypeScript)

### Problem 1: Merge Intervals

```typescript
function merge(intervals: number[][]): number[][] {
  if (intervals.length <= 1) return intervals;

  intervals.sort((a, b) => a[0] - b[0]);
  const merged: number[][] = [];
  let current = [...intervals[0]];

  for (let i = 1; i < intervals.length; i++) {
    if (intervals[i][0] <= current[1]) {
      current[1] = Math.max(current[1], intervals[i][1]);
    } else {
      merged.push(current);
      current = [...intervals[i]];
    }
  }

  merged.push(current);
  return merged;
}

// Example
console.log(merge([[1,3],[2,6],[8,10],[15,18]]));
// [[1,6],[8,10],[15,18]]
console.log(merge([[1,4],[4,5]]));
// [[1,5]]
```

### Problem 2: Insert Interval

```typescript
function insert(intervals: number[][], newInterval: number[]): number[][] {
  const result: number[][] = [];
  let i = 0;

  while (i < intervals.length && intervals[i][1] < newInterval[0]) {
    result.push(intervals[i]);
    i++;
  }

  while (i < intervals.length && intervals[i][0] <= newInterval[1]) {
    newInterval[0] = Math.min(newInterval[0], intervals[i][0]);
    newInterval[1] = Math.max(newInterval[1], intervals[i][1]);
    i++;
  }

  result.push(newInterval);

  while (i < intervals.length) {
    result.push(intervals[i]);
    i++;
  }

  return result;
}

// Example
console.log(insert([[1,3],[6,9]], [2,5]));
// [[1,5],[6,9]]
console.log(insert([[1,2],[3,5],[6,7],[8,10],[12,16]], [4,8]));
// [[1,2],[3,10],[12,16]]
```

### Problem 3: Meeting Rooms II

```typescript
import { MinHeap } from './07-Heap';

function minMeetingRooms(intervals: number[][]): number {
  if (intervals.length === 0) return 0;

  const sorted = [...intervals].sort((a, b) => a[0] - b[0]);
  const heap: number[] = []; // min-heap of end times

  for (const interval of sorted) {
    if (heap.length > 0 && heap[0] <= interval[0]) {
      heap.shift(); // remove earliest ending meeting
    }
    heap.push(interval[1]);
    heap.sort((a, b) => a - b); // maintain min-heap
  }

  return heap.length;
}

// Example
console.log(minMeetingRooms([[0,30],[5,10],[15,20]])); // 2
console.log(minMeetingRooms([[7,10],[2,4]])); // 1
```

### Problem 4: Non-overlapping Intervals

```typescript
function eraseOverlapIntervals(intervals: number[][]): number {
  if (intervals.length === 0) return 0;

  intervals.sort((a, b) => a[1] - b[1]);
  let count = 0;
  let end = intervals[0][1];

  for (let i = 1; i < intervals.length; i++) {
    if (intervals[i][0] < end) {
      count++; // overlapping, remove this interval
    } else {
      end = intervals[i][1]; // no overlap, update end
    }
  }

  return count;
}

// Example
console.log(eraseOverlapIntervals([[1,2],[2,3],[3,4],[1,3]])); // 1
console.log(eraseOverlapIntervals([[1,2],[1,2],[1,2]])); // 2
```

### Problem 5: Minimum Number of Arrows to Burst Balloons

```typescript
function findMinArrowShots(points: number[][]): number {
  if (points.length === 0) return 0;

  points.sort((a, b) => a[1] - b[1]);
  let arrows = 1;
  let end = points[0][1];

  for (let i = 1; i < points.length; i++) {
    if (points[i][0] > end) {
      arrows++;
      end = points[i][1];
    }
  }

  return arrows;
}

// Example
console.log(findMinArrowShots([[10,16],[2,8],[1,6],[7,12]])); // 2
console.log(findMinArrowShots([[1,2],[3,4],[5,6],[7,8]])); // 4
```

### Problem 6: Employee Free Time

```typescript
function employeeFreeTime(schedule: number[][][]): number[][] {
  const allIntervals: number[][] = [];

  for (const employee of schedule) {
    for (const interval of employee) {
      allIntervals.push(interval);
    }
  }

  allIntervals.sort((a, b) => a[0] - b[0]);

  const merged: number[][] = [allIntervals[0]];
  for (let i = 1; i < allIntervals.length; i++) {
    if (allIntervals[i][0] <= merged[merged.length - 1][1]) {
      merged[merged.length - 1][1] = Math.max(
        merged[merged.length - 1][1],
        allIntervals[i][1]
      );
    } else {
      merged.push(allIntervals[i]);
    }
  }

  const freeTime: number[][] = [];
  for (let i = 1; i < merged.length; i++) {
    freeTime.push([merged[i - 1][1], merged[i][0]]);
  }

  return freeTime;
}

// Example
const schedule = [
  [[1,2],[5,6]],
  [[1,3]],
  [[4,10]]
];
console.log(employeeFreeTime(schedule));
// [[3,4]]
```

## Common Mistakes

1. **Not sorting intervals**: Always sort by start time first
2. **Wrong comparison**: Use end time for greedy, start time for merging
3. **Off-by-one errors**: Be careful with strict vs non-strict comparisons
4. **Not handling empty input**: Check for empty arrays
5. **Modifying input**: Create copies when needed

## Time/Space Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Sort | O(n log n) | O(1) or O(n) |
| Merge | O(n) | O(n) |
| Insert | O(n) | O(n) |
| Meeting Rooms | O(n log n) | O(n) |

## Interview Problems

### Easy

1. **Merge Sorted Array** (LeetCode 88)
2. **Meeting Rooms** (LeetCode 252)

### Medium

1. **Merge Intervals** (LeetCode 56)
2. **Insert Interval** (LeetCode 57)
3. **Non-overlapping Intervals** (LeetCode 435)
4. **Minimum Number of Arrows to Burst Balloons** (LeetCode 452)
5. **Interval List Intersections** (LeetCode 986)

### Hard

1. **Meeting Rooms II** (LeetCode 253)
2. **Employee Free Time** (LeetCode 759)
3. **Maximum Number of Non-overlapping Intervals** (LeetCode 1985)

## Summary

Interval problems are common in scheduling and range-based scenarios. The key is sorting intervals appropriately and then using greedy or merging strategies.

## Cheat Sheet

```
Pattern: Intervals
Use when: Merging, inserting, checking overlaps
Time: O(n log n) | Space: O(n)

Key operations:
┌─────────────────────────────────────────┐
│ Merge: Sort by start, merge overlaps    │
│ Insert: Find position, merge if needed  │
│ Check overlap: start1 < end2 && start2 < end1 │
│ Meeting rooms: Use min-heap for end times│
└─────────────────────────────────────────┘

When to sort by:
- Start time: For merging intervals
- End time: For greedy (non-overlapping)

Key insight:
- Merge if current.start <= previous.end
- Non-overlap if current.start > previous.end
```

---

## References & Learn More
- [LeetCode Intervals](https://leetcode.com/tag/interval/)
- [NeetCode Intervals](https://neetcode.io/)
- [CP-Algorithms](https://cp-algorithms.com/)
- [Algorithm Design by Kleinberg & Tardos](https://www.amazon.com/Algorithm-Design-Kleinberg-Jon/dp/0321295358)
- [GeeksforGeeks Intervals](https://www.geeksforgeeks.org/merging-intervals/)
