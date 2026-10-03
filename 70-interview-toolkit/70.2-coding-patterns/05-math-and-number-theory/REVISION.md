<!-- section: Coding Patterns | category: Reference | tags: revision, practi | role-priority: optional | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Coding%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Optional-lightgrey)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../../docs/topic-importance.md)

# Math & Number Theory — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Number Theory & Combinatorics

Source: [Number Theory & Combinatorics](70.2.5.01-number-theory-combinatorics.md)

**Q:** When does Fermat exponentiation provide a modular inverse?

**A:** The modulus must be prime and the value nonzero modulo it. More generally an inverse exists only when the value and modulus are coprime.

**Q:** Why can reducing both operands still leave multiplication unsafe?

**A:** Their product can exceed the language's exact integer range before the remainder is taken. Use a proven bounded-width case, wider intermediates, BigInteger/BigInt, or an overflow-safe multiplication algorithm.

**Q:** Why does a factorial-and-inverse nCr formula need n below a prime modulus?

**A:** When n reaches the modulus, factorial contains a zero factor and cannot be inverted. Different methods are needed for larger n or composite moduli.

**Q:** Why divide by gcd before multiplying for lcm?

**A:** It reduces the intermediate product, but does not guarantee the final result fits. Handle zero inputs and check overflow under the function's numeric contract.

**Q:** What must a probability-as-counts argument establish?

**A:** A well-defined sample space, equally likely outcomes or explicit weights, and correct counting without overlap. Independence is an assumption to justify before multiplying probabilities.

## Summary

Check the modulus, invertibility, intermediate numeric range, and sample space before applying a formula. These conditions determine whether the arithmetic result has the intended meaning.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
