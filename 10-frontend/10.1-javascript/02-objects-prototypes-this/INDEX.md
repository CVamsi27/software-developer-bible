# Objects, Prototypes & `this` — JavaScript

> **Study time:** ≈ 37 min of reading (4 files, ~9 min average).
> **4 files.** JavaScript's object model: how `this` binding really works, the prototype chain behind every property lookup, and metaprogramming with `Proxy` and `Reflect`.

[![Files](https://img.shields.io/badge/files-4-blue)](#chapters)
[![Category](https://img.shields.io/badge/category-Objects_Prototypes_this-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Chapters

The Files badge counts these 3 chapters plus the revision companion.

| Order | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [`this` Keyword](10.1.2.01-this.md) | Implicit and explicit binding, sloppy boxing, `.bind()` slots, arrow functions, callbacks, and construction | Essential | Foundational | 11 min |
| 02 | [Prototypes](10.1.2.02-prototypes.md) | Prototype chain, 4-step `new`, descriptors, `__proto__`, `Object.create`, `instanceof`, `class`, and pollution | Essential | Foundational | 11 min |
| 03 | [Proxy & Reflect](10.1.2.03-proxy-reflect.md) | Metaprogramming traps, receiver forwarding, invariants, internal slots, and lazy `WeakMap` wrapping | Important | Specialized | 11 min |

---

## Read order

Start with [`this`](10.1.2.01-this.md): follow how an invocation supplies the receiver, and why extracting a method changes that relationship.

Then read [Prototypes](10.1.2.02-prototypes.md): separate where a property is found from which receiver a method uses. Follow with [Proxy & Reflect](10.1.2.03-proxy-reflect.md) to intercept those operations and forward them deliberately.

Trace one shared method called on two objects, then explain what changes when a proxy wraps one receiver. Use [section revision](REVISION.md) after the chapters.

---

## Docita Anchor

Examples in [Docita](https://github.com/CVamsi27/docita), a healthcare-platform repository with a NestJS API and React and Astro apps in a TypeScript monorepo. Study the chapter, then locate the implementation:

| Topic in this category | Docita evidence |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Prototypes & inheritance (`class`, `extends`) | `apps/api/src/shared/common/errors/domain.errors.ts` - domain errors extend a base `Error` subclass chain |
| `this` binding & class methods | `packages/ui/src/components/feedback/error-boundary.tsx` - class component using static lifecycle, instance methods, and `this.props` |

---

## Navigation

[← Back to JavaScript](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
