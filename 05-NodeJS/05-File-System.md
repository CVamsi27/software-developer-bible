---
section: Node.js
category: Backend
tags: [concept]
---

# File System (fs)

The Node.js `fs` module provides an API for interacting with the file system, enabling file read/write, directory operations, file metadata inspection, and file watching. It offers three API styles: promise-based (`fs.promises`), callback-based, and synchronous.

## Definition

The `fs` module is a built-in Node.js module for file system operations. It supports:

- **File operations**: read, write, append, truncate, rename, copy, delete
- **Directory operations**: create, read, delete, traverse
- **File metadata**: stats, permissions, ownership, timestamps
- **Watching**: file and directory change monitoring
- **Stream I/O**: efficient large file processing via streams
- **File descriptors**: low-level POSIX file operations

## Why Do We Need It?

1. **Persistence**: Read/write configuration, logs, and application data

2. **Asset management**: Serve static files, process uploads, manage builds

3. **Data processing**: Parse CSV/JSON/XML files, transform data in chunks

4. **Logging**: Append to log files, rotate logs, create error archives

5. **Module system**: Node.js itself uses `fs` to load modules from disk

6. **CLI tools**: Build command-line tools that read/write files and directories

## How It Works

### API Styles

```text
fs module API styles:
═══════════════════════════════════════

Promise-based (fs.promises):
  const fs = require('fs/promises');
  const data = await fs.readFile('file.txt', 'utf8');

Callback-based:
  const fs = require('fs');
  fs.readFile('file.txt', 'utf8', (err, data) => {
    if (err) throw err;
    console.log(data);
  });

Synchronous:
  const fs = require('fs');
  const data = fs.readFileSync('file.txt', 'utf8');
```

### File Descriptor Lifecycle

```text
┌─────────────────────────────────────────────────────────────┐
│                  FILE DESCRIPTOR LIFECYCLE                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  fs.open(path, flags, mode)                                  │
│       │                                                     │
│       ▼                                                     │
│  File Descriptor (integer, process-scoped)                  │
│       │                                                     │
│  fs.read(fd, buffer, offset, length, position)              │
│  fs.write(fd, buffer/data)                                   │
│       │                                                     │
│       ▼                                                     │
│  fs.close(fd) — MUST close!                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples (Node.js)

### Reading Files

```javascript
// Promise-based (recommended)
const fs = require('fs/promises');

async function readFile() {
  try {
    // Read entire file
    const data = await fs.readFile('config.json', 'utf8');
    console.log(JSON.parse(data));

    // Partial read with buffer
    const buffer = Buffer.alloc(100);
    const fd = await fs.open('large.txt', 'r');
    const { bytesRead } = await fd.read(buffer, 0, 100, 0);
    console.log(buffer.toString('utf8', 0, bytesRead));
    await fd.close();
  } catch (err) {
    console.error('File read error:', err.message);
  }
}

// Callback-based
const fsCallback = require('fs');
fsCallback.readFile('data.json', 'utf8', (err, data) => {
  if (err) return console.error(err);
  console.log(JSON.parse(data));
});

// Synchronous (blocking — avoid in production)
try {
  const data = fsCallback.readFileSync('config.json', 'utf8');
  console.log(data);
} catch (err) {
  console.error(err);
}
```

### Writing Files

```javascript
// Promise-based
const fs = require('fs/promises');

async function writeFiles() {
  // Write (overwrites)
  await fs.writeFile('output.txt', 'Hello, World!', 'utf8');

  // Append
  await fs.appendFile('output.txt', '\nNew line', 'utf8');

  // Write with buffer
  const buffer = Buffer.from('Binary data');
  await fs.writeFile('binary.bin', buffer);

  // Atomic write (write to temp, then rename)
  await fs.writeFile('output.tmp', 'Content');
  await fs.rename('output.tmp', 'output.txt');
}

// Stream-based writing for large data
const fsStream = require('fs');
const writeStream = fsStream.createWriteStream('large-output.txt');
writeStream.write('Line 1\n');
writeStream.write('Line 2\n');
writeStream.end('Final line\n');
writeStream.on('finish', () => console.log('Write complete'));
```

### File & Directory Operations

```javascript
const fs = require('fs/promises');
const path = require('path');

