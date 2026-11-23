"""Test the static certificates of Theorem U (theory.md, section 2) on the saved census.

Reads ../d6-hurwitz-census/census_n*.json (n <= 10).  Enumerates nothing new: every pair
and its LIT/DARK verdict comes from the saved files.  For each pair (sigma, tau) the script
looks for a certificate tower Q -> N -> P' -> B and reports

  soundness : number of LIT pairs that get a full certificate (must be 0);
  coverage  : number of DARK pairs without a full certificate (the "only if" conjecture
              says 0).

Certificates, all checked in the single basis stored in the census file:

  base B, per corner x in {b, c, d}; N = Q / Pi for a block system Pi with >= 2 blocks:
    Par(x)  phi(sigma) != phi(tau); N has no regular point over x.
    Rig(x)  N has identity monodromy at a corner y not in {a, x}; phi(tau) is outside the
            live component of phi(sigma) in the graph of the tail arc a -> x in N.
            A vertex is live if some regular point of Q lies over it.
    Cut(x)  phi(sigma) == phi(tau); every regular point of Q over a and x maps to a
            regular point of N; the monodromy of N at a corner y not in {a, x} is one cycle.
  base P' (a block system whose quotient is a pillowcase other than B):
    ParRel  sigma, tau over one P'-corner c0; for each other P'-corner x' some N between
            Q and P' separates sigma, tau and has no regular point over x'.
    RigRel  sigma, tau over different P'-corners c_s, c_t; some N between Q and P' has
            only poles over a third P'-corner; a tail arc of the basis lifts to a P'-arc
            c_s -> c_t; phi(tau) is outside the live component of phi(sigma) along it.

The script also compares Rig with the edge rule coded in d6 rigid_factor.g6_dark (an edge
needs a sheet of Q whose two end points are regular in the given basis).

Run: python3 -B unified_test.py        (writes unified_test.json)
"""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
D6 = HERE.parent / 'd6-hurwitz-census'
sys.path.insert(0, str(D6))
import d4_monodromy as d4            # noqa: E402
from hurwitz import cycles           # noqa: E402


class Factor:
    """Q -> N = Q / part, with the data the certificates need."""

    def __init__(self, t, part):
        n = len(t[0])
        self.part = part
        self.m = len(part)
        self.where = [0] * n
        for b, blk in enumerate(part):
            for s in blk:
                self.where[s] = b
        self.ig = [d4.induced(g, part) for g in t]
        self.ncid, self.nlen, self.live = [], [], []
        for y in range(4):
            cid = [0] * self.m
            lens = []
            for k, cy in enumerate(cycles(self.ig[y])):
                lens.append(len(cy))
                for b in cy:
                    cid[b] = k
            live = [False] * len(lens)
            for c in cycles(t[y]):
                if len(c) == 2:
                    live[cid[self.where[c[0]]]] = True
            self.ncid.append(cid)
            self.nlen.append(lens)
            self.live.append(live)

    def a_point(self, sheet):
        return self.ncid[0][self.where[sheet]]

    def live_component(self, x, start):
        """N-points over a in the live component of `start` along the tail arc a -> x."""
        if not self.live[0][start]:
            return {start}
        adj = {}
        for b in range(self.m):
            u, v = ('a', self.ncid[0][b]), ('x', self.ncid[x][b])
            if self.live[0][u[1]] and self.live[x][v[1]]:
                adj.setdefault(u, set()).add(v)
                adj.setdefault(v, set()).add(u)
        seen = {('a', start)}
        stack = [('a', start)]
        while stack:
            u = stack.pop()
            for v in adj.get(u, ()):
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        return {u[1] for u in seen if u[0] == 'a'}


def par(F, x, s, q):
    return F.a_point(s) != F.a_point(q) and 2 not in F.nlen[x]


def rig(F, x, s, q):
    if not any(all(l == 1 for l in F.nlen[y]) for y in (1, 2, 3) if y != x):
        return False
    return F.a_point(q) not in F.live_component(x, F.a_point(s))


def cut(F, t, x, s, q):
    if F.a_point(s) != F.a_point(q):
        return False
    for y in (0, x):
        for c in cycles(t[y]):
            if len(c) == 2 and F.nlen[y][F.ncid[y][F.where[c[0]]]] != 2:
                return False
    return any(len(F.nlen[y]) == 1 for y in (1, 2, 3) if y != x)


def g6_coded_edges(F, t, x, s, q):
    """Rig with the d6 edge rule (both Q-end points of a sheet regular in this basis)."""
    if not any(all(l == 1 for l in F.nlen[y]) for y in (1, 2, 3) if y != x):
        return False
    n = len(t[0])
    qlen = []
    for y in (0, x):
        L = [0] * n
        for c in cycles(t[y]):
            for i in c:
                L[i] = len(c)
        qlen.append(L)
    parent = {}

    def find(u):
        while parent.setdefault(u, u) != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u

    for i in range(n):
        if qlen[0][i] == 2 and qlen[1][i] == 2:
            b = F.where[i]
            ru, rv = find(('a', F.ncid[0][b])), find(('x', F.ncid[x][b]))
            if ru != rv:
                parent[ru] = rv
    return find(('a', F.a_point(s))) != find(('a', F.a_point(q)))


def is_pillowcase(F):
    lens = [l for y in range(4) for l in F.nlen[y]]
    return max(lens) <= 2 and lens.count(1) == 4


def refines(small, big):
    return all(len({big.where[s] for s in blk}) == 1 for blk in small.part)


def corners_of(Pp):
    """P'-corners as (B-corner index y, block of P' fixed by the induced g_y)."""
    return [(y, b) for y in range(4) for b in range(Pp.m) if Pp.ig[y][b] == b]


