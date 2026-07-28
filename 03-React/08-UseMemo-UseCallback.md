[![Category: Frontend](https://img.shields.io/badge/category-Frontend-00b4d8)](.)

# useMemo & useCallback

## Definition

`useMemo` and `useCallback` are React Hooks for performance optimization through memoization. `useMemo` memoizes a **computed value** — it returns a cached result of an expensive computation. `useCallback` memoizes a **function** — it returns a cached reference to a function between re-renders.

Both hooks accept a dependency array and only re-compute/re-create when dependencies change.

## Why Do We Need It?

### The Problem

React re-renders components when state or props change. This can cause:

1. **Expensive computations** to run on every render

2. **New function references** to be created on every render

3. **Child components** to re-render unnecessarily (if functions/objects are passed as props)

### Example of the Problem

```typescript
// WITHOUT memoization:
const Parent = () => {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');

  // Expensive computation runs on every render
  const sortedItems = items.sort((a, b) => a.value - b.value);

  // New function reference on every render
  const handleClick = () => console.log('clicked');

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>+1</button>
      <input value={name} onChange={e => setName(e.target.value)} />
      {/* Child re-renders because handleClick is a new reference */}
      <ExpensiveChild onClick={handleClick} items={sortedItems} />
    </div>
  );
};

```

### The Solution

```typescript
// WITH memoization:
const Parent = () => {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');

  // Expensive computation only runs when items changes
  const sortedItems = useMemo(
    () => items.sort((a, b) => a.value - b.value),
    [items]
  );

  // Function reference stays the same across re-renders
  const handleClick = useCallback(() => console.log('clicked'), []);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>+1</button>
      <input value={name} onChange={e => setName(e.target.value)} />
      {/* Child only re-renders when sortedItems or handleClick changes */}
      <ExpensiveChild onClick={handleClick} items={sortedItems} />
    </div>
  );
};

```

## How It Works

### useMemo

```text
useMemo:
═══════════════════════════════════════════════════════════════

Syntax:
const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);

Behavior:
┌─────────────────────────────────────────────────────────────┐
│ First render:                                               │
│ - computeExpensiveValue(a, b) runs                          │
│ - Result cached                                             │
│ - memoizedValue = result                                    │
│                                                             │
│ Re-render (a or b changed):                                │
│ - computeExpensiveValue(a, b) runs again                    │
│ - New result cached                                         │
│ - memoizedValue = new result                                │
│                                                             │
│ Re-render (a and b same):                                  │
│ - computeExpensiveValue does NOT run                        │
│ - memoizedValue = cached result                             │
└─────────────────────────────────────────────────────────────┘

Memory Model:
┌─────────────────────────────────────────────────────────────┐
│ Fiber Node:                                                │
│ ├── memoizedState: [value, deps]                           │
│ │   ├── value: cached result                               │
│ │   └── deps: dependency array                             │
│ │                                                          │
│ On each render:                                            │
│ 1. Compare new deps with memoized deps                    │
│ 2. If same → return cached value                          │
│ 3. If different → run function, cache new value            │
└─────────────────────────────────────────────────────────────┘

```

### useCallback

```text
useCallback:
═══════════════════════════════════════════════════════════════

Syntax:
const memoizedFn = useCallback(() => {
  doSomething(a, b);
}, [a, b]);

Equivalent to:
const memoizedFn = useMemo(() => {
  return () => {
    doSomething(a, b);
  };
}, [a, b]);

Behavior:
┌─────────────────────────────────────────────────────────────┐
│ First render:                                               │
│ - Function created                                          │
│ - Function reference cached                                 │
│ - memoizedFn = function reference                           │
│                                                             │
│ Re-render (deps changed):                                  │
│ - New function created                                      │
│ - New reference cached                                      │
│ - memoizedFn = new function reference                       │
│                                                             │
│ Re-render (deps same):                                     │
│ - Function does NOT get recreated                           │
│ - memoizedFn = cached function reference                    │
└─────────────────────────────────────────────────────────────┘

```

### When to Use Each

```text
useMemo vs useCallback:
═══════════════════════════════════════════════════════════════

useMemo: Memoize VALUES
├── Expensive computations (sorting, filtering, parsing)
├── Derived state (computed from props/state)
├── Object/array references (prevent child re-renders)
└── Heavy calculations that shouldn't run every render

useCallback: Memoize FUNCTIONS
├── Event handlers passed as props
├── Callbacks passed to child components
├── Functions used in useEffect dependencies
└── Functions that shouldn't cause child re-renders

Example:
┌─────────────────────────────────────────────────────────────┐
│ const sortedItems = useMemo(                                │
│   () => items.sort((a, b) => a.value - b.value),           │
│   [items]                                                   │
│ );                                                          │
│ // useMemo: memoizes the SORTED ARRAY (value)              │
│                                                             │
│ const handleClick = useCallback(                            │
│   () => console.log('clicked'),                             │
│   []                                                        │
│ );                                                          │
│ // useCallback: memoizes the FUNCTION (reference)          │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### Basic useMemo

```typescript
import React, { useMemo, useState } from 'react';

const ExpensiveList = ({ items }: { items: Item[] }) => {
  const [filter, setFilter] = useState('');

  // Without useMemo: sorts on every render
  // const sortedItems = items.sort((a, b) => a.value - b.value);

  // With useMemo: only sorts when items changes
  const sortedItems = useMemo(
    () => [...items].sort((a, b) => a.value - b.value),
    [items]
  );

  const filteredItems = useMemo(
    () => sortedItems.filter(item =>
      item.name.toLowerCase().includes(filter.toLowerCase())
    ),
    [sortedItems, filter]
  );

  return (
    <div>
      <input value={filter} onChange={e => setFilter(e.target.value)} />
      <ul>
        {filteredItems.map(item => (
          <li key={item.id}>{item.name} - {item.value}</li>
        ))}
      </ul>
    </div>
  );
};

```

### Basic useCallback

```typescript
const TodoList = ({ todos }: { todos: Todo[] }) => {
  const [count, setCount] = useState(0);

  // Without useCallback: new function on every render
  // const handleToggle = (id: number) => toggleTodo(id);

  // With useCallback: stable function reference
  const handleToggle = useCallback((id: number) => {
    toggleTodo(id);
  }, []);

  const handleDelete = useCallback((id: number) => {
    deleteTodo(id);
  }, []);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>+1</button>
      {todos.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={handleToggle}
          onDelete={handleDelete}
        />
      ))}
    </div>
  );
};

