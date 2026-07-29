# Role-Based Access Control (RBAC)

[![Category: Architecture](https://img.shields.io/badge/category-Architecture-800080)](.)

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

```text
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

```text
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

```text
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

---

## See Also
- [REST APIs](../07-REST-API/)
- [System Design](../11-System-Design/)

## References & Learn More

- [NIST RBAC - RBAC Explained](https://csrc.nist.gov/pubs/legacy/ir/1992/sandhu-ferraiolo-kuhn-rbac.pdf)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [RBAC vs ABAC - Comparison](https://www.pingidentity.com/en/company/blog/posts/posts/2023/role-based-access-control-vs-attribute-based-access-control.html)
- [AWS IAM - RBAC Example](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- [OAuth 2.0 Scopes](https://datatracker.ietf.org/doc/html/rfc6749#section-3.3)
