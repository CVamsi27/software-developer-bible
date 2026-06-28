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

## Interview Questions

### Beginner (5-10)

**Q1: What is SQL injection?**
A: SQL injection is a vulnerability where user input is inserted directly into SQL queries, allowing attackers to execute arbitrary SQL code. It can lead to data theft, authentication bypass, and data modification.

**Q2: How do you prevent SQL injection?**
A: Use parameterized queries (prepared statements), use ORMs (Prisma, TypeORM), validate input types, implement least privilege for database accounts, and use stored procedures with parameters.

**Q3: What is a parameterized query?**
A: A parameterized query separates SQL code from user data. The SQL template is defined first, then parameters are bound separately. The database treats parameters as data, not executable code.

**Q4: What is the difference between SQL injection and ORM?**
A: SQL injection exploits direct SQL string construction. ORMs abstract SQL queries and automatically parameterize them, preventing most SQLi. However, ORMs can still be vulnerable if raw queries are used unsafely.

**Q5: Can SQL injection affect all database systems?**
A: Yes, SQL injection affects all SQL databases (MySQL, PostgreSQL, SQL Server, Oracle, SQLite). The syntax may vary, but the vulnerability exists in any system where user input is concatenated into queries.

**Q6: What is blind SQL injection?**
A: Blind SQL injection occurs when the application doesn't return SQL errors or results directly. Attackers infer information through boolean conditions (true/false) or time delays (sleep functions).

**Q7: What is a UNION-based SQL injection?**
A: UNION-based SQL injection uses the UNION SQL operator to combine results from the original query with results from injected queries, allowing attackers to extract data from other tables.

**Q8: What is second-order SQL injection?**
A: Second-order SQL injection occurs when malicious input is stored in the database and later used in a vulnerable query. The initial input doesn't trigger the vulnerability; the stored data does when retrieved.

**Q9: How does Prisma prevent SQL injection?**
A: Prisma automatically parameterizes all queries, whether using the query builder or raw queries. It treats user input as data, not executable SQL code, preventing injection attacks.

**Q10: What is input validation and how does it help?**
A: Input validation checks user input against expected formats (type, length, range, format). While not a primary defense against SQLi, it reduces the attack surface by rejecting invalid input.

### Intermediate (5-10)

**Q11: How would you implement SQL injection protection in a legacy application?**
A: Implement parameterized queries gradually. Use ORM wrappers. Deploy WAF rules. Implement input validation. Add query monitoring. Plan for code refactoring to use parameterized queries.

**Q12: How do you test for SQL injection vulnerabilities?**
A: Use automated scanners (SQLMap, OWASP ZAP), manual testing with payloads, code review, and static analysis. Test all input fields, URL parameters, and HTTP headers.

**Q13: What is the impact of SQL injection on stored procedures?**
A: Stored procedures can be vulnerable if they use dynamic SQL without parameterization. Use QUOTENAME in SQL Server, proper escaping, or pass parameters to stored procedures.

**Q14: How do you handle SQL injection in NoSQL databases?**
A: NoSQL databases (MongoDB, CouchDB) are also vulnerable. Use parameterized queries, validate input types, avoid $where operators with user input, and use ORM methods.

**Q15: What is a WAF and how does it help with SQLi?**
A: Web Application Firewall (WAF) filters and monitors HTTP traffic. It can detect and block common SQLi payloads. However, WAF is not a substitute for proper input validation and parameterized queries.

**Q16: How do you prevent SQL injection in dynamic SQL?**
A: Use parameterized dynamic SQL (sp_executesql in SQL Server), QUOTENAME for identifiers, proper escaping, and validate all dynamic inputs. Avoid constructing dynamic SQL when possible.

**Q17: What is the principle of least privilege in database security?**
A: Grant database users only the minimum permissions needed for their function. Application database accounts should have limited permissions (e.g., no DROP TABLE, no admin operations).

**Q18: How do you handle SQL injection in file upload functionality?**
A: Validate file types and content. Use parameterized queries for metadata storage. Never use file content in SQL queries. Implement virus scanning. Store files separately from the database.

**Q19: What is SQL injection through HTTP headers?**
A: Attackers can inject SQL payloads in HTTP headers (User-Agent, Referer, etc.) if the application logs or queries these values. Always parameterize header values used in database operations.

**Q20: How do you monitor for SQL injection attacks?**
A: Log all database queries, implement anomaly detection, monitor for unusual query patterns, use database activity monitoring tools, and set up alerts for suspicious activities.

### Senior (10-15)

**Q21: Design a comprehensive SQL injection defense strategy for a large application.**
A: Layer 1: Parameterized queries everywhere. Layer 2: Input validation with allowlists. Layer 3: ORM with strict schemas. Layer 4: WAF rules. Layer 5: Database activity monitoring. Layer 6: Regular security audits.

