"""Exact physical and whole-family verification of ONE frozen two-bounce path."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
import illumination_geometry as g
from boundary_replay import replay,on,sub,dot,cross
from guard_checker import path_requirements
raw=json.loads((HERE/'room.json').read_text());r=json.loads((HERE/'result.json').read_text())
assert r['status']=='FOUND_EXACT_PATH_PENDING_INDEPENDENT_VERIFICATION'
assert hashlib.sha256((HERE/'room.json').read_bytes()).hexdigest()==r['room_sha256']
assert hashlib.sha256((HERE/'search.py').read_bytes()).hexdigest()==r['search_source_sha256']
P=[tuple(F(*x) for x in p) for p in r['candidate']['path']]
assert P==[(F(0),F(0)),(F(-1),F(-3,2)),(F(-2,3),F(-2)),(F(2),F(2))]
room={tuple(sorted(map(tuple,t))) for t in raw['triangles']};V=list(map(tuple,raw['vertices']))
geo=g.check({'triangles':sorted(room),'marked':[(0,0),(2,2)],'require_simple':True},strict=False)
assert geo['simple_polygon'] and geo['walls']==20 and set(geo['interior_A'])=={(0,0),(2,0),(2,2)}
assert replay(V,(0,0),(2,2),P)==2
assert replay(V,(2,2),(0,0),P[::-1])==2
sigma=lambda p:(2-p[1],2-p[0])
SP=[sigma(p) for p in P[::-1]]
assert replay([sigma(p) for p in V],(0,0),(2,2),SP)==2
U,Z=path_requirements(P);assert U<=room and not Z&room
rays=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
centers={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan(site,ss):
 a=centers[site] if isinstance(site,str) else site
 return {tuple(sorted((a,(a[0]+rays[i%8][0],a[1]+rays[i%8][1]),(a[0]+rays[(i+1)%8][0],a[1]+rays[(i+1)%8][1])))) for i in ss}
H=set().union(*(fan(a,range(8)) for a in [(0,0),(2,0),(2,2)]))
minimum=H|fan('B',[1,2,3])
maximum=H|fan('B',[0,1,2,3,5,6,7])|set().union(*(fan(k,range(8)) for k in ['L','D','R','E','Tc','N']))
assert U<=minimum and not Z&maximum
assert minimum<=room<=maximum
assert Z&fan('B',[4])
# Two named complete critical-B symbolic envelopes: no additional room.
applications={}
for label,ss in [('Bwest',[1,2,3]),('Brectangle',[0,1,2,3])]:
 mi=H|fan('B',ss);ma=mi|set().union(*(fan(k,range(8)) for k in ['L','D','R','E','Tc','N']))
 assert U<=mi and not Z&ma
 applications[label]={'status':'WHOLE_SUPPORT_PASS','minimum':sorted(mi),'maximum':sorted(ma)}
ur,zr=path_requirements(P[::-1]);assert ur==U and zr==Z
tr=lambda ts:{tuple(sorted(sigma(v) for v in t)) for t in ts}
us,zs=path_requirements(SP);assert us==tr(U) and zs==tr(Z)
# Physical finite-mirror unfolding of actual T, separately from the guards.
q=P[-1];walls=[]
for p in P[-2:0:-1]:
 hits=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if on(p,a,b) and p not in (a,b)]
 assert len(hits)==1
 a,b=hits[0];w=sub(b,a);v=sub(q,a)
 q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1));walls.append((a,b))
assert q==(-4,-6) and cross(q,(-2,-3))==0
# Hand endpoint equation, strict source/floor/chamber gates.
d=F(2,3);assert F(3,5)<d<F(3,4)
assert -2<-1/d<-1 and -1<2*d-2<0 and 1<5*d-2<3
assert P==[(F(0),F(0)),(F(-1),-1/d),(2*d-2,F(-2)),(6*d-2,F(2))]
# The final straight segment passes through C=(0,-1), an INTERIOR point.
assert on((0,-1),P[2],P[3])
from guard_checker import incident
assert incident((F(0),F(-1)))<=minimum
out={'status':'PHYSICAL_TWO_PATH_AND_WHOLE_FAMILY_PASS','reflections':2,'path':[[str(x) for x in p] for p in P],'geometry':raw['ledger'],'actual_unfolded_target':list(map(str,q)),'actual_forward_reverse_sigma_firstT_corneravoidance':'PASS','required':sorted(U),'forbidden':sorted(Z),'minimum':sorted(minimum),'maximum':sorted(maximum),'applications':applications,'hand':{'launch':'(-d,-1)','parameter':'2/3','strict_sufficient_interval':['3/5','3/4'],'endpoint_equation':'6d-2=2','interior_C_crossing':[0,-1]},'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'room.json',HERE/'result.json',HERE/'search.py',Path(__file__),ROOT/'triangle-composition/inputs/boundary_replay.py',ROOT/'triangle-composition/inputs/guard_checker.py']},'limits':'Search ONE fixed room, stopped first candidate. Independent physical checker uses historical geometry/guard primitives; peer independent review pending. Two named symbolic envelopes only, no second room construction or search. No full Delta4 or universal minimum claim.'}
(HERE/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: actual2 finitewall/firstT/corneravoidance/reverse/sigma, unfold(-4,-6), whole H+B123 with all other K stars allowed; west AND rectangle ENTIRE conditional families.')
