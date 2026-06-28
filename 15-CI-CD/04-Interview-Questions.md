# CI/CD Interview Questions

## 30 Most Asked CI/CD Interview Questions with Detailed Answers

---

### Question 1: What is CI/CD and why is it important?

**Answer:**

**CI (Continuous Integration)**: Automatically build and test code changes when pushed to a repository.

**CD (Continuous Delivery/Deployment)**: Automatically deploy code changes to production.

**Importance:**

- Faster release cycles
- Reduced manual errors
- Early bug detection
- Consistent deployments
- Improved developer productivity

---

### Question 2: What is the difference between Continuous Delivery and Continuous Deployment?

**Answer:**

| Aspect | Continuous Delivery | Continuous Deployment |
|---|---|---|
| Deployment | Manual approval | Automatic |
| Release | On-demand | Every change |
| Risk | Lower (manual gate) | Higher (automated) |
| Speed | Slower | Faster |

---

### Question 3: What are the stages of a CI/CD pipeline?

**Answer:**

```text

1. Source     --> Code commit triggers pipeline

2. Build      --> Compile code, build artifacts

3. Test       --> Unit tests, integration tests

4. Security   --> Vulnerability scanning

5. Package    --> Create Docker image/artifacts

6. Deploy     --> Deploy to staging/production

7. Monitor    --> Verify deployment health

```

---

### Question 4: What is a Dockerfile and why use it?

**Answer:**

A Dockerfile is a text file with instructions to build a Docker image.

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]

```

**Benefits:**

- Reproducible builds
- Environment consistency
- Version control for infrastructure
- Easy deployment

---

### Question 5: What is the difference between a Docker image and a container?

**Answer:**

| Aspect | Image | Container |
|---|---|---|
| State | Immutable | Mutable |
| Storage | Registry | Local filesystem |
| Creation | `docker build` | `docker run` |
| Analogy | Class | Instance |

---

### Question 6: What is Kubernetes and why use it?

**Answer:**

Kubernetes is a container orchestration platform that automates deployment, scaling, and management of containerized applications.

**Key Features:**

- Self-healing
- Horizontal scaling
- Service discovery
- Automated rollouts
- Secret management

---

### Question 7: What is a Kubernetes Deployment?

**Answer:**

A Deployment manages ReplicaSets and Pods, providing:

- Rolling updates
- Rollbacks
- Scaling
- Self-healing

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    spec:
      containers:

        - name: myapp
          image: myapp:1.0.0

```

---

### Question 8: What is Infrastructure as Code (IaC)?

**Answer:**

Managing infrastructure through code instead of manual processes.

**Tools:**

- Terraform
- AWS CloudFormation
- Pulumi
- Ansible

**Benefits:**

- Version control
- Reproducibility
- Automation
- Documentation

---

### Question 9: What is a CI/CD pipeline?

**Answer:**

An automated workflow that builds, tests, and deploys code changes.

```yaml
# Example GitHub Actions workflow
name: CI/CD
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:

      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test
      - run: docker build -t myapp .
      - run: docker push myapp:latest

```

---

### Question 10: What is version control and why is it important?

**Answer:**

Version control tracks changes to code over time.

**Benefits:**

- Collaboration
- History tracking
- Branching/merging
- Rollback capability
- Audit trail

**Tools:**

- Git
- GitHub
- GitLab
- Bitbucket

---

### Question 11: What is a microservices architecture?

**Answer:**

An architecture style where applications are built as small, independent services.

**Benefits:**

- Independent deployment
- Technology flexibility
- Scalability
- Fault isolation

**Challenges:**

- Distributed system complexity
- Network latency
- Data consistency

---

### Question 12: What is a container registry?

**Answer:**

A storage system for Docker images.

**Examples:**

- Docker Hub
- AWS ECR
- Google GCR
- Azure ACR
- Harbor (self-hosted)

---

### Question 13: What is the difference between `docker build` and `docker compose`?

**Answer:**

| Aspect | docker build | docker compose |
|---|---|---|
| Purpose | Build single image | Manage multi-container apps |
| Configuration | Dockerfile | docker-compose.yml |
| Use case | Image creation | Application stack |

---

### Question 14: What is a Kubernetes Service?

**Answer:**

A Service provides stable networking for Pods.

**Types:**

- ClusterIP: Internal only
- NodePort: Expose on node IP
- LoadBalancer: Cloud load balancer

---

### Question 15: What is Helm?

**Answer:**

The package manager for Kubernetes.

**Benefits:**

- Packages multiple manifests
- Manages releases
- Configurable via values
- Rollback capability

---

### Question 16: What is a webhook in CI/CD?

**Answer:**

A webhook triggers a CI/CD pipeline when an event occurs (e.g., code push, PR creation).

