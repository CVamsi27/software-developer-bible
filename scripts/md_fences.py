#!/usr/bin/env python3
"""Nesting-aware CommonMark fence tracking — the single fence owner.

Every script that classifies markdown lines as inside/outside a code fence
used to carry its own `in_fence = not in_fence` toggle. That toggle desyncs
on nested fences (a ``` line inside a ```` block flips it off and the rest
of the file is misclassified as prose) — a bug class proven real on
2026-09-20 when a repair pass built on the naive toggle corrupted three
files. This module is now the only fence parser; import `walk`.

Semantics (documented trade-off): a fence line closes the block when it
uses the SAME character at >= the opener's length — including a labeled
close, which CommonMark renderers would treat as content. The corpus gate
(check_template.fence_problems) rejects labeled closes, so no passing file
can distinguish the two readings; closing on them makes every consumer
self-healing if one ever appears. Shorter or other-character fence lines
inside a block are content, which is what makes documented nested-fence
examples (``` inside ````) parse correctly.
"""
import re

FENCE_LINE = re.compile(r'^\s*(`{3,}|~{3,})(.*)$')


def walk(lines):
    """Yield (index, line, in_fence, is_fence_line) for each line.

    `in_fence` is the state AFTER processing the line; `is_fence_line` is
    True only on lines that actually open or close a block — a ``` line
    inside a ```` block is content (in_fence=True, is_fence_line=False),
    NOT a delimiter. Consumers may trust is_fence_line as 'safe to treat
    as a delimiter'; pairing it with the naive regex match instead would
    let fixers misedit nested-fence content — the repair-pass bug class
    this module exists to prevent:

        for i, line, in_fence, is_fence in md_fences.walk(lines):
            if is_fence:
                continue
            if in_fence:
                continue   # or handle code content
            ...            # prose handling
    """
    in_fence = False
    open_char, open_len = '', 0
    for i, line in enumerate(lines):
        m = FENCE_LINE.match(line)
        is_fence_line = False
        if m:
            marker = m.group(1)
            if in_fence:
                if marker[0] == open_char and len(marker) >= open_len:
                    in_fence = False
                    is_fence_line = True
                # shorter / other-char fence line inside a block: content
            else:
                in_fence = True
                open_char, open_len = marker[0], len(marker)
                is_fence_line = True
        yield i, line, in_fence, is_fence_line
