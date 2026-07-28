---
section: SDE Role
category: Interview
tags: [guide]
---

# The Ultimate SDE Interview Preparation Guide

> **Target Roles:** SDE II / SDE III at Microsoft, Google, Amazon, Meta, Apple, Netflix, and top product-based companies.
> **Experience Level:** 3–7 years of software development experience.
> **Last Updated:** July 2026

---

## How to Use This Guide

This guide is designed to be a **single, comprehensive resource** that covers everything you need to land a job at a top product-based company. Each section includes:

- **Full Explanation** — Deep conceptual understanding with diagrams and examples
- **Code Examples** — Java implementations you can study and practice
- **LeetCode Problems** — Curated problems organized by difficulty and pattern
- **Resources** — Books, websites, videos, and courses to learn more
- **Interview Tips** — What interviewers actually look for

### Recommended Study Plan

| Phase | Topic | Hours | Priority |
|-------|-------|------:|----------|
| 1 | Java Language Mastery | 25 | 🔴 Critical |
| 2 | Time & Space Complexity | 10 | 🔴 Critical |
| 3 | Data Structures | 40 | 🔴 Critical |
| 4 | Algorithms | 30 | 🔴 Critical |
| 5 | Pattern Recognition | 60 | 🔴 Critical |
| 6 | Dynamic Programming | 40 | 🟡 High |
| 7 | Graph Algorithms | 30 | 🟡 High |
| 8 | Trees | 25 | 🟡 High |
| 9 | Bit Manipulation | 10 | 🟡 High |
| 10 | Mathematics | 15 | 🟡 High |
| 11 | OOP & Design Patterns | 25 | 🟡 High |
| 12 | Operating Systems | 20 | 🟡 High |
| 13 | Computer Networks | 20 | 🟡 High |
| 14 | Databases | 25 | 🟡 High |
| 15 | NoSQL & Distributed Systems | 15 | 🟢 Medium |
| 16 | System Design | 60 | 🔴 Critical |
| 17 | REST API Design | 15 | 🟡 High |
| 18 | Security | 15 | 🟡 High |
| 19 | Concurrency & Multithreading | 20 | 🟡 High |
| 20 | Git & DevOps | 10 | 🟢 Medium |
| 21 | Linux & Shell | 10 | 🟢 Medium |
| 22 | Behavioral Interviews | 20 | 🔴 Critical |
| 23 | Resume Deep Dive | 10 | 🔴 Critical |
| 24 | Testing | 15 | 🟡 High |
| 25 | Cloud & Infrastructure | 15 | 🟡 High |
| 26 | Frontend (Full-Stack) | 20 | 🟡 High |
| 27 | Mock Interviews & Practice | 40 | 🔴 Critical |
| 28 | Company-Specific Preparation | 15 | 🔴 Critical |

**Total: ~640 hours (~16 weeks at 40 hrs/week, or ~32 weeks at 20 hrs/week)**

---

# Phase 1: Java Language Mastery

> **Why Java?** Java is the most commonly used language in FAANG interviews due to its rich standard library, strong typing, and explicit handling of data structures. Even if you use TypeScript daily, knowing Java well gives you an edge.

## 1.1 Variables and Data Types

### Primitive Types

| Type | Size | Default | Range |
|------|------|---------|-------|
| `byte` | 1 byte | 0 | -128 to 127 |
| `short` | 2 bytes | 0 | -32,768 to 32,767 |
| `int` | 4 bytes | 0 | -2³¹ to 2³¹-1 |
| `long` | 8 bytes | 0L | -2⁶³ to 2⁶³-1 |
| `float` | 4 bytes | 0.0f | ±3.4×10³⁸ |
| `double` | 8 bytes | 0.0d | ±1.7×10³⁰⁸ |
| `char` | 2 bytes | '\u0000' | 0 to 65,535 |
| `boolean` | 1 bit | false | true/false |

### Reference Types

```java
// Strings are immutable objects
String name = "Alice";
String greeting = new String("Hello"); // heap allocated

// Arrays
int[] nums = new int[5];
String[] names = {"Alice", "Bob", "Charlie"};

// 2D Arrays
int[][] matrix = new int[3][3];
int[][] grid = {{1, 2, 3}, {4, 5, 6}};

```

### Autoboxing and Unboxing

```java
// Autoboxing: primitive → wrapper
Integer a = 10;        // int → Integer
Double b = 3.14;       // double → Double
Boolean c = true;      // boolean → Boolean

// Unboxing: wrapper → primitive
int x = a;             // Integer → int
double y = b;          // Double → double

```

### Variable Scope and Shadowing

```java
public void example() {
    int x = 10;              // method scope
    if (x > 5) {
        int y = 20;          // block scope
        System.out.println(x + y); // 30
    }
    // System.out.println(y); // ERROR: y is not in scope
}

```

## 1.2 Operators

### Arithmetic, Relational, Logical

```java
// Arithmetic
int sum = 10 + 3;      // 13
int diff = 10 - 3;     // 7
int prod = 10 * 3;     // 30
int quot = 10 / 3;     // 3 (integer division)
int rem = 10 % 3;      // 1 (modulus)

// Relational
boolean eq = 5 == 5;   // true
boolean neq = 5 != 3;  // true
boolean gt = 5 > 3;    // true
boolean lte = 5 <= 5;  // true

// Logical
boolean and = true && false;  // false
boolean or = true || false;   // true
boolean not = !true;          // false

// Bitwise
int bitwiseAnd = 5 & 3;   // 1 (0101 & 0011 = 0001)
int bitwiseOr = 5 | 3;    // 7 (0101 | 0011 = 0111)
int bitwiseXor = 5 ^ 3;   // 6 (0101 ^ 0011 = 0110)
int leftShift = 1 << 3;   // 8 (0001 → 1000)
int rightShift = 8 >> 2;  // 2 (1000 → 0010)

```

### Ternary Operator

```java
int max = (a > b) ? a : b;
String parity = (n % 2 == 0) ? "even" : "odd";

```

### instanceof

```java
Object obj = "Hello";
if (obj instanceof String) {
    String s = (String) obj;  // safe cast
}

// Pattern matching (Java 16+)
if (obj instanceof String s) {
    System.out.println(s.length());
}

```

## 1.3 Control Flow

### Loops

```java
// for loop
for (int i = 0; i < n; i++) {
    System.out.println(i);
}

// enhanced for loop (for-each)
int[] arr = {1, 2, 3, 4, 5};
for (int num : arr) {
    System.out.println(num);
}

// while loop
int i = 0;
while (i < n) {
    System.out.println(i);
    i++;
}

// do-while loop (executes at least once)
int j = 0;
do {
    System.out.println(j);
    j++;
} while (j < n);

// labeled break (useful for 2D arrays)
outer:
for (int r = 0; r < rows; r++) {
    for (int c = 0; c < cols; c++) {
        if (matrix[r][c] == target) {
            break outer;
        }
    }
}

```

## 1.4 Strings

### String Immutability

```java
String s = "Hello";
s = s + " World";  // Creates a NEW String object, "Hello" is not modified

// String pool: JVM maintains a pool of strings
String a = "hello";
String b = "hello";
System.out.println(a == b);      // true (same reference from pool)

String c = new String("hello");
System.out.println(a == c);      // false (different objects)
System.out.println(a.equals(c)); // true (same content)

```

### Essential String Methods

```java
String s = "Hello, World!";

s.length()                    // 13
s.charAt(0)                   // 'H'
s.substring(0, 5)             // "Hello"
s.substring(7)                // "World!"
s.indexOf("World")            // 7
s.indexOf('o')                // 4
s.lastIndexOf('o')            // 8
s.contains("World")           // true
s.startsWith("Hello")         // true
s.endsWith("!")               // true
s.toUpperCase()               // "HELLO, WORLD!"
s.toLowerCase()               // "hello, world!"
s.trim()                      // "Hello, World!" (removes leading/trailing spaces)
s.replace("World", "Java")    // "Hello, Java!"
s.split(", ")                 // ["Hello", "World!"]
s.toCharArray()               // ['H','e','l','l','o',',',' ','W','o','r','l','d','!']
s.equals("Hello, World!")     // true
s.equalsIgnoreCase("hello, world!") // true
s.compareTo("Hello")          // 0 (lexicographic comparison)
s.isEmpty()                   // false
s.isBlank()                   // false (Java 11+)
s.repeat(3)                   // "Hello, World!Hello, World!Hello, World!" (Java 11+)
s.strip()                     // "Hello, World!" (Unicode-aware trim)

```

### StringBuilder (Mutable)

```java
// Use StringBuilder for string concatenation in loops
StringBuilder sb = new StringBuilder();
for (int i = 0; i < n; i++) {
    sb.append(i).append(" ");
}
String result = sb.toString();

// Reverse a string
String reversed = new StringBuilder(s).reverse().toString();

// Other useful methods
sb.insert(0, "Start ");    // insert at index
sb.delete(0, 6);           // delete range [0, 6)
sb.replace(0, 5, "New");   // replace range [0, 5)
sb.charAt(0);              // get char at index
sb.length();               // current length

```

### String Comparison Patterns

```java
// NEVER use == to compare string content
String a = new String("hello");
String b = new String("hello");
System.out.println(a == b);      // false!
System.out.println(a.equals(b)); // true ✓

// Null-safe comparison
String s = null;
// s.equals("hello")  // NullPointerException!
"hello".equals(s)      // false ✓
Objects.equals(s, "hello") // false ✓

```

## 1.5 Arrays

### Array Operations

```java
// Declaration and initialization
int[] arr = new int[5];           // [0, 0, 0, 0, 0]
int[] arr2 = {1, 2, 3, 4, 5};    // literal initialization
int[] arr3 = new int[]{1, 2, 3}; // anonymous array

// Common operations
arr.length                     // 5 (not a method!)
arr[0] = 10;                   // set
int val = arr[0];              // get

// Array copy
int[] copy1 = Arrays.copyOf(arr, arr.length);
int[] copy2 = Arrays.copyOfRange(arr, 1, 4); // [arr[1], arr[2], arr[3]]
int[] copy3 = new int[arr.length];
System.arraycopy(arr, 0, copy3, 0, arr.length);

// Sorting
Arrays.sort(arr);              // ascending
Arrays.sort(arr, Collections.reverseOrder()); // descending (for Integer[], not int[])

// Searching (array MUST be sorted)
int idx = Arrays.binarySearch(arr, target);

// Fill
Arrays.fill(arr, 0);           // fill all with 0

// toString
System.out.println(Arrays.toString(arr)); // [1, 2, 3, 4, 5]

```

### 2D Arrays

```java
int[][] matrix = new int[3][3];
int[][] grid = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

// Traversal
for (int i = 0; i < grid.length; i++) {
    for (int j = 0; j < grid[i].length; j++) {
        System.out.print(grid[i][j] + " ");
    }
    System.out.println();
}

// For-each
for (int[] row : grid) {
    for (int cell : row) {
        System.out.print(cell + " ");
    }
}

```

### Key Array Patterns for Interviews

```java
// Kadane's Algorithm (Maximum Subarray Sum)
public int maxSubArray(int[] nums) {
    int maxSum = nums[0];
    int currentSum = nums[0];
    for (int i = 1; i < nums.length; i++) {
        currentSum = Math.max(nums[i], currentSum + nums[i]);
        maxSum = Math.max(maxSum, currentSum);
    }
    return maxSum;
}

// Prefix Sum
public int[] prefixSum(int[] nums) {
    int[] prefix = new int[nums.length + 1];
    for (int i = 0; i < nums.length; i++) {
        prefix[i + 1] = prefix[i] + nums[i];
    }
    return prefix;
}

// Range Sum Query: sum[l..r] = prefix[r+1] - prefix[l]

```

## 1.6 Collections Framework

### The Collections Hierarchy

