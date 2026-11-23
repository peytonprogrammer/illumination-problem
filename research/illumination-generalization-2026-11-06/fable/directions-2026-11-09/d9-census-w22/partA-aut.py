#!/usr/bin/env python3
"""Translation automorphisms of the marked unfolding (M, Sigma).

An automorphism is a permutation s of the squares of M with s r = r s,
s u = u s, that maps squares whose lower-left corner is a corner lift to
squares of the same kind.  M is connected, so s is fixed by the image of one
square.  Usage: partA-aut.py ROOMSFILE [TAGS] -- prints |Aut| per room tag.
"""
import sys, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "d3-review"))
from surface import Surface


def automorphisms(S):
    n = len(S.sq)
    marked = [S.marked_ll(i) for i in range(n)]
    auts = []
    for t in range(n):
        if marked[t] != marked[0]:
            continue
        img = {0: t}
        stack = [0]
        ok = True
        while stack and ok:
            a = stack.pop()
            for f in (S.r, S.u, S.ri, S.ui):
                b, c = f[a], f[img[a]]
                if b in img:
                    if img[b] != c:
                        ok = False
                        break
                else:
                    if marked[b] != marked[c]:
                        ok = False
                        break
                    img[b] = c
                    stack.append(b)
        if ok and len(set(img.values())) == n:
            auts.append([img[i] for i in range(n)])
    return auts


def cells_of(t):
    a = int(t[0]); xs = list(map(int, t[2:2 + 2 * a]))
    return [(xs[2 * i], xs[2 * i + 1]) for i in range(a)]


if __name__ == "__main__":
    stat = Counter()
    for l in open(sys.argv[1]):
        t = l.split()
        tag = t[0]
        if tag.isdigit():
            tag, t = "room", t
        else:
            t = t[1:]
        S = Surface(cells_of(t))
        stat[(tag, len(automorphisms(S)))] += 1
    for k, v in sorted(stat.items()):
        print(k, v)
