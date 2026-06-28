# Reconciliation

## Definition

Reconciliation is the process by which React determines which parts of the Virtual DOM need to be created, updated, or destroyed when state or props change. It's the algorithm that compares the new Virtual DOM tree with the previous one and computes the minimal set of changes needed to update the real DOM. Reconciliation is also commonly called "diffing."

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

## Interview Questions

### Beginner (5-10)

**Q1: What is reconciliation in React?**
A: Reconciliation is the process by React compares the new Virtual DOM tree with the previous one to determine what needs to change in the real DOM. It's React's diffing algorithm that computes the minimal set of DOM operations.

**Q2: Why does React use reconciliation?**
A: Direct DOM manipulation is expensive. Reconciliation allows React to compute minimal changes and batch DOM updates, making UI updates efficient even with frequent state changes.

**Q3: What is the key prop's role in reconciliation?**
A: The `key` prop helps React identify which list items have changed, been added, or been removed. Without keys, React uses element index for comparison, which breaks when lists are reordered.

**Q4: What is the O(n) complexity in reconciliation?**
A: React's reconciliation algorithm runs in O(n) time complexity by making two assumptions: (1) different component types produce different trees, and (2) keys identify stable elements. This is much faster than a true O(n³) tree diff.

**Q5: What happens when a component's type changes?**
A: React unmounts the old component (destroying its state and DOM) and mounts a new one. This is a complete replacement, not an update.

**Q6: Can you force a re-render without state change?**
A: Yes, using `forceUpdate()` in class components or by changing the key prop. However, `forceUpdate()` is generally discouraged in favor of proper state management.

**Q7: What is the difference between reconciliation and rendering?**
A: Reconciliation determines what changes are needed (diffing Virtual DOM). Rendering applies those changes to the DOM (commit phase). They are separate phases in React's update cycle.

**Q8: How does React handle conditional rendering?**
A: React compares the type of element being rendered. If the type changes (e.g., from `<div>` to `<span>`), React destroys the old subtree and creates a new one. If the type stays the same, React updates attributes.

**Q9: What is the difference between `key` and `id`?**
A: `key` is a special React prop used for reconciliation. `id` is a regular HTML attribute. While they often have the same value, they serve different purposes. React uses `key` for tracking; browsers use `id` for DOM querying.

**Q10: How does React know when to re-render?**
A: React re-renders when: (1) component state changes, (2) parent component re-renders (unless memoized), (3) context value changes, or (4) force update is called.

### Intermediate (5-10)

**Q11: Explain the three levels of diffing in reconciliation.**
A:
1. **Tree Diff**: Different component types → destroy old subtree, create new
2. **Component Diff**: Same type → update props, keep instance
3. **Element Diff**: Same type → update attributes; different type → replace node

**Q12: Why are array indices bad keys?**
A: When list items reorder, array indices change. React matches items by index, so it incorrectly thinks items have changed when they've only moved. This causes unnecessary re-renders and can cause bugs with component state.

**Q13: How does reconciliation handle component state?**
A: When a component type changes, React unmounts the old instance (losing all state) and mounts a new one (fresh state). When the type stays the same, React keeps the instance and updates props.

**Q14: What is the impact of deep nesting on reconciliation?**
A: Deep nesting increases traversal time because React must walk the entire tree. Each level adds overhead. For very deep trees (50+ levels), consider flattening the hierarchy.

**Q15: How does `React.memo` affect reconciliation?**
A: `React.memo` adds a shallow comparison check before reconciliation. If props haven't changed, React skips the entire subtree, avoiding unnecessary Virtual DOM creation and diffing.

**Q16: What is the difference between `key` and `ref` in reconciliation?**
A: `key` helps React track element identity for efficient updates. `ref` provides direct access to the DOM node or component instance. Keys are used during reconciliation; refs are used after commit.

**Q17: How does reconciliation handle fragments?**
A: Fragments are transparent to reconciliation. React treats the fragment's children as direct children of the parent. Fragment keys help React track the children when the fragment itself is in a list.

**Q18: What is the "reconciliation key" concept?**
A: The reconciliation key is the `key` prop that React uses to match elements across renders. It's how React knows which elements have been added, removed, or reordered.

**Q19: How does React handle list reordering?**
A: With stable keys, React efficiently reorders by moving DOM nodes. Without keys (or with index keys), React updates all items, causing unnecessary re-renders and potential state bugs.

**Q20: What happens when a key changes?**
A: React treats the component with the new key as completely new. It unmounts the old component (running cleanup effects) and mounts a new one (running new effects). All state is lost.

### Senior (10-15)

**Q21: Explain the complete reconciliation algorithm step by step.**
A:
1. Compare root elements by type
2. If same type: update props, recurse into children
3. If different type: unmount old subtree, mount new subtree
4. For lists: use keys to match elements
5. Matched elements: update if props changed
6. Unmatched old elements: unmount
7. New elements: mount
8. Recurse through all children depth-first

