"""Independent prescribed six A52 certificates; no author code execution or discovery."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'construction';sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
a=json.loads((P/'small-depth-far-repair-check.json').read_text());rows=[]
for z in a['rows']:
 p,q=z['original_depths'];w=z['w'];h=z['h'];label=z['chart'];assert p in(0,1,2) and q==p+2 and w>q and z['virtual_target_depth']==2*w-q
 s=6;t=s+2*h;G=2*h+18;ell={'mean':h+6,'bottom':h,'top':G-h}[label];left=[(ell,ell+2),(ell+4,ell+6)] if label!='top' else[(ell-4,ell-2),(ell,ell+2)]
 V=[(0,0),(1,0),(1,s-1),(p+2,s-1),(p+2,s+1),(1,s+1),(1,t-1),(1+w,t-1),(1+w,t+1),(1,t+1),(1,G),(0,G)]
 for l,u in sorted(left,reverse=True):V.extend([(0,u),(-2,u),(-2,l),(0,l)])
 shift=0 if (1+p)%2==0 else 1;V=[(Q(x+shift),Q(y)) for x,y in V];g.simple(V)
 saved=[tuple(map(Q,v)) for v in z['polygon']];assert {frozenset(e) for e in g.edges(V)}=={frozenset(e) for e in g.edges(saved)}
 path=[tuple(map(Q,v)) for v in z['path']];S=(Q(1+p+shift),Q(s));T=(Q(1+q+shift),Q(t));assert path[0]==S and path[-1]==T
 assert all(int(x)%2==int(y)%2==0 for x,y in(S,T)) and not any(g.on(u,v,T) for u,v in zip(path[:-2],path[1:-1]))
 tau=Q(z['tau']);N=w*tau;assert N.denominator==1 and Q(z['N'])==N and Q(z['farphase'])==(w-q)*tau
 far=(w-q)*tau;assert not(far.denominator==1 and far.numerator%2)
 res=g.path_check(V,path);assert res['reflections']==z['reflections'] and res['wall_leg_guards']==z['wall_leg_guards']
 rows.append({'depths':[p,q],'w':w,'h':h,'chart':label,**res})
assert len(rows)==6
out={'status':'A52_SIX_ACTUAL_CERTIFICATES_INDEPENDENTLY_PASS','rows':rows,'reflections':sum(z['reflections'] for z in rows),'wall_leg_guards':sum(z['wall_leg_guards'] for z in rows),'discovery':False,'whole_goal_complete':False,'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['../construction/small-depth-far-repair-check.json','resumed-exact-check.py']}}
(R/'small-depth-far-repair-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
