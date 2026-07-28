---
section: Security
category: Architecture
tags: [concept]
---

# SQL Injection

## Definition

SQL Injection (SQLi) is a code injection technique that exploits security vulnerabilities in an application's database layer. It occurs when user input is incorrectly filtered or not properly parameterized and is placed into an SQL query. SQL injection allows attackers to execute arbitrary SQL code, potentially accessing, modifying, or deleting data. It consistently ranks in the OWASP Top 10 as one of the most critical web application security risks.

## Why Do We Need It?

- **Data Breach**: Attackers can access sensitive data (user records, passwords, financial data)
- **Data Modification**: Attackers can insert, update, or delete records
- **Authentication Bypass**: Attackers can bypass login systems
- **Server Compromise**: In some cases, attackers can execute operating system commands
- **Regulatory Violations**: SQLi breaches can violate GDPR, HIPAA, PCI DSS
- **Reputational Damage**: Data breaches destroy user trust

## How It Works

### Attack Types

```text
┌─────────────────────────────────────────────────────────────────┐
│                     SQL Injection Types                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. In-band SQLi (Classic)                                      │
│     ┌──────────┐      ┌──────────┐                              │
│     │ Attacker │─────>│ Database │                              │
│     │          │<─────│          │                              │
│     └──────────┘      └──────────┘                              │
│     Results visible in response                                  │
│                                                                 │
│  2. Blind SQLi                                                  │
│     ┌──────────┐      ┌──────────┐                              │
│     │ Attacker │─────>│ Database │                              │
│     │          │      │          │                              │
│     └──────────┘      └──────────┘                              │
│     Results not directly visible                                 │
│                                                                 │
│  3. Out-of-band SQLi                                            │
│     ┌──────────┐      ┌──────────┐      ┌──────────┐           │
│     │ Attacker │      │ Database │      │ External │           │
│     │          │<─────│          │─────>│ Server   │           │
│     └──────────┘      └──────────┘      └──────────┘           │
│     Data exfiltrated via external server                        │
│                                                                 │
│  4. Second-order SQLi                                           │
│     ┌──────────┐      ┌──────────┐      ┌──────────┐           │
│     │ Attacker │─────>│  Server  │─────>│ Database │           │
│     │          │      │ (Store)  │      │ (Later)  │           │
│     └──────────┘      └──────────┘      └──────────┘           │
│     Payload stored, executed later                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

### Attack Flow

```text
┌──────────┐                    ┌──────────┐                    ┌──────────┐
│ Attacker │                    │  Server  │                    │ Database │
└────┬─────┘                    └────┬─────┘                    └────┬─────┘
     │                               │                               │
     │  1. User: admin' --          │                               │
     │     (SQL: WHERE user='admin' │                               │
     │      --')                    │                               │
     │──────────────────────────────>│                               │
     │                               │                               │
     │                    2. SQL: SELECT * FROM users               │
     │                       WHERE user='admin' --'                │
     │                       (-- comments out password check)       │
     │                               │                               │
     │                               │──────────────────────────────>│
     │                               │                               │
     │                               │  3. Returns all admin data    │
     │                               │<──────────────────────────────│
     │                               │                               │
     │  4. Authentication bypassed   │                               │
     │<──────────────────────────────│                               │

```

## Code Examples

### Vulnerable Code

```typescript
// ❌ VULNERABLE: Direct string concatenation
app.post("/login", async (req, res) => {
  const { username, password } = req.body;
  const query = `SELECT * FROM users WHERE username='${username}' AND password='${password}'`;
  const result = await db.query(query);
  // Attacker can input: username = admin' --
});

// ❌ VULNERABLE: Template literal
app.get("/users", async (req, res) => {
  const { id } = req.query;
  const query = `SELECT * FROM users WHERE id = ${id}`;
  const result = await db.query(query);
});

// ❌ VULNERABLE: LIKE clause
app.get("/search", async (req, res) => {
  const { term } = req.query;
  const query = `SELECT * FROM products WHERE name LIKE '%${term}%'`;
  const result = await db.query(query);
});

```

### Secure Code Examples

```typescript
// ✅ SECURE: Parameterized queries
app.post("/login", async (req, res) => {
  const { username, password } = req.body;
  const query = "SELECT * FROM users WHERE username = $1 AND password = $2";
  const result = await db.query(query, [username, password]);
});

// ✅ SECURE: Using Prisma ORM (automatic parameterization)
app.post("/login", async (req, res) => {
  const { username, password } = req.body;
  const user = await prisma.user.findFirst({
    where: {
      username,
      password, // Prisma parameterizes this automatically
    },
  });
});

// ✅ SECURE: Parameterized LIKE queries
app.get("/search", async (req, res) => {
  const { term } = req.query;
  const query = "SELECT * FROM products WHERE name LIKE $1";
  const result = await db.query(query, [`%${term}%`]);
});

// ✅ SECURE: Prisma with dynamic conditions
app.get("/users", async (req, res) => {
  const { role, department } = req.query;

  const where: any = {};
  if (role) where.role = role;
  if (department) where.department = department;

  const users = await prisma.user.findMany({ where });
  res.json(users);
});

// ✅ SECURE: Input validation
import { z } from "zod";

const loginSchema = z.object({
  username: z.string().min(3).max(50).regex(/^[a-zA-Z0-9_]+$/),
  password: z.string().min(8).max(100),
});

app.post("/login", async (req, res) => {
  const result = loginSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json({ error: "Invalid input" });
  }

  const { username, password } = result.data;
  const query = "SELECT * FROM users WHERE username = $1 AND password = $2";
  const user = await db.query(query, [username, password]);
});

