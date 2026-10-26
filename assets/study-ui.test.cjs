/* DOM behavior tests; install jsdom outside the repo and set NODE_PATH. */
const {test} = require('node:test');
const assert = require('node:assert/strict');
const {JSDOM} = require('jsdom');
const fs = require('node:fs');
const path = require('node:path');
const root = path.join(__dirname, '..');
const chapter='/10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.05-lexical-environment.html';
const next=chapter.replace('05-lexical-environment','06-closures');
const revision=chapter.slice(0,chapter.lastIndexOf('/')+1)+'REVISION.html';
const paths=[chapter,next,revision,'/INDEX.html'];
function boot(html, route, scripts, setup){
 const dom=new JSDOM(html,{url:'https://study.buildora.work'+route,runScripts:'outside-only',pretendToBeVisual:true});
 const w=dom.window; w.StudyPublishedPaths=paths; w.matchMedia=()=>({matches:false,addEventListener(){}}); w.scrollTo=()=>{};
 if(setup)setup(w);
 for(const script of ['study-state.js','roadmap-return.js',...scripts]){
  const p=path.join(__dirname,script); if(fs.existsSync(p))w.eval(fs.readFileSync(p,'utf8'));
 }
 w.document.dispatchEvent(new w.Event('DOMContentLoaded'));
 return dom;
}
const article='<main><div class="post-content"><p><a href="#"><img alt="Section" src="https://img.shields.io/badge/section-JavaScript-blue"></a></p><h1>Lexical Environment</h1><h2 id="definition">Definition</h2><p>Original prose.</p><h2 id="first-principles">First Principles</h2><p>Reasoning.</p><h2 id="summary">Summary</h2><p>Authored summary.</p><h2 id="see-also">See Also</h2><a href="REVISION.html">Category revision</a><p><a href="'+next+'">Next: Closures →</a></p></div></main>';
test('reader keeps metadata and leaves authored next and revision navigation in one place',()=>{
 const dom=boot(article,chapter,['reading-ui.js']); const d=dom.window.document;
 assert.ok(d.querySelector('select[aria-label="Reading width"]'),'Reading width control is available');
 assert.equal(d.querySelector('.chapter-details img').alt,'Section');
 assert.equal(d.querySelector('.study-continuation'),null,'No mirrored chapter navigation is generated');
 assert.equal([...d.querySelectorAll('a[href*="closures"]')].length,1,'The authored Next link appears once');
 assert.equal([...d.querySelectorAll('a[href*="REVISION"]')].length,1,'The authored revision link appears once');
 dom.window.close();
});
test('reader shows the roadmap return link only with valid roadmap context',()=>{
 const plain=boot(article,chapter,['reading-ui.js']),plainDoc=plain.window.document;
 assert.equal(plainDoc.querySelector('.roadmap-return'),null,'No personal roadmap link without context');
 plain.window.close();
 for(const [date,task] of [['2026-10-12','germany:2026:day:2026-10-12'],['2026-10-26','fullstack:2026-10-26:day:2026-10-26']]){
  const dom=boot(article,chapter+'?roadmapDate='+date+'&roadmapTask='+encodeURIComponent(task),['reading-ui.js']),d=dom.window.document;
  const back=d.querySelector('.reader-breadcrumb .roadmap-return');
  assert.ok(back,'Breadcrumb return link appears with roadmap context');
  assert.equal(back.textContent,'Return to personal roadmap');
  assert.equal(new URL(back.href).origin,'https://personal.buildora.work');
  assert.equal(new URL(back.href).searchParams.get('date'),date);
  assert.equal(new URL(back.href).searchParams.get('task'),task);
  dom.window.close();
 }
});
test('indexes get no chapter width or narration controls',()=>{
 const dom=boot(article,'/INDEX.html',['reading-ui.js','read-aloud.js']);
 assert.equal(dom.window.document.querySelector('.read-aloud'),null);
 assert.equal(dom.window.document.querySelector('[aria-label="Reading width"]'),null); dom.window.close();
});
test('revision reveal preserves complete answers and uncertain authored blocks',()=>{
 const html='<div class="post-content"><h1>Revision</h1><h2>Topic</h2><p>Source: chapter</p><p><strong>Q:</strong> Explain?</p><p><strong>A:</strong> First paragraph.</p><p>Second paragraph.</p><pre><code>answer()</code></pre><ul><li>Boundary.</li></ul><p><strong>Q:</strong> Unanswered?</p><p>Keep this visible.</p><h2>Another topic</h2></div>';
 const dom=boot(html,revision,['revision-ui.js']); const d=dom.window.document;
 assert.equal(d.querySelectorAll('.revision-answer').length,1);
 assert.equal(d.querySelector('.revision-answer pre').textContent,'answer()');
 assert.equal(d.querySelector('.revision-answer li').textContent,'Boundary.');
 assert.ok(d.querySelector('.revision-answer').textContent.includes('Second paragraph.'));
 d.querySelector('[data-reveal-all]').click(); assert.equal(d.querySelector('.revision-answer').open,true);
 assert.ok([...d.querySelectorAll('.post-content > p')].some(p=>p.textContent==='Keep this visible.'));dom.window.close();
});
test('interview practice remains separate from revision reveal',()=>{
 const dom=boot('<div class="post-content"><p><strong>Q:</strong> Question?</p><p><strong>A:</strong> Answer.</p></div>',chapter.replace('05-lexical-environment','11-interview-questions'),['revision-ui.js']);
 assert.equal(dom.window.document.querySelector('details'),null);dom.window.close();
});
test('resume validates catalog and strips unrelated fields; denied storage still works in memory',()=>{
 const dom=boot('',chapter,[]);const w=dom.window;
 const fallback={read:()=>null,write:()=>false,clear:()=>null};
 const store=w.StudyState?.createStore({getItem(){throw Error('denied')},setItem(){throw Error('denied')},removeItem(){throw Error('denied')}},paths)||fallback;
 store.write({version:1,path:chapter,anchor:'summary',title:'Lexical Environment',section:'Summary',savedAt:Date.now(),query:'secret',roadmapTask:'private'});
 const record=store.read();assert.equal(record?.path,chapter);assert.equal(record.query,undefined);assert.equal(record.roadmapTask,undefined);
 const old=store.clear();assert.equal(store.read(),null);store.write(old);assert.equal(store.read().anchor,'summary');
 assert.equal(store.write({...old,path:'/auth/login.html'}),false);
 assert.equal(store.write({...old,path:'/removed.html'}),false);
 assert.equal(store.write({...old,version:2}),false);dom.window.close();
});
test('search filters material, clears filters without clearing query and restores Back state',()=>{
 let html=fs.readFileSync(path.join(root,'search.html'),'utf8').replace(/<script\b[^>]*>[\s\S]*?<\/script>/g,'');
 const rows=[{p:chapter.slice(1),t:'Scope lesson',s:'JavaScript',c:'Core',g:['concept'],m:15},{p:revision.slice(1),t:'Scope revision',s:'JavaScript',c:'Reference',g:['revision'],m:4},{p:'other.html',t:'Other topic',s:'Node.js',c:'Core',g:[],m:5}];
 html+='<script id="study-search-data" type="application/json">'+JSON.stringify(rows)+'</script>';
 const dom=boot(html,'/search.html?q=scope',['search-ui.js']);const w=dom.window,d=w.document;
 const material=d.querySelector('#material');assert.ok(material,'Material filter is available');
 material.value='revision';material.dispatchEvent(new w.Event('change'));
 assert.equal(d.querySelectorAll('.search-result').length,1);assert.ok(d.querySelector('.search-result').textContent.includes('Scope revision'));
 d.querySelector('[data-clear-filters]').click();assert.equal(d.querySelector('#q').value,'scope');assert.equal(d.querySelectorAll('.search-result').length,2);
 w.history.replaceState(null,'','?q=scope&material=revision');w.dispatchEvent(new w.PopStateEvent('popstate'));
 assert.equal(material.value,'revision');assert.equal(d.querySelectorAll('.search-result').length,1);dom.window.close();
});

