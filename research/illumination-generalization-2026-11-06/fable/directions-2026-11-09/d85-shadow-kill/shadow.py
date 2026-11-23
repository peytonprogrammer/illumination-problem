"""D85: shadow-budget kill test. |H_L(S)| in named orthogonal lattice rooms.

H_L(S) = same-parity interior/smooth lattice points of the room not reached by any
legal billiard path from S of unfolded length <= L. A path from lattice S whose
unfolded displacement is the integer vector D (both components even, so the end has
S's parity) is traced exactly in integers: crossing times i/|Dx| and j/|Dy| are
compared as i*|Dy| vs j*|Dx|. Any contact with a corner (convex or reflex), or a run
along a wall, makes the path illegal. Every legal path from S to a same-parity
lattice point unfolds to such a D, so the enumeration over the disk |D| <= L is
complete for length L.
"""
import json, sys, time
from math import isqrt, hypot
from itertools import combinations

sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/d8-perturbation-test')


def rect(x0, x1, y0, y1):
    return {(x, y) for x in range(x0, x1) for y in range(y0, y1)}


def cross(b):
    return rect(-b, b, -2, 2) | rect(-2, 2, -b, b)


def U2(k=0):  # copied from d84-review-cylinders/indep.py
    base = rect(0, 9, 0, 2) | rect(0, 2, 2, 9) | rect(7, 9, 2, 7) | rect(5, 7, 5, 7)
    return {(x + (4 * k if x >= 4 else 0), y) for x, y in base} | rect(4, 4 + 4 * k, 0, 2)


def incid(C, x, y):
    return ((x - 1, y - 1) in C) + ((x, y - 1) in C) + ((x - 1, y) in C) + ((x, y) in C)


def pinch(C, x, y):
    return incid(C, x, y) == 2 and ((x - 1, y - 1) in C) == ((x, y) in C)


def facts(C):
    pts = {(x + a, y + b) for x, y in C for a in (0, 1) for b in (0, 1)}
    corners = [p for p in pts if incid(C, *p) in (1, 3)]
    r = sum(incid(C, *p) == 3 for p in corners)
    regular = {p for p in pts if incid(C, *p) in (2, 4) and not pinch(C, *p)}
    assert not any(pinch(C, *p) for p in pts)
    diam = max(hypot(p[0] - q[0], p[1] - q[1]) for p, q in combinations(corners, 2))
    classes = sorted({(p[0] % 2, p[1] % 2) for p in regular if incid(C, *p) == 4})
    return dict(area=len(C), walls=len(corners), r=r, diam=diam, regular=regular, classes=classes)


def shoot(C, S, Dx, Dy):
    """Endpoint of the legal billiard path from S with unfolded displacement (Dx, Dy),
    or None if the path meets a corner or runs along a wall."""
    if Dx == 0 or Dy == 0:
        return shoot_axial(C, S, Dx, Dy)
    vx = 1 if Dx > 0 else -1
    vy = 1 if Dy > 0 else -1
    ax, ay = abs(Dx), abs(Dy)
    cx = S[0] if vx > 0 else S[0] - 1
    cy = S[1] if vy > 0 else S[1] - 1
    if (cx, cy) not in C:
        return None
    i = j = 0
    while True:
        a, b = (i + 1) * ay, (j + 1) * ax
        if a < b:
            i += 1
            if (cx + vx, cy) in C: cx += vx
            else: vx = -vx
        elif b < a:
            j += 1
            if (cx, cy + vy) in C: cy += vy
            else: vy = -vy
        else:
            i += 1; j += 1
            px, py = cx + (vx > 0), cy + (vy > 0)
            k = incid(C, px, py)
            if k not in (2, 4):
                return None
            if i == ax:
                return (px, py)
            if k == 4:
                cx += vx; cy += vy
            elif (cx + vx, cy) in C:      # horizontal wall through P
                vy = -vy; cx += vx
            elif (cx, cy + vy) in C:      # vertical wall through P
                vx = -vx; cy += vy
            else:
                raise AssertionError('pinch')


def shoot_axial(C, S, Dx, Dy):
    sw = Dx == 0
    b, A = (S[0], S[1]) if sw else (S[1], S[0])
    va = Dy if sw else Dx
    s = 1 if va > 0 else -1
    cell = (lambda u, v: (v, u)) if sw else (lambda u, v: (u, v))  # (along, across) -> cell
    pt = (lambda A: (b, A)) if sw else (lambda A: (A, b))

    def seg(A, s):
        lo = A if s > 0 else A - 1
        return (cell(lo, b - 1) in C) + (cell(lo, b) in C)

    for q in range(abs(va)):
        if q > 0 and incid(C, *pt(A)) not in (2, 4):
            return None
        k = seg(A, s)
        if k == 0:
            s = -s; k = seg(A, s)
        if k != 2:
            return None
        A += s
    p = pt(A)
    return p if incid(C, *p) in (2, 4) else None


def reach(C, S, L):
    """Minimal unfolded length (squared) at which each lattice point is reached."""
    best = {}
    R = isqrt(L * L)
    for Dx in range(-R - (R % 2), R + 1, 2):
        for Dy in range(-R - (R % 2), R + 1, 2):
            n = Dx * Dx + Dy * Dy
            if n == 0 or n > L * L:
                continue
            p = shoot(C, S, Dx, Dy)
            if p is not None and (p not in best or n < best[p]):
                best[p] = n
    return best


def run(name, C, S, mults):
    f = facts(C)
    assert incid(C, *S) == 4, (name, S)
    targets = {p for p in f['regular'] if (p[0] - S[0]) % 2 == 0 and (p[1] - S[1]) % 2 == 0 and p != S}
    Ls = [round(m * f['diam']) for m in mults]
    t = time.process_time()
    best = reach(C, S, Ls[-1])
    dt = time.process_time() - t
    H = {L: sorted(p for p in targets if best.get(p, 10**18) > L * L) for L in Ls}
    row = dict(room=name, area=f['area'], walls=f['walls'], r=f['r'], classes=f['classes'],
               S=S, targets=len(targets), diam=round(f['diam'], 2), L=Ls,
               H={L: len(h) for L, h in H.items()},
               Hpts={L: h for L, h in H.items() if len(h) <= 10}, cpu=round(dt, 1))
    print(json.dumps(row), flush=True)
    return row


if __name__ == '__main__':
    rooms = json.load(open(__file__.rsplit('/', 2)[0] + '/d8-perturbation-test/rooms.json'))
    byid = {r['id']: {tuple(c) for c in r['cells']} for r in rooms}
    mults = (2, 4, 8)
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if which in ('all', 'control'):
        run('R22', byid['R22-base'], (0, 0), mults)
        run('R22-L1-005', byid['R22-L1-005'], (0, 0), mults)
    if which in ('all', 'U2'):
        for k in (0, 2, 4, 6):
            for S in ((1, 1), (6 + 4 * k, 6)):
                run(f'U2 k={k}', U2(k), S, mults)
    if which in ('all', 'cross'):
        for b in (7, 9, 11, 13, 15, 17):
            for S in ((0, 0), (b - 1, 1)):
                run(f'cross b={b}', cross(b), S, mults)
