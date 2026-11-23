"""D126 checks for whole-room-decomposition.snapshot.md.

Exact integer arithmetic only. Named room: the normalized cov279 stretch
(d117 bands, t = 3/q, horizontal scale q) at the saved parameters
q = 12j + 4, j = 1..5. No search over rooms, rays, directions or
reflection words. The only "trace" is the d124 first-hit cover automaton
read along the fixed reference slope alpha = 1/phi^2, as in d124.

Sections
 A. Room facts: area 13q+3, r = 6, strict simplicity, wall gcds.
 B. Both canonical parallel decompositions: cut count <= r, pieces are
    rectangles, count <= r+1, dual graph is a tree, single-door access,
    long sides of each piece are physical walls, doors pairwise separated.
 C. Per piece: L, H, door sides, attachment areas B, the note's
    Z_B = 4H(1+F_(12B-1))^2, the refined Z* = 4H(1+F_(k*+2))^2 from the
    computed first full index k*, and the farthest-cell travel bound.
    Check that no piece of either decomposition meets L >= Z* (hence
    none meets L >= Z_B), and that every piece has a side <= 3.
 D. Decomposition-independent block argument at each q.
 E. Algebra: span identities at the threshold, area cutoff, census.
"""
from fractions import Fraction as Fr
from math import gcd, isqrt, ceil
from functools import reduce
import time

T0 = time.process_time()
OUT = []


def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s)
    OUT.append(s)


FIB = [0, 1]
while len(FIB) < 12 * (11 * 64 + 3) + 10:
    FIB.append(FIB[-1] + FIB[-2])


def W(k):  # Fibonacci word prefixes, |W_k| = F_(k+2)
    a, b = '0', '01'
    if k == 0:
        return a
    for _ in range(k - 1):
        a, b = b, b + a
    return b


def cov279(q):
    c = set()
    for y in (0, 1):
        c |= {(x, y) for x in range(0, 2 * q)}
    c |= {(x, 2) for x in range(2 * q - 3, 4 * q)}
    c |= {(x, 3) for x in range(2 * q, 5 * q)}
    for y in (4, 5):
        c |= {(x, y) for x in range(4 * q, 6 * q)}
    return c


def vertex_types(cells):
    pts = {(x + dx, y + dy) for (x, y) in cells for dx in (0, 1) for dy in (0, 1)}
    refl, conv, pinch = [], [], []
    for (X, Y) in pts:
        q4 = [(X - 1, Y - 1) in cells, (X, Y - 1) in cells, (X - 1, Y) in cells, (X, Y) in cells]
        k = sum(q4)
        if k == 3:
            refl.append((X, Y))
        elif k == 1:
            conv.append((X, Y))
        elif k == 2 and q4[0] == q4[3]:
            pinch.append((X, Y))
    return sorted(refl), conv, pinch


def connected(cells):
    cells = set(cells)
    if not cells:
        return True
    st = [next(iter(cells))]
    seen = {st[0]}
    while st:
        x, y = st.pop()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if n in cells and n not in seen:
                seen.add(n); st.append(n)
    return len(seen) == len(cells)


def hole_free(cells):
    xs = [x for x, _ in cells]; ys = [y for _, y in cells]
    box = {(x, y) for x in range(min(xs) - 1, max(xs) + 2) for y in range(min(ys) - 1, max(ys) + 2)}
    return connected(box - set(cells))


def vertical_decomp(cells):
    """Canonical vertical parallel-cut decomposition (note, first section).
    Cut unit segments are keyed (X, y): segment x = X, y..y+1."""
    refl, _, _ = vertex_types(cells)
    cuts = set()
    chords = set()
    for (X, Y) in refl:
        north_missing = (X - 1, Y) not in cells or (X, Y) not in cells
        step = -1 if north_missing else 1  # extend away from the incident vertical edge
        y = Y if step == 1 else Y - 1
        seg = []
        while (X - 1, y) in cells and (X, y) in cells:
            seg.append((X, y)); y += step
        assert seg, 'empty chord'
        cuts |= set(seg)
        chords.add((X, min(s[1] for s in seg), max(s[1] for s in seg) + 1))
    # pieces
    pid = {}
    pieces = []
    for c0 in sorted(cells):
        if c0 in pid:
            continue
        st = [c0]; pid[c0] = len(pieces); comp = [c0]
        while st:
            x, y = st.pop()
            nbs = []
            if (x + 1, y) in cells and (x + 1, y) not in cuts:
                nbs.append((x + 1, y))
            if (x - 1, y) in cells and (x, y) not in cuts:
                nbs.append((x - 1, y))
            for n in ((x, y + 1), (x, y - 1)):
                if n in cells:
                    nbs.append(n)
            for n in nbs:
                if n not in pid:
                    pid[n] = len(pieces); st.append(n); comp.append(n)
        pieces.append(comp)
    return refl, chords, cuts, pid, pieces


