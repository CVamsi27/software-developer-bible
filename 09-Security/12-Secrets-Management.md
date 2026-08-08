---
section: Security
category: Architecture
tags: [concept]
---

# Secrets Management

> **TL;DR:** Secrets (DB passwords, API keys, signing keys) must never be in code, in `.env` files committed to git, or in plain environment variables at rest. The senior pattern is a dedicated secrets manager (HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager) with short-lived dynamic credentials, audit logs, and rotation. The senior test is the full lifecycle: where the secret is born, where it travels, where it dies.
>
> **Why it matters:** This is an Architecture interview topic you will be asked about at the senior level (5+ YoE) — not for definition recall, but for tradeoffs, production failure modes, and the ability to compare it against alternatives.

## Definition

**Secrets management** is the discipline of storing, distributing, rotating, and auditing sensitive credentials (database passwords, API keys, signing keys, OAuth client secrets) outside of source code and unencrypted disks. The senior stack is: a **secrets manager** (Vault, AWS Secrets Manager, GCP Secret Manager) as the source of truth, **short-lived dynamic credentials** (database roles, IAM-bound) preferred over long-lived static keys, and **audit logs** for every read. The leaky-secret incident in 2024 (Snowflake, etc.) is a reminder: every static long-lived credential is a future breach.

## Why Do We Need It?

1. **Single source of truth** — One place to rotate, audit, and revoke; not 50 `.env` files.
2. **Rotation** — Static passwords that never rotate outlive their usefulness; rotation limits blast radius.
3. **Auditability** — Every secret read is logged; you know exactly what credential touched what system.
4. **Dynamic credentials** — Vault can mint a Postgres role that's valid for 1 hour; the long-lived `postgres` password is no longer a thing.
5. **Least privilege** — Each service gets only the secrets it needs, scoped to the env (`dev`, `staging`, `prod`).
6. **No secrets in git** — A pre-commit hook + a secrets scanner (gitleaks, trufflehog) catches leaks before they hit origin.
7. **Compliance** — SOC 2, PCI-DSS, HIPAA all require centralized secrets management.

## How It Works

### Secret Lifecycle

```text
Created (operator / automated)
   │
   ▼
Stored encrypted in Secrets Manager (KMS-wrapped)
   │
   ▼
Distributed to workloads
   ├── Env var (still encrypted at rest on the host)
   ├── Volume mount (file)
   └── SDK call (fetch at boot or refresh on TTL)
   │
   ▼
Used (logged: who, when, what system)
   │
   ▼
Rotated (operator / automated, every N days)
   │
   ▼
Revoked (incident response, employee offboard)
```

### Pattern: App Fetches Secret at Boot, Caches in Memory

```text
App start
   │
   ├── Authenticate to Vault (Kubernetes service account / IAM role)
   ├── Read secret: db/password
   ├── Decrypt in memory
   ├── Connect to DB
   │
   ▼
At TTL (e.g. 1h)
   │
   ├── Re-read secret
   └── Connection pool re-establishes
```

### Pattern: Dynamic Database Credentials (Vault)

```text
Service requests Postgres role from Vault
   │
   ▼
Vault creates a temporary role: vault-root-XXXX
   │  - username: v-root-XXXX
   │  - password: random 32 chars
   │  - TTL: 1 hour
   │  - GRANT: only the tables the service needs
   │
   ▼
Service uses the role to connect
   │
   ▼
After TTL, role is dropped (recreated next time)
```

## Code Examples

### AWS Secrets Manager (Node SDK)

```typescript
// config/secrets.ts
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';

const sm = new SecretsManagerClient({ region: 'us-east-1' });

export async function loadSecret<T = Record<string, string>>(name: string): Promise<T> {
  const out = await sm.send(new GetSecretValueCommand({ SecretId: name }));
  if (!out.SecretString) throw new Error(`Secret ${name} is empty`);
  return JSON.parse(out.SecretString) as T;
}

// usage
const { DB_HOST, DB_USER, DB_PASSWORD } = await loadSecret<{
  DB_HOST: string; DB_USER: string; DB_PASSWORD: string;
}>('prod/orders/db');
```

### Caching with TTL

