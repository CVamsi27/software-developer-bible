const {chromium} = require('@playwright/test');
const assert = require('node:assert/strict');
function luminance(rgb) {
  const c = rgb.match(/[\d.]+/g).slice(0, 3).map(Number).map(v => {
    v /= 255; return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
  });
  return c[0] * .2126 + c[1] * .7152 + c[2] * .0722;
}
function contrast(a, b) {
  const x = luminance(a), y = luminance(b);
  return (Math.max(x, y) + .05) / (Math.min(x, y) + .05);
}
(async () => {
  const browser = await chromium.launch({headless: true});
  try {
    const page = await browser.newPage({colorScheme: 'dark', reducedMotion: 'reduce'});
    await page.goto('http://127.0.0.1:4337/10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.05-lexical-environment.html');
    const fence = page.locator('div.highlighter-rouge').first();
    assert.equal(await fence.locator('div.highlight').evaluate(n => getComputedStyle(n).backgroundColor), await fence.evaluate(n => getComputedStyle(n).backgroundColor), 'nested code surface follows the dark palette');
    const outline = page.locator('.chapter-outline');
    assert.equal(await outline.count(), 1, 'chapters offer an outline');
    await outline.locator('summary').click();
    const links = await outline.locator('a').evaluateAll(nodes => nodes.map(a => ({href: a.getAttribute('href'), text: a.textContent, target: !!document.getElementById(a.hash.slice(1))})));
    assert(links.length >= 5 && links.every(a => a.target && !a.text.startsWith('#')));
    await outline.locator('a').first().click();
    assert.equal(await page.locator('.post-content h2').first().evaluate(h => h === document.activeElement), true);
    await page.evaluate(() => {
      const fixture = document.createElement('div'); fixture.id = 'contrast-fixture';
      fixture.innerHTML = '<div class="highlight"><pre><code><span class="k">const</span> <span class="nv">count</span> = <span class="s">text</span>; <span class="c1">comment</span></code></pre></div><blockquote class="markdown-alert alert-warning"><div class="alert-title">Warning</div></blockquote>';
      document.querySelector('.post-content').append(fixture);
    });
    for (const theme of ['system', 'light', 'dark']) {
      await page.evaluate(theme => theme === 'system' ? document.documentElement.removeAttribute('data-theme') : document.documentElement.setAttribute('data-theme', theme), theme);
      const colors = await page.evaluate(() => {
        const rgb = (node, property) => getComputedStyle(node)[property];
        const body = document.body, code = document.querySelector('#contrast-fixture .highlight');
        return [
          [rgb(body, 'color'), rgb(body, 'backgroundColor'), 'body'],
          ...Array.from(code.querySelectorAll('span')).map(n => [rgb(n, 'color'), rgb(code, 'backgroundColor'), n.className]),
          [rgb(document.querySelector('.site-title'), 'color'), rgb(body, 'backgroundColor'), 'site title']
        ];
      });
      for (const [fg, bg, name] of colors) assert(contrast(fg, bg) >= 4.5, `${theme}: ${name} contrast below 4.5:1 (${fg} on ${bg})`);
      await page.setViewportSize({width: 375, height: 800});
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
      if (theme !== 'light') assert.notEqual(await page.locator('.site-nav').evaluate(n => getComputedStyle(n).backgroundColor), 'rgb(253, 253, 253)');
    }
    await page.setViewportSize({width: 1280, height: 900});
    await page.reload();
    const toggle = page.getByRole('button', {name: 'Switch to light mode', exact: true});
    await toggle.click();
    assert.equal(await page.locator('html').getAttribute('data-theme'), 'light');
    await page.reload();
    assert.equal(await page.locator('html').getAttribute('data-theme'), 'light');
    if (process.env.STUDY_UI_SCREENSHOT) {
      await page.getByRole('button', {name: 'Switch to dark mode', exact: true}).click();
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.setViewportSize({width: 375, height: 800});
      await page.screenshot({path: process.env.STUDY_UI_SCREENSHOT + '-mobile.png'});
      await page.setViewportSize({width: 1280, height: 900});
      await page.screenshot({path: process.env.STUDY_UI_SCREENSHOT + '-desktop.png'});
      await page.locator('div.highlighter-rouge').first().scrollIntoViewIfNeeded();
      await page.screenshot({path: process.env.STUDY_UI_SCREENSHOT + '-code.png'});
    }
    console.log('PASS: chapter outline, keyboard destination, system/explicit themes, text and syntax contrast, mobile width, persisted toggle.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
