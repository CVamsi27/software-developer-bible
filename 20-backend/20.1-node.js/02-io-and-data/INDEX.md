# I/O & Data - Node.js

> **Study time:** ≈ 40 min of reading (5 files, ~8 min average).
> **5 files.** The I/O primitives every backend service uses: streams for piece-by-piece data handling, buffers for binary data, the file system module, and the raw HTTP server that Express/Fastify/NestJS sit on top of.

[![Files](https://img.shields.io/badge/files-5-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-I%2FO%20%26%20Data-success)](../INDEX.md)

---

## Reading flow

1. Follow a write through the streams chapter: acceptance, pressure, finish and failure.
2. Inspect the same data as bytes in Buffers; trace a split frame and the ownership of its payload.
3. Move those bytes through a file replacement, then a bounded HTTP request/response.
4. Use [Revision](REVISION.md) to explain the failure boundaries after the examples.

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Streams](20.1.2.01-streams.md) | Readable, Writable, Transform, Duplex, backpressure, `pipeline()`, error handling | Important | Important | 10 min |
| 02 | [Buffers](20.1.2.02-buffers.md) | Buffer creation, encoding (utf8, base64, hex), allocation, `alloc` vs `allocUnsafe`, TypedArray interop, memory pooling | Important | Important | 10 min |
| 03 | [File System](20.1.2.03-file-system.md) | `fs` module, read/write (sync vs async vs stream), file watching, permissions, atomic writes, always handle errors | Essential | Foundational | 8 min |
| 04 | [HTTP Module](20.1.2.04-http-module.md) | `createServer`, `IncomingMessage`/`ServerResponse` as streams, routing manually, client requests, reverse proxy, keep-alive | Essential | Foundational | 10 min |

---

[← Back to Node.js](../INDEX.md)

---

## Docita Anchor

The [Docita case study](../../../projects/docita/INDEX.md) supplies code pointers to inspect against the chapter contracts. Current streaming, admission and operational guarantees need runtime evidence; these paths do not alone establish deployment status.

| Topic | Docita evidence |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Buffers | `apps/api/src/shared/modules/document-generation/pdf/pdf-generator.service.ts` - PDFKit document assembled chunk-by-chunk into a returned `Buffer` |
| File system | `apps/api/src/shared/modules/database/database-backup.service.ts` - spawns `pg_dump`, writes dump files under a retention policy |
| File uploads | `apps/api/src/shared/common/utils/upload.utils.ts` - inspect multer disk staging and admission checks; MIME labels alone do not validate file content |
| HTTP module / server | `apps/api/src/main.ts` - Express bootstrap: CORS allow-list, helmet, URI versioning, Sentry instrumentation |

Inspect current pipeline/library staging and error ownership before attributing bounded streaming or cleanup guarantees to the case study. The chapter fixtures state and test their own I/O contracts.
---

[← Previous: Runtime & Async](../01-runtime-and-async/INDEX.md) · [Next: Processes & Concurrency →](../03-processes-and-concurrency/INDEX.md)