```text

Iterable
├── Collection
│   ├── List (ordered, duplicates allowed)
│   │   ├── ArrayList
│   │   ├── LinkedList
│   │   └── Vector / Stack
│   ├── Set (no duplicates)
│   │   ├── HashSet
│   │   ├── LinkedHashSet
│   │   └── TreeSet
│   └── Queue (FIFO)
│       ├── PriorityQueue
│       ├── ArrayDeque
│       └── LinkedList
├── Map (key-value pairs)
│   ├── HashMap
│   ├── LinkedHashMap
│   ├── TreeMap
│   └── Hashtable

```

### ArrayList

```java
List<Integer> list = new ArrayList<>();
list.add(1);                    // [1]
list.add(2);                    // [1, 2]
list.add(0, 0);                 // [0, 1, 2] (insert at index)
list.get(0);                    // 0
list.set(0, 10);                // [10, 1, 2]
list.remove(0);                 // [1, 2]
list.remove(Integer.valueOf(1)); // [2] (remove by value)
list.contains(2);               // true
list.indexOf(2);                // 0
list.size();                    // 1
list.isEmpty();                 // false
list.clear();                   // []

// Initialize with values
List<Integer> nums = new ArrayList<>(Arrays.asList(1, 2, 3, 4, 5));

// Sort
Collections.sort(list);                          // ascending
Collections.sort(list, Collections.reverseOrder()); // descending
list.sort(Comparator.naturalOrder());             // Java 8+
list.sort(Comparator.reverseOrder());             // Java 8+

```

### LinkedList

```java
LinkedList<Integer> linkedList = new LinkedList<>();
linkedList.addFirst(1);       // [1]
linkedList.addLast(2);        // [1, 2]
linkedList.add(3);            // [1, 2, 3] (same as addLast)
linkedList.getFirst();        // 1
linkedList.getLast();         // 3
linkedList.removeFirst();     // [2, 3]
linkedList.removeLast();      // [2]

// LinkedList implements both List and Deque
// Use as Queue:
Queue<Integer> queue = new LinkedList<>();
queue.offer(1);               // add to tail
queue.poll();                 // remove from head
queue.peek();                 // peek at head

// Use as Stack:
Deque<Integer> stack = new LinkedList<>();
stack.push(1);                // add to head
stack.pop();                  // remove from head
stack.peek();                 // peek at head

```

### HashMap

```java
Map<String, Integer> map = new HashMap<>();
map.put("Alice", 90);         // add/put
map.put("Bob", 85);
map.get("Alice");              // 90
map.getOrDefault("Charlie", 0); // 0 (default if not found)
map.containsKey("Alice");     // true
map.containsValue(90);        // true
map.remove("Alice");          // delete
map.size();                   // 1
map.isEmpty();                // false
map.keySet();                 // Set<String> of keys
map.values();                 // Collection<Integer> of values
map.entrySet();               // Set<Map.Entry<String, Integer>>

// Iteration
for (Map.Entry<String, Integer> entry : map.entrySet()) {
    System.out.println(entry.getKey() + ": " + entry.getValue());
}

// Compute if absent (put if not exists)
map.putIfAbsent("Alice", 0);
map.computeIfAbsent("Alice", k -> k.length());

// Merge
map.merge("Alice", 10, Integer::sum); // adds 10 to existing value

```

### HashMap Internals (Interview Critical!)

```java
/*
 * HashMap uses an array of buckets.
 * Key's hashCode() determines the bucket index.
 *
 * Collision Resolution: Chaining (linked list in each bucket)
 *
 * Load Factor: 0.75 (default)
 * - When load > threshold, HashMap resizes (doubles capacity)
 *
 * Time Complexity:
 * - put():    O(1) average, O(n) worst case
 * - get():    O(1) average, O(n) worst case
 * - remove(): O(1) average, O(n) worst case
 *
 * In Java 8+: When a bucket has > 8 entries,
 * the linked list converts to a balanced tree (red-black tree).
 * This makes worst case O(log n) instead of O(n).
 */

```

### HashSet

```java
Set<Integer> set = new HashSet<>();
set.add(1);        // [1]
set.add(2);        // [1, 2]
set.add(1);        // [1, 2] (no duplicate)
set.contains(1);   // true
set.remove(1);     // [2]
set.size();        // 1
set.isEmpty();     // false

// Set operations
Set<Integer> a = new HashSet<>(Arrays.asList(1, 2, 3));
Set<Integer> b = new HashSet<>(Arrays.asList(2, 3, 4));

// Union
Set<Integer> union = new HashSet<>(a);
union.addAll(b);  // [1, 2, 3, 4]

// Intersection
Set<Integer> intersection = new HashSet<>(a);
intersection.retainAll(b); // [2, 3]

// Difference
Set<Integer> diff = new HashSet<>(a);
diff.removeAll(b); // [1]

```

### TreeSet (Sorted Set)

```java
TreeSet<Integer> treeSet = new TreeSet<>();
treeSet.add(3);
treeSet.add(1);
treeSet.add(2);
// Stored as [1, 2, 3] (sorted)

treeSet.first();     // 1
treeSet.last();      // 3
treeSet.lower(2);    // 1 (greatest element < 2)
treeSet.higher(2);   // 3 (smallest element > 2)
treeSet.floor(2);    // 2 (greatest element <= 2)
treeSet.ceiling(2);  // 2 (smallest element >= 2)
treeSet.pollFirst(); // 1 (remove and return smallest)
treeSet.pollLast();  // 3 (remove and return largest)

// Subset operations
treeSet.subSet(1, true, 3, true); // [1, 2, 3] (inclusive)
treeSet.headSet(2);               // [1] (elements < 2)
treeSet.tailSet(2);               // [2, 3] (elements >= 2)

```

### PriorityQueue (Heap)

```java
// Min Heap (default)
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
minHeap.offer(5);
minHeap.offer(1);
minHeap.offer(3);
minHeap.peek();      // 1
minHeap.poll();      // 1
minHeap.poll();      // 3

// Max Heap
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
maxHeap.offer(5);
maxHeap.offer(1);
maxHeap.offer(3);
maxHeap.peek();      // 5
maxHeap.poll();      // 5

// Custom Comparator
PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]); // sort by first element
PriorityQueue<String> pq2 = new PriorityQueue<>(Comparator.comparingInt(String::length));

```

### Deque (ArrayDeque)

```java
// ArrayDeque is faster than LinkedList for stack/queue operations
Deque<Integer> deque = new ArrayDeque<>();

// As Queue (FIFO)
deque.offer(1);      // add to tail
deque.offer(2);
deque.poll();        // remove from head → 1
deque.peek();        // peek at head → 2

// As Stack (LIFO)
deque.push(1);       // add to head
deque.push(2);
deque.pop();         // remove from head → 2
deque.peek();        // peek at head → 1

// Both ends
deque.offerFirst(0); // add to head
deque.offerLast(3);  // add to tail
deque.pollFirst();   // remove from head
deque.pollLast();    // remove from tail

```

## 1.7 Comparable vs Comparator

```java
// Comparable: natural ordering (implements Comparable interface)
class Student implements Comparable<Student> {
    String name;
    int age;

    @Override
    public int compareTo(Student other) {
        return this.age - other.age; // ascending by age
    }
}

// Comparator: custom ordering (passed to sort methods)
Comparator<Student> byName = Comparator.comparing(s -> s.name);
Comparator<Student> byAge = Comparator.comparingInt(s -> s.age);
Comparator<Student> byAgeDesc = byAge.reversed();
Comparator<Student> composite = byName.thenComparing(byAge);

List<Student> students = new ArrayList<>();
Collections.sort(students, byName);           // by name
students.sort(byAgeDesc);                     // by age descending
students.sort(composite);                           // by name, then by age

```

## 1.8 Lambda Expressions and Streams API

### Lambda Expressions

```java
// Functional Interface: interface with exactly one abstract method
@FunctionalInterface
interface Calculator {
    int calculate(int a, int b);
}

// Lambda syntax
Calculator add = (a, b) -> a + b;
Calculator multiply = (a, b) -> a * b;

// With body
Calculator divide = (a, b) -> {
    if (b == 0) throw new ArithmeticException("Division by zero");
    return a / b;
};

// No parameters
Runnable runnable = () -> System.out.println("Hello");

// Method references (shorthand for lambdas)
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
names.forEach(name -> System.out.println(name));  // lambda
names.forEach(System.out::println);                // method reference

```

### Streams API

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

// Filter
List<Integer> even = numbers.stream()
    .filter(n -> n % 2 == 0)
    .collect(Collectors.toList());  // [2, 4, 6, 8, 10]

// Map
List<String> strings = numbers.stream()
    .map(n -> "Number: " + n)
    .collect(Collectors.toList());

// Reduce
int sum = numbers.stream()
    .reduce(0, Integer::sum);  // 55

// Sort
List<Integer> sorted = numbers.stream()
    .sorted(Comparator.reverseOrder())
    .collect(Collectors.toList());

// Distinct
List<Integer> unique = Arrays.asList(1, 1, 2, 2, 3).stream()
    .distinct()
    .collect(Collectors.toList());  // [1, 2, 3]

// Grouping
Map<Boolean, List<Integer>> grouped = numbers.stream()
    .collect(Collectors.groupingBy(n -> n % 2 == 0));

// Partitioning
Map<Boolean, List<Integer>> partitioned = numbers.stream()
    .collect(Collectors.partitioningBy(n -> n > 5));

// Counting
long count = numbers.stream()
    .filter(n -> n > 5)
    .count();  // 5

// Min/Max
int min = numbers.stream().min(Integer::compare).orElse(-1);
int max = numbers.stream().max(Integer::compare).orElse(-1);

// Any/All/None Match
boolean anyEven = numbers.stream().anyMatch(n -> n % 2 == 0);   // true
boolean allPositive = numbers.stream().allMatch(n -> n > 0);    // true
boolean noneNegative = numbers.stream().noneMatch(n -> n < 0);  // true

// FlatMap
List<List<Integer>> nested = Arrays.asList(
    Arrays.asList(1, 2),
    Arrays.asList(3, 4),
    Arrays.asList(5, 6)
);
List<Integer> flat = nested.stream()
    .flatMap(Collection::stream)
    .collect(Collectors.toList());  // [1, 2, 3, 4, 5, 6]

// String operations
String joined = Arrays.asList("A", "B", "C").stream()
    .collect(Collectors.joining(", "));  // "A, B, C"

// Stats
IntSummaryStatistics stats = numbers.stream()
    .mapToInt(Integer::intValue)
    .summaryStatistics();
// count=10, sum=55, min=1, max=10, average=5.5

// Custom Collectors
Map<Integer, List<Integer>> byRemainder = numbers.stream()
    .collect(Collectors.groupingBy(n -> n % 3));

```

## 1.9 Optional

```java
// Avoid NullPointerException
Optional<String> opt = Optional.ofNullable(getName());
opt.ifPresent(name -> System.out.println(name));
String name = opt.orElse("Unknown");
String name2 = opt.orElseThrow(() -> new RuntimeException("Name not found"));

// Chaining
String result = Optional.ofNullable(user)
    .map(User::getAddress)
    .map(Address::getCity)
    .orElse("Unknown");

// Filtering
Optional<Integer> filtered = Optional.of(10)
    .filter(n -> n > 5);  // Optional[10]
Optional<Integer> empty = Optional.of(5)
    .filter(n -> n > 5);  // Optional.empty()

```

## 1.10 Exception Handling

```java
// Try-Catch-Finally
try {
    int result = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("Error: " + e.getMessage());
} finally {
    System.out.println("Always executes");
}

// Multi-catch
try {
    // code
} catch (IOException | SQLException e) {
    // handle both
}

// Try-with-resources (AutoCloseable)
try (BufferedReader br = new BufferedReader(new FileReader("file.txt"))) {
    String line = br.readLine();
} // br is automatically closed

// Custom exceptions
class InsufficientFundsException extends Exception {
    private double deficit;

    public InsufficientFundsException(double deficit) {
        super("Insufficient funds. Deficit: " + deficit);
        this.deficit = deficit;
    }

    public double getDeficit() { return deficit; }
}

// Checked vs Unchecked
// Checked: IOException, SQLException → must catch or declare (throws)
// Unchecked: NullPointerException, ArrayIndexOutOfBounds → runtime exceptions

