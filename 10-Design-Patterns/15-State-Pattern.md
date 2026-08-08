---
section: Design Patterns
category: Architecture
tags: [concept]
---

# State Pattern & State Machines

> **TL;DR:** The State pattern lets an object change its behavior when its internal state changes — it is the right tool when an entity has a small, well-defined set of states with explicit transitions (order: pending → paid → shipped). The senior test is knowing when to reach for an explicit state machine library (XState) vs. a discriminated union + transition function, and how to model the transitions so they cannot be bypassed.
>
> **Why it matters:** This is an Architecture interview topic you will be asked about at the senior level (5+ YoE) — not for definition recall, but for tradeoffs, production failure modes, and the ability to compare it against alternatives.

## Definition

The **State pattern** encapsulates state-specific behavior into separate state objects, with the context delegating the work to the current state. In TypeScript, the canonical implementation is a **discriminated union of states** plus a transition function that returns the next state based on events. For more complex systems, an **explicit state machine library** (XState) provides a declarative, visualizable statechart, with side effects, guards, and entry/exit actions. The senior design choice is: do you need a state machine, or do you need a state field with a `switch`? The answer is whether the transitions are complex, audited, or have side effects.

## Why Do We Need It?

1. **Encapsulation** — State-specific behavior lives with the state, not in a giant `switch` in the entity.
2. **Explicit transitions** — The set of legal transitions is data, not buried in conditionals.
3. **Auditability** — "How can this order go from paid to cancelled?" is one lookup, not a code spelunking.
4. **Visualization** — State machines can be rendered (mermaid, XState visualizer) and shared with product.
5. **Bypass prevention** — The transition function is the only path to a new state; you cannot set `state = 'shipped'` from anywhere else.
6. **Testability** — Each transition is a pure function; side effects are explicit; unit tests are trivial.
7. **Side effect coordination** — `onEntry` / `onExit` actions make the system observable; "what happens when an order is paid?" is in the machine.

## How It Works

### Discriminated Union + Transition Function

```text
type State = { kind: 'pending' } | { kind: 'paid', paidAt: Date } | { kind: 'shipped', tracking: string } | { kind: 'cancelled', reason: string };
type Event = { type: 'PAY' } | { type: 'SHIP', tracking: string } | { type: 'CANCEL', reason: string };
type Transition = (state: State, event: Event) => State;

Order (current state)
   │
   ▼
transition(state, event) → next state
   │
   ├── on PAY from 'pending' → 'paid'
   ├── on SHIP from 'paid' → 'shipped'
   ├── on CANCEL from 'pending' | 'paid' → 'cancelled'
   ├── on PAY from 'shipped' → throws (illegal transition)
   └── on unknown event → throws
```

### XState (Statecharts)

```text
Machine / Statechart
   ├── States (with nested substates)
   ├── Events
   ├── Transitions (event + guard → next state)
   ├── Actions (entry, exit, on transition)
   ├── Guards (conditional transitions)
   ├── Services (async work)
   └── Actor model (spawn, send, invoke)
```

## Code Examples

### Discriminated Union with Transition Function

```typescript
// domain/order-state.ts
export type OrderState =
  | { kind: 'pending' }
  | { kind: 'paid'; paidAt: Date }
  | { kind: 'shipped'; tracking: string; shippedAt: Date }
  | { kind: 'cancelled'; reason: string; cancelledAt: Date };

export type OrderEvent =
  | { type: 'PAY'; paidAt: Date }
  | { type: 'SHIP'; tracking: string; shippedAt: Date }
  | { type: 'CANCEL'; reason: string; cancelledAt: Date };

export class IllegalTransitionError extends Error {
  constructor(from: OrderState['kind'], event: OrderEvent['type']) {
    super(`Illegal transition: ${event} from ${from}`);
  }
}

export function transition(state: OrderState, event: OrderEvent): OrderState {
  switch (state.kind) {
    case 'pending':
      if (event.type === 'PAY')  return { kind: 'paid', paidAt: event.paidAt };
      if (event.type === 'CANCEL') return { kind: 'cancelled', reason: event.reason, cancelledAt: event.cancelledAt };
      break;
    case 'paid':
      if (event.type === 'SHIP') return { kind: 'shipped', tracking: event.tracking, shippedAt: event.shippedAt };
      if (event.type === 'CANCEL') return { kind: 'cancelled', reason: event.reason, cancelledAt: event.cancelledAt };
      break;
    case 'shipped':
      // shipped is terminal — no transitions
      break;
    case 'cancelled':
      // cancelled is terminal — no transitions
      break;
  }
  throw new IllegalTransitionError(state.kind, event.type);
}
```