```

### ORM Usage (Prisma)

```typescript
// Prisma automatically parameterizes all queries
const createUser = async (data: CreateUserInput) => {
  return prisma.user.create({ data });
};

const findUsers = async (filters: UserFilters) => {
  const where: Prisma.UserWhereInput = {};

  if (filters.role) {
    where.role = filters.role;
  }

  if (filters.search) {
    where.OR = [
      { name: { contains: filters.search, mode: "insensitive" } },
      { email: { contains: filters.search, mode: "insensitive" } },
    ];
  }

  return prisma.user.findMany({ where });
};

// Raw queries with parameters
const rawQuery = async (userId: string) => {
  return prisma.$queryRaw`
    SELECT * FROM users WHERE id = ${userId}
  `;
};

// Dynamic queries with Prisma
const dynamicQuery = async (filters: Record<string, any>) => {
  const where: Prisma.UserWhereInput = {};

  // Build where clause safely
  Object.entries(filters).forEach(([key, value]) => {
    if (typeof value === "string") {
      where[key as keyof Prisma.UserWhereInput] = {
        contains: value,
        mode: "insensitive",
      };
    } else {
      where[key as keyof Prisma.UserWhereInput] = value;
    }
  });

  return prisma.user.findMany({ where });
};

```

### Stored Procedure Security

```sql
-- ✅ SECURE: Parameterized stored procedure
CREATE PROCEDURE GetUserById(@UserId INT)
AS
BEGIN
    SELECT * FROM Users WHERE Id = @UserId;
END;

-- ✅ SECURE: Dynamic SQL with QUOTENAME
CREATE PROCEDURE SearchUsers(@ColumnName NVARCHAR(128), @SearchTerm NVARCHAR(128))
AS
BEGIN
    DECLARE @Sql NVARCHAR(MAX);
    SET @Sql = N'SELECT * FROM Users WHERE ' +
               QUOTENAME(@ColumnName) + N' LIKE @SearchTerm';
    EXEC sp_executesql @Sql, N'@SearchTerm NVARCHAR(128)', @SearchTerm = @SearchTerm;
END;

```

## Real-World Use Cases

### 1. Login Authentication

- Attackers bypass authentication with `' OR '1'='1`
- Always use parameterized queries for authentication
- Implement account lockout after failed attempts

### 2. Search Functionality

- User search inputs can contain SQLi payloads
- Use parameterized queries with LIKE clauses
- Validate and sanitize search terms

### 3. Data Export

- SQLi in data export can dump entire database
- Use parameterized queries for all queries
- Implement access control on export functionality

### 4. Admin Interfaces

- Admin panels often have more database access
- SQLi in admin interfaces is especially dangerous
- Implement least privilege for database accounts

## Common Mistakes

1. **Using string concatenation**: Never concatenate user input into SQL

2. **Not using parameterized queries**: Always use prepared statements

3. **Trusting user input**: Validate and sanitize all input

4. **Using ORM raw queries unsafely**: Even with ORMs, raw queries need parameterization

5. **Not validating data types**: Validate input types before using in queries

6. **Using dynamic SQL without sanitization**: Use QUOTENAME or equivalent

7. **Granting excessive database privileges**: Use least privilege principle

8. **Not monitoring database queries**: Log and monitor for suspicious queries

## Best Practices

1. **Use parameterized queries** for all database operations

2. **Use ORM** (Prisma, TypeORM, Sequelize) for automatic parameterization

3. **Validate input types** and formats before using in queries

4. **Implement least privilege** for database accounts

5. **Use stored procedures** with parameters

6. **Implement input validation** with allowlists

7. **Use Web Application Firewalls** (WAF) for additional protection

8. **Regular security audits** and penetration testing

9. **Monitor database queries** for suspicious patterns
10. **Keep database software** up to date

## Performance Considerations

| Aspect | Consideration |
|--------|---------------|
| Parameterized Queries | Minimal overhead vs concatenation |
| ORM vs Raw | ORMs add abstraction overhead |
| Connection Pooling | Use pooling for parameterized queries |
| Query Caching | Parameterized queries enable query plan caching |
| Index Usage | Proper parameterization preserves index usage |

## Summary

SQL Injection is a critical vulnerability that can lead to complete data compromise. Key takeaways:

- Always use parameterized queries
- Use ORMs (Prisma) for automatic parameterization
- Validate and sanitize all user input
- Implement least privilege for database accounts
- Monitor database queries for suspicious patterns
- Conduct regular security audits and penetration testing
- Keep database software up to date

## Cheat Sheet
| Defense | Implementation |
|---------|---------------|
| Parameterized Queries | Separate SQL code from data |
| ORM (Prisma) | Automatic parameterization |
| Input Validation | Allowlists for expected formats |
| Least Privilege | Minimal database permissions |
| Stored Procedures | Use parameters, not dynamic SQL |
| WAF | Filter malicious payloads |
| Monitoring | Log and alert on suspicious queries |
| Escaping | Database-specific escaping functions |

---

## See Also
- [REST APIs](../07-REST-API/)
- [System Design](../11-System-Design/)

## References & Learn More

- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [PortSwigger SQL Injection Tutorials](https://portswigger.net/web-security/sql-injection)
- [Prisma SQL Injection Prevention](https://www.prisma.io/docs/guides/security/sanitization)
- [Bobby Tables - SQL Injection Examples](https://bobby-tables.com/)
- [SQL Injection Knowledge Base](https://sql injection knowledge base)
