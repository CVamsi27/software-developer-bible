---
section: Node.js
category: Backend
tags: [concept]
---

# Node.js Streams

## TL;DR

Streams are Node's abstraction for handling data piece-by-piece without loading it all into memory. Four types: Readable, Writable, Transform, Duplex. Backpressure occurs when a writable can't keep up with a readable. `pipeline()` is the safe way to compose streams.

## Why It Matters

Senior engineers use streams for: large file processing, HTTP request/response bodies, real-time data pipelines. They know to use `pipeline()` (which cleans up on error) over `.pipe()` (which leaks), and to handle backpressure with `drain` events or async iteration.

## Definition

**Streams** are one of the most powerful concepts in Node.js. They are instances of `Stream` class that allow you to read or write data sequentially, piece by piece (in chunks), rather than loading the entire data into memory at once. Streams implement the `EventEmitter` interface, making them event-driven and easy to use.

## Why Do We Need It?

Streams solve critical problems with traditional data handling:

1. **Memory Efficiency**: Process large files without loading them entirely into memory

2. **Time Efficiency: Start processing data before the entire payload arrives

3. **Composability: Pipe streams together for complex data transformations

4. **Backpressure**: Handle scenarios where data is produced faster than consumed

Without streams, processing a 1GB file would require 1GB+ of memory. With streams, you can process it with just a few KB of memory.

## How It Works

### The Four Stream Types

```text
┌───────────────────────────────────────────────────────────────┐
│                      STREAM TYPES                             │
├───────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐                                             │
│  │  Readable   │  Produces data (source)                     │
│  │  Stream     │  Example: fs.createReadStream()             │
│  └──────┬──────┘                                             │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────┐                                             │
│  │ Transform   │  Modifies data (optional)                   │
│  │  Stream     │  Example: zlib.createGzip()                 │
│  └──────┬──────┘                                             │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────┐                                             │
│  │  Writable   │  Consumes data (destination)                │
│  │  Stream     │  Example: fs.createWriteStream()            │
│  └─────────────┘                                             │
│                                                              │
│  ┌─────────────┐                                             │
│  │  Duplex     │  Both Readable and Writable                 │
│  │  Stream     │  Example: net.Socket                        │
│  └─────────────┘                                             │
│                                                              │
└───────────────────────────────────────────────────────────────┘

```

### Stream Flow Diagram

```text
┌───────────────────────────────────────────────────────────────┐
│                    STREAM PIPE FLOW                          │
├───────────────────────────────────────────────────────────────┤
│                                                              │
│  Readable Stream                                             │
│  ┌─────────────────────────────────────────┐                │
│  │  [Chunk1] [Chunk2] [Chunk3] ... [End]  │                │
│  └─────────────────┬───────────────────────┘                │
│                    │                                         │
│                    ▼                                         │
│              .pipe() method                                  │
│                    │                                         │
│                    ▼                                         │
│  Transform Stream (optional)                                 │
│  ┌─────────────────────────────────────────┐                │
│  │  Input → [Process] → Output            │                │
│  └─────────────────┬───────────────────────┘                │
│                    │                                         │
│                    ▼                                         │
│  Writable Stream                                             │
│  ┌─────────────────────────────────────────┐                │
│  │  Write → Buffer → Flush → Done         │                │
│  └─────────────────────────────────────────┘                │
│                                                              │
└───────────────────────────────────────────────────────────────┘

```

### Backpressure Mechanism

```text
┌───────────────────────────────────────────────────────────────┐
│                    BACKPRESSURE FLOW                         │
├───────────────────────────────────────────────────────────────┤
│                                                              │
│  Producer (fast) ──────────> Consumer (slow)                │
│                                                              │
│  1. Producer emits chunks faster than consumer processes     │
│  2. Consumer's buffer fills up (highWaterMark reached)      │
│  3. Producer's write() returns false                        │
│  4. Producer pauses (emits 'pause' event)                   │
│  5. Consumer processes buffered data                        │
│  6. Consumer's buffer drains below threshold                │
│  7. Consumer emits 'drain' event                            │
│  8. Producer resumes (emits 'resume' event)                 │
│                                                              │
│  ┌─────────┐    writes     ┌─────────┐    processes        │
│  │ Producer ├──────────────>│Consumer │                     │
│  │         │               │         │                      │
│  │  pause()│<───────drain──┤         │                      │
│  └─────────┘               └─────────┘                      │
│                                                              │
└───────────────────────────────────────────────────────────────┘

```

