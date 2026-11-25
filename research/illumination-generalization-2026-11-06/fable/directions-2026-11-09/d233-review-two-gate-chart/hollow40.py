"""D233 claim 7: exact coset hollowness at N=40 (own code, no gatebox import).
Itinerary = visits (a_j, w_j, h_j), events (lo, hi, lo_closed, hi_closed).
Folded coordinates: u_{j+1} = u_j + p h_j - c_j - 2 w_j k_j, c_j = 0 or 2 sigma_j a_j,
u_{g+1} = sigma_{g+1} T_x, physical x_i = sigma_i u_i. Coset u = v + Phi k.
Enumeration: column HNF of the integer-scaled Phi gives a lower-triangular basis L,
u = v + L z, z in Z^g; then exact triangular slicing (each coordinate is an interval
given the previous ones). This is complete: every coset point is v + L z for a unique z."""
import sys, time, itertools, math
from fractions import Fraction as F
from math import floor, ceil, gcd

def egcd(a, b):
    if b == 0: return (abs(a), (1 if a >= 0 else -1), 0)
    g, x, y = egcd(b, a % b); return (g, y, x - (a // b) * y)

def col_hnf_lower(M):
    """M: g x m integer, rank g. Column ops -> lower triangular g x g basis of column lattice."""
    g, m = len(M), len(M[0]); A = [row[:] for row in M]
    for r in range(g):
        for c in range(r + 1, m):
            a, b = A[r][r], A[r][c]
            if b == 0: continue
            d, x, y = egcd(a, b)
            for i in range(g):
                cr, cc = A[i][r], A[i][c]
                A[i][r] = x * cr + y * cc
                A[i][c] = (-b // d) * cr + (a // d) * cc
        assert A[r][r] != 0, "rank deficient"
        if A[r][r] < 0:
            for i in range(g): A[i][r] = -A[i][r]
    for c in range(g, m): assert all(A[i][c] == 0 for i in range(g))
    return [[A[i][j] for j in range(g)] for i in range(g)]

def setup(visits, x0, xT, eps):
    g = len(visits) - 1
    h = [F(v[2]) for v in visits]; w = [F(v[1]) for v in visits]; a = [F(v[0]) for v in visits]
    Y = [sum(h[:i], F(0)) for i in range(g + 2)]; H = Y[g + 1]
    sig = [1]; c = []
    for j in range(g + 1):
        c.append(F(0) if eps[j] == 0 else 2 * sig[j] * a[j]); sig.append(sig[j] * (1 if eps[j] == 0 else -1))
    # k = 0 point
    p0 = (sig[g + 1] * F(xT) - F(x0) + sum(c)) / H
    v = [F(x0) + p0 * Y[i] - sum(c[:i], F(0)) for i in range(1, g + 1)]
    Phi = [[2 * w[j] * (Y[i] / H - (1 if j < i else 0)) for j in range(g + 1)] for i in range(1, g + 1)]
    return v, Phi, sig, (h, w, a, Y, H, c)

def enumerate_box(v, Phi, sig, events, order, limit=10**6):
    g = len(v)
    # physical x_i = sig[i] u_i in event i -> u_i interval = sig_i * J_i
    iv = []
    for i, (lo, hi, lc, hc) in enumerate(events):
        s = sig[i + 1]
        iv.append((F(lo), F(hi), lc, hc) if s == 1 else (-F(hi), -F(lo), hc, lc))
    # permute rows
    vP = [v[i] for i in order]; PhiP = [Phi[i] for i in order]; ivP = [iv[i] for i in order]
    Dn = 1
    for row in PhiP:
        for x in row: Dn = Dn * x.denominator // gcd(Dn, x.denominator)
    Mi = [[int(x * Dn) for x in row] for row in PhiP]
    L = col_hnf_lower(Mi)
    L = [[F(x, Dn) for x in row] for row in L]
    hits = []; nodes = [0]
    def rec(r, z, partial):
        if len(hits) >= limit: return
        nodes[0] += 1
        if r == g:
            hits.append(list(z)); return
        lo, hi, lc, hc = ivP[r]
        base = vP[r] + sum(L[r][j] * z[j] for j in range(r))
        d = L[r][r]  # >0
        zlo = (lo - base) / d; zhi = (hi - base) / d
        a_ = ceil(zlo) if lc else floor(zlo) + 1
        b_ = floor(zhi) if hc else ceil(zhi) - 1
        for zz in range(a_, b_ + 1):
            z.append(zz); rec(r + 1, z, None); z.pop()
    rec(0, [], None)
    covol = F(1)
    for i in range(g): covol *= L[i][i]
    return hits, nodes[0], covol, L, (vP, ivP)

N = 40; B = 2 * N + 2
x0, xT = N - 1, F(5 * N, 2)
t0 = time.process_time()
out = []
def log(s): print(s); out.append(s)

# monotone itinerary: slab [0,1] (0,N) h=1 ; middle (N-1,2N+1) h=B ; slab [1+B,2+B] (2N,3N) h=1 ; T at top
mono_visits = [(0, N, 1), (N - 1, N + 2, B), (2 * N, N, 1)]
mono_events = [(N - 1, N, False, False), (2 * N, 2 * N + 1, False, False)]   # both endpoints are corners
log(f"N={N} monotone itinerary: visits (a,w,h)={mono_visits}, gates={mono_events}")
lit_total = 0
for eps in itertools.product((0, 1), repeat=3):
    v, Phi, sig, aux = setup(mono_visits, x0, xT, eps)
    hits, nodes, covol, L, _ = enumerate_box(v, Phi, sig, mono_events, [0, 1])
    lit_total += bool(hits)
    log(f"  parity {''.join(map(str,eps))}: covol={covol} basis L={[[str(x) for x in r] for r in L]} nodes={nodes} hits={len(hits)}")
log(f"  monotone: lit parity cosets = {lit_total}/8")

# sanity of the enumerator (not a room/direction search): widen both gates by 1 on each side
v, Phi, sig, aux = setup(mono_visits, x0, xT, (0, 0, 0))
hits, nodes, covol, L, _ = enumerate_box(v, Phi, sig, [(N - 2, N + 1, False, False), (2 * N - 1, 2 * N + 2, False, False)], [0, 1])
log(f"  enumerator sanity, gates widened to (N-2,N+1)x(2N-1,2N+2), parity 000: hits={len(hits)}")
# positive control of the parametrization: the witness, all-even parity, k=0, must give u_i = x_i of the trace
wv = [(0, N, 1), (N - 1, N + 2, B)] + [(2 * N, N, 1), (2 * N, 2 * N, 1), (2 * N, 2 * N, 1), (2 * N, N, 1)] * ((N - 2) // 4) + [(2 * N, N, 1), (2 * N, 2*N, 1), (2*N, 2*N, 1)][: (N - 1) - 4 * ((N - 2) // 4)]
assert sum(x[2] for x in wv) == 1 + B + N - 1, sum(x[2] for x in wv)
v, Phi, sig, aux = setup(wv, x0, xT, (0,) * len(wv))
log(f"  witness k=0 even parity: g={len(v)}, p={(aux[4] and (xT - x0)/aux[4])}, first u={[str(x) for x in v[:4]]}, last u={[str(x) for x in v[-3:]]}")

# single excursion: roof bounce in the top tier, then down to T (arrive from above)
ex_visits = [(0, N, 1), (N - 1, N + 2, B), (2 * N, N, 1), (2 * N, 2 * N, 1), (2 * N, 2 * N, 1)]
ex_events = [(N - 1, N, False, False), (2 * N, 2 * N + 1, False, False),
             (2 * N, 3 * N, True, False),      # level 2+B: x=2N smooth wall point (closed), 3N reflex corner
             (2 * N, 4 * N, False, False)]     # roof y=3+B, whole outer face, corner endpoints
log(f"N={N} single excursion (top roof bounce, T reached from above): visits={ex_visits}, events={ex_events}")
lit_total = 0; tot_nodes = 0
for eps in itertools.product((0, 1), repeat=5):
    v, Phi, sig, aux = setup(ex_visits, x0, xT, eps)
    hits, nodes, covol, L, _ = enumerate_box(v, Phi, sig, ex_events, [0, 1, 2, 3])
    lit_total += bool(hits); tot_nodes += nodes
    if hits: log(f"  parity {''.join(map(str,eps))}: HIT {hits[:3]}")
log(f"  excursion: lit parity cosets = {lit_total}/32 (enumeration nodes {tot_nodes}, covol at last parity {covol})")
log(f"CPU seconds {time.process_time() - t0:.2f}")
