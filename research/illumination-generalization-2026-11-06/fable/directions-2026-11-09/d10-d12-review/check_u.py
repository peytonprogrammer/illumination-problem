"""Theorem U (d10-mechanisms/theory.md, section 2) on the saved census, from the definitions.

For every census pair (sigma, tau) and every pillowcase factor P' of Q (B included) with
sigma and tau over corners c_s, c_t of P', the script decides, for every target corner x'
of P', whether some factor N with Q -> N -> P' satisfies Par(x'), Rig(x'), or Cut(x')
RELATIVE TO P'. Unlike d10-mechanisms/unified_test.py it implements all three kinds over
every pillowcase base, and it builds the Rig graph from the lifts of an actual P'-arc.

Rig needs one simple arc of P' from c_s to x'. The script takes the straight lift of a
tail arc a -> x_j of a basis in the pure-braid orbit. It walks literal bases (no
conjugation) and transports each corner point by the conjugating permutation of its loop,
so block systems and points keep their identity.

Output: u_nN.json.gz. Soundness of Theorem U means no LIT pair has a full certificate.
Run: python3 -B check_u.py N [N ...]
"""
import json
import sys
import time
from collections import Counter, deque

from lib import save_out, mul, inv, cyc, cyc_id, conj_fn, all_block_systems, induced, census_orbits

STATE_CAP = 4000


class Fac:
    """Q -> N = Q / where, in one basis t."""

    def __init__(self, t, where):
        self.where = where
        self.m = max(where) + 1
        self.ig = [induced(g, where, self.m) for g in t]
        self.cid, self.len = [], []
        for y in range(4):
            c, l = cyc_id(self.ig[y])
            self.cid.append(c)
            self.len.append(l)

    def point(self, y, sheet):
        return self.cid[y][self.where[sheet]]


def refines(N, P):
    seen = {}
    for a, b in zip(N.where, P.where):
        if seen.setdefault(a, b) != b:
            return False
    return True


def is_pillowcase(P):
    fixed = 0
    for y in range(4):
        for l in P.len[y]:
            if l > 2:
                return False
            fixed += (l == 1)
    return fixed == 4


def corners(P):
    return [(y, b) for y in range(4) for b in range(P.m) if P.ig[y][b] == b]


def nblocks_in(N, P, beta):
    """N-blocks contained in the P'-block beta."""
    return sorted({N.where[i] for i in range(len(N.where)) if P.where[i] == beta})


def two_cycles(g):
    return [(i, j) for i, j in enumerate(g) if i < j and g[j] == i]


def par(N, P, phis, phit, x):
    y, beta = x
    if phis == phit:
        return False
    return all(N.len[y][N.cid[y][b]] != 2 for b in nblocks_in(N, P, beta))


def cut(t, N, P, phis, phit, cs, x, allc):
    if phis != phit:
        return False
    for (y, beta) in (cs, x):
        for (i, j) in two_cycles(t[y]):
            if P.where[i] == beta and N.len[y][N.point(y, i)] != 2:
                return False
    for (y2, b2) in allc:
        if (y2, b2) in (cs, x):
            continue
        nb = nblocks_in(N, P, b2)
        if len({N.cid[y2][b] for b in nb}) == 1 and N.len[y2][N.cid[y2][nb[0]]] == len(nb):
            return True
    return False


def rigid_corner(N, P, cs, x, allc):
    """Some P'-corner outside {c_s, x} over which N -> P' has identity monodromy."""
    for (y2, b2) in allc:
        if (y2, b2) in (cs, x):
            continue
        if all(N.ig[y2][b] == b for b in nblocks_in(N, P, b2)):
            return True
    return False


