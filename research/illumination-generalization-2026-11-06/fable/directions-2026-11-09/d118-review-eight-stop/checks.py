"""d118 checks: replay the R34 claims of eight-stop-consult.snapshot.md.

Exact (Fraction) arithmetic. Named room R34-base only. Only the directions
and steps the note names are traced; nothing is searched.
"""
import json
import os
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ROOMS = os.path.join(HERE, "..", "d8-perturbation-test", "rooms.json")
room = next(r for r in json.load(open(ROOMS)) if r["id"] == "R34-base")
CELLS = {tuple(c) for c in room["cells"]}
S, T = (2, 0), (6, 0)
assert [list(S), list(T)] == room["marks"]


def quad(p):
    """Cells around lattice point p, keyed NE, NW, SW, SE."""
    x, y = p
    return {"NE": (x, y) in CELLS, "NW": (x - 1, y) in CELLS,
            "SW": (x - 1, y - 1) in CELLS, "SE": (x, y - 1) in CELLS}


def kind(p):
    q = quad(p)
    n = sum(q.values())
    if n == 4:
        return "interior"
    if n == 3:
        return "reflex"
    if n == 1:
        return "convex"
    if n == 2:
        if (q["NE"] and q["SW"]) or (q["NW"] and q["SE"]):
            return "pinch"
        return "smooth"
    return "outside"


xs = [c[0] for c in CELLS]
ys = [c[1] for c in CELLS]
pts = [(x, y) for x in range(min(xs), max(xs) + 2) for y in range(min(ys), max(ys) + 2)]
K = {p: kind(p) for p in pts}
conv = [p for p in pts if K[p] == "convex"]
refl = [p for p in pts if K[p] == "reflex"]
print("== Room R34-base")
print("cells", len(CELLS), "convex", len(conv), "reflex", len(refl), "W", len(conv) + len(refl),
      "pinches", sum(K[p] == "pinch" for p in pts))
assert len(conv) == 19 and len(refl) == 15
print("S", K[S], "T", K[T])
assert K[S] == K[T] == "interior"


def cls(p):
    return (p[0] % 2, p[1] % 2)


print("\n== Parity classes (claim: each off-class has 5 reflexes and 4 convex)")
for c in [(0, 0), (1, 0), (0, 1), (1, 1)]:
    r = sorted(p for p in refl if cls(p) == c)
    v = sorted(p for p in conv if cls(p) == c)
    reg = sorted(p for p in pts if cls(p) == c and K[p] in ("interior", "smooth"))
    print(c, "reflex", len(r), "convex", len(v), "regular", [(p, K[p]) for p in reg])
    print("    reflexes", r)
ee_reg = sorted(p for p in pts if cls(p) == (0, 0) and K[p] in ("interior", "smooth"))
assert ee_reg == [(2, 0), (4, 0), (6, 0), (8, -2)]
assert K[(4, 0)] == K[(8, -2)] == "smooth"

print("\n== Strip [1,7]x[-1,0]")
print("cells (1..6,-1) all present:", all((x, -1) in CELLS for x in range(1, 7)))
print("left end x=1 is a wall:", (0, -1) not in CELLS, " right end x=7 is a wall:", (7, -1) not in CELLS)


