---
section: Microservices
category: Architecture
tags: [concept]
---

# Service Discovery

## Definition

Service Discovery is a mechanism that allows services to find and communicate with each other dynamically in a microservices architecture. Instead of hardcoding network locations, services register themselves with a discovery server and look up other services through it.

## Why Do We Need It?

In microservices:

- Services are deployed across multiple hosts/containers
- Instances are created/destroyed dynamically (auto-scaling, deployments)
- Network locations (IPs, ports) change constantly
- Manual configuration is impossible at scale
- Need automatic detection of healthy instances

## How It Works

### Client-Side Discovery

```text
┌─────────────┐     1. Query      ┌─────────────────┐
│   Client    │ ─────────────────>│  Discovery      │
│  Service A  │<─────────────────│  Server         │
│             │  2. Return list   │  (Eureka/Consul)│
└──────┬──────┘                   └─────────────────┘
       │
       │ 3. Select instance
       ▼
┌─────────────┐
│  Service B  │
│  (Instance) │
└─────────────┘

```

**Flow:**

1. Client queries discovery server for available instances

2. Discovery server returns list of healthy instances

3. Client selects instance (load balancing) and makes request

### Server-Side Discovery

```text
┌─────────────┐     1. Request    ┌─────────────────┐     3. Forward     ┌─────────────┐
│   Client    │ ─────────────────>│  Load Balancer  │ ─────────────────>│  Service B  │
│  Service A  │<─────────────────│  / Router       │<─────────────────│  (Instance) │
└─────────────┘  4. Response      └─────────────────┘  2. Lookup         └─────────────┘
                                    │
                                    ▼
                              ┌─────────────────┐
                              │  Discovery      │
                              │  Server         │
                              └─────────────────┘

```

**Flow:**

1. Client sends request to load balancer/router

2. Load balancer queries discovery server

3. Load balancer forwards to selected instance

4. Response returns through load balancer

## Code Examples

### TypeScript - Service Registration

```typescript
import { v4 as uuidv4 } from 'uuid';

interface ServiceInstance {
  id: string;
  name: string;
  host: string;
  port: number;
  metadata: Record<string, unknown>;
  healthStatus: 'UP' | 'DOWN';
  lastHeartbeat: Date;
}

class ServiceRegistry {
  private services: Map<string, ServiceInstance[]> = new Map();
  private heartbeatInterval: NodeJS.Timeout | null = null;

  register(instance: Omit<ServiceInstance, 'id' | 'lastHeartbeat'>): string {
    const id = uuidv4();
    const fullInstance: ServiceInstance = {
      ...instance,
      id,
      lastHeartbeat: new Date(),
    };

    const instances = this.services.get(instance.name) || [];
    instances.push(fullInstance);
    this.services.set(instance.name, instances);

    console.log(`Service registered: ${instance.name} at ${instance.host}:${instance.port}`);
    return id;
  }

  deregister(serviceName: string, instanceId: string): void {
    const instances = this.services.get(serviceName) || [];
    const filtered = instances.filter(i => i.id !== instanceId);
    this.services.set(serviceName, filtered);
    console.log(`Service deregistered: ${serviceName} instance ${instanceId}`);
  }

  discover(serviceName: string): ServiceInstance[] {
    const instances = this.services.get(serviceName) || [];
    return instances.filter(i => i.healthStatus === 'UP');
  }

  updateHeartbeat(instanceId: string): void {
    for (const [name, instances] of this.services) {
      const instance = instances.find(i => i.id === instanceId);
      if (instance) {
        instance.lastHeartbeat = new Date();
        instance.healthStatus = 'UP';
        break;
      }
    }
  }

  startHealthCheck(intervalMs: number = 30000): void {
    this.heartbeatInterval = setInterval(() => {
      const now = new Date();
      for (const [name, instances] of this.services) {
        const healthy = instances.filter(i => {
          const timeSinceHeartbeat = now.getTime() - i.lastHeartbeat.getTime();
          return timeSinceHeartbeat < 90000; // 90s threshold
        });
        this.services.set(name, healthy);
      }
    }, intervalMs);
  }

  stopHealthCheck(): void {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
    }
  }
}

// Client-side discovery implementation
class ServiceClient {
  constructor(private registry: ServiceRegistry) {}

  async callService<T>(serviceName: string, path: string): Promise<T> {
    const instances = this.registry.discover(serviceName);

    if (instances.length === 0) {
      throw new Error(`No instances available for service: ${serviceName}`);
    }

    // Simple round-robin load balancing
    const instance = instances[Math.floor(Math.random() * instances.length)];
    const url = `http://${instance.host}:${instance.port}${path}`;

    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Service call failed: ${response.statusText}`);
    }

    return response.json() as Promise<T>;
  }
}

```

### TypeScript - Client-Side Discovery with Load Balancing

