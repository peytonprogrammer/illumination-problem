#!/usr/bin/env python3
"""Status of reduced rooms (diag(gx, gy) images of a smaller room).

A diagonal linear map sends billiard paths to billiard paths in orthogonal
rooms, so a reduced room has a dark pair exactly when its normal form has one.
For each RED line, compute the normal form and report its status from the
cover results (class (iii) normal forms) or "class i/ii" (Part A covers it).

usage: python3 reduced.py REDFILE RESULTS...
"""
import sys
from math import gcd

from cyl import point_type
from validate_x import canon


def normal_form(cells):
    cells = frozenset(cells)
    corners = sorted({(a + dx, b + dy) for a, b in cells for dx in (0, 1) for dy in (0, 1)
                      if point_type(cells, a + dx, b + dy) in ("convex", "reflex")})
    x0, y0 = corners[0]
    gx = gy = 0
    for x, y in corners:
        gx, gy = gcd(gx, x - x0), gcd(gy, y - y0)
    mx, my = min(a for a, _ in cells), min(b for _, b in cells)
    return frozenset(((a - mx) // gx, (b - my) // gy) for a, b in cells), (gx, gy)


def main():
    status = {}
    for fn in sys.argv[2:]:
        for ln in open(fn):
            if ln.startswith("ROOM"):
                head, cs, _ = ln.split("|", 2)
                v = list(map(int, cs.split()))
                status[canon(frozenset((v[2 * i], v[2 * i + 1]) for i in range(len(v) // 2)))] = head.split()[4]
    out = {}
    for ln in open(sys.argv[1]):
        t = ln.split()
        A, W = int(t[1]), int(t[2])
        v = list(map(int, t[3:]))
        nf, g = normal_form([(v[2 * i], v[2 * i + 1]) for i in range(A)])
        st = status.get(canon(nf), "class i/ii")
        out.setdefault((A, st), []).append((W, g, sorted(nf)))
    for (A, st), lst in sorted(out.items()):
        print(f"area {A} normal-form status {st}: {len(lst)}")
        if st != "class i/ii":
            for W, g, nf in lst:
                print(f"   W {W} scale {g} normal form {nf}")


if __name__ == "__main__":
    main()
