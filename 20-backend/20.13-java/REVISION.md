<!-- section: Java | category: Reference | tags: revision | role-priority: deferred | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Java-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Deferred-lightgrey)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../docs/topic-importance.md)

# Java — Revision

After each reading pass, explain the failure first, then the mechanism that prevents it. Return to the source when the boundary is unclear.

## Language Fundamentals

Source: [Language Fundamentals](20.13.01-java-language-fundamentals.md)

**Q:** Does successful class loading prove the class can initialize and run?

**A:** No. Loading obtains the class definition; linking includes verification, preparation, and resolution, and initialization later runs the class initializer. Resolution may be deferred, so a failure can surface only when a symbolic reference is first used.

**Q:** Which run-time areas are part of the JVM contract, and which details belong to HotSpot?

**A:** The JVM specification defines logical areas such as per-thread stacks, the heap, and the method area, but not their physical layout. HotSpot's Metaspace, compilation tiers, collector, and pause profile are implementation choices. Diagnose them with the target JDK's logs and profiling data.

**Q:** Why can a Java service benchmark faster after warm-up?

**A:** HotSpot can collect execution feedback and compile hot methods while the service runs. A cold measurement includes startup and interpreter work; a warmed measurement may include compiled code. Compare both against the actual workload and JDK.

**Q:** Why is a request pause not automatically equal to the logged garbage-collection pause?

**A:** HotSpot may spend time bringing threads to a safepoint before coordinated work begins. Application latency can also include scheduling, compilation, and I/O delays. Compare GC and safepoint logs with Flight Recorder data rather than attributing the entire delay to collection.

**Q:** A two-character-looking string has length four. What does length measure?

**A:** UTF-16 code units, not grapheme clusters. Select code-point or grapheme-aware processing according to the requirement.

**Q:** Why can subtracting two integer sort keys reverse their intended ordering?

**A:** The subtraction may overflow. Integer.compare expresses ordering without that arithmetic overflow.

**Q:** What must be true before calling `Arrays.binarySearch` with a comparator?

**A:** The array must already be sorted using the same ordering. Searching an unsorted array, or one sorted with a different comparator, does not promise a correct match or insertion point.

**Q:** Is primitive type pattern matching in `instanceof` and `switch` a production feature in Java 27?

**A:** No. It remains a preview feature in Java 27; compile and run with preview enabled for that exact JDK release, or use the stable reference-type patterns.

## OOP and SOLID

Source: [OOP and SOLID](20.13.02-java-oop-solid.md)

**Q:** How could a negative withdrawal break encapsulation even with private fields?

**A:** Without a positive-amount check, subtracting a negative amount increases the balance. Encapsulation is useful when the methods enforce invariants.

**Q:** Does storing a collaborator in a final field make the collaborator immutable?

**A:** No. The reference cannot be reassigned; the referenced object may still mutate. Deep immutability requires a separate state and copying policy.

**Q:** Why can `Square extends Rectangle` violate substitutability even though a square is mathematically a rectangle?

**A:** A mutable `Rectangle` contract may promise that setting width leaves height unchanged. A square must change both dimensions to preserve its own invariant, so it breaks that postcondition. Use an immutable common shape contract or redesign the mutation API.

**Q:** A class implements two interfaces that provide the same default method. Which implementation runs?

**A:** The conflict must be resolved in the class, usually by overriding the method and choosing or combining the defaults. Java does not select one based on interface order.

**Q:** Does constructor injection prove that a design follows dependency inversion?

**A:** No. Injection supplies an object. Inversion also requires that high-level policy own the abstraction and that lower-level details implement it; injecting a concrete infrastructure class leaves the dependency direction unchanged.

**Q:** When does an OCP extension point help rather than add unnecessary indirection?

**A:** When a real, repeated variation is expected and the new behavior satisfies a stable contract. Keep a workflow unchanged only when new implementations fit that contract; otherwise revise the abstraction rather than stacking flags or conditionals around it.

## Concurrency

Source: [Concurrency](20.13.03-java-concurrency-multithreading.md)

**Q:** What must a consumer do after freeing a slot in a bounded buffer?

**A:** Signal the not-full condition while holding the lock. Waiting producers then reacquire the lock and recheck their condition in a loop.

**Q:** Why does a read lock fail to protect an incremented reader counter?

**A:** Several readers hold the read lock concurrently. A shared increment still races; remove the counter or protect its mutation separately.

**Q:** Does anyOf wait for the first successful future?

**A:** It completes on the first completion, including failure. First-success semantics need their own policy for failures and cancellation.

**Q:** Why can LongAdder statistics exceed what a capacity admission check can safely use?

**A:** Its sum is not an atomic snapshot across concurrent updates. Use an atomic check/update, lock or semaphore when the decision must reserve bounded capacity.

**Q:** If timed tryLock returns false, should finally unlock anyway?

**A:** No. Unlock only after successful acquisition; unlocking an unowned ReentrantLock throws. Interrupted acquisition also leaves no ownership to release.

