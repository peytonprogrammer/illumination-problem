"""D131 checks for passage-complexity.2026-11-21-2125.md.

Named rooms only: the st279 end-square stretch with side m (m a multiple of 8),
bands (bottom to top)  y (0,m):[0,m]  (m,m+1):[m-1,m+2]  (m+1,m+2):[m,m+3]
(m+2,2m+2):[m+2,2m+2].  S = (m/2, m/2), T_j = (3m/2+2+2j, 5m/4+2), |2j| <= sqrt(m).
The transposed room is used only to express the canonical VERTICAL
decomposition of the same room as horizontal bands.

Two independent exact tracers:
  * passage tracer: one integer congruence per band passage (the note's
    definition), coordinates scaled by the slope denominator b;
  * cell tracer: Fraction ray through unit cells of the room, reflecting at
    cell walls; stops at every corner (reflex or convex).  It knows nothing
    about bands.  Counts reflections and the passages of both decompositions.

Checks
 A. Room facts: one boundary loop, reflex count, wall-length gcds, marks.
 B. Slope-shift lemma on every ray from S (both vertical senses, both
    horizontal senses, many slopes): events identical for s and s+24 for the
    first 60 passages; controls s+12 and s+8.
 C. Horizontal search s in (0,24] (complete modulo 24 by B), b <= BMAX:
    lit T_j, fewest passages found, cell-tracer replay, compressed
    reflections <= 26k, and replay at s+24, s+48.
 D. Explicit constant in the determinant bound: smallest m for which the
    passage bound beats the trivial value 4.
 E. Vertical decomposition: search mostly-vertical rays with <= 5 vertical
    passages (the minimum possible); replay in the original room with the
    cell tracer and report both passage counts.
Directions are searched only in the named rooms.  Step caps everywhere.
"""
from fractions import Fraction as F
from math import gcd, isqrt, sqrt
import time

CPU0 = time.process_time()


def st279(m):
    return [(0, m, 0, m), (m, m + 1, m - 1, m + 2),
            (m + 1, m + 2, m, m + 3), (m + 2, 2 * m + 2, m + 2, 2 * m + 2)]


def transpose_bands(m):
    # canonical vertical decomposition of st279(m), written in (y, x) coordinates
    return [(0, m - 1, 0, m), (m - 1, m, 0, m + 1), (m, m + 2, m, m + 2),
            (m + 2, m + 3, m + 1, 2 * m + 2), (m + 3, 2 * m + 2, m + 2, 2 * m + 2)]


