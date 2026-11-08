"""Exact linear perturbation off the tight face of the fixed147-row cone."""
from pathlib import Path
from fractions import Fraction as F
import json
B=Path(__file__).resolve().parent
r=json.loads((B/'result.json').read_text());c=json.loads((B/'cone.json').read_text());rows=[list(map(F,g)) for g in r['rows']];d=list(map(F,c['delta']));values=list(map(F,c['constraint_values']));zero=[g for g,v in zip(rows,values) if not v]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
piv={}
for g in zero:
 v=[*g,F(1)]
 for k,q in sorted(piv.items()):
  if v[k]:a=v[k];v=[x-a*y for x,y in zip(v,q)]
 k=next((k for k in range(48) if v[k]),None);assert k is not None
 a=v[k];piv[k]=[x/a for x in v]
z=[F(0)]*48
for k,q in sorted(piv.items(),reverse=True):z[k]=q[-1]-sum(q[j]*z[j] for j in range(k+1,48))
assert all(dot(g,z)==1 for g in zero)
zvals=[dot(g,z) for g in rows]
eta=min([F(1)]+[v/(-2*w) for v,w in zip(values,zvals) if v>0 and w<0])
d2=[x+eta*y for x,y in zip(d,z)];assert all(dot(g,d2)>0 for g in rows)
# A single bounded rational approximation is accepted only after exact checks.
scale=max(map(abs,d2));candidate=[F(float(x/scale)).limit_denominator(10**8) for x in d2]
if all(dot(g,candidate)>0 for g in rows):d2=candidate
vals=[dot(g,d2) for g in rows];assert min(vals)>0
out=dict(status='EXACT_STRICT_SURVIVAL_TANGENT',events=147,variables=48,tight_rows=41,tight_rank=41,delta=list(map(str,d2)),constraint_values=list(map(str,vals)),minimum=str(min(vals)),maximum=str(max(vals)),conclusion='All saved signed event determinants increase strictly along one nonsymmetry deformation. For a sufficiently small positive straight perturbation, all147 determinants are positive. This does not assert darkness or absence of other paths.')
(B/'strict-escape.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('delta','constraint_values')},indent=2))
