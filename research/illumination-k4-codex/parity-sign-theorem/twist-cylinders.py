"""Exact cellular homology of two prescribed origami foliations; no orbit search."""
import sys
if not __debug__:
    raise RuntimeError('Run without -O: exact certificate checks are required')
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import importlib.util
import json, hashlib
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('twist_origami',B/'inputs/twist_origami.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def cycles(p):
    assert sorted(p)==list(range(len(p)))
    unseen=set(range(len(p))); out=[]
    while unseen:
        x=min(unseen); c=[]
        while x in unseen:
            unseen.remove(x); c.append(x); x=p[x]
        assert x==c[0]
        out.append(c)
    return out

def add(row,k,v):
    row[k]=row.get(k,F(0))+v
    if not row[k]: del row[k]

def reduce(row,basis):
    row={k:F(v) for k,v in row.items() if v}
    for k,b in sorted(basis.items()):
        if k in row:
            a=row[k]
            for j,v in b.items(): add(row,j,-a*v)
    return row

def span(rows,basis=None):
    basis={} if basis is None else dict(basis)
    for row in rows:
        row=reduce(row,basis)
        if row:
            k=min(row); a=row[k]
            basis[k]={j:v/a for j,v in row.items()}
    return basis

def inspect(r,u):
    n=len(r); assert n==len(u)
    cycles(r); cycles(u)
    todo=[0]; connected={0}
    for s in todo:
        for t in (r[s],u[s]):
            if t not in connected: connected.add(t); todo.append(t)
    assert len(connected)==n
    parent=list(range(4*n))
    def root(x):
        while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def union(x,y): parent[root(x)]=root(y)
    for s in range(n):
        for a,b,t in ((1,0,r[s]),(2,3,r[s]),(3,0,u[s]),(2,1,u[s])):
            union(4*s+a,4*t+b)
    edges=[(root(4*s),root(4*s+1)) for s in range(n)]+[(root(4*s),root(4*s+3)) for s in range(n)]
    def boundary(row):
        out={}
        for e,a in row.items():
            p,q=edges[e]; add(out,p,-a); add(out,q,a)
        return out
    faces=[]
    for s in range(n):
        row={}
        for e,a in ((s,1),(n+r[s],1),(u[s],-1),(n+s,-1)): add(row,e,F(a))
        assert not boundary(row)
        faces.append(row)
    fb=span(faces); assert len(fb)==n-1
    v=len({root(i) for i in range(4*n)}); h1=n+2-v
    assert h1%2==0
    assert len(span([{p:-F(1),q:F(1)} for p,q in edges if p!=q]))==v-1
    result={'squares':n,'vertices':v,'face_rank':len(fb),'genus':h1//2,'H1_dimension':h1}
    for name,p,offset in (('horizontal',r,0),('vertical',u,n)):
        cs=cycles(p); cores=[{offset+s:F(1) for s in c} for c in cs]
        assert all(not boundary(c) for c in cores)
        basis=span(cores,fb)
        result[name]={'row_cycle_count':len(cs),'row_cycle_lengths':sorted(map(len,cs)),
            'core_homology_rank':len(basis)-len(fb),
            'rank_one_sufficient_condition':len(basis)-len(fb)==1,
            'reduced_core_rows':[{str(k):str(a) for k,a in sorted(reduce(c,fb).items())} for c in cores]}
    return result

room=json.loads((B/'inputs/room.json').read_text())
r,u,lab,s0=m.build(list(map(tuple,room['vertices'])),*map(tuple,room['marked']))
main=inspect(r,u)
assert main['squares']==112 and main['genus']==28
assert all(main[d]['core_homology_rank']==15 for d in ('horizontal','vertical'))
# Prescribed cellular controls: torus and a three-square genus-two L origami.
torus=inspect([0],[0]); assert torus['genus']==1
assert all(torus[d]['core_homology_rank']==1 for d in ('horizontal','vertical'))
lshape=inspect([1,0,2],[2,1,0]); assert lshape['genus']==2
assert all(lshape[d]['core_homology_rank']==2 for d in ('horizontal','vertical'))
stacked=inspect([0,1],[1,0])
assert stacked['genus']==1 and stacked['horizontal']['row_cycle_count']==2
assert all(stacked[d]['core_homology_rank']==1 for d in ('horizontal','vertical'))
# Four-direction convex balance, exact arithmetic; one prescribed nonaxis vector.
p,q,a,b=F(5),F(11),F(12),F(12)
A=a*q; C=b*p
weights=[F(1,4)-p/(2*A),F(1,4)+p/(2*A),F(1,4)-q/(2*C),F(1,4)+q/(2*C)]
directions=[(p+A,q),(p-A,q),(p,q+C),(p,q-C)]
assert min(weights)>0 and sum(weights)==1
assert all(sum(t*w[j] for t,w in zip(weights,directions))==0 for j in (0,1))
result={'status':'EXACT_STRUCTURAL_PASS','scope':'Single frozen room; only horizontal/vertical cellular core ranks. No lighting, shear-orbit or ray searches.',
    'input_sha256':{str(f.relative_to(B)):hashlib.sha256(f.read_bytes()).hexdigest() for f in (B/'inputs/room.json',B/'inputs/twist_origami.py')},
    'room':main,'controls':{'one_square_torus':torus,'three_square_L':lshape,'two_square_stacked_torus':stacked},
    'positive_balance_control':{'directions':[[str(x) for x in w] for w in directions],'weights':list(map(str,weights))},
    'criterion_applies':all(main[d]['rank_one_sufficient_condition'] for d in ('horizontal','vertical'))}
(B/'twist-cylinders.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('room','controls')},indent=2))
for name,data in [('room',main),('torus',torus),('L',lshape)]:
    print(name, {k:v for k,v in data.items() if k not in ('horizontal','vertical')},
        {d:{k:v for k,v in data[d].items() if k!='reduced_core_rows'} for d in ('horizontal','vertical')})
