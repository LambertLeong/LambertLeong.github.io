"""Convert rendered public page content to Markdown using only the standard library."""
import json
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit


class Node:
    def __init__(self, tag='', attrs=()):
        self.tag = tag
        self.attrs = dict(attrs)
        self.children = []
        self.parent = None

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()

    def text(self):
        return ''.join(c.text() if isinstance(c, Node) else c for c in self.children)


class Document(HTMLParser):
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        node.parent = self.stack[-1]
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                self.stack = self.stack[:index]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)



def escape_text(text):
    # MathJax delimiters remain intact; ordinary prose must stay literal.
    math = r'(\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|\$[^$\n]+\$)'
    parts = re.split(math, text)
    for index in range(0, len(parts), 2):
        parts[index] = re.sub(r'([\\`*\[\]_<>])', r'\\\1', parts[index])
        parts[index] = re.sub(r'^(\s*)([#>+\-]|\d+\.)(?=\s)', lambda m: m[1] + '\\' + m[2] if not m[2][0].isdigit() else m[1] + m[2][:-1] + r'\.', parts[index])
    return ''.join(parts)


class Markdown:
    BLOCKS = {'p', 'div', 'section', 'article', 'header', 'footer', 'main', 'figure', 'figcaption', 'center', 'details', 'summary', 'dl', 'dt', 'dd'}

    def __init__(self, url):
        self.url = url

    def link(self, value):
        value = urljoin(self.url, value or '')
        if urlsplit(value).scheme not in ('http', 'https', 'mailto', 'tel'):
            return ''
        return value.replace(' ', '%20').replace('(', '%28').replace(')', '%29')

    def children(self, node):
        return ''.join(self.render(c) for c in node.children)

    def render(self, node):
        if isinstance(node, str):
            return escape_text(re.sub(r'\s+', ' ', node))
        tag, attrs = node.tag, node.attrs
        if tag == 'script' and attrs.get('type', '').startswith('math/tex'):
            math = node.text().strip()
            return '\n\n$$\n' + math + '\n$$\n\n' if 'display' in attrs['type'] else '$' + math + '$'
        if tag in {'script', 'style', 'noscript', 'nav', 'button', 'input', 'select', 'textarea'} or 'hidden' in attrs:
            return ''
        if tag == 'pre':
            code = next((n for n in node.walk() if n.tag == 'code'), node)
            ancestor = node
            classes = code.attrs.get('class', '')
            while ancestor is not None:
                classes += ' ' + ancestor.attrs.get('class', '')
                ancestor = ancestor.parent
            language = re.search(r'language-([\w+-]+)', classes)
            text = code.text().rstrip('\n')
            fence = '`' * max(3, max((len(s) + 1 for s in re.findall(r'`+', text)), default=3))
            return '\n\n' + fence + (language.group(1) if language else '') + '\n' + text + '\n' + fence + '\n\n'
        if tag == 'img':
            src = self.link(attrs.get('src') or attrs.get('data-src'))
            alt = (attrs.get('alt') or '').replace('[', '\\[').replace(']', '\\]')
            return f'![{alt}]({src})' if src else ''
        if tag == 'form':
            return f'\n\n[Use the form on the original page]({self.link(self.url)}).\n\n'
        if tag in {'iframe', 'video', 'audio'}:
            src = attrs.get('src') or next((n.attrs.get('src') for n in node.walk() if n.tag == 'source'), '')
            return f'\n\n[Embedded media]({self.link(src)})\n\n' if src else self.children(node)
        if tag == 'table':
            rows = []
            for row in node.walk():
                if row.tag == 'tr':
                    cells = [self.children(c).strip().replace('|', '\\|').replace('\n', '<br>') for c in row.children if isinstance(c, Node) and c.tag in {'td', 'th'}]
                    if cells:
                        rows.append(cells)
            if not rows:
                return ''
            width = max(map(len, rows))
            rows = [r + [''] * (width - len(r)) for r in rows]
            rows.insert(1, ['---'] * width)
            return '\n\n' + '\n'.join('| ' + ' | '.join(r) + ' |' for r in rows) + '\n\n'
        if tag in {'ul', 'ol'}:
            items = []
            start = int(attrs.get('start', '1')) if str(attrs.get('start', '1')).isdigit() else 1
            for child in node.children:
                if isinstance(child, Node) and child.tag == 'li':
                    prefix = f'{start + len(items)}. ' if tag == 'ol' else '- '
                    content = self.children(child).strip()
                    lines = content.splitlines()
                    items.append(prefix + ('\n' + ' ' * len(prefix)).join(lines))
            return '\n' + '\n'.join(items) + '\n'
        text = self.children(node)
        if re.fullmatch(r'h[1-6]', tag):
            return '\n\n' + '#' * int(tag[1]) + ' ' + text.strip() + '\n\n'
        if tag in {'strong', 'b'}:
            return '**' + text.strip() + '**' if text.strip() else ''
        if tag in {'em', 'i'}:
            return '*' + text.strip() + '*' if text.strip() else ''
        if tag in {'sub', 'sup'}:
            return f'<{tag}>{text}</{tag}>'
        if tag == 'code':
            text = node.text()
            fence = '`' * max(1, max((len(s) + 1 for s in re.findall(r'`+', text)), default=1))
            return fence + ' ' + text + ' ' + fence if '`' in text else fence + text + fence
        if tag == 'a':
            href = self.link(attrs.get('href')) if attrs.get('href') else ''
            return f'[{text.strip()}]({href})' if href and text.strip() else text
        if tag == 'blockquote':
            return '\n\n' + '\n'.join('> ' + line for line in text.strip().splitlines()) + '\n\n'
        if tag == 'br':
            return '\n'
        if tag == 'hr':
            return '\n\n---\n\n'
        if tag in self.BLOCKS:
            return '\n\n' + text.strip() + '\n\n' if text.strip() else ''
        return text