```

## 1.11 Enums

```java
// Basic enum
enum Direction {
    NORTH, SOUTH, EAST, WEST
}

// Enum with fields and methods
enum Planet {
    MERCURY(3.303e+23, 2.4397e6),
    VENUS(4.869e+24, 6.0518e6),
    EARTH(5.976e+24, 6.37814e6);

    private final double mass;
    private final double radius;

    Planet(double mass, double radius) {
        this.mass = mass;
        this.radius = radius;
    }

    double surfaceGravity() {
        final double G = 6.67300E-11;
        return G * mass / (radius * radius);
    }
}

// Enum in switch
Direction dir = Direction.NORTH;
switch (dir) {
    case NORTH -> System.out.println("Going north");
    case SOUTH -> System.out.println("Going south");
    case EAST -> System.out.println("Going east");
    case WEST -> System.out.println("Going west");
}

// Useful enum methods
Direction.NORTH.name();        // "NORTH"
Direction.valueOf("NORTH");    // Direction.NORTH
Direction.values();            // [NORTH, SOUTH, EAST, WEST]

```

## 1.12 Generics

```java
// Generic class
class Box<T> {
    private T content;

    public Box(T content) { this.content = content; }
    public T getContent() { return content; }
    public void setContent(T content) { this.content = content; }
}

Box<Integer> intBox = new Box<>(10);
Box<String> strBox = new Box<>("Hello");

// Bounded type parameters
class MathUtils {
    public static <T extends Comparable<T>> T max(T a, T b) {
        return a.compareTo(b) >= 0 ? a : b;
    }
}

// Wildcards
List<Integer> intList = Arrays.asList(1, 2, 3);
List<Number> numList = new ArrayList<>();

// Upper bounded wildcard (read)
public double sum(List<? extends Number> list) {
    return list.stream().mapToDouble(Number::doubleValue).sum();
}

// Lower bounded wildcard (write)
public void addNumbers(List<? super Integer> list) {
    list.add(1);
    list.add(2);
}

// Unbounded wildcard (read only)
public void printList(List<?> list) {
    for (Object item : list) {
        System.out.println(item);
    }
}

```

## 1.13 Multithreading Basics

```java
// Thread creation
// 1. Extending Thread
class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("Thread running: " + getName());
    }
}

// 2. Implementing Runnable
Runnable task = () -> System.out.println("Runnable running");
new Thread(task).start();

// 3. Callable (returns result)
Callable<Integer> callable = () -> {
    Thread.sleep(1000);
    return 42;
};
ExecutorService executor = Executors.newSingleThreadExecutor();
Future<Integer> future = executor.submit(callable);
int result = future.get(); // blocks until done

// Synchronization
class Counter {
    private int count = 0;

    public synchronized void increment() {
        count++; // thread-safe
    }

    public void decrement() {
        synchronized (this) {
            count--;
        }
    }
}

// ReentrantLock
ReentrantLock lock = new ReentrantLock();
lock.lock();
try {
    // critical section
} finally {
    lock.unlock();
}

// Wait/Notify
class ProducerConsumer {
    private final Queue<Integer> queue = new LinkedList<>();
    private final int CAPACITY = 10;

    public synchronized void produce(int item) throws InterruptedException {
        while (queue.size() == CAPACITY) {
            wait();
        }
        queue.add(item);
        notifyAll();
    }

    public synchronized int consume() throws InterruptedException {
        while (queue.isEmpty()) {
            wait();
        }
        int item = queue.poll();
        notifyAll();
        return item;
    }
}

```

### ExecutorService

```java
// Thread pools
ExecutorService fixed = Executors.newFixedThreadPool(4);
ExecutorService cached = Executors.newCachedThreadPool();
ExecutorService single = Executors.newSingleThreadExecutor();
ExecutorService scheduled = Executors.newScheduledThreadPool(4);

// Submit tasks
fixed.submit(() -> System.out.println("Task 1"));
fixed.submit(() -> System.out.println("Task 2"));

// Shutdown
fixed.shutdown();
fixed.awaitTermination(5, TimeUnit.SECONDS);

// CompletableFuture (modern async)
CompletableFuture.supplyAsync(() -> fetchDataFromAPI())
    .thenApply(data -> process(data))
    .thenAccept(result -> System.out.println(result))
    .exceptionally(ex -> {
        System.out.println("Error: " + ex.getMessage());
        return null;
    });

```

### Resources for Java

- 📘 **Book:** *Effective Java* by Joshua Bloch (MUST READ)
- 📘 **Book:** *Head First Java* by Kathy Sierra (beginners)
- 📘 **Book:** *Java Concurrency in Practice* by Brian Goetz
- 🌐 **Website:** [Oracle Java Tutorials](https://docs.oracle.com/javase/tutorial/)
- 🌐 **Website:** [Baeldung](https://www.baeldung.com/) — excellent Java tutorials
- 🎥 **YouTube:** [Telusko](https://www.youtube.com/@Telusko) — Java full course
- 🎥 **YouTube:** [Java Brain](https://www.youtube.com/@JavaBrainsChannel) — Java concepts

---

# Phase 2: Time & Space Complexity

> **Why It Matters:** Every interview question expects you to analyze complexity. Being able to quickly identify the complexity of your solution and explain trade-offs is essential.

## Big O Notation

Big O notation describes the **upper bound** of an algorithm's growth rate. We care about the **worst case** because it guarantees performance.

### Common Complexities

| Complexity | Name | Example | Operations for n=10⁶ |
|-----------|------|---------|---------------------|
| O(1) | Constant | Array access, HashMap lookup | 1 |
| O(log n) | Logarithmic | Binary search | 20 |
| O(n) | Linear | Linear search, single loop | 1,000,000 |
| O(n log n) | Linearithmic | Merge sort, Quick sort (avg) | 20,000,000 |
| O(n²) | Quadratic | Nested loops | 10¹² (too slow!) |
| O(n³) | Cubic | Triple nested loops | 10¹⁸ (way too slow!) |
| O(2ⁿ) | Exponential | Subsets, brute force recursion | 10³⁰⁰⁰⁰ (impossible) |
| O(n!) | Factorial | Permutations | Even worse! |

### How to Analyze Complexity

```java
// O(1) — Constant
int x = arr[5];           // array access
map.get(key);              // HashMap lookup
stack.push(val);           // Stack push

// O(n) — Linear
for (int i = 0; i < n; i++) {
    System.out.println(arr[i]);
}

// O(n²) — Quadratic
for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
        System.out.println(arr[i] + arr[j]);
    }
}

// O(log n) — Logarithmic
int low = 0, high = n - 1;
while (low <= high) {
    int mid = low + (high - low) / 2;
    if (arr[mid] == target) break;
    else if (arr[mid] < target) low = mid + 1;
    else high = mid - 1;
}

// O(n log n) — Linearithmic (e.g., Merge Sort)
// The n comes from iterating, the log n from dividing

// O(2^n) — Exponential
void generateSubsets(int[] arr, int index, List<Integer> current) {
    if (index == arr.length) {
        System.out.println(current);
        return;
    }
    // Include current element
    current.add(arr[index]);
    generateSubsets(arr, index + 1, current);
    current.remove(current.size() - 1);
    // Exclude current element
    generateSubsets(arr, index + 1, current);
}

```

### Space Complexity

```java
// O(1) space
int sum = 0;
for (int i = 0; i < n; i++) sum += i;

// O(n) space
int[] result = new int[n];
Map<String, Integer> map = new HashMap<>(); // up to n entries

// O(n) space — recursion stack
void traverse(TreeNode node) {
    if (node == null) return;
    traverse(node.left);   // depth = O(n) for skewed tree
    traverse(node.right);
}

// O(log n) space — balanced recursion
void traverseBalanced(TreeNode node) {
    if (node == null) return;
    traverseBalanced(node.left);   // depth = O(log n) for balanced tree
    traverseBalanced(node.right);
}

```

### Amortized Analysis

```java
/*
 * ArrayList.add() is O(1) amortized.
 *
 * When the internal array is full, it doubles in size.
 * Copying all elements takes O(n), but this happens rarely.
 * Over n additions:
 * - Most adds: O(1)
 * - Some adds: O(n) (when resizing)
 * - Average: O(1) per operation
 *
 * Similarly, HashMap.resize() is O(n) but amortized O(1).
 */

```

### Quick Reference: When to Use What

| Situation | Complexity | Algorithm |
|-----------|-----------|-----------|
| Search in sorted array | O(log n) | Binary Search |
| Find max/min in unsorted | O(n) | Linear Scan |
| Sort n elements | O(n log n) | Merge/Quick Sort |
| Check all pairs | O(n²) | Nested loops |
| Generate all subsets | O(2ⁿ) | Backtracking |
| Generate all permutations | O(n!) | Backtracking |

### Resources for Complexity Analysis

- 📘 **Book:** *Introduction to Algorithms* (CLRS) — Chapter on asymptotic analysis
- 🌐 **Website:** [Big O Cheat Sheet](https://www.bigocheatsheet.com/)
- 🌐 **Website:** [VisuAlgo](https://visualgo.net/) — visual algorithm animations
- 🎥 **YouTube:** [Abdul Bari](https://www.youtube.com/@abdul_bari) — algorithm complexity
- 🌐 **Website:** [Complexity Zoo](https://complexityzoo.net/)

---

# Phase 3: Data Structures

> **Why It Matters:** Data structures are the building blocks of algorithms. Choosing the right data structure can mean the difference between O(n²) and O(n log n).

## 3.1 Arrays

### When to Use
- Need fast random access: O(1)
- Know the size in advance
- Don't need frequent insertions/deletions

### Key Operations
| Operation | Time | Notes |
|-----------|------|-------|
| Access by index | O(1) | |
| Search (unsorted) | O(n) | |
| Search (sorted) | O(log n) | Binary search |
| Insert at end | O(1) amortized | |
| Insert at middle | O(n) | Must shift elements |
| Delete at middle | O(n) | Must shift elements |

### Problems to Practice

| Problem | Difficulty | Pattern |
|---------|-----------|---------|
| [Two Sum](https://leetcode.com/problems/two-sum/) | Easy | HashMap |
| [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | Easy | Kadane's |
| [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | Medium | Kadane's |
| [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | Medium | Prefix/Suffix |
| [Merge Intervals](https://leetcode.com/problems/merge-intervals/) | Medium | Sorting |
| [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Hard | Two Pointers |
| [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Medium | Two Pointers |
| [3Sum](https://leetcode.com/problems/3sum/) | Medium | Two Pointers + Sort |
| [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | Medium | Prefix Sum + HashMap |
| [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) | Medium | DP / Track min/max |

## 3.2 Strings

### When to Use
- Text processing
- Character manipulation
- Pattern matching

### Key Operations
| Operation | Time | Notes |
|-----------|------|-------|
| Length | O(1) | |
| Access char | O(1) | |
| Concatenation | O(n) | Use StringBuilder |
| Substring | O(n) | |
| Search | O(n*m) | Brute force |
| Compare | O(min(n,m)) | |

### Essential String Patterns

```java
// Sliding Window for substrings
public int lengthOfLongestSubstring(String s) {
    Map<Character, Integer> map = new HashMap<>();
    int maxLen = 0;
    int left = 0;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        if (map.containsKey(c)) {
            left = Math.max(left, map.get(c) + 1);
        }
        map.put(c, right);
        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}

// Character frequency counting
public boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    int[] count = new int[26];
    for (int i = 0; i < s.length(); i++) {
        count[s.charAt(i) - 'a']++;
        count[t.charAt(i) - 'a']--;
    }
    for (int c : count) {
        if (c != 0) return false;
    }
    return true;
}

```

### Problems to Practice

| Problem | Difficulty | Pattern |
|---------|-----------|---------|
| [Valid Anagram](https://leetcode.com/problems/valid-anagram/) | Easy | Frequency Count |
| [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Medium | Sliding Window |
| [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | Medium | Expand Around Center |
| [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | Medium | HashMap + Sort |
| [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | Hard | Sliding Window |
| [Palindrome Pairs](https://leetcode.com/problems/palindrome-pairs/) | Hard | Trie + HashMap |
| [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | Medium | Sliding Window |
| [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Easy | Stack |

## 3.3 Linked List

### Singly Linked List Implementation

```java
class ListNode {
    int val;
    ListNode next;

    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

class LinkedList {
    ListNode head;
    int size;

