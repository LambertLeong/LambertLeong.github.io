# Markdown publishing

Every normal Jekyll build generates Markdown alongside the HTML. The source of truth is the existing page or post; do not maintain a second copy.

- `/about.html` (also served as `/about`) exports `/about.md`.
- `/thoughts/example` exports `/thoughts/example.md`.
- `/` exports `/index.md`; directory URLs export `index.md` inside that directory.
- `/llms.txt` lists all exported pages by category.
- Each HTML page links to its Markdown alternate and the directory in its head.
- Each export includes the original production URL, author, and available publication/update dates. Original HTML URLs remain in the sitemap.

The Jekyll hook in `_plugins/markdown_exports.rb` processes rendered HTML through `scripts/export_markdown.py` (Python 3 standard library only). This includes Liquid content, listings, articles, and galleries. It exports the main content, resolving links and images to absolute URLs. Interactive forms link back to the original page. PDFs and other binary assets remain links; the generator does not transcribe them or invent image descriptions.

Unpublished, hidden, future-dated, redirect, noindex, and error pages are excluded, as are pages with `sitemap: false`. Optional front matter `markdown_export: false` disables an individual export. Builds with `--drafts`, `--future`, or `--unpublished` disable all exports, including listings, so preview-only titles and excerpts cannot leak into them. When a page is removed or unpublished, Jekyll's normal cleanup removes its old export. Use full builds, not `--incremental` or `--safe`; safe mode disables custom plugins.

## Local review

```sh
python3 -m unittest discover -s tests -p 'test_markdown_export*.py'
bundle exec jekyll build
python3 scripts/check_markdown_exports.py _site
bundle exec jekyll serve --host 0.0.0.0 --port 4000
```

The hook also runs on Jekyll serve rebuilds. Generated exports are build artifacts and should not be committed separately. Preview exports deliberately contain production citation URLs, using `markdown_exports_origin` in `_config.yml` even when Jekyll serve overrides `url` with localhost.

## Publishing workflow

`.github/workflows/pages.yml` tests, builds, and verifies both formats for pull requests and pushes to master. Only a push to master or a manual run on master deploys. It never commits generated content to the repository. A failed conversion or validation blocks publication.

One-time setup when ready to publish: in the repository's **Settings → Pages → Build and deployment → Source**, select **GitHub Actions**. Branch-based GitHub Pages builds disable custom plugins and will not run this generator. Preserve the existing custom domain setting. After the workflow is committed and pushed, it creates the Pages artifact and deploys it. No local assistant rules or configuration are required.

Review a generated article, `/about.md`, and `/llms.txt` after the first deployment. Check the Actions build logs if Markdown files are missing.
