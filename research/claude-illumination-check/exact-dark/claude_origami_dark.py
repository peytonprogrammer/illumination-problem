"""Exact, complete darkness decision for canonical 45-degree rooms (no ray bound).

Unfold the room to X = room x D4. X is square-tiled by unit squares, every vertex is an
integer point, and source and target lifts lie over 0 mod 2Z^2. A connecting segment
therefore has rational direction v = k(p, q) with (p, q) primitive. It meets integer points
exactly at each multiple of (p, q), and between them meets no vertex. Each integer point is a
blocker (a corner lift: cone or rho-fixed), a target lift, or transparent (regular, not
rho-fixed: an interior or smooth-boundary point of the room). Some gamma in SL(2,Z) maps
(p, q) to (1, 0), and the direction-(p, q) flow on X becomes the horizontal flow on gamma X.

So the room is dark exactly when, for every labelled origami Y in the SL(2,Z) orbit of X and
every source square i, the walk i, r(i), r(r(i)), ... meets a blocker corner before a target
corner. The orbit is finite. Shears T: (r, u) -> (r, u r^-1) and T': (r, u) -> (r u^-1, u)
generate SL(2,Z) and fix every square's lower-left corner, so per-square corner labels carry
over unchanged.
Usage: claude_origami_dark.py room.json [room.json ...]
"""
import json
import sys
from collections import deque
from itertools import combinations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent/'refolding'))
from claude_unfold import G, NEG, app, mul, refl  # noqa: E402

BLOCK, TARGET, SOURCE, CLEAR = 'B', 'T', 'S', '.'