### highWaterMark and Buffer Management

```text
┌───────────────────────────────────────────────────────────────┐
│              highWaterMark Buffer States                     │
├───────────────────────────────────────────────────────────────┤
│                                                              │
│  Writable Stream Buffer:                                     │
│  ┌──────────────────────────────────────────────────┐       │
│  │████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│       │
│  └──────────────────────────────────────────────────┘       │
│  ▲                    ▲                                      │
│  │                    └── highWaterMark (16KB default)      │
│  └── Current buffer level                                   │
│                                                              │
│  When buffer < highWaterMark: write() returns true          │
│  When buffer >= highWaterMark: write() returns false        │
│                                                              │
│  Readable Stream Buffer:                                     │
│  ┌──────────────────────────────────────────────────┐       │
│  │████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│       │
│  └──────────────────────────────────────────────────┘       │
│  ▲            ▲                                              │
│  │            └── highWaterMark                              │
│  └── Current buffer level                                   │
│                                                              │
│  When buffer < highWaterMark: read() returns null           │
│  When buffer >= highWaterMark: flow() pauses                │
│                                                              │
└───────────────────────────────────────────────────────────────┘

```

## Code Examples

### Basic Readable Stream

```typescript
// readable-stream.ts

import * as fs from 'fs';
import { Readable } from 'stream';

// Method 1: Using fs.createReadStream
const fileStream = fs.createReadStream('./large-file.txt', {
  encoding: 'utf8',
  highWaterMark: 1024, // 1KB chunks
});

// Method 2: Creating custom readable stream
class NumberStream extends Readable {
  private current = 0;
  private max: number;

  constructor(max: number) {
    super({ objectMode: true });
    this.max = max;
  }

  _read(size: number): void {
    if (this.current <= this.max) {
      this.push(this.current++);
    } else {
      this.push(null); // Signal end of stream
    }
  }
}

// Using readable stream
const numberStream = new NumberStream(10);

numberStream.on('data', (chunk) => {
  console.log('Received:', chunk);
});

numberStream.on('end', () => {
  console.log('Stream finished');
});

numberStream.on('error', (err) => {
  console.error('Error:', err);
});

// Manual read
numberStream.on('readable', () => {
  let chunk;
  while ((chunk = numberStream.read()) !== null) {
    console.log('Read:', chunk);
  }
});

```

### Basic Writable Stream

```typescript
// writable-stream.ts

import * as fs from 'fs';
import { Writable } from 'stream';

// Method 1: Using fs.createWriteStream
const writeStream = fs.createWriteStream('./output.txt', {
  encoding: 'utf8',
  highWaterMark: 16 * 1024, // 16KB buffer
});

// Method 2: Creating custom writable stream
class ConsoleWriter extends Writable {
  _write(
    chunk: any,
    encoding: BufferEncoding,
    callback: (error?: Error | null) => void
  ): void {
    console.log('Written:', chunk.toString());
    callback();
  }
}

// Using writable stream
const consoleWriter = new ConsoleWriter();

// Write data
consoleWriter.write('Hello, ');
consoleWriter.write('World!\n');

// Signal end
consoleWriter.end('Goodbye!\n');

consoleWriter.on('finish', () => {
  console.log('All data flushed');
});

// Handle write errors
writeStream.on('error', (err) => {
  console.error('Write error:', err);
});

```

### Transform Stream

```typescript
// transform-stream.ts

import { Transform, TransformCallback } from 'stream';

// Method 1: Using built-in transforms
import { createGzip, createGunzip } from 'zlib';

// Method 2: Custom transform stream
class UpperCaseTransform extends Transform {
  constructor() {
    super({ readableObjectMode: true, writableObjectMode: true });
  }

  _transform(
    chunk: any,
    encoding: BufferEncoding,
    callback: TransformCallback
  ): void {
    // Transform the data
    const transformed = chunk.toString().toUpperCase();
    this.push(transformed);
    callback();
  }

  _flush(callback: TransformCallback): void {
    // Called when stream ends - cleanup or final transform
    callback();
  }
}

// Usage
const upperCaseStream = new UpperCaseTransform();

process.stdin
  .pipe(upperCaseStream)
  .pipe(process.stdout);

// Chaining transforms
import { createCipheriv, createDecipheriv, randomBytes } from 'crypto';

const algorithm = 'aes-256-cbc';
const key = randomBytes(32);
const iv = randomBytes(16);

class EncryptTransform extends Transform {
  private cipher = createCipheriv(algorithm, key, iv);

  _transform(
    chunk: any,
    encoding: BufferEncoding,
    callback: TransformCallback
  ): void {
    const encrypted = this.cipher.update(chunk);
    this.push(encrypted);
    callback();
  }

  _flush(callback: TransformCallback): void {
    this.push(this.cipher.final());
    callback();
  }
}

```

