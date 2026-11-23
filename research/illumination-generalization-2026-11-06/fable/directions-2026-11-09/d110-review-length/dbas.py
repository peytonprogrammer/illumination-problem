"""D110 claims 2 and 3 on DBas (d69: rect(0,5,0,4)|rect(5,5+L,1,2)|rect(5+L,9+L,-1,5); L=4 is DBas).
Own tracer (geom.shoot) cross-checked against d109's path.shoot (cell-based)."""
import sys
from fractions import Fraction as F
from math import gcd
from pathlib import Path
from geom import room, shoot
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'd109-check-dbas'))
import path as P109
from room import cells


def both(L, S, d, T, maxev=200000):
    """Return (own result, d109 result): number of wall hits, or the error string."""
    out = []
    for f in (lambda: len(shoot(room('DBas', L)['V'], S, d, T, maxev)),
              lambda: len(P109.shoot(cells(L), S, (F(d[0]), F(d[1])), T, maxev))):
        try:
            out.append(f())
        except Exception as e:  # vertex hit or no arrival
            out.append(str(e)[:40])
    return out


def door_heights(L, S, d, T):
    hits = shoot(room('DBas', L)['V'], S, d, T)
    pts = [S] + [q for _, q in hits] + [T]
    hs = []
    for a, b in zip(pts, pts[1:]):
        for X in (5, 5 + L):
            if (a[0] - X) * (b[0] - X) < 0:
                hs.append((X, a[1] + (X - a[0]) * (b[1] - a[1]) / (b[0] - a[0])))
    return hs


def T_ins(p, q, w=1):
    return 1 if q == 0 else 2 * w * abs(p) // gcd(abs(q), 2 * w * abs(p))


print("== claim 2: DBas L=4, S=(1,3), T=(11,3), directions (7+1040j,-2) ==")
S, T = (F(1), F(3)), (F(11), F(3))
print("j=0 (7,-2):", both(4, S, (7, -2), T))
for j in (1, 2, 3):
    p = 7 + 1040 * j
    r = both(4, S, (p, -2), T)
    hs = door_heights(4, S, (p, -2), T) if isinstance(r[0], int) else []
    print(f"j={j} dir=({p},-2) T(p,q)={T_ins(p, -2)} reach: own/d109 = {r}; corridor crossings={len(hs)//2*2 and len(hs)}")
    assert T_ins(p, -2) == p
    # insertion test: lengthen the corridor by D, translate the right chamber and T
    for D in (p, 2 * p, 1, 2, p - 2):
        Tn = (T[0] + D, T[1])
        rr = both(4 + D, S, (p, -2), Tn, maxev=3 * 10 ** 4)
        print(f"     insert D={D}: same direction reaches translated T? own/d109 = {rr}")

print("\n== claim 3: DBas family, mark (1,3) -> (5+L+c,3) ==")


def mk(L):
    c = 2 if L % 2 == 0 else 1
    return (F(1), F(3)), (F(5 + L + c), F(3)), 8 - c


def branch2(L):
    """leftward branch: even integers k in ((L+6+b)/6, 2(L+6+b)/b); m = k/(L+6+b)."""
    S, T, b = mk(L)
    H = L + 6 + b
    return [k for k in range(1, 2 * H) if k % 2 == 0 and F(H, 6) < k < F(2 * H, b)], H


def branch1(L):
    S, T, b = mk(L)
    H = L + 4 + b
    return [k for k in range(1, 2 * H) if k % 2 == 0 and F(H, 4) < k < F(2 * H, b)], H


for L in (2, 3, 10, 45, 47):
    S, T, b = mk(L)
    ks, H = branch2(L)
    print(f"L={L} b={b} branch-2 interval ({F(H,6)},{F(2*H,b)}) even k: {ks}")
    for k in ks:
        m = F(k, H)
        d = (-m.denominator, -m.numerator)
        r = both(L, S, d, T)
        hs = door_heights(L, S, d, T)
        print(f"   k={k} m={m} dir={d} own/d109={r} door heights={[str(y) for _, y in hs]}")
        assert all(isinstance(z, int) for z in r) and all(1 < y < 2 for _, y in hs)
    k1, H1 = branch1(L)
    print(f"   branch-1 interval ({F(H1,4)},{F(2*H1,b)}) even k: {k1}")
    for k in k1:
        m = F(k, H1)
        d = (m.denominator, -m.numerator)
        r = both(L, S, d, T)
        print(f"   branch-1 k={k} m={m} own/d109={r}")
        assert all(isinstance(z, int) for z in r)
    if L == 45:
        for k in (14, 16):
            m = F(k, H1)
            print(f"   branch-1 endpoint k={k} m={m}: own/d109={both(L, S, (m.denominator, -m.numerator), T)}")
# displacement check at n=67,73,89
for L, k in ((23, 8), (29, 8), (45, 10)):
    S, T, b = mk(L); H = L + 6 + b
    print(f"L={L} k={k}: leftward developed displacement (-{H},-{k})")
# full scan of branch 2 for 2 <= L <= 300, own tracer, every admissible k
bad = []
for L in range(1, 301):
    S, T, b = mk(L)
    ks, H = branch2(L)
    if not ks:
        bad.append(L); continue
    for k in ks:
        m = F(k, H)
        shoot(room('DBas', L)['V'], S, (-m.denominator, -m.numerator), T)
print("branch-2 scan L=1..300: lengths with no even k:", bad, "; all admissible k traced to T")