```typescript
class CachedSecret<T> {
  private value: T | undefined;
  private fetchedAt = 0;
  constructor(private readonly name: string, private readonly ttlMs = 60 * 60_000) {}

  async get(): Promise<T> {
    if (this.value && Date.now() - this.fetchedAt < this.ttlMs) return this.value;
    this.value = await loadSecret<T>(this.name);
    this.fetchedAt = Date.now();
    return this.value;
  }

  invalidate() { this.value = undefined; this.fetchedAt = 0; }
}

const dbSecret = new CachedSecret<{ DB_PASSWORD: string }>('prod/orders/db', 3600_000);
```

### HashiCorp Vault (Node SDK)

```typescript
// config/vault.ts
import * as vault from 'node-vault';

const client = vault({
  apiVersion: 'v1',
  endpoint: process.env.VAULT_ADDR,
  token: process.env.VAULT_TOKEN,   // injected by Vault Agent / k8s service account
});

export async function getDbCreds(): Promise<{ username: string; password: string }> {
  const res = await client.read('database/creds/orders-app');
  return res.data;   // { username: 'v-orders-app-XXX', password: '...' }
}
```

### Dynamic Postgres Credentials (Vault)

```bash
# Vault config
vault write database/config/orders \
  plugin_name=postgresql-database-plugin \
  allowed_roles="orders-app" \
  connection_url="postgresql://{{username}}:{{password}}@db.internal:5432/orders" \
  username="vault" password="vault-root-password"

vault write database/roles/orders-app \
  db_name=orders \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" max_ttl="24h"
```

```typescript
// Each service instance fetches a fresh role on startup
const { username, password } = await getDbCreds();
const client = new pg.Client({ host: 'db.internal', user: username, password, database: 'orders' });
await client.connect();
```

### Kubernetes Secrets (with Sealed Secrets / External Secrets Operator)

```yaml
# k8s/external-secret.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: orders-db
spec:
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: orders-db-secret
  data:
    - secretKey: DB_PASSWORD
      remoteRef:
        key: secret/data/orders/db
        property: password
```

```bash
# Apply the manifest; ESO fetches from Vault and materializes a K8s Secret
kubectl apply -f external-secret.yaml
```

### Pre-Commit Secret Scanner

```bash
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

```bash
# Or in CI, scan the whole repo
gitleaks detect --source . --report-path gitleaks.json
```

### Signing Keys with KMS (Don't Store Private Keys in Secrets)

```typescript
// ❌ Wrong: a 2048-bit RSA private key in Secrets Manager
const { privateKey } = await loadSecret('jwt/signing-key');
jwt.sign(payload, privateKey, { algorithm: 'RS256' });

