"""Named checks at prescribed stretch sizes and in prescribed directions only."""
from itertools import product
from pathlib import Path
import sys
archive=Path(__file__).resolve().parents[2]/'illumination-generalization-2026-11-06/fable/directions-2026-11-09'
sys.path.insert(0,str(archive/'d72-cylinder-test'))
import cyl
rt=cyl.PL

def rect(a,b,c,d):
    return set(product(range(a,b),range(c,d)))

def report(name,cells,source):
    _,g=rt.room_tuple(cells,source)
    degrees=[len(rt.class_congruence(g,[i])) for i in range(4)]
    swaps=[sum(len(c)==2 for c in cyl.cycles(p)) for p in g]
    print(name,'n',len(cells),'canonical degrees',degrees,'two-cycles',swaps)

def lit(cells,s,t,v):
    for x,y in cyl.SHEETS:
        state=(s,(x*v[0],y*v[1]))
        seen=set()
        while state and state not in seen:
            seen.add(state)
            state=cyl.vertex_step(cells,*state)
            if state and state[0]==t: return True
    return False

for H in [5,7]:
    cells=rect(0,5,0,H)|rect(5,8,2,3)|rect(8,13,0,H)
    report(f'DB55 H={H}',cells,(2,2))
    hits=[lit(cells,(2,2),(4,4),(1,2*j)) for j in (25,28)]
    assert hits==([False,True] if H==5 else [True,False])
    print('j=25,28',hits)
for b in [7,9]:
    cells=rect(-b,b,-2,2)|rect(-2,2,-b,b)
    report(f'cross {b}',cells,(6,0))
    print('diagonal pair',lit(cells,(6,0),(0,6),(1,1)))
rooms=dict(cyl.rooms())
report('cov4181',rooms['cov4181'],(2,3))
report('c4181s',rooms['c4181s'],(4,3))
