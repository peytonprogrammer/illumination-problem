"""Resonant instance builder shared by tests.py and double.py."""
from fractions import Fraction as Fr
from build import instance, config

def resonant(mask, S, T, k, ell_mode):
    """Construct an H-failing resonant instance; ell_mode 'long' (E window guaranteed)
    or 'double' (ell = 2h so the E family is resonant as well)."""
    cfgd = config(mask, S, T)
    C, d = cfgd[5], cfgd[3][4]
    L, w, beta = Fr(4), Fr(1, 2 ** k), Fr(1, 20)
    n = int(L / (16 * w))                                   # kappa = 1/16
    # corridor length / h
    if ell_mode == 'double':
        ell = Fr(1, 4); fh = Fr(1, 2)
    else:
        ell = Fr(1); fh = Fr(1, 20)
    room, geo, info = instance(mask, S, T, L=L, w=w, pi=Fr(3, 2), u=Fr(2, 3), D=Fr(1), h=None, beta=beta, ell=ell, fh=fh)
    h = geo[6][1] - geo[4]
    if ell_mode == 'double' and h * 2 != ell:              # T not at mid-height: not a double design
        pass
    D = 16 * h
    n = L * h / (w * D)
    assert n.denominator == 1
    n = int(n)
    j = round((Fr(n, 3) - Fr(7, 40)) / 2); i = round((Fr(j * 2 + Fr(7, 40), 2) - Fr(3, 40)) / 2)
    pi = (Fr(7, 40) + 2 * j) * L / n; u = (Fr(3, 40) + 2 * i) * L / n
    room, geo, info = instance(mask, S, T, L=L, w=w, pi=pi, u=u, D=D, h=None, beta=beta, ell=ell, fh=fh)
    return room, geo, info

