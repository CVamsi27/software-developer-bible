---
section: TypeScript
category: Core
tags: [concept]
---

# Branded Types

## TL;DR

Branded (or nominal) types are a TypeScript pattern that adds a phantom property to a primitive to create a distinct type. They prevent mixing `UserId` and `OrderId` even though both are strings at runtime. The pattern uses intersection with `{ __brand: 'UserId' }`.

## Why It Matters

Senior engineers use branded types to: prevent mixing IDs (`UserId` vs `OrderId`), enforce units (`Meters` vs `Feet`), and validate external data at the type boundary. They are the standard way to get nominal typing in TypeScript's structural type system.

## Definition

**Branded types** (also called **nominal types** or **opaque types**) are a TypeScript pattern that creates distinct types from structurally identical primitives by adding a unique "brand" property. Since TypeScript uses structural typing (duck typing), two types with the same shape are interchangeable — which can lead to bugs. Branded types add a phantom property that makes structurally identical types distinct at compile time, catching errors like passing a UserId where an OrderId is expected.

## Why Do We Need It?

1. **Distinguish structurally identical types** — `UserId` and `OrderId` are both `string`, but shouldn't be interchangeable
2. **Runtime safety** — Prevent mixing up sensitive identifiers (credit card vs transaction ID)
3. **Domain modeling** — Encode domain constraints in the type system
4. **Type-level documentation** — Brand names document what a value represents
5. **Zero runtime cost** — Brands are erased at compile time; no runtime overhead

## How It Works

### Structural vs Nominal Typing

```text
Structural vs Nominal:
═══════════════════════════════════════════════════════════════

Structural Typing (TypeScript default):
┌─────────────────────────────────────────────────────────────┐
│  type UserId = string;                                       │
│  type ProductId = string;                                    │
│                                                              │
│  function getUser(id: UserId) { ... }                        │
│  function getProduct(id: ProductId) { ... }                  │
│                                                              │
│  const uid: UserId = 'abc';                                  │
│  getProduct(uid);  // ✅ No error! Both are string          │
│  // ⚠️ Passed UserId to getProduct by accident               │
└─────────────────────────────────────────────────────────────┘

Nominal Typing (Branded):
┌─────────────────────────────────────────────────────────────┐
│  type UserId = string & { readonly __brand: 'UserId' };      │
│  type ProductId = string & { readonly __brand: 'ProductId' } │
│                                                              │
│  function getUser(id: UserId) { ... }                        │
│  function getProduct(id: ProductId) { ... }                  │
│                                                              │
│  const uid = createUserId('abc');                            │
│  getProduct(uid);  // ❌ Type error!                         │
│  // ✅ TypeScript prevents passing UserId to getProduct      │
└─────────────────────────────────────────────────────────────┘

```

### Brand Implementation Patterns

```typescript
// ─── Common Brand Idiom ──────────────────────────────────────
type Brand<T, B extends string> = T & { readonly __brand: B };

type UserId = Brand<string, 'UserId'>;
type OrderId = Brand<string, 'OrderId'>;
type ProductId = Brand<string, 'ProductId'>;

// ─── Brand with Symbol (truly unique) ────────────────────────
declare const __brand: unique symbol;

type Branded<T, B extends string> = T & {
  readonly [__brand]: B;
};

type Email = Branded<string, 'Email'>;

// ─── Brand Factory Helper ────────────────────────────────────
function createBrand<T, B extends string>(brand: B) {
  return (value: T): Brand<T, B> => value as Brand<T, B>;
}

const createUserId = createBrand<string, 'UserId'>('UserId');
const uid = createUserId('user_123'); // Type: UserId
```

## Code Examples

### 1. Basic Branded Types