### Duplex Stream

```typescript
// duplex-stream.ts

import { Duplex } from 'stream';
import * as net from 'net';

// Custom duplex stream
class EchoStream extends Duplex {
  private buffer: Buffer[] = [];

  constructor() {
    super({ readableObjectMode: true, writableObjectMode: true });
  }

  _write(
    chunk: any,
    encoding: BufferEncoding,
    callback: (error?: Error | null) => void
  ): void {
    console.log('Echoing:', chunk.toString());
    this.buffer.push(chunk);
    callback();
  }

  _read(size: number): void {
    if (this.buffer.length > 0) {
      this.push(this.buffer.shift());
    }
  }

  _final(callback: (error?: Error | null) => void): void {
    // Called when write end is finished
    callback();
  }
}

// Using net.Socket (built-in duplex)
const server = net.createServer((socket) => {
  // socket is a duplex stream
  socket.on('data', (data) => {
    socket.write(`Echo: ${data}`);
  });
});

```

### Piping and Error Handling

```typescript
// pipe-error-handling.ts

import * as fs from 'fs';
import { createGzip, createGunzip } from 'zlib';
import { pipeline, Transform } from 'stream';
import { promisify } from 'util';

const pipelineAsync = promisify(pipeline);

// Method 1: Using .pipe() with error handling
const readStream = fs.createReadStream('input.txt');
const gzipStream = createGzip();
const writeStream = fs.createWriteStream('output.txt.gz');

readStream
  .on('error', (err) => console.error('Read error:', err))
  .pipe(gzipStream)
  .on('error', (err) => console.error('Gzip error:', err))
  .pipe(writeStream)
  .on('error', (err) => console.error('Write error:', err))
  .on('finish', () => console.log('Compression complete'));

// Method 2: Using pipeline (recommended - handles errors automatically)
async function compressFile(input: string, output: string) {
  try {
    await pipelineAsync(
      fs.createReadStream(input),
      createGzip(),
      fs.createWriteStream(output)
    );
    console.log('Compression complete');
  } catch (err) {
    console.error('Pipeline failed:', err);
  }
}

// Method 3: Custom transform with error handling
class StrictTransform extends Transform {
  _transform(
    chunk: any,
    encoding: BufferEncoding,
    callback: TransformCallback
  ): void {
    try {
      const data = JSON.parse(chunk.toString());

      if (!data.id) {
        // Emit error instead of throwing
        this.destroy(new Error('Missing id field'));
        return;
      }

      this.push(JSON.stringify(data));
      callback();
    } catch (err) {
      callback(err as Error);
    }
  }
}

```

### Backpressure Handling

```typescript
// backpressure-handling.ts

import * as fs from 'fs';
import { Readable, Writable, Transform, TransformCallback } from 'stream';

// Manual backpressure handling
class SlowProcessor extends Transform {
  private processing = false;

  _transform(
    chunk: any,
    encoding: BufferEncoding,
    callback: TransformCallback
  ): void {
    this.processing = true;

    // Simulate slow processing
    setTimeout(() => {
      this.push(chunk.toString().toUpperCase());
      this.processing = false;
      callback();
    }, 100);
  }
}

async function processWithBackpressure() {
  const readStream = fs.createReadStream('large-file.txt', {
    encoding: 'utf8',
  });
  const transformStream = new SlowProcessor();
  const writeStream = fs.createWriteStream('output.txt');

  // Manual backpressure handling
  readStream.on('data', (chunk) => {
    const canContinue = transformStream.write(chunk);

    if (!canContinue) {
      // Backpressure: pause readable
      readStream.pause();

      // Resume when transform buffer drains
      transformStream.once('drain', () => {
        readStream.resume();
      });
    }
  });

  readStream.on('end', () => {
    transformStream.end();
  });

  transformStream.on('data', (chunk) => {
    const canContinue = writeStream.write(chunk);

    if (!canContinue) {
      // Backpressure: pause transform
      transformStream.pause();

      writeStream.once('drain', () => {
        transformStream.resume();
      });
    }
  });

  transformStream.on('end', () => {
    writeStream.end();
  });

  writeStream.on('finish', () => {
    console.log('Processing complete');
  });
}

```

