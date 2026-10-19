#!/usr/bin/env python3
"""Regression tests for generated study-time text."""

import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_counts  # noqa: E402
import read_time  # noqa: E402


class StudyTimeGrammarTests(unittest.TestCase):
    def test_source_walk_ignores_generated_and_vendored_markdown(self):
        with tempfile.TemporaryDirectory() as root:
            stack = os.path.join(root, "10-stack")
            rendered_stack = os.path.join(root, "_site", "10-stack")
            vendor_stack = os.path.join(root, "vendor", "10-stack")
            os.makedirs(stack)
            os.makedirs(rendered_stack)
            os.makedirs(vendor_stack)
            with open(os.path.join(stack, "INDEX.md"), "w", encoding="utf-8") as index:
                index.write("# Source index\n")
            with open(os.path.join(stack, "chapter.md"), "w", encoding="utf-8") as chapter:
                chapter.write("# Source chapter\n")
            with open(os.path.join(rendered_stack, "INDEX.md"), "w", encoding="utf-8") as index:
                index.write("# Rendered index\n")
            with open(os.path.join(rendered_stack, "chapter.md"), "w", encoding="utf-8") as chapter:
                chapter.write("# Rendered chapter\n")
            with open(os.path.join(vendor_stack, "dependency.md"), "w", encoding="utf-8") as chapter:
                chapter.write("# Dependency documentation\n")

            original_root = read_time.ROOT
            original_counts_root = check_counts.ROOT
            try:
                read_time.ROOT = root
                check_counts.ROOT = root
                self.assertEqual(list(read_time.content_files()), ["10-stack/chapter.md"])
                self.assertEqual(list(read_time.index_files()), [os.path.join(stack, "INDEX.md")])
                self.assertEqual(check_counts.repo_totals(), (2, 2))
            finally:
                read_time.ROOT = original_root
                check_counts.ROOT = original_counts_root

    def render_index(self, chapter_count):
        with tempfile.TemporaryDirectory() as root:
            stack = os.path.join(root, "stack")
            os.makedirs(stack)
            index_path = os.path.join(stack, "INDEX.md")
            with open(index_path, "w", encoding="utf-8") as index:
                index.write("# Study Stack\n")
            for number in range(chapter_count):
                with open(
                    os.path.join(stack, f"chapter-{number}.md"),
                    "w",
                    encoding="utf-8",
                ) as chapter:
                    chapter.write(f"# Chapter {number}\n\nA short concept.\n")

            original_root = read_time.ROOT
            try:
                read_time.ROOT = root
                read_time.write_indexes()
                with open(index_path, encoding="utf-8") as index:
                    return index.read()
            finally:
                read_time.ROOT = original_root

    def test_single_chapter_uses_singular_file(self):
        generated = self.render_index(1)
        self.assertIn("(1 file, ~2 min average)", generated)

    def test_multiple_chapters_use_plural_files(self):
        generated = self.render_index(2)
        self.assertIn("(2 files, ~2 min average)", generated)

    def test_stale_read_time_row_refreshes_even_when_study_line_matches(self):
        """A row-only drift is still a change the writer must write.

        History: comparing the rewrite against the already-refreshed text hid
        row fixes from --write and from the fixed-point gate, so an INDEX could
        ship an 8 min row next to a 9 min badge and nothing flagged it.
        """
        with tempfile.TemporaryDirectory() as root:
            stack = os.path.join(root, "stack")
            os.makedirs(stack)
            index_path = os.path.join(stack, "INDEX.md")
            with open(index_path, "w", encoding="utf-8") as index:
                index.write(
                    "# Study Stack\n\n"
                    "> **Study time:** ≈ 3 min of reading (1 file, ~3 min average).\n\n"
                    "| Order | File | Topics | Read time |\n"
                    "| --- | --- | --- | ---: |\n"
                    "| 01 | [Chapter](chapter.md) | Words | 99 min |\n"
                )
            with open(os.path.join(stack, "chapter.md"), "w", encoding="utf-8") as chapter:
                chapter.write("# Chapter\n\n" + "word " * 600 + "\n")

            original_root = read_time.ROOT
            try:
                read_time.ROOT = root
                read_time.write_indexes()
            finally:
                read_time.ROOT = original_root
            with open(index_path, encoding="utf-8") as index:
                self.assertIn("| 3 min |", index.read())


if __name__ == "__main__":
    unittest.main()
