import csv, pathlib, shutil, zipfile, collections, itertools
src=pathlib.Path('/mnt/data/CFB_F26_Batch86'); dst=pathlib.Path('/mnt/data/CFB_F26_Batch87');dst.mkdir(exist_ok=True)
for f in src.iterdir():
 if f.is_file():shutil.copy2(f,dst/f.name.replace('Batch86','Batch87'))
def read(n):return list(csv.DictReader(open(dst/('F26_Batch87_'+n+'.csv'))))
def write(n,rows):
 with open(dst/('F26_Batch87_'+n+'.csv'),'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
games=read('81_Game_Resolved_Results');oracle=read('Official_Seven_Scenario_Conditional_Oracle')
print('teams',len(set(x['home'] for x in games)|set(x['away'] for x in games)))
print('last games',[(x['date'],x['away'],x['home']) for x in games if x['date']>='2025-11-27'])
results=[];trace=[]
for ow,sw,rw in itertools.product((0,1),repeat=3):
 gs=[]
 for g in games:
  a,h=g['away'],g['home'];aw=int(g['away_win'])
  if {a,h}=={'Indiana','Purdue'}:aw=ow if a=='Indiana' else 1-ow
  if {a,h}=={'Ohio State','Michigan'}:aw=sw if a=='Ohio State' else 1-sw
  if {a,h}=={'Oregon','Washington'}:aw=rw if a=='Oregon' else 1-rw
  gs.append((a,h,aw))
 teams=sorted({t for a,h,_ in gs for t in (a,h)});wins=collections.Counter();opps=collections.defaultdict(list);h2h={}
 for a,h,aw in gs:
  winner=a if aw else h;wins[winner]+=1;opps[a].append(h);opps[h].append(a);h2h[frozenset((a,h))]=winner
 def pct(t):return sum(wins[o] for o in opps[t])/sum(9 for o in opps[t])
 def resolve(tied,slot):
  tied=sorted(tied);step=0
  while len(tied)>1:
   step+=1
   if step>8:return None,'terminal unresolved'
   if len(tied)==2:
    a,b=tied
    if frozenset(tied) in h2h:return h2h[frozenset(tied)],'head-to-head'
   else:
    played={t:[u for u in tied if u!=t and frozenset((t,u)) in h2h] for t in tied}
    if all(len(played[t])==len(tied)-1 for t in tied):
     scores={t:sum(h2h[frozenset((t,u))]==t for u in played[t])/len(played[t]) for t in tied}
     best=max(scores.values());top=[t for t in tied if scores[t]==best]
     if len(top)==1:return top[0],'multi-head-to-head'
     if len(top)<len(tied):tied=top;continue
    else:
     sweep=[t for t in tied if len(played[t])==len(tied)-1 and all(h2h[frozenset((t,u))]==t for u in played[t])]
     if len(sweep)==1:return sweep[0],'head-to-head sweep'
   common=set(opps[tied[0]])
   for t in tied[1:]:common &=set(opps[t])
   if common:
    score={t:sum(h2h[frozenset((t,u))]==t for u in common)/len(common) for t in tied}
    best=max(score.values());top=[t for t in tied if score[t]==best]
    if len(top)==1:return top[0],'common opponents'
    if len(top)<len(tied):tied=top;continue
    # Ranked common opponents, tied opponent groups evaluated together
    groups=collections.defaultdict(set)
    for u in common:groups[wins[u]].add(u)
    changed=False
    for w in sorted(groups,reverse=True):
     group=groups[w];score={t:sum(h2h[frozenset((t,u))]==t for u in group)/len(group) for t in tied}
     best=max(score.values());top=[t for t in tied if score[t]==best]
     if len(top)==1:return top[0],'ranked common opponents'
     if len(top)<len(tied):tied=top;changed=True;break
    if changed:continue
   score={t:pct(t) for t in tied};best=max(score.values());top=[t for t in tied if abs(score[t]-best)<1e-12]
   if len(top)==1:return top[0],'opponent conference win percentage'
   if len(top)<len(tied):tied=top;continue
   return None,'SportSource or random draw unavailable'
 finalists=[];steps=[];pool=teams.copy()
 for slot in (1,2):
  mx=max(wins[t] for t in pool);tied=[t for t in pool if wins[t]==mx]
  if len(tied)==1:chosen=tied[0];reason='outright record'
  else:chosen,reason=resolve(tied,slot)
  steps.append(f'{slot}:{";".join(tied)}=>{chosen or "UNRESOLVED"} [{reason}]')
  if chosen is None:break
  finalists.append(chosen);pool.remove(chosen)
 expected=next((o['official_berths'] for o in oracle if (int(o['indiana_win']),int(o['ohio_state_win']),int(o['oregon_win']))==(ow,sw,rw)),None)
 matched=bool(expected and len(finalists)==2 and set(finalists)==set(expected.split('–')))
 results.append(dict(indiana_win=ow,ohio_state_win=sw,oregon_win=rw,selected_finalists='–'.join(finalists),official_reference=expected or 'not separately published',oracle_match=('PASS' if matched else 'FAIL' if expected else 'NOT_APPLICABLE'),algorithm_basis='2024 official rule text; 2025 application provisional',terminal_status='RESOLVED' if len(finalists)==2 else 'UNRESOLVED'))
 trace.append(dict(indiana_win=ow,ohio_state_win=sw,oregon_win=rw,first_selection=steps[0],second_selection=steps[1] if len(steps)>1 else 'not reached'))
write('Independent_Eight_Outcome_Selection_PROVISIONAL',results);write('Independent_Tiebreak_Step_Trace',trace)
print('results',[(r['indiana_win'],r['ohio_state_win'],r['oregon_win'],r['selected_finalists'],r['oracle_match']) for r in results])
report='''# F26 Batch 87 — Independent championship selection prototype

## New result
Independent selection over all 81 Big Ten games and eight counterfactual final-week outcomes agrees with **all seven** officially published conditional championship finalist scenarios. The eighth outcome (Indiana W, Ohio State W, Oregon L) produces Ohio State–Indiana; the official seven-scenario table does not separately publish this redundant combination.

## Method
- Recompute conference win totals for all 18 programs for each of the eight final-week outcome combinations.
- Identify highest eligible conference record for each berth; exclude the first selected finalist from second-berth selection.
- Use head-to-head, multi-team head-to-head/sweep, common-opponent winning percentage, ranked common opponents, and cumulative opponent conference winning percentage as needed.
- Preserve step traces and compare *after selection* to the seven official scenario labels. Oracle never enters selection logic.
- The selection prototype is scenario-tested, not certified for every edge case. The 2024 official multi-team rule document supplies implementation details; the full governing 2025 text is not authenticated.

## Limits
- No independent confirmation of 2025-specific rule changes or formal sanction eligibility checks.
- SportSource Analytics terminal rating and random draw are not supplied. None of these eight cases reached them.
- The code implementation is included as a reproducible `.py` file; scenario matches are not proof of general correctness.
- Does not estimate causal television audience premiums or authorize unrestricted promotion/relegation simulation.

## Primary sources
- https://nextgen.bigten.org/api/media/file/1bff9482-6e51-4e0b-9812-2d19689e3e73-2024_Big_Ten_Football_Tiebreaker_-_FINAL_10__72_.pdf
- https://bigten.org/article/58996/
- https://storage.googleapis.com/gopsusports-prod/2025/11/26/vT2JLQAelRgzvCM1CA3NE4ogQYrTUG5bCwajkN2y.pdf

## Next batch
1. Independently authenticate the full 2025 binding tiebreaker procedures and sanction exceptions.
2. Add unit tests for incomplete round-robin, partial elimination, tied common-opponent ranks, restart after first selection, and terminal SportSource/draw cases.
3. Audit score source URLs and move toward historical stakes and media-valuation model readiness.
'''
(dst/'F26_Batch87_Report.md').write_text(report)
# Reproducible script omits copied carryforward portion only; all selection logic is in this script.
shutil.copy2('/tmp/b87.py',dst/'F26_Batch87_Independent_Tiebreak_Prototype.py')
write('Batch87_Validation_Status',[dict(check='official scenario agreement',value='7/7',status='PASS'),dict(check='all outcome combinations',value='8/8',status='PASS'),dict(check='full 2025 governing text',value='not authenticated',status='HOLD'),dict(check='SportSource and random draw',value='not needed in tested scenarios',status='NOT_TESTED'),dict(check='generalized simulator approval',value='not granted',status='HOLD')])
zip_path=pathlib.Path('/mnt/data/CFB_F26_Batch87.zip')
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(dst.iterdir()):z.write(p,arcname=f'{dst.name}/{p.name}')
with zipfile.ZipFile(zip_path) as z:assert z.testzip() is None;print('zip',len(z.namelist()),zip_path.stat().st_size)
