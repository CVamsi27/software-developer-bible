# Circuit Breaker

## Definition

Circuit Breaker is a design pattern that prevents an application from repeatedly trying to execute an operation that's likely to fail. It wraps calls to external services and monitors for failures, opening the circuit to stop requests when failures exceed a threshold, and allowing limited requests through to test recovery.

## Why Do We Need It?

In microservices:
- Prevent cascade failures when downstream services fail
- Allow failing services time to recover
- Provide fallback behavior during outages
- Reduce load on struggling services
- Improve system resilience and user experience

## How It Works

### Circuit Breaker States

```
┌─────────────────────────────────────────────────────────────────┐
│                    CIRCUIT BREAKER STATES                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────┐     Failure Threshold     ┌─────────┐            │
│   │ CLOSED  │ ─────────────────────────>│  OPEN   │            │
│   │         │                           │         │            │
│   │ Requests│                           │ Requests│            │
│   │ Pass    │                           │ Blocked │            │
│   └─────────┘<───────────────────────── └─────────┘            │
│        ▲                                │                       │
│        │ Success                        │ Timeout               │
│        │                                │                       │
│        │         ┌───────────┐          │                       │
│        └─────────│ HALF-OPEN │<─────────┘                       │
│                  │           │                                  │
│                  │ Probe     │                                  │
│                  │ Requests  │                                  │
│                  └───────────┘                                  │
└─────────────────────────────────────────────────────────────────┘
```

### State Transitions

```
CLOSED → OPEN: When failure count exceeds threshold
OPEN → HALF-OPEN: After timeout period expires
HALF-OPEN → CLOSED: If probe request succeeds
HALF-OPEN → OPEN: If probe request fails
```

### Request Flow

```
                    ┌─────────────────┐
                    │  Client Request │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Circuit Breaker │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
         ┌────────┐    ┌────────┐    ┌────────┐
         │ CLOSED │    │  OPEN  │    │HALF-   │
         │        │    │        │    │  OPEN  │
         └───┬────┘    └───┬────┘    └───┬────┘
             │             │             │
             ▼             ▼             ▼
        ┌────────┐    ┌────────┐    ┌────────┐
        │Forward │    │Reject/ │    │Forward │
        │Request │    │Fallback│    │Probe   │
        └────────┘    └────────┘    └────────┘
```

## Code Examples

### TypeScript - Basic Circuit Breaker

```typescript
enum CircuitState {
  CLOSED = 'CLOSED',
  OPEN = 'OPEN',
  HALF_OPEN = 'HALF_OPEN',
}

interface CircuitBreakerConfig {
  failureThreshold: number;
  successThreshold: number;
  timeout: number;
  monitorInterval: number;
}

interface CircuitBreakerStats {
  failures: number;
  successes: number;
  lastFailureTime: number;
  lastSuccessTime: number;
}

class CircuitBreaker {
  private state: CircuitState = CircuitState.CLOSED;
  private stats: CircuitBreakerStats = {
    failures: 0,
    successes: 0,
    lastFailureTime: 0,
    lastSuccessTime: 0,
  };
  private nextAttempt: number = 0;
  private config: CircuitBreakerConfig;

  constructor(config: Partial<CircuitBreakerConfig> = {}) {
    this.config = {
      failureThreshold: config.failureThreshold || 5,
      successThreshold: config.successThreshold || 2,
      timeout: config.timeout || 30000,
      monitorInterval: config.monitorInterval || 10000,
    };
  }

  async execute<T>(operation: () => Promise<T>): Promise<T> {
    if (this.state === CircuitState.OPEN) {
      if (Date.now() > this.nextAttempt) {
        this.state = CircuitState.HALF_OPEN;
        console.log('Circuit breaker: OPEN → HALF_OPEN');
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess(): void {
    this.stats.successes++;
    this.stats.lastSuccessTime = Date.now();

    if (this.state === CircuitState.HALF_OPEN) {
      if (this.stats.successes >= this.config.successThreshold) {
        this.state = CircuitState.CLOSED;
        this.stats.failures = 0;
        console.log('Circuit breaker: HALF_OPEN → CLOSED');
      }
    }

    if (this.state === CircuitState.CLOSED) {
      this.stats.failures = 0;
    }
  }

  private onFailure(): void {
    this.stats.failures++;
    this.stats.lastFailureTime = Date.now();

    if (this.state === CircuitState.CLOSED) {
      if (this.stats.failures >= this.config.failureThreshold) {
        this.state = CircuitState.OPEN;
        this.nextAttempt = Date.now() + this.config.timeout;
        console.log('Circuit breaker: CLOSED → OPEN');
      }
    } else if (this.state === CircuitState.HALF_OPEN) {
      this.state = CircuitState.OPEN;
      this.nextAttempt = Date.now() + this.config.timeout;
      console.log('Circuit breaker: HALF_OPEN → OPEN');
    }
  }

  getState(): CircuitState {
    return this.state;
  }

  getStats(): CircuitBreakerStats {
    return { ...this.stats };
  }

  reset(): void {
    this.state = CircuitState.CLOSED;
    this.stats = {
      failures: 0,
      successes: 0,
      lastFailureTime: 0,
      lastSuccessTime: 0,
    };
    console.log('Circuit breaker: Reset to CLOSED');
  }
}
```

