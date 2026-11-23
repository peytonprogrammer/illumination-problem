"""Capped scan of (1,3,4) rooms: n=8, b=3, at most k extra tiles, W <= Wmax.

Reuses d7-review/enum_rooms.py (exhaustive Redelmeier enumeration) and
d7-review/shoot.py (exact tracer, midpoint-targeted search). One change:
T candidates whose star shares a C-tip with St(S) (T = 2c) are dropped
before enumeration, because every such room is lit by Proposition R2.1.

For each kept room, every pair of interior A points is searched:
plain image search depth 0..dmax, then midpoint search depth 1..mmax.
Plain search tries only images of exact word length d at depth d.
Paths are confirmed by the exact tracer (fastshoot.py prefilters in floats).
Usage: python3 scan.py k Wmax dmax mmax [Wmin] [n b] [--exact]
(--exact skips the float prefilter and uses shoot.py directly;
--nofilter keeps shared-C-tip T, for validation.)
"""
import sys, os, time, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'd7-review'))
import enum_rooms
from geom import star
from shoot import Tracer, find_path_mid
from fastshoot import Fast

EXACT = '--exact' in sys.argv
NOFILTER = '--nofilter' in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith('--')]
k, Wmax, dmax, mmax = map(int, args[:4])
Wmin = int(args[4]) if len(args) > 4 else 0
n, b = (int(args[5]), int(args[6])) if len(args) > 6 else (8, 3)
_orig = enum_rooms.t_candidates
dropped = []

def t_filtered(U, tri, starS, kk):
    F = tri.F
    cS = {t.V['C'] for t in starS}
    out = {}
    for T, d in _orig(U, tri, starS, kk).items():
        if any(F.smul(2, c) == T for c in cS):
            dropped.append(T)
        else:
            out[T] = d
    return out

if not NOFILTER:
    enum_rooms.t_candidates = t_filtered

rooms = {}
byW_all = {}

def on_room(room, T, K):
    byW_all[room.W] = byW_all.get(room.W, 0) + 1
    if Wmin <= room.W <= Wmax:
        rooms.setdefault(frozenset(t.key for t in room.tiles), (room, T, len(K)))

t0 = time.time()
res = enum_rooms.enumerate_rooms(n, b, k, log=lambda *a: None, on_room=on_room)
t_enum = round(time.time() - t0)
print('enum', k, 'T kept', res['stats']['T_star_ok'], 'dropped', len(dropped),
      'valid', res['stats']['valid'], 'byW', dict(sorted(byW_all.items())),
      'kept W<=%d' % Wmax, len(rooms), t_enum, 's', flush=True)


def solve(tr, F, S, T, mids):
    fs = Fast(tr)
    for d in range(dmax + 1):
        r = tr.find_path(S, T, d) if EXACT else fs.find_path(S, T, d)
        if r['found']:
            return 'd%d' % d, len(r['walls_hit']), r
    for d in range(1, mmax + 1):
        r = find_path_mid(tr, S, T, mids, d) if EXACT else fs.find_path_mid(S, T, mids, d)
        if r['found']:
            return 'mid%d' % d, len(r['walls_hit']), r
    return None, None, None


summ = {}
recs = []
cands = []
for room, T, nk in sorted(rooms.values(), key=lambda x: x[0].W):
    F = room.tri.F
    tr = Tracer(room)
    A = room.interiorA
    worst = None
    for P, Q in itertools.combinations(A, 2):
        how, refl, r = solve(tr, F, P, Q, room.transparentE)
        if how is None:
            cands.append({'W': room.W, 'k': nk, 'tiles_n': len(room.tiles), 'clean': room.clean,
                          'pair': [list(P), list(Q)], 'S': [0] * 8, 'T': list(T),
                          'tiles': [[t.s, t.k, list(t.t)] for t in room.tiles]})
            print('CANDIDATE W', room.W, 'clean', room.clean, flush=True)
            continue
        if worst is None or refl > worst[1]:
            worst = (how, refl)
    key = '%d/k%d' % (room.W, nk)
    s = summ.setdefault(key, {})
    s[str(worst[0] if worst else None)] = s.get(str(worst[0] if worst else None), 0) + 1
    recs.append({'W': room.W, 'k': nk, 'tiles_n': len(room.tiles), 'nA': len(A),
                 'worst_how': worst[0] if worst else None, 'worst_refl': worst[1] if worst else None,
                 'T': list(T), 'tiles': [[t.s, t.k, list(t.t)] for t in room.tiles]})
print('summary', json.dumps(summ), round(time.time() - t0), 's', flush=True)
hard = sorted([r for r in recs if r['worst_refl'] is not None], key=lambda r: -r['worst_refl'])[:5]
json.dump({'n': n, 'b': b, 'k': k, 'Wmax': Wmax, 'dmax': dmax, 'mmax': mmax,
           'enum_stats': res['stats'], 'byW_all_noshared': dict(sorted(byW_all.items())),
           'kept_rooms': len(rooms), 'by_W_k_worst': summ, 'n_candidates': len(cands),
           'candidates': cands, 'hardest': hard,
           'seconds': round(time.time() - t0)},
          open(os.path.join(HERE, 'scan-%d-%d-k%d-W%d-%d%s.json' % (n, b, k, Wmin, Wmax, ('-exact' if EXACT else '') + ('-nofilter' if NOFILTER else ''))), 'w'))