    // Insert at beginning — O(1)
    public void addFirst(int val) {
        head = new ListNode(val, head);
        size++;
    }

    // Insert at end — O(n)
    public void addLast(int val) {
        if (head == null) {
            head = new ListNode(val);
        } else {
            ListNode curr = head;
            while (curr.next != null) curr = curr.next;
            curr.next = new ListNode(val);
        }
        size++;
    }

    // Delete by value — O(n)
    public void delete(int val) {
        if (head == null) return;
        if (head.val == val) {
            head = head.next;
            size--;
            return;
        }
        ListNode curr = head;
        while (curr.next != null && curr.next.val != val) {
            curr = curr.next;
        }
        if (curr.next != null) {
            curr.next = curr.next.next;
            size--;
        }
    }

    // Reverse — O(n) time, O(1) space
    public void reverse() {
        ListNode prev = null, curr = head;
        while (curr != null) {
            ListNode next = curr.next;
            curr.next = prev;
            prev = curr;
            curr = next;
        }
        head = prev;
    }

    // Detect cycle (Floyd's) — O(n) time, O(1) space
    public boolean hasCycle() {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) return true;
        }
        return false;
    }

    // Find middle element — O(n)
    public ListNode findMiddle() {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }
}

```

### Doubly Linked List

```java
class DoublyListNode {
    int val;
    DoublyListNode prev, next;

    DoublyListNode(int val) { this.val = val; }
}

```

### Key Linked List Patterns

```java
// Fast and Slow Pointers
// - Detect cycle
// - Find middle
// - Find start of cycle
// - Check palindrome

// Two Pointers
// - Merge two sorted lists
// - Remove nth node from end
// - Reverse in groups of k

// Dummy Head
// - Simplifies edge cases (head deletion, merging)
ListNode dummy = new ListNode(0);
dummy.next = head;
// ... operations ...
return dummy.next;

```

### Problems to Practice

| Problem | Difficulty | Pattern |
|---------|-----------|---------|
| [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | Easy | In-place reversal |
| [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | Easy | Two Pointers |
| [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | Easy | Fast/Slow Pointers |
| [Remove Nth Node From End](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | Medium | Two Pointers |
| [Reorder List](https://leetcode.com/problems/reorder-list/) | Medium | Split + Reverse + Merge |
| [LRU Cache](https://leetcode.com/problems/lru-cache/) | Medium | HashMap + Doubly LL |
| [Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | Medium | Simulation |
| [Swap Nodes in Pairs](https://leetcode.com/problems/swap-nodes-in-pairs/) | Medium | Pointer manipulation |
| [Rotate List](https://leetcode.com/problems/rotate-list/) | Medium | Cycle + Cut |
| [Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) | Medium | HashMap / Interleaving |

## 3.4 Stack

### Stack Implementation

```java
// Using ArrayDeque (preferred)
Deque<Integer> stack = new ArrayDeque<>();
stack.push(1);
stack.push(2);
stack.push(3);
int top = stack.peek();    // 3
int popped = stack.pop();  // 3
boolean empty = stack.isEmpty();

// Using ArrayList
class Stack<T> {
    private ArrayList<T> list = new ArrayList<>();

    public void push(T item) { list.add(item); }
    public T pop() { return list.remove(list.size() - 1); }
    public T peek() { return list.get(list.size() - 1); }
    public boolean isEmpty() { return list.isEmpty(); }
    public int size() { return list.size(); }
}

```

### Monotonic Stack

```java
// Next Greater Element pattern
public int[] nextGreaterElement(int[] nums) {
    int[] result = new int[nums.length];
    Deque<Integer> stack = new ArrayDeque<>(); // stores indices

    for (int i = nums.length - 1; i >= 0; i--) {
        while (!stack.isEmpty() && nums[stack.peek()] <= nums[i]) {
            stack.pop();
        }
        result[i] = stack.isEmpty() ? -1 : nums[stack.peek()];
        stack.push(i);
    }
    return result;
}

// Daily Temperatures
public int[] dailyTemperatures(int[] temperatures) {
    int[] result = new int[temperatures.length];
    Deque<Integer> stack = new ArrayDeque<>();

    for (int i = 0; i < temperatures.length; i++) {
        while (!stack.isEmpty() && temperatures[i] > temperatures[stack.peek()]) {
            int prev = stack.pop();
            result[prev] = i - prev;
        }
        stack.push(i);
    }
    return result;
}

```

### Problems to Practice

| Problem | Difficulty | Pattern |
|---------|-----------|---------|
| [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Easy | Stack matching |
| [Min Stack](https://leetcode.com/problems/min-stack/) | Medium | Auxiliary stack |
| [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | Medium | Stack simulation |
| [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | Medium | Monotonic stack |
| [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | Hard | Monotonic stack |
| [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Hard | Monotonic stack |
| [Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/) | Medium | Monotonic stack (circular) |
| [Car Fleet](https://leetcode.com/problems/car-fleet/) | Medium | Sort + Stack |
| [Asteroid Collision](https://leetcode.com/problems/asteroid-collision/) | Medium | Stack simulation |
| [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) | Medium | Stack/Backtracking |

## 3.5 Queue and Deque

```java
// Queue interface
Queue<Integer> queue = new LinkedList<>();
queue.offer(1);   // add to tail
queue.poll();     // remove from head
queue.peek();     // peek at head

// Deque interface (double-ended queue)
Deque<Integer> deque = new ArrayDeque<>();
deque.offerFirst(1);  // add to head
deque.offerLast(2);   // add to tail
deque.pollFirst();    // remove from head
deque.pollLast();     // remove from tail

// BFS template using Queue
public void bfs(TreeNode root) {
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    while (!queue.isEmpty()) {
        int size = queue.size(); // process level by level
        for (int i = 0; i < size; i++) {
            TreeNode node = queue.poll();
            // process node
            if (node.left != null) queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
    }
}

```

## 3.6 Heap (Priority Queue)

```java
// Min Heap — O(log n) insert, O(log n) extract min
PriorityQueue<Integer> minHeap = new PriorityQueue<>();

// Max Heap — O(log n) insert, O(log n) extract max
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());

// Top K pattern
public int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int num : nums) {
        freq.put(num, freq.getOrDefault(num, 0) + 1);
    }

    // Min heap of size k
    PriorityQueue<Map.Entry<Integer, Integer>> pq =
        new PriorityQueue<>((a, b) -> a.getValue() - b.getValue());

    for (Map.Entry<Integer, Integer> entry : freq.entrySet()) {
        pq.offer(entry);
        if (pq.size() > k) pq.poll();
    }

    int[] result = new int[k];
    for (int i = 0; i < k; i++) {
        result[i] = pq.poll().getKey();
    }
    return result;
}

```

### Problems to Practice

| Problem | Difficulty | Pattern |
|---------|-----------|---------|
| [Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | Easy | Min Heap |
| [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | Medium | Heap / Bucket Sort |
| [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | Hard | Two Heaps |
| [Task Scheduler](https://leetcode.com/problems/task-scheduler/) | Medium | Greedy + Heap |
| [Merge K Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | Hard | Min Heap |
| [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | Medium | Max Heap |
| [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | Hard | Monotonic Deque |
| [Employee Free Time](https://leetcode.com/problems/employee-free-time/) | Hard | Min Heap + Merge |
| [Reorganize String](https://leetcode.com/problems/reorganize-string/) | Medium | Greedy + Heap |
| [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | Medium | BFS + Priority Queue |

## 3.7 Trees

### Binary Tree Implementation

```java
class TreeNode {
    int val;
    TreeNode left, right;

    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}

```

### Tree Traversals

```java
// Inorder (Left, Root, Right) — produces sorted order for BST
void inorder(TreeNode node) {
    if (node == null) return;
    inorder(node.left);
    System.out.println(node.val);
    inorder(node.right);
}

// Iterative Inorder
void inorderIterative(TreeNode root) {
    Deque<TreeNode> stack = new ArrayDeque<>();
    TreeNode curr = root;
    while (curr != null || !stack.isEmpty()) {
        while (curr != null) {
            stack.push(curr);
            curr = curr.left;
        }
        curr = stack.pop();
        System.out.println(curr.val);
        curr = curr.right;
    }
}

// Preorder (Root, Left, Right) — used for serialization
void preorder(TreeNode node) {
    if (node == null) return;
    System.out.println(node.val);
    preorder(node.left);
    preorder(node.right);
}

// Postorder (Left, Right, Root) — used for deletion
void postorder(TreeNode node) {
    if (node == null) return;
    postorder(node.left);
    postorder(node.right);
    System.out.println(node.val);
}

// Level Order (BFS)
List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    if (root == null) return result;

    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);

    while (!queue.isEmpty()) {
        int size = queue.size();
        List<Integer> level = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            TreeNode node = queue.poll();
            level.add(node.val);
            if (node.left != null) queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
        result.add(level);
    }
    return result;
}

```

### Binary Search Tree (BST)

```java
class BST {
    TreeNode root;

    // Insert — O(log n) average
    TreeNode insert(TreeNode node, int val) {
        if (node == null) return new TreeNode(val);
        if (val < node.val) node.left = insert(node.left, val);
        else if (val > node.val) node.right = insert(node.right, val);
        return node;
    }

    // Search — O(log n) average
    TreeNode search(TreeNode node, int val) {
        if (node == null || node.val == val) return node;
        if (val < node.val) return search(node.left, val);
        return search(node.right, val);
    }

    // Delete — O(log n) average
    TreeNode delete(TreeNode node, int val) {
        if (node == null) return null;
        if (val < node.val) {
            node.left = delete(node.left, val);
        } else if (val > node.val) {
            node.right = delete(node.right, val);
        } else {
            // Node found
            if (node.left == null) return node.right;
            if (node.right == null) return node.left;
            // Two children: replace with inorder successor
            TreeNode successor = findMin(node.right);
            node.val = successor.val;
            node.right = delete(node.right, successor.val);
        }
        return node;
    }

    TreeNode findMin(TreeNode node) {
        while (node.left != null) node = node.left;
        return node;
    }
}

```

### Trie (Prefix Tree)

```java
class TrieNode {
    TrieNode[] children = new TrieNode[26];
    boolean isEnd = false;
}

class Trie {
    TrieNode root = new TrieNode();

    public void insert(String word) {
        TrieNode node = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) {
                node.children[idx] = new TrieNode();
            }
            node = node.children[idx];
        }
        node.isEnd = true;
    }

    public boolean search(String word) {
        TrieNode node = findNode(word);
        return node != null && node.isEnd;
    }

    public boolean startsWith(String prefix) {
        return findNode(prefix) != null;
    }

    private TrieNode findNode(String s) {
        TrieNode node = root;
        for (char c : s.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) return null;
            node = node.children[idx];
        }
        return node;
    }
}

```

### More Advanced Trees

> **Note:** For Segment Tree, Fenwick Tree (BIT), and AVL Tree concepts, see [Advanced Topics](05-Advanced-Topics.md).

### Problems to Practice

| Problem | Difficulty | Pattern |
|---------|-----------|---------|
| [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | Easy | DFS/BFS |
| [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | Easy | DFS |
| [Same Tree](https://leetcode.com/problems/same-tree/) | Easy | DFS |
| [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | Medium | BFS |
| [Validate BST](https://leetcode.com/problems/validate-binary-search-tree/) | Medium | Inorder/DFS |
| [Lowest Common Ancestor](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | Medium | DFS |
| [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | Hard | BFS/DFS |
| [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | Hard | DFS |
| [Construct Binary Tree from Preorder and Inorder](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | Medium | Recursion |
| [Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | Medium | Inorder |
| [Implement Trie](https://leetcode.com/problems/implement-trie-prefix-tree/) | Medium | Trie |
| [Word Search II](https://leetcode.com/problems/word-search-ii/) | Hard | Trie + Backtracking |

## 3.8 Graphs

### Graph Representations

```java
// Adjacency List (most common)
Map<Integer, List<Integer>> graph = new HashMap<>();
// Add edge
graph.computeIfAbsent(u, k -> new ArrayList<>()).add(v);
// For undirected: also add graph.computeIfAbsent(v, k -> new ArrayList<>()).add(u);

