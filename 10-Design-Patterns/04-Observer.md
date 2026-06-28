# Observer Pattern

## Definition

The Observer pattern is a behavioral design pattern that defines a one-to-many dependency between objects so that when one object (the subject) changes state, all its dependents (observers) are notified and updated automatically.

Also known as Publish-Subscribe (Pub/Sub) pattern, it's one of the most widely used patterns in event-driven programming, UI frameworks, and real-time applications.

## Why Do We Need It?

Without the Observer pattern, objects are tightly coupled, leading to:

1. **Tight coupling**: Subject needs to know about all observers
2. **Code duplication**: Notification logic repeated everywhere
3. **Difficult maintenance**: Adding new observers requires modifying the subject
4. **Memory leaks**: Observers not properly cleaned up

## How It Works

The Observer pattern works by:

1. Defining a subject that maintains a list of observers
2. Providing methods to attach, detach, and notify observers
3. Defining an observer interface with an update method
4. When the subject's state changes, it notifies all observers

```
┌─────────────────────────────────────────────────┐
│              Observer Pattern                   │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐                               │
│  │   Subject     │◄── Maintains observer list    │
│  └──────────────┘                               │
│         │                                       │
│         │ attach(observer)                      │
│         │ detach(observer)                      │
│         │ notify()                             │
│         ▼                                       │
│  ┌──────────────────────────────────────────┐   │
│  │         Observer Interface               │   │
│  │    + update(data): void                  │   │
│  └──────────────────────────────────────────┘   │
│         │                                       │
│    ┌────┴────┬────────────┐                    │
│    ▼         ▼            ▼                    │
│ ┌──────┐ ┌──────┐   ┌──────┐                  │
│ │Obs 1 │ │Obs 2 │   │Obs 3 │                  │
│ └──────┘ └──────┘   └──────┘                  │
│                                                  │
│  When subject changes, all observers             │
│  are notified automatically                      │
└─────────────────────────────────────────────────┘
```

## Code Examples

### Basic Observer Pattern

```typescript
// Observer interface
interface Observer {
  update(data: any): void;
  getId(): string;
}

// Subject interface
interface Subject {
  attach(observer: Observer): void;
  detach(observer: Observer): void;
  notify(): void;
}

// Concrete subject
class NewsAgency implements Subject {
  private observers: Observer[] = [];
  private latestNews: string = '';

  attach(observer: Observer): void {
    const exists = this.observers.find(o => o.getId() === observer.getId());
    if (!exists) {
      this.observers.push(observer);
      console.log(`Observer ${observer.getId()} attached`);
    }
  }

  detach(observer: Observer): void {
    const index = this.observers.findIndex(o => o.getId() === observer.getId());
    if (index !== -1) {
      this.observers.splice(index, 1);
      console.log(`Observer ${observer.getId()} detached`);
    }
  }

  notify(): void {
    console.log(`Notifying ${this.observers.length} observers...`);
    this.observers.forEach(observer => {
      observer.update(this.latestNews);
    });
  }

  addNews(news: string): void {
    this.latestNews = news;
    console.log(`News added: ${news}`);
    this.notify();
  }
}

// Concrete observers
class NewsChannel implements Observer {
  private id: string;
  private name: string;

  constructor(id: string, name: string) {
    this.id = id;
    this.name = name;
  }

  update(data: string): void {
    console.log(`${this.name} received news: ${data}`);
  }

  getId(): string {
    return this.id;
  }
}

class NewsApp implements Observer {
  private id: string;
  private notifications: string[] = [];

  constructor(id: string) {
    this.id = id;
  }

  update(data: string): void {
    this.notifications.push(data);
    console.log(`App ${this.id} received: ${data}`);
  }

  getId(): string {
    return this.id;
  }

  getNotifications(): string[] {
    return [...this.notifications];
  }
}

// Usage
const agency = new NewsAgency();
const channel1 = new NewsChannel('ch1', 'CNN');
const channel2 = new NewsChannel('ch2', 'BBC');
const app = new NewsApp('app1');

agency.attach(channel1);
agency.attach(channel2);
agency.attach(app);

agency.addNews('Breaking: New technology breakthrough!');

agency.detach(channel2);

agency.addNews('Update: Market reaches new high');
```

