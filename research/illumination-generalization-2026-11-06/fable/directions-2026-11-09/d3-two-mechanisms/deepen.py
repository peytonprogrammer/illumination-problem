#!/usr/bin/env python3
"""Two-phase exact check: all leaves up to B0, then only the surviving pairs
up to B1. Prints the pairs still unjoined and, for each joined survivor, the
smallest max(p,q) that joined it.

Usage: deepen.py ROOM N B0 B1
"""
import sys
from math import gcd
from leafcheck import build, forward, neg, run, frac


def deepen(room, N, B0, B1):
    pts, unlit = run(room, N, B0, verbose=False)
    cells, _ = build(room, N)
    remaining = set(unlit)
    worst = B0
    hist = {}
    for m in range(B0 + 1, B1 + 1):
        if not remaining:
            break
        dirs = [(p, q) for p in range(m + 1) for q in range(m + 1)
                if max(p, q) == m and gcd(p, q) == 1]
        srcs = {a for a, _ in remaining}
        for a in srcs:
            partners = {b for (x, b) in remaining if x == a}
            for (p, q) in dirs:
                for d in {(p, q), (-p, q), (p, -q), (-p, -q)}:
                    F, _c = forward(cells, N, a, d)
                    hit = partners.intersection(s[0] for s in F)
                    for b in hit:
                        remaining.discard((a, b))
                        hist[(a, b)] = m
                        worst = m
                    partners -= hit
                    if not partners:
                        break
                if not partners:
                    break
    print(f"room={room} N={N} points={len(pts)} pairs={len(pts)*(len(pts)-1)//2} "
          f"after B0={B0}: {len(unlit)} unjoined; after B1={B1}: "
          f"{len(remaining)} unjoined; largest bound needed={worst}")
    for a, b in sorted(remaining):
        print("   UNJOINED", frac(a, N), frac(b, N))
    return remaining


if __name__ == "__main__":
    deepen(sys.argv[1], *map(int, sys.argv[2:5]))