async function fileOperations() {
  // Copy
  await fs.cp('source.txt', 'dest.txt', { recursive: true });

  // Move / Rename
  await fs.rename('old.txt', 'new.txt');

  // Delete
  await fs.unlink('temp.txt');       // File
  await fs.rmdir('empty-dir');        // Empty directory
  await fs.rm('folder', { recursive: true, force: true }); // Non-empty

  // Directory creation
  await fs.mkdir('nested/a/b/c', { recursive: true });

  // Directory listing
  const entries = await fs.readdir('my-folder');
  for (const entry of entries) {
    const fullPath = path.join('my-folder', entry);
    const stat = await fs.stat(fullPath);
    console.log(`${entry} — ${stat.isDirectory() ? 'dir' : 'file'}, ${stat.size} bytes`);
  }

  // File existence check
  try {
    await fs.access('file.txt', fs.constants.F_OK);
    console.log('File exists');
  } catch {
    console.log('File does not exist');
  }
}
```

### File Metadata (Stats)

```javascript
const fs = require('fs/promises');

async function getStats() {
  const stats = await fs.stat('file.txt');

  console.log({
    size: stats.size,             // File size in bytes
    isFile: stats.isFile(),       // Regular file?
    isDirectory: stats.isDirectory(),
    isSymbolicLink: stats.isSymbolicLink(),
    birthtime: stats.birthtime,   // Creation time
    mtime: stats.mtime,           // Last modified
    atime: stats.atime,           // Last accessed
    mode: stats.mode.toString(8), // Unix permissions (e.g., 644)
    uid: stats.uid,               // Owner user ID
    gid: stats.gid,               // Owner group ID
  });
}
```

### File Watching

```javascript
const fs = require('fs');

// Watch a file for changes
fs.watchFile('config.json', { interval: 1000 }, (curr, prev) => {
  console.log(`File modified: ${new Date(curr.mtime)}`);
});

// Watch a directory (more efficient)
const watcher = fs.watch('logs/', { recursive: true });
watcher.on('change', (eventType, filename) => {
  console.log(`${eventType}: ${filename}`);
});
// watcher.close(); // Clean up
```

### Working with File Paths

```javascript
const path = require('path');

// Path manipulation
console.log(path.join('folder', 'sub', 'file.txt'));
// → 'folder/sub/file.txt'

console.log(path.resolve('relative/path'));
// → '/absolute/path/to/relative/path'

console.log(path.basename('/a/b/file.txt'));   // 'file.txt'
console.log(path.dirname('/a/b/file.txt'));    // '/a/b'
console.log(path.extname('/a/b/file.txt'));    // '.txt'
console.log(path.parse('/a/b/file.txt'));
// → { root: '/', dir: '/a/b', base: 'file.txt', ext: '.txt', name: 'file' }

// Cross-platform paths
console.log(path.sep); // '/' on POSIX, '\\' on Windows
```

### Streaming Large Files

```javascript
const fs = require('fs');
const { Transform } = require('stream');

// Pipe streams for efficient processing
const readStream = fs.createReadStream('source.txt', { highWaterMark: 64 * 1024 });
const writeStream = fs.createWriteStream('dest.txt');
const transform = new Transform({
  transform(chunk, encoding, callback) {
    this.push(chunk.toString().toUpperCase());
    callback();
  },
});

readStream.pipe(transform).pipe(writeStream);
writeStream.on('finish', () => console.log('Transformation complete'));
```

## Real-World Use Cases

### 1. Configuration File Loader

```javascript
const fs = require('fs/promises');
const path = require('path');

class ConfigLoader {
  constructor(configDir) {
    this.configDir = configDir;
    this.cache = new Map();
  }

  async load(name) {
    if (this.cache.has(name)) return this.cache.get(name);

    const configPath = path.join(this.configDir, `${name}.json`);
    try {
      const data = await fs.readFile(configPath, 'utf8');
      const config = JSON.parse(data);
      this.cache.set(name, config);
      return config;
    } catch (err) {
      if (err.code === 'ENOENT') {
        throw new Error(`Config not found: ${name}`);
      }
      throw err;
    }
  }

  async watch(name, callback) {
    const configPath = path.join(this.configDir, `${name}.json`);
    const watcher = fs.watch(configPath, (eventType) => {
      if (eventType === 'change') {
        this.cache.delete(name);
        this.load(name).then(callback).catch(console.error);
      }
    });
    return () => watcher.close();
  }
}
```

### 2. Log Rotator

```javascript
const fs = require('fs/promises');
const path = require('path');

class LogRotator {
  constructor(logDir, maxSize = 10 * 1024 * 1024) {
    this.logDir = logDir;
    this.maxSize = maxSize;
  }

