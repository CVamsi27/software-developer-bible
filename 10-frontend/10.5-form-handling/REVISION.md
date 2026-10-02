<!-- section: Form Handling | category: Reference | tags: revision, retrieval-practice -->
[![Section](https://img.shields.io/badge/section-Form%20Handling-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

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

## Autosave & Draft Recovery

Source: [Autosave & Draft Recovery](10.5.06-autosave-draft-recovery.md)

**Q:** Why stop and drain the autosave writer before deleting a submitted draft?

**A:** A queued or in-flight write can recreate the draft after deletion. Stop new scheduling, await prior writes, then clear storage.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
