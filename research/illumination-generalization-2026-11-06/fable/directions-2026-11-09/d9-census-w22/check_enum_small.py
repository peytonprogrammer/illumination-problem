"""Independent brute-force check of enum_rooms.c for small areas.

Grows free polyominoes by set expansion (no Redelmeier), tests strict
simplicity by walking the boundary edge graph (every boundary vertex has
degree 2 and the boundary is one cycle), counts walls as turning points of
that cycle, and compares counts per (area, W) and the eligible rooms with the
C output.  usage: python3 check_enum_small.py NMAX c_output_file
"""
import sys
from collections import Counter


def norm(cells):
    mx = min(x for x, _ in cells)
    my = min(y for _, y in cells)
    return frozenset((x - mx, y - my) for x, y in cells)


def canon(cells):
    best = None
    for t in range(8):
        img = []
        for x, y in cells:
            a, b = (x, y) if t < 4 else (y, x)
            if t & 1:
                a = -a
            if t & 2:
                b = -b
            img.append((a, b))
        k = tuple(sorted(norm(img)))
        if best is None or k < best:
            best = k
    return best


def boundary_walls(cells):
    """Return number of turning points of the boundary, or None if not a simple cycle."""
    edges = []
    for a, b in cells:
        if (a - 1, b) not in cells: edges.append(((a, b), (a, b + 1)))
        if (a + 1, b) not in cells: edges.append(((a + 1, b), (a + 1, b + 1)))
        if (a, b - 1) not in cells: edges.append(((a, b), (a + 1, b)))
        if (a, b + 1) not in cells: edges.append(((a, b + 1), (a + 1, b + 1)))
    adj = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    if any(len(v) != 2 for v in adj.values()):
        return None
    start = min(adj)
    prev, cur, cyc = None, start, [start]
    while True:
        nxt = adj[cur][0] if adj[cur][0] != prev else adj[cur][1]
        prev, cur = cur, nxt
        if cur == start:
            break
        cyc.append(cur)
    if len(cyc) != len(adj):
        return None
    m = len(cyc)
    turns = 0
    for i in range(m):
        p, q, r = cyc[i - 1], cyc[i], cyc[(i + 1) % m]
        if (q[0] - p[0], q[1] - p[1]) != (r[0] - q[0], r[1] - q[1]):
            turns += 1
    return turns


def interior_points(cells):
    pts = {(x + dx, y + dy) for x, y in cells for dx in (0, 1) for dy in (0, 1)}
    return [p for p in pts if all(c in cells for c in
            ((p[0] - 1, p[1] - 1), (p[0], p[1] - 1), (p[0] - 1, p[1]), p))]


def main():
    nmax = int(sys.argv[1])
    level = {canon([(0, 0)])}
    counts, elig = Counter(), set()
    for n in range(1, nmax + 1):
        if n > 1:
            nxt = set()
            for P in level:
                S = set(P)
                for x, y in P:
                    for c in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if c not in S:
                            nxt.add(canon(S | {c}))
            level = nxt
        for P in level:
            S = set(P)
            w = boundary_walls(S)
            if w is None or w > 22:
                continue
            counts[(n, w)] += 1
            cl = Counter((x % 2, y % 2) for x, y in interior_points(S))
            if any(v >= 2 for v in cl.values()):
                elig.add(P)
    ccounts, celig = Counter(), set()
    for line in open(sys.argv[2]):
        if line.startswith("# count"):
            f = line.split()
            ccounts[(int(f[3]), int(f[5]))] = int(f[7])
        elif not line.startswith("#"):
            f = list(map(int, line.split()))
            cells = [(f[i], f[i + 1]) for i in range(2, len(f), 2)]
            assert len(cells) == f[0]
            celig.add(canon(cells))
    ok = (counts == ccounts) and (elig == celig)
    print("python counts:", sorted(counts.items()))
    print("eligible python", len(elig), "C", len(celig))
    print("MATCH" if ok else "MISMATCH")
    if counts != ccounts:
        for k in sorted(set(counts) | set(ccounts)):
            if counts[k] != ccounts[k]:
                print("  diff", k, counts[k], ccounts[k])


if __name__ == "__main__":
    main()
