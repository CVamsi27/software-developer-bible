# Portals

[![Category: Frontend](https://img.shields.io/badge/category-Frontend-00b4d8)](.)

onent's children into a different DOM subtree outside of the parent component's DOM hierarchy. While the portal content renders elsewhere in the DOM, it remains within the React component tree — meaning context, props, and event bubbling behave as if the portal were still a child of the parent component. Portals are created using `ReactDOM.createPortal(child, container)`.

## Why Do We Need It?

1. **Z-index stacking contexts** — Render modals, tooltips, and dropdowns above all other content
2. **Overflow clipping** — Escape parent containers with `overflow: hidden` or `clip-path`
3. **CSS transform interference** — Avoid fixed positioning breaking inside transformed parents
4. **Separate scroll containers** — Render notifications/banners outside main scrollable areas
5. **Third-party widget isolation** — Embed widgets in specific DOM nodes without component coupling

## How It Works

### DOM vs React Tree

```text
Portal DOM Position vs React Tree Position:
═══════════════════════════════════════════════════════════════

React Component Tree:             Actual DOM Tree:
┌────────────────────────┐       ┌────────────────────────┐
│  App                   │       │  <div id="root">        │
│  ├── Header            │       │    <header>...</header> │
│  ├── Main              │       │    <main>               │
│  │   └── ModalPortal ──┼──┐    │      <p>Content</p>    │
│  │       └── Modal     │  │    │    </main>              │
│  └── Footer            │  │    │  </div>                 │
│                         │  │    │                         │
│  Portal target:         │  │    │  <div id="modal-root">  │
│  document.getElementById│  │    │    ├── <div class="    │
│    ('modal-root')       │  │    │    │   modal-overlay">  │
│                         │  │    │    │   Modal content    │
│                         │  │    │    │   here             │
└─────────────────────────┘  │    │    └── </div>           │
                             │    └────────────────────────┘
                             │
  Key Insight:               │
  ├── Modal is a child of   │
  │   Main in React tree     │
  ├── Props/Context flow     │
  │   from Main → Modal      │
  ├── Event bubbling goes    │
  │   from Modal → Main      │
  └── BUT DOM renders with   │
      the #modal-root div    │
                             │
```

### Event Bubbling Through Portals

```text
Event Bubbling:
═══════════════════════════════════════════════════════════════

Even though the Portal renders in a different DOM node,
events bubble UP through the React component tree — NOT
the DOM tree.

┌─────────────────────────────────────────────────────────────┐
│ Click inside Modal:                                        │
│                                                              │
│  1. Click event fires on <button> inside portal DOM         │
│  2. Event bubbles DOM-wise (within #modal-root div)        │
│  3. React intercepts and translates to React tree:         │
│     Modal → ModalPortal → Main → App                       │
│  4. onClick on <div id="app"> catches it                   │
│                                                              │
│  If <div id="app"> has onClick, it WILL fire               │
│  even though modal is NOT nested in the DOM there           │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### 1. Basic Portal

```typescript
import { createPortal } from 'react-dom';

interface PortalProps {
  children: React.ReactNode;
  container?: Element | DocumentFragment;
}

const Portal = ({ children, container }: PortalProps) => {
  const mountNode = container ?? document.body;
  return createPortal(children, mountNode);
};

// Usage
const App = () => {
  return (
    <div>
      <h1>My App</h1>
      <Portal>
        <div className="toast">This renders in document.body</div>
      </Portal>
    </div>
  );
};
```

### 2. Modal Component

```typescript
import { createPortal } from 'react-dom';
import { useEffect, useRef, useState } from 'react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
  title?: string;
}

const Modal = ({ isOpen, onClose, children, title }: ModalProps) => {
  const overlayRef = useRef<HTMLDivElement>(null);

  // Close on Escape key
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEsc);
      document.body.style.overflow = 'hidden'; // Prevent scroll
    }

    return () => {
      document.removeEventListener('keydown', handleEsc);
      document.body.style.overflow = '';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return createPortal(
    <div
      ref={overlayRef}
      className="modal-overlay"
      onClick={(e) => {
        if (e.target === overlayRef.current) onClose();
      }}
      role="dialog"
      aria-modal="true"
      aria-label={title}
    >
      <div className="modal-content">
        <div className="modal-header">
          {title && <h2>{title}</h2>}
          <button onClick={onClose} aria-label="Close">
            &times;
          </button>
        </div>
        <div className="modal-body">{children}</div>
      </div>
    </div>,
    document.getElementById('modal-root') ?? document.body
  );
};

