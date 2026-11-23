"""d64 validation of the room list (no quotient list, no arc model in part A).

A  brute: Redelmeier enumeration of all fixed polyominoes with <= NMAX cells. Keep the free
   representatives that are strictly simple, have r <= 8, and are normalized. For each parity
   class x compute B_x directly (fold.B, closure of the 2-cycles of g_x). If some x has
   1 < deg N_x < n, the room is in RL-fin scope and must be in covers.json (by isometry key).
   Also reports rooms in covers.json with n <= NMAX that brute does not find.
B  generic: d52's model-free cover enumerator (validate_generic.generic_covers) against the
   arc model (enum_P.covers) for delta = 2 cases with d * 2 <= NMAXB, up to a CPU cap.
Usage: python3 -B validate.py NMAX NMAXB CAP_B_SECONDS
"""
import json
import sys
import time
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd52-fold-enumeration'))
sys.path.insert(0, str(HERE.parent / 'd10-mechanisms'))
from fold import from_cells, B, CLASSES  # noqa: E402
import enum_P  # noqa: E402
from validate_generic import generic_covers  # noqa: E402
from roomtools import is_strictly_simple, status, lattice_points  # noqa: E402
from covers import iso_key, edge_gcds  # noqa: E402


def redelmeier(nmax, visit):
    """Fixed polyominoes: cells (x, y) with y > 0 or (y == 0 and x >= 0)."""
    def ok(c):
        return c[1] > 0 or (c[1] == 0 and c[0] >= 0)

    def rec(poly, untried, seen):
        while untried:
            c = untried.pop()
            poly.append(c)
            visit(poly)
            if len(poly) < nmax:
                new = []
                for nb in ((c[0] + 1, c[1]), (c[0] - 1, c[1]), (c[0], c[1] + 1), (c[0], c[1] - 1)):
                    if ok(nb) and nb not in seen:
                        new.append(nb)
                for nb in new:
                    seen.add(nb)
                rec(poly, untried + new, seen)
                for nb in new:
                    seen.discard(nb)
            poly.pop()
    rec([], [(0, 0)], {(0, 0)})


if __name__ == '__main__':
    nmax, nmaxb, capb = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
    t0 = time.process_time()
    data = json.load(open(HERE / 'data' / 'covers.json'))
    have = {tuple(tuple(c) for c in r['cells']): r for r in data['rooms']}
    cnt = Counter()
    found = set()

    def visit(poly):
        cnt['fixed'] += 1
        key = iso_key(poly)
        mx = min(p[0] for p in poly)
        my = min(p[1] for p in poly)
        if tuple(sorted((x - mx, y - my) for x, y in poly)) != key:
            return
        cnt['free'] += 1
        cells = set(key)
        if not is_strictly_simple(cells):
            return
        r = sum(1 for p in lattice_points(cells) if status(cells, p) == 'reflex')
        if r > 8:
            return
        gh, gv = edge_gcds(key)
        if gh != 1 or gv != 1:
            cnt['not_normalized'] += 1
            return
        cnt['rooms'] += 1
        G, _ = from_cells(cells)
        n = len(cells)
        degs = [max(B(G, cls)) + 1 for cls in CLASSES]
        if any(1 < dg < n for dg in degs):
            cnt['in_scope'] += 1
            found.add(key)
            if key in have:
                cnt['in_scope_found_in_covers'] += 1
            else:
                cnt['MISSING'] += 1
                print('MISSING', key, degs, flush=True)
    redelmeier(nmax, visit)
    extra = [k for k, r in have.items() if r['n'] <= nmax and r['normalized'] and k not in found]
    cnt['covers_rooms_n<=NMAX_normalized'] = sum(1 for r in have.values() if r['n'] <= nmax and r['normalized'])
    cnt['covers_rooms_not_in_brute'] = len(extra)
    print('A brute NMAX=%d: %s CPU s %.1f' % (nmax, dict(cnt), time.process_time() - t0), flush=True)
    for k in extra[:10]:
        print('  extra (has no 1 < deg N_x < n by brute):', k)

    t1 = time.process_time()
    adm = json.load(open(HERE / 'data' / 'K_adm.json'))
    tot = Counter()
    seenz = Counter()
    for i, k in enumerate(adm):
        if 2 not in k['deltas'] or 2 * k['d'] > nmaxb:
            continue
        if time.process_time() - t1 > capb:
            print('B: CPU cap reached')
            break
        K = [list(r) for r in k['canon']]
        gen = set(generic_covers(K, 2, 8))
        coll = set()
        enum_P.covers(K, k['z'], 2, 8, collect=coll)
        tot['cases'] += 1
        seenz[k['z']] += 1
        tot['generic'] += len(gen)
        tot['arc'] += len(coll)
        tot['missing_from_arc'] += len(gen - coll)
        tot['extra_in_arc'] += len(coll - gen)
        if gen != coll:
            print('B MISMATCH K%d' % i, len(gen), len(coll), flush=True)
    print('B generic vs arc, delta 2, n <= %d: %s cases by z %s CPU s %.1f' % (
        nmaxb, dict(tot), dict(seenz), time.process_time() - t1))
