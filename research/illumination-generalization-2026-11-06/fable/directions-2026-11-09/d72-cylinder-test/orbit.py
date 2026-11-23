"""d72: exact all-direction CC test by SL2(Z)-orbit enumeration of the coloured origami.

Colours on squares (by LL corner): 1 marked (vertex lift), 2 lift of S, 3 lift of T, 0 other.
For every M in SL2(Z), M.X is reached by BFS over the generators T, V (a finite orbit, so
forward closure = group orbit).  Elements are stored up to relabelling (canonical form:
BFS numbering from each colour-2 square, minimum).  CC holds in some rational direction iff
some orbit element has a colour-2 and a colour-3 square in one horizontal open cylinder.
Every primitive direction v is M^-1 (1, 0) for some M, so the test is complete when BFS ends.
Usage: python3 -B orbit.py ROOM:Sx,Sy:Tx,Ty ... [--cap N]
"""
import sys
import time
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cyl  # noqa: E402


def canon(r, u, col):
    best = None
    N = len(r)
    for s0 in (i for i in range(N) if col[i] == 2):
        lab = {s0: 0}
        order = [s0]
        k = 0
        while k < len(order):
            i = order[k]
            k += 1
            for j in (r[i], u[i]):
                if j not in lab:
                    lab[j] = len(order)
                    order.append(j)
        key = tuple(lab[r[i]] for i in order) + tuple(lab[u[i]] for i in order) + tuple(col[i] for i in order)
        if best is None or key < best:
            best = key
    return best


def unpack(key, N):
    return list(key[:N]), list(key[N:2 * N]), list(key[2 * N:])


class Marked:
    def __init__(self, col):
        self.marked = [c == 1 for c in col]


def has_cc(r, u, col):
    Dc = cyl.Decomp(Marked(col), r, u)
    ss = [i for i in range(len(r)) if col[i] == 2]
    ts = [i for i in range(len(r)) if col[i] == 3]
    return any(Dc.cc(s, t) for s in ss for t in ts)


def run(cells, S, T, cap):
    O = cyl.Origami(cells)
    N = len(O.sq)
    col = [1 if O.marked[i] else 2 if O.ll[i] == S else 3 if O.ll[i] == T else 0 for i in range(N)]
    k0 = canon(O.r, O.u, col)
    seen = {k0}
    dq = deque([k0])
    while dq:
        key = dq.popleft()
        r, u, c = unpack(key, N)
        if has_cc(r, u, c):
            return 'CC', len(seen)
        for g in (('T', 1),), (('V', 1),):
            r2, u2 = cyl.act(r, u, g)
            k2 = canon(r2, u2, c)
            if k2 not in seen:
                if len(seen) >= cap:
                    return 'CAP', len(seen)
                seen.add(k2)
                dq.append(k2)
    return 'NO_CC_ANY_DIRECTION', len(seen)


if __name__ == '__main__':
    args = sys.argv[1:]
    cap = 200000
    if '--cap' in args:
        i = args.index('--cap')
        cap = int(args[i + 1])
        args = args[:i] + args[i + 2:]
    rooms = dict(cyl.rooms())
    for a in args:
        t0 = time.process_time()
        nm, s, t = a.split(':')
        S = tuple(map(int, s.split(',')))
        T = tuple(map(int, t.split(',')))
        v, n = run(set(map(tuple, rooms[nm])), S, T, cap)
        print(nm, S, T, v, 'orbit elements', n, 'CPU %.1f s' % (time.process_time() - t0), flush=True)
