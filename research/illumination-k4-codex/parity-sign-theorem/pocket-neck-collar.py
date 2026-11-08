"""Four collar weights versus existing reflection-load identities; no search."""
from pathlib import Path
import json
b=Path(__file__).resolve().parent
I=((1,0),(0,1));D=((0,1),(1,0));H=((1,0),(0,-1));R=((0,-1),(1,0));V=((-1,0),(0,1));u=(0,-1)
def mul(A,B):return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def mv(A,x):return tuple(sum(a*y for a,y in zip(row,x)) for row in A)
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
weights=[u]
for _ in range(3):weights.append(mv(R,weights[-1]))
assert len(set(weights))==4 and mv(V,u)==u
prefixes=[]
for swap in (False,True):
 for sx in (-1,1):
  for sy in (-1,1):prefixes.append(((0,sx),(sy,0)) if swap else ((sx,0),(0,sy)))
# These six words are the local maps already stated in Section2.
words={'D':[D],'DH':[D,H],'DHD':[D,H,D],
       'DHDH':[D,H,D,H],'HDH':[H,D,H],'HD':[H,D]}
def product(mats):
 A=I
 for B in mats:A=mul(A,B)
 return A
assert product(words['DHD'])==V
assert [word for word,mats in words.items() if mv(product(mats),u)==u]==['DHD']
rows=[]
for g in prefixes:
 for word,mats in words.items():
  G=product(mats);gout=mul(g,G)
  nin=weights.index(mv(g,u));nout=weights.index(mv(gout,u))
  nu=[0]*4;nu[nin]+=1;nu[nout]-=1
  from_necks=tuple(sum(weights[j][k]*nu[j] for j in range(4)) for k in range(2))
  load=mv(g,sub(u,mv(G,u)))
  assert from_necks==load
  # Same local development but an actual moving-corner source:
  partial=sub(load,mv(g,u));assert partial==tuple(-x for x in mv(gout,u))
  rows.append(dict(prefix=g,existing_map=word,entry=nin,exit=nout,
                   complete_load=load,moving_corner_partial=partial))
central=[]
for g in prefixes:
 assert mv(mul(g,V),u)==mv(g,u)
 central.append(tuple(-2*x for x in mv(g,u)))
assert len(rows)==48 and len(central)==8
out=dict(status='PRESCRIBED_COLLAR_LOAD_IDENTITIES_PASS',existing_return_prefix_controls=48,
 moving_corner_partial_controls=48,central_fixed_flank_controls=8,
 canonical_weights=weights,absolute_coefficients=[0,1],
 rows=rows,scope='Given six local return maps and D4 transports only. Annulus geometry and relative material marking are hand-proof obligations.',
 universal_actual_unequal_neck_counts='OPEN',optical_discovery_runs=0)
(b/'pocket-neck-collar.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
