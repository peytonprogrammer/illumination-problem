"""Instances of the 10 door pairs in the canonical Lemma H frame (exact)."""
import json
from fractions import Fraction as Fr
from exact import RRoom, canonical
import newlemmas as nl
from door_geom import DOOR, far_end

ROWS = {r['mask']: r for r in json.load(open('../d57-witness-mining-r3/tools/cert_r3.json'))}


def config(mask, S, T):
    """Canonical frame with the viewer left of the door. Returns (cells, nx, ny, cfg, viewer, corr)."""
    r = ROWS[mask]
    for sym in nl.SYMS:
        nx, ny, cells, g = canonical(r['nx'], r['ny'], mask, sym)
        o = g.tr(sym)
        for A, B in ((S, T), (T, S)):
            a, b = g.tp(sym, A), g.tp(sym, B)
            for cfg in nl.H_configs(o, a, b):
                if a[0] < cfg[2]:
                    return nx, ny, cells, cfg, a, b, sym, o
    raise ValueError


def instance(mask, S, T, L, w, pi, u, D, h, beta, ell, other=Fr(1), fh=None):
    """Real room + geo with channel length L, door width w at offset pi from a,
    viewer offset u from a, viewer depth D below the door line, T at height h
    above it with relative position beta, corridor length ell."""
    nx, ny, cells, (a, b, p, q, d), V, C, sym, o = config(mask, S, T)
    assert q - p == 2 and V[0] % 2 == 1 and V[0] < p and C[0] == p + 1
    gx = [other] * nx
    left = list(range(a // 2, p // 2))          # channel columns left of the door
    right = list(range(q // 2, b // 2))
    iv = V[0] // 2
    e = pi / (8 * len(left))
    for c in left: gx[c] = e
    gx[iv] = pi - e * (len(left) - 1)
    fvx = (u - e * (iv - a // 2)) / gx[iv]
    assert 0 < fvx < 1, fvx
    gx[p // 2] = w
    if right:
        for c in right: gx[c] = (L - pi - w) / len(right)
    else: assert L == pi + w
    # y: rows between viewer and door, corridor rows
    gy = [other] * ny
    e_ = far_end(o, p, q, C)[0]
    assert far_end(o, p, q, C)[1] == 'dead-end'
    crow = list(range(d // 2, e_ // 2))
    for c in crow: gy[c] = ell / len(crow)
    nr = len(crow)
    if h is None:
        h = ell / nr * ((C[1] // 2 - d // 2) + (fh if C[1] % 2 else 0))
    if C[1] % 2 == 1:
        jt = C[1] // 2
        fty = (h - (ell / len(crow)) * (jt - d // 2)) / gy[jt]
        assert 0 < fty < 1, fty
    else:
        fty = None
        assert h == (ell / len(crow)) * (C[1] // 2 - d // 2), (h, ell)
    vrows = list(range((V[1]) // 2, d // 2))
    if V[1] % 2 == 1:
        jv = V[1] // 2
        for c in vrows: gy[c] = D / (2 * len(vrows))
        gy[jv] = D - (D / (2 * len(vrows))) * (len(vrows) - 1) + D / 2   # viewer row taller
        fvy = 1 - (D - sum(gy[c] for c in vrows if c != jv)) / gy[jv]
        assert 0 < fvy < 1
    else:
        for c in vrows: gy[c] = D / len(vrows)
        fvy = None
    room = RRoom(nx, ny, cells, gx, gy)
    sv = (room.coord(V[0], 0, fvx), room.coord(V[1], 1, fvy))
    tc = (room.xs[p // 2] + beta * w, room.coord(C[1], 1, fty))
    A_, B_ = room.xs[a // 2], room.xs[b // 2]
    P_, Q_, D_ = room.xs[p // 2], room.xs[q // 2], room.ys[d // 2]
    geo = (A_, B_, P_, Q_, D_, sv, tc)
    assert B_ - A_ == L and Q_ - P_ == w and D_ - sv[1] == D and tc[1] - D_ == h, geo
    # back wall of the viewer's channel (if the channel continues below with one run)
    return room, geo, dict(cfg=(a, b, p, q, d), V=V, C=C, ell=room.ys[e_ // 2] - D_)
