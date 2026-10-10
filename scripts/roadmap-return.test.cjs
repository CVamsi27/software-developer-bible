const {test}=require('node:test');const assert=require('node:assert/strict');const {roadmapReturnUrl,chapterWithContext}=require('../assets/roadmap-return.js');
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