def transpose(cells):
    return {(y, x) for (x, y) in cells}


def cover_kstar(chamber, X, ylo, yhi):
    """d124 four-copy cover of a sealed lattice chamber with vertical portal
    x = X, rows ylo..yhi-1. Returns (transitive, first full index k*)."""
    cs = set(chamber)
    sq = [(i, j, sx, sy) for (i, j) in sorted(cs) for sx in (1, -1) for sy in (1, -1)]
    idx = {s: n for n, s in enumerate(sq)}
    R, U, Rhit = [], [], []
    for (i, j, sx, sy) in sq:
        nb = (i + sx, j)
        if nb in cs:
            R.append(idx[(i + sx, j, sx, sy)]); Rhit.append(False)
        else:
            R.append(idx[(i, j, -sx, sy)])
            xe = i + 1 if sx > 0 else i
            Rhit.append(xe == X and ylo <= j < yhi)
        nb = (i, j + sy)
        U.append(idx[nb + (sx, sy)] if nb in cs else idx[(i, j, sx, -sy)])
    n = len(sq)
    seen, st = {0}, [0]
    while st:
        x = st.pop()
        for y in (R[x], U[x]):
            if y not in seen:
                seen.add(y); st.append(y)
    comp = lambda g, h: [g[h[x]] for x in range(n)]

    def inv(g):
        r = [0] * n
        for x in range(n):
            r[g[x]] = x
        return r
    g0 = list(R)
    g1 = comp([R[U[x]] for x in range(n)], g0)
    P0 = {x for x in range(n) if Rhit[x]}
    P1 = {x for x in range(n) if Rhit[x] or Rhit[U[R[x]]]}
    gs, Ps = [g0, g1], [P0, P1]
    k = 1 if len(P1) < n else (0 if len(P0) == n else 1)
    while len(Ps[-1]) < n:
        gk, gk1 = gs[-2], gs[-1]
        gi = inv(gk1)
        Ps.append(Ps[-1] | {gi[x] for x in Ps[-2]})
        gs.append(comp(gk, gk1))
        assert len(Ps) < 3 * n + 5
    kstar = next(i for i, P in enumerate(Ps) if len(P) == n)
    # brute cross-check of P_k for k <= 6 by reading words directly
    def read(word, x):
        for c in word:
            if c == '1':
                x = U[x]
            if Rhit[x]:
                return True
            x = R[x]
        return False
    brute = all(Ps[kk] == {x for x in range(n) if read(W(kk), x)} for kk in range(min(7, len(Ps))))
    return len(seen) == n, kstar, brute


