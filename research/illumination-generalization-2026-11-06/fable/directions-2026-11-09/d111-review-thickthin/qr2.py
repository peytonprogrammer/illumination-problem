"""Exact arithmetic in Q(sqrt2): numbers a + b*sqrt2 with Fraction a, b."""
from fractions import Fraction as F


class Q2:
    __slots__ = ("a", "b")

    def __init__(self, a, b=0):
        self.a, self.b = F(a), F(b)

    def __add__(s, o):
        o = o if isinstance(o, Q2) else Q2(o)
        return Q2(s.a + o.a, s.b + o.b)
    __radd__ = __add__

    def __neg__(s):
        return Q2(-s.a, -s.b)

    def __sub__(s, o):
        return s + (-(o if isinstance(o, Q2) else Q2(o)))

    def __rsub__(s, o):
        return Q2(o) - s

    def __mul__(s, o):
        o = o if isinstance(o, Q2) else Q2(o)
        return Q2(s.a * o.a + 2 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__

    def inv(s):
        n = s.a * s.a - 2 * s.b * s.b
        assert n != 0
        return Q2(s.a / n, -s.b / n)

    def __truediv__(s, o):
        o = o if isinstance(o, Q2) else Q2(o)
        return s * o.inv()

    def sign(s):
        a, b = s.a, s.b
        if a >= 0 and b >= 0:
            return 0 if a == 0 and b == 0 else 1
        if a <= 0 and b <= 0:
            return -1
        # mixed signs: compare a^2 with 2 b^2
        d = a * a - 2 * b * b
        return (1 if a > 0 else -1) if d > 0 else (1 if b > 0 else -1)

    def __lt__(s, o): return (s - o).sign() < 0
    def __le__(s, o): return (s - o).sign() <= 0
    def __gt__(s, o): return (s - o).sign() > 0
    def __ge__(s, o): return (s - o).sign() >= 0

    def __eq__(s, o):
        o = o if isinstance(o, Q2) else Q2(o)
        return s.a == o.a and s.b == o.b

    def __hash__(s):
        return hash((s.a, s.b))

    def __float__(s):
        return float(s.a) + float(s.b) * 2 ** 0.5

    def __repr__(s):
        return f"({s.a}+{s.b}r2)"


R2 = Q2(0, 1)