def half_move_k(t, i, sign):
    """Returns (t', pos_from, pos_to, k): the loop at pos_from moves to pos_to and its
    cycles become the k-images of the old cycles. The other loop of the pair swaps place
    unchanged."""
    t = list(t)
    x, y = t[i], t[i + 1]
    if sign > 0:
        k = inv(x)
        t[i], t[i + 1] = conj_fn(y, k), x
        return tuple(t), i + 1, i, k
    t[i], t[i + 1] = y, conj_fn(x, y)
    return tuple(t), i, i + 1, y


def pure_k(t, K, i, sign):
    """s_i^(2 sign) on a tuple with corners in place; K[y] transports the points over y."""
    K = list(K)
    order = [0, 1, 2, 3]                       # order[pos] = corner
    for _ in range(2):
        t, pf, pt_, k = half_move_k(t, i, sign)
        c = order[pf]
        K[c] = mul(K[c], k)                    # apply the old transport, then k
        order[i], order[i + 1] = order[i + 1], order[i]
    assert order == [0, 1, 2, 3]
    return t, tuple(K)


def straight_lift(P, j, beta):
    """P'-blocks along the straight lift of the tail arc a -> x_j from the corner (0, beta).
    Returns (blocks, sides, end corner); sides[i] is the corner crossed after blocks[i]."""
    blocks, sides = [beta], []
    side, cur = j, beta
    while True:
        nxt = P.ig[side][cur]
        if nxt == cur:
            return blocks, sides, (side, cur)
        sides.append(side)
        blocks.append(nxt)
        cur = nxt
        side = 0 if side == j else j


def rig_graph_separates(t, N, P, j, s_sheet, t_sheet):
    """Live component of phi(sigma) in Gamma_alpha'(N), alpha' the straight lift of tail
    arc j from the P'-corner of sigma. True when phi(tau) is outside it."""
    blocks, sides, end = straight_lift(P, j, P.where[s_sheet])
    live = [set(), set(), set(), set()]
    for y in range(4):
        for (i, _) in two_cycles(t[y]):
            live[y].add(N.point(y, i))
    adj = {}
    for b in nblocks_in(N, P, blocks[0]):
        u = (0, N.cid[0][b])
        cur = b
        for s in sides:
            cur = N.ig[s][cur]
        assert P.where[N.where.index(cur)] == blocks[-1]
        v = (end[0], N.cid[end[0]][cur])
        if u[1] in live[u[0]] and v[1] in live[v[0]]:
            adj.setdefault(u, set()).add(v)
            adj.setdefault(v, set()).add(u)
    start = (0, N.point(0, s_sheet))
    goal = (0, N.point(0, t_sheet))
    seen = {start}
    st = [start]
    while st:
        u = st.pop()
        for v in adj.get(u, ()):
            if v not in seen:
                seen.add(v)
                st.append(v)
    return goal not in seen


