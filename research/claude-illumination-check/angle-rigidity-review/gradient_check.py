"""Independent exact gradients of the 147 saved event functions in all 48 coordinates.

Uses this folder's own unfolding (independent_check.py) with a sparse forward-mode derivative type.
Checks: rows equal Codex's result.json rows exactly, rank 43, and the kernel equals the 5 known
symmetry tangents (2 translations, 1 rotation, 2 axis scalings). No new words, directions, or rooms.
"""
import json
from fractions import Fraction as F

import independent_check as ic


class G:
    """Value plus a sparse gradient over the 48 coordinates."""
    __slots__ = ("a", "b")

    def __init__(self, a, b=None):
        self.a, self.b = F(a), b or {}

    @staticmethod
    def lift(x):
        return x if isinstance(x, G) else G(x)

    def __add__(self, o):
        o = G.lift(o)
        b = dict(self.b)
        for k, v in o.b.items():
            b[k] = b.get(k, 0) + v
        return G(self.a + o.a, b)
    __radd__ = __add__

    def __neg__(self):
        return G(-self.a, {k: -v for k, v in self.b.items()})

    def __sub__(self, o):
        return self + (-G.lift(o))

    def __rsub__(self, o):
        return G.lift(o) - self

    def __mul__(self, o):
        o = G.lift(o)
        b = {k: v * o.a for k, v in self.b.items()}
        for k, v in o.b.items():
            b[k] = b.get(k, 0) + self.a * v
        return G(self.a * o.a, b)
    __rmul__ = __mul__

    def __truediv__(self, o):
        o = G.lift(o)
        inv = G(1 / o.a, {k: -v / (o.a * o.a) for k, v in o.b.items()})
        return self * inv

    def __rtruediv__(self, o):
        return G.lift(o) / self


def var(x, k):
    return G(x, {k: F(1)})


def rank(rows):
    piv = {}
    for row in rows:
        r = list(row)
        for i, p in sorted(piv.items()):
            if r[i]:
                c = r[i]
                r = [x - c * y for x, y in zip(r, p)]
        if any(r):
            i = next(i for i, x in enumerate(r) if x)
            piv[i] = [x / r[i] for x in r]
    return len(piv)


def main():
    n = ic.n
    V = [(var(x, 2 * i), var(y, 2 * i + 1)) for i, (x, y) in enumerate(ic.V0)]
    S = (var(ic.S0[0], 44), var(ic.S0[1], 45))
    T = (var(ic.T0[0], 46), var(ic.T0[1], 47))
    codex = [[F(x) for x in r] for r in ic.res["rows"]]
    rows = []
    for ev in ic.events:
        ic.analyze(ev, ic.V0, ic.S0, ic.T0, base=True)  # sets the corner leg from the base geometry
        w, c, k = ev["word"], ic.V0.index(tuple(map(F, ev["corner"]))), ev["_leg"]
        A = ic.sub(ic.unfold(T, w, V), S)
        C = ic.sub(ic.unfold(V[c], w[:k], V), S)
        f = ev["perturb_side"] * ic.cross(A, C)
        assert f.a == 0
        rows.append([f.b.get(j, F(0)) for j in range(48)])
    pts = ic.V0 + [ic.S0, ic.T0]
    sym = [[c for p in pts for c in m(p)] for m in (lambda p: (1, 0), lambda p: (0, 1), lambda p: (-p[1], p[0]),
                                                    lambda p: (p[0], 0), lambda p: (0, p[1]))]
    ann = all(sum(g * s for g, s in zip(r, q)) == 0 for r in rows for q in sym)
    out = {"rows_equal_codex": rows == codex, "rank": rank(rows), "symmetry_rank": rank(sym),
           "symmetries_annihilated": ann, "kernel_dimension": 48 - rank(rows)}
    out["status"] = "PASS" if out["rows_equal_codex"] and out["rank"] == 43 and ann and out["symmetry_rank"] == 5 else "FAIL"
    json.dump(out, open(ic.HERE / "gradient_check.json", "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
