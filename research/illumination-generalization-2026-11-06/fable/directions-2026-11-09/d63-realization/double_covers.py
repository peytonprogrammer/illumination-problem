"""d63 abstract test: every genus-0 double cover Q' -> N of each canonical factor N = N_x that
occurs in a named room (cross12, dumb12, R22, P6), branched over two poles of N.

Construction: Q' sheets (b, e), e in GF(2); g'_y(b, e) = (g_y b, e + c_y(b)). The cocycle c
solves the GF(2) system "product relation lifts to the identity" and "the sum of c_y over a
cycle C of g_y is 1 exactly at the two chosen poles". Cycle lengths of Q' stay <= 3 and
Q' has genus 0 (Riemann-Hurwitz with two simple branch points). Each Q' is then handed to
realize.test_level for every corner class a (rotating the labels is not needed: the
classes are covered by taking each named-room class origin, as in realize.py).

This enumerates abstract covers of the small N_x of the named rooms only (task item 3).
Run: python3 -B double_covers.py
"""
import sys, json, time
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import realize as R  # noqa: E402
from realize import d4, cycles, room_tuple, lattice_points, class_congruence, test_level  # noqa: E402
from fh_tower import quotient  # noqa: E402


def solve_gf2(rows, nvar):
    """rows: list of (set of var indices, rhs). Return one solution or None."""
    piv = {}
    for vs, rhs in rows:
        v = 0
        for i in vs:
            v ^= 1 << i
        r = rhs
        while v:
            p = v.bit_length() - 1
            if p in piv:
                pv, pr = piv[p]
                v ^= pv
                r ^= pr
            else:
                piv[p] = (v, r)
                break
        else:
            if r:
                return None
    sol = 0
    for p in sorted(piv):
        v, r = piv[p]
        rest = v & ~(1 << p)
        val = r ^ (bin(rest & sol).count('1') & 1)
        if val:
            sol |= 1 << p
    return [(sol >> i) & 1 for i in range(nvar)]


def double_cover(t, branch):
    """branch: set of (y, cycle as tuple) poles of N. Returns the tuple of Q' or None."""
    m = len(t[0])
    var = lambda y, b: 4 * b + y
    rows = []
    for b in range(m):
        vs, cur = [], b
        for y in range(4):
            vs.append(var(y, cur))
            cur = t[y][cur]
        assert cur == b
        rows.append((vs, 0))
    for y in range(4):
        for c in cycles(t[y]):
            rows.append(([var(y, b) for b in c], 1 if (y, tuple(c)) in branch else 0))
    sol = solve_gf2([(set(v) if len(set(v)) == len(v) else _odd(v), r) for v, r in rows], 4 * m)
    if sol is None:
        return None
    return tuple(tuple(2 * t[y][s // 2] + ((s % 2) ^ sol[var(y, s // 2)]) for s in range(2 * m))
                 for y in range(4))


def _odd(v):
    out = set()
    for i in v:
        out ^= {i}
    return out


def main():
    t_all = time.process_time()
    summary = []
    seen = set()
    for name, cells in R.rooms():
        if name in ('Lroom', 'P6found'):
            continue
        pts = lattice_points(cells)
        for cls_off in ((0, 0), (1, 0), (1, 1), (0, 1)):
            origin = next(p for p in pts if ((p[0] - pts[0][0]) % 2, (p[1] - pts[0][1]) % 2) == cls_off)
            _, t = room_tuple(cells, origin)
            for x in (1, 2, 3):
                Bx = class_congruence(t, [x])
                if len(Bx) == len(t[0]):
                    continue
                N = quotient(t, Bx)[0] if len(Bx) > 1 else tuple((0,) for _ in range(4))
                key = (name, cls_off, len(Bx), tuple(map(tuple, Bx)))
                if key in seen:
                    continue
                seen.add(key)
                poles = [(y, tuple(c)) for y in range(4) for c in cycles(N[y]) if len(c) == 1]
                for br in combinations(poles, 2):
                    Qp = double_cover(N, set(br))
                    assert Qp is not None
                    rows, per_x, normalized, trans = test_level('%s~2' % name, str(cls_off),
                                                                'N%d br %s' % (len(Bx), [p[0] for p in br]), Qp)
                    for xx in (1, 2, 3):
                        rx = [r for r in rows if r['x'] == 'abcd'[xx]]
                        s = dict(base=name, a=str(cls_off), Nx_of='abcd'[x], degN=len(Bx), branch=[p[0] for p in br],
                                 n=len(Qp[0]), normalized=normalized, x='abcd'[xx], rows=len(rx),
                                 lit=sum(r['lit'] for r in rx), dark_rig=sum((not r['lit']) and r['rig'] for r in rx),
                                 dark_cut=sum((not r['lit']) and r['cut'] and not r['rig'] for r in rx),
                                 CE=sum(r['counterexample'] for r in rx),
                                 sound=sum(r['sound_violation'] for r in rx), nontrans=trans['abcd'[xx]],
                                 degNx=per_x[xx]['degNx'], k=per_x[xx]['k'],
                                 CE_rows=[dict(A=r['A'], B=r['B'], states=r['states']) for r in rx if r['counterexample']])
                        summary.append(s)
                        if s['rows']:
                            print('%-8s a=%s N=%d(B_%s) br=%s n=%2d %s x=%s degNx=%2d k=%2d rows=%3d lit=%3d '
                                  'darkRig=%d darkCut=%d CE=%d sound=%d nontrans=%d'
                                  % (name, s['a'], s['degN'], s['Nx_of'], s['branch'], s['n'],
                                     'norm' if normalized else 'NONNORM', s['x'], s['degNx'], s['k'], s['rows'],
                                     s['lit'], s['dark_rig'], s['dark_cut'], s['CE'], s['sound'], s['nontrans']),
                                  flush=True)
    json.dump(summary, open(HERE / 'double_covers.json', 'w'), indent=1, default=str)
    print('total CPU %.2f s' % (time.process_time() - t_all))


if __name__ == '__main__':
    main()
