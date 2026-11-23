"""Replay nine fixed certificates. All slopes come from archived D8 witnesses."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
import json
from math import gcd
from pathlib import Path
import sys

data = next(Path(__file__).resolve().parents[2].glob('illumination-generalization*/fable/directions*'))
archive = data / 'd8-perturbation-test'
sys.path.insert(0, str(archive))
from tracer import advance, trace

S,T = (0,0),(2,2)
cells = {tuple(pt) for pt in next(room['cells'] for room in json.loads((archive/'rooms.json').read_text())
                                 if room['id']=='R22-base')}
records = {r['id']:r for r in map(json.loads,(archive/'results.jsonl').read_text().splitlines())}
# Corner, D8 edit ID suffix, launches from S and T, primitive step counts.
certificates = [
    ((0,-1),'L2-0320',(-8,11),(8,-11),1,3),
    ((0,1),'L1-004',(-2,1),(-2,-1),1,1),
    ((1,-2),'L1-027',(7,-4),(-7,-4),1,1),
    ((1,-1),'L2-0210',(9,-5),(-9,5),1,1),
    ((1,1),'L1-008',(1,1),(-1,-1),1,1),
    ((1,2),'L1-000',(3,2),(3,2),1,1),
    ((3,1),'L2-0210',(9,5),(9,5),1,1),
    ((3,2),'L2-0398',(9,2),(9,2),1,1),
    ((4,1),'L1-021',(4,7),(4,-7),1,1),
]


def incidences(room):
    return Counter((x+i,y+j) for x,y in room for i in (0,1) for j in (0,1))


def leg(start,corner,direction,steps):
    dx,dy=direction
    end,ok,hits,arrival=advance(cells,*map(Fraction,start),Fraction(dx*steps),Fraction(dy*steps))
    assert not ok and end==corner and hits[-1]==corner and len(hits)==steps
    assert all(counts[z] in (2,4) for z in hits[:-1])
    return hits,tuple(v/steps for v in arrival)


counts=incidences(cells)
assert {z for z,k in counts.items() if k==3}=={c[0] for c in certificates}
scale=12
scaled={(scale*x+i,scale*y+j) for x,y in cells for i in range(scale) for j in range(scale)}
supports=[]
for corner,edit,vs,vt,i,j in certificates:
    rec=records['R22-'+edit]
    w=next(p['witness'] for p in rec['pairs'] if p['marks'])
    absolute=tuple(abs(x)//gcd(*w) for x in w)
    assert absolute==tuple(map(abs,vs))==tuple(map(abs,vt))
    left,vin=leg(S,corner,vs,i)
    right,win=leg(T,corner,vt,j)
    assert vin==tuple(-x for x in win)
    support=set(left+right)
    supports.append(support)
    # Deterministic check of the stated 1/12 local repair on the same ray.
    x,y=(scale*t for t in corner)
    (cap,)={(x+u,y+v) for u in (-1,0) for v in (-1,0)}-scaled
    repaired=scaled|{cap}
    end,ok,_=trace(repaired,(0,0),tuple(scale*(i+j)*v for v in vs))
    assert ok and end==tuple(scale*t for t in T)
    print(corner,edit,'internal lattice sites',sorted(support),'straight join and 1/12 repair verified')
assert all(a.isdisjoint(b) for a,b in combinations(supports,2))
assert [len(s) for s in supports]==[3]+[1]*8

covers=json.loads((data/'d64-finite-case/data/covers.json').read_text())['rooms']
control=sorted((r for r in covers if r['normalized']),key=lambda r:(r['n'],r['cells']))[4181]
reflex={p for p,k in incidences(control['cells']).items() if k==3}
source_class={p for p in reflex if (p[0]%2,p[1]%2)==(0,1)}
failed_class={p for p in reflex if (p[0]%2,p[1]%2)==(0,0)}
assert source_class=={(6,3)} and not failed_class
print('cov4181 source-parity reflexes',sorted(source_class),'failed-parity reflexes',sorted(failed_class))
