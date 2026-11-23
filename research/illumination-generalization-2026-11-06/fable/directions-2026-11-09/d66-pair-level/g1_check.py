"""d66: different-class lattice pairs (gap G1), exact integer billiards, no permutations.

shoot() is d62 billiard.shoot copied with one change: hits are recorded at steps of a given
parity (odd = the other class). For each room and each interior lattice point S, every
primitive direction (p, q) with max(p, q) <= H and all four signs is shot once; every interior
lattice point T of a different class reached before a corner is lit from S (an exact path).
A pair with no witness is UNRESOLVED (not dark). Unresolved pairs are retried at H2.
Rooms: the named rooms and the R* rooms of pair_level.json that have a same-class pair.
With a third argument 'all', every normalized room of d64 covers.json is added.
Usage: python3 -B g1_check.py H H2 [all]
"""
import json
import resource
import sys
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
sys.path.insert(0, str(D / 'd10-mechanisms'))
sys.path.insert(0, str(D / 'd64-finite-case'))
sys.path.insert(0, str(D / 'd65-nx-equals-b'))
import rl_test  # noqa: E402,F401  (path setup)
import notch12 as NZ  # noqa: E402
from realize import rooms as named_rooms  # noqa: E402
from roomtools import lattice_points, status  # noqa: E402

resource.setrlimit(resource.RLIMIT_CPU, (300, 300))


def quad(v, sx, sy):
    return (v[0] + (0 if sx > 0 else -1), v[1] + (0 if sy > 0 else -1))


def shoot(cells, S, p, q, sx, sy, targets, lim, parity=0):
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
        if step % 2 == parity and v in targets:
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




def lit_from(cells, S, H, targets):
    lim = 8 * len(lattice_points(cells)) + 8
    got = set()
    for p in range(H + 1):
        for q in range(H + 1):
            if gcd(p, q) != 1:
                continue
            for sx in (1, -1):
                for sy in ((1, -1) if q else (1,)):
                    if not p and sy < 0:
                        continue
                    for T, c in shoot(cells, S, p, q, sx, sy, targets - got, lim, parity=1):
                        got.add(T)
                    if got == targets:
                        return got
    return got


def run(name, cells, H, H2):
    ipts = [p for p in lattice_points(cells) if status(cells, p) == 'interior']
    pairs = {(S, T) for S in ipts for T in ipts if S < T and ((S[0] - T[0]) % 2, (S[1] - T[1]) % 2) != (0, 0)}
    lit = set()
    for S in ipts:
        tg = {T for T in ipts if ((S[0] - T[0]) % 2, (S[1] - T[1]) % 2) != (0, 0)}
        for T in lit_from(cells, S, H, tg):
            lit.add((min(S, T), max(S, T)))
    unres = pairs - lit
    for S, T in sorted(unres):
        if T in lit_from(cells, S, H2, {T}):
            lit.add((S, T))
    return len(pairs), len(pairs - lit), sorted(pairs - lit)


if __name__ == '__main__':
    import time
    H, H2 = int(sys.argv[1]), int(sys.argv[2])
    t0 = time.process_time()
    cov = [r for r in json.load(open(D / 'd64-finite-case' / 'data' / 'covers.json'))['rooms'] if r['normalized']]
    cov.sort(key=lambda r: (r['n'], r['cells']))
    pl = json.load(open(HERE / 'pair_level.json'))['rooms']
    named = {}
    for r in pl:
        if not r['name'].startswith('cov') or r['counts'].get('pairs'):
            named[r['name']] = r
    if len(sys.argv) > 3 and sys.argv[3] == 'all':
        for i in range(len(cov)):
            named.setdefault('cov%d' % i, None)
    tot = [0, 0, 0]
    cellmap = dict(named_rooms())
    cellmap.update(Z12=NZ.Z12, S10=NZ.S10)
    for name, r in named.items():
        if name.startswith('cov') or name.startswith('room'):
            cells = set(tuple(c) for c in cov[int(name[3:] if name.startswith('cov') else name[4:])]['cells'])
        elif name in cellmap:
            cells = set(cellmap[name])
        else:
            continue
        npairs, nun, un = run(name, cells, H, H2)
        tot[0] += 1
        tot[1] += npairs
        tot[2] += nun
        if nun or not name.startswith('cov'):
            print(name, 'n', len(cells), 'different-class pairs', npairs, 'unresolved', nun, un[:6], flush=True)
    print('rooms %d different-class interior pairs %d unresolved %d CPU %.1f' % (tot[0], tot[1], tot[2], time.process_time() - t0))