### TypeScript - Advanced Circuit Breaker with Fallback

```typescript
interface FallbackConfig {
  enabled: boolean;
  timeout: number;
}

class AdvancedCircuitBreaker<T> {
  private circuit: CircuitBreaker;
  private fallbackFn?: (error: Error) => Promise<T>;
  private fallbackConfig: FallbackConfig;

  constructor(
    private serviceName: string,
    config: Partial<CircuitBreakerConfig> = {},
    fallbackConfig: Partial<FallbackConfig> = {}
  ) {
    this.circuit = new CircuitBreaker(config);
    this.fallbackConfig = {
      enabled: fallbackConfig.enabled ?? true,
      timeout: fallbackConfig.timeout ?? 5000,
    };
  }

  withFallback(fallbackFn: (error: Error) => Promise<T>): this {
    this.fallbackFn = fallbackFn;
    return this;
  }

  async call(operation: () => Promise<T>): Promise<T> {
    try {
      return await this.circuit.execute(operation);
    } catch (error) {
      console.error(`Circuit breaker caught error for ${this.serviceName}:`, error);

      if (this.fallbackConfig.enabled && this.fallbackFn) {
        try {
          return await Promise.race([
            this.fallbackFn(error as Error),
            this.timeoutPromise(this.fallbackConfig.timeout),
          ]);
        } catch (fallbackError) {
          console.error(`Fallback failed for ${this.serviceName}:`, fallbackError);
          throw error;
        }
      }

      throw error;
    }
  }

  private timeoutPromise(ms: number): Promise<never> {
    return new Promise((_, reject) => {
      setTimeout(() => reject(new Error('Fallback timeout')), ms);
    });
  }

  getState(): CircuitState {
    return this.circuit.getState();
  }

  getStats(): CircuitBreakerStats {
    return this.circuit.getStats();
  }
}

// Usage example
class UserService {
  private circuit: AdvancedCircuitBreaker<any>;

  constructor() {
    this.circuit = new AdvancedCircuitBreaker('user-service', {
      failureThreshold: 3,
      timeout: 5000,
    }).withFallback(async (error) => {
      // Return cached data or default
      return this.getCachedUser();
    });
  }

  async getUser(userId: string): Promise<any> {
    return this.circuit.call(async () => {
      const response = await fetch(`http://user-service/users/${userId}`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      return response.json();
    });
  }

  private async getCachedUser(): Promise<any> {
    // Return cached or default user
    return { id: 'default', name: 'Guest User' };
  }
}
```

### TypeScript - Retry with Exponential Backoff

```typescript
interface RetryConfig {
  maxRetries: number;
  baseDelay: number;
  maxDelay: number;
  backoffMultiplier: number;
  jitter: boolean;
}

class RetryWithBackoff {
  private config: RetryConfig;

  constructor(config: Partial<RetryConfig> = {}) {
    this.config = {
      maxRetries: config.maxRetries || 3,
      baseDelay: config.baseDelay || 1000,
      maxDelay: config.maxDelay || 30000,
      backoffMultiplier: config.backoffMultiplier || 2,
      jitter: config.jitter ?? true,
    };
  }

