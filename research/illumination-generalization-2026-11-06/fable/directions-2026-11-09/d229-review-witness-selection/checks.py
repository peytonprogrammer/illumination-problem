"""D229 independent review of l1-witness-selection (note-snapshot.md).

Reuses the exact Fraction tracer from ../d227-review-pinned-pairs/checks.py.
Named families only: the five-reflex parabola room and the seven-reflex window room of
l1-excursion-normal-form.md. Every (m,u), c and direction is hand-chosen and listed; no sweeps.
Run: nice -n 10 python3 -B checks.py
"""
import os
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'd227-review-pinned-pairs'))
import checks as d227  # noqa: E402  (main guarded by __name__)

trace, inside, fmt = d227.trace, d227.inside, d227.fmt
orthogonal, strictly_simple, reflex_count = d227.orthogonal, d227.strictly_simple, d227.reflex_count

T0 = time.process_time()
FAILS = []


def say(*a):
    print(*a, flush=True)


def check(cond, msg):
    say(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


def from_tiers(tiers):
    """tiers: list of ((y0,y1),(l,r)) bottom to top; interior of the union of closed rectangles."""
    R, L = [], []
    for (y0, y1), (l, r) in tiers:
        R += [(r, y0), (r, y1)]
    for (y0, y1), (l, r) in reversed(tiers):
        L += [(l, y1), (l, y0)]
    out = []
    for p in R + L:
        if not out or out[-1] != p:
            out.append(p)
    if out[0] == out[-1]:
        out.pop()
    changed = True
    while changed:
        changed = False
        for i in range(len(out)):
            a, b, c = out[i - 1], out[i], out[(i + 1) % len(out)]
            if a[0] == b[0] == c[0] or a[1] == b[1] == c[1]:
                out.pop(i)
                changed = True
                break
    return out


def five(m, u):
    m, u = F(m), F(u)
    lv = [F(-1), F(0), m, u - 1, u, u + 1]
    iv = [(F(-2), F(1)), (F(-1), F(1)), (F(0), m), (F(0), m + 2), (F(0), m + 3)]
    return from_tiers([((lv[i], lv[i + 1]), iv[i]) for i in range(5)])


def seven(c):
    c = F(c)
    iv = [(-2, 4), (-1, 4), (0, 10), (4, 11), (2, 8)]
    return from_tiers([((F(i - 1), F(i)), (c * a, c * b)) for i, (a, b) in enumerate(iv)])


def pinned(P, p):
    return p[0] in {v[0] for v in P} and p[1] in {v[1] for v in P}


def nearest_j(m2, V):
    """nearest nonnegative j to m2/(2V) (either one on a tie)."""
    j = m2 // (2 * V)
    return j if abs(m2 - 2 * j * V) <= abs(m2 - 2 * (j + 1) * V) else j + 1


def note_witness(m, u):
    """The note's winding choice. Returns dict with D, j, delta, p, sigma, branch."""
    U = u - m
    m2 = m * m
    D, V, branch = u, U, 'nearest'
    j = nearest_j(m2, V)
    if m2 - 2 * j * V == 0:
        if U < m:
            j, branch = j + 1, 'j+1'
        else:
            assert m2 % (2 * U) == 0
            branch = 'roof'
            D, V = u + 2, U + 2
            j = nearest_j(m2, V)
    err = m2 - 2 * j * V
    delta = F(err, D)
    p = F(m + 2 * j, D)
    sgn = 1 if delta > 0 else -1
    sigma = sgn * (-1) ** j
    return dict(U=U, D=D, V=V, j=j, err=err, delta=delta, p=p, sigma=sigma, branch=branch)


def crossing_x(path, y):
    """abscissa of the first strict crossing of level y (reflection points never lie on y here)."""
    for (ax, ay), (bx, by) in zip(path, path[1:]):
        if (ay - y) * (by - y) < 0:
            return ax + (bx - ax) * (y - ay) / (by - ay)
    return None


# ------------------------------------------------------------------ claim 1
POINTS = [(3, 5), (4, 6), (6, 9), (4, 12), (6, 24), (5, 24), (5, 25), (5, 26), (20, 22), (20, 220), (20, 401)]


def claim1():
    say("\n=== Claim 1: five-reflex parabola room is strictly simple, 5 reflexes, marks interior and pinned")
    for m, u in POINTS:
        P = five(m, u)
        S, T = (F(0), F(0)), (F(m), F(u))
        check(orthogonal(P) and strictly_simple(P) and reflex_count(P) == 5 and len(P) == 14 and
              inside(P, S) and inside(P, T) and pinned(P, S) and pinned(P, T),
              f"(m,u)=({m},{u}): 14 vertices, orthogonal, strictly simple, 5 reflexes, S,T interior and pinned")


# ------------------------------------------------------------------ claims 2-3
def claim23():
    say("\n=== Claims 2-3: winding choice, gate lemma, exact traces of the note's witness")
    for m, u in POINTS:
        w = note_witness(m, u)
        U, D, j, d, p = w['U'], w['D'], w['j'], w['delta'], w['p']
        roof = w['branch'] == 'roof'
        arith = 0 < abs(d) < 1 and abs(w['err']) < D
        if roof:
            arith = arith and (m * m) % (2 * U) == 0 and U >= m and (m * m) % (2 * (U + 2)) != 0 and m - p > 0 and p < 1
        if w['branch'] == 'j+1':
            arith = arith and abs(w['err']) == 2 * U and 2 * U < u
        check(arith, f"(m,u)=({m},{u}) U={U} branch={w['branch']} D={D} j={j} err={w['err']} delta={d} p={p}: "
                     f"0<|delta|<1, |err|<D" + (", 2(U+2)!|m^2, m-p>0" if roof else ""))
        P = five(m, u)
        S, T = (F(0), F(0)), (F(m), F(u))
        res, _, path = trace(P, S, (w['sigma'] * (m + 2 * j), D), T, maxref=4 * (m + 2 * j) + 20)
        refl = path[1:-1]
        low = [q for q in refl if q[1] < m]
        high = [q for q in refl if q[1] > m]
        alt = all(abs(q[0]) == 1 for q in low) and all(a[0] == -b[0] for a, b in zip(low, low[1:]))
        gx = crossing_x(path, F(m))
        exp_high = ([(F(0), F(2 * j) / p)] if d < 0 else [])
        if roof:
            exp_high.append((m - p, F(u + 1)))
        check(res == 'T' and gx == abs(d) and alt and sorted(high) == sorted(exp_high),
              f"(m,u)=({m},{u}) dir=({w['sigma'] * (m + 2 * j)},{D}): {res}; {len(low)} narrow-tier bounces "
              f"alternating x=+-1; gate x={gx} (=|delta|); upper reflections {[fmt(q) for q in high]}")
    say("-- direct template (j=0, no roof) near u=m^2, m=5")
    for u, want in ((24, False), (25, False), (26, True)):
        res, pt, _ = trace(five(5, u), (F(0), F(0)), (5, u), (F(5), F(u)))
        check((res == 'T') == want, f"(5,{u}) direct chord: {res} {fmt(pt)}; expected lit={want}")


# ------------------------------------------------------------------ claim 4
def claim4():
    say("\n=== Claim 4: seven-reflex window room, witness (-5c,1)")
    base = None
    for c in (1, 2, 9):
        P = seven(c)
        S, T = (F(0), F(0)), (F(8 * c), F(2))
        res, _, path = trace(P, S, (-5 * c, 1), T)
        ok = orthogonal(P) and strictly_simple(P) and reflex_count(P) == 7 and inside(P, S) and inside(P, T) \
            and pinned(P, S) and pinned(P, T)
        if base is None:
            base = path
        scaled = [(q[0] * c, q[1]) for q in base] == path
        check(ok and res == 'T' and path[1] == (F(-c), F(1, 5)) and crossing_x(path, F(1)) == 3 * c and scaled,
              f"c={c}: room ok (7 reflexes, pinned), {res}, path {[fmt(q) for q in path]} = c-scaled c=1 path")


# ------------------------------------------------------------------ claim 5
def unfold(path):
    """developed points of a traced path, starting direction kept."""
    out = [path[0]]
    sx = sy = None
    for a, b in zip(path, path[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        if sx is None:
            sx, sy = (1 if dx > 0 else -1), (1 if dy > 0 else -1)
        out.append((out[-1][0] + sx * abs(dx), out[-1][1] + sy * abs(dy)))
    return out


def claim5():
    say("\n=== Claim 5: cycle translation and affine cleared tests (narrow-tier cycle of the (20,22) witness)")
    m, u = 20, 22
    w = note_witness(m, u)
    _, _, path = trace(five(m, u), (F(0), F(0)), (w['sigma'] * (m + 2 * w['j']), w['D']), (F(m), F(u)), maxref=1000)
    dev = unfold(path)
    Dx, Dy = dev[-1][0] - dev[0][0], dev[-1][1] - dev[0][1]
    sgn = 1 if Dx > 0 else -1
    for wall in (1, -1):
        idx = [i for i, q in enumerate(path[1:-1], 1) if q[1] < m and q[0] == wall]
        X = [dev[i][0] for i in idx]
        diffs = {b - a for a, b in zip(X, X[1:])}
        # cleared face test for face x=a, ordinates (0,m): 0 < a*Dy*sgn < m*|Dx|
        t1 = [a * Dy * sgn for a in X]
        t2 = [m * abs(Dx) - a * Dy * sgn for a in X]
        aff = all(len({b - a for a, b in zip(t, t[1:])}) <= 1 for t in (t1, t2))
        ends = all(t[0] > 0 and t[-1] > 0 for t in (t1, t2))
        mid = all(v > 0 for v in t1 + t2)
        check(len(diffs) == 1 and abs(diffs.pop()) == 4 and aff and ends and mid,
              f"phase x={wall}: {len(X)} occurrences, developed faces translate by v=(+-4,0); "
              f"cleared tests affine in j; positive at extremes and hence everywhere")
    # time order between consecutive phases: developed times are affine too
    times = [dev[i][0] / Dx for i in range(1, len(path) - 1) if path[i][1] < m]
    gaps = {b - a for a, b in zip(times, times[1:])}
    check(len(gaps) == 1 and gaps.pop() > 0, "consecutive narrow-tier event times have constant positive spacing")


# ------------------------------------------------------------------ claim 6
def claim6():
    say("\n=== Claim 6: one-gap tail, fixed word m=5, j=1, delta>0 branch, gap g=u-1-m")
    m, j = 5, 1
    for u in (11, 12, 17, 18):
        # gate face y=m in developed coordinates (2j, 2j+1); target image (m+2j, u); tests affine in u
        a1 = m * (m + 2 * j) - 2 * j * u        # slope -2j < 0: tail infeasible
        a2 = (2 * j + 1) * u - m * (m + 2 * j)  # slope 2j+1 > 0
        pred = a1 > 0 and a2 > 0
        res, pt, _ = trace(five(m, u), (F(0), F(0)), ((-1) ** j * (m + 2 * j), u), (F(m), F(u)), maxref=100)
        check((res == 'T') == pred, f"u={u}: cleared gate tests ({a1},{a2}) predict lit={pred}; trace {res} {fmt(pt)}")


if __name__ == '__main__':
    claim1()
    claim23()
    claim4()
    claim5()
    claim6()
    say(f"\ncpu {time.process_time() - T0:.2f}s")
    say(f"FAILURES: {len(FAILS)}" + (f" ({FAILS})" if FAILS else ""))
