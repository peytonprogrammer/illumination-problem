"""d83: stress test of the open reachability lemma on the saved single edits of R22.

For R22 and every saved level-1 edit of R22 in d8-perturbation-test that is strictly
simple, has r <= 8, and keeps the marks interior:
  1. n, r, marked valency d, and regular coincidences by class relative to S
     (d82 indep.py monodromy, loaded unmodified).
  2. Trace each saved witness exactly with two tracers (d8 tracer.py, d3 surface.py),
     take the point at half the length, and its class.
  3. Check that the midpoint carries a regular coincidence of the marked union, at
     sheet level: the 2-cycle at the midpoint that contains the arrival cell.
  4. Only for rooms whose saved witnesses all have source-class midpoints: a targeted
     per-candidate check (not reached in this run unless printed).
No search over rooms, rays, directions or reflection words.
Run: python3 -B stress.py
"""
import json
import sys
import time
from fractions import Fraction as Fr
from pathlib import Path

D = Path(__file__).resolve().parent.parent
D8 = D / 'd8-perturbation-test'
sys.path.insert(0, str(D8))
sys.path.insert(0, str(D8 / 'ref'))
from room import is_strictly_simple, status  # noqa: E402
from tracer import advance, certify as trace_certify  # noqa: E402
import surface as SF  # noqa: E402

src = (D / 'd82-review-necessity' / 'indep.py').read_text().rsplit('\nmain()', 1)[0]
IND = {'__file__': str(D / 'd82-review-necessity' / 'indep.py'), '__name__': 'indep'}
exec(compile(src, 'indep', 'exec'), IND)
NAMES = {(0, 0): 'a(source)', (1, 1): 'b', (1, 0): 'c1', (0, 1): 'c2'}


def coincidences(cells, S, T):
    cl, idx, g, local = IND['monodromy'](cells)
    n = len(cl)
    lab, sizes = IND['orbit_partition'](list(g.values()), n)
    keys = IND['marked_union'](lab, idx, S, T)
    d = sum(sizes[k] for k in keys) // n
    r = sum(k == 'reflex' for _, _, k, _ in local)
    rel = lambda p: ((p[0] - S[0]) % 2, (p[1] - S[1]) % 2)
    reg = []   # (class, point, kind, 2-cycle)
    J = 0
    for x, p, kind, cyc in local:
        for cy in cyc:
            if len(cy) == 2 and lab[cy[0], cy[1]] in keys:
                reg.append((rel(p), p, kind, tuple(cy)))
            elif len(cy) == 3:
                J += sum(lab[cy[0], cy[s]] in keys for s in (1, 2))
    assert 2 * d == len(reg) + J
    return n, r, d, reg, idx


def half_trace(cells, S, T, W):
    """Signed vector Ds for witness W (both tracers), midpoint, arrival cell."""
    Ds = trace_certify(cells, S, T, W)
    if Ds is None:
        return None
    H = (Fr(Ds[0], 2), Fr(Ds[1], 2))
    end, ok, _, v = advance(cells, Fr(S[0]), Fr(S[1]), H[0], H[1])
    assert ok
    M = (int(end[0]), int(end[1]))
    assert end == M
    # arrival cell: the cell holding M - eps * v
    cx = M[0] - 1 if v[0] > 0 else M[0]
    cy = M[1] - 1 if v[1] > 0 else M[1]
    arrival = (cx, cy) if v[0] != 0 and v[1] != 0 else None
    # second tracer: d3 surface, half vector and full vector
    surf = SF.Surface(cells)
    if Ds[0] != 0 and Ds[1] != 0:
        rp, ok2, _ = surf.segment((Fr(S[0]), Fr(S[1])), H)
        rp_full, ok3, _ = surf.segment((Fr(S[0]), Fr(S[1])), Ds)
        second = ok2 and ok3 and rp == end and rp_full == (Fr(T[0]), Fr(T[1]))
    else:
        second = None
    return Ds, M, arrival, second


def main():
    t0 = time.process_time()
    rooms = [json.loads(l) for l in open(D8 / 'results.jsonl')]
    rooms = [x for x in rooms if x['base'] == 'R22' and x['level'] <= 1]
    rooms.sort(key=lambda x: (x['level'], x['id']))
    rows = []
    for x in rooms:
        cells = set(map(tuple, x['cells']))
        S, T = map(tuple, x['marks'])
        ok_room = (is_strictly_simple(cells) and status(cells, S) == 'interior'
                   and status(cells, T) == 'interior')
        n, r, d, reg, idx = coincidences(cells, S, T)
        assert r == x['r'] and x['W'] == 4 + 2 * r and n == x['area']
        if x['level'] == 1 and not (ok_room and r <= 8):
            continue
        by = {}
        for c, p, kind, cy in reg:
            by.setdefault(c, []).append((p, kind))
        off = sum(len(v) for c, v in by.items() if c != (0, 0))
        print('%s moves=%r strictly_simple+interior=%s n=%d r=%d d=%d 2n/3=%.1f d=n-1:%s'
              % (x['id'], x['moves'], ok_room, n, r, d, 2 * n / 3, d == n - 1))
        for c in sorted(by):
            print('   class %-9s %2d: %s' % (NAMES[c], len(by[c]), sorted(by[c])))
        bound = 2 * -(-2 * n // 3) - 16 - n // 2
        print('   off-class regular coincidences=%d; lemma bound (if d>=2n/3)=%d; 2d-2r-floor(n/2)=%d'
              % (off, bound, 2 * d - 2 * r - n // 2))
        mids = []
        for pr in x['pairs']:
            if not pr['marks'] or pr.get('witness') is None:
                continue
            res = half_trace(cells, S, T, tuple(pr['witness']))
            assert res is not None, 'saved witness not certified'
            Ds, M, arrival, second = res
            c = ((M[0] - S[0]) % 2, (M[1] - S[1]) % 2)
            cyc = None
            if arrival is not None and status(cells, M) == 'smooth':
                # one 2-cycle at a flat-wall point; v may already be reflected at M
                cyc = [cy for cc, p, kind, cy in reg if p == M]
            elif arrival is not None:
                cyc = [cy for cc, p, kind, cy in reg if p == M and idx[arrival] in cy]
            pt_hit = any(p == M for _, p, _, _ in reg)
            print('   witness %s signed %s: midpoint %s (%s), class %s; second tracer agrees=%s; '
                  'point in coincidence list=%s; arrival-cell 2-cycle in union=%s'
                  % (pr['witness'], Ds, M, status(cells, M), NAMES[c], second, pt_hit,
                     bool(cyc) if cyc is not None else 'axis'))
            mids.append(c)
        if x['level'] == 1 and mids and all(c == (0, 0) for c in mids):
            print('   STEP 4 NEEDED: all saved midpoints in the source class')
        rows.append((x['id'], x['moves'], n, r, d, off,
                     ','.join(NAMES[c] for c in mids) or 'none (dark)'))
    print()
    print('| Room | Moves | n | r | d | Off-class regular coincidences | Witness midpoint class |')
    print('| --- | --- | ---: | ---: | ---: | ---: | --- |')
    for row in rows:
        print('| `%s` | %s | %d | %d | %d | %d | %s |' % ((row[0], row[1].replace(' | ', '; ') or 'none') + row[2:]))
    print('CPU seconds: %.1f' % (time.process_time() - t0))


if __name__ == '__main__':
    main()
