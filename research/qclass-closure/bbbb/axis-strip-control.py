"""Test the horizontal and vertical common open strips on three named rooms."""
from collections import Counter
from itertools import combinations, product
from math import gcd
from pathlib import Path
import sys
archive = Path(__file__).resolve().parents[2] / 'illumination-generalization-2026-11-06/fable/directions-2026-11-09/d72-cylinder-test'
sys.path.insert(0,str(archive))
import cyl

def classes(r,up,decomp,s,t):
    if not decomp.cc(s,t):
        return set()
    for step in (up,cyl.inv(up)):
        i,h=s,0
        while decomp.reg[decomp.row[i]]:
            if decomp.row[i]==decomp.row[t]:
                u=0
                while i!=t: i,u=r[i],u+1
                C=len(decomp.rows_saved[decomp.row[t]])
                if not h: return {(1,0)}
                b=h & -h
                if u%(C & -C) or h%(C & -C):
                    g=gcd(u,h)
                    return {(u//g%2,h//g%2)}
                return {(0,1),(1,1)} if b==C & -C else {(0,1),(1,1),(1,0)}
            i,h=step[i],h+1
            if i==s: break
    raise AssertionError('common strip has no row connection')

rooms=dict(cyl.rooms())
cross={(x,y) for x in range(-7,7) for y in range(-7,7) if -2<=x<2 or -2<=y<2}
for name,cells,example in [('DB55',rooms['DB55'],((2,2),(10,2))),('cross7',cross,((6,0),(0,6))),('cov4181',rooms['cov4181'],((2,3),(4,3)))]:
    O=cyl.Origami(cells)
    pairs=cyl.pairs_of(cells)
    hits={pair:set() for pair in pairs}
    for vertical in (False,True):
        r,up=cyl.act(O.r,O.u,cyl.word(0,1)) if vertical else (O.r,O.u)
        d=cyl.Decomp(O,r,up)
        d.rows_saved=cyl.cycles(r)
        for s,t in pairs:
            for a,b in product(cyl.SHEETS,repeat=2):
                found=classes(r,up,d,O.lift(s,a),O.lift(t,b))
                hits[s,t].update((y,(x+y)%2) if vertical else (x,y) for x,y in found)
    print(name,sorted(Counter(map(len,hits.values())).items()),'example',sorted(hits[tuple(sorted(example))]))
