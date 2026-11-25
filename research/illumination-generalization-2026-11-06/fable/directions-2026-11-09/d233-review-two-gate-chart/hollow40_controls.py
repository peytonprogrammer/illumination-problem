"""D233 claim 7 controls: synthetic widened boxes on the same N=40 lattices (enumerator check only,
not a room search), brute-force k-enumeration cross-check, and the split covector of the monotone coset."""
import itertools, time
from fractions import Fraction as F
import importlib.util, sys
spec = importlib.util.spec_from_file_location("h", "hollow40.py")
src = open("hollow40.py").read().split("N = 40; B")[0]
ns = {}; exec(src, ns)
setup, enumerate_box = ns['setup'], ns['enumerate_box']
t0 = time.process_time()
N = 40; B = 82; x0, xT = 39, F(100)
mono = [(0, 40, 1), (39, 42, 82), (80, 40, 1)]
for eps in itertools.product((0, 1), repeat=3):
    v, Phi, sig, aux = setup(mono, x0, xT, eps)
    # split covector l=(1/80,1/80) in physical coordinates x_i = sig_i u_i
    s1, s2 = sig[1], sig[2]
    lv = (v[0] + v[1]) / 80
    # check l . Phi columns are integers -> l in dual lattice
    dual = all(((Phi[0][j] + Phi[1][j]) / 80).denominator == 1 for j in range(3))
    # projection of the folded box (s1*J1) x (s2*J2) under u1+u2, divided by 80
    J1 = sorted([s1 * 39, s1 * 40]); J2 = sorted([s2 * 80, s2 * 81])
    lo, hi = F(J1[0] + J2[0] , 80) - lv, F(J1[1] + J2[1], 80) - lv
    import math
    miss = math.floor(lo) + 1 >= hi
    print(f"parity {''.join(map(str,eps))}: (1/80,1/80) in dual={dual}; projected window minus offset=({lo},{hi}) width={hi-lo} miss={miss}")
# synthetic widened box that contains the projection hit (window must contain 139 mod 80 = 59 in u1+u2 at parity 000)
v, Phi, sig, aux = setup(mono, x0, xT, (0, 0, 0))
box = [(39, 40, False, False), (80, 101, False, False)]
hits, nodes, covol, L, _ = enumerate_box(v, Phi, sig, box, [0, 1])
# brute force over k in a range; dedupe event vectors
bf = set()
for k in itertools.product(range(-3, 4), range(-3, 4), range(-60, 61)):
    u = [v[i] + sum(Phi[i][j] * k[j] for j in range(3)) for i in range(2)]
    if 39 < u[0] < 40 and 80 < u[1] < 101: bf.add(tuple(u))
en = set(tuple(v[i] + sum(L[i][j] * z[j] for j in range(len(z))) for i in range(2)) for z in hits)
print(f"synthetic box (39,40)x(80,101), parity 000: enumerator hits={len(en)}, brute-force (|k0|,|k1|<=3,|k2|<=60) distinct points={len(bf)}, brute subset of enum={bf <= en}")
print("  example points", sorted(en)[:3])
# excursion lattice, synthetic widened gate 2 to (80,101)
ex = [(0, 40, 1), (39, 42, 82), (80, 40, 1), (80, 80, 1), (80, 80, 1)]
v, Phi, sig, aux = setup(ex, x0, xT, (0,) * 5)
hits, nodes, covol, L, _ = enumerate_box(v, Phi, sig, [(39, 40, False, False), (80, 101, False, False), (80, 120, True, False), (80, 160, False, False)], [0, 1, 2, 3])
print(f"excursion lattice, synthetic gate2=(80,101), parity 00000: hits={len(hits)}")
print(f"CPU seconds {time.process_time() - t0:.2f}")
