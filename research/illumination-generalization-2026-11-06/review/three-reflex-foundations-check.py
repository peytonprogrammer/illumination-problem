#!/usr/bin/env python3
"""Prescribed finite turn-word partition/base pins; no room/ray census."""
from pathlib import Path
from collections import Counter
from itertools import permutations
import hashlib,json
base=Path(__file__).parents[1];workspace=Path.cwd()
# Independent enumeration of ordered positive gap compositions, not labelled subsets.
compositions=[(a,b,10-a-b) for a in range(1,9) for b in range(1,10-a) if 10-a-b>0]
assert len(compositions)==36
classes=sorted(set(tuple(sorted(t)) for t in compositions))
expected=[(1,1,8),(1,2,7),(1,3,6),(1,4,5),(2,2,6),(2,3,5),(2,4,4),(3,3,4)]
assert classes==expected
counts={t:10*len(set(permutations(t)))//3 for t in classes};assert sum(counts.values())==120
coordinator=json.loads((workspace/'.context/codex-proof-verification/specialist-ideas/geometric-reduction-goals/three-reflex-turn-types.json').read_text())
assert {tuple(row['cyclic_gap_multiset']):row['labelled_words'] for row in coordinator['types']}==counts
review=json.loads((base/'construction/whole-staircase-independent-review.json').read_text())
pins=[]
for name,pin in review['source_sha256'].items():
 actual=hashlib.sha256((workspace/name).read_bytes()).hexdigest();assert actual==pin;pins.append({'path':name,'sha256':actual,'pass':True})
assert hashlib.sha256((base/'construction/whole-staircase-independent-review.md').read_bytes()).hexdigest()==review['review_sha256']
accept=json.loads((base/'review/whole-staircase-acceptance.json').read_text())
for name,pin in accept['source_sha256'].items():assert hashlib.sha256((base/'review'/name).read_bytes()).hexdigest()==pin
P=[(2,2),(2,10),(10,10),(10,4),(6,4),(6,0),(14,0),(14,14),(0,14),(0,2)]
Q=[(0,0),(40,0),(40,12),(12,12),(12,16),(8,16),(8,20),(4,20),(4,40),(0,40)]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def gaps(poly):
 assert sum(cross(a,b) for a,b in zip(poly,poly[1:]+poly[:1]))>0
 indices=[i for i,p in enumerate(poly) if cross(sub(p,poly[i-1]),sub(poly[(i+1)%len(poly)],p))<0]
 assert len(indices)==3
 return indices,sorted((indices[(i+1)%3]-indices[i])%10 for i in range(3))
assert gaps(P)[1]==[1,1,8] and gaps(Q)[1]==[2,2,6]
scaled=[(2*x,2*y) for x,y in P]
S=(2,6);T=(14,2)
# Horizontal bands of the accepted scaled spiral, read from its actual walls.
bands=[(0,4,[(12,28)]),(4,8,[(0,4),(12,28)]),(8,20,[(0,4),(20,28)]),(20,28,[(0,28)])]
assert any(lo<S[1]<hi and any(a<S[0]<b for a,b in intervals) for lo,hi,intervals in bands)
assert any(lo<T[1]<hi and any(a<T[0]<b for a,b in intervals) for lo,hi,intervals in bands)
assert all(v%2==0 for p in [S,T] for v in p)
out={'status':'PASS_PREREQUISITES_ONLY','method':'Independent ordered positive gap compositions plus dihedral S3 quotient; existing frozen base source hashes and prescribed existing control turns. No room/ray search.','gap_types':[{'type':t,'labelled_words':counts[t]} for t in classes],'ordered_compositions':36,'labelled_subsets_total':120,'base_scope':'Every finite strictly simple real orthogonal polygon with <=8 maximal walls, every distinct real interior pair.','base_pin_checks':pins,'base_independent_review_hash_pass':True,'base_acceptance_receipt_hashes_pass':True,'known_control_gap_types':{'three_consecutive_spiral':gaps(P),'four_band_axis_obstruction':gaps(Q)},'scaled_spiral_endpoint_stress':{'polygon':scaled,'S':S,'T':T,'both_actual_interior_even_even':True,'r':3,'W':10,'physical_illumination_verdict':'NOT established by this check','geometry_simple_inherited_by_positive_uniform_scaling':True},'optical_progress_claimed':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'gap_types':8,'source_pins':len(pins),'control_types':[[1,1,8],[2,2,6]],'new_optical_theorem':False}))
