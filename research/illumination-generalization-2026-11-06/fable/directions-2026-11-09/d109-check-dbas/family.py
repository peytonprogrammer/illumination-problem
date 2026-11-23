"""For every prime n=44+l<=NMAX: both least axial twists fix every lattice lift (computed
decomposition), the room is a 12-wall, 4-reflex strictly simple room; and for the members with
no one-reversal slope, whether d103's find_path lights the pair at all."""
import sys
from pathlib import Path
from cylinders import analyse
from room import cells, marks
from path import isprime
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'd103-twenty-check'))
import tracer as T103
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 400
bad = 0
for n in range(45, NMAX + 1):
    if not isprime(n): continue
    o = analyse(n - 44)
    ok = o['walls'] == 12 and o['reflex'] == 4 and not o['H']['levels_moved'] and not o['V']['levels_moved'] and o['V']['lambda'] == 24
    bad += not ok
    print(f"n={n} l={n-44} walls={o['walls']} r={o['reflex']} lamH={o['H']['lambda']} lamV={o['V']['lambda']} all-lattice-lifts-fixed={ok}")
print("members failing:", bad)
for l in (23, 29, 45):
    S, T, _ = marks(l)
    v = T103.find_path(cells(l), S, T, 6)
    print(f"no-one-reversal member l={l} n={44+l}: d103 find_path(R=6) -> {v}")
