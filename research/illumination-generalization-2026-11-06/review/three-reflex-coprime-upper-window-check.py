"""Independent CE08 open-window constructor; prescribed exact rays only."""
from pathlib import Path
from fractions import Fraction as Q
from math import floor,ceil
import json,hashlib
HERE=Path(__file__).parent
src=(HERE/'three-reflex-coprime-source-width-check.py').read_text().split('\nfixtures=')[0]
old='delta=gcd(P*C,N);Lam=lcm(P,N,K);assert delta<K and gcd(Lam*d2,L)==1'
new='delta=gcd(P*C,N);Lam=lcm(P,N,K);assert u>h and gcd(Lam*d2,L)==1'
assert src.count(old)==1;src=src.replace(old,new)
a=src.index('    good=[]');b=src.index('    k=floor(',a)
src=src[:a]+'''    B=s+C*(A+z-s)/D
    m=0 if q_fixed is not None else max(0,ceil((B+K*e-A)/(2*A)))
    lower=((2*m+1)*A-K*e-B)*D/(2*e*C)
    upper=((2*m+1)*A+K*e-B)*D/(2*e*C)
    q0=max(1,floor(lower)+1);choices=[q0,q0+1]
    assert all(lower<x<upper for x in choices)
    good=[q for q in choices if ((s+(D-d2)*(A+z-s+2*e*q)/D-A-K*e)/(2*e)).denominator!=1]
    assert good
    q=good[0] if q_fixed is None else q_fixed;assert q in good
    tau0=(A+z-s+2*e*q)/D;tau=tau0;n=0;z0=s;X0=s+C*tau;M=0
    z1=X0-(2*m+1)*A
''' +src[b:]
src=src.replace('cap_gcd=delta,slope=','cap_gcd=delta,cap_interval=(lower,upper),two_indices=choices,good_indices=good,slope=')
ns={'__file__':str(HERE/'three-reflex-coprime-source-width-check.py'),'__name__':'own_upper_window_constructor'}
exec(compile(src,'<independent-upper-window>','exec'),ns)
fixtures=[
 ('CE08-nominated',4,1,3,4,9,1,3,6,10,(2,8),(28,2),1),
 ('CE08-integral-open-endpoint',4,1,3,4,9,1,3,6,10,(3,8),(34,2),1),
 ('CE08-first-index-bad',4,1,3,4,9,1,3,6,10,(2,8),(Q(242,9),2),2)]
rows=[ns['ray'](*f) for f in fixtures]
assert (rows[0]['slope'],rows[0]['finalJ'])==(221,28)
assert rows[1]['cap_interval'][0]==0
assert rows[2]['two_indices']==[1,2] and rows[2]['good_indices']==[2]
# Independently replay the known singular final slope, bypassing selector only.
Pgon=[(4,1),(4,5),(12,5),(12,4),(8,4),(8,0),(20,0),(20,7),(0,7),(0,1)]
assert ns['ns']['fold'](Q(2)+2*Q(18),Q(20))==2
suffix=ns['replay'](Pgon,(Q(2),Q(6)),(Q(10),Q(2)),Q(18),Q(4),(-Q(18),-Q(1)),0)
rows.append(dict(label='known-singular-S-return-suffix',slope=18,singular_prefix_discarded=True,**suffix))
request=HERE.parent/'construction/three-reflex-coprime-extension-upperwindow-review-request.json'
files=sorted((HERE.parent/'construction').glob('three-reflex-coprime-extension-upperwindow-*'))
pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files]
out=dict(status='PASS_INDEPENDENT_UPPER_WINDOW_PREREQUISITE',request_present=request.exists(),author_snapshot_at_end=pins,rows=rows,cases=len(rows),reflections=sum(x['reflections'] for x in rows),wall_leg_guards=sum(x['wall_leg_guards'] for x in rows),author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('rows','author_snapshot_at_end')}))