// TodoItem with React.memo - only re-renders if props change
const TodoItem = React.memo(({ todo, onToggle, onDelete }: TodoItemProps) => {
  console.log(`TodoItem ${todo.id} rendered`);

  return (
    <div>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo.id)}
      />
      <span>{todo.text}</span>
      <button onClick={() => onDelete(todo.id)}>Delete</button>
    </div>
  );
});

```

### useMemo with Object References

```typescript
const Chart = ({ data, options }: { data: DataPoint[]; options: ChartOptions }) => {
  const [hoveredPoint, setHoveredPoint] = useState<DataPoint | null>(null);

  // Without useMemo: new object reference on every render
  // const chartConfig = { data, options, hoveredPoint };

  // With useMemo: stable object reference
  const chartConfig = useMemo(
    () => ({ data, options, hoveredPoint }),
    [data, options, hoveredPoint]
  );

  // Without useMemo: new function on every render
  // const handleHover = (point: DataPoint) => setHoveredPoint(point);

  // With useCallback: stable function reference
  const handleHover = useCallback((point: DataPoint) => {
    setHoveredPoint(point);
  }, []);

  return <D3Chart config={chartConfig} onHover={handleHover} />;
};

```

### useCallback with Dependencies

```typescript
const SearchComponent = ({ apiEndpoint }: { apiEndpoint: string }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Result[]>([]);

  // useCallback with dependencies
  const performSearch = useCallback(async (searchQuery: string) => {
    const response = await fetch(`${apiEndpoint}?q=${searchQuery}`);
    const data = await response.json();
    setResults(data.results);
  }, [apiEndpoint]); // Re-create when apiEndpoint changes

  useEffect(() => {
    if (query) {
      const timeoutId = setTimeout(() => {
        performSearch(query);
      }, 300);

      return () => clearTimeout(timeoutId);
    }
  }, [query, performSearch]);

  return (
    <div>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <ResultList results={results} />
    </div>
  );
};

