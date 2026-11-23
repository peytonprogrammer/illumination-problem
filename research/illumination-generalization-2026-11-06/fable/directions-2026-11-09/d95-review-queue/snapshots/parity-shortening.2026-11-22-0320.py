"""Replay the one fixed line in the three-chamber test; no direction search."""
from itertools import product
from pathlib import Path
import sys

archive = Path(__file__).resolve().parents[2] / 'illumination-generalization-2026-11-06/fable/directions-2026-11-09'
sys.path.insert(0, str(archive / 'd72-cylinder-test'))
import cyl

def replay(X,Y):
    starts = 0,3+X,6+X+Y
    cells = set(product(range(9+X+Y), [1]))
    cells.update((x,y) for a in starts for x in range(a,a+3) for y in range(3))
    S,T = (2,1),(4+X,1)
    outcomes = []
    for sx,sy in product((-1,1),repeat=2):
        state = S,(2*sx,sy)
        seen = set()
        while state and state not in seen and state[0]!=T:
            seen.add(state)
            state = cyl.vertex_step(cells,*state)
        outcomes.append('target' if state and state[0]==T else 'repeat' if state else 'corner')
    print(X,Y,S,T,outcomes)
    return 'target' in outcomes

for k in (0,2):
    L = 4+12*k
    assert not replay(L,L)
    assert replay(L-2,L)
