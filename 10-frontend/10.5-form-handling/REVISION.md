<!-- section: Form Handling | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Form%20Handling-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../docs/topic-importance.md)

# Form Handling — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## React Hook Form

Source: [React Hook Form](10.5.01-react-hook-form.md)

**Q:** How can an uncontrolled RHF input still cause React renders?

**A:** Watch and form-state subscribers react to changes. Uncontrolled DOM values avoid one root state update per keystroke, but do not make the whole application render-free.

## Zod

Source: [Zod](10.5.02-zod.md)

**Q:** Why can z.input and z.output differ for the same Zod schema?

**A:** Transforms, preprocessing and coercion can accept one input type and return another. z.infer describes the output, so form defaults and parsed results may need different types.

## Formik

Source: [Formik](10.5.03-formik.md)

**Q:** Why should resetForm run after confirmed success rather than in finally?

**A:** Finally also runs after failure. Resetting there can destroy the user's input before they can correct or retry it.

## TanStack Form

Source: [TanStack Form](10.5.04-tanstack-form.md)

**Q:** Why must a TanStack form-level validator use an object schema?

**A:** It receives the entire values object, whereas a field validator receives its field value. Validation transformations also do not automatically replace form values.

## Server Actions & Modern Form Patterns

Source: [Server Actions & Modern Form Patterns](10.5.05-server-actions-and-form-patterns.md)

**Q:** Why pass the server function directly to useActionState for progressive enhancement?

**A:** The framework can preserve the server-function form path and return state before hydration. A client-only wrapper requires JavaScript and does not inherit that contract.

**Q:** Why is an uploaded file's name or MIME type not enough to accept it?

**A:** The browser submits both as untrusted metadata. Enforce size and format policy on the server, inspect and decode content as needed, generate a storage key, and authorize access. For larger files, use a scoped direct-upload path and validate it again before finalizing.

## Autosave & Draft Recovery

Source: [Autosave & Draft Recovery](10.5.06-autosave-draft-recovery.md)

**Q:** Why stop and drain the autosave writer before deleting a submitted draft?

**A:** A queued or in-flight write can recreate the draft after deletion. Stop new scheduling, await prior writes, then clear storage.

## Form state versus business commitment

Source: [Learning chapter](10.5.01-react-hook-form.md)

**Q:** Why does disabling submit while isSubmitting not guarantee one booking?

**A:** It controls this UI while the awaited callback runs. Network uncertainty, another client or direct API retry still needs a server-side idempotency/transaction contract.

**Q:** What must a multistep form do beyond retaining unmounted values?

**A:** Validate visible steps before advancing and validate the complete payload at final submit and on the server. Retained values alone do not rerun every unmounted built-in field rule.


## Parsing and conversion boundaries

Source: [Learning chapter](10.5.02-zod.md)

**Q:** Why is z.input different from z.output for a string-to-number schema?

**A:** The raw accepted value is a string, while the successfully parsed value is a number. z.infer describes output, so form collection and submit types can differ.

**Q:** Why should textual false not go through z.coerce.boolean blindly?

**A:** JavaScript Boolean of a nonempty string is true. Explicitly map the permitted textual values before treating them as booleans.

**Q:** Does a parsed invoice payload establish tenant permission?

**A:** No. The schema establishes shape/constraints; authorization, ownership and transactional business invariants remain separate checks.
## Controlled submission and selected subscriptions

Source: [Formik](10.5.03-formik.md), [TanStack Form](10.5.04-tanstack-form.md)

**Q:** Why can a synchronous wizard Next handler leave Formik pending?
**A:** A non-promise submit handler must explicitly settle isSubmitting. Changing the step alone does not finish the submission cycle.

**Q:** Why does a stable row ID coexist with an indexed form path?
**A:** React identity should follow the row after removal/reordering, while its field path describes the current position in the model.

**Q:** A schema transform validates successfully. Does TanStack automatically submit that transformed value?
**A:** No. Parse deliberately at the submit boundary when normalized output is needed; validation and model replacement are different jobs.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
