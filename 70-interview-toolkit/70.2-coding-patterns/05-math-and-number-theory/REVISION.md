<!-- section: Coding Patterns | category: Reference | tags: revision, practice | role-priority: optional | general-importance: specialized -->
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

**A:** For prime modulus p, a value a that is not divisible by p has inverse a^(p−2) modulo p. The inverse is a value that multiplies with a to give remainder 1. More generally, an inverse exists when a and the modulus are coprime: their greatest common divisor is 1.

**Q:** Why can reducing both operands still leave multiplication unsafe?

**A:** Reducing each operand does not guarantee that their product fits the numeric type. The multiplication happens before the remainder operation, so it can overflow or lose precision first. Check the largest intermediate product, or use BigInt, a wider integer type, or a multiplication algorithm that avoids overflow.

**Q:** Why does a factorial-and-inverse nCr formula need n below a prime modulus?

**A:** The formula needs inverses of factorials. If n is at least the prime modulus p, n! includes p and has remainder 0, which has no inverse. The usual factorial table and inverse formula therefore stop working. Use a method designed for larger n or for a composite modulus.

**Q:** Why divide by gcd before multiplying for lcm?

**A:** For positive integers, compute lcm as (a / gcd(a, b)) × b. Dividing first makes the intermediate values smaller than multiplying a × b first. The final result can still exceed the numeric range. Handle zero inputs separately and check whether the chosen type can represent the result.

**Q:** What must a probability-as-counts argument establish?

**A:** List which outcomes are possible and why they are equally likely. If they are not, use their actual probabilities instead of counting alone. Count without including the same outcome twice. Before multiplying probabilities, justify that the events are independent or use the appropriate conditional probabilities.

**Q:** Why can the sieve start crossing out multiples at p²?

**A:** A smaller multiple p×k with k<p already has a factor less than p and was crossed out by an earlier prime. Starting at p² avoids repeating that work without skipping a composite.

**Q:** How does choosing an ordered pair differ from choosing an unordered pair?

**A:** From n distinct candidates without replacement, ordered choices give n×(n−1). Every unordered pair has two orderings, so divide by 2. With replacement, the choice count and duplicate argument change.

**Q:** Why are two draws without replacement not independent?

**A:** The first draw changes the remaining population. After one of four distinct items is selected, a particular different item has conditional probability 1/3 on the next draw, not its original 1/4. Count the joint outcomes or multiply by the correct conditional probability.

## Summary

Check the modulus, invertibility, intermediate numeric range, and sample space before applying a formula. These conditions determine whether the arithmetic result has the intended meaning.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
