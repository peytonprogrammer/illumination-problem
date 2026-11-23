"""d38 referee checks on three named rooms only (22-wall room, P6, d37 L-room). No search.

For each room: corner classes, n vs 5r, canonical partitions B_x and R_y, the quotient
data (delta, d, z) used by the d36 area bound, and the three basic arc graphs
(edges = sheets; A-vertex = g_a cycle, x-vertex = g_x cycle). For each basic graph it
checks that every regular component lies in one fibre of phi_x (d37 section 3) and
reports regular A-fibre sizes and component sizes per fibre (d37 section 7).
"""
import sys, time, resource
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU, (60, 60))
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd10-mechanisms'))
from roomtools import *  # noqa

def rigid(t, y):
    seeds = [(c[0], s) for c in cycles(t[y]) for s in c[1:]]
    return closure_partition(len(t[0]), t, seeds)

def quotient_data(t, part):
    n = len(t[0]); dq = len(part); delta = n // dq
    ig = [induced(g, part) for g in t]
    z = sum(1 for g in ig for c in cycles(g) if len(c) == 3)
    p = sum(1 for g in ig for c in cycles(g) if len(c) == 1)
    reg = [sum(1 for c in cycles(g) if len(c) == 2) for g in ig]
    return dict(blocks=dq, delta=delta, d=dq, z=z, p=p, regular_per_class=reg)

def report(label, cells, S, T, origin):
    t0 = time.process_time()
    led = ledger(cells, origin)
    room, t = room_tuple(cells, origin)
    n = len(t[0]); r = led['r']
    cls = {((x - origin[0]) % 2, (y - origin[1]) % 2) for (x, y) in led['reflex'] + led['convex']}
    print('==', label, 'n', n, 'r', r, '5r', 5 * r, 'W', led['W'], 'corner classes', sorted(cls),
          'strictly simple', is_strictly_simple(cells))
    print('  types', [cycle_type(g) for g in t])
    LS, LT = lifts(room, t, S, origin), lifts(room, t, T, origin)
    for name, x in (('b', 1), ('c', 2), ('d', 3)):
        B = class_congruence(t, [x]); R = rigid(t, x)
        qd = quotient_data(t, B)
        imS = {a_image(t, B, s[0])[0] for s in LS}; imT = {a_image(t, B, s[0])[0] for s in LT}
        bound = (qd['d'] <= 4 * qd['z'] + 1) and (qd['delta'] * qd['z'] <= r) if qd['d'] > 1 else None
        print('  B_%s' % name, qd, 'separates', not (imS & imT), 'd<=4z+1 & delta*z<=r:', bound,
              '| R_%s blocks' % name, len(R))
        # basic arc graph for class x: edges = sheets
        ca, _ = cycle_index(t[0]); cx, lx = cycle_index(t[x])
        la = {k: len(c) for k, c in enumerate(cycles(t[0]))}
        regA = {k for k, L in la.items() if L == 2}
        regX = {k for k, L in enumerate(lx) if L == 2} if isinstance(lx, list) else {k for k in lx if lx[k] == 2}
        adj = {}
        for s in range(n):
            a, y = ('A', ca[s]), ('X', cx[s])
            if ca[s] in regA and cx[s] in regX:
                adj.setdefault(a, set()).add(y); adj.setdefault(y, set()).add(a)
            else:
                adj.setdefault(a, set()); adj.setdefault(y, set())
        seen = set(); comps = []
        for v in adj:
            if v in seen or not ((v[0] == 'A' and v[1] in regA) or (v[0] == 'X' and v[1] in regX)):
                continue
            st = [v]; comp = set([v]); seen.add(v)
            while st:
                u = st.pop()
                for w in adj[u]:
                    if w not in seen:
                        seen.add(w); comp.add(w); st.append(w)
            comps.append(sorted(k for (tag, k) in comp if tag == 'A'))
        # fibre of phi_x on regular A points
        rep = {k: c[0] for k, c in enumerate(cycles(t[0]))}
        fib = {k: a_image(t, B, rep[k])[0] for k in regA}
        ok = all(len({fib[k] for k in c}) <= 1 for c in comps)
        fsize = {}
        for k, f in fib.items():
            fsize[f] = fsize.get(f, 0) + 1
        sA = {cycle_index(t[0])[0][s[0]] for s in LS} | {cycle_index(t[0])[0][s[0]] for s in LT}
        fibST = sorted({fib[k] for k in sA})
        print('    basic %s-graph: regular comps (A-vertex lists, nonempty)' % name,
              [c for c in comps if c], 'all in one fibre:', ok)
        print('    regular-A fibre sizes', dict(sorted(fsize.items())), 'fibres of mark lifts', fibST)
    print('  CPU', round(time.process_time() - t0, 4))

R22 = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1), (5, 1),
       (5, 0), (3, 0), (3, 1), (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2), (0, -2), (0, -1)]
report('22-wall', cells_from_vertices(R22), (0, 0), (2, 2), (0, 0))
Q = {(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)}
P6 = Q | {(i, -j - 1) for i, j in Q} | {(5 - i, -j - 1) for i, j in Q} | {(i, 5 - j) for i, j in Q}
report('P6 (d36 construction)', P6, (1, 0), (3, -2), (1, 0))
import json
f = json.load(open(HERE.parent / 'd31-run-dark-min' / 'found.json'))[0]
c6 = {tuple(c) for c in f['cells']}
(S6, T6, _) = f['pairs'][0]
report('P6 (found.json[0])', c6, tuple(S6), tuple(T6), tuple(S6))
L = {(i, j) for i in range(4) for j in range(2)} | {(i, j) for i in range(2) for j in range(2, 4)}
report('L-room (d37)', L, (1, 1), (3, 1), (1, 1))