**Q22: How does React handle the "cross-level" mutation problem?**
A: React assumes components don't move across different tree levels. If a component moves from level 2 to level 3, React destroys it and creates a new one. This is an O(n) trade-off that avoids expensive cross-level comparison.

**Q23: What is the `shouldComponentUpdate` optimization and how does it relate to reconciliation?**
A: `shouldComponentUpdate` is called during the begin phase. If it returns `false`, React skips the entire subtree. This is a manual optimization that prevents unnecessary reconciliation of the component's children.

**Q24: How does React handle the "sibling swap" problem?**
A: Without keys, React compares siblings by index. Swapping siblings causes React to update both, even though only their positions changed. With stable keys, React detects the swap and moves DOM nodes instead.

**Q25: Explain the trade-offs between reconciliation speed and accuracy.**
A: React prioritizes speed over perfect accuracy:
- Assumes different types = different trees (may miss moves)
- Assumes keys are stable (breaks with dynamic keys)
- O(n) instead of O(n³) (misses some optimizations)
Trade-off is worth it because these edge cases are rare.

**Q26: How does reconciliation interact with concurrent rendering?**
A: During concurrent rendering, React can create multiple Virtual DOM trees. Reconciliation happens for each tree, but React can pause and resume. The commit phase applies all reconciled changes atomically.

**Q27: What is the "single child" optimization?**
A: When a component has a single child, React can skip some reconciliation steps. It directly compares the old and new child without list matching. This is faster than multi-child reconciliation.

**Q28: How does React handle the "conditional rendering" pattern?**
A: React compares the type of element at each conditional branch. If the condition changes the element type, React unmounts the old and mounts the new. If the type stays the same, React updates props.

**Q29: What is the impact of `React.memo` on reconciliation performance?**
A: `React.memo` prevents unnecessary subtree reconciliation. For a component with 1000 children, skipping reconciliation saves:
- Virtual DOM creation: ~1000 objects
- Diffing: ~1000 comparisons
- Potential DOM updates: 0 (no changes)

**Q30: How does React handle the "list key collision" problem?**
A: If two elements have the same key, React treats them as the same element. This causes unpredictable behavior: one element is updated, the other is orphaned. Always ensure keys are unique within their list.

### FAANG-style (5-10)

**Q31: Design a reconciliation strategy for a virtualized list with 100,000 items.**
A:
1. **Virtualization**: Only render visible items (~50 at a time)
2. **Stable keys**: Use database IDs, not indices
3. **Memoization**: `React.memo` for item components
4. **State design**: Store only visible item data
5. **Lazy loading**: Load items as user scrolls
6. **Pagination**: Load data in pages

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

const VirtualList = ({ items }: { items: Item[] }) => {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
    overscan: 10,
  });

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div style={{ height: virtualizer.getTotalSize(), position: 'relative' }}>
        {virtualizer.getVirtualItems().map(virtualRow => (
          <ListItem key={items[virtualRow.index].id} item={items[virtualRow.index]} />
        ))}
      </div>
    </div>
  );
};
```

**Q32: How would you implement a custom reconciliation algorithm?**
A:
1. **Define fiber nodes**: Create your own node structure
2. **Implement diffing**: Compare old and new trees
3. **Handle updates**: Create, update, delete nodes
4. **Commit changes**: Apply to target platform (DOM, Canvas, etc.)
5. **Integration**: Use `react-reconciler` package

```typescript
// Conceptual custom reconciler
const HostConfig = {
  createInstance(type: string, props: Record<string, any>) {
    return createNode(type, props);
  },
  appendChild(parent: Node, child: Node) {
    parent.appendChild(child);
  },
  removeChild(parent: Node, child: Node) {
    parent.removeChild(child);
  },
  // ... other methods
};