  async execute<T>(
    operation: () => Promise<T>,
    shouldRetry?: (error: Error) => boolean
  ): Promise<T> {
    let lastError: Error | null = null;

    for (let attempt = 0; attempt <= this.config.maxRetries; attempt++) {
      try {
        return await operation();
      } catch (error) {
        lastError = error as Error;

        if (attempt === this.config.maxRetries) {
          break;
        }

        if (shouldRetry && !shouldRetry(lastError)) {
          break;
        }

        const delay = this.calculateDelay(attempt);
        console.log(
          `Attempt ${attempt + 1} failed, retrying in ${delay}ms...`
        );
        await this.sleep(delay);
      }
    }

    throw lastError;
  }

  private calculateDelay(attempt: number): number {
    let delay = this.config.baseDelay * Math.pow(this.config.backoffMultiplier, attempt);
    delay = Math.min(delay, this.config.maxDelay);

    if (this.config.jitter) {
      delay = this.addJitter(delay);
    }

    return delay;
  }

  private addJitter(delay: number): number {
    return delay + Math.random() * delay * 0.1;
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Usage with circuit breaker
class ResilientServiceClient {
  private circuitBreaker: AdvancedCircuitBreaker<any>;
  private retry: RetryWithBackoff;

  constructor(private baseUrl: string) {
    this.circuitBreaker = new AdvancedCircuitBreaker('external-service', {
      failureThreshold: 5,
      timeout: 10000,
    });

    this.retry = new RetryWithBackoff({
      maxRetries: 3,
      baseDelay: 1000,
    });
  }

  async call<T>(path: string): Promise<T> {
    return this.circuitBreaker.call(async () => {
      return this.retry.execute(
        async () => {
          const response = await fetch(`${this.baseUrl}${path}`);

          if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
          }

          return response.json();
        },
        (error) => {
          // Don't retry client errors (4xx)
          const message = error.message;
          return !message.includes('4') && !message.includes('400');
        }
      );
    });
  }
}
```

### TypeScript - Circuit Breaker with Metrics

```typescript
import { EventEmitter } from 'events';

interface CircuitMetrics {
  totalRequests: number;
  successfulRequests: number;
  failedRequests: number;
  rejectedRequests: number;
  averageResponseTime: number;
  lastStateChange: Date;
}

class MonitoredCircuitBreaker extends EventEmitter {
  private breaker: CircuitBreaker;
  private metrics: CircuitMetrics;
  private responseTimes: number[] = [];

  constructor(
    private serviceName: string,
    config: Partial<CircuitBreakerConfig> = {}
  ) {
    super();
    this.breaker = new CircuitBreaker(config);
    this.metrics = {
      totalRequests: 0,
      successfulRequests: 0,
      failedRequests: 0,
      rejectedRequests: 0,
      averageResponseTime: 0,
      lastStateChange: new Date(),
    };
  }

  async execute<T>(operation: () => Promise<T>): Promise<T> {
    const startTime = Date.now();
    this.metrics.totalRequests++;

    try {
      const result = await this.breaker.execute(operation);
      const duration = Date.now() - startTime;

      this.metrics.successfulRequests++;
      this.recordResponseTime(duration);
      this.emit('success', { serviceName: this.serviceName, duration });

      return result;
    } catch (error) {
      const duration = Date.now() - startTime;
      const err = error as Error;

      if (err.message === 'Circuit breaker is OPEN') {
        this.metrics.rejectedRequests++;
        this.emit('rejected', { serviceName: this.serviceName, duration });
      } else {
        this.metrics.failedRequests++;
        this.recordResponseTime(duration);
        this.emit('failure', { serviceName: this.serviceName, duration, error: err });
      }

      throw error;
    }
  }

  private recordResponseTime(duration: number): void {
    this.responseTimes.push(duration);
    if (this.responseTimes.length > 100) {
      this.responseTimes.shift();
    }
    this.metrics.averageResponseTime =
      this.responseTimes.reduce((a, b) => a + b, 0) / this.responseTimes.length;
  }

  getMetrics(): CircuitMetrics {
    return {
      ...this.metrics,
      lastStateChange: new Date(),
    };
  }

  getState(): CircuitState {
    return this.breaker.getState();
  }

  reset(): void {
    this.breaker.reset();
    this.metrics = {
      totalRequests: 0,
      successfulRequests: 0,
      failedRequests: 0,
      rejectedRequests: 0,
      averageResponseTime: 0,
      lastStateChange: new Date(),
    };
    this.responseTimes = [];
  }
}

// Health check endpoint
class CircuitBreakerHealthCheck {
  private breakers: Map<string, MonitoredCircuitBreaker> = new Map();

