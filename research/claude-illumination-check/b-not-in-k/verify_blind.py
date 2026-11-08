"""Re-verify (1,1)+(2,1)-blind completions from mirror_complete.py with the older, separate pipeline.

Fixed-room checks on rooms already produced by the approved enumeration (Daniel, 2026-11-02). For each
room: build the corner polygon V from its triangles; the original existing_rooms_21.pockets(V) must
find the pocket; existing_rooms_21.triangles(V) must rebuild the same triangle set; a raw test copied
from seed-unbounded/seedcheck.py must pass with two interior A marks. Then all seven direction classes
with |theta|^2 <= 25 run through core_loads.py, each core checked by the polygon second tracer of
existing_rooms_21.py.
"""
import importlib.util
import json
import sys
from collections import Counter
from fractions import Fraction as F


def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


er = load("er", "existing_rooms_21.py")
cl = er.cl
DIRECTIONS = [(1, 0), (1, 1), (2, 1), (3, 1), (3, 2), (4, 1), (4, 3)]


def inside_closed(V, x, y):
    """Copied from seed-unbounded/seedcheck.py."""
    n = len(V)
    for i in range(n):
        (ax, ay), (bx, by) = V[i], V[(i + 1) % n]
        if (bx - ax) * (y - ay) - (by - ay) * (x - ax) == 0 and min(ax, bx) <= x <= max(ax, bx) and min(ay, by) <= y <= max(ay, by):
            return "edge"
    c = False
    for i in range(n):
        (ax, ay), (bx, by) = V[i], V[(i + 1) % n]
        if (ay > y) != (by > y) and x < ax + F(y - ay) * (bx - ax) / (by - ay):
            c = not c
    return "in" if c else "out"


def raw_ok(V, marks):
    """Copied from seed-unbounded/seedcheck.py: every non-A lattice point of the closed room is a vertex."""
    Vs = set(V)
    xs = [p[0] for p in V]
    ys = [p[1] for p in V]
    for x in range(min(xs), max(xs) + 1):
        for y in range(min(ys), max(ys) + 1):
            r = inside_closed(V, x, y)
            if r == "out" or (x % 2 == 0 and y % 2 == 0):
                continue
            if (x, y) not in Vs:
                return False
    return all(inside_closed(V, *m) == "in" for m in marks)


def polygon(tris):
    cnt = Counter()
    for t in tris:
        for a in range(3):
            cnt[tuple(sorted((t[a], t[(a + 1) % 3])))] += 1
    walls = [e for e, n in cnt.items() if n == 1]
    adj = {}
    for a, b in walls:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    start = min(adj)
    cyc, prev, cur = [start], None, start
    while True:
        nxt = adj[cur][0] if adj[cur][0] != prev else adj[cur][1]
        if nxt == start:
            break
        cyc.append(nxt)
        prev, cur = cur, nxt
    n = len(cyc)
    V = [p for i, p in enumerate(cyc)
         if (p[0] - cyc[i - 1][0]) * (cyc[(i + 1) % n][1] - p[1]) - (p[1] - cyc[i - 1][1]) * (cyc[(i + 1) % n][0] - p[0]) != 0]
    if er.shoelace2(V) and sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(V, V[1:] + V[:1])) < 0:
        V = V[::-1]
    return V


def main():
    src = json.load(open(sys.argv[1]))
    out, bad = [], 0
    for b in src["bands"]:
        for ci, r in enumerate(b["completions"]):
            if r["loaded_21"] != 0:
                continue
            tris = [tuple(tuple(p) for p in t) for t in r["tris"]]
            V = polygon(tris)
            pk = er.pockets(V)
            rebuilt = er.triangles(V)
            pts = {p for t in tris for p in t}
            cnt = Counter(p for t in tris for p in t)
            marks = sorted(p for p in pts if p[0] % 2 == 0 and p[1] % 2 == 0 and cnt[p] == 8)
            checks = {"pocket_found": ((1, 1), (2, 0), (1, 0)) in pk,
                      "triangles_match": sorted(map(sorted, rebuilt)) == sorted(map(sorted, tris)),
                      "area_match": len(rebuilt) == er.shoelace2(V),
                      "raw_ok": raw_ok(V, marks[:2]), "marks": len(marks)}
            cl.TRIANGLES = rebuilt
            cl.ROOM = {cl.key(F(sum(p[0] for p in t), 3), F(sum(p[1] for p in t), 3)) for t in rebuilt}
            pts_u = er.unit_points(V)
            W = [tuple(sorted(s)) for s in zip(pts_u, pts_u[1:] + pts_u[:1])]
            dirs, mism = {}, 0
            for th in DIRECTIONS:
                d = cl.run_direction(th)
                er.THETA = th
                for c in d["cores"]:
                    x0 = F(c["start_x_on_D"])
                    got = er.second_trace(W, V, (x0, 2 - x0), tuple(c["start_velocity"]))
                    mism += got != (c["wall_hits"], c["D_hits"], c["H_hits"], c["Q"])
                qs = [c["Q"] for c in d["cores"]]
                dirs[str(th)] = {"cores": len(qs), "loaded": sum(q != [0, 0] for q in qs), "Q": qs,
                                 "hits": [c["wall_hits"] for c in d["cores"]]}
            ok = checks["pocket_found"] and checks["triangles_match"] and checks["area_match"] and checks["raw_ok"] and checks["marks"] >= 2 and not mism
            bad += not ok
            row = {"band": b["band"], "completion": ci, "n_tri": len(tris), "corners": len(V), "V": V,
                   "marks": marks, "checks": checks, "mismatches": mism, "directions": dirs}
            out.append(row)
            print(f"band {b['band']} completion {ci}: n_tri={len(tris)} corners={len(V)} marks={len(marks)} checks={checks} mism={mism}")
            print("   " + " ".join(f"{k}:{v['loaded']}/{v['cores']}" for k, v in dirs.items()))
    json.dump({"source": sys.argv[1], "rooms": out}, open(sys.argv[2], "w"), indent=1, default=str)
    print("rooms", len(out), "failed checks", bad)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
