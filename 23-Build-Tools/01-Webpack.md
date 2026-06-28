# Webpack

## Definition
Webpack is a static module bundler for modern JavaScript applications. When webpack processes your application, it internally builds a dependency graph from one or more entry points and then bundles every module your project needs into one or more bundles (usually JavaScript files) to be used by a browser.

## Why Do We Need It?
In modern web development, applications are composed of many modules, assets (images, fonts, CSS), and dependencies. Browsers cannot natively understand most of these modules (ES modules, CommonJS, CSS, images). Webpack solves this by:
- **Bundling**: Combining all assets into optimized bundles
- **Transformations**: Using loaders to transform non-JS files into valid modules
- **Optimization**: Minifying, code-splitting, and tree-shaking for performance
- **Development Experience**: Hot Module Replacement (HMR), dev server, watch mode

## How It Works
Webpack uses a configuration file (`webpack.config.js`) that defines entry points, output, loaders, plugins, and other settings. It reads the entry point, follows all `import`/`require` statements, builds a dependency graph, and outputs bundles.

### Webpack Compilation Flow
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Entry      │───▶│  Resolve    │───▶│  Loaders    │───▶│  Plugins    │
│  Points     │    │  Modules    │    │  Transform  │    │  Optimize   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                                                       │
       ▼                                                       ▼
┌─────────────┐                                       ┌─────────────┐
│  Dependency │                                       │  Output     │
│  Graph      │                                       │  Bundles    │
└─────────────┘                                       └─────────────┘
```

## Code Examples

### Basic Configuration
```javascript
// webpack.config.js
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  // Entry point(s)
  entry: './src/index.js',

  // Output configuration
  output: {
    filename: 'bundle.[contenthash].js',
    path: path.resolve(__dirname, 'dist'),
    clean: true,
  },

  // Module rules (loaders)
  module: {
    rules: [
      {
        test: /\.jsx?$/,          // Transform JavaScript/JSX
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react']
          }
        }
      },
      {
        test: /\.css$/,           // Process CSS
        use: ['style-loader', 'css-loader']
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,  // Handle images
        type: 'asset/resource'
      }
    ]
  },

  // Plugins
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/index.html'
    })
  ],

  // Development/Production modes
  mode: 'development',  // or 'production'

  // Dev server
  devServer: {
    static: './dist',
    hot: true,
    port: 3000
  }
};
```

### Entry & Output
```javascript
// Multiple entry points
module.exports = {
  entry: {
    main: './src/index.js',
    admin: './src/admin/index.js'
  },
  output: {
    filename: '[name].[contenthash].js',
    path: path.resolve(__dirname, 'dist'),
    publicPath: '/',
    clean: true
  }
};
```

### Loaders
```javascript
// Loader examples
module: {
  rules: [
    // Babel for modern JS
    {
      test: /\.js$/,
      exclude: /node_modules/,
      use: 'babel-loader'
    },
    // SCSS processing
    {
      test: /\.scss$/,
      use: ['style-loader', 'css-loader', 'sass-loader']
    },
    // TypeScript
    {
      test: /\.tsx?$/,
      use: 'ts-loader',
      exclude: /node_modules/
    }
  ]
}
```

### Plugins
```javascript
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const { DefinePlugin } = require('webpack');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

plugins: [
  // Extract CSS to separate file
  new MiniCssExtractPlugin({
    filename: '[name].[contenthash].css'
  }),

  // Define environment variables
  new DefinePlugin({
    'process.env.NODE_ENV': JSON.stringify('production')
  }),

  // Bundle analysis
  new BundleAnalyzerPlugin()
]
```

### Code Splitting
```javascript
// Dynamic imports for code splitting
const Home = React.lazy(() => import('./pages/Home'));
const About = React.lazy(() => import('./pages/About'));

