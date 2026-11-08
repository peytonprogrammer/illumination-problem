"""R38 exact first witnesses for ONLY accepted B/C1/C2 finite proof bases."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
from math import gcd
import importlib.util,json,signal,hashlib
R=Path(__file__).resolve().parent
end=datetime.fromisoformat(json.loads((R/'c2-BC-closure-effort.json').read_text())['deadline_utc'])
def deadline():assert datetime.now(timezone.utc)<end
sp=importlib.util.spec_from_file_location('own_trace',R/'c1-critical-family-check.py');B=importlib.util.module_from_spec(sp);sp.loader.exec_module(B);B.deadline=deadline;g=B.g
signal.setitimer(signal.ITIMER_REAL,max(.001,(end-datetime.now(timezone.utc)).total_seconds()))
sp=importlib.util.spec_from_file_location('frozen_orbit',R/'marked-origami-orbit-check.py');O=importlib.util.module_from_spec(sp);sp.loader.exec_module(O);O.deadline=deadline;O.build.deadline=deadline

def room(family,r=0):
 if family=='B':G=8;s=2;t=6;left=[(0,2),(4,6)]
 else:
  G=(10 if family=='C1' else 12)+4*r;mu=G//2-(family=='C1');s=mu-2;t=mu+2;left=[(0,2),(mu,mu+2),(G-2,G)]
 right=[(s-1,s+1),(t-1,t+1)];cells={(x,y) for x in(0,1) for y in range(G)}
 cells|={(-1,y) for a,b in left for y in range(a,b)};cells|={(2,y) for a,b in right for y in range(a,b)}
 boundary=set()
 for x,y in cells:
  corners=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
  for a,b in g.edges(corners):
   if (b,a)in boundary:boundary.remove((b,a))
   else:boundary.add((a,b))
 out={}
 for a,b in boundary:assert a not in out;out[a]=b
 p=[min(out)];v=out[p[0]]
 while v!=p[0]:p.append(v);v=out[v]
 assert len(p)==len(boundary)
 p=[z for i,z in enumerate(p) if g.det(g.vec(p[i-1],z),g.vec(z,p[(i+1)%len(p)]))!=0];g.simple(p);p=[tuple(map(Q,z))for z in p]
 assert len(p)==(18 if family=='B' else 20)
 assert abs(sum(g.det(a,b)for a,b in g.edges(p)))/2==len(cells)
 S=(Q(2),Q(s));T=(Q(2),Q(t));A=[(Q(x),Q(y))for x in(0,2)for y in range(0,G+1,2)if g.location(p,(x,y))==1];assert set(A)=={S,T}
 for z in(S,T):assert all((int(z[0])+dx,int(z[1])+dy)in cells for dx in(-1,0)for dy in(-1,0))
 return p,S,T,{'G':G,'left':left,'right':right,'area':len(cells),'actual_A_count':len(A)}

def orbit_prefix(family):
 V,S,T,geom=room(family);b=O.build.certify([tuple(map(int,z))for z in V],tuple(map(int,S)),tuple(map(int,T)));result,_=O.orbit(O.encode(b),cap=50000);found=None
 if result['status']=='LIT':
  A=((1,0),(0,1));gens={'T':((1,1),(0,1)),'U':((1,0),(1,1))}
  for ch in result['word']:A=O.build.mul(gens[ch],A)
  d=(A[1][1],-A[1][0]);fr=b['source_root_matrix'];v=(fr[0][0]*d[0]+fr[1][0]*d[1],fr[0][1]*d[0]+fr[1][1]*d[1]);path,reason=B.trace(V,S,T,v);assert path,reason
  found={'velocity':v,'path':path,**g.path_check(V,path)}
 return {'family':family,'r':0,'isolated':True,'polygon':V,'source':S,'target':T,**geom,'orbit':result,'first_path':found}
rows=[orbit_prefix('B'),orbit_prefix('C1')]
for family,bases in(('C1',range(1,7)),('C2',range(6))):
 for r in bases:
  deadline();V,S,T,geom=room(family,r);found=None;trials=[]
  for p in range(1,36):
   if found:break
   for q in(1,3):
    if found:break
    if gcd(p,q)!=1:continue
    for sx,sy in((-1,1),(1,1),(-1,-1),(1,-1)):
     v=(Q(sx*p),Q(sy*q));path,reason=B.trace(V,S,T,v);trials.append({'velocity':v,'status':reason})
     if path:
      result=g.path_check(V,path);assert not any(g.on(a,b,T)for a,b in zip(path[:-2],path[1:-1]));found={'velocity':v,'path':path,**result};break
  rows.append({'family':family,'r':r,'isolated':False,'polygon':V,'source':S,'target':T,**geom,'trials':trials,'first_path':found})
  if not found:break
status={}
for f,need in(('B',1),('C1',7),('C2',6)):
 a=[r for r in rows if r['family']==f];status[f]='ALL_REQUIRED_EXACT_SEEDS_PASS' if len(a)==need and all(r['first_path']for r in a)else'INCOMPLETE_NO_DARKNESS_INFERRED'
out={'status':'FINITE_PROOF_BASE_DISCOVERY_TERMINAL','families':status,'rows':rows,'whole_goal_complete':False,'discovery':True,'original_deadline':end.isoformat(),'finished_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest()for f in ['c1-critical-family-check.py','marked-origami-orbit-check.py','marked-origami-builder-check.py','resumed-exact-check.py']}}
deadline();(R/'c2-BC-closure-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items()if k not in('rows','source_sha256')}));print(json.dumps([{'family':r['family'],'r':r['r'],'trials':len(r.get('trials',[])),'orbit':r.get('orbit'),'witness':{k:v for k,v in r['first_path'].items()if k!='path'}if r['first_path']else None}for r in rows],default=str))
