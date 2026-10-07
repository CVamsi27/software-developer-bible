<!-- section: JavaScript | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-JavaScript-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Execution & Scope — Revision

Finish the category’s learning chapters, then answer without reopening them. Check the linked source when an answer misses the mechanism or boundary.

## Execution Context

Source: [Execution Context](10.1.1.01-execution-context.md)

**Q:** What does an execution context track, and why is it different from a lexical environment?

**A:** It tracks the current evaluation, including environment references and other execution state. An environment describes bindings and enclosing scope; a block can add an environment without making a new function call.

**Q:** Why can a var binding be read as undefined before its assignment, while an inner let binding cannot?

**A:** Declaration instantiation initializes var to undefined. A lexical binding remains uninitialized until its declaration evaluates; reading it earlier raises ReferenceError.

**Q:** You copy obj.run into a variable and call that variable. Does it keep obj as its receiver?

**A:** An ordinary function gets this from its invocation, not from the object it was copied from. A plain strict-mode call has undefined as this. An arrow instead keeps the enclosing this; host callbacks have their own invocation rules.

## Scope

Source: [Scope](10.1.1.02-scope.md)

**Q:** Does calling a function from a different scope change which enclosing variable its body refers to?

**A:** No. Ordinary lexical lookup follows the environment associated with the function’s definition, not the caller’s local declarations. Dynamic mechanisms such as eval have additional rules.

**Q:** Why does a block constrain let and const but not an ordinary var declaration?

**A:** Lexical declarations create block bindings. Var belongs to its enclosing function or applicable script environment; top-level module declarations stay in the module.

**Q:** What happens if an assignment targets an unresolved name?

**A:** A strict-mode assignment raises ReferenceError. In ordinary sloppy code it can create a global-object property. Declare the intended binding rather than relying on that behavior.

**Q:** Does const prevent changes to an object’s properties?

**A:** No. It prevents reassignment of that binding. Choose let when the binding itself must change; object mutation is a separate decision.

## Call Stack

Source: [Call Stack](10.1.1.03-call-stack.md)

**Q:** Why does a synchronous nested call return before its caller continues?

**A:** The caller’s evaluation waits while the nested call runs. The conceptual stack represents that last-in-first-out sequence; engines may optimize physical frames.

**Q:** Why can a loop freeze a page without deep recursion?

**A:** Long synchronous work prevents the event loop from handling other work on that thread. Yielding between chunks or moving suitable work to a worker addresses responsiveness; reducing stack depth alone does not.

**Q:** Is there one portable JavaScript recursion limit?

**A:** No. Supported depth and the reported error vary by runtime and workload. Use iteration or an explicit work stack when input can require unbounded nesting.

**Q:** Does an error stack always reproduce every call exactly?

**A:** No. Formatting, omitted or optimized frames and async stack information are runtime-dependent. It is diagnostic evidence, not a specification of engine memory layout.

## Hoisting

Source: [Hoisting](10.1.1.04-hoisting.md)

**Q:** Does hoisting physically move source statements?

**A:** No. It describes declaration setup before statement evaluation. Var starts initialized to undefined; lexical bindings start uninitialized; ordinary function declarations are initialized with a function object under their applicable rules.

**Q:** How do calling an uninitialized const function binding and calling an unassigned var function binding differ?

**A:** The first fails when reading the binding with ReferenceError. The second reads undefined, then fails when attempting to call it with TypeError.

**Q:** Why does typeof sometimes throw instead of returning undefined?

**A:** It returns the string undefined for an unresolved name, but reading an existing uninitialized lexical binding still raises ReferenceError.

**Q:** Can a function declared inside an if block safely be treated as a function-scoped declaration?

**A:** In strict code and modules it is block-scoped. Sloppy scripts have legacy Annex B rules with eligibility conditions. Avoid depending on those differences; declare the intended outer binding explicitly.

## Lexical Environment

Source: [Lexical Environment](10.1.1.05-lexical-environment.md)

**Q:** What information does an Environment Record hold about variables?

**A:** It describes the names in one scope, whether their variables are ready to read, and whether their values can be reassigned. It also links to the surrounding scope. This is information described by the language rules, not an ordinary object that application code can access.

**Q:** Why does reading an inner `let` variable before its declaration not return the outer variable's value?

**A:** JavaScript finds the inner variable and stops searching. That variable is not ready to read until its declaration runs, so the read throws a `ReferenceError`. JavaScript does not skip it and continue to the outer variable.

**Q:** Are declarative, function, module, object and global records five parts of every environment?

**A:** No. They are different kinds of record for different situations. Function and module records add information to a declarative record. A global record combines declared variables with names stored as properties of the global object.

**Q:** Does the scope-chain diagram show exactly how an engine stores variables or how fast lookup will be?

**A:** No. It explains which variable a read should find. An engine can store variables and find them differently while keeping that behavior. Use performance and memory tools to check speed and what stays in memory.

## Closures

Source: [Closures](10.1.1.06-closures.md)

**Q:** Does returning a function copy the current values of its enclosing variables?

**A:** No. The returned function continues to access the relevant bindings. Later changes are visible to functions sharing those bindings.

**Q:** Why can two functions from one factory share state while functions from different factory calls do not?

**A:** One call supplies a shared set of enclosing bindings to the functions it creates. Separate calls create separate bindings.

**Q:** Why do callbacks from a var loop commonly observe the same final index, while a let loop can preserve each iteration’s index?

**A:** The var callbacks share one binding; the let loop supplies separate iteration bindings. The result also depends on when callbacks execute, so trace both binding identity and timing.

**Q:** What survives between calls to a debounced function?

**A:** The returned function keeps access to the timer-handle binding. Later invocations can cancel the pending timer before scheduling another; the original factory call need not remain on the stack.

**Q:** Does a closure prove that every nearby local variable remains in memory?

**A:** No. Engines can avoid retaining unused values. Inspect retaining paths and release long-lived owners or capture smaller state when diagnosing memory use.

## Summary

Distinguish active evaluation, lexical binding identity and callback timing. If an answer relies on a drawing of engine memory or a memorized phase count, return to the chapter’s observable example.

## See Also

- [Category reading order](INDEX.md)

## References & Learn More

The linked chapters contain the technical sources.
