const {test}=require('node:test');const assert=require('node:assert/strict');const {roadmapReturnUrl,chapterWithContext}=require('../assets/roadmap-return.js');
test('keeps the forward campaign context across lesson and revision links',()=>{
 const task='fullstack:2026-10-26:day:2026-10-26';
 const search='?roadmapDate=2026-10-26&roadmapTask='+encodeURIComponent(task)+'&token=secret';
 const url=new URL(roadmapReturnUrl(search));
 assert.equal(url.origin,'https://personal.buildora.work');
 assert.equal(url.pathname,'/roadmap');
 assert.equal(url.searchParams.get('date'),'2026-10-26');
 assert.equal(url.searchParams.get('task'),task);
 assert.equal(url.searchParams.has('token'),false);
 const revision=new URL(chapterWithContext('https://study.buildora.work/10-frontend/REVISION.html#scope',search));
 assert.equal(revision.searchParams.get('roadmapTask'),task);
 assert.equal(revision.hash,'#scope');
 for(const invalid of [
  '?roadmapDate=2026-10-26&roadmapTask=fullstack:2026-10-26:day:2026-10-27',
  '?roadmapDate=2026-02-30&roadmapTask=fullstack:2026-10-26:day:2026-02-30',
  '?roadmapDate=2026-10-26&roadmapTask=fullstack:arbitrary:day:2026-10-26',
  '?roadmapDate=2026-10-26&roadmapTask=fullstack:2026-10-26:day:2026-10-26:assignment:study:0630',
 ])assert.equal(roadmapReturnUrl(invalid),'https://personal.buildora.work/roadmap');
});
test('returns to the fixed personal route with matching date/task only',()=>{
 const url=new URL(roadmapReturnUrl('?roadmapDate=2026-10-12&roadmapTask=germany%3A2026%3Aday%3A2026-10-12'));
 assert.equal(url.origin,'https://personal.buildora.work');assert.equal(url.pathname,'/roadmap');assert.equal(url.searchParams.get('date'),'2026-10-12');assert.equal(url.searchParams.get('task'),'germany:2026:day:2026-10-12');
 for(const q of ['?roadmapDate=2026-02-30','?roadmapDate=2026-10-12&roadmapTask=https://evil.example/','?roadmapDate=2026-10-12&roadmapTask=germany:2026:day:2026-10-13&token=secret','?return=https://evil.example/'])assert.equal(roadmapReturnUrl(q),'https://personal.buildora.work/roadmap');
});
test('carries only the safe context to a local chapter/revision destination',()=>{
 const search='?roadmapDate=2026-10-12&roadmapTask=germany:2026:day:2026-10-12&token=secret';
 assert.equal(chapterWithContext('https://study.buildora.work/10-frontend/REVISION.html#scope',search),'https://study.buildora.work/10-frontend/REVISION.html?roadmapDate=2026-10-12&roadmapTask=germany%3A2026%3Aday%3A2026-10-12#scope');
 assert.equal(chapterWithContext('https://evil.example/a.html',search),'https://evil.example/a.html');
 assert.equal(chapterWithContext('https://study.buildora.work/auth/logout',search),'https://study.buildora.work/auth/logout');
});
