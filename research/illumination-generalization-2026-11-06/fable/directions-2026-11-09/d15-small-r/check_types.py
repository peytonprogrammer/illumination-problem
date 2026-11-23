"""Independent count of order types for small r: brute force over all cell
subsets of an nx x ny grid, with the d8 test for strict simplicity.
Usage: check_types.py r"""
import sys
from itertools import product
sys.path.insert(0, "../d8-perturbation-test")
from room import is_strictly_simple, status
r = int(sys.argv[1]); W = 2 * r + 4
def canon(nx, ny, cells):
    best = None
    for tr in (0, 1):
        if tr and nx != ny: continue
        for fx in (0, 1):
            for fy in (0, 1):
                out = []
                for (i, j) in cells:
                    a = nx - 1 - i if fx else i; b = ny - 1 - j if fy else j
                    out.append((b, a) if tr else (a, b))
                key = tuple(sorted(out))
                if best is None or key < best: best = key
    return best
total = 0
for nx in range(1, r + 2):
    for ny in range(nx, r + 2):
        seen = set()
        all_cells = [(i, j) for i in range(nx) for j in range(ny)]
        for bits in range(1, 1 << len(all_cells)):
            cells = {c for k, c in enumerate(all_cells) if (bits >> k) & 1}
            if not is_strictly_simple(cells): continue
            verts = [(x, y) for x in range(nx + 1) for y in range(ny + 1) if status(cells, (x, y)) in ("convex", "reflex")]
            if len(verts) != W: continue
            if {v[0] for v in verts} != set(range(nx + 1)) or {v[1] for v in verts} != set(range(ny + 1)): continue
            seen.add(canon(nx, ny, cells))
        total += len(seen)
        if seen: print(nx, ny, len(seen))
print("r", r, "order types", total)