def n_points_over(N, Pp, corner):
    """Indices of N-points at B-corner y lying over the P'-corner (y, beta)."""
    y, beta = corner
    return {N.ncid[y][sb] for sb in range(N.m) if Pp.where[N.part[sb][0]] == beta}


def tail_end(Pp, j, beta):
    """End corner of the P'-arc that lifts the tail arc a -> x_j, starting at (0, beta)."""
    side, cur = j, beta
    while True:
        nxt = Pp.ig[side][cur]
        if nxt == cur:
            return (side, cur)
        cur = nxt
        side = 0 if side == j else j


def analyse_pair(t, factors, s, q):
    """Return (certificate description or None, flags)."""
    flags = Counter()
    proper = [F for F in factors if F.m > 1]
    perx = {}
    for x in (1, 2, 3):
        kinds = set()
        for F in proper:
            if par(F, x, s, q):
                kinds.add('Par')
            if rig(F, x, s, q):
                kinds.add('Rig')
            if cut(F, t, x, s, q):
                kinds.add('Cut')
            a, b = rig(F, x, s, q), g6_coded_edges(F, t, x, s, q)
            if b and not a:
                flags['coded G6 edge rule separates, live rule does not'] += 1
        perx[x] = kinds
    base_b = all(perx[x] for x in (1, 2, 3))
    one_parity = any(all(par(F, x, s, q) for x in (1, 2, 3)) for F in proper)

    rel = None
    for Pp in factors:
        if Pp.m == 1 or Pp.m == len(t[0]) or not is_pillowcase(Pp):
            continue
        bs, bq = Pp.where[s], Pp.where[q]
        if Pp.ig[0][bs] != bs or Pp.ig[0][bq] != bq:
            continue                       # a mark over a non-corner of P'
        mids = [N for N in factors if N.m >= Pp.m and refines(N, Pp)]
        cs, ct = (0, bs), (0, bq)
        if cs == ct:
            others = [c for c in corners_of(Pp) if c != cs]
            ok = True
            for c in others:
                if not any(N.a_point(s) != N.a_point(q)
                           and all(N.nlen[c[0]][k] != 2 for k in n_points_over(N, Pp, c))
                           for N in mids):
                    ok = False
                    break
            if ok:
                rel = ('ParRel', len(t[0]) // Pp.m)
                break
        else:
            arcs = [j for j in (1, 2, 3) if tail_end(Pp, j, bs) == ct]
            if not arcs:
                flags['RigRel: no tail arc of the basis joins c_s to c_t'] += 1
                continue
            j = arcs[0]
            for N in mids:
                third = [c for c in corners_of(Pp) if c not in (cs, ct)]
                if not any(all(N.nlen[c[0]][k] == 1 for k in n_points_over(N, Pp, c)) for c in third):
                    continue
                if N.a_point(q) not in N.live_component(j, N.a_point(s)):
                    rel = ('RigRel', len(t[0]) // Pp.m)
                    break
            if rel:
                break

    if one_parity:
        desc = 'one parity factor'
    elif base_b:
        desc = 'B: ' + ' / '.join('+'.join(sorted(perx[x])) for x in (1, 2, 3))
    elif rel:
        desc = '%s over a pillowcase of degree %d' % (rel[0], len(t[0]) // rel[1])
    else:
        desc = None
    return desc, flags, perx, rel


def canonical_kind(desc):
    """Collapse the corner order: sort the three per-corner certificate sets."""
    if desc and desc.startswith('B: '):
        return 'B: ' + ' / '.join(sorted(desc[3:].split(' / ')))
    return desc


def main():
    out = {}
    for f in sorted(D6.glob('census_n*.json'), key=lambda p: int(p.stem[8:])):
        d = json.loads(f.read_text())
        n = d['n']
        S = Counter()
        kinds = Counter()
        flags = Counter()
        uncovered = []
        for cl in d['classes']:
            for o in cl['orbits']:
                if o['n_two_cycles_a'] < 2:
                    continue
                t = tuple(tuple(g) for g in o['rep'])
                factors = [Factor(t, part) for part in d4.all_block_systems(list(t), n)]
                for p in o['pairs']:
                    desc, fl, perx, rel = analyse_pair(t, factors, p['sheets_P'][0], p['sheets_Q'][0])
                    flags.update(fl)
                    lit = p['lit']
                    S['pairs'] += 1
                    blocked = sum(1 for x in (1, 2, 3) if perx[x])
                    if lit:
                        S['LIT pairs'] += 1
                        S['LIT pairs with %d of 3 corners certified over B' % blocked] += 1
                        if desc:
                            S['LIT pairs with a certificate (unsound)'] += 1
                    else:
                        S['DARK pairs'] += 1
                        for drop in ('Par', 'Rig', 'Cut'):
                            if not rel and not all(perx[x] - {drop} for x in (1, 2, 3)):
                                S['DARK pairs that need ' + drop] += 1
                        if rel and not all(perx[x] for x in (1, 2, 3)):
                            S['DARK pairs that need a relative certificate'] += 1
                        if desc:
                            S['DARK pairs with a certificate'] += 1
                            kinds[canonical_kind(desc)] += 1
                        else:
                            S['DARK pairs without a certificate'] += 1
                            uncovered.append(dict(cts=cl['cts'], rep=o['rep'], sigma=p['sheets_P'],
                                                  tau=p['sheets_Q']))
        out[str(n)] = dict(counts=dict(S), certificate_kinds=dict(kinds), flags=dict(flags),
                           uncovered=uncovered)
        print(n, dict(S))
        for k, v in sorted(kinds.items()):
            print('     ', v, k)
        if flags:
            print('      flags', dict(flags))
    (HERE / 'unified_test.json').write_text(json.dumps(out, indent=1) + '\n')


if __name__ == '__main__':
    main()
