"""One hand-derived joined-pocket path, no room construction or discovery."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements,incident
from boundary_replay import cross,sub,dot,on
rays=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
centers={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def fan(site,ss):
 a=centers[site] if isinstance(site,str) else site
 return {tuple(sorted((a,(a[0]+rays[i%8][0],a[1]+rays[i%8][1]),(a[0]+rays[(i+1)%8][0],a[1]+rays[(i+1)%8][1])))) for i in ss}
H=set().union(*(fan(a,range(8)) for a in [(0,0),(2,0),(2,2)]))
d=F(1,5);assert F(1,7)<d<F(2,9)
P=[(F(0),F(0)),(2*d/(1-d),-2/(1-d)),(F(1),-2-3*d),(4*d/(1+d),-2-4*d/(1+d)),(9*d,F(3)),(10*d,F(2))]
assert P==[(F(0),F(0)),(F(1,2),F(-5,2)),(F(1),F(-13,5)),(F(2,3),F(-8,3)),(F(9,5),F(3)),(F(2),F(2))]
assert all(not on((2,2),a,b) for a,b in zip(P[:-2],P[1:-1]))
U,Z=path_requirements(P)
minimum=H|fan('B',[7,0,1])|fan('D',[2,3])
maximum=H|fan('B',[0,1,2,3,4,5,7])|fan('D',[0,1,2,3,5,6,7])|fan('Tc',[0,1,2,3,4,6,7])|set().union(*(fan(k,range(8)) for k in ['L','R','E','N']))
assert U<=minimum and not Z&maximum
walls=[((0,-2),(1,-3)),((1,-3),(1,-2)),((0,-2),(1,-3)),((1,3),(2,3))]
for a,p,b,(c,e) in zip(P,P[1:],P[2:],walls):
 assert on(p,c,e) and p not in (c,e)
 incoming=sub(p,a);w=sub(e,c)
 v=tuple(2*dot(incoming,w)*w[k]/dot(w,w)-incoming[k] for k in (0,1))
 assert cross(v,sub(b,p))==0 and dot(v,sub(b,p))>0
assert on((1,-1),P[3],P[4])
assert incident((F(1),F(-1)))<=minimum
withoutD2=minimum-fan('D',[2])
assert not incident((F(1),F(-1)))<=withoutD2
assert U&fan('D',[2]) and Z&fan('D',[4]) and Z&fan('B',[6]) and Z&fan('Tc',[5])
ur,zr=path_requirements(P[::-1]);assert ur==U and zr==Z
sigma=lambda p:(2-p[1],2-p[0])
tr=lambda ts:{tuple(sorted(sigma(v) for v in t)) for t in ts}
sp=[sigma(p) for p in P[::-1]];us,zs=path_requirements(sp)
assert sp[0]==(0,0) and sp[-1]==(2,2) and us==tr(U) and zs==tr(Z)
q=P[-1]
for a,b in walls[::-1]:
 w=sub(b,a);v=sub(q,a)
 q=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
assert q==(2,-10)
# Exactly TWO declared symbolic root envelopes, Tc5 absent in both.
applications={}
for label,ss in [('O3',[7,0,1]),('H4',[7,0,1,2])]:
 mi=H|fan('B',ss)|fan('D',[2,3]);ma=mi|fan('Tc',[4,6,7])|set().union(*(fan(k,range(8)) for k in ['L','R','E','N']))
 assert U<=mi and not Z&ma
 applications[label]={'minimum':sorted(mi),'maximum':sorted(ma),'status':'WHOLE_SUPPORT_PASS'}
# One complementary HAND-prescribed Tc5 normal return, not a search.
d6=F(1,6);assert F(1,7)<d6<F(2,11)
P6=[(F(0),F(0)),(2*d6/(1-d6),-2/(1-d6)),(F(1),-2-3*d6),
 (4*d6/(1+d6),-2-4*d6/(1+d6)),(8*d6/(1-d6),2+8*d6/(1-d6)),
 (F(2),2+10*d6),(12*d6/(1+d6),2+12*d6/(1+d6)),(12*d6,F(2))]
assert P6[-1]==(2,2) and len(P6)-2==6
assert all(not on((2,2),a,b) for a,b in zip(P6[:-2],P6[1:-1]))
u6,z6=path_requirements(P6)
mi6=H|fan('B',[7,0,1])|fan('Tc',[5])
ma6=H|fan('B',[0,1,2,3,4,5,7])|fan('D',[0,1,2,3,5,6,7])|fan('Tc',[0,1,2,3,5,7])|set().union(*(fan(k,range(8)) for k in ['L','R','E','N']))
assert u6<=mi6 and not z6&ma6
walls6=walls[:3]+[((1,3),(2,4)),((2,3),(2,4)),((1,3),(2,4))]
for a,p,b,(c,e) in zip(P6,P6[1:],P6[2:],walls6):
 assert on(p,c,e) and p not in (c,e)
 incoming=sub(p,a);w=sub(e,c)
 v=tuple(2*dot(incoming,w)*w[k]/dot(w,w)-incoming[k] for k in (0,1))
 assert cross(v,sub(b,p))==0 and dot(v,sub(b,p))>0
q6=P6[-1]
for a,b in walls6[::-1]:
 w=sub(b,a);v=sub(q6,a)
 q6=tuple(a[k]+2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
assert q6==(2,-12)
u6r,z6r=path_requirements(P6[::-1]);assert u6r==u6 and z6r==z6
u6s,z6s=path_requirements([sigma(p) for p in P6[::-1]]);assert u6s==tr(u6) and z6s==tr(z6)
app6={}
for label,ss in [('O3',[7,0,1]),('H4',[7,0,1,2])]:
 mi=H|fan('B',ss)|fan('D',[2,3])|fan('Tc',[5]);ma=mi|set().union(*(fan(k,range(8)) for k in ['L','R','E','N']))
 assert u6<=mi and not z6&ma
 app6[label]='WHOLE_SUPPORT_PASS_ORDINARY_TC5'
six={'path':[[str(x) for x in p] for p in P6],'minimum':sorted(mi6),'maximum':sorted(ma6),'required':sorted(u6),'forbidden':sorted(z6),'reflections':6,'parameter':'1/6','strict_interval':['1/7','2/11'],'endpoint_equation':'12d=2','actual_unfolded_target':list(map(str,q6)),'applications':app6,'reverse_sigma_firstT_finitewalls':'PASS'}
out={'status':'JOINED_FOUR_HAND_PATH_AND_WHOLE_SUPPORT_PASS','six_path_complement':six,'reflections':4,'path':[[str(x) for x in p] for p in P],'minimum':sorted(minimum),'maximum':sorted(maximum),'required':sorted(U),'forbidden':sorted(Z),'physical_mirrors':walls,'actual_unfolded_target':list(map(str,q)),'hand':{'launch':'(d,-1)','parameter':'1/5','strict_interval':['1/7','2/9'],'actual_endpoint_equation':'10d=2','essential_interior_crossing':[1,-1]},'applications':applications,'reverse_sigma':'PASS','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),HERE/'argument.txt',HERE/'critical-B.txt',ROOT/'triangle-composition/inputs/guard_checker.py',ROOT/'triangle-composition/inputs/boundary_replay.py']},'limits':'Hand-composed fixed path plus exact full support proof only. No assembled room or boundary census/search/discovery/archive/worker. Four path does not cover O4/B6 or Dsingle3/4; complementary six handles ordinary Tc5 and even Dsingle3, not D4. No O4/B6 closure. Independent review pending.'}
(HERE/'joined-four-check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: joined O3/H4 FOUR + complementary SIX, fullU-Z/strictfinitewalls/firstT/reverse/sigma; whole ordinary-Tc split closes both root forms. O4/B6 remains open.')
