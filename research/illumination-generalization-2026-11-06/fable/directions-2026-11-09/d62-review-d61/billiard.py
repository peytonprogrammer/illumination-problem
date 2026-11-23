"""d62: independent billiard ground truth on R22 (interior + smooth wall marks).

Exact integer billiards in the cell room, no permutations, no orbit walk. For each primitive
direction (p, q) with max(p, q) <= H and each sign pair, shoot from S; continue straight
through interior and smooth-wall lattice points (reflecting at walls), stop at convex or
reflex corners or on a repeated state. Record the class x of the direction and the copy bit
(parity of wall reflections) on arrival at T. Compare with d61 rows at N = B.
"""
import sys, json, time, re
from math import gcd
from itertools import combinations
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd61-fold-converse'))
sys.path.insert(0, str(HERE.parent / 'd10-mechanisms'))
from roomtools import lattice_points, status  # noqa: E402
from fold_converse import rooms  # noqa: E402


def quad(v, sx, sy):
    return (v[0] + (0 if sx > 0 else -1), v[1] + (0 if sy > 0 else -1))


def shoot(cells, S, p, q, sx, sy, targets, lim):
    """Yield (T, copy) for every target T reached at an even step before a corner."""
    v, c = S, 0
    seen = set()
    hits = []
    for step in range(1, lim):
        # leave lattice point v
        if p and q:
            if quad(v, sx, sy) not in cells:
                if quad(v, sx, -sy) in cells:
                    sy, c = -sy, c ^ 1
                elif quad(v, -sx, sy) in cells:
                    sx, c = -sx, c ^ 1
                else:
                    raise AssertionError(('stuck', v))
            cell = quad(v, sx, sy)
            # crossings: vertical at k/p, horizontal at m/q (never simultaneous inside)
            k = m = 1
            while k < p or m < q:
                if m >= q or (k < p and k * q < m * p):
                    nb = (cell[0] + sx, cell[1])
                    if nb in cells:
                        cell = nb
                    else:
                        sx, c = -sx, c ^ 1
                    k += 1
                else:
                    nb = (cell[0], cell[1] + sy)
                    if nb in cells:
                        cell = nb
                    else:
                        sy, c = -sy, c ^ 1
                    m += 1
            v = (cell[0] + (1 if sx > 0 else 0), cell[1] + (1 if sy > 0 else 0))
        else:
            # axis direction along a grid line
            for _ in range(2):
                if p:   # horizontal, sign sx
                    adj = [(v[0] + (0 if sx > 0 else -1), v[1] + dy) for dy in (0, -1)]
                    if any(a in cells for a in adj):
                        v = (v[0] + sx, v[1]); break
                    sx, c = -sx, c ^ 1
                else:
                    adj = [(v[0] + dx, v[1] + (0 if sy > 0 else -1)) for dx in (0, -1)]
                    if any(a in cells for a in adj):
                        v = (v[0], v[1] + sy); break
                    sy, c = -sy, c ^ 1
            else:
                raise AssertionError('stuck axis')
        st = status(cells, v)
        if step % 2 == 0 and v in targets:
            hits.append((v, c))
        if st not in ('interior', 'smooth'):
            break
        key = (v, sx, sy, c)
        if key in seen:
            break
        seen.add(key)
    else:
        raise AssertionError('lim')
    return hits


def main(H, name='R22'):
    cells = dict(rooms())[name]
    pts = [p for p in lattice_points(cells) if status(cells, p) in ('interior', 'smooth')]
    dirs = [(p, q) for p in range(H + 1) for q in range(H + 1) if gcd(p, q) == 1]
    lim = 8 * len(lattice_points(cells)) + 8
    lit = defaultdict(set)      # (S, T, x) -> copies
    for S in pts:
        targets = {T for T in pts if T != S and (T[0] - S[0]) % 2 == 0 and (T[1] - S[1]) % 2 == 0}
        if not targets:
            continue
        for p, q in dirs:
            x = {(1, 0): 'b', (1, 1): 'c', (0, 1): 'd'}[(p % 2, q % 2)]
            for sx in (1, -1):
                for sy in (1, -1):
                    for T, c in shoot(cells, S, p, q, sx, sy, targets, lim):
                        lit[(S, T, x)].add(c)
    return cells, pts, lit


if __name__ == '__main__':
    H = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    name = sys.argv[2] if len(sys.argv) > 2 else 'R22'
    src = sys.argv[3] if len(sys.argv) > 3 else 'fc_wall_cross12_R22.json'
    t0 = time.process_time()
    cells, pts, lit = main(H, name)
    rows = json.load(open(HERE.parent / 'd61-fold-converse' / src))
    d61 = defaultdict(int)
    tags = set()
    for r in rows:
        if r['room'] == name and r['blocks'] == 1:
            tags.add(r['tag'])
            d61[(r['tag'], r['x'])] += r['lit_x']
    bad = 0
    for tag in sorted(tags):
        nums = [int(z) for z in re.findall(r'-?\d+', tag)]
        S, T = tuple(nums[:2]), tuple(nums[2:])
        for x in 'bcd':
            C = lit.get((S, T, x), set())
            iS, iT = status(cells, S) == 'interior', status(cells, T) == 'interior'
            if iS:
                mine = (2 * len(C)) if iT else 2 * bool(C)
            else:
                mine = len(C) if iT else int(bool(C))
            ok = mine == d61[(tag, x)]
            bad += not ok
            print('%-18s x=%s  billiard lit lift pairs=%d  d61=%d %s' % (tag, x, mine, d61[(tag, x)],
                                                                        '' if ok else '<-- MISMATCH'))
    print('H=%d mismatches %d  CPU %.1f s' % (H, bad, time.process_time() - t0))
