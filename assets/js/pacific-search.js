(function () {
  'use strict';
  var disclosure = document.getElementById('header-search');
  if (!disclosure) return;
  var trigger = disclosure.querySelector('summary');
  var input = document.getElementById('header-search-input');
  var results = document.getElementById('header-search-results');
  var status = disclosure.querySelector('[role="status"]');
  var indexPromise;

  function loadIndex() {
    if (!indexPromise) {
      indexPromise = fetch(disclosure.dataset.index).then(function (response) {
        if (!response.ok) throw new Error('Search unavailable');
        return response.json();
      }).catch(function (error) {
        indexPromise = undefined;
        throw error;
      });
    }
    return indexPromise;
  }

  function search() {
    var query = input.value.trim().toLocaleLowerCase();
    results.replaceChildren();
    if (!query) {
      status.textContent = 'Search thoughts, projects, and more.';
      return;
    }
    status.textContent = 'Searching…';
    loadIndex().then(function (posts) {
      if (input.value.trim().toLocaleLowerCase() !== query) return;
      var words = query.split(/\s+/);
      var matches = posts.filter(function (post) {
        var text = [post.title, post.summary, post.description, post.category, post.label].join(' ').toLocaleLowerCase();
        return words.every(function (word) { return text.includes(word); });
      });
      results.replaceChildren();
      matches.slice(0, 6).forEach(function (post) {
        var url = new URL(post.url, window.location.origin);
        if (url.origin !== window.location.origin) return;
        var item = document.createElement('li');
        var link = document.createElement('a');
        link.href = url.href;
        link.textContent = post.title;
        item.appendChild(link);
        results.appendChild(item);
      });
      status.textContent = matches.length ? matches.length + ' result' + (matches.length === 1 ? '' : 's') + (matches.length > 6 ? ' — showing the first 6.' : '.') : 'No matching posts. Try another keyword.';
    }).catch(function () {
      if (input.value.trim().toLocaleLowerCase() === query) status.textContent = 'Search could not load. Please try again.';
    });
  }

  disclosure.addEventListener('toggle', function () {
    if (disclosure.open) input.focus();
  });
  input.addEventListener('input', search);
  disclosure.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault();
    search();
  });
  disclosure.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
      disclosure.open = false;
      trigger.focus();
    }
  });
  document.addEventListener('click', function (event) {
    if (disclosure.open && !disclosure.contains(event.target)) disclosure.open = false;
  });
}());