// ✅ Right: keep the key in KMS, sign via the KMS API
import { KMSClient, SignCommand } from '@aws-sdk/client-kms';
const kms = new KMSClient({});
const out = await kms.send(new SignCommand({
  KeyId: 'arn:aws:kms:...:key/abc',
  Message: Buffer.from(payload),
  SigningAlgorithm: 'RSASSA_PKCS1_V1_5_SHA_256',
}));
jwt.sign(payload, out.Signature, { algorithm: 'RS256' });
```

## Real-World Use Cases

1. **Database credentials** — Static password in Vault with 30-day rotation, or dynamic Postgres roles with 1-hour TTL.
2. **Third-party API keys** — Stripe, Twilio, OpenAI in Secrets Manager; the service reads at boot, never from `.env`.
3. **JWT signing keys** — In KMS, never in code or a `.env` file; sign via the KMS API.
4. **TLS private keys** — In a secret manager; rotated annually or on incident; never committed.
5. **OAuth client secrets** — Encrypted at rest; scoped per env (`dev` / `staging` / `prod`); rotated on personnel change.
6. **CI/CD pipeline** — GitHub Actions secrets, GitLab CI variables, or Vault; injected at runtime; never echoed in logs.
7. **Incident response** — When an employee leaves, revoke all secrets they had access to in one place.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Secrets in `.env` files committed to git | `.env.example` for shape; real secrets from a secret manager |
| Long-lived static DB passwords that never rotate | Dynamic credentials (Vault) or scheduled rotation (Secrets Manager) |
| Secrets in container image layers | Multi-stage build; pass secrets at runtime via env or volume mount |
| Logging the secret value | Redact in logs; structured loggers must support a redact list |
| Echoing the secret in CI output | `set +x` or explicitly mask; review the CI YAML for accidental `echo` |
| Putting private keys in Secrets Manager | Private keys belong in KMS / HSM, not in a string field |
| All services share one root DB password | One service = one role = one credential, scoped to its tables |
| No pre-commit secret scan | Add gitleaks / trufflehog to `.pre-commit-config.yaml` and to CI |
| Secrets in error messages or stack traces | Catch-all error filter must redact known secret keys |
| No rotation policy | Every secret has a TTL and an owner; rotation is automated, not manual |

## Best Practices

1. **One secret manager** — Vault, AWS Secrets Manager, or GCP Secret Manager; not both, not "depends on the team".
2. **Dynamic credentials over static** — Postgres role per service, TTL 1h, dropped on expiry; the root password is never used by an app.
3. **Rotate on a schedule** — Static secrets rotate every 30–90 days; on incident, rotate immediately.
4. **Audit every read** — Every secret fetch is logged with `who, when, from where, to which workload`.
5. **Least privilege** — A service can only read the secret it needs; not the whole tree.
6. **Never log the secret value** — Structured loggers with a redact list; code review enforces it.
7. **Scan for leaks in CI** — gitleaks / trufflehog on every PR; block merges on findings.
8. **Private keys in KMS / HSM** — Don't store raw private keys in secrets; use the KMS API to sign.
9. **Rotate on personnel change** — When someone with secret access leaves, rotate everything they could read.
10. **Test the rotation** — A rotation policy you have never tested is a rotation policy you don't have.

## Performance Considerations

- Fetching a secret at boot costs ~50–200ms over a regional network; cache in memory for the boot lifetime.
- KMS signing is slower than local signing (~5–20ms per call); batch signing where possible.
- Vault Agent / sidecar pattern offloads secret fetching from the app; the app reads from a local file.
- External Secrets Operator materializes K8s Secrets; the pod reads from the K8s Secret like any other env var — no Vault SDK in the app.

## Summary

- Secrets management is the discipline of storing, distributing, rotating, and auditing credentials outside of code and unencrypted disks.
- Use a dedicated secrets manager (Vault, AWS Secrets Manager, GCP Secret Manager); never commit secrets to git.
- Dynamic credentials (Vault DB roles) are the gold standard; rotate static secrets on a schedule.
- Scan for leaks in pre-commit and CI; never log secret values; private keys belong in KMS / HSM, not in a string field.

## Cheat Sheet

| Concept | Description |
|---------|-------------|
| Secrets manager | Centralized store: Vault, AWS Secrets Manager, GCP Secret Manager |
| Dynamic credentials | Short-lived DB roles minted on demand (Vault DB engine) |
| Static credentials | Long-lived API key/DB password; rotate on a schedule |
| Rotation | Scheduled (30/90 days) + on-incident |
| Audit log | Every secret fetch is logged: who, when, from where |
| Least privilege | Each service reads only the secret it needs |
| Pre-commit scanner | gitleaks / trufflehog in `.pre-commit-config.yaml` and CI |
| `redact` list | Log scrubber that strips known secret keys from log output |
| KMS / HSM | Where private keys live; sign via the KMS API, not by loading the key |
| Vault Agent | Sidecar / daemon that fetches and renews secrets; app reads a local file |
| External Secrets Operator | K8s controller that materializes secrets from Vault into K8s Secrets |
| `.env.example` | Shape only — committed, no real values |
| `.env.local` | Per-developer — gitignored, not committed |
| Incident rotation | Offboard an employee? Rotate everything they could read. |

---

## See Also
- [Microservices](../12-Microservices/) (per-service credentials)
- [REST APIs](../07-REST-API/) (API key storage)
- [System Design](../11-System-Design/) (secrets in system design)
- [Web Security](./09-Web-Security.md) (HTTPS, TLS in production)

## References & Learn More

- [HashiCorp Vault](https://www.vaultproject.io/)
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
- [GCP Secret Manager](https://cloud.google.com/secret-manager/docs)
- [External Secrets Operator](https://external-secrets.io/)
- [gitleaks](https://github.com/gitleaks/gitleaks)
- [trufflehog](https://github.com/trufflehog/trufflehog)
- [Vault Dynamic Secrets for Postgres](https://developer.hashicorp.com/vault/docs/secrets/databases/postgresql)
- [OWASP — Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
