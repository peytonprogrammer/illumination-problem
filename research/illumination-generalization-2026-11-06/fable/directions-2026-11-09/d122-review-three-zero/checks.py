"""d122 checks for the three-zero notes. Run: python3 -B checks.py > checks.log

Part A: the 64 sign arrays on the alternating six-cycle, det F, and the
        Cauchy-Binet minors.
Part B: topological intersection numbers of doubled arcs, computed on explicit
        hyperelliptic models (branch cuts as rays, sheets tracked along
        racetrack loops). B1 is a genus-two bigon; B2 is the genus-four hexagon.
Part C: integer counts in the recognition and divisor notes.
No rooms, rays of billiard trajectories, directions or reflection words.
"""
import cmath
import itertools
import math
from fractions import Fraction


def det2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


E = [[1, 0], [-1, 1], [0, -1]]  # columns (1,-1,0) and (0,1,-1)


def detF(C):
    # F = E^T C E
    CE = [[sum(C[i][k] * E[k][j] for k in range(3)) for j in range(2)] for i in range(3)]
    F = [[sum(E[k][i] * CE[k][j] for k in range(3)) for j in range(2)] for i in range(2)]
    return det2(F)


SUPPORT = [(i, i) for i in range(3)] + [(i, (i - 1) % 3) for i in range(3)]
# C[i][i]   : a_i and b_i share Z_i
# C[i][i-1] : a_i and b_{i-1} share P_i


def array_from_signs(signs):
    C = [[0] * 3 for _ in range(3)]
    for (i, j), s in zip(SUPPORT, signs):
        C[i][j] = s
    return C


def part_a():
    print("== Part A: sign arrays on the six-cycle")
    # E maximal minors
    minors_E = [E[r][0] * E[s][1] - E[r][1] * E[s][0] for r, s in itertools.combinations(range(3), 2)]
    print("maximal minors of E:", minors_E)
    dist = {}
    by_prod = {1: {}, -1: {}}
    all_minors_unit = True
    for signs in itertools.product([1, -1], repeat=6):
        C = array_from_signs(signs)
        for rows in itertools.combinations(range(3), 2):
            for cols in itertools.combinations(range(3), 2):
                m = det2([[C[r][c] for c in cols] for r in rows])
                if abs(m) != 1:
                    all_minors_unit = False
        d = abs(detF(C))
        dist[d] = dist.get(d, 0) + 1
        p = math.prod(signs)
        by_prod[p][d] = by_prod[p].get(d, 0) + 1
    print("every 2x2 minor of C is +-1 for all 64 arrays:", all_minors_unit)
    print("|det F| distribution over 64 arrays:", dict(sorted(dist.items())))
    print("  split by product of the six signs = +1:", dict(sorted(by_prod[1].items())))
    print("  split by product of the six signs = -1:", dict(sorted(by_prod[-1].items())))
    I = [[1 if i == j else 0 for j in range(3)] for i in range(3)]
    S = [[1 if j == (i - 1) % 3 else 0 for j in range(3)] for i in range(3)]
    for name, sz, sq in [("I+S", 1, 1), ("I-S", 1, -1)]:
        C = [[sz * I[i][j] + sq * S[i][j] for j in range(3)] for i in range(3)]
        print(f"C = {name}: det F = {detF(C)}, det C = {det3(C)}")
    print()


# ---------- Part B: intersection numbers on hyperelliptic models ----------

def seg_intersect(p1, p2, q1, q2):
    """Return (t, u) with p1 + t (p2-p1) = q1 + u (q2-q1), 0<=t<1, 0<=u<1, or None."""
    d1 = p2 - p1
    d2 = q2 - q1
    den = (d1.conjugate() * d2).imag
    if abs(den) < 1e-15:
        return None
    w = q1 - p1
    t = (w.conjugate() * d2).imag / den
    u = (w.conjugate() * d1).imag / den
    if 0 <= t < 1 and 0 <= u < 1:
        return t, u
    return None


def ray_hits(p1, p2, ray):
    """Parameters t in [0,1) where segment p1p2 crosses ray (origin, direction)."""
    o, d = ray
    far = o + d * 1e3
    r = seg_intersect(p1, p2, o, far)
    return [] if r is None else [r[0]]