```

### useMemo for Expensive Computation

```typescript
const DataVisualization = ({ rawData }: { rawData: RawDataPoint[] }) => {
  const [timeRange, setTimeRange] = useState('all');
  const [chartType, setChartType] = useState('line');

  // Expensive computation: process raw data for visualization
  const processedData = useMemo(() => {
    console.log('Processing data...'); // Only logs when dependencies change

    // Heavy computation: filter, aggregate, transform
    const filtered = rawData.filter(d =>
      timeRange === 'all' || d.timestamp >= Date.now() - timeRangeToMs(timeRange)
    );

    const aggregated = aggregateByTime(filtered);
    const transformed = transformForChart(aggregated, chartType);

    return transformed;
  }, [rawData, timeRange, chartType]); // Only re-compute when these change

  return (
    <div>
      <Controls
        timeRange={timeRange}
        chartType={chartType}
        onTimeRangeChange={setTimeRange}
        onChartTypeChange={setChartType}
      />
      <Chart data={processedData} />
    </div>
  );
};

```

## Real-World Use Cases

### 1. Memoized List Filtering

```typescript
const FilteredList = ({ items, query }: { items: Item[]; query: string }) => {
  const filteredItems = useMemo(() => {
    if (!query) return items;

    return items.filter(item =>
      item.name.toLowerCase().includes(query.toLowerCase()) ||
      item.description.toLowerCase().includes(query.toLowerCase())
    );
  }, [items, query]);

  return (
    <ul>
      {filteredItems.map(item => (
        <ListItem key={item.id} item={item} />
      ))}
    </ul>
  );
};

