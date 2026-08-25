# Objects, Prototypes & `this` — JavaScript

> **3 files.** JavaScript's object model: how `this` binding really works, the prototype chain behind every property lookup, and metaprogramming with Proxy and Reflect.

[![Files](https://img.shields.io/badge/files-3-blue)](#files)
[![Category](https://img.shields.io/badge/category-Objects_Prototypes_this-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [`this` Keyword](10.1.2.01-this.md) | Implicit/explicit binding, arrow functions, `call`/`apply`/`bind`, the four binding rules | 25 min |
| 02 | [Prototypes](10.1.2.02-prototypes.md) | Prototype chain, `__proto__`, `Object.create`, classical inheritance, `class` keyword | 30 min |
| 03 | [Proxy & Reflect](10.1.2.03-proxy-reflect.md) | Metaprogramming, traps, validation, reactive patterns (Vue 3 uses these) | 25 min |

---

## Read order

`this` → Prototypes → Proxy & Reflect.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
|------------------------|-----------------|
| Prototypes & inheritance (`class`, `extends`) | `apps/api/src/shared/common/errors/domain.errors.ts` - domain errors extend a base `Error` subclass chain |
| `this` binding & class methods | `packages/ui/src/components/feedback/error-boundary.tsx` - class component using static lifecycle, instance methods, and `this.props` |

---

## Navigation

[← Back to JavaScript](../INDEX.md)