test('resume rejects corrupt, stale and queried records',()=>{
 const dom=boot('',chapter,[]),w=dom.window;
 for(const value of ['bad json',JSON.stringify({version:2}),JSON.stringify({version:1,path:'/removed.html'})]){
  const storage={getItem:()=>value,removeItem(){}};assert.equal(w.StudyState.createStore(storage,paths).read(),null);
 }
 const storage=w.localStorage,store=w.StudyState.createStore(storage,paths);
 const r={version:1,path:chapter,anchor:'summary',title:'Title',section:'Summary',savedAt:Date.now()};
 assert.equal(store.write({...r,path:chapter+'?q=secret'}),false);
 assert.equal(store.write({...r,savedAt:Infinity}),false);
 assert.equal(store.write({...r,anchor:'summary?token=private'}),false);
 assert.equal(w.StudyState.material({p:'x-interview-questions.html',c:'Reference',g:['concept']}),'interview');dom.window.close();
});
function resumeBoot(route,record){
 const html=article;
 const dom=new JSDOM(html,{url:'https://study.buildora.work'+route,runScripts:'outside-only',pretendToBeVisual:true});
 const w=dom.window; w.StudyPublishedPaths=paths; w.scrollTo=function(options){w.scrolledTop=options.top;}; w.HTMLElement.prototype.scrollIntoView=function(){w.scrolledTo=this.id;};
 if(record)w.localStorage.setItem('sdb-study-resume-v1',JSON.stringify(record));
 for(const file of ['study-state.js','study-resume.js'])w.eval(fs.readFileSync(path.join(__dirname,file),'utf8'));
 w.document.dispatchEvent(new w.Event('DOMContentLoaded'));return dom;
}
test('resume is explicit, a direct fragment wins, and stale anchors give a notice',()=>{
 const r={version:1,path:chapter,anchor:'summary',title:'Title',section:'Summary',savedAt:Date.now()};
 let dom=resumeBoot(chapter,r);assert.equal(dom.window.scrolledTo,undefined);dom.window.close();
 dom=resumeBoot(chapter+'?resume=1#definition',r);assert.equal(dom.window.scrolledTo,undefined);dom.window.close();
 dom=resumeBoot(chapter+'?resume=1',r);assert.equal(dom.window.scrolledTo,'summary');assert.equal(dom.window.location.hash,'#summary');dom.window.close();
 dom=resumeBoot(chapter+'?resume=1',{...r,anchor:'removed'});assert.match(dom.window.document.querySelector('[role="status"]').textContent,/chapter changed/);assert.equal(dom.window.scrolledTop,0);dom.window.close();
});
test('only deliberate chapter activity saves, and pagehide flushes the latest section',()=>{
 const dom=resumeBoot(chapter),w=dom.window,d=w.document,h=d.getElementById('summary');
 d.dispatchEvent(new w.CustomEvent('study:section',{detail:{heading:h,deliberate:false}}));
 assert.equal(w.StudyResumeStore.read(),null);
 d.dispatchEvent(new w.CustomEvent('study:section',{detail:{heading:h,deliberate:true}}));
 w.dispatchEvent(new w.Event('pagehide'));assert.equal(w.StudyResumeStore.read().anchor,'summary');dom.window.close();
 const other=resumeBoot(revision);other.window.document.dispatchEvent(new other.window.CustomEvent('study:section',{detail:{heading:other.window.document.getElementById('summary'),deliberate:true}}));
 other.window.dispatchEvent(new other.window.Event('pagehide'));assert.equal(other.window.StudyResumeStore.read(),null);other.window.close();
});