```typescript
// Define brands
type Brand<T, B extends string> = T & { readonly __brand: B };
type UserId = Brand<string, 'UserId'>;
type OrderId = Brand<string, 'OrderId'>;
type ProductId = Brand<string, 'ProductId'>;

// Factory functions (type-safe creation)
function toUserId(id: string): UserId {
  return id as UserId;
}

function toOrderId(id: string): OrderId {
  return id as OrderId;
}

// Typed functions
function getUser(userId: UserId): void {
  console.log(`Fetching user: ${userId}`);
}

function getOrder(orderId: OrderId): void {
  console.log(`Fetching order: ${orderId}`);
}

// Usage
const uid = toUserId('user_456');
const oid = toOrderId('order_789');

getUser(uid);   // ✅ Correct
getOrder(oid);  // ✅ Correct
// getUser(oid); // ❌ Type error! Argument of type 'OrderId' not assignable to 'UserId'
// getOrder(uid); // ❌ Type error!
```

### 2. Branded Numbers

```typescript
type Brand<T, B extends string> = T & { readonly __brand: B };

// Number brands
type Quantity = Brand<number, 'Quantity'>;
type Price = Brand<number, 'Price'>;
type Discount = Brand<number, 'Discount'>;

// Factory functions
function validateQuantity(n: number): Quantity | Error {
  if (n < 0 || n > 999) return new Error('Invalid quantity');
  return n as Quantity;
}

function validatePrice(n: number): Price | Error {
  if (n < 0 || n > 99999) return new Error('Invalid price');
  return n as Price;
}

// Typed business logic
function calculateTotal(price: Price, quantity: Quantity, discount: Discount): Price {
  const total = (price as number) * (quantity as number) * (1 - (discount as number));
  return total as Price;
}

// Safe usage
const price = validatePrice(29.99) as Price;
const quantity = validateQuantity(3) as Quantity;
const discount = 0.1 as Discount;

const total = calculateTotal(price, quantity, discount); // ✅
// calculateTotal(price, 3 as Quantity, discount); // ✅ Explicit cast
// calculateTotal(price, 29.99, discount); // ❌ Type error
```

### 3. Branded Object Types

```typescript
type Brand<T, B extends string> = T & { readonly __brand: B };

// Object brands
type Email = Brand<string, 'Email'>;
type Phone = Brand<string, 'Phone'>;
type SSN = Brand<string, 'SSN'>;

// Sensitive data types
interface User {
  id: UserId;
  email: Email;
  phone: Phone;
  ssn: SSN;
}

// Validation functions
function validateEmail(input: string): Email | null {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(input) ? (input as Email) : null;
}

function validatePhone(input: string): Phone | null {
  const cleaned = input.replace(/\D/g, '');
  return cleaned.length === 10 ? (cleaned as Phone) : null;
}

// Type-safe API
function sendEmail(email: Email, message: string): void {
  console.log(`Sending to ${email}: ${message}`);
}

function sendSMS(phone: Phone, message: string): void {
  console.log(`SMS to ${phone}: ${message}`);
}

// Usage
const email = validateEmail('user@example.com');
if (email) {
  sendEmail(email, 'Welcome!'); // ✅
  // sendSMS(email, 'Welcome!'); // ❌ Cannot send SMS to email
}

// Masking sensitive data
function maskSSN(ssn: SSN): string {
  const str = ssn as string;
  return `***-**-${str.slice(-4)}`;
}
```

### 4. Branded Types with Union Types

```typescript
type Brand<T, B extends string> = T & { readonly __brand: B };

// Discriminated unions with brands
type Success<T> = Brand<{ data: T }, 'Success'>;
type Failure = Brand<{ error: string }, 'Failure'>;
type Loading = Brand<{}, 'Loading'>;

type AsyncState<T> = Success<T> | Failure | Loading;

function handleState<T>(state: AsyncState<T>): string {
  if ('data' in state) {
    return `Success: ${state.data}`; // TypeScript infers Success<T>
  }
  if ('error' in state) {
    return `Error: ${state.error}`; // TypeScript infers Failure
  }
  return 'Loading'; // Must be Loading
}

// API response types
type ApiResponse<T> = Brand<
  | { status: 200; data: T }
  | { status: 400; error: string }
  | { status: 401; error: string }
  | { status: 500; error: string },
  'ApiResponse'
>;

function parseResponse<T>(response: ApiResponse<T>): T | never {
  if (response.status === 200) return response.data;
  throw new Error(`API Error: ${response.error}`);
}
```

