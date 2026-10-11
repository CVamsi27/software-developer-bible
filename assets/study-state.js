/* Shared, dependency-free study rules. No query or private context is persisted. */
(function (root) {
  'use strict';
  var key = 'sdb-study-resume-v1';
  function material(row) {
    if (/interview[-_ ]questions/i.test(row.p)) return 'interview';
    if (/\/REVISION\.html$/i.test(row.p)) return 'revision';
    if (row.c === 'Reference' || (row.g || []).includes('reference')) return 'reference';
    return 'learn';
  }
  function isLearningPath(path) {
    return typeof path === 'string' && /^\/(?:\d{2}(?:\.\d+)?-[^/]+\/)+\d{2}(?:\.\d+)+-[a-z0-9-]+\.html$/.test(path) &&
      !/\/personal\/|interview-questions|\/auth\//i.test(path);
  }
  function clean(record, paths) {
    if (!record || record.version !== 1 || !isLearningPath(record.path) || !paths.includes(record.path) ||
        typeof record.anchor !== 'string' || record.anchor.length > 250 || /[\s?#/]/.test(record.anchor) ||
        typeof record.savedAt !== 'number' || !Number.isFinite(record.savedAt) || record.savedAt <= 0 ||
        record.savedAt > Date.now() + 60000 || typeof record.title !== 'string' || !record.title.trim() ||
        typeof record.section !== 'string') return null;
    return {version: 1, path: record.path, anchor: record.anchor, title: record.title.slice(0, 160),
      section: record.section.slice(0, 160), savedAt: record.savedAt};
  }
  function createStore(storage, paths) {
    paths = Array.isArray(paths) ? paths : [];
    var memory = null, initialized = false;
    function read() {
      if (!initialized) {
        initialized = true;
        try { memory = clean(JSON.parse(storage.getItem(key)), paths); } catch (_) { memory = null; }
        if (!memory) { try { storage.removeItem(key); } catch (_) {} }
      }
      return memory && Object.assign({}, memory);
    }
    function write(record) {
      var safe = clean(record, paths);
      if (!safe) return false;
      initialized = true; memory = safe;
      try { storage.setItem(key, JSON.stringify(safe)); } catch (_) {}
      return true;
    }
    function clear() {
      var previous = read(); initialized = true; memory = null;
      try { storage.removeItem(key); } catch (_) {}
      return previous;
    }
    return {read: read, write: write, clear: clear};
  }
  var api = {material: material, isLearningPath: isLearningPath, createStore: createStore};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.StudyState = api;
})(typeof window === 'undefined' ? globalThis : window);
