"""Independent validator for the d236 immersed-disc class (see README.md).

Complex: list `nb` of cells; nb[c][d] is the cell glued across side d of c,
or -1.  Directions d: 0=E, 1=N, 2=W, 3=S.  Gluing is symmetric:
nb[c][d] = x  <=>  nb[x][(d+2)%4] = c.  Positions follow from the gluings
(developing map), so a connected complex is fixed by `nb` alone.

Corner q of a cell lies between sides q and q+1 (0=NE, 1=NW, 2=SW, 3=SE).
Crossing side q from corner q lands on the neighbour's corner q+1; crossing
side q+1 lands on corner q-1.  Links are the components of that graph.

Usage: python3 validate.py MAXAREA [LIGHTAREA]
"""
import sys
import time
from collections import deque
from math import comb

DX = ((1, 0), (0, 1), (-1, 0), (0, -1))
SYMS = [tuple((d + k) % 4 for d in range(4)) for k in range(4)] + \
       [tuple((k - d) % 4 for d in range(4)) for k in range(4)]
# SYMS[g][d] = image of old direction d.  Inverse tables:
SYMI = [tuple(p.index(e) for e in range(4)) for p in SYMS]


def positions(nb):
    pos = [None] * len(nb)
    pos[0] = (0, 0)
    q = [0]
    for c in q:
        x, y = pos[c]
        for d in range(4):
            n = nb[c][d]
            if n >= 0 and pos[n] is None:
                pos[n] = (x + DX[d][0], y + DX[d][1])
                q.append(n)
    return pos


def links(nb):
    """Return (comp, info): comp[c*4+q] = link id; info[id] = (size, is_cycle)."""
    n4 = 4 * len(nb)
    par = list(range(n4))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    # Side q of c joins corner q of c to corner q+1 of the neighbour.  The
    # other endpoint (corner q-1 of c) is joined from the neighbour's side.
    for c, row in enumerate(nb):
        for q in range(4):
            x = row[q]
            if x >= 0:
                a, b = find(4 * c + q), find(4 * x + (q + 1) % 4)
                if a != b:
                    par[a] = b
    comp = [find(i) for i in range(n4)]
    ids = {}
    size = []
    for r in comp:
        if r not in ids:
            ids[r] = len(size)
            size.append(0)
        size[ids[r]] += 1
    comp = [ids[r] for r in comp]
    # link edges: every glued side pair gives one edge at each of its 2 endpoints
    ledges = [0] * len(size)
    for c, row in enumerate(nb):
        for d in (0, 1):  # count each glued pair once via E and N sides
            x = row[d]
            if x >= 0:
                # side d of c has endpoints at corners d-1 and d of c
                ledges[comp[4 * c + d]] += 1
                ledges[comp[4 * c + (d - 1) % 4]] += 1
    info = [(size[i], ledges[i] == size[i]) for i in range(len(size))]
    return comp, info


def links_ok(info):
    for s, cyc in info:
        if cyc:
            if s != 4:
                return False
        elif s > 3:
            return False
    return True


def canon(nb):
    n = len(nb)
    best = None
    for g in range(8):
        inv = SYMI[g]
        for r in range(n):
            num = {r: 0}
            order = [r]
            k = 0
            while k < len(order):
                row = nb[order[k]]
                k += 1
                for e in range(4):
                    x = row[inv[e]]
                    if x >= 0 and x not in num:
                        num[x] = len(order)
                        order.append(x)
            key = tuple(num[x] if x >= 0 else -1
                        for c in order for x in (nb[c][inv[0]], nb[c][inv[1]],
                                                  nb[c][inv[2]], nb[c][inv[3]]))
            if best is None or key < best:
                best = key
    return best