// Adjacency List with weights
Map<Integer, List<int[]>> weightedGraph = new HashMap<>();
weightedGraph.computeIfAbsent(u, k -> new ArrayList<>()).add(new int[]{v, weight});

// 2D Grid representation
int[][] grid = new int[m][n];
// Cell (i,j) neighbors: (i-1,j), (i+1,j), (i,j-1), (i,j+1)
int[][] dirs = {{-1,0}, {1,0}, {0,-1}, {0,1}};

```

### Key Graph Algorithms

```java
// DFS — O(V + E)
void dfs(Map<Integer, List<Integer>> graph, int node, Set<Integer> visited) {
    if (visited.contains(node)) return;
    visited.add(node);
    System.out.println(node);
    for (int neighbor : graph.getOrDefault(node, new ArrayList<>())) {
        dfs(graph, neighbor, visited);
    }
}

// BFS — O(V + E)
void bfs(Map<Integer, List<Integer>> graph, int start) {
    Queue<Integer> queue = new LinkedList<>();
    Set<Integer> visited = new HashSet<>();
    queue.offer(start);
    visited.add(start);

    while (!queue.isEmpty()) {
        int node = queue.poll();
        System.out.println(node);
        for (int neighbor : graph.getOrDefault(node, new ArrayList<>())) {
            if (!visited.contains(neighbor)) {
                visited.add(neighbor);
                queue.offer(neighbor);
            }
        }
    }
}

// Topological Sort (Kahn's Algorithm — BFS)
List<Integer> topologicalSort(Map<Integer, List<Integer>> graph, int numNodes) {
    int[] inDegree = new int[numNodes];
    for (int u : graph.keySet()) {
        for (int v : graph.get(u)) {
            inDegree[v]++;
        }
    }

    Queue<Integer> queue = new LinkedList<>();
    for (int i = 0; i < numNodes; i++) {
        if (inDegree[i] == 0) queue.offer(i);
    }

    List<Integer> result = new ArrayList<>();
    while (!queue.isEmpty()) {
        int node = queue.poll();
        result.add(node);
        for (int neighbor : graph.getOrDefault(node, new ArrayList<>())) {
            inDegree[neighbor]--;
            if (inDegree[neighbor] == 0) queue.offer(neighbor);
        }
    }
    return result.size() == numNodes ? result : new ArrayList<>(); // cycle detected
}

// Dijkstra's Shortest Path — O((V + E) log V)
int[] dijkstra(Map<Integer, List<int[]>> graph, int start, int n) {
    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[start] = 0;

    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]);
    pq.offer(new int[]{start, 0});

    while (!pq.isEmpty()) {
        int[] curr = pq.poll();
        int u = curr[0], d = curr[1];
        if (d > dist[u]) continue;

        for (int[] edge : graph.getOrDefault(u, new ArrayList<>())) {
            int v = edge[0], weight = edge[1];
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                pq.offer(new int[]{v, dist[v]});
            }
        }
    }
    return dist;
}

// Union Find
class UnionFind {
    int[] parent, rank;

    UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }

    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]); // path compression
        return parent[x];
    }

    boolean union(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return false;
        if (rank[px] < rank[py]) { int temp = px; px = py; py = temp; }
        parent[py] = px;
        if (rank[px] == rank[py]) rank[px]++;
        return true;
    }
}

```

### Problems to Practice

| Problem | Difficulty | Pattern |
|---------|-----------|---------|
| [Number of Islands](https://leetcode.com/problems/number-of-islands/) | Medium | DFS/BFS |
| [Clone Graph](https://leetcode.com/problems/clone-graph/) | Medium | DFS/BFS + HashMap |
| [Course Schedule](https://leetcode.com/problems/course-schedule/) | Medium | Topological Sort |
| [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | Medium | Topological Sort |
| [Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) | Medium | Multi-source BFS |
| [Word Ladder](https://leetcode.com/problems/word-ladder/) | Hard | BFS |
| [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) | Hard | Topological Sort |
| [Network Delay Time](https://leetcode.com/problems/network-delay-time/) | Medium | Dijkstra's |
| [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | Medium | BFS + PQ |
| [Accounts Merge](https://leetcode.com/problems/accounts-merge/) | Medium | Union Find |
| [Redundant Connection](https://leetcode.com/problems/redundant-connection/) | Medium | Union Find |
| [Graph Valid Tree](https://leetcode.com/problems/graph-valid-tree/) | Medium | Union Find / DFS |

---

# Phase 4: Algorithms

## 4.1 Sorting Algorithms

### Comparison Sort

```java
// Bubble Sort — O(n²) average and worst, O(n) best
void bubbleSort(int[] arr) {
    int n = arr.length;
    for (int i = 0; i < n - 1; i++) {
        boolean swapped = false;
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                swapped = true;
            }
        }
        if (!swapped) break; // already sorted
    }
}

// Selection Sort — O(n²) always
void selectionSort(int[] arr) {
    int n = arr.length;
    for (int i = 0; i < n - 1; i++) {
        int minIdx = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIdx]) minIdx = j;
        }
        int temp = arr[i];
        arr[i] = arr[minIdx];
        arr[minIdx] = temp;
    }
}

// Insertion Sort — O(n²) worst, O(n) best
void insertionSort(int[] arr) {
    for (int i = 1; i < arr.length; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}

// Merge Sort — O(n log n) always, O(n) space
void mergeSort(int[] arr, int left, int right) {
    if (left >= right) return;
    int mid = left + (right - left) / 2;
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);
    merge(arr, left, mid, right);
}

void merge(int[] arr, int left, int mid, int right) {
    int[] temp = new int[right - left + 1];
    int i = left, j = mid + 1, k = 0;

    while (i <= mid && j <= right) {
        if (arr[i] <= arr[j]) temp[k++] = arr[i++];
        else temp[k++] = arr[j++];
    }
    while (i <= mid) temp[k++] = arr[i++];
    while (j <= right) temp[k++] = arr[j++];

    System.arraycopy(temp, 0, arr, left, temp.length);
}

// Quick Sort — O(n log n) average, O(n²) worst, O(log n) space
void quickSort(int[] arr, int low, int high) {
    if (low >= high) return;
    int pivot = partition(arr, low, high);
    quickSort(arr, low, pivot - 1);
    quickSort(arr, pivot + 1, high);
}

int partition(int[] arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
    int temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;
    return i + 1;
}

// Heap Sort — O(n log n) always, O(1) space
void heapSort(int[] arr) {
    int n = arr.length;
    // Build max heap
    for (int i = n / 2 - 1; i >= 0; i--) heapify(arr, n, i);
    // Extract elements
    for (int i = n - 1; i > 0; i--) {
        int temp = arr[0];
        arr[0] = arr[i];
        arr[i] = temp;
        heapify(arr, i, 0);
    }
}

void heapify(int[] arr, int n, int i) {
    int largest = i, left = 2 * i + 1, right = 2 * i + 2;
    if (left < n && arr[left] > arr[largest]) largest = left;
    if (right < n && arr[right] > arr[largest]) largest = right;
    if (largest != i) {
        int temp = arr[i];
        arr[i] = arr[largest];
        arr[largest] = temp;
        heapify(arr, n, largest);
    }
}

```

### Non-Comparison Sort

```java
// Counting Sort — O(n + k) time, O(k) space
void countingSort(int[] arr) {
    int max = Arrays.stream(arr).max().getAsInt();
    int[] count = new int[max + 1];
    for (int num : arr) count[num]++;

    int idx = 0;
    for (int i = 0; i <= max; i++) {
        while (count[i]-- > 0) {
            arr[idx++] = i;
        }
    }
}

// Radix Sort — O(d × (n + k)) time
void radixSort(int[] arr) {
    int max = Arrays.stream(arr).max().getAsInt();
    for (int exp = 1; max / exp > 0; exp *= 10) {
        countingSortByDigit(arr, exp);
    }
}

```

### Sorting Comparison Table

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Bubble | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Heap | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Counting | O(n + k) | O(n + k) | O(n + k) | O(k) | Yes |
| Radix | O(d(n + k)) | O(d(n + k)) | O(d(n + k)) | O(n + k) | Yes |

## 4.2 Searching Algorithms

### Binary Search

```java
// Standard Binary Search — O(log n)
int binarySearch(int[] arr, int target) {
    int low = 0, high = arr.length - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2; // avoid overflow
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}

// Lower Bound (first index where arr[i] >= target)
int lowerBound(int[] arr, int target) {
    int low = 0, high = arr.length;
    while (low < high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] < target) low = mid + 1;
        else high = mid;
    }
    return low;
}

// Upper Bound (first index where arr[i] > target)
int upperBound(int[] arr, int target) {
    int low = 0, high = arr.length;
    while (low < high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] <= target) low = mid + 1;
        else high = mid;
    }
    return low;
}

// Binary Search on Answer (Binary Search on Range)
// Example: Find minimum capacity to ship packages within D days
int minCapacity(int[] weights, int days) {
    int low = Arrays.stream(weights).max().getAsInt();
    int high = Arrays.stream(weights).sum();

    while (low < high) {
        int mid = low + (high - low) / 2;
        if (canShip(weights, days, mid)) {
            high = mid;
        } else {
            low = mid + 1;
        }
    }
    return low;
}

boolean canShip(int[] weights, int days, int capacity) {
    int currentLoad = 0, daysNeeded = 1;
    for (int w : weights) {
        if (currentLoad + w > capacity) {
            daysNeeded++;
            currentLoad = 0;
        }
        currentLoad += w;
    }
    return daysNeeded <= days;
}

```

### Problems to Practice

| Problem | Difficulty | Pattern |
|---------|-----------|---------|
| [Binary Search](https://leetcode.com/problems/binary-search/) | Easy | Standard |
| [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | Medium | Modified BS |
| [Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | Medium | Modified BS |
| [Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) | Medium | Binary Search |
| [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | Medium | BS on Answer |
| [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) | Hard | BS on Answer |
| [Capacity To Ship Packages](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | Medium | BS on Answer |
| [Find Peak Element](https://leetcode.com/problems/find-peak-element/) | Medium | Modified BS |
| [Time Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store/) | Medium | Binary Search |
| [Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) | Hard | Binary Search |

---

# Phase 5: Complete Pattern Recognition

> **The key to solving 90% of LeetCode problems is recognizing which pattern to apply.** Below are the 20 most important patterns with explanations and representative problems.

## Pattern 1: Two Pointers

**When to use:** Pair of elements in sorted array, comparing elements from both ends.

```java
// Two Sum (Sorted Array)
int[] twoSum(int[] numbers, int target) {
    int left = 0, right = numbers.length - 1;
    while (left < right) {
        int sum = numbers[left] + numbers[right];
        if (sum == target) return new int[]{left + 1, right + 1};
        else if (sum < target) left++;
        else right--;
    }
    return new int[]{-1, -1};
}

// Container With Most Water
int maxArea(int[] height) {
    int left = 0, right = height.length - 1;
    int maxArea = 0;
    while (left < right) {
        int area = Math.min(height[left], height[right]) * (right - left);
        maxArea = Math.max(maxArea, area);
        if (height[left] < height[right]) left++;
        else right--;
    }
    return maxArea;
}

```

**Problems:**
| Problem | Difficulty |
|---------|-----------|
| [Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | Medium |
| [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | Easy |
| [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Medium |
| [3Sum](https://leetcode.com/problems/3sum/) | Medium |
| [4Sum](https://leetcode.com/problems/4sum/) | Medium |
| [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Hard |

## Pattern 2: Sliding Window

**When to use:** Contiguous subarray/substring with specific properties.

```java
// Maximum Sum Subarray of Size K
int maxSum(int[] arr, int k) {
    int windowSum = 0, maxSum = 0;
    for (int i = 0; i < k; i++) windowSum += arr[i];
    maxSum = windowSum;
    for (int i = k; i < arr.length; i++) {
        windowSum += arr[i] - arr[i - k];
        maxSum = Math.max(maxSum, windowSum);
    }
    return maxSum;
}

