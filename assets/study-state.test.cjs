const {test}=require('node:test');
const assert=require('node:assert/strict');
const {material,isLearningPath,createStore}=require('./study-state.js');
const path='/10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.05-lexical-environment.html';
const record={version:1,path,anchor:'summary',title:'Lexical Environment',section:'Summary',savedAt:Date.now()};
test('material distinguishes interview banks, revision companions and references',()=>{
 assert.equal(material({p:'topic-interview-questions.html',c:'Reference',g:['concept']}),'interview');
 assert.equal(material({p:'stack/REVISION.html',c:'Reference',g:[]}),'revision');
 assert.equal(material({p:'topic.html',c:'Reference',g:[]}),'reference');
 assert.equal(material({p:'topic.html',c:'Core',g:['concept']}),'learn');
});
test('only published learning chapters can be saved, with bounded labels and no extra fields',()=>{
 const store=createStore(null,[path]);
 assert.equal(store.write({...record,query:'private',roadmapTask:'private',title:'x'.repeat(200)}),true);
 assert.equal(store.read().title.length,160);assert.equal(store.read().query,undefined);
 for(const invalid of [{path:'/auth/login.html'},{path:path+'?q=private'},{path:'/removed.html'},{version:2},{anchor:'x?token=private'},{savedAt:Infinity}])assert.equal(store.write({...record,...invalid}),false);
 assert.equal(isLearningPath('/INDEX.html'),false);assert.equal(isLearningPath('/80-lanes-abroad-full-stack/personal/80.01-profile.html'),false);
});
test('malformed state is ignored and storage refusal retains a reversible in-memory position',()=>{
 const corrupt=createStore({getItem:()=>'{bad',removeItem(){}},[path]);assert.equal(corrupt.read(),null);
 const denied=createStore({getItem(){throw Error()},setItem(){throw Error()},removeItem(){throw Error()}},[path]);
 assert.equal(denied.read(),null);denied.write(record);const prior=denied.clear();assert.equal(denied.read(),null);denied.write(prior);assert.deepEqual(denied.read(),record);
});
