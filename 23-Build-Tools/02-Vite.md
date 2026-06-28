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
```
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
```
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
```
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

## Interview Questions

### Beginner (5-10)
1. **What is Vite and how does it differ from Webpack?**
   - Vite uses native ES modules in development for instant server start, while Webpack bundles everything.

2. **What is the entry point in a Vite project?**
   - `index.html` is the entry point, which imports JavaScript modules directly.

3. **How do you start a Vite dev server?**
   - Run `npm run dev` or `vite` command. It starts instantly without bundling.

4. **What is pre-bundling in Vite?**
   - Dependencies are pre-bundled with esbuild for faster cold starts.

5. **How do you configure Vite for React?**
   - Install `@vitejs/plugin-react` and add it to plugins in `vite.config.js`.

6. **What is `import.meta.env` in Vite?**
   - Object containing environment variables prefixed with `VITE_`.

7. **How does Vite handle CSS?**
   - Native CSS support with automatic PostCSS processing and CSS modules.

8. **What is the difference between `dev` and `build` in Vite?**
   - Dev uses native ES modules, build uses Rollup for production optimization.

### Intermediate (5-10)
9. **How do you create a custom Vite plugin?**
   - Export a function returning object with hooks like `transform`, `configureServer`.

10. **How do you configure path aliases in Vite?**
    - Use `resolve.alias` in `vite.config.js` to map paths.

11. **What is the purpose of `vite.config.js`?**
    - Configuration file for plugins, server settings, build options, and more.

12. **How do you handle environment variables in Vite?**
    - Use `.env` files with `VITE_` prefix, access via `import.meta.env`.

13. **How do you set up proxy in Vite?**
    - Configure `server.proxy` in `vite.config.js` for API forwarding.

14. **What is library mode in Vite?**
    - Build mode for creating reusable libraries with `build.lib` option.

15. **How do you optimize build size in Vite?**
    - Use `build.rollupOptions.output.manualChunks`, enable compression.

16. **What is the difference between Vite and Vite SSR?**
    - Vite SSR provides server-side rendering support with `vite ssr` command.

### Senior (10-15)
17. **Explain Vite's dependency pre-bundling algorithm.**
    - Uses esbuild to bundle node_modules dependencies, converting CJS to ESM.

18. **How does Vite's HMR work internally?**
    - Uses WebSocket connection, updates modules via `import.meta.hot` API.

19. **How do you migrate a Webpack project to Vite?**
    - Replace config, update imports, handle environment variables, test thoroughly.

20. **What are the limitations of Vite?**
    - Native ES module requirement (no IE11), smaller plugin ecosystem than Webpack.

21. **How do you handle SSR with Vite?**
    - Use `vite-plugin-ssr` or frameworks like Nuxt, SvelteKit that integrate SSR.

22. **How do you debug Vite configuration issues?**
    - Use `vite --debug`, inspect with `vite inspect`, check browser network tab.

23. **What is the purpose of `optimizeDeps` in Vite?**
    - Controls dependency pre-bundling behavior and inclusion/exclusion.

24. **How do you handle monorepos with Vite?**
    - Use workspaces, configure `resolve.alias` for shared packages.

### FAANG-style (5-10)
25. **Design a Vite configuration for a large-scale application with 50+ routes.**
    - Consider: code splitting, dynamic imports, shared chunks, manual chunks configuration.

26. **How would you optimize Vite build time for a monorepo with 20 packages?**
    - Parallel builds, shared configs, caching, incremental compilation.

27. **Compare Vite and Webpack for enterprise applications.**
    - DX, build time, plugin ecosystem, legacy support, team expertise.

28. **How would you implement micro-frontends with Vite?**
    - Use Module Federation plugin or import maps for runtime sharing.

29. **Explain Vite's architecture and extensibility points.**
    - Plugin API with hooks, middleware system, resolver customization.

### Follow-ups (5-10)
30. **What happens when Vite encounters a CommonJS module?**
    - Pre-bundles it with esbuild to convert to ESM for browser consumption.

31. **How does Vite handle dynamic imports?**
    - Uses native `import()` with automatic code splitting via Rollup.

32. **What is the impact of `build.target` on bundle size?**
    - Higher targets produce smaller bundles by using modern JavaScript features.

33. **How do you handle CSS-in-JS with Vite?**
    - Most CSS-in-JS libraries work out of the box; configure if needed.

34. **What is the future of Vite in the frontend ecosystem?**
    - Growing adoption, framework-agnostic, potential for wider tooling integration.

## Summary
Vite represents a paradigm shift in frontend tooling, offering instant development servers and optimized production builds. Its use of native ES modules for development and Rollup for production makes it fast, simple, and powerful. While it has some limitations, its benefits in developer experience and performance make it an excellent choice for modern web applications.

## References & Learn More
- [Vite Official Documentation](https://vitejs.dev/)
- [Vite GitHub Repository](https://github.com/vitejs/vite)
- [Awesome Vite](https://github.com/vitejs/awesome-vite)
- [Vite Plugin API](https://vitejs.dev/guide/api-plugin.html)
- [Vite vs Webpack Comparison](https://vitejs.dev/guide/comparisons.html)