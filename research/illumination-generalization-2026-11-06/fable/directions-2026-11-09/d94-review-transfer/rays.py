"""d94: exact lattice-direction billiard check between two lattice points of a polyomino room.
A ray from lattice point s in primitive direction (p,q) is tracked by its cell; between consecutive
lattice points it crosses |p|-1 vertical and |q|-1 horizontal grid lines (coprime => never simultaneously),
then reaches a lattice point. Corner (pole or zero) => stop. Reaching t => lit. Period detection on states."""
import sys
from math import gcd
sys.path.insert(0, __import__('os').path.dirname(__file__))
from cross import setup, cycles, room

def run(cells, s, t, P):
    idx, n, S, g = setup(cells)
    cyc = {}
    for k in g:
        for c in cycles(g[k]):
            for a in c: cyc[(k, a)] = len(c)
    hits = []
    dirs = [(p, q) for p in range(-P, P + 1) for q in range(-P, P + 1) if gcd(p, q) == 1]
    for p, q in dirs:
        # starting cells: for axis directions try both adjacent cells (same physical ray)
        sx, sy = s
        cx = [sx if p > 0 else sx - 1] if p else [sx - 1, sx]
        cy = [sy if q > 0 else sy - 1] if q else [sy - 1, sy]
        starts = [(i, j) for i in cx for j in cy if (i, j) in idx]
        if not starts or (p == 0 and len(starts) < 2 and len(cx) == 2) or (q == 0 and len(starts) < 2 and len(cy) == 2):
            continue  # ray leaves into a wall or runs along one
        a = idx[starts[0]]; X, Y = sx, sy; seen = set()
        while True:
            # cross interior grid lines: vertical lines X+sgn*m, horizontal Y+sgn*m, ordered by time
            ev = [(m / abs(p), 0, X + (m if p > 0 else -m) + (0 if p > 0 else 0)) for m in range(1, abs(p))] if p else []
            ev += [(m / abs(q), 1, Y + (m if q > 0 else -m)) for m in range(1, abs(q))] if q else []
            for _, ax, line in sorted(ev):
                a = S[(ax, line % 2)][a]
            X += p; Y += q
            k = (X % 2, Y % 2)
            if cyc[(k, a)] != 2: break  # corner
            i, j = cells[a]
            phys = (i if i % 2 == X % 2 else i + 1, j if j % 2 == Y % 2 else j + 1)
            if p == 0: phys = (sx, phys[1]) if False else phys
            if phys == tuple(t): hits.append((p, q)); break
            if p and q: a = g[k][a]
            elif p: a = S[(0, X % 2)][a]
            else: a = S[(1, Y % 2)][a]
            st = (a, X % 2, Y % 2)
            if st in seen: break
            seen.add(st)
    return len(dirs), hits

if __name__ == '__main__':
    import json, os
    D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    R22 = sorted(tuple(c) for c in [r for r in json.load(open(os.path.join(D, 'd8-perturbation-test', 'rooms.json'))) if r['id'] == 'R22-base'][0]['cells'])
    stair = [(-1, 0), (0, 0), (0, 1), (1, 1), (1, 2)]
    P = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    rect = [(i, j) for i in range(4) for j in range(3)]
    for name, cells, s, t in [('rectangle 4x3 control (1,1)-(3,2)', rect, (1, 1), (3, 2)), ('R22 seed', R22, (0, 0), (2, 2)), 
                              ('staircase images u,v', stair, (0, 0), (2, 2)), ('cross b=7 S,T', room(7), (6, 0), (0, 6)), ('cross b=9 S,T', room(9), (6, 0), (0, 6))]:
        nd, h = run(cells, s, t, P)
        if name.startswith('rect'): assert (2, 1) in h and (1, 0) not in h
        print(f'{name}: {nd} primitive directions |p|,|q|<={P}; lighting directions: {h[:6]}{" ..." if len(h) > 6 else ""} ({len(h)})')
