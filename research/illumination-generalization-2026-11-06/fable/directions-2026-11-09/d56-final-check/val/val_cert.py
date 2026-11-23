"""Cross-check the C certificate code (check.c, CHECK_DEBUG=1) against the Python reference.

Reference: ../../d10-mechanisms roomtools (pillowcase tuple, closure partitions, mark points),
unified_test.Factor / par / cut, d4.all_block_systems for Cut (all 2- and 3-block factors), and a
live-graph Rig written from unified_test.Factor.live_component, extended to a target over x
(d48 item 2 step 4).  The cert room is the original room scaled by (a, b) (d47 Prop 2.1).

usage: python3 -B val_cert.py DEBUGFILE [MAXGROUPS]
Compares, per (room, pair, lattice) group and per target, the sorted list of certificate bits
over the 4 lift pairs.
"""
import sys
import random
import resource
from collections import defaultdict
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU, (900, 900))
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / 'd10-mechanisms'))
from roomtools import room_tuple, closure_partition, cycles, class_congruence, ledger, OFFS  # noqa
from unified_test import Factor, par, cut  # noqa
import d4_monodromy as d4  # noqa


RIGTESTED = [0]


def rig_x(F, x, s, q, qc):
    if not any(all(L == 1 for L in F.nlen[y]) for y in (1, 2, 3) if y != x):
        return False
    st = F.ncid[0][F.where[s]]
    tg = ('a', F.ncid[0][F.where[q]]) if qc == 0 else ('x', F.ncid[x][F.where[q]])
    if not F.live[0][st]:
        return tg != ('a', st)
    adj = defaultdict(set)
    for b in range(F.m):
        u, v = ('a', F.ncid[0][b]), ('x', F.ncid[x][b])
        if F.live[0][u[1]] and F.live[x][v[1]]:
            adj[u].add(v); adj[v].add(u)
    seen = {('a', st)}; stack = [('a', st)]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v); stack.append(v)
    return tg not in seen


def ref_bits(cells, S, T):
    room, t = room_tuple(cells, S)
    n = len(t[0])
    r = ledger(cells, S)['r']
    cs, pS = room.points_at((0, 0))
    ct, pT = room.points_at((T[0] - S[0], T[1] - S[1]))
    assert tuple(cs) == (0, 0)
    xt = OFFS[tuple(ct)]
    LS = [c[0] for c in pS if len(c) == 2]
    LT = [c[0] for c in pT if len(c) == 2]
    assert len(LS) == 2 and len(LT) == 2
    Bx = {x: Factor(t, class_congruence(t, [x])) for x in (1, 2, 3)}
    Ry = {y: Factor(t, closure_partition(n, t, [(c[0], s) for c in cycles(t[y]) for s in c[1:]])) for y in (1, 2, 3)}
    vonly = {x: not any(len(c) == 2 for c in cycles(t[x])) for x in (1, 2, 3)}
    small = None
    if any(Ry[y].m >= 2 for y in (1, 2, 3)):
        RIGTESTED[0] += 1
    out = {}
    for x in (1, 2, 3):
        if xt and x != xt:
            continue
        bits = []
        for s in LS:
            for q in LT:
                b = 0
                if xt == 0 and Bx[x].m >= 2 and par(Bx[x], x, s, q):
                    b |= 1
                for y in (1, 2, 3):
                    if y != x and Ry[y].m >= 2 and rig_x(Ry[y], x, s, q, xt and x):
                        b |= 2
                if xt == 0 and (n <= 3 * r or (n <= 4 * r + 4 and vonly[x])):
                    if small is None:
                        small = [Factor(t, p) for p in d4.all_block_systems(list(t), n) if len(p) in (2, 3)]
                    if any(cut(F, t, x, s, q) for F in small):
                        b |= 4
                bits.append(b)
        out[x] = sorted(bits)
    return out


if __name__ == '__main__':
    # debug lines are preceded by "ROOMLINE area W cells" lines written by the driver below
    cur = None
    groups = {}
    for line in open(sys.argv[1]):
        if line.startswith('ROOMLINE'):
            v = list(map(int, line.split()[1:]))
            cur = (v[0], tuple(zip(v[2::2], v[3::2])))
            continue
        if not line.startswith('CERTDBG'):
            continue
        head, ab, lp = line.rstrip('\n').split(' | ')
        f = ab.split(); g = lp.split()
        key = (cur, head, int(f[1]), int(f[2]), (int(f[5]), int(f[6])), (int(f[8]), int(f[9])))
        groups.setdefault(key, defaultdict(list))[int(g[4])].append(int(g[6]))
    keys = list(groups)
    random.seed(1)
    if len(sys.argv) > 2 and len(keys) > int(sys.argv[2]):
        keys = random.sample(keys, int(sys.argv[2]))
    agree = dis = 0
    nonzero = defaultdict(int)
    for key in keys:
        (area, cells0), head, a, b, S, T = key
        cells = {(a * i + u, b * j + v) for (i, j) in cells0 for u in range(a) for v in range(b)}
        ref = ref_bits(cells, S, T)
        got = {x: sorted(v) for x, v in groups[key].items()}
        if ref == got:
            agree += 1
        else:
            dis += 1
            print('DISAGREE', key, 'C', got, 'ref', ref)
        for x, v in ref.items():
            for bb in v:
                for k, nm in ((1, 'Par'), (2, 'Rig'), (4, 'Cut')):
                    if bb & k:
                        nonzero[nm] += 1
    print('groups compared', len(keys), 'agree', agree, 'disagree', dis,
          'reference certificate instances by kind', dict(nonzero),
          'groups with a nontrivial R_y (Rig evaluated)', RIGTESTED[0])
