"""Exercise the real Jekyll hook in a tiny, isolated site without model execution."""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


class BuildTest(unittest.TestCase):
    def test_build_discovery_exclusions_and_cleanup(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'source'
            destination = Path(directory) / 'site'
            for path in ('_plugins', 'scripts', '_layouts', '_posts', '_drafts'):
                (source / path).mkdir(parents=True, exist_ok=True)
            shutil.copy(REPO / '_plugins/markdown_exports.rb', source / '_plugins')
            shutil.copy(REPO / 'scripts/export_markdown.py', source / 'scripts')
            (source / '_config.yml').write_text('url: http://localhost:4000\nmarkdown_exports_origin: https://example.com\nname: Lambert Leong\ntitle: Test site\nexclude: [scripts]\n')
            (source / '_layouts/default.html').write_text('<html><head><title>{{ page.title }}</title></head><body><main>{{ content }}</main></body></html>')
            (source / 'index.html').write_text('---\nlayout: default\ntitle: Home\n---\n<h1>Home</h1><p>{{ site.name }}</p>{% for post in site.posts %}<p>{{ post.title }}</p>{% endfor %}')
            article = source / '_posts/2020-01-01-test.md'
            article.write_text('---\nlayout: default\ntitle: Test post\npermalink: /thoughts/test\n---\n## Working example\n\n```python\nx = 1\n```\n')
            for filename, fields in [('hidden', 'hide: true'), ('unpublished', 'published: false'), ('disabled', 'markdown_export: false'), ('nositemap', 'sitemap: false')]:
                (source / (filename + '.html')).write_text(f'---\nlayout: default\ntitle: {filename}\n{fields}\n---\n<p>Do not export.</p>')
            (source / '_drafts/private.md').write_text('---\nlayout: default\ntitle: Private draft\n---\nPrivate draft body')
            (source / '_posts/2999-01-01-future.md').write_text('---\nlayout: default\ntitle: Future\n---\nFuture body')
            (source / 'redirect.html').write_text('---\nlayout: default\ntitle: Redirect\n---\n<meta http-equiv="refresh" content="0;url=/">')
            (source / 'private.html').write_text('---\nlayout: default\ntitle: Noindex\n---\n<meta name="robots" content="noindex">')
            (source / 'nested').mkdir()
            (source / 'nested/index.html').write_text('---\nlayout: default\ntitle: Nested\n---\n<p>Nested content</p>')

            def build(*flags):
                result = subprocess.run(['bundle', 'exec', 'jekyll', 'build', '--source', str(source), '--destination', str(destination), *flags], cwd=REPO, text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            build()
            exports = sorted(p.relative_to(destination).as_posix() for p in destination.rglob('*.md'))
            self.assertEqual(exports, ['index.md', 'nested/index.md', 'thoughts/test.md'])
            self.assertIn('Lambert Leong', (destination / 'index.md').read_text())
            self.assertIn('```python\nx = 1\n```', (destination / 'thoughts/test.md').read_text())
            self.assertIn('href="https://example.com/thoughts/test.md"', (destination / 'thoughts/test.html').read_text())
            self.assertNotIn('type="text/markdown"', (destination / 'hidden.html').read_text())
            self.assertNotIn('Private draft', (destination / 'llms.txt').read_text())
            article.write_text(article.read_text().replace('title: Test post', 'title: Test post\npublished: false'))
            (source / 'new.html').write_text('---\nlayout: default\ntitle: New page\n---\n<p>Automatically included</p>')
            build()
            self.assertFalse((destination / 'thoughts/test.md').exists())
            self.assertTrue((destination / 'new.md').exists())
            self.assertNotIn('/thoughts/test.md', (destination / 'llms.txt').read_text())
            self.assertIn('/new.md', (destination / 'llms.txt').read_text())
            build('--drafts', '--future')
            self.assertFalse((destination / 'llms.txt').exists())
            self.assertEqual(list(destination.rglob('*.md')), [])
            build()
            build('--unpublished')
            self.assertFalse((destination / 'llms.txt').exists())
            self.assertEqual(list(destination.rglob('*.md')), [])


if __name__ == '__main__':
    unittest.main()