### Event Emitter Pattern (Node.js Style)

```typescript
type EventCallback = (...args: any[]) => void;

class EventEmitter {
  private listeners: Map<string, EventCallback[]> = new Map();
  private onceListeners: Map<string, EventCallback[]> = new Map();

  on(event: string, callback: EventCallback): this {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event)!.push(callback);
    return this;
  }

  once(event: string, callback: EventCallback): this {
    if (!this.onceListeners.has(event)) {
      this.onceListeners.set(event, []);
    }
    this.onceListeners.get(event)!.push(callback);
    return this;
  }

  off(event: string, callback: EventCallback): this {
    const listeners = this.listeners.get(event);
    if (listeners) {
      const index = listeners.indexOf(callback);
      if (index !== -1) {
        listeners.splice(index, 1);
      }
    }

    const onceListeners = this.onceListeners.get(event);
    if (onceListeners) {
      const index = onceListeners.indexOf(callback);
      if (index !== -1) {
        onceListeners.splice(index, 1);
      }
    }

    return this;
  }

  emit(event: string, ...args: any[]): boolean {
    const listeners = this.listeners.get(event) || [];
    const onceListeners = this.onceListeners.get(event) || [];

    const allListeners = [...listeners, ...onceListeners];

    if (allListeners.length === 0) {
      return false;
    }

    allListeners.forEach(listener => {
      listener(...args);
    });

    // Clear once listeners
    this.onceListeners.delete(event);

    return true;
  }

  removeAllListeners(event?: string): this {
    if (event) {
      this.listeners.delete(event);
      this.onceListeners.delete(event);
    } else {
      this.listeners.clear();
      this.onceListeners.clear();
    }
    return this;
  }

  listenerCount(event: string): number {
    const listeners = this.listeners.get(event) || [];
    const onceListeners = this.onceListeners.get(event) || [];
    return listeners.length + onceListeners.length;
  }

  eventNames(): string[] {
    const eventSet = new Set([
      ...this.listeners.keys(),
      ...this.onceListeners.keys()
    ]);
    return Array.from(eventSet);
  }
}

// Usage
const emitter = new EventEmitter();

// Subscribe to events
emitter.on('userCreated', (user) => {
  console.log('User created:', user);
});

emitter.on('userCreated', (user) => {
  console.log('Sending welcome email to:', user.email);
});

// One-time subscription
emitter.once('appStarted', () => {
  console.log('App started - this will only log once');
});

// Emit events
emitter.emit('userCreated', { id: 1, name: 'John', email: 'john@example.com' });
emitter.emit('appStarted');
emitter.emit('appStarted'); // This won't trigger the once listener

// Remove listener
const handler = (data) => console.log(data);
emitter.on('data', handler);
emitter.off('data', handler);
```

### React-Style State Management

```typescript
interface State {
  count: number;
  user: { name: string; email: string } | null;
}

type StateListener<K extends keyof State> = (value: State[K], oldValue: State[K]) => void;

class Store {
  private state: State = {
    count: 0,
    user: null
  };

  private listeners: Map<string, Set<StateListener<any>>> = new Map();

  get<K extends keyof State>(key: K): State[K] {
    return this.state[key];
  }

  set<K extends keyof State>(key: K, value: State[K]): void {
    const oldValue = this.state[key];
    this.state[key] = value;
    this.notify(key, value, oldValue);
  }

  subscribe<K extends keyof State>(key: K, listener: StateListener<K>): () => void {
    if (!this.listeners.has(key)) {
      this.listeners.set(key, new Set());
    }

    this.listeners.get(key)!.add(listener);

    // Return unsubscribe function
    return () => {
      this.listeners.get(key)?.delete(listener);
    };
  }

  private notify<K extends keyof State>(key: K, newValue: State[K], oldValue: State[K]): void {
    const listeners = this.listeners.get(key);
    if (listeners) {
      listeners.forEach(listener => {
        listener(newValue, oldValue);
      });
    }
  }
}

// Usage
const store = new Store();

// Subscribe to changes
const unsubscribe = store.subscribe('count', (newValue, oldValue) => {
  console.log(`Count changed from ${oldValue} to ${newValue}`);
});

store.subscribe('user', (user) => {
  console.log('User changed:', user);
});

// Update state
store.set('count', 1); // Logs: Count changed from 0 to 1
store.set('count', 2); // Logs: Count changed from 1 to 2
store.set('user', { name: 'John', email: 'john@example.com' });

// Unsubscribe
unsubscribe();
store.set('count', 3); // No log
```