const CustomReconciler = createReconciler(HostConfig);
```

**Q33: Analyze the performance impact of wrong keys in a production app.**
A:
- **Memory**: Each re-render creates new Virtual DOM nodes
- **CPU**: Unnecessary diffing and DOM updates
- **DOM**: Excessive insertions, deletions, and updates
- **State**: Component state incorrectly preserved or lost
- **Real example**: A todo list with 1000 items and index keys causes ~1000 unnecessary DOM updates on every reorder

**Q34: How would you benchmark reconciliation performance?**
A:
1. **React Profiler**: Measure render and commit times
2. **Chrome DevTools Performance**: Record and analyze flame charts
3. **Custom benchmarks**: Use `React.Profiler` with `onRender` callback
4. **Memory profiling**: Heap snapshots to track Virtual DOM memory
5. **Comparison tests**: Compare different key strategies

**Q35: Design a reconciliation-aware state management system.**
A:
1. **Normalize state**: Store data in flat, normalized structures
2. **Stable references**: Use IDs, not object references
3. **Selective updates**: Update only changed entities
4. **Batching**: Group related state changes
5. **Memoization**: Cache derived data

**Q36: How does React handle the "dynamic component type" pattern?**
A:
```typescript
const DynamicComponent = ({ type }: { type: string }) => {
  const Component = getComponent(type);
  return <Component />;
  // When type changes:
  // 1. getComponent returns different component
  // 2. React unmounts old component, mounts new
  // 3. All state is lost
  // This is correct behavior for dynamic components
};
```

**Q37: Explain the reconciliation implications of React Server Components.**
A: Server Components don't participate in client-side reconciliation. They're serialized as a reference tree. Client Components reconcile normally. React merges the server and client trees, reconciling only the client parts.

**Q38: How would you optimize reconciliation for a real-time collaborative app?**
A:
1. **CRDT-based state**: Conflict-free replicated data types
2. **Incremental updates**: Only send changed data
3. **Operational transformation**: Transform operations across clients
4. **Virtualization**: Only render visible collaboration elements
5. **Priority updates**: User's own changes > remote changes

**Q39: Analyze the memory implications of reconciliation for large component trees.**
A:
- **Per component**: ~1-2KB for fiber node
- **Virtual DOM**: ~2x memory for old + new trees
- **Large app**: 10,000 components → ~20-40MB
- **Mitigation**: Virtualization, unmounting, state cleanup
- **Monitoring**: Chrome DevTools Memory tab

**Q40: How would you design a reconciliation system for a non-React framework?**
A:
1. **Define update model**: How state changes trigger UI updates
2. **Virtual representation**: Create in-memory UI tree
3. **Diffing algorithm**: Compare old and new trees
4. **Patching strategy**: Apply minimal DOM changes
5. **Scheduling**: Prioritize updates, batch changes
6. **Error handling**: Graceful degradation on failures

### Follow-ups (5-10)

**Q41: How would you explain reconciliation to a non-technical person?**
A: "When you change something on a website, React doesn't rebuild the entire page. Instead, it compares what the page looked like before and after your change, and only updates the parts that actually changed. This is like editing a document — you don't rewrite the whole thing, just the parts that need to change."

**Q42: What are the edge cases in reconciliation?**
A:
- Conditional fragments with different structures
- Dynamic component types
- Portal rendering (breaks tree structure)
- Suspense boundaries
- Error boundaries catching during reconciliation

**Q43: How does reconciliation handle the "key change" edge case?**
A: When a key changes, React treats it as a completely new element. It unmounts the old component (losing state, running cleanup) and mounts a new one (fresh state, running effects). This is intentional — keys identify component identity.

**Q44: Can reconciliation cause memory leaks?**
A: Reconciliation itself doesn't cause memory leaks, but improper cleanup in components can. When React unmounts a component during reconciliation, it runs cleanup effects. If cleanup is missing (e.g., event listeners, subscriptions), memory leaks occur.

**Q45: How does React handle the "list mutation" problem?**
A: React expects lists to be treated as immutable. If you mutate a list (e.g., `array.push()`), React may not detect the change because the array reference is the same. Always create new arrays when updating lists.

**Q46: What is the relationship between reconciliation and React DevTools?**
A: React DevTools uses reconciliation internals to display the component tree. It shows fiber nodes, their props, state, and why they re-rendered. The Profiler uses reconciliation timing data to measure performance.

**Q47: How would you test reconciliation behavior?**
A:
1. **Unit tests**: Test component rendering with different props
2. **Integration tests**: Test component interactions
3. **Visual regression tests**: Compare screenshots before/after changes
4. **Performance tests**: Measure render times with React Profiler
5. **Edge case tests**: Test key changes, conditional rendering, etc.

**Q48: How does reconciliation handle the "deep comparison" problem?**
A: React uses shallow comparison by default. Deep comparison is expensive. For complex objects, use:
- `React.memo` with custom comparator
- `useMemo` to memoize expensive computations
- Normalized state to reduce comparison depth

**Q49: What is the impact of React strict mode on reconciliation?**
A: StrictMode intentionally double-renders components in development. This helps detect side effects in the render phase (which should be idempotent). It doesn't affect production reconciliation.

**Q50: How would you design a debugging tool for reconciliation?**
A:
1. **Visualization**: Show Virtual DOM tree before/after changes
2. **Diff highlighting**: Color-code created, updated, deleted nodes
3. **Timeline**: Show reconciliation steps over time
4. **Performance metrics**: Render time, commit time, DOM operations
5. **Key analysis**: Show which keys matched, which didn't

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

## References & Learn More

- [React Docs: Reconciliation](https://react.dev/reference/react/Children)
- [React Reconciliation Algorithm](https://www.freecodecamp.org/news/the-new-react-algorithm-in-/)
- [React Key Prop](https://react.dev/learn/rendering-lists#keeping-list-items-in-order-with-key)
