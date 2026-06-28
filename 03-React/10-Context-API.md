# Context API

## Definition

React Context API is a mechanism for passing data through the component tree without having to pass props down manually at every level. It provides a way to share values (like themes, authentication status, or language preferences) between components that are "connected" — that is, don't need to be direct parent-child relationships.

Context consists of three parts:

1. **Context Object**: Created with `React.createContext()`

2. **Provider**: Wraps the component tree to provide the value

3. **Consumer**: Reads the value from the nearest Provider

## Why Do We Need It?

### The Problem: Prop Drilling

Without Context, data must be passed through props from parent to child, even if intermediate components don't need it:

```text
Prop Drilling Problem:
═══════════════════════════════════════════════════════════════

App (has theme state)
├── Layout (receives theme, passes it down)
│   ├── Sidebar (receives theme, passes it down)
│   │   └── ThemeToggle (NEEDS theme) ← Target
│   └── Main (receives theme, passes it down)
│       └── Content (receives theme, passes it down)
│           └── Article (NEEDS theme) ← Target

Problem: Layout, Sidebar, Main, Content all receive theme
props even though they don't use them!

```

### The Solution: Context

```text
Context Solution:
═══════════════════════════════════════════════════════════════

ThemeContext.Provider (has theme state)
├── Layout (NO theme prop needed)
│   ├── Sidebar (NO theme prop needed)
│   │   └── ThemeToggle (uses useContext(ThemeContext)) ← Direct access!
│   └── Main (NO theme prop needed)
│       └── Content (NO theme prop needed)
│           └── Article (uses useContext(ThemeContext)) ← Direct access!

Benefit: Only ThemeToggle and Article need to know about theme

```

## How It Works

### Context Creation and Usage

```text
Context API Flow:
═══════════════════════════════════════════════════════════════

1. Create Context:
┌─────────────────────────────────────────────────────────────┐
│ const ThemeContext = React.createContext('light');           │
│ // Default value: 'light'                                   │
└─────────────────────────────────────────────────────────────┘

2. Provide Context:
┌─────────────────────────────────────────────────────────────┐
│ const App = () => {                                         │
│   const [theme, setTheme] = useState('light');              │
│                                                             │
│   return (                                                  │
│     <ThemeContext.Provider value={theme}>                   │
│       <Layout />                                            │
│     </ThemeContext.Provider>                                │
│   );                                                        │
│ };                                                          │
└─────────────────────────────────────────────────────────────┘

3. Consume Context:
┌─────────────────────────────────────────────────────────────┐
│ const ThemeToggle = () => {                                 │
│   const theme = useContext(ThemeContext);                    │
│                                                             │
│   return (                                                  │
│     <button onClick={() => setTheme(                        │
│       theme === 'light' ? 'dark' : 'light'                  │
│     )}>                                                     │
│       Current: {theme}                                      │
│     </button>                                               │
│   );                                                        │
│ };                                                          │
└─────────────────────────────────────────────────────────────┘

```

### Context Propagation

```text
Context Propagation:
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│ ThemeContext.Provider value="dark"                          │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Component A (no useContext)                             │ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ Component B (no useContext)                         │ │ │
│ │ │ ┌─────────────────────────────────────────────────┐ │ │ │
│ │ │ │ Component C (useContext) → gets "dark"          │ │ │ │
│ │ │ └─────────────────────────────────────────────────┘ │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ Multiple Providers:                                         │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ ThemeContext.Provider value="dark"                      │ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ ThemeContext.Provider value="light"                 │ │ │
│ │ │ ┌─────────────────────────────────────────────────┐ │ │ │
│ │ │ │ Component (useContext) → gets "light"           │ │ │ │
│ │ │ └─────────────────────────────────────────────────┘ │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ Inner Provider shadows outer Provider                      │
└─────────────────────────────────────────────────────────────┘

```

### Consumer Component

