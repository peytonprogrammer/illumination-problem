"""Independent replay of four prescribed A51 formula certificates; no discovery."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'construction';s=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
a=json.loads((P/'common-depth-zigzag-check.json').read_text());rows=[]
for z in a['rows']:
 h,d=z['h'],z['d'];c,D=map(Q,(z['c'],z['D']));ws,wt,w1,w2=map(Q,z['widths']);upper=h+d+2 if z['case']=='A1' else h+4;G=2*h+(d if z['case']=='A1' else 0)+4
 V=[(0,0),(c,0),(c,1),(c+ws,1),(c+ws,3),(c,3),(c,2*h+1),(c+wt,2*h+1),(c+wt,2*h+3),(c,2*h+3),(c,G),(0,G),(0,upper+2),(-w2,upper+2),(-w2,upper),(0,upper),(0,h+2),(-w1,h+2),(-w1,h),(0,h)];V=[tuple(map(Q,p)) for p in V];g.simple(V)
 saved=[tuple(map(Q,p)) for p in z['polygon']];assert {frozenset(e) for e in g.edges(V)}=={frozenset(e) for e in g.edges(saved)}
 path=[tuple(map(Q,p)) for p in z['path']];assert path[0]==(c+D,2) and path[-1]==(c+D,2*h+2)
 assert not any(g.on(u,v,path[-1]) for u,v in zip(path[:-2],path[1:-1]))
 m,n=z['m'],z['n'];tau,delta=map(Q,(z['tau'],z['delta']));assert n==(D*h/(2*m*c)+Q(1,2))//1 and tau==(h+2*n)/(m*c+D) and delta==D*tau-2*n and abs(delta)<1
 vin=(-1,(-1)**n*tau);e=g.vec(path[0],path[1]);assert g.det(vin,e)==0 and g.dot(vin,e)>0
 res=g.path_check(V,path);assert res['reflections']==2*n+2*m-1
 for p,i in zip(path[1:-1],z['walls']):assert g.on(saved[i],saved[(i+1)%len(saved)],p)
 rows.append({'case':z['case'],'h':h,'d':d,'n':n,'m':m,**res})
out={'status':'FOUR_A51_FORMULAS_INDEPENDENTLY_PASS','rows':rows,'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'discovery':False,'whole_goal_complete':False,'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['../construction/common-depth-zigzag-check.json','resumed-exact-check.py']}}
(R/'common-depth-zigzag-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
