"""d102: replay the saved Q-class witnesses with an independent exact tracer.

The tracer is d67's integer billiard (indep.shoot) with two changes: it stops at
the target, and it counts lattice-point events so the saved step count m can be
compared. It imports nothing from qclass-closure or d9; it reads only the
witness files.

Per room it also checks, with d67's geometry helpers: strict simplicity, wall
count <= 20, a corner-only parity class, and that the saved pairs are exactly
the unordered pairs of interior lattice points.

Usage: python3 -B replay.py SEED NROOMS   (NROOMS = 0 replays every room)
"""
import gzip
import random
import sys
import time
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'd67-review-d64'))
import indep as I  # noqa: E402

Q = Path(__file__).resolve().parents[4] / 'qclass-closure'


def trace(cs, S, T, dx, dy, m):
    """Return the lattice-step count at which the path from S first reaches T, or None.
    Absorbed at convex, reflex and pinch points. Gives up after m + 1 lattice steps."""
    p, q = abs(dx), abs(dy)
    sx, sy = (1 if dx >= 0 else -1), (1 if dy >= 0 else -1)
    X, Y = S
    if p == 0 or q == 0:
        if p + q != 1:
            return None
        ex, ey = (sx, 0) if q == 0 else (0, sy)
        for step in range(1, m + 2):
            X += ex
            Y += ey
            k = sum(c in cs for c in I.vertex_cells(X, Y))
            if k == 2:
                ex, ey = -ex, -ey
            elif k != 4:
                return None
            if (X, Y) == T:
                return step
        return None
    Xs, Ys = X * q, Y * p
    step = 0
    while step <= m:
        rx, ry = Xs % q, Ys % p
        ddx = (q - rx) if sx > 0 else (rx if rx else q)
        ddy = (p - ry) if sy > 0 else (ry if ry else p)
        st = min(ddx, ddy)
        Xs += sx * st
        Ys += sy * st
        if ddx == ddy:
            step += 1
            x, y = Xs // q, Ys // p
            fi = x - 1 if sx > 0 else x
            fj = y - 1 if sy > 0 else y
            ai = x if sx > 0 else x - 1
            aj = y if sy > 0 else y - 1
            if (fi, fj) not in cs:
                return None          # should never happen: we arrive from inside
            hA, vA, dg = (ai, fj) in cs, (fi, aj) in cs, (ai, aj) in cs
            k = 1 + hA + vA + dg
            if k == 4:
                pass
            elif k == 2 and hA:
                sy = -sy
            elif k == 2 and vA:
                sx = -sx
            else:
                return None
            if (x, y) == T:
                return step
        elif ddx < ddy:
            x, j = Xs // q, Ys // p
            if (x if sx > 0 else x - 1, j) not in cs:
                sx = -sx
        else:
            y, i = Ys // p, Xs // q
            if (i, y if sy > 0 else y - 1) not in cs:
                sy = -sy
    return None


def rooms(name):
    cells = rows = None
    with gzip.open(Q / name, 'rt') as f:
        for line in f:
            t = line[0]
            if t == 'R':
                if cells is not None:
                    yield cells, rows
                a = list(map(int, line.split()[1:]))
                cells = tuple(zip(a[4::2], a[5::2]))
                assert len(cells) == a[1]
                rows = []
            elif t == 'P':
                rows.append(line.split())
    if cells is not None:
        yield cells, rows


def check_room(cells, rows, retry, c, bad):
    cs = set(cells)
    pts = I.lattice_pts(cs)
    st = {pt: I.vstatus(cs, pt) for pt in pts}
    walls = sum(v in ('cvx', 'rfx') for v in st.values())
    qok = any(all(st[pt] in ('cvx', 'rfx') for pt in pts if (pt[0] % 2, pt[1] % 2) == cl)
              for cl in ((0, 0), (0, 1), (1, 0), (1, 1)))
    if not (qok and walls <= 20 and I.strictly_simple(cs)):
        c['hyp_fail'] += 1
        bad.append(('hyp', cells))
    inter = sorted(pt for pt, v in st.items() if v == 'int')
    want = set(combinations(inter, 2))
    seen = set()
    for r in rows:
        S, T = (int(r[1]), int(r[2])), (int(r[3]), int(r[4]))
        key = tuple(sorted((S, T)))
        if key in seen or key not in want:
            c['pair_extra_or_dup'] += 1
            bad.append(('pair', cells, key))
        seen.add(key)
        if r[5] == 'U':
            c['first_pass_U'] += 1
            w = retry.get(cells, {}).get(key)
            if w is None:
                c['U_no_retry'] += 1
                bad.append(('noretry', cells, key))
                continue
            S, T, dx, dy, m = w
            c['retry_used'] += 1
        else:
            dx, dy, m = int(r[7]), int(r[8]), int(r[9])
        c['witnesses'] += 1
        got = trace(cs, S, T, dx, dy, m)
        if got is None:
            c['FAIL'] += 1
            bad.append(('fail', cells, S, T, dx, dy, m))
        elif got != m:
            c['lit_but_m_differs'] += 1
    c['pair_missing'] += len(want - seen)
    if want - seen:
        bad.append(('missing', cells, sorted(want - seen)[:3]))


def main():
    seed, N = int(sys.argv[1]), int(sys.argv[2])
    t0 = time.process_time()
    retry = {}
    for cells, rows in rooms('witnesses-retry.txt.gz'):
        d = retry.setdefault(cells, {})
        for r in rows:
            S, T = (int(r[1]), int(r[2])), (int(r[3]), int(r[4]))
            d[tuple(sorted((S, T)))] = (S, T, int(r[7]), int(r[8]), int(r[9]))
    total = 780565
    keep = None
    if N:
        random.seed(seed)
        keep = set(random.sample(range(total), N))
    c = {k: 0 for k in ('rooms', 'hyp_fail', 'witnesses', 'FAIL', 'lit_but_m_differs', 'first_pass_U',
                        'retry_used', 'U_no_retry', 'pair_missing', 'pair_extra_or_dup')}
    bad = []
    t_parse = time.process_time()
    for idx, (cells, rows) in enumerate(rooms('witnesses.txt.gz')):
        if keep is not None and idx not in keep:
            continue
        c['rooms'] += 1
        check_room(cells, rows, retry, c, bad)
    t1 = time.process_time()
    print('seed', seed, 'requested rooms', N or 'all', c)
    for b in bad[:20]:
        print('BAD', b)
    print('CPU total %.1f s (retry load %.1f s)' % (t1 - t0, t_parse - t0))


if __name__ == '__main__':
    main()
