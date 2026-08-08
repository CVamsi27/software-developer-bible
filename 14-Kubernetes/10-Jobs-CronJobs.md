---
section: Kubernetes
category: DevOps
tags: [concept]
---

# Jobs & CronJobs

## TL;DR

Jobs run a workload to completion. CronJobs schedule Jobs on a cron expression. Both support parallelism, backoff, and history limits.

**Why it matters:** Tests completion semantics, retries with exponential backoff, concurrency policies, and the common mistake of using a Deployment for a one-shot task.

## Definition

**Jobs** manage short-lived, batch workloads that run to completion. **CronJobs** create Jobs on a time-based schedule. Both are essential for ETL pipelines, database migrations, backups, report generation, and cleanup tasks in Kubernetes.

## Why Do We Need It?

1. **Jobs**: Run-to-completion tasks, parallel processing, retry with backoff, guaranteed execution
2. **CronJobs**: Scheduled jobs (backups @daily, report generation @weekly), timezone-aware, concurrency policies

## Code Examples

### Job

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: data-migration
spec:
  completions: 1
  parallelism: 1
  backoffLimit: 3
  activeDeadlineSeconds: 300
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: migration
        image: myapp:latest
        command: ["npm", "run", "migrate"]
```

### CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-backup
spec:
  schedule: "0 2 * * *"
  timeZone: "America/New_York"
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:15
            command: ["pg_dump", "-U", "admin", "mydb"]
          restartPolicy: Never
```

## Summary

- Jobs manage batch processing tasks that run to completion, with retry and parallelism controls
- CronJobs schedule Jobs on a time-based schedule using standard cron syntax
- Jobs support parallel execution via completions and parallelism parameters for distributed processing
- Failed Jobs automatically retry based on the backoffLimit and restartPolicy configuration
- CronJob concurrency policies (Allow, Forbid, Replace) control overlapping execution behavior

---

## Cheat Sheet
```text
JOBS & CRONJOBS CHEAT SHEET
============================================================

INTERVIEW TIPS:
  - Understand the core concepts and trade-offs
  - Be ready to explain with real-world examples
  - Discuss performance implications and best practices
  - Show awareness of common pitfalls

```

---

## See Also
- [CI/CD](../15-CI-CD/)
- [Deployments](02-Deployments.md)

## References & Learn More

- [Kubernetes Jobs Docs](https://kubernetes.io/docs/concepts/workloads/controllers/job/)
- [Kubernetes CronJob Docs](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)