def analyse_pair(t, systems, s_sheet, t_sheet):
    n = len(t[0])
    e = tuple(range(n))
    facs = [Fac(t, w) for w in systems]
    res = dict(full=None, certB={}, flags=[])
    for Pi, P in enumerate(facs):
        if not is_pillowcase(P):
            continue
        bs, bt = P.where[s_sheet], P.where[t_sheet]
        if P.ig[0][bs] != bs or P.ig[0][bt] != bt:
            continue
        cs, ct = (0, bs), (0, bt)
        allc = corners(P)
        targets = [c for c in allc if c != cs] if cs == ct else [ct]
        mids = [(Ni, N) for Ni, N in enumerate(facs) if refines(N, P)]
        kinds = {x: set() for x in targets}
        need_rig = {}
        for x in targets:
            for Ni, N in mids:
                phis, phit = N.point(0, s_sheet), N.point(0, t_sheet)
                if cs == ct and par(N, P, phis, phit, x):
                    kinds[x].add('Par')
                if cs == ct and cut(t, N, P, phis, phit, cs, x, allc):
                    kinds[x].add('Cut')
                if phis != phit and rigid_corner(N, P, cs, x, allc):
                    need_rig.setdefault(x, []).append(Ni)
        if need_rig:
            # walk literal bases until every pending target has an arc
            pending = set(need_rig)
            K0 = (e, e, e, e)
            seen = {(t, K0)}
            queue = deque([(t, K0)])
            while queue and pending:
                tt, K = queue.popleft()
                Pc = Fac(tt, P.where)
                s_now, t_now = K[0][s_sheet], K[0][t_sheet]
                for j in (1, 2, 3):
                    _, _, end = straight_lift(Pc, j, Pc.where[s_now])
                    # name of the end corner in the base state
                    Kinv = inv(K[end[0]])
                    rep_sheet = Kinv[Pc.where.index(end[1])]
                    base_name = (end[0], P.where[rep_sheet])
                    if base_name in pending:
                        pending.discard(base_name)
                        for Ni in need_rig[base_name]:
                            Nc = Fac(tt, facs[Ni].where)
                            if rig_graph_separates(tt, Nc, Pc, j, s_now, t_now):
                                kinds[base_name].add('Rig')
                                break
                if len(seen) > STATE_CAP:
                    break
                for (i, sg) in ((0, 1), (0, -1), (1, 1), (1, -1)):
                    t2, K2 = pure_k(tt, K, i, sg)
                    if (t2, K2) not in seen:
                        seen.add((t2, K2))
                        queue.append((t2, K2))
            if pending:
                res['flags'].append('no arc found for a Rig target within the state cap')
        if P.m == 1:
            res['certB'] = {x[0]: ''.join(sorted(k[0] for k in kinds[x])) for x in targets}
            res['one_parity'] = any(
                all(par(N, P, N.point(0, s_sheet), N.point(0, t_sheet), x) for x in targets)
                for _, N in mids)
        if all(kinds[x] for x in targets) and res['full'] is None:
            res['full'] = dict(base_degree=P.m, same_corner=(cs == ct),
                               kinds=[''.join(sorted(k[0] for k in kinds[x])) for x in targets])
    return res


def main():
    for n in [int(a) for a in sys.argv[1:]]:
        t0 = time.time()
        S = Counter()
        recs = []
        for cts, o in census_orbits(n):
            t = tuple(tuple(g) for g in o['rep'])
            systems = all_block_systems(t)
            for p in o['pairs']:
                r = analyse_pair(t, systems, p['sheets_P'][0], p['sheets_Q'][0])
                lit = p['lit']
                S['pairs'] += 1
                S['LIT' if lit else 'DARK'] += 1
                ncert = sum(1 for x in (1, 2, 3) if r['certB'].get(x))
                if lit:
                    S['LIT, %d of 3 corners certified over B' % ncert] += 1
                    S['LIT with a separating parity factor'] += r['one_parity']
                    if r['full']:
                        S['LIT with a full certificate (Theorem U false)'] += 1
                else:
                    S['DARK without a separating parity factor'] += (not r['one_parity'])
                    S['DARK, certified at b, c, d over B, no separating parity factor'] += (
                        ncert == 3 and not r['one_parity'])
                    if r['full']:
                        S['DARK with a full certificate'] += 1
                        f = r['full']
                        S['DARK full: base degree %d, %s' % (
                            f['base_degree'], 'same corner' if f['same_corner'] else 'two corners')] += 1
                    else:
                        S['DARK without a full certificate'] += 1
                for fl in r['flags']:
                    S['flag: ' + fl] += 1
                recs.append(dict(rep=o['rep'], P=p['P'], Q=p['Q'], lit=lit, full=r['full'],
                                 one_parity=r['one_parity'],
                                 certB=[r['certB'].get(x, '') for x in (1, 2, 3)]))
        save_out(f'u_n{n}.json', dict(n=n, counts=dict(S), pairs=recs))
        print(n, round(time.time() - t0), 's')
        for k, v in sorted(S.items()):
            print('   ', k, v)


if __name__ == '__main__':
    main()
