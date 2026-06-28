# Zod

## Definition
Zod is a TypeScript-first schema declaration and validation library. It provides a concise, expressive syntax for defining data schemas and validating data at runtime, with automatic TypeScript type inference.

## Why Do We Need It?
- **Type Safety**: TypeScript-first with automatic type inference
- **Runtime Validation**: Validate data at runtime with clear error messages
- **Expressive API**: Concise, readable schema definitions
- **Integration**: Works with React Hook Form, tRPC, and more
- **Performance**: Fast validation with minimal overhead

## How It Works

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ZOD ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Schema Definition                         │   │
│  │  • Define shape of data                                     │   │
│  │  • Specify validation rules                                 │   │
│  │  • Set default values                                       │   │
│  │  • Create transformations                                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Validation Engine                         │   │
│  │  • Parse input data                                         │   │
│  │  • Apply validation rules                                   │   │
│  │  • Generate detailed errors                                 │   │
│  │  • Return typed result                                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│         ┌────────────────────┼────────────────────┐                │
│         ▼                    ▼                    ▼                │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐            │
│  │  Safe Parse │    │   Parse     │    │  Type       │            │
│  │  (Result)   │    │  (Throw)    │    │  Inference  │            │
│  └─────────────┘    └─────────────┘    └─────────────┘            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Code Examples

### 1. Basic Schemas

```typescript
import { z } from 'zod';

// Primitive types
const stringSchema = z.string();
const numberSchema = z.number();
const booleanSchema = z.boolean();
const dateSchema = z.date();

// String validations
const emailSchema = z.string().email();
const urlSchema = z.string().url();
const uuidSchema = z.string().uuid();
const minLengthSchema = z.string().min(3);
const maxLengthSchema = z.string().max(100);
const patternSchema = z.string().regex(/^[A-Z]+$/);

// Number validations
const positiveSchema = z.number().positive();
const rangeSchema = z.number().min(0).max(100);
const intSchema = z.number().int();

// Object schema
const userSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
  createdAt: z.date().default(() => new Date()),
});

// Type inference
type User = z.infer<typeof userSchema>;
// Result: { id: string; name: string; email: string; age?: number; createdAt: Date }
```

### 2. Complex Schemas

```typescript
import { z } from 'zod';

// Nested objects
const addressSchema = z.object({
  street: z.string(),
  city: z.string(),
  state: z.string().length(2),
  zipCode: z.string().regex(/^\d{5}(-\d{4})?$/),
  country: z.string().default('US'),
});

const userWithAddressSchema = z.object({
  name: z.string(),
  email: z.string().email(),
  address: addressSchema,
});

// Arrays
const tagsSchema = z.array(z.string());
const numbersSchema = z.array(z.number()).min(1).max(10);

// Objects with arrays
const postSchema = z.object({
  id: z.string().uuid(),
  title: z.string().min(1).max(200),
  content: z.string(),
  tags: z.array(z.string()),
  author: z.object({
    id: z.string(),
    name: z.string(),
  }),
  publishedAt: z.date().nullable(),
});

// Record (object with dynamic keys)
const metadataSchema = z.record(z.string(), z.string());

// Tuple
const coordinateSchema = z.tuple([z.number(), z.number()]);

// Union
const statusSchema = z.union([
  z.literal('active'),
  z.literal('inactive'),
  z.literal('pending'),
]);

// Enum
const roleSchema = z.enum(['admin', 'user', 'guest']);

// Discriminated union
const eventSchema = z.discriminatedUnion('type', [
  z.object({
    type: z.literal('click'),
    x: z.number(),
    y: z.number(),
  }),
  z.object({
    type: z.literal('keypress'),
    key: z.string(),
    code: z.number(),
  }),
]);
```

### 3. Transformations

```typescript
import { z } from 'zod';

// Transform data
const userInputSchema = z.object({
  email: z.string().transform((val) => val.toLowerCase().trim()),
  age: z.string().transform((val) => parseInt(val, 10)),
  birthday: z.string().transform((val) => new Date(val)),
});

// Preprocess (for raw input)
const numberInputSchema = z.preprocess(
  (val) => (typeof val === 'string' ? parseInt(val, 10) : val),
  z.number()
);

// Refine (add custom validation)
const passwordSchema = z
  .string()
  .min(8)
  .refine(
    (val) => /[A-Z]/.test(val),
    'Password must contain at least one uppercase letter'
  )
  .refine(
    (val) => /[0-9]/.test(val),
    'Password must contain at least one number'
  );

// SuperRefine (complex validation)
const registrationSchema = z
  .object({
    email: z.string().email(),
    password: z.string().min(8),
    confirmPassword: z.string(),
  })
  .superRefine((data, ctx) => {
    if (data.password !== data.confirmPassword) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: 'Passwords do not match',
        path: ['confirmPassword'],
      });
    }
  });
```

### 4. React Hook Form Integration

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

type LoginFormData = z.infer<typeof loginSchema>;

