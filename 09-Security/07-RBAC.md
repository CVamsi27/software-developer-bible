# Role-Based Access Control (RBAC)

## Definition

Role-Based Access Control (RBAC) is a method of regulating access to resources based on the roles of individual users. In RBAC, permissions are assigned to roles, and users are assigned to roles. Users inherit the permissions of their assigned roles. RBAC simplifies access management by providing a structured approach to assigning and managing permissions across an organization.

RBAC is defined by NIST SP 800-162 and is widely used in enterprise applications, cloud platforms, and security-critical systems.

## Why Do We Need It?

- **Simplified Management**: Manage permissions at role level, not per user
- **Principle of Least Privilege**: Users get only permissions needed for their role
- **Separation of Duties**: Prevent conflicts by assigning different roles
- **Compliance**: Meets regulatory requirements (SOX, HIPAA, PCI DSS)
- **Auditability**: Clear trail of who has access to what
- **Scalability**: Easy to manage as organization grows

## How It Works

### RBAC Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    RBAC Components                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Users ──────> Roles ──────> Permissions                        │
│                                                                 │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐              │
│  │  Alice   │─────>│  Admin   │─────>│ create   │              │
│  │  Bob     │─────>│  Editor  │─────>│ read     │              │
│  │  Charlie │─────>│  Viewer  │─────>│ update   │              │
│  │  Diana   │─────>│          │─────>│ delete   │              │
│  └──────────┘      └──────────┘      └──────────┘              │
│                                                                 │
│  Hierarchy:                                                     │
│  Admin > Editor > Viewer                                        │
│  (Inherits all lower-level permissions)                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### RBAC Flow

```
┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
│  User    │─────>│  Check   │─────>│  Check   │─────>│  Grant/  │
│  Request │      │  Role    │      │  Perm    │      │  Deny    │
└──────────┘      └──────────┘      └──────────┘      └──────────┘
     │                │                 │                 │
     │           Get user's        Check role has      Return
     │           assigned roles    required perm       response
```

## Code Examples

### Basic RBAC Implementation (TypeScript)

```typescript
// Types
interface Permission {
  id: string;
  resource: string;
  action: "create" | "read" | "update" | "delete" | "manage";
}

interface Role {
  id: string;
  name: string;
  permissions: Permission[];
  inherits?: string[]; // Parent roles
}

interface User {
  id: string;
  email: string;
  roles: string[];
}

// RBAC Service
class RBACService {
  private roles: Map<string, Role> = new Map();
  private users: Map<string, User> = new Map();

  addRole(role: Role): void {
    this.roles.set(role.id, role);
  }

  assignRole(userId: string, roleId: string): void {
    const user = this.users.get(userId);
    if (user && !user.roles.includes(roleId)) {
      user.roles.push(roleId);
    }
  }

  removeRole(userId: string, roleId: string): void {
    const user = this.users.get(userId);
    if (user) {
      user.roles = user.roles.filter((r) => r !== roleId);
    }
  }

  getPermissions(userId: string): Permission[] {
    const user = this.users.get(userId);
    if (!user) return [];

    const permissions: Permission[] = [];

    for (const roleId of user.roles) {
      const role = this.roles.get(roleId);
      if (role) {
        permissions.push(...this.getRolePermissions(role));
      }
    }

    return this.deduplicatePermissions(permissions);
  }

  private getRolePermissions(role: Role): Permission[] {
    let permissions = [...role.permissions];

    // Include inherited permissions
    if (role.inherits) {
      for (const parentRoleId of role.inherits) {
        const parentRole = this.roles.get(parentRoleId);
        if (parentRole) {
          permissions.push(...this.getRolePermissions(parentRole));
        }
      }
    }

    return permissions;
  }

  private deduplicatePermissions(permissions: Permission[]): Permission[] {
    const seen = new Set<string>();
    return permissions.filter((p) => {
      const key = `${p.resource}:${p.action}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  hasPermission(userId: string, resource: string, action: string): boolean {
    const permissions = this.getPermissions(userId);
    return permissions.some(
      (p) =>
        p.resource === resource &&
        (p.action === action || p.action === "manage")
    );
  }

  canAccess(userId: string, resource: string, action: string): boolean {
    return this.hasPermission(userId, resource, action);
  }
}

