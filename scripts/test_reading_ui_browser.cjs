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
    for (const width of [1280, 1920]) {
      await page.setViewportSize({width, height: 900});
      const sizes = await page.evaluate(() => {
        const article = document.querySelector('.post-content');
        const paragraph = Array.from(article.children).find(n => n.tagName === 'P' && !n.querySelector('img'));
        return {article: article.clientWidth, paragraph: paragraph.getBoundingClientRect().width};
      });
      assert(Math.abs(sizes.article - sizes.paragraph) <= 1, `paragraph fills article at ${width}px: ${JSON.stringify(sizes)}`);
    }
    // Long inline configuration names must not widen a mobile document.
    await page.evaluate(() => {
      const paragraph = document.createElement('p');
      paragraph.id = 'inline-code-width-fixture';
      const code = document.createElement('code');
      code.textContent = 'unclean.leader.election.enable=false';
      paragraph.append('Configuration: ', code);
      document.querySelector('.post-content').append(paragraph);
    });
    for (const theme of ['light', 'dark']) {
      await page.evaluate(theme => document.documentElement.setAttribute('data-theme', theme), theme);
      for (const width of [320, 375]) {
        await page.setViewportSize({width, height: 900});
        const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
        assert(scrollWidth <= width, `long inline code widens ${theme} page: ${scrollWidth} > ${width}`);
      }
    }
    await page.evaluate(() => document.getElementById('inline-code-width-fixture').remove());
    await page.setViewportSize({width: 1280, height: 900});
    const fence = page.locator('div.highlighter-rouge').first();
    assert.equal(await fence.locator('.copy-code-btn').count(), 1, 'one Copy control per code block');
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
          ...Array.from(document.querySelectorAll('.read-aloud [data-read], .read-aloud [data-pause]')).map(n => [rgb(n, 'color'), rgb(n, 'backgroundColor'), 'read-aloud action']),
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
    await page.emulateMedia({colorScheme: 'light'});
    await page.getByRole('button', {name: 'Switch to dark mode', exact: true}).waitFor({timeout: 2000});
    assert.equal(await page.getByRole('button', {name: 'Switch to dark mode', exact: true}).count(), 1, 'toggle follows a changed system preference');
    await page.emulateMedia({colorScheme: 'dark'});
    await page.getByRole('button', {name: 'Switch to light mode', exact: true}).waitFor({timeout: 2000});
    const toggle = page.getByRole('button', {name: 'Switch to light mode', exact: true});
    await toggle.click();
    assert.equal(await page.locator('html').getAttribute('data-theme'), 'light');
    await page.reload();
    assert.equal(await page.locator('html').getAttribute('data-theme'), 'light');
    const deniedStoragePage = await browser.newPage({colorScheme: 'dark'});
    await deniedStoragePage.addInitScript(() => {
      Storage.prototype.getItem = () => { throw new DOMException('Storage unavailable', 'SecurityError'); };
      Storage.prototype.setItem = () => { throw new DOMException('Storage unavailable', 'SecurityError'); };
    });
    await deniedStoragePage.goto(page.url());
    await deniedStoragePage.getByRole('button', {name: 'Switch to light mode', exact: true}).click();
    assert.equal(await deniedStoragePage.locator('html').getAttribute('data-theme'), 'light', 'theme works when preference storage is unavailable');
    await deniedStoragePage.close();
    const motionPage = await browser.newPage({colorScheme: 'light', reducedMotion: 'no-preference'});
    await motionPage.goto(page.url());
    await motionPage.locator('.theme-toggle-btn').waitFor();
    await motionPage.setViewportSize({width: 1280, height: 900});
    await motionPage.evaluate(() => document.documentElement.setAttribute('data-theme', 'light'));
    await motionPage.setViewportSize({width: 375, height: 800});
    await motionPage.evaluate(() => document.documentElement.setAttribute('data-theme', 'dark'));
    const motionState = await motionPage.evaluate(() => new Promise(resolve => requestAnimationFrame(() => {
      const control = document.querySelector('.theme-toggle-btn');
      const menu = document.querySelector('label[for="nav-trigger"]');
      const r = control.getBoundingClientRect(), m = menu.getBoundingClientRect();
      const hit = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2);
      resolve({controlRight: r.right, menuLeft: m.left, hit: control === hit || control.contains(hit),
        headerBackground: getComputedStyle(document.querySelector('.site-header')).backgroundColor,
        titleColor: getComputedStyle(document.querySelector('.site-title')).color,
        expectedHeaderBackground: getComputedStyle(document.documentElement).getPropertyValue('--header-bg').trim()});
    })));
    assert(motionState.controlRight + 4 <= motionState.menuLeft && motionState.hit,
      `normal-motion resize keeps the theme control reachable: ${JSON.stringify(motionState)}`);
    assert.equal(motionState.headerBackground, motionState.expectedHeaderBackground,
      'theme foreground and header background change together without an intermediate palette');
    assert(contrast(motionState.titleColor, motionState.headerBackground) >= 4.5,
      'theme switch preserves immediate header-title contrast with normal motion');
    await motionPage.close();
    if (process.env.STUDY_UI_SCREENSHOT) {
      await page.evaluate(() => document.getElementById('contrast-fixture')?.remove());
      for (const theme of ['light', 'dark']) {
        if (await page.locator('html').getAttribute('data-theme') !== theme) {
          await page.getByRole('button', {name: 'Switch to ' + theme + ' mode', exact: true}).click();
        }
        for (const [label, width, height] of [['mobile', 375, 800], ['desktop', 1280, 900]]) {
          await page.setViewportSize({width, height});
          await page.evaluate(() => window.scrollTo(0, 0));
          await page.screenshot({path: process.env.STUDY_UI_SCREENSHOT + '-' + theme + '-' + label + '.png'});
        }
        await page.locator('div.highlighter-rouge').first().scrollIntoViewIfNeeded();
        await page.screenshot({path: process.env.STUDY_UI_SCREENSHOT + '-' + theme + '-code.png'});
      }
    }
    console.log('PASS: chapter outline, keyboard destination, system/explicit themes, text and syntax contrast, mobile width, persisted toggle.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
