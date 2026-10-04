const { chromium } = require('@playwright/test');
const assert = require('node:assert/strict');
const path = require('node:path');
(async () => {
  const browser = await chromium.launch({headless: true});
  try {
    const page = await browser.newPage();
    await page.addInitScript(() => {
      window.recordedSpeech = [];
      Object.defineProperty(window, 'speechSynthesis', {value: {
        cancel() { window.speechCancels = (window.speechCancels || 0) + 1; }, pause() {}, resume() {},
        speak(u) { window.recordedSpeech.push(u); }
      }});
      window.SpeechSynthesisUtterance = function(text) { this.text = text; };
    });
    await page.goto(process.env.STUDY_TEST_URL || 'http://127.0.0.1:4337/10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.05-lexical-environment.html');
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
    await page.setContent('<main class="post-content"><h1>Title</h1><p><a><img alt="Badge"></a></p><nav>Skip navigation</nav><p>Use <code>const</code> here.</p><pre>Do not read code</pre><ul><li>First<ul><li>Nested</li></ul></li><li>Last</li></ul><p hidden>Secret</p><p><button>Copy</button>Explanation<a class="heading-anchor">#</a></p></main>');
    await page.addScriptTag({path: path.resolve('assets/read-aloud.js')});
    const text = await page.evaluate(() => window.SDBReadAloud.extractChapter(document.querySelector('.post-content')));
    assert.deepEqual(text, ['Title', 'Use const here.', 'First', 'Nested', 'Last', 'Explanation']);
    await page.setViewportSize({width: 375, height: 800});
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
    const unsupported = await browser.newPage();
    await unsupported.setContent('<main class="post-content"><h1>Title</h1></main>');
    await unsupported.evaluate(() => { Object.defineProperty(window, 'speechSynthesis', {value: undefined}); });
    await unsupported.addScriptTag({path: path.resolve('assets/read-aloud.js')});
    assert.equal(await unsupported.getByRole('button', {name: 'Read aloud', exact: true}).isDisabled(), true);
    assert.match(await unsupported.getByRole('status').textContent(), /unavailable/);
    console.log('PASS: rendered chapter controls, pause/resume/stop, extraction order, mobile width, speed, departure cancellation, unsupported browser.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