// Usage
const rbac = new RBACService();

// Define roles
rbac.addRole({
  id: "admin",
  name: "Administrator",
  permissions: [
    { id: "1", resource: "user", action: "manage" },
    { id: "2", resource: "post", action: "manage" },
    { id: "3", resource: "comment", action: "manage" },
  ],
});

rbac.addRole({
  id: "editor",
  name: "Editor",
  permissions: [
    { id: "4", resource: "post", action: "create" },
    { id: "5", resource: "post", action: "read" },
    { id: "6", resource: "post", action: "update" },
    { id: "7", resource: "comment", action: "read" },
    { id: "8", resource: "comment", action: "delete" },
  ],
  inherits: ["viewer"],
});

rbac.addRole({
  id: "viewer",
  name: "Viewer",
  permissions: [
    { id: "9", resource: "post", action: "read" },
    { id: "10", resource: "comment", action: "read" },
  ],
});

// Assign roles and check permissions
rbac.assignRole("user-1", "admin");
rbac.hasPermission("user-1", "user", "manage"); // true
rbac.hasPermission("user-1", "post", "delete"); // true
```

### NestJS RBAC Implementation

```typescript
// role.entity.ts
import { Entity, PrimaryGeneratedColumn, ManyToMany } from "typeorm";
import { Permission } from "./permission.entity";

@Entity()
export class Role {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true })
  name: string;

  @Column()
  description: string;

  @ManyToMany(() => Permission, (permission) => permission.roles)
  permissions: Permission[];
}

// permission.entity.ts
@Entity()
export class Permission {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  resource: string;

  @Column()
  action: string;

  @ManyToMany(() => Role, (role) => role.permissions)
  roles: Role[];
}

// roles.guard.ts
import {
  Injectable,
  CanActivate,
  ExecutionContext,
  ForbiddenException,
} from "@nestjs/common";
import { Reflector } from "@nestjs/core";
import { RBACService } from "./rbac.service";

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(
    private reflector: Reflector,
    private rbacService: RBACService
  ) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.get<string[]>(
      "roles",
      context.getHandler()
    );

    if (!requiredRoles) {
      return true;
    }

    const request = context.switchToHttp().getRequest();
    const user = request.user;

    if (!user) {
      throw new ForbiddenException("User not authenticated");
    }

    const hasRole = requiredRoles.some((role) => user.roles.includes(role));

    if (!hasRole) {
      throw new ForbiddenException("Insufficient permissions");
    }

    return true;
  }
}

// permissions.guard.ts
@Injectable()
export class PermissionsGuard implements CanActivate {
  constructor(
    private reflector: Reflector,
    private rbacService: RBACService
  ) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredPermissions = this.reflector.get<string[]>(
      "permissions",
      context.getHandler()
    );

    if (!requiredPermissions) {
      return true;
    }

    const request = context.switchToHttp().getRequest();
    const user = request.user;

    for (const permission of requiredPermissions) {
      const [resource, action] = permission.split(":");

      if (!this.rbacService.hasPermission(user.id, resource, action)) {
        throw new ForbiddenException(`Missing permission: ${permission}`);
      }
    }

    return true;
  }
}

// Usage in controller
import { Controller, Get, UseGuards } from "@nestjs/common";
import { Roles } from "./roles.decorator";
import { Permissions } from "./permissions.decorator";

@Controller("users")
@UseGuards(AuthGuard, RolesGuard, PermissionsGuard)
export class UsersController {
  @Get()
  @Roles("admin")
  @Permissions("user:read")
  findAll() {
    return this.userService.findAll();
  }

