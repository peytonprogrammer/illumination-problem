"""Exact tests of fixed physical pairs across the stored D72 charts."""
from pathlib import Path
from math import gcd
import runpy
from itertools import combinations
rim=runpy.run_path(str(Path(__file__).with_name('rim-trees.py')))
old=rim['old']; cyl=rim['cyl']

def chart(O,v):
    result=rim['trees'](O,v)
    if not result:return None
    C,trees=result
    r,u=cyl.act(O.r,O.u,cyl.word(*v))
    row=next(q for q in cyl.cycles(r) if any(cyl.incid(O.cells,O.ll[s])==3 for s in q))
    assert C==2*len(O.cells)
    contours=[[O.ll[s] for s in row],[O.ll[u[s]] for s in row]]
    good=[{x for x in range(2,C,2) if any(0<(x-i+m)%C<2*(j-i) for i,j,m,_ in es)} for es in trees]
    sig=tuple(sorted(tuple(sorted(j-i for i,j,_,_ in es)) for es in trees))
    return contours,good,sig

def test(c,S,T):
    contours,good,_=c
    for side,ps in enumerate(contours):
        a=[i for i,z in enumerate(ps) if z==S];b=[i for i,z in enumerate(ps) if z==T]
        if a:
            assert b and len(a)==len(b)==4
            ds={(i-j)%len(ps) for i in a for j in b}
            return ds,good[1-side]
    raise AssertionError

for name,report in old['data'].items():
    if report['group']!='BBBB' and name!='R22':continue
    O=cyl.Origami(old['rooms'][name])
    vs={tuple(p[k][0]) for p in report['pairs'] for k in ('cc','lit') if p.get(k)}
    if name=='R22':vs={(4,7),(7,4)}
    charts={v:c for v in sorted(vs) if (c:=chart(O,v))}
    if not charts:continue
    misses={}; ranks={}
    for p in report['pairs']:
        S,T=tuple(p['S']),tuple(p['T'])
        bad=[]
        for v,c in charts.items():
            d,e=test(c,S,T)
            if not d&e:bad.append(v)
        misses[S,T]=bad
        ranks[S,T]=len({charts[v][2] for v in bad})
    best=max(ranks,key=ranks.get)
    print(name,'charts',len(charts),'signatures',len({c[2] for c in charts.values()}),'pairs missed by all',sum(len(b)==len(charts) for b in misses.values()),'of',len(misses),'most distinct misses',best,ranks[best])
    for v in misses[best]:
        d,e=test(charts[v],*best);print(v,'wanted',sorted(d),'available',sorted(e),'gcd',gcd(2*len(O.cells),*e))

# Full continuum control for CR34. In one chart a pair missed by the
# open-cylinder and opposite-rim tests must have q*x and p*y integral.
from fractions import Fraction
for v in ((1,2),(1,3)):
    cells=old['rooms']['CR34']
    m=abs(v[1])
    fine={(m*x+i,m*y+j) for x,y in cells for i in range(m) for j in range(m)}
    O=cyl.Origami(fine)
    C,sides=rim['trees'](O,v)
    r,u=cyl.act(O.r,O.u,cyl.word(*v))
    row=next(row for row in cyl.cycles(r) if any(cyl.incid(O.cells,O.ll[s])==3 for s in row))
    top=row[:]
    while True:
        top=[u[s] for s in top]
        if any(cyl.incid(O.cells,O.ll[s])==3 for s in top):break
    coords=[[O.ll[s] for s in R] for R in (row,top)]
    misses=[]; checked=0; covered=set()
    for side,cont in enumerate(coords):
        reps={}
        for i,z in enumerate(cont):
            if z[1]%m==0 and cyl.incid(fine,z)==4:
                reps.setdefault(z,[]).append(i)
        good={x for x in range(1,C) if any(0<(x-i+a)%C<2*(j-i) for i,j,a,_ in sides[1-side])}
        assert all(len(a)==4 for a in reps.values()) and not covered.intersection(reps)
        covered.update(reps)
        for (S,A),(T,B) in combinations(reps.items(),2):
            checked+=1
            if not any((a-b)%C in good for a in A for b in B):
                misses.append(tuple(tuple(Fraction(t,m) for t in z) for z in (S,T)))
    assert covered=={z for z in set(O.ll) if z[1]%m==0 and cyl.incid(fine,z)==4}
    assert not misses
    print('grid marks and same-rim pairs',len(covered),checked)
    print('CR34 single-chart continuum two-traversal misses',v,len(misses),misses[:1])
