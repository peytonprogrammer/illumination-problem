"""One hand-prescribed floor replacement, exact path/guard identities; no search."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements
from boundary_replay import on,cross,sub,dot
rays=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
centers={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan(site,ss):
 a=centers[site] if isinstance(site,str) else site
 return {tuple(sorted((a,(a[0]+rays[i%8][0],a[1]+rays[i%8][1]),(a[0]+rays[(i+1)%8][0],a[1]+rays[(i+1)%8][1])))) for i in ss}
H=set().union(*(fan(a,range(8)) for a in [(0,0),(2,0),(2,2)]))
d=F(2,7)
assert F(3,11)<d<F(3,10)
P=[(F(0),F(0)),(2*d/(1+d),2/(1+d)),(F(0),2-2*d),(2*d/(1-d),2-2*d/(1-d)),(5*d,F(-1)),(9*d,F(3)),(14*d/(1+d),14*d/(1+d)-2),(F(1),13*d-2),(F(2),14*d-2)]
assert P[-1]==(2,2) and len(P)-2==7
assert 0<d<3*d<1 and 1<5*d<2 and 2<9*d<3
assert 1<12-3/d<2 and 3<P[6][0]<4 and 1<13*d-2<2
assert all(not on((2,2),a,b) for a,b in zip(P[:-2],P[1:-1]))
U,Z=path_requirements(P)
minimum=H|fan('N',[6])|fan('E',[3,4])
maximum=minimum|set().union(*(fan(k,range(8)) for k in ['L','B','R']))|fan('Tc',[4,5])|fan('D',[0,1,3,4,5,6,7])
assert U<=minimum and not Z&maximum
assert Z&fan('D',[2])
# Fixed finite mirror segments derived from the actual local geometry.
walls=[((0,2),(1,1)),((0,1),(0,2)),((0,2),(1,1)),((1,-1),(2,-1)),((2,3),(3,3)),((3,1),(4,2)),((1,1),(1,2))]
for prev,p,nxt,(a,b) in zip(P,P[1:],P[2:],walls):
 assert on(p,a,b) and p!=a and p!=b
 v=sub(p,prev);w=sub(b,a)
 reflected=tuple(2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
 assert cross(reflected,sub(nxt,p))==0 and dot(reflected,sub(nxt,p))>0
# Actual endpoint unfolding through these seven physical mirror lines.
q=P[-1]
for a,b in walls[::-1]:
 w=sub(b,a);v=sub(q,a)
 q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
assert q==(4,14)
assert cross(q,(2,7))==0
ur,zr=path_requirements(P[::-1]);assert ur==U and zr==Z
sigma=lambda p:(2-p[1],2-p[0])
transform=lambda ts:{tuple(sorted(sigma(v) for v in t)) for t in ts}
SP=[sigma(p) for p in P[::-1]]
us,zs=path_requirements(SP)
assert SP[0]==(0,0) and SP[-1]==(2,2) and us==transform(U) and zs==transform(Z)
# Exactly two predeclared b0 branch envelopes, no assembled room or census.
applications={}
for label,ss in [('Bwest',[1,2,3]),('Brectangle',[0,1,2,3])]:
 mi=minimum|fan('B',ss)|fan('L',[7,0])|fan('D',[1])|fan('Tc',[5])
 ma=mi|fan('R',range(8))
 assert U<=mi and not Z&ma
 applications[label]='WHOLE_SUPPORT_PASS_D1_N6_WITH_ARBITRARY_R'
receipt={'status':'HAND_SEVEN_PATH_AND_COMPLETE_SUPPORT_PASS','path':[[str(x) for x in p] for p in P],'reflections':7,'actual_unfolded_target':list(map(str,q)),'initial_direction':[2,7],'parameter':'2/7','strict_interval':['3/11','3/10'],'endpoint_equation':'14d-2=2','minimum':sorted(minimum),'maximum':sorted(maximum),'required':sorted(U),'forbidden':sorted(Z),'finite_mirrors':walls,'reverse_sigma':'PASS','applications':applications,'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),ROOT/'triangle-composition/inputs/guard_checker.py',ROOT/'triangle-composition/inputs/boundary_replay.py']},'limits':'One analytically prescribed composition only. No room construction, ray/direction/word discovery, archive, or whole polygon physical replay. Complete U/Z establishes finite first mirrors and strict interior in any valid room in envelope; independent review pending.'}
(HERE/'seven-path-floor-check.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: hand-derived seven reflections, all finite mirrors strict, complete U/Z, first actual T, reverse/sigma, unfold (4,14); two symbolic b0 D1 applications.')