### Object Streams

```typescript
// object-streams.ts

import { Transform, TransformCallback } from 'stream';

// Object mode streams
class JSONParser extends Transform {
  constructor() {
    super({ objectMode: true });
  }

  _transform(
    chunk: any,
    encoding: BufferEncoding,
    callback: TransformCallback
  ): void {
    try {
      const obj = JSON.parse(chunk.toString());
      this.push(obj);
      callback();
    } catch (err) {
      callback(err as Error);
    }
  }
}

class FilterTransform extends Transform {
  private filterFn: (obj: any) => boolean;

  constructor(filterFn: (obj: any) => boolean) {
    super({ objectMode: true });
    this.filterFn = filterFn;
  }

  _transform(
    chunk: any,
    encoding: BufferEncoding,
    callback: TransformCallback
  ): void {
    if (this.filterFn(chunk)) {
      this.push(chunk);
    }
    callback();
  }
}

// Usage
import { Readable } from 'stream';

const dataArray = [
  JSON.stringify({ id: 1, name: 'Alice' }),
  JSON.stringify({ id: 2, name: 'Bob' }),
  JSON.stringify({ id: 3, name: 'Charlie' }),
];

const readable = Readable.from(dataArray);

readable
  .pipe(new JSONParser())
  .pipe(new FilterTransform((obj) => obj.id > 1))
  .on('data', (obj) => {
    console.log('Filtered:', obj);
  });

```

### Stream Utilities

```typescript
// stream-utils.ts

import { Readable, Transform, TransformCallback, pipeline } from 'stream';
import { promisify } from 'util';

const pipelineAsync = promisify(pipeline);

// Utility: Collect all data from readable stream
async function collectStream(readable: Readable): Promise<any[]> {
  const chunks: any[] = [];

  for await (const chunk of readable) {
    chunks.push(chunk);
  }

  return chunks;
}

// Utility: Convert async iterable to readable stream
function asyncIterableToStream<T>(iterable: AsyncIterable<T>): Readable {
  return new Readable({
    objectMode: true,
    async read() {
      try {
        const { value, done } = await iterable[Symbol.asyncIterator]().next();
        if (done) {
          this.push(null);
        } else {
          this.push(value);
        }
      } catch (err) {
        this.destroy(err as Error);
      }
    },
  });
}

// Utility: Debounce stream events
class DebounceTransform extends Transform {
  private timeout: NodeJS.Timeout | null = null;
  private delay: number;

  constructor(delay: number) {
    super({ objectMode: true });
    this.delay = delay;
  }

  _transform(
    chunk: any,
    encoding: BufferEncoding,
    callback: TransformCallback
  ): void {
    if (this.timeout) {
      clearTimeout(this.timeout);
    }

    this.timeout = setTimeout(() => {
      this.push(chunk);
      callback();
    }, this.delay);
  }

  _flush(callback: TransformCallback): void {
    if (this.timeout) {
      clearTimeout(this.timeout);
    }
    callback();
  }
}

// Utility: Throttle stream
class ThrottleTransform extends Transform {
  private lastTime = 0;
  private interval: number;

  constructor(interval: number) {
    super({ objectMode: true });
    this.interval = interval;
  }

  _transform(
    chunk: any,
    encoding: BufferEncoding,
    callback: TransformCallback
  ): void {
    const now = Date.now();
    const elapsed = now - this.lastTime;

    if (elapsed < this.interval) {
      setTimeout(() => {
        this.push(chunk);
        this.lastTime = Date.now();
        callback();
      }, this.interval - elapsed);
    } else {
      this.push(chunk);
      this.lastTime = now;
      callback();
    }
  }
}

```

## Real-World Use Cases

### 1. File Compression Pipeline