### Using the State Machine

```typescript
// orders.service.ts
@Injectable()
export class OrdersService {
  constructor(private readonly repo: OrdersRepository) {}

  async pay(orderId: string, paidAt: Date) {
    const order = await this.repo.getById(orderId);
    const next = transition(order.state, { type: 'PAY', paidAt });   // throws if illegal
    await this.repo.updateState(orderId, next);
    return this.repo.getById(orderId);
  }
}
```

### Unit Test the Transitions

```typescript
// order-state.spec.ts
import { transition, IllegalTransitionError } from './order-state';

describe('Order state machine', () => {
  it('PAY from pending → paid', () => {
    const next = transition({ kind: 'pending' }, { type: 'PAY', paidAt: new Date() });
    expect(next.kind).toBe('paid');
  });

  it('SHIP from shipped → throws', () => {
    const shipped = { kind: 'shipped' as const, tracking: 't1', shippedAt: new Date() };
    expect(() => transition(shipped, { type: 'SHIP', tracking: 't2', shippedAt: new Date() })).toThrow(IllegalTransitionError);
  });

  it('CANCEL from pending is allowed', () => {
    const next = transition({ kind: 'pending' }, { type: 'CANCEL', reason: 'user', cancelledAt: new Date() });
    expect(next.kind).toBe('cancelled');
  });
});
```

### XState (Statecharts for Complex Flows)

```typescript
// domain/order.machine.ts
import { createMachine, assign } from 'xstate';

export const orderMachine = createMachine({
  id: 'order',
  initial: 'pending',
  context: { attempts: 0 },
  states: {
    pending: {
      on: {
        PAY: { target: 'paid' },
        CANCEL: { target: 'cancelled', actions: ['recordCancellation'] },
      },
    },
    paid: {
      on: {
        SHIP: { target: 'shipped', actions: ['recordShipment'] },
        CANCEL: { target: 'cancelled', actions: ['refund'] },
      },
    },
    shipped: { type: 'final' },
    cancelled: { type: 'final' },
  },
}, {
  actions: {
    recordCancellation: assign({ cancelledAt: () => new Date() }),
    recordShipment: assign({ shippedAt: () => new Date() }),
    refund: () => { /* call payment provider */ },
  },
});
```

### Visualize the Statechart (mermaid)

```text
stateDiagram-v2
  [*] --> pending
  pending --> paid : PAY
  pending --> cancelled : CANCEL
  paid --> shipped : SHIP
  paid --> cancelled : CANCEL (refund)
  shipped --> [*]
  cancelled --> [*]
```

### Persistence (Snapshot the State, Replay on Load)

```typescript
// Load an order from DB
const snapshot = await this.repo.getState(orderId);       // { kind: 'paid', paidAt }
const actor = createActor(orderMachine, { snapshot });
actor.start();
// Continue from the saved state; no need to replay history
```

### Guards (Conditional Transitions)

```typescript
// XState: only allow CANCEL within 24h of payment
paid: {
  on: {
    CANCEL: {
      target: 'cancelled',
      guard: ({ context, event }) => Date.now() - context.paidAt.getTime() < 24 * 60 * 60 * 1000,
      actions: ['refund'],
    },
  },
},
```

## Real-World Use Cases

1. **Order lifecycle** — `pending → paid → shipped → delivered` with `cancelled` as a terminal fork.
2. **Subscription state** — `trial → active → past_due → cancelled`; the billing run is the side effect.
3. **Document workflow** — `draft → review → approved → published`; only certain roles can move between states.
4. **Connection lifecycle** — WebSocket / database connection: `connecting → open → closing → closed`; reconnect logic depends on the state.
5. **Onboarding flows** — `signup → email_verified → profile_completed → active`; each step has a guard.
6. **Feature rollout** — `disabled → enabled_for_staff → enabled_for_beta → enabled_for_all`; transitions are gated.
7. **Saga compensation** — A distributed transaction modeled as a state machine per step; failure transitions to the compensation path.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `state = 'shipped'` set from anywhere | All transitions go through the transition function |
| `if (state === 'paid') ... else if (state === 'shipped') ...` | Use a transition function; the switch is the state machine |
| A field that is not in the state — e.g., `paidAt: Date` on a `pending` order | Use a discriminated union; the type system enforces the shape |
| Mixing business logic with state transitions | Keep `transition` pure; side effects live in the service that calls it |
| State that mutates silently — `order.state = 'paid'` with no event log | Log every transition as an event; the log is the audit trail |
| Re-implementing the state machine per service | One machine per aggregate; share via a library |
| Not handling illegal transitions | Throw or return a `Result`; never silently no-op |
| Storing only the state, not the transition history | Store the state AND the event log; "how did we get here?" is a query |

