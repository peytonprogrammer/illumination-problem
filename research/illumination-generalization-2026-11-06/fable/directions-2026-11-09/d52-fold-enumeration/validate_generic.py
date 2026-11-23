"""d52 validation of the arc/slit cover model: a second, model-free enumerator of all W-sets P
with an equivariant map P -> K of fibre size delta (cells labelled by K-cells; low-index search
on cells; only the room-local orbit types and r <= RMAX are imposed). Compares canonical forms
with enum_P.covers(..., collect=...), and reports positives found by the generic search.
Usage: python3 -B validate_generic.py K_admissible.json RMAX NMAX [maxcpu_s [maxdelta]]
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
from analyze_K import deltas  # noqa

resource.setrlimit(resource.RLIMIT_CPU, (1800, 1800))
P_TYPES = {'cvx', 'smooth', 'rfx', 'int'}
CLS_OF_GEN = enum_P.CLS_OF_GEN


def generic_covers(K, delta, rmax):
    d = len(K[0])
    n = d * delta
    G = [[-1] * n for _ in range(4)]
    lab = [-1] * n
    cnt = [0] * d
    lab[0] = 0
    cnt[0] = 1
    found = {}

    def counts_ok(m):
        z = 0
        for cls in CLASSES:
            a, b = cg(cls)
            seen = set()
            for c in range(m):
                if c in seen:
                    continue
                cells, kind = trace(G, a, b, c)
                seen.update(cells)
                z += orbit_type(cells, kind) == 'rfx'
        return z <= rmax

    def local_ok(touched, g):
        for cls in CLS_OF_GEN[g]:
            a, b = cg(cls)
            for c in touched:
                cl, kind = trace(G, a, b, c)
                if not partial_ok(cl, kind, P_TYPES):
                    return False
        return True

    def rec(m, ptr):
        while ptr < 4 * m and G[ptr % 4][ptr // 4] != -1:
            ptr += 1
        if ptr == 4 * m:
            if m < n:
                return
            P = [row[:] for row in G]
            prof = profile(P)
            if prof is None:
                return
            s = summary(prof)
            if s['genus0'] and s['z'] <= rmax:
                found.setdefault(canon(P), P)
            return
        c, g = ptr // 4, ptr % 4
        v = K[g][lab[c]]
        if v == lab[c]:
            G[g][c] = c
            if local_ok([c], g) and counts_ok(m):
                rec(m, ptr + 1)
            G[g][c] = -1
        for c2 in range(c + 1, m):
            if G[g][c2] == -1 and lab[c2] == v:
                G[g][c] = c2
                G[g][c2] = c
                if local_ok([c, c2], g) and counts_ok(m):
                    rec(m, ptr + 1)
                G[g][c] = -1
                G[g][c2] = -1
        if m < n and cnt[v] < delta:
            G[g][c] = m
            G[g][m] = c
            lab[m] = v
            cnt[v] += 1
            if local_ok([c, m], g) and counts_ok(m + 1):
                rec(m + 1, ptr + 1)
            cnt[v] -= 1
            lab[m] = -1
            G[g][c] = -1
            G[g][m] = -1
    rec(1, 0)
    return found


if __name__ == '__main__':
    adm = json.load(open(sys.argv[1]))
    rmax, nmax = int(sys.argv[2]), int(sys.argv[3])
    maxcpu = float(sys.argv[4]) if len(sys.argv) > 4 else 1e9
    maxdelta = int(sys.argv[5]) if len(sys.argv) > 5 else 99
    t0 = time.process_time()
    tot = Counter()
    for i, k in enumerate(adm):
        K = [list(r) for r in k['canon']]
        for dl in deltas(k, rmax):
            if k['d'] * dl > nmax or dl > maxdelta:
                continue
            if time.process_time() - t0 > maxcpu:
                print('CPU cap reached; stopping')
                break
            gen = generic_covers(K, dl, rmax)
            coll = set()
            res, stats, st = enum_P.covers(K, k['z'], dl, rmax, collect=coll)
            g = set(gen)
            npos_gen = sum(1 for P in gen.values() if summary(profile(P))['z'] <= rmax and positives(P)[0]
                           and len([c for c, ts in profile(P).items() if 'cvx' in ts or 'rfx' in ts]) >= 3)
            tot['cases'] += 1
            tot['generic_rooms'] += len(g)
            tot['arc_rooms'] += len(coll)
            tot['missing_from_arc_model'] += len(g - coll)
            tot['extra_in_arc_model'] += len(coll - g)
            tot['generic_positives'] += npos_gen
            flag = '' if g == coll else '  <-- MISMATCH'
            print('K%d d=%d z=%d cone=%d delta=%d: generic %d, arc model %d, generic positives %d%s' % (
                i, k['d'], k['z'], k['cone'], dl, len(g), len(coll), npos_gen, flag), flush=True)
    print('TOTAL', dict(tot), 'CPU s %.1f' % (time.process_time() - t0))
