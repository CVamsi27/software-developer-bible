# Node.js Streams

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

```
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

```
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

```
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

```
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

## Interview Questions

### Beginner

1. **What are streams in Node.js?**
   - Streams are objects that allow reading or writing data sequentially in chunks, rather than loading the entire data into memory at once.

2. **Name the four types of streams.**
   - Readable, Writable, Duplex (both), and Transform (modify data).

3. **What is the difference between readable and writable streams?**
   - Readable streams produce data (sources), while writable streams consume data (destinations).

4. **What is piping in streams?**
   - Piping connects a readable stream to a writable stream, automatically managing data flow between them using `.pipe()`.

5. **What is backpressure?**
   - Backpressure occurs when a writable stream can't keep up with a readable stream's data production rate. It's handled by pausing the readable stream.

6. **What is highWaterMark?**
   - A threshold that determines when a stream should apply backpressure. Default is 16KB for buffers, 16 for object mode.

7. **How do you handle errors in streams?**
   - Use `.on('error', handler)` or use `pipeline()` for automatic error propagation.

8. **What is objectMode in streams?**
   - A stream configuration that allows processing JavaScript objects instead of Buffers or strings.

9. **What is the difference between .pipe() and pipeline()?**
   - `.pipe()` doesn't handle errors, while `pipeline()` provides automatic error handling and cleanup.

10. **When should you use streams?**
    - When processing large files, real-time data, or when memory efficiency is critical.

### Intermediate

11. **How does a Transform stream work?**
    - Transform streams receive input data, modify it, and produce output. They implement both Readable and Writable interfaces.

12. **What is the _flush method in Transform streams?**
    - Called when there's no more data to process, allowing cleanup or flushing of buffered data.

13. **How do you implement custom backpressure handling?**
    - Check the return value of `write()`, pause the readable stream when false, and resume on 'drain' event.

14. **What is a highWaterMark in object mode?**
    - The number of objects that can be buffered before backpressure is applied (default 16).

15. **How do streams handle errors differently from other Node.js code?**
    - Streams emit 'error' events instead of throwing exceptions. You must listen for these events.

16. **What is the purpose of the 'finish' event?**
    - Emitted when all data has been flushed to the underlying system.

17. **How do you create a readable stream from an array?**
    - Use `Readable.from(array)` or implement a custom Readable with `_read()`.

18. **What is the difference between push(null) and end()?**
    - `push(null)` signals end of readable data, while `end()` signals end of writable data.

19. **How do you handle multiple pipes?**
    - Chain pipes: `a.pipe(b).pipe(c).pipe(d)`. Handle errors at each stage.

20. **What is the 'drain' event?**
    - Emitted when a writable stream's buffer falls below highWaterMark after being full.

### Senior

21. **How would you design a streaming ETL pipeline?**
    - Use Transform streams for each ETL stage, implement error boundaries, add monitoring, and handle backpressure throughout.

22. **Explain memory management in long-running stream processing.**
    - Monitor heap usage, implement stream cleanup, avoid accumulating data, and use object pooling for transforms.

23. **How would you implement a distributed stream processing system?**
    - Use message queues (Kafka/RabbitMQ), implement checkpointing, handle reconnection, and ensure exactly-once processing.

24. **How do you debug stream issues in production?**
    - Use stream events for monitoring, implement custom metrics, log stream states, and use APM tools.

25. **What are the performance implications of object vs buffer mode?**
    - Object mode has higher overhead due to serialization, while buffer mode is more efficient for binary data.

26. **How would you implement rate limiting in streams?**
    - Use Transform streams with timing logic, implement token buckets, or use external rate limiters.

27. **Explain how to handle stream errors in microservices.**
    - Implement circuit breakers, add retry logic, use dead letter queues, and propagate errors via events.

28. **How do you optimize stream performance for high throughput?**
    - Tune highWaterMark, use parallel processing, implement connection pooling, and optimize chunk sizes.

29. **What is the impact of V8 garbage collection on streams?**
    - Large buffers can trigger major GCs. Optimize by using smaller chunks and releasing references.

30. **How would you implement a streaming API for real-time analytics?**
    - Use Server-Sent Events or WebSocket with Transform streams for aggregation and filtering.

### FAANG-style

31. **Design a streaming data pipeline processing 1M events/second.**
    - Use partitioned streams, implement backpressure handling, use shared-nothing architecture, and add monitoring.

32. **How would you implement exactly-once stream processing?**
    - Use idempotent operations, implement checkpointing, use transactional messaging, and add deduplication.

33. **Design a stream processing system with fault tolerance.**
    - Implement checkpointing, use replication, add automatic recovery, and implement dead letter queues.

34. **How would you handle schema evolution in streaming systems?**
    - Use schema registries, implement backward/forward compatibility, and version your data formats.

35. **Design a real-time fraud detection system using streams.**
    - Use windowed aggregations, implement complex event processing, add ML model inference, and handle late-arriving data.

36. **How would you implement stream processing with exactly-once semantics?**
    - Use transactional outbox pattern, implement idempotent consumers, and use distributed transactions.

37. **Design a streaming system for IoT data processing.**
    - Handle high cardianality, implement time-window aggregations, use edge processing, and add data validation.

38. **How would you optimize stream processing for cost efficiency?**
    - Use auto-scaling, implement batch processing, optimize serialization, and use spot instances.

39. **Design a multi-region streaming architecture.**
    - Implement cross-region replication, handle conflict resolution, optimize for latency, and add failover.

40. **How would you implement stream processing with ML model integration?**
    - Use feature stores, implement online inference, handle model versioning, and add A/B testing.

### Follow-ups

41. **What happens when a stream's buffer is full?**
    - The stream applies backpressure, pausing the source and emitting 'pause' event.

42. **How do you handle stream errors in async/await?**
    - Use promisified pipeline or wrap in try/catch with stream events.

43. **What is the difference between readable.pipe() and readable.pipe()?**
    - `pipe()` returns the destination stream, allowing chaining. Both handle backpressure.

44. **How do you implement custom stream classes?**
    - Extend Stream class, implement `_read()`, `_write()`, or `_transform()` methods.

45. **What is the 'close' event in streams?**
    - Emitted when the stream and any of its underlying resources have been closed.

46. **How do you handle stream cleanup?**
    - Use 'close' event, implement _destroy() method, and use pipeline() for automatic cleanup.

47. **What is the impact of encoding on stream performance?**
    - Encoding affects buffer size and processing speed. UTF-8 is common but has overhead for binary data.

48. **How do you implement stream retry logic?**
    - Track failed chunks, implement exponential backoff, and use dead letter queues.

49. **What is the difference between stream modes?**
    - Streams can be in flowing mode (auto-reading), paused mode (manual reading), or object mode.

50. **How do you monitor stream health in production?**
    - Track throughput, latency, error rates, and backpressure events using custom metrics.

## Summary

Streams are essential for processing large data efficiently in Node.js. Key takeaways:

- Four stream types: Readable, Writable, Duplex, Transform
- Always handle errors and use pipeline() for safety
- Understand backpressure and implement proper flow control
- Object mode is convenient but has performance implications
- Monitor stream performance and memory usage in production

## Cheat Sheet

```
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

## References & Learn More

- [Node.js Streams Docs](https://nodejs.org/api/stream.html)
- [The Stream Handbook by Substack](https://github.com/substack/stream-handbook)
- [Node.js Stream冒险游戏](https://github.com/substack/stream-adventure)
- [Stream Consumption Patterns](https://nodejs.org/en/learn/asynchronous-work/continuous-processing-of-readable-streams)