def origami(room):
    """Return (r, u, label) for the unfolded room; label[i] is the lower-left corner's role."""
    tiles = [tuple(sorted(map(tuple, t))) for t in room['triangles']]
    slits = {tuple(sorted(map(tuple, s))) for s in room.get('slits', [])}
    marks = [tuple(p) for p in room['marked']]
    owners = {}
    for i, t in enumerate(tiles):
        for e in combinations(t, 2):
            owners.setdefault(e, []).append(i)
    par = {}

    def find(x):
        par.setdefault(x, x)
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    nbr = {}
    for e, own in owners.items():
        s = tuple(tuple(int(v) for v in row) for row in refl(e))
        for i in own:
            for g in G:
                if len(own) == 2 and e not in slits:
                    j, h = (own[0] if own[1] == i else own[1]), g
                else:
                    j, h = i, mul(g, s)
                nbr[(i, g), e] = (j, h)
                for p in e:
                    par[find((i, g, p))] = find((j, h, p))
    cells = [(i, g) for i in range(len(tiles)) for g in G]
    members = {}
    for i, g in cells:
        for p in tiles[i]:
            members.setdefault(find((i, g, p)), []).append((i, g, p))

    def ang(i, p):
        a, b = [q for q in tiles[i] if q != p]
        return 2 if (a[0]-p[0])*(b[0]-p[0])+(a[1]-p[1])*(b[1]-p[1]) == 0 else 1
    m = {v: sum(ang(i, p) for i, g, p in ms)//8 for v, ms in members.items()}
    rho = {v: find((ms[0][0], mul(NEG, ms[0][1]), ms[0][2])) for v, ms in members.items()}
    role = {}
    for v, ms in members.items():
        q = ms[0][2]
        if m[v] > 1 or (rho[v] == v and __import__('os').environ.get('CLAUDE_RETRO90') != '1'):
            role[v] = BLOCK  # CLAUDE_RETRO90=1: regular corner lifts (90-degree corners) reflect straight back
        elif q == marks[0]:
            role[v] = SOURCE
        elif q == marks[1]:
            role[v] = TARGET
        else:
            role[v] = CLEAR
    dev = lambda c: [app(c[1], p) for p in tiles[c[0]]]
    sq_of, squares = {}, []
    for c in cells:
        if c in sq_of:
            continue
        d = dev(c)
        hyp = next(e for e in combinations(tiles[c[0]], 2) if abs(app(c[1], e[0])[0]-app(c[1], e[1])[0]) == 1
                   and abs(app(c[1], e[0])[1]-app(c[1], e[1])[1]) == 1)
        c2 = nbr[c, hyp]
        sq_of[c] = sq_of[c2] = len(squares); squares.append((c, c2))
    n = len(squares)

    def ll(k):
        """Lower-left corner of square k, in the chart of its first cell."""
        c, c2 = squares[k]
        d = dev(c)
        return min(x for x, y in d), min(y for x, y in d)

    def side(k, which):
        """Square across the given side of square k. which: 'R' (x = x0+1) or 'U' (y = y0+1)."""
        x0, y0 = ll(k)
        for cc, (sx, sy) in chart(k):
            for e in combinations(tiles[cc[0]], 2):
                a, b = app(cc[1], e[0]), app(cc[1], e[1])
                a, b = (a[0]+sx, a[1]+sy), (b[0]+sx, b[1]+sy)
                if which == 'R' and a[0] == b[0] == x0+1 or which == 'U' and a[1] == b[1] == y0+1:
                    return sq_of[nbr[cc, e]]
        raise AssertionError

    def chart(k):
        """Both cells of square k with the translation putting each in the first cell's chart."""
        c, c2 = squares[k]
        d, d2 = dev(c), dev(c2)
        hyp = sorted(p for p in d if sum(1 for q in d if abs(q[0]-p[0]) == 1 and abs(q[1]-p[1]) == 1))
        hyp2 = sorted(p for p in d2 if sum(1 for q in d2 if abs(q[0]-p[0]) == 1 and abs(q[1]-p[1]) == 1))
        shift = (hyp[0][0]-hyp2[0][0], hyp[0][1]-hyp2[0][1])
        assert [(x+shift[0], y+shift[1]) for x, y in hyp2] == hyp
        return [(c, (0, 0)), (c2, shift)]
    r = [side(k, 'R') for k in range(n)]
    u = [side(k, 'U') for k in range(n)]
    assert sorted(r) == list(range(n)) and sorted(u) == list(range(n))

    def corner_role(k):
        x0, y0 = ll(k)
        for cc, (sx, sy) in chart(k):
            for p in tiles[cc[0]]:
                if (app(cc[1], p)[0]+sx, app(cc[1], p)[1]+sy) == (x0, y0):
                    return role[find((cc[0], cc[1], p))]
        raise AssertionError
    label = ''.join(corner_role(k) for k in range(n))
    return r, u, label


def inv(p):
    q = [0]*len(p)
    for i, j in enumerate(p):
        q[j] = i
    return q


def canon(r, u, label):
    """Canonical form of a labelled origami up to square relabelling."""
    best = None
    n = len(r)
    for s in range(n):
        if label[s] != max(label):  # only start from squares with the lexicographically largest label
            continue
        order = {s: 0}; q = deque([s])
        while q:
            i = q.popleft()
            for j in (r[i], u[i]):
                if j not in order:
                    order[j] = len(order); q.append(j)
        if len(order) < n:
            raise ValueError('disconnected')
        inv_o = sorted(order, key=order.get)
        key = (tuple(order[r[i]] for i in inv_o), tuple(order[u[i]] for i in inv_o), ''.join(label[i] for i in inv_o))
        if best is None or key < best:
            best = key
    return best


def horizontal_lit(r, label):
    """Return a source square whose rightward walk meets a target before a blocker, else None."""
    for i, lab in enumerate(label):
        if lab != SOURCE:
            continue
        j = r[i]
        while j != i:
            if label[j] == BLOCK:
                break
            if label[j] == TARGET:
                return i
            j = r[j]
    return None


def components(r, u, label):
    """Split a possibly disconnected origami into relabelled connected components."""
    n = len(r); comp = [-1]*n; out = []
    for s0 in range(n):
        if comp[s0] >= 0:
            continue
        order = [s0]; comp[s0] = len(out)
        for i in order:
            for j in (r[i], u[i], r.index(i), u.index(i)):
                if comp[j] < 0:
                    comp[j] = len(out); order.append(j)
        idx = {old: k for k, old in enumerate(order)}
        out.append(([idx[r[i]] for i in order], [idx[u[i]] for i in order], ''.join(label[i] for i in order)))
    return out


def decide(room, cap=10**6):
    """Lit if some component of the unfolding has a lit direction; dark if none does."""
    r, u, label = origami(room)
    parts = components(r, u, label)
    results = [decide_one(*part, cap=cap) for part in parts if SOURCE in part[2] and TARGET in part[2]]
    for res in results:
        if res['status'] == 'lit':
            return dict(res, components=len(parts))
    if any(res['status'] == 'cap' for res in results):
        return dict(status='cap', components=len(parts), parts=results)
    return dict(status='dark', components=len(parts), parts=results)


def decide_one(r, u, label, cap=10**6):
    start = canon(r, u, label)
    seen = {start: ()}; q = deque([start]); visited = 0
    while q:
        key = q.popleft(); visited += 1
        if visited % 20000 == 0:
            print('  progress', visited, len(seen), flush=True)
        r_, u_, lab = list(key[0]), list(key[1]), key[2]
        i = horizontal_lit(r_, lab)
        if i is not None:
            return dict(status='lit', word=''.join(seen[key]), orbit_seen=len(seen), squares=len(r))
        if len(seen) > cap:
            return dict(status='cap', orbit_seen=len(seen), squares=len(r))
        ri = inv(r_); ui = inv(u_)
        for name, (nr, nu) in (('T', (r_, [u_[ri[i]] for i in range(len(r_))])),
                               ('t', (r_, [u_[r_[i]] for i in range(len(r_))])),
                               ('S', ([r_[ui[i]] for i in range(len(r_))], u_)),
                               ('s', ([r_[u_[i]] for i in range(len(r_))], u_))):
            k = canon(nr, nu, lab)
            if k not in seen:
                seen[k] = seen[key]+(name,); q.append(k)
    return dict(status='dark', orbit=len(seen), squares=len(r))


if __name__ == '__main__':
    for f in sys.argv[1:]:
        print(f, json.dumps(decide(json.loads(Path(f).read_text()))), flush=True)