  register(name: string, breaker: MonitoredCircuitBreaker): void {
    this.breakers.set(name, breaker);
  }

  getHealthStatus(): Record<string, any> {
    const status: Record<string, any> = {};

    for (const [name, breaker] of this.breakers) {
      const metrics = breaker.getMetrics();
      status[name] = {
        state: breaker.getState(),
        metrics,
        healthy: breaker.getState() !== CircuitState.OPEN,
      };
    }

    return status;
  }

  isHealthy(): boolean {
    for (const breaker of this.breakers.values()) {
      if (breaker.getState() === CircuitState.OPEN) {
        return false;
      }
    }
    return true;
  }
}
```

## Real-World Use Cases

### 1. Netflix
- Circuit breakers on all external service calls
- Fallback to cached data or degraded functionality
- Prevent cascade failures across microservices

### 2. E-Commerce
- Payment service circuit breaker
- Fallback to alternative payment provider
- Cache product data when inventory service fails

### 3. Social Media
- Circuit breaker on recommendation service
- Show cached recommendations during outage
- Graceful degradation of features

### 4. Banking
- Circuit breaker on core banking API
- Fallback to read-only mode during issues
- Queue transactions for later processing

## Common Mistakes

1. **Wrong thresholds** - Too sensitive or not sensitive enough
2. **No fallback** - Circuit opens with no recovery path
3. **Not monitoring** - Missing visibility into circuit state
4. **No timeout** - Requests hang indefinitely
5. **Ignoring half-open** - Not allowing recovery testing
6. **Not resetting** - Circuit stays open permanently
7. **Wrong error classification** - Retrying non-retryable errors
8. **No logging** - Can't debug circuit breaker behavior

## Best Practices

1. **Set appropriate thresholds** - Based on service SLA and error tolerance
2. **Always implement fallback** - Provide degraded functionality
3. **Monitor circuit state** - Alert on state changes
4. **Use timeouts** - Prevent hung requests
5. **Log state transitions** - Essential for debugging
6. **Test circuit breakers** - Chaos engineering, fault injection
7. **Use exponential backoff** - For retries
8. **Consider bulkheading** - Isolate failures to specific services

## Performance Considerations

- **Timeout values** - Balance between responsiveness and allowing recovery
- **Monitor interval** - How often to check service health
- **Failure threshold** - Number of failures before opening circuit
- **Success threshold** - Number of successes before closing circuit
- **Jitter** - Prevent thundering herd when circuit closes

## Interview Questions

### Beginner (5-10)

1. **What is the Circuit Breaker pattern?**
   - Pattern that prevents cascade failures by stopping calls to failing services.

2. **Why use circuit breakers?**
   - Prevent cascade failures, allow recovery, provide fallback behavior.

3. **What are the three states of a circuit breaker?**
   - CLOSED (normal), OPEN (failing), HALF-OPEN (testing recovery).

4. **When does circuit breaker open?**
   - When failure count exceeds threshold within time window.

5. **When does circuit breaker close?**
   - When probe requests succeed in HALF-OPEN state.

6. **What is a fallback?**
   - Alternative behavior when circuit is open (cached data, default response).

7. **How is circuit breaker different from retry?**
   - Circuit breaker stops requests; retry attempts again after delay.

8. **What is exponential backoff?**
   - Increasing delay between retry attempts to reduce load.

### Intermediate (5-10)

9. **How do you set failure thresholds?**
   - Based on service SLA, error tolerance, and recovery time.

10. **What is bulkheading?**
    - Isolating failures to prevent one failing service from affecting others.

11. **How do you monitor circuit breakers?**
    - Track state changes, failure rates, fallback usage, response times.

12. **What is a half-open state?**
    - Testing if service has recovered with limited probe requests.

13. **How do you handle timeout in circuit breakers?**
    - Set appropriate timeout values, use Promise.race for timeout.

14. **What is a health check?**
    - Periodic probe to determine if service is healthy.

15. **How do you test circuit breakers?**
    - Fault injection, chaos engineering, integration tests.

16. **What metrics should you track?**
    - Request count, failure rate, circuit state, response time.

### Senior (10-15)

17. **Design a circuit breaker system from scratch.**
    - State machine, configuration, monitoring, fallback integration.

18. **How do you handle distributed circuit breakers?**
    - Shared state via distributed cache, eventual consistency.

19. **What is the relationship between circuit breakers and service mesh?**
    - Service mesh provides built-in circuit breaking at infrastructure level.

20. **How do you implement circuit breakers in event-driven systems?**
    - Circuit breakers on event producers/consumers, dead letter queues.

21. **Explain circuit breaker patterns in microservices.**
    - Hierarchical circuits, cascading fallbacks, compensation.

22. **How do you handle circuit breakers during deployments?**
    - Gradual rollout, feature flags, traffic shifting.

23. **What is adaptive circuit breaking?**
    - Dynamic thresholds based on real-time metrics.

24. **How do you debug circuit breaker issues?**
    - Distributed tracing, logging, metrics visualization.

25. **What are the limitations of circuit breakers?**
    - Eventual consistency, complex configuration, false positives.

### FAANG-style (5-10)

26. **Design Netflix's circuit breaker system.**
    - Hystrix-like implementation, fallback strategies, monitoring.

27. **How would you implement circuit breakers for 1000+ services?**
    - Hierarchical circuits, bulkheading, shared infrastructure.

28. **Design circuit breakers for global deployment.**
    - Regional circuits, global state, latency-aware thresholds.

29. **How do you prevent thundering herd with circuit breakers?**
    - Jitter, gradual recovery, request coalescing.

30. **Explain circuit breakers in serverless architecture.**
    - Cold start handling, function-level circuits, async fallbacks.

### Follow-ups (5-10)

31. **How do you migrate to circuit breakers?**
    - Gradual adoption, wrapper pattern, feature flags.

32. **What is the impact of circuit breakers on latency?**
    - Adds overhead, but benefits outweigh costs during failures.

33. **How do you choose between circuit breaker and retry?**
    - Circuit breaker for persistent failures; retry for transient issues.

34. **What is the future of circuit breaking?**
    - AI-driven adaptive thresholds, service mesh integration.

35. **How do you handle circuit breakers in synchronous vs async?**
    - Different timeout strategies, async monitoring.

## Summary

Circuit Breaker is essential for building resilient microservices. It prevents cascade failures by stopping requests to failing services and providing fallback behavior. Key aspects include state management, threshold configuration, and monitoring.

## Cheat Sheet

```
┌─────────────────────────────────────────────────────────┐
│                CIRCUIT BREAKER                          │
├─────────────────────────────────────────────────────────┤
│ STATES:                                                 │
│ • CLOSED: Normal operation, requests pass through       │
│ • OPEN: Failing, requests blocked/rejected              │
│ • HALF-OPEN: Testing recovery, limited probe requests   │
│                                                         │
│ TRANSITIONS:                                            │
│ CLOSED → OPEN: Failure threshold exceeded               │
│ OPEN → HALF-OPEN: Timeout period expires                │
│ HALF-OPEN → CLOSED: Probe requests succeed              │
│ HALF-OPEN → OPEN: Probe requests fail                   │
│                                                         │
│ KEY CONFIG:                                             │
│ • Failure Threshold: # failures before opening          │
│ • Success Threshold: # successes before closing         │
│ • Timeout: Time before attempting probe                 │
│                                                         │
│ BEST PRACTICES:                                         │
│ • Always implement fallback                             │
│ • Monitor circuit state changes                         │
│ • Use exponential backoff with retry                    │
│ • Log state transitions                                 │
│ • Test with chaos engineering                           │
│ • Consider bulkheading                                  │
│                                                         │
│ METRICS:                                                │
│ • Request count, success/failure rates                  │
│ • Circuit state, response times                         │
│ • Fallback usage, rejection rates                       │
└─────────────────────────────────────────────────────────┘
```

---

## References & Learn More
- [Microservices Patterns by Chris Richardson](https://www.amazon.com/Microservices-Patterns-designing-Chris-Richardson/dp/1617294543)
- [Building Microservices by Sam Newman](https://www.amazon.com/Building-Microservices-designing-Systems/dp/1491950358)
- [Microservices.io](https://microservices.io/)
- [Martin Fowler - Microservices](https://martinfowler.com/microservices/)
- [Domain-Driven Design by Eric Evans](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215)