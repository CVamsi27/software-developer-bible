const test = require('node:test');
const assert = require('node:assert/strict');
const { splitText, createReader, groupChunks, pickStartGroup, rankVoices, wordAt } = require('./read-aloud.js');
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
test('plays chunks in order', () => {
  const {reader, spoken, updates} = setup();
  reader.start(['First', 'Second']); assert.equal(spoken[0].text, 'First');
  spoken[0].onend();
  assert.equal(spoken[1].text, 'Second');
  spoken[1].onend(); assert.equal(updates.at(-1), 'idle');
});
test('pause ignores cancellation completion and resumes its current chunk', () => {
  const {reader, spoken} = setup(); reader.start(['First', 'Second']);
  reader.togglePause(); spoken[0].onend(); assert.equal(spoken.length, 1);
  reader.togglePause(); assert.equal(spoken.length, 2);
  assert.equal(spoken[1].text, 'First');
  spoken[1].onend(); assert.equal(spoken[2].text, 'Second');
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
  reader.setRate(0.5);
  reader.start(['First', 'Second']);
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

test('every requested tenth-speed reaches the speech engine without a 0.5 floor', () => {
  for (const rate of [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2]) {
    const {reader, spoken} = setup();
    reader.setRate(rate); reader.start(['A passage.']);
    assert.equal(spoken[0].rate, rate);
  }
});
test('invalid speeds fall back to normal and out-of-range speeds are bounded', () => {
  for (const [input, expected] of [[0.01, 0.2], [3, 2], ['bad', 1], [Infinity, 1], [0, 1]]) {
    const {reader, spoken} = setup();
    reader.setRate(input); reader.start(['A passage.']);
    assert.equal(spoken[0].rate, expected);
  }
});
test('a live speed change resumes at the last word boundary and ignores old callbacks', () => {
  const {reader, spoken, updates} = setup();
  reader.start(['First words keep going.', 'Next passage.']);
  const old = spoken[0]; old.onboundary({name: 'word', charIndex: 12});
  reader.setRate(0.3);
  assert.equal(spoken[1].text, 'keep going.'); assert.equal(spoken[1].rate, 0.3);
  old.onend(); old.onerror({error: 'interrupted'});
  assert.equal(spoken.length, 2); assert.equal(updates.at(-1), 'reading');
  spoken[1].onend(); assert.equal(spoken[2].text, 'Next passage.');
});
test('voice and speed changes while paused do not play until resume', () => {
  const {reader, spoken} = setup();
  reader.start(['First words keep going.']);
  spoken[0].onboundary({name: 'word', charIndex: 12});
  reader.togglePause(); reader.setRate(0.2);
  const voice = {voiceURI: 'samantha', lang: 'en-US'};
  reader.setVoice(voice);
  assert.equal(spoken.length, 1);
  reader.togglePause();
  assert.equal(spoken[1].text, 'keep going.');
  assert.equal(spoken[1].rate, 0.2); assert.equal(spoken[1].voice, voice);
});
test('repeated setting changes retain an absolute word position', () => {
  const {reader, spoken} = setup(); reader.start(['One two three four.']);
  spoken[0].onboundary({name: 'word', charIndex: 4}); reader.setRate(0.3);
  spoken[1].onboundary({name: 'word', charIndex: 4}); reader.setRate(1.2);
  assert.equal(spoken[2].text, 'three four.');
});
test('short speech chunks prefer complete sentence endings', () => {
  const first = 'This whole sentence should end before the next one begins. ';
  const chunks = splitText(first + 'A longer explanation '.repeat(20));
  assert.equal(chunks[0], first.trim());
  assert.ok(chunks.every(text => text.length <= 240));
});
test('Samantha and enhanced variants lead local English voices without novelty or network voices', () => {
  const voice = (name, voiceURI, lang = 'en-US', localService = true) => ({name, voiceURI, lang, localService, default: false});
  const voices = [voice('Victoria', 'victoria'), voice('Ava (Enhanced)', 'ava-enhanced'),
    voice('Zarvox', 'robot'), voice('Samantha', 'samantha'), voice('Samantha (Premium)', 'samantha-premium'),
    voice('Microsoft Jenny Natural', 'remote', 'en-US', false), voice('Amélie', 'fr', 'fr-FR'),
    voice('Daniel', 'daniel', 'en-GB'), voice('Samantha', 'samantha')];
  assert.deepEqual(rankVoices(voices).map(v => v.voiceURI), ['samantha-premium', 'samantha', 'ava-enhanced', 'daniel', 'victoria']);
  assert.deepEqual(rankVoices(voices.slice().reverse()).map(v => v.voiceURI), ['samantha-premium', 'samantha', 'ava-enhanced', 'daniel', 'victoria']);
});
test('the listening menu excludes the legacy and character voices seen in the browser', () => {
 const names=['Eddy (English (United States))','Flo (English (United Kingdom))','Fred','Grandma (English (United States))','Grandpa (English (United Kingdom))','Kathy','Reed (English (United States))','Rocko (English (United States))','Sandy (English (United Kingdom))','Shelley (English (United States))','Samantha','Daniel','Karen','Rishi'];
 const voices=names.map(name=>({name,voiceURI:name,lang:'en-US',localService:true}));
 assert.deepEqual(rankVoices(voices).map(v=>v.name),['Samantha','Daniel','Karen','Rishi']);
});
test('unmarked or unavailable local services cannot silently select a remote default', () => {
  assert.deepEqual(rankVoices([{name: 'Samantha', voiceURI: 'unknown', lang: 'en-US'}, null,
    {name: 'Google US English', voiceURI: 'network', lang: 'en-US', localService: false}]), []);
});
test('a voice-list refresh with the same voice does not interrupt speech', () => {
  const {reader, spoken} = setup();
  reader.setVoice({voiceURI: 'samantha', lang: 'en-US'}); reader.start(['Keep reading.']);
  reader.setVoice({voiceURI: 'samantha', lang: 'en-US'});
  assert.equal(spoken.length, 1);
});
test('events from a finished chunk cannot skip or move the next chunk', () => {
  const {reader, spoken} = setup(); reader.start(['First chunk.', 'Second chunk.', 'Third chunk.']);
  const old = spoken[0]; old.onend(); old.onend(); old.onerror();
  assert.equal(spoken.length, 2); assert.equal(spoken[1].text, 'Second chunk.');
  spoken[1].onend(); assert.equal(spoken[2].text, 'Third chunk.');
});
test('a word boundary identifies one word when the engine omits its length', () => {
  assert.deepEqual(wordAt('Read this example now.', 10, 0), {start: 10, end: 17});
  assert.deepEqual(wordAt('Read this example now.', 18, undefined), {start: 18, end: 21});
  assert.deepEqual(wordAt('“Don’t” stop.', 1, 0), {start: 1, end: 6});
  assert.deepEqual(wordAt('A résumé example.', 2, 0), {start: 2, end: 8});
  assert.equal(wordAt('Read this.', -1, 0), null);
  assert.equal(wordAt('Read this.', 10, 0), null);
  assert.equal(wordAt('Read this.', 4, 0), null);
});
test('a supplied word length can highlight a spoken part of an acronym', () => {
  assert.deepEqual(wordAt('API calls.', 0, 1), {start: 0, end: 1});
  assert.deepEqual(wordAt('API calls.', 4, 99), {start: 4, end: 9});
});
test('word callbacks retain original chunk offsets after speed changes and resume', () => {
  const spoken = [], words = [], chunk = {text: 'Read this example now.', element: {}};
  const synth = {speak(u) { spoken.push(u); }, resume() {}, cancel() {}};
  const reader = createReader(synth, function (text) { this.text = text; }, () => {}, () => {},
    (source, start, end) => words.push({source, start, end}));
  reader.start([chunk]);
  spoken[0].onboundary({name: 'word', charIndex: 10, charLength: 0});
  assert.deepEqual(words.at(-1), {source: chunk, start: 10, end: 17});
  reader.setRate(.3);
  spoken[1].onboundary({name: 'word', charIndex: 8, charLength: 3});
  assert.deepEqual(words.at(-1), {source: chunk, start: 18, end: 21});
  reader.togglePause();
  spoken[0].onboundary({name: 'word', charIndex: 0});
  spoken[1].onboundary({name: 'word', charIndex: 0});
  assert.equal(words.length, 2, 'obsolete or paused speech cannot move the highlight');
  reader.togglePause(); spoken[2].onboundary({name: 'word', charIndex: 0, charLength: 3});
  assert.deepEqual(words.at(-1), {source: chunk, start: 18, end: 21});
  spoken[2].onboundary({name: 'sentence', charIndex: 0});
  spoken[2].onboundary({name: 'word', charIndex: 100});
  assert.equal(words.length, 3, 'sentence and invalid boundaries leave the current word alone');
});