```text
Consumer Component:
═══════════════════════════════════════════════════════════════

useContext Hook (Recommended):
┌─────────────────────────────────────────────────────────────┐
│ const ThemeToggle = () => {                                 │
│   const theme = useContext(ThemeContext);                    │
│   return <button>Current: {theme}</button>;                 │
│ };                                                          │
└─────────────────────────────────────────────────────────────┘

Consumer Component (Alternative):
┌─────────────────────────────────────────────────────────────┐
│ const ThemeToggle = () => {                                 │
│   return (                                                  │
│     <ThemeContext.Consumer>                                 │
│       {theme => <button>Current: {theme}</button>}          │
│     </ThemeContext.Consumer>                                │
│   );                                                        │
│ };                                                          │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### Basic Context

```typescript
import React, { createContext, useContext, useState } from 'react';

// 1. Create context with default value
const ThemeContext = createContext<'light' | 'dark'>('light');

// 2. Provider component
const ThemeProvider = ({ children }: { children: React.ReactNode }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  const toggleTheme = () => {
    setTheme(prev => (prev === 'light' ? 'dark' : 'light'));
  };

  return (
    <ThemeContext.Provider value={theme}>
      {children}
    </ThemeContext.Provider>
  );
};

// 3. Custom hook for consuming context
const useTheme = () => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

// 4. Components that use context
const Header = () => {
  const theme = useTheme();
  return (
    <header className={theme}>
      <h1>My App</h1>
    </header>
  );
};

const ThemeToggle = () => {
  const theme = useTheme();
  return (
    <button onClick={() => {/* toggle logic */}}>
      Current: {theme}
    </button>
  );
};

// 5. App with provider
const App = () => (
  <ThemeProvider>
    <Header />
    <ThemeToggle />
  </ThemeProvider>
);

```

### Context with Multiple Values

```typescript
interface AppContextType {
  theme: 'light' | 'dark';
  user: User | null;
  setTheme: (theme: 'light' | 'dark') => void;
  setUser: (user: User | null) => void;
}

const AppContext = createContext<AppContextType | null>(null);

const AppProvider = ({ children }: { children: React.ReactNode }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const [user, setUser] = useState<User | null>(null);

  const value = useMemo(() => ({
    theme,
    user,
    setTheme,
    setUser,
  }), [theme, user]);

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
};

```

### Context with Performance Optimization

```typescript
const ThemeContext = createContext<{
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}>({
  theme: 'light',
  toggleTheme: () => {},
});

const ThemeProvider = ({ children }: { children: React.ReactNode }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  const toggleTheme = useCallback(() => {
    setTheme(prev => (prev === 'light' ? 'dark' : 'light'));
  }, []);

  // Memoize context value to prevent unnecessary re-renders
  const value = useMemo(() => ({
    theme,
    toggleTheme,
  }), [theme, toggleTheme]);

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

```

### Context with TypeScript

```typescript
// Define context type
interface AuthContextType {
  user: User | null;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

// Create context with proper typing
const AuthContext = createContext<AuthContextType | null>(null);

// Provider component
const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);

  const login = async (credentials: Credentials) => {
    const response = await api.login(credentials);
    setUser(response.user);
  };

  const logout = () => {
    setUser(null);
  };

  const value = useMemo(() => ({
    user,
    login,
    logout,
    isAuthenticated: !!user,
  }), [user]);

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook with proper error handling
const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

```

### Nested Context

```typescript
const ThemeContext = createContext('light');
const UserContext = createContext<User | null>(null);

const App = () => {
  const [theme, setTheme] = useState('light');
  const [user, setUser] = useState<User | null>(null);

  return (
    <ThemeContext.Provider value={theme}>
      <UserContext.Provider value={user}>
        <Layout />
      </UserContext.Provider>
    </ThemeContext.Provider>
  );
};

// Components can consume either context
const Header = () => {
  const theme = useContext(ThemeContext);
  const user = useContext(UserContext);

  return (
    <header className={theme}>
      {user ? `Welcome, ${user.name}` : 'Welcome, Guest'}
    </header>
  );
};

```

## Real-World Use Cases

### 1. Authentication Context

```typescript
interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
}

interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (data: RegisterData) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [state, setState] = useState<AuthState>({
    user: null,
    token: localStorage.getItem('token'),
    isLoading: true,
  });

  useEffect(() => {
    const verifyToken = async () => {
      try {
        const token = localStorage.getItem('token');
        if (token) {
          const user = await api.verifyToken(token);
          setState(prev => ({ ...prev, user, isLoading: false }));
        } else {
          setState(prev => ({ ...prev, isLoading: false }));
        }
      } catch {
        localStorage.removeItem('token');
        setState({ user: null, token: null, isLoading: false });
      }
    };
    verifyToken();
  }, []);

  const login = async (email: string, password: string) => {
    const { user, token } = await api.login({ email, password });
    localStorage.setItem('token', token);
    setState({ user, token, isLoading: false });
  };

  const logout = () => {
    localStorage.removeItem('token');
    setState({ user: null, token: null, isLoading: false });
  };

  const value = useMemo(() => ({
    ...state,
    login,
    logout,
  }), [state]);

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

```

### 2. Theme Context

```typescript
type Theme = 'light' | 'dark' | 'system';

interface ThemeContextType {
  theme: Theme;
  resolvedTheme: 'light' | 'dark';
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextType | null>(null);

export const ThemeProvider = ({ children }: { children: React.ReactNode }) => {
  const [theme, setTheme] = useState<Theme>(() => {
    return (localStorage.getItem('theme') as Theme) || 'system';
  });

  const [resolvedTheme, setResolvedTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

    const getResolvedTheme = (): 'light' | 'dark' => {
      if (theme === 'system') {
        return mediaQuery.matches ? 'dark' : 'light';
      }
      return theme;
    };

    setResolvedTheme(getResolvedTheme());
    localStorage.setItem('theme', theme);

    const handleChange = () => {
      if (theme === 'system') {
        setResolvedTheme(mediaQuery.matches ? 'dark' : 'light');
      }
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [theme]);

  const value = useMemo(() => ({
    theme,
    resolvedTheme,
    setTheme,
  }), [theme, resolvedTheme]);

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
};

```

### 3. Internationalization Context

```typescript
interface I18nContextType {
  locale: string;
  t: (key: string, params?: Record<string, any>) => string;
  setLocale: (locale: string) => void;
}

const I18nContext = createContext<I18nContextType | null>(null);

export const I18nProvider = ({ children }: { children: React.ReactNode }) => {
  const [locale, setLocale] = useState(() => {
    return navigator.language.split('-')[0] || 'en';
  });

  const [translations, setTranslations] = useState<Record<string, string>>({});

  useEffect(() => {
    import(`../locales/${locale}.json`).then(module => {
      setTranslations(module.default);
    });
  }, [locale]);

  const t = useCallback((key: string, params?: Record<string, any>) => {
    let translation = translations[key] || key;
    if (params) {
      Object.entries(params).forEach(([param, value]) => {
        translation = translation.replace(`{{${param}}}`, String(value));
      });
    }
    return translation;
  }, [translations]);

  const value = useMemo(() => ({
    locale,
    t,
    setLocale,
  }), [locale, t]);

  return (
    <I18nContext.Provider value={value}>
      {children}
    </I18nContext.Provider>
  );
};

export const useI18n = () => {
  const context = useContext(I18nContext);
  if (!context) {
    throw new Error('useI18n must be used within I18nProvider');
  }
  return context;
};

```

### 4. Shopping Cart Context

```typescript
interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartContextType {
  items: CartItem[];
  addItem: (item: Omit<CartItem, 'quantity'>) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  total: number;
  itemCount: number;
}

const CartContext = createContext<CartContextType | null>(null);

export const CartProvider = ({ children }: { children: React.ReactNode }) => {
  const [items, setItems] = useState<CartItem[]>([]);

  const addItem = useCallback((item: Omit<CartItem, 'quantity'>) => {
    setItems(prev => {
      const existing = prev.find(i => i.id === item.id);
      if (existing) {
        return prev.map(i =>
          i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i
        );
      }
      return [...prev, { ...item, quantity: 1 }];
    });
  }, []);

  const removeItem = useCallback((id: string) => {
    setItems(prev => prev.filter(item => item.id !== id));
  }, []);

  const updateQuantity = useCallback((id: string, quantity: number) => {
    setItems(prev =>
      prev.map(item =>
        item.id === id ? { ...item, quantity } : item
      )
    );
  }, []);

  const total = useMemo(
    () => items.reduce((sum, item) => sum + item.price * item.quantity, 0),
    [items]
  );

  const itemCount = useMemo(
    () => items.reduce((sum, item) => sum + item.quantity, 0),
    [items]
  );

  const value = useMemo(() => ({
    items,
    addItem,
    removeItem,
    updateQuantity,
    total,
    itemCount,
  }), [items, addItem, removeItem, updateQuantity, total, itemCount]);

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within CartProvider');
  }
  return context;
};

```

## Common Mistakes

### 1. Not Memoizing Context Value

```typescript
// ❌ BAD: New object on every render
const App = () => {
  const [theme, setTheme] = useState('light');

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {/* Every render creates a new value object */}
      {/* All consumers re-render even if theme didn't change */}
      <Child />
    </ThemeContext.Provider>
  );
};

