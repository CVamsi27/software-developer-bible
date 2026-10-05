let chromium;
try { ({chromium} = require('@playwright/test')); }
catch (_) { ({chromium} = require('playwright')); }
const assert = require('node:assert/strict');
const path = require('node:path');
async function installReaderAssets(page) {
  await page.addStyleTag({path: path.resolve('assets/read-aloud.css')});
  await page.addStyleTag({path: path.resolve('assets/reading-ui.css')});
  await page.addScriptTag({path: path.resolve('assets/reading-ui.js')});
  await page.addScriptTag({path: path.resolve('assets/read-aloud.js')});
  await page.evaluate(() => document.dispatchEvent(new Event('DOMContentLoaded')));
}
(async () => {
  const browser = await chromium.launch({headless: true, executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH});
  try {
    const page = await browser.newPage();
    await page.addInitScript(() => {
      window.recordedSpeech = [];
      window.followedBlocks = [];
      Object.defineProperty(window, 'speechSynthesis', {value: {
        cancel() { window.speechCancels = (window.speechCancels || 0) + 1; }, pause() {}, resume() {},
        speak(u) { window.recordedSpeech.push(u); }
      }});
      window.SpeechSynthesisUtterance = function(text) { this.text = text; };
    });
    if (process.env.STUDY_TEST_URL) {
      await page.goto(process.env.STUDY_TEST_URL);
    } else {
      await page.setContent('<script>window.recordedSpeech=[];window.followedBlocks=[];Object.defineProperty(window,"speechSynthesis",{configurable:true,value:{cancel(){window.speechCancels=(window.speechCancels||0)+1},pause(){},resume(){},speak(u){window.recordedSpeech.push(u)}}});Object.defineProperty(window,"SpeechSynthesisUtterance",{configurable:true,value:function(text){this.text=text}})</script><style>:root{--theme-bg:#fff;--theme-text:#1f2937;--theme-text-muted:#4b5563;--theme-heading:#111827;--theme-border:#e5e7eb;--theme-link:#2563eb;--card-bg:#fff;--nav-pill-bg:#f3f4f6}html[data-theme="dark"]{--theme-bg:#111820;--theme-text:#d5deea;--theme-text-muted:#a4b3c5;--theme-heading:#f8fafc;--theme-border:#2c3b4d;--theme-link:#60a5fa;--card-bg:#18222d;--nav-pill-bg:#1e2b39}html[data-theme="light"]{color-scheme:light}</style><main class="post-content"><h1>Lexical Environment</h1><p>A lexical environment is used to find the variable for a name.</p><h2 id="one">Bindings</h2><h2 id="two">Scope lookup</h2><h2 id="three">Nested functions</h2><h2 id="four">A final example</h2></main>');
      await installReaderAssets(page);
    }
    assert.equal(await page.locator('.chapter-title-row > h1').count(), 1);
    assert.equal(await page.locator('.chapter-title-row > .read-aloud').count(), 1);
    assert.equal(await page.locator('.chapter-title-row').evaluate(row => row.nextElementSibling.classList.contains('chapter-outline')), true);
    assert.equal(await page.locator('[aria-label="Reading speed"] option[value="0.5"]').textContent(), '0.5×');
    assert.equal(await page.evaluate(() => {
      const chunks = window.SDBReadAloud.extractChapter(document.querySelector('.post-content'));
      return chunks[0].element.tagName === 'H1' && chunks[1].element.tagName === 'P' && chunks[0].element !== chunks[1].element;
    }), true);
    assert.equal(await page.locator('[data-pause]').isVisible(), false);
    assert.equal(await page.locator('[data-stop]').isVisible(), false);
    await page.getByRole('button', {name: 'Read aloud', exact: true}).click({timeout: 5000});
    assert.equal(await page.locator('[data-read]').isVisible(), false);
    assert.equal(await page.locator('[data-pause]').evaluate(el => el === document.activeElement), true);
    assert.equal(await page.getByRole('button', {name: 'Pause', exact: true}).isEnabled(), true);
    const first = await page.evaluate(() => window.recordedSpeech[0].text);
    assert.equal(first, 'Lexical Environment');
    await page.getByRole('button', {name: 'Pause', exact: true}).click();
    await page.getByRole('button', {name: 'Resume', exact: true}).click();
    await page.getByRole('button', {name: 'Stop', exact: true}).click();
    assert.equal(await page.getByRole('button', {name: 'Read aloud', exact: true}).isEnabled(), true);
    assert.equal(await page.locator('[data-read]').evaluate(el => el === document.activeElement), true);
    await page.setViewportSize({width: 375, height: 800});
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
    await page.getByRole('combobox', {name: 'Reading speed'}).selectOption('0.5');
    await page.getByRole('button', {name: 'Read aloud', exact: true}).click();
    assert.equal(await page.evaluate(() => window.recordedSpeech.at(-1).rate), 0.5);
    await page.getByRole('button', {name: 'Stop', exact: true}).click();
    await page.getByRole('combobox', {name: 'Reading speed'}).selectOption('1.5');
    await page.getByRole('button', {name: 'Read aloud', exact: true}).click();
    assert.equal(await page.evaluate(() => window.recordedSpeech.at(-1).rate), 1.5);
    const before = await page.evaluate(() => window.speechCancels);
    await page.evaluate(() => window.dispatchEvent(new Event('pagehide')));
    assert.equal(await page.evaluate(() => window.speechCancels), before + 1);
    await page.setViewportSize({width: 1280, height: 900});
    if (process.env.STUDY_SCREENSHOT) {
      await page.screenshot({path: process.env.STUDY_SCREENSHOT});
      await page.setViewportSize({width: 375, height: 800});
      await page.screenshot({path: process.env.STUDY_SCREENSHOT.replace('.png', '-mobile.png')});
      await page.evaluate(() => document.documentElement.setAttribute('data-theme', 'dark'));
      await page.getByRole('button', {name: 'Read aloud', exact: true}).click();
      assert.equal(await page.locator('[data-stop]').isVisible(), true);
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
      await page.screenshot({path: process.env.STUDY_SCREENSHOT.replace('.png', '-dark.png')});
      await page.getByRole('button', {name: 'Stop', exact: true}).click();
    }
    await page.evaluate(() => document.documentElement.setAttribute('data-theme', 'dark'));
    assert.deepEqual(await page.locator('.read-aloud').evaluate(el => ({
      controlBackground: getComputedStyle(el.querySelector('select')).backgroundColor,
      controlColor: getComputedStyle(el.querySelector('select')).color,
      primaryBackground: getComputedStyle(el.querySelector('[data-read]')).backgroundColor,
      primaryColor: getComputedStyle(el.querySelector('[data-read]')).color,
      controlScheme: getComputedStyle(el.querySelector('select')).colorScheme
    })), {controlBackground: 'rgb(24, 34, 45)', controlColor: 'rgb(213, 222, 234)', primaryBackground: 'rgb(96, 165, 250)', primaryColor: 'rgb(17, 24, 32)', controlScheme: 'dark'});
    await page.evaluate(() => document.documentElement.setAttribute('data-theme', 'light'));
    assert.deepEqual(await page.locator('.read-aloud').evaluate(el => ({
      controlBackground: getComputedStyle(el.querySelector('select')).backgroundColor,
      controlColor: getComputedStyle(el.querySelector('select')).color,
      primaryBackground: getComputedStyle(el.querySelector('[data-read]')).backgroundColor,
      primaryColor: getComputedStyle(el.querySelector('[data-read]')).color,
      controlScheme: getComputedStyle(el.querySelector('select')).colorScheme
    })), {controlBackground: 'rgb(255, 255, 255)', controlColor: 'rgb(31, 41, 55)', primaryBackground: 'rgb(37, 99, 235)', primaryColor: 'rgb(255, 255, 255)', controlScheme: 'light'});
    await page.setContent('<main class="post-content"><h1>Title</h1><p><a><img alt="Badge"></a></p><nav>Skip navigation</nav><p>Use <code>const</code> here.</p><pre>Do not read code</pre><ul><li>First<ul><li>Nested</li></ul></li><li>Last</li></ul><p hidden>Secret</p><p><button>Copy</button>Explanation<a class="heading-anchor">#</a></p><p id="long">' + 'x'.repeat(500) + '</p></main>');
    await installReaderAssets(page);
    const text = await page.evaluate(() => window.SDBReadAloud.extractChapter(document.querySelector('.post-content')));
    assert.deepEqual(text.map(chunk => chunk.text), ['Title', 'Use const here.', 'First', 'Nested', 'Last', 'Explanation', 'x'.repeat(240), 'x'.repeat(240), 'x'.repeat(20)]);
    assert.equal(await page.evaluate(() => window.SDBReadAloud.extractChapter(document.querySelector('.post-content')).filter(chunk => chunk.element.id === 'long').length), 3);
    assert.equal(await page.locator('.chapter-title-row > h1').count(), 1);
    await page.setContent('<main class="post-content"><h1>Follow test</h1><div style="height:1200px"></div><p id="source">Speak this paragraph.</p></main>');
    await installReaderAssets(page);
    await page.locator('#source').evaluate(el => { el.scrollIntoView = options => { window.followedBlocks.push({id: el.id, options}); }; });
    await page.evaluate(() => {
      window.__nativeScrollBy = window.scrollBy.bind(window);
      window.scrollBy = options => window.followedBlocks.push({id: 'source', options});
    });
    await page.emulateMedia({reducedMotion: 'reduce'});
    await page.getByRole('button', {name: 'Read aloud', exact: true}).click();
    await page.evaluate(() => { window.recordedSpeech.at(-1).onend(); window.recordedSpeech.at(-1).onstart(); });
    assert.equal(await page.locator('#source').getAttribute('data-read-aloud-active'), 'true');
    const followedSource = await page.evaluate(() => window.followedBlocks.at(-1));
    assert.equal(followedSource.id, 'source');
    assert.equal(followedSource.options.behavior, 'auto');
    assert.ok(followedSource.options.top > 0);
    await page.getByRole('button', {name: 'Stop', exact: true}).click();
    assert.equal(await page.locator('#source').getAttribute('data-read-aloud-active'), null);
    await page.setViewportSize({width: 375, height: 800});
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
    await page.setContent('<main class="post-content"><h1>Long paragraph follow</h1><div style="height:1200px"></div><p id="long-follow">' + ('A focused spoken chunk moves the reading position. ').repeat(30) + '</p></main>');
    await page.evaluate(() => { if (window.__nativeScrollBy) window.scrollBy = window.__nativeScrollBy; });
    await page.evaluate(() => {
      window.recordedSpeech = [];
      Object.defineProperty(window, 'speechSynthesis', {configurable: true, value: {cancel() {}, pause() {}, resume() {}, speak(utterance) { window.recordedSpeech.push(utterance); }}});
      Object.defineProperty(window, 'SpeechSynthesisUtterance', {configurable: true, value: function (text) { this.text = text; }});
    });
    await installReaderAssets(page);
    const longChunks = await page.evaluate(() => window.SDBReadAloud.extractChapter(document.querySelector('.post-content')).filter(chunk => chunk.element.id === 'long-follow').map(chunk => ({text: chunk.text, rangeText: chunk.range && chunk.range.toString()})));
    assert.ok(longChunks.length > 2);
    assert.deepEqual(longChunks.map(chunk => chunk.rangeText), longChunks.map(chunk => chunk.text));
    await page.setViewportSize({width: 375, height: 320});
    await page.emulateMedia({reducedMotion: 'reduce'});
    await page.evaluate(() => document.querySelector('#long-follow').scrollIntoView = function () { window.blockStartScrolls = (window.blockStartScrolls || 0) + 1; });
    await page.getByRole('button', {name: 'Read aloud', exact: true}).click();
    const followProgress = await page.evaluate(() => {
      window.recordedSpeech[0].onend();
      const firstChunk = window.recordedSpeech.at(-1);
      firstChunk.onstart(); const firstChunkScrollY = window.scrollY;
      firstChunk.onend();
      const secondChunk = window.recordedSpeech.at(-1);
      secondChunk.onstart();
      return {firstChunkScrollY, secondChunkScrollY: window.scrollY, blockStartScrolls: window.blockStartScrolls || 0};
    });
    assert.ok(followProgress.secondChunkScrollY > followProgress.firstChunkScrollY, 'later text chunks should move the reading position down the long paragraph: ' + JSON.stringify(followProgress));
    assert.equal(followProgress.blockStartScrolls, 0, 'follow should use each spoken text span instead of repeatedly jumping to the paragraph start');
    await page.getByRole('button', {name: 'Stop', exact: true}).click();
    const unsupported = await browser.newPage();
    await unsupported.setContent('<main class="post-content"><h1>Title</h1></main>');
    await unsupported.evaluate(() => { Object.defineProperty(window, 'speechSynthesis', {value: undefined}); });
    await installReaderAssets(unsupported);
    assert.equal(await unsupported.getByRole('button', {name: 'Read aloud', exact: true}).isDisabled(), true);
    assert.match(await unsupported.getByRole('status').textContent(), /unavailable/);
    console.log('PASS: rendered chapter controls, pause/resume/stop, extraction order, mobile width, speed, departure cancellation, unsupported browser.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
