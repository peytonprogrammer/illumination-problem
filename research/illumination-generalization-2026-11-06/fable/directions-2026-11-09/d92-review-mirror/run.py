"""d92 review computations. Usage: python3 -B run.py r22 | cross7 | cross9"""
import json
import math
import os
import sys
import time
from surf import Room, full_group, check_affine, orbit_pairs, compose, inv, act_T, act_R, iso, vertex_map

HERE = os.path.dirname(os.path.abspath(__file__))
t0 = time.process_time()


def cross(b):
    cells = set()
    for x in range(-b, b):
        for y in range(-2, 2):
            cells.add((x, y))
            cells.add((y, x))
    return sorted(cells)


def r22():
    rooms = json.load(open(os.path.join(HERE, '..', 'd8-perturbation-test', 'rooms.json')))
    r = rooms[0]
    assert r['id'] == 'R22-base'
    return r['cells'], [tuple(m) for m in r['marks']]


def walls(room):
    # count boundary corners
    pts = {(x + a, y + b) for (x, y) in room.cells for a in (0, 1) for b in (0, 1)}
    cv = sum(room.ncell(P) == 1 for P in pts)
    rf = sum(room.ncell(P) == 3 for P in pts)
    return cv, rf


def lit_from(room, w, L):
    """M vertices reached by a legal straight segment from regular vertex w with
    developed direction primitive (a,b), |(a,b)| <= L (any number of steps)."""
    lit = set()
    for a in range(-L, L + 1):
        for b in range(-L, L + 1):
            if (a, b) != (0, 0) and math.gcd(a, b) == 1 and a * a + b * b <= L * L:
                lit.update(room.ray(w, a, b))
    return lit


def qhidden(room, w, L):
    """Q lattice points (tau classes, regular, not forbidden) hidden from Q point
    of w, up to length-L directions, source excluded."""
    lit = set(room.qclass(x) for x in lit_from(room, w, L))
    lit |= set(room.qclass(x) for x in lit_from(room, room.vtau[w], L))
    allq = {room.qclass(x) for x in range(room.V) if not room.forbidden[x]}
    return allq - lit - {room.qclass(w)}


def name(room, x):
    e = sorted(room.vsheets[x])
    return f"{room.vphys[x]}{'w' if len(e) > 1 else ''}[{','.join('%+d%+d' % s for s in e)}]"


def analyse(room, gens, marks, log):
    I = room.viota
    qc = room.qclass
    res = {}
    for P in marks:
        s = room.vert((1, 1), P)
        orb = orbit_pairs(gens, (s, I[s]))
        qs = qc(s)
        Gs = {qc(a) for a, _ in orb}
        e = {qc(b) for a, b in orb if qc(a) == qs}
        e2 = {qc(b) for a, b in orb if qc(a) == qc(I[s])}  # lift-independence check
        log(f'  S={P}: |G.s|={len(Gs)}  e(S)=|G_s.iota s|={len(e)}  (other lift: {len(e2)})' + (f'  set={sorted(name(room, x) for x in e)}' if len(e) <= 6 else ''))
        res[P] = (s, e, len(Gs))
    return res


def kernel(room, auts, log):
    # K on Q: tau-compatible automorphisms mod tau; physical description
    desc = set()
    for f in auts:
        # physical action on vertex positions of sheet (1,1) points
        sample = [w for w in range(room.V) if not room.forbidden[w]][:6]
        desc.add(tuple((room.vphys[w], room.vphys[f[w]], tuple(sorted(room.vsheets[f[w]]))) for w in sample[:2]))
    log(f'  |Aut_tau(M)| = {len(auts)} -> |K| = {len(auts)} on Q (derivative +-I lifts: Aut and tau*Aut)')


def parabolic(room, word, n_max, log):
    """Find an affine map with derivative W T^n W^-1 for the smallest n>=1, word
    W given as a string over 'TR' applied right-to-left to the base."""
    mark = [1 if c else 0 for c in room.convex]
    base = (room.h, room.v, room.tau, room.p0)
    # X = W^{-1} M; find the smallest n with T^n X ~ X (marks and tau kept).
    X = base
    def act_Tinv(s):
        h, v, t, p = s
        return (h, [v[h[k]] for k in range(len(h))], [inv(h)[t[k]] for k in range(len(h))], p)
    for ch in word:  # W = w1 w2 ... ; W^{-1} = ... w2^-1 w1^-1 ; apply w1^-1 first
        X = act_Tinv(X) if ch == 'T' else act_R(act_R(act_R(X)))
    Y = X
    cand = [k for k in range(room.N) if mark[X[3][k]]]
    for n in range(1, n_max + 1):
        Y = act_T(Y)
        sig = iso(Y, X, mark, cand[0], [k for k in range(room.N) if mark[Y[3][k]]])
        if sig is not None:
            return n, vertex_map(room, Y, X, sig)
    return None, None