// ✅ GOOD: Memoize context value
const App = () => {
  const [theme, setTheme] = useState('light');

  const value = useMemo(() => ({
    theme,
    setTheme,
  }), [theme]);

  return (
    <ThemeContext.Provider value={value}>
      {/* Only re-renders consumers when theme changes */}
      <Child />
    </ThemeContext.Provider>
  );
};

```

### 2. Creating Context Inside Component

```typescript
// ❌ BAD: Creating context inside component
const Parent = () => {
  const ThemeContext = createContext('light'); // New context every render!

  return (
    <ThemeContext.Provider value="light">
      <Child />
    </ThemeContext.Provider>
  );
};

// ✅ GOOD: Create context outside component
const ThemeContext = createContext('light');

const Parent = () => {
  return (
    <ThemeContext.Provider value="light">
      <Child />
    </ThemeContext.Provider>
  );
};

```

### 3. Not Providing Error Handling

```typescript
// ❌ BAD: No error handling
const useTheme = () => {
  return useContext(ThemeContext); // Could be undefined!
};

// ✅ GOOD: Error handling
const useTheme = () => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

```

### 4. Overusing Context

```typescript
// ❌ BAD: Using context for local state
const Component = () => {
  const [count, setCount] = useState(0);

  return (
    <CountContext.Provider value={{ count, setCount }}>
      {/* Unnecessary context for local state */}
      <button onClick={() => setCount(c => c + 1)}>+1</button>
    </CountContext.Provider>
  );
};

// ✅ GOOD: Use context only for shared state
const Component = () => {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(c => c + 1)}>+1</button>
  );
};

```

## Best Practices

1. **Memoize context value**: Use `useMemo` to prevent unnecessary consumer re-renders.

2. **Create context outside components**: Don't create context inside render functions.

3. **Provide error handling**: Throw errors in custom hooks when context is undefined.

4. **Split contexts**: Don't put everything in one context. Split by concern.

5. **Use custom hooks**: Encapsulate context consumption in custom hooks.

6. **Default values wisely**: Provide meaningful default values or null.

7. **Don't overuse context**: Use local state for component-specific data.

## Performance Considerations

### Context Performance

| Aspect | Impact | Mitigation |
|--------|--------|------------|
| Value changes | All consumers re-render | Memoize value, split contexts |
| Large contexts | Many consumers affected | Split by concern |
| Frequent updates | Frequent consumer re-renders | Use `useTransition` for non-urgent |
| Deep nesting | Performance overhead | Flatten context structure |

### When to Use Context

| Use Case | Context | State Management |
|----------|---------|------------------|
| Theme | ✅ | ❌ |
| Authentication | ✅ | ❌ |
| Language | ✅ | ❌ |
| Shopping cart | ✅ | ✅ (Redux/Zustand) |
| Complex app state | ❌ | ✅ (Redux/Zustand) |

## Interview Questions

### Beginner (5-10)

**Q1: What is Context API?**
A: Context API is a React mechanism for passing data through the component tree without passing props at every level. It's used for global data like themes, authentication, and language.

**Q2: What are the three parts of Context?**
A:

1. **Context Object**: Created with `React.createContext()`

2. **Provider**: Wraps component tree to provide value

3. **Consumer**: Reads value from nearest Provider

**Q3: What is prop drilling?**
A: Prop drilling is passing props through intermediate components that don't use them. Context solves this by providing data directly to components that need it.

**Q4: How do you create a context?**
A: `const ThemeContext = createContext('light')`. The argument is the default value.

**Q5: How do you provide context?**
A: Wrap components with Provider: `<ThemeContext.Provider value={theme}>...</ThemeContext.Provider>`

**Q6: How do you consume context?**
A: Use `useContext` hook: `const theme = useContext(ThemeContext)`

**Q7: What happens if no Provider is found?**
A: The default value from `createContext()` is used.

**Q8: Can you have multiple Providers?**
A: Yes. Each Provider provides a different context. You can also nest Providers of the same context.

**Q9: What is the Consumer component?**
A: Consumer is an alternative to `useContext` for reading context. It uses render props: `<ThemeContext.Consumer>{theme => ...}</ThemeContext.Consumer>`

**Q10: When should you use Context?**
A: Use Context for:

- Global data (themes, language)
- Authentication state
- Any data needed by many components at different nesting levels

### Intermediate (5-10)

**Q11: How does Context affect performance?**
A: When a Provider's value changes, all consumers re-render. This can be optimized by memoizing the value and splitting contexts by concern.

**Q12: How do you optimize Context performance?**
A:

1. Memoize Provider value with `useMemo`

2. Split large contexts into smaller ones

3. Use `useTransition` for non-urgent updates

4. Memoize consumer components with `React.memo`

**Q13: What is the relationship between Context and Redux?**
A: Context is for simple global state. Redux is for complex state with updates, middleware, and devtools. Context is built into React; Redux is a third-party library.

**Q14: How do you handle Context updates?**
A: Context updates when the Provider's value prop changes. Consumers re-render. Use `useMemo` to prevent unnecessary value changes.

**Q15: Can you use Context with TypeScript?**
A: Yes. Create typed context:

```typescript
const ThemeContext = createContext<string | null>(null);

