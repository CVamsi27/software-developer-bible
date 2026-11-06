/* Browser integration checks; install Playwright outside the checkout. */
let chromium;
try { ({chromium} = require('@playwright/test')); }
catch (_) { ({chromium} = require('playwright')); }
const assert = require('node:assert/strict');
const path = require('node:path');
const CHAPTER = '/10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.05-lexical-environment.html';
const ORIGIN = 'https://study.buildora.work';
const localVoice = (name, uri, lang = 'en-US') => ({name, voiceURI: uri, lang, localService: true, default: false});
const VOICES = [localVoice('Victoria', 'victoria'), localVoice('Samantha', 'samantha'), localVoice('Ava (Enhanced)', 'ava'),
  localVoice('Zarvox', 'robot'), localVoice('Daniel', 'daniel', 'en-GB'), localVoice('Karen', 'karen', 'en-AU'),
  localVoice('Moira', 'moira', 'en-IE'), localVoice('Amélie', 'fr', 'fr-FR'),
  {...localVoice('Microsoft Jenny Natural', 'remote'), localService: false}];
const TOKENS = '<style>:root{--theme-bg:#fff;--theme-text:#1f2937;--theme-text-muted:#4b5563;--theme-heading:#111827;--theme-border:#d1d5db;--theme-link:#1967d2;--theme-action-bg:#1967d2;--theme-action-text:#fff;--card-bg:#fff;--nav-pill-bg:#f3f4f6}html[data-theme="dark"]{--theme-bg:#111820;--theme-text:#d5deea;--theme-text-muted:#a4b3c5;--theme-heading:#f8fafc;--theme-border:#3c4b5d;--theme-link:#a8c7fa;--theme-action-bg:#a8c7fa;--theme-action-text:#062e6f;--card-bg:#18222d;--nav-pill-bg:#1e2b39;color-scheme:dark}body{margin:0;background:var(--theme-bg);color:var(--theme-text);font-family:sans-serif}.post-content{padding:24px;font-size:18px;line-height:1.7}</style>';
const ARTICLE = '<main class="post-content"><h1>Lexical Environment</h1><p>A lexical environment is used to find the variable for a name.</p><h2 id="one">Bindings</h2><p>Bindings connect a name to a value.</p><h2 id="two">Scope lookup</h2><p>Lookup walks outward until it finds a match.</p><h2 id="three">Nested functions</h2><p>Nested functions keep their outer references alive.</p><h2 id="four">A final example</h2><p>The final example shows the whole lookup.</p><pre><code>neverSpeakThisCode()</code></pre></main>';
function luminance(rgb) {
  const c = rgb.match(/[\d.]+/g).slice(0, 3).map(Number).map(v => { v /= 255; return v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; });
  return c[0] * .2126 + c[1] * .7152 + c[2] * .0722;
}
function contrast(a, b) { const x = luminance(a), y = luminance(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); }
(async () => {
  const browser = await chromium.launch({headless: true, executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH});
  try {
    async function open(options = {}) {
      const page = await browser.newPage({viewport: {width: 1280, height: 900}, reducedMotion: 'reduce'});
      await page.addInitScript(({voices, unsupported, denied, saved, legacy, fallbackHighlight}) => {
        window.recordedSpeech = []; window.voiceListeners = []; window.testVoices = voices;
        if (fallbackHighlight) Object.defineProperty(CSS, 'highlights', {value: undefined});
        if (saved) localStorage.setItem('sdb-read-aloud-settings-v1', JSON.stringify(saved));
        if (legacy) localStorage.setItem('sdb-read-aloud-voice-v2', legacy);
        if (denied) {
          Storage.prototype.getItem = () => { throw new DOMException('Unavailable', 'SecurityError'); };
          Storage.prototype.setItem = () => { throw new DOMException('Unavailable', 'SecurityError'); };
        }
        Object.defineProperty(window, 'speechSynthesis', {value: unsupported ? undefined : {
          cancel() { window.speechCancels = (window.speechCancels || 0) + 1; }, pause() {}, resume() {},
          speak(utterance) { window.recordedSpeech.push(utterance); }, getVoices() { return window.testVoices; },
          addEventListener(type, callback) { if (type === 'voiceschanged') window.voiceListeners.push(callback); }
        }});
        window.SpeechSynthesisUtterance = function (text) { this.text = text; };
      }, {voices: options.voices || VOICES, unsupported: options.unsupported, denied: options.denied, saved: options.saved, legacy: options.legacy, fallbackHighlight: options.fallbackHighlight});
      if (!options.rendered) await page.route(ORIGIN + '/**', async route => {
        const url = new URL(route.request().url());
        if (url.pathname.startsWith('/assets/')) return route.fulfill({path: path.resolve('.' + url.pathname)});
        const head = ['read-aloud.css', 'reading-ui.css', 'reference-reader.css'].map(file => '<link rel="stylesheet" href="/assets/' + file + '">').join('');
        const scripts = '<script>window.StudyPublishedPaths=' + JSON.stringify([CHAPTER]) + '</script>' + ['study-state.js', 'reading-ui.js', 'read-aloud.js'].map(file => '<script src="/assets/' + file + '" defer></script>').join('');
        return route.fulfill({contentType: 'text/html', body: '<!doctype html><html><head>' + TOKENS + head + scripts + '</head><body>' + (options.article || ARTICLE) + '</body></html>'});
      });
      await page.goto((options.rendered ? process.env.STUDY_TEST_URL.replace(/\/$/, '') : ORIGIN) + CHAPTER);
      await page.locator('.read-aloud').waitFor();
      return page;
    }
    const finish = page => page.evaluate(() => window.recordedSpeech.at(-1).onend());
    const settings = page => page.getByRole('button', {name: 'Audio settings', exact: true});
    const listen = page => page.getByRole('button', {name: 'Read aloud', exact: true});

    const page = await open();
    assert.equal(await page.locator('body > .read-aloud').count(), 1);
    assert.equal(await page.locator('.read-aloud').evaluate(n => getComputedStyle(n).position), 'fixed');
    await settings(page).click();
    assert.equal(await page.getByRole('combobox', {name: 'Reading voice'}).isVisible(), true, 'configure voice before playback');
    assert.equal(await page.locator('[data-voice]').inputValue(), 'samantha');
    assert.deepEqual(await page.locator('[data-voice] option').evaluateAll(nodes => nodes.map(n => n.value)), ['samantha', 'ava', 'daniel', 'karen', 'moira', 'victoria']);
    const rates = await page.locator('[data-speed] option').evaluateAll(nodes => nodes.map(n => Number(n.value)));
    for (const rate of [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.9, 1, 1.1, 1.2, 1.25, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2]) assert(rates.includes(rate), 'speed available: ' + rate);
    await page.selectOption('[data-speed]', '0.2');
    await page.getByRole('button', {name: 'Preview voice', exact: true}).click();
    assert.equal(await page.evaluate(() => window.recordedSpeech.at(-1).rate), .2);
    await finish(page);
    assert.equal(await page.locator('.read-aloud').getAttribute('data-state'), 'idle', 'preview does not start the chapter');
    await page.selectOption('[data-voice]', 'daniel');
    await page.selectOption('[data-mode]', 'paragraph');
    await page.locator('[data-follow]').uncheck();
    await page.reload(); await settings(page).click();
    assert.equal(await page.locator('[data-voice]').inputValue(), 'daniel');
    assert.equal(await page.locator('[data-speed]').inputValue(), '0.2');
    assert.equal(await page.locator('[data-mode]').inputValue(), 'paragraph');
    assert.equal(await page.locator('[data-follow]').isChecked(), false);
    await page.keyboard.press('Escape');
    assert.equal(await settings(page).getAttribute('aria-expanded'), 'false');
    assert.equal(await settings(page).evaluate(n => n === document.activeElement), true);
    await listen(page).click();
    assert.equal(await page.evaluate(() => window.recordedSpeech.at(-1).voice.voiceURI), 'daniel');
    await finish(page);
    assert.equal(await page.locator('.read-aloud').getAttribute('data-state'), 'ready');
    assert.equal(await page.evaluate(() => window.recordedSpeech.length), 1, 'manual mode waits after a passage');
    await page.getByRole('button', {name: 'Continue listening', exact: true}).click();
    assert.match(await page.evaluate(() => window.recordedSpeech.at(-1).text), /^A lexical/);
    await page.close();

    const continuous = await open();
    await listen(continuous).click(); await finish(continuous);
    assert.match(await continuous.evaluate(() => window.recordedSpeech.at(-1).text), /^A lexical/);
    await continuous.evaluate(() => window.recordedSpeech.at(-1).onstart());
    assert.equal(await continuous.locator('p[data-read-aloud-active]').count(), 1);
    await continuous.getByRole('button', {name: 'Next passage', exact: true}).click();
    assert.equal(await continuous.evaluate(() => window.recordedSpeech.at(-1).text), 'Bindings');
    await continuous.getByRole('button', {name: 'Previous passage', exact: true}).click();
    assert.match(await continuous.evaluate(() => window.recordedSpeech.at(-1).text), /^A lexical/);
    await settings(continuous).click();
    await continuous.evaluate(() => window.recordedSpeech.at(-1).onboundary({name: 'word', charIndex: 10}));
    await continuous.selectOption('[data-speed]', '0.3');
    assert.equal(await continuous.evaluate(() => window.recordedSpeech.at(-1).text), 'environment is used to find the variable for a name.');
    assert.equal(await continuous.evaluate(() => window.recordedSpeech.at(-1).rate), .3);
    await continuous.getByRole('button', {name: 'Pause', exact: true}).click();
    const beforeResume = await continuous.evaluate(() => window.recordedSpeech.length);
    await continuous.selectOption('[data-speed]', '2');
    assert.equal(await continuous.evaluate(() => window.recordedSpeech.length), beforeResume);
    await continuous.getByRole('button', {name: 'Resume', exact: true}).click();
    assert.equal(await continuous.evaluate(() => window.recordedSpeech.at(-1).rate), 2);
    const old = await continuous.evaluate(() => window.recordedSpeech.length - 1);
    await continuous.getByRole('button', {name: 'Preview voice', exact: true}).click();
    await finish(continuous);
    assert.equal(await continuous.locator('.read-aloud').getAttribute('data-state'), 'paused');
    await continuous.evaluate(i => window.recordedSpeech[i].onend(), old);
    assert.equal(await continuous.locator('.read-aloud').getAttribute('data-state'), 'paused', 'late chapter event cannot advance during preview');
    await continuous.getByRole('button', {name: 'Resume', exact: true}).click();
    for (let i = 0; i < 10 && await continuous.locator('.read-aloud').getAttribute('data-state') === 'reading'; i++) await finish(continuous);
    assert.equal(await continuous.locator('.read-aloud').getAttribute('data-state'), 'complete');
    assert.equal(await continuous.locator('[data-progress]').getAttribute('value'), '10');
    assert(!(await continuous.evaluate(() => window.recordedSpeech.map(u => u.text).join(' '))).includes('neverSpeakThisCode'));
    await continuous.getByRole('button', {name: 'Listen again', exact: true}).click();
    assert.equal(await continuous.evaluate(() => window.recordedSpeech.at(-1).text), 'Lexical Environment');
    await continuous.getByRole('button', {name: 'Stop', exact: true}).click();
    assert.equal(await continuous.locator('[data-read-aloud-active]').count(), 0);
    await continuous.locator('.post-content p').nth(1).click();
    await continuous.getByRole('button', {name: 'Read selected paragraph', exact: true}).click();
    assert.equal(await continuous.evaluate(() => window.recordedSpeech.at(-1).text), 'Bindings connect a name to a value.');
    const cancels = await continuous.evaluate(() => window.speechCancels);
    await continuous.evaluate(() => window.dispatchEvent(new Event('pagehide')));
    assert(await continuous.evaluate(() => window.speechCancels) > cancels);
    await continuous.close();

    const pending = await open(); await listen(pending).click();
    await pending.locator('.post-content p').nth(2).click();
    const pendingCount = await pending.evaluate(() => window.recordedSpeech.length);
    await finish(pending);
    assert.equal(await pending.evaluate(() => window.recordedSpeech.length), pendingCount, 'pending selection waits at the passage boundary');
    await pending.getByRole('button', {name: 'Read selected paragraph', exact: true}).click();
    assert.equal(await pending.evaluate(() => window.recordedSpeech.at(-1).text), 'Lookup walks outward until it finds a match.');
    await pending.close();

    const wordArticle = '<main class="post-content"><h1>Word tracking</h1><p id="word-tracking">  Read <strong>this</strong>   ex<em>am</em>ple <code>word</code> now.  </p><p>Next paragraph.</p></main>';
    const words = await open({article: wordArticle});
    const highlightedWord = page => page.evaluate(() => { const h = CSS.highlights.get('sdb-spoken-word'); return h && Array.from(h)[0].toString(); });
    const beforeWords = await words.locator('#word-tracking').innerHTML();
    await words.locator('#word-tracking').click();
    await words.getByRole('button', {name: 'Read selected paragraph', exact: true}).click();
    await words.evaluate(() => { window.previousSpeech = window.recordedSpeech.at(-1); previousSpeech.onstart(); previousSpeech.onboundary({name: 'word', charIndex: 10, charLength: 4}); });
    assert.equal(await highlightedWord(words), 'example', 'a word range crosses inline nodes and normalized whitespace exactly');
    assert.equal(await words.locator('#word-tracking').getAttribute('data-read-aloud-active'), 'true', 'the whole paragraph stays highlighted');
    assert.equal(await words.locator('#word-tracking').innerHTML(), beforeWords, 'word highlighting does not rewrite authored markup');
    await words.getByRole('button', {name: 'Pause', exact: true}).click();
    await words.evaluate(() => previousSpeech.onboundary({name: 'word', charIndex: 18}));
    assert.equal(await highlightedWord(words), 'example', 'pause freezes the current word');
    await settings(words).click(); await words.selectOption('[data-speed]', '0.3');
    await words.getByRole('button', {name: 'Resume', exact: true}).click();
    await words.evaluate(() => { const u = recordedSpeech.at(-1); u.onstart(); u.onboundary({name: 'word', charIndex: 8, charLength: 4}); });
    assert.equal(await highlightedWord(words), 'word', 'resumed word offsets include the retained chunk position');
    for (const theme of ['light', 'dark']) {
      await words.evaluate(t => document.documentElement.setAttribute('data-theme', t), theme);
      const colors = await words.locator('#word-tracking').evaluate(n => {
        const code = n.querySelector('code');
        const marker = getComputedStyle(code, '::highlight(sdb-spoken-word)');
        const pixel = document.createElement('canvas').getContext('2d');
        for (const element of [document.body, n, code]) {
          pixel.fillStyle = getComputedStyle(element).backgroundColor;
          pixel.fillRect(0, 0, 1, 1);
        }
        pixel.fillStyle = marker.backgroundColor;
        pixel.fillRect(0, 0, 1, 1);
        const rgb = Array.from(pixel.getImageData(0, 0, 1, 1).data).slice(0, 3);
        return [marker.color, `rgb(${rgb.join(', ')})`];
      });
      assert(contrast(...colors) >= 4.5, theme + ' spoken word contrast');
    }
    await words.getByRole('button', {name: 'Next passage', exact: true}).click();
    assert.equal(await highlightedWord(words), undefined, 'navigation clears the previous spoken word');
    await words.evaluate(() => { const u = recordedSpeech.at(-1); u.onstart(); u.onboundary({name: 'word', charIndex: 0}); });
    assert.equal(await highlightedWord(words), 'Next');
    await finish(words); assert.equal(await highlightedWord(words), undefined, 'completion clears the word');
    await words.getByRole('button', {name: 'Listen again', exact: true}).click();
    await words.evaluate(() => { const u = recordedSpeech.at(-1); u.onstart(); u.onboundary({name: 'word', charIndex: 0}); });
    await words.getByRole('button', {name: 'Stop', exact: true}).click();
    assert.equal(await highlightedWord(words), undefined, 'stop clears word and paragraph');
    assert.equal(await words.locator('[data-read-aloud-active]').count(), 0);
    const laterChunkWord = await words.evaluate(() => {
      const source = document.createElement('p');
      source.textContent = 'First sentence. '.repeat(13) + 'SecondChunk continues with a unique word and enough text to require a later speech chunk.';
      const article = document.createElement('article'); article.append(source);
      return SDBReadAloud.extractChapter(article)[1].rangeForOffsets(0, 11).toString();
    });
    assert.equal(laterChunkWord, 'SecondChunk', 'later chunk ranges retain offsets within the complete paragraph');
    const separatedInlineWords = await words.evaluate(() => {
      const article = document.createElement('article');
      article.innerHTML = '<p><strong>Read</strong> <em>this</em> <code>word</code></p>';
      const chunk = SDBReadAloud.extractChapter(article)[0];
      const range = chunk.rangeForOffsets(10, 14);
      return {text: chunk.text, word: range && range.toString()};
    });
    assert.deepEqual(separatedInlineWords, {text: 'Read this word', word: 'word'}, 'whitespace-only nodes separate adjacent formatted words');
    await words.close();

    const fallbackWords = await open({article: wordArticle, fallbackHighlight: true});
    await fallbackWords.locator('#word-tracking').click();
    await fallbackWords.getByRole('button', {name: 'Read selected paragraph', exact: true}).click();
    await fallbackWords.evaluate(() => { const u = recordedSpeech.at(-1); u.onstart(); u.onboundary({name: 'word', charIndex: 10}); });
    assert(await fallbackWords.locator('.read-aloud-word-box').count() > 0, 'older browsers paint word rectangles without changing the chapter');
    assert.equal(await fallbackWords.locator('#word-tracking').innerHTML(), beforeWords);
    assert.equal(await fallbackWords.locator('.read-aloud-word-overlay').evaluate(n => getComputedStyle(n).pointerEvents), 'none', 'the fallback leaves text and links interactive');
    await fallbackWords.setViewportSize({width: 375, height: 800});
    await fallbackWords.waitForFunction(() => {
      const source = SDBReadAloud.extractChapter(document.querySelector('.post-content')).find(c => c.element.id === 'word-tracking');
      const rect = source.rangeForOffsets(10, 17).getClientRects()[0];
      const box = document.querySelector('.read-aloud-word-box').getBoundingClientRect();
      return Math.abs(box.left - rect.left) < 1 && Math.abs(box.top - rect.top) < 1;
    });
    await fallbackWords.getByRole('button', {name: 'Stop', exact: true}).click();
    assert.equal(await fallbackWords.locator('.read-aloud-word-box').count(), 0);
    await fallbackWords.close();

    const longArticle = '<main class="post-content"><h1>Long chapter</h1><div style="height:1400px"></div><p id="target">' + 'A focused spoken chunk moves the reading position. '.repeat(35) + '</p><p>The final paragraph.</p></main>';
    const follow = await open({article: longArticle});
    await follow.setViewportSize({width: 375, height: 500});
    await follow.evaluate(() => scrollTo(0, document.getElementById('target').offsetTop - 130));
    await listen(follow).click();
    assert.match(await follow.evaluate(() => window.recordedSpeech.at(-1).text), /^A focused/, 'start from view skips the offscreen chapter title');
    const ranges = await follow.evaluate(() => window.SDBReadAloud.extractChapter(document.querySelector('.post-content')).filter(c => c.element.id === 'target').map(c => [c.text, c.range.toString()]));
    assert(ranges.length > 2 && ranges.every(([text, range]) => text === range), 'spoken chunks retain exact source ranges');
    await follow.evaluate(() => window.recordedSpeech.at(-1).onstart());
    const firstPosition = await follow.evaluate(() => scrollY);
    assert.equal(firstPosition, await follow.evaluate(() => document.getElementById('target').offsetTop - 130),
      'starting a chunk leaves its already visible first line in place');
    await follow.evaluate(() => {
      const speech = recordedSpeech.at(-1);
      speech.onboundary({name: 'word', charIndex: speech.text.lastIndexOf('reading')});
      const rect = Array.from(CSS.highlights.get('sdb-spoken-word'))[0].getBoundingClientRect();
      scrollBy(0, rect.top - 130);
    });
    await follow.getByRole('button', {name: 'Pause', exact: true}).click();
    const beforeResumePosition = await follow.evaluate(() => scrollY);
    await follow.getByRole('button', {name: 'Resume', exact: true}).click();
    await follow.evaluate(() => recordedSpeech.at(-1).onstart());
    assert.equal(await follow.evaluate(() => scrollY), beforeResumePosition,
      'resuming from a visible word does not jump back to the start of the chunk');
    await follow.evaluate(() => {
      const content = document.querySelector('.post-content');
      const nextChunk = SDBReadAloud.extractChapter(content).filter(c => c.element.id === 'target')[1];
      const firstLine = nextChunk.range.getClientRects()[0];
      scrollBy(0, firstLine.top - innerHeight + 40);
    });
    const beforeNextChunk = await follow.evaluate(() => scrollY);
    await finish(follow); await follow.evaluate(() => window.recordedSpeech.at(-1).onstart());
    assert(await follow.evaluate(() => scrollY) > beforeNextChunk, 'successive chunks follow their own first lines');
    await settings(follow).click(); await follow.locator('[data-follow]').uncheck();
    await settings(follow).click(); await follow.evaluate(() => scrollTo(0, 0));
    await finish(follow); await follow.evaluate(() => window.recordedSpeech.at(-1).onstart());
    assert.equal(await follow.evaluate(() => scrollY), 0, 'follow can be switched off while keeping the active highlight');
    await follow.close();

    const delayed = await open({voices: []});
    assert.equal(await listen(delayed).isDisabled(), true);
    assert.match(await delayed.locator('.read-aloud [role="status"]').textContent(), /English.*voice/i);
    await delayed.evaluate(voices => { window.testVoices = voices; window.voiceListeners.forEach(fn => fn()); }, VOICES);
    assert.equal(await listen(delayed).isEnabled(), true);
    await settings(delayed).click(); await delayed.selectOption('[data-voice]', 'daniel');
    await delayed.evaluate(() => window.voiceListeners.forEach(fn => fn()));
    assert.equal(await delayed.locator('[data-voice]').inputValue(), 'daniel', 'voice refresh keeps explicit choice');
    await delayed.close();
    const remote = await open({voices: [{...localVoice('Samantha', 'remote'), localService: false}]});
    assert.equal(await listen(remote).isDisabled(), true, 'no fallback to network voice'); await remote.close();
    const migrated = await open({legacy: 'victoria'});
    await settings(migrated).click(); assert.equal(await migrated.locator('[data-voice]').inputValue(), 'samantha'); await migrated.close();
    const denied = await open({denied: true});
    await settings(denied).click(); await denied.selectOption('[data-speed]', '0.3'); await listen(denied).click();
    assert.equal(await denied.evaluate(() => window.recordedSpeech.at(-1).rate), .3); await denied.close();
    const unsupported = await open({unsupported: true});
    assert.equal(await listen(unsupported).isDisabled(), true);
    assert.match(await unsupported.locator('.read-aloud [role="status"]').textContent(), /unavailable/); await unsupported.close();

    const layout = await open(); await settings(layout).click();
    for (const theme of ['light', 'dark']) {
      await layout.evaluate(theme => document.documentElement.setAttribute('data-theme', theme), theme);
      for (const [width, height] of [[320, 568], [375, 800], [667, 320], [1280, 900]]) {
        await layout.setViewportSize({width, height});
        const box = await layout.locator('.read-aloud').boundingBox();
        assert(box.x >= 0 && box.x + box.width <= width + 1 && box.y >= 0 && box.y + box.height <= height + 1, 'dock fits ' + theme + ' ' + width + 'x' + height);
        assert(await layout.evaluate(() => document.documentElement.scrollWidth <= innerWidth), 'no horizontal overflow');
        const colors = await layout.locator('.read-aloud').evaluate(el => [el.querySelector('[data-read]'), el.querySelector('[data-speed]'), el.querySelector('[data-preview]'), el.querySelector('[role="status"]')].map(n => [getComputedStyle(n).color, getComputedStyle(n).backgroundColor]));
        // Status inherits the opaque dock surface; controls own their surfaces.
        const surface = await layout.locator('.read-aloud').evaluate(n => getComputedStyle(n).backgroundColor);
        colors.forEach(([fg, bg]) => assert(contrast(fg, bg === 'rgba(0, 0, 0, 0)' ? surface : bg) >= 4.5, theme + ' player contrast'));
        if (process.env.STUDY_SCREENSHOT) await layout.screenshot({path: process.env.STUDY_SCREENSHOT + '-' + theme + '-' + width + '.png'});
      }
    }
    await layout.close();
    if (process.env.STUDY_TEST_URL) {
      const actual = await open({rendered: true});
      assert.equal(await actual.getByRole('combobox', {name: 'Reading width'}).count(), 0, 'the current wide reader has no width option');
      const wide = await actual.locator('.post-content').evaluate(article => ({article: article.clientWidth, prose: article.querySelector(':scope > p').getBoundingClientRect().width}));
      assert(Math.abs(wide.article - wide.prose) <= 1, 'the current reader keeps prose wide');
      for (const theme of ['light', 'dark']) {
        await actual.evaluate(theme => document.documentElement.setAttribute('data-theme', theme), theme);
        for (const [width, height] of [[320, 568], [375, 800], [667, 320], [1280, 900]]) {
          await actual.setViewportSize({width, height});
          await actual.evaluate(() => scrollTo(0, 0));
          await listen(actual).click();
          const targets = await actual.locator('.read-aloud-transport button:visible').evaluateAll(nodes => nodes.map(n => ({label: n.getAttribute('aria-label'), rect: n.getBoundingClientRect().toJSON()})));
          const dock = await actual.locator('.read-aloud').boundingBox();
          for (const {label, rect} of targets) assert(rect.width >= 43.5 && rect.height >= 44 && rect.x >= dock.x && rect.right <= dock.x + dock.width, label + ' remains reachable at ' + width + ': ' + JSON.stringify(rect));
          await settings(actual).click();
          assert(await actual.getByRole('combobox', {name: 'Reading voice'}).isVisible());
          assert(await actual.evaluate(() => document.documentElement.scrollWidth <= innerWidth), 'rendered chapter fits ' + width);
          await actual.getByRole('button', {name: 'Stop', exact: true}).click();
          await settings(actual).click();
        }
      }
      await actual.close();
    }
    console.log('PASS: local voices, settings, all speeds, previews, continuous/manual playback, navigation, spoken word and paragraph highlights, cross-node and later-chunk ranges, pause/resume, fallback rectangles, persistence, delayed voices, storage denial, themes and responsive dock.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
