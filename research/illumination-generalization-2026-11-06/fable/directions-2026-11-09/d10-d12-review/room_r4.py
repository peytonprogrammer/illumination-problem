"""Fixed-polygon checks for the gap in Proposition R4, step 3 (no room search).

R4 step 3 says the degree-3 Cut target N is the double of the planar L-tromino. That holds
when the two [2,1] classes are diagonal. When they are adjacent, the unique cover with
types [2,1], [2,1], [1^3], [3] is the double of a 3-cell disc K2 with an interior cone
point of angle pi. This script shows K2 occurs as a fold target of strictly simple rooms:

  H   : the Z-hexomino, rows y=1: x=-1..1 and y=0: x=0..2.
  P12 : H and its mirror image in the line y = 0.
  L   : the L-tromino (control, diagonal case).
  X   : the 12-wall cross (control, the room of R4).

Class a = (even, even), b = (odd, even), c = (odd, odd), d = (even, odd) after the shift
by `origin`. Tuples: g_a = k_da k_ab, g_b = k_ab k_bc, g_c = k_bc k_cd, g_d = k_cd k_da,
where k_E crosses the edge of type E (identity at a wall). The product telescopes to 1.
"""
import sys
from lib import mul, cyc, cyc_id, ctype, all_block_systems, induced, D6
from check_u import Fac, analyse_pair

sys.path.insert(0, str(D6))
from hurwitz import marked_orbit, initial_pt          # the validated decider, verdicts only


def room_tuple(cells, origin=(0, 0)):
    cells = sorted(cells)
    idx = {c: i for i, c in enumerate(cells)}
    kap = {E: list(range(len(cells))) for E in ('ab', 'bc', 'cd', 'da')}
    for (i, j), s in idx.items():
        pi, pj = (i - origin[0]) % 2, (j - origin[1]) % 2
        edges = {(i, j - 1): 'ab' if pj == 0 else 'cd', (i, j + 1): 'cd' if pj == 0 else 'ab',
                 (i - 1, j): 'da' if pi == 0 else 'bc', (i + 1, j): 'bc' if pi == 0 else 'da'}
        for nb, E in edges.items():
            if nb in idx:
                kap[E][s] = idx[nb]
    k = {E: tuple(v) for E, v in kap.items()}
    t = (mul(k['da'], k['ab']), mul(k['ab'], k['bc']), mul(k['bc'], k['cd']), mul(k['cd'], k['da']))
    assert mul(mul(mul(t[0], t[1]), t[2]), t[3]) == tuple(range(len(cells)))
    return cells, idx, t, k


def status(cells, p):
    x, y = p
    return sum(1 for c in ((x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)) if c in cells)


def star(idx, p):
    x, y = p
    return sorted(idx[c] for c in ((x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)) if c in idx)


def report(name, cells, origin, marks):
    cells = set(cells)
    cl, idx, t, k = room_tuple(cells, origin)
    n = len(cl)
    print(f'== {name}: {n} cells, origin {origin}')
    print('   types a b c d:', [list(ctype(g)) for g in t])
    pts = sorted({(i + dx, j + dy) for (i, j) in cells for dx in (0, 1) for dy in (0, 1)})
    interior = [p for p in pts if status(cells, p) == 4]
    names = 'adbc'
    print('   interior lattice points:',
          [(p, names[2 * ((p[0] - origin[0]) % 2) + ((p[1] - origin[1]) % 2)]) for p in interior])
    systems = all_block_systems(t)
    for w in systems:
        m = max(w) + 1
        if m in (1, n):
            continue
        F = Fac(t, w)
        inv_k = all(len({w[kk[i]] for i in range(n) if w[i] == b}) == 1
                    for kk in k.values() for b in range(m))
        print(f'   factor of degree {m}: types', [sorted(F.len[y], reverse=True) for y in range(4)],
              '| kappa-invariant:', inv_k)
        if m == 3:
            # Cut hypothesis: every regular point of Q over a and b maps to a regular point of N
            bad = []
            for y in (0, 1):
                for c in cyc(t[y]):
                    if len(c) == 2 and F.len[y][F.point(y, c[0])] != 2:
                        bad.append(('ab'[y], c))
            print('      regular points of DP over a or b that map to a pole of N:', bad)
    if marks:
        S, T = marks
        sS, sT = star(idx, S), star(idx, T)
        print(f'   marks {S} (status {status(cells, S)}), {T} (status {status(cells, T)})')
        cid, plen = initial_pt(t[0])
        res = marked_orbit(t)
        for c1 in {cid[s] for s in sS}:
            for c2 in {cid[s] for s in sT}:
                s1 = next(s for s in sS if cid[s] == c1)
                s2 = next(s for s in sT if cid[s] == c2)
                r = analyse_pair(t, systems, s1, s2)
                print('      lift pair', (c1, c2), 'certificates over B (b, c, d):',
                      [r['certB'].get(x, '') for x in (1, 2, 3)], '| full:', bool(r['full']),
                      '| decider LIT:', frozenset((c1, c2)) in res['lit'])


H = [(-1, 1), (0, 1), (1, 1), (0, 0), (1, 0), (2, 0)]
P12 = H + [(i, -1 - j) for (i, j) in H]
L = [(0, 0), (1, 0), (0, 1)]
X = [(i, j) for i in range(4) for j in range(4) if not (i in (0, 3) and j in (0, 3))]

if __name__ == '__main__':
    report('Z-hexomino H (adjacent case; marks are wall points)', H, (0, 0), ((2, 0), (0, 2)))
    report('P12 = H with its mirror in y = 0', P12, (0, 0), None)
    report('L-tromino (diagonal case, control)', L, (1, 0), None)
    report('12-wall cross, S = (1,2), T = (3,2) (the room of R4)', X, (1, 2), ((1, 2), (3, 2)))
