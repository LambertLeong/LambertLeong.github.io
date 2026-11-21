# Generate alternate content formats from the same rendered pages used by the site.
require 'json'
require 'open3'
require 'cgi'
require 'fileutils'

module MarkdownExports
  class Output < Jekyll::StaticFile
    def initialize(site, path, content)
      super(site, site.source, File.dirname(path), File.basename(path))
      @content = content
    end

    def write(dest)
      target = destination(dest)
      FileUtils.mkdir_p(File.dirname(target))
      File.write(target, @content, mode: 'w', encoding: 'UTF-8')
      true
    end

    def modified?
      true
    end
  end

  def self.path_for(url)
    path = url.split('?').first
    return "#{path}index.md" if path.end_with?('/')
    path.sub(/\.html?\z/, '') + '.md'
  end

  def self.date(value)
    value.respond_to?(:strftime) ? value.strftime('%Y-%m-%d') : value&.to_s
  end

  def self.generate(site)
    # Watch rebuilds must replace, rather than accumulate, prior generated files.
    site.static_files.reject! { |file| file.is_a?(Output) }
    if site.config['show_drafts'] || site.config['future'] || site.config['unpublished']
      Jekyll.logger.warn 'Markdown exports:', 'disabled for draft/future/unpublished previews'
      return
    end
    base = (site.config['markdown_exports_origin'] || site.config.fetch('url', '')).sub(%r{/$}, '') + site.baseurl.to_s.sub(%r{/$}, '')
    raise 'Markdown exports require an absolute site url' unless base.match?(%r{\Ahttps?://})

    candidates = (site.pages + site.collections.values.flat_map(&:docs)).select do |doc|
      doc.output_ext == '.html' && doc.data['published'] != false &&
        !doc.data['hide'] && doc.data['sitemap'] != false &&
        doc.data['layout'] != 'redirect' && !doc.data['redirect_to'] &&
        !doc.data['markdown_export'].equal?(false) &&
        !(doc.respond_to?(:draft?) && doc.draft?) &&
        !(doc.respond_to?(:date) && doc.date > site.time) &&
        !doc.url.start_with?('/404', '/_tmp/')
    end
    pages = candidates.map do |doc|
      categories = Array(doc.data['categories'])
      author = site.config.fetch('authors', {})[doc.data['author']] || {}
      {
        'path' => path_for(doc.url), 'url' => base + doc.url,
        'title' => doc.data['title'] || site.config['title'],
        'author' => author['display_name'] || author['name'] || site.config['name'],
        'date' => date(doc.data['date']),
        'updated' => date(doc.data['last_modified_at'] || doc.data['lastmod']),
        'group' => categories.first || 'Pages', 'html' => doc.output
      }
    end
    result, error, status = Open3.capture3('python3', File.join(site.source, 'scripts/export_markdown.py'), stdin_data: JSON.generate(pages))
    raise "Markdown export failed: #{error}" unless status.success?
    exports = JSON.parse(result).select { |entry| entry['markdown'] }
    by_path = exports.to_h { |entry| [entry['path'], entry] }
    raise 'Duplicate Markdown output URL' unless by_path.size == exports.size
    reserved = site.static_files.map(&:relative_path) + site.pages.map(&:url)
    exports.each do |entry|
      raise "Markdown output would overwrite #{entry['path']}" if reserved.include?(entry['path'])
      site.static_files << Output.new(site, entry['path'], entry['markdown'])
    end
    candidates.each do |doc|
      next unless by_path.key?(path_for(doc.url))
      links = "<link rel=\"alternate\" type=\"text/markdown\" href=\"#{CGI.escapeHTML(base + path_for(doc.url))}\">\n" \
              "<link rel=\"describedby\" type=\"text/plain\" href=\"#{CGI.escapeHTML(base + '/llms.txt')}\">\n"
      doc.output = doc.output.sub('</head>', links + '</head>')
    end
    index = ["# #{site.config['name']}", '', '> Published pages, thoughts, projects, and experience from Lambert Leong, PhD.', '',
             'These Markdown files contain the same content as the public webpages. Each includes its original webpage URL for citation.', '']
    exports.group_by { |entry| entry['group'] }.sort.each do |group, entries|
      index << "## #{group.to_s.capitalize}"
      index << ''
      entries.sort_by { |entry| [entry['title'].to_s, entry['path']] }.each do |entry|
        title = entry['title'].to_s.gsub(/[\r\n]/, ' ').gsub('[', '\\[').gsub(']', '\\]')
        index << "- [#{title}](#{base}#{entry['path']})"
      end
      index << ''
    end
    raise 'llms.txt already exists in source' if reserved.include?('/llms.txt')
    site.static_files << Output.new(site, '/llms.txt', index.join("\n") + "\n")
    Jekyll.logger.info 'Markdown exports:', "#{exports.size} pages and llms.txt"
  end
end

Jekyll::Hooks.register :site, :post_render do |site|
  MarkdownExports.generate(site)
end
