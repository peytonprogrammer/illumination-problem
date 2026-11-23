"""d120 referee checks for rank-two-periodic.snapshot.md.

No discovery search. Three exact or numerical sanity checks:
  A. Genus, Weierstrass, dimension and form-divisor bookkeeping for z = 1..8.
  B. Degree-two branch: explicit sphere models of both deck cases.
  C. Axis-interval lemma: winding-number identity on a symmetric loop.
"""
import cmath
import math
import random
from math import comb

random.seed(20261120)

print("A. Bookkeeping for Y in Q(1^z, -1^(z+4)), X its orientation double")
print(" z  g  W=2g+2  2g-2  dimQ  rankQ  hr-thresh  dimPM  dimA2  "
      "#forms  Pdim  codim  exp.dim")
for z in range(1, 9):
    g = z + 1
    weier = 2 * z + 4                       # odd singularities = branch points
    assert weier == 2 * g + 2
    assert 2 * z == 2 * g - 2               # z double zeros of omega
    dim_q = (z + (z + 4)) - 2               # genus-zero stratum, n points
    rank_q = dim_q // 2                     # rel = 0 for all-simple genus 0
    hr = g / 2 + 1                          # Apisa-Wright high-rank threshold
    dim_pm = 2 * 2 + 0 - 1                  # rank 2, rel 0, projectivized
    dim_a2 = 3
    # Local orders of p(x)dx/y, p = prod_{i<=z}(x-a_i), y^2 = prod_{2g+2}(x-a_j).
    # At a root of p: x-a = t^2, y ~ t, dx = 2t dt  -> order 2 + 1 - 1 = 2.
    # At an infinity point: x = 1/s, y ~ s^-(g+1), dx ~ s^-2 ds.
    ord_branch = 2 * 1 + 1 - 1
    ord_inf = -z + (g + 1) - 2
    assert ord_branch == 2 and ord_inf == 0
    assert z * ord_branch + 2 * ord_inf == 2 * g - 2
    n_forms = comb(weier, z)                # finite choices of [omega] on fixed X
    pdim = g - 1                            # P(H^0(K_X))
    codim = pdim - 1                        # line through a fixed point of P^pdim
    print(f"{z:2d} {g:2d}  {weier:5d}  {2*g-2:4d}  {dim_q:4d}  {rank_q:5d}  "
          f"{hr:9.1f}  {dim_pm:5d}  {dim_a2:5d}  {n_forms:6d}  {pdim:4d}  "
          f"{codim:5d}  {dim_a2 - codim:7d}")
print("  rankQ = g, so rank 2 is proper for z >= 2; hr-thresh > 2 for g >= 4.")
print("  exp.dim = heuristic dimension of the zero-pattern locus over A_2;")
print("  a minimal rank-two locus needs exp.dim = 3 identically.")

print()
print("B. Degree-two branch on explicit sphere models")


def rnd_upper():
    return complex(random.uniform(-3, 3), random.uniform(0.05, 3))


def rnd_disk():
    r = math.sqrt(random.uniform(0.0025, 0.95))
    return r * cmath.exp(1j * random.uniform(0, 2 * math.pi))


cases = {
    # halves = upper/lower half-planes, seam = real line
    "exchange": dict(iota=lambda w: w.conjugate(), delta=lambda w: 1 / w,
                     f=lambda w: w + 1 / w, tau=lambda u: u.conjugate(),
                     sample=rnd_upper, fixed=[1, -1]),
    # halves = unit disk / its exterior, seam = unit circle
    "preserve": dict(iota=lambda w: 1 / w.conjugate(), delta=lambda w: -w,
                     f=lambda w: w * w, tau=lambda u: 1 / u.conjugate(),
                     sample=rnd_disk, fixed=[0]),
}
for name, c in cases.items():
    io, de, f, tau = c["iota"], c["delta"], c["f"], c["tau"]
    bad_comm = bad_equiv = bad_iff = 0
    collapses = 0
    for _ in range(20000):
        s = c["sample"]()
        if abs(de(io(s)) - io(de(s))) > 1e-9:
            bad_comm += 1
        if abs(f(io(s)) - tau(f(s))) > 1e-9:
            bad_equiv += 1
        real_u = abs(tau(f(s)) - f(s)) < 1e-9
        collapse = abs(de(s) - io(s)) < 1e-9
        bad_iff += real_u != collapse
    # forced collapse: put s on the axis (fixed set of iota*delta in the half)
    if name == "exchange":
        for _ in range(2000):
            s = cmath.exp(1j * random.uniform(0.01, math.pi - 0.01))
            u = f(s)
            collapses += abs(tau(u) - u) < 1e-9 and abs(de(s) - io(s)) < 1e-9
    print(f"  {name:8s}: commute fails {bad_comm}, f.iota=tau.f fails "
          f"{bad_equiv}, (tau u=u) != (delta s=iota s) {bad_iff}, "
          f"axis collapses {collapses}")
    for p in c["fixed"]:
        u = f(complex(p))
        print(f"    ramification {p}: branch value {u}, tau-fixed "
              f"{abs(tau(u) - u) < 1e-9 if u != 0 else 'n/a (0 <-> inf)'}")
print("  preserve: branch values 0 and inf are swapped by tau(u)=1/conj(u),")
print("  so they form the unique nonreal (off-seam) branch pair.")

print()
print("C. Axis lemma: winding of gamma * reflect(gamma)^-1 about p on the axis")
# Axis = real line, p = 0, a < 0 < b on the axis, gamma random path a -> b.
odd = 0
trials = 500
for _ in range(trials):
    a, b = -random.uniform(0.5, 2), random.uniform(0.5, 2)
    pts = [complex(a, 0)]
    for _ in range(40):
        pts.append(complex(random.uniform(-3, 3), random.uniform(-3, 3)))
    pts.append(complex(b, 0))
    pts = [q for q in pts if abs(q) > 1e-3]
    loop = pts + [q.conjugate() for q in reversed(pts)][1:]
    w = 0.0
    for q0, q1 in zip(loop, loop[1:]):
        w += cmath.phase(q1 / q0)
    n = round(w / (2 * math.pi))
    odd += n % 2 == 1
print(f"  loops with odd winding: {odd}/{trials}")
print("  Odd winding means the loop encloses p, so a simply connected")
print("  symmetric room has no gap point: the axis meets it in one interval.")
