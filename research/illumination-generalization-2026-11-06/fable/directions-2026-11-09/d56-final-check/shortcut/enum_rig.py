"""d56 shortcut: Rig-quotient version of the d52 fold enumeration, for residue D20.

Stage 1: every transitive W-set K on 5 cells (all labelled classes, deduped by relabelling)
         whose double N is a sphere with z = 2 zeros and only poles ('cvx'/'cone') over
         some class y (identity monodromy at y).
Stage 2: every W-set P with a W-map P -> K of fibre size 4 (model-free low-index search,
         copied from d52 validate_generic.generic_covers), room local types, genus 0, r <= 8.
Stage 3: keep strictly simple rooms with r = 8 (W = 20), area 20, corners in >= 3 classes.
Writes rooms.json. Usage: python3 -B enum_rig.py
"""
import json
import resource
import sys
import time
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from fold import (CLASSES, cg, trace, orbit_type, partial_ok, profile, summary,  # noqa: E402
                  transitive, canon, develop, is_room)

resource.setrlimit(resource.RLIMIT_CPU, (300, 300))
try:
    resource.setrlimit(resource.RLIMIT_DATA, (1 << 30, 1 << 30))
except (ValueError, OSError):
    pass  # macOS: RLIMIT_AS unsupported; peak RSS is reported instead
P_TYPES = {'cvx', 'smooth', 'rfx', 'int'}
CLS_OF_GEN = {0: [(0, 0), (0, 1)], 1: [(1, 0), (1, 1)], 2: [(0, 0), (1, 0)], 3: [(0, 1), (1, 1)]}
D, DELTA, RMAX = 5, 4, 8


def involutions(n):
    out = []

    def rec(p, i):
        if i == n:
            out.append(tuple(p))
            return
        if p[i] != -1:
            rec(p, i + 1)
            return
        p[i] = i
        rec(p, i + 1)
        for j in range(i + 1, n):
            if p[j] == -1:
                p[i], p[j] = j, i
                rec(p, i + 1)
                p[j] = -1
        p[i] = -1
    rec([-1] * n, 0)
    return out


def rig_classes(prof):
    return [y for y in CLASSES if all(t in ('cvx', 'cone') for t in prof[y])]


def enum_K():
    seen = {}
    for G in product(involutions(D), repeat=4):
        G = [list(g) for g in G]
        if not transitive(G):
            continue
        prof = profile(G)
        if prof is None:
            continue
        s = summary(prof)
        if not s['genus0'] or s['z'] != 2 or not rig_classes(prof):
            continue
        seen.setdefault(canon(G), (G, prof, s))
    return seen


def generic_covers(K, delta, rmax):
    """Verbatim logic of d52 validate_generic.generic_covers."""
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


def iso_key(cells):
    """Canonical form of a cell set under lattice isometries (D4 and translations)."""
    best = None
    for sx, sy, sw in product((1, -1), (1, -1), (False, True)):
        cs = []
        for X, Y in cells:
            corners = [(X + u, Y + v) for u in (0, 1) for v in (0, 1)]
            im = [((sx * x, sy * y) if not sw else (sy * y, sx * x)) for x, y in corners]
            cs.append((min(p[0] for p in im), min(p[1] for p in im)))
        mx, my = min(c[0] for c in cs), min(c[1] for c in cs)
        f = tuple(sorted((c[0] - mx, c[1] - my) for c in cs))
        if best is None or f < best:
            best = f
    return best


if __name__ == '__main__':
    t0 = time.process_time()
    Ks = enum_K()
    nK_rig = sum(len(rig_classes(p)) for _, p, _ in Ks.values())
    print('stage 1: %d K shapes (labelled classes, up to relabelling), %d (K, y) pairs, CPU %.1f s'
          % (len(Ks), nK_rig, time.process_time() - t0), flush=True)
    Ps = {}
    for i, (cf, (K, prof, s)) in enumerate(sorted(Ks.items())):
        found = generic_covers(K, DELTA, RMAX)
        print('K%d cone=%d rig_y=%s types=%s: %d covers' % (
            i, s['cone'], rig_classes(prof), {''.join(map(str, c)): ts for c, ts in prof.items()},
            len(found)), flush=True)
        for c2, P in found.items():
            Ps.setdefault(c2, (P, []))[1].append(i)
    print('stage 2: %d distinct cover W-sets (genus 0, room local types, r <= 8), CPU %.1f s'
          % (len(Ps), time.process_time() - t0), flush=True)
    rooms, iso = [], {}
    stats = dict(r8=0, room=0, classes3=0)
    for c2, (P, ks) in Ps.items():
        s = summary(profile(P))
        if s['z'] != 8:
            continue
        stats['r8'] += 1
        if not is_room(P):
            continue
        stats['room'] += 1
        if len(s['sing']) < 3:
            continue
        stats['classes3'] += 1
        pos = develop(P)[0]
        cells = sorted(pos.values())
        key = iso_key(cells)
        if key not in iso:
            iso[key] = len(rooms)
            rooms.append(dict(cells=[list(c) for c in cells], from_K=ks))
    print('stage 3:', stats, 'rooms up to lattice isometry: %d, CPU %.1f s'
          % (len(rooms), time.process_time() - t0))
    json.dump(rooms, open(HERE / 'rooms.json', 'w'))
    print('peak RSS MB %.0f' % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20))
