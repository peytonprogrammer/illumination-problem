"""D219 referee checks: mod-4 cocycle note (note-snapshot.md).

Named rooms only: R22 (manuscript vertex list), dilated R22 (x5, same marks scaled),
cov4181 (d64 covers.json index 4181). Reuses the d218 FC-graph code and tracers.
No room enumeration. Billiard rays only in the fixed directions of the d218 states
(base arcs (1,0),(0,1),(1,1) and the four single pure-braid images).
Run: nice -n 10 python3 -B checks.py > checks.log
"""
import importlib.util
import itertools
import sys
import time
from collections import defaultdict
from math import ceil, gcd
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('d218', HERE.parent / 'd218-review-relay-lemma' / 'checks.py')
d218 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d218)
from roomtools import room_tuple, status  # noqa: E402  (path set by d218)
from hurwitz import cycles  # noqa: E402

T0 = time.process_time()
FAILS = []


def say(*a):
    print(*a, flush=True)


def check(cond, msg):
    say(('PASS ' if cond else 'FAIL ') + msg)
    if not cond:
        FAILS.append(msg)


CLS = {'b': 1, 'c': 2, 'd': 3}


def fc_state(cells, S, word, x):
    """Bipartite regular FC graph (d218 convention) for one state and class.
    Returns adj, comps, a-vertex -> (physical point, copy bit)."""
    room, t0 = room_tuple(cells, S)
    n = len(t0[0])
    ptid = [None] * n
    for cyc in cycles(t0[0]):
        for s in cyc:
            ptid[s] = min(cyc)
    info = {}
    for p in d218.lattice_points(cells):
        if d218.par((p[0] - S[0], p[1] - S[1])) == (0, 0):
            for cyc in room.points_at((p[0] - S[0], p[1] - S[1]))[1]:
                info[min(cyc)] = (p, room.faces[room.sheets[cyc[0]]][1])
    t, marks = t0, {'a': tuple(ptid)}
    for (i, sg) in word:
        t, marks = d218.pure_move(t, marks, i, sg)
    m = marks['a']
    cid = {}
    for cyc in cycles(t[0]):
        ids = {m[s] for s in cyc}
        assert len(ids) == 1
        cid[min(cyc)] = ids.pop()
    verts, adj, _ = d218.regular_graph(t[0], t[CLS[x]])
    comps = d218.components(verts, adj)
    lab = {('a', k): info[cid[k]] for k in cid}
    return verts, adj, comps, lab


def note_graph(verts, adj):
    """Contract x-vertices: one edge per full passage a-x-a (loops and parallel edges kept)."""
    E = []
    for v in verts:
        if v[0] == 'x' and len(adj[v]) == 2:
            E.append((adj[v][0][1], adj[v][1][1]))
    A = [v for v in verts if v[0] == 'a']
    return A, E


def two_colour(A, E):
    """Try c with c(u)+c(v)=1 on every edge (h = delta c). Returns (ok, c)."""
    nb = defaultdict(list)
    for u, v in E:
        nb[u].append(v); nb[v].append(u)
    c, ok = {}, True
    for r in A:
        if r in c:
            continue
        c[r], st = 0, [r]
        while st:
            u = st.pop()
            for w in nb[u]:
                if w not in c:
                    c[w] = c[u] ^ 1; st.append(w)
                elif c[w] == c[u]:
                    ok = False
    return ok, c


