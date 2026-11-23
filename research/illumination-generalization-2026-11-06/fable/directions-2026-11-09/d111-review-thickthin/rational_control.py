"""Negative control for the irrationality step (search only, no darkness claim).
Triply rational dumbbell: D1=H1=D2=H2=1, L=2, rational marks.  The window centres differ by
values in a fixed lattice, so for small w the construction finds no overlap of width delta.
Instance A from thin_door.py (H2=sqrt2) is rerun with the same search as a positive contrast."""
from fractions import Fraction as F
from qr2 import Q2, R2
from thin_door import witness
q = lambda v: Q2(F(v))
S, T = (q(F(1, 3)), q(F(1, 5))), (q(F(37, 10)), q(F(6, 5)))
for w in (F(1, 20), F(1, 60), F(1, 150), F(1, 1000)):
    for name, H2 in (("rational H2=1", q(1)), ("irrational H2=sqrt2", R2)):
        res = []
        for c1 in (0, 1):
            for c2 in (0, 1):
                r = witness(q(1), q(1), q(1), H2, q(2), q(F(3, 10)), q(0), Q2(w), S, T, c1, c2, Kmax=200000)
                res.append("none" if r is None else f"k={r[2]}")
        print(f"w={w} {name}: caps 00,01,10,11 -> {res}")
