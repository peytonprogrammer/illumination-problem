"""Independent checks for the d207 snapshot (area bound for a BBBB dark pair).

Cell-incidence arithmetic on the three named control rooms only, plus the
closed-form integer checks. No rooms, rays, directions or words are searched.
"""
from fractions import Fraction as F
from itertools import combinations
from math import ceil, floor

ROOMS = {
    # d29-rigidity-test/control22.sv (cells after '|'), S=(1,3), T=(3,5)
    "R22": [(0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 4),
            (2, 5), (3, 4), (3, 5), (4, 3), (4, 4), (5, 3)],
    # d66-pair-level/README.md section 7
    "cov4181": [(0, y) for y in range(6)] + [(1, 2), (1, 3), (2, 2), (2, 3)]
    + [(3, y) for y in range(6)] + [(4, y) for y in range(6)]
    + [(5, 2), (5, 3), (6, 2), (7, 0), (7, 1), (7, 2)],
    # d69-bbbb/README.md section 3 picture (row strings, x left to right)
    "cov2929": None,
}
PIC2929 = {5: "....##.#", 4: "....####", 3: "..####..", 2: "..####..",
           1: "####....", 0: "#.##...."}
ROOMS["cov2929"] = [(x, y) for y, row in PIC2929.items() for x, ch in enumerate(row) if ch == "#"]

CLASSES = [(0, 0), (0, 1), (1, 0), (1, 1)]  # physical parity order 00,01,10,11


def incidence(cells):
    cs = set(cells)
    pts = {(x + dx, y + dy) for x, y in cs for dx in (0, 1) for dy in (0, 1)}
    cnt = {y: dict(v=0, s=0, r=0, i=0) for y in CLASSES}
    for (px, py) in pts:
        nb = [(px - 1, py - 1), (px, py - 1), (px - 1, py), (px, py)]  # SW SE NW NE
        k = sum(c in cs for c in nb)
        if k == 2 and ((nb[0] in cs) == (nb[3] in cs)):
            raise ValueError(f"pinch at {(px, py)}")
        key = {1: "v", 2: "s", 3: "r", 4: "i"}[k]
        cnt[(px % 2, py % 2)][key] += 1
    return cnt


def ftarget(n, r=8):
    return 2 * ceil(F(2 * n, 3)) - 2 * r - n // 2


def main():
    print("== Claim 1: per-class identities and Claim 3: two-class estimate ==")
    for name, cells in ROOMS.items():
        n = len(cells)
        cnt = incidence(cells)
        r = sum(c["r"] for c in cnt.values())
        v = sum(c["v"] for c in cnt.values())
        m = {y: cnt[y]["s"] + 2 * cnt[y]["i"] for y in CLASSES}
        c = {y: cnt[y]["v"] + 3 * cnt[y]["r"] for y in CLASSES}
        assert v == r + 4, (name, v, r)
        for y in CLASSES:
            assert n == c[y] + 2 * m[y], (name, y)
        assert sum(c.values()) == 4 * r + 4
        assert sum(m.values()) == 2 * (n - r - 1)
        print(f"{name}: n={n} r={r} W={2*r+4}")
        for y in CLASSES:
            print(f"   class {y}: v={cnt[y]['v']} s={cnt[y]['s']} r={cnt[y]['r']} "
                  f"i={cnt[y]['i']}  c={c[y]} m={m[y]}")
        best = None
        for I in combinations(CLASSES, 2):
            out = [y for y in CLASSES if y not in I]
            M = sum(m[y] for y in I)
            t = sum(cnt[y]["r"] for y in out)
            vout = sum(cnt[y]["v"] for y in out)
            assert (3 * t + vout) % 2 == 0
            assert n == 2 * r + 2 + M - (3 * t + vout) // 2
            U = 2 * r + 2 + M - ceil(F(3 * t, 2))
            assert U - n == vout // 2
            print(f"   I={I}: M={M} t={t} v_out={vout} U={U} U-n={U-n}")
            if best is None or U < best[0]:
                best = (U, I, M, t)
        print(f"   min U = {best[0]} at I={best[1]} (M={best[2]}, t={best[3]}); "
              f"pass 25: {best[0] <= 25}; Q classes: {[y for y in CLASSES if m[y]==0]}")

    print("\n== Claim 2: f(n) = 2*ceil(2n/3) - 16 - floor(n/2) ==")
    print("   n:", {n: ftarget(n) for n in range(18, 56)})
    assert all(ftarget(n) >= 26 for n in range(49, 49 + 6))
    assert all(ftarget(n + 6) == ftarget(n) + 5 for n in range(0, 200))
    assert all(ftarget(n) >= 7 for n in range(26, 32)) and ftarget(25) == 6
    print("   min f on n>=49 (one residue period):", min(ftarget(n) for n in range(49, 55)))
    print("   min f on n>=26 (one residue period):", min(ftarget(n) for n in range(26, 32)))
    print("   f(48) =", ftarget(48), "(so H<=25 does not exclude n=48)")

    print("\n== Claim 4: fixed points of tau(u)=u+e on (R^2/2Z^2)/{+-1} ==")
    for e in [(1, 0), (0, 1), (1, 1)]:
        # solve 2u = e mod 2 on the torus R^2/2Z^2: u = e/2 + Z^2 mod 2
        sols = [((F(e[0], 2) + a) % 2, (F(e[1], 2) + b) % 2) for a in (0, 1) for b in (0, 1)]
        for u in sols:
            assert ((2 * u[0] - e[0]) % 2, (2 * u[1] - e[1]) % 2) == (0, 0)
            assert ((-u[0]) % 2, (-u[1]) % 2) != u  # not a pole (no sign-fixed u)
        orbits = {min(u, ((-u[0]) % 2, (-u[1]) % 2)) for u in sols}
        assert len(orbits) == 2
        # brute check over a half-integer grid that there are no other fixed points
        grid = [(F(i, 2), F(j, 2)) for i in range(4) for j in range(4)]
        fixed = [u for u in grid if ((u[0] + e[0] + u[0]) % 2, (u[1] + e[1] + u[1]) % 2) == (0, 0)]
        assert sorted(fixed) == sorted(sols)
        print(f"   e={e}: torus solutions {[(str(a), str(b)) for a, b in sols]}, "
              f"base points {len(orbits)}: {[(str(a), str(b)) for a, b in sorted(orbits)]}")

    # midpoint relation: -(T* - v t) + e == S + v t mod 2 whenever T* = T mod 2, e = T - S
    for S in [(0, 0), (1, 0), (0, 1), (1, 1)]:
        for T in [(0, 0), (1, 0), (0, 1), (1, 1)]:
            if S == T:
                continue
            e = ((T[0] - S[0]) % 2, (T[1] - S[1]) % 2)
            for Tst in [(T[0] + 2 * a, T[1] + 2 * b) for a in (-1, 0, 1) for b in (-1, 0, 1)] + \
                       [(-T[0], -T[1])]:
                for j in (0, 1):
                    assert ((-Tst[j] + e[j] - S[j]) % 2) == 0
    print("   development relation -(T*-vt)+e = S+vt mod 2: ok for all parity pairs")


if __name__ == "__main__":
    main()