### Reactive Data Binding

```typescript
interface BindingOptions {
  debounce?: number;
  transform?: (value: any) => any;
}

class ReactiveProperty<T> {
  private value: T;
  private listeners: Set<(value: T) => void> = new Set();
  private options: BindingOptions;
  private debounceTimer: NodeJS.Timeout | null = null;

  constructor(initialValue: T, options: BindingOptions = {}) {
    this.value = initialValue;
    this.options = options;
  }

  get(): T {
    return this.value;
  }

  set(newValue: T): void {
    const transformedValue = this.options.transform
      ? this.options.transform(newValue)
      : newValue;

    if (this.options.debounce) {
      if (this.debounceTimer) {
        clearTimeout(this.debounceTimer);
      }
      this.debounceTimer = setTimeout(() => {
        this.value = transformedValue;
        this.notify();
      }, this.options.debounce);
    } else {
      this.value = transformedValue;
      this.notify();
    }
  }

  subscribe(listener: (value: T) => void): () => void {
    this.listeners.add(listener);

    return () => {
      this.listeners.delete(listener);
    };
  }

  private notify(): void {
    this.listeners.forEach(listener => {
      listener(this.value);
    });
  }
}

// Usage
const searchQuery = new ReactiveProperty<string>('', {
  debounce: 300
});

const unsubscribe = searchQuery.subscribe((value) => {
  console.log('Searching for:', value);
});

searchQuery.set('hello'); // Debounced - will execute after 300ms
searchQuery.set('hello world'); // Previous timer cleared, new one set
```

## Real-World Use Cases

### 1. User Activity Tracker

```typescript
interface Activity {
  type: string;
  timestamp: Date;
  data: any;
}

interface ActivityListener {
  onActivity(activity: Activity): void;
}

class UserActivityTracker {
  private listeners: ActivityListener[] = [];
  private activities: Activity[] = [];

  addListener(listener: ActivityListener): void {
    this.listeners.push(listener);
  }

  removeListener(listener: ActivityListener): void {
    const index = this.listeners.indexOf(listener);
    if (index !== -1) {
      this.listeners.splice(index, 1);
    }
  }

  track(activity: Omit<Activity, 'timestamp'>): void {
    const fullActivity: Activity = {
      ...activity,
      timestamp: new Date()
    };

    this.activities.push(fullActivity);
    this.notifyListeners(fullActivity);
  }

  private notifyListeners(activity: Activity): void {
    this.listeners.forEach(listener => {
      listener.onActivity(activity);
    });
  }

  getActivities(): Activity[] {
    return [...this.activities];
  }
}

// Concrete listeners
class AnalyticsTracker implements ActivityListener {
  onActivity(activity: Activity): void {
    console.log(`[Analytics] ${activity.type}:`, activity.data);
    // Send to analytics service
  }
}

class Logger implements ActivityListener {
  onActivity(activity: Activity): void {
    console.log(`[Logger] ${activity.timestamp.toISOString()}: ${activity.type}`);
  }
}

class AlertSystem implements ActivityListener {
  onActivity(activity: Activity): void {
    if (activity.type === 'login_failed') {
      console.log(`[Alert] Failed login attempt:`, activity.data);
      // Send security alert
    }
  }
}

// Usage
const tracker = new UserActivityTracker();
tracker.addListener(new AnalyticsTracker());
tracker.addListener(new Logger());
tracker.addListener(new AlertSystem());

tracker.track({ type: 'page_view', data: { page: '/home' } });
tracker.track({ type: 'login_failed', data: { ip: '192.168.1.1' } });
```

### 2. Price Alert System