```

### 2. Memoized Event Handlers

```typescript
const DataTable = ({ data, columns }: DataTableProps) => {
  const [sortConfig, setSortConfig] = useState({ key: '', direction: 'asc' });

  const handleSort = useCallback((key: string) => {
    setSortConfig(prev => ({
      key,
      direction: prev.key === key && prev.direction === 'asc' ? 'desc' : 'asc',
    }));
  }, []);

  const handleRowClick = useCallback((row: Row) => {
    console.log('Row clicked:', row);
  }, []);

  const sortedData = useMemo(() => {
    if (!sortConfig.key) return data;

    return [...data].sort((a, b) => {
      if (a[sortConfig.key] < b[sortConfig.key]) {
        return sortConfig.direction === 'asc' ? -1 : 1;
      }
      if (a[sortConfig.key] > b[sortConfig.key]) {
        return sortConfig.direction === 'asc' ? 1 : -1;
      }
      return 0;
    });
  }, [data, sortConfig]);

  return (
    <table>
      <thead>
        <tr>
          {columns.map(col => (
            <th key={col.key} onClick={() => handleSort(col.key)}>
              {col.label} {sortConfig.key === col.key ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {sortedData.map(row => (
          <tr key={row.id} onClick={() => handleRowClick(row)}>
            {columns.map(col => (
              <td key={col.key}>{row[col.key]}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

```

### 3. Memoized Context Value

```typescript
const AppContext = React.createContext<AppContextType>(null!);

const AppProvider = ({ children }: { children: React.ReactNode }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const [user, setUser] = useState<User | null>(null);

  // Memoize context value to prevent unnecessary re-renders
  const contextValue = useMemo(
    () => ({
      theme,
      user,
      setTheme,
      setUser,
    }),
    [theme, user]
  );

  return (
    <AppContext.Provider value={contextValue}>
      {children}
    </AppContext.Provider>
  );
};

```

### 4. Memoized Animation Callbacks

```typescript
const AnimatedList = ({ items }: { items: Item[] }) => {
  const [animating, setAnimating] = useState(false);

  const handleAnimationComplete = useCallback(() => {
    setAnimating(false);
  }, []);

  const startAnimation = useCallback(() => {
    setAnimating(true);
  }, []);

  return (
    <div>
      <button onClick={startAnimation} disabled={animating}>
        Animate
      </button>
      <AnimatedItems
        items={items}
        animating={animating}
        onComplete={handleAnimationComplete}
      />
    </div>
  );
};

```

## Common Mistakes

### 1. Overusing useMemo/useCallback

```typescript
// ❌ BAD: Memoizing everything, even cheap computations
const Component = ({ a, b }: { a: number; b: number }) => {
  const sum = useMemo(() => a + b, [a, b]); // a + b is cheap!
  const name = useMemo(() => `User ${a}`, [a]); // String concatenation is cheap!
  const handleClick = useCallback(() => console.log('clicked'), []); // Simple function!

  return <div>{sum} - {name}</div>;
};

// ✅ GOOD: Only memoize expensive operations or when passing to memoized children
const Component = ({ a, b }: { a: number; b: number }) => {
  const sum = a + b; // Cheap, no memoization needed
  const name = `User ${a}`; // Cheap, no memoization needed
  const handleClick = useCallback(() => console.log('clicked'), []); // Needed if passed to memoized child

  return <div>{sum} - {name}</div>;
};

```

### 2. Wrong Dependency Array

```typescript
// ❌ BAD: Missing dependency
const Component = ({ items }: { items: Item[] }) => {
  const sorted = useMemo(() => items.sort((a, b) => a.value - b.value), []);
  // items not in deps! Will always use initial items
};

// ❌ BAD: Including unnecessary dependencies
const Component = ({ items }: { items: Item[] }) => {
  const sorted = useMemo(
    () => items.sort((a, b) => a.value - b.value),
    [items, items.length, items[0]] // Unnecessary deps
  );
};

// ✅ GOOD: Only include necessary dependencies
const Component = ({ items }: { items: Item[] }) => {
  const sorted = useMemo(
    () => [...items].sort((a, b) => a.value - b.value),
    [items] // Only items is needed
  );
};

```

### 3. Mutating Memoized Values

```typescript
// ❌ BAD: Mutating memoized array
const Component = ({ items }: { items: Item[] }) => {
  const sorted = useMemo(() => items.sort((a, b) => a.value - b.value), [items]);
  // items.sort mutates the original array!

  // ❌ BAD: Using memoized value incorrectly
  const handleClick = useCallback(() => {
    sorted.push(new Item()); // Mutating memoized value!
  }, [sorted]);
};

// ✅ GOOD: Create new arrays, don't mutate
const Component = ({ items }: { items: Item[] }) => {
  const sorted = useMemo(
    () => [...items].sort((a, b) => a.value - b.value),
    [items]
  );

  const handleClick = useCallback(() => {
    setItems(prev => [...prev, new Item()]); // Update state, not memoized value
  }, []);
};

```

### 4. Using useMemo/useCallback When React.memo Is Enough

```typescript
// ❌ BAD: Memoizing function that's not passed to memoized child
const Parent = () => {
  const [count, setCount] = useState(0);
  const handleClick = useCallback(() => console.log('clicked'), []); // Not needed!

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>+1</button>
      <button onClick={handleClick}>Click</button> {/* Not a memoized child */}
    </div>
  );
};

// ✅ GOOD: Only memoize when passing to memoized children
const Parent = () => {
  const [count, setCount] = useState(0);
  const handleClick = useCallback(() => console.log('clicked'), []); // Needed!

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>+1</button>
      <MemoizedChild onClick={handleClick} /> {/* Memoized child */}
    </div>
  );
};

```

## Best Practices

1. **Only memoize expensive computations**: Don't memoize cheap operations like `a + b`.

2. **Memoize when passing to memoized children**: Use `useCallback` for functions passed to `React.memo` children.

3. **Use `useMemo` for object/array references**: Prevent unnecessary re-renders of children.

4. **Always include correct dependencies**: Missing dependencies cause bugs.

5. **Don't mutate memoized values**: Create new arrays/objects instead.

6. **Profile before memoizing**: Use React DevTools Profiler to find actual bottlenecks.

7. **Consider React Compiler**: Future React versions may auto-memoize.

## Performance Considerations

### Memoization Overhead

| Operation | Cost | Benefit |
|-----------|------|---------|
| `useMemo` (cheap computation) | ~0.1ms | Minimal |
| `useMemo` (expensive computation) | ~10ms | Significant |
| `useCallback` | ~0.05ms | Prevents child re-renders |
| React.memo (child re-render) | ~1ms per child | Significant |

### When to Use

| Scenario | useMemo | useCallback |
|----------|---------|------------|
| Expensive computation | ✅ | ❌ |
| Object/array reference | ✅ | ❌ |
| Function passed to memoized child | ❌ | ✅ |
| Function in useEffect deps | ❌ | ✅ |
| Simple computation | ❌ | ❌ |

## Summary

`useMemo` and `useCallback` are performance optimization hooks that memoize computed values and functions. They prevent unnecessary re-computations and re-creations, which can prevent child re-renders when combined with `React.memo`. Use them for expensive computations and functions passed to memoized children.

## Cheat Sheet
```text
useMemo/useCallback Key Points:
├── useMemo: Memoizes computed values
├── useCallback: Memoizes functions
├── Both: Prevent unnecessary re-computations/re-creations
├── Dependencies: Control when to re-compute/re-create
└── Overhead: Only use when beneficial

When to Use:
├── useMemo: Expensive computations, object/array references
├── useCallback: Functions passed to memoized children
├── Don't use: Cheap operations, simple computations
└── Profile before: Use React DevTools Profiler

Common Mistakes:
├── Overusing (memoizing everything)
├── Wrong dependencies (missing or extra)
├── Mutating memoized values
├── Using when React.memo is enough
└── Not profiling before memoizing

Performance:
├── useMemo: Prevents expensive re-computations
├── useCallback: Prevents child re-renders
├── React.memo: Prevents component re-renders
├── State colocation: Reduces re-render scope
└── React Compiler: Automatic memoization

Best Practices:
├── Only memoize expensive computations
├── Memoize when passing to memoized children
├── Use correct dependency arrays
├── Don't mutate memoized values
├── Profile before memoizing
├── Consider React Compiler
└── Don't over-memoize

Relationships:
├── useMemo + React.memo = Prevent child re-renders
├── useCallback + React.memo = Prevent child re-renders
├── useMemo + state colocation = Optimize performance
└── React Compiler = Automatic memoization

```

---

## See Also
- [Animation](../30-Animation/)
- [Custom Hooks](16-Custom-Hooks.md)
- [Form Handling](../29-Form-Handling/)
- [JavaScript](../01-JavaScript/)
- [Next.js](../04-NextJS/)
- [Testing](../16-Testing/)

## References & Learn More

- [React Docs: useMemo](https://react.dev/reference/react/useMemo)
- [React Docs: useCallback](https://react.dev/reference/react/useCallback)
- [When to useMemo and useCallback](https://react.dev/reference/react/useMemo#when-to-use-usememo)
- [Kent C. Dodds: When to useMemo and useCallback](https://kentcdodds.com/blog/usememo-and-usecallback)