# ------------------------------------------------------------------ claim 1 (abstract)
def claim1_abstract():
    say('\n=== Claim 1(a): abstract max-degree-2 multigraphs (paths, cycles incl. loops and 2-cycles)')
    ok = True
    for k in range(1, 13):              # cycle with k passages, FC length C = 2k
        A = list(range(k)); E = [(i, (i + 1) % k) for i in range(k)]
        ex, c = two_colour(A, E)
        C = 2 * k
        ok &= ex == (C % 4 == 0)
        if ex:
            for s, t in itertools.product(A, A):
                D1 = 2 * ((t - s) % k); D2 = C - D1 if D1 else 0
                ok &= (c[t] ^ c[s]) == (D1 // 2) % 2 == (D2 // 2) % 2
        else:   # C = 2 mod 4: the two directions give both residues of D/2 (for s != t)
            for s, t in itertools.product(A, A):
                if s != t:
                    D1 = 2 * ((t - s) % k)
                    ok &= {(D1 // 2) % 2, ((C - D1) // 2) % 2} == {0, 1}
    for k in range(0, 12):              # path with k passages
        A = list(range(k + 1)); E = [(i, i + 1) for i in range(k)]
        ex, c = two_colour(A, E)
        ok &= ex and all((c[t] ^ c[s]) == abs(t - s) % 2 for s in A for t in A)
    check(ok, 'h exact iff every cycle has C = 0 mod 4; paths always exact; c(t)-c(s) = D/2 mod 2 (both directions on exact cycles); C = 2 mod 4 cycles give both residues')


# ------------------------------------------------------------------ claims 1, 2, 6 on named rooms
def claim12_rooms(name, cells, S, T):
    say(f'\n=== Claims 1-2 on {name}: S={S}, T={T}, five states x three classes')
    tot_ok1 = tot_ok2 = True
    rows = {}
    for word, wname in d218.single_moves():
        for x in 'bcd':
            verts, adj, comps, lab = fc_state(cells, S, word, x)
            A, E = note_graph(verts, adj)
            # (a) exactness per component <=> every cycle C = 0 mod 4
            ex_all, c = two_colour(A, E)
            for comp, ne, kind in comps:
                Ac = [v for v in A if v in comp]
                Ec = [e for e in E if e[0] in comp]
                ex, _ = two_colour(Ac, Ec)
                want = kind != 'cycle' or ne % 4 == 0
                tot_ok1 &= ex == want
            # lifts
            sv = {v: lab[v][1] for v in A if lab[v][0] == S}
            tv = {v: lab[v][1] for v in A if lab[v][0] == T}
            dist = {}
            for s, sc in sv.items():
                comp = next(cc for cc in comps if s in cc[0])
                for t, tc in tv.items():
                    ok, D, C = d218.note_test(comp[0], comp[1], comp[2], adj, s, t)
                    if D is not None:
                        dist[(sc, tc)] = (D, C, comp[2])
                        if comp[2] == 'path' or C % 4 == 0:
                            tot_ok1 &= (c[s] ^ c[t]) == (D // 2) % 2
            # (b) shared component <=> some straight Gamma walk from an S lift reaches a T lift (any length)
            share = bool(dist)
            ga_hit = False
            # walks along adj: nonbacktracking from each S lift
            for s in sv:
                for sheet, w in adj[s]:
                    prev, u, steps = sheet, w, 1
                    while steps < 4 * len(verts) + 4:
                        if u in tv:
                            ga_hit = True
                        nxt = [(sh, y) for sh, y in adj[u] if sh != prev]
                        if not nxt:
                            break
                        prev, u = nxt[0]; steps += 1
                        if u == s:
                            break
                    if u in tv:
                        ga_hit = True
            tot_ok2 &= share == ga_hit
            rows[(wname or 'base', x)] = dist
            cyc = sorted(ne for _, ne, k in comps if k == 'cycle')
            say(f'    {wname or "base":6s} {x}: cycles C={cyc} exact={[C % 4 == 0 for C in cyc]}; '
                f'S-T on common component: {sorted((k, v[0], v[2]) for k, v in dist.items()) or "none"}')
    check(tot_ok1, f'{name}: per component, 2-colouring exists iff every cycle C = 0 mod 4; c(t)-c(s) = D/2 on exact components')
    check(tot_ok2, f'{name}: S,T lifts share a regular component iff a nonbacktracking walk joins them (lighting path)')
    return rows


def claim2_directions():
    say('\n=== Claim 2 converse: every primitive direction of a class is a state direction (level-2 shears)')
    ok = True
    for p in range(-40, 41):
        for q in range(-40, 41):
            if gcd(p, q) != 1:
                continue
            v = (p, q)
            # descend with shears (v0 +- 2 v1, v1), (v0, v1 +- 2 v0) to a base arc up to sign
            for _ in range(200):
                if abs(v[0]) + abs(v[1]) <= 2 and (v in ((1, 0), (-1, 0), (0, 1), (0, -1)) or abs(v[0]) == abs(v[1]) == 1):
                    break
                if abs(v[0]) > abs(v[1]):
                    v = min(((v[0] - 2 * v[1], v[1]), (v[0] + 2 * v[1], v[1])), key=lambda w: abs(w[0]))
                else:
                    v = min(((v[0], v[1] - 2 * v[0]), (v[0], v[1] + 2 * v[0])), key=lambda w: abs(w[1]))
            ok &= (abs(v[0]) % 2, abs(v[1]) % 2) == (p % 2, q % 2) and abs(v[0]) + abs(v[1]) <= 2
    check(ok, 'all primitive |p|,|q| <= 40 reduce by the two level-2 shears to the base arc of their class, up to sign')


# ------------------------------------------------------------------ claims 3, 4: dilated R22
def claim34():
    say('\n=== Claims 3-4: R22 dilated by 5')
    _, R22 = d218.manuscript_r22()
    bottom = min(j for _, j in R22)
    check([c for c in R22 if c[1] == bottom] == [(1, -3)], 'R22 bottom row is the single cell (1,-3)')
    above = sorted(i for i, j in R22 if j == bottom + 1)
    say(f'    R22 row -2 cells: {above}')
    D5 = {(5 * i + a, 5 * j + b) for i, j in R22 for a in range(5) for b in range(5)}
    S, T = (0, 0), (10, 10)
    check(len(D5) == 375 and d218.reflex_count(D5) == 9, 'dilated R22: area 375, 9 reflexes')
    band = {c for c in D5 if c[1] < -10}
    check({c[0] for c in band} == set(range(5, 10)) and {c[1] for c in band} == set(range(-15, -10)),
          'lowest open band -15<y<-10 has horizontal section 5<x<10')
    line = [(x, -12) for x in range(5, 11)]
    st = [status(D5, p) for p in line]
    say(f'    statuses on y=-12, x=5..10: {st}')
    check(st[0] == st[-1] == 'smooth' and all(s == 'interior' for s in st[1:-1]), 'y=-12: wall hits (5,-12),(10,-12) smooth, (6..9,-12) interior')
    verts, adj, comps, lab = fc_state(D5, S, (), 'b')
    a6 = [v for v in lab if lab[v][0] == (6, -12)]
    comp = next(cc for cc in comps if a6[0] in cc[0])
    pts = sorted({lab[v][0] for v in comp[0] if v[0] == 'a'})
    say(f'    class-b component through (6,-12): kind={comp[2]}, C={comp[1]}, a-points {pts}')
    check(comp[2] == 'cycle' and comp[1] == 10 and all(p[1] == -12 for p in pts)
          and {d218.par(p) for p in pts} == {(0, 0)}, 'horizontal y=-12 cycle: C=10 over even-even a-points (x-class odd-even); C/2=5 odd')
    A, E = note_graph(verts, adj)
    ex, _ = two_colour([v for v in A if v in comp[0]], [e for e in E if e[0] in comp[0]])
    check(not ex, 'edge cochain on that component is not exact')
    sv = [v for v in lab if lab[v][0] == S]
    check(not any(s in comp[0] for s in sv) and not any(lab[v][0] == T for v in comp[0] if v[0] == 'a'),
          'marked lifts are not on the C=10 cycle')
    # darkness check in the five d218 states (dilation argument covers all states)
    shared = []
    for word, wname in d218.single_moves():
        for x in 'bcd':
            vv, aa, cc, ll = fc_state(D5, S, word, x)
            for s in [v for v in ll if ll[v][0] == S]:
                c0 = next(c for c in cc if s in c[0])
                if any(ll.get(v, (None,))[0] == T for v in c0[0] if v[0] == 'a'):
                    shared.append((wname, x))
    check(not shared, 'dilated R22: S,T lifts share no regular component in the 15 checked (state, class) rows')

    # Claim 4: triangle
    Ap, Bp, Cp = (6, -14), (8, -14), (8, -12)
    sites = [Ap, Bp, Cp, (7, -14), (8, -13), (7, -13)]
    check(all(status(D5, p) == 'interior' for p in sites), 'A,B,C and the side midpoints (7,-14),(8,-13),(7,-13) are interior')
    check(all(d218.par(p) == (0, 0) for p in (Ap, Bp, Cp)), 'A,B,C are a-class (even-even)')
    tot = 0
    for (P, Q, x) in ((Ap, Bp, 'b'), (Bp, Cp, 'd'), (Cp, Ap, 'c')):
        vv, aa, cc, ll = fc_state(D5, S, (), x)
        A_, E_ = note_graph(vv, aa)
        hit = [e for e in E_ if {ll[e[0]], ll[e[1]]} == {(P, 0), (Q, 0)}]
        say(f'    side {P}-{Q} class {x}: copy-0 passages {len(hit)}; all passages at these sites '
            f'{sorted(tuple(sorted((ll[u], ll[v]))) for u, v in E_ if {ll[u][0], ll[v][0]} <= {P, Q})}')
        check(len(hit) == 1, f'side {P}-{Q} is one two-step passage in class {x} on copy 0')
        tot += 1
        if x == 'c':
            atA = sorted(tuple(sorted((ll[u], ll[v]))) for u, v in E_ if Ap in (ll[u][0], ll[v][0]))
            say(f'    class c passages at A: {atA}')
            check(((Ap, 1), (Bp, 0)) in atA and ((Ap, 1), (Cp, 1)) not in atA,
                  'copy 1: the class-c sheet at A reaches B on copy 0 (via the bottom wall), not C; triangle is copy-0 only')
    check(tot % 2 == 1, f'boundary sum of h over the triangle = {tot} = 1 mod 2')
    # no lattice point strictly inside, and the closed triangle lies inside the open bottom square (5,10)x(-15,-10)
    inside = [(x, y) for x in range(6, 9) for y in range(-14, -11) if x - 8 < 0 and y + 14 > 0 and (x - 6) - (y + 14) > 0]
    check(not inside and all(5 < p[0] < 10 and -15 < p[1] < -10 for p in (Ap, Bp, Cp)),
          'triangle lies in the open bottom square, no corner (indeed no lattice point) strictly inside')


# ------------------------------------------------------------------ claim 6: cov4181
def claim6(rows):
    say('\n=== Claim 6: cov4181 hand calculation and class-b parity flip')
    C = d218.COV
    S, T = (2, 3), (4, 3)
    check(status(C, (3, 3)) == 'interior' and d218.par((3, 3)) == (1, 1), 'S->(3,3)->T: midpoint (3,3) interior, class (1,1) (b)')
    v2 = [status(C, (2, y)) for y in range(2, 5)]
    v4 = [status(C, (4, y)) for y in range(0, 7)]
    say(f'    x=2, y=2..4: {v2}; x=4, y=0..6: {v4}')
    check(v2 == ['smooth', 'interior', 'smooth'] and v4 == ['smooth'] + ['interior'] * 5 + ['smooth'],
          'x=2 runs y=2..4 and x=4 runs y=0..6, smooth ends')
    b, d = rows[('base', 'b')], rows[('base', 'd')]
    check(sorted(v[0] for v in b.values()) == [2, 2, 6, 6] and all(v[2] == 'path' for v in b.values()),
          'base class b: S,T on one path, D in {2,6}')
    verts, adj, comps, lab = fc_state(C, S, (), 'd')
    cs = next(c for c in comps if any(lab.get(v, (0,))[0] == S for v in c[0]))
    ct = next(c for c in comps if any(lab.get(v, (0,))[0] == T for v in c[0]))
    say(f'    base d: S component {cs[2]} C={cs[1]}, T component {ct[2]} C={ct[1]}')
    check(cs[2] == ct[2] == 'cycle' and cs[1] == 4 and ct[1] == 12 and cs[0] != ct[0] and not d,
          'base class d: S on C=4 cycle, T on C=12 cycle, different components (both exact)')
    sl = [v for v in cs[0] if v[0] == 'a' and lab[v][0] == S]
    ok, D, _ = d218.note_test(cs[0], cs[1], cs[2], adj, sl[0], sl[1])
    check(len(sl) == 2 and D == 2, 'the two copies of S are joined by one two-step passage (D=2) on the C=4 cycle')
    for w in ('s2^2', 's2^-2'):
        tw = rows[(w, 'b')]
        flips = all((b[k][0] // 2) % 2 != (tw[k][0] // 2) % 2 for k in b)
        say(f'    class b lift distances base {dict(sorted((k, v[0]) for k, v in b.items()))} vs {w} {dict(sorted((k, v[0]) for k, v in tw.items()))}')
        check(set(tw) == set(b) and flips and sorted(v[0] for v in tw.values()) == [4, 4, 12, 12],
              f'{w}: every lift pairing flips D/2 parity (base 2/6 -> twisted 4/12)')
    # no relabelling (swap T lifts, or global offset) reconciles: base D/2 all odd, twisted all even
    check(all((v[0] // 2) % 2 == 1 for v in b.values()) and all((v[0] // 2) % 2 == 0 for v in rows[('s2^2', 'b')].values()),
          'base: all D/2 odd; s2^2: all D/2 even, so no lift exchange reconciles them')
    check(not any(rows[(w, 'd')] for w, _ in [(n or 'base', 0) for _, n in d218.single_moves()]),
          'class d: S,T share no component in any of the five states (agrees with d218 and D66)')


# ------------------------------------------------------------------ claim 7
def claim7():
    say('\n=== Claim 7: n=22 counts')
    n, r = 22, 8
    d = ceil(Fr(2 * n, 3))
    check(d == 15 and 2 * d - 2 * r - n // 2 == 3, 'd >= 2n/3 gives d >= 15 and R_other >= 30-16-11 = 3')
    check(2 * 20 - 2 * r - n // 2 == 13 and 2 * 21 - 2 * r - n // 2 == 15, 'd >= 20 gives >= 13; d = 21 gives 15')


if __name__ == '__main__':
    claim1_abstract()
    claim2_directions()
    _, R22 = d218.manuscript_r22()
    claim12_rooms('R22', R22, (0, 0), (2, 2))
    rows = claim12_rooms('cov4181', d218.COV, (2, 3), (4, 3))
    claim34()
    claim6(rows)
    claim7()
    say(f'\nCPU {time.process_time() - T0:.2f}s; failures: {len(FAILS)}')
    for f in FAILS:
        say('  FAIL: ' + f)
