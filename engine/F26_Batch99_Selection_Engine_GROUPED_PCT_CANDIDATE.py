"""Import-safe Big Ten 2024-rule-based experimental selection engine. NOT certified 2025 policy."""
from collections import Counter,defaultdict

def select(games, eligible=None, ratings=None):
    teams=sorted({t for a,h,w in games for t in (a,h)})
    eligible=set(teams) if eligible is None else set(eligible)
    wins=Counter(); played=defaultdict(list); h2h={}
    for a,h,away_wins in games:
        if a==h or frozenset((a,h)) in h2h: raise ValueError('duplicate or self game')
        winner=a if away_wins else h
        wins[winner]+=1;played[a].append(h);played[h].append(a);h2h[frozenset((a,h))]=winner
    trace=[]
    def record(team,opponents):
        return sum(h2h[frozenset((team,o))]==team for o in opponents)/len(opponents)
    def opponent_pct(team):
        opponents=played[team]
        return sum(wins[o] for o in opponents)/sum(len(played[o]) for o in opponents) if opponents else None
    def resolve(tied,slot):
        tied=sorted(tied)
        while len(tied)>1:
            if len(tied)==2 and frozenset(tied) in h2h:
                return h2h[frozenset(tied)],'two-team head-to-head'
            if len(tied)>2:
                head={t:[u for u in tied if u!=t and frozenset((t,u)) in h2h] for t in tied}
                if all(len(head[t])==len(tied)-1 for t in tied):
                    scores={t:record(t,head[t]) for t in tied}
                    high=max(scores.values());top=[t for t in tied if scores[t]==high]
                    if len(top)==1:return top[0],'multi-team round robin'
                    if len(top)<len(tied):
                        trace.append((slot,'partial elimination',tuple(tied),tuple(top)))
                        tied=top;continue
                else:
                    sweep=[t for t in tied if len(head[t])==len(tied)-1 and all(h2h[frozenset((t,u))]==t for u in head[t])]
                    if len(sweep)==1:return sweep[0],'multi-team sweep'
            common=set(played[tied[0]])
            for t in tied[1:]:common.intersection_update(played[t])
            common.difference_update(tied)
            if common:
                scores={t:record(t,common) for t in tied}
                high=max(scores.values());top=[t for t in tied if scores[t]==high]
                if len(top)==1:return top[0],'all common opponents'
                if len(top)<len(tied):
                    trace.append((slot,'partial elimination',tuple(tied),tuple(top)))
                    tied=top;continue
                grouped=defaultdict(set)
                for o in common:grouped[(wins[o]/len(played[o]) if played[o] else -1)].add(o)
                changed=False
                for key in sorted(grouped,key=lambda k:k,reverse=True):
                    scores={t:record(t,grouped[key]) for t in tied}
                    high=max(scores.values());top=[t for t in tied if scores[t]==high]
                    if len(top)==1:return top[0],'ranked common opponents'
                    if len(top)<len(tied):
                        trace.append((slot,'partial elimination',tuple(tied),tuple(top)))
                        tied=top;changed=True;break
                if changed:continue
            pcts={t:opponent_pct(t) for t in tied}
            if all(p is not None for p in pcts.values()):
                high=max(pcts.values());top=[t for t in tied if abs(pcts[t]-high)<1e-12]
                if len(top)==1:return top[0],'opponent winning percentage'
                if len(top)<len(tied):
                    trace.append((slot,'partial elimination',tuple(tied),tuple(top)))
                    tied=top;continue
            if ratings and all(t in ratings for t in tied):
                high=max(ratings[t] for t in tied);top=[t for t in tied if ratings[t]==high]
                if len(top)==1:return top[0],'SportSource rating (supplied)'
            return None,'UNRESOLVED: rating or commissioner draw required'
        return tied[0],'only remaining team'
    finalists=[]
    for slot in (1,2):
        pool=[t for t in teams if t in eligible and t not in finalists]
        if not pool:break
        high=max(wins[t]/len(played[t]) if played[t] else -1 for t in pool)
        tied=[t for t in pool if played[t] and wins[t]/len(played[t])==high]
        if not tied:break
        chosen,reason=(tied[0],'outright record') if len(tied)==1 else resolve(tied,slot)
        trace.append((slot,reason,tuple(tied),chosen))
        if chosen is None:break
        finalists.append(chosen)
    return {'finalists':finalists,'trace':trace,'resolved':len(finalists)==2}