## Best Practices

1. **Discriminated union for the state** — TypeScript's narrowing makes the rest of the code self-documenting.
2. **One transition function per aggregate** — The transition is the only path to a new state; reject everything else.
3. **Pure transitions** — The function takes state + event and returns state; no side effects, no DB.
4. **Side effects in the caller** — The service emits events, calls APIs, writes to DB; the transition is the gate.
5. **Persist the state, log the events** — State is the current snapshot; the event log is the history.
6. **Unit test every transition** — Including the illegal ones; that is the contract.
7. **Use XState when transitions are complex** — Nested states, guards, parallel states, side effects — the library earns its keep.
8. **Use a discriminated union + transition when transitions are simple** — Don't pull in a state machine library for a 4-state entity.
9. **Visualize the statechart** — Mermaid, XState visualizer; share with product and QA.
10. **Snapshot the state on read** — Resume from the snapshot; don't replay history unless you need it for debugging.

## Performance Considerations

- A pure transition function is sub-microsecond; no perf concern.
- XState's interpreter has overhead (~5–20µs per event); fine for most apps, irrelevant for high-frequency loops.
- Persisting every state change as an event is an event-sourcing pattern; the cost is storage and replay time.
- For simple 3–4 state entities, a `switch` statement and a `status` column are enough; reach for XState when complexity demands it.

## Summary

- The State pattern encapsulates state-specific behavior; in TypeScript that is a discriminated union + transition function.
- Use a state machine library (XState) when transitions have guards, side effects, nested states, or visualization needs.
- Keep transitions pure; side effects live in the service that calls the transition.
- Persist the state, log the events; unit test every transition including the illegal ones.

## Cheat Sheet

| Concept | Description |
|---------|-------------|
| State pattern | Behavior depends on state; encapsulate per-state behavior in a state object |
| State machine | A model of states + transitions + events; the entity moves through states on events |
| Discriminated union | `type State = { kind: 'pending' } \| { kind: 'paid', paidAt: Date }` — TS narrowing for free |
| Transition function | Pure: `(state, event) → next state`; throws on illegal |
| Statechart | Visual model of a state machine; XState is the canonical TS lib |
| Guard | Conditional transition; only fire if the predicate is true |
| Entry / Exit actions | Side effects on entering or leaving a state |
| `assign` | XState helper to update context on a transition |
| Snapshot | Persisted state; resume from the snapshot on load |
| Event log | Append-only history of every transition; the audit trail |
| Mermaid | `stateDiagram-v2` for visualizing the statechart |
| Saga compensation | Modeling each step of a distributed transaction as a state machine |

---

## See Also
- [Coding Patterns](../19-Coding-Patterns/) (state in algorithms)
- [JavaScript](../01-JavaScript/) (state in functional vs OO styles)
- [NestJS](../06-NestJS/) (lifecycle states, sagas in microservices)
- [System Design](../11-System-Design/) (workflows in design)

## References & Learn More

- [XState](https://stately.ai/docs/xstate)
- [State Pattern — Refactoring Guru](https://refactoring.guru/design-patterns/state)
- [Statecharts — David Harel](https://www.sciencedirect.com/science/article/pii/0167642387900359/pdf)
- [Modeling with State Machines — XState Guide](https://stately.ai/docs/actions)
- [Mermaid State Diagrams](https://mermaid.js.org/syntax/stateDiagram.html)
- [Workflow Engine pattern (Camunda, Temporal)](https://temporal.io/blog/temporal-vs-cadence)
- [Workflow Engines — Martin Fowler](https://martinfowler.com/eaaCatalog/workflow.html)