def analyse(cells, orient, q):
    """orient 'V': as is; 'H': transposed so horizontal cuts become vertical."""
    C = cells if orient == 'V' else transpose(cells)
    refl, chords, cuts, pid, pieces = vertical_decomp(C)
    r = len(refl)
    ok_rect = all(len(p) == (max(x for x, _ in p) - min(x for x, _ in p) + 1) *
                  (max(y for _, y in p) - min(y for _, y in p) + 1) for p in pieces)
    # doors = chords; adjacency
    adj = {i: set() for i in range(len(pieces))}
    doors = []
    for (X, ya, yb) in sorted(chords):
        a, b = pid[(X - 1, ya)], pid[(X, ya)]
        assert all(pid[(X - 1, y)] == a and pid[(X, y)] == b for y in range(ya, yb))
        adj[a].add(b); adj[b].add(a)
        doors.append((X, ya, yb, a, b))
    nedges = len(doors)
    tree = nedges == len(pieces) - 1 and connected_graph(adj)
    # doors on a common line pairwise separated (no shared endpoint)
    sep = all(not (d1[0] == d2[0] and (d1[2] == d2[1] or d2[2] == d1[1]))
              for d1 in doors for d2 in doors if d1 != d2)
    log(f"  {orient}: r={r}, cuts={len(chords)} (<= r: {len(chords) <= r}), pieces={len(pieces)} "
        f"(<= r+1: {len(pieces) <= r + 1}), all rectangles {ok_rect}, dual tree {tree}, "
        f"doors separated {sep}")
    rows = []
    for i, p in enumerate(pieces):
        x0 = min(x for x, _ in p); x1 = max(x for x, _ in p) + 1
        y0 = min(y for _, y in p); y1 = max(y for _, y in p) + 1
        L, H = x1 - x0, y1 - y0
        # long sides physical: no cut segment on horizontal sides by construction;
        # check every cell on top/bottom row has its outward neighbour outside the room
        walls = all((x, y1) not in C for x in range(x0, x1)) and all((x, y0 - 1) not in C for x in range(x0, x1))
        atts = []
        for (X, ya, yb, a, b) in doors:
            if i not in (a, b):
                continue
            other = b if a == i else a
            side = 'L' if X == x0 else 'R'
            assert X in (x0, x1) and y0 <= ya and yb <= y1
            # component of tree minus i containing other
            comp_ids, st = {other}, [other]
            while st:
                u = st.pop()
                for v in adj[u]:
                    if v != i and v not in comp_ids:
                        comp_ids.add(v); st.append(v)
            ch = [c for j in comp_ids for c in pieces[j]]
            # single-door access: exactly one door joins this component to R
            ndoor = sum(1 for d in doors if (d[3] == i and d[4] in comp_ids) or (d[4] == i and d[3] in comp_ids))
            assert ndoor == 1
            assert hole_free(ch) and connected(ch) and not vertex_types(set(ch))[2]
            trans, ks, brute = cover_kstar(ch, X, ya, yb)
            far = max(abs(cx + 0.5 - X) for cx, _ in ch)
            atts.append(dict(side=side, area=len(ch), w=yb - ya, ks=ks, trans=trans, brute=brute,
                             far=far, door=(X, ya, yb)))
        sides = ''.join(sorted({a['side'] for a in atts}))
        B = max((a['area'] for a in atts), default=0)
        kmax = max((a['ks'] for a in atts), default=None)
        if atts:
            TB = 1 + FIB[12 * B - 1]
            ZB = 4 * H * TB * TB
            Ts = 1 + FIB[kmax + 2]
            Zs = 4 * H * Ts * Ts
            farmax = max(a['far'] for a in atts)
        else:
            ZB = Zs = None; Ts = None; farmax = 0
        rows.append(dict(i=i, x0=x0, x1=x1, y0=y0, y1=y1, L=L, H=H, walls=walls, sides=sides,
                         atts=atts, B=B, kmax=kmax, Ts=Ts, Zs=Zs, ZB=ZB, farmax=farmax))
        fmt = lambda z: 'n/a' if z is None else (str(z) if z < 10 ** 12 else f"~10^{len(str(z)) - 1}")
        log(f"    piece {i}: [{x0},{x1}]x[{y0},{y1}] L={L} H={H} walls-on-long-sides={walls} "
            f"doors on {sides or '-'}; attach (side,area,width,k*,transitive)="
            f"{[(a['side'], a['area'], a['w'], a['ks'], a['trans'] and a['brute']) for a in atts]}; "
            f"B={B}; Z_B={fmt(ZB)}; T*={Ts}; Z*={fmt(Zs)}; far-cell travel >= {farmax - 0.5}; "
            f"L>=Z*? {Zs is not None and L >= Zs}; min side {min(L, H)}")
    return r, rows


def connected_graph(adj):
    if not adj:
        return True
    st, seen = [0], {0}
    while st:
        u = st.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v); st.append(v)
    return len(seen) == len(adj)


