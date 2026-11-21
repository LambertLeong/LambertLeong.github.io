"""Validate generated alternate-format links before publishing a Jekyll build."""
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit
from export_markdown import Document


def check(root):
    root = Path(root)
    index = (root / 'llms.txt').read_text()
    paths = re.findall(r'^- \[.*\]\((https?://[^\s]+)\)$', index, re.M)
    if not paths:
        raise ValueError('llms.txt has no exported pages')
    for url in paths:
        path = urlsplit(url).path.lstrip('/')
        markdown = (root / path).read_text()
        if not markdown.startswith('# ') or '\nOriginal: https://' not in markdown:
            raise ValueError(f'Missing title or citation URL in {path}')
    discovered = set()
    for html in root.rglob('*.html'):
        if '_tmp' in html.relative_to(root).parts:
            continue
        document = Document(html.read_text()).root
        for node in document.walk():
            if node.tag == 'link' and node.attrs.get('rel') == 'alternate' and node.attrs.get('type') == 'text/markdown':
                url = node.attrs['href']
                if not (root / urlsplit(url).path.lstrip('/')).is_file():
                    raise ValueError(f'Broken alternate link in {html}: {url}')
                discovered.add(url)
    if discovered != set(paths):
        raise ValueError(f'Discovery links and llms.txt differ: {discovered.symmetric_difference(paths)}')
    print(f'Validated {len(paths)} Markdown exports, HTML discovery links, and llms.txt.')


if __name__ == '__main__':
    check(sys.argv[1] if len(sys.argv) > 1 else '_site')
