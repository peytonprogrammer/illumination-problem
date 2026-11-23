"""d52 step 5: sanity at r = 9 and r = 12. Identify every positive cover found at r = 9 with a
lattice room up to lattice isometry, and check that P6's quotient yields P6 at delta = 4, r = 12.
Usage: python3 -B sanity.py
"""
import json
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from fold import *  # noqa
import enum_P  # noqa
from named import ROOMS  # noqa

# generator permutations induced by lattice isometries: V0<->V1, H0<->H1, V<->H
PERMS = []
for sv in (0, 1):
    for sh in (0, 1):
        for sw in (0, 1):
            p = [sv, 1 - sv, 2 + sh, 3 - sh]
            if sw:
                p = [p[2], p[3], p[0], p[1]]
            PERMS.append(p)


def full_canon(G):
    return min(canon([G[p[0]], G[p[1]], G[p[2]], G[p[3]]]) for p in PERMS)


def normalise(G, x):
    i, j = x
    return [G[i], G[1 - i], G[2 + j], G[3 - j]]


named = {name: full_canon(from_cells(c)[0]) for name, c in ROOMS.items()}

print('== r = 9: positives over admissible K (z <= 3)')
adm9 = json.load(open(HERE / 'data' / 'K_adm_r9.json'))
P9 = json.load(open(HERE / 'data' / 'P_r9.json'))
rooms9 = {}
for line in P9:
    if not line['positives']:
        continue
    k = adm9[line['K']]
    K = [list(r) for r in k['canon']]
    res, stats, st = enum_P.covers(K, k['z'], line['delta'], 9)
    for rec in res:
        P = rec['P']
        fc = full_canon(P)
        pos, dev_ok, emb = develop(P)
        cells = sorted(pos.values())
        ss = is_room(P)
        which = [nm for nm, c in named.items() if c == fc]
        rooms9.setdefault(fc, []).append((line['K'], line['delta']))
        print('  K%d delta=%d: n=%d r=%d embedded=%s true room=%s identified as %s; pairs %s' % (
            line['K'], line['delta'], rec['n'], rec['r'], emb, ss, which or 'NEW', rec['pos']))
print('  distinct positive rooms at r = 9 (up to lattice isometry):', len(rooms9))

print('== r = 12: P6')
G6, _ = from_cells(ROOMS['P6'])
for x in CLASSES:
    blk = B(G6, x)
    if max(blk) + 1 == 1:
        continue
    Gn = normalise(G6, x)
    K = quotient(Gn, B(Gn, (0, 0)))
    s = summary(profile(K))
    coll = set()
    res, stats, st = enum_P.covers(K, s['z'], len(G6[0]) // len(K[0]), 12, collect=coll)
    hit = [r for r in res if full_canon(r['P']) == named['P6']]
    print('  x=%s: K d=%d z=%d cone=%d, delta=%d: %d disc covers, %d positive, P6 among positives: %s, P6 among covers: %s'
          % (x, len(K[0]), s['z'], s['cone'], len(G6[0]) // len(K[0]), stats['rooms'], len(res), bool(hit),
             canon(Gn) in coll))
    for r in res:
        print('    positive cover n=%d r=%d embedded=%s is P6: %s' % (r['n'], r['r'], r['embedded'],
              full_canon(r['P']) == named['P6']))

print('== 22-wall room: its delta >= 3 quotients and membership')
G22, _ = from_cells(ROOMS['22-wall'])
for x in CLASSES:
    blk = B(G22, x)
    dl = len(G22[0]) // (max(blk) + 1)
    if dl < 3:
        continue
    Gn = normalise(G22, x)
    K = quotient(Gn, B(Gn, (0, 0)))
    kc = canon(K)
    idx = [i for i, k in enumerate(adm9) if tuple(tuple(r) for r in k['canon']) == kc]
    print('  x=%s: delta=%d, K index in r=9 admissible list: %s' % (x, dl, idx))