def sheet_profile(loop, rays):
    """For each segment of the closed polygon, list of crossing params and the
    starting sheet of the segment. Returns (start_sheets, crossings, closes)."""
    n = len(loop)
    sheet = 0
    starts, cross = [], []
    for k in range(n):
        p1, p2 = loop[k], loop[(k + 1) % n]
        ts = sorted(t for ray in rays for t in ray_hits(p1, p2, ray))
        starts.append(sheet)
        cross.append(ts)
        sheet ^= (len(ts) % 2)
    return starts, cross, sheet == 0


def sheet_at(starts, cross, k, t):
    return starts[k] ^ (sum(1 for x in cross[k] if x < t) % 2)


def racetrack(path, r, m=48):
    """Closed polygon around a polyline path (list of complex), offset r,
    traversed counterclockwise around the arc."""
    pts = []
    dense = []
    for a, b in zip(path, path[1:]):
        for s in range(m):
            dense.append(a + (b - a) * s / m)
    dense.append(path[-1])
    normals = []
    for k in range(len(dense)):
        a = dense[max(k - 1, 0)]
        b = dense[min(k + 1, len(dense) - 1)]
        d = (b - a) / abs(b - a)
        normals.append(d * 1j)
    right = [p - r * nrm for p, nrm in zip(dense, normals)]
    left = [p + r * nrm for p, nrm in zip(dense, normals)]
    end_dir = normals[-1] / 1j
    start_dir = normals[0] / 1j
    pts += right
    # cap at end: from right side to left side around the endpoint
    ang0 = cmath.phase(-normals[-1])
    for s in range(1, m):
        pts.append(dense[-1] + r * cmath.exp(1j * (ang0 + math.pi * s / m)))
    pts += left[::-1]
    ang1 = cmath.phase(normals[0])
    for s in range(1, m):
        pts.append(dense[0] + r * cmath.exp(1j * (ang1 + math.pi * s / m)))
    return pts


def lifted_intersection(loop1, loop2, rays):
    s1, c1, ok1 = sheet_profile(loop1, rays)
    s2, c2, ok2 = sheet_profile(loop2, rays)
    assert ok1 and ok2, "lift does not close"
    total = 0
    count = 0
    n1, n2 = len(loop1), len(loop2)
    for i in range(n1):
        p1, p2 = loop1[i], loop1[(i + 1) % n1]
        for j in range(n2):
            q1, q2 = loop2[j], loop2[(j + 1) % n2]
            r = seg_intersect(p1, p2, q1, q2)
            if r is None:
                continue
            t, u = r
            count += 1
            if sheet_at(s1, c1, i, t) == sheet_at(s2, c2, j, u):
                d1, d2 = p2 - p1, q2 - q1
                total += 1 if (d1.conjugate() * d2).imag > 0 else -1
    return total, count


def radial_rays(points, center=0j):
    rays = []
    for k, p in enumerate(points):
        d = p - center
        if abs(d) < 1e-9:
            d = cmath.exp(1j * (0.37 + k))
        d = d / abs(d) * cmath.exp(0.013j * (k + 1))  # avoid exact symmetries
        rays.append((p, d))
    return rays


def part_b1():
    print("== Part B1: genus-two bigon, arcs a, b from z0 to q5 with disjoint interiors")
    z0, q5 = -1 + 0j, 1 + 0j
    a = [z0, 0.0 + 0.6j, q5]
    b = [z0, 0.0 - 0.6j, q5]
    inside_slots = [-0.35 + 0.15j, 0.35 - 0.12j, 0.05 + 0.3j, -0.1 - 0.35j]
    outside_slots = [-2.1 + 1.3j, 2.3 + 1.1j, 1.9 - 1.7j, -2.2 - 1.4j]
    for n_in in range(0, 5):
        others = inside_slots[:n_in] + outside_slots[:4 - n_in]
        rays = radial_rays([z0, q5] + others, center=0.03 + 0.02j)
        la = racetrack(a, 0.05)
        lb = racetrack(b, 0.09)
        val, cnt = lifted_intersection(la, lb, rays)
        print(f"  branch points inside the bigon: {n_in}; delta(a).delta(b) = {val} "
              f"(downstairs crossings {cnt})")
    print()