// Longest Substring Without Repeating Characters
int lengthOfLongestSubstring(String s) {
    Map<Character, Integer> map = new HashMap<>();
    int maxLen = 0, left = 0;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        if (map.containsKey(c)) {
            left = Math.max(left, map.get(c) + 1);
        }
        map.put(c, right);
        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}

// Minimum Window Substring
String minWindow(String s, String t) {
    Map<Character, Integer> need = new HashMap<>();
    Map<Character, Integer> have = new HashMap<>();
    for (char c : t.toCharArray()) need.put(c, need.getOrDefault(c, 0) + 1);

    int haveCount = 0, needCount = need.size();
    int left = 0, minLen = Integer.MAX_VALUE, minStart = 0;

    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        have.put(c, have.getOrDefault(c, 0) + 1);
        if (need.containsKey(c) && have.get(c).equals(need.get(c))) {
            haveCount++;
        }

        while (haveCount == needCount) {
            if (right - left + 1 < minLen) {
                minLen = right - left + 1;
                minStart = left;
            }
            char leftChar = s.charAt(left);
            have.put(leftChar, have.get(leftChar) - 1);
            if (need.containsKey(leftChar) && have.get(leftChar) < need.get(leftChar)) {
                haveCount--;
            }
            left++;
        }
    }
    return minLen == Integer.MAX_VALUE ? "" : s.substring(minStart, minStart + minLen);
}

```

**Problems:**
| Problem | Difficulty |
|---------|-----------|
| [Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/) | Easy |
| [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Medium |
| [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | Medium |
| [Permutation in String](https://leetcode.com/problems/permutation-in-string/) | Medium |
| [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | Hard |
| [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | Hard |

## Pattern 3: Fast & Slow Pointers

**When to use:** Cycle detection, finding middle of linked list, happy number.

```java
// Linked List Cycle Detection
boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;
    }
    return false;
}

// Find Start of Cycle
ListNode detectCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) {
            slow = head;
            while (slow != fast) {
                slow = slow.next;
                fast = fast.next;
            }
            return slow;
        }
    }
    return null;
}

// Happy Number
boolean isHappy(int n) {
    int slow = n, fast = sumOfSquares(n);
    while (fast != 1 && slow != fast) {
        slow = sumOfSquares(slow);
        fast = sumOfSquares(sumOfSquares(fast));
    }
    return fast == 1;
}

```

**Problems:**
| Problem | Difficulty |
|---------|-----------|
| [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | Easy |
| [Happy Number](https://leetcode.com/problems/happy-number/) | Easy |
| [Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/) | Easy |
| [Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/) | Medium |
| [Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/) | Medium |

## Pattern 4: Binary Search

**When to use:** Sorted array, search space reduction, finding optimal value.

```java
// Search in Rotated Sorted Array
int search(int[] nums, int target) {
    int low = 0, high = nums.length - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (nums[mid] == target) return mid;
        if (nums[low] <= nums[mid]) { // left half sorted
            if (target >= nums[low] && target < nums[mid]) high = mid - 1;
            else low = mid + 1;
        } else { // right half sorted
            if (target > nums[mid] && target <= nums[high]) low = mid + 1;
            else high = mid - 1;
        }
    }
    return -1;
}

```

## Pattern 5: Prefix Sum

**When to use:** Range sum queries, subarray sum problems.

```java
// Subarray Sum Equals K
int subarraySum(int[] nums, int k) {
    Map<Integer, Integer> prefixSum = new HashMap<>();
    prefixSum.put(0, 1);
    int sum = 0, count = 0;
    for (int num : nums) {
        sum += num;
        if (prefixSum.containsKey(sum - k)) {
            count += prefixSum.get(sum - k);
        }
        prefixSum.put(sum, prefixSum.getOrDefault(sum, 0) + 1);
    }
    return count;
}

```

## Pattern 6: Stack (Monotonic)

**When to use:** Next greater/smaller element, histogram problems.

```java
// Next Greater Element
int[] nextGreaterElement(int[] nums) {
    int[] result = new int[nums.length];
    Deque<Integer> stack = new ArrayDeque<>();
    for (int i = nums.length - 1; i >= 0; i--) {
        while (!stack.isEmpty() && stack.peek() <= nums[i]) stack.pop();
        result[i] = stack.isEmpty() ? -1 : stack.peek();
        stack.push(nums[i]);
    }
    return result;
}

```

## Pattern 7: BFS (Level-by-Level)

**When to use:** Shortest path in unweighted graph, level order traversal.

```java
// Rotting Oranges
int orangesRotting(int[][] grid) {
    Queue<int[]> queue = new LinkedList<>();
    int fresh = 0;
    for (int i = 0; i < grid.length; i++) {
        for (int j = 0; j < grid[0].length; j++) {
            if (grid[i][j] == 2) queue.offer(new int[]{i, j});
            else if (grid[i][j] == 1) fresh++;
        }
    }
    if (fresh == 0) return 0;

    int[][] dirs = {{-1,0},{1,0},{0,-1},{0,1}};
    int minutes = 0;
    while (!queue.isEmpty()) {
        int size = queue.size();
        boolean rotten = false;
        for (int i = 0; i < size; i++) {
            int[] cell = queue.poll();
            for (int[] d : dirs) {
                int r = cell[0] + d[0], c = cell[1] + d[1];
                if (r >= 0 && r < grid.length && c >= 0 && c < grid[0].length && grid[r][c] == 1) {
                    grid[r][c] = 2;
                    queue.offer(new int[]{r, c});
                    fresh--;
                    rotten = true;
                }
            }
        }
        if (rotten) minutes++;
    }
    return fresh == 0 ? minutes : -1;
}

```

## Pattern 8: DFS (Recursive/Backtracking)

**When to use:** Permutations, combinations, subsets, path finding.

```java
// Subsets
List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, 0, new ArrayList<>(), result);
    return result;
}

void backtrack(int[] nums, int start, List<Integer> current, List<List<Integer>> result) {
    result.add(new ArrayList<>(current));
    for (int i = start; i < nums.length; i++) {
        current.add(nums[i]);
        backtrack(nums, i + 1, current, result);
        current.remove(current.size() - 1);
    }
}

```

## Pattern 9: Topological Sort

**When to use:** Task scheduling, course prerequisites, dependency resolution.

```java
// Course Schedule
boolean canFinish(int numCourses, int[][] prerequisites) {
    List<List<Integer>> graph = new ArrayList<>();
    int[] inDegree = new int[numCourses];
    for (int i = 0; i < numCourses; i++) graph.add(new ArrayList<>());

    for (int[] pre : prerequisites) {
        graph.get(pre[1]).add(pre[0]);
        inDegree[pre[0]]++;
    }

    Queue<Integer> queue = new LinkedList<>();
    for (int i = 0; i < numCourses; i++) {
        if (inDegree[i] == 0) queue.offer(i);
    }

    int count = 0;
    while (!queue.isEmpty()) {
        int course = queue.poll();
        count++;
        for (int next : graph.get(course)) {
            inDegree[next]--;
            if (inDegree[next] == 0) queue.offer(next);
        }
    }
    return count == numCourses;
}

```

## Pattern 10: Union Find

**When to use:** Connected components, cycle detection in undirected graph, dynamic connectivity.

```java
// Number of Provinces
int findCircleNum(int[][] isConnected) {
    int n = isConnected.length;
    UnionFind uf = new UnionFind(n);
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (isConnected[i][j] == 1) uf.union(i, j);
        }
    }
    return uf.count;
}

```

## Pattern 11: Greedy

**When to use:** Optimal local choices lead to global optimum.

```java
// Jump Game
boolean canJump(int[] nums) {
    int maxReach = 0;
    for (int i = 0; i < nums.length; i++) {
        if (i > maxReach) return false;
        maxReach = Math.max(maxReach, i + nums[i]);
    }
    return true;
}

// Activity Selection / Non-overlapping Intervals
int eraseOverlapIntervals(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> a[1] - b[1]);
    int count = 0, end = Integer.MIN_VALUE;
    for (int[] interval : intervals) {
        if (interval[0] >= end) {
            end = interval[1];
        } else {
            count++;
        }
    }
    return count;
}

```

## Pattern 12: Dynamic Programming

See Phase 6 for full coverage.

## Pattern 13: Backtracking

**When to use:** Generate all possibilities, prune search space.

```java
// N-Queens
List<List<String>> solveNQueens(int n) {
    List<List<String>> result = new ArrayList<>();
    char[][] board = new char[n][n];
    for (char[] row : board) Arrays.fill(row, '.');
    backtrack(board, 0, result);
    return result;
}

void backtrack(char[][] board, int row, List<List<String>> result) {
    if (row == board.length) {
        List<String> snapshot = new ArrayList<>();
        for (char[] r : board) snapshot.add(new String(r));
        result.add(snapshot);
        return;
    }
    for (int col = 0; col < board.length; col++) {
        if (isValid(board, row, col)) {
            board[row][col] = 'Q';
            backtrack(board, row + 1, result);
            board[row][col] = '.';
        }
    }
}

```

## Pattern 14: Trie

**When to use:** Word search, prefix matching, autocomplete.

## Pattern 15: Bit Manipulation

**When to use:** XOR problems, subset generation, bit masks.

```java
// Single Number
int singleNumber(int[] nums) {
    int result = 0;
    for (int num : nums) result ^= num;
    return result;
}

// Counting Bits
int[] countBits(int n) {
    int[] dp = new int[n + 1];
    for (int i = 1; i <= n; i++) {
        dp[i] = dp[i >> 1] + (i & 1);
    }
    return dp;
}

```

## Pattern 16: Merge Intervals

```java
int[][] merge(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
    List<int[]> merged = new ArrayList<>();
    for (int[] interval : intervals) {
        if (merged.isEmpty() || merged.get(merged.size() - 1)[1] < interval[0]) {
            merged.add(interval);
        } else {
            merged.get(merged.size() - 1)[1] = Math.max(
                merged.get(merged.size() - 1)[1], interval[1]);
        }
    }
    return merged.toArray(new int[0][]);
}

```

## Pattern 17: Heap / Priority Queue

**When to use:** Kth element, merge K sorted lists, scheduling.

## Pattern 18: Matrix Traversal

```java
// Spiral Matrix
List<Integer> spiralOrder(int[][] matrix) {
    List<Integer> result = new ArrayList<>();
    int top = 0, bottom = matrix.length - 1, left = 0, right = matrix[0].length - 1;

    while (top <= bottom && left <= right) {
        for (int i = left; i <= right; i++) result.add(matrix[top][i]);
        top++;
        for (int i = top; i <= bottom; i++) result.add(matrix[i][right]);
        right--;
        if (top <= bottom) {
            for (int i = right; i >= left; i--) result.add(matrix[bottom][i]);
            bottom--;
        }
        if (left <= right) {
            for (int i = bottom; i >= top; i--) result.add(matrix[i][left]);
            left++;
        }
    }
    return result;
}

```

## Pattern 19: Hashing

**When to use:** Frequency counting, two sum, grouping.

## Pattern 20: Design (LC Design Problems)

```java
// LRU Cache
class LRUCache extends LinkedHashMap<Integer, Integer> {
    private int capacity;

    public LRUCache(int capacity) {
        super(capacity, 0.75f, true);
        this.capacity = capacity;
    }

    public int get(int key) {
        return super.getOrDefault(key, -1);
    }

    public void put(int key, int value) {
        super.put(key, value);
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry eldest) {
        return size() > capacity;
    }
}