```typescript
// compress-pipeline.ts

import * as fs from 'fs';
import { createGzip, createBrotliCompress } from 'zlib';
import { pipeline, Transform, TransformCallback } from 'stream';
import { promisify } from 'util';

const pipelineAsync = promisify(pipeline);

class ProgressTracker extends Transform {
  private total = 0;
  private processed = 0;

  constructor() {
    super();
  }

  _transform(
    chunk: any,
    encoding: BufferEncoding,
    callback: TransformCallback
  ): void {
    this.total += chunk.length;
    this.processed += chunk.length;

    const progress = ((this.processed / this.total) * 100).toFixed(2);
    process.stdout.write(`\rProgress: ${progress}%`);

    this.push(chunk);
    callback();
  }
}

async function compressDirectory(inputDir: string, outputDir: string) {
  const files = fs.readdirSync(inputDir);

  for (const file of files) {
    const inputPath = `${inputDir}/${file}`;
    const outputPath = `${outputDir}/${file}.gz`;

    try {
      await pipelineAsync(
        fs.createReadStream(inputPath),
        new ProgressTracker(),
        createGzip({ level: 9 }),
        fs.createWriteStream(outputPath)
      );
      console.log(`\nCompressed: ${file}`);
    } catch (err) {
      console.error(`Failed to compress ${file}:`, err);
    }
  }
}

```

### 2. Real-time Data Processing

```typescript
// real-time-processing.ts

import * as net from 'net';
import { Transform, TransformCallback, Writable } from 'stream';

class DataParser extends Transform {
  private buffer = '';

  constructor() {
    super({ objectMode: true });
  }

  _transform(
    chunk: any,
    encoding: BufferEncoding,
    callback: TransformCallback
  ): void {
    this.buffer += chunk.toString();
    const lines = this.buffer.split('\n');
    this.buffer = lines.pop() || '';

    for (const line of lines) {
      try {
        const data = JSON.parse(line);
        this.push(data);
      } catch {
        // Skip invalid JSON
      }
    }

    callback();
  }
}

class Aggregator extends Writable {
  private metrics: Map<string, number> = new Map();

  _write(
    chunk: any,
    encoding: BufferEncoding,
    callback: (error?: Error | null) => void
  ): void {
    const { metric, value } = chunk;
    const current = this.metrics.get(metric) || 0;
    this.metrics.set(metric, current + value);
    callback();
  }

  _final(callback: (error?: Error | null) => void): void {
    console.log('Aggregated metrics:', Object.fromEntries(this.metrics));
    callback();
  }
}

// TCP server with stream processing
const server = net.createServer((socket) => {
  socket
    .pipe(new DataParser())
    .pipe(new Aggregator());
});

```

### 3. Image Processing Pipeline

```typescript
// image-processing.ts

import { Transform, TransformCallback } from 'stream';
import sharp from 'sharp';

class ImageResizer extends Transform {
  private width: number;
  private height: number;

  constructor(width: number, height: number) {
    super();
    this.width = width;
    this.height = height;
  }

  _transform(
    chunk: any,
    encoding: BufferEncoding,
    callback: TransformCallback
  ): void {
    sharp(chunk)
      .resize(this.width, this.height)
      .toBuffer()
      .then((resized) => {
        this.push(resized);
        callback();
      })
      .catch((err) => {
        callback(err);
      });
  }
}

class ImageOptimizer extends Transform {
  private quality: number;

  constructor(quality: number = 80) {
    super();
    this.quality = quality;
  }

  _transform(
    chunk: any,
    encoding: BufferEncoding,
    callback: TransformCallback
  ): void {
    sharp(chunk)
      .jpeg({ quality: this.quality })
      .toBuffer()
      .then((optimized) => {
        this.push(optimized);
        callback();
      })
      .catch((err) => {
        callback(err);
      });
  }
}

// Usage
const processImages = async (inputPaths: string[], outputDir: string) => {
  const { pipeline } = require('stream');
  const { promisify } = require('util');
  const fs = require('fs');
  const pipelineAsync = promisify(pipeline);

  for (const inputPath of inputPaths) {
    const outputPath = `${outputDir}/${inputPath.split('/').pop()}`;

    await pipelineAsync(
      fs.createReadStream(inputPath),
      new ImageResizer(800, 600),
      new ImageOptimizer(85),
      fs.createWriteStream(outputPath)
    );
  }
};

```

## Common Mistakes

### 1. Not Handling Stream Errors

