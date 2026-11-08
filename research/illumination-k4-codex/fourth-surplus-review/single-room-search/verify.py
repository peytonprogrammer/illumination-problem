"""Independent physical verification of the ONE frozen search result; no discovery."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
import illumination_geometry as g
from boundary_replay import replay,inside,cross,sub,dot,on
from guard_checker import path_requirements
raw=json.loads((HERE/'room.json').read_text());result=json.loads((HERE/'result.json').read_text())
assert result['status']=='FOUND_EXACT_PATH_PENDING_INDEPENDENT_VERIFICATION'
assert hashlib.sha256((HERE/'room.json').read_bytes()).hexdigest()==result['room_sha256']
assert hashlib.sha256((HERE/'search.py').read_bytes()).hexdigest()==result['search_source_sha256']
V=list(map(tuple,raw['vertices']));room={tuple(sorted(map(tuple,t))) for t in raw['triangles']}
P=[tuple(F(*x) for x in p) for p in result['candidate']['path']]
S=(0,0);T=(2,2)
geo=g.check({'triangles':sorted(room),'marked':[S,T],'require_simple':True},strict=False)
assert geo['simple_polygon'] and geo['walls']==20 and set(geo['interior_A'])=={S,(2,0),T}
# Boundary edges are the actual maximal segments, not unfolded image mirrors.
atomic={e for e,owners in g.owners_of(sorted(room)).items() if len(owners)==1}
for a,b in atomic:
 assert sum(on(a,c,d) and on(b,c,d) for c,d in zip(V,V[1:]+V[:1]))==1
assert len(P)-2==9
assert replay(V,S,T,P)==9
assert replay(V,T,S,P[::-1])==9
sigma=lambda p:(2-p[1],2-p[0])
SP=[sigma(p) for p in P[::-1]];SV=[sigma(p) for p in V]
assert replay(SV,S,T,SP)==9
U,Z=path_requirements(P)
assert U<=room and not Z&room
# Hand-declared whole-family minimum, no second room constructed or searched.
RAYS=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
centers={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan(a,ss):return {tuple(sorted((a,(a[0]+RAYS[i%8][0],a[1]+RAYS[i%8][1]),(a[0]+RAYS[(i+1)%8][0],a[1]+RAYS[(i+1)%8][1])))) for i in ss}
H=set().union(*(fan(a,range(8)) for a in [S,(2,0),T]))
minimum=H|fan(centers['N'],[6])|fan(centers['D'],[2])|fan(centers['E'],[3,4])
maximum=minimum|set().union(*(fan(centers[k],range(8)) for k in ['L','B','R']))|fan(centers['Tc'],[4,5])
assert U<=minimum and not Z&maximum
assert room<=maximum
# Actual-wall unfolding and named hand formulas.
q=P[-1]
actualwalls=[]
for p in P[-2:0:-1]:
 walls=[(a,b) for a,b in zip(V,V[1:]+V[:1]) if on(p,a,b) and p not in (a,b)]
 assert len(walls)==1
 a,b=walls[0];e=sub(b,a);v=sub(q,a)
 q=tuple(a[k]+2*dot(v,e)*e[k]/dot(e,e)-v[k] for k in (0,1))
 actualwalls.append((a,b))
assert cross(q,(1,4))==0 and dot(q,(1,4))>0
assert q==(4,16)
d=F(1,4);assert F(3,13)<d<F(4,15)
formula=[S,(2*d/(1+d),2/(1+d)),(F(0),2-2*d),(2*d/(1-d),2-2*d/(1-d)),
 (4*d/(1-d),-4*d/(1-d)),(F(2),-6*d),(8*d/(1+d),-8*d/(1+d)),
 (11*d,F(3)),(16*d/(1+d),16*d/(1+d)-2),(F(1),15*d-2),(F(2),16*d-2)]
assert P==formula
assert 0<d<3*d<1 and 1<5*d<7*d<2
assert 2<11*d<3 and 1<15*d-2<2 and 16*d-2==2
out={'status':'INDEPENDENT_PHYSICAL_AND_HAND_NINE_PATH_PASS','reflections':9,'path':[[str(x) for x in p] for p in P],
 'geometry':raw['ledger'],'actual_unfolded_target':list(map(str,q)),'physical_forward_reverse_sigma_firstT_corner_avoidance':'PASS',
 'whole_family':{'minimum':sorted(minimum),'maximum':sorted(maximum),'required':sorted(U),'forbidden':sorted(Z),'allows_full_L_B_R_and_Tc45':True},
 'parameter':'1/4','strict_sufficient_interval':['3/13','4/15'],'actual_endpoint_equation':'16d-2=2',
 'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'room.json',HERE/'result.json',HERE/'search.py',Path(__file__),ROOT/'triangle-composition/inputs/boundary_replay.py',ROOT/'triangle-composition/inputs/guard_checker.py']},
 'limits':'Search ONE fixed room only, stopped at first candidate. Verification uses exact physical polygon replay and historical independent guard primitives, unlike integer-frame discovery. No second room search/construction or formal/expert verification. Peer independent hand challenge requested separately.'}
(HERE/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: actual9 finite-wall reflections, firstT, corneravoidance, reverse/sigma, full U/Z; unfold actualT(4,16); hand endpoint16d-2=2.')