```

**Q16: What is the difference between Context and prop drilling?**
A: Context passes data directly to consumers. Prop drilling passes data through intermediate components. Context is more efficient for deep component trees.

**Q17: How do you split Contexts?**
A: Split by concern:

```typescript
const ThemeContext = createContext('light');
const UserContext = createContext<User | null>(null);
const AuthContext = createContext<AuthContextType | null>(null);

```

**Q18: What is the default value in createContext?**
A: The default value is used when no Provider is found. It's useful for testing and default behavior.

**Q19: How do you test Context?**
A: Wrap test components with Provider:

```typescript
render(
  <ThemeContext.Provider value="dark">
    <Component />
  </ThemeContext.Provider>
);

```

**Q20: What are the common Context patterns?**
A:

- Provider component with state
- Custom hook for consumption
- Memoized context value
- Error handling in custom hooks

### Senior (10-15)

**Q21: Explain the complete Context update lifecycle.**
A:

1. Provider value prop changes

2. React notifies all consumers

3. Consumers re-render with new value

4. React updates DOM if needed

**Q22: How does Context interact with React.memo?**
A: `React.memo` prevents re-renders when props haven't changed. However, Context updates bypass `React.memo` — consumers always re-render when Provider value changes.

**Q23: What is the relationship between Context and concurrent rendering?**
A: Concurrent rendering can pause rendering. Context updates can be deferred using `useTransition`. This keeps the UI responsive during heavy updates.

**Q24: How do you handle Context in server components?**
A: Server Components can't use Context directly. Client Components hydrate with normal Context behavior. Server Components pass data as props.

**Q25: What is the performance impact of Context on large apps?**
A: Large contexts with many consumers cause frequent re-renders. Mitigate by splitting contexts and memoizing values.

**Q26: How do you handle Context with React DevTools?**
A: React DevTools shows Context values in the component tree. You can inspect Provider values and consumer updates.

**Q27: What is the relationship between Context and state management?**
A: Context provides simple global state. Complex apps need Redux/Zustand for:

- Complex update logic
- Middleware
- Devtools
- Performance optimization

**Q28: How do you handle Context with Suspense?**
A: Suspense can suspend rendering during Context updates. This allows React to keep the old UI visible while preparing new values.

**Q29: What is the memory impact of Context?**
A: Each Context stores state in fiber nodes. Large contexts increase memory usage. Memoization reduces unnecessary value creation.

**Q30: How do you handle Context with error boundaries?**
A: Error boundaries catch errors in Context consumers. They don't catch errors in Providers. Use error boundaries around consumers.

### FAANG-style (5-10)

**Q31: Design a Context-based state management system.**
A:

1. **Split contexts**: By concern (theme, auth, data)

2. **Memoize values**: Prevent unnecessary re-renders

3. **Custom hooks**: Encapsulate consumption

4. **Error handling**: Throw errors for missing providers

5. **Performance**: Use `useTransition` for non-urgent updates

**Q32: How would you debug a Context performance issue?**
A:

1. React DevTools: Check Provider value changes

2. Profiler: Measure consumer re-renders

3. Console logging: Log value changes

4. Chrome DevTools: Record interactions

5. Memoization analysis: Check if values are memoized

**Q33: Analyze the memory implications of Context.**
A:

- Each Context: ~100 bytes per consumer
- Provider value: Depends on value type
- For 1000 consumers: ~100KB
- Memoization reduces memory churn

**Q34: How would you implement a Context-based form system?**
A:

```typescript
const FormContext = createContext<FormContextType | null>(null);

