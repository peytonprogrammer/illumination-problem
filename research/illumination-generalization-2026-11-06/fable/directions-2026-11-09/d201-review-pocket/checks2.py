"""d201 follow-up checks for snapshot2.md (l1-pocket-general.md).

Standard library only, exact Fractions. Arithmetic checks plus prescribed
rays in two named rooms. No ray, direction, word or room-size search.
Run: python3 -B checks2.py > checks2.log
"""
from fractions import Fraction as F
from pathlib import Path
import json
import math
import time
from checks import trace, word_of, canon, inside, on_boundary

T0 = time.process_time()
ARCH = Path(__file__).resolve().parent.parent
LED = json.load(open(ARCH / "d163-pattern-ledger" / "ledger.json"))["words"]

# (a) dictionary F L^j F L^(4-j)
print("(a) cyclic-word dictionary, F = RRLLLLRR")
claimed = {2: "LLLLRRLLRRLLLLRRLLRR", 1: "LLLLRRLLLRRLLLLRRLRR",
           0: "LLLLRRLLLLRRLLLLRRRR"}
Fw = "RRLLLLRR"
for j in range(5):
    w = canon(Fw + "L" * j + Fw + "L" * (4 - j))
    e = LED.get(w)
    print("  j=%d canon %s claimed-match=%s ledger=%s" % (
        j, w, claimed.get(min(j, 4 - j)) == w,
        None if e is None else (e["status"], e["family"], e["W"], e["r"])))


def rect_union_poly(cells):
    """Boundary word of a union of unit cells (simple room), CCW vertices."""
    edges = {}
    for (x, y) in cells:
        for a, b in [((x, y), (x + 1, y)), ((x + 1, y), (x + 1, y + 1)),
                     ((x + 1, y + 1), (x, y + 1)), ((x, y + 1), (x, y))]:
            if (b, a) in edges:
                del edges[(b, a)]
            else:
                edges[(a, b)] = 1
    nxt = {a: b for (a, b) in edges}
    start = min(nxt)
    poly = [start]
    p = nxt[start]
    while p != start:
        poly.append(p)
        p = nxt[p]
    # drop collinear vertices
    out = []
    n = len(poly)
    for i in range(n):
        a, b, c = poly[i - 1], poly[i], poly[(i + 1) % n]
        if (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]) != 0:
            out.append(b)
    return out


def box(x0, y0, x1, y1):
    return {(x, y) for x in range(x0, x1) for y in range(y0, y1)}


# Named realizations: middle 3x3 chamber at [0,3]^2, unit necks length 1,
# 3x3 end chambers.
real = {
    "opposite": box(0, 0, 3, 3) | box(-1, 1, 0, 2) | box(-4, 0, -1, 3)
    | box(3, 1, 4, 2) | box(4, 0, 7, 3),
    "adjacent": box(0, 0, 3, 3) | box(-1, 1, 0, 2) | box(-4, 0, -1, 3)
    | box(1, 3, 2, 4) | box(0, 4, 3, 7),
}
# same side: two necks down from the bottom of a 7-wide middle chamber
real["same-side"] = (box(0, 0, 7, 3) | box(1, -1, 2, 0) | box(0, -4, 3, -1)
                     | box(5, -1, 6, 0) | box(4, -4, 7, -1))
for k, cells in real.items():
    V = rect_union_poly(cells)
    print("  realization %-9s W=%d word %s" % (k, len(V), canon(word_of(V))))

# R22-comparison family: width-1 chambers of height H, unit necks at (1,H-1).
print("  width-1 family:")
for H in (5, 6, 9):
    cells = box(0, 0, 1, H) | box(1, 1, 2, H - 1) | box(2, 0, 3, H) \
        | box(3, 1, 4, H - 1) | box(4, 0, 5, H)
    V = rect_union_poly(cells)
    maps = [lambda x, y: (x, y), lambda x, y: (x, -y - 1),
            lambda x, y: (y, x), lambda x, y: (-y - 1, x)]
    found = 0
    for m in maps:
        C = {m(*c) for c in cells}
        cx = [c[0] for c in C]
        cy = [c[1] for c in C]
        for a0 in range(min(cx), max(cx) + 1):
            for w in range(3, max(cx) - a0 + 2):
                for b0 in range(min(cy), max(cy) + 1):
                    for h in range(1, max(cy) - b0 + 2):
                        if not all((a0 + i, b0 + j) in C for i in range(w) for j in range(h)):
                            continue
                        if (all((a0 + i, b0 + h) not in C for i in range(w))
                                and all((a0 - 1, b0 + j) not in C and (a0 + w, b0 + j) not in C
                                        for j in range(h))
                                and all((a0 + i, b0 - 1) in C for i in range(w))):
                            found += 1
    marks = [(x, y) for x in (1, 2, 3, 4) for y in range(2, H - 1)]
    ok = all(inside(V, p) and not on_boundary(V, p) for p in marks)
    print("    H=%d W=%d word=%s full-mouth pockets(w>=3,h>=1)=%d marks interior=%s"
          % (H, len(V), canon(word_of(V)) == claimed[2], found, ok))

# (b) strip transit test in a named displaced room.
print("\n(b) displaced strip transit")
w, Hm, l1, r1, l2, r2, L1, L2, e = 3, 6, 1, 2, 4, 5, 2, 2, 3
cells = (box(0, 0, w, Hm) | box(-L1, l1, 0, r1) | box(-L1 - e, 0, -L1, Hm)
         | box(w, l2, w + L2, r2) | box(w + L2, 0, w + L2 + e, Hm))
V = rect_union_poly(cells)
delta = l2 - r1
print("  room: middle %dx%d, left neck (%d,%d), right neck (%d,%d), delta=%d, W=%d"
      % (w, Hm, l1, r1, l2, r2, delta, len(V)))
for S, T in [((-3, r1 - 1), (6, l2 + 1)), ((-4, r1 - 1), (6, l2 + 1))]:
    U, Vx = F(S[0]), F(T[0])
    g1, g2 = r1 - S[1], T[1] - l2
    lo = max(F(0), -U / g1, (Vx - w) / g2)
    hi = min((w - U) / g1, Vx / g2)
    sp = F(2 * w, g1 + delta + g2)
    c0 = (Vx - U) / (g1 + delta + g2)
    c = c0 + sp * (math.floor((lo - c0) / sp) + 1)
    assert lo < c < hi
    a, b = U + g1 * c, Vx - g2 * c
    assert 0 < a < w and 0 < b < w and (a + delta * c - b) % (2 * w) == 0
    A, K = -U, Vx - w
    assert hi - lo == w - abs(A - K)
    st, bn = trace(V, S, (c, 1), T)
    print("  S=%s T=%s A=%s K=%s |A-K|<w*d/(d+2)=%s interval=(%s,%s) c=%s a=%s b=%s -> %s, %d bounces"
          % (S, T, A, K, abs(A - K) < F(w * delta, delta + 2), lo, hi, c, a, b, st, len(bn)))

# (c) obstruction arithmetic.
print("\n(c) obstructions")
bad = 0
for ww in range(1, 8):
    for A in range(1, 20):
        for K in range(1, 20):
            lo, hi = max(0, A, K), min(ww + A, ww + K)
            if abs(A - K) >= ww and lo < hi:
                bad += 1
print("  g1=g2=1, |A-K|>=w gives an empty interval: counterexamples", bad)
print("  straight unit-neck leg of length L has |dy/dx| < 1/L; the upper pocket needs"
      " climb > delta within run < w; impossible iff delta*L >= w (stated for that leg only)")
print("\nCPU seconds: %.2f" % (time.process_time() - T0))