def from_key(key):
    return [list(key[4 * i:4 * i + 4]) for i in range(len(key) // 4)]


def children(nb):
    """All complexes made by adding one cell glued to >= 1 present cell,
    with every subset (at most one cell per side) of its other possible
    gluings."""
    pos = positions(nb)
    at = {}
    for c, p in enumerate(pos):
        at.setdefault(p, []).append(c)
    targets = set()
    for c, p in enumerate(pos):
        for d in range(4):
            if nb[c][d] < 0:
                targets.add((p[0] + DX[d][0], p[1] + DX[d][1]))
    n = len(nb)
    for P in targets:
        opts = []
        for e in range(4):
            Q = (P[0] + DX[e][0], P[1] + DX[e][1])
            o = [-1] + [x for x in at.get(Q, ()) if nb[x][(e + 2) % 4] < 0]
            opts.append(o)
        for a in opts[0]:
            for b in opts[1]:
                for c in opts[2]:
                    for d in opts[3]:
                        sel = (a, b, c, d)
                        if sel == (-1, -1, -1, -1):
                            continue
                        new = [row[:] for row in nb]
                        new.append(list(sel))
                        for e, x in enumerate(sel):
                            if x >= 0:
                                new[x][(e + 2) % 4] = n
                        yield new


def classify(nb, comp, info):
    F = len(nb)
    G = sum(1 for row in nb for x in row if x >= 0) // 2
    V = len(info)
    chi = F - (4 * F - G) + V
    W = sum(1 for s, cyc in info if not cyc and s in (1, 3))
    marks = sum(1 for s, cyc in info if cyc)
    pos = positions(nb)
    if len(set(pos)) < F:
        bucket = "OVERLAP"
    else:
        at = {p: c for c, p in enumerate(pos)}
        emb = True
        for c, (x, y) in enumerate(pos):
            for d in range(4):
                o = at.get((x + DX[d][0], y + DX[d][1]))
                if o is not None and nb[c][d] != o:
                    emb = False
        if emb:
            lp = {}
            for c, (x, y) in enumerate(pos):
                for q, (ox, oy) in enumerate(((1, 1), (0, 1), (0, 0), (1, 0))):
                    lp.setdefault((x + ox, y + oy), set()).add(comp[4 * c + q])
            emb = all(len(s) == 1 for s in lp.values())
        bucket = "EMBEDDED" if emb else "TOUCHING"
    return chi, W, marks, bucket


# ---------------- lighting: 4-sheet unfolding + SL(2,Z) orbit ----------------

SHEETS = ((1, 1), (-1, 1), (1, -1), (-1, -1))


def unfold(nb, comp, info):
    """Squares (c, s).  In sheet (sx, sy) developing +x is room direction sx,
    developing +y is room direction sy.  Label = link at the developing
    bottom-left corner."""
    n = len(nb)
    h, v, lab = [], [], []
    for c in range(n):
        for s, (sx, sy) in enumerate(SHEETS):
            dh = 0 if sx > 0 else 2
            x = nb[c][dh]
            h.append(4 * x + s if x >= 0 else 4 * c + SHEETS.index((-sx, sy)))
            dv = 1 if sy > 0 else 3
            x = nb[c][dv]
            v.append(4 * x + s if x >= 0 else 4 * c + SHEETS.index((sx, -sy)))
            right, top = sx < 0, sy < 0
            q = {(True, True): 0, (False, True): 1, (False, False): 2, (True, False): 3}[(right, top)]
            lab.append(comp[4 * c + q])
    return h, v, lab


def orbit_decide(h0, v0, dec, nsrc, cap=200000):
    """dec[i]: source index >= 0, -1 stop (link size 1 or 3), -2 pass.
    Returns (lit set of (a,b) a<b, nstates, complete)."""
    n = len(h0)
    allpairs = {(a, b) for a in range(nsrc) for b in range(a + 1, nsrc)}
    lit = set()

    def key(h, v, d):
        best = None
        for a in range(n):
            if d[a] != 0:
                continue
            num = [-1] * n
            num[a] = 0
            order = [a]
            k = 0
            while k < len(order):
                x = order[k]
                k += 1
                for y in (h[x], v[x]):
                    if num[y] < 0:
                        num[y] = len(order)
                        order.append(y)
            kk = (tuple(num[h[x]] for x in order), tuple(num[v[x]] for x in order),
                  tuple(d[x] for x in order))
            if best is None or kk < best:
                best = kk
        return best

    def scan(h, d):
        for i in range(n):
            a = d[i]
            if a < 0:
                continue
            cur = h[i]
            while cur != i and d[cur] != -1:
                b = d[cur]
                if b >= 0 and b != a:
                    lit.add((min(a, b), max(a, b)))
                cur = h[cur]

    st = key(h0, v0, dec)
    seen = {st}
    dq = deque([st])
    while dq:
        h, v, d = dq.popleft()
        h, v, d = list(h), list(v), list(d)
        scan(h, d)
        if lit >= allpairs:
            return lit, len(seen), True
        hi = [0] * n
        vi = [0] * n
        for i in range(n):
            hi[h[i]] = i
            vi[v[i]] = i
        for a, b in ((h, [v[hi[i]] for i in range(n)]),
                     (h, [v[h[i]] for i in range(n)]),
                     ([h[vi[i]] for i in range(n)], v),
                     ([h[v[i]] for i in range(n)], v)):
            s2 = key(a, b, d)
            if s2 not in seen:
                seen.add(s2)
                dq.append(s2)
                if len(seen) > cap:
                    return lit, len(seen), False
    return lit, len(seen), True


def light(nb, comp, info, srcs=None):
    """srcs: list of link ids to use as sources (default: all marks)."""
    if srcs is None:
        srcs = [i for i, (s, cyc) in enumerate(info) if cyc]
    sid = {l: k for k, l in enumerate(srcs)}
    h, v, lab = unfold(nb, comp, info)
    dec = []
    for l in lab:
        if l in sid:
            dec.append(sid[l])
        elif not info[l][1] and info[l][0] in (1, 3):
            dec.append(-1)
        else:
            dec.append(-2)
    return orbit_decide(h, v, dec, len(srcs)), srcs


def complex_from_cells(cells):
    """Embedded complex: all plane-adjacent pairs glued."""
    cl = sorted(cells)
    ix = {c: k for k, c in enumerate(cl)}
    nb = []
    for (x, y) in cl:
        nb.append([ix.get((x + dx, y + dy), -1) for dx, dy in DX])
    return nb, cl


def describe(nb):
    pos = positions(nb)
    lines = []
    for c, row in enumerate(nb):
        lines.append("  cell %d at %s glued E,N,W,S = %s" % (c, pos[c], row))
    return "\n".join(lines)


def main():
    maxa = int(sys.argv[1])
    lighta = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    out = sys.argv[3] if len(sys.argv) > 3 else "."
    t0 = time.process_time()

    # G3-style control: d205 22-wall room, pair (1,3)-(3,5) must be DARK.
    cells = [(2, 0), (1, 1), (2, 1), (0, 2), (1, 2), (0, 3), (1, 3), (4, 3), (5, 3),
             (1, 4), (2, 4), (3, 4), (4, 4), (2, 5), (3, 5)]
    cnb, cl = complex_from_cells(cells)
    comp, info = links(cnb)
    ix = {c: k for k, c in enumerate(cl)}
    # link id of interior point (1,3) = NE corner (q=0) of cell (0,2); (3,5) = NE of (2,4)
    s1, s2 = comp[4 * ix[(0, 2)] + 0], comp[4 * ix[(2, 4)] + 0]
    assert info[s1] == (4, True) and info[s2] == (4, True)
    (lit, ns, full), _ = light(cnb, comp, info, [s1, s2])
    print("control: W=%d lit=%s states=%d complete=%s" % (
        classify(cnb, comp, info)[1], sorted(lit), ns, full), flush=True)

    level = {canon([[-1, -1, -1, -1]])}
    counts = {}
    finals = {}
    for F in range(1, maxa + 1):
        for key in level:
            nb = from_key(key)
            comp, info = links(nb)
            chi, W, marks, bucket = classify(nb, comp, info)
            if chi != 1 or W > 26:
                continue
            r = counts.setdefault((F, W, bucket), [0, 0])
            r[0] += 1
            r[1] += comb(marks, 2)
            if bucket != "EMBEDDED" and F <= lighta and marks >= 2:
                finals.setdefault((F, W, bucket), []).append(key)
        print("area %d: %d intermediate states, cpu %.1fs" % (
            F, len(level), time.process_time() - t0), flush=True)
        if F == maxa:
            break
        nxt = set()
        for key in level:
            for ch in children(from_key(key)):
                comp, info = links(ch)
                if links_ok(info):
                    nxt.add(canon(ch))
        level = nxt

    with open(out + "/counts.tsv", "w") as f:
        f.write("area\tW\tbucket\tdiscs\tpairs\n")
        for (F, W, b) in sorted(counts):
            f.write("%d\t%d\t%s\t%d\t%d\n" % (F, W, b, *counts[(F, W, b)]))

    rows = []
    dark = []
    for (F, W, b) in sorted(counts):
        if b == "EMBEDDED" or F > lighta:
            continue
        P = L = D = U = 0
        for key in finals.get((F, W, b), []):
            nb = from_key(key)
            comp, info = links(nb)
            (lit, ns, full), srcs = light(nb, comp, info)
            m = len(srcs)
            P += comb(m, 2)
            L += len(lit)
            rest = comb(m, 2) - len(lit)
            if full:
                D += rest
                for a in range(m):
                    for c in range(a + 1, m):
                        if (a, c) not in lit:
                            dark.append((F, W, b, srcs[a], srcs[c], ns, nb))
            else:
                U += rest
        rows.append((F, W, b, P, L, D, U))
    with open(out + "/lighting.tsv", "w") as f:
        f.write("area\tW\tbucket\tpairs\tlit\tdark\tundecided\n")
        for r in rows:
            f.write("%d\t%d\t%s\t%d\t%d\t%d\t%d\n" % r)
    with open(out + "/dark.txt", "w") as f:
        if not dark:
            f.write("No dark pairs among TOUCHING and OVERLAP discs of area <= %d.\n" % lighta)
        for (F, W, b, l1, l2, ns, nb) in dark:
            f.write("area %d W %d %s: links %d and %d DARK (%d states)\n%s\n\n" % (
                F, W, b, l1, l2, ns, describe(nb)))
    print("done, cpu %.1fs, dark pairs %d" % (time.process_time() - t0, len(dark)))


if __name__ == "__main__":
    main()
