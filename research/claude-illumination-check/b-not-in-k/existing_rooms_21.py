"""(2,1) slide loads for every literal pocket in the 57 existing rooms.

Fixed-room check approved by Daniel on 2026-11-02. Rooms: the 31 rooms of
seed-unbounded/study.jsonl and the 26 of seed-unbounded/res_rooms.jsonl, no new
rooms. Direction: (2,1) only, fixed in advance. A literal pocket follows
pocket-detection.md Section 1: a leaf triangle B,A,C attached through its axial
edge BC, with the wall continuing straight past B and past C. Each pocket is
moved by a lattice symmetry onto the Section 33 position, then core_loads.py
traces every (2,1) core that meets D. A second tracer reflects off the polygon's
own unit wall segments and must reproduce hits, D, H, and Q for every core.
"""
import json
import sys
from fractions import Fraction as F
import importlib.util

spec = importlib.util.spec_from_file_location("cl", "core_loads.py")
cl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cl)

SEED = "../seed-unbounded/"
THETA = (2, 1)


def unit_points(V):
    pts = []
    for (px, py), (qx, qy) in zip(V, V[1:] + V[:1]):
        dx, dy = qx - px, qy - py
        n = max(abs(dx), abs(dy))
        assert dx == 0 or dy == 0 or abs(dx) == abs(dy)
        sx, sy = (dx > 0) - (dx < 0), (dy > 0) - (dy < 0)
        pts += [(px + k * sx, py + k * sy) for k in range(n)]
    return pts


def inside_poly(V, p):
    x, y = p
    c = False
    for (ax, ay), (bx, by) in zip(V, V[1:] + V[:1]):
        if (ay > y) != (by > y):
            xi = ax + F(y - ay) * (bx - ax) / (by - ay)
            if xi > x:
                c = not c
    return c


def pockets(V):
    out = []
    for pts in (unit_points(V), unit_points(V)[::-1]):
        n = len(pts)
        for i in range(n):
            B, A, C = pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
            sub = lambda p, q: (p[0] - q[0], p[1] - q[1])
            if A[0] % 2 or A[1] % 2:
                continue
            ab, ca, cb = sub(A, B), sub(C, A), sub(C, B)
            if abs(ab[0]) != 1 or abs(ab[1]) != 1 or abs(ca[0]) + abs(ca[1]) != 1 or abs(cb[0]) + abs(cb[1]) != 1:
                continue
            if pts[i - 1] != sub(B, cb) or pts[(i + 3) % n] != (C[0] + cb[0], C[1] + cb[1]):
                continue
            if inside_poly(V, (F(A[0] + B[0] + C[0], 3), F(A[1] + B[1] + C[1], 3))):
                out.append((B, A, C))
    return out


def to_s33(B, A, C):
    for g in cl.D4:
        ga = cl.matvec(g, A)
        t = (2 - ga[0], 0 - ga[1])
        f = lambda p: (cl.matvec(g, p)[0] + t[0], cl.matvec(g, p)[1] + t[1])
        if f(B) == (1, 1) and f(C) == (1, 0):
            return f
    raise AssertionError


def triangles(V):
    xs, ys = [p[0] for p in V], [p[1] for p in V]
    tris = []
    for i in range(min(xs), max(xs)):
        for j in range(min(ys), max(ys)):
            if (i - j) % 2 == 0:
                cand = [((i, j), (i + 1, j), (i + 1, j + 1)), ((i, j), (i + 1, j + 1), (i, j + 1))]
            else:
                cand = [((i, j), (i + 1, j), (i, j + 1)), ((i + 1, j), (i + 1, j + 1), (i, j + 1))]
            for t in cand:
                if inside_poly(V, (F(sum(p[0] for p in t), 3), F(sum(p[1] for p in t), 3))):
                    tris.append(t)
    return tris


def shoelace2(V):
    return abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(V, V[1:] + V[:1])))


# Second tracer: polygon unit wall segments and a polygon inside test.
def hit(z, v, seg):
    (ax, ay), (bx, by) = seg
    ex, ey = bx - ax, by - ay
    den = v[0] * ey - v[1] * ex
    if den == 0:
        return None
    t = F((ax - z[0]) * ey - (ay - z[1]) * ex) / den
    s = F((ax - z[0]) * v[1] - (ay - z[1]) * v[0]) / den
    if t <= 0 or s < 0 or s > 1:
        return None
    assert 0 < s < 1, "path meets a wall endpoint"
    return t, seg


