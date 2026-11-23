"""Tracer sanity: shots into a reflex door corner and a convex corner must die; a direct
cross-door shot at a nonzero slope that clears the corridor must light."""
from fractions import Fraction as F
from qr2 import Q2, R2
from tracer import trace
from thin_door import room
q = lambda v: Q2(F(v))
w = q(F(1, 20)); P = room(q(1), q(1), q(1), R2, q(2), q(F(3, 10)), q(0), w)
S = (q(F(1, 3)), q(F(1, 5)))
print("reflex (1,3/10):", trace(P, S, (q(F(37, 10)), q(F(6, 5))), (q(F(3, 10)) - S[1]) / (1 - S[0]), 1, 1)[3])
print("convex (1,1):  ", trace(P, S, (q(F(37, 10)), q(F(6, 5))), (1 - S[1]) / (1 - S[0]), 1, 1)[3])
S2 = (q(F(1, 2)), q(F(31, 100)))
T2 = (S2[0] + 3, S2[1] + q(F(3, 100)))
print("straight shot through corridor:", trace(P, S2, T2, q(F(1, 100)), 1, 1)[3])
