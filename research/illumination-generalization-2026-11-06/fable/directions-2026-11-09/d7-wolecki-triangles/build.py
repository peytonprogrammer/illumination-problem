"""Explicit rooms: constructions that give upper bounds on the wall count.

Families (all checked by rooms.analyze, exact arithmetic):
  two_star(g)        S-star + one pair of tiles at a shared B tip + T-star
  arc_family(g)      S-star + an arc of the fan around one bridge centre M + T-star,
                     plus (right triangles) one third tile at every 2-tile C point
"""
import itertools
import sys
from collections import defaultdict

from rooms import Geo, Invalid, LABELS, analyze, any_overlap, tiles_overlap


def two_star(g):
    t0 = g.base
    t1 = g.reflect_tile(t0, 0)      # across BC: new A vertex S'
    t2 = g.reflect_tile(t1, 2)      # across the spoke P-S'
    t3 = g.reflect_tile(t2, 0)      # across BC: a tile of the T star
    return g.star(t0) + [t1, t2] + g.star(t3)


def skeletons(g):
    """Yield (j, first, tiles): arc m_0..m_j around M = base A vertex, stars mirrored across both ends."""
    n = g.n
    for first in (2, 1):
        ms = g.star(g.base, first)
        s_star = g.star(g.reflect_tile(ms[0], 0))
        if any_overlap(g, s_star, ms[:1]):
            continue
        for j in range(1, 2 * n - 1):
            t_star = g.star(g.reflect_tile(ms[j], 0))
            arc = ms[:j + 1]
            tiles = list(dict.fromkeys(s_star + arc + t_star))
            if len(tiles) != 4 * n + j + 1:
                continue
            if any_overlap(g, s_star, t_star) or any_overlap(g, arc, s_star) or any_overlap(g, arc, t_star):
                continue
            yield j, first, tiles


def _index(tiles):
    cls, at = {}, defaultdict(list)
    for t in tiles:
        for i, p in enumerate(t):
            if cls.setdefault(p, LABELS[i]) != LABELS[i]:
                return None, None
            at[p].append(t)
    return cls, at


def complete_right(g, K, max_full=40):
    """Right triangle: add one third tile at every C point with 2 tiles. Returns best report or None."""
    n = g.n
    cls, at = _index(K)
    if cls is None:
        return None
    need = []
    for p, ts in at.items():
        if cls[p] == 'C':
            if len(ts) == 2:
                need.append(p)
            elif len(ts) not in (1, 3):
                return None
    Kset = set(K)
    cands = []
    for p in need:
        opts = []
        for t in at[p]:
            u = g.reflect_tile(t, 0)
            if u in Kset:
                continue
            if any(cls.get(q, LABELS[i]) != LABELS[i] for i, q in enumerate(u)):
                continue
            if any_overlap(g, [u], K):
                continue
            opts.append(u)
        if not opts:
            return None
        cands.append(opts)
    flat = [u for opts in cands for u in opts]
    bad = set()
    for a, b in itertools.combinations(flat, 2):
        if tiles_overlap(g, a, b) or any(a[i] in b and b.index(a[i]) != i for i in range(3)):
            bad.add((a, b))
            bad.add((b, a))
    base_count = {p: len(ts) for p, ts in at.items()}
    ang = g.ang
    scored = []

    def rec(i, chosen):
        if i == len(cands):
            cnt = dict(base_count)
            c2 = dict(cls)
            for u in chosen:
                for k, q in enumerate(u):
                    cnt[q] = cnt.get(q, 0) + 1
                    c2[q] = LABELS[k]
            w = sum(1 for q, k in cnt.items() if k * ang[c2[q]] not in (n, 2 * n))
            scored.append((w, tuple(chosen)))
            return
        for u in cands[i]:
            if all((u, v) not in bad for v in chosen):
                rec(i + 1, chosen + [u])
    rec(0, [])
    scored.sort(key=lambda x: x[0])
    tried = 0
    for w, chosen in scored:
        if tried >= max_full:
            break
        tried += 1
        try:
            rep = analyze(g, K + list(chosen))
        except Invalid:
            continue
        if rep['clean'] and len(rep['interior_A']) >= 2:
            rep['completions_enumerated'] = len(scored)
            rep['completions_fully_checked'] = tried
            return rep
    return None


def arc_family(g, verbose=False):
    """Best room in the arc family. Returns (report, j, first) or None."""
    right = (2 * g.c == g.n)
    best = None
    for j, first, K in skeletons(g):
        try:
            rep = complete_right(g, K, 10 ** 6 if g.n == 4 else 40) if right else analyze(g, K)
        except Invalid as e:
            if verbose:
                print("   j=%d first=%d invalid: %s" % (j, first, e))
            continue
        if rep is None or not rep['clean'] or len(rep['interior_A']) < 2:
            continue
        if verbose:
            print("   j=%d first=%d walls=%d tiles=%d" % (j, first, rep['walls'], rep['tiles']))
        if best is None or rep['walls'] < best[0]['walls']:
            best = (rep, j, first)
    return best


if __name__ == '__main__':
    for n, b in [tuple(map(int, a.split(','))) for a in sys.argv[1:]]:
        g = Geo(n, b)
        print("triangle (1,%d,%d), n=%d" % (b, g.c, n))
        r = arc_family(g, verbose=True)
        if r:
            print("  best: walls=%d tiles=%d j=%d first=%d %s" % (r[0]['walls'], r[0]['tiles'], r[1], r[2], r[0]['corner_types']))
        else:
            print("  no valid room in the arc family")
