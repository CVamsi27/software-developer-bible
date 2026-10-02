<!-- section: Java | category: Reference | tags: revision -->
[![Section](https://img.shields.io/badge/section-Java-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

# Java — Revision

After each reading pass, explain the failure first, then the mechanism that prevents it. Return to the source when the boundary is unclear.

## Language Fundamentals

Source: [Language Fundamentals](20.13.01-java-language-fundamentals.md)

**Q:** A two-character-looking string has length four. What does length measure?

**A:** UTF-16 code units, not grapheme clusters. Select code-point or grapheme-aware processing according to the requirement.

**Q:** Why can subtracting two integer sort keys reverse their intended ordering?

**A:** The subtraction may overflow. Integer.compare expresses ordering without that arithmetic overflow.

## OOP and SOLID

Source: [OOP and SOLID](20.13.02-java-oop-solid.md)

**Q:** How could a negative withdrawal break encapsulation even with private fields?

**A:** Without a positive-amount check, subtracting a negative amount increases the balance. Encapsulation is useful when the methods enforce invariants.

**Q:** Does storing a collaborator in a final field make the collaborator immutable?

**A:** No. The reference cannot be reassigned; the referenced object may still mutate. Deep immutability requires a separate state and copying policy.

## Concurrency

Source: [Concurrency](20.13.03-java-concurrency-multithreading.md)

**Q:** What must a consumer do after freeing a slot in a bounded buffer?

**A:** Signal the not-full condition while holding the lock. Waiting producers then reacquire the lock and recheck their condition in a loop.

**Q:** Why does a read lock fail to protect an incremented reader counter?

**A:** Several readers hold the read lock concurrently. A shared increment still races; remove the counter or protect its mutation separately.

**Q:** Does anyOf wait for the first successful future?

**A:** It completes on the first completion, including failure. First-success semantics need their own policy for failures and cancellation.

## Testing

Source: [Testing](20.13.04-java-testing-junit-mockito.md)

**Q:** Why can a fresh JUnit test instance still inherit another test's side effects?

**A:** Static state, shared dependencies, files and databases outlive that instance. Isolate or reset those resources explicitly.

**Q:** What does a database container establish, and what remains unproven?

**A:** It exercises the selected database version and configuration. Deployment topology, production data distribution and unrepresented settings need additional checks.

## Spring Boot

Source: [Spring Boot](20.13.05-spring-boot.md)

**Q:** Why does a self-invoked transactional method not create a transaction boundary?

**A:** In proxy mode the call through this bypasses interception. Put the boundary on the externally called service method or call another bean; an existing caller transaction may still apply.

**Q:** When can a stateless HTTP API still need CSRF protection?

**A:** When a browser automatically attaches credentials, including cookies. Stateless session configuration alone does not remove that attack path.

**Q:** Will validated configuration reject every unknown property?

**A:** No. Register the configuration type and validation first; missing required values can fail validation, but unknown properties are ignored by default unless configured otherwise.

## Summary

Use these prompts for retrieval practice. The source chapters contain examples; the interview bank adds longer spoken-answer prompts.

## See Also

- [Reading flow](INDEX.md)
- [Interview Questions](20.13.06-interview-questions.md)

## References & Learn More

- [Java 21 documentation](https://docs.oracle.com/en/java/javase/21/)
- [Spring Boot reference](https://docs.spring.io/spring-boot/index.html)