def reflect(v, seg):
    (ax, ay), (bx, by) = seg
    ex, ey = bx - ax, by - ay
    k = F(2 * (v[0] * ex + v[1] * ey), ex * ex + ey * ey)
    return (k * ex - v[0], k * ey - v[1])


def lin_of(seg):
    (ax, ay), (bx, by) = seg
    ex, ey = bx - ax, by - ay
    n2 = ex * ex + ey * ey
    return ((F(ex * ex - ey * ey, n2), F(2 * ex * ey, n2)), (F(2 * ex * ey, n2), F(ey * ey - ex * ex, n2)))


DSEG, HSEG = ((1, 1), (2, 0)), ((1, 0), (2, 0))


def second_trace(W, V, z0, v0):
    L0 = cl.frame_to(THETA, v0)
    L = tuple(tuple(F(x) for x in r) for r in L0)
    z, v = z0, v0
    Q = [F(0), F(0)]
    nD = nH = hits = 0
    while True:
        t, seg = min((h for h in (hit(z, v, w) for w in W) if h), key=lambda h: h[0])
        p = (z[0] + t * v[0], z[1] + t * v[1])
        assert inside_poly(V, ((z[0] + p[0]) / 2, (z[1] + p[1]) / 2)), "segment leaves the room"
        hits += 1
        if seg in (DSEG, HSEG):
            a = (1, 1) if seg == DSEG else (0, 2)
            Q[0] += L[0][0] * a[0] + L[0][1] * a[1]
            Q[1] += L[1][0] * a[0] + L[1][1] * a[1]
            nD += seg == DSEG
            nH += seg == HSEG
        L = cl.matmul(L, lin_of(seg))
        v = reflect(v, seg)
        z = p
        if z == z0 and v == v0 and L == L0:
            return hits, nD, nH, [int(Q[0]), int(Q[1])]


def main():
    rooms = [("study", k, json.loads(l)) for k, l in enumerate(open(SEED + "study.jsonl"))]
    rooms += [("res", k, json.loads(l)) for k, l in enumerate(open(SEED + "res_rooms.jsonl"))]
    out, mismatches = [], 0
    for src, k, r in rooms:
        V = [tuple(p) for p in r["V"]]
        for B, A, C in pockets(V):
            f = to_s33(B, A, C)
            V2 = [f(p) for p in V]
            tris = triangles(V2)
            assert len(tris) == shoelace2(V2), "triangle area differs from polygon area"
            cl.TRIANGLES = tris
            cl.ROOM = {cl.key(F(sum(p[0] for p in t), 3), F(sum(p[1] for p in t), 3)) for t in tris}
            assert cl.key(F(4, 3), F(1, 3)) in cl.ROOM
            d = cl.run_direction(THETA)
            pts = unit_points(V2)
            W = [tuple(sorted(s)) for s in zip(pts, pts[1:] + pts[:1])]
            assert DSEG in W and HSEG in W
            for c in d["cores"]:
                x0 = F(c["start_x_on_D"])
                got = second_trace(W, V2, (x0, 2 - x0), tuple(c["start_velocity"]))
                want = (c["wall_hits"], c["D_hits"], c["H_hits"], c["Q"])
                mismatches += got != want
            qs = [c["Q"] for c in d["cores"]]
            out.append({"room": f"{src}{k}", "W": len(V), "pocket_BAC": [B, A, C], "triangles": len(tris),
                        "cores_meeting_D": len(qs), "loaded": sum(q != [0, 0] for q in qs),
                        "odd": sum(q[0] % 2 != 0 for q in qs), "Q": qs, "strip_sum": d["strip_weighted_sum"]})
    json.dump({"theta": THETA, "pockets": out, "second_tracer_mismatches": mismatches},
              open(sys.argv[1], "w"), indent=1, default=str)
    rooms_with = sorted({p["room"] for p in out}, key=lambda s: (s[0], int(s.lstrip("studyres"))))
    print(f"rooms 57, rooms with a literal pocket {len(rooms_with)}, pockets {len(out)}")
    for p in out:
        print(f"{p['room']:>8} W={p['W']:>2} pocket={p['pocket_BAC']} tri={p['triangles']:>3} "
              f"cores={p['cores_meeting_D']} loaded={p['loaded']} odd={p['odd']} sum={p['strip_sum']} Q={p['Q']}")
    print("pockets with a loaded (2,1) core:", sum(p["loaded"] > 0 for p in out), "of", len(out))
    print("second tracer mismatches", mismatches)
    sys.exit(1 if mismatches else 0)


if __name__ == "__main__":
    main()
