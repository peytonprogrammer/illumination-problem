"""Combinatorial test of the Lemma U hypothesis for each open pair.

Lemma U (README): if one point (say T) lies strictly inside a corridor
E = [x_i0, x_i1] x [y_j0, y_j1] (both side lines are walls on the whole height,
all cells between are in P), and the other point's x-index range is disjoint
from the closed column range [2 i0, 2 i1], then shrinking the gaps of columns
i0..i1-1 to 0 (all else fixed) forces the reflection count of every lighting
path to infinity. Same with axes swapped and with S, T swapped.
Output: thin_corridor_r3.tsv with one row per open pair."""
import json, sys
import wm

def corridors(ot, P, axis):
    """Corridors along `axis` ('v' = vertical corridor, side walls are vertical
    lines) containing P strictly inside. Yields (i0, i1, j0, j1)."""
    nx, ny = (ot.nx, ot.ny) if axis == 'v' else (ot.ny, ot.nx)
    ins = (lambda i, j: ot.ins(i, j)) if axis == 'v' else (lambda i, j: ot.ins(j, i))
    X, Y = (P[0], P[1]) if axis == 'v' else (P[1], P[0])
    for i0 in range(nx):
        for i1 in range(i0 + 1, nx + 1):
            if not (2 * i0 < X < 2 * i1): continue
            def ok(j):
                return all(ins(i, j) for i in range(i0, i1)) and not ins(i0 - 1, j) and not ins(i1, j)
            rows = [j for j in range(ny) if ok(j)]
            # maximal run of rows containing P strictly inside
            for j0 in range(ny):
                j1 = j0
                while j1 < ny and ok(j1): j1 += 1
                if j1 > j0 and 2 * j0 < Y < 2 * j1:
                    yield (i0, i1, j0, j1)

def lemma_u(ot, S, T):
    hits = []
    for A, B, nmA in ((S, T, 'S'), (T, S, 'T')):
        for axis in ('v', 'h'):
            for (i0, i1, j0, j1) in corridors(ot, A, axis):
                Bx = B[0] if axis == 'v' else B[1]
                if Bx < 2 * i0 or Bx > 2 * i1:
                    hits.append((nmA, axis, i0, i1, j0, j1))
    return hits

if __name__ == '__main__':
    rows = json.load(open('tools/cert_r3.json'))
    kinds = {}
    for line in open('kinds_r3.tsv'):
        m, s, t, k = line.rstrip('\n').split('\t'); kinds[(int(m), s, t)] = k
    out = open('thin_corridor_r3.tsv', 'w')
    out.write('mask\tshape\tS\tT\tkind\tlemmaU\twitness_corridor\n')
    n = nyes = 0
    from collections import Counter
    byk = Counter()
    for r in rows:
        ot = wm.OT.from_mask(r['nx'], r['ny'], r['mask'])
        for S, T in r['uncovered']:
            S, T = tuple(S), tuple(T)
            h = lemma_u(ot, S, T)
            k = kinds[(r['mask'], str(S), str(T))]
            n += 1; nyes += bool(h); byk[(k, bool(h))] += 1
            out.write(f"{r['mask']}\t{r['shape']}\t{S}\t{T}\t{k}\t{int(bool(h))}\t{h[0] if h else ''}\n")
    print('open pairs', n, 'with a Lemma U corridor', nyes, dict(byk))
