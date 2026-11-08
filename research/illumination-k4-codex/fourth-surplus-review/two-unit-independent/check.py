"""Independent fixed-path/classification review; no discovery or assignments."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter, defaultdict
import hashlib
import json
import runpy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sources = {
    'peer_proof': ROOT/'surplus-four-local/two-unit.txt',
    'peer_receipt': ROOT/'surplus-four-local/check.json',
    'predecessor': ROOT/'third-surplus-review/local-two-unit.txt',
    'left12': ROOT/'first-surplus-review/centered-left-check.json',
    'caps': ROOT/'zero-surplus-L/guard-incidence-check.json',
    'short': ROOT/'first-surplus-review/square-exchange-check.json',
    'five': ROOT/'second-surplus-review/five-path-check.json',
    'zero': ROOT/'zero-surplus-L/cover-check.json',
    'checker': ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py',
}
data = {k:json.loads(p.read_text()) for k,p in sources.items()
        if p.suffix == '.json'}
guard = runpy.run_path(str(sources['checker']))
tri = lambda t: tuple(sorted(map(tuple,t)))
decode = lambda raw: [tuple(F(*q) for q in p) for p in raw]
caps = {n:tri(t) for n,t in data['caps']['cap_options'].items()}
D = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
sub = lambda a,b: (a[0]-b[0],a[1]-b[1])
cross = lambda a,b: a[0]*b[1]-a[1]*b[0]
dot = lambda a,b: a[0]*b[0]+a[1]*b[1]


def fan(c, sectors):
    x,y=c
    return {tri((c,(x+D[i][0],y+D[i][1]),
                 (x+D[(i+1)%8][0],y+D[(i+1)%8][1]))) for i in sectors}


H = set().union(*(fan(c,range(8)) for c in [(0,0),(2,0),(2,2)]))
sigma = lambda p: (2-p[1],2-p[0])
transform = lambda ts: {tri(sigma(p) for p in t) for t in ts}
P = decode(data['left12']['paths']['left']['path'])
U,Z = guard['path_requirements'](P)
assert len(P)-2 == 12 and P[0] == (0,0) and P[-1] == (2,2)
assert P == [tuple(map(F,p)) for p in data['peer_receipt']['new_implication']['path']]
centerL,centerB = fan((-2,0),[7,0]),fan((0,-2),[1,2])
fixed = H|centerL|centerB|{caps[n] for n in ['Nb-','E-','T-']}
allowed = (fixed|set(caps.values()))-{caps[n] for n in ['Nb+','Nr-','Nr+','E+','T+']}
assert U <= fixed and not Z & allowed
Ps = list(reversed([sigma(p) for p in P]))
Us,Zs = guard['path_requirements'](Ps)
assert Us == transform(U) and Zs == transform(Z)
assert Us <= transform(fixed) and not Zs & transform(allowed)


def polygon(ts):
    edges=set()
    for t in ts:
        a,b,c=t
        if cross(sub(b,a),sub(c,a))<0: b,c=c,b
        for u,v in [(a,b),(b,c),(c,a)]:
            if (v,u) in edges: edges.remove((v,u))
            else: edges.add((u,v))
    outgoing=dict(edges)
    assert len(outgoing)==len(edges)==len(set(outgoing.values()))
    start=min(outgoing); cycle=[start]; p=outgoing[start]
    while p != start:
        assert p not in cycle
        cycle.append(p);p=outgoing[p]
    assert len(cycle)==len(edges)
    return [p for i,p in enumerate(cycle)
            if cross(sub(p,cycle[i-1]),sub(cycle[(i+1)%len(cycle)],p))]


def ledger(ts):
    at=defaultdict(set)
    groups=defaultdict(set)
    h_edges=Counter(tuple(sorted((t[i],t[(i+1)%3]))) for t in H for i in range(3))
    for t in ts:
        a=next(p for p in t if p[0]%2==p[1]%2==0)
        groups[a].add(t)
        for p in t: at[p].add(t)
    Q=J=sN=0; positive=[]; fullA=[]; missing=[]
    for a,parts in groups.items():
        m=len(parts)
        if m==8: fullA.append(a);continue
        q=3 if m==4 else m;Q+=q
        touching=set()
        for t in parts:
            bc=tuple(sorted(p for p in t if p!=a))
            if h_edges[bc]==1:
                touching.add(next(p for p in bc if p[0]%2!=p[1]%2))
        d=len(touching)
        if q-d: positive.append(dict(A=a,m=m,q=q,d=d,e=q-d))
    for p,parts in at.items():
        if p[0]%2==p[1]%2==0:continue
        angle=len(parts)*(45 if p[0]%2==p[1]%2==1 else 90)
        J+=angle==360;sN+=angle==180
        h_parts={t for t in H if p in t}
        if p[0]%2!=p[1]%2 and len(h_parts)==2 and parts==h_parts:
            missing.append(p)
    assert set(fullA)=={(0,0),(2,0),(2,2)}
    V=polygon(ts)
    return dict(W=len(V),Q=Q,J=J,sN=sN,k=J+sN,Delta=Q+sN-8,
                b=sN-len(missing),positive_cells=positive,vertices=V)


# One hand-prescribed geometry, not a generated family of assignments.
Bquarter, Dsingle = fan((0,-2),[0,1]),fan((2,-2),[3])
gap_base=H|Bquarter|Dsingle|{caps[n] for n in ['L+','E-','T-']}
gap_control=gap_base|{caps[n] for n in ['Nb-','R+']}
gap_ledger=ledger(gap_control)
assert (gap_ledger['W'],gap_ledger['k'],gap_ledger['Delta'],gap_ledger['b']) == (20,6,4,2)
assert sorted((p['m'],p['q'],p['d'],p['e']) for p in gap_ledger['positive_cells']) == [(1,1,0,1),(2,2,1,1)]

# Explicit repair of the missing B-quarter/D-single geometry. R/N caps
# stay symbolic. The left/east/top short forcing is justified in review.txt.
gap_paths = {
    'B_two': decode(data['short']['paths']['B_four']['path']),
    'five': decode(data['five']['five_path']),
    'sigma13': decode(data['zero']['paths']['thirteen_sigma']['path']),
}
extra = {caps[n] for n in ['R-','R+','Nb-','Nb+','Nr-','Nr+']}
repairs={}
for name,path in gap_paths.items():
    u,z=guard['path_requirements'](path)
    if name=='B_two':
        required=H|Bquarter
        possible=(H|Bquarter|Dsingle|set(caps.values()))-{caps[n] for n in ['B-','D-','D+','T-']}
    elif name=='five':
        required=gap_base
        possible=gap_base| (extra-{caps['Nb+']})
    else:
        required=gap_base|{caps['Nb+']}
        possible=required|{caps['R-'],caps['R+']}
    assert u<=required and not z&possible,(name,u-required,z&possible)
    if name=='five': assert u<=gap_control and not z&gap_control
    rev=list(reversed([sigma(p) for p in path]))
    ru,rz=guard['path_requirements'](rev)
    assert ru==transform(u) and rz==transform(z)
    repairs[name]=dict(reflections=len(path)-2,symbolic_implication='PASS',sigma='PASS')
out=dict(status='PASS',verdict='SOURCE NEEDS EXPLICIT d0-IN-K SUPPLEMENT; SUPPLEMENT VERIFIED',
         scope='Hand completeness audit plus supplied L12/sigma guards and one prescribed missing-case geometry; three named retained repair paths. No census or discovery.',
         new_centerLB_Nbminus=dict(reflections=12,required=sorted(U),forbidden=sorted(Z),symbolic='PASS',sigma='PASS'),
         missing_case_control=gap_ledger,missing_case_repairs=repairs,
         inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources.values()})
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: L12/sigma implication; missing d0 K-leaf valid W20/k6/Delta4/b2; named-path supplement')
