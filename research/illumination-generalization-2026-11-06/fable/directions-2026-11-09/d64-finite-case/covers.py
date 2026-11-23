"""d64 step 2: all degree-delta W-set covers P -> K of each admissible K (d52 arc model,
enum_P.covers, unchanged), for every delta in K['deltas'] (delta >= 2). Keeps every genus-0
disc cover with r <= RMAX, then classifies: strictly simple room (fold.is_room), normalized
(gcd of horizontal and of vertical edge lengths is 1), and dedupes rooms up to lattice isometry.
Usage: python3 -B covers.py K_adm.json RMAX start end out.json
"""
import json
import sys
import time
from collections import Counter
from math import gcd
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'd52-fold-enumeration'))
import enum_P  # noqa: E402  (sets RLIMIT_CPU 3000 s)
from fold import is_room, develop  # noqa: E402

D4 = [lambda x, y: (x, y), lambda x, y: (-x, y), lambda x, y: (x, -y), lambda x, y: (-x, -y),
      lambda x, y: (y, x), lambda x, y: (-y, x), lambda x, y: (y, -x), lambda x, y: (-y, -x)]


def iso_key(cells):
    best = None
    for f in D4:
        pts = [f(i + 0.5, j + 0.5) for i, j in cells]
        mx = min(p[0] for p in pts)
        my = min(p[1] for p in pts)
        key = tuple(sorted((int(p[0] - mx), int(p[1] - my)) for p in pts))
        if best is None or key < best:
            best = key
    return best


def edge_gcds(cells):
    """gcd of horizontal wall-run lengths and of vertical wall-run lengths (maximal edges)."""
    cs = set(cells)
    hx = {}
    vy = {}
    for (i, j) in cs:
        for jj, out in ((j, (i, j - 1)), (j + 1, (i, j + 1))):
            if out not in cs:
                hx.setdefault((jj, out[1] > j), set()).add(i)
        for ii, out in ((i, (i - 1, j)), (i + 1, (i + 1, j))):
            if out not in cs:
                vy.setdefault((ii, out[0] > i), set()).add(j)
    gh = gv = 0
    for runs, acc in ((hx, 'h'), (vy, 'v')):
        for _, s in runs.items():
            s = sorted(s)
            start = prev = s[0]
            for v in s[1:] + [None]:
                if v is not None and v == prev + 1:
                    prev = v
                    continue
                L = prev - start + 1
                if acc == 'h':
                    gh = gcd(gh, L)
                else:
                    gv = gcd(gv, L)
                if v is not None:
                    start = prev = v
    return gh, gv


if __name__ == '__main__':
    recs = json.load(open(sys.argv[1]))
    rmax = int(sys.argv[2])
    lo, hi = int(sys.argv[3]), int(sys.argv[4])
    t0 = time.process_time()
    tot = Counter()
    rooms = {}
    lines = []
    for i in range(lo, min(hi, len(recs))):
        k = recs[i]
        K = [list(r) for r in k['canon']]
        for dl in k['deltas']:
            t1 = time.process_time()
            coll = set()
            _, stats, st = enum_P.covers(K, k['z'], dl, rmax, collect=coll)
            tot.update(stats)
            c = Counter()
            for form in coll:
                G = [list(r) for r in form]
                if not is_room(G):
                    c['disc_not_room'] += 1
                    continue
                pos, _, _ = develop(G)
                cells = sorted(pos.values())
                key = iso_key(cells)
                gh, gv = edge_gcds(cells)
                c['room_covers'] += 1
                rec = rooms.setdefault(key, dict(cells=[list(x) for x in key], n=len(cells),
                                                 normalized=(gh == 1 and gv == 1), src=[]))
                rec['src'].append([i, dl])
            tot.update(c)
            lines.append(dict(K=i, d=k['d'], z=k['z'], cone=k['cone'], delta=dl, free=st['nfree'],
                              stats=dict(stats), cls=dict(c), cpu=round(time.process_time() - t1, 3)))
    json.dump(dict(cases=lines, rooms=list(rooms.values())), open(sys.argv[5], 'w'))
    print('K %d..%d cases %d TOTAL %s unique rooms %d (normalized %d) CPU s %.1f' % (
        lo, hi, len(lines), dict(tot), len(rooms), sum(r['normalized'] for r in rooms.values()),
        time.process_time() - t0), flush=True)
