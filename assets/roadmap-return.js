/* Fixed-origin roadmap context; no arbitrary redirect or credential parameters. */
(function(root){
 var base='https://personal.buildora.work/roadmap';
 function context(search){
  var q=new URLSearchParams(search),date=q.get('roadmapDate'),task=q.get('roadmapTask');
  if(!date||!/^\d{4}-\d{2}-\d{2}$/.test(date)||task!=='germany:2026:day:'+date)return null;
  var parsed=new Date(date+'T12:00:00Z');
  if(!Number.isFinite(parsed.getTime())||parsed.toISOString().slice(0,10)!==date)return null;
  return {date:date,task:task};
 }
 function roadmapReturnUrl(search){
  var c=context(search);if(!c)return base;
  var url=new URL(base);url.searchParams.set('view','roadmap');url.searchParams.set('panel','today');url.searchParams.set('date',c.date);url.searchParams.set('task',c.task);return url.toString();
 }
 function chapterWithContext(url,search){
  var c=context(search);if(!c)return url;
  try{var target=new URL(url);if(target.origin!=='https://study.buildora.work'||/^\/(?:auth|api)\//.test(target.pathname)||! /\.(?:md|html)$/.test(target.pathname))return url;
   target.searchParams.set('roadmapDate',c.date);target.searchParams.set('roadmapTask',c.task);return target.toString();
  }catch{return url;}
 }
 if(typeof module!=='undefined')module.exports={roadmapReturnUrl,chapterWithContext,context};
 else root.GermanyRoadmapReturn={roadmapReturnUrl,chapterWithContext,context};
})(typeof window==='undefined'?globalThis:window);
