"""Two normal-square substitutions on supplied fixed paths; no discovery."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements,incident
from boundary_replay import cross,sub,dot,on
source=HERE/'joined-four-check.json';old=json.loads(source.read_text())
rays=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
centers={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan(site,ss):
 a=centers[site] if isinstance(site,str) else site
 return {tuple(sorted((a,(a[0]+rays[i%8][0],a[1]+rays[i%8][1]),(a[0]+rays[(i+1)%8][0],a[1]+rays[(i+1)%8][1])))) for i in ss}
H=set().union(*(fan(a,range(8)) for a in [(0,0),(2,0),(2,2)]))
O4=fan('B',[6,7,0,1]);allD=fan('D',range(8))
fullrest=set().union(*(fan(k,range(8)) for k in ['L','R','E','N']))
sigma=lambda p:(2-p[1],2-p[0]);tr=lambda ts:{tuple(sorted(sigma(v) for v in t)) for t in ts}
answers={}
for name,record,d in [('two',old,F(1,5)),('four',old['six_path_complement'],F(1,6))]:
 before=[tuple(F(x) for x in p) for p in record['path']]
 assert 0<2*d<4*d<1
 # Actual same inlet and outlet, opposite initial/final normal velocity.
 inlet=(2*d,F(-2));bottom=(3*d,F(-3));outlet=(4*d,F(-2))
 assert cross(sub(bottom,inlet),(d,-1))==0 and cross(sub(outlet,bottom),(d,1))==0
 assert 0<bottom[0]<1
 P=[before[0],bottom]+before[4:]
 assert P[0]==(0,0) and P[-1]==(2,2)
 assert all(not on((2,2),a,b) for a,b in zip(P[:-2],P[1:-1]))
 u,z=path_requirements(P)
 if name=='two':
  mi=H|O4|fan('D',[2,3]);ma=mi|allD|fullrest|fan('Tc',[0,1,2,3,4,6,7])
  walls=[((0,-3),(1,-3)),((1,3),(2,3))]
  assert on((1,-1),P[1],P[2]) and incident((F(1),F(-1)))<=mi
  assert not incident((F(1),F(-1))) <= (mi-fan('D',[2]))
 else:
  mi=H|O4|fan('Tc',[5]);ma=mi|allD|fullrest|fan('Tc',[0,1,2,3,5,7])
  walls=[((0,-3),(1,-3)),((1,3),(2,4)),((2,3),(2,4)),((1,3),(2,4))]
 assert u<=mi and not z&ma
 for a,p,b,(c,e) in zip(P,P[1:],P[2:],walls):
  assert on(p,c,e) and p not in (c,e)
  v=sub(p,a);w=sub(e,c)
  rv=tuple(2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
  assert cross(rv,sub(b,p))==0 and dot(rv,sub(b,p))>0
 ur,zr=path_requirements(P[::-1]);assert ur==u and zr==z
 us,zs=path_requirements([sigma(p) for p in P[::-1]]);assert us==tr(u) and zs==tr(z)
 q=P[-1]
 for a,b in walls[::-1]:
  w=sub(b,a);v=sub(q,a);q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
 assert q==(2,-10 if name=='two' else -12)
 answers[name]={'path':[[str(x) for x in p] for p in P],'reflections':len(P)-2,'minimum':sorted(mi),'maximum':sorted(ma),'required':sorted(u),'forbidden':sorted(z),'actual_unfolded_target':list(map(str,q)),'parameter':str(d),'normal_square_exchange':'SAME_ENTRY_EXIT_VELOCITY_PASS','finitewalls_firstT_reverse_sigma':'PASS','D_support':'all D allowed in maximum'}
result={'status':'O4_NORMAL_SQUARE_TWO_FOUR_PASS','paths':answers,'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,Path(__file__),ROOT/'triangle-composition/inputs/guard_checker.py',ROOT/'triangle-composition/inputs/boundary_replay.py']},'limits':'Two declared substitutions only; no new room or direction/path search. Two needs joinedD23, four permits allD incl singleleaf3/4. Whole joined Tcordinary split; independent review pending.'}
(HERE/'joined-square-check.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: O4 exact normal-square exchange; TWO if Tc5 absent with D23, FOUR for ordinary Tc5 with ALL D support; fullU-Z/strictfinitewalls/actualT/reverse/sigma.')