```typescript
interface PriceAlert {
  productId: string;
  targetPrice: number;
  condition: 'below' | 'above';
}

interface PriceChange {
  productId: string;
  oldPrice: number;
  newPrice: number;
}

interface PriceAlertListener {
  onPriceAlert(alert: PriceAlert, currentPrice: number): void;
}

class PriceMonitor {
  private alerts: PriceAlert[] = [];
  private listeners: PriceAlertListener[] = [];
  private prices: Map<string, number> = new Map();

  addAlert(alert: PriceAlert): void {
    this.alerts.push(alert);
  }

  removeAlert(productId: string): void {
    this.alerts = this.alerts.filter(a => a.productId !== productId);
  }

  addListener(listener: PriceAlertListener): void {
    this.listeners.push(listener);
  }

  updatePrice(productId: string, newPrice: number): void {
    const oldPrice = this.prices.get(productId);
    this.prices.set(productId, newPrice);

    if (oldPrice !== undefined) {
      this.checkAlerts(productId, oldPrice, newPrice);
    }
  }

  private checkAlerts(productId: string, oldPrice: number, newPrice: number): void {
    const relevantAlerts = this.alerts.filter(a => a.productId === productId);

    relevantAlerts.forEach(alert => {
      const shouldTrigger =
        (alert.condition === 'below' && newPrice <= alert.targetPrice) ||
        (alert.condition === 'above' && newPrice >= alert.targetPrice);

      if (shouldTrigger) {
        this.notifyListeners(alert, newPrice);
      }
    });
  }

  private notifyListeners(alert: PriceAlert, currentPrice: number): void {
    this.listeners.forEach(listener => {
      listener.onPriceAlert(alert, currentPrice);
    });
  }
}

// Usage
const monitor = new PriceMonitor();
monitor.addListener({
  onPriceAlert: (alert, price) => {
    console.log(`Price alert for ${alert.productId}: ${price}`);
  }
});

monitor.addAlert({ productId: 'laptop', targetPrice: 999, condition: 'below' });
monitor.updatePrice('laptop', 1200); // No alert
monitor.updatePrice('laptop', 899); // Alert triggered!
```

### 3. Form Validation Observer

```typescript
interface ValidationState {
  field: string;
  isValid: boolean;
  error?: string;
}

interface FormObserver {
  onValidationChange(state: ValidationState): void;
  onFormSubmit(isValid: boolean): void;
}

class FormValidator {
  private fields: Map<string, (value: any) => string | null> = new Map();
  private values: Map<string, any> = new Map();
  private observers: FormObserver[] = [];

  addField(name: string, validator: (value: any) => string | null): void {
    this.fields.set(name, validator);
  }

  addObserver(observer: FormObserver): void {
    this.observers.push(observer);
  }

  removeObserver(observer: FormObserver): void {
    const index = this.observers.indexOf(observer);
    if (index !== -1) {
      this.observers.splice(index, 1);
    }
  }

  setValue(field: string, value: any): void {
    this.values.set(field, value);
    this.validateField(field);
  }

  private validateField(field: string): void {
    const validator = this.fields.get(field);
    const value = this.values.get(field);

    if (validator) {
      const error = validator(value);
      const state: ValidationState = {
        field,
        isValid: error === null,
        error: error || undefined
      };

      this.notifyValidation(state);
    }
  }

  validateAll(): boolean {
    let isValid = true;

    this.fields.forEach((validator, field) => {
      const value = this.values.get(field);
      const error = validator(value);

      if (error) {
        isValid = false;
        this.notifyValidation({
          field,
          isValid: false,
          error
        });
      }
    });

    return isValid;
  }

  submit(): void {
    const isValid = this.validateAll();
    this.notifySubmit(isValid);
  }

  private notifyValidation(state: ValidationState): void {
    this.observers.forEach(observer => {
      observer.onValidationChange(state);
    });
  }

  private notifySubmit(isValid: boolean): void {
    this.observers.forEach(observer => {
      observer.onFormSubmit(isValid);
    });
  }
}

// Usage
const form = new FormValidator();
form.addField('email', (value) => {
  if (!value) return 'Email is required';
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return 'Invalid email';
  return null;
});

form.addField('password', (value) => {
  if (!value) return 'Password is required';
  if (value.length < 8) return 'Password too short';
  return null;
});

form.addObserver({
  onValidationChange: (state) => {
    console.log(`${state.field}: ${state.isValid ? 'Valid' : state.error}`);
  },
  onFormSubmit: (isValid) => {
    console.log(`Form submitted: ${isValid ? 'Success' : 'Failed'}`);
  }
});

form.setValue('email', 'invalid-email'); // email: Invalid email
form.setValue('email', 'test@example.com'); // email: Valid
form.setValue('password', '123'); // password: Password too short
form.submit(); // Form submitted: Failed
```