  @Post()
  @Roles("admin")
  @Permissions("user:create")
  create(@Body() createUserDto: CreateUserDto) {
    return this.userService.create(createUserDto);
  }
}
```

### Database Schema (Prisma)

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  roles     UserRole[]

  @@map("users")
}

model Role {
  id          String       @id @default(cuid())
  name        String       @unique
  permissions RolePermission[]
  users       UserRole[]

  @@map("roles")
}

model Permission {
  id     String   @id @default(cuid())
  resource String
  action   String
  roles  RolePermission[]

  @@unique([resource, action])
  @@map("permissions")
}

model UserRole {
  userId   String
  roleId   String
  user     User     @relation(fields: [userId], references: [id])
  role     Role     @relation(fields: [roleId], references: [id])

  @@id([userId, roleId])
  @@map("user_roles")
}

model RolePermission {
  roleId       String
  permissionId String
  role         Role       @relation(fields: [roleId], references: [id])
  permission   Permission @relation(fields: [permissionId], references: [id])

  @@id([roleId, permissionId])
  @@map("role_permissions")
}
```

### Prisma Query for RBAC

```typescript
// Get user with roles and permissions
const getUserWithPermissions = async (userId: string) => {
  return prisma.user.findUnique({
    where: { id: userId },
    include: {
      roles: {
        include: {
          role: {
            include: {
              permissions: {
                include: {
                  permission: true,
                },
              },
            },
          },
        },
      },
    },
  });
};

// Check if user has permission
const hasPermission = async (
  userId: string,
  resource: string,
  action: string
): Promise<boolean> => {
  const user = await getUserWithPermissions(userId);

  if (!user) return false;

  return user.roles.some((ur) =>
    ur.role.permissions.some(
      (rp) =>
        rp.permission.resource === resource &&
        (rp.permission.action === action || rp.permission.action === "manage")
    )
  );
};
```

## Real-World Use Cases

### 1. Enterprise Applications
- Employee roles (admin, manager, employee)
- Department-based access (HR, Finance, Engineering)
- Hierarchical permissions

### 2. Cloud Platforms (AWS, GCP, Azure)
- IAM roles and policies
- Service account permissions
- Resource-based access control

### 3. Content Management Systems
- Editor roles (admin, editor, author, viewer)
- Content type permissions
- Workflow approvals

### 4. Multi-Tenant SaaS
- Tenant-specific roles
- Organization-level permissions
- Feature-based access control

## Common Mistakes

1. **Role explosion**: Too many granular roles become unmanageable
2. **Not implementing least privilege**: Granting more permissions than needed
3. **Hardcoding permissions**: Permissions should be configurable
4. **Not auditing role assignments**: Regular review of who has what access
5. **Ignoring role inheritance**: Properly model hierarchical permissions
6. **Not handling role changes**: Update permissions in real-time
7. **Mixing authentication and authorization**: RBAC is authorization, not authentication
8. **Not testing permission boundaries**: Verify access control in tests

## Best Practices

1. **Implement least privilege**: Grant only necessary permissions
2. **Use role hierarchy**: Model inheritance properly
3. **Audit regularly**: Review role assignments and permissions
4. **Separate duties**: Prevent conflicts with role separation
5. **Use descriptive role names**: Clear naming conventions
6. **Implement permission caching**: Reduce database queries
7. **Test access control**: Include RBAC in test suites
8. **Document roles and permissions**: Maintain clear documentation
9. **Implement time-based access**: Temporary role assignments
10. **Use attribute-based access control (ABAC)** for complex scenarios

## Performance Considerations

| Aspect | Consideration |
|--------|---------------|
| Permission Caching | Cache user permissions to reduce DB queries |
| Role Hierarchy | Pre-compute inherited permissions |
| Database Queries | Use efficient joins for role/permission lookups |
| Cache Invalidation | Invalidate cache on role/permission changes |
| Real-time Updates | Use pub/sub for permission changes |

## Interview Questions

### Beginner (5-10)

**Q1: What is RBAC?**
A: Role-Based Access Control is a method where permissions are assigned to roles, and users are assigned to roles. Users inherit permissions from their roles. It simplifies access management and enforces least privilege.

**Q2: What is the difference between RBAC and ACL?**
A: RBAC assigns permissions to roles, and users to roles. ACL (Access Control List) assigns permissions directly to users for specific resources. RBAC is more scalable for large organizations.

**Q3: What is least privilege?**
A: The principle that users should only have the minimum permissions needed to perform their job functions. This limits the impact of compromised accounts.

