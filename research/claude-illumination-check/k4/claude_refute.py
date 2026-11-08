"""Try to refute darkness of a candidate room by independent means.

1. Boundary: trace the room boundary from the tiles, count corners, list the B/C points
   that aren't corners (the transparent exceptions).
2. Direction sweep: fold every primitive direction (p, q) with |p|, |q| <= M from the source
   (all D4 images) using claude_verify_lit.fold, an in-room exact tracer independent of the
   origami code; any path reaching the target is checked with Claude's exact checker.
Usage: claude_refute.py room.json M
"""
import json, sys
from math import gcd
from pathlib import Path
from itertools import combinations
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent), str(HERE.parent/'exact-dark'), str(HERE.parent/'refolding')]
from claude_verify_lit import fold
from claude_ray_guard_check import check_path

d = json.loads(Path(sys.argv[1]).read_text()); M = int(sys.argv[2])
tiles = [tuple(sorted(map(tuple, t))) for t in d['triangles']]
s, t = map(tuple, d['marked'])
owners = {}
for x in tiles:
    for e in combinations(x, 2):
        owners.setdefault(e, []).append(x)
bnd = [e for e, o in owners.items() if len(o) == 1]
deg = {}
for a, b in bnd:
    deg.setdefault(a, []).append(b); deg.setdefault(b, []).append(a)
role = lambda p: 'A' if p[0] % 2 == 0 and p[1] % 2 == 0 else ('B' if p[0] % 2 and p[1] % 2 else 'C')
corners, smooth = [], []
for p, nb in deg.items():
    assert len(nb) == 2, ('pinch', p)
    u = (nb[0][0]-p[0], nb[0][1]-p[1]); v = (nb[1][0]-p[0], nb[1][1]-p[1])
    (smooth if u[0]*v[1]-u[1]*v[0] == 0 else corners).append(p)
interior_bc = sorted(p for p in {q for x in tiles for q in x} if p not in deg and role(p) != 'A')
print(json.dumps(dict(boundary_edges=len(bnd), walls=len(corners), smooth_bc=sorted(p for p in smooth if role(p) != 'A'),
                      interior_bc=interior_bc, interior_A=sorted(p for p in {q for x in tiles for q in x} if p not in deg and role(p) == 'A'))))
room = frozenset(tiles); tried = lit = 0
for p in range(-M, M+1):
    for q in range(-M, M+1):
        if gcd(abs(p), abs(q)) != 1:
            continue
        tried += 1
        pts = fold(sorted(room), set(), s, t, (p, q), max_steps=4*M)
        if pts:
            path = [[[c.numerator, c.denominator] for c in x] for x in pts]
            ok, why, _ = check_path(room, path, [s, t])
            print('LIT' if ok else 'fold-reached-but-checker-rejected', (p, q), why, len(pts)-2, 'reflections', flush=True)
            lit += ok
print(json.dumps(dict(directions=tried, lit=lit)))
