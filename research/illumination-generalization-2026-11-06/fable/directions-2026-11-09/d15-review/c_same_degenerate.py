"""Lemma C, same form, read literally with one corridor used as both arms.

Room: the rectangle [-1, 1] x [0, 1]. Hub G = [0, 1] x [0, 1]. The corridor
[-1, 0] x [0, 1] is an arm with flat end (0, 0) and also an arm with flat end
(0, 1). The side x = 1 of G is a wall. S = (-1/10, 33/100) and
T = (-1/5, 9/25).

For each sign pair the script lists every (k1, k2) whose segment crosses both
door lines inside the full-period windows, and traces it.

Usage: python3 -B c_same_degenerate.py
"""
import sys
from fractions import Fraction as Fr

sys.dont_write_bytecode = True
import rv  # noqa: E402

Q = rv.field(2)


def main():
    L = H = Fr(1)
    R = rv.Room(1, 1, [(0, 0)], [Q(-1), Q(1)], [Q(0), Q(1)])
    al, s = Fr(1, 10), Fr(33, 100)
    be, t = Fr(1, 5), Fr(9, 25)
    S = (Q(-al), Q(s))
    T = (Q(-be), Q(t))
    assert R.interior(S) and R.interior(T)
    tx = 2 * L + be                       # arm 2 reflected in x = L
    for e1 in (1, -1):
        for e2 in (1, -1):
            out = []
            for k1 in range(-8, 9):
                for k2 in range(-8, 9):
                    sig = e1 * s + 2 * H * k1
                    th = H + e2 * (t - H) + 2 * H * k2
                    slope = (th - sig) / (tx + al)
                    a = sig + al * slope
                    b = th - be * slope
                    if -H < a < H and 0 < b < 2 * H:
                        st = rv.trace(R, S, (Q(tx + al), Q(e1 * (th - sig))), T)[0]
                        out.append((k1, k2, f"a={a}", f"b={b}", f"x=L at {(a + b) / 2}", st))
            print(f"signs ({e1:+d}, {e2:+d}): window solutions {out}")


if __name__ == "__main__":
    main()