### 5. Branded Types with Generics

```typescript
type Brand<T, B extends string> = T & { readonly __brand: B };

// Generic branded types
type Id<T extends string> = Brand<string, T>;
type Money<C extends string> = Brand<number, C>;

// Currency brands
type USD = Money<'USD'>;
type EUR = Money<'EUR'>;
type JPY = Money<'JPY'>;

// Generic financial operations
function addMoney<C extends string>(a: Money<C>, b: Money<C>): Money<C> {
  return ((a as number) + (b as number)) as Money<C>;
}

function convertCurrency<From extends string, To extends string>(
  amount: Money<From>,
  rate: number
): Money<To> {
  return ((amount as number) * rate) as Money<To>;
}

// Usage
const usd1 = 100 as USD;
const usd2 = 50 as USD;
const totalUSD = addMoney(usd1, usd2); // USD ✅
// addMoney(usd1, 50 as EUR); // ❌ Type error! Can't add USD + EUR

const eurAmount = convertCurrency<'USD', 'EUR'>(usd1, 0.85); // EUR ✅

// Entity ID brands
type Entity<T extends string> = Brand<string, T>;
type UserId = Entity<'User'>;
type PostId = Entity<'Post'>;
type CommentId = Entity<'Comment'>;

// Generic entity finder
function findById<T extends string>(id: Entity<T>): { type: T; id: string } {
  return { type: id as unknown as T, id: id as string };
}

const user = findById('u123' as UserId); // { type: "User"; id: "u123" }
```

### 6. Branded Types with Runtime Validation

```typescript
type Brand<T, B extends string> = T & { readonly __brand: B };

// Runtime validation with branded return types
type NonEmptyString = Brand<string, 'NonEmptyString'>;
type EmailAddress = Brand<string, 'EmailAddress'>;
type PositiveInteger = Brand<number, 'PositiveInteger'>;

// Validation function that returns branded type
function nonEmpty(input: string): NonEmptyString | null {
  return input.trim().length > 0 ? (input as NonEmptyString) : null;
}

function email(input: string): EmailAddress | null {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(input) ? (input as EmailAddress) : null;
}

function positiveInt(input: number): PositiveInteger | null {
  return Number.isInteger(input) && input > 0 ? (input as PositiveInteger) : null;
}

// Zod-like schema with branded types
interface BrandedSchema<T, B extends string> {
  parse: (input: unknown) => Brand<T, B>;
  safeParse: (input: unknown) => { success: true; data: Brand<T, B> } | { success: false; error: string };
}

function createBrandedSchema<T, B extends string>(
  validator: (input: unknown) => input is T,
  brand: B
): BrandedSchema<T, B> {
  return {
    parse: (input: unknown): Brand<T, B> => {
      if (!validator(input)) throw new Error(`Validation failed for ${brand}`);
      return input as Brand<T, B>;
    },
    safeParse: (input: unknown) => {
      if (validator(input)) return { success: true, data: input as Brand<T, B> };
      return { success: false, error: `Invalid ${brand}` };
    },
  };
}

const UserIdSchema = createBrandedSchema(
  (x): x is string => typeof x === 'string' && /^u_\d+$/.test(x),
  'UserId'
);

const parsed = UserIdSchema.safeParse('u_123');
if (parsed.success) {
  // parsed.data is UserId (branded string)
  console.log(parsed.data);
}
```

### 7. Branded Types for Units

