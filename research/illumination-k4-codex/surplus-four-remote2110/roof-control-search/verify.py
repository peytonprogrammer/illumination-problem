"""Independent exact verification of ONE stopped remote2110 roof candidate.
Fraction primitive prefix only; no search or peer checker execution/import.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py';e={'__file__':str(src)}
exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H'];fp=lambda ps:[tuple(F(x)for x in p)for p in ps]
raw=json.loads((HERE/'room.json').read_text());found=json.loads((HERE/'result.json').read_text())
assert found['status']=='FOUND_EXACT_PATH_PENDING_INDEPENDENT_VERIFICATION'
for n,k in [('room.json','room_sha256'),('search.py','search_source_sha256')]:assert hashlib.sha256((HERE/n).read_bytes()).hexdigest()==found[k]
P=[tuple(F(*x)for x in p)for p in found['candidate']['path']]
assert P==fp([(0,0),('-1/4',1),('-3/4',-1),('-4/3','4/3'),(-2,'3/2'),('-8/5','8/5'),(-2,0),('10/3','4/3'),('7/2',2),('18/5','8/5'),(2,2)])
walls=[((-1,1),(1,1)),((-1,-1),(0,-1)),((-2,2),(-1,1)),((-2,1),(-2,2)),((-2,2),(-1,1)),((-3,1),(-1,-1)),((3,1),(4,2)),((3,2),(4,2)),((3,1),(4,2))]
mi=H|fan('L',[7,0,1,2])|fan((-2,2),[6])|fan('E',[4])
# Compute guards first; permit every other local triangle not forbidden,
# but only this ONE remote triangle. This is a whole support envelope.
u,z,_=e['constraints'](P,walls)
allK=H|set().union(*(fan(k,range(8))for k in e['C']))
ma=(allK|fan((-2,2),[6]))-z
image=P[-1]
for a,b in walls[::-1]:
 v=e['reflect'](e['sub'](image,a),a,b);image=tuple(a[k]+v[k]for k in (0,1))
u,z,proof=e['audit'](P,walls,mi,ma,image)
assert proof['reflections']==9 and image==(-4,16)
for a,b in zip(P[1:-1],P[2:]):assert not e['on']((0,0),a,b)
room={tuple(sorted(map(tuple,t)))for t in raw['triangles']}
assert room==H|set().union(*(fan(k,ss)for k,ss in raw['spec'].items()))|fan(tuple(raw['remote_center']),raw['remote_sectors'])
assert len(room)==35 and mi<=room<=ma
V=e['boundary'](room);assert len(V)==20 and set(V)==set(map(tuple,raw['vertices']))
e['physical'](P,V);e['physical'](P[::-1],V);e['physical']([e['sigma'](p)for p in P[::-1]],[e['sigma'](p)for p in V])
def angle(ts,p):
 return sum(90 if e['dot'](*[e['sub'](v,p)for v in t if v!=p])==0 else 45 for t in ts if p in t)
pts={p for t in room for p in t};A={p for p in pts if p[0]%2==p[1]%2==0}
assert {p for p in A if angle(room,p)==360}=={(0,0),(2,0),(2,2)}
J=sum(angle(room,p)==360 for p in pts-A);sN=sum(angle(room,p)==180 for p in pts-A)
Q=sum(3 if angle(room,p)==180 else angle(room,p)//45 for p in A if angle(room,p)!=360)
assert (J,sN,Q,J+sN,Q+sN-8)==(4,2,10,6,4)
assert angle(room,(-2,0))==180 and (-2,0)not in V
assert e['incident']((F(-1),F(0)))<=mi and e['on']((-1,0),P[2],P[3])
assert e['incident']((F(2),F(1)))<=H and e['on']((2,1),P[6],P[7])
# All contacts from physical lines and actual endpoint equation.
def path(d):
 a=4*d/(1-d);b=8*d/(1+d);c=10*d/(1+d)
 j=10*d/(1-d);k=18*d/(1+d)
 return fp([(0,0),(-d,1),(-3*d,-1),(-a,a),(-2,6*d),(-b,b),(-c,c-2),(j,j-2),(14*d,2),(k,k-2),(2,16*d-2)])
d=F(1,4);lo,hi=F(3,13),F(4,15)
assert lo<d<hi and 16*d-2==2 and path(d)==P
# Contact/portal expressions monotone, without poles in the chosen gate.
checks=[(lambda t:-t,-1,0),(lambda t:-3*t,-1,0),(lambda t:-4*t/(1-t),-2,-1),(lambda t:6*t,1,2),(lambda t:-8*t/(1+t),-2,-1),(lambda t:-10*t/(1+t),-3,-1),(lambda t:1/t-4,-1,1),(lambda t:9*t-2,-1,1),(lambda t:3/t-10,1,3),(lambda t:10*t/(1-t),3,4),(lambda t:14*t,3,4),(lambda t:18*t/(1+t),3,4),(lambda t:15*t-2,1,2)]
for fn,a,b in checks:
 x,y=fn(lo),fn(hi);assert a<=x<=b and a<=y<=b and x!=y,(str(fn),x,y,a,b)
# Whole centeredTc family with ordinary N empty/right: no extra room built.
apps=[]
for n in [(),(0,),(6,),(7,)]:
 lower=H|fan('L',[7,0,1,2])|fan((-2,2),[6])|fan('Tc',[5,6])|fan('B',[1])|fan('E',[4])|fan('N',n)
 upper=lower|fan('D',[1,2])|fan('R',[3,4])
 assert u<=lower and not z&upper
 apps.append({'ordinary_N':n,'full_ordinary_D_R_safe':True,'reflections':9})
owned=lambda ts:{str(a):[i for i in range(8)if fan(a,[i])&ts]for a in list(e['C'].values())+[(-2,2),(-4,0)]if ts&fan(a,range(8))}
reads=[src,Path(__file__),HERE/'room.json',HERE/'result.json',HERE/'search.py']
out={'status':'PARENT_REMOTE2110_ROOF_CONTROL_NINE_AND_RIGHT_N_ORDINARY_FAMILY_PASS','path':[[str(x)for x in p]for p in P],'walls':walls,'minimum':sorted(mi),'maximum':sorted(ma),'required':sorted(u),'forbidden':sorted(z),'required_owners':owned(u),'forbidden_owners':owned(z),'proof':proof,'image':image,'smooth_A_L_minus2_0':True,'root':'1/4','strict_gate':['3/13','4/15'],'endpoint_equation':'16d-2=2','applications':apps,'geometry':{'triangles':35,'W':20,'J':J,'sN':sN,'Q':Q,'k':6,'Delta':4,'fullA':'SUT'},'source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest()for p in reads},'limits':'ONE fixed authorized search stopped36vectors, no extra room; ownFraction fullguards and finiteboundary proof. Parent family lemma pending independentreview; doesnotclosewhole2110. Only N5 is blocked among ordinaryNchoices.'}
(HERE/'verification.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(out['status'],len(u),'U',len(z),'Z',out['forbidden_owners'])
