"""R37 unchanged deadline: isolated h5 full-direction method, THREE fixed period seeds."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
from math import gcd
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('base',R/'c1-critical-family-check.py');B=importlib.util.module_from_spec(sp);sp.loader.exec_module(B);g=B.g
sp=importlib.util.spec_from_file_location('frozen_orbit',R/'marked-origami-orbit-check.py');O=importlib.util.module_from_spec(sp);sp.loader.exec_module(O);O.deadline=B.deadline;O.build.deadline=B.deadline
rows=[];h=5;V=B.polygon(h);S=(Q(0),Q(2));T=(Q(0),Q(12));g.simple(V)
b=O.build.certify([tuple(map(int,z)) for z in V],tuple(map(int,S)),tuple(map(int,T)));result,_=O.orbit(O.encode(b),cap=50000)
if result['status']=='LIT':
 A=((1,0),(0,1));gens={'T':((1,1),(0,1)),'U':((1,0),(1,1))}
 for ch in result['word']:A=O.build.mul(gens[ch],A)
 d=(A[1][1],-A[1][0]);frame=b['source_root_matrix'];v=(frame[0][0]*d[0]+frame[1][0]*d[1],frame[0][1]*d[0]+frame[1][1]*d[1])
 path,why=B.trace(V,S,T,v);assert path is not None,why;witness=g.path_check(V,path)
 found={'velocity':v,'path':path,**witness};rows.append({'h':5,'method':'ISOLATED_FULL_ORBIT_FIRST_CANDIDATE','orbit_candidate':result,'first_path':found,'polygon':V,'source':S,'target':T})
else:rows.append({'h':5,'method':'ISOLATED_FULL_ORBIT_FIRST_CANDIDATE','orbit_candidate':result,'first_path':None,'status':'UNDECIDED_NO_PATH','polygon':V,'source':S,'target':T})
if rows[0]['first_path']:
 for h in(7,9,11):
  B.deadline();V=B.polygon(h);g.simple(V);S=(Q(0),Q(2));T=(Q(0),Q(2*h+2));trials=[];found=None
  for p in range(1,36):
   if found:break
   for q in(1,3):
    if gcd(p,q)!=1:continue
    if found:break
    for sx,sy in((-1,1),(1,1),(-1,-1),(1,-1)):
     v=(Q(sx*p),Q(sy*q));path,why=B.trace(V,S,T,v);trials.append({'velocity':v,'result':why})
     if path:
      res=g.path_check(V,path);assert not any(g.on(a,b,T) for a,b in zip(path[:-2],path[1:-1]));found={'velocity':v,'path':path,**res};break
  rows.append({'h':h,'method':'PRESCRIBED_Q13_PERIOD_SEED','trials':trials,'first_path':found,'polygon':V,'source':S,'target':T,'status':'FIRST_ACTUAL_PATH_VERIFIED' if found else'UNDECIDED_PACK_EXHAUSTED'})
  if not found:break
out={'status':'ALL_FOUR_BASES_EXACTLY_LIT' if len(rows)==4 and all(r['first_path'] for r in rows) else'INCOMPLETE_NO_DARKNESS_INFERRED','rows':rows,'whole_goal_complete':False,'discovery':True,'original_deadline':B.end.isoformat(),'finished_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['c1-critical-family-check.py','c1-critical-q13-failure.json','marked-origami-builder-check.py','marked-origami-orbit-check.py','resumed-exact-check.py']}}
B.deadline();(R/'c1-critical-final-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('rows','source_sha256')}));print(json.dumps([{'h':r['h'],'method':r['method'],'trials':len(r.get('trials',[])),'orbit':r.get('orbit_candidate'),'witness':{k:v for k,v in r['first_path'].items() if k!='path'} if r['first_path'] else None} for r in rows],default=str))
