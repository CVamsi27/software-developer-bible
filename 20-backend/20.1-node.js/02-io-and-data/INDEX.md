# I/O & Data - Node.js

> **4 files.** The I/O primitives every backend service uses: streams for piece-by-piece data handling, buffers for binary data, the file system module, and the raw HTTP server that Express/Fastify/NestJS sit on top of.

[![Files](https://img.shields.io/badge/files-4-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-I%2FO%20%26%20Data-success)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Streams](20.1.2.01-streams.md) | Readable, Writable, Transform, Duplex, backpressure, `pipeline()`, error handling | 30 min |
| 02 | [Buffers](20.1.2.02-buffers.md) | Buffer creation, encoding (utf8, base64, hex), allocation, `alloc` vs `allocUnsafe`, TypedArray interop, memory pooling | 20 min |
| 03 | [File System](20.1.2.03-file-system.md) | `fs` module, read/write (sync vs async vs stream), file watching, permissions, atomic writes, always handle errors | 25 min |
| 04 | [HTTP Module](20.1.2.04-http-module.md) | `createServer`, `IncomingMessage`/`ServerResponse` as streams, routing manually, client requests, reverse proxy, keep-alive | 30 min |

---

[← Back to Node.js](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Buffers | `apps/api/src/shared/modules/document-generation/pdf/pdf-generator.service.ts` - PDFKit document assembled chunk-by-chunk into a returned `Buffer` |
| File system | `apps/api/src/shared/modules/database/database-backup.service.ts` - spawns `pg_dump`, writes dump files under a retention policy |
| File uploads | `apps/api/src/shared/common/utils/upload.utils.ts` - multer `diskStorage` temp dir gated by a MIME allow-list |
| HTTP module / server | `apps/api/src/main.ts` - Express bootstrap: CORS allow-list, helmet, URI versioning, Sentry instrumentation |

_Raw `stream.pipeline()` wiring: no direct docita implementation yet._ Streaming happens inside libraries; uploads stage to disk instead of piping through transforms.
