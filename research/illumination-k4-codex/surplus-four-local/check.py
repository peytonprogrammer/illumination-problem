"""Check the missing two-unit symbolic branch and one prescribed control."""
from pathlib import Path
from fractions import Fraction as F
import hashlib, json, sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements,dot,cross,sub
from boundary_replay import replay
import illumination_geometry as geom
tri=lambda t:tuple(sorted(map(tuple,t)))
D=geom.DIRS

def fan(c,start,m):
 return {tri((c,(c[0]+D[i%8][0],c[1]+D[i%8][1]),(c[0]+D[(i+1)%8][0],c[1]+D[(i+1)%8][1]))) for i in range(start,start+m)}
H=set().union(*(fan(c,0,8) for c in [(0,0),(2,0),(2,2)]))
caps={k:tri(t) for k,t in json.loads((ROOT/'triangle-composition/inputs/caps.json').read_text())['cap_options'].items()}
base=H|fan((-2,0),7,2)|fan((0,-2),1,2)|{caps[n] for n in ['Nb-','E-','T-']}

def polygon(ts):
 edges=set()
 for t in ts:
  a,b,c=t
  if cross(sub(b,a),sub(c,a))<0:b,c=c,b
  for u,v in [(a,b),(b,c),(c,a)]:
   if (v,u) in edges:edges.remove((v,u))
   else:edges.add((u,v))
 out={a:b for a,b in edges};assert len(out)==len(edges)
 start=min(out);p=start;cycle=[]
 while True:
  assert p not in cycle;cycle.append(p);p=out[p]
  if p==start:break
 assert len(cycle)==len(edges)
 return [p for i,p in enumerate(cycle) if cross(sub(p,cycle[i-1]),sub(cycle[(i+1)%len(cycle)],p))]

record=json.loads((ROOT/'first-surplus-review/centered-left-check.json').read_text())['paths']['left']
P=[tuple(F(*v) for v in p) for p in record['path']]
U,Z=path_requirements(P)
assert U<=base and not Z&base
possible=(base|set(caps.values()))-{caps[n] for n in ['E+','T+','Nb+','Nr-','Nr+']}
assert not Z&possible
# The sigma/reversal has actual endpoint order S to T as well.
sigma=lambda p:(2-p[1],2-p[0])
Ps=[sigma(p) for p in P][::-1]
Us,Zs=path_requirements(Ps)
assert Us=={tri(sigma(p) for p in t) for t in U}
assert Zs=={tri(sigma(p) for p in t) for t in Z}
room=base|{caps[n] for n in ['D-','R+']}
g=geom.check({'triangles':sorted(room),'marked':[(0,0),(2,2)],'require_simple':True},strict=False)
V=polygon(room)
assert replay(V,(0,0),(2,2),P)==12
assert replay(V,(2,2),(0,0),P[::-1])==12
assert replay([sigma(p) for p in V],(0,0),(2,2),Ps)==12
owners=geom.owners_of(list(room));opens={e for e,os in owners.items() if len(os)==2}
Q=0;sN=[];J=[]
for p in {p for t in room for p in t}:
 angles,full=geom.check_fan_angles(list(room),p,owners,opens)
 if geom.label(p)=='A':
  if not full:Q+=3 if angles==[4] else sum(angles)
 elif full:J.append(p)
 elif angles==[4]:sN.append(p)
ledger={'W':g['walls'],'k':len(g['transparent_vertices']),'Q':Q,'sN':len(sN),'J':len(J),'Delta':Q+len(sN)-8,'full_A':g['interior_A']}
assert ledger['W']==18 and ledger['k']==7 and ledger['Delta']==4
result={'status':'PASS','scope':'One missing symbolic inherited implication and sigma; one prescribed geometry control. No trajectory/room search.',
 'input_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'first-surplus-review/centered-left-check.json',ROOT/'third-surplus-review/local-two-unit.txt']},
 'new_implication':{'name':'centerL_centerB_Nbminus_present','path_source':'first-surplus-review/centered-left-check.json left',
 'path':[[str(x) for x in p] for p in P],'reflections':12,'required_triangles':sorted(U),'forbidden_triangles':sorted(Z),
 'ordinary_cap_blockers':sorted(k for k,t in caps.items() if t in Z),'forced_caps':['L-','L+','B-','B+','E-','T-','Nb-'],
 'excluded_ordinary_caps':['E+','T+','Nb+','Nr-','Nr+'],'symbolic_implication':'PASS','ledger':ledger,'vertices':V,'triangles':sorted(room),'forward_reverse':'PASS','sigma':'PASS'}}
(HERE/'check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','implication':result['new_implication']['name'],'reflections':12,'blockers':result['new_implication']['ordinary_cap_blockers'],'ledger':ledger}))
