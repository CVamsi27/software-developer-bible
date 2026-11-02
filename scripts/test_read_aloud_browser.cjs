let chromium;
try { ({chromium} = require('@playwright/test')); }
catch (_) { ({chromium} = require('playwright')); }
const assert = require('node:assert/strict');
const path = require('node:path');
const CHAPTER = '/10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.05-lexical-environment.html';
const CHAPTER_URL = 'https://study.buildora.work' + CHAPTER;
const TOKENS = '<style>:root{--theme-bg:#fff;--theme-text:#1f2937;--theme-text-muted:#4b5563;--theme-heading:#111827;--theme-border:#e5e7eb;--theme-link:#2563eb;--card-bg:#fff;--nav-pill-bg:#f3f4f6}html[data-theme="dark"]{--theme-bg:#111820;--theme-text:#d5deea;--theme-text-muted:#a4b3c5;--theme-heading:#f8fafc;--theme-border:#2c3b4d;--theme-link:#60a5fa;--card-bg:#18222d;--nav-pill-bg:#1e2b39}html[data-theme="light"]{color-scheme:light}body{margin:0;font-family:sans-serif}</style>';
const READER_FIXTURE = TOKENS + '<main class="post-content"><h1>Lexical Environment</h1><p>A lexical environment is used to find the variable for a name.</p><h2 id="one">Bindings</h2><p>Bindings connect a name to a value.</p><h2 id="two">Scope lookup</h2><p>Lookup walks outward until it finds a match.</p><h2 id="three">Nested functions</h2><p>Nested functions keep their outer references alive.</p><h2 id="four">A final example</h2><p>The final example shows the whole lookup.</p></main>';
function luminance(rgb) {
  const channels = rgb.match(/[\d.]+/g).slice(0, 3).map(Number).map(value => {
    value /= 255;
    return value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
  });
  return channels[0] * 0.2126 + channels[1] * 0.7152 + channels[2] * 0.0722;
}
function contrast(a, b) {
  const x = luminance(a), y = luminance(b);
  return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05);
}
async function installReaderAssets(page) {
  await page.evaluate(() => { window.recordedSpeech = []; window.followedBlocks = []; });
  await page.addStyleTag({path: path.resolve('assets/read-aloud.css')});
  await page.addStyleTag({path: path.resolve('assets/reading-ui.css')});
  await page.addStyleTag({path: path.resolve('assets/reference-reader.css')});
  await page.addScriptTag({path: path.resolve('assets/study-state.js')});
  await page.evaluate(paths => { window.StudyPublishedPaths = paths; }, [CHAPTER]);
  await page.addScriptTag({path: path.resolve('assets/reading-ui.js')});
  await page.addScriptTag({path: path.resolve('assets/read-aloud.js')});
  await page.evaluate(() => document.dispatchEvent(new Event('DOMContentLoaded')));
}
(async () => {
  const browser = await chromium.launch({headless: true, executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH});
  try {
    const context = await browser.newContext({viewport: {width: 1280, height: 900}});
    await context.addInitScript(() => {
      window.recordedSpeech = [];
      window.followedBlocks = [];
      Object.defineProperty(window, 'speechSynthesis', {value: {
        cancel() { window.speechCancels = (window.speechCancels || 0) + 1; },
        pause() { window.speechPauses = (window.speechPauses || 0) + 1; },
        resume() { window.speechResumes = (window.speechResumes || 0) + 1; },
        speak(utterance) { window.recordedSpeech.push(utterance); },
        getVoices() { return [
          {name: 'Voice A', voiceURI: 'voice-a', lang: 'en-US'},
          {name: 'Voice B', voiceURI: 'voice-b', lang: 'en-GB'},
          {name: 'Voice C', voiceURI: 'voice-c', lang: 'en-AU'},
          {name: 'Voice D', voiceURI: 'voice-d', lang: 'en-CA'},
          {name: 'Voice E', voiceURI: 'voice-e', lang: 'en-IN'},
          {name: 'Voice F', voiceURI: 'voice-f', lang: 'en-NZ'},
          {name: 'Voix française', voiceURI: 'voice-fr', lang: 'fr-FR'}
        ]; },
        addEventListener() {}
      }});
      window.SpeechSynthesisUtterance = function (text) { this.text = text; };
    });
    await context.route('https://study.buildora.work/**', route => route.fulfill({status: 200, contentType: 'text/html', body: '<!doctype html><html><body></body></html>'}));
    const page = await context.newPage();
    await page.goto(CHAPTER_URL);
    await page.setContent(READER_FIXTURE);
    await page.evaluate(() => {
      const arrow = document.createElement('button');
      arrow.className = 'back-to-top visible';
      arrow.setAttribute('aria-label', 'Back to top');
      document.body.append(arrow);
    });
    await installReaderAssets(page);

    // The player is a fixed dock owned by the page, not a title-row control.
    assert.equal(await page.locator('.chapter-title-row > .read-aloud').count(), 0);
    assert.equal(await page.locator('body > .read-aloud').count(), 1);
    assert.equal(await page.locator('.read-aloud').evaluate(bar => getComputedStyle(bar).position), 'fixed');
    assert.equal(await page.locator('.read-aloud').getAttribute('data-state'), 'idle');
    assert.equal(await page.locator('[data-read]').isVisible(), true);
    assert.equal(await page.locator('[data-voice]').isVisible(), false, 'voice stays out of the way until listening starts');
    assert.equal(await page.locator('[data-speed]').isVisible(), false, 'speed stays out of the way until listening starts');
    assert.equal(await page.locator('.chapter-title-row > h1').count(), 1);
    assert.equal(await page.locator('.chapter-title-row .reading-width').count(), 0);
    assert.equal(await page.locator('[aria-label="Reading speed"] option[value="0.5"]').textContent(), '0.5×');
    assert.deepEqual(await page.locator('[data-voice] option').allTextContents(), [
      'Voice A (en-US)', 'Voice B (en-GB)', 'Voice C (en-AU)', 'Voice D (en-CA)', 'Voice E (en-IN)'
    ]);
    const alignedActions = await page.evaluate(() => {
      const listen = document.querySelector('[data-read]').getBoundingClientRect();
      const arrow = document.querySelector('.back-to-top');
      const top = arrow.getBoundingClientRect();
      return {parent: arrow.parentElement.className, display: getComputedStyle(arrow).display,
        centerDifference: Math.abs((listen.top + listen.bottom) / 2 - (top.top + top.bottom) / 2)};
    });
    assert.equal(alignedActions.parent, 'read-aloud-controls');
    assert.equal(alignedActions.display, 'flex');
    assert.ok(alignedActions.centerDifference <= 1, 'back-to-top aligns with Listen in the idle row');
    assert.equal(await page.locator('[data-pause]').isVisible(), false);
    assert.equal(await page.locator('[data-next]').isVisible(), false);
    assert.equal(await page.locator('[data-stop]').isVisible(), false);
    assert.equal(await page.evaluate(() => window.SDBReadAloud.extractChapter(document.querySelector('.post-content')).length > 0), true);

    // One activation reads one paragraph, then waits for Next instead of
    // automatically rushing through the chapter.
    await page.getByRole('button', {name: 'Read aloud', exact: true}).click();
    assert.equal(await page.evaluate(() => window.recordedSpeech.at(-1).text), 'Lexical Environment');
    assert.equal(await page.locator('[data-read]').isVisible(), false);
    assert.equal(await page.locator('[data-voice]').isVisible(), true);
    assert.equal(await page.locator('[data-speed]').isVisible(), true);
    assert.equal(await page.locator('[data-pause]').isVisible(), true);
    assert.equal(await page.locator('[data-pause]').evaluate(el => el === document.activeElement), true);
    await page.evaluate(() => window.recordedSpeech.at(-1).onstart());
    assert.equal(await page.locator('h1').getAttribute('data-read-aloud-active'), 'true');
    await page.evaluate(() => window.recordedSpeech.at(-1).onend());
    assert.equal(await page.locator('.read-aloud').getAttribute('data-state'), 'ready');
    assert.equal(await page.locator('[data-next]').isVisible(), true);
    assert.equal(await page.locator('[data-pause]').isVisible(), false);
    assert.equal(await page.locator('[data-stop]').isVisible(), true);
    assert.match(await page.locator('.read-aloud-progress').textContent(), /^1 \/ \d+$/);
    assert.equal(await page.evaluate(() => window.recordedSpeech.length), 1, 'the player must stop after the first paragraph');

    await page.getByRole('button', {name: 'Read the next paragraph', exact: true}).click();
    assert.equal(await page.evaluate(() => window.recordedSpeech.at(-1).text), 'A lexical environment is used to find the variable for a name.');
    assert.equal(await page.locator('[data-pause]').isVisible(), true);
    await page.evaluate(() => window.recordedSpeech.at(-1).onstart());
    assert.equal(await page.locator('p[data-read-aloud-active="true"]').textContent(), 'A lexical environment is used to find the variable for a name.');
    await page.getByRole('button', {name: 'Pause', exact: true}).click();
    assert.equal(await page.locator('.read-aloud').getAttribute('data-state'), 'paused');
    await page.getByRole('button', {name: 'Resume', exact: true}).click();
    assert.equal(await page.locator('.read-aloud').getAttribute('data-state'), 'reading');
    await page.selectOption('[data-voice]', 'voice-b');
    assert.equal(await page.evaluate(() => localStorage.getItem('sdb-read-aloud-voice')), 'voice-b');
    await page.getByRole('button', {name: 'Stop', exact: true}).click();
    assert.equal(await page.locator('.read-aloud').getAttribute('data-state'), 'idle');
    assert.equal(await page.locator('[data-read]').isVisible(), true);
    assert.equal(await page.locator('[data-voice]').isVisible(), false, 'stopping returns the player to its compact idle state');
    assert.equal(await page.locator('.post-content [data-read-aloud-active]').count(), 0);

    // Voice selection persists and is applied to the next paragraph.
    await page.getByRole('button', {name: 'Read aloud', exact: true}).click();
    assert.equal(await page.evaluate(() => window.recordedSpeech.at(-1).voice.voiceURI), 'voice-b');
    assert.equal(await page.evaluate(() => window.recordedSpeech.at(-1).lang), 'en-GB');
    await page.getByRole('button', {name: 'Stop', exact: true}).click();

    // The fixed dock stays in view, and Listen starts at the paragraph in view.
    await page.setContent(TOKENS + '<main class="post-content"><h1>Start from here</h1><div style="height:1200px"></div><p id="target">Unique target paragraph starts here.</p><p id="after">The paragraph after the target.</p></main>');
    await installReaderAssets(page);
    await page.evaluate(() => window.scrollTo(0, document.getElementById('target').offsetTop - 180));
    const dock = await page.locator('.read-aloud').boundingBox();
    assert.ok(dock && dock.y >= 0 && dock.y + dock.height <= 900, 'floating player stays in the viewport');
    await page.getByRole('button', {name: 'Read aloud', exact: true}).click();
    assert.equal(await page.evaluate(() => window.recordedSpeech.at(-1).text), 'Unique target paragraph starts here.');
    await page.evaluate(() => window.recordedSpeech.at(-1).onstart());
    const highlight = await page.locator('p[data-read-aloud-active="true"]').evaluate(el => ({
      padding: getComputedStyle(el).paddingInlineStart,
      margin: getComputedStyle(el).marginInlineStart,
      shadow: getComputedStyle(el).boxShadow
    }));
    assert.deepEqual(highlight, {padding: '14px', margin: '-14px', shadow: 'none'}, 'the highlight leaves a gutter instead of covering the first letter');
    await page.evaluate(() => window.recordedSpeech.at(-1).onend());
    await page.selectOption('[data-speed]', '0.5');
    await page.getByRole('button', {name: 'Read the next paragraph', exact: true}).click();
    assert.equal(await page.evaluate(() => window.recordedSpeech.at(-1).rate), 0.5);
    await page.evaluate(() => window.recordedSpeech.at(-1).onend());
    assert.equal(await page.locator('.read-aloud').getAttribute('data-state'), 'complete');
    assert.equal(await page.getByRole('button', {name: 'Listen again', exact: true}).isVisible(), true);
    await page.getByRole('button', {name: 'Listen again', exact: true}).click();
    assert.equal(await page.evaluate(() => window.recordedSpeech.at(-1).text), 'Start from here', 'Listen again restarts at the chapter opening');
    await page.getByRole('button', {name: 'Stop', exact: true}).click();

    // Long source blocks still follow their spoken text ranges, one chunk at
    // a time, without jumping back to the paragraph start.
    await page.setContent(TOKENS + '<main class="post-content"><h1>Long paragraph follow</h1><div style="height:1200px"></div><p id="long-follow">' + ('A focused spoken chunk moves the reading position. ').repeat(30) + '</p><p id="after-long">The paragraph after the long one.</p></main>');
    await installReaderAssets(page);
    const longChunks = await page.evaluate(() => window.SDBReadAloud.extractChapter(document.querySelector('.post-content')).filter(chunk => chunk.element.id === 'long-follow').map(chunk => ({text: chunk.text, rangeText: chunk.range && chunk.range.toString()})));
    assert.ok(longChunks.length > 2);
    assert.deepEqual(longChunks.map(chunk => chunk.rangeText), longChunks.map(chunk => chunk.text));
    await page.setViewportSize({width: 375, height: 320});
    await page.emulateMedia({reducedMotion: 'reduce'});
    await page.evaluate(() => {
      document.querySelector('#long-follow').scrollIntoView = function () { window.blockStartScrolls = (window.blockStartScrolls || 0) + 1; };
      window.scrollTo(0, document.getElementById('long-follow').offsetTop - 80);
    });
    await page.getByRole('button', {name: 'Read aloud', exact: true}).click();
    const followProgress = await page.evaluate(() => {
      window.recordedSpeech[0].onstart();
      window.recordedSpeech[0].onend();
      const firstChunk = window.recordedSpeech.at(-1);
      firstChunk.onstart();
      const firstChunkScrollY = window.scrollY;
      firstChunk.onend();
      const secondChunk = window.recordedSpeech.at(-1);
      secondChunk.onstart();
      return {firstChunkScrollY, secondChunkScrollY: window.scrollY, blockStartScrolls: window.blockStartScrolls || 0};
    });
    assert.ok(followProgress.secondChunkScrollY > followProgress.firstChunkScrollY, 'later text chunks move the reading position down the long paragraph: ' + JSON.stringify(followProgress));
    assert.equal(followProgress.blockStartScrolls, 0, 'follow uses each spoken text span instead of jumping to the paragraph start');
    await page.getByRole('button', {name: 'Stop', exact: true}).click();

    // Mobile keeps the dock inside the viewport with no horizontal overflow.
    await page.setViewportSize({width: 375, height: 800});
    await page.setContent(READER_FIXTURE);
    await installReaderAssets(page);
    const mobileBox = await page.locator('.read-aloud').boundingBox();
    assert.ok(mobileBox && mobileBox.x >= 0 && mobileBox.x + mobileBox.width <= 375 && mobileBox.y + mobileBox.height <= 800);
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
    assert.equal(await page.evaluate(() => getComputedStyle(document.body).paddingBottom !== '0px'), true, 'the dock reserves space at the page bottom');

    // Contrast survives both explicit themes for every player action.
    for (const theme of ['dark', 'light']) {
      await page.evaluate(theme => document.documentElement.setAttribute('data-theme', theme), theme);
      const colors = await page.locator('.read-aloud').evaluate(el => {
        const sample = node => [getComputedStyle(node).color, getComputedStyle(node).backgroundColor];
        return [sample(el.querySelector('[data-read]')), sample(el.querySelector('[data-pause]')), sample(el.querySelector('[data-stop]')), sample(el.querySelector('select'))];
      });
      colors.forEach(([fg, bg], index) => assert(contrast(fg, bg) >= 4.5, `${theme} control ${index} contrast is below 4.5:1 (${fg} on ${bg})`));
    }

    // Leaving the page cancels the current narration.
    await page.setContent(READER_FIXTURE);
    await installReaderAssets(page);
    await page.getByRole('button', {name: 'Read aloud', exact: true}).click();
    const before = await page.evaluate(() => window.speechCancels || 0);
    await page.evaluate(() => window.dispatchEvent(new Event('pagehide')));
    assert.equal(await page.evaluate(() => window.speechCancels || 0), before + 1);

    // A paragraph can be selected explicitly, and a later selection can
    // replace the current target without interrupting speech until Listen.
    await page.setContent(READER_FIXTURE);
    await installReaderAssets(page);
    const selectedParagraph = page.locator('.post-content p').nth(1);
    await selectedParagraph.click();
    assert.equal(await selectedParagraph.getAttribute('data-read-aloud-selected'), 'true');
    assert.match(await page.getByRole('status').textContent(), /Paragraph selected/);
    await page.getByRole('button', {name: 'Read selected paragraph'}).click();
    assert.equal(await page.evaluate(() => window.recordedSpeech.at(-1).text), 'Bindings connect a name to a value.');
    assert.equal(await selectedParagraph.getAttribute('data-read-aloud-selected'), null, 'the selected outline gives way to the active spoken block');
    const currentCount = await page.evaluate(() => window.recordedSpeech.length);
    const nextSelection = page.locator('.post-content p').nth(2);
    await nextSelection.click();
    assert.equal(await nextSelection.getAttribute('data-read-aloud-selected'), 'true');
    assert.equal(await page.evaluate(() => window.recordedSpeech.length), currentCount, 'selecting another paragraph does not stop current speech');
    await page.getByRole('button', {name: 'Read selected paragraph'}).click();
    assert.equal(await page.evaluate(() => window.recordedSpeech.at(-1).text), 'Lookup walks outward until it finds a match.');

    const unsupported = await browser.newPage();
    await unsupported.addInitScript(() => { Object.defineProperty(window, 'speechSynthesis', {value: undefined}); });
    await unsupported.route('https://study.buildora.work/**', route => route.fulfill({status: 200, contentType: 'text/html', body: '<!doctype html><html><body></body></html>'}));
    await unsupported.goto(CHAPTER_URL);
    await unsupported.setContent(READER_FIXTURE);
    await installReaderAssets(unsupported);
    assert.equal(await unsupported.getByRole('button', {name: 'Read aloud', exact: true}).isDisabled(), true);
    assert.equal(await unsupported.getByRole('combobox', {name: 'Reading voice'}).isDisabled(), true);
    assert.match(await unsupported.getByRole('status').textContent(), /unavailable/);
    await unsupported.close();

    console.log('PASS: floating dock, paragraph pause/Next, start from view, voice selection, speed, highlight gutter, follow, themes, mobile width, departure cancellation, unsupported browser.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