```typescript
type Brand<T, B extends string> = T & { readonly __brand: B };

// Unit types
type Meters = Brand<number, 'Meters'>;
type Seconds = Brand<number, 'Seconds'>;
type Kilograms = Brand<number, 'Kilograms'>;

// Derived units (type-safe physics)
type MetersPerSecond = Brand<number, 'MetersPerSecond'>;
type Newtons = Brand<number, 'Newtons'>;
type Joules = Brand<number, 'Joules'>;

// Physics functions with unit safety
function speed(distance: Meters, time: Seconds): MetersPerSecond {
  return ((distance as number) / (time as number)) as MetersPerSecond;
}

function force(mass: Kilograms, acceleration: MetersPerSecond): Newtons {
  return ((mass as number) * (acceleration as number)) as Newtons;
}

function work(force: Newtons, distance: Meters): Joules {
  return ((force as number) * (distance as number)) as Joules;
}

// Usage
const d = 100 as Meters;
const t = 9.58 as Seconds;  // Usain Bolt's 100m world record

const v = speed(d, t);        // MetersPerSecond ✅
// speed(d, 100 as Kilograms); // ❌ Type error! Can't pass Kilograms for time

const m = 80 as Kilograms;
const f = force(m, v);         // Newtons ✅
const w = work(f, d);          // Joules ✅

console.log(`Speed: ${v} m/s, Force: ${f} N, Work: ${w} J`);
```

### 8. Branded Types for ISO Strings

```typescript
type Brand<T, B extends string> = T & { readonly __brand: B };

// Date/time branded types
type ISO8601Date = Brand<string, 'ISO8601Date'>;
type ISO8601DateTime = Brand<string, 'ISO8601DateTime'>;
type UUID = Brand<string, 'UUID'>;
type JWT = Brand<string, 'JWT'>;

// Type-safe date handling
function parseISODate(date: ISO8601Date): Date {
  return new Date(date as string);
}

function formatToISODate(date: Date): ISO8601Date {
  return date.toISOString().split('T')[0] as ISO8601Date;
}

interface Event {
  id: UUID;
  title: string;
  startDate: ISO8601Date;
  startTime: ISO8601DateTime;
  createdAt: ISO8601DateTime;
  token?: JWT;
}

// Validation
function isUUID(str: string): str is UUID {
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  return uuidRegex.test(str);
}

function isJWT(str: string): str is JWT {
  return /^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$/.test(str);
}

// Usage
const event: Event = {
  id: '550e8400-e29b-41d4-a716-446655440000' as UUID,
  title: 'Meeting',
  startDate: '2024-06-15' as ISO8601Date,
  startTime: '2024-06-15T09:00:00Z' as ISO8601DateTime,
  createdAt: new Date().toISOString() as ISO8601DateTime,
};
```

### 9. Flavoring (Lightweight Branding)

```typescript
// "Flavoring" — a weaker form of branding that allows
// the branded type to still be assignable FROM the base type
// but NOT TO other branded types

type Flavor<T, B extends string> = T & { __flavor?: B };

type UserId = Flavor<string, 'UserId'>;
type OrderId = Flavor<string, 'OrderId'>;

// Flavoring allows assignment from string:
const uid: UserId = 'user_123'; // ✅ Allowed (flavor is optional)

// But still prevents cross-assignment:
function getUser(id: UserId) { /* ... */ }
// getUser(oid as OrderId); // ❌ Type error (different flavors)

// When to use Flavor vs Brand:
// ─────────────────────────────
// Flavor: When you want to allow raw values but prevent
//         mixing up IDs from different domains
//
// Brand:  When you want strict enforcement and require
//         explicit construction via factory functions

// Flavoring in function parameters:
function setUserId(id: UserId) {
  // `id` is branded but can receive raw strings
  console.log(id);
}

setUserId('abc');        // ✅ Allowed with Flavor
// setUserId('abc' as OrderId); // ❌ Different flavor
```

### 10. Branded Types with Discriminated Unions