## Common Mistakes

### 1. Memory Leaks

```typescript
// ❌ BAD - Not cleaning up observers
class BadSubject {
  private observers: Observer[] = [];

  attach(observer: Observer): void {
    this.observers.push(observer);
  }

  // No detach method!
  // Observers can't be removed, causing memory leaks
}
```

### 2. Tight Coupling

```typescript
// ❌ BAD - Subject knows about concrete observers
class BadSubject {
  private observers: ConcreteObserver[] = [];

  notify(): void {
    this.observers.forEach(observer => {
      observer.specificMethod(); // Tight coupling
    });
  }
}
```

### 3. Not Handling Errors

```typescript
// ❌ BAD - Observer errors break notification
class BadSubject {
  notify(): void {
    this.observers.forEach(observer => {
      observer.update(this.data); // If one throws, others won't get notified
    });
  }
}
```

### 4. Circular Dependencies

```typescript
// ❌ BAD - Observer notifies subject, causing infinite loop
class BadObserver implements Observer {
  update(data: any): void {
    subject.notify(); // Circular dependency
  }
}
```

## Best Practices

### 1. Always Provide Detach Method

```typescript
// ✅ GOOD - Clean up observers
class Subject {
  private observers: Observer[] = [];

  attach(observer: Observer): void {
    this.observers.push(observer);
  }

  detach(observer: Observer): void {
    const index = this.observers.indexOf(observer);
    if (index !== -1) {
      this.observers.splice(index, 1);
    }
  }
}
```

### 2. Use Weak References When Appropriate

```typescript
// ✅ GOOD - Weak references for automatic cleanup
class Subject {
  private observers: WeakRef<Observer>[] = [];

  attach(observer: Observer): void {
    this.observers.push(new WeakRef(observer));
  }

  notify(): void {
    this.observers = this.observers.filter(ref => {
      const observer = ref.deref();
      if (observer) {
        observer.update(this.data);
        return true;
      }
      return false;
    });
  }
}
```

### 3. Handle Observer Errors

```typescript
// ✅ GOOD - Error handling
class Subject {
  notify(): void {
    this.observers.forEach(observer => {
      try {
        observer.update(this.data);
      } catch (error) {
        console.error('Observer error:', error);
      }
    });
  }
}
```

### 4. Use Interface for Observers

```typescript
// ✅ GOOD - Common interface
interface Observer {
  update(data: any): void;
}

class ConcreteObserver implements Observer {
  update(data: any): void {
    // Implementation
  }
}
```

## Performance Considerations

1. **Notification Overhead**: Notifying many observers has O(n) complexity.

2. **Memory Usage**: Each observer consumes memory; use WeakRef for automatic cleanup.

3. **Synchronous vs Asynchronous**: Consider async notification for heavy observers.

4. **Batch Updates**: Batch multiple state changes before notifying observers.

5. **Priority Ordering**: If observers have priorities, use a priority queue.

## Interview Questions

### Beginner

1. **What is the Observer pattern?**
   - A behavioral pattern that defines a one-to-many dependency between objects.

2. **When would you use Observer pattern?**
   - For event handling, UI updates, notifications, and reactive programming.

3. **What's the difference between Observer and Pub/Sub?**
   - Observer is direct notification; Pub/Sub uses a message broker for decoupling.

4. **How do you prevent memory leaks in Observer?**
   - Always provide a detach method and clean up observers when done.

