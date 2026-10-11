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
test('reader keeps metadata and offers published next and revision after Summary',()=>{
 const dom=boot(article,chapter,['reading-ui.js']); const d=dom.window.document;
 assert.ok(d.querySelector('select[aria-label="Reading width"]'),'Reading width control is available');
 assert.equal(d.querySelector('.chapter-details img').alt,'Section');
 assert.equal(d.querySelector('.study-continuation a[href*="REVISION"]').pathname,revision);
 assert.equal(d.querySelector('.study-continuation a[href*="closures"]').pathname,next);
 assert.ok(d.querySelector('.study-continuation').compareDocumentPosition(d.getElementById('see-also'))&4);
 dom.window.close();
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
