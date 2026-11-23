"""Independent exact checks of individual proof steps.

C1  Closed-star triangles (3c >= 2n), n <= 24: every tile that shares a
    boundary edge with a star is incompatible with the star.
C2  Right triangles n = 8..24 (case 2): build t1, y, w_near, w_far, N, F
    exactly as in the proof and test the claimed incompatibilities.
C3  Classification: E, closed-star, right, (8,2), 60-degree, generic, for
    n <= 60; and the smallest generic obtuse triangle.
"""
import json
from math import gcd

from geom import Triangle, star, mirror, compatible, Tile


def classify(n, b):
    c = n - 1 - b
    E = [V for V, v in (("B", b), ("C", c)) if n % v == 0 and (n // v) % 2 == 0]
    if 3 * c >= 2 * n:
        cls = "closed-star"
    elif 2 * c == n:
        cls = "right"
    elif n % b == 0:
        cls = "b|n"
    else:
        cls = "generic"
    return cls, E


def c1():
    out = {}
    for n in range(4, 25, 2):
        for b in range(1, n):
            c = n - 1 - b
            if not (b < c) or 3 * c < 2 * n:
                continue
            tri = Triangle(n, b)
            st = star(tri, tri.F.zero)
            bad = 0
            for t in st:
                m = mirror(tri, t, "BC")
                if all(compatible(tri, m, s) for s in st):
                    bad += 1
            out[f"{n},{b}"] = bad
    return {"attachable_tiles_per_triangle": out, "PASS": all(v == 0 for v in out.values())}


def c2():
    res = {}
    for n in range(8, 25, 2):
        b = n // 2 - 1
        tri = Triangle(n, b)
        F = tri.F
        st = star(tri, F.zero)
        # pick star tile with B at the B-tip on angle 0 and its C-tip
        s_i = [t for t in st if t.s == 1 and t.k == 0][0]   # (S, B, C_i)
        t1 = mirror(tri, s_i, "BC")                          # exit tile (M, B, C_i)
        y = mirror(tri, t1, "AB")                            # (M, B, C')
        w_near = mirror(tri, y, "BC")
        y_alt = mirror(tri, y, "AC")                         # across M C'
        w_far = mirror(tri, y_alt, "BC")
        B = s_i.V["B"]
        s_j = [t for t in st if t.V["B"] == B and t.key != s_i.key][0]   # (S, B, C_j)
        N = mirror(tri, s_j, "BC")
        s_j2 = [t for t in st if t.V["C"] == s_j.V["C"] and t.key != s_j.key][0]
        Ftile = mirror(tri, s_j2, "BC")
        r = {
            "w_far is point reflection of y in C'": w_far.V["C"] == y.V["C"]
                and F.add(w_far.V["A"], y.V["A"]) == F.smul(2, y.V["C"]),
            "F vs w_far compatible": compatible(tri, Ftile, w_far),
            "N vs w_near compatible": compatible(tri, N, w_near),
            "N vs w_far compatible": compatible(tri, N, w_far),
            "F vs w_near compatible": compatible(tri, Ftile, w_near),
            "tiles at B (star2 + t1 + y)": 4,
            "fifth tile at B fits (5b <= 2n)": 5 * b <= 2 * n,
        }
        res[n] = r
    ok = all(not v["F vs w_far compatible"] for v in res.values())
    ok8 = not any(res[8][k] for k in ("N vs w_near compatible", "N vs w_far compatible", "F vs w_near compatible", "F vs w_far compatible"))
    return {"per_n": res, "PASS_F_wfar_all_n>=8": ok, "PASS_n8_all_four_pairs_overlap": ok8}


def c3():
    rows = []
    for n in range(4, 61, 2):
        for b in range(1, n):
            c = n - 1 - b
            if b >= c:
                continue
            cls, E = classify(n, b)
            rows.append((n, b, c, cls, E))
    cnt = {}
    for r in rows:
        cnt[r[3]] = cnt.get(r[3], 0) + 1
    bn = [(n, b) for n, b, c, cls, E in rows if cls == "b|n"]
    sixty = all(3 * b == n or (n, b) == (8, 2) for n, b in bn)
    nonempty_E = sorted({(n, b) for n, b, c, cls, E in rows if E and cls not in ("closed-star",)})
    gen = [(n, b) for n, b, c, cls, E in rows if cls == "generic"]
    return {"counts": cnt, "b|n obtuse are exactly 3b=n or (8,2)": sixty,
            "E nonempty outside closed-star (n<=60)": [list(x) for x in nonempty_E if x[0] <= 60][:40],
            "smallest generic": gen[:5]}


if __name__ == "__main__":
    out = {"C1": c1(), "C2": c2(), "C3": c3()}
    json.dump(out, open("checks.json", "w"), indent=1, default=str)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk not in ("per_n", "attachable_tiles_per_triangle")} for k, v in out.items()}, indent=1, default=str))
    print("C2 n=8:", out["C2"]["per_n"][8])
    print("C2 n=10:", out["C2"]["per_n"][10])
