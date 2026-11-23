#!/usr/bin/env python3
"""Face structure of one direction on the room, and full cylinders.

In cell (a, b) a face is a pair (i, j): plus strip i and minus strip j whose
intersection meets the open cell. For p, q >= 1 the open diamond
{i < qx - py < i+1, j < qx + py < j+1} is, in coordinates s = 2qx, d = 2py,
the open L1-ball of radius 1 around the integer point (i+j+1, j-i). It meets
the open rectangle (2qa, 2q(a+1)) x (2pb, 2p(b+1)) iff the centre lies in the
closed rectangle (integer corners, side lengths >= 2).
"""


def faces(a, b, p, q):
    k0 = q * a - p * b
    m0 = q * a + p * b
    if p == 0 or q == 0:
        # both families are the same axis-parallel strips; one strip per cell
        for i in range(k0 - p, k0 + q):
            for j in range(m0, m0 + p + q):
                yield i, j
        return
    for i in range(k0 - p, k0 + q):
        for j in range(m0, m0 + p + q):
            c1, c2 = i + j + 1, j - i
            if 2 * q * a <= c1 <= 2 * q * (a + 1) and 2 * p * b <= c2 <= 2 * p * (b + 1):
                yield i, j


def full_cylinders(L, cells):
    """full[D] is True iff the closure of DP cylinder D projects onto the room:
    every open face of every cell has its plus or its minus label equal to D
    (closures of finitely many closed strips cover a dense set, hence all)."""
    p, q = L.p, L.q
    out = []
    for D in range(L.ncyl):
        out.append(all(L.plus[c][i] == D or L.minus[c][j] == D
                       for c in cells for (i, j) in faces(c[0], c[1], p, q)))
    return out
