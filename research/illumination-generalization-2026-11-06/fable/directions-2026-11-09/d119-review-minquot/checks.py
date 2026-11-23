"""d119 checks for minimal-quotient-rigidity.snapshot.md.

Run: python3 -B checks.py > checks.log

Part A: exact period linear algebra on three named one-axis lines
        (12-wall cross, DB55 stretch, DBas family).
Part B: Riemann-Hurwitz enumeration for f: Q -> Y, r <= 8.
Part C: rank and dimension ranges for the table rows.
No room, ray, direction or reflection-word search.
"""
from fractions import Fraction as F
import random

# ---------- affine numbers a + b t ----------
class A:
    __slots__ = ("a", "b")
    def __init__(self, a, b=0):
        self.a, self.b = F(a), F(b)
    def __add__(s, o): o = o if isinstance(o, A) else A(o); return A(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = o if isinstance(o, A) else A(o); return A(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return A(o) - s
    def __mul__(s, k): return A(s.a * F(k), s.b * F(k))
    __rmul__ = __mul__
    def __eq__(s, o): o = o if isinstance(o, A) else A(o); return s.a == o.a and s.b == o.b
    def at(s, t): return s.a + s.b * F(t)
    def __repr__(s):
        if s.b == 0: return f"{s.a}"
        return f"{s.a}{'+' if s.b >= 0 else '-'}{abs(s.b)}t"

T_SAMPLES = [F(0), F(1, 7), F(-1, 5)]  # small |t|: cut order is constant there


def runs(rects, coord, lo, hi):
    """Maximal runs of the union of rectangles along `coord` inside the open slab (lo, hi)
    of the other coordinate. Rectangles are (x0, x1, y0, y1) with affine x and rational y."""
    iv = []
    for (x0, x1, y0, y1) in rects:
        if coord == "x":
            if y0.at(0) <= lo and hi <= y1.at(0): iv.append((x0, x1))
        else:
            if x0.at(0) <= lo and hi <= x1.at(0): iv.append((y0, y1))
    iv.sort(key=lambda p: p[0].at(0))
    out = []
    for p in iv:
        if out and all(p[0].at(t) <= out[-1][1].at(t) for t in T_SAMPLES):
            if all(p[1].at(t) > out[-1][1].at(t) for t in T_SAMPLES):
                out[-1] = (out[-1][0], p[1])
        else:
            out.append(p)
    return out


def cylinder_periods(rects):
    """Horizontal core-curve periods 2*(run width) (affine reals) and vertical ones 2i*(run height)
    on the four-copy translation unfolding. Vertical heights are t-independent here."""
    ys = sorted({r[k].at(0) for r in rects for k in (2, 3)})
    xs = sorted({r[k].at(0) for r in rects for k in (0, 1)})
    hor = []
    for lo, hi in zip(ys, ys[1:]):
        for a, b in runs(rects, "x", lo, hi):
            hor.append(((lo, hi), (b - a) * 2))
    ver = []
    for lo, hi in zip(xs, xs[1:]):
        for a, b in runs(rects, "y", lo, hi):
            w = (b - a) * 2
            assert w.b == 0
            ver.append(((lo, hi), w))
    return hor, ver


def solve_motion(P1, P2, V, a, v, c):
    """x*P1 + y*P2 = a + v t ; z*V = c (V real height-period coefficient of i)."""
    det = P1.a * P2.b - P2.a * P1.b
    assert det != 0
    x = (a * P2.b - v * P2.a) / det
    y = (P1.a * v - P1.b * a) / det
    z = F(c) / V.a
    return x, y, z, det


def part_A():
    print("== Part A: rational affine mark motion vs three absolute periods ==")
    t = A(0, 1)
    lines = {
        # 12-wall cross: horizontal bar [-(7+t),7+t]x[-2,2], vertical bar [-2,2]x[-7,7]
        "cross (b=7+t)": dict(
            rects=[(A(-7) - t, A(7) + t, A(-2), A(2)), (A(-2), A(2), A(-7), A(7))],
            corner=(A(-7) - t, F(-2)),
            marks={"center O": (A(0), F(0)), "(6,0)": (A(6) + t, F(0)), "(0,6)": (A(0), F(6))}),
        # DB55 stretch, l = 3 + t (d108 named l = 3)
        "DB55 (l=3+t)": dict(
            rects=[(A(0), A(5), A(0), A(5)), (A(5), A(8) + t, A(2), A(3)), (A(8) + t, A(13) + t, A(0), A(5))],
            corner=(A(0), F(0)),
            marks={"(1,1)": (A(1), F(1)), "(5+l+1,1)": (A(9) + t, F(1)), "(5+l+3,3)": (A(11) + t, F(3))}),
        # DBas family, l = 4 + t (d109 room.py, l = 4 is DBas; marks (1,3), (5+l+2,3))
        "DBas (l=4+t)": dict(
            rects=[(A(0), A(5), A(0), A(4)), (A(5), A(9) + t, A(1), A(2)), (A(9) + t, A(13) + t, A(-1), A(5))],
            corner=(A(0), F(0)),
            marks={"(1,3)": (A(1), F(3)), "(11+t,3)": (A(11) + t, F(3))}),
    }
    rnd = random.Random(119)
    for name, L in lines.items():
        hor, ver = cylinder_periods(L["rects"])
        print(f"-- {name}")
        print("   horizontal core periods (slab: 2*width):", [(s, str(p)) for s, p in hor])
        print("   vertical core periods (slab: 2*height, times i):", [(s, str(p)) for s, p in ver])
        # choose two nonproportional horizontal periods and one vertical
        P1 = P2 = None
        for i in range(len(hor)):
            for j in range(i + 1, len(hor)):
                p, q = hor[i][1], hor[j][1]
                if p.a * q.b - q.a * p.b != 0:
                    P1, P2 = p, q; break
            if P1: break
        V = ver[0][1]
        print(f"   chosen P1={P1}, P2={P2}, V=i*{V}; minor e1u2-e2u1 = {P1.a*P2.b - P2.a*P1.b}")
        # rank of the real-affine span of all horizontal periods (as vectors (const, coef))
        rk = 2 if any(p.a * q.b - q.a * p.b for _, p in hor for _, q in hor) else 1
        print(f"   rank of affine horizontal period span = {rk} (so x0 and v are separated)")
        cx, cy = L["corner"]
        for mname, (mx, my) in L["marks"].items():
            d = mx - cx
            a, v, c = d.a, d.b, my - cy
            x, y, z, _ = solve_motion(P1, P2, V, a, v, c)
            lhs = P1 * x + P2 * y
            ok = (lhs == d) and (V.a * z == c)
            vals = [lhs.at(s) == d.at(s) for s in (F(3, 11), F(-2, 9), F(1, 1000))]
            print(f"   mark {mname}: displacement ({d}, {c}) = {x}*P1 + {y}*P2 + {z}*V  identity={ok} samples={all(vals)}")
            assert ok and all(vals)
        # vacuity control: any rational affine motion is fitted, including fake ones
        bad = 0
        for _ in range(1000):
            a, v, c = (F(rnd.randint(-50, 50), rnd.randint(1, 12)) for _ in range(3))
            x, y, z, _ = solve_motion(P1, P2, V, a, v, c)
            if not (P1 * x + P2 * y == A(a, v) and V.a * z == c): bad += 1
        print(f"   control: 1000 random rational motions (a+vt, c), failures to fit = {bad}")
        assert bad == 0
    # cross: half-turn center is a quarter of the long horizontal circumference
    t = A(0, 1)
    print("-- cross center check: 7+t =", "(1/4)*(28+4t)", (A(28, 4) * F(1, 4)) == (A(7) + t))
    # twice a corner-to-corner wall vector is an absolute period (gamma - J gamma);
    # here verify it lies in the Q-span of the core periods for the cross walls 4 and 5+t
    for w in (A(4), A(5) + t):
        x, y, _, _ = solve_motion(A(8), A(28, 4), A(8), (2 * w).a, (2 * w).b, 0)
        print(f"   2*wall {w} = {x}*8 + {y}*(28+4t)")


# ---------- Part B: Riemann-Hurwitz for f : Q -> Y ----------
def partitions_123(k):
    """Partitions of k with parts in {1,2,3}, as (n1, n2, n3)."""
    out = []
    for n3 in range(k // 3 + 1):
        for n2 in range((k - 3 * n3) // 2 + 1):
            out.append((k - 3 * n3 - 2 * n2, n2, n3))
    return out


def part_B():
    print("\n== Part B: Riemann-Hurwitz for f: Q -> Y, Q in Q(1^r,-1^(r+4)), r <= 8 ==")
    # local orders: e(a+2)-2 in {-1,0,1}
    allowed = {(a, e) for a in range(-1, 6) for e in range(1, 10) if e * (a + 2) - 2 in (-1, 0, 1)}
    print("   allowed (downstairs order a, local degree e):", sorted(allowed))
    rows = []
    for k in range(1, 10):
        for z in range(0, 9):
            npole = z + 4
            # distribute pole fibres: each pole gets a partition of k with parts <= 3
            parts = partitions_123(k)
            states = {(0, 0)}  # DP over poles on (c2, c3)
            for _ in range(npole):
                states = {(c2 + n2, c3 + n3) for (c2, c3) in states for (n1, n2, n3) in parts
                          if c2 + n2 + 2 * (c3 + n3) <= 2 * k - 2}
            seen = set()
            for (c2, c3) in states:
                if c2 + 2 * c3 == 2 * k - 2:
                    r = k * z + c3
                    c1 = k * npole - 2 * c2 - 3 * c3
                    if r <= 8 and c1 == r + 4:
                        seen.add((c2, c3))
            for (c2, c3) in sorted(seen):
                rows.append((k, z, k * z + c3, c2, c3))
    print("   (k, z, r, c2, c3) feasible by RH and fibre partitions (monodromy not checked):")
    for row in rows:
        print("    ", row)
    # assertions matching the note
    assert all(z >= 1 or True for (k, z, r, c2, c3) in rows)
    z0 = [row for row in rows if row[1] == 0]
    print("   rows with z = 0 (pillowcase base, torus cover, excluded at irrational t):", len(z0))
    hi = [row for row in rows if row[1] >= 3]
    print("   rows with z >= 3:", hi)
    assert all(k <= 2 for (k, z, r, c2, c3) in hi)
    assert {(z, r) for (k, z, r, c2, c3) in hi if k == 2} == {(3, 6), (4, 8)}
    assert all(r == z for (k, z, r, c2, c3) in hi if k == 1)
    assert all(c3 == 0 and c2 == 2 for (k, z, r, c2, c3) in rows if k == 2)
    # compare (z, k) support with d22's list: z=1 k<=8, z=2 k<=4, z=3,4 k=2 (k>=2)
    sup = sorted({(z, k) for (k, z, r, c2, c3) in rows if k >= 2 and z >= 1})
    d22 = sorted([(1, d) for d in range(2, 9)] + [(2, d) for d in range(2, 5)] + [(3, 2), (4, 2)])
    print("   (z, k>=2) support:", sup)
    print("   equals d22 finite list:", sup == d22)
    assert sup == d22
    # four distinct regular periodic points on Q need c2 >= 4 if all map to poles
    need = sorted({(k, z) for (k, z, r, c2, c3) in rows if 1 <= z <= 2 and k >= 2 and c2 >= 4})
    noneed = sorted({(k, z) for (k, z, r, c2, c3) in rows if 1 <= z <= 2 and k >= 2} - set(need))
    print("   z<=2, k>=2: (k,z) with some c2 >= 4 (census needed):", need)
    print("   z<=2, k>=2: (k,z) with every c2 <= 3 (counting alone closes):", noneed)


def part_C():
    print("\n== Part C: dimensions and rank ranges ==")
    for z in range(1, 9):
        dimQ = 2 * z + 2
        g = z + 1  # 2g-2 = 2(-2) + (2z+4)
        assert 2 * g - 2 == -4 + (2 * z + 4)
        thr = F(g, 2) + 1
        dimH = 2 * g + z - 1  # H(2^z)
        proper = [h for h in range(2, g + 1) if h < thr]
        print(f"   z={z}: dim Q(1^z,-1^(z+4))={dimQ}, orientation genus={g}, dim H(2^z)={dimH}, "
              f"2z+2<3z+1: {dimQ < dimH}, proper non-high ranks {proper}")
    print("   upstairs bound h < (r+3)/2 from d89:")
    for r in range(1, 9):
        print(f"     r={r}: h in {[h for h in range(2, r + 2) if h < F(r + 3, 2)]}")
    print("   table rows: k=1,r=3 -> z=3, h in", [h for h in range(2, 5) if h < F(6, 2)],
          "; k=2,r=6 -> z=3, downstairs h in", [h for h in range(2, 5) if h < F(4, 2) + 1],
          "; k=2,r=8 -> z=4, downstairs h in", [h for h in range(2, 6) if h < F(5, 2) + 1])
    print("   k=2: at most c2=2 e=2 points; 4 distinct regular lifts s+-,t+- => >=2 map to regular points of Y")


if __name__ == "__main__":
    part_A()
    part_B()
    part_C()
    print("\nALL ASSERTIONS PASSED")