const FormProvider = ({ children }: { children: React.ReactNode }) => {
  const [values, setValues] = useState<Record<string, any>>({});
  const [errors, setErrors] = useState<Record<string, string>>({});

  const setValue = useCallback((field: string, value: any) => {
    setValues(prev => ({ ...prev, [field]: value }));
  }, []);

  const value = useMemo(() => ({
    values,
    errors,
    setValue,
  }), [values, errors, setValue]);

  return (
    <FormContext.Provider value={value}>
      {children}
    </FormContext.Provider>
  );
};

```

**Q35: Design a Context-based real-time data system.**
A:

```typescript
const DataContext = createContext<DataContextType | null>(null);

const DataProvider = ({ children }: { children: React.ReactNode }) => {
  const [data, setData] = useState<Data[]>([]);

  useEffect(() => {
    const ws = new WebSocket('wss://api.example.com/data');
    ws.onmessage = (event) => {
      const newData = JSON.parse(event.data);
      setData(prev => [...prev, newData]);
    };
    return () => ws.close();
  }, []);

  const value = useMemo(() => ({ data }), [data]);

  return (
    <DataContext.Provider value={value}>
      {children}
    </DataContext.Provider>
  );
};

```

**Q36: How does Context handle the "tearing" problem?**
A: Tearing occurs when different parts of the UI show inconsistent states. Context prevents this by providing consistent values to all consumers.

**Q37: Analyze the performance characteristics of Context.**
A:

| Metric | Without Memo | With Memo |
|--------|--------------|-----------|
| Value creation | Every render | When deps change |
| Consumer re-renders | All consumers | Only affected |
| Memory usage | Higher | Lower |

**Q38: How would you implement a Context-based caching system?**
A:

```typescript
const CacheContext = createContext<CacheContextType | null>(null);

const CacheProvider = ({ children }: { children: React.ReactNode }) => {
  const [cache, setCache] = useState<Record<string, any>>({});

  const get = useCallback((key: string) => {
    return cache[key];
  }, [cache]);

  const set = useCallback((key: string, value: any) => {
    setCache(prev => ({ ...prev, [key]: value }));
  }, []);

  const value = useMemo(() => ({ get, set }), [get, set]);

  return (
    <CacheContext.Provider value={value}>
      {children}
    </CacheContext.Provider>
  );
};

```

**Q39: How does Context interact with React Suspense?**
A: Suspense can suspend rendering during Context updates. This keeps the old UI visible while preparing new values.

**Q40: Design a Context-based testing utility.**
A:

```typescript
const TestWrapper = ({ children, contextValue }: { children: React.ReactNode; contextValue: any }) => {
  return (
    <ThemeContext.Provider value={contextValue}>
      {children}
    </ThemeContext.Provider>
  );
};

render(<Component />, { wrapper: TestWrapper });

```

### Follow-ups (5-10)

**Q41: How would you explain Context to a junior developer?**
A: "Context is like a walkie-talkie system. Instead of passing notes through people (props), you broadcast on a channel (Provider). Anyone with a walkie-talkie tuned to that channel (Consumer) can hear the message directly."

**Q42: What are the edge cases in Context?**
A:

- Missing Provider (uses default value)
- Value changes causing all consumers to re-render
- Circular dependencies between contexts
- Context updates during render

**Q43: How does Context handle the "context update" problem?**
A: Context updates when Provider value changes. All consumers re-render. Memoize value to prevent unnecessary updates.

**Q44: What is the relationship between Context and React DevTools?**
A: React DevTools shows Context values and consumer updates. It's essential for debugging Context-related issues.

**Q45: How does Context interact with React StrictMode?**
A: StrictMode double-renders in development. Context persists across double-renders, so it's not affected.

**Q46: What is the future of Context in React?**
A: React is exploring:

- Better concurrent rendering support
- Improved performance
- Better DevTools integration
- Automatic splitting

**Q47: How would you implement Context-based i18n?**
A:

```typescript
const I18nContext = createContext<I18nContextType | null>(null);

