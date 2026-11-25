"""D233 checks: claim 2 rectangle, claims 3-4 room geometry, claim 6 witness traces.
Exact Fractions. Named rooms only: N in {40, 42, 100}."""
import sys, time
from fractions import Fraction as F
sys.path.insert(0, '../d231-review-gate-box')
import gatebox as gb

t0 = time.process_time()
# ---------------- claim 2: the rectangle
v0 = (F(1, 2), F(-1, 100)); e1 = (F(6), F(3, 5)); e2 = (F(-1, 50), F(1, 5))
print("claim2 dot(e1,e2) =", e1[0]*e2[0] + e1[1]*e2[1])
verts = [v0, (v0[0]+e1[0], v0[1]+e1[1]), (v0[0]+e2[0], v0[1]+e2[1]), (v0[0]+e1[0]+e2[0], v0[1]+e1[1]+e2[1])]
print("claim2 vertices", [tuple(map(str, p)) for p in verts])
ys = [p[1] for p in verts]; print("claim2 y-span", min(ys), max(ys))
# slice at y=0: s*0.6 + t*0.2 = 0.01, 0<s,t<1 ; x = 0.5 + 6 s - 0.02 t ; param by t
# s = (1/100 - t/5)/(3/5) ; need 0<s<1 and 0<t<1
tlo, thi = F(0), min(F(1), F(1, 100) / F(1, 5))  # s>0 <=> t<1/20 ; s<1 automatic
xs = [v0[0] + 6*((F(1,100) - t/5)/F(3,5)) - t/50 for t in (tlo, thi)]
print("claim2 row y=0 open x-slice endpoints", sorted(xs), "contains integer:", any(sorted(xs)[0] < n < sorted(xs)[1] for n in range(-2, 10)))
# width identity and lower bound for p != 0 (finite symbolic check of the two cases done in review.md);
# here: check identity on a grid and min over |p|,|q|<=60 (not a search over rooms; this is the rectangle's own dual)
best = None
for p in range(-60, 61):
    for q in range(-60, 61):
        if p == 0 and q == 0: continue
        wdir = abs(p*e1[0] + q*e1[1]) + abs(p*e2[0] + q*e2[1])
        assert wdir == F(3,5)*abs(10*p+q) + F(1,50)*abs(-p+10*q)
        if p != 0: assert wdir > 1
        # projection miss test: open interval (min, max) of p*x+q*y over closed rect vertices
        vals = [p*P[0] + q*P[1] for P in verts]; lo, hi = min(vals), max(vals)
        import math
        miss = math.floor(lo) + 1 >= hi
        if miss: print("claim2 PROJECTION MISS at", p, q)
        if best is None or wdir < best[0]: best = (wdir, p, q, lo, hi)
print("claim2 min width over |p|,|q|<=60:", best[0], "at", best[1:3], "projection", best[3], best[4])

# ---------------- claims 3,4,6
def room(N):
    B = 2*N + 2
    tiers = [(-1, 0, 0, F(5*N, 2)), (0, 1, 0, N), (1, 1+B, N-1, 2*N+1), (1+B, 2+B, 2*N, 3*N), (2+B, 3+B, 2*N, 4*N)]
    tiers = [tuple(F(x) for x in t) for t in tiers]
    return gb.room_from_tiers(tiers), B

for N in (40, 42, 100):
    V, B = room(N)
    refl, area = gb.check_room(V)
    A, C, Dd, E, Fs, G, H, J = 0, N-1, N, 2*N, 2*N+1, F(5*N, 2), 3*N, 4*N
    order = A < C < Dd < E < Fs < G < H < J
    S = (F(N-1), F(0)); T = (F(5*N, 2), F(2+B))
    print(f"N={N}: walls={len(V)} reflex={refl} area={area} strict-order={order} S interior={gb.interior(V,S)} T interior={gb.interior(V,T)}")
    print("   vertices", [(str(x), str(y)) for x, y in V])
    levels = [F(-1), F(0), F(1), F(1+B), F(2+B), F(3+B)]
    Htot = 1 + B + (N - 1)
    st, ev, end = gb.trace(V, S, T, F(1, 2), F(1), Htot, levels)
    R = [e for e in ev if e[2] == 'R']
    onw = [e for e in ev if e[3]]
    # vertical-wall reflections: the tracer records them only when on a level; recompute by checking vx sign:
    # vx stays +1/2 iff every recorded x is increasing in time
    xseq = [e[1] for e in ev]
    mono = all(xseq[i] < xseq[i+1] for i in range(len(xseq)-1))
    print(f"   witness: status={st} end={tuple(map(str,end))} ==T:{end==T} events={len(ev)} axial reversals={len(R)} (N/2-1={N//2-1}) on-wall-level events={len(onw)} x strictly increasing={mono}")
    print("   first events", [(str(L), str(x), k) for (L, x, k, _) in ev[:6]], "last", [(str(L), str(x), k) for (L, x, k, _) in ev[-3:]])
    # predicted: crossings N-1/2 at y=1, 2N+1/2 at 1+B; floor hits 2N+5/2+2k; roof 2N+3/2+2k; crossings of 2+B at 2N+1+k
    pred_ok = ev[0][:3] == (F(1), N - F(1,2), 'T') and ev[1][:3] == (F(1+B), 2*N + F(1,2), 'T')
    floors = [e[1] for e in R if e[0] == 1+B]; roofs = [e[1] for e in R if e[0] == 3+B]
    pred_ok &= floors == [2*N + F(5,2) + 2*k for k in range(len(floors))]
    pred_ok &= roofs == [2*N + F(3,2) + 2*k for k in range(len(roofs))]
    c4 = [e[1] for e in ev if e[0] == 2+B]
    pred_ok &= c4 == [2*N + 1 + k for k in range(len(c4))]
    pred_ok &= all(2*N+1 < x < 3*N for x in floors) and all(2*N < x < 3*N for x in c4)
    print(f"   matches note's predicted abscissas: {pred_ok}; floor hits={len(floors)} roof hits={len(roofs)} passes of y=2+B={len(c4)}")
    # transverse decomposition: crossings of the vertical support lines x in {D,E,F}
    # x(t) = N-1 + t/2 with t = absolute axial travel; y via event list is folded, so report travel
    for xl in (Dd, E, Fs):
        t = 2*(xl - (N-1)); print(f"   crosses x={xl} at axial travel {t} (lower leg ends 1, middle ends {1+B})")
    # obstruction consistency: A_s=1, A_t=N-1, p=1/2
    As, At, p = 1, N-1, F(1,2)
    d1 = min(abs(As*p - N*m) for m in range(-2, 3)); d2 = min(abs(At*p - F(N,2) - N*m) for m in range(-3, 3))
    print(f"   obstruction check: dist(A_s p,NZ)={d1}<=2 {d1<=2}; dist(A_t p,N/2+NZ)={d2}<=1 {d2<=1}; N/2<=2A_t+A_s {F(N,2) <= 2*At+As}")
print("CPU seconds", round(time.process_time() - t0, 2))