**Q4: What is separation of duties?**
A: A security principle where critical tasks require multiple users to complete. Prevents fraud by ensuring no single user has complete control.

**Q5: What is role hierarchy?**
A: A structure where roles inherit permissions from parent roles. For example, an "Admin" role might inherit all permissions from "Editor" and "Viewer" roles.

**Q6: What is the difference between RBAC and ABAC?**
A: RBAC assigns permissions based on roles. ABAC (Attribute-Based Access Control) assigns permissions based on attributes (user, resource, environment). ABAC is more flexible but complex.

**Q7: How do you implement RBAC in a web application?**
A: Define roles and permissions in the database. Assign roles to users. Check permissions in middleware/guards before allowing access to resources. Use decorators for role-based access.

**Q8: What is a permission?**
A: A specific action allowed on a resource (e.g., "user:create", "post:read"). Permissions define what operations users can perform.

**Q9: What is a role?**
A: A collection of permissions that define what a user can do. Roles are assigned to users, and users inherit the role's permissions.

**Q10: How do you handle role changes in real-time?**
A: Use pub/sub messaging to notify services of permission changes. Implement cache invalidation. Use event-driven architecture for real-time updates.

### Intermediate (5-10)

**Q11: How would you implement RBAC for a multi-tenant SaaS?**
A: Use tenant-specific roles. Implement organization-level permission inheritance. Use tenant context in permission checks. Implement tenant isolation in queries.

**Q12: How do you handle RBAC in a microservices architecture?**
A: Use a centralized authorization service. Implement permission caching. Use JWT claims for role information. Validate permissions at API gateway.

**Q13: How do you test RBAC implementations?**
A: Write tests for each role/permission combination. Test edge cases (no role, multiple roles). Use integration tests for permission checks. Implement permission assertion helpers.

**Q14: How do you handle RBAC for APIs?**
A: Validate JWT tokens for role information. Check permissions in middleware. Use OpenAPI specifications for documentation. Implement rate limiting per role.

**Q15: How do you audit RBAC?**
A: Log all permission checks. Maintain audit trail of role assignments. Implement regular access reviews. Use SIEM for monitoring.

**Q16: How do you handle RBAC for file uploads?**
A: Check upload permissions before processing. Use role-based storage paths. Implement file-level permissions. Audit file access.

**Q17: How do you handle RBAC for admin dashboards?**
A: Implement role-based UI components. Hide unauthorized features. Validate permissions on API calls. Use feature flags for role-based features.

**Q18: How do you handle RBAC for GraphQL?**
A: Implement resolver-level permission checks. Use directive-based authorization. Validate query permissions. Implement field-level access control.

**Q19: How do you handle RBAC for real-time features?**
A: Validate permissions on WebSocket connections. Check permissions for each message. Implement room/channel-level access control.

**Q20: How do you handle RBAC for batch operations?**
A: Validate permissions for each operation. Implement batch permission checks. Use parallel permission validation. Audit batch operations.

### Senior (10-15)

**Q21: Design an RBAC system for a global enterprise with 100,000+ users.**
A: Use hierarchical role structure. Implement permission caching with Redis. Use event-driven permission updates. Implement multi-region deployment. Use efficient database queries.

**Q22: How would you implement RBAC for a financial trading platform?**
A: Implement strict separation of duties. Use time-based permissions. Implement step-up authentication for sensitive operations. Audit all trading actions.

**Q23: Design an RBAC system that supports both internal and external users.**
A: Use different role hierarchies for internal/external. Implement guest roles with limited permissions. Use attribute-based access for complex scenarios.

**Q24: How would you handle RBAC for a healthcare application?**
A: Implement HIPAA-compliant access controls. Use patient-level permissions. Implement emergency access procedures. Audit all PHI access.

**Q25: Design an RBAC system for a cloud infrastructure platform.**
A: Use IAM-style roles and policies. Implement resource-based access control. Use service accounts for machine access. Implement cross-account access.

**Q26: How would you implement RBAC for a content management system?**
A: Implement content-type permissions. Use workflow-based access control. Implement draft/published state permissions. Use editorial roles (author, editor, publisher).

