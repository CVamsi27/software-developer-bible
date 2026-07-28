[![Category: DevOps](https://img.shields.io/badge/category-DevOps-ff7f00)](.)

# Jobs & CronJobs

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

### See Also

- [Deployments](02-Deployments.md)
- [Health Checks](06-Health-Checks.md)
- [Interview Questions](08-Interview-Questions.md)
- [StatefulSets & DaemonSets](09-StatefulSets-DaemonSets.md)

## References & Learn More

- [Kubernetes Jobs Docs](https://kubernetes.io/docs/concepts/workloads/controllers/job/)
- [Kubernetes CronJob Docs](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)
