"""Batch97 rule-first candidate. Based on Batch96 engine, not 2025-certified.
For a sole ineligible leader, the next two standings positions are eligible representatives.
For ties involving an ineligible team, remove the ineligible team before tiebreaking.
"""
from collections import Counter,defaultdict
from fractions import Fraction
import importlib.util
from pathlib import Path
_spec=importlib.util.spec_from_file_location('batch97_base',Path(__file__).with_name('F26_Batch99_State_Machine_Selection_Engine_EXPERIMENTAL.py'))
_base=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_base)

def select(games,eligible=None,ratings=None,group_equal_pct=False):
    teams=sorted({t for a,b,_ in games for t in (a,b)})
    allowed=set(teams) if eligible is None else set(eligible)
    played=Counter();wins=Counter()
    for a,b,away_wins in games:
        played[a]+=1;played[b]+=1;wins[a if away_wins else b]+=1
    records={t:Fraction(wins[t],played[t]) for t in teams if played[t]}
    if not records:return {'finalists':[],'trace':[('eligibility','no games')],'resolved':False,'policy_flags':[]}
    high=max(records.values());leaders=sorted(t for t in records if records[t]==high)
    eligible_leaders=[t for t in leaders if t in allowed]
    flags=[]
    if len(leaders)==2 and len(eligible_leaders)==2:
        pair=frozenset(leaders)
        head=next((a if aw else b for a,b,aw in games if frozenset((a,b))==pair),None)
        ordered=([head]+[t for t in leaders if t!=head]) if head else leaders
        return {'finalists':ordered,'trace':[('DIRECT_TWO_WAY_FIRST',tuple(leaders),'head-to-head ranking' if head else 'seeding unresolved')],'resolved':True,'policy_flags':['SEEDING_UNRESOLVED'] if not head else []}
    if any(t not in allowed for t in leaders):flags.append('INELIGIBLE_LEADER_REMOVED')
    result=_base.select(games,eligible=allowed,ratings=ratings,group_equal_pct=group_equal_pct)
    result['trace']=[('ELIGIBILITY',tuple(leaders),tuple(eligible_leaders))]+result['trace']
    result['policy_flags']=flags
    return result
