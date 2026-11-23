"""Exact Fraction geometry replay using the separate Python cylinder implementation."""
from pathlib import Path
import sys
base=Path(__file__).resolve().parent
sys.path.insert(0,str(next(base.parents[1].glob('illumination-generalization*/fable/directions*/d13-cylinder-cover'))))
from ill import run
from xset import intersect
r=base/(sys.argv[1]+'.room')
f=list(map(int,r.read_text().split()[2:]));cells=set(zip(f[::2],f[1::2]))
ds=[tuple(map(int,l.split())) for l in r.with_suffix('.dirs').read_text().splitlines()]
live,hist=run(cells,ds,verbose=True)
assert all(len(V)==1 for c,V,Q in live)
pts=[(V[0],Q) for c,V,Q in live]
def contains(Q,P):
    return any(intersect((P,),A) for c,A in Q)
from itertools import combinations
remaining=[(s,t) for (s,q),(t,r) in combinations(pts,2) if contains(q,t) and contains(r,s)]
assert all(all(c.denominator==1 for c in s+t) for s,t in remaining)
print("only grid pairs remain",len(remaining),flush=True)