---

### Question 17: What is the difference between a build and a release?

**Answer:**

| Aspect | Build | Release |
|---|---|---|
| Purpose | Create artifacts | Distribute artifacts |
| Trigger | Code change | Manual/automated |
| Output | Docker image, binary | Deployed application |

---

### Question 18: What is a staging environment?

**Answer:**

A production-like environment used for testing before deployment.

**Purpose:**

- Integration testing
- Performance testing
- User acceptance testing
- Validation

---

### Question 19: What is a canary deployment?

**Answer:**

Gradually rolling out changes to a small subset of users.

**Benefits:**

- Reduced risk
- Real-world testing
- Easy rollback

---

### Question 20: What is blue-green deployment?

**Answer:**

Maintaining two identical environments and switching traffic between them.

**Benefits:**

- Zero downtime
- Instant rollback
- Easy testing

---

### Question 21: What is feature flagging?

**Answer:**

A technique to enable/disable features without deployment.

```javascript
if (featureFlags.newCheckout) {
  return newCheckoutFlow();
}

```

**Benefits:**

- Decouple deployment from release
- A/B testing
- Gradual rollout

---

### Question 22: What is observability in CI/CD?

**Answer:**

Monitoring and understanding system state through logs, metrics, and traces.

**Components:**

- Logging (ELK, Loki)
- Metrics (Prometheus, Grafana)
- Tracing (Jaeger, Zipkin)

---

### Question 23: What is GitOps?

**Answer:**

A Git-centric approach to infrastructure and deployment.

**Principles:**

- Git as single source of truth
- Automated deployment
- Version control for infrastructure
- Pull-based model

**Tools:**

- Argo CD
- Flux

---

### Question 24: What is a pipeline as code?

**Answer:**

Defining CI/CD pipelines in version-controlled files.

**Examples:**

- GitHub Actions (YAML)
- GitLab CI (.gitlab-ci.yml)
- Jenkins (Jenkinsfile)

---

### Question 25: What is artifact management?

**Answer:**

Storing and versioning build artifacts.

**Examples:**

- Docker images (registry)
- npm packages (npm registry)
- Maven artifacts (Nexus)
- Helm charts (chart museum)

---

### Question 26: What is the difference between a build agent and a runner?

**Answer:**

| Aspect | Build Agent | Runner |
|---|---|---|
| Usage | Jenkins, Bamboo | GitHub Actions, GitLab CI |
| Configuration | Manual | YAML-based |
| Management | Self-hosted | GitHub-hosted or self-hosted |

---

### Question 27: What is a secrets manager?

**Answer:**

A tool for securely storing and accessing secrets.

**Examples:**

- HashiCorp Vault
- AWS Secrets Manager
- Azure Key Vault
- GitHub Secrets

---

### Question 28: What is a Kubernetes Ingress?

**Answer:**

Manages external HTTP/HTTPS access to Services.

**Features:**

- TLS termination
- Host-based routing
- Path-based routing

---

### Question 29: What is a service mesh?

**Answer:**

An infrastructure layer for service communication.

**Examples:**

- Istio
- Linkerd
- Consul Connect

**Features:**

- Traffic management
- Security (mTLS)
- Observability

---

### Question 30: What are the best practices for CI/CD?

**Answer:**

1. **Automate everything** - Build, test, deploy

2. **Version control** - All configuration and code

3. **Fast feedback** - Short pipeline duration

4. **Security scanning** - Integrate in pipeline

5. **Monitoring** - Track pipeline health

6. **Rollback strategy** - Automated rollback on failure

7. **Environment parity** - Same across environments

8. **Secrets management** - Never hardcode

9. **Documentation** - Maintain runbooks
10. **Continuous improvement** - Regular pipeline reviews

---

## Summary

CI/CD interview questions cover:

- Core concepts (CI, CD, pipelines)
- Container technologies (Docker, Kubernetes)
- Deployment strategies (blue-green, canary)
- Infrastructure as Code
- Monitoring and observability
- Best practices

Focus on understanding the **why** behind each concept.

## Cheat Sheet

```bash
# Git
git commit -m "message"
git push origin main
git pull

# Docker
docker build -t myapp .
docker run -p 3000:3000 myapp
docker push myapp:latest

# Kubernetes
kubectl apply -f deployment.yaml
kubectl rollout status deployment/myapp
kubectl rollout undo deployment/myapp

# Helm
helm install myrelease ./mychart
helm upgrade myrelease ./mychart
helm rollback myrelease 1

```

---

## References & Learn More

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [CI/CD Pipeline Design Patterns](https://martinfowler.com/articles/continuousIntegration.html)
- [The Phoenix Project](https://www.amazon.com/Phoenix-Project-DevOps-Helping-Business/dp/0991538429)