**Q:** Does a `synchronized` block pin a virtual thread to its carrier on every supported JDK?

**A:** No. JDK 24 removed monitor pinning while blocked in `synchronized`; native and foreign-function calls can still pin. JDK 21 and earlier have the older monitor behavior, so check the deployed runtime.

## Testing

Source: [Testing](20.13.04-java-testing-junit-mockito.md)

**Q:** Why can a fresh JUnit test instance still inherit another test's side effects?

**A:** Static state, shared dependencies, files and databases outlive that instance. Isolate or reset those resources explicitly.

**Q:** What does a database container establish, and what remains unproven?

**A:** It exercises the selected database version and configuration. Deployment topology, production data distribution and unrepresented settings need additional checks.

**Q:** A Boot 4 MVC slice fails to compile with the older `WebMvcTest` import. What changed?

**A:** Boot 4 split web testing into a focused module; use the `spring-boot-webmvc-test` dependency and `org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest` package.

**Q:** Why does `PostgreSQLContainer<?>` fail after importing the Testcontainers 2 PostgreSQL module class?

**A:** The new `org.testcontainers.postgresql.PostgreSQLContainer` is not generic. Declare `PostgreSQLContainer` and construct it without diamond syntax. The old `org.testcontainers.containers` package used the generic type; changing only the import leaves a compile error.

## Spring Boot

Source: [Spring Boot](20.13.05-spring-boot.md)

**Q:** Why does a self-invoked transactional method not create a transaction boundary?

**A:** In proxy mode the call through this bypasses interception. Put the boundary on the externally called service method or call another bean; an existing caller transaction may still apply.

**Q:** When can a stateless HTTP API still need CSRF protection?

**A:** When a browser automatically attaches credentials, including cookies. Stateless session configuration alone does not remove that attack path.

**Q:** Will validated configuration reject every unknown property?

**A:** No. Register the configuration type and validation first; missing required values can fail validation, but unknown properties are ignored by default unless configured otherwise.

**Q:** Which starter should a new Spring Boot 4 MVC service use?

**A:** `spring-boot-starter-webmvc`; Boot 4 deprecates `spring-boot-starter-web` in favor of the focused MVC starter.

## Follow a Trace and Change One Condition

Source: [Language trace](20.13.01-java-language-fundamentals.md#trace-references-copies-and-collection-order), [account](20.13.02-java-oop-solid.md#1-encapsulation), [buffer cycle](20.13.03-java-concurrency-multithreading.md#follow-a-full-puttake-cycle), [testing](20.13.04-java-testing-junit-mockito.md), and [request lifecycle](20.13.05-spring-boot.md#trace-one-request-through-the-whole-application).

**Q:** A method adds to a list then reassigns its parameter. Which change does the caller see?

**A:** The add affects the shared object. Reassigning the copied reference only changes the local parameter; Java remains pass-by-value.

**Q:** Does a copied ArrayList protect against mutation of shared element objects?

**A:** No. It copies the structure, not each element. Deep immutability or copying needs an explicit element contract.

**Q:** A 100-cent account withdraws 30, then attempts 90. What remains?

**A:** Seventy cents. The second call returns false without mutation; a negative amount throws instead of increasing the balance.

**Q:** A producer receives not-full but another producer fills the slot first. Why is await inside while?

**A:** The awakened producer must reacquire and recheck the condition. Signals do not reserve capacity, and spurious wakes are permitted.

**Q:** A repository test flushes then reads the same id without clearing its entity manager. What could the assertion miss?

**A:** It can receive the same managed entity instead of reading the persisted row. Clear before the lookup and separately test transaction/concurrency behavior.

**Q:** A singleton service stores a request's tenant in a field. Can constructor injection make that safe?

**A:** No. Concurrent requests share the bean. Pass trusted request state explicitly and keep transaction-scoped access on the correct connection.

## Summary

Use these prompts for retrieval practice. The source chapters contain examples; the interview bank adds longer spoken-answer prompts.

## See Also

- [Reading flow](INDEX.md) — return to prerequisites and learning stages for language, concurrency and framework contracts
- [Interview Questions](20.13.06-interview-questions.md) — apply language, thread and framework contracts to timed failure scenarios

## References & Learn More

- [Java SE 27 documentation](https://docs.oracle.com/en/java/javase/27/)
- [Java Language Specification, Java SE 27](https://docs.oracle.com/javase/specs/jls/se27/html/)
- [Spring Boot 4.1 reference](https://docs.spring.io/spring-boot/reference/index.html)
- [Spring Framework 7 transaction proxy semantics](https://docs.spring.io/spring-framework/reference/7.0/data-access/transaction/declarative/annotations.html)
- [JUnit 6.0.3 user guide](https://docs.junit.org/6.0.3/user-guide/)
- [Testcontainers PostgreSQL module](https://java.testcontainers.org/modules/databases/postgres/)
- [JEP 491: Synchronize Virtual Threads without Pinning](https://openjdk.org/jeps/491)