// Usage
const App = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div>
      <button onClick={() => setIsOpen(true)}>Open Modal</button>
      <Modal
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        title="Confirm Action"
      >
        <p>Are you sure you want to proceed?</p>
        <button onClick={() => setIsOpen(false)}>Confirm</button>
      </Modal>
    </div>
  );
};
```

### 3. Tooltip with Portal

```typescript
import { createPortal } from 'react-dom';
import { useState, useRef, useEffect, useCallback } from 'react';

interface TooltipProps {
  text: string;
  children: React.ReactNode;
  position?: 'top' | 'bottom' | 'left' | 'right';
}

const Tooltip = ({ text, children, position = 'top' }: TooltipProps) => {
  const [isVisible, setIsVisible] = useState(false);
  const [tooltipPos, setTooltipPos] = useState({ top: 0, left: 0 });
  const triggerRef = useRef<HTMLDivElement>(null);

  const calculatePosition = useCallback(() => {
    const trigger = triggerRef.current;
    if (!trigger) return;

    const rect = trigger.getBoundingClientRect();
    const offset = 8; // Gap between trigger and tooltip

    const positions = {
      top: { top: rect.top - offset, left: rect.left + rect.width / 2 },
      bottom: { top: rect.bottom + offset, left: rect.left + rect.width / 2 },
      left: { top: rect.top + rect.height / 2, left: rect.left - offset },
      right: { top: rect.top + rect.height / 2, left: rect.right + offset },
    };

    setTooltipPos(positions[position]);
  }, [position]);

  useEffect(() => {
    if (isVisible) calculatePosition();
  }, [isVisible, calculatePosition]);

  useEffect(() => {
    const handleResize = () => { if (isVisible) calculatePosition(); };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [isVisible, calculatePosition]);

  return (
    <>
      <div
        ref={triggerRef}
        onMouseEnter={() => setIsVisible(true)}
        onMouseLeave={() => setIsVisible(false)}
        onFocus={() => setIsVisible(true)}
        onBlur={() => setIsVisible(false)}
        style={{ display: 'inline-block' }}
      >
        {children}
      </div>

      {isVisible && createPortal(
        <div
          role="tooltip"
          style={{
            position: 'fixed',
            top: tooltipPos.top,
            left: tooltipPos.left,
            transform: 'translate(-50%, -50%)',
            zIndex: 9999,
            backgroundColor: '#333',
            color: '#fff',
            padding: '4px 8px',
            borderRadius: 4,
            fontSize: 12,
            pointerEvents: 'none',
            whiteSpace: 'nowrap',
          }}
        >
          {text}
        </div>,
        document.body
      )}
    </>
  );
};

// Usage
const App = () => (
  <div style={{ overflow: 'hidden' }}>
    {/* Tooltip escapes overflow:hidden via portal */}
    <Tooltip text="This tooltip can overflow its parent">
      <button>Hover me</button>
    </Tooltip>
  </div>
);
```

### 4. Dropdown Menu (Escape Clipping)

```typescript
import { createPortal } from 'react-dom';
import { useState, useRef, useEffect, useCallback } from 'react';

interface DropdownMenuProps {
  trigger: React.ReactNode;
  children: React.ReactNode;
}

const DropdownMenu = ({ trigger, children }: DropdownMenuProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [menuPos, setMenuPos] = useState({ top: 0, left: 0, width: 0 });
  const triggerRef = useRef<HTMLDivElement>(null);

  const updatePosition = useCallback(() => {
    const trigger = triggerRef.current;
    if (!trigger) return;

    const rect = trigger.getBoundingClientRect();
    setMenuPos({
      top: rect.bottom,
      left: rect.left,
      width: rect.width,
    });
  }, []);

  // Close on outside click
  useEffect(() => {
    if (!isOpen) return;

    const handleClick = (e: MouseEvent) => {
      if (triggerRef.current?.contains(e.target as Node)) return;
      setIsOpen(false);
    };

    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, [isOpen]);

  // Recalculate position on scroll/resize
  useEffect(() => {
    if (!isOpen) return;
    window.addEventListener('scroll', updatePosition, true);
    window.addEventListener('resize', updatePosition);
    return () => {
      window.removeEventListener('scroll', updatePosition, true);
      window.removeEventListener('resize', updatePosition);
    };
  }, [isOpen, updatePosition]);

  return (
    <>
      <div ref={triggerRef} onClick={() => { updatePosition(); setIsOpen(prev => !prev); }}>
        {trigger}
      </div>

      {isOpen && createPortal(
        <div
          style={{
            position: 'fixed',
            top: menuPos.top,
            left: menuPos.left,
            width: menuPos.width,
            zIndex: 1000,
            backgroundColor: '#fff',
            border: '1px solid #ddd',
            borderRadius: 4,
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
          }}
        >
          {children}
        </div>,
        document.body
      )}
    </>
  );
};
```

### 5. Notification Toast System

```typescript
import { createPortal } from 'react-dom';
import { useState, useCallback, useEffect } from 'react';

// Toast context for app-wide notifications
interface Toast {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info' | 'warning';
  duration?: number;
}

let toastId = 0;
let addToastGlobal: ((toast: Omit<Toast, 'id'>) => void) | null = null;

export const toast = {
  success: (message: string) => addToastGlobal?.({ message, type: 'success' }),
  error: (message: string) => addToastGlobal?.({ message, type: 'error' }),
  info: (message: string) => addToastGlobal?.({ message, type: 'info' }),
  warning: (message: string) => addToastGlobal?.({ message, type: 'warning' }),
};

const ToastContainer = () => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = useCallback((t: Omit<Toast, 'id'>) => {
    const id = String(++toastId);
    setToasts(prev => [...prev, { ...t, id }]);

    setTimeout(() => {
      setToasts(prev => prev.filter(toast => toast.id !== id));
    }, t.duration ?? 3000);
  }, []);

  useEffect(() => {
    addToastGlobal = addToast;
    return () => { addToastGlobal = null; };
  }, [addToast]);

  return createPortal(
    <div
      style={{
        position: 'fixed',
        top: 16,
        right: 16,
        zIndex: 10000,
        display: 'flex',
        flexDirection: 'column',
        gap: 8,
      }}
    >
      {toasts.map(t => (
        <div
          key={t.id}
          style={{
            padding: '12px 16px',
            borderRadius: 6,
            color: '#fff',
            backgroundColor:
              t.type === 'success' ? '#22c55e' :
              t.type === 'error' ? '#ef4444' :
              t.type === 'warning' ? '#f59e0b' : '#3b82f6',
            boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
            minWidth: 200,
          }}
        >
          {t.message}
        </div>
      ))}
    </div>,
    document.body
  );
};

// Usage: Add <ToastContainer /> to root layout
const App = () => {
  return (
    <div>
      <ToastContainer />
      <button onClick={() => toast.success('Saved!')}>Save</button>
      <button onClick={() => toast.error('Failed!')}>Fail</button>
    </div>
  );
};
```

### 6. Portal with Context Propagation

```typescript
import { createPortal } from 'react-dom';
import { createContext, useContext, useState } from 'react';

// Theme context — will propagate THROUGH portal
const ThemeContext = createContext('light');

const ThemeProvider = ({ children }: { children: React.ReactNode }) => {
  const [theme] = useState('dark');
  return (
    <ThemeContext.Provider value={theme}>
      {children}
    </ThemeContext.Provider>
  );
};

const PortalContent = () => {
  // ✅ Context works inside portal because React tree position matters
  const theme = useContext(ThemeContext);
  return <div className={theme}>Portal content (theme: {theme})</div>;
};

const App = () => {
  const portalContainer = document.getElementById('portal-root')!;

  return (
    <ThemeProvider>
      <div className="app">
        <p>App content</p>
        {/* PortalContent gets ThemeContext from ThemeProvider */}
        {createPortal(<PortalContent />, portalContainer)}
      </div>
    </ThemeProvider>
  );
};
```

### 7. Portal with Event Bubbling

```typescript
import { createPortal } from 'react-dom';
import { useState } from 'react';

const App = () => {
  const [clicks, setClicks] = useState<string[]>([]);

  const handleDivClick = (source: string) => {
    setClicks(prev => [...prev, `div clicked: ${source}`]);
  };

  const handlePortalClick = () => {
    setClicks(prev => [...prev, 'portal clicked']);
  };

  return (
    // Even though portal renders in document.body,
    // clicks bubble up through THIS div in the React tree
    <div onClick={() => handleDivClick('outer div')}>
      <h1>Event Bubbling Demo</h1>

      {createPortal(
        <button onClick={handlePortalClick}>
          Click me (portal)
        </button>,
        document.body
      )}

      <div>
        {clicks.map((msg, i) => (
          <p key={i}>{msg}</p>
        ))}
      </div>
    </div>
  );
};
```

### 8. Multi-Root Portals

```typescript
import { createPortal } from 'react-dom';

// Multiple portal targets
const PortalRoots = () => (
  <>
    <div id="modal-root" />
    <div id="tooltip-root" />
    <div id="notification-root" />
    <div id="sidebar-root" />
  </>
);

// Dedicated portal components
const ModalPortal = ({ children }: { children: React.ReactNode }) =>
  createPortal(children, document.getElementById('modal-root')!);

const TooltipPortal = ({ children }: { children: React.ReactNode }) =>
  createPortal(children, document.getElementById('tooltip-root')!);

const NotificationPortal = ({ children }: { children: React.ReactNode }) =>
  createPortal(children, document.getElementById('notification-root')!);

const App = () => (
  <div>
    <PortalRoots />
    <main>
      <ModalPortal>
        <ModalContent />
      </ModalPortal>
      <TooltipPortal>
        <TooltipContent />
      </TooltipPortal>
      <NotificationPortal>
        <NotificationContent />
      </NotificationPortal>
    </main>
  </div>
);
```

### 9. SSR-Safe Portal

```typescript
import { createPortal } from 'react-dom';
import { useEffect, useState } from 'react';

const ClientOnlyPortal = ({
  children,
  selector,
}: {
  children: React.ReactNode;
  selector: string;
}) => {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null; // Don't render on server

  const container = document.querySelector(selector);
  if (!container) return null;

  return createPortal(children, container);
};

// Usage — safe for SSR/SSG
const Modal = () => (
  <ClientOnlyPortal selector="#modal-root">
    <div className="modal">Content</div>
  </ClientOnlyPortal>
);
```

### 10. Creating a Reusable Portal Hook

```typescript
import { createPortal } from 'react-dom';
import { useMemo, useRef, useEffect } from 'react';

function usePortal(selector?: string): HTMLElement {
  const container = useMemo(() => {
    // Try to find existing container, or create one
    const existing = selector
      ? document.querySelector(selector)
      : document.getElementById('portal-container');

    if (existing) return existing as HTMLElement;

    // Create new container
    const el = document.createElement('div');
    if (selector) el.id = selector.replace('#', '');
    else el.id = 'portal-container';
    document.body.appendChild(el);
    return el;
  }, [selector]);

  return container;
}

// Usage
const PortalRenderer = ({ children }: { children: React.ReactNode }) => {
  const container = usePortal('#app-portals');
  return createPortal(children, container);
};
```

## Real-World Use Cases

| Use Case | Portal Reason | DOM Target |
|----------|---------------|------------|
| **Modal/Dialog** | Z-index stacking, overflow escape | `#modal-root` |
| **Tooltip** | Overflow hidden, CSS transform | `#tooltip-root` or `document.body` |
| **Dropdown Menu** | Overflow hidden, scroll containers | `document.body` |
| **Toast/Notification** | Fixed position, stacking | `#notification-root` |
| **Context Menu** | Position at cursor, above everything | `document.body` |
| **DatePicker/Select** | Escape card/grid clipping | `#overlay-root` |
| **Side Panel / Drawer** | Separate scroll, z-index | `#drawer-root` |
| **Loading Bar (top)** | Outside app layout structure | `document.body` |

## Common Mistakes

### 1. Not Cleaning Up Portal Container

```typescript
// ❌ BAD: Portal container left in DOM after unmount
const Modal = () => {
  const container = document.createElement('div');
  document.body.appendChild(container);

  useEffect(() => {
    // No cleanup!
  }, []);

  return createPortal(<div>Modal</div>, container);
};

// ✅ GOOD: Clean up on unmount
const Modal = () => {
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const el = document.createElement('div');
    document.body.appendChild(el);
    containerRef.current = el;

    return () => {
      document.body.removeChild(el);
    };
  }, []);

  if (!containerRef.current) return null;
  return createPortal(<div>Modal</div>, containerRef.current);
};
```

### 2. Assuming DOM Position = Z-Index Order

```typescript
// ❌ BAD: Relying on DOM position for z-index
// Portal renders in document.body, not where you expect

// ✅ GOOD: Manage z-index explicitly
const Modal = () => (
  createPortal(
    <div style={{ zIndex: 1000 }}> {/* Always set z-index */}
      Modal content
    </div>,
    document.body
  )
);
```

### 3. Breaking Event Bubbling Unexpectedly

```typescript
// ❌ BAD: Clicking modal closes it because event bubbles to overlay
const Modal = ({ onClose }: { onClose: () => void }) => (
  <div className="overlay" onClick={onClose}>
    <div className="modal-content">
      {/* Click here also triggers onClose! */}
      <p>Modal body</p>
    </div>
  </div>
);

// ✅ GOOD: Stop propagation on content clicks
const Modal = ({ onClose }: { onClose: () => void }) => (
  <div className="overlay" onClick={onClose}>
    <div className="modal-content" onClick={e => e.stopPropagation()}>
      <p>Modal body</p>
      <button onClick={() => console.log('clicked')}>Button</button>
    </div>
  </div>
);
```

### 4. Trying to Select Portal DOM with Query Selectors

```typescript
// ❌ BAD: Portal renders elsewhere, can't find child by DOM traversal
const Parent = () => {
  const handleClick = () => {
    const btn = document.querySelector('.portal-btn'); // Not in this DOM tree!
    btn?.click();
  };
  return <button onClick={handleClick}>Find Portal Button</button>;
};

// ✅ GOOD: Use React refs and callbacks instead
```

## Best Practices

1. **Always render portal container in HTML** — Add `<div id="modal-root">` near `</body>`
2. **Manage z-index explicitly** — Don't rely on DOM position for stacking
3. **Clean up portals on unmount** — Remove dynamically created containers
4. **Provide accessible attributes** — `role="dialog"`, `aria-modal`, focus trapping
5. **Use CSS containment** — `contain: content` on portal wrappers for performance
6. **Close on Escape key** — Add keyboard handling for modals/dialogs
7. **Prevent body scroll** — Set `overflow: hidden` when modal is open
8. **SSR safety** — Guard portal containers with `typeof window !== 'undefined'`
9. **Use dedicated portal roots** — Separate containers for modals, tooltips, toasts
10. **Test event bubbling** — Understand React tree vs DOM tree behavior

## Performance Considerations

| Aspect | Impact | Mitigation |
|--------|--------|------------|
| **Portal creation** | Minimal overhead | Pre-create containers once |
| **Event delegation** | Normal bubbling | No special perf concern |
| **Re-renders** | Portals re-render with parent | `React.memo` for heavy portal content |
| **CSS containment** | Improves paint perf | `contain: content` on portal wrappers |
| **Reflows** | Separate DOM tree | Isolates layout effects |

## Summary

Portals allow rendering components outside the parent DOM tree while preserving React context and event bubbling. They are essential for modals, tooltips, dropdowns, and notifications that need to escape CSS clipping, overflow, or z-index constraints. Always manage z-index explicitly, clean up dynamically created containers, and provide proper accessibility attributes.

## Cheat Sheet

```typescript
// Basic portal
import { createPortal } from 'react-dom';
createPortal(children, container);

// Modal pattern
const Modal = ({ isOpen, onClose, children }) => {
  if (!isOpen) return null;

  return createPortal(
    <div className="overlay" onClick={onClose} role="dialog">
      <div className="content" onClick={e => e.stopPropagation()}>
        {children}
      </div>
    </div>,
    document.getElementById('modal-root') ?? document.body
  );
};

// SSR-safe portal
const SafePortal = ({ children, selector }) => {
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  if (!mounted) return null;
  return createPortal(children, document.querySelector(selector)!);
};

// Portal hook
const usePortal = (id = 'portal-root') => {
  const el = useMemo(() => {
    const existing = document.getElementById(id);
    if (existing) return existing;
    const created = document.createElement('div');
    created.id = id;
    document.body.appendChild(created);
    return created;
  }, [id]);
  return el;
};

// Event bubbling note
// Clicks in portal bubble up React component tree, NOT DOM tree!
```

---

## See Also

- [Context API](10-Context-API.md)
- [Error Boundary](12-Error-Boundary.md)
- [Performance](13-Performance.md)
- [Reconciliation](03-Reconciliation.md)
- [useRef](09-UseRef.md)

## References & Learn More

- [React Docs: Portals](https://react.dev/reference/react-dom/createPortal)
- [React Portals on MDN](https://developer.mozilla.org/en-US/docs/Web/API/ReactDOM/createPortal)
- [React Portals: Event Bubbling](https://react.dev/reference/react-dom/createPortal#event-bubbling-through-portals)
- [A Complete Guide to React Portals](https://blog.logrocket.com/learn-react-portals-by-example/)
- [Using Portals in React](https://css-tricks.com/using-react-portals/)
