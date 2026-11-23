"""d52 validation: brute-force every immersed room W-set P with n <= NMAX cells and r <= RMAX
(low-index search on cells; no arc model, no quotient list). For each class x with delta_x >= 3,
normalise x to (0, 0), and check that
  (a) K = P / B_x is in the admissible list, or fails an admissibility filter for a reason
      that P itself also fails (P has <= 2 corner classes); and
  (b) P is produced by enum_P.covers(K, z, delta) (canonical forms compared).
Also reports positives among the brute-force rooms.
Usage: python3 -B validate_brute.py NMAX RMAX K_admissible.json
"""
import json
import resource
import sys
import time
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fold import *  # noqa
import enum_P  # noqa

resource.setrlimit(resource.RLIMIT_CPU, (1500, resource.getrlimit(resource.RLIMIT_CPU)[1]))
CLS_OF_GEN = enum_P.CLS_OF_GEN
P_TYPES = {'cvx', 'smooth', 'rfx', 'int'}


def all_rooms(nmax, rmax):
    G = [[-1] * nmax for _ in range(4)]
    found = {}

    def counts_ok(n):
        z = cvx = 0
        for cls in CLASSES:
            a, b = cg(cls)
            seen = set()
            for c in range(n):
                if c in seen:
                    continue
                cells, kind = trace(G, a, b, c)
                seen.update(cells)
                t = orbit_type(cells, kind)
                z += t == 'rfx'
                cvx += t == 'cvx'
        return z <= rmax and cvx <= rmax + 4

    def local_ok(touched, g):
        for cls in CLS_OF_GEN[g]:
            a, b = cg(cls)
            for c in touched:
                cl, kind = trace(G, a, b, c)
                if not partial_ok(cl, kind, P_TYPES):
                    return False
        return True

    def rec(n, ptr):
        while ptr < 4 * n and G[ptr % 4][ptr // 4] != -1:
            ptr += 1
        if ptr == 4 * n:
            P = [row[:n] for row in G]
            prof = profile(P)
            if prof is None:
                return
            s = summary(prof)
            if s['genus0']:
                found.setdefault(canon(P), P)
            return
        c, g = ptr // 4, ptr % 4
        G[g][c] = c
        if local_ok([c], g) and counts_ok(n):
            rec(n, ptr + 1)
        G[g][c] = -1
        for c2 in range(c + 1, n):
            if G[g][c2] == -1:
                G[g][c] = c2
                G[g][c2] = c
                if local_ok([c, c2], g) and counts_ok(n):
                    rec(n, ptr + 1)
                G[g][c] = -1
                G[g][c2] = -1
        if n < nmax:
            G[g][c] = n
            G[g][n] = c
            if local_ok([c, n], g) and counts_ok(n + 1):
                rec(n + 1, ptr + 1)
            G[g][c] = -1
            G[g][n] = -1
    rec(1, 0)
    return list(found.values())


def normalise(G, x):
    i, j = x
    return [G[i], G[1 - i], G[2 + j], G[3 - j]]


if __name__ == '__main__':
    nmax, rmax = int(sys.argv[1]), int(sys.argv[2])
    adm = json.load(open(sys.argv[3]))
    adm_idx = {tuple(tuple(r) for r in k['canon']): i for i, k in enumerate(adm)}
    t0 = time.process_time()
    rooms = all_rooms(nmax, rmax)
    print('immersed room W-sets with n <= %d, r <= %d: %d (CPU %.1f s)' % (nmax, rmax, len(rooms),
          time.process_time() - t0), flush=True)
    stat = Counter()
    cover_cache = {}
    npos = 0
    for P in rooms:
        prof = profile(P)
        s = summary(prof)
        ncls = len([c for c, ts in prof.items() if 'cvx' in ts or 'rfx' in ts])
        pos, _ = positives(P)
        emb = is_room(P)
        stat['rooms'] += 1
        stat['true_room'] += emb
        if pos:
            npos += 1
            print('POSITIVE brute-force room n=%d r=%d embedded=%s classes=%d' % (len(P[0]), s['z'], emb, ncls))
        for x in CLASSES:
            blk = B(P, x)
            d = max(blk) + 1
            delta = len(P[0]) // d
            if delta < 3:
                continue
            stat['class_delta>=3'] += 1
            Pn = normalise(P, x)
            K = quotient(Pn, B(Pn, (0, 0)))
            kc = canon(K)
            if kc not in adm_idx:
                kz = summary(profile(K))['z']
                stat['K_not_adm_d=%d_z=%d_%s' % (d, kz, 'in_scope' if ncls >= 3 else 'out_of_scope')] += 1
                if ncls >= 3 and d > 1:
                    kp = summary(profile(K))
                    print('  NOTE: in-scope P, K not admissible: d=%d delta=%d z=%d sing=%s' % (
                        d, delta, kp['z'], kp['sing']))
                continue
            ki = adm_idx[kc]
            key = (ki, delta)
            if key not in cover_cache:
                Kg = [list(r) for r in adm[ki]['canon']]
                coll = set()
                enum_P.covers(Kg, adm[ki]['z'], delta, rmax, collect=coll)
                cover_cache[key] = coll
            if canon(Pn) in cover_cache[key]:
                stat['found_as_cover'] += 1
            else:
                stat['MISSED'] += 1
                print('  MISSED: P n=%d over K%d delta=%d' % (len(P[0]), ki, delta))
    print(dict(stat))
    print('positives among brute-force rooms:', npos, ' total CPU %.1f s' % (time.process_time() - t0))
