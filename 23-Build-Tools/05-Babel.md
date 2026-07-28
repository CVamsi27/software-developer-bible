# Babel

[![Category: DevOps](https://img.shields.io/badge/category-DevOps-ff7f00)](.)

 code into backward-compatible JavaScript for older browsers. It processes syntax transformation (arrow functions, optional chaining), polyfills (Promise, Array.flatMap), and is extensible via plugins and presets.

## Why Do We Need It?

1. **Browser compatibility**: Use modern syntax while supporting IE11 and older browsers
2. **Experimental features**: Try stage-0/1 proposals before standardization
3. **Custom transforms**: JSX, TypeScript (without tsc), Flow, decorators
4. **Polyfills**: `core-js` bridges runtime gaps for new APIs
5. **Optimization**: Minification, dead code elimination via plugins

## Code Examples

### Configuration

```json
// babel.config.json
{
  "presets": [
    ["@babel/preset-env", {
      "targets": "> 0.25%, not dead",
      "useBuiltIns": "usage",
      "corejs": 3
    }],
    ["@babel/preset-react", {
      "runtime": "automatic"
    }],
    ["@babel/preset-typescript"]
  ],
  "plugins": [
    "@babel/plugin-transform-runtime",
    ["@babel/plugin-proposal-decorators", { "version": "2023-05" }]
  ]
}
```

### Transform Example

```javascript
// Input (ES6+)
const double = (x) => x * 2;
const obj = { a: 1, b: 2 };
const merged = { ...obj, c: 3 };
class Animal {
  #name;
  constructor(name) { this.#name = name; }
  speak() { console.log(`${this.#name} speaks`); }
}

// Output (ES5)
var double = function double(x) { return x * 2; };
var obj = { a: 1, b: 2 };
var merged = Object.assign({}, obj, { c: 3 });
function Animal(name) { this._name = name; }
Animal.prototype.speak = function() { console.log(this._name + ' speaks'); };
```

## Best Practices

1. **Use `babel.config.json`** (project-wide) over `.babelrc` (file-relative)
2. **Set `useBuiltIns: 'usage'`** for minimal polyfills
3. **Pin `core-js` version** and install as dependency
4. **Use `@babel/plugin-transform-runtime`** to avoid helper duplication
5. **Cache Babel output** (`babel-loader` cacheDirectory in webpack)

## Summary

- Babel is a JavaScript compiler that transforms modern JS/TS code into backwards-compatible versions
- Presets (@babel/preset-env, @babel/preset-react, @babel/preset-typescript) configure transformation rules
- Plugins enable fine-grained control over specific syntax transformations and optimizations
- Polyfilling via core-js and @babel/polyfill adds runtime support for missing browser features
- Babel integrates with Webpack, Vite, and other bundlers through loader/plugin interfaces

---

## Cheat Sheet
```text
BABEL CHEAT SHEET
============================================================

INTERVIEW TIPS:
  - Understand the core concepts and trade-offs
  - Be ready to explain with real-world examples
  - Discuss performance implications and best practices
  - Show awareness of common pitfalls

```
## See Also
- [Build Optimization](04-Build-Optimization.md)
- [Next.js](../04-NextJS/)

## References & Learn More

- [Babel Documentation](https://babeljs.io/docs/)
- [Babel Preset Env](https://babeljs.io/docs/babel-preset-env)
- [Babel Plugins List](https://babeljs.io/docs/plugins-list)