# ------------------------------------------------------------------ A, B, C
log('== A-C. Normalized cov279 stretch at q = 12j+4 ==')
summary = []
for j in range(1, 6):
    q = 12 * j + 4
    cells = cov279(q)
    refl, conv, pinch = vertex_types(cells)
    hw = [2 * q, 2 * q - 3, 2 * q, 3, q, 2 * q, q, 2 * q]  # horizontal wall lengths
    vw = [2, 1, 1, 2, 2, 1, 1, 2]  # vertical wall lengths
    log(f"q={q}: area={len(cells)} (13q+3={13 * q + 3}), reflex={len(refl)}, convex={len(conv)}, "
        f"pinch={len(pinch)}, connected={connected(cells)}, hole-free={hole_free(cells)}, "
        f"width={max(x for x, _ in cells) + 1} (6q={6 * q}), height={max(y for _, y in cells) + 1}, "
        f"gcd horiz walls={reduce(gcd, hw)}, gcd vert walls={reduce(gcd, vw)}, walls={len(refl) + len(conv)}")
    log(f"  reflex corners: {refl}")
    rV = analyse(cells, 'V', q)
    rH = analyse(cells, 'H', q)
    bad = [p for _, rows in (rV, rH) for p in rows if p['Zs'] is not None and p['L'] >= p['Zs']]
    big2 = [p for _, rows in (rV, rH) for p in rows if min(p['L'], p['H']) > 3]
    summary.append((q, len(bad), len(big2)))
    log(f"  pieces meeting L >= Z* (hence L >= Z_B) in either decomposition: {len(bad)}; "
        f"pieces with both sides > 3: {len(big2)}")

# ------------------------------------------------------------------ D
log('\n== D. Decomposition-independent block argument ==')
for j in range(1, 6):
    q = 12 * j + 4
    cells = cov279(q)
    blk_lo = {(x, y) for x in range(0, 2 * q) for y in (0, 1)}
    blk_hi = {(x, y) for x in range(4 * q, 6 * q) for y in (4, 5)}
    assert blk_lo <= cells and blk_hi <= cells
    # any rectangle meeting both in positive area contains cell (2q, 1)
    outside = (2 * q, 1) not in cells and all((x, y) not in cells for x in range(2 * q, 6 * q) for y in (0, 1))
    Bmin = ceil(Fr(4 * q, 6))
    TB = 1 + FIB[12 * Bmin - 1]
    ZBmin = 4 * 1 * TB * TB
    log(f"q={q}: blocks inside room, areas {len(blk_lo)},{len(blk_hi)} (4q={4 * q}); "
        f"bottom-height cells with x>=2q all outside: {outside}; "
        f"B >= ceil(2q/3)={Bmin}; Z_B >= 4(1+F_{12 * Bmin - 1})^2 ~10^{len(str(ZBmin)) - 1} > 6q={6 * q}: {ZBmin > 6 * q}")
# farthest-cell bound: any first-access bound T* >= horizontal reach.
# vertical piece: attachment area >= 2q/3, height <= 6 -> >= q/9 columns,
# so some cell centre is at distance >= q/18 - 1/2 from the door line,
# travel >= q/18 - 1, Z* >= 4 (q/18 - 1)^2 vs L <= 6q.
q0 = next(q for q in range(18, 10 ** 6) if 4 * Fr(q - 18, 18) ** 2 > 6 * q)
log(f"generic refined bound: 4(q/18-1)^2 > 6q for all q >= {q0} (horizontal pieces fail since L <= 6 < 16 <= 4H(1+F_2)^2)")

# ------------------------------------------------------------------ E
log('\n== E. Threshold algebra and census arithmetic ==')
for H in (1, 2, 3, 6):
    for T in (2, 90, 145):
        Z = 4 * H * T * T
        d = Fr(1, 2 * T * T)
        log(f"H={H} T={T}: closed end two-leg span (2Z)d={2 * Z * d} vs 2H={2 * H}; "
            f"one-leg depth span Z*d={Z * d} vs 2H; opposite-end span Z*d={Z * d}; "
            f"same-end far-wall span 2Z*d={2 * Z * d} vs 4H={4 * H}")
log("fractions p/q, q<=T, within 1/(3T^2) of alpha: checked in d124; delta/2 = 1/(4T^2) < 1/(3T^2)")
log(f"area cutoff: L >= (n-rB)/D and 4DT^2 <= (n-rB)/D iff n >= rB+4D^2T^2 (identity)")
rate = Fr(3933192) / Fr(725, 10)
log(f"census: 3,933,192/72.5 = {float(rate):.1f}/s; 1e11 -> {1e11 / float(rate) / 3600:.0f} CPU-h; "
    f"1e12 -> {1e12 / float(rate) / 3600:.0f} CPU-h")
log(f"summary (q, pieces meeting L>=Z*, pieces with both sides >3): {summary}")
log(f"CPU seconds: {time.process_time() - T0:.2f}")
open(__file__.replace('checks.py', 'checks.log'), 'w').write('\n'.join(OUT) + '\n')
