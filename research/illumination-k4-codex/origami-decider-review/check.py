"""Prescribed permutation algebra and builder controls; no orbit or ray search."""
from pathlib import Path
import itertools,importlib.util,json
r=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('frozen_peer',r/'inputs/origami_dark.py')
peer=importlib.util.module_from_spec(spec);spec.loader.exec_module(peer)

def inv(p): return tuple(p.index(i) for i in range(len(p)))
def compose(*ps):
    out=tuple(range(len(ps[0])))
    for p in reversed(ps): out=tuple(p[x] for x in out)
    return out

def vertex_cycle(R,U): return compose(U,R,inv(U),inv(R))
def canonical(R,U,labels,s):
    todo=[s]; mapping={s:0}
    for x in todo:
        for y in (R[x],U[x]):
            if y not in mapping: mapping[y]=len(todo);todo.append(y)
    return tuple(mapping[R[x]] for x in todo),tuple(mapping[U[x]] for x in todo),tuple(labels[x] for x in todo)

algebra=canonical_checks=0
for n in range(1,5):
    for R in itertools.permutations(range(n)):
        for U in itertools.permutations(range(n)):
            k=vertex_cycle(R,U)
            for RR,UU in [(R,compose(U,inv(R))),(compose(R,inv(U)),U)]:
                assert vertex_cycle(RR,UU)==k
                algebra+=1
            labels=tuple(str(i) for i in range(n))
            p=tuple(reversed(range(n))); pi=inv(p)
            RP=compose(p,R,pi); UP=compose(p,U,pi)
            labP=tuple(labels[pi[i]] for i in range(n))
            for s in range(n):
                expected=canonical(R,U,labels,s)
                assert peer.canon(R,U,labels,s)==expected
                assert peer.canon(RP,UP,labP,p[s])==expected
                canonical_checks+=1

fixtures=[
    ('square-interior-to-wall',[(0,0),(2,0),(2,2),(0,2)],(1,1),(1,0)),
    ('square-wall-to-interior',[(0,0),(2,0),(2,2),(0,2)],(1,0),(1,1)),
    ('diagonal-wall-marks',[(0,0),(2,0),(2,2)],(1,1),(1,0)),
    ('L-interior',[(0,0),(4,0),(4,2),(2,2),(2,4),(0,4)],(1,3),(3,1)),
    ('L-wall-start',[(0,0),(4,0),(4,2),(2,2),(2,4),(0,4)],(2,3),(3,1))]
results=[]
for label,V,S,T in fixtures:
    R,U,labels,s0=peer.build(V,S,T); n=len(R)
    assert sorted(R)==sorted(U)==list(range(n))
    k=vertex_cycle(tuple(R),tuple(U))
    assert all(labels[i]==labels[k[i]] for i in range(n))
    assert labels[s0]=='S' and 'T' in labels
    # Any allowed smooth source is regular: its lower-left vertex cycle is fixed.
    assert all(k[i]==i for i in range(n) if labels[i] in ('S','T'))
    C=peer.canon(R,U,labels,s0)
    results.append(dict(label=label,squares=n,start_component_squares=len(C[0]),target_lifts=labels.count('T')))

# Endpoint-domain hole: a directly visible terminal corner is never labeled T.
V=[(0,0),(2,0),(2,2),(0,2)]
R,U,labels,s0=peer.build(V,(1,1),(0,0))
assert labels.count('T')==0
result=dict(status='PASS_WITH_DOMAIN_RESTRICTION',shear_identities=algebra,
    relabeling_and_root_checks=canonical_checks,builder_fixtures=results,
    unsupported_corner_target=dict(source=[1,1],target=[0,0],direct_visibility=True,target_labels=labels.count('T')),
    scope='permutation identities, canonicalization covariance and fixed builder controls only; no darkness orbit run')
(r/'check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
