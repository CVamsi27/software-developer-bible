/* Exercise navigation pages as well as chapters: inferred titles and long tables
 * differ from the small chapter fixture used by the reader suite. */
const {chromium} = require('@playwright/test');
const assert = require('node:assert/strict');
function luminance(value) {
  const channels = value.match(/[\d.]+/g).slice(0, 3).map(Number).map(v => {
    v /= 255; return v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4;
  });
  return channels[0] * .2126 + channels[1] * .7152 + channels[2] * .0722;
}
async function textSurfaces(locator) {
  return locator.evaluateAll(nodes => {
    function background(node) {
      const layers = [];
      for (let n = node; n; n = n.parentElement) {
        const value = getComputedStyle(n).backgroundColor.match(/[\d.]+/g).map(Number);
        layers.push(value);
        if ((value[3] ?? 1) === 1) break;
      }
      let rgb = [255, 255, 255];
      for (const c of layers.reverse()) {
        rgb = rgb.map((v, i) => c[i] * (c[3] ?? 1) + v * (1 - (c[3] ?? 1)));
      }
      return 'rgb(' + rgb.join(',') + ')';
    }
    return nodes.map(n => ({
      fg: getComputedStyle(n).color, bg: background(n),
      text: n.textContent.trim().slice(0, 35)
    }));
  });
}
(async () => {
  const browser = await chromium.launch({headless: true});
  const failures = [];
  const check = (name, action) => { try { action(); } catch (error) { failures.push(name + ': ' + error.message); } };
  try {
    const context = await browser.newContext({reducedMotion: 'reduce', permissions: ['clipboard-read', 'clipboard-write']});
    const page = await context.newPage();
    page.setDefaultTimeout(5000);
    const homeRoute = process.env.STUDY_HOME_ROUTE || 'index.html';
    const scopeIndex = '10-frontend/10.1-javascript/01-execution-and-scope/INDEX.html';
    const motionChapter = '10-frontend/10.6-animation/10.6.02-framer-motion.html';
    for (const route of ['ROADMAP.html', 'README.html', 'INDEX.html', homeRoute, 'search.html', scopeIndex, motionChapter]) {
      const response = await page.goto('http://127.0.0.1:4337/' + route, {waitUntil: 'domcontentloaded'});
      check(route + ' response', () => assert.equal(response.status(), 200));
      if (response.status() !== 200) continue;
      if (route !== 'search.html') await page.locator('.back-to-top').waitFor({state: 'attached'});
      const titles = await page.locator('h1:visible').allTextContents();
      check(route + ' title', () => assert.equal(titles.length, 1, 'one visible page title'));
      if (route === scopeIndex) {
        check(route + ' authored title', () => assert.equal(titles[0].trim(), 'Execution & Scope — JavaScript'));
      }
      if (route === motionChapter) {
        check(route + ' authored title', () => assert.equal(titles[0].trim(), 'Motion for React (formerly Framer Motion)'));
      }
      for (const theme of ['light', 'dark']) {
        await page.evaluate(theme => document.documentElement.setAttribute('data-theme', theme), theme);
        await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
        for (const width of [320, 375, 600, 1280]) {
          await page.setViewportSize({width, height: 850});
          const scroll = await page.evaluate(() => document.documentElement.scrollWidth);
          check(route + ' ' + theme + ' width', () => assert(scroll <= width, `page width ${scroll} exceeds viewport ${width}`));
          if (width <= 600 && await page.locator('#nav-trigger').count()) {
            const controls = await page.evaluate(() => {
              const theme = document.querySelector('.theme-toggle-btn');
              const menu = document.querySelector('label[for="nav-trigger"]');
              const title = document.querySelector('.site-title');
              const rect = node => {
                const r = node.getBoundingClientRect();
                const hit = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2);
                return {left: r.left, right: r.right, width: r.width, height: r.height, hit: node === hit || node.contains(hit)};
              };
              return {theme: rect(theme), menu: rect(menu), title: rect(title)};
            });
            check(route + ' ' + width + ' header controls', () => {
              assert(controls.theme.right + 4 <= controls.menu.left, 'theme and menu need separate hit areas');
              assert(controls.title.right + 4 <= controls.theme.left, 'site title must leave room for controls');
              for (const control of [controls.theme, controls.menu]) {
                assert(control.width >= 44 && control.height >= 44, 'touch targets need 44 pixels');
                assert(control.left >= 0 && control.right <= width && control.hit, 'control is inside viewport and clickable');
              }
            });
            await page.locator('label[for="nav-trigger"]').click();
            const menuWidth = await page.evaluate(() => document.documentElement.scrollWidth);
            check(route + ' menu width', () => assert(menuWidth <= width));
            const opened = await page.locator('.site-nav .trigger').isVisible();
            check(route + ' opened menu', () => assert(opened));
            assert(await page.locator('.theme-toggle-btn').evaluate(node => {
              const r = node.getBoundingClientRect();
              return node.contains(document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2));
            }), 'opened menu leaves theme control accessible');
            await page.locator('label[for="nav-trigger"]').click();
            const toggle = page.getByRole('button', {name: 'Toggle navigation', exact: true});
            await toggle.focus();
            await page.keyboard.press('Enter');
            assert.equal(await toggle.getAttribute('aria-expanded'), 'true');
            assert(await page.locator('.site-nav .trigger').isVisible());
            await page.keyboard.press('Escape');
            assert.equal(await toggle.getAttribute('aria-expanded'), 'false');
            assert(!await page.locator('.site-nav .trigger').isVisible());
            assert(await toggle.evaluate(node => node === document.activeElement));
            await page.keyboard.press('Space');
            assert.equal(await toggle.getAttribute('aria-expanded'), 'true');
            assert(await page.locator('.site-nav .trigger').isVisible());
            await page.keyboard.press('Space');
            assert.equal(await toggle.getAttribute('aria-expanded'), 'false');
            assert(!await page.locator('.site-nav .trigger').isVisible());
          }
        }
        if (await page.locator('table').count()) {
          const surfaces = await textSurfaces(page.locator('table th, table td, table td a'));
          for (const c of surfaces) {
            const a = luminance(c.fg), b = luminance(c.bg);
            check(route + ' ' + theme + ' table ' + c.text, () => assert((Math.max(a,b)+.05)/(Math.min(a,b)+.05) >= 4.5));
          }
          const rows = page.locator('table tbody tr');
          if (await rows.count()) {
            const row = rows.nth(Math.min(1, await rows.count() - 1));
            await row.hover();
            const hovered = await textSurfaces(row.locator('td, td a'));
            for (const c of hovered) {
              const a = luminance(c.fg), b = luminance(c.bg);
              check(route + ' ' + theme + ' hovered cell ' + c.text, () => assert((Math.max(a,b)+.05)/(Math.min(a,b)+.05) >= 4.5));
            }
            await page.mouse.move(0, 0);
          }
        }
        if (route === homeRoute) {
          if (!await page.locator('.hero-actions a').count()) {
            failures.push('homepage actions missing: on a case-insensitive preview filesystem, use STUDY_HOME_ROUTE for the separately rendered homepage');
            continue;
          }
          const colors = await page.locator('.hero-actions a').evaluateAll(nodes => nodes.map(n => {
            const s = getComputedStyle(n); return {fg: s.color, bg: s.backgroundColor};
          }));
          for (const c of colors) {
            const a = luminance(c.fg), b = luminance(c.bg);
            check(theme + ' homepage action contrast', () => assert((Math.max(a,b)+.05)/(Math.min(a,b)+.05) >= 4.5));
          }
        }
      }
      if (route === 'ROADMAP.html') {
        const block = page.locator('div.highlighter-rouge').first();
        const expected = await block.locator('pre code').textContent();
        await block.hover();
        await block.getByRole('button', {name: 'Copy code', exact: true}).click();
        await block.locator('.copied').waitFor();
        assert.equal(await page.evaluate(() => navigator.clipboard.readText()), expected, 'Copy preserves the code text');
      }
    }
    assert.deepEqual(failures, []);
    console.log('PASS: navigation titles, responsive layout, separate mobile header targets, opened menus, table/hover and homepage contrast, and copied text.');
  } finally { await browser.close(); }
})().catch(error => {console.error(error); process.exitCode = 1;});
