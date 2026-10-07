<!-- section: Node.js | category: Reference | tags: revision | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Node.js-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Node.js — Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Node.js Security

Source: [Node.js Security](20.1.4.01-node-security.md)

**Q:** Why is a valid report format insufficient permission to export an order?

**A:** Validation checks the request shape. The server must separately authenticate the caller and authorize the specific tenant/resource before invoking the export operation.

**Q:** What remains dangerous after shell interpretation is removed?

**A:** The executable still interprets options and accesses resources using process authority. A fixed operation, validated arguments, controlled paths/privileges and bounded output/runtime remain necessary.

**Q:** Why does a null-prototype dictionary not solve every prototype-pollution path?

**A:** It avoids inherited-property behavior for that dictionary. A later generic deep merge or privileged lookup on another object can still introduce unsafe property paths; prefer known schema fields and explicit construction.

**Q:** Can a Node permission flag safely run a malicious dependency?

**A:** The official permission model protects trusted code from unintended resource use; it does not promise isolation from malicious code. Use a separate OS isolation boundary for untrusted execution.

## Debugging & Profiling Node.js

Source: [Debugging & Profiling Node.js](20.1.4.02-debugging-profiling-nodejs.md)

**Q:** How do CPU usage and event-loop utilization describe different resources?

**A:** Process CPU includes other threads and isolates. Utilization describes active/idle loop time and is not a CPU percentage; correlate interval differences with delay, traces and workload.

**Q:** Why can an automatic snapshot near OOM worsen an incident?

**A:** Building the snapshot stops work in its thread and needs substantial additional memory, potentially doubling heap use and crashing the process. Capture on an instance whose interruption/loss is acceptable with private storage and spare capacity.

**Q:** Why is counting TCPSocketWrap resources not an FD metric?

**A:** Active resource types describe work keeping the loop alive. They are not an exhaustive count of OS descriptors; use platform metrics for open descriptors.

## Express & Fastify Internals

Source: [Express & Fastify Internals](20.1.4.03-express-fastify-internals.md)

**Q:** What connects a mounted Express router to the outer application stack?

**A:** The application dispatches into the router layer, strips the mount path from req.url for inner matching, sets req.baseUrl, and retains the original URL. next can continue within or back out of the nested dispatch.

**Q:** Which Fastify phase receives the object before it becomes the response payload?

**A:** preSerialization can shape suitable object payloads before serialization; onSend sees the serialized payload and may also receive stream/buffer/string/null forms. Return that payload rather than encoding it again.

**Q:** Does fastify-plugin always make a decoration global?

**A:** It normally skips encapsulation for that registration, so additions land in its parent scope. If the parent is an encapsulated feature, visibility remains within that subtree.

**Q:** Why does a response schema not make every data leak impossible?

**A:** It constrains the response path/status/schema where it is applied. Other schemas, additionalProperties, raw writes, streams and later hooks can emit different data; authorization and every response path still need review.

## Summary

Use these prompts after the reading pass to recall the mechanism and its limits.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide the API documentation and further reading.