const I18nProvider = ({ children }: { children: React.ReactNode }) => {
  const [locale, setLocale] = useState('en');
  const [translations, setTranslations] = useState<Record<string, string>>({});

  useEffect(() => {
    import(`../locales/${locale}.json`).then(setTranslations);
  }, [locale]);

  const t = useCallback((key: string) => {
    return translations[key] || key;
  }, [translations]);

  const value = useMemo(() => ({ locale, t, setLocale }), [locale, t]);

  return (
    <I18nContext.Provider value={value}>
      {children}
    </I18nContext.Provider>
  );
};

```

**Q48: How does Context handle the "derived context" pattern?**
A: Compute derived values during render:

```typescript
const ThemeContext = createContext('light');
const DarkThemeContext = createContext(false);

const App = () => {
  const theme = useContext(ThemeContext);
  const isDark = theme === 'dark';

  return (
    <DarkThemeContext.Provider value={isDark}>
      {children}
    </DarkThemeContext.Provider>
  );
};

```

**Q49: What is the relationship between Context and React.memo?**
A: `React.memo` prevents re-renders when props haven't changed. Context updates bypass `React.memo` — consumers always re-render.

**Q50: How would you implement Context-based form validation?**
A:

```typescript
const FormContext = createContext<FormContextType | null>(null);

const FormProvider = ({ children }: { children: React.ReactNode }) => {
  const [values, setValues] = useState({});
  const [errors, setErrors] = useState({});

  const validate = useCallback(() => {
    const newErrors = validateForm(values);
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }, [values]);

  const value = useMemo(() => ({
    values,
    errors,
    setValues,
    validate,
  }), [values, errors, validate]);

  return (
    <FormContext.Provider value={value}>
      {children}
    </FormContext.Provider>
  );
};

```

## Summary

Context API is React's built-in solution for sharing data across the component tree without prop drilling. It's ideal for global data like themes, authentication, and language. Performance can be optimized by memoizing context values and splitting contexts by concern.

## Cheat Sheet

```text
Context API Key Points:
├── What: Share data across component tree without prop drilling
├── Parts: Context Object, Provider, Consumer
├── Create: React.createContext(defaultValue)
├── Provide: <Context.Provider value={value}>
├── Consume: useContext(Context)
├── Performance: Memoize value, split contexts

When to Use:
├── Theme (light/dark mode)
├── Authentication state
├── Language/locale
├── Shopping cart
├── Any data needed by many components

When NOT to Use:
├── Component-specific state (use useState)
├── Complex state management (use Redux/Zustand)
├── Performance-critical updates (use local state)

Performance:
├── Memoize Provider value with useMemo
├── Split contexts by concern
├── Use useTransition for non-urgent updates
├── Memoize consumer components with React.memo
└── Context updates bypass React.memo

Common Mistakes:
├── Not memoizing context value
├── Creating context inside components
├── Not providing error handling
├── Overusing context for local state
└── Creating large, monolithic contexts

Best Practices:
├── Memoize context value
├── Create context outside components
├── Provide error handling in custom hooks
├── Split contexts by concern
├── Use custom hooks for consumption
├── Provide meaningful default values
└── Don't overuse context

Relationships:
├── Context vs Redux: Simple vs complex state
├── Context vs props: Global vs local data
├── Context vs state: Shared vs component-specific
└── Context + React.memo: Context bypasses memo

```

## References & Learn More

- [React Docs: Context](https://react.dev/learn/passing-data-deeply-with-context)
- [React Context API Guide](https://www.freecodecamp.org/news/context-api-in-react/)
- [When to Use Context API vs Redux](https://www.robinwieruch.de/react-context-redis/)
