#!/usr/bin/env python3
"""Check generated pages, local assets and fragments against the built artifact.

Source existence does not prove publication: Jekyll can exclude a linked page.
Run after building: python3 scripts/check_rendered_links.py _site --json report.json
"""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        key = 'href' if tag in ('a', 'link') else 'src' if tag in ('img', 'script') else ''
        if key and attrs.get(key):
            self.links.append(attrs[key])


def audit_site(site_root, functions_root=None, aliases=None):
    root = Path(site_root).resolve()
    functions = Path(functions_root).resolve() if functions_root else None
    aliases = aliases or {}
    # Path.is_file() accepts INDEX.html as index.html on macOS. Route checks
    # must use the exact emitted spelling, as Cloudflare and Linux do.
    files = {p.resolve() for p in root.rglob('*') if p.is_file()}
    pages = {}
    for path in sorted(root.rglob('*.html')):
        parser = PageLinks()
        parser.feed(path.read_text(errors='replace'))
        pages[path.resolve()] = parser
    report = {'htmlFiles': len(pages), 'checkedLinks': 0, 'readerMarkdownLinks': 0, 'errors': []}
    if not pages:
        report['errors'].append('No rendered HTML pages found; build the site first.')
        return report
    origin = 'https://study.buildora.work/'
    for source, parser in pages.items():
        relative = source.relative_to(root).as_posix()
        if relative in aliases and aliases[relative] != relative:
            continue  # This local file is served through its explicit preview alias.
        has_reader = any(urlsplit(href).path.endswith('/assets/reading-ui.js') or urlsplit(href).path == 'assets/reading-ui.js' for href in parser.links)
        for href in parser.links:
            url = urlsplit(urljoin(origin + relative, href))
            if url.scheme not in ('http', 'https') or url.netloc != urlsplit(origin).netloc:
                continue
            report['checkedLinks'] += 1
            name = unquote(url.path).lstrip('/')
            target = (root / name).resolve()
            if not target.is_relative_to(root):
                report['errors'].append(f'{relative}: {href} escapes the built site')
                continue
            candidates = [target]
            if url.path.endswith('/') or not target.suffix:
                candidates = [target / 'index.html']
                if target != root:
                    candidates.append(Path(str(target) + '.html'))
            elif target.suffix == '.md':
                # reading-ui resolves legacy badge hrefs through the rendered
                # catalog. A copied raw Markdown file is not a reader route.
                html = target.with_suffix('.html')
                preview = aliases.get(html.relative_to(root).as_posix())
                if preview:
                    html = root / preview
                if has_reader and html in files:
                    candidates = [html]
                    report['readerMarkdownLinks'] += 1
            candidates = [root / aliases.get(p.relative_to(root).as_posix(), p.relative_to(root).as_posix()) for p in candidates]
            resolved = next((p for p in candidates if p in files), None)
            if resolved is None:
                route = functions / name if functions else None
                if route and not route.name.startswith('_') and any(Path(str(route) + ext).is_file() for ext in ('.ts', '.js')):
                    continue
                report['errors'].append(f'{relative}: {href} has no published destination')
                continue
            if url.fragment and resolved.suffix == '.html':
                page = pages.get(resolved.resolve())
                if page and unquote(url.fragment) not in page.ids:
                    report['errors'].append(f'{relative}: {href} has no rendered fragment')
    report['errors'] = sorted(set(report['errors']))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('site', nargs='?', default='_site')
    parser.add_argument('--functions', default='functions')
    parser.add_argument('--json', type=Path)
    parser.add_argument('--preview-aliases', type=Path, help='Local case-insensitive preview route map; omitted in CI')
    args = parser.parse_args()
    aliases = json.loads(args.preview_aliases.read_text()) if args.preview_aliases else None
    report = audit_site(args.site, args.functions, aliases)
    if aliases:
        report['previewAliases'] = aliases
    if args.json:
        args.json.write_text(json.dumps(report, indent=2) + '\n')
    for error in report['errors']:
        print(error)
    print(f"Rendered links: {report['htmlFiles']} HTML pages, {report['checkedLinks']} links, {len(report['errors'])} errors")
    return int(bool(report['errors']))


if __name__ == '__main__':
    raise SystemExit(main())
