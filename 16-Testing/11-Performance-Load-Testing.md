# Performance & Load Testing

[![Category: Quality](https://img.shields.io/badge/category-Quality-brightgreen)](.)

calability requirements under expected and peak loads. Load testing simulates real-world traffic patterns to identify bottlenecks, while stress testing pushes beyond normal limits to find breaking points.

## Tools

| Tool | Type | Use Case |
|------|------|----------|
| **k6** | Open-source, scriptable | Developer-friendly load testing, CI/CD integration |
| **Artillery** | YAML-based, Node.js | HTTP, WebSocket, Socket.IO load testing |
| **Apache JMeter** | GUI-based, Java | Enterprise, complex scenarios |
| **Locust** | Python-based | Distributed load testing |

## Code Examples

### k6 Script

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },  // Ramp up
    { duration: '5m', target: 100 },  // Stay
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/users');
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
```

## Key Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| p50/p95/p99 | Latency percentiles | p95 < 500ms |
| RPS | Requests per second | Varies by system |
| Error rate | % failed requests | < 1% |
| Memory/CPU | Resource utilization | < 80% |

## Summary

- Performance testing validates system behavior under expected and peak load conditions
- k6 provides developer-friendly load testing with JavaScript scripting and CLI execution
- Artillery offers declarative YAML-based load testing with built-in HTTP, WebSocket, and Socket.io support
- Key metrics include response time percentiles, throughput, error rate, and resource utilization
- Load testing should cover smoke, spike, stress, soak, and endurance test scenarios

---

### See Also

- [Core Web Vitals](../26-Performance-Monitoring/01-Core-Web-Vitals.md)
- [Interview Questions](09-Interview-Questions.md)
- [Jest](02-Jest.md)
- [Performance Monitoring](../26-Performance-Monitoring/)
- [Testing Overview](01-Testing-Overview.md)

## References & Learn More

- [k6 Documentation](https://k6.io/docs/)
- [Artillery Documentation](https://www.artillery.io/docs)
