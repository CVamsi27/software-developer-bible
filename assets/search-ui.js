/* Metadata search. URL state is restored on Back; roadmap context stays validated. */
document.addEventListener('DOMContentLoaded', function () {
  'use strict';
  var data = document.getElementById('study-search-data');
  if (!data || document.querySelector('#results .search-result')) return;
  var rows = JSON.parse(data.textContent), state = {q: '', sec: [], cat: [], tag: [], material: ''};
  var q = document.getElementById('q'), resultList = document.getElementById('results');
  var count = document.getElementById('result-count'), chips = document.getElementById('selected-filters');
  var labels = {learn: 'Learn', revision: 'Revision', interview: 'Interview practice', reference: 'Reference'};
  ['sec', 'cat', 'tag'].forEach(function (key) {
    var values = new Set();
    rows.forEach(function (r) { (key === 'tag' ? r.g : [r[key === 'sec' ? 's' : 'c']]).forEach(function (v) { if (v) values.add(v); }); });
    Array.from(values).sort().forEach(function (value) {
      var option = document.createElement('option'); option.value = value; option.textContent = value;
      document.getElementById(key).append(option);
    });
  });
  function restore() {
    var params = new URLSearchParams(location.search);
    state.q = params.get('q') || ''; q.value = state.q;
    ['sec', 'cat', 'tag'].forEach(function (key) {
      state[key] = (params.get(key) || '').split(',').filter(Boolean);
      document.getElementById(key).value = state[key][0] || '';
    });
    state.material = labels[params.get('material')] ? params.get('material') : '';
    document.getElementById('material').value = state.material;
  }
  function sync() {
    var params = new URLSearchParams();
    if (state.q) params.set('q', state.q);
    ['sec', 'cat', 'tag'].forEach(function (key) { if (state[key].length) params.set(key, state[key].join(',')); });
    if (state.material) params.set('material', state.material);
    var context = window.GermanyRoadmapReturn && window.GermanyRoadmapReturn.context(location.search);
    if (context) { params.set('roadmapDate', context.date); params.set('roadmapTask', context.task); }
    history.replaceState(null, '', location.pathname + (params.size ? '?' + params : '') + location.hash);
  }
  function render() {
    var query = state.q.trim().toLocaleLowerCase();
    var paths = window.StudyPublishedPaths;
    var matches = rows.filter(function (r) {
      if (location.protocol !== 'file:' && Array.isArray(paths) && !paths.includes('/' + r.p)) return false;
      return (!query || [r.t, r.s, r.c].concat(r.g).join(' ').toLocaleLowerCase().includes(query)) &&
        (!state.sec.length || state.sec.includes(r.s)) && (!state.cat.length || state.cat.includes(r.c)) &&
        (!state.tag.length || state.tag.some(function (t) { return r.g.includes(t); })) &&
        (!state.material || window.StudyState.material(r) === state.material);
    });
    resultList.replaceChildren();
    matches.forEach(function (r) {
      var item = document.createElement('li'); item.className = 'search-result';
      var link = document.createElement('a'); link.className = 'result-title'; link.textContent = r.t;
      var href = new URL(r.p, location.href).href;
      link.href = window.GermanyRoadmapReturn ? window.GermanyRoadmapReturn.chapterWithContext(href, location.search) : href;
      var context = document.createElement('p'); context.className = 'result-context'; context.textContent = [r.s, r.c].filter(Boolean).join(' / ');
      var meta = document.createElement('p'); meta.className = 'result-meta'; meta.textContent = labels[window.StudyState.material(r)] + ' · ' + r.m + ' min read';
      item.append(link, context, meta); resultList.append(item);
    });
    count.textContent = matches.length + (matches.length === 1 ? ' topic' : ' topics');
    document.getElementById('empty-state').hidden = matches.length !== 0;
    chips.replaceChildren();
    var active = [];
    ['sec', 'cat', 'tag'].forEach(function (key) { state[key].forEach(function (value) { active.push({key: key, value: value, label: value}); }); });
    if (state.material) active.push({key: 'material', value: state.material, label: labels[state.material]});
    active.forEach(function (filter) {
      var button = document.createElement('button'); button.type = 'button'; button.textContent = filter.label + ' — remove';
      button.setAttribute('aria-label', 'Remove ' + filter.label + ' filter');
      button.addEventListener('click', function () {
        if (filter.key === 'material') state.material = '';
        else state[filter.key] = state[filter.key].filter(function (v) { return v !== filter.value; });
        document.getElementById(filter.key).value = filter.key === 'material' ? state.material : state[filter.key][0] || '';
        sync(); render(); document.getElementById(filter.key).focus();
      });
      chips.append(button);
    });
    document.querySelector('[data-clear-filters]').hidden = active.length === 0;
  }
  var timer;
  q.addEventListener('input', function () { clearTimeout(timer); state.q = q.value; render(); timer = setTimeout(sync, 180); });
  q.addEventListener('keydown', function (event) {
    if (event.key === 'ArrowDown') { var first = resultList.querySelector('a'); if (first) { event.preventDefault(); first.focus(); } }
  });
  document.getElementById('search-form').addEventListener('submit', function (event) { event.preventDefault(); clearTimeout(timer); sync(); render(); });
  ['sec', 'cat', 'tag', 'material'].forEach(function (key) {
    document.getElementById(key).addEventListener('change', function (event) {
      state[key] = key === 'material' ? event.target.value : event.target.value ? [event.target.value] : [];
      sync(); render();
    });
  });
  document.getElementById('clear-query').addEventListener('click', function () { clearTimeout(timer); state.q = ''; q.value = ''; sync(); render(); q.focus(); });
  document.querySelector('[data-clear-filters]').addEventListener('click', function () {
    ['sec', 'cat', 'tag'].forEach(function (key) { state[key] = []; document.getElementById(key).value = ''; });
    state.material = ''; document.getElementById('material').value = ''; sync(); render(); document.getElementById('material').focus();
  });
  window.addEventListener('popstate', function () { clearTimeout(timer); restore(); render(); });
  document.addEventListener('keydown', function (event) {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); q.focus(); q.select(); }
  });
  restore();
  if (Array.isArray(window.StudyPublishedPaths) || location.protocol === 'file:') render();
  else {
    count.textContent = 'Loading the library…';
    var catalog = document.createElement('script'); catalog.src = 'assets/study-catalog.js';
    catalog.onload = render;
    catalog.onerror = function () { count.textContent = 'Search could not load. Browse the library or reload to try again.'; document.getElementById('empty-state').hidden = false; };
    document.head.append(catalog);
  }
});
