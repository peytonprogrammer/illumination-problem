"""Exact descent of the two manuscript charts; fixed cov4181 quotient comparison."""
from collections import Counter
from pathlib import Path
import runpy
import sys

here=Path(__file__).resolve().parent
rim=runpy.run_path(str(here/'rim-trees.py'))
cyl=rim['cyl']
rooms=rim['old']['rooms']
base={(-1,-1),(0,-1),(0,-2),(1,-2),(1,-3)}
P=cyl.Origami(base)
O=cyl.Origami(rooms['R22'])
F=[]
for (x,y),(ex,ey) in O.sq:
    images=[((x,y),(ex,ey)),((x,-1-y),(ex,-ey)),((3-x,-1-y),(-ex,-ey))]
    (image,)=[item for item in images if item[0] in base]
    F.append(P.idx[image])
assert set(Counter(F).values())=={3}
for perm,baseperm in ((O.r,P.r),(O.u,P.u)):
    assert all(F[perm[i]]==baseperm[f] for i,f in enumerate(F))

for v in ((4,7),(7,4)):
    r,u=cyl.act(O.r,O.u,cyl.word(*v))
    R,U=cyl.act(P.r,P.u,cyl.word(*v))
    assert all(F[r[i]]==R[f] and F[u[i]]==U[f] for i,f in enumerate(F))
    b=next(row for row in cyl.cycles(r) if any(cyl.incid(O.cells,O.ll[s])==3 for s in row))
    rows=[b,[u[s] for s in b]]
    C,trees=rim['trees'](O,v)
    assert C==30
    for row in rows:
        seq=[F[s] for s in row]
        assert seq==seq[:10]*3 and len(set(seq[:10]))==10
    near=next(k for k,row in enumerate(rows) if any(O.ll[s]==(0,0) for s in row))
    def residues(mark):
        return sorted({i%10 for i,s in enumerate(rows[near]) if O.ll[s]==mark})
    a,b=residues((0,0)),residues((2,2))
    far=rows[1-near]
    regular=[(i,O.ll[s],P.ll[F[s]]) for i,s in enumerate(far) if not O.marked[s]]
    assert all(cyl.incid(base,p)==1 for _,_,p in regular)
    D=[d for d in range(2,C,2) if any(0<(d-(i-m))%C<2*(j-i) for i,j,m,_ in trees[1-near])]
    print(v,'base circumferences',list(map(len,cyl.cycles(R))),'S,T mod 10',a,b,'far regular occurrences',regular,'differences',D)
    assert D==[10,20] and set(a).isdisjoint(b)

sys.path.insert(0,str(rim['old']['base']/'d4-monodromy-blocks'))
import monodromy
cells=set(rooms['cov4181'])
room,t=cyl.PL.room_tuple(cells,(2,3))
(Pi,)=[P for P in monodromy.all_block_systems(list(t),28) if 1<len(P)<28]
indices={s:i for i,B in enumerate(Pi) for s in B}
for mark in ((0,0),(2,0)):
    print('cov4181 mark relative to S',mark,'quotient fibres', [sorted({indices[s] for s in cycle}) for cycle in room.points_at(mark)[1]])
print('cov4181 block sizes',list(map(len,Pi)))
for label,g in zip('abcd',t):
    bg=[indices[g[B[0]]] for B in Pi]
    pairs=Counter(tuple(sorted((indices[i],indices[j]))) for i,j in enumerate(g) if i<j and g[j]==i)
    print(label,'on blocks',bg,'regular swaps',sorted(pairs.items()))