def period(f, x, qc):
    y = f[x]
    n = 1
    while qc(y) != qc(x):
        y = f[y]
        n += 1
    return n


def main(which):
    out = []
    log = lambda s: (print(s), out.append(s))
    if which == 'r22':
        cells, (S, T) = r22()
        room = Room(cells)
        marks = [S, T, (1, 0), (0, 1), (2, 1), (1, 2), (3, 1), (1, -1), (1, -2)]
    else:
        b = int(which[5:])
        cells = cross(b)
        room = Room(cells)
        S, T = (6, 0), (0, 6)
        marks = [(6, 0), (0, 6), (5, 1), (6, 1), (3, 1), (1, 1), (4, 1), (2, 1), (b - 1, 1), (0, 0), (1, 0)]
    cv, rf = walls(room)
    log(f'== {which}: area {len(room.cells)}, walls {cv + rf} (convex {cv}, reflex {rf}); M: {room.N} squares, {room.V} vertices')
    gens, auts, idx = full_group(room, log)
    for f in gens:
        check_affine(room, f)
    log(f'  all {len(gens)} maps preserve corners and commute with tau; cpu {time.process_time() - t0:.1f}s')
    kernel(room, auts, log)
    res = analyse(room, gens, marks, log)
    qc = room.qclass
    I = room.viota
    log(f'  cpu {time.process_time() - t0:.1f}s')
    # Claim 2: parabolic F and mirror conjugate F* = iota F iota
    for word in ['', 'R', 'T', 'TR', 'TT', 'RT', 'TTR', 'RTT']:
        n, F = parabolic(room, word, 400, log)
        if F is None:
            log(f'  parabolic W={word!r}: none up to n=400')
            continue
        Fs = compose(I, compose(F, I))
        row = []
        for P in marks:
            s = res[P][0]
            u, v = period(F, s, qc), period(Fs, s, qc)
            # check period_F(iota s) = v
            assert period(F, I[s], qc) == v
            r = max(u, v) // math.gcd(u, v)
            assert r <= len(res[P][1]), (P, u, v, len(res[P][1]))
            row.append(f'{P}:u={u},v={v},ratio={r}')
        log(f'  parabolic W={word!r} n={n}: ' + '; '.join(row))
    log(f'  claim-2 ratios all <= exact e(S): checked; cpu {time.process_time() - t0:.1f}s')
    if which == 'r22':
        L = 30
        s, t = room.vert((1, 1), S), room.vert((1, 1), T)
        Hs = qhidden(room, s, L)
        Ht = qhidden(room, t, L)
        log(f'  hidden Q lattice points from s=(0,0) (|dir|<={L}): {sorted(name(room, x) for x in Hs)}')
        log(f'  hidden Q lattice points from t=(2,2) (|dir|<={L}): {sorted(name(room, x) for x in Ht)}')
        # G_s orbit of t lifts must be hidden from s
        gens_q = gens
        for a0, b0 in [(s, t), (s, I[t]), (t, s), (t, I[s])]:
            orb = orbit_pairs(gens_q, (a0, b0))
            img = {qc(b) for a, b in orb if qc(a) == qc(a0)}
            H = Hs if a0 == s else Ht
            log(f'  G_{name(room, a0)} . {name(room, b0)} = {sorted(name(room, x) for x in img)}; subset of hidden: {img <= H}')
        # the bipartite graph of claim 1, built exactly
        E = set()
        for a0 in (s, I[s]):
            for b0 in (t, I[t]):
                for a, b2 in orbit_pairs(gens, (a0, b0)):
                    E.add((qc(a), qc(b2)))
        left = {a for a, _ in E}
        right = {b2 for _, b2 in E}
        degL = {x: sum(1 for a, _ in E if a == x) for x in left}
        degR = {y: sum(1 for _, b2 in E if b2 == y) for y in right}
        walks = sum(degR[y] - 1 for (a, y) in E if a == qc(s))
        eS = len(res[S][1])
        eT = len(res[T][1])
        log(f'  graph: |left|={len(left)} |right|={len(right)} |E|={len(E)} max degL={max(degL.values())} max degR={max(degR.values())}')
        log(f'  walks of length 2 from s to other left vertices = {walks}; 2e(S) = {2 * eS}; |H(s)|(|H(t)|-1) = {len(Hs) * (len(Ht) - 1)}')
        log(f'  e(S)={eS}, e(T)={eT}; check 2e(S) <= |H(s)|(|H(s)|-1) [B replaced by observed max hidden count {max(len(Hs), len(Ht))}]: '
            f'{2 * eS} <= {max(len(Hs), len(Ht)) * (max(len(Hs), len(Ht)) - 1)}')
    log(f'  total cpu {time.process_time() - t0:.1f}s')
    open(os.path.join(HERE, f'{which}.log'), 'w').write('\n'.join(out) + '\n')


if __name__ == '__main__':
    main(sys.argv[1])