```typescript
// BAD: Missing error handler
const readStream = fs.createReadStream('file.txt');
const writeStream = fs.createWriteStream('output.txt');
readStream.pipe(writeStream);

// GOOD: Always handle errors
const readStream = fs.createReadStream('file.txt');
const writeStream = fs.createWriteStream('output.txt');
readStream
  .on('error', (err) => console.error('Read error:', err))
  .pipe(writeStream)
  .on('error', (err) => console.error('Write error:', err));

```

### 2. Not Properly Handling Backpressure

```typescript
// BAD: Ignoring backpressure
readStream.on('data', (chunk) => {
  writeStream.write(chunk); // May cause memory issues
});

// GOOD: Handle backpressure
readStream.on('data', (chunk) => {
  const canContinue = writeStream.write(chunk);
  if (!canContinue) {
    readStream.pause();
    writeStream.once('drain', () => readStream.resume());
  }
});

```

### 3. Using .pipe() Without Error Handling

```typescript
// BAD: .pipe() doesn't propagate errors
readStream.pipe(transform).pipe(writeStream);

// GOOD: Use pipeline() for automatic error handling
import { pipeline } from 'stream';
import { promisify } from 'util';

const pipelineAsync = promisify(pipeline);
await pipelineAsync(readStream, transform, writeStream);

```

### 4. Not Destroying Streams

```typescript
// BAD: Streams may leak resources
const stream = fs.createReadStream('file.txt');
// Never closes on error

// GOOD: Handle cleanup
const stream = fs.createReadStream('file.txt');
stream.on('error', () => stream.destroy());
// Or use try/finally
try {
  await processStream(stream);
} finally {
  stream.destroy();
}

```

### 5. Mixing Object and Buffer Modes

```typescript
// BAD: Mixing modes without conversion
const readable = new Readable({ objectMode: true });
readable.push({ data: 'test' });
readable.pipe(process.stdout); // Will fail

// GOOD: Use proper transform
readable.pipe(new Transform({
  transform(chunk, encoding, callback) {
    this.push(JSON.stringify(chunk));
    callback();
  }
})).pipe(process.stdout);

```

## Best Practices

### 1. Always Use pipeline() for Safety

```typescript
import { pipeline } from 'stream';
import { promisify } from 'util';

const pipelineAsync = promisify(pipeline);

// Automatic error handling and cleanup
await pipelineAsync(
  source,
  transform1,
  transform2,
  destination
);

```

### 2. Implement Proper Error Handling

```typescript
class SafeTransform extends Transform {
  _transform(chunk, encoding, callback) {
    try {
      // Process data
      const result = processChunk(chunk);
      this.push(result);
      callback();
    } catch (err) {
      // Use callback with error instead of throwing
      callback(err);
    }
  }

  _flush(callback) {
    // Handle remaining buffered data
    try {
      if (this.buffer.length > 0) {
        this.push(this.processBuffer());
      }
      callback();
    } catch (err) {
      callback(err);
    }
  }
}

```

### 3. Use Object Mode When Appropriate

```typescript
// For structured data, use objectMode
const jsonParser = new Transform({
  objectMode: true,
  transform(chunk, encoding, callback) {
    try {
      const obj = JSON.parse(chunk.toString());
      this.push(obj);
      callback();
    } catch (err) {
      callback(err);
    }
  }
});

```

### 4. Implement Backpressure Properly

```typescript
function createThrottledWriter(writeFn: (chunk: any) => boolean) {
  let waiting = false;

  return new Writable({
    write(chunk, encoding, callback) {
      const canContinue = writeFn(chunk);

      if (!canContinue && !waiting) {
        waiting = true;
        this.once('drain', () => {
          waiting = false;
          callback();
        });
      } else {
        callback();
      }
    },
  });
}

```

### 5. Monitor Stream Performance

```typescript
class MonitoredTransform extends Transform {
  private startTime = Date.now();
  private bytesProcessed = 0;

  _transform(chunk, encoding, callback) {
    this.bytesProcessed += chunk.length;

    // Log progress periodically
    if (this.bytesProcessed % (1024 * 1024) === 0) {
      const elapsed = Date.now() - this.startTime;
      const throughput = (this.bytesProcessed / elapsed) * 1000;
      console.log(`Processed: ${this.bytesProcessed} bytes, ${throughput} bytes/sec`);
    }

    this.push(chunk);
    callback();
  }

  _flush(callback) {
    const elapsed = Date.now() - this.startTime;
    const throughput = (this.bytesProcessed / elapsed) * 1000;
    console.log(`Final: ${this.bytesProcessed} bytes in ${elapsed}ms, ${throughput} bytes/sec`);
    callback();
  }
}

```