```typescript
type Brand<T, B extends string> = T & { readonly __brand: B };

// Type-safe payment processing
type CardPayment = Brand<
  { type: 'card'; cardNumber: string; expiry: string; cvv: string },
  'CardPayment'
>;

type BankTransfer = Brand<
  { type: 'bank'; accountNumber: string; routingNumber: string },
  'BankTransfer'
>;

type CryptoPayment = Brand<
  { type: 'crypto'; walletAddress: string; currency: 'BTC' | 'ETH' },
  'CryptoPayment'
>;

type Payment = CardPayment | BankTransfer | CryptoPayment;

// Type-safe payment handler
function processPayment(payment: Payment): string {
  // TypeScript narrows based on the branded type's data
  switch (payment.type) {
    case 'card':
      return `Processing card ${payment.cardNumber.slice(-4)}`;
    case 'bank':
      return `Processing transfer from ${payment.accountNumber}`;
    case 'crypto':
      return `Processing ${payment.currency} from ${payment.walletAddress}`;
  }
}

// Factory with validation
function createCardPayment(
  cardNumber: string,
  expiry: string,
  cvv: string
): CardPayment | Error {
  if (!/^\d{16}$/.test(cardNumber)) return new Error('Invalid card number');
  if (!/^\d{2}\/\d{2}$/.test(expiry)) return new Error('Invalid expiry');
  if (!/^\d{3,4}$/.test(cvv)) return new Error('Invalid CVV');

  return { type: 'card', cardNumber, expiry, cvv } as CardPayment;
}
```

## Real-World Use Cases

| Use Case | Branded Type | Prevents |
|----------|-------------|----------|
| **User IDs vs Order IDs** | `UserId`, `OrderId` | Mixing up IDs in API calls |
| **Currency amounts** | `USD`, `EUR`, `JPY` | Adding different currencies |
| **Units of measurement** | `Meters`, `Seconds`, `Kg` | Passing meters where seconds expected |
| **Sensitive data** | `Email`, `SSN`, `Phone` | Logging or displaying sensitive data |
| **API keys vs Tokens** | `ApiKey`, `JWT`, `RefreshToken` | Using wrong auth in headers |
| **ISO date vs datetime** | `ISO8601Date`, `ISO8601DateTime` | Date-time format confusion |
| **Validation state** | `Validated<T>`, `Sanitized<T>` | Using unvalidated user input |
| **Entity IDs** | `Entity<'User'>`, `Entity<'Post'>` | Generic but distinct ID types |

## Common Mistakes

### 1. Brands That Don't Actually Enforce

```typescript
// ❌ BAD: Brands without intersection (&)
type UserId = { __brand: 'UserId' }; // Creates a new type, not a branded string!
// This doesn't extend string, so it can't be used as one

// ✅ GOOD: Intersection with base type
type UserId = string & { readonly __brand: 'UserId' };
```

### 2. Not Using Readonly

```typescript
// ❌ BAD: Mutable brand can be removed
type UserId = string & { __brand: 'UserId' };
// Brand can be removed by mutation:
(uid as any).__brand = undefined;

// ✅ GOOD: Readonly brand
type UserId = string & { readonly __brand: 'UserId' };
```

### 3. Using the Same Brand Name

```typescript
// ❌ BAD: Same brand name for different concepts
type UserId = string & { readonly __brand: 'Id' };
type OrderId = string & { readonly __brand: 'Id' };
// These are the same type! (same brand string)

// ✅ GOOD: Unique brand per concept
type UserId = string & { readonly __brand: 'UserId' };
type OrderId = string & { readonly __brand: 'OrderId' };
```

### 4. Runtime Brand Exposure

```typescript
// ❌ BAD: Brand leaks at runtime
type UserId = string & { readonly __brand: 'UserId' };
const uid = 'abc' as UserId;
console.log(JSON.stringify(uid));
// "abc" — but there's no __brand property at runtime!

// Brands are compile-time only. Don't check them at runtime.
```

## Best Practices

```typescript
// 1. Use a shared Brand utility type
type Brand<T, B extends string> = T & { readonly __brand: B };

// 2. Create factory functions for construction
function createUserId(id: string): UserId {
  if (!id.startsWith('u_')) throw new Error('Invalid UserId format');
  return id as UserId;
}

// 3. Use brands for public API boundaries
//    (internal code can use raw types)

// 4. Combine with validation for runtime safety
type Validated<T> = Brand<T, 'Validated'>;
function validate<T>(input: T): Validated<T> {
  return input as Validated<T>;
}

// 5. Brand function return types, not parameters
function fetchUser(id: UserId): Promise<User> { /* ... */ }
```

