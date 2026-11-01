const test = require('node:test');
const assert = require('node:assert/strict');
const { splitText, createReader, groupChunks, pickStartGroup } = require('./read-aloud.js');
function setup() {
  const spoken = []; const updates = [];
  const synth = { speak(u) { spoken.push(u); }, pause() {}, resume() {}, cancel() {} };
  const reader = createReader(synth, function (text) { this.text = text; }, state => updates.push(state));
  return { reader, spoken, updates };
}
test('short chunks preserve all prose including long unpunctuated words', () => {
  const text = 'A sentence. ' + 'x'.repeat(700) + ' Final sentence.';
  const chunks = splitText(text);
  assert.ok(chunks.every(x => x.length <= 240));
  assert.equal(chunks.join('').replace(/\s/g, ''), text.replace(/\s/g, ''));
});
test('plays in order and applies speed to subsequent utterances', () => {
  const {reader, spoken, updates} = setup();
  reader.start(['First', 'Second']); assert.equal(spoken[0].text, 'First');
  reader.setRate(1.5); spoken[0].onend();
  assert.equal(spoken[1].text, 'Second'); assert.equal(spoken[1].rate, 1.5);
  spoken[1].onend(); assert.equal(updates.at(-1), 'idle');
});
test('completion while paused waits for resume', () => {
  const {reader, spoken} = setup(); reader.start(['First', 'Second']);
  reader.togglePause(); spoken[0].onend(); assert.equal(spoken.length, 1);
  reader.togglePause(); assert.equal(spoken.length, 2);
});
test('stop ignores late events from a canceled narration', () => {
  const {reader, spoken, updates} = setup(); reader.start(['Old', 'Obsolete']);
  const old = spoken[0]; reader.stop(); reader.start(['New']); old.onend();
  old.onerror({error: 'interrupted'});
  assert.equal(spoken.length, 2); assert.equal(updates.at(-1), 'reading');
});
test('speech failures return a recoverable error state', () => {
  const {reader, spoken, updates} = setup(); reader.start(['Text']);
  spoken[0].onerror({error: 'synthesis-failed'}); assert.equal(updates.at(-1), 'error');
  reader.start(['Retry']); assert.equal(updates.at(-1), 'reading');
});
test('starting a chunk reports the source element that owns it', () => {
  const source = {};
  const spoken = [];
  const started = [];
  const synth = { speak(u) { spoken.push(u); }, pause() {}, resume() {}, cancel() {} };
  const reader = createReader(synth, function (text) { this.text = text; }, () => {}, element => started.push(element));
  reader.start([{text: 'First paragraph', element: source}]);
  assert.equal(spoken[0].text, 'First paragraph');
  spoken[0].onstart();
  assert.deepEqual(started, [source]);
});
test('late starts from a canceled utterance do not activate its source element', () => {
  const obsoleteSource = {};
  const spoken = [];
  const started = [];
  const synth = { speak(u) { spoken.push(u); }, pause() {}, resume() {}, cancel() {} };
  const reader = createReader(synth, function (text) { this.text = text; }, () => {}, element => started.push(element));
  reader.start([{text: 'Old', element: obsoleteSource}]);
  const obsoleteUtterance = spoken[0];
  reader.stop();
  obsoleteUtterance.onstart();
  assert.deepEqual(started, []);
});
test('0.5 speed applies to the next speech chunk', () => {
  const {reader, spoken} = setup();
  reader.start(['First', 'Second']);
  reader.setRate(0.5);
  spoken[0].onend();
  assert.equal(spoken[1].rate, 0.5);
});
test('a paragraph can finish in a ready state instead of racing on', () => {
  const {reader, spoken, updates} = setup();
  reader.start(['Only paragraph'], {doneState: 'ready'});
  spoken[0].onend();
  assert.equal(updates.at(-1), 'ready');
  assert.equal(spoken.length, 1);
});
test('the selected voice is applied to the next utterance', () => {
  const spoken = [];
  const voice = {name: 'Reader', voiceURI: 'reader', lang: 'en-GB'};
  const synth = {speak(u) { spoken.push(u); }, pause() {}, resume() {}, cancel() {}};
  const reader = createReader(synth, function (text) { this.text = text; }, () => {});
  reader.setVoice(voice);
  reader.start(['Hello']);
  assert.equal(spoken[0].voice, voice);
  assert.equal(spoken[0].lang, 'en-GB');
});
test('source blocks group their chunks into paragraph units', () => {
  const first = {getBoundingClientRect: () => ({bottom: 100})};
  const second = {getBoundingClientRect: () => ({bottom: 200})};
  const groups = groupChunks([
    {text: 'First part', element: first},
    {text: 'First part continued', element: first},
    {text: 'Second block', element: second}
  ]);
  assert.deepEqual(groups.map(group => group.chunks.map(chunk => chunk.text)), [
    ['First part', 'First part continued'],
    ['Second block']
  ]);
});
test('a scrolled chapter starts at the first block in view, not the title', () => {
  const group = bottom => ({element: {getBoundingClientRect: () => ({bottom})}});
  const groups = [group(-420), group(280), group(600)];
  assert.equal(pickStartGroup(groups, 220), 1);
  assert.equal(pickStartGroup([group(-10), group(-20)], 220), 1);
  assert.equal(pickStartGroup([], 220), -1);
});