```typescript
interface LoadBalancer {
  select(instances: ServiceInstance[]): ServiceInstance;
}

class RoundRobinBalancer implements LoadBalancer {
  private index = 0;

  select(instances: ServiceInstance[]): ServiceInstance {
    const instance = instances[this.index % instances.length];
    this.index = (this.index + 1) % instances.length;
    return instance;
  }
}

class RandomBalancer implements LoadBalancer {
  select(instances: ServiceInstance[]): ServiceInstance {
    return instances[Math.floor(Math.random() * instances.length)];
  }
}

class WeightedBalancer implements LoadBalancer {
  select(instances: ServiceInstance[]): ServiceInstance {
    const weights = instances.map(i => i.metadata.weight || 1);
    const totalWeight = weights.reduce((a, b) => a + b, 0);
    let random = Math.random() * totalWeight;

    for (let i = 0; i < instances.length; i++) {
      random -= weights[i];
      if (random <= 0) return instances[i];
    }

    return instances[instances.length - 1];
  }
}

class DiscoveryClient {
  private cache: Map<string, { instances: ServiceInstance[]; expiry: number }> = new Map();
  private cacheTTL = 30000; // 30 seconds

  constructor(
    private registry: ServiceRegistry,
    private loadBalancer: LoadBalancer
  ) {}

  async getServiceInstance(serviceName: string): Promise<ServiceInstance> {
    // Check cache first
    const cached = this.cache.get(serviceName);
    if (cached && Date.now() < cached.expiry) {
      return this.loadBalancer.select(cached.instances);
    }

    // Fetch fresh instances
    const instances = this.registry.discover(serviceName);
    if (instances.length === 0) {
      throw new Error(`No instances available for: ${serviceName}`);
    }

    // Update cache
    this.cache.set(serviceName, {
      instances,
      expiry: Date.now() + this.cacheTTL,
    });

    return this.loadBalancer.select(instances);
  }

  async call<T>(serviceName: string, path: string, options?: RequestInit): Promise<T> {
    const instance = await this.getServiceInstance(serviceName);
    const url = `http://${instance.host}:${instance.port}${path}`;

    const response = await fetch(url, options);
    if (!response.ok) {
      throw new Error(`Service call failed: ${response.status}`);
    }

    return response.json() as Promise<T>;
  }
}

```

### TypeScript - DNS-Based Discovery

```typescript
import dns from 'dns';
import { promisify } from 'util';

const resolveSrv = promisify(dns.resolveSrv);

class DnsServiceDiscovery {
  async discover(serviceName: string): Promise<ServiceInstance[]> {
    try {
      // SRV record lookup: _serviceName._tcp.domain.com
      const records = await resolveSrv(`_${serviceName}._tcp.example.com`);

      return records.map((record, index) => ({
        id: `dns-${serviceName}-${index}`,
        name: serviceName,
        host: record.name,
        port: record.port,
        metadata: { priority: record.priority, weight: record.weight },
        healthStatus: 'UP' as const,
        lastHeartbeat: new Date(),
      }));
    } catch (error) {
      console.error(`DNS discovery failed for ${serviceName}:`, error);
      return [];
    }
  }
}

```

## Real-World Use Cases

### 1. E-Commerce Platform

- Product service instances auto-register when deployed
- Order service discovers product service dynamically
- Handles scaling during flash sales

### 2. Microservices Mesh

- Service mesh (Istio, Linkerd) uses discovery for traffic routing
- Automatic failover when instances become unhealthy
- Blue/green deployments without client changes

### 3. Multi-Region Deployment

- Services register with region-specific discovery servers
- Cross-region discovery for disaster recovery
- Latency-aware instance selection

## Common Mistakes

1. **Hardcoding service locations** - Defeats the purpose of discovery

2. **No health checks** - Routing to dead instances

3. **Missing deregistration** - Ghost instances consuming resources

4. **Ignoring caching** - Overwhelming discovery server

5. **Not handling failures** - Crashing when discovery server is down

6. **Using discovery for synchronous calls only** - Should also work for async

7. **No retry logic** - First failure causes immediate error

## Best Practices

1. **Always implement health checks** - Both active and passive

2. **Cache discovery results** - Reduce load on discovery server

3. **Use circuit breakers** - Prevent cascade failures

4. **Implement graceful degradation** - Fallback to cached data

5. **Monitor discovery server** - High availability is critical

6. **Use DNS when possible** - Built-in caching, no extra infrastructure

7. **Version your services** - Support running multiple versions

8. **Implement retry with backoff** - Handle transient failures

## Performance Considerations

- **Cache TTL**: Balance between freshness and performance (10-60s typical)
- **Health check frequency**: Every 10-30 seconds
- **Heartbeat timeout**: 2-3x heartbeat interval
- **DNS TTL**: 30-60 seconds for service records
- **Connection pooling**: Reuse connections to discovered instances

## Summary

Service Discovery is fundamental to microservices architecture, enabling dynamic service location without hardcoded addresses. Key concepts include client-side vs server-side discovery, health checks, and caching strategies. Modern implementations often use service meshes and integrate with container orchestration platforms.

## Cheat Sheet
```text
┌─────────────────────────────────────────────────────────┐
│                 SERVICE DISCOVERY                       │
├─────────────────────────────────────────────────────────┤
│ CLIENT-SIDE: Client queries registry, selects instance  │
│ SERVER-SIDE: Load balancer handles selection            │
│                                                         │
│ TOOLS: Eureka, Consul, etcd, ZooKeeper, DNS SRV        │
│                                                         │
│ KEY CONCEPTS:                                           │
│ • Registration: Service announces itself                │
│ • Deregistration: Service removes itself                │
│ • Health Check: Verify instance is alive                │
│ • Heartbeat: periodic health signal                     │
│                                                         │
│ BEST PRACTICES:                                         │
│ • Cache discovery results                               │
│ • Implement health checks                               │
│ • Use circuit breakers                                  │
│ • Handle discovery server failure                       │
│ • Monitor registration metrics                          │
└─────────────────────────────────────────────────────────┘

```

---

---

## See Also
- [NestJS](../06-NestJS/)
- [System Design](../11-System-Design/)
- [Docker](../13-Docker/)
- [Kubernetes](../14-Kubernetes/)

## References & Learn More

- [Microservices Patterns by Chris Richardson](https://www.amazon.com/Microservices-Patterns-designing-Chris-Richardson/dp/1617294543)
- [Building Microservices by Sam Newman](https://www.amazon.com/Building-Microservices-designing-Systems/dp/1491950358)
- [Microservices.io](https://microservices.io/)
- [Martin Fowler - Microservices](https://martinfowler.com/microservices/)
- [Domain-Driven Design by Eric Evans](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215)