5. **What are the benefits of Observer pattern?**
   - Loose coupling, automatic notifications, and dynamic relationships.

### Intermediate

6. **How do you handle observer errors?**
   - Use try-catch in notification, log errors, and continue notifying other observers.

7. **Can observers be notified asynchronously?**
   - Yes, use Promise.all or event loop for async notification.

8. **How do you test Observer pattern?**
   - Mock observers, verify notification calls, test attach/detach operations.

9. **What's the relationship between Observer and Strategy?**
   - Observer notifies; Strategy defines algorithms; they can be combined.

10. **How do you handle circular dependencies?**
    - Use event queues, break cycles, or redesign the relationship.

### Senior

11. **How does Observer pattern affect scalability?**
    - Can become a bottleneck with many observers; consider batching or async.

12. **What are the SOLID violations with Observer?**
    - Usually follows SOLID; watch for subject violating Single Responsibility.

13. **How do you handle Observer in microservices?**
    - Use message brokers, event buses, or distributed pub/sub systems.

14. **What are the memory implications of Observer?**
    - Observers persist as long as they're attached; use WeakRef for cleanup.

15. **How do you refactor Observer code?**
    - Extract common logic, use generics, and apply SOLID principles.

### FAANG-style

16. **Design an Observer for a real-time chat system.**
    - Consider scalability, message ordering, and offline users.

17. **How would you implement Observer for distributed systems?**
    - Use message brokers, event sourcing, and eventual consistency.

18. **What are the implications of Observer in cloud-native applications?**
    - Consider serverless functions, event-driven architecture, and scaling.

19. **How do you handle Observer in event-driven architectures?**
    - Use event buses, message queues, and CQRS patterns.

20. **Design an Observer that supports backpressure.**
    - Consider buffering, rate limiting, and flow control.

### Follow-ups

21. **Can Observer pattern be combined with other patterns?**
    - Yes, commonly with Mediator, Command, and Memento patterns.

22. **How do you handle Observer in testing frameworks?**
    - Use dependency injection, create test observers, and mock implementations.

23. **What are the memory implications of Observer pattern?**
    - Observers persist as long as attached; use WeakRef for automatic cleanup.

24. **How do you handle Observer in serverless environments?**
    - Consider stateless design, event-driven triggers, and cold starts.

25. **What's the impact of Observer on code maintainability?**
    - Improves maintainability by decoupling subjects and observers.

## Summary

The Observer pattern is essential for event-driven programming and reactive systems. It provides loose coupling between subjects and observers, automatic notifications, and dynamic relationships. Use it for UI updates, event handling, notifications, and real-time data synchronization.

## Cheat Sheet

```
┌─────────────────────────────────────────────┐
│           OBSERVER PATTERN                  │
├─────────────────────────────────────────────┤
│ ✅ USE WHEN:                                │
│ • One-to-many notifications                 │
│ • Event handling                            │
│ • Reactive programming                      │
│ • UI updates                                │
├─────────────────────────────────────────────┤
│ ❌ AVOID WHEN:                              │
│ • Simple one-to-one relationships           │
│ • Observers are rarely added/removed        │
│ • Performance is critical                   │
│ • Observers have complex dependencies       │
├─────────────────────────────────────────────┤
│ 🎯 KEY CONCEPTS:                           │
│ • Subject maintains observer list           │
│ • Observer interface with update method     │
│ • Attach/detach operations                  │
│ • Automatic notification                    │
├─────────────────────────────────────────────┤
│ ⚠️  WATCH OUT FOR:                          │
│ • Memory leaks                              │
│ • Circular dependencies                     │
│ • Observer errors                           │
│ • Performance with many observers           │
├─────────────────────────────────────────────┤
│ 🔧 RELATED PATTERNS:                       │
│ • Pub/Sub (decoupled)                       │
│ • Mediator (centralized)                    │
│ • Event Sourcing (state changes)            │
└─────────────────────────────────────────────┘
```

## References & Learn More

- [GoF Design Patterns](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)
- [Refactoring Guru: Observer](https://refactoring.guru/design-patterns/observer)
- [Node.js EventEmitter Docs](https://nodejs.org/api/events.html)
