"""Stage-1 scan of (1,3,4) rooms (n=8, b=3): k extra tiles, W <= Wp.

Copy of ../d7-review/enum_rooms.enumerate_rooms with two changes:
1. T whose star shares a C-tip with St(S) (T = 2c) is dropped (Prop. R2.1).
2. B-point prune: every B point of a (1,3,4) room is a wall corner (its angle
   is 3j*pi/8, never pi or 2pi), and the set of B points of U0 + K only grows
   as tiles are added. So a partial set with more than Wp distinct B points
   has no completion with W <= Wp. This holds for every completion.
3. Finalized-corner prune: in a Redelmeier subtree, tiles popped from the
   untried list are excluded for good. If every edge-neighbour of the fan at
   an A or C vertex v (across the two edges of each room tile at v) is in the
   room, excluded, or incompatible with St(S) + St(T), no completion adds a
   tile at v, so v keeps its angle. An A or C vertex whose angle is not pi or
   2pi is then a corner of every completion. Prune when
   (#B points) + (#finalized A/C corners) > Wp.
Rooms with W <= Wp are recorded with their profile; for W <= Ws every
interior A pair is searched for an exact lighting path (as in ../d33).
Usage: python3 scan34.py k Wp Ws [part nparts] [--noprune]
"""
import sys, os, time, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'd7-review'))
sys.path.insert(0, os.path.join(HERE, '..', 'd33-134-rooms'))
from geom import Triangle, star, Room
from enum_rooms import Universe, t_candidates
from shoot import Tracer
from fastshoot import Fast
from profile34 import profile, check

NOPRUNE = '--noprune' in sys.argv
FIN = '--fin' in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith('--')]
k, Wp, Ws = map(int, args[:3])
part, nparts = (int(args[3]), int(args[4])) if len(args) > 4 else (0, 1)
n, b = 8, 3
DMAX, MMAX = 5, 4


def solve(tr, S, T, mids):
    fs = Fast(tr)
    for d in range(DMAX + 1):
        r = fs.find_path(S, T, d)
        if r['found']:
            return 'd%d' % d, len(r['walls_hit'])
    for d in range(1, MMAX + 1):
        r = fs.find_path_mid(S, T, mids, d)
        if r['found']:
            return 'mid%d' % d, len(r['walls_hit'])
    return None, None


tri = Triangle(n, b)
F = tri.F
U = Universe(tri)
starS = [U.intern(t) for t in star(tri, F.zero)]
cS = {t.V['C'] for t in starS}
cands = t_candidates(U, tri, starS, k)
order = sorted(cands.items(), key=lambda kv: kv[1])
order = [(T, d) for T, d in order if not any(F.smul(2, c) == T for c in cS)]
order = order[part::nparts]
INF = 10 ** 9
calls = {'sets': 0, 'valid': 0, 'pruned': 0, 'pruned_fin': 0}
EAT = {'A': (0, 1), 'C': (1, 2)}
byW = {}          # on_room count per (W, |K|), as in d33's byW_all
rooms = {}        # dedup by tile set, W <= Wp
t0 = time.time()

