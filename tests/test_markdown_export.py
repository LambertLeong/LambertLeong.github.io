import importlib.util
from pathlib import Path
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'scripts' / 'export_markdown.py'
spec = importlib.util.spec_from_file_location('export_markdown', MODULE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class MarkdownExportTest(unittest.TestCase):
    def render(self, body, **kwargs):
        page = dict(url='https://www.lambertleong.com/thoughts/example', title='Example',
                    author='Lambert Leong', html='<html><head></head><body><main>'+body+'</main></body></html>')
        page.update(kwargs)
        return m.export_page(page)

    def test_content_links_and_attribution(self):
        result = self.render('<h1>Example</h1><h2>Result</h2><p>A <strong>useful</strong> result. <a href="/projects">Projects</a></p><img src="../assets/chart.png" alt="Accuracy by size">', date='2026-11-20')
        self.assertEqual(result.count('# Example\n'), 1)
        self.assertIn('## Result', result)
        self.assertIn('**useful**', result)
        self.assertIn('[Projects](https://www.lambertleong.com/projects)', result)
        self.assertIn('![Accuracy by size](https://www.lambertleong.com/assets/chart.png)', result)
        self.assertIn('Author: Lambert Leong', result)
        self.assertIn('Published: 2026-11-20', result)
        self.assertIn('Original: https://www.lambertleong.com/thoughts/example', result)

    def test_code_math_tables_and_nested_lists(self):
        result = self.render('<pre><code class="language-python">x = 1\n\n\nprint(x &lt; 2)\n</code></pre><script type="math/tex; mode=display">x^2 + y^2</script><table><tr><th>A</th><th>B</th></tr><tr><td>1</td><td>2</td></tr></table><ol><li>First<ul><li>Nested</li></ul></li><li>Second</li></ol>')
        self.assertIn('```python\nx = 1\n\n\nprint(x < 2)\n```', result)
        self.assertIn('$$\nx^2 + y^2\n$$', result)
        self.assertIn('| A | B |\n| --- | --- |\n| 1 | 2 |', result)
        self.assertIn('1. First\n   - Nested', result)
        self.assertIn('2. Second', result)

    def test_article_body_excludes_navigation_and_related_posts(self):
        result = self.render('<nav>Category</nav><article><h1>Example</h1><div class="article-post"><p>Actual article</p></div><aside>Related posts</aside></article>')
        self.assertIn('Actual article', result)
        self.assertNotIn('Related posts', result)
        self.assertNotIn('Category', result)

    def test_cover_and_scientific_notation(self):
        result = self.render('<article><figure class="pacific-article-cover"><img src="/cover.png" alt="Study diagram"></figure><div class="article-post"><p>H<sub>2</sub>O and x<sup>2</sup></p></div></article>')
        self.assertIn('![Study diagram](https://www.lambertleong.com/cover.png)', result)
        self.assertIn('H<sub>2</sub>O', result)
        self.assertIn('x<sup>2</sup>', result)

    def test_literal_text_and_inline_code(self):
        result = self.render('<p>Literal *stars* and [text](https://example.org).</p><p><code>a  b</code></p><p>\\[x_1 + y^2\\]</p>')
        self.assertIn(r'Literal \*stars\* and \[text\](https://example.org).', result)
        self.assertIn('`a  b`', result)
        self.assertIn(r'\[x_1 + y^2\]', result)

    def test_scripts_and_forms(self):
        result = self.render('<script>SECRET_SCRIPT</script><style>.secret{}</style><form><input><button>Send</button></form><p>Contact <a href="mailto:a@example.com">email</a>.</p>')
        self.assertNotIn('SECRET_SCRIPT', result)
        self.assertNotIn('.secret', result)
        self.assertIn('form on the original page', result)
        self.assertIn('mailto:a@example.com', result)

    def test_no_main_and_redirects_are_not_exported(self):
        self.assertIsNone(m.export_page(dict(html='<meta http-equiv="refresh" content="0;url=/about"><main>Redirect</main>', url='https://example.com/', title='Redirect')))
        self.assertIsNone(m.export_page(dict(html='<p>No content region</p>', url='https://example.com/', title='Nothing')))

if __name__ == '__main__':
    unittest.main()
