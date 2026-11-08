"""Claude's blind finite reduction for I=3 full A stars with exactly three B/C exceptions.

Written before reading Codex's findings. Uses no Codex code.

Facts used, each derived in report.md:
- W = 20 + Q - E <= 23, so Q <= 3 + E, where E = 2J + s_N and J + s_N = 3.
- Adjacent full cells share an interior C midpoint: J >= f_adj.
- An absent external neighbor makes every shared side midpoint a smooth C:
  a' (absent incidences) <= s_N, and a <= a'.
- Every used partial cell has charge >= 1: Q >= P.
- Connected used-cell graph with full degree <= 4 - (absent incidences):
  Q >= sum partial degree >= 2(3 + P - 1) - (12 - a') = 2P - 8 + a'.
- Every used cell outside R = F + N(F) lies within Manhattan distance `out` of R,
  and the components of R need outside connectors.
"""
import json
from itertools import combinations, product
from pathlib import Path

NB = ((1, 0), (-1, 0), (0, 1), (0, -1))
BASE = Path(__file__).parent
D4 = [lambda x, y: (x, y), lambda x, y: (-y, x), lambda x, y: (-x, -y), lambda x, y: (y, -x),
      lambda x, y: (-x, y), lambda x, y: (x, -y), lambda x, y: (y, x), lambda x, y: (-y, -x)]


def canon(cells):
    best = None
    for g in D4:
        pts = [g(*p) for p in cells]
        mx = min(pts)
        key = tuple(sorted((x-mx[0], y-mx[1]) for x, y in pts))
        best = key if best is None or key < best else best
    return best


def neighbors(cells):
    return {(x+dx, y+dy) for x, y in cells for dx, dy in NB} - set(cells)


def components(cells):
    cells, comps = set(cells), []
    while cells:
        st = [cells.pop()]; comp = set(st)
        while st:
            x, y = st.pop()
            for dx, dy in NB:
                q = (x+dx, y+dy)
                if q in cells:
                    cells.discard(q); comp.add(q); st.append(q)
        comps.append(comp)
    return comps


def connectors_needed(R):
    """Exact minimum number of extra cells joining all components of R (<=3 components)."""
    comps = components(R)
    if len(comps) == 1:
        return 0
    def dist(a, b):
        return min(abs(p[0]-q[0])+abs(p[1]-q[1]) for p in a for q in b)
    if len(comps) == 2:
        return dist(*comps) - 1
    # Three components: the cheaper of a path tree or a Steiner point.
    a, b, c = comps
    d = [dist(a, b), dist(b, c), dist(a, c)]
    best = sum(sorted(d)[:2]) - 2
    xs = [p for comp in comps for p in comp]
    lo = min(min(p) for p in xs) - 1; hi = max(max(p) for p in xs) + 1
    for s in product(range(lo, hi+1), repeat=2):
        if s in R:
            continue
        cost = 1 + sum(min(abs(s[0]-p[0])+abs(s[1]-p[1]) for p in comp) - 1 for comp in comps)
        best = min(best, cost)
    return best


def budget(F):
    """Largest number of used partial cells outside R over all legal parameters, or None."""
    ext = neighbors(F)
    f_adj = sum(1 for p, q in combinations(F, 2) if abs(p[0]-q[0])+abs(p[1]-q[1]) == 1)
    full_nb = {c: sum(1 for d in NB if (c[0]+d[0], c[1]+d[1]) in F) for c in ext}
    conn = connectors_needed(set(F) | ext)
    best = None
    for J in range(4):
        sN = 3 - J
        if J < f_adj:
            continue
        Qmax = 3 + 2*J + sN
        # choose absent set: only its size a and incidence a' matter; enumerate subsets.
        ext_list = sorted(ext)
        for r in range(0, sN+1):
            for absent in combinations(ext_list, r):
                ap = sum(full_nb[c] for c in absent)
                if ap > sN:
                    continue
                a = len(absent)
                Pmax = min(Qmax, (Qmax + 8 - ap)//2)
                out = Pmax - (len(ext) - a)
                if out < conn:
                    continue  # connector requirement also ignores absent-cell breaks: still a valid bound
                best = out if best is None else max(best, out)
    return best


def main():
    shapes = {}
    L = 12
    window = [(x, y) for x in range(-L, L+1) for y in range(-L, L+1) if 0 < abs(x)+abs(y) <= L]
    for b, c in combinations(window, 2):
        F = [(0, 0), b, c]
        k = canon(F)
        if k in shapes:
            continue
        shapes[k] = budget(F)
    feasible = {k: v for k, v in shapes.items() if v is not None}
    far = max(max(abs(x)+abs(y) for x, y in k) for k in feasible)
    out = dict(shapes_examined=len(shapes), feasible_shapes=len(feasible), max_extent=far,
               shapes=[dict(cells=k, outside_budget=v) for k, v in sorted(feasible.items())])
    (BASE/'claude-three-star-reduction.json').write_text(json.dumps(out, indent=1)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'shapes'}))
    for s in out['shapes']:
        print(s)


if __name__ == '__main__':
    main()
