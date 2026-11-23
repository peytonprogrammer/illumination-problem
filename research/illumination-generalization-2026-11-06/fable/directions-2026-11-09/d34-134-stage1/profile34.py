"""Profile of a (1,3,4) room and the conditions of ../d32-fold-minimum/astra-r3.md.
Angles are in units of pi/8: A = 1, B = 3, C = 4 per tile."""
CEIL = {17: 40, 18: 42, 19: 44, 20: 48, 21: 50}
W18_BIG = {(16, (1,), 1, 0, 2, 1, 41), (16, (1, 1), 0, 0, 2, 1, 42), (17, (2,), 0, 0, 2, 1, 42)}


def profile(room):
    ang = room.tri.ang
    nu = [0] * 6
    A, I, f = [], 0, 0
    C = [0] * 5  # C[j] = C points with j tiles: 1 convex, 2 flat, 3 reflex, 4 interior
    for p, l in room.vlabel.items():
        j = room.vang[p] // ang[l]
        if l == 'B':
            nu[j] += 1
        elif l == 'A':
            if p not in room.bset:
                I += 1
            elif j == 8:
                f += 1
            else:
                A.append(j)
        else:
            C[j] += 1
    be = {}
    for (a, b), lst in room.edges.items():
        if len(lst) == 1:
            t = ''.join(sorted(room.vlabel[a] + room.vlabel[b]))
            be[t] = be.get(t, 0) + 1
    return {'W': room.W, 'F': len(room.tiles), 'b': sum(nu), 'nu': nu[1:], 'A': sorted(A), 'p': C[1], 's': C[2],
            'm': C[3], 't': C[4], 'I': I, 'f': f, 'bdry_edges': be}


def check(pr):
    W, F, b, nu, A, p, s, m, t, I, f = (pr[x] for x in 'W F b nu A p s m t I f'.split())
    nu = [0] + nu
    a, K = len(A), sum(A)
    e = []
    if W < 17: e.append('W<17')
    if F > CEIL.get(W, 99): e.append('F above ceiling')
    if F != 16 * I + 8 * f + K: e.append('F != 16I+8f+K')
    if W != b + a + p + m: e.append('W != b+a+p+m')
    if K + p + 3 * m + 12 * I + 6 * f != 2 * W - 4: e.append('boxed identity')
    if any(x < 1 or x > 15 or x == 8 for x in A): e.append('A fan range')
    if b < 16: e.append('b<16')
    if nu[1] > b - 16: e.append('nu1>b-16')
    if sum((j // 2) * nu[j] for j in range(1, 6)) < 8 * I: e.append('BA spokes')
    if I == 3 and (b < 20 or (b == 20 and (nu[1] or nu[4] + nu[5] < 4))): e.append('I=3 B tips')
    if F != p + 3 * m + 2 * s + 4 * t: e.append('C incidences')
    if F != 2 * (I + t) + W + f + s - 2: e.append('Euler')
    if s + t + m < 16: e.append('C tips')
    oA = sum(x % 2 for x in A)
    oB = nu[1] + nu[3] + nu[5]
    c = p + m
    x = b + a + f - c - s
    if not (oA <= x <= 2 * (a + f) - oA and oB <= x <= 2 * b - oB): e.append('x range')
    if len({x % 2, oA % 2, oB % 2, c % 2}) != 1: e.append('parity')
    if not (c <= 2 * (a + f) - x <= c + 2 * s and c <= 2 * b - x <= c + 2 * s): e.append('AC/BC range')
    be = pr['bdry_edges']
    if (be.get('AB', 0), be.get('AC', 0), be.get('BC', 0)) != (x, 2 * (a + f) - x, 2 * b - x): e.append('edge counts')
    if W == 18 and F > 40 and (b, tuple(A), p, m, I, f, F) not in W18_BIG: e.append('not in W18 F>40 families')
    return e