**Q27: Design an RBAC system that supports dynamic permissions.**
A: Use attribute-based access control. Implement policy-based permissions. Use rule engines for complex logic. Implement real-time permission evaluation.

**Q28: How would you handle RBAC for a multiplayer game?**
A: Implement player roles (admin, moderator, player). Use game-state permissions. Implement anti-cheat access controls. Audit player actions.

**Q29: Design an RBAC system for a DevOps platform.**
A: Implement environment-based permissions (dev, staging, prod). Use deployment permissions. Implement infrastructure access controls. Audit all changes.

**Q30: How would you implement RBAC for a financial reporting system?**
A: Implement report-level permissions. Use data masking based on roles. Implement approval workflows. Audit report access and generation.

### FAANG-style (5-10)

**Q31: Design an RBAC system for a platform with 1 billion users.**
A: Use distributed permission caching. Implement hierarchical role structure. Use event-driven permission updates. Implement multi-region deployment. Use efficient indexing.

**Q32: How would you implement RBAC for a system requiring real-time permission changes?**
A: Use pub/sub messaging for permission updates. Implement WebSocket-based notifications. Use optimistic locking for permission changes. Implement conflict resolution.

**Q33: Design an RBAC system that supports complex organizational hierarchies.**
A: Use tree-based role structures. Implement permission inheritance. Use organizational context in permission checks. Implement cross-department access.

**Q34: How would you implement RBAC for a system with strict compliance requirements?**
A: Implement comprehensive audit logging. Use time-based access controls. Implement emergency access procedures. Use cryptographic verification for permissions.

**Q35: Design an RBAC system for a system with multiple authentication methods.**
A: Use authentication-agnostic permission checks. Implement context-based permissions. Use attribute-based access control. Implement permission binding to authentication methods.

### Follow-ups (5-10)

**Q36: How would your RBAC design change for a system with temporary access needs?**
A: Implement time-based role assignments. Use just-in-time access. Implement access expiration. Audit temporary access usage.

**Q37: If RBAC was causing performance issues, how would you optimize?**
A: Implement permission caching. Use database indexing. Pre-compute inherited permissions. Use efficient query patterns. Implement lazy loading.

**Q38: How would you implement RBAC for a system with complex approval workflows?**
A: Implement approval-based permissions. Use workflow engines. Implement step-up authentication. Audit approval decisions.

**Q39: How would your approach change for a system with international users?**
A: Implement locale-based permissions. Use regional compliance requirements. Implement cross-border access controls. Audit international access.

**Q40: If you discovered unauthorized access, what would be your incident response?**
A: Immediately revoke compromised permissions. Audit access logs. Notify affected users. Implement additional monitoring. Conduct post-mortem.

## Summary

RBAC is a scalable and manageable approach to access control that assigns permissions to roles and users to roles. Key takeaways:

- Implement least privilege principle
- Use role hierarchy for inheritance
- Separate duties for critical operations
- Audit role assignments regularly
- Test access control thoroughly
- Use caching for performance
- Document roles and permissions
- Consider ABAC for complex scenarios

## Cheat Sheet

| Concept | Implementation |
|---------|---------------|
| Role | Collection of permissions |
| Permission | Action on resource (resource:action) |
| Hierarchy | Roles inherit from parent roles |
| Least Privilege | Minimum necessary permissions |
| Separation of Duties | Multiple roles for critical tasks |
| Audit | Log all permission changes |
| Caching | Redis for permission caching |
| Testing | Test each role/permission combination |

## References & Learn More

- [NIST RBAC - RBAC Explained](https://csrc.nist.gov/CSRC/media/Projects/access-control-policy-database/documents/sandhu-ferraiolo-kuhn-00.pdf)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [RBAC vs ABAC - Comparison](https://www.pingidentity.com/en/company/blog/posts/posts/2023/role-based-access-control-vs-attribute-based-access-control.html)
- [AWS IAM - RBAC Example](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- [OAuth 2.0 Scopes](https://datatracker.ietf.org/doc/html/rfc6749#section-3.3)