function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    mode: 'onChange',
  });

  const onSubmit = async (data: LoginFormData) => {
    // Data is typed as LoginFormData
    console.log(data.email, data.password);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          {...register('email')}
        />
        {errors.email && <span>{errors.email.message}</span>}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          {...register('password')}
        />
        {errors.password && <span>{errors.password.message}</span>}
      </div>

      <button type="submit">Login</button>
    </form>
  );
}
```

### 5. Error Handling

```typescript
import { z } from 'zod';

const userSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email'),
  age: z.number().min(18, 'Must be at least 18'),
});

// Safe parse (returns result object)
const result = userSchema.safeParse({
  name: '',
  email: 'invalid',
  age: 15,
});

if (result.success) {
  console.log('Valid:', result.data);
} else {
  console.log('Errors:', result.error.errors);
  // Output:
  // [
  //   { code: 'too_small', path: ['name'], message: 'Name is required' },
  //   { code: 'invalid_string', path: ['email'], message: 'Invalid email' },
  //   { code: 'too_small', path: ['age'], message: 'Must be at least 18' }
  // ]
}

// Parse (throws on error)
try {
  const user = userSchema.parse(invalidData);
} catch (error) {
  if (error instanceof z.ZodError) {
    console.log(error.errors);
  }
}

// Format errors for display
function formatErrors(error: z.ZodError): Record<string, string> {
  const formatted: Record<string, string> = {};
  
  for (const issue of error.errors) {
    const path = issue.path.join('.');
    formatted[path] = issue.message;
  }
  
  return formatted;
}
```

### 6. API Validation

```typescript
import { z } from 'zod';

// API request schemas
const CreateUserRequestSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  role: z.enum(['admin', 'user']),
});

const UpdateUserRequestSchema = CreateUserRequestSchema.partial();

// API response schemas
const UserResponseSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  email: z.string().email(),
  role: z.enum(['admin', 'user']),
  createdAt: z.string().datetime(),
  updatedAt: z.string().datetime(),
});

const ErrorResponseSchema = z.object({
  error: z.object({
    code: z.string(),
    message: z.string(),
    details: z.record(z.string()).optional(),
  }),
});

// Validate API responses
async function fetchUser(id: string) {
  const response = await fetch(`/api/users/${id}`);
  const data = await response.json();
  
  // Validate response
  const result = UserResponseSchema.safeParse(data);
  
  if (!result.success) {
    throw new Error('Invalid API response');
  }
  
  return result.data;
}