test('returning home prioritizes the saved chapter and clearing is reversible',()=>{
 const html=fs.readFileSync(path.join(root,'index.html'),'utf8').replace(/^---[\s\S]*?---/, '');
 const record={version:1,path:chapter,anchor:'summary',title:'Lexical Environment',section:'Summary',savedAt:Date.now()};
 const dom=boot(html,'/',['study-resume.js'],w=>w.localStorage.setItem('sdb-study-resume-v1',JSON.stringify(record))),d=dom.window.document;
 assert.equal(d.querySelector('.home-intro h1').textContent,'Continue your study.');
 assert.equal(d.querySelector('.resume-card').hidden,false);
 d.querySelector('[data-clear-resume]').click();assert.equal(d.querySelector('.resume-card').hidden,true);
 assert.equal(d.querySelector('.home-intro h1').textContent,'Make your next study session count.');
 d.querySelector('.resume-feedback button').click();assert.equal(d.querySelector('.resume-card').hidden,false);
 assert.equal(d.querySelector('.home-intro h1').textContent,'Continue your study.');dom.window.close();
});

test('chapter details moves only the original header badges, leaving lesson badges in place',()=>{
 const html=article.replace('<p>Original prose.</p>','<p id="body-badge"><img alt="Build status" src="https://img.shields.io/badge/build-passing-green">Original prose.</p>');
 const dom=boot(html,chapter,['reading-ui.js']),d=dom.window.document;
 assert.equal(d.getElementById('body-badge').closest('.chapter-details'),null);
 assert.equal(d.getElementById('body-badge').previousElementSibling.id,'definition');dom.window.close();
});

