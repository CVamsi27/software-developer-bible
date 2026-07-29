# Core Computer Science Fundamentals (Phases 9–15)

[![Category: Interview](https://img.shields.io/badge/category-Interview-1f7a8a)](.)

---

# Phase 9: Bit Manipulation

> **Why It Matters:** Bit manipulation questions appear frequently in interviews because they test your understanding of binary representation and low-level operations. They're often the key to O(1) space solutions.

## Core Concepts

### Bitwise Operators

```java
// AND (&) — both bits must be 1
5 & 3 = 1     // 0101 & 0011 = 0001

// OR (|) — at least one bit must be 1
5 | 3 = 7     // 0101 | 0011 = 0111

// XOR (^) — bits must differ
5 ^ 3 = 6     // 0101 ^ 0011 = 0110

// NOT (~) — flip all bits
~5 = -6       // ~0101 = ...11111010 (two's complement)

// Left Shift (<<) — multiply by 2^n
5 << 1 = 10   // 0101 << 1 = 1010
5 << 2 = 20   // 0101 << 2 = 10100

// Right Shift (>>) — divide by 2^n (sign-preserving)
10 >> 1 = 5   // 1010 >> 1 = 0101
-8 >> 1 = -4  // sign preserved

// Unsigned Right Shift (>>>) — fill with zeros
-8 >>> 1 = positive value

```

### Essential Bit Tricks

```java
// Check if number is even/odd
boolean isEven(int n) { return (n & 1) == 0; }

// Check if number is power of 2
boolean isPowerOfTwo(int n) { return n > 0 && (n & (n - 1)) == 0; }

// Get ith bit
int getBit(int n, int i) { return (n >> i) & 1; }

// Set ith bit
int setBit(int n, int i) { return n | (1 << i); }

// Clear ith bit
int clearBit(int n, int i) { return n & ~(1 << i); }

// Toggle ith bit
int toggleBit(int n, int i) { return n ^ (1 << i); }

// Clear rightmost set bit
int clearRightmost(int n) { return n & (n - 1); }

// Get rightmost set bit
int rightmostSetBit(int n) { return n & (-n); }

// Count set bits (Brian Kernighan's)
int countBits(int n) {
    int count = 0;
    while (n != 0) {
        n = n & (n - 1); // clear rightmost set bit
        count++;
    }
    return count;
}

// Reverse bits
int reverseBits(int n) {
    int result = 0;
    for (int i = 0; i < 32; i++) {
        result = (result << 1) | (n & 1);
        n >>= 1;
    }
    return result;
}

// XOR properties
// a ^ a = 0
// a ^ 0 = a
// a ^ b = b ^ a (commutative)
// (a ^ b) ^ c = a ^ (b ^ c) (associative)

```

### Subset Generation with Bitmasks

```java
// Generate all subsets of an array
void generateSubsets(int[] nums) {
    int n = nums.length;
    for (int mask = 0; mask < (1 << n); mask++) {
        List<Integer> subset = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) {
                subset.add(nums[i]);
            }
        }
        System.out.println(subset);
    }
}

```

## Bit Manipulation Problems

| Problem | Difficulty | Key Concept |
|---------|-----------|-------------|
| [Single Number](https://leetcode.com/problems/single-number/) | Easy | XOR |
| [Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) | Easy | Brian Kernighan's |
| [Counting Bits](https://leetcode.com/problems/counting-bits/) | Easy | DP + Bit |
| [Reverse Bits](https://leetcode.com/problems/reverse-bits/) | Easy | Bit shift |
| [Power of Two](https://leetcode.com/problems/power-of-two/) | Easy | n & (n-1) |
| [Missing Number](https://leetcode.com/problems/missing-number/) | Easy | XOR |
| [Sum of Two Integers](https://leetcode.com/problems/sum-of-two-integers/) | Medium | Bit manipulation |
| [Bitwise AND of Numbers Range](https://leetcode.com/problems/bitwise-and-of-numbers-range/) | Medium | Common prefix |
| [Maximum XOR of Two Numbers](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/) | Medium | Trie + Bit |
| [Subsets](https://leetcode.com/problems/subsets/) | Medium | Bitmask |
| [Single Number III](https://leetcode.com/problems/single-number-iii/) | Medium | XOR + isolation |
| [Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/) | Medium | Bit manipulation |
| [UTF-8 Validation](https://leetcode.com/problems/utf-8-validation/) | Medium | Bit masking |
| [IPAddress to CIDR](https://leetcode.com/problems/ip-to-cidr/) | Medium | Bit manipulation |

### Resources for Bit Manipulation

- 📘 **Book:** *Hacker's Delight* by Henry Warren — comprehensive bit manipulation
- 🌐 **Website:** [Bit Manipulation Tutorial](https://cp-algorithms.com/algebra/bit-manipulation.html)
- 🎥 **YouTube:** [take U forward - Bit Manipulation](https://www.youtube.com/watch?v=5rADyAO-77c)

---

# Phase 10: Mathematics

## Prime Numbers

```java
// Check if prime — O(√n)
boolean isPrime(int n) {
    if (n < 2) return false;
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) return false;
    }
    return true;
}

// Sieve of Eratosthenes — O(n log log n)
boolean[] sieve(int n) {
    boolean[] isPrime = new boolean[n + 1];
    Arrays.fill(isPrime, true);
    isPrime[0] = isPrime[1] = false;

    for (int i = 2; i * i <= n; i++) {
        if (isPrime[i]) {
            for (int j = i * i; j <= n; j += i) {
                isPrime[j] = false;
            }
        }
    }
    return isPrime;
}

// Count primes up to n
int countPrimes(int n) {
    boolean[] isPrime = new boolean[n];
    Arrays.fill(isPrime, true);
    int count = 0;
    for (int i = 2; i < n; i++) {
        if (isPrime[i]) {
            count++;
            for (long j = (long) i * i; j < n; j += i) {
                isPrime[(int) j] = false;
            }
        }
    }
    return count;
}

// Prime Factorization
Map<Integer, Integer> primeFactorization(int n) {
    Map<Integer, Integer> factors = new HashMap<>();
    for (int i = 2; i * i <= n; i++) {
        while (n % i == 0) {
            factors.put(i, factors.getOrDefault(i, 0) + 1);
            n /= i;
        }
    }
    if (n > 1) factors.put(n, 1);
    return factors;
}

```

## GCD and LCM

```java
// Euclidean Algorithm — O(log(min(a, b)))
int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

// LCM
int lcm(int a, int b) {
    return a / gcd(a, b) * b; // divide first to avoid overflow
}

// Extended Euclidean — finds x, y such that ax + by = gcd(a, b)
int[] extendedGCD(int a, int b) {
    if (b == 0) return new int[]{a, 1, 0};
    int[] prev = extendedGCD(b, a % b);
    int gcd = prev[0];
    int x = prev[2];
    int y = prev[1] - (a / b) * prev[2];
    return new int[]{gcd, x, y};
}

```

## Modular Arithmetic

```java
final long MOD = 1_000_000_007;

// Modular addition
long addMod(long a, long b) {
    return (a + b) % MOD;
}

// Modular multiplication
long mulMod(long a, long b) {
    return (a * b) % MOD;
}

// Modular exponentiation — O(log n)
long powerMod(long base, long exp, long mod) {
    long result = 1;
    base %= mod;
    while (exp > 0) {
        if ((exp & 1) == 1) {
            result = result * base % mod;
        }
        exp >>= 1;
        base = base * base % mod;
    }
    return result;
}

// Modular inverse (when MOD is prime)
long modInverse(long a) {
    return powerMod(a, MOD - 2, MOD); // Fermat's little theorem
}

// nCr modulo MOD
long nCr(int n, int r, long mod) {
    if (r > n) return 0;
    long[] fact = new long[n + 1];
    fact[0] = 1;
    for (int i = 1; i <= n; i++) fact[i] = fact[i - 1] * i % mod;

    long num = fact[n];
    long den = fact[r] * fact[n - r] % mod;
    return num * powerMod(den, mod - 2, mod) % mod;
}

```

## Combinatorics and Probability

```java
// Generate all permutations
void permutations(int[] nums, int start, List<List<Integer>> result) {
    if (start == nums.length) {
        result.add(Arrays.stream(nums).boxed().collect(Collectors.toList()));
        return;
    }
    for (int i = start; i < nums.length; i++) {
        swap(nums, start, i);
        permutations(nums, start + 1, result);
        swap(nums, start, i);
    }
}

// Generate all combinations
void combinations(int n, int k, int start, List<Integer> current, List<List<Integer>> result) {
    if (current.size() == k) {
        result.add(new ArrayList<>(current));
        return;
    }
    for (int i = start; i <= n; i++) {
        current.add(i);
        combinations(n, k, i + 1, current, result);
        current.remove(current.size() - 1);
    }
}

```

## Math Problems

| Problem | Difficulty | Key Concept |
|---------|-----------|-------------|
| [Count Primes](https://leetcode.com/problems/count-primes/) | Medium | Sieve |
| [Power of Three](https://leetcode.com/problems/power-of-three/) | Easy | Math |
| [Excel Sheet Column Number](https://leetcode.com/problems/excel-sheet-column-number/) | Easy | Base conversion |
| [Factorial Trailing Zeroes](https://leetcode.com/problems/factorial-trailing-zeroes/) | Medium | Count factors of 5 |
| [Rotate Image](https://leetcode.com/problems/rotate-image/) | Medium | Matrix math |
| [Spiral Matrix](https://leetcode.com/problems/spiral-matrix/) | Medium | Simulation |
| [Happy Number](https://leetcode.com/problems/happy-number/) | Easy | Cycle detection |
| [Max Points on a Line](https://leetcode.com/problems/max-points-on-a-line/) | Hard | GCD + HashMap |
| [Largest Number](https://leetcode.com/problems/largest-number/) | Medium | Custom sort |
| [Multiply Strings](https://leetcode.com/problems/multiply-strings/) | Medium | Math simulation |

### Resources for Math

- 📘 **Book:** *Competitive Programming* by Steven Halim — math chapter
- 🌐 **Website:** [CP-Algorithms](https://cp-algorithms.com/) — algebra and number theory
- 🌐 **Website:** [Brilliant.org](https://brilliant.org/) — interactive math courses

---

# Phase 11: Object-Oriented Programming

## OOP Principles

### 1. Encapsulation

```java
// Bundle data and methods, hide internal details
class BankAccount {
    private double balance;  // private — hidden from outside
    private String owner;

    public BankAccount(String owner, double initialBalance) {
        this.owner = owner;
        this.balance = initialBalance;
    }

    // Public methods provide controlled access
    public void deposit(double amount) {
        if (amount <= 0) throw new IllegalArgumentException("Amount must be positive");
        balance += amount;
    }

    public boolean withdraw(double amount) {
        if (amount > balance) return false;
        balance -= amount;
        return true;
    }

    public double getBalance() { return balance; }
}

```

### 2. Abstraction

```java
// Hide complexity, show only essential features
abstract class Shape {
    abstract double area();
    abstract double perimeter();

    // Template method pattern
    public void describe() {
        System.out.println("Area: " + area() + ", Perimeter: " + perimeter());
    }
}

class Circle extends Shape {
    double radius;

    Circle(double radius) { this.radius = radius; }

    @Override
    double area() { return Math.PI * radius * radius; }

    @Override
    double perimeter() { return 2 * Math.PI * radius; }
}

class Rectangle extends Shape {
    double width, height;

    Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }

    @Override
    double area() { return width * height; }

    @Override
    double perimeter() { return 2 * (width + height); }
}

```

### 3. Inheritance

```java
// IS-A relationship — code reuse
class Animal {
    String name;

    Animal(String name) { this.name = name; }

    void speak() { System.out.println(name + " speaks"); }
}

class Dog extends Animal {
    Dog(String name) { super(name); }

    @Override
    void speak() { System.out.println(name + " barks"); }

    void fetch() { System.out.println(name + " fetches"); }
}

// Multi-level inheritance
class Puppy extends Dog {
    Puppy(String name) { super(name); }

    @Override
    void speak() { System.out.println(name + " yips"); }
}

```

### 4. Polymorphism

```java
// Compile-time (method overloading)
class Calculator {
    int add(int a, int b) { return a + b; }
    double add(double a, double b) { return a + b; }
    String add(String a, String b) { return a + b; }
}

// Runtime (method overriding)
void makeSound(Animal animal) {
    animal.speak(); // calls the overridden version at runtime
}

Dog dog = new Dog("Rex");
Animal animal = dog;
makeSound(animal); // "Rex barks" — polymorphism in action

```

### 5. Composition (HAS-A relationship)

```java
// Prefer composition over inheritance
class Engine {
    void start() { System.out.println("Engine started"); }
}

class Car {
    private Engine engine;  // composition
    private List<Wheel> wheels;

    Car() {
        this.engine = new Engine();
        this.wheels = Arrays.asList(new Wheel(), new Wheel(), new Wheel(), new Wheel());
    }

    void start() {
        engine.start();
        System.out.println("Car started");
    }
}

```

## Interfaces vs Abstract Classes

```java
// Interface — contract (can have multiple inheritance)
interface Flyable {
    void fly();  // abstract by default

    default void glide() {  // default method (Java 8+)
        System.out.println("Gliding");
    }

    static boolean canFly(Flyable f) {
        return f != null;
    }
}

interface Swimmable {
    void swim();
}

// A class can implement multiple interfaces
class Duck extends Animal implements Flyable, Swimmable {
    Duck(String name) { super(name); }

    @Override public void fly() { System.out.println(name + " flies"); }
    @Override public void swim() { System.out.println(name + " swims"); }
}

// Abstract class — partial implementation (single inheritance only)
abstract class Vehicle {
    String name;

    Vehicle(String name) { this.name = name; }

    abstract void start();  // must be implemented

    void stop() {  // concrete method
        System.out.println(name + " stopped");
    }
}

```

## SOLID Principles

```java
// S — Single Responsibility Principle
// Each class should have only one reason to change
class UserValidator {
    boolean validate(User user) { /* validation logic */ }
}
class UserRepository {
    void save(User user) { /* persistence logic */ }
}
class EmailService {
    void sendWelcomeEmail(User user) { /* email logic */ }
}

// O — Open/Closed Principle
// Open for extension, closed for modification
interface DiscountStrategy {
    double applyDiscount(double price);
}

class SeasonalDiscount implements DiscountStrategy {
    public double applyDiscount(double price) { return price * 0.9; }
}

class LoyaltyDiscount implements DiscountStrategy {
    public double applyDiscount(double price) { return price * 0.85; }
}

// Adding new discounts doesn't require modifying existing code!

// L — Liskov Substitution Principle
// Subtypes must be substitutable for their base types
interface PaymentProcessor {
    PaymentResult process(double amount);
}

class CreditCardProcessor implements PaymentProcessor {
    public PaymentResult process(double amount) {
        // credit card processing
    }
}

class PayPalProcessor implements PaymentProcessor {
    public PaymentResult process(double amount) {
        // PayPal processing
    }
}

// I — Interface Segregation Principle
// Clients shouldn't depend on interfaces they don't use
interface Workable {
    void work();
}

interface Feedable {
    void eat();
}

interface Sleepable {
    void sleep();
}

class Robot implements Workable {
    public void work() { /* robots work */ }
    // doesn't implement eat() or sleep() — doesn't need to
}

// D — Dependency Inversion Principle
// Depend on abstractions, not concretions
class OrderService {
    private final PaymentProcessor processor;  // depends on interface

    OrderService(PaymentProcessor processor) {
        this.processor = processor;
    }

    void processOrder(double amount) {
        processor.process(amount);
    }
}

```

## Composition vs Inheritance

| Aspect | Inheritance | Composition |
|--------|-------------|-------------|
| Relationship | IS-A | HAS-A |
| Coupling | Tight | Loose |
| Flexibility | Limited (single inheritance) | High |
| Reuse | Code reuse | Behavior delegation |
| When to use | Clear hierarchy | Flexible, testable |

**Rule of thumb:** Favor composition over inheritance unless there's a clear IS-A relationship.

### Resources for OOP

- 📘 **Book:** *Head First Design Patterns* — OOP principles
- 📘 **Book:** *Clean Code* by Robert Martin — SOLID principles
- 🌐 **Website:** [Refactoring.Guru](https://refactoring.guru/) — OOP and design patterns
- 🎥 **YouTube:** [Amigoscode](https://www.youtube.com/@Amigoscode) — Java OOP

---

# Phase 12: Design Patterns

> **Why It Matters:** Interviewers ask about design patterns to gauge your ability to write maintainable, extensible code. Knowing the right pattern for a situation shows architectural maturity.

## Creational Patterns

### Singleton

```java
// Ensure only one instance exists
class DatabaseConnection {
    private static volatile DatabaseConnection instance;
    private Connection connection;

    private DatabaseConnection() {
        connection = createConnection();
    }

    public static DatabaseConnection getInstance() {
        if (instance == null) {
            synchronized (DatabaseConnection.class) {
                if (instance == null) {
                    instance = new DatabaseConnection();
                }
            }
        }
        return instance;
    }

    private Connection createConnection() {
        // create database connection
        return null;
    }
}

// Enum-based Singleton (Joshua Bloch's recommendation)
enum Database {
    INSTANCE;

    private Connection connection;

    Database() {
        connection = createConnection();
    }

    public Connection getConnection() { return connection; }
}

```

### Factory Method

```java
// Create objects without specifying exact class
interface Notification {
    void send(String message);
}

class EmailNotification implements Notification {
    public void send(String message) { System.out.println("Email: " + message); }
}

class SMSNotification implements Notification {
    public void send(String message) { System.out.println("SMS: " + message); }
}

class PushNotification implements Notification {
    public void send(String message) { System.out.println("Push: " + message); }
}

class NotificationFactory {
    static Notification create(String type) {
        return switch (type.toLowerCase()) {
            case "email" -> new EmailNotification();
            case "sms" -> new SMSNotification();
            case "push" -> new PushNotification();
            default -> throw new IllegalArgumentException("Unknown type: " + type);
        };
    }
}

// Usage
Notification notification = NotificationFactory.create("email");
notification.send("Hello!");

```

### Builder

```java
// Construct complex objects step by step
class Pizza {
    private String size;
    private boolean cheese;
    private boolean pepperoni;
    private boolean mushrooms;
    private List<String> toppings;

    private Pizza() {} // private constructor

    // Builder
    static class Builder {
        private Pizza pizza = new Pizza();

        Builder size(String size) { pizza.size = size; return this; }
        Builder cheese(boolean cheese) { pizza.cheese = cheese; return this; }
        Builder pepperoni(boolean pepperoni) { pizza.pepperoni = pepperoni; return this; }
        Builder mushrooms(boolean mushrooms) { pizza.mushrooms = mushrooms; return this; }
        Builder addTopping(String topping) {
            if (pizza.toppings == null) pizza.toppings = new ArrayList<>();
            pizza.toppings.add(topping);
            return this;
        }
        Pizza build() { return pizza; }
    }
}

// Usage
Pizza pizza = new Pizza.Builder()
    .size("Large")
    .cheese(true)
    .pepperoni(true)
    .addTopping("olives")
    .build();

```

## Structural Patterns

### Adapter

```java
// Convert one interface to another
interface MediaPlayer {
    void play(String filename);
}

class VLCAdapter implements MediaPlayer {
    private VLCLibrary vlc = new VLCLibrary();

    public void play(String filename) {
        vlc.playVLC(filename); // adapts the interface
    }
}

```

### Decorator

```java
// Add behavior dynamically
interface Coffee {
    double getCost();
    String getDescription();
}

class SimpleCoffee implements Coffee {
    public double getCost() { return 1.0; }
    public String getDescription() { return "Simple coffee"; }
}

abstract class CoffeeDecorator implements Coffee {
    protected Coffee coffee;
    CoffeeDecorator(Coffee coffee) { this.coffee = coffee; }
}

class MilkDecorator extends CoffeeDecorator {
    MilkDecorator(Coffee coffee) { super(coffee); }
    public double getCost() { return coffee.getCost() + 0.5; }
    public String getDescription() { return coffee.getDescription() + ", milk"; }
}

class SugarDecorator extends CoffeeDecorator {
    SugarDecorator(Coffee coffee) { super(coffee); }
    public double getCost() { return coffee.getCost() + 0.3; }
    public String getDescription() { return coffee.getDescription() + ", sugar"; }
}

// Usage
Coffee coffee = new SugarDecorator(new MilkDecorator(new SimpleCoffee()));
// cost: 1.8, description: "Simple coffee, milk, sugar"

```

### Facade

```java
// Simplify complex subsystem
class ComputerFacade {
    private CPU cpu;
    private Memory memory;
    private HardDrive hardDrive;

    ComputerFacade() {
        this.cpu = new CPU();
        this.memory = new Memory();
        this.hardDrive = new HardDrive();
    }

    void start() {
        cpu.freeze();
        memory.load(0, hardDrive.read(0, 1024));
        cpu.jump(0);
        cpu.execute();
    }
}

```

## Behavioral Patterns

### Observer

```java
// Publish-subscribe pattern
interface Observer {
    void update(String event);
}

class EventEmitter {
    private Map<String, List<Observer>> listeners = new HashMap<>();

    void subscribe(String event, Observer observer) {
        listeners.computeIfAbsent(event, k -> new ArrayList<>()).add(observer);
    }

    void unsubscribe(String event, Observer observer) {
        listeners.get(event).remove(observer);
    }

    void emit(String event) {
        for (Observer observer : listeners.getOrDefault(event, new ArrayList<>())) {
            observer.update(event);
        }
    }
}

```

### Strategy

```java
// Interchangeable algorithms
interface SortStrategy {
    void sort(int[] arr);
}

class BubbleSort implements SortStrategy {
    public void sort(int[] arr) { /* bubble sort */ }
}

class QuickSort implements SortStrategy {
    public void sort(int[] arr) { /* quick sort */ }
}

class Sorter {
    private SortStrategy strategy;

    Sorter(SortStrategy strategy) { this.strategy = strategy; }
    void setStrategy(SortStrategy strategy) { this.strategy = strategy; }
    void sort(int[] arr) { strategy.sort(arr); }
}

// Usage
Sorter sorter = new Sorter(new QuickSort());
sorter.sort(array);
sorter.setStrategy(new BubbleSort());
sorter.sort(array);

```

### Command

```java
// Encapsulate actions as objects
interface Command {
    void execute();
    void undo();
}

class TextEditor {
    private StringBuilder text = new StringBuilder();
    void type(String words) { text.append(words); }
    void delete(int count) { text.delete(text.length() - count, text.length()); }
    String getText() { return text.toString(); }
}

class TypeCommand implements Command {
    private TextEditor editor;
    private String text;

    TypeCommand(TextEditor editor, String text) {
        this.editor = editor;
        this.text = text;
    }

    public void execute() { editor.type(text); }
    public void undo() { editor.delete(text.length()); }
}

```

### Strategy vs Observer vs State

| Pattern | Purpose | Example |
|---------|---------|---------|
| Strategy | Swap algorithm at runtime | Sort algorithm selection |
| Observer | Notify dependents of state change | Event listeners |
| State | Change behavior based on state | Game character states |

## Design Patterns Summary Table

| Pattern | Type | Use Case |
|---------|------|----------|
| Singleton | Creational | Database connection pool |
| Factory | Creational | Object creation with type parameter |
| Builder | Creational | Complex object construction |
| Adapter | Structural | Interface compatibility |
| Decorator | Structural | Dynamic behavior addition |
| Facade | Structural | Simplify complex systems |
| Proxy | Structural | Access control, caching |
| Observer | Behavioral | Event systems, notifications |
| Strategy | Behavioral | Algorithm selection |
| Command | Behavioral | Undo/redo, task queuing |
| Template Method | Behavioral | Define algorithm skeleton |
| Iterator | Behavioral | Sequential access |
| State | Behavioral | State-dependent behavior |
| Mediator | Behavioral | Communication between objects |

## More Design Patterns

> **Note:** For Dependency Injection, Repository, and MVC patterns, see [Advanced Topics](05-Advanced-Topics.md).

## Problems to Practice

| Problem | Difficulty | Pattern |
|---------|-----------|---------|
| [Design Twitter](https://leetcode.com/problems/design-twitter/) | Medium | OOP + Data Structures |
| [Implement Trie](https://leetcode.com/problems/implement-trie-prefix-tree/) | Medium | Trie |
| [LRU Cache](https://leetcode.com/problems/lru-cache/) | Medium | Design + DLL |
| [Min Stack](https://leetcode.com/problems/min-stack/) | Medium | Stack + Auxiliary |
| [Design Add and Search Words](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | Medium | Trie + DFS |
| [Design HashMap](https://leetcode.com/problems/design-hashmap/) | Easy | Hashing |
| [Design Linked List](https://leetcode.com/problems/design-linked-list/) | Medium | Linked List |
| [Design HashSet](https://leetcode.com/problems/design-hashset/) | Easy | Hashing |
| [Snapshot Array](https://leetcode.com/problems/snapshot-array/) | Medium | Binary Search + Design |
| [LFU Cache](https://leetcode.com/problems/lfu-cache/) | Hard | Design |

### Resources for Design Patterns

- 📘 **Book:** *Head First Design Patterns* — visual, beginner-friendly
- 📘 **Book:** *Design Patterns: Elements of Reusable OO Software* (Gang of Four) — the original
- 📘 **Book:** *Effective Java* by Joshua Bloch — Java-specific patterns
- 🌐 **Website:** [Refactoring.Guru](https://refactoring.guru/design-patterns) — comprehensive pattern catalog
- 🌐 **Website:** [SourceMaking](https://sourcemaking.com/design_patterns) — detailed explanations
- 🎥 **YouTube:** [Amigoscode](https://www.youtube.com/@Amigoscode) — Java design patterns

---

# Phase 13: Operating Systems

> **Why It Matters:** OS questions test your understanding of how computers actually work. Knowledge of processes, threads, memory management, and synchronization is critical for writing efficient concurrent code.

## Processes vs Threads

| Aspect | Process | Thread |
|--------|---------|--------|
| Definition | Independent program execution | Lightweight process within a process |
| Memory | Separate address space | Shared address space |
| Creation overhead | High | Low |
| Communication | IPC (pipes, sockets, shared memory) | Direct (shared variables) |
| Failure impact | Isolated | Can crash entire process |
| Context switch | Expensive | Cheaper |

## Process Scheduling

```text

CPU Scheduling Algorithms:
├── FCFS (First Come First Served) — non-preemptive
├── SJF (Shortest Job First) — non-preemptive
├── SRTF (Shortest Remaining Time First) — preemptive
├── Round Robin — preemptive, time quantum
├── Priority Scheduling — can starve low priority
└── Multilevel Queue — combination approach

Key Metrics:
- Turnaround Time = Completion Time - Arrival Time
- Waiting Time = Turnaround Time - Burst Time
- Response Time = First Response Time - Arrival Time

```

## Deadlocks

### Four Conditions (Coffman Conditions)

1. **Mutual Exclusion** — resource can only be held by one process
2. **Hold and Wait** — process holds resource while waiting for another
3. **No Preemption** — resources cannot be forcibly taken
4. **Circular Wait** — circular chain of processes waiting for each other

### Prevention Strategies

```java
// Resource ordering (break circular wait)
// Assign numbers to resources, always acquire in order
Thread 1: lock(A) → lock(B)  // A=1, B=2
Thread 2: lock(A) → lock(B)  // must acquire A first, then B

// Try-lock with timeout
ReentrantLock lock = new ReentrantLock();
try {
    if (lock.tryLock(1, TimeUnit.SECONDS)) {
        // acquired lock
    } else {
        // timeout — back off
    }
} finally {
    lock.unlock();
}

// Banker's Algorithm — safe state detection
// Before granting request, check if system remains in safe state

```

## Memory Management

### Virtual Memory

```text

Virtual Memory: Each process thinks it has its own memory space
├── Page Table: maps virtual → physical addresses
├── Page: fixed-size block of virtual memory (typically 4KB)
├── Frame: fixed-size block of physical memory
├── Page Fault: accessing page not in physical memory → OS loads it
└── Thrashing: excessive page faults, system spends more time swapping

Page Replacement Algorithms:
├── FIFO — simple, Belady's anomaly
├── LRU — good approximation, needs hardware support
├── Optimal — theoretical best, not implementable
├── Clock — approximation of LRU
└── LFU — least frequently used

```

### Cache

```text

Cache Levels:
├── L1 — smallest, fastest (32KB-64KB, ~1ns)
├── L2 — medium (256KB-512KB, ~3ns)
├── L3 — largest, shared (2MB-8MB, ~10ns)
└── Main Memory — ~100ns

Cache Associativity:
├── Direct Mapped — each block maps to exactly one cache line
├── Fully Associative — block can go anywhere
└── Set Associative — block can go anywhere in a set

```

## Synchronization Primitives

```java
// Mutex — mutual exclusion, only one thread can hold
ReentrantLock mutex = new ReentrantLock();
mutex.lock();
try {
    // critical section
} finally {
    mutex.unlock();
}

// Semaphore — allows N concurrent access
Semaphore semaphore = new Semaphore(3); // 3 permits
semaphore.acquire(); // blocks if no permits
try {
    // critical section
} finally {
    semaphore.release();
}

// Monitor — high-level synchronization construct
synchronized void method() {
    // only one thread at a time
    // can use wait(), notify(), notifyAll()
}

// Barrier — wait for all threads to reach a point
CyclicBarrier barrier = new CyclicBarrier(3, () -> {
    System.out.println("All threads reached barrier");
});

// CountDownLatch — wait for N events
CountDownLatch latch = new CountDownLatch(3);
// in worker threads:
latch.countDown();
// in waiting thread:
latch.await(); // blocks until count reaches 0

```

## Inter-Process Communication (IPC)

```text

IPC Methods:
├── Pipes — unidirectional, parent-child
├── Named Pipes (FIFO) — bidirectional, unrelated processes
├── Message Queues — asynchronous, kernel-managed
├── Shared Memory — fastest, but needs synchronization
├── Sockets — network communication
├── Signals — asynchronous notification
└── Semaphores — synchronization between processes

```

## OS Problems

| Problem | Difficulty | Topic |
|---------|-----------|-------|
| [Design Hit Counter](https://leetcode.com/problems/design-hit-counter/) | Medium | Concurrency |
| [Print in Order](https://leetcode.com/problems/print-in-order/) | Easy | Synchronization |
| [Print FooBar Alternately](https://leetcode.com/problems/print-foobar-alternately/) | Medium | Synchronization |
| [Print Zero Even Odd](https://leetcode.com/problems/print-zero-even-odd/) | Medium | Synchronization |
| [Fizz Buzz Multithreaded](https://leetcode.com/problems/fizz-buzz-multithreaded/) | Medium | Synchronization |
| [Building H2O](https://leetcode.com/problems/building-h2o/) | Medium | Semaphore |
| [The Dining Philosophers](https://leetcode.com/problems/the-dining-philosophers/) | Medium | Deadlock prevention |
| [Web Crawler Multithreaded](https://leetcode.com/problems/web-crawler-multithreaded/) | Medium | Concurrency |
| [Design Bounded Blocking Queue](https://leetcode.com/problems/design-bounded-blocking-queue/) | Medium | Producer-Consumer |

### Resources for Operating Systems

- 📘 **Book:** *Operating System Concepts* (Dinosaur Book) by Silberschatz
- 📘 **Book:** *Operating Systems: Three Easy Pieces* (free online)
- 🌐 **Website:** [OS Study Guide](https://wiki.osdev.org/Main_Page)
- 🎥 **YouTube:** [Nand2Tetris](https://www.youtube.com/@nand2tetris) — building a computer from scratch
- 🎥 **YouTube:** [MIT 6.828](https://www.youtube.com/playlist?list=PLfIH1vrcn8mJjMazW11S4oT20z2g) — operating system engineering
- 🌐 **Website:** [OSTEP](https://pages.cs.wisc.edu/~remzi/OSTEP/) — free online textbook

---

# Phase 14: Computer Networks

> **Why It Matters:** Every web application relies on networking. Understanding protocols, the request-response cycle, and security is essential for designing scalable systems.

## The OSI Model

```text

Layer 7: Application    — HTTP, HTTPS, FTP, SMTP, DNS
Layer 6: Presentation   — SSL/TLS, encryption, compression
Layer 5: Session        — session management, authentication
Layer 4: Transport      — TCP, UDP, port numbers
Layer 3: Network        — IP, routing, packets
Layer 2: Data Link      — MAC addresses, frames, switches
Layer 1: Physical       — cables, signals, bits

```

## TCP vs UDP

| Aspect | TCP | UDP |
|--------|-----|-----|
| Connection | Connection-oriented | Connectionless |
| Reliability | Guaranteed delivery | Best effort |
| Ordering | Maintains order | No ordering |
| Speed | Slower (overhead) | Faster |
| Error checking | Yes | Optional |
| Use cases | HTTP, email, file transfer | Video streaming, gaming, DNS |

### TCP Three-Way Handshake

```text

Client → Server: SYN (I want to connect)
Server → Client: SYN-ACK (I acknowledge)
Client → Server: ACK (connection established)

Connection termination: FIN → FIN-ACK → ACK

```

### TCP Flow Control and Congestion Control

```text

Flow Control:
- Sliding window protocol
- Receiver advertises window size
- Sender limits unacknowledged data

Congestion Control:
- Slow Start — exponential growth
- Congestion Avoidance — linear growth
- Fast Retransmit — 3 duplicate ACKs
- Fast Recovery — after fast retransmit

```

## HTTP/HTTPS

### HTTP Methods

| Method | Idempotent | Safe | Use Case |
|--------|-----------|------|----------|
| GET | Yes | Yes | Read resource |
| POST | No | No | Create resource |
| PUT | Yes | No | Replace resource |
| PATCH | No | No | Partial update |
| DELETE | Yes | No | Delete resource |
| HEAD | Yes | Yes | Get headers only |
| OPTIONS | Yes | Yes | Get allowed methods |

### HTTP Status Codes

```text

1xx: Informational
  100 Continue
  101 Switching Protocols

2xx: Success
  200 OK
  201 Created
  202 Accepted
  204 No Content

3xx: Redirection
  301 Moved Permanently
  302 Found (Temporary Redirect)
  304 Not Modified

4xx: Client Error
  400 Bad Request
  401 Unauthorized
  403 Forbidden
  404 Not Found
  405 Method Not Allowed
  409 Conflict
  422 Unprocessable Entity
  429 Too Many Requests

5xx: Server Error
  500 Internal Server Error
  502 Bad Gateway
  503 Service Unavailable
  504 Gateway Timeout

```

### HTTPS and TLS

```text

TLS Handshake (simplified):
1. Client Hello — supported cipher suites
2. Server Hello — chosen cipher suite + certificate
3. Client verifies certificate with CA
4. Key exchange — generate session key
5. Encrypted communication begins

Security Properties:
- Confidentiality — encryption
- Integrity — message authentication codes
- Authentication — certificates

```

## DNS

```text

DNS Resolution Process:
1. Browser cache
2. OS cache
3. Router cache
4. ISP DNS server
5. Root name server
6. TLD name server (.com, .org)
7. Authoritative name server

Record Types:
- A: domain → IPv4
- AAAA: domain → IPv6
- CNAME: alias → canonical name
- MX: mail exchange
- TXT: text records (SPF, DKIM)
- NS: name server

```

## Load Balancing

```text

Algorithms:
├── Round Robin — simple rotation
├── Weighted Round Robin — based on server capacity
├── Least Connections — route to least busy
├── IP Hash — consistent routing
├── Least Response Time — fastest server
└── Resource Based — based on real-time metrics

L4 vs L7 Load Balancing:
- L4: Transport layer (TCP/UDP) — faster, less flexible
- L7: Application layer (HTTP) — content-based routing, SSL termination

```

## Caching

```text

Cache Levels:
├── Browser Cache — client-side
├── CDN Edge Cache — distributed globally
├── Reverse Proxy Cache — nginx, Varnish
├── Application Cache — in-memory (Redis, Memcached)
└── Database Cache — query result cache

Cache Strategies:
├── Cache-Aside (Lazy Loading) — app manages cache
├── Write-Through — write to cache and DB simultaneously
├── Write-Behind (Write-Back) — write to cache, async to DB
└── Read-Through — cache manages DB reads

Cache Policies:
├── LRU — Least Recently Used
├── LFU — Least Frequently Used
├── FIFO — First In First Out
└── TTL — Time To Live expiration

```

## WebSocket vs SSE vs HTTP

```text

WebSocket:
- Full-duplex communication
- Persistent connection
- Use case: chat, real-time gaming, collaboration

Server-Sent Events (SSE):
- Server → Client only
- Auto-reconnection
- Use case: notifications, live feeds, updates

HTTP Polling:
- Client repeatedly requests
- Wasteful if no new data
- Use case: legacy systems

HTTP Long Polling:
- Server holds request until data available
- Compromise between polling and push

```

## gRPC

```text

- Built on HTTP/2
- Protocol Buffers (binary serialization)
- Four types: Unary, Server streaming, Client streaming, Bidirectional
- Use case: microservices communication
- 10x faster than REST for binary data

```

## Network Problems

| Problem | Difficulty | Topic |
|---------|-----------|-------|
| [Design URL Shortener](https://leetcode.com/problems/design-url-shortener/) | Medium | DNS, hashing |
| [Design Rate Limiter](https://leetcode.com/problems/design-rate-limiter/) | Medium | Token bucket, sliding window |
| [Implement HTTP Router](https://leetcode.com/problems/design-url-shortener/) | Medium | Trie, routing |
| [Design Web Crawler](https://leetcode.com/problems/web-crawler/) | Medium | BFS, concurrency |
| [Design IP Address Counter](https://leetcode.com/problems/design-ip-address-counter/) | Hard | Trie, CIDR |

### Resources for Computer Networks

- 📘 **Book:** *Computer Networking: A Top-Down Approach* by Kurose & Ross
- 📘 **Book:** *TCP/IP Illustrated* by W. Richard Stevens
- 🌐 **Website:** [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web) — HTTP, networking
- 🌐 **Website:** [HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)
- 🎥 **YouTube:** [Computerphile](https://www.youtube.com/@Computerphile) — networking concepts
- 🎥 **YouTube:** [Practical Networking](https://www.youtube.com/@PracticalNetworking) — networking deep dives
- 🌐 **Website:** [How HTTPS Works](https://howhttps.works/) — visual HTTPS explanation

---

# Phase 15: Databases

> **Why It Matters:** Database knowledge is critical for system design interviews. You need to understand when to use SQL vs NoSQL, how to optimize queries, and how to design schemas that scale.

## SQL Fundamentals

### DDL (Data Definition Language)

```sql
-- Create table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Alter table
ALTER TABLE users ADD COLUMN age INTEGER;
ALTER TABLE users DROP COLUMN age;
ALTER TABLE users ALTER COLUMN name SET NOT NULL;

-- Drop table
DROP TABLE IF EXISTS users;

-- Create index
CREATE INDEX idx_users_email ON users(email);
CREATE UNIQUE INDEX idx_users_email ON users(email);

```

### DML (Data Manipulation Language)

```sql
-- Insert
INSERT INTO users (email, name) VALUES ('alice@example.com', 'Alice');
INSERT INTO users (email, name) VALUES
    ('bob@example.com', 'Bob'),
    ('charlie@example.com', 'Charlie');

-- Update
UPDATE users SET name = 'Alice Smith' WHERE id = 1;

-- Delete
DELETE FROM users WHERE id = 1;

-- Upsert (PostgreSQL)
INSERT INTO users (email, name) VALUES ('alice@example.com', 'Alice')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name;

```

### Joins

```sql
-- INNER JOIN — only matching rows
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN — all from left, matching from right
SELECT u.name, COALESCE(SUM(o.total), 0) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;

-- RIGHT JOIN — all from right, matching from left
SELECT u.name, o.id as order_id
FROM users u
RIGHT JOIN orders o ON u.id = o.user_id;

-- FULL OUTER JOIN — all from both
SELECT u.name, o.id as order_id
FROM users u
FULL OUTER JOIN orders o ON u.id = o.user_id;

-- Self JOIN
SELECT e.name as employee, m.name as manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;

-- Cross Join (Cartesian Product)
SELECT u.name, p.name
FROM users u
CROSS JOIN products p;

```

### Aggregate Functions

```sql
-- COUNT, SUM, AVG, MIN, MAX
SELECT
    COUNT(*) as total_users,
    COUNT(DISTINCT email) as unique_emails,
    AVG(age) as average_age,
    MIN(created_at) as earliest,
    MAX(created_at) as latest
FROM users;

-- GROUP BY
SELECT
    department,
    COUNT(*) as emp_count,
    AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING COUNT(*) > 5
ORDER BY avg_salary DESC;

-- Window Functions
SELECT
    name,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rank,
    LAG(salary) OVER (ORDER BY salary) as prev_salary,
    LEAD(salary) OVER (ORDER BY salary) as next_salary,
    SUM(salary) OVER (PARTITION BY department) as dept_total,
    AVG(salary) OVER (PARTITION BY department) as dept_avg
FROM employees;

```

### Subqueries and CTEs

```sql
-- Subquery
SELECT * FROM orders
WHERE user_id IN (SELECT id FROM users WHERE is_active = true);

-- CTE (Common Table Expression)
WITH active_users AS (
    SELECT id, name FROM users WHERE is_active = true
),
user_orders AS (
    SELECT user_id, COUNT(*) as order_count
    FROM orders
    GROUP BY user_id
)
SELECT au.name, COALESCE(uo.order_count, 0) as orders
FROM active_users au
LEFT JOIN user_orders uo ON au.id = uo.user_id;

-- Recursive CTE (for hierarchical data)
WITH RECURSIVE org_chart AS (
    SELECT id, name, manager_id, 1 as level
    FROM employees WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, oc.level + 1
    FROM employees e
    INNER JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT * FROM org_chart ORDER BY level, name;

```

## Normalization

```text

1NF — First Normal Form
- Each column contains atomic values
- No repeating groups
- Each row is unique

2NF — Second Normal Form
- In 1NF
- No partial dependencies (all non-key columns depend on entire primary key)

3NF — Third Normal Form
- In 2NF
- No transitive dependencies (non-key columns don't depend on other non-key columns)

BCNF — Boyce-Codd Normal Form
- In 3NF
- Every determinant is a candidate key

Example:
Users (id, name, email)           — 3NF ✓
Orders (id, user_id, product_id, product_name)
  → product_name depends on product_id, not id — violates 3NF
  → Fix: Products (id, name), Orders (id, user_id, product_id)

```

## Indexes

```sql
-- B-Tree Index (default) — good for equality and range queries
CREATE INDEX idx_users_name ON users(name);

-- Composite Index — order matters!
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);
-- Can be used for: WHERE user_id = ? AND created_at > ?
-- Can be used for: WHERE user_id = ?
-- Cannot be used for: WHERE created_at > ? (leading column missing)

-- Partial Index — index only subset of rows
CREATE INDEX idx_active_users ON users(email) WHERE is_active = true;

-- Covering Index — includes all columns needed by query
CREATE INDEX idx_orders_covering ON orders(user_id, created_at, total)
-- Query: SELECT created_at, total FROM orders WHERE user_id = ?
-- Can be answered entirely from index (no table lookup)

-- Hash Index — good for equality only
CREATE INDEX idx_users_email_hash ON users USING hash(email);

-- Analyze query plan
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'alice@example.com';

```

### Index Best Practices

```text

DO:
✅ Index columns used in WHERE, JOIN, ORDER BY
✅ Index foreign keys
✅ Use composite indexes for multi-column queries
✅ Consider covering indexes for frequent queries

DON'T:
❌ Index every column (slows writes)
❌ Index low-cardinality columns (like boolean)
❌ Over-index (each index slows INSERT/UPDATE/DELETE)
❌ Use functions on indexed columns (breaks index usage)

```

## Transactions and ACID

```sql
-- Transaction
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- Rollback
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
ROLLBACK; -- undo all changes

```

### ACID Properties

| Property | Description | Implementation |
|----------|-------------|----------------|
| Atomicity | All or nothing | WAL (Write-Ahead Logging) |
| Consistency | Valid state transitions | Constraints, triggers |
| Isolation | Concurrent transactions don't interfere | MVCC, locking |
| Durability | Committed data survives crashes | WAL, fsync |

### Isolation Levels

```text

Level               | Dirty Read | Non-Repeatable Read | Phantom Read
---------------------|------------|---------------------|-------------
Read Uncommitted     | Yes        | Yes                 | Yes
Read Committed       | No         | Yes                 | Yes
Repeatable Read      | No         | No                  | Yes
Serializable         | No         | No                  | No

In PostgreSQL:
- Default: Read Committed
- REPEATABLE READ uses MVCC
- SERIALIZABLE uses SSI (Serializable Snapshot Isolation)

```

## Query Optimization

```sql
-- EXPLAIN ANALYZE — see query plan and actual execution
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'alice@example.com';

-- Common optimizations:
-- 1. Add index on filtered column
-- 2. Avoid SELECT * — only select needed columns
-- 3. Use LIMIT for pagination
-- 4. Avoid functions on indexed columns
-- 5. Use EXPLAIN to identify full table scans
-- 6. JOIN order matters — filter early

-- Bad: function on indexed column
SELECT * FROM users WHERE LOWER(email) = 'alice@example.com';
-- Good: functional index
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

```

## Partitioning

```sql
-- Range partitioning (by date)
CREATE TABLE orders (
    id SERIAL,
    created_at TIMESTAMP,
    total DECIMAL
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2024 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE orders_2025 PARTITION OF orders
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

-- Benefits:
-- - Faster queries (only scan relevant partitions)
-- - Easier data management (drop old partitions)
-- - Better parallelism

```

## Replication and Sharding

```text

Replication:
├── Primary-Replica — read replicas for read scaling
├── Multi-Master — multiple write nodes
├── Synchronous — replicas updated before commit
└── Asynchronous — replicas updated after commit (eventual consistency)

Sharding:
├── Horizontal — split rows across databases
├── Vertical — split columns across databases
├── Hash-based — consistent hashing
├── Range-based — partition by range
└── Directory-based — lookup service maps keys to shards

Sharding Challenges:
- Cross-shard queries
- Distributed transactions
- Rebalancing
- Joins across shards

```

## Database Problems

| Problem | Difficulty | Topic |
|---------|-----------|-------|
| [Second Highest Salary](https://leetcode.com/problems/second-highest-salary/) | Easy | Subquery |
| [Department Top Three Salaries](https://leetcode.com/problems/department-top-three-salaries/) | Hard | Window Functions |
| [Consecutive Numbers](https://leetcode.com/problems/consecutive-numbers/) | Medium | Window Functions |
| [Immediate Food Delivery](https://leetcode.com/problems/immediate-food-delivery-ii/) | Medium | GROUP BY |
| [Exchange Seats](https://leetcode.com/problems/exchange-seats/) | Medium | SQL logic |
| [Swap Salary](https://leetcode.com/problems/swap-salary/) | Easy | UPDATE |
| [Delete Duplicate Emails](https://leetcode.com/problems/delete-duplicate-emails/) | Easy | DELETE + JOIN |
| [Rising Temperature](https://leetcode.com/problems/rising-temperature/) | Easy | JOIN + DATEDIFF |

### Resources for Databases

- 📘 **Book:** *Database System Concepts* by Silberschatz
- 📘 **Book:** *Designing Data-Intensive Applications* by Martin Kleppmann (MUST READ)
- 📘 **Book:** *SQL Performance Explained* by Markus Winand
- 🌐 **Website:** [Use The Index, Luke](https://use-the-index-luke.com/) — SQL indexing
- 🌐 **Website:** [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- 🎥 **YouTube:** [CMU Database Group](https://www.youtube.com/@CMUDatabaseGroup) — database internals
- 🌐 **Website:** [DB Fiddle](https://www.db-fiddle.com/) — practice SQL online

---

# NoSQL & Distributed Systems

> **Why It Matters:** NoSQL databases solve specific problems that relational databases can't handle efficiently. Understanding when to use each type is critical for system design interviews.

## CAP Theorem

```text

In a distributed system, you can only guarantee 2 of 3:
├── Consistency — every read gets the most recent write
├── Availability — every request gets a response
└── Partition Tolerance — system works despite network failures

Since network partitions are inevitable:
- CP Systems: Consistent but may be unavailable (e.g., HBase, MongoDB)
- AP Systems: Available but may be inconsistent (e.g., Cassandra, DynamoDB)
- CA Systems: Consistent and available but no partition tolerance (single node)

```

## Types of NoSQL Databases

### 1. Key-Value Store (Redis, DynamoDB)

```text

Characteristics:
├── Simple key-value pairs
├── O(1) read/write
├── Horizontal scaling easy
└── Limited querying (by key only)

Use Cases:
- Caching (Redis)
- Session storage
- User profiles
- Shopping carts

```

### 2. Document Store (MongoDB, CouchDB)

```text

Characteristics:
├── JSON/BSON documents
├── Flexible schema
├── Rich querying (by fields)
└── Nested documents supported

Use Cases:
- Content management
- User profiles
- Product catalogs
- Event logging

```

### 3. Wide Column Store (Cassandra, HBase)

```text

Characteristics:
├── Rows with dynamic columns
├── Optimized for writes
├── Horizontal scaling
└── Tunable consistency

Use Cases:
- Time-series data
- IoT data
- Chat messages
- Event sourcing

```

### 4. Graph Database (Neo4j, ArangoDB)

```text

Characteristics:
├── Nodes and relationships
├── Optimized for traversals
├── Natural for connected data
└── Cypher query language

Use Cases:
- Social networks
- Recommendation engines
- Fraud detection
- Knowledge graphs

```

## When to Use What

```text

| Need                        | Use                    |
|-----------------------------|------------------------|
| Simple caching              | Redis                  |
| Session storage             | Redis                  |
| Flexible documents          | MongoDB                |
| Time-series data            | Cassandra              |
| Social connections          | Neo4j                  |
| Full-text search            | Elasticsearch          |
| Geospatial queries          | MongoDB + Redis GEO    |
| Strong consistency          | PostgreSQL             |
| Event sourcing              | Cassandra / EventStore |

```

## Distributed Systems Concepts

```text

Consistency Models:
├── Strong Consistency — read returns most recent write
├── Eventual Consistency — read eventually returns most recent write
├── Causal Consistency — causally related operations seen in order
└── Read-your-writes — user sees their own writes immediately

Replication Strategies:
├── Leader-Follower — writes to leader, reads from followers
├── Multi-Leader — multiple leaders accept writes
├── Leaderless — any node can accept writes (quorum)
└── Consistent Hashing — distribute data across nodes

```

## Redis Deep Dive

```java
// Redis Data Structures
// Strings
redis.set("key", "value");
redis.get("key");
redis.incr("counter");
redis.expire("key", 3600);

// Lists
redis.lpush("queue", "task1");
redis.rpop("queue");
redis.lrange("queue", 0, -1);

// Sets
redis.sadd("tags", "java", "python");
redis.smembers("tags");
redis.sinter("set1", "set2"); // intersection

// Hashes
redis.hset("user:1", "name", "Alice");
redis.hget("user:1", "name");
redis.hgetall("user:1");

// Sorted Sets (ZSet)
redis.zadd("leaderboard", 100, "player1");
redis.zrange("leaderboard", 0, -1, "WITHSCORES");
redis.zrank("leaderboard", "player1");

// HyperLogLog (cardinality estimation)
redis.pfadd("visitors", "user1", "user2");
redis.pfcount("visitors"); // approximate unique count

// Pub/Sub
redis.publish("channel", "message");
redis.subscribe("channel");

```

## NoSQL Problems

| Problem | Difficulty | Topic |
|---------|-----------|-------|
| [Design Twitter](https://leetcode.com/problems/design-twitter/) | Medium | CAP, Replication |
| [Design a Key-Value Store](https://leetcode.com/problems/design-hashmap/) | Medium | Consistent Hashing |
| [Design a Leaderboard](https://leetcode.com/problems/design-a-number-container-system/) | Medium | Sorted Set |
| [Design a Time-Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store/) | Medium | Document Store |

## MongoDB Quick Reference

```javascript
// Insert
db.users.insertOne({ name: "Alice", email: "alice@example.com", age: 30 });
db.users.insertMany([{ name: "Bob" }, { name: "Charlie" }]);

// Query
db.users.find({ age: { $gt: 25 } });
db.users.findOne({ email: "alice@example.com" });
db.users.find({ "address.city": "Seattle" });
db.users.find({ tags: { $in: ["admin"] } });
db.users.find().sort({ age: -1 }).limit(10);

// Update
db.users.updateOne({ name: "Alice" }, { $set: { age: 31 } });
db.users.updateMany({ age: { $lt: 18 } }, { $set: { status: "minor" } });

// Delete
db.users.deleteOne({ name: "Bob" });
db.users.deleteMany({ status: "inactive" });

// Aggregation
db.orders.aggregate([
    { $match: { status: "completed" } },
    { $group: { _id: "$userId", total: { $sum: "$amount" } } },
    { $sort: { total: -1 } },
    { $limit: 10 }
]);

// Indexes
db.users.createIndex({ email: 1 }, { unique: true });
db.users.createIndex({ "address.city": 1 });

```

### Resources for NoSQL & Distributed Systems

- 📘 **Book:** *Designing Data-Intensive Applications* by Martin Kleppmann — **MUST READ**
- 📘 **Book:** *Database Internals* by Alex Petrov
- 🌐 **Website:** [Redis Documentation](https://redis.io/documentation)
- 🌐 **Website:** [MongoDB Documentation](https://www.mongodb.com/docs/)
- 🌐 **Website:** [Cassandra Documentation](https://cassandra.apache.org/doc/)
- 🎥 **YouTube:** [ByteByteGo](https://www.youtube.com/@ByteByteGo)

---

## 🔗 Related Files

| File | Description |
|------|-------------|
| [Complete Guide](01-Complete-Guide.md) | Phases 1-8: Java, DSA, Algorithms |
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

This guide covers the core computer science fundamentals required for technical interviews, including bit manipulation, mathematics, sorting algorithms, data structures, dynamic programming, and graph algorithms with Java implementations.

## See Also
- [Behavioral](../18-Behavioral/)
- [Coding Patterns](../19-Coding-Patterns/)
- [JavaScript](../01-JavaScript/)
- [React](../03-React/)
- [System Design](../11-System-Design/)
- [TypeScript](../02-TypeScript/)

---

## Cheat Sheet
```text
CORE COMPUTER SCIENCE FUNDAMENTALS (PHASES 9–15) CHEAT SHEET
============================================================

COMMON PATTERNS:
```
  5 & 3 = 1     // 0101 & 0011 = 0001
  5 | 3 = 7     // 0101 | 0011 = 0111
  5 ^ 3 = 6     // 0101 ^ 0011 = 0110
  ~5 = -6       // ~0101 = ...11111010 (two's complement)
  5 << 1 = 10   // 0101 << 1 = 1010
  5 << 2 = 20   // 0101 << 2 = 10100
```
```
  void generateSubsets(int[] nums) {
      int n = nums.length;
      for (int mask = 0; mask < (1 << n); mask++) {
          List<Integer> subset = new ArrayList<>();
          for (int i = 0; i < n; i++) {
              if ((mask & (1 << i)) != 0) {
```

INTERVIEW TIPS:
  - Understand the core concepts and trade-offs
  - Be ready to explain with real-world examples
  - Discuss performance implications and best practices
  - Show awareness of common pitfalls

```
## References & Learn More

- [LeetCode](https://leetcode.com/)
- [NeetCode](https://neetcode.io/)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [Levels.fyi](https://www.levels.fyi/)
- [Cracking the Coding Interview](http://www.crackingthecodinginterview.com/)
