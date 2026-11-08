from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
reads=[]
def read(rel):
 p=ROOT/rel;reads.append(p);return json.loads(p.read_text())
def decode(ts):return {tuple(sorted(map(tuple,t))) for t in ts}
old=read('fourth-surplus-review/three-unit-b1-independent/check.json')
fixtures=read('fourth-surplus-review/mixed-e2-e1/critical-L-check.json')
guards=dict(old['named_guards'])
assert len(guards)==148
for rel in ['fourth-surplus-review/peer-E4-six-independent/check.json','fourth-surplus-review/peer-N70-four-N0-six-independent/check.json','fourth-surplus-review/west-D1-search/check.json']:
 for name,g in read(rel)['fixed_paths'].items():guards[rel+':'+name]=g
rows=[]
for name in fixtures['optically_open_fixture_names']:
 f=fixtures['hand_forced_fixtures'][name];room=decode(f['triangles']);matches=[]
 for label,g in guards.items():
  u,z=decode(g['required']),decode(g['forbidden'])
  if u<=room and not z&room:matches.append({'guard':label,'reflections':g['reflections']})
 rows.append({'fixture':name,'matches':matches,'old_geometry_status':f['status']})
covered=[r for r in rows if r['matches']];uncovered=[r['fixture'] for r in rows if not r['matches']]
# ONE specifically named accepted B4 path, no other stored paths read.
from fractions import Fraction as F
import sys
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements
from boundary_replay import replay,on,sub,cross,dot
path_data=read('third-surplus-review/local-three-unit-check.json')['new_paths']['B4']
B4=[tuple(F(*v) for v in p) for p in path_data]
sigma=lambda p:(2-p[1],2-p[0])
P=[sigma(p) for p in B4[::-1]]
u,z=path_requirements(P)
chosen=guards['three_missB_EC_0']
assert u==decode(chosen['required']) and z==decode(chosen['forbidden'])
physical_rows=[]
for row in covered:
 fixture=fixtures['hand_forced_fixtures'][row['fixture']];V=list(map(tuple,fixture['vertices']));room=decode(fixture['triangles'])
 assert u<=room and not z&room
 assert replay(V,(0,0),(2,2),P)==replay(V,(2,2),(0,0),P[::-1])==4
 assert replay([sigma(v) for v in V],(0,0),(2,2),[sigma(p) for p in P[::-1]])==4
 assert all(not on((2,2),a,b) for a,b in zip(P[:-2],P[1:-1]))
 assert all(not on((0,0),a,b) for a,b in zip(P[1:],P[2:]))
 walls=[]
 for a,p,b in zip(P,P[1:],P[2:]):
  hit=[(v,w) for v,w in zip(V,V[1:]+V[:1]) if on(p,v,w) and p not in (v,w)]
  assert len(hit)==1;v,w=hit[0];axis=sub(w,v);incoming=sub(p,a)
  reflected=tuple(2*dot(incoming,axis)*axis[k]/dot(axis,axis)-incoming[k] for k in (0,1))
  assert cross(reflected,sub(b,p))==0 and dot(reflected,sub(b,p))>0;walls.append(hit[0])
 q=P[-1]
 for a,b in walls[::-1]:
  axis=sub(b,a);v=sub(q,a);q=tuple(a[k]+2*dot(v,axis)*axis[k]/dot(axis,axis)-v[k] for k in (0,1))
 assert cross(sub(P[1],P[0]),q)==0 and dot(sub(P[1],P[0]),q)>0
 physical_rows.append({'fixture':row['fixture'],'reflections':4,'firstwall_reverse_sigma':'PASS','unfolded_actual_T':list(map(str,q))})
print('SAME sigmaB4 exact path',[[str(x) for x in p] for p in P])
print('U/Z',len(u),len(z))
# Derive each guard tile owner by its even-even A vertex for a readable lemma.
owned=lambda ts:[{'A':next([x,y] for x,y in t if x%2==y%2==0),'triangle':t} for t in sorted(ts)]
DIRECTIONS=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def fan(a,sectors):return {tuple(sorted((a,(a[0]+DIRECTIONS[i%8][0],a[1]+DIRECTIONS[i%8][1]),(a[0]+DIRECTIONS[(i+1)%8][0],a[1]+DIRECTIONS[(i+1)%8][1])))) for i in sectors}
H=set().union(*(fan(a,range(8)) for a in ((0,0),(2,0),(2,2))))
minimum=H|fan((-2,0),(0,1))|fan((4,2),(3,4))
assert u<=minimum
assert z==fan((-2,0),(2,))|fan((0,2),(0,))|fan((4,2),(2,5))
out={'status':'FROZEN_GUARD_TRANSFER_ONLY','named_fixture_count':len(rows),'guard_count':len(guards),'covered_count':len(covered),'stronger_lemma_minimum':sorted(minimum),'same_sigma_B4_path':[[str(x) for x in p] for p in P],'required':sorted(u),'forbidden':sorted(z),'required_owners':owned(u),'forbidden_owners':owned(z),'physical_replay':physical_rows,'rows':rows,'remaining_named_fixtures':uncovered,'limits':'Only fixed eleven supplied triangle sets and148stored guards plus8specified new actualpaths. No rooms generated, archive, candidate rays/directions/words or search. Noncoverage does not imply darkness. Underlying guard validity inherited; new matches require actual path retrieval/physical check.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in reads+[Path(__file__)]}}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('Matched',len(covered),'of',len(rows),'against',len(guards),'supplied guards')
for r in covered:print(r['fixture'],r['matches'])
print('Uncovered:',uncovered)
