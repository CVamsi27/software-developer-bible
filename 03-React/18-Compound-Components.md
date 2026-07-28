# Compound Components

[![Category: Frontend](https://img.shields.io/badge/category-Frontend-00b4d8)](.)

ts work together implicitly by sharing implicit state through React Context or `React.Children` utilities. A parent component manages shared state and exposes child components that automatically wire into that state — similar to HTML `<select>` and `<option>` elements. Popular examples include `<Tabs.Tab />`, `<Accordion.Panel />`, and `<Menu.Item />`.

## Why Do We Need It?

1. **Declarative API** — Components express intent through structure: `<Tabs><Tab label="A">...</Tab></Tabs>`
2. **Implicit state sharing** — Children automatically get parent state without manual prop drilling
3. **Flexible layout** — Consumers control component structure, ordering, and wrapping
4. **Clean composition** — Related components are naturally grouped and namespaced
5. **Type safety** — Only valid compound children can be used inside parent components

## How It Works

### State Sharing via Context

```text
Compound Components Architecture:
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│                    COMPOUND COMPONENT                         │
│                                                              │
│  <Tabs> ← Parent manages active state via Context           │
│  ├── <TabList> ← Receives active index, renders tabs        │
│  │   ├── <Tab index={0}> ← Highlighted if active           │
│  │   └── <Tab index={1}>                                    │
│  └── <TabPanels> ← Shows the active panel                  │
│      ├── <TabPanel> ← Only visible if active               │
│      └── <TabPanel>                                         │
│                                                              │
│  Data Flow:                                                  │
│  ┌─────────────┐         ┌─────────────┐                   │
│  │  Tabs       │──Context──▶ TabList     │                   │
│  │  (state:    │         │ (reads:      │                   │
│  │   activeIdx)│         │  activeIndex)│                   │
│  └──────┬──────┘         └─────────────┘                   │
│         │                                                   │
│         │ Context                                            │
│         ▼                                                   │
│  ┌─────────────┐         ┌─────────────┐                   │
│  │  Tab        │         │  TabPanel   │                   │
│  │ (reads:     │         │ (reads:     │                   │
│  │  activeIndex│         │  activeIndex)│                   │
│  │  + onClick) │         │  + shows if │                   │
│  └─────────────┘         │  match)     │                   │
│                          └─────────────┘                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### 1. Tabs with Context

```typescript
import React, { createContext, useContext, useState, useCallback, useMemo } from 'react';

// ─── Context ─────────────────────────────────────────────────

interface TabsContextType {
  activeIndex: number;
  setActiveIndex: (index: number) => void;
}

const TabsContext = createContext<TabsContextType | null>(null);

const useTabsContext = () => {
  const context = useContext(TabsContext);
  if (!context) throw new Error('Tabs compound components must be used within Tabs');
  return context;
};

// ─── Tabs Parent ─────────────────────────────────────────────

interface TabsProps {
  defaultIndex?: number;
  children: React.ReactNode;
}

const Tabs = ({ defaultIndex = 0, children }: TabsProps) => {
  const [activeIndex, setActiveIndex] = useState(defaultIndex);

  const value = useMemo(
    () => ({ activeIndex, setActiveIndex }),
    [activeIndex]
  );

  return (
    <TabsContext.Provider value={value}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
};

// ─── TabList ─────────────────────────────────────────────────

const TabList = ({ children }: { children: React.ReactNode }) => (
  <div className="tab-list" role="tablist">{children}</div>
);

// ─── Tab ─────────────────────────────────────────────────────

interface TabProps {
  index: number;
  children: React.ReactNode;
}

const Tab = ({ index, children }: TabProps) => {
  const { activeIndex, setActiveIndex } = useTabsContext();

  return (
    <button
      role="tab"
      aria-selected={activeIndex === index}
      className={activeIndex === index ? 'tab tab--active' : 'tab'}
      onClick={() => setActiveIndex(index)}
    >
      {children}
    </button>
  );
};

// ─── TabPanels ───────────────────────────────────────────────

const TabPanels = ({ children }: { children: React.ReactNode }) => (
  <div className="tab-panels">{children}</div>
);

// ─── TabPanel ────────────────────────────────────────────────

interface TabPanelProps {
  index: number;
  children: React.ReactNode;
}

const TabPanel = ({ index, children }: TabPanelProps) => {
  const { activeIndex } = useTabsContext();

  if (activeIndex !== index) return null;

  return (
    <div role="tabpanel" className="tab-panel">
      {children}
    </div>
  );
};

// Attach compound children
Tabs.TabList = TabList;
Tabs.Tab = Tab;
Tabs.TabPanels = TabPanels;
Tabs.TabPanel = TabPanel;

// ─── Usage ───────────────────────────────────────────────────

const App = () => (
  <Tabs defaultIndex={0}>
    <Tabs.TabList>
      <Tabs.Tab index={0}>Profile</Tabs.Tab>
      <Tabs.Tab index={1}>Settings</Tabs.Tab>
      <Tabs.Tab index={2}>Security</Tabs.Tab>
    </Tabs.TabList>

    <Tabs.TabPanels>
      <Tabs.TabPanel index={0}>
        <ProfileForm />
      </Tabs.TabPanel>
      <Tabs.TabPanel index={1}>
        <SettingsForm />
      </Tabs.TabPanel>
      <Tabs.TabPanel index={2}>
        <SecuritySettings />
      </Tabs.TabPanel>
    </Tabs.TabPanels>
  </Tabs>
);
```

### 2. Accordion Compound Component

```typescript
import { createContext, useContext, useState, useCallback, useMemo } from 'react';

// ─── Context ─────────────────────────────────────────────────

interface AccordionContextType {
  openItems: Set<number>;
  toggleItem: (index: number) => void;
  allowMultiple: boolean;
}

const AccordionContext = createContext<AccordionContextType | null>(null);

const useAccordionContext = () => {
  const context = useContext(AccordionContext);
  if (!context) throw new Error('Must be inside Accordion');
  return context;
};

// ─── Accordion Parent ────────────────────────────────────────

interface AccordionProps {
  allowMultiple?: boolean;
  children: React.ReactNode;
}

const Accordion = ({ allowMultiple = false, children }: AccordionProps) => {
  const [openItems, setOpenItems] = useState<Set<number>>(new Set());

  const toggleItem = useCallback((index: number) => {
    setOpenItems(prev => {
      const next = new Set(prev);
      if (next.has(index)) {
        next.delete(index);
      } else {
        if (!allowMultiple) next.clear();
        next.add(index);
      }
      return next;
    });
  }, [allowMultiple]);

  const value = useMemo(
    () => ({ openItems, toggleItem, allowMultiple }),
    [openItems, toggleItem, allowMultiple]
  );

  return (
    <AccordionContext.Provider value={value}>
      <div className="accordion">{children}</div>
    </AccordionContext.Provider>
  );
};

// ─── AccordionItem ───────────────────────────────────────────

interface AccordionItemProps {
  index: number;
  title: string;
  children: React.ReactNode;
}

const AccordionItem = ({ index, title, children }: AccordionItemProps) => {
  const { openItems, toggleItem } = useAccordionContext();
  const isOpen = openItems.has(index);

  return (
    <div className="accordion-item">
      <button
        className="accordion-header"
        onClick={() => toggleItem(index)}
        aria-expanded={isOpen}
      >
        {title}
        <span className={`chevron ${isOpen ? 'chevron--open' : ''}`}>▼</span>
      </button>
      {isOpen && (
        <div className="accordion-body">{children}</div>
      )}
    </div>
  );
};

Accordion.Item = AccordionItem;

// ─── Usage ───────────────────────────────────────────────────

const FaqSection = () => (
  <Accordion allowMultiple>
    <Accordion.Item index={0} title="What is React?">
      <p>React is a JavaScript library for building user interfaces.</p>
    </Accordion.Item>
    <Accordion.Item index={1} title="What are hooks?">
      <p>Hooks let you use state and other React features without writing a class.</p>
    </Accordion.Item>
    <Accordion.Item index={2} title="What is TypeScript?">
      <p>TypeScript is a typed superset of JavaScript that compiles to plain JavaScript.</p>
    </Accordion.Item>
  </Accordion>
);
```

### 3. Select / Menu Compound Component

```typescript
import { createContext, useContext, useState, useRef, useEffect, useMemo } from 'react';

// ─── Context ─────────────────────────────────────────────────

interface SelectContextType {
  isOpen: boolean;
  selectedValue: string | null;
  selectedLabel: string | null;
  toggle: () => void;
  select: (value: string, label: string) => void;
  registerOption: (value: string, label: string) => void;
}

const SelectContext = createContext<SelectContextType | null>(null);

const useSelectContext = () => {
  const context = useContext(SelectContext);
  if (!context) throw new Error('Must be inside Select');
  return context;
};

// ─── Select Parent ───────────────────────────────────────────

interface SelectProps {
  value?: string;
  onChange: (value: string) => void;
  placeholder?: string;
  children: React.ReactNode;
}

const Select = ({ value, onChange, placeholder = 'Select...', children }: SelectProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [options] = useState<Map<string, string>>(new Map());
  const ref = useRef<HTMLDivElement>(null);

  const selectedLabel = value ? options.get(value) ?? null : null;

  const toggle = useCallback(() => setIsOpen(prev => !prev), []);
  const select = useCallback((val: string, label: string) => {
    onChange(val);
    setIsOpen(false);
  }, [onChange]);

  const registerOption = useCallback((val: string, label: string) => {
    options.set(val, label);
  }, [options]);

  // Close on outside click
  useEffect(() => {
    if (!isOpen) return;
    const handleClick = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, [isOpen]);

  const ctx = useMemo(() => ({
    isOpen, selectedValue: value ?? null, selectedLabel, toggle, select, registerOption,
  }), [isOpen, value, selectedLabel, toggle, select, registerOption]);

  return (
    <SelectContext.Provider value={ctx}>
      <div ref={ref} className="custom-select">{children}</div>
    </SelectContext.Provider>
  );
};

// ─── SelectTrigger ───────────────────────────────────────────

const SelectTrigger = () => {
  const { selectedLabel, toggle, isOpen } = useSelectContext();
  return (
    <button className="select-trigger" onClick={toggle} aria-expanded={isOpen}>
      {selectedLabel ?? 'Select...'}
      <span>▼</span>
    </button>
  );
};

// ─── SelectOption ────────────────────────────────────────────

interface SelectOptionProps {
  value: string;
  children: React.ReactNode;
}

const SelectOption = ({ value, children }: SelectOptionProps) => {
  const { selectedValue, select, registerOption } = useSelectContext();
  const label = typeof children === 'string' ? children : value;

  useEffect(() => { registerOption(value, label); }, [value, label, registerOption]);

  return (
    <div
      className={`select-option ${selectedValue === value ? 'select-option--selected' : ''}`}
      onClick={() => select(value, label)}
      role="option"
      aria-selected={selectedValue === value}
    >
      {children}
    </div>
  );
};

Select.Trigger = SelectTrigger;
Select.Option = SelectOption;
Select.Options = ({ children }: { children: React.ReactNode }) => {
  const { isOpen } = useSelectContext();
  if (!isOpen) return null;
  return <div className="select-dropdown">{children}</div>;
};
```

### 4. Form Field Compound Component

```typescript
import { createContext, useContext, useState, useId, useMemo } from 'react';

// ─── Context ─────────────────────────────────────────────────

interface FormFieldContextType {
  id: string;
  name: string;
  error?: string;
  isRequired: boolean;
}

const FormFieldContext = createContext<FormFieldContextType | null>(null);

const useFormField = () => {
  const context = useContext(FormFieldContext);
  if (!context) throw new Error('Must be inside FormField');
  return context;
};

// ─── FormField Parent ────────────────────────────────────────

interface FormFieldProps {
  name: string;
  label: string;
  error?: string;
  required?: boolean;
  children: React.ReactNode;
}

const FormField = ({ name, label, error, required = false, children }: FormFieldProps) => {
  const id = useId();

  const value = useMemo(() => ({
    id: `${id}-${name}`,
    name,
    error,
    isRequired: required,
  }), [id, name, error, required]);

  return (
    <FormFieldContext.Provider value={value}>
      <div className="form-field">
        {children}
      </div>
    </FormFieldContext.Provider>
  );
};

// ─── FormField.Label ─────────────────────────────────────────

const Label = ({ children }: { children?: React.ReactNode }) => {
  const { id, isRequired } = useFormField();
  return (
    <label htmlFor={id} className="form-label">
      {children ?? name}
      {isRequired && <span className="required">*</span>}
    </label>
  );
};

// ─── FormField.Input ─────────────────────────────────────────

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = (props: InputProps) => {
  const { id, name, error } = useFormField();
  return (
    <input
      id={id}
      name={name}
      className={`form-input ${error ? 'form-input--error' : ''}`}
      aria-invalid={!!error}
      aria-describedby={error ? `${id}-error` : undefined}
      {...props}
    />
  );
};

// ─── FormField.Error ─────────────────────────────────────────

const ErrorMessage = () => {
  const { id, error } = useFormField();
  if (!error) return null;

  return (
    <p id={`${id}-error`} className="form-error" role="alert">
      {error}
    </p>
  );
};

FormField.Label = Label;
FormField.Input = Input;
FormField.Error = ErrorMessage;

// ─── Usage ───────────────────────────────────────────────────

const SignupForm = () => (
  <form>
    <FormField name="email" label="Email" required error={errors.email}>
      <FormField.Label />
      <FormField.Input type="email" placeholder="Enter email" />
      <FormField.Error />
    </FormField>

    <FormField name="password" label="Password" required>
      <FormField.Label />
      <FormField.Input type="password" />
      <FormField.Error />
    </FormField>
  </form>
);
```

### 5. TypeScript Generics with Compound Components

```typescript
import { createContext, useContext, useState } from 'react';

// ─── Generic Compound Component ─────────────────────────────

interface ListContextType<T> {
  items: T[];
  selectedItem: T | null;
  selectItem: (item: T) => void;
  renderItem: (item: T) => React.ReactNode;
}

// eslint-disable-next-line @typescript-eslint/no-empty-object-type
const ListContext = createContext<ListContextType<any> | null>(null);

interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  children: React.ReactNode;
}

function List<T>({ items, renderItem, children }: ListProps<T>) {
  const [selectedItem, setSelectedItem] = useState<T | null>(null);

  const value = useMemo(() => ({
    items,
    selectedItem,
    selectItem: setSelectedItem,
    renderItem,
  }), [items, selectedItem, renderItem]);

  return (
    <ListContext.Provider value={value}>
      <div className="list">{children}</div>
    </ListContext.Provider>
  );
}

List.Items = function ListItems() {
  const { items, renderItem, selectItem } = useContext(ListContext)!;
  return (
    <ul>
      {items.map((item, i) => (
        <li key={i} onClick={() => selectItem(item)}>
          {renderItem(item)}
        </li>
      ))}
    </ul>
  );
};

List.Selected = function ListSelected() {
  const { selectedItem, renderItem } = useContext(ListContext)!;
  return selectedItem ? (
    <div className="selected">Selected: {renderItem(selectedItem)}</div>
  ) : null;
};
```

## Real-World Use Cases

| Library | Pattern | Compound Components |
|---------|---------|-------------------|
| **React Router** | `<Routes><Route path="..." element={...} /></Routes>` | Routes, Route |
| **Reach UI / Radix** | `Menu.Button`, `Menu.Items`, `Menu.Item` | Trigger, Items, Item |
| **Chakra UI** | `<Tabs><TabList><Tab>...</Tab></TabList><TabPanels><TabPanel>...</TabPanel></TabPanels></Tabs>` | TabList, Tab, TabPanels, TabPanel |
| **Ant Design** | `<Form><Form.Item><Input /></Form.Item></Form>` | Form.Item, Form.List |
| **Downshift** | `<Select><Select.Input /><Select.Menu /><Select.Item /></Select>` | Input, Menu, Item |

## Common Mistakes

### 1. Not Providing Error Messages for Missing Context

```typescript
// ❌ BAD: Silent failure
const useTabs = () => useContext(TabsContext); // Returns undefined

// ✅ GOOD: Throw descriptive error
const useTabs = () => {
  const ctx = useContext(TabsContext);
  if (!ctx) throw new Error('Tabs.* components must be rendered inside a <Tabs> component');
  return ctx;
};
```

### 2. Mutating Children with React.Children

```typescript
// ❌ BAD: Using React.Children.map to clone elements
const Tabs = ({ children }) => (
  <div>
    {React.Children.map(children, (child, i) =>
      React.cloneElement(child, { index: i }) // Fragile!
    )}
  </div>
);

// ✅ GOOD: Use Context to share state
const Tabs = ({ children }) => {
  const [activeIndex, setActiveIndex] = useState(0);
  return (
    <TabsContext.Provider value={{ activeIndex, setActiveIndex }}>
      <div>{children}</div>
    </TabsContext.Provider>
  );
};
```

### 3. Not Memoizing Context Value

```typescript
// ❌ BAD: New object every render → all children re-render
<TabsContext.Provider value={{ activeIndex, setActiveIndex }}>
  {children}
</TabsContext.Provider>

// ✅ GOOD: Memoize context value
const value = useMemo(() => ({ activeIndex, setActiveIndex }), [activeIndex]);
<TabsContext.Provider value={value}>{children}</TabsContext.Provider>
```

## Best Practices

1. **Always guard context** — Throw helpful errors when children are used outside parent
2. **Memoize context values** — Prevent unnecessary re-renders of all compound children
3. **Namespace components** — Attach children as static properties: `Tabs.Tab = Tab`
4. **Document the pattern** — Show how to import and use each compound child
5. **Use TypeScript** — Restrict children to valid compound types where possible
6. **Keep context focused** — Only share what compound children need
7. **Support composition** — Allow arbitrary nesting and wrapping
8. **Use `displayName`** — Set meaningful display names for debugging

## Performance Considerations

| Aspect | Impact | Mitigation |
|--------|--------|------------|
| Context updates | All children re-render | Split contexts, use memo |
| Many compound children | Render overhead | Virtualize if 100+ items |
| Deeply nested context | Prop drilling avoided | Context vs prop comparison: context wins |
| `React.Children` | Cloning creates new refs | Prefer Context over cloning |

## Summary

Compound components provide a declarative, flexible API by sharing implicit state through React Context. They are ideal for groups of related components like tabs, accordions, selects, and form fields. Always guard context access with descriptive errors and memoize context values to prevent unnecessary re-renders.

## Cheat Sheet

```typescript
// 1. Create Context
interface CompoundCtx { sharedState: T; actions: { doSomething: () => void } }
const CompoundCtx = createContext<CompoundCtx | null>(null);

// 2. Guard hook
const useCompound = () => {
  const ctx = useContext(CompoundCtx);
  if (!ctx) throw new Error('Must be inside Parent');
  return ctx;
};

// 3. Parent provides context
const Parent = ({ children }: { children: ReactNode }) => (
  <CompoundCtx.Provider value={{ sharedState, actions }}>
    {children}
  </CompoundCtx.Provider>
);

// 4. Children consume context
const Child = () => {
  const { sharedState } = useCompound();
  return <div>{sharedState}</div>;
};

// 5. Attach children to parent
Parent.Child = Child;

// 6. Usage
<Parent>
  <Parent.Child />
</Parent>
```

---

## See Also

- [Context API](10-Context-API.md)
- [Custom Hooks](16-Custom-Hooks.md)
- [Performance](13-Performance.md)
- [State Management](14-State-Management.md)

## References & Learn More

- [React Docs: Compound Components](https://react.dev/learn/thinking-in-react#step-2-build-a-static-version-in-react)
- [Patterns.dev: Compound Components](https://www.patterns.dev/react/compound-pattern/)
- [Kent C. Dodds: Compound Components](https://kentcdodds.com/blog/compound-components-with-react-hooks)
- [React Context to the Rescue](https://www.robinwieruch.de/react-context/)
