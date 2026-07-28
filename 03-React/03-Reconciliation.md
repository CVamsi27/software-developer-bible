# Reconciliation

[![Category: Frontend](https://img.shields.io/badge/category-Frontend-00b4d8)](.)

s of the Virtual DOM need to be created, updated, or destroyed when state or props change. It's the algorithm that compares the new Virtual DOM tree with the previous one and computes the minimal set of changes needed to update the real DOM. Reconciliation is also commonly called "diffing."

Reconciliation is central to React's performance model. Without it, every state change would require re-rendering the entire application from scratch, which would be prohibitively slow.

## Why Do We Need It?

### The Problem

When a component's state changes, React needs to figure out:

1. Which components need to re-render

2. What changed between the old and new UI

3. How to update the real DOM efficiently

### Naive Approach (O(n³))

A "perfect" tree diff algorithm would:

1. Compare every node in the old tree with every node in the new tree: O(n²)

2. Find the minimum number of operations to transform one tree to another: O(n³)

For a 1,000-node tree, that's 1,000,000,000 operations. Too slow for real-time UIs.

### React's Approach (O(n))

React makes two key assumptions that reduce complexity to O(n):

1. **Different node types produce different trees**: If a `<div>` changes to a `<span>`, React destroys the old subtree and creates a new one.

2. **Keys identify stable elements**: The `key` prop tells React which elements have moved, been added, or removed.

```text
Reconciliation Complexity Comparison:
═══════════════════════════════════════════════════════════════

Naive Algorithm:
┌─────────────────────────────────────────┐
│ Compare ALL nodes: O(n²)               │
│ Find min operations: O(n³)             │
│ 1,000 nodes → 1,000,000,000 operations │
│ Too slow for real-time UIs             │
└─────────────────────────────────────────┘

React's Algorithm:
┌─────────────────────────────────────────┐
│ Traverse tree once: O(n)               │
│ Heuristics skip unnecessary comparisons│
│ 1,000 nodes → 1,000 operations         │
│ Fast enough for real-time UIs          │
└─────────────────────────────────────────┘

```

## How It Works

### The Three-Level Diff

React's reconciliation operates at three levels:

```text
Reconciliation Levels:
═══════════════════════════════════════════════════════════════

Level 1: Tree Diff
┌─────────────────────────────────────────────────────────┐
│ Compare trees at the top level                          │
│                                                         │
│ Old Tree:        New Tree:                              │
│ ┌─────┐          ┌─────┐                               │
│ │ App │          │ App │ ← Same type, continue         │
│ └──┬──┘          └──┬──┘                               │
│    │                │                                   │
│  ┌─┴─┐            ┌─┴─┐                                │
│  │ A │            │ B │ ← Different type → REPLACE     │
│  └───┘            └───┘                                │
│                                                         │
│ Heuristic: Different types = destroy old subtree       │
└─────────────────────────────────────────────────────────┘

Level 2: Component Diff
┌─────────────────────────────────────────────────────────┐
│ Compare component instances                             │
│                                                         │
│ Same component type?                                    │
│ YES → Update props, keep instance                       │
│ NO  → Unmount old, mount new                           │
│                                                         │
│ Example:                                                │
│ <UserProfile user={user1} /> → <UserProfile user={user2} /> │
│ Same type → Update props only                          │
│                                                         │
│ <UserProfile /> → <UserProfileCard />                  │
│ Different type → Unmount, mount new                    │
└─────────────────────────────────────────────────────────┘

Level 3: Element Diff
┌─────────────────────────────────────────────────────────┐
│ Compare child elements                                  │
│                                                         │
│ Same type? Update attributes                            │
│ Different type? Replace node                            │
│ Key changed? Unmount old, mount new                     │
│                                                         │
│ <div key="1">A</div> → <div key="1">B</div>            │
│ Same key + same type → Update textContent              │
│                                                         │
│ <div key="1">A</div> → <span key="1">A</span>          │
│ Same key + different type → Replace node               │
└─────────────────────────────────────────────────────────┘

```

### Reconciliation Algorithm in Detail

```typescript
// Simplified reconciliation algorithm
function reconcileChildren(
  fiber: FiberNode,
  children: ReactNode[],
) {
  const existingChildren = mapRemainingChildren(fiber.child);
  let newFirstChild: FiberNode | null = null;
  let previousNewFiber: FiberNode | null = null;

  for (let i = 0; i < children.length; i++) {
    const child = children[i];
    const key = child.key !== null ? child.key : i;

    // Try to match with existing fiber
    let matchedFiber = existingChildren.get(key);

    if (matchedFiber) {
      // Same key found: update or replace
      if (matchedFiber.element.type === child.type) {
        // Same type: update props
        updateFiberProps(matchedFiber, child.props);
      } else {
        // Different type: replace
        matchedFiber = createFiberFromElement(child);
      }
      existingChildren.delete(key);
    } else {
      // New element: create fiber
      matchedFiber = createFiberFromElement(child);
    }

    // Build fiber linked list
    if (previousNewFiber === null) {
      newFirstChild = matchedFiber;
    } else {
      previousNewFiber.sibling = matchedFiber;
    }
    previousNewFiber = matchedFiber;
  }

  // Delete remaining old fibers
  for (const [key, fiber] of existingChildren) {
    deleteRemainingChildren(fiber);
  }

  return newFirstChild;
}

```

### Key Prop: The Secret Sauce

The `key` prop is the most critical part of reconciliation for list rendering:

```text
Key Prop Behavior:
═══════════════════════════════════════════════════════════════

Without Keys (index-based):
Old: [A, B, C] (indices: 0, 1, 2)
New: [D, A, B, C] (indices: 0, 1, 2, 3)

React compares by index:
Index 0: A → D (update text)
Index 1: B → A (update text)
Index 2: C → B (update text)
Index 3: new → C (create)

Result: ALL items re-rendered, even though only D was added!

With Keys (stable IDs):
Old: [A(id:1), B(id:2), C(id:3)]
New: [D(id:4), A(id:1), B(id:2), C(id:3)]

React compares by key:
Key 1: A → A (no change)
Key 2: B → B (no change)
Key 3: C → C (no change)
Key 4: new → D (create)

Result: Only D is created, A/B/C are reused!

```

### ASCII Diagram: Full Reconciliation Flow

```text
Full Reconciliation Flow:
═══════════════════════════════════════════════════════════════

State Change
     │
     ▼
┌─────────────────┐
│ Render Phase     │
│ (Create new VDOM)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Reconcile        │
│ (Diff old vs new)│
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐ ┌───────┐
│ Same  │ │Different│
│ Type  │ │ Type   │
└───┬───┘ └───┬───┘
    │         │
    ▼         ▼
┌───────┐ ┌─────────┐
│ Update│ │ Unmount │
│ Props │ │ + Mount │
└───┬───┘ └────┬────┘
    │          │
    └────┬─────┘
         │
         ▼
┌─────────────────┐
│ Commit Phase     │
│ (Apply DOM changes)│
└─────────────────┘

```

## Code Examples

### Basic Reconciliation

```typescript
import React from 'react';

// React reconciles these changes:
const App = () => {
  const [count, setCount] = useState(0);

  return (
    <div>
      <h1>Count: {count}</h1>
      <button onClick={() => setCount(count + 1)}>+1</button>
    </div>
  );
  // When count changes:
  // 1. React creates new VDOM with updated h1 text
  // 2. Reconciles: div type same ✓, h1 type same ✓, text changed ✗
  // 3. Updates only the text node in the real DOM
};

```

### List Reconciliation with Keys

```typescript
// ❌ BAD: Using array index as key
const BadList = ({ items }: { items: string[] }) => (
  <ul>
    {items.map((item, index) => (
      <li key={index}>{item}</li>
      // If items reorder, React incorrectly matches old and new items
      // This causes unnecessary re-renders and potential bugs
    ))}
  </ul>
);

// ✅ GOOD: Using stable unique IDs
const GoodList = ({ items }: { items: { id: number; text: string }[] }) => (
  <ul>
    {items.map(item => (
      <li key={item.id}>{item.text}</li>
      // React correctly tracks items by ID
      // Reordering only moves DOM nodes, no re-renders
    ))}
  </ul>
);

```

### Conditional Rendering

```typescript
const ConditionalComponent = ({ showDetails }: { showDetails: boolean }) => (
  <div>
    {showDetails ? (
      <DetailsPanel />  // When true: mount DetailsPanel
    ) : (
      <SummaryPanel />  // When false: mount SummaryPanel
    )}
    {/* React reconciles by:

        1. Different component types (DetailsPanel vs SummaryPanel)

        2. Unmount old component

        3. Mount new component

        4. Run cleanup effects, then new effects */}
  </div>
);

```

### Key Changing Behavior

```typescript
const KeyExample = () => {
  const [activeTab, setActiveTab] = useState('tab1');

  return (
    <div>
      <TabBar
        tabs={['tab1', 'tab2', 'tab3']}
        active={activeTab}
        onChange={setActiveTab}
      />
      {/* Different key forces full unmount/mount */}
      {activeTab === 'tab1' && <Tab1Content key="tab1" />}
      {activeTab === 'tab2' && <Tab2Content key="tab2" />}
      {activeTab === 'tab3' && <Tab3Content key="tab3" />}
      {/* Each tab has a different key, so switching tabs
          completely unmounts the old and mounts the new */}
    </div>
  );
};

// Alternative: Same key, conditional rendering
const SameKeyExample = () => {
  const [activeTab, setActiveTab] = useState('tab1');

  return (
    <div>
      <TabBar tabs={['tab1', 'tab2', 'tab3']} active={activeTab} onChange={setActiveTab} />
      {/* Same key means React keeps the component instance */}
      <TabContent key="tab-content" tab={activeTab} />
    </div>
  );
};

```

### Fragment Reconciliation

```typescript
// Fragments help reconciliation by providing stable keys
const FragmentExample = ({ items }: { items: Item[] }) => (
  <>
    {items.map(item => (
      <Fragment key={item.id}>
        <dt>{item.term}</dt>
        <dd>{item.definition}</dd>
      </Fragment>
    ))}
  </>
  // Without Fragment keys, React would have trouble tracking
  // the dt/dd pairs when items are reordered
);

```

### Component Type Change

```typescript
const ComponentTypeChange = ({ useNewComponent }: { useNewComponent: boolean }) => (
  <div>
    {useNewComponent ? (
      <NewComponent />  // Different type from OldComponent
    ) : (
      <OldComponent />  // React unmounts OldComponent, mounts NewComponent
    )}
    {/* Even if NewComponent renders the same JSX,
        React treats it as a completely new component */}
  </div>
);

```

### Reconciliation with State

```typescript
const StateReconciliation = () => {
  const [items, setItems] = useState([
    { id: 1, text: 'First' },
    { id: 2, text: 'Second' },
  ]);

  // Adding an item at the beginning
  const addItem = () => {
    setItems([
      { id: 0, text: 'New First' },
      ...items,
    ]);
    // React reconciles:
    // 1. key 0: new → create New First
    // 2. key 1: First → First (no change)
    // 3. key 2: Second → Second (no change)
    // Only the new item is created and inserted
  };

  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>{item.text}</li>
      ))}
      <button onClick={addItem}>Add First</button>
    </ul>
  );
};

```

## Real-World Use Cases

### 1. Chat Application with Message List

```typescript
const ChatMessages = ({ messages }: { messages: Message[] }) => (
  <div className="chat-messages">
    {messages.map(message => (
      <MessageBubble
        key={message.id} // Stable ID ensures efficient updates
        message={message}
      />
    ))}
    {/* React efficiently:

        - Creates new messages only (no key matches)
        - Updates existing messages if edited
        - Removes deleted messages (unmatched keys)
        - Reorders if messages are sorted differently */}
  </div>
);

```

### 2. Dynamic Form with Conditional Fields

```typescript
const DynamicForm = ({ config }: { config: FormConfig }) => (
  <form>
    {config.fields.map(field => (
      <FormField key={field.id} field={field} />
    ))}
    {/* When config changes:

        - Same fields: update props
        - New fields: create components
        - Removed fields: unmount components
        - Reordered fields: move DOM nodes efficiently */}
  </form>
);

```

### 3. Table with Sorting and Filtering

```typescript
const DataTable = ({ data, sortKey, filterText }: DataTableProps) => {
  const filteredData = data
    .filter(row => row.name.includes(filterText))
    .sort((a, b) => a[sortKey] > b[sortKey] ? 1 : -1);

  return (
    <table>
      <tbody>
        {filteredData.map(row => (
          <tr key={row.id}>
            <td>{row.name}</td>
            <td>{row.value}</td>
          </tr>
        ))}
        {/* React efficiently handles:

            - Filtering: removes unmatched items
            - Sorting: reorders DOM nodes (keys stay same)
            - Data changes: updates only changed cells */}
      </tbody>
    </table>
  );
};

```

### 4. Tabs with Shared State

```typescript
const TabbedInterface = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [sharedData, setSharedData] = useState<SharedData>({});

  return (
    <div>
      <TabBar active={activeTab} onChange={setActiveTab} />
      {/* Using a key based on activeTab ensures each tab
          component is fully unmounted/mounted when switching */}
      <TabPanel key={activeTab} tab={activeTab} data={sharedData} />
    </div>
  );
};

```

## Common Mistakes

### 1. Using Array Index as Key

```typescript
// ❌ BAD: Array index as key
const BadTodoList = ({ todos }: { todos: Todo[] }) => (
  <ul>
    {todos.map((todo, index) => (
      <TodoItem key={index} todo={todo} />
    ))}
  </ul>
);

// Problem: If todos reorder, React matches wrong items
// Example:
// Old: [A(0), B(1), C(2)] (indices as keys)
// New: [C(0), A(1), B(2)] (reordered)
// React thinks: key 0 changed from A to C (update!)
//               key 1 changed from B to A (update!)
//               key 2 changed from C to B (update!)
// All items re-rendered unnecessarily!

```

### 2. Changing Key to Force Re-render

```typescript
// ❌ BAD: Using random keys to force re-render
const BadComponent = () => {
  const [, forceRender] = useState(0);

  return (
    <ExpensiveChild key={Math.random()} />
    // This completely destroys and recreates the child
    // Losing all state and effects
  );
};

// ✅ GOOD: Use key to intentionally reset state
const GoodComponent = ({ userId }: { userId: string }) => (
  <UserProfile key={userId} userId={userId} />
  // When userId changes, the profile resets
  // This is the correct use case for key-based reset
);

```

### 3. Not Providing Keys for Dynamic Lists

```typescript
// ❌ BAD: No key (React uses index, causes issues)
const NoKeyList = ({ items }: { items: string[] }) => (
  <ul>
    {items.map(item => (
      <li>{item}</li> // React warning: Each child needs a key
    ))}
  </ul>
);

// ✅ GOOD: Always provide keys
const GoodKeyList = ({ items }: { items: { id: string; text: string }[] }) => (
  <ul>
    {items.map(item => (
      <li key={item.id}>{item.text}</li>
    ))}
  </ul>
);

```

### 4. Misunderstanding Re-render Scope

```typescript
// ❌ BAD: Assuming reconciliation only affects changed component
const Parent = () => {
  const [count, setCount] = useState(0);

  console.log('Parent rendered'); // Logs on every count change

  return (
    <div>
      <h1>Count: {count}</h1>
      <button onClick={() => setCount(c => c + 1)}>+1</button>
      <Child /> {/* Child re-renders too, even though its props didn't change */}
    </div>
  );
};

// ✅ GOOD: Memoize children to prevent unnecessary re-renders
const Parent = () => {
  const [count, setCount] = useState(0);

  return (
    <div>
      <h1>Count: {count}</h1>
      <button onClick={() => setCount(c => c + 1)}>+1</button>
      <React.memo(Child) /> {/* Child only re-renders if props change */}
    </div>
  );
};

```

## Best Practices

1. **Always use stable, unique keys**: Never use array indices for reorderable lists.

2. **Use domain IDs as keys**: Database IDs, UUIDs, or other stable identifiers.

3. **Don't change key to force re-render**: Use state or context instead.

4. **Understand key-based reset**: Changing a key intentionally resets component state.

5. **Memoize expensive children**: Use `React.memo` to prevent unnecessary re-renders.

6. **Avoid inline objects/arrays in JSX**: They create new references each render.

7. **Profile before optimizing**: Use React DevTools Profiler to identify actual bottlenecks.

## Performance Considerations

### Reconciliation Cost Factors

| Factor | Impact | Mitigation |
|--------|--------|------------|
| Tree depth | Deeper trees take longer to traverse | Flatten component hierarchy |
| Node count | More nodes = more diffing | Virtualize long lists |
| Key stability | Stable keys = efficient updates | Use domain IDs |
| Component type changes | Forces subtree recreation | Avoid dynamic component types |
| State colocation | Less state = less re-rendering | Move state closer to usage |

### When Reconciliation Is Fast

- Most nodes haven't changed (early bail-out)
- Keys are stable and unique
- Component types remain the same
- Shallow prop comparisons succeed (`React.memo`)

### When Reconciliation Is Slow

- Frequent full-tree re-renders
- Unstable keys causing unnecessary unmounting
- Deep component hierarchies
- Many different component types changing

## Summary

Reconciliation is React's core algorithm that determines how to efficiently update the UI. By comparing Virtual DOM trees with O(n) complexity using heuristics (type comparison and keys), React minimizes expensive DOM operations. Understanding reconciliation is crucial for writing performant React applications.

## Cheat Sheet
```text
Reconciliation Key Points:
├── What: Process of diffing old and new Virtual DOM trees
├── Why: Minimize expensive DOM operations
├── How: O(n) algorithm with type and key heuristics
├── Three Levels: Tree diff → Component diff → Element diff
├── Keys: Enable stable element identity for efficient list updates
├── Type Change: Unmount old subtree, mount new subtree
├── Same Type: Update props, keep instance
├── Lists: Match by key, not index

Key Rules:
├── Always use stable, unique keys
├── Never use array indices for reorderable lists
├── Key change = full unmount + mount
├── Type change = full unmount + mount
├── Same type = update props only

Common Pitfalls:
├── Array index keys cause bugs on reorder
├── Changing key to force re-render loses state
├── Not providing keys causes React warnings
├── Inline objects/functions cause unnecessary re-renders
└── Deep nesting increases reconciliation time

Optimization Strategies:
├── React.memo: Skip subtree if props unchanged
├── useMemo: Memoize expensive computations
├── useCallback: Stabilize function references
├── Virtualization: Only render visible items
├── State colocation: Move state closer to usage
└── Key-based reset: Use key to intentionally reset state

```

---

## See Also
- [Animation](../30-Animation/)
- [Form Handling](../29-Form-Handling/)
- [JavaScript](../01-JavaScript/)
- [Next.js](../04-NextJS/)
- [Portals](17-Portals.md)
- [Testing](../16-Testing/)

## References & Learn More

- [React Docs: Reconciliation](https://react.dev/reference/react/Children)
- [React Reconciliation Algorithm](https://www.freecodecamp.org/news/react-reconciliation-algorithm/)
- [React Key Prop](https://react.dev/learn/rendering-lists#keeping-list-items-in-order-with-key)
