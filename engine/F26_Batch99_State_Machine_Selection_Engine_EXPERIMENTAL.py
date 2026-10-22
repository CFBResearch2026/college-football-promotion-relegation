"""F26 Batch95: experimental 2024-reference state-machine tiebreaker. NOT binding 2025 certification."""
from collections import Counter,defaultdict
from fractions import Fraction

def transition(candidates,scores,slot,head_to_head=None):
    """Rule-based state transition. Return action, remaining, selected; pure and independently testable."""
    top=tuple(sorted(t for t in candidates if scores[t]==max(scores.values())))
    if len(top)==len(candidates):return 'NEXT_STEP',top,()
    if len(top)==1:return 'SELECT',top,top
    if slot==1 and len(top)==2:return 'SELECT_BOTH',top,top
    if len(top)==2:
        if head_to_head is not None:return 'SELECT_H2H',top,(head_to_head,)
        return 'TWO_TEAM_RULES',top,()
    return 'NEXT_STEP',top,()

def select(games,eligible=None,ratings=None,group_equal_pct=False):
    teams=sorted({t for a,h,w in games for t in (a,h)})
    eligible=set(teams) if eligible is None else set(eligible)
    wins=Counter();played=defaultdict(list);h2h={}
    for a,h,aw in games:
        if a==h or frozenset((a,h)) in h2h:raise ValueError('duplicate or self game')
        winner=a if aw else h;wins[winner]+=1;played[a].append(h);played[h].append(a);h2h[frozenset((a,h))]=winner
    trace=[]
    def pct(t):return Fraction(wins[t],len(played[t])) if played[t] else Fraction(-1)
    def record(t,ops):return Fraction(sum(h2h[frozenset((t,o))]==t for o in ops),len(ops))
    def opp_pct(t):
        den=sum(len(played[o]) for o in played[t]);return Fraction(sum(wins[o] for o in played[t]),den) if den else None
    def solve(tied,slot,initial_step=0):
        tied=tuple(sorted(tied));step=initial_step;guard=0
        while len(tied)>1 and guard<30:
            guard+=1
            if len(tied)==2:
                pair=frozenset(tied)
                if step<=0 and pair in h2h:return (h2h[pair],),'two-team H2H'
                # With no head-to-head, start at common-opponent rule.
                if step==0:step=1
            if step==0 and len(tied)>2:
                head={t:[u for u in tied if u!=t and frozenset((t,u)) in h2h] for t in tied}
                if all(len(head[t])==len(tied)-1 for t in tied):
                    scores={t:record(t,head[t]) for t in tied}
                    action,top,selected=transition(tied,scores,slot, h2h.get(frozenset(top)) if False else None)
                    trace.append((slot,'multi H2H',tied,action,top))
                    if selected:return selected,'multi H2H '+action
                    if action=='TWO_TEAM_RULES':return solve(top,slot,0)
                    tied=top
                else:
                    sweep=[t for t in tied if len(head[t])==len(tied)-1 and all(h2h[frozenset((t,u))]==t for u in head[t])]
                    if len(sweep)==1:
                        trace.append((slot,'sweep restart',tied,sweep[0]))
                        return (sweep[0],),'multi-team sweep'
                step=1;continue
            if step==1:
                common=set(played[tied[0]])
                for t in tied[1:]:common.intersection_update(played[t])
                common.difference_update(tied)
                if common:
                    scores={t:record(t,common) for t in tied}
                    action,top,selected=transition(tied,scores,slot,h2h.get(frozenset(top)) if False else None)
                    trace.append((slot,'common opponents',tied,action,top))
                    if selected:return selected,'common opponents '+action
                    if action=='TWO_TEAM_RULES':return solve(top,slot,0)
                    tied=top
                step=2;continue
            if step==2:
                common=set(played[tied[0]])
                for t in tied[1:]:common.intersection_update(played[t])
                common.difference_update(tied)
                groups=defaultdict(set)
                for o in common:
                    key=Fraction(wins[o],len(played[o])) if group_equal_pct else (wins[o],len(played[o]))
                    groups[key].add(o)
                keys=sorted(groups,key=lambda k:k if group_equal_pct else Fraction(*k),reverse=True)
                moved=False
                for key in keys:
                    scores={t:record(t,groups[key]) for t in tied}
                    action,top,selected=transition(tied,scores,slot)
                    trace.append((slot,'ranked opponents',tied,action,top))
                    if selected:return selected,'ranked opponents '+action
                    if action=='TWO_TEAM_RULES':return solve(top,slot,0)
                    if len(top)<len(tied):tied=top
                step=3;continue
            if step==3:
                vals={t:opp_pct(t) for t in tied}
                if all(v is not None for v in vals.values()):
                    action,top,selected=transition(tied,vals,slot)
                    trace.append((slot,'opponent pct',tied,action,top))
                    if selected:return selected,'opponent pct '+action
                    if action=='TWO_TEAM_RULES':return solve(top,slot,0)
                    tied=top
                step=4;continue
            if step==4:
                if ratings and all(t in ratings for t in tied):
                    action,top,selected=transition(tied,{t:ratings[t] for t in tied},slot)
                    trace.append((slot,'rating',tied,action,top))
                    if selected:return selected,'supplied rating '+action
                    if action=='TWO_TEAM_RULES':return solve(top,slot,0)
                    tied=top
                return (), 'UNRESOLVED: SportSource rating/draw unavailable'
        return ((tied[0],),'only remaining') if len(tied)==1 else ((),'UNRESOLVED: loop guard')
    finalists=[]
    for slot in (1,2):
        if len(finalists)==2:break
        pool=[t for t in teams if t in eligible and t not in finalists and played[t]]
        if not pool:break
        high=max(pct(t) for t in pool);tied=[t for t in pool if pct(t)==high]
        selected,reason=((tied[0],),'outright record') if len(tied)==1 else solve(tied,slot)
        trace.append((slot,'selection',tuple(tied),selected,reason))
        if not selected:break
        finalists.extend(selected[:2-len(finalists)])
    return {'finalists':finalists,'trace':trace,'resolved':len(finalists)==2}