def tidy(text):
    lines = []
    fence = None
    for line in text.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if fence:
            lines.append(line)
            if match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence):
                fence = None
        elif match:
            fence = match.group(1)
            lines.append(line)
        elif line.strip():
            lines.append(line.rstrip())
        elif lines and lines[-1] != '':
            lines.append('')
    return '\n'.join(lines).strip() + '\n'


def export_page(page):
    root = Document(page['html']).root
    nodes = list(root.walk())
    for node in nodes:
        if node.tag == 'meta':
            attrs = node.attrs
            if attrs.get('http-equiv', '').lower() == 'refresh':
                return None
            if attrs.get('name', '').lower() == 'robots' and 'noindex' in attrs.get('content', '').lower():
                return None
    main = next((n for n in nodes if n.tag == 'main'), None)
    if main is None:
        return None
    body = next((n for n in main.walk() if 'article-post' in n.attrs.get('class', '').split()), main)
    converter = Markdown(page['url'])
    content = converter.children(body).strip()
    cover = next((n for n in main.walk() if 'pacific-article-cover' in n.attrs.get('class', '').split()), None)
    if cover is not None and body is not main:
        content = converter.render(cover).strip() + '\n\n' + content
    title = re.sub(r'\s+', ' ', page.get('title') or 'Lambert Leong').strip()
    # A single document title accompanies the citation metadata.
    content = re.sub(r'^# ' + re.escape(title) + r'\s*\n', '', content, count=1).lstrip()
    metadata = [f'# {title}', '', 'Author: ' + page.get('author', 'Lambert Leong'), 'Original: ' + page['url']]
    if page.get('date'):
        metadata.append('Published: ' + page['date'])
    if page.get('updated'):
        metadata.append('Updated: ' + page['updated'])
    metadata.extend(['', 'Please cite the original webpage linked above.', '', '---', '', content, ''])
    return tidy('\n'.join(metadata))


def main():
    pages = json.load(sys.stdin)
    json.dump([dict(path=p['path'], title=p['title'], group=p['group'], markdown=export_page(p)) for p in pages], sys.stdout)


if __name__ == '__main__':
    main()