**Q22: How would you migrate a large codebase from string concatenation to parameterized queries?**
A: Audit codebase for vulnerable patterns. Use static analysis tools. Refactor incrementally. Implement automated testing. Deploy gradually with feature flags. Monitor for regressions.

**Q23: Explain how SQL injection can lead to remote code execution.**
A: In some databases (SQL Server with xp_cmdshell, MySQL with UDF), attackers can execute OS commands through SQL injection. This requires specific database configurations and is highly dangerous.

**Q24: How would you implement SQL injection protection for a multi-tenant SaaS application?**
A: Use tenant-specific database connections or schemas. Validate tenant context in all queries. Implement row-level security. Use parameterized queries with tenant ID. Audit cross-tenant access attempts.

**Q25: Design a system for automatic SQL injection detection and prevention.**
A: Implement static analysis in CI/CD. Deploy runtime protection (WAF, RASP). Use database activity monitoring. Build automated response system. Implement continuous security testing.

**Q26: How would you handle SQL injection in a microservices architecture?**
A: Implement parameterized queries at service level. Use API gateway for input validation. Deploy WAF at perimeter. Implement service mesh for inter-service security. Monitor database queries across services.

**Q27: Explain the impact of SQL injection on database replication.**
A: SQL injection can corrupt replicated data, spread malicious data across replicas, and compromise the entire replication chain. Implement security measures on all nodes and monitor replication traffic.

**Q28: How would you implement SQL injection protection for a GraphQL API?**
A: Use query whitelisting. Validate all input arguments. Use parameterized resolvers. Implement query depth limiting. Monitor for suspicious query patterns.

**Q29: Design a SQL injection testing strategy for a critical application.**
A: Combine automated scanning, manual penetration testing, code review, and red team exercises. Test in staging environment. Implement bug bounty program. Conduct regular security assessments.

**Q30: How would you handle SQL injection in a containerized environment?**
A: Implement database connection pooling. Use secrets management for credentials. Deploy WAF in service mesh. Monitor container-to-database traffic. Implement network segmentation.

### FAANG-style (5-10)

**Q31: Design a SQL injection prevention system for a database handling 10 million queries per minute.**
A: Implement connection pooling with parameterized queries. Use query plan caching. Deploy distributed WAF. Implement real-time anomaly detection. Use machine learning for pattern recognition.

**Q32: How would you implement SQL injection protection for a system with dynamic schema changes?**
A: Use schema validation at query time. Implement parameterized queries for dynamic schemas. Use ORM with schema introspection. Deploy runtime protection. Monitor schema changes.

**Q33: Design a system that detects and prevents zero-day SQL injection attacks.**
A: Implement behavioral analysis. Use machine learning for anomaly detection. Deploy runtime application self-protection (RASP). Build automated response system. Implement honeypots.

**Q34: How would you handle SQL injection in a globally distributed database system?**
A: Implement region-specific security policies. Use centralized WAF with regional deployment. Monitor cross-region queries. Implement data residency controls. Use encryption in transit and at rest.

**Q35: Design a SQL injection prevention system that adapts to new attack patterns.**
A: Use machine learning for pattern recognition. Implement threat intelligence feeds. Deploy adaptive WAF rules. Build automated rule generation. Implement continuous learning from attacks.

### Follow-ups (5-10)

**Q36: How would your SQL injection defense change for a system with 99.999% uptime requirements?**
A: Implement zero-downtime security updates. Use blue-green deployments for WAF rules. Deploy canary releases for security patches. Implement automated rollback. Monitor for false positives.

**Q37: If parameterized queries were not available, how would you prevent SQL injection?**
A: Use stored procedures with parameters. Implement input validation with strict allowlists. Use escaping functions specific to the database. Deploy WAF. Implement database activity monitoring.

**Q38: How would you handle SQL injection in a system with complex reporting queries?**
A: Use parameterized views. Implement query builders. Use reporting tools with built-in SQL injection protection. Validate all report parameters. Implement query signing.

**Q39: How would your approach change for a healthcare application with HIPAA requirements?**
A: Implement encryption for all PHI. Use audit logging for all database access. Implement access controls. Conduct regular security assessments. Maintain compliance documentation.

**Q40: If you discovered SQL injection in production, what would be your incident response?**
A: Immediately deploy WAF rules to block attack patterns. Rotate database credentials. Audit all database changes. Notify affected users. Conduct post-mortem. Implement additional monitoring.

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

## References & Learn More

- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [PortSwigger SQL Injection Tutorials](https://portswigger.net/web-security/sql-injection)
- [Prisma SQL Injection Prevention](https://www.prisma.io/docs/guides/security/sanitization)
- [Bobby Tables - SQL Injection Examples](https://bobby-tables.com/)
- [SQL Injection Knowledge Base](https://sql injection knowledge base)