def part_b2():
    print("== Part B2: genus-four hexagon Z1 P1 Z3 P3 Z2 P2 on the unit circle, 4 more poles")
    # vertex order around the circle: Z1, P1, Z3, P3, Z2, P2
    names = ["Z1", "P1", "Z3", "P3", "Z2", "P2"]
    pos = {nm: cmath.exp(1j * (math.pi / 3) * k) for k, nm in enumerate(names)}
    arcs_a = [("Z1", "P1"), ("Z2", "P2"), ("Z3", "P3")]          # a_i : Z_i -> P_i
    arcs_b = [("Z1", "P2"), ("Z2", "P3"), ("Z3", "P1")]          # b_i : Z_i -> P_{i+1}
    inside_slots = [0.2 + 0.1j, -0.25 + 0.15j, 0.05 - 0.3j, -0.1 - 0.05j]
    outside_slots = [2.0 + 0.7j, -1.8 + 1.5j, -0.4 - 2.2j, 1.6 - 1.6j]
    radii_a = [0.04, 0.05, 0.06]
    radii_b = [0.075, 0.085, 0.095]
    for n_in in range(0, 5):
        others = inside_slots[:n_in] + outside_slots[:4 - n_in]
        rays = radial_rays([pos[n] for n in names] + others, center=0.01 + 0.02j)
        la = [racetrack([pos[s], pos[t]], r) for (s, t), r in zip(arcs_a, radii_a)]
        lb = [racetrack([pos[s], pos[t]], r) for (s, t), r in zip(arcs_b, radii_b)]
        C = [[lifted_intersection(la[i], lb[j], rays)[0] for j in range(3)] for i in range(3)]
        aa = [lifted_intersection(la[i], la[k], rays)[0] for i in range(3) for k in range(3) if i < k]
        bb = [lifted_intersection(lb[i], lb[k], rays)[0] for i in range(3) for k in range(3) if i < k]
        prod = math.prod(C[i][j] for i, j in SUPPORT)
        print(f"  extra poles inside the hexagon: {n_in}; C = {C}; a.a = {aa}; b.b = {bb}; "
              f"product of six entries = {prod}; |det F| with these lifts = {abs(detF(C))}")
    print()


def part_c():
    print("== Part C: integer counts")
    g, z = 4, 3
    print(f"  z = 3: branch points 2z+4 = {2*z+4}, genus z+1 = {z+1}, "
          f"dim Q(1^3,-1^7) = 2z+2 = {2*z+2}, dim H(2,2,2) = 2g+z-1 = {2*g+z-1}, codim = {2*g+z-1-(2*z+2)}")
    print(f"  lower stratum Q(1^2,-1^6): orientation genus {2+1}, dim {2*2+2}")
    pf_max = 9
    pa_max = 1 + pf_max
    print(f"  birational image: p_a <= 1 + 9 = {pa_max}; available delta <= p_a - g = {pa_max - g}")
    print(f"  three branches with pairwise intersection >= 3: delta >= {3*3}")
    sols = []
    for gp in range(0, 5):
        for k in range(2, 7):
            ram = (2 * g - 2) - k * (2 * gp - 2)
            if ram >= 0 and gp >= 2:
                sols.append((gp, k, ram))
    print("  Riemann-Hurwitz (genus(Y) >= 2, k >= 2): (genus, degree, ramification) =", sols)
    print("  with k >= 3 forced by the common fiber:", [s for s in sols if s[1] >= 3])
    # pullback multiplies the unimodular genus-two cup form by k = 3: Pfaffian of 3*J4 = 9
    print("  Pfaffian of 3 * (standard rank-4 symplectic form) =", 3 * 3)
    # downstairs cover profile: degree 3 sphere -> sphere, 4 simple branch points over poles
    k, z0, n_poles_base = 3, 1, 5
    rh = -2 - (k * (-2) + 4)
    poles_up = 4 * 1 + 3
    print(f"  downstairs degree-3 cover of Q(1,-1^5): RH defect {rh} (0 means consistent), "
          f"zeros above = {k*z0}, poles above = {poles_up}, regular ramified points = 4")
    # divisor note: tree counts
    print("  rim trees for a one-cylinder sphere in Q(1^s,-1^(s+4)):")
    for s in range(1, 6):
        splits = [(k1, s - k1) for k1 in range(0, s + 1) if k1 >= s - k1]
        leaves_ok = all((k1 + 2) + (k2 + 2) == s + 4 for k1, k2 in splits)
        kmax_min = min(k1 for k1, _ in splits)
        print(f"    s={s}: splits {splits}; leaves sum to s+4: {leaves_ok}; "
              f"area-fraction bound 1/(ceil(s/2)+2) = {Fraction(1, kmax_min + 2)}")
    print()


if __name__ == "__main__":
    part_a()
    part_b1()
    part_b2()
    part_c()
