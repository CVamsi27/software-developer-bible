"""Generated-site navigation regressions; no network or browser required."""
import tempfile
import unittest
from pathlib import Path
from check_rendered_links import audit_site


class RenderedLinks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.site = self.root / '_site'
        self.site.mkdir()

    def write(self, name, text):
        target = self.site / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def test_missing_published_page_fails_even_when_its_source_exists(self):
        self.write('index.html', '<a href="81-lane/guide.md">Guide</a>')
        source = self.root / '81-lane/guide.md'
        source.parent.mkdir(); source.write_text('# Excluded source')
        report = audit_site(self.site)
        self.assertTrue(any('81-lane/guide.md' in error for error in report['errors']))

    def test_relative_links_queries_and_fragments_resolve(self):
        self.write('index.html', '<a href="topics/lesson.html?from=home#example">Study</a>')
        self.write('topics/lesson.html', '<h2 id="example">Example</h2><a href="../index.html">Home</a>')
        self.assertEqual(audit_site(self.site)['errors'], [])

    def test_markdown_url_is_not_a_published_html_url(self):
        self.write('index.html', '<a href="topics/lesson.md">Study</a>')
        self.write('topics/lesson.html', '<h1>Lesson</h1>')
        self.assertTrue(audit_site(self.site)['errors'])

    def test_legacy_badge_links_require_the_reader_and_a_published_html_target(self):
        self.write('index.html', '<script src="assets/reading-ui.js?v=1"></script><a href="topics/lesson.md#example">Study</a>')
        self.write('assets/reading-ui.js', '// Reader asset')
        self.write('topics/lesson.html', '<h2 id="example">Example</h2>')
        report = audit_site(self.site)
        self.assertEqual(report['errors'], [])
        self.assertEqual(report['readerMarkdownLinks'], 1)

    def test_missing_fragment_fails(self):
        self.write('index.html', '<a href="#absent">Missing section</a>')
        self.assertTrue(any('absent' in error for error in audit_site(self.site)['errors']))

    def test_function_endpoint_requires_a_real_route(self):
        self.write('index.html', '<a href="/auth/start">Sign in</a>')
        functions = self.root / 'functions'
        (functions / 'auth').mkdir(parents=True)
        (functions / 'auth/start.ts').write_text('export function onRequestGet() {}')
        self.assertEqual(audit_site(self.site, functions)['errors'], [])
        (functions / 'auth/start.ts').unlink()
        self.assertTrue(audit_site(self.site, functions)['errors'])

    def test_local_assets_are_checked_and_external_sources_are_skipped(self):
        self.write('index.html', '<a href="https://github.com/example/source">Source</a><img src="/missing.png"><script src="/missing.js"></script>')
        errors = audit_site(self.site)['errors']
        self.assertEqual(len(errors), 2)
        self.assertTrue(any('missing.png' in error for error in errors))

    def test_same_host_absolute_links_are_internal(self):
        self.write('index.html', '<a href="https://study.buildora.work/missing.html">Missing</a>')
        self.assertTrue(audit_site(self.site)['errors'])

    def test_empty_site_cannot_pass(self):
        self.assertTrue(audit_site(self.site)['errors'])

    def test_explicit_local_aliases_keep_home_and_library_fragments_separate(self):
        self.write('index.html', '<h1 id="library">Physical collision</h1>')
        self.write('home-preview.html', '<a href="/INDEX.html#library">Library</a><a href="/">Home</a>')
        self.write('library-preview.html', '<h1 id="library">Library</h1>')
        aliases = {'index.html': 'home-preview.html', 'INDEX.html': 'library-preview.html'}
        self.assertEqual(audit_site(self.site, aliases=aliases)['errors'], [])
        self.write('library-preview.html', '<h1 id="different">Library</h1>')
        self.assertTrue(audit_site(self.site, aliases=aliases)['errors'])

    def test_raw_repository_document_can_remain_an_actual_published_file(self):
        self.write('index.html', '<a href="contributing.md">Source guide</a>')
        self.write('contributing.md', '# Contribution conventions')
        self.assertEqual(audit_site(self.site)['errors'], [])

    def test_directory_routes_cannot_depend_on_case_insensitive_index_lookup(self):
        self.write('index.html', '<a href="topics/">Topics</a>')
        self.write('topics/INDEX.html', '<h1>Topics</h1>')
        self.assertTrue(audit_site(self.site)['errors'])
        self.write('index.html', '<a href="topics/INDEX.html">Topics</a>')
        self.assertEqual(audit_site(self.site)['errors'], [])


if __name__ == '__main__':
    unittest.main()