// webpack.config.js optimization
optimization: {
  splitChunks: {
    chunks: 'all',
    cacheGroups: {
      vendor: {
        test: /[\\/]node_modules[\\/]/,
        name: 'vendors',
        chunks: 'all'
      }
    }
  }
}
```

## Real-World Use Cases
1. **Single Page Applications (SPA)**: Bundling React, Vue, Angular apps
2. **Micro-frontends**: Splitting large apps into independently deployable pieces
3. **Legacy browser support**: Transpiling modern JavaScript for older browsers
4. **SSR applications**: Server-side rendering with webpack for Node.js
5. **Library development**: Creating reusable component libraries

## Common Mistakes
1. **Not setting `mode`**: Always set `mode` to 'development' or 'production'
2. **Ignoring tree shaking**: Use ES modules and `sideEffects: false` in package.json
3. **Over-bundling**: Not configuring code splitting properly
4. **Missing loaders**: Forgetting to install required loaders
5. **Not using environment variables**: Hardcoding values instead of using DefinePlugin
6. **Large node_modules in bundle**: Not excluding node_modules properly

## Best Practices
1. **Use production mode**: For builds, always use `mode: 'production'`
2. **Enable tree shaking**: Use ES modules and mark side effects
3. **Code split**: Use dynamic imports and `splitChunks`
4. **Use content hashing**: For cache busting in filenames
5. **Monitor bundle size**: Use BundleAnalyzerPlugin
6. **Use loaders efficiently**: Only transform what's needed
7. **Cache builds**: Use webpack's built-in caching

## Performance Considerations
- **Build speed**: Use `cache: true` for faster rebuilds
- **Bundle size**: Enable tree shaking and code splitting
- **Loaders**: Use `include`/`exclude` to limit loader scope
- **Plugins**: Use only necessary plugins
- **Source maps**: Use appropriate devtool settings for dev vs prod
- **Parallel processing**: Use thread-loader for heavy tasks

## Interview Questions

### Beginner (5-10)
1. **What is Webpack and why is it used?**
   - Webpack is a module bundler that combines assets into optimized bundles for browsers.

2. **What is the difference between entry and output in Webpack?**
   - Entry: Starting point(s) for the dependency graph. Output: Where bundles are written.

3. **What are loaders in Webpack?**
   - Loaders transform non-JS files (CSS, images) into valid modules webpack can process.

4. **What are plugins in Webpack?**
   - Plugins perform broader tasks like optimization, asset management, and environment variable injection.

5. **What is the purpose of webpack-dev-server?**
   - Provides a development server with HMR, live reloading, and proxying.

6. **What does `mode` do in Webpack configuration?**
   - Sets environment-specific optimizations: development, production, or none.

7. **What is Hot Module Replacement (HMR)?**
   - Updates modules in the browser without full page reload during development.

8. **How do you handle static assets in Webpack?**
   - Use asset modules (asset/resource, asset/inline) or file-loader/url-loader.

### Intermediate (5-10)
9. **What is code splitting and how do you implement it?**
   - Breaking bundles into smaller chunks. Use dynamic imports, splitChunks plugin, or entry points.

10. **What is tree shaking?**
   - Removing unused code from bundles. Requires ES modules and `sideEffects: false`.

11. **How do you optimize Webpack build performance?**
   - Use caching, limit loader scope, minimize plugins, use thread-loader.

12. **What is the difference between `style-loader` and `MiniCssExtractPlugin`?**
   - style-loader injects CSS into DOM via JS. MiniCssExtractPlugin extracts CSS to files.

13. **How do you configure Webpack for TypeScript?**
   - Use ts-loader or babel-loader with @babel/preset-typescript.

14. **What is the purpose of `contenthash` in output filenames?**
   - Provides unique hashes based on file content for effective cache busting.

15. **How do you handle different environments in Webpack?**
   - Use environment variables, separate config files, or webpack-merge.

### Senior (10-15)
16. **Explain Webpack's compilation flow in detail.**
   - Entry → Resolve → Loaders → Plugins → Optimize → Output

17. **How do you implement micro-frontends with Webpack?**
   - Use Module Federation plugin for runtime sharing of dependencies.

18. **What is the purpose of `splitChunks.cacheGroups`?**
   - Defines rules for how chunks are split, like separating vendor code.

19. **How do you debug Webpack configuration issues?**
   - Use `webpack --stats verbose`, analyze with BundleAnalyzerPlugin, inspect output.

20. **What is the difference between `require.ensure` and dynamic `import()`?**
   - Both create split points, but `import()` is standard and more flexible.

21. **How do you handle server-side rendering with Webpack?**
   - Create separate client and server configs, use `target: 'node'` for server.

22. **What are Webpack externals and when to use them?**
   - Exclude dependencies from bundle. Use for libraries already available globally.

23. **How do you implement long-term caching with Webpack?**
   - Use contenthash, splitChunks, and proper chunk naming.

### FAANG-style (5-10)
24. **Design a Webpack configuration for a large-scale application with 100+ routes.**
    - Consider: code splitting per route, vendor chunking, shared modules, parallel builds.

25. **How would you reduce initial load time by 50% for a React application?**
    - Route-based code splitting, lazy loading, prefetching, tree shaking, compression.

26. **Explain how Module Federation works at runtime.**
    - Containers expose/consume modules at runtime, sharing dependencies dynamically.

27. **How do you handle monorepo builds with Webpack?**
    - Use workspaces, shared configs, cache across packages, parallel compilation.

28. **What are the trade-offs between Webpack and Vite for large applications?**
    - Build time, DX, plugin ecosystem, production optimization, legacy support.

### Follow-ups (5-10)
29. **How does Webpack's caching mechanism work internally?**
    - Filesystem caching stores build metadata for faster subsequent builds.

30. **What happens when a loader throws an error during compilation?**
    - Webpack stops compilation, reports the error, and waits for file changes.

31. **How do you handle circular dependencies in Webpack?**
    - Webpack handles them but may cause undefined imports. Refactor to avoid.

32. **What is the impact of `devtool` settings on build performance?**
    - Source maps vary in speed/quality. `eval` is fastest, `source-map` is slowest.

33. **How do you test Webpack configurations?**
    - Use webpack's Node.js API, mock file system, and validate output.

## Summary
Webpack is a powerful, flexible module bundler essential for modern web development. It handles complex dependency graphs, transforms various file types, and optimizes output for production. Understanding entry/output, loaders, plugins, code splitting, and optimization techniques is crucial for building performant applications.

## References & Learn More
- [Webpack Official Documentation](https://webpack.js.org/)
- [Webpack GitHub Repository](https://github.com/webpack/webpack)
- [Webpack Academy](https://webpack.academy/)
- [SurviveJS - Webpack](https://survivejs.com/webpack/)
- [Webpack Configuration Examples](https://github.com/webpack/webpack/tree/main/examples)