  async rotate(logName) {
    const logPath = path.join(this.logDir, logName);
    try {
      const stats = await fs.stat(logPath);
      if (stats.size < this.maxSize) return;

      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const rotatedPath = path.join(this.logDir, `${logName}.${timestamp}`);
      await fs.rename(logPath, rotatedPath);

      // Keep only last 5 rotated files
      const files = await fs.readdir(this.logDir);
      const rotated = files
        .filter(f => f.startsWith(logName + '.'))
        .sort()
        .reverse();
      for (const old of rotated.slice(5)) {
        await fs.unlink(path.join(this.logDir, old));
      }
    } catch (err) {
      if (err.code !== 'ENOENT') throw err;
    }
  }
}
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using sync methods in request handlers | Always use async/promise methods for I/O in production |
| Forgetting to close file descriptors | Use `fs.promises.open()` with `try/finally` to close |
| Silently catching ENOENT errors | Check `err.code === 'ENOENT'` to handle missing files differently |
| Not using `recursive: true` for mkdir | `mkdir('a/b/c')` fails if `a` doesn't exist without `recursive` |
| Path traversal vulnerabilities | Validate user-supplied paths; use `path.resolve()` and check prefix |

## Best Practices

1. **Prefer `fs/promises`** over callbacks for modern async code
2. **Use streams** for files > 100MB to avoid memory issues
3. **Handle ENOENT separately** from other errors
4. **Use `path.join()`** for cross-platform path building
5. **Validate user-supplied file paths** to prevent directory traversal
6. **Use atomic writes** (write to temp, rename) to prevent partial writes
7. **Clean up file descriptors** in `finally` blocks
8. **Use `fs.constants`** for file permission checks (`R_OK`, `W_OK`)

## Performance Considerations

- **Synchronous I/O blocks the event loop** — never use in production request handlers
- **Streams handle large files efficiently** — default highWaterMark is 64KB
- **File watching is resource-intensive** — avoid watching many files
- **Directory operations are slower than file operations** — batch when possible
- **Concurrent writes to same file** — use file locking or a queue

## Summary

The `fs` module is essential for server-side JavaScript, enabling file persistence, configuration management, logging, and data processing. Use promise-based APIs for modern code, streams for large files, and always handle errors properly. The three API styles (promise, callback, sync) give flexibility for different contexts.

## Cheat Sheet

```text
fs MODULE CHEAT SHEET
═══════════════════════════════════════

IMPORT:
  import * as fs from 'fs/promises';   // Promise API
  import * as fs from 'fs';             // Callback + sync API

READ:
  fs.readFile(path, encoding)           // Full file
  fs.open(path).read(buffer, ...)       // Partial read
  fs.createReadStream(path)             // Streaming

WRITE:
  fs.writeFile(path, data)              // Write (overwrite)
  fs.appendFile(path, data)             // Append
  fs.createWriteStream(path)            // Streaming

FILES:
  fs.copyFile(src, dest)                // Copy
  fs.rename(old, new)                   // Move/rename
  fs.unlink(path)                       // Delete
  fs.stat(path)                         // Metadata
  fs.access(path, mode)                 // Check existence

DIRS:
  fs.mkdir(path, { recursive })         // Create
  fs.readdir(path)                      // List
  fs.rmdir(path)                        // Remove empty
  fs.rm(path, { recursive })            // Remove all

WATCH:
  fs.watch(path, callback)              // Watch for changes

PATH MODULE:
  path.join(...parts)                   // Join segments
  path.resolve(...parts)                // Absolute path
  path.basename/path.dirname/path.extname
  path.parse(path)                      // All parts
```

---

### See Also

- [Streams](02-Streams.md) — streaming file processing
- [Buffers](03-Buffers.md) — binary data handling
- [Child Processes & Workers](07-Child-Processes-Workers.md) — spawning I/O in subprocesses
- [Process & Environment](08-Process-Environment.md) — process lifecycle
- [Error Handling](../01-JavaScript/12-Error-Handling.md) — error patterns

### References

- [Node.js fs Documentation](https://nodejs.org/api/fs.html)
- [Node.js path Documentation](https://nodejs.org/api/path.html)
- [Node.js Streams Guide](https://nodejs.org/en/learn/manipulating-files/working-with-file-streams)
- [Node.js File System Guide](https://nodejs.org/en/learn/manipulating-files/reading-files-with-node-js)