```

### Resources for Pattern Recognition

- 📘 **Book:** *Elements of Programming Interviews* by Adnan Aziz
- 📘 **Book:** *Cracking the Coding Interview* by Gayle McDowell
- 🌐 **Website:** [NeetCode.io](https://neetcode.io/) — patterns organized by category
- 🌐 **Website:** [LeetCode Patterns](https://seanprashad.com/leetcode-patterns/) — curated by pattern
- 🌐 **Website:** [Educative.io - Coding Interview Patterns](https://www.educative.io/blog/coding-interview-leetcode-patterns)
- 🎥 **YouTube:** [NeetCode](https://www.youtube.com/@NeetCode) — video explanations
- 🎥 **YouTube:** [take U forward](https://www.youtube.com/@takeUforward) — Striver's DSA Sheet

---

# Phase 6: Dynamic Programming

> **Why It Matters:** DP is the most feared topic in interviews. Master the patterns and you'll solve 80% of DP problems.

## Core Concepts

### Memoization (Top-Down) — Recursion + Cache

```java
// Fibonacci with Memoization
Map<Integer, Long> memo = new HashMap<>();

long fib(int n) {
    if (n <= 1) return n;
    if (memo.containsKey(n)) return memo.get(n);
    long result = fib(n - 1) + fib(n - 2);
    memo.put(n, result);
    return result;
}

```

### Tabulation (Bottom-Up) — Iterative

```java
// Fibonacci with Tabulation
long fib(int n) {
    if (n <= 1) return n;
    long[] dp = new long[n + 1];
    dp[0] = 0;
    dp[1] = 1;
    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    return dp[n];
}

```

### Space Optimization

```java
// Fibonacci with O(1) space
long fib(int n) {
    if (n <= 1) return n;
    long prev2 = 0, prev1 = 1;
    for (int i = 2; i <= n; i++) {
        long curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}

```

## DP Patterns

### 1. Fibonacci Pattern

```java
// Climbing Stairs
int climbStairs(int n) {
    if (n <= 2) return n;
    int[] dp = new int[n + 1];
    dp[1] = 1; dp[2] = 2;
    for (int i = 3; i <= n; i++) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    return dp[n];
}

```

**Problems:** Fibonacci, Climbing Stairs, House Robber, Min Cost Climbing Stairs

### 2. 0/1 Knapsack

```java
int knapsack(int[] weights, int[] values, int capacity) {
    int n = weights.length;
    int[][] dp = new int[n + 1][capacity + 1];

    for (int i = 1; i <= n; i++) {
        for (int w = 0; w <= capacity; w++) {
            dp[i][w] = dp[i - 1][w]; // don't take
            if (weights[i - 1] <= w) {
                dp[i][w] = Math.max(dp[i][w],
                    dp[i - 1][w - weights[i - 1]] + values[i - 1]);
            }
        }
    }
    return dp[n][capacity];
}

```

**Problems:** 0/1 Knapsack, Partition Equal Subset Sum, Target Sum, Last Stone Weight II

### 3. Unbounded Knapsack

```java
// Coin Change
int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);
    dp[0] = 0;

    for (int i = 1; i <= amount; i++) {
        for (int coin : coins) {
            if (coin <= i) {
                dp[i] = Math.min(dp[i], dp[i - coin] + 1);
            }
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}

```

**Problems:** Coin Change, Coin Change 2, Rod Cutting, Integer Break

### 4. Longest Common Subsequence (LCS)

```java
int lcs(String text1, String text2) {
    int m = text1.length(), n = text2.length();
    int[][] dp = new int[m + 1][n + 1];

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }
    return dp[m][n];
}

```

**Problems:** LCS, Edit Distance, Longest Increasing Subsequence, Shortest Common Supersequence

### 5. Longest Increasing Subsequence (LIS)

```java
// O(n²) DP
int lengthOfLIS(int[] nums) {
    int[] dp = new int[nums.length];
    Arrays.fill(dp, 1);
    int maxLen = 1;

    for (int i = 1; i < nums.length; i++) {
        for (int j = 0; j < i; j++) {
            if (nums[j] < nums[i]) {
                dp[i] = Math.max(dp[i], dp[j] + 1);
            }
        }
        maxLen = Math.max(maxLen, dp[i]);
    }
    return maxLen;
}

// O(n log n) Binary Search + Patience Sorting
int lengthOfLISOptimal(int[] nums) {
    List<Integer> sub = new ArrayList<>();
    for (int num : nums) {
        int pos = Collections.binarySearch(sub, num);
        if (pos < 0) pos = -(pos + 1);
        if (pos == sub.size()) sub.add(num);
        else sub.set(pos, num);
    }
    return sub.size();
}

```

**Problems:** LIS, Russian Doll Envelopes, Number of Longest Increasing Subsequence

### 6. Grid DP

```java
// Unique Paths
int uniquePaths(int m, int n) {
    int[][] dp = new int[m][n];
    for (int i = 0; i < m; i++) dp[i][0] = 1;
    for (int j = 0; j < n; j++) dp[0][j] = 1;

    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
        }
    }
    return dp[m - 1][n - 1];
}

// Minimum Path Sum
int minPathSum(int[][] grid) {
    int m = grid.length, n = grid[0].length;
    int[][] dp = new int[m][n];
    dp[0][0] = grid[0][0];

    for (int i = 1; i < m; i++) dp[i][0] = dp[i - 1][0] + grid[i][0];
    for (int j = 1; j < n; j++) dp[0][j] = dp[0][j - 1] + grid[0][j];

    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[i][j] = Math.min(dp[i - 1][j], dp[i][j - 1]) + grid[i][j];
        }
    }
    return dp[m - 1][n - 1];
}

```

**Problems:** Unique Paths, Unique Paths II, Minimum Path Sum, Dungeon Game, Maximal Square

### 7. Interval DP

```java
// Matrix Chain Multiplication
int matrixChainOrder(int[] dims) {
    int n = dims.length - 1;
    int[][] dp = new int[n][n];

    for (int len = 2; len <= n; len++) {
        for (int i = 0; i < n - len + 1; i++) {
            int j = i + len - 1;
            dp[i][j] = Integer.MAX_VALUE;
            for (int k = i; k < j; k++) {
                dp[i][j] = Math.min(dp[i][j],
                    dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]);
            }
        }
    }
    return dp[0][n - 1];
}

```

**Problems:** Matrix Chain Multiplication, Palindrome Partitioning, Burst Balloons

### 8. Digit DP

```java
// Count numbers with specific digit properties
// Used for problems like: count numbers from 1 to N with certain digit constraints

```

### DP Problems to Practice (by difficulty)

| Problem | Difficulty | Pattern |
|---------|-----------|---------|
| [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | Easy | Fibonacci |
| [House Robber](https://leetcode.com/problems/house-robber/) | Medium | Linear DP |
| [Coin Change](https://leetcode.com/problems/coin-change/) | Medium | Unbounded Knapsack |
| [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) | Medium | LCS |
| [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | Medium | LIS |
| [Word Break](https://leetcode.com/problems/word-break/) | Medium | Unbounded Knapsack |
| [Decode Ways](https://leetcode.com/problems/decode-ways/) | Medium | Fibonacci-like |
| [Unique Paths](https://leetcode.com/problems/unique-paths/) | Medium | Grid DP |
| [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) | Medium | Grid DP |
| [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | Medium | 0/1 Knapsack |
| [Target Sum](https://leetcode.com/problems/target-sum/) | Medium | 0/1 Knapsack |
| [Edit Distance](https://leetcode.com/problems/edit-distance/) | Medium | LCS variant |
| [Maximal Square](https://leetcode.com/problems/maximal-square/) | Medium | Grid DP |
| [Longest Palindromic Subsequence](https://leetcode.com/problems/longest-palindromic-subsequence/) | Medium | LCS variant |
| [Burst Balloons](https://leetcode.com/problems/burst-balloons/) | Hard | Interval DP |
| [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) | Hard | 2D DP |
| [Longest Valid Parentheses](https://leetcode.com/problems/longest-valid-parentheses/) | Hard | Stack/DP |

### Resources for DP

- 📘 **Book:** *Introduction to Algorithms* (CLRS) — Dynamic Programming chapter
- 📘 **Book:** *Elements of Programming Interviews* — DP chapter
- 🌐 **Website:** [LeetCode DP Study Plan](https://leetcode.com/studyplan/dynamic-programming/)
- 🎥 **YouTube:** [take U forward - DP Series](https://www.youtube.com/playlist?list=PLgZDfOG0dJyMRq1J_0xS2LqF5HgIh0y1z) — 50+ DP problems explained
- 🎥 **YouTube:** [NeetCode DP playlist](https://www.youtube.com/@NeetCode)
- 🌐 **Website:** [CP-Algorithms](https://cp-algorithms.com/) — competitive programming DP

---

# Phase 7: Graph Algorithms

## DFS and BFS

```java
// DFS — uses Stack (recursive or iterative)
void dfs(List<List<Integer>> graph, int node, boolean[] visited) {
    visited[node] = true;
    for (int neighbor : graph.get(node)) {
        if (!visited[neighbor]) dfs(graph, neighbor, visited);
    }
}

// BFS — uses Queue
void bfs(List<List<Integer>> graph, int start) {
    Queue<Integer> queue = new LinkedList<>();
    boolean[] visited = new boolean[graph.size()];
    queue.offer(start);
    visited[start] = true;

    while (!queue.isEmpty()) {
        int node = queue.poll();
        for (int neighbor : graph.get(node)) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                queue.offer(neighbor);
            }
        }
    }
}

```

## Shortest Path Algorithms

### Dijkstra's Algorithm — O((V + E) log V)

```java
// Single source shortest path (non-negative weights)
int[] dijkstra(List<List<int[]>> graph, int start) {
    int n = graph.size();
    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[start] = 0;

    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]);
    pq.offer(new int[]{start, 0});

    while (!pq.isEmpty()) {
        int[] curr = pq.poll();
        int u = curr[0], d = curr[1];
        if (d > dist[u]) continue;

        for (int[] edge : graph.get(u)) {
            int v = edge[0], weight = edge[1];
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                pq.offer(new int[]{v, dist[v]});
            }
        }
    }
    return dist;
}

```

### Bellman-Ford — O(VE)

```java
// Handles negative weights, detects negative cycles
int[] bellmanFord(int n, int[][] edges, int start) {
    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[start] = 0;

    for (int i = 0; i < n - 1; i++) {
        for (int[] edge : edges) {
            int u = edge[0], v = edge[1], w = edge[2];
            if (dist[u] != Integer.MAX_VALUE && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
            }
        }
    }
    return dist;
}

```

### Floyd-Warshall — O(V³)

```java
// All pairs shortest path
int[][] floydWarshall(int[][] dist) {
    int n = dist.length;
    for (int k = 0; k < n; k++) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (dist[i][k] != Integer.MAX_VALUE && dist[k][j] != Integer.MAX_VALUE) {
                    dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);
                }
            }
        }
    }
    return dist;
}

```

## Minimum Spanning Tree

### Kruskal's Algorithm — O(E log E)

```java
int kruskal(int n, int[][] edges) {
    Arrays.sort(edges, (a, b) -> a[2] - b[2]);
    UnionFind uf = new UnionFind(n);
    int totalWeight = 0, edgesUsed = 0;

    for (int[] edge : edges) {
        if (uf.union(edge[0], edge[1])) {
            totalWeight += edge[2];
            edgesUsed++;
            if (edgesUsed == n - 1) break;
        }
    }
    return totalWeight;
}

```

### Prim's Algorithm — O(E log V)

```java
int prim(List<List<int[]>> graph) {
    int n = graph.size();
    boolean[] visited = new boolean[n];
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]);
    pq.offer(new int[]{0, 0}); // {node, weight}
    int totalWeight = 0;

    while (!pq.isEmpty()) {
        int[] curr = pq.poll();
        int u = curr[0], w = curr[1];
        if (visited[u]) continue;
        visited[u] = true;
        totalWeight += w;

        for (int[] edge : graph.get(u)) {
            if (!visited[edge[0]]) {
                pq.offer(new int[]{edge[0], edge[1]});
            }
        }
    }
    return totalWeight;
}

