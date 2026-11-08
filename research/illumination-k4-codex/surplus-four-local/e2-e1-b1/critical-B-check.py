"""Review two supplied paths only. No search or new room construction.
Independent Fraction geometry; imports no peer or historical geometry code.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter, defaultdict
import json, hashlib
BASE=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
PEER=BASE/'fourth-surplus-review'
R=((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
C={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def tri(t): return tuple(sorted(t))
def ccw(t):
 a,b,c=t
 return (a,b,c) if cross(sub(b,a),sub(c,a))>0 else (a,c,b)
def fan(a,ss):
 if isinstance(a,str): a=C[a]
 return {tri((a,(a[0]+R[i][0],a[1]+R[i][1]),(a[0]+R[(i+1)%8][0],a[1]+R[(i+1)%8][1]))) for i in ss}
H=set().union(*(fan(a,range(8)) for a in [(0,0),(2,0),(2,2)]))
# Finite local tiling universe only for incidence tests, not room generation.
TILES=set().union(*(fan((x,y),range(8)) for x in range(-6,9,2) for y in range(-6,9,2)))
def signs(p,t):
 t=ccw(t)
 return [cross(sub(t[(i+1)%3],t[i]),sub(p,t[i])) for i in range(3)]
def incident(p): return {t for t in TILES if min(signs(p,t))>=0}
def on(p,a,b): return cross(sub(p,a),sub(b,a))==0 and dot(sub(p,a),sub(p,b))<=0
def edge_times(a,b,c,d):
 v=sub(b,a);w=sub(d,c);den=cross(v,w)
 if den:
  t=F(cross(sub(c,a),w),den);u=F(cross(sub(c,a),v),den)
  return [t] if 0<=t<=1 and 0<=u<=1 else []
 if cross(sub(c,a),v):return []
 k=0 if v[0] else 1
 return [F(p[k]-a[k],v[k]) for p in (c,d) if on(p,a,b)]
def reflect(v,a,b):
 w=sub(b,a)
 return tuple(2*dot(v,w)*w[k]/dot(w,w)-v[k] for k in (0,1))
def constraints(P,walls):
 used=set();absent=set();events=[]
 for a,b in zip(P,P[1:]):
  times={F(0),F(1)}
  for t in TILES:
   for c,d in zip(t,t[1:]+t[:1]):times.update(edge_times(a,b,c,d))
  times=sorted(times);samples=times[1:-1]+[(l+h)/2 for l,h in zip(times,times[1:])]
  for s in samples:
   p=tuple(a[k]+s*(b[k]-a[k]) for k in (0,1));used.update(incident(p))
  events.append(len(times)-2)
 for before,p,after,(a,b) in zip(P,P[1:],P[2:],walls):
  assert on(p,a,b) and p not in (a,b)
  v=reflect(sub(p,before),a,b);w=sub(after,p)
  assert cross(v,w)==0 and dot(v,w)>0
  side=cross(sub(b,a),sub(before,p));assert side
  assert side*cross(sub(b,a),sub(after,p))>0
  for t in incident(p):
   ss=[cross(sub(b,a),sub(q,p)) for q in t]
   assert min(ss)>=0 or max(ss)<=0
   s=sum(ss);assert s
   (used if s*side>0 else absent).add(t)
 assert not used&absent
 return used,absent,events
sigma=lambda p:(2-p[1],2-p[0])
def transform(ts):return {tri(tuple(sigma(p) for p in t)) for t in ts}
def audit(P,walls,minimum,maximum,target):
 assert P[0]==(0,0) and P[-1]==(2,2)
 for a,b in zip(P[:-2],P[1:-1]):assert not on((2,2),a,b)
 U,Z,events=constraints(P,walls)
 assert U<=minimum and not Z&maximum
 ur,zr,_=constraints(P[::-1],walls[::-1]);assert (ur,zr)==(U,Z)
 ps=[sigma(p) for p in P[::-1]];ws=[(sigma(a),sigma(b)) for a,b in walls[::-1]]
 us,zs,_=constraints(ps,ws);assert (us,zs)==(transform(U),transform(Z))
 # Independent specular checks above also cover reverse and sigma paths.
 q=P[-1]
 for a,b in walls[::-1]:
  v=reflect(sub(q,a),a,b);q=tuple(a[k]+v[k] for k in (0,1))
 assert q==target
 return U,Z,{'reflections':len(walls),'required_count':len(U),'forbidden_count':len(Z),'segment_internal_edge_events':events,'unfolded_target':q,'forward_reverse_sigma':'PASS'}
def boundary(room):
 edges=Counter()
 for t in room:
  t=ccw(t)
  for a,b in zip(t,t[1:]+t[:1]):edges[(a,b)]+=1
 edge={e for e in edges if not edges[(e[1],e[0])]}
 nxt=defaultdict(list)
 for a,b in edge:nxt[a].append(b)
 assert all(len(v)==1 for v in nxt.values())
 p=min(nxt);start=p;cycle=[]
 while True:
  assert p not in cycle;cycle.append(p);p=nxt[p][0]
  if p==start:break
 assert len(cycle)==len(edge)
 return [p for i,p in enumerate(cycle) if cross(sub(p,cycle[i-1]),sub(cycle[(i+1)%len(cycle)],p))]
def inside(p,V):
 if any(on(p,a,b) for a,b in zip(V,V[1:]+V[:1])):return False
 n=0
 for a,b in zip(V,V[1:]+V[:1]):
  if (a[1]>p[1])!=(b[1]>p[1]):
   x=a[0]+F(p[1]-a[1],b[1]-a[1])*(b[0]-a[0]);n+=x>p[0]
 return n%2==1
def physical(P,V):
 for i,(a,b) in enumerate(zip(P,P[1:])):
  assert inside(tuple((a[k]+b[k])/2 for k in (0,1)),V)
  hits=[]
  for c,d in zip(V,V[1:]+V[:1]):
   for s in edge_times(a,b,c,d):
    if s>0:hits.append((s,c,d))
  if i==len(P)-2:assert not hits
  else:
   assert hits and min(h[0] for h in hits)==1
   hit=[h for h in hits if h[0]==1];assert len(hit)==1 and b not in V
   _,c,d=hit[0];v=reflect(sub(b,a),c,d);w=sub(P[i+2],b)
   assert cross(v,w)==0 and dot(v,w)>0

def path(d,nine):
 P=[(F(0),F(0)),(2*d/(1+d),2/(1+d)),(F(0),2-2*d),(2*d/(1-d),2-2*d/(1-d))]
 if nine:P +=[(4*d/(1-d),-4*d/(1-d)),(F(2),-6*d),(8*d/(1+d),-8*d/(1+d))]
 else:P +=[(5*d,F(-1))]
 k=16 if nine else 14
 P +=[((k-5)*d,F(3)),(k*d/(1+d),k*d/(1+d)-2),(F(1),(k-1)*d-2),(F(2),k*d-2)]
 return P
# Selected existing witnesses only: no catalog search or new path discovery.
def read(rel):return json.loads((BASE/rel).read_text())
def dec(P):return [tuple(F(*x) if isinstance(x,list) else F(x) for x in p) for p in P]
zero=read('zero-surplus-L/cover-check.json')

paths={'five':dec(read('second-surplus-review/five-path-check.json')['five_path']),
       '13':dec(zero['paths']['thirteen']['path']),
       'sigma13':dec(zero['paths']['thirteen_sigma']['path']),
       'L3':dec(read('first-surplus-review/residual-cover-check.json')['path']),
       'B6':dec(read('first-surplus-review/bottom-residual-check.json')['path']),
       'uniform7':[tuple(map(F,p)) for p in read('surplus-four-local/single-e2-check.json')['universal_lemmas']['uniform_seven']['path']]}
paths['T3']=[sigma(p) for p in paths['L3'][::-1]]
paths['E6']=[sigma(p) for p in paths['B6'][::-1]]
fullfan=lambda k:fan(k,range(8))
paths['L12']=dec(read('first-surplus-review/centered-left-check.json')['paths']['left']['path'])
paths['E11']=dec(read('first-surplus-review/square-exchange-check.json')['paths']['E_thirteen']['path'])
paths['Lsquare5']=[paths['uniform7'][0],(F(-2),F(1,3))]+paths['uniform7'][4:]
paths['top_square3']=[(F(0),F(0)),(F(1,6),F(1)),(F(2,3),F(-2)),(F(5,3),F(4)),(F(2),F(2))]
paths['BT9']=paths['13'][:8]+[(F(6,11),F(-2)),(F(18,11),F(4))]+paths['13'][14:]
force=read('third-surplus-review/independent-review/guard-extension-check.json')['forcing_paths']
for key in ['outerB2','sigma_outerB2','sigma_centeredB3']:paths[key]=dec(force[key]['path'])
for key in ['one_sigma','four_sigma']:paths[key]=dec(zero['paths'][key]['path'])
# Fixed supplied paths' triangle requirements; named incidence diagnostic.
requirements={}
for name,P in paths.items():
 ws=[]
 for before,p,after in zip(P,P[1:],P[2:]):
  v=sub(p,before);w=sub(after,p);found=[]
  for t in [(1,0),(0,1),(1,1),(1,-1)]:
   ref=reflect(v,p,(p[0]+t[0],p[1]+t[1]))
   if cross(ref,w)==0 and dot(ref,w)>0 and cross(t,v):found.append(t)
  assert len(found)==1
  t=found[0];ws.append(((p[0]-t[0],p[1]-t[1]),(p[0]+t[0],p[1]+t[1])))
 U,Z,_=constraints(P,ws);requirements[name]=(U,Z)
 def labels(ts):
  return {k:[i for i in range(8) if fan(k,[i])&ts] for k in C if fullfan(k)&ts}
 # Retain exact named guard requirements for the final receipt.
# New prescribed normal-return replacement, preserving both portal states.
old=paths['five'];new=paths['top_square3']
entry=(F(3,2),F(3));exit=(F(11,6),F(3));hit=(F(5,3),F(4))
for a,b,v in [(old[2],entry,(1,6)),(entry,old[3],(1,6)),(old[5],exit,(1,-6)),(exit,old[6],(1,-6)),(entry,hit,(1,6)),(hit,exit,(1,-6))]:
 w=sub(b,a);assert cross(w,v)==0 and dot(w,v)>0
assert F(1,2)+2*F(1,6)==F(5,6)
# Physical declared mirror lines: source ceiling, B square floor, Tc top.
newwalls=[((0,1),(1,1)),((0,-2),(1,-2)),((1,4),(2,4))]
newU,newZ,newproof=audit(new,newwalls,H|fan('B',[0,1])|fan('Tc',[4,5]),
 H|fan('B',[0,1,2,3,4,5,6])|fan('Tc',[0,1,2,4,5,6,7])|fan('N',[0,1,2,3,4,5,7])|set().union(*(fullfan(k) for k in ['L','D','R','E'])),(2,12))
# Reflection count and first actualT were checked in audit, no room built.
assert requirements['top_square3']==(newU,newZ)
LC=fan('L',[7,0]);LO=fan('L',[0,1]);EC=fan('E',[3,4]);EO=fan('E',[4,5]);TC=fan('Tc',[5,6]);TO=fan('Tc',[4,5])
L0=fan('L',[0]);E4=fan('E',[4]);T5=fan('Tc',[5]);DR=fullfan('D')|fullfan('R')
checks=[]
def cover(label,key,mi,ma):
 U,Z=requirements[key];assert U<=mi,(label,'missing',U-mi)
 assert not Z&ma,(label,'mirror',Z&ma)
 checks.append({'name':label,'path':key,'reflections':len(paths[key])-2,'minimum':sorted(mi),'maximum':sorted(ma)})
# Nine predeclared whole envelopes: Beast012 has B01 and lacks B7.
# B1234 lacks B0, so cannot use this five/top-square dispatch.
for label,ss in [('Beast012',[0,1,2])]:
 b=fan('B',ss)
 cover(label+'_awayT_N6abs','five',H|b|T5,H|b|T5|fullfan('L')|fullfan('E')|DR|(fullfan('N')-fan('N',[6])))
 cover(label+'_LC_N6','L12',H|b|LC|E4,H|b|LC|E4|T5|DR|fan('N',[6]))
 cover(label+'_LO_N6','Lsquare5',H|b|LO|E4,H|b|LO|E4|T5|DR|fan('N',[6]))
 cover(label+'_EC_N6','E6',H|b|L0|EC,H|b|L0|EC|T5|DR|fan('N',[6]))
 cover(label+'_EO_N6','E11',H|b|L0|EO,H|b|L0|EO|T5|DR|fan('N',[6]))
 cover(label+'_noncritical_N456','sigma13',H|b|L0|E4,H|b|L0|E4|T5|DR|fan('N',[4,5,6]))
 cover(label+'_Tcenter','T3',H|b|E4|TC,H|b|E4|TC|fullfan('L')|DR|fullfan('N'))
 cover(label+'_Touter_N6abs','top_square3',H|b|TO,H|b|TO|fullfan('L')|fullfan('E')|DR|(fullfan('N')-fan('N',[6])))
 cover(label+'_Touter_N7abs','uniform7',H|b|L0|E4|TO,H|b|L0|E4|TO|DR|(fullfan('N')-fan('N',[7])))
# Three joined forms plus B1234, six conditional envelopes each. These do NOT assume
# ordinary Tc5 is forced: Tc6 remains in maxima unless a path forbids it.
for label,ss in [('O3_701',[7,0,1]),('O4_6701',[6,7,0,1]),('H4_7012',[7,0,1,2]),('West1234',[1,2,3,4])]:
 b=fan('B',ss)
 cover(label+'_ordinaryLE_N7abs','uniform7',H|b|L0|E4,H|b|L0|E4|DR|fullfan('Tc')|(fullfan('N')-fan('N',[7])))
 cover(label+'_LO_N7abs','Lsquare5',H|b|LO|E4,H|b|LO|E4|DR|fullfan('Tc')|(fullfan('N')-fan('N',[7])))
 cover(label+'_Tcenter','T3',H|b|E4|TC,H|b|E4|TC|DR|fullfan('L')|fullfan('N'))
 cover(label+'_EC_N0abs','E6',H|b|L0|EC,H|b|L0|EC|DR|fullfan('Tc')|(fullfan('N')-fan('N',[0])))
 cover(label+'_EO_T6N0N7abs','E11',H|b|L0|EO,H|b|L0|EO|DR|(fullfan('Tc')-fan('Tc',[6]))|(fullfan('N')-fan('N',[0,7])))
 cover(label+'_LC_T6N0N7abs','L12',H|b|LC|E4,H|b|LC|E4|DR|(fullfan('Tc')-fan('Tc',[6]))|(fullfan('N')-fan('N',[0,7])))
assert len(checks)==33 and max(x['reflections'] for x in checks)<=13
allK=H|set().union(*(fullfan(k) for k in C))
cover('force_E4','one_sigma',H,allK-fan('E',[4]))
cover('force_L0_Eordinary','four_sigma',H|E4,(allK-fullfan('E')-L0)|E4)
cover('force_L0_Ecenter','sigma_centeredB3',H|EC,(allK-fullfan('E')-L0)|EC)
cover('force_L0_Eouter','sigma_outerB2',H|EO,(allK-fullfan('E')-L0)|EO)
cover('force_T5_Beast_B2harmless','outerB2',H|fan('B',[0,1,2]),(allK-fullfan('B')-T5)|fan('B',[0,1,2]))
assert len(checks)==38
# Local b1 obstructions: triangle incidence only, not completed rooms.
def angle(ts,p):
 total=0
 for t in ts:
  if p in t:
   a,b=[sub(v,p) for v in t if v!=p];total+=90 if dot(a,b)==0 else 45
 return total
angles=[]
for label,ss in [('O3',[7,0,1]),('O4',[6,7,0,1]),('H4',[7,0,1,2])]:
 b=fan('B',ss)
 assert angle(H|b,(1,-2))==180
 assert angle(H|b|fan('D',[2,3]),(1,-2))==270
 assert angle(H|b|LO,( -1,1))==180
 assert angle(H|b|TO,(1,3))==180
 assert angle(H|b|fan('N',[7,0])|T5,(1,3))==180
 # Only D3/4 could touch the outside east C among other K cells;
 # with an e1 ROOT at D the only such fan is D23.
 assert not any((1,-2) in t for k in ['L','R','E','Tc','N'] for t in fullfan(k))
 angles.append({'B':label,'outside_C':180,'D23_healed':270,'LO_without_N5':180,'TO_without_N0':180,'N70_with_T5':180})
assert angle(H|fan('B',[7,0,1,2])|LC,(-1,-1))==180
# For D23 + N7 ordinary, all non-A outside smoothness is zero: test
# symbolic ordinary contributions at each possible B point individually.
# No cap assignment combination is constructed. The only b terms are
# N5 and Tc5*N0; under N7 both vanish.
joined_coeff={}
ordinary={'L0':L0,'E4':E4,'T5':T5,'T6':fan('Tc',[6]),'R3':fan('R',[3]),'R4':fan('R',[4]),'N5':fan('N',[5]),'N6':fan('N',[6]),'N7':fan('N',[7]),'N0':fan('N',[0])}
for label,ss in [('O3',[7,0,1]),('O4',[6,7,0,1]),('H4',[7,0,1,2])]:
 fixed=H|fan('B',ss)|fan('D',[2,3])|L0|E4
 pts={p for t in fixed|set().union(*ordinary.values()) for p in t if p[0]%2==p[1]%2==1}
 coeff={}
 for p in sorted(pts):
  constant=angle(fixed,p);vars={k:angle(v,p) for k,v in ordinary.items() if k not in ['L0','E4'] and angle(v,p)}
  coeff[str(p)]={'constant':constant,'variables':vars}
  if p not in [(-1,1),(1,3)]:
   assert constant>=225 or constant+sum(vars.values())<180,(label,p,constant,vars)
 assert coeff[str((-1,1))]=={'constant':135,'variables':{'N5':45}}
 assert coeff[str((1,3))]=={'constant':90,'variables':{'T5':45,'N0':45}}
 joined_coeff[label]=coeff
assert angle(H|fan('B',[1,2,3,4]),(-1,-2))==180
assert angle(H|fan('B',[1,2,3,4])|L0,(-1,-1))==180
assert angle(H|fan('B',[1,2,3,4])|LC,(-1,-1))==225
assert angle(H|fan('Tc',[6,7])|E4,(3,3))==180
assert not any((-1,-2) in t for k in ['L','D','R','E','Tc','N'] for t in fullfan(k))
# West1234 + forced LC: exact extra-smooth B coefficients.
westfixed=H|fan('B',[1,2,3,4])|LC|E4
westvars={'T5':T5,'T6':fan('Tc',[6]),'D1':fan('D',[1]),'D2':fan('D',[2]),'R3':fan('R',[3]),'R4':fan('R',[4]),'N5':fan('N',[5]),'N6':fan('N',[6]),'N7':fan('N',[7]),'N0':fan('N',[0])}
westcoeff={}
pts={p for t in westfixed|set().union(*westvars.values()) for p in t if p[0]%2==p[1]%2==1}
for p in sorted(pts):
 constant=angle(westfixed,p);vs={k:angle(v,p) for k,v in westvars.items() if angle(v,p)}
 westcoeff[str(p)]={'constant':constant,'variables':vs}
 if p not in [(-1,1),(1,3),(3,-1)]:assert constant>=225 or constant+sum(vs.values())<180,(p,constant,vs)
assert westcoeff[str((-1,1))]=={'constant':135,'variables':{'N5':45}}
assert westcoeff[str((1,3))]=={'constant':90,'variables':{'T5':45,'N0':45}}
assert westcoeff[str((3,-1))]=={'constant':90,'variables':{'D1':45,'R4':45}}
# EC+N0 consumes no further b only if Tc is empty: either Tc cap makes180.
for ss in [[7,0,1],[6,7,0,1],[7,0,1,2]]:
 base=H|fan('B',ss)|L0|EC|fan('N',[0])
 assert angle(base|T5,(1,3))==180
 assert angle(base|fan('Tc',[6]),(3,3))==180
inputs=['third-surplus-review/independent-review/guard-extension-check.json','zero-surplus-L/cover-check.json','first-surplus-review/residual-cover-check.json','first-surplus-review/bottom-residual-check.json','first-surplus-review/centered-left-check.json','first-surplus-review/square-exchange-check.json','second-surplus-review/five-path-check.json','surplus-four-local/single-e2-check.json','surplus-four-local/e2-e1-b1/argument.txt']
receipt={'status':'PARENT_CRITICAL_B_CONSOLIDATION_PASS','whole_envelopes':checks,'new_three_reflection_normal_exchange':newproof,'source_and_exit_states':{'entry':['3/2','3'],'exit':['11/6','3'],'old_three_contacts':3,'new_one_contact':1},'local_angle_identities':angles,'joined_D23_b_coefficients':joined_coeff,'West1234_b_coefficients':westcoeff,'source_sha256':{n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in inputs},'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'33 prescribed optical envelopes plus5 forcing implications, not cap/room enumeration. Earlier reference forcing, active e1 fan classification and b1 interpretation inherited. No raw archive or discovery. New3 proof and consolidation independently unreviewed.'}
Path(__file__).resolve().parent.joinpath('critical-B-check.json').write_text(json.dumps(receipt,indent=2,default=str)+'\n')
print('PASS:33 named optical envelopes plus5 forcing implications, new3 normal exchange, local angle exclusions and joinedD23 b formula. Parent proof only.')