test('Cloudflare clean chapter routes mount reader and save a canonical resume path',()=>{
 const clean=chapter.replace(/\.html$/, '');
 const dom=boot(article,clean,['reading-ui.js','read-aloud.js','study-resume.js']);
 const w=dom.window,d=w.document;
 assert.ok(d.querySelector('[aria-label="Reading width"]'));
 assert.ok(d.querySelector('.read-aloud'));
 d.dispatchEvent(new w.CustomEvent('study:section',{detail:{heading:d.getElementById('summary'),deliberate:true}}));
 w.dispatchEvent(new w.Event('pagehide'));
 assert.equal(w.StudyResumeStore.read().path,chapter);
 dom.window.close();
});
test('Cloudflare clean revision routes reveal answers and mount the reader',()=>{
 const dom=boot('<div class="post-content"><h1>Revision</h1><h2 id="topic">Topic</h2><p><strong>Q:</strong> Explain?</p><p><strong>A:</strong> Answer.</p></div>',revision.replace(/\.html$/, ''),['reading-ui.js','revision-ui.js','read-aloud.js']);
 assert.ok(dom.window.document.querySelector('.revision-answer'));
 assert.equal(dom.window.document.querySelector('.post-content').dataset.studyReader,'true');
 assert.ok(dom.window.document.querySelector('.read-aloud'));
 dom.window.close();
});
test('reference reader exposes metadata tokens and decorative line numbers without changing code',()=>{
 const code='const label = 1;\nconsole.log(label);\n';
 const dom=boot(article.replace('<p>Original prose.</p>','<div class="language-javascript highlighter-rouge"><div class="highlight"><pre class="highlight"><code>'+code+'</code></pre></div></div>'),chapter,['reading-ui.js']);
 const d=dom.window.document;
 assert.equal(d.querySelector('.reader-meta-section').textContent,'JavaScript');
 assert.equal(d.querySelector('.code-line-numbers').getAttribute('aria-hidden'),'true');
 assert.equal(d.querySelector('.code-line-numbers').textContent,'1\n2');
 assert.equal(d.querySelector('pre code').textContent,code);
 dom.window.close();
});
test('code panels are named keyboard scroll regions and mobile outline closes after navigation',()=>{
 const panel='<div class="language-javascript highlighter-rouge"><div class="highlight"><pre><code>const value = 1;\n</code></pre></div></div>';
 const dom=boot(article.replace('<p>Original prose.</p>',panel),chapter,['reading-ui.js']);
 const d=dom.window.document,pre=d.querySelector('pre');
 assert.equal(pre.getAttribute('tabindex'),'0');
 assert.equal(pre.getAttribute('role'),'region');
 assert.equal(pre.getAttribute('aria-label'),'JavaScript code');
 const outline=d.querySelector('.chapter-outline'); outline.open=true;
 outline.querySelector('a').click();
 assert.equal(outline.open,false);
 assert.equal(d.activeElement.id,'definition');
 dom.window.close();
});
test('desktop outline stays open when its heading is clicked',()=>{
 const dom=boot(article,chapter,['reading-ui.js'],w=>{w.matchMedia=()=>({matches:true,addEventListener(){}});});
 const outline=dom.window.document.querySelector('.chapter-outline');
 assert.equal(outline.open,true);outline.querySelector('summary').click();assert.equal(outline.open,true);
 dom.window.close();
});
test('copy reports a live confirmation while preserving code text and focus',async()=>{
 const dom=boot('<div class="language-javascript highlighter-rouge"><pre><code>const count = 1;\n</code></pre></div>',chapter,[]);
 const w=dom.window,d=w.document;let copied;
 w.navigator.clipboard={writeText:async text=>{copied=text;}};
 const head=fs.readFileSync(path.join(root,'_includes/head-custom.html'),'utf8');
 const start=head.indexOf('var codeContainers ='),end=head.indexOf('// 5. GitHub Alert',start);
 assert.ok(start>=0 && end>start);w.eval(head.slice(start,end));
 const button=d.querySelector('.copy-code-btn');button.focus();button.click();
 await Promise.resolve();
 assert.equal(copied,'const count = 1;\n');
 assert.equal(d.activeElement,button);
 assert.equal(d.querySelector('[role="status"]').textContent,'Code copied to clipboard.');
 assert.equal(button.getAttribute('aria-label'),'Code copied');
 dom.window.close();
});
test('theme button DOM order follows the desktop and phone header layouts',()=>{
 const html='<header class="site-header"><div class="wrapper"><a class="site-title" href="/">Developer Bible</a><nav class="site-nav">Library</nav><form class="header-search"><input name="q"></form></div></header>';
 for(const mobile of [false,true]){
  const dom=boot(html,chapter,['theme.js'],w=>{w.matchMedia=query=>({matches:query==='(max-width: 700px)' && mobile,addEventListener(){}});});
  const wrapper=dom.window.document.querySelector('.wrapper');
  assert.equal(wrapper.children[mobile?1:3].className,'theme-toggle-btn');
  dom.window.close();
 }
});
test('copy failures give recovery guidance and feedback is excluded from narration',async()=>{
 for(const unavailable of [false,true]){
  const dom=boot('<div class="post-content"><h1>Lesson</h1><p>Authored explanation.</p><div class="highlighter-rouge"><pre><code>const value = 1;</code></pre></div></div>',chapter,['read-aloud.js']);
  const w=dom.window,d=w.document;
  if(!unavailable)w.navigator.clipboard={writeText:async()=>{throw Error('denied');}};
  const head=fs.readFileSync(path.join(root,'_includes/head-custom.html'),'utf8');
  const start=head.indexOf('var codeContainers ='),end=head.indexOf('// 5. GitHub Alert',start);w.eval(head.slice(start,end));
  d.querySelector('.copy-code-btn').click();await new Promise(resolve=>setImmediate(resolve));
  assert.match(d.querySelector('.copy-feedback').textContent,/Select the code and copy it manually/);
  const spoken=w.SDBReadAloud.extractChapter(d.querySelector('.post-content')).map(group=>group.text).join(' ');
  assert.ok(spoken.includes('Authored explanation.'));
  assert.ok(!spoken.includes('copy it manually'));
  dom.window.close();
 }
});
test('the last outline section is current at the document bottom even below the header threshold',()=>{
 const html=article.replace('</div></main>','<h2 id="references">References</h2><p>Source links.</p></div></main>');
 const dom=boot(html,chapter,['reading-ui.js'],w=>{
  w.innerHeight=1000;w.scrollY=2000;
  Object.defineProperty(w.document.documentElement,'scrollHeight',{value:3000});
  w.document.querySelectorAll('h2').forEach(h=>{h.getBoundingClientRect=()=>({top:h.id==='references'?250:100});});
 });
 assert.equal(dom.window.document.querySelector('.chapter-outline a[aria-current]').hash,'#references');
 dom.window.close();
});
test('narration skips decorative language captions while retaining authored prose',()=>{
 const html=article.replace('<p>Original prose.</p>','<p>Original prose.</p><div class="language-javascript highlighter-rouge"><pre><code>const count = 1;</code></pre></div>');
 const dom=boot(html,chapter,['reading-ui.js','read-aloud.js']);
 const spoken=dom.window.SDBReadAloud.extractChapter(dom.window.document.querySelector('.post-content')).map(group=>group.text).join(' ');
 assert.ok(spoken.includes('Original prose.'));assert.ok(!spoken.includes('JavaScript'));
 dom.window.close();
});