```

## Topological Sort

```java
// Kahn's Algorithm (BFS-based)
List<Integer> topologicalSort(int n, List<List<Integer>> graph) {
    int[] inDegree = new int[n];
    for (int i = 0; i < n; i++) {
        for (int v : graph.get(i)) inDegree[v]++;
    }

    Queue<Integer> queue = new LinkedList<>();
    for (int i = 0; i < n; i++) {
        if (inDegree[i] == 0) queue.offer(i);
    }

    List<Integer> result = new ArrayList<>();
    while (!queue.isEmpty()) {
        int node = queue.poll();
        result.add(node);
        for (int v : graph.get(node)) {
            inDegree[v]--;
            if (inDegree[v] == 0) queue.offer(v);
        }
    }
    return result.size() == n ? result : new ArrayList<>();
}

```

## Cycle Detection

```java
// Directed graph — DFS with color (0=unvisited, 1=in progress, 2=done)
boolean hasCycle(List<List<Integer>> graph) {
    int[] color = new int[graph.size()];
    for (int i = 0; i < graph.size(); i++) {
        if (color[i] == 0 && dfsCycle(graph, i, color)) return true;
    }
    return false;
}

boolean dfsCycle(List<List<Integer>> graph, int node, int[] color) {
    color[node] = 1;
    for (int neighbor : graph.get(node)) {
        if (color[neighbor] == 1) return true; // back edge = cycle
        if (color[neighbor] == 0 && dfsCycle(graph, neighbor, color)) return true;
    }
    color[node] = 2;
    return false;
}

// Undirected graph — Union Find
boolean hasCycleUndirected(int n, int[][] edges) {
    UnionFind uf = new UnionFind(n);
    for (int[] edge : edges) {
        if (!uf.union(edge[0], edge[1])) return true; // same component = cycle
    }
    return false;
}

```

## Bipartite Graph

```java
boolean isBipartite(int[][] graph) {
    int[] color = new int[graph.length];
    Arrays.fill(color, -1);

    for (int i = 0; i < graph.length; i++) {
        if (color[i] == -1) {
            Queue<Integer> queue = new LinkedList<>();
            queue.offer(i);
            color[i] = 0;
            while (!queue.isEmpty()) {
                int node = queue.poll();
                for (int neighbor : graph[node]) {
                    if (color[neighbor] == -1) {
                        color[neighbor] = 1 - color[node];
                        queue.offer(neighbor);
                    } else if (color[neighbor] == color[node]) {
                        return false;
                    }
                }
            }
        }
    }
    return true;
}

```

## Strongly Connected Components (Kosaraju's Algorithm)

```java
// Step 1: Get finish order with DFS
// Step 2: Transpose graph
// Step 3: DFS on transposed graph in reverse finish order

```

## Graph Problems to Practice

| Problem | Difficulty | Pattern |
|---------|-----------|---------|
| [Number of Islands](https://leetcode.com/problems/number-of-islands/) | Medium | DFS/BFS |
| [Clone Graph](https://leetcode.com/problems/clone-graph/) | Medium | DFS/BFS |
| [Course Schedule](https://leetcode.com/problems/course-schedule/) | Medium | Topological Sort |
| [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | Medium | Topological Sort |
| [Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) | Medium | Multi-source BFS |
| [Word Ladder](https://leetcode.com/problems/word-ladder/) | Hard | BFS |
| [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) | Hard | Topological Sort |
| [Network Delay Time](https://leetcode.com/problems/network-delay-time/) | Medium | Dijkstra's |
| [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | Medium | BFS + PQ |
| [Accounts Merge](https://leetcode.com/problems/accounts-merge/) | Medium | Union Find |
| [Redundant Connection](https://leetcode.com/problems/redundant-connection/) | Medium | Union Find |
| [Graph Valid Tree](https://leetcode.com/problems/graph-valid-tree/) | Medium | Union Find |
| [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | Medium | Union Find |
| [Is Graph Bipartite?](https://leetcode.com/problems/is-graph-bipartite/) | Medium | BFS/DFS coloring |
| [Number of Provinces](https://leetcode.com/problems/number-of-provinces/) | Medium | Union Find/DFS |
| [Evaluate Division](https://leetcode.com/problems/evaluate-division/) | Medium | BFS/DFS on graph |
| [Reconstruct Itinerary](https://leetcode.com/problems/reconstruct-itinerary/) | Hard | Eulerian Path |
| [Word Search II](https://leetcode.com/problems/word-search-ii/) | Hard | Trie + DFS |

### Resources for Graphs

- 📘 **Book:** *Introduction to Algorithms* (CLRS) — Graph chapters
- 🌐 **Website:** [CP-Algorithms](https://cp-algorithms.com/graph/) — comprehensive graph algorithms
- 🌐 **Website:** [Visualgo](https://visualgo.net/en/dfsbfs) — visual graph algorithm animations
- 🎥 **YouTube:** [William Fiset](https://www.youtube.com/@WilliamFiset-videos) — graph theory playlist

---

# Phase 8: Trees (Advanced)

## Binary Tree Operations

```java
// Diameter of Binary Tree
int diameter = 0;
int diameterOfBinaryTree(TreeNode root) {
    height(root);
    return diameter;
}

int height(TreeNode node) {
    if (node == null) return 0;
    int left = height(node.left);
    int right = height(node.right);
    diameter = Math.max(diameter, left + right);
    return 1 + Math.max(left, right);
}

// Lowest Common Ancestor
TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    if (root == null || root == p || root == q) return root;
    TreeNode left = lowestCommonAncestor(root.left, p, q);
    TreeNode right = lowestCommonAncestor(root.right, p, q);
    if (left != null && right != null) return root;
    return left != null ? left : right;
}

// Path Sum II (all root-to-leaf paths with target sum)
List<List<Integer>> pathSum(TreeNode root, int targetSum) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(root, targetSum, new ArrayList<>(), result);
    return result;
}

void backtrack(TreeNode node, int remaining, List<Integer> path, List<List<Integer>> result) {
    if (node == null) return;
    path.add(node.val);
    if (node.left == null && node.right == null && remaining == node.val) {
        result.add(new ArrayList<>(path));
    } else {
        backtrack(node.left, remaining - node.val, path, result);
        backtrack(node.right, remaining - node.val, path, result);
    }
    path.remove(path.size() - 1);
}

```

## Binary Search Tree Operations

```java
// Validate BST
boolean isValidBST(TreeNode root) {
    return validate(root, Long.MIN_VALUE, Long.MAX_VALUE);
}

boolean validate(TreeNode node, long min, long max) {
    if (node == null) return true;
    if (node.val <= min || node.val >= max) return false;
    return validate(node.left, min, node.val) && validate(node.right, node.val, max);
}

// Kth Smallest in BST (inorder traversal)
int kthSmallest(TreeNode root, int k) {
    Deque<TreeNode> stack = new ArrayDeque<>();
    TreeNode curr = root;
    while (curr != null || !stack.isEmpty()) {
        while (curr != null) {
            stack.push(curr);
            curr = curr.left;
        }
        curr = stack.pop();
        if (--k == 0) return curr.val;
        curr = curr.right;
    }
    return -1;
}

```

## Serialize and Deserialize Binary Tree

```java
// Serialize
String serialize(TreeNode root) {
    if (root == null) return "null";
    StringBuilder sb = new StringBuilder();
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    while (!queue.isEmpty()) {
        TreeNode node = queue.poll();
        if (node == null) {
            sb.append("null,");
        } else {
            sb.append(node.val).append(",");
            queue.offer(node.left);
            queue.offer(node.right);
        }
    }
    return sb.toString();
}

// Deserialize
TreeNode deserialize(String data) {
    String[] values = data.split(",");
    if (values[0].equals("null")) return null;
    TreeNode root = new TreeNode(Integer.parseInt(values[0]));
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    int i = 1;
    while (!queue.isEmpty() && i < values.length) {
        TreeNode node = queue.poll();
        if (!values[i].equals("null")) {
            node.left = new TreeNode(Integer.parseInt(values[i]));
            queue.offer(node.left);
        }
        i++;
        if (!values[i].equals("null")) {
            node.right = new TreeNode(Integer.parseInt(values[i]));
            queue.offer(node.right);
        }
        i++;
    }
    return root;
}

```

## Advanced Tree Problems

| Problem | Difficulty | Pattern |
|---------|-----------|---------|
| [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | Hard | DFS |
| [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | Hard | BFS/DFS |
| [Binary Search Tree Iterator](https://leetcode.com/problems/binary-search-tree-iterator/) | Medium | Stack |
| [Construct Binary Tree from Preorder and Inorder](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | Medium | Recursion |
| [Flatten Binary Tree to Linked List](https://leetcode.com/problems/flatten-binary-tree-to-linked-list/) | Medium | DFS |
| [Populating Next Right Pointers](https://leetcode.com/problems/populating-next-right-pointers-in-each-node/) | Medium | BFS/DFS |
| [Symmetric Tree](https://leetcode.com/problems/symmetric-tree/) | Easy | DFS |
| [Subtree of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/) | Easy | DFS |
| [Construct Binary Search Tree from Preorder Traversal](https://leetcode.com/problems/construct-binary-search-tree-from-preorder-traversal/) | Medium | Recursion |
| [Two Sum IV - BST](https://leetcode.com/problems/two-sum-iv-input-is-a-bst/) | Easy | DFS + HashSet |
| [Vertical Order Traversal](https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree/) | Hard | BFS + Sorting |
| [Serialize and Deserialize N-ary Tree](https://leetcode.com/problems/serialize-and-deserialize-n-ary-tree/) | Hard | DFS |

### Resources for Trees

- 📘 **Book:** *Introduction to Algorithms* (CLRS) — Binary Search Trees chapter
- 🌐 **Website:** [Visualgo BST](https://visualgo.net/en/bst)
- 🎥 **YouTube:** [take U forward - Trees playlist](https://www.youtube.com/playlist?list=PLgZDfOG0dJyMRq1J_0xS2LqF5HgIh0y1z)

---

## 🔗 Related Files

| File | Description |
|------|-------------|
| [Complete Guide](01-Complete-Guide.md) | Phases 1-8: Java, DSA, Algorithms |
| [Core CS Fundamentals](02-Core-CS-Fundamentals.md) | Phases 9-16: CS Fundamentals, NoSQL |
| [System Design & APIs](03-System-Design-APIs-Security.md) | Phases 17-20: System Design, REST, Security |
| [DevOps & Career](04-DevOps-Behavioral-Career.md) | Phases 21-28: Git, Linux, Behavioral, Cloud |
| [Advanced Topics](05-Advanced-Topics.md) | Segment Tree, DI, Repository, MVC |
| [LeetCode Study Plan](06-LeetCode-Study-Plan.md) | 12-week intensive study plan |
| [Cheat Sheet](07-Cheat-Sheet.md) | Last-minute review for all 28 phases |
| [Microsoft Guide](16-Microsoft-Azure-Interview-Guide.md) | Microsoft Azure team-specific prep |
| [Progress Tracker](08-Progress-Tracker.md) | Track your weekly progress |
| [Mock Interview Bank](09-Mock-Interview-Question-Bank.md) | 90 questions (Coding + SD + Behavioral) |
| [Google Guide](17-Google-Interview-Guide.md) | Google-specific interview prep |
| [Amazon Guide](18-Amazon-Interview-Guide.md) | Amazon Leadership Principles prep |
| [Meta Guide](19-Meta-Interview-Guide.md) | Meta-specific interview prep |
| [Apple Guide](20-Apple-Interview-Guide.md) | Apple-specific interview prep |
---


## Summary

This comprehensive guide covers all essential topics for senior full-stack engineer interviews, from core CS fundamentals to system design, behavioral preparation, and career strategy. Master these concepts to demonstrate breadth and depth across the full engineering spectrum.

## References & Learn More

- [LeetCode](https://leetcode.com/)
- [NeetCode](https://neetcode.io/)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [Levels.fyi](https://www.levels.fyi/)
- [Cracking the Coding Interview](http://www.crackingthecodinginterview.com/)

## See Also
- [JavaScript](../01-JavaScript/)
- [TypeScript](../02-TypeScript/)
- [React](../03-React/)
- [System Design](../11-System-Design/)
- [Behavioral](../18-Behavioral/)
- [Coding Patterns](../19-Coding-Patterns/)