## Performance Considerations

### 1. Buffer Size Optimization

```typescript
// Larger buffers = fewer syscalls = better throughput
const readStream = fs.createReadStream('file.txt', {
  highWaterMark: 64 * 1024, // 64KB chunks
});

// Smaller buffers = lower memory usage
const readStream = fs.createReadStream('file.txt', {
  highWaterMark: 1024, // 1KB chunks
});

```

### 2. Concurrency Control

```typescript
import { Pool } from 'generic-pool';

const pool = Pool({
  create: () => createWorker(),
  destroy: (worker) => worker.close(),
  max: 10,
});

async function processFiles(filePaths: string[]) {
  const results = await Promise.all(
    filePaths.map(async (filePath) => {
      const worker = await pool.acquire();
      try {
        return await processFile(worker, filePath);
      } finally {
        pool.release(worker);
      }
    })
  );
  return results;
}

```

### 3. Memory Leak Prevention

```typescript
// BAD: Accumulating data in memory
class BadTransform extends Transform {
  private allData: any[] = [];

  _transform(chunk, encoding, callback) {
    this.allData.push(chunk); // Memory leak!
    this.push(chunk);
    callback();
  }
}

// GOOD: Process and discard
class GoodTransform extends Transform {
  _transform(chunk, encoding, callback) {
    const result = processChunk(chunk);
    this.push(result);
    callback();
  }
}

```

## Summary

Streams are essential for processing large data efficiently in Node.js. Key takeaways:

- Four stream types: Readable, Writable, Duplex, Transform
- Always handle errors and use pipeline() for safety
- Understand backpressure and implement proper flow control
- Object mode is convenient but has performance implications
- Monitor stream performance and memory usage in production

## Cheat Sheet
```text
┌───────────────────────────────────────────────────────────────┐
│                    STREAMS CHEAT SHEET                       │
├───────────────────────────────────────────────────────────────┤
│                                                              │
│  STREAM TYPES:                                               │
│  • Readable: fs.createReadStream(), process.stdin            │
│  • Writable: fs.createWriteStream(), process.stdout          │
│  • Duplex: net.Socket                                        │
│  • Transform: zlib.createGzip(), crypto.createCipher         │
│                                                              │
│  KEY METHODS:                                                │
│  • pipe(destination): Connect streams                        │
│  • write(chunk): Write data                                  │
│  • end(): Close writable                                     │
│  • destroy(): Clean up stream                                │
│  • pause()/resume(): Flow control                            │
│                                                              │
│  EVENTS:                                                     │
│  • 'data': Chunk available (readable)                        │
│  • 'end': No more data (readable)                            │
│  • 'finish': All data flushed (writable)                     │
│  • 'drain': Buffer below highWaterMark (writable)            │
│  • 'error': Error occurred                                   │
│  • 'close': Stream closed                                    │
│                                                              │
│  BEST PRACTICES:                                             │
│  • Use pipeline() instead of pipe()                          │
│  • Always handle 'error' events                              │
│  • Implement backpressure handling                           │
│  • Use objectMode for structured data                        │
│  • Monitor memory usage                                      │
│                                                              │
│  COMMON PITFALLS:                                            │
│  • Not handling errors                                       │
│  • Ignoring backpressure                                     │
│  • Mixing object and buffer modes                            │
│  • Not destroying streams                                    │
│                                                              │
│  PERFORMANCE:                                                │
│  • Tune highWaterMark for your use case                      │
│  • Use parallel processing where possible                    │
│  • Implement connection pooling                              │
│  • Monitor GC impact                                         │
│                                                              │
└───────────────────────────────────────────────────────────────┘

```

---

## See Also
- [Docker](../13-Docker/)
- [JavaScript](../01-JavaScript/)
- [NestJS](../06-NestJS/)

## References & Learn More

- [Node.js Streams Docs](https://nodejs.org/api/stream.html)
- [The Stream Handbook by Substack](https://github.com/substack/stream-handbook)
- [Node.js Stream冒险游戏](https://github.com/substack/stream-adventure)
- [Stream Consumption Patterns](https://nodejs.org/en/learn/asynchronous-work/streams)
