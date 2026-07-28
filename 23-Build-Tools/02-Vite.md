---
section: Build Tools
category: DevOps
tags: [concept]
---

# Vite

## Definition
Vite (French word for "fast", pronounced /vit/) is a modern frontend build tool that provides an extremely fast development experience and optimized production builds. It leverages native ES modules in development and Rollup for production bundling.

## Why Do We Need It?
Traditional bundlers like Webpack process the entire application before serving, causing slow startup times in large projects. Vite addresses this by:

- **Instant Server Start**: No bundling needed for development
- **Lightning Fast HMR**: Hot Module Replacement that's fast regardless of app size
- **Optimized Builds**: Uses Rollup for production with tree shaking and code splitting
- **Out-of-the-box**: TypeScript, JSX, CSS support without configuration

## How It Works
Vite uses a fundamentally different approach than traditional bundlers:

### Development Mode

```text
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Browser        │───▶│  Vite Dev       │───▶│  Native ES      │
│  Request        │    │  Server         │    │  Modules        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  On-demand      │
                       │  Transform      │
                       └─────────────────┘

```

### Production Mode

```text
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Source Code    │───▶│  Rollup         │───▶│  Optimized      │
│  (ES Modules)   │    │  Bundler        │    │  Bundles        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Tree Shaking   │
                       │  Code Splitting │
                       │  Minification   │
                       └─────────────────┘

```

## Code Examples

### Basic Configuration

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  // Plugins
  plugins: [react()],

  // Development server
  server: {
    port: 3000,
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true
      }
    }
  },

  // Build options
  build: {
    outDir: 'dist',
    sourcemap: true,
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom']
        }
      }
    }
  },

  // Resolve aliases
  resolve: {
    alias: {
      '@': '/src'
    }
  }
});

```

### Project Structure

```text
my-vite-app/
├── index.html           # Entry point
├── vite.config.js       # Configuration
├── package.json
├── src/
│   ├── main.js          # Main entry
│   ├── App.jsx          # Root component
│   ├── components/
│   ├── styles/
│   └── assets/
└── public/
    └── favicon.ico

```

### React with Vite

```jsx
// src/main.jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/main.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

```

### Vue with Vite

```javascript
// vite.config.js for Vue
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': '/src'
    }
  }
});

```

### CSS Preprocessors

```javascript
// vite.config.js
export default defineConfig({
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `
          @import "./src/variables.scss";
          @import "./src/mixins.scss";
        `
      }
    }
  }
});

```

### Environment Variables

```javascript
// .env.development
VITE_API_URL=http://localhost:8080
VITE_APP_TITLE=My App (Dev)

// .env.production
VITE_API_URL=https://api.example.com
VITE_APP_TITLE=My App

// Usage in code
console.log(import.meta.env.VITE_API_URL);

```

### Custom Plugin

```javascript
// my-plugin.js
export default function myPlugin() {
  return {
    name: 'my-plugin',
    transform(code, id) {
      if (id.endsWith('.custom')) {
        // Transform custom file format
        return `export default ${JSON.stringify(code)}`;
      }
    },
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        // Add custom middleware
        next();
      });
    }
  };
}

// vite.config.js
import myPlugin from './my-plugin.js';

export default defineConfig({
  plugins: [myPlugin()]
});

```

## Real-World Use Cases

1. **Single Page Applications**: React, Vue, Svelte apps with instant dev server

2. **Library Development**: Create component libraries with `library mode`

3. **Monorepos**: Fast development across multiple packages

4. **Static Sites**: With frameworks like Astro, VitePress

5. **Migration Projects**: Gradually migrate from Webpack to Vite

## Common Mistakes

1. **Using CommonJS in config**: Vite uses ESM, so use `import/export` in `vite.config.js`

2. **Ignoring `index.html`**: Vite treats `index.html` as part of the module graph

3. **Missing `.jsx` extension**: React files must use `.jsx` extension

4. **Incorrect environment variables**: Must prefix with `VITE_` to expose to client

5. **Using `require()`**: Vite uses native ES modules, avoid CommonJS

6. **Not handling older browsers**: Configure `build.target` for compatibility

## Best Practices

1. **Use native ES modules**: Import without extensions when possible

2. **Leverage `import.meta.env`**: For environment variables

3. **Use `@` alias**: For clean imports from `src/`

4. **Configure proxy**: For API calls during development

5. **Use CSS modules**: For scoped styles by default

6. **Enable compression**: For production builds

7. **Use dynamic imports**: For code splitting

## Performance Considerations

- **Dev server**: Vite starts instantly by pre-bundling dependencies with esbuild
- **HMR**: Updates are instant regardless of app size
- **Build**: Rollup produces optimized bundles with tree shaking
- **Pre-bundling**: Dependencies are pre-bundled with esbuild (10-100x faster than Webpack)
- **Source maps**: Use `hidden` for production to reduce bundle size

## Summary
Vite represents a paradigm shift in frontend tooling, offering instant development servers and optimized production builds. Its use of native ES modules for development and Rollup for production makes it fast, simple, and powerful. While it has some limitations, its benefits in developer experience and performance make it an excellent choice for modern web applications.

---

## See Also
- [Next.js](../04-NextJS/)
- [Performance Monitoring](../26-Performance-Monitoring/)
- [React](../03-React/)

## References & Learn More

- [Vite Official Documentation](https://vitejs.dev/)
- [Vite GitHub Repository](https://github.com/vitejs/vite)
- [Awesome Vite](https://github.com/vitejs/awesome-vite)
- [Vite Plugin API](https://vitejs.dev/guide/api-plugin.html)
- [Vite vs Webpack Comparison](https://vitejs.dev/guide/comparisons.html)
