#!/bin/zsh

export PATH="$(ruby -e 'print Gem.user_dir')/bin:$PATH"

echo "view in browser at http://localhost:4000"
bundle exec jekyll serve