def marks(m):
    S = (m // 2, m // 2)
    J = isqrt(m) // 2           # |2j| <= sqrt(m)  <=>  |j| <= floor(sqrt(m)/2)
    T = [(3 * m // 2 + 2 + 2 * j, 5 * m // 4 + 2) for j in range(-J, J + 1)]
    return S, T, J


def cells_of(bands):
    c = set()
    for y0, y1, x0, x1 in bands:
        for i in range(x0, x1):
            for j in range(y0, y1):
                c.add((i, j))
    return c


# ---------------------------------------------------------------- A. room facts
def room_facts(m):
    cells = cells_of(st279(m))
    # boundary edges oriented with interior on the left
    edges = {}
    for (i, j) in cells:
        if (i, j - 1) not in cells: edges[(i, j)] = (i + 1, j)
        if (i + 1, j) not in cells: edges[(i + 1, j)] = (i + 1, j + 1)
        if (i, j + 1) not in cells: edges[(i + 1, j + 1)] = (i, j + 1)
        if (i - 1, j) not in cells: edges[(i, j + 1)] = (i, j)
    nedges = sum(1 for (i, j) in cells for nb in ((i, j - 1), (i + 1, j), (i, j + 1), (i - 1, j)) if nb not in cells)
    assert nedges == len(edges), "a lattice point has two outgoing boundary edges (not simple)"
    start = min(edges); loop = [start]; p = edges[start]
    while p != start:
        loop.append(p); p = edges[p]
    one_loop = len(loop) == len(edges)
    # vertices = direction changes
    n = len(loop); verts = []; refl = conv = 0
    for k in range(n):
        a, b, c = loop[k - 1], loop[k], loop[(k + 1) % n]
        d1 = (b[0] - a[0], b[1] - a[1]); d2 = (c[0] - b[0], c[1] - b[1])
        cr = d1[0] * d2[1] - d1[1] * d2[0]
        if cr != 0:
            verts.append(b)
            if cr > 0: conv += 1
            else: refl += 1
    hl, vl = [], []
    for k in range(len(verts)):
        a, b = verts[k], verts[(k + 1) % len(verts)]
        (hl if a[1] == b[1] else vl).append(abs(a[0] - b[0]) + abs(a[1] - b[1]))
    gh = 0
    for v in hl: gh = gcd(gh, v)
    gv = 0
    for v in vl: gv = gcd(gv, v)
    return cells, one_loop, len(verts), refl, conv, gh, gv, len(cells)


def interior_lattice(cells, p):
    x, y = p
    return all(c in cells for c in ((x, y), (x - 1, y), (x, y - 1), (x - 1, y - 1)))


# ---------------------------------------------------------------- passage tracer
def ptrace(bands, S, targets, a, b, e, ey, kcap, record=False):
    """One congruence per band passage.  Direction: horizontal sign e, vertical
    sign ey, slope s = a/b = |dx/dy| (a, b > 0).  Scaled abscissa X = b*x.
    Returns (status, info, k, R, events)."""
    i = next(n for n, bd in enumerate(bands) if bd[0] < S[1] < bd[1])
    X = b * S[0]; y = S[1]; R = 0; ev = []
    for k in range(1, kcap + 1):
        y0, y1, x0, x1 = bands[i]
        l = b * x0; u = b * (x1 - x0); U2 = 2 * u
        yend = y1 if ey > 0 else y0
        P = (X - l) if e > 0 else (U2 - (X - l))
        for t, (tx, ty) in enumerate(targets):
            if y0 < ty < y1 and (ty - y) * ey > 0:
                PT = P + abs(ty - y) * a
                q = PT % U2
                XT = l + q if q <= u else l + U2 - q
                if XT == b * tx:
                    R += (PT - 1) // u - P // u
                    if record: ev.append((k, i, 'T', t))
                    return 'hit', t, k, R, ev
        Pn = P + abs(yend - y) * a
        q = Pn % U2
        if q % u == 0:
            return 'corner', (i, yend), k, R, ev
        R += (Pn - 1) // u - P // u
        Xn, en = (l + q, 1) if q < u else (l + U2 - q, -1)
        j = i + ey
        nb = bands[j] if 0 <= j < len(bands) and (bands[j][0] == yend or bands[j][1] == yend) else None
        ends = {b * x0, b * x1}
        if nb: ends |= {b * nb[2], b * nb[3]}
        if Xn in ends:
            return 'corner', (i, yend), k, R, ev
        if nb and b * max(x0, nb[2]) < Xn < b * min(x1, nb[3]):
            typ = 'cross'; i = j
        else:
            typ = 'mirror'; ey = -ey; R += 1
        if record: ev.append((k, yend, F(Xn, b), en, typ, i))
        X, e, y = Xn, en, yend
    return 'cap', None, kcap, R, ev


# ---------------------------------------------------------------- cell tracer
def ctrace(cells, S, T, vx, vy, hcuts, vcuts, maxsteps):
    """Exact Fraction ray through unit cells.  Returns dict or None (cap/stop)."""
    x, y = F(S[0]), F(S[1]); R = 0; hp = 1; vp = 1; steps = 0
    Tx, Ty = F(T[0]), F(T[1])
    while steps < maxsteps:
        steps += 1
        nx = (x.__floor__() + 1) if vx > 0 else (x.__ceil__() - 1)
        ny = (y.__floor__() + 1) if vy > 0 else (y.__ceil__() - 1)
        tx = (nx - x) / vx; ty = (ny - y) / vy; t = min(tx, ty)
        tt = (Tx - x) / vx
        if 0 < tt <= t and y + tt * vy == Ty:
            return dict(R=R, hpass=hp, vpass=vp, steps=steps)
        x += t * vx; y += t * vy
        if tx < ty:      # vertical grid line, non-lattice point
            X = int(x); row = y.__floor__()
            ahead = (X if vx > 0 else X - 1, row)
            if ahead in cells:
                if X in vcuts: vp += 1
            else:
                vx = -vx; R += 1; vp += 1
        elif ty < tx:    # horizontal grid line
            Y = int(y); col = x.__floor__()
            ahead = (col, Y if vy > 0 else Y - 1)
            if ahead in cells:
                if Y in hcuts: hp += 1
            else:
                vy = -vy; R += 1; hp += 1
        else:            # lattice point
            X, Y = int(x), int(y)
            cxa = X if vx > 0 else X - 1; cxb = X - 1 if vx > 0 else X
            cya = Y if vy > 0 else Y - 1; cyb = Y - 1 if vy > 0 else Y
            Hc = (cxa, cyb) in cells; Vc = (cxb, cya) in cells; Ac = (cxa, cya) in cells
            if Hc and Vc and Ac:
                if X in vcuts: vp += 1
                if Y in hcuts: hp += 1
            elif Hc and not Vc and not Ac:
                vy = -vy; R += 1; hp += 1
                if X in vcuts: vp += 1
            elif Vc and not Hc and not Ac:
                vx = -vx; R += 1; vp += 1
                if Y in hcuts: hp += 1
            else:
                return None   # reflex or convex corner: stop
    return None


def log(*a):
    print(*a, flush=True)


# =============================================================== run
MS = [8, 16, 24, 32]
log("D131 checks: passage-complexity snapshot 2026-11-21-2125")
log("\n== A. Room facts and marks ==")
CELLS = {}
for m in MS + [64]:
    cells, one, nv, refl, conv, gh, gv, area = room_facts(m)
    CELLS[m] = cells
    S, T, J = marks(m)
    par = all(c % 2 == 0 for p in [S] + T for c in p)
    inS = interior_lattice(cells, S) and S[0] < m and S[1] < m
    inT = all(interior_lattice(cells, t) and t[0] > m + 2 and t[1] > m + 2 for t in T)
    log(f"m={m:3d} area={area} (2m^2+6={2*m*m+6}) loop={one} vertices={nv} reflex={refl} convex={conv} "
        f"gcd_h={gh} gcd_v={gv} | S={S} T_j j=-{J}..{J}: {T[0]}..{T[-1]} count={len(T)} "
        f"even={par} S_in_lower={inS} T_in_upper={inT}")

log("\n== B. Slope-shift lemma: events for s vs s+24 (and controls) ==")
for m in (8, 16):
    bands = st279(m); S, T, J = marks(m)
    tot = same24 = same12 = same8 = 0
    neck = top = down = mir = mirmid = 0
    same24h = same12h = hits = 0; over26 = 0; worst = F(0)
    for b in range(1, 31):
        for a in range(1, 24 * b + 1):
            if gcd(a, b) != 1: continue
            for e in (1, -1):
                for ey in (1, -1):
                    r0 = ptrace(bands, S, [], a, b, e, ey, 60, True)
                    r24 = ptrace(bands, S, [], a + 24 * b, b, e, ey, 60, True)
                    r12 = ptrace(bands, S, [], a + 12 * b, b, e, ey, 60, True)
                    r8 = ptrace(bands, S, [], a + 8 * b, b, e, ey, 60, True)
                    tot += 1
                    key = lambda r: (r[0], r[1], r[4])
                    same24 += key(r0) == key(r24); same12 += key(r0) == key(r12); same8 += key(r0) == key(r8)
                    ev = r0[4]
                    neck += any(x[5] >= 1 for x in ev)
                    top += any(x[5] == 3 for x in ev)
                    down += any(x[4] == 'cross' and x[5] >= 1 and ev[n + 1][5] < x[5] if n + 1 < len(ev) else False
                                for n, x in enumerate(ev))
                    mir += any(x[4] == 'mirror' for x in ev)
                    mirmid += any(x[4] == 'mirror' and x[5] in (1, 2) for x in ev)
                    h0 = ptrace(bands, S, T, a, b, e, ey, 60)[:3]
                    h24 = ptrace(bands, S, T, a + 24 * b, b, e, ey, 60)[:3]
                    h12 = ptrace(bands, S, T, a + 12 * b, b, e, ey, 60)[:3]
                    hits += h0[0] == 'hit'; same24h += h0 == h24; same12h += h0 == h12
                    if h0[0] == 'hit':
                        Rh = ptrace(bands, S, T, a, b, e, ey, 60)[3]
                        over26 += Rh > 26 * h0[2]; worst = max(worst, F(Rh, h0[2]))
    log(f"m={m}: rays from S (4 senses, s=a/b in (0,24], b<=30, 60 passages) = {tot}")
    log(f"  no targets: event lists identical for s+24: {same24}; s+12: {same12}; s+8: {same8}")
    log(f"  rays entering the neck: {neck}; reaching the upper square: {top}; "
        f"returning down through an interface: {down}; with a mirror event: {mir}; mirror in a middle band: {mirmid}")
    log(f"  with the target row: (status, target, k) identical for s+24 on {same24h}/{tot} "
        f"({hits} rays hit some T_j); for s+12 on {same12h}/{tot}")
    log(f"  hits with s in (0,24]: R > 26k on {over26}; largest R/k = {worst} = {float(worst):.2f}")

log("\n== C. Horizontal decomposition: lit T_j, passages, replay ==")
BMAX = 60; KCAP = 60
summary = {}
for m in MS:
    bands = st279(m); S, T, J = marks(m); cells = CELLS[m]
    best = {}
    t0 = time.process_time()
    for b in range(1, BMAX + 1):
        for a in range(1, 24 * b + 1):
            if gcd(a, b) != 1: continue
            for e in (1, -1):
                for ey in (1, -1):
                    st, t, k, R, _ = ptrace(bands, S, T, a, b, e, ey, KCAP)
                    if st == 'hit' and (t not in best or k < best[t][0] or (k == best[t][0] and R < best[t][1])):
                        best[t] = (k, R, a, b, e, ey)
    log(f"m={m}: search s=a/b in (0,24], b<={BMAX}, <= {KCAP} passages, {time.process_time()-t0:.1f}s CPU")
    hc = {m, m + 1, m + 2}; vc = {m - 1, m, m + 2, m + 3}
    ks = []
    for t in range(len(T)):
        j = t - J
        if t not in best:
            log(f"   j={j:+d} T={T[t]}: no route found in the searched set")
            continue
        k, R, a, b, e, ey = best[t]; ks.append(k)
        rep = ctrace(cells, S, T[t], e * a, ey * b, hc, vc, 200000)
        ok = rep is not None and rep['R'] == R and rep['hpass'] == k
        shifts = []
        for sh in (1, 2):
            st2, t2, k2, R2, _ = ptrace(bands, S, T, a + 24 * sh * b, b, e, ey, KCAP)
            shifts.append((st2 == 'hit' and t2 == t and k2 == k, R2))
        log(f"   j={j:+d} T={T[t]}: lit, dir=({e*a},{ey*b}) s={F(a,b)} k={k} R={R} "
            f"<=26k:{R <= 26*k} cell-replay(R,hpass,vpass)={(rep['R'],rep['hpass'],rep['vpass']) if rep else None} "
            f"match={ok} | s+24,s+48 same target & k: {[x[0] for x in shifts]} R={[x[1] for x in shifts]}")
    summary[m] = (len(best), len(T), min(ks) if ks else None, max(ks) if ks else None)
log("summary m: (lit found, targets, min k, max k) =", summary)

log("\n== D. Explicit constant of the determinant bound ==")


def forced_R(m):
    d0 = (2 + sqrt(m)) / m + 1 / m        # endpoint errors (T: x <= (2+sqrt m)/m, y 2/m; crossing 1/m)
    R = 0
    while True:
        d = d0 + 6 * R / m
        if 12 * (R + 1) * d + 2 * d * d >= 1 / 8:
            return R
        R += 1


for m in [8, 64, 10**4, 10**6, 10**8, 4 * 10**8, 10**9, 10**10]:
    R = forced_R(m)
    log(f"m={m:>12}: inequality forces R >= {R:>6}; passages k >= max(4, ceil(R/26)) = {max(4, -(-R // 26))}")
lo, hi = 8, 10**12
while hi - lo > 1:
    mid = (lo + hi) // 2
    if -(-forced_R(mid) // 26) >= 5: hi = mid
    else: lo = mid
log(f"smallest m with forced k >= 5 (beats the trivial 4): about {hi:.3e}")

log("\n== E. Vertical decomposition of the same room ==")
VMS = [8, 16, 32, 64, 128, 256]
for m in VMS:
    vb = transpose_bands(m); S, T, J = marks(m)
    TT = [(t[1], t[0]) for t in T]; ST = (S[1], S[0])
    found = {}
    t0 = time.process_time()
    for b in range(1, 17):
        for a in range(1, 40 * m + 1):
            if gcd(a, b) != 1: continue
            for e in (1, -1):
                for ey in (1, -1):
                    st, t, k, R, _ = ptrace(vb, ST, TT, a, b, e, ey, 9)
                    if st == 'hit' and (t not in found or k < found[t][0]):
                        found[t] = (k, R, a, b, e, ey)
    log(f"m={m}: {len(found)}/{len(T)} targets lit with <= 9 vertical passages "
        f"(slopes a/b, b<=16, a<=40m), {time.process_time()-t0:.1f}s CPU; "
        f"(j, fewest vertical passages): {sorted((t - J, found[t][0]) for t in found)}")
    if m <= 32:
        cells = CELLS[m]; hc = {m, m + 1, m + 2}; vc = {m - 1, m, m + 2, m + 3}
        for t in sorted(found, key=lambda t: found[t][0])[:3]:
            k, R, a, b, e, ey = found[t]
            # transposed direction (x^T, y^T) = (e a, ey b)  ->  original (vx, vy) = (ey b, e a)
            rep = ctrace(cells, S, T[t], ey * b, e * a, hc, vc, 400000)
            log(f"   j={t-J:+d} T={T[t]} original dir=({ey*b},{e*a}) vertical k={k} R={R} | cell replay: "
                f"{'R=%d vpass=%d hpass=%d' % (rep['R'], rep['vpass'], rep['hpass']) if rep else 'FAILED'}")

log(f"\nTotal CPU {time.process_time()-CPU0:.1f}s")