## Performance Considerations

| Aspect | Impact | Notes |
|--------|--------|-------|
| **Compile time** | Negligible | Brands are just type intersections |
| **Runtime** | Zero | Brands are completely erased at compile time |
| **Bundle size** | Zero | No JavaScript emitted for brands |
| **IDE performance** | Minimal | Large branded union types may slow autocomplete |
| **Serialization** | No effect | Brands don't produce runtime properties |

## Summary

Branded types add nominal typing to TypeScript's structural type system, preventing accidental mixing of structurally identical types like UserId and OrderId. They are a compile-time-only pattern with zero runtime cost. Use factory functions for construction, combine with validation for runtime safety, and always use unique brand strings for each distinct concept.

## Cheat Sheet

```typescript
// Brand utility
type Brand<T, B extends string> = T & { readonly __brand: B };

// Basic usage
type UserId = Brand<string, 'UserId'>;
type Email = Brand<string, 'Email'>;
type USD = Brand<number, 'USD'>;

// Factory functions
function createUserId(id: string): UserId {
  return id as UserId;
}

// Type safety
type Meters = Brand<number, 'Meters'>;
type Seconds = Brand<number, 'Seconds'>;

function speed(d: Meters, t: Seconds): MetersPerSecond {
  return ((d as number) / (t as number)) as MetersPerSecond;
}

// Flavoring (weak branding)
type Flavor<T, B extends string> = T & { __flavor?: B };

// With generics
type Entity<T extends string> = Brand<string, T>;
type UserId = Entity<'User'>;
type ProductId = Entity<'Product'>;

// Unique symbol brand (strongest)
declare const __brand: unique symbol;
type StrongBrand<T, B extends string> = T & {
  readonly [__brand]: B;
};
```

```text
Branded Types Key Points:
├── Pattern: T & { readonly __brand: B }
├── Runtime cost: Zero (compile-time only)
├── Purpose: Prevent mixing up structurally identical types
├── Factory: Use functions to construct branded values
├── Flavor: Allowed from base, NOT to other flavors
├── Symbol: Use unique symbol for strongest isolation
└── Gotcha: No runtime enforcement (cast only)

When to Use:
├── IDs (User, Order, Product, etc.)
├── Currency amounts (USD, EUR, etc.)
├── Units (Meters, Seconds, etc.)
├── Sensitive data (Email, SSN, Phone)
├── Validated data (Validated<T>)
└── API boundaries (public vs internal types)

Don't Use:
├── Simple wrappers (just document instead)
├── Runtime validation (use Zod, io-ts)
└── Over-engineering (one-off usage)
```

---

## See Also
- [Advanced Generics](10-Advanced-Generics.md)
- [Conditional Types](04-Conditional-Types.md)
- [Declaration Files](14-Declaration-Files.md)
- [Infer](05-Infer.md)
- [JavaScript](../01-JavaScript/)
- [Mapped Types](07-Mapped-Types.md)
- [Template Literal Types](12-Template-Literal-Types.md)
- [Type Narrowing](08-Type-Narrowing.md)

## References & Learn More

- [TypeScript Handbook: Branded Types](https://www.typescriptlang.org/play#example/nominal-typing)
- [Nominal Typing in TypeScript](https://michalzalecki.com/nominal-typing-in-typescript/)
- [TypeScript Deep Dive: Branded Types](https://basarat.gitbook.io/typescript/main-1/nominaltyping)
- [Branded Types for Better Type Safety](https://dev.to/tipsy_dev/advanced-typescript-made-easy-branded-types-2p3l)
- [flavor Pattern](https://github.com/Microsoft/TypeScript/issues/202#issuecomment-566337388)
