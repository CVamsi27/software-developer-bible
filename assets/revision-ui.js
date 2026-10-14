/* Reveal only explicit authored Q/A groups in category revision companions. */
document.addEventListener('DOMContentLoaded', function () {
  if (!/\/REVISION(?:\.html)?$/i.test(location.pathname)) return;
  var content = document.querySelector('.post-content');
  if (!content || content.querySelector('.revision-controls')) return;
  function marker(node, kind) { return node && node.tagName === 'P' && node.firstElementChild && node.firstElementChild.tagName === 'STRONG' && node.firstElementChild.textContent.trim() === kind + ':' && !node.firstChild.textContent.trim().replace(kind + ':', ''); }
  var questions = Array.from(content.children).filter(function (node) { return marker(node, 'Q'); });
  var answers = [];
  questions.forEach(function (question) {
    var answer = question.nextElementSibling;
    if (!marker(answer, 'A')) return;
    var nodes = [], current = answer;
    while (current && !/^H[1-6]$/.test(current.tagName) && !marker(current, 'Q') && current.tagName !== 'HR') {
      nodes.push(current); current = current.nextElementSibling;
    }
    var details = document.createElement('details'); details.className = 'revision-answer';
    var summary = document.createElement('summary'); summary.textContent = 'Show answer';
    details.append(summary); answer.before(details); nodes.forEach(function (node) { details.append(node); });
    details.addEventListener('toggle', function () { summary.textContent = details.open ? 'Hide answer' : 'Show answer'; });
    answers.push(details);
  });
  if (!answers.length) return;
  var controls = document.createElement('div'); controls.className = 'revision-controls';
  var hint = document.createElement('p'); hint.textContent = 'Try each question, then reveal its answer.';
  var all = document.createElement('button'); all.type = 'button'; all.dataset.revealAll = ''; all.textContent = 'Show all answers'; all.setAttribute('aria-expanded', 'false');
  function update() { var everyOpen = answers.every(function (answer) { return answer.open; }); all.textContent = everyOpen ? 'Hide all answers' : 'Show all answers'; all.setAttribute('aria-expanded', String(everyOpen)); }
  all.addEventListener('click', function () { var open = !answers.every(function (answer) { return answer.open; }); answers.forEach(function (answer) { answer.open = open; }); update(); });
  answers.forEach(function (answer) { answer.addEventListener('toggle', update); });
  var printState = null;
  window.addEventListener('beforeprint', function () { printState = answers.map(function (answer) { return answer.open; }); answers.forEach(function (answer) { answer.open = true; }); });
  window.addEventListener('afterprint', function () { if (printState) answers.forEach(function (answer, index) { answer.open = printState[index]; }); printState = null; update(); });
  controls.append(hint, all);
  var firstGroup = content.querySelector('h2'); if (firstGroup) firstGroup.before(controls); else questions[0].before(controls);
});