// Validate API requests
function validateCreateUserRequest(body: unknown) {
  const result = CreateUserRequestSchema.safeParse(body);
  
  if (!result.success) {
    return {
      success: false,
      error: result.error.format(),
    };
  }
  
  return {
    success: true,
    data: result.data,
  };
}
```

## Real-World Use Cases

### Form Validation
```
Form Schema:
┌─────────────────────────────────────────────────────────────────┐
│  Registration Form                                              │
│  ├── email: z.string().email()                                 │
│  ├── password: z.string().min(8).max(100)                      │
│  ├── confirmPassword: z.string()                               │
│  ├── name: z.string().min(1).max(50)                           │
│  ├── age: z.number().int().min(13).max(150)                    │
│  └── terms: z.literal(true)                                    │
│                                                                 │
│  Cross-field validation:                                        │
│  └── password === confirmPassword                              │
└─────────────────────────────────────────────────────────────────┘
```

### API Contract Validation
```
API Schema:
┌─────────────────────────────────────────────────────────────────┐
│  POST /api/users                                                │
│  Request: CreateUserRequestSchema                               │
│  Response: UserResponseSchema | ErrorResponseSchema            │
│                                                                 │
│  GET /api/users/:id                                            │
│  Response: UserResponseSchema | ErrorResponseSchema            │
│                                                                 │
│  Benefits:                                                      │
│  • Type-safe API calls                                         │
│  • Runtime validation                                          │
│  • Clear error messages                                        │
│  • Auto-generated documentation                                │
└─────────────────────────────────────────────────────────────────┘
```

## Common Mistakes

1. **Not inferring types**: Manually defining types instead of using `z.infer`
2. **Over-validating**: Adding unnecessary validations
3. **Missing defaults**: Not setting default values
4. **Ignoring transforms**: Not using transforms for data normalization
5. **Poor error messages**: Not customizing error messages

## Best Practices

1. **Use `z.infer`**: Always infer TypeScript types from schemas
2. **Compose schemas**: Build complex schemas from simple ones
3. **Custom error messages**: Provide clear, user-friendly error messages
4. **Use transforms**: Normalize data at validation time
5. **Validate at boundaries**: Validate API requests/responses

## Performance Considerations

```
Zod Performance:
┌─────────────────────────────────────────────────────────────────┐
│  Fast Validation:                                                │
│  • Optimized validation engine                                  │
│  • Minimal allocations                                          │
│  • Short-circuit evaluation                                     │
│                                                                 │
│  Bundle Size:                                                    │
│  • ~14KB gzipped                                                │
│  • Tree-shakeable                                               │
│  • No dependencies                                              │
│                                                                 │
│  Caching:                                                        │
│  • Schemas are reusable                                         │
│  • Compiled validators                                          │
│  • Memoized transforms                                          │
└─────────────────────────────────────────────────────────────────┘
```

## Interview Questions

### Beginner (5)
1. **What is Zod?**
   - Answer: A TypeScript-first schema declaration and validation library with automatic type inference.

2. **What is `z.infer`?**
   - Answer: A utility type that infers TypeScript types from Zod schemas.

3. **What is the difference between `parse` and `safeParse`?**
   - Answer: `parse` throws on error; `safeParse` returns a result object with success/error.

4. **How do you create an object schema?**
   - Answer: Use `z.object()` with property definitions: `z.object({ name: z.string() })`.

5. **How do you add default values?**
   - Answer: Use `.default()`: `z.string().default('value')`.

### Intermediate (5)
6. **How do you handle optional fields?**
   - Answer: Use `.optional()`: `z.string().optional()` or `z.string().nullable()`.

7. **What are transformations?**
   - Answer: Functions that modify validated data: `z.string().transform(val => val.toUpperCase())`.

8. **How do you handle nested objects?**
   - Answer: Compose schemas: `z.object({ address: z.object({ city: z.string() }) })`.

9. **What is `superRefine`?**
   - Answer: A method for complex cross-field validation with custom error paths.

10. **How do you validate arrays?**
    - Answer: Use `z.array()`: `z.array(z.string()).min(1).max(10)`.

### Senior (10)
11. **How do you handle discriminated unions?**
    - Answer: Use `z.discriminatedUnion()` for tagged unions with a discriminant field.

12. **How do you integrate Zod with tRPC?**
    - Answer: Use Zod schemas for input/output validation in tRPC procedures.

13. **How do you handle async validation?**
    - Answer: Use `.refine()` with async validation logic, but prefer sync validation when possible.

14. **How do you optimize Zod performance?**
    - Answer: Reuse schemas, avoid unnecessary transforms, use `safeParse` for error handling.

15. **How do you handle API contract validation?**
    - Answer: Define request/response schemas, validate at API boundaries, share schemas between client/server.

16. **How do you handle complex conditional validation?**
    - Answer: Use `superRefine` or `.refine()` with conditional logic.

17. **How do you handle file uploads?**
    - Answer: Use `z.instanceof(File)` or custom validation for file metadata.

18. **How do you handle internationalized error messages?**
    - Answer: Pass error message functions that return localized strings.

19. **How do you test Zod schemas?**
    - Answer: Test valid/invalid inputs, test transforms, test error messages.

20. **How do you handle schema composition?**
    - Answer: Use `.merge()`, `.extend()`, or `.pick()` to compose schemas.

### FAANG-style (5)
21. **Design a type-safe API layer with Zod**
- **Answer**: 
  - Define request/response schemas
  - Share schemas between client/server
  - Validate at API boundaries
  - Auto-generate TypeScript types
  - Document with schemas

22. **How would you handle form validation at scale?**
- **Answer**: 
  - Shared validation schemas
  - Custom validation rules
  - Performance optimization
  - Accessibility compliance
  - Analytics integration

23. **Explain Zod's type inference system**
- **Answer**: 
  - Maps Zod types to TypeScript types
  - Handles complex types (unions, intersections)
  - Preserves literal types
  - Infers optional/nullable correctly

24. **How do you optimize Zod for large schemas?**
- **Answer**: 
  - Schema composition
  - Lazy evaluation
  - Caching
  - Selective validation

25. **Design a validation system for a microservices architecture**
- **Answer**: 
  - Shared schemas in a package
  - Service-specific validation
  - Contract testing
  - Schema versioning

### Follow-ups (5)
26. **How do you handle Zod in server-side rendering?**
- **Answer**: Validate data on server, pass validated data to client, use schemas for both.

27. **How do you handle Zod with React Server Components?**
- **Answer**: Validate data on server, pass typed data to client components.

28. **How do you handle Zod in edge functions?**
- **Answer**: Zod works in edge environments, use lightweight schemas for performance.

29. **How do you handle Zod schema versioning?**
- **Answer**: Version schemas, migrate gradually, maintain backward compatibility.

30. **How do you handle Zod in micro-frontends?**
- **Answer**: Share schemas via package, validate at boundaries, consistent error handling.

## Summary

Zod provides a powerful, type-safe approach to schema validation in TypeScript. Master its API, integration patterns, and best practices for building robust validation systems.

## References & Learn More

- [Zod Documentation](https://zod.dev/)
- [Zod GitHub](https://github.com/colinhacks/zod)
- [React Hook Form Integration](https://react-hook-form.com/docs/useform/resolver#zod)
- [tRPC with Zod](https://trpc.io/docs/)
- [Zod Examples](https://github.com/colinhacks/zod#examples)