for T, dT in order:
    starT = [U.intern(t) for t in star(tri, T)]
    keysS = {t.key for t in starS}
    if any(t.key in keysS for t in starT):
        continue
    if not all(U.compat(a, c) for a in starS for c in starT):
        continue
    keysT = {t.key for t in starT}
    U0 = starS + starT
    U0keys = {t.key for t in U0}
    okU0 = {}
    Bc = {}
    for t in U0:
        Bc[t.V['B']] = Bc.get(t.V['B'], 0) + 1
    nB = [len(Bc)]
    vt = {}
    for t in U0:
        for l, p in t.V.items():
            vt.setdefault(p, []).append(t)
    roomkeys = set(U0keys)

    def fin_corners(K, s2, avail):
        cnt = 0
        done = set()
        for x in K:
            for l in 'AC':
                v = x.V[l]
                if v in done:
                    continue
                done.add(v)
                ts = vt[v]
                u = len(ts) * tri.ang[l]
                if u == 8 or u >= 16:
                    continue
                fin = True
                for y in ts:
                    nbs = U.neighbors(y)
                    for e in EAT[l]:
                        nb = nbs[e]
                        kk = nb.key
                        if kk in roomkeys:
                            continue
                        if (kk in avail or kk not in s2) and ok_with_U0(nb):
                            fin = False
                            break
                    if not fin:
                        break
                cnt += fin
        return cnt

    def ok_with_U0(t):
        v = okU0.get(t.key)
        if v is None:
            v = all(U.compat(t, u) for u in U0)
            okU0[t.key] = v
        return v

    def evaluate(K):
        calls['sets'] += 1
        room = Room(tri, U0 + K)
        if not room.analyze(check_pairs=False):
            return
        calls['valid'] += 1
        W = room.W
        key = (W, len(K))
        byW[key] = byW.get(key, 0) + 1
        if W <= Wp:
            rooms.setdefault(frozenset(t.key for t in room.tiles), (room, T, len(K)))

    distT = {t.key: 0 for t in starT}
    fr = list(starT)
    for dd in range(1, k + 2):
        nf = []
        for t in fr:
            for nb in U.neighbors(t):
                if nb.key not in distT:
                    distT[nb.key] = dd
                    nf.append(nb)
        fr = nf
    Tnode = "T"
    seen = set(U0keys)
    init = []
    for t in starS:
        for nb in U.neighbors(t):
            if nb.key in keysT:
                if Tnode not in seen:
                    seen.add(Tnode)
                    init.append(Tnode)
            elif nb.key not in seen:
                seen.add(nb.key)
                init.append(nb)
    TN = []
    for t in starT:
        for nb in U.neighbors(t):
            if nb.key not in U0keys:
                TN.append(nb)

    def rec(untried, K, seen, haveT, mind):
        untried = list(untried)
        while untried:
            t = untried.pop()
            if isinstance(t, str):
                if all(ok_with_U0(x) for x in K):
                    evaluate(K)
                    if len(K) < k:
                        new = []
                        s2 = set(seen)
                        for nb in TN:
                            if nb.key not in s2:
                                s2.add(nb.key)
                                new.append(nb)
                        rec(untried + new, K, s2, True, 0)
                continue
            if len(K) >= k:
                continue
            if not ok_with_U0(t) or not all(U.compat(t, x) for x in K):
                continue
            md = min(mind, distT.get(t.key, INF))
            if not haveT and len(K) + 1 + md - 1 > k:
                continue
            bp = t.V['B']
            newB = bp not in Bc
            if newB and not NOPRUNE and nB[0] + 1 > Wp:
                calls['pruned'] += 1
                continue
            Bc[bp] = Bc.get(bp, 0) + 1
            nB[0] += newB
            K.append(t)
            roomkeys.add(t.key)
            for l, p in t.V.items():
                vt.setdefault(p, []).append(t)
            new = []
            s2 = set(seen)
            for nb in U.neighbors(t):
                if nb.key in keysT:
                    if Tnode not in s2:
                        s2.add(Tnode)
                        new.append(Tnode)
                elif nb.key not in s2:
                    s2.add(nb.key)
                    new.append(nb)
            cut = False
            if FIN:
                avail = {x.key for x in untried if not isinstance(x, str)}
                avail.update(x.key for x in new if not isinstance(x, str))
                if nB[0] + fin_corners(K, s2, avail) > Wp:
                    calls['pruned_fin'] += 1
                    cut = True
            if not cut:
                if haveT:
                    evaluate(K)
                if len(K) < k or not haveT:
                    rec(untried + new, K, s2, haveT, md)
            K.pop()
            roomkeys.discard(t.key)
            for l, p in t.V.items():
                vt[p].pop()
            Bc[bp] -= 1
            if Bc[bp] == 0:
                del Bc[bp]
            nB[0] -= newB

    rec(init, [], seen, False, min(distT.get(t.key, INF) for t in starS))
    print('T done', dT, calls, round(time.time() - t0), 's', flush=True)

t_enum = round(time.time() - t0)
byWt = {}
for (W, kk), c in byW.items():
    if W <= Wp:
        byWt[W] = byWt.get(W, 0) + c
print('enum k', k, 'part', part, nparts, 'T', len(order), calls, 'byW<=Wp', dict(sorted(byWt.items())),
      'distinct rooms', len(rooms), t_enum, 's', flush=True)

recs, cands_out, bad = [], [], []
for room, T, nk in sorted(rooms.values(), key=lambda x: x[0].W):
    pr = profile(room)
    errs = check(pr)
    if errs:
        bad.append({'W': room.W, 'k': nk, 'errs': errs, 'profile': pr,
                    'tiles': [[t.s, t.k, list(t.t)] for t in room.tiles]})
        print('PROFILE VIOLATION', room.W, errs, flush=True)
    rec_ = {'W': room.W, 'k': nk, 'F': len(room.tiles), 'profile': pr, 'T': list(T)}
    if room.W <= Ws:
        tr = Tracer(room)
        worst = None
        for P, Q in itertools.combinations(room.interiorA, 2):
            how, refl = solve(tr, P, Q, room.transparentE)
            if how is None:
                cands_out.append({'W': room.W, 'k': nk, 'clean': room.clean, 'pair': [list(P), list(Q)],
                                  'tiles': [[t.s, t.k, list(t.t)] for t in room.tiles]})
                print('CANDIDATE W', room.W, 'clean', room.clean, flush=True)
            elif worst is None or refl > worst[1]:
                worst = (how, refl)
        rec_['worst'] = worst
        rec_['tiles'] = [[t.s, t.k, list(t.t)] for t in room.tiles]
    recs.append(rec_)
out = {'k': k, 'Wp': Wp, 'Ws': Ws, 'part': part, 'nparts': nparts, 'noprune': NOPRUNE, 'calls': calls,
       'byW_k': {'%d/%d' % kk: c for kk, c in sorted(byW.items())}, 'distinct_rooms': len(rooms),
       'candidates': cands_out, 'profile_violations': bad, 'rooms': recs,
       'seconds_enum': t_enum, 'seconds': round(time.time() - t0)}
json.dump(out, open(os.path.join(HERE, 'scan34-k%d-W%d-%d-p%dof%d%s.json' % (k, Wp, Ws, part, nparts, ('-noprune' if NOPRUNE else '') + ('-fin' if FIN else ''))), 'w'))
print('done candidates', len(cands_out), 'violations', len(bad), round(time.time() - t0), 's', flush=True)