def cell_of(p, v):
    """Unit cell containing p + eps*v (p exact, v nonzero integer)."""
    e = F(1, 10 ** 6)
    return (int((p[0] + e * v[0]) // 1), int((p[1] + e * v[1]) // 1))


def trace(p, v, max_events=200):
    """Exact billiard from lattice point p with integer velocity v.

    Returns (first lattice point reached, list of wall bounces, final velocity).
    Aborts if the launch cell or any later cell is outside the room.
    """
    p = (F(p[0]), F(p[1]))
    vx, vy = v
    cur = cell_of(p, (vx, vy))
    assert cur in CELLS, ("launch leaves room", p, v)
    bounces = []
    for _ in range(max_events):
        tx = ty = None
        if vx:
            nx = cur[0] + 1 if vx > 0 else cur[0]
            tx = (nx - p[0]) / vx
        if vy:
            ny = cur[1] + 1 if vy > 0 else cur[1]
            ty = (ny - p[1]) / vy
        ts = [t for t in (tx, ty) if t is not None]
        t = min(ts)
        p = (p[0] + t * vx, p[1] + t * vy)
        hitx = tx is not None and tx == t
        hity = ty is not None and ty == t
        if hitx and hity or (p[0].denominator == 1 and p[1].denominator == 1):
            return (int(p[0]), int(p[1])), bounces, (vx, vy)
        if hitx:
            nxt = (cur[0] + (1 if vx > 0 else -1), cur[1])
            if nxt in CELLS:
                cur = nxt
            else:
                bounces.append(("x", p))
                vx = -vx
        else:
            nxt = (cur[0], cur[1] + (1 if vy > 0 else -1))
            if nxt in CELLS:
                cur = nxt
            else:
                bounces.append(("y", p))
                vy = -vy
    raise RuntimeError("no lattice hit")


def fmt(b):
    return [(a, (str(q[0]), str(q[1]))) for a, q in b]


print("\n== Indispensability certificates (strip legs from the bottom midpoints)")
CERTS = {(3, -1): [((-3, 1), S), ((3, 1), T)],
         (4, -1): [((-2, 1), S), ((2, 1), T)],
         (5, -1): [((-3, 1), S), ((3, 1), T)]}
for C, legs in CERTS.items():
    assert K[C] == "reflex", C
    print("C", C, K[C], "class", cls(C), "quadrants", quad(C))
    for v, target in legs:
        hit, b, vout = trace(C, v)
        ok = hit == target
        print("   leg", v, "-> first lattice point", hit, "bounces", fmt(b), "arrive v", vout, "OK" if ok else "FAIL")
        assert ok
        for _, q in b:
            assert -1 < q[1] < 0
    (a, _), (c, _) = legs
    print("   |components| equal:", (abs(a[0]), abs(a[1])) == (abs(c[0]), abs(c[1])),
          "; vertical mirror of S-leg", (a[0], -a[1]), "is -T-leg:", (a[0], -a[1]) == (-c[0], -c[1]),
          "; physical rays differ:", a != c)

# Link geometry at C=(3,-1) with exact quarter-turn bookkeeping (angles in
# units where the S-leg physical angle is pi - t and the T-leg angle is t).
print("\n== Link check at C=(3,-1): room wedge is [0, 3pi/2] (SE missing)")
print("   room copy: theta_T = t, theta_S = pi - t, gap = pi - 2t (not pi): no straight passage")
print("   vertically mirrored copy (sector [-3pi/2, 0]): theta_S = -(pi - t), gap to theta_T = pi exactly")
print("   that pi-arc [-(pi - t), t] contains the sector boundary 0, so the note's affine move is needed")

print("\n== Ten accessible reflexes from S at the first primitive step")
ACC = [(1, 0), (3, 0), (2, 1), (2, -1), (1, 1)] + [(j, -1) for j in range(3, 8)]
assert len(set(ACC)) == 10
for C in ACC:
    v = (C[0] - S[0], C[1] - S[1])
    hit, b, _ = trace(S, v)
    print("  ", C, K[C], "dir", v, "first lattice point", hit, "bounces", len(b),
          "OK" if hit == C and K[C] == "reflex" else "FAIL")
    assert hit == C and K[C] == "reflex"
print("   reflexes not in the list:", sorted(set(refl) - set(ACC)))

print("\n== Convex-corner fold (Section 1): product of the two perpendicular reflections")
Rx = ((-1, 0), (0, 1))
Ry = ((1, 0), (0, -1))
prod = tuple(tuple(sum(Rx[i][k] * Ry[k][j] for k in range(2)) for j in range(2)) for i in range(2))
print("   Rx*Ry =", prod, "== -I:", prod == ((-1, 0), (0, -1)))
print("\nall checks passed")
