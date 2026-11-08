"""Independent prescribed geometry, six paths and all-n transfer controls; no search."""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'construction'
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def expected(h):
 return list(map(lambda z:tuple(map(Q,z)),[(0,0),(2,0),(2,1),(3,1),(3,3),(2,3),(2,2*h+1),(3,2*h+1),(3,2*h+3),(2,2*h+3),(2,2*h+4),(0,2*h+4),(0,h+6),(-1,h+6),(-1,h+4),(0,h+4),(0,h+2),(-1,h+2),(-1,h),(0,h)]))
def check(V,path,S,T):
 g.simple(V);assert len(V)==20 and path[0]==S and path[-1]==T
 assert abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in g.edges(V)))/2==4*(T[1]-2)/2+16
 As=[(Q(x),Q(y)) for x in range(0,4,2) for y in range(0,int(max(z[1] for z in V))+1,2) if g.location(V,(x,y))==1];assert set(As)=={S,T}
 assert not any(g.on(a,b,T) for a,b in zip(path[:-2],path[1:-1]))
 return g.path_check(V,path)
def insert(V,path,cut,H):
 def shifted(p):return(p[0],p[1]+(H if p[1]>cut else 0))
 out=[shifted(path[0])]
 for a,b in zip(path,path[1:]):
  assert cut not in(a[1],b[1])
  if min(a[1],b[1])<cut<max(a[1],b[1]):
   f=(cut-a[1])/(b[1]-a[1]);x=a[0]+f*(b[0]-a[0]);assert 0<x<2
   rate=(b[0]-a[0])/abs(b[1]-a[1]);assert (rate*H/4).denominator==1
   sign=1 if b[1]>a[1] else-1;start=cut+(H if sign<0 else 0);out.append((x,start));hits=[]
   for j in range(int(min(x,x+rate*H)//2)-1,int(max(x,x+rate*H)//2)+2):
    v=(2*j-x)/rate
    if 0<v<H:hits.append((v,(g.fold(Q(2*j),Q(2)),start+sign*v)))
   out.extend(z for _,z in sorted(hits));out.append((x,start+sign*H))
  out.append(shifted(b))
 return[shifted(z) for z in V],out

def cut(lo,hi,path):
 ys={p[1] for p in path}
 for d in range(2,100):
  c=lo+(hi-lo)/d
  if c not in ys:return c
 raise AssertionError('control cut selection')
raw=json.loads((P/'c2-critical-family-check.json').read_text());rows=[]
for r in raw['rows']:
 h=r['h'];V=expected(h);peerV=[tuple(map(Q,z)) for z in r['polygon']];g.simple(peerV)
 assert {frozenset(e) for e in g.edges(V)}=={frozenset(e) for e in g.edges(peerV)}
 path=[tuple(map(Q,z)) for z in r['actual']['path']];S=(Q(2),Q(2));T=(Q(2),Q(2*h+2));res=check(V,path,S,T)
 velocity=tuple(map(Q,r['actual']['direction']));assert abs(velocity[1])==3 and gcd(int(abs(velocity[0])),3)==1
 assert g.det(velocity,g.vec(path[0],path[1]))==0 and g.dot(velocity,g.vec(path[0],path[1]))>0
 assert res['reflections']==r['actual']['reflections']
 assert len(r['actual']['walls'])==len(path)-2
 for z,i in zip(path[1:-1],r['actual']['walls']):assert g.on(peerV[i],peerV[(i+1)%20],z)
 rows.append({'h':h,'n':0,**res})
 cuts=[cut(Q(3),Q(h),path),cut(Q(h+6),Q(2*h+1),path)]
 n=1;v,p=V,path;v,p=insert(v,p,cuts[0],Q(12*n));v,p=insert(v,p,cuts[1]+12*n,Q(12*n))
 assert {frozenset(e) for e in g.edges(v)}=={frozenset(e) for e in g.edges(expected(h+12*n))}
 result=check(v,p,S,(Q(2),Q(2*(h+12*n)+2)));rows.append({'h':h+12*n,'base_h':h,'n':n,**result})
# A40 stored path is exactly the first six-residue base's existing certificate.
a40=json.loads((P/'c2-four-corner-check.json').read_text());assert a40['actual']['path']==raw['rows'][0]['actual']['path']
out={'status':'ALL_SIX_BASES_AND_SIX_NONZERO_INSERTIONS_INDEPENDENTLY_PASS','rows':rows,'base_reflections':sum(r['reflections'] for r in rows if r['n']==0),'base_wall_leg_guards':sum(r['wall_leg_guards'] for r in rows if r['n']==0),'all_reflections':sum(r['reflections'] for r in rows),'all_wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'whole_goal_complete':False,'discovery':False,'source_sha256':{'../construction/c2-critical-family-check.json':hashlib.sha256((P/'c2-critical-family-check.json').read_bytes()).hexdigest(),'../construction/c2-four-corner-check.json':hashlib.sha256((P/'c2-four-corner-check.json').read_bytes()).hexdigest(),'resumed-exact-check.py':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest()}}
(R/'c2-critical-family-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in('rows','source_sha256')}))
