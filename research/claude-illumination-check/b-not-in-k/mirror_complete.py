"""Stage B of the bounded mirror-room enumeration (Daniel approved 2026-11-02: "ok do 1 then 2").

For each closed mirror band from mirror_bands.py (fixed box R), complete the decided cells to full raw
rooms with SAT, inside the band box widened by PAD on every side. A completion is a strictly simple
canonical room (one disk) in which every B and C point is a corner, with at least two full A fans for
the marks S and T. Connectivity and holes are enforced by lazy cuts. Up to NC distinct completions per
band: the first prefers few triangles, the rest use seeded random phases.

Each completion is then re-checked without the SAT model (one boundary cycle, raw corners, no
interior B or C point), and core_loads.py runs (1,1) and (2,1). The (1,1) run must be blind, which
confirms the mirror band. A second tracer that reflects off the room's own wall segments must
reproduce every core's hits, D hits, H hits, and Q.
"""
import importlib.util
import json
import random
import sys
from collections import Counter
from fractions import Fraction as F

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver

R, PAD, NC = int(sys.argv[1]), 4, int(sys.argv[2])


def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


mb = load("mb", "mirror_bands.py")
cl = load("cl", "core_loads.py")
mb.R = R

I0, I1, J0, J1 = 1 - R - PAD, R + PAD, -R - PAD, R - 1 + PAD
BOX = [(i, j, s) for i in range(I0, I1 + 1) for j in range(J0, J1 + 1) for s in (False, True)]
BOXSET = set(BOX)
EDGES = {}
for k in BOX:
    v = mb.verts(k)
    for a in range(3):
        EDGES.setdefault(tuple(sorted((v[a], v[(a + 1) % 3]))), []).append(k)
NBR = {k: [] for k in BOX}
for e, ks in EDGES.items():
    if len(ks) == 2:
        NBR[ks[0]].append(ks[1])
        NBR[ks[1]].append(ks[0])
POINTS = sorted({p for k in BOX for p in mb.verts(k)})
OUTER = {k for k in BOX if len(NBR[k]) < 3}
POCKET = mb.key(F(4, 3), F(1, 3))


def base_cnf(pool):
    x = {k: pool.id(k) for k in BOX}
    cls = []
    for p in POINTS:
        ks = mb.tris_at(p)
        allowed = set(mb.ALLOWED[mb.ptype(p)])
        for m in range(1 << len(ks)):
            if m in allowed:
                continue
            c, dead = [], False
            for b, k in enumerate(ks):
                if k not in BOXSET:
                    if m >> b & 1:
                        dead = True
                        break
                    continue
                c.append(-x[k] if m >> b & 1 else x[k])
            if not dead:
                cls.append(c)
    fans = []
    for p in POINTS:
        ks = mb.tris_at(p)
        if mb.ptype(p) == "A" and all(k in BOXSET for k in ks):
            f = pool.id(("full", p))
            fans.append(f)
            cls += [[-f, x[k]] for k in ks]
    cls += CardEnc.atleast(lits=fans, bound=2, vpool=pool, encoding=EncType.seqcounter).clauses
    return x, cls


def components(nodes, nbr):
    seen, comps = set(), []
    for n in nodes:
        if n in seen:
            continue
        comp, stack = [], [n]
        seen.add(n)
        while stack:
            a = stack.pop()
            comp.append(a)
            for b in nbr(a):
                if b not in seen:
                    seen.add(b)
                    stack.append(b)
        comps.append(comp)
    return comps


def cuts(room, x):
    """Separator cuts. A component X off the pocket: every grid path from X to the pocket crosses the
    non-room ring N(X), so x_u implies some ring cell for each u in X. A hole H: its room ring separates it
    from the outside, so a cell of H being out implies some ring cell is out."""
    out = []
    for comp in components(sorted(room), lambda a: [b for b in NBR[a] if b in room]):
        if POCKET not in comp:
            cs = set(comp)
            ring = sorted({b for a in comp for b in NBR[a] if b not in cs})
            out += [[-x[u]] + [x[b] for b in ring] for u in comp]
    holes = components(sorted(BOXSET - room), lambda a: [b for b in NBR[a] if b not in room])
    for comp in holes:
        if not any(a in OUTER for a in comp):
            cs = set(comp)
            ring = sorted({b for a in comp for b in NBR[a] if b not in cs})
            out += [[x[u]] + [-x[b] for b in ring] for u in comp]
    return out


def independent_check(room):
    """Raw and strictly simple, from the boundary alone: one cycle; every B/C point of the closed room
    is a turning boundary vertex."""
    cnt = Counter()
    for k in room:
        v = mb.verts(k)
        for a in range(3):
            cnt[tuple(sorted((v[a], v[(a + 1) % 3])))] += 1
    walls = [e for e, n in cnt.items() if n == 1]
    deg = Counter(p for e in walls for p in e)
    if any(d != 2 for d in deg.values()):
        return False, "boundary vertex of degree != 2"
    adj = {}
    for a, b in walls:
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    start = walls[0][0]
    cyc, prev, cur = [start], None, start
    while True:
        nxt = adj[cur][0] if adj[cur][0] != prev else adj[cur][1]
        if nxt == start:
            break
        cyc.append(nxt)
        prev, cur = cur, nxt
    if len(cyc) != len(deg):
        return False, "boundary is not one cycle"
    n = len(cyc)
    for i, p in enumerate(cyc):
        a, b = cyc[i - 1], cyc[(i + 1) % n]
        straight = (p[0] - a[0]) * (b[1] - p[1]) - (p[1] - a[1]) * (b[0] - p[0]) == 0
        if straight and mb.ptype(p) != "A":
            return False, f"smooth {mb.ptype(p)} point {p}"
    pts = {p for k in room for p in mb.verts(k)}
    for p in pts - set(deg):
        if mb.ptype(p) != "A":
            return False, f"interior {mb.ptype(p)} point {p}"
    fulls = [p for p in pts - set(deg)]
    if len(fulls) < 2:
        return False, "fewer than two interior A points"
    return True, cyc


def second_tracer(room, walls, z0, v0, theta):
    """Reflect off unit wall segments; independent of the triangle-key walk in core_loads."""
    def inside(q):
        """Closed-triangle test: chord midpoints can lie on shared interior edges."""
        import math
        for i in {math.floor(q[0]), math.ceil(q[0]) - 1}:
            for j in {math.floor(q[1]), math.ceil(q[1]) - 1}:
                for s in (False, True):
                    if (i, j, s) not in room:
                        continue
                    a, b, c = mb.verts((i, j, s))
                    d = [(u[0] - t[0]) * (q[1] - t[1]) - (u[1] - t[1]) * (q[0] - t[0]) for t, u in ((a, b), (b, c), (c, a))]
                    if all(e >= 0 for e in d) or all(e <= 0 for e in d):
                        return True
        return False
    dseg, hseg = ((1, 1), (2, 0)), ((1, 0), (2, 0))
    L0 = cl.frame_to(theta, v0)
    L = tuple(tuple(F(a) for a in r) for r in L0)
    z, v, Q, nD, nH, hits = z0, v0, [F(0), F(0)], 0, 0, 0
    while True:
        best = None
        for (ax, ay), (bx, by) in walls:
            ex, ey = bx - ax, by - ay
            den = v[0] * ey - v[1] * ex
            if den == 0:
                continue
            t = F((ax - z[0]) * ey - (ay - z[1]) * ex) / den
            s = F((ax - z[0]) * v[1] - (ay - z[1]) * v[0]) / den
            if t > 0 and 0 <= s <= 1 and (best is None or t < best[0]):
                assert 0 < s < 1, "path meets a wall endpoint"
                best = (t, ((ax, ay), (bx, by)))
        t, seg = best
        p = (z[0] + t * v[0], z[1] + t * v[1])
        assert inside(((z[0] + p[0]) / 2, (z[1] + p[1]) / 2)), "segment leaves the room"
        hits += 1
        if seg in (dseg, hseg):
            a = (1, 1) if seg == dseg else (0, 2)
            Q = [Q[0] + L[0][0] * a[0] + L[0][1] * a[1], Q[1] + L[1][0] * a[0] + L[1][1] * a[1]]
            nD += seg == dseg
            nH += seg == hseg
        (ax, ay), (bx, by) = seg
        ex, ey = bx - ax, by - ay
        n2 = ex * ex + ey * ey
        lin = ((F(ex * ex - ey * ey, n2), F(2 * ex * ey, n2)), (F(2 * ex * ey, n2), F(ey * ey - ex * ex, n2)))
        L = cl.matmul(L, lin)
        kk = F(2 * (v[0] * ex + v[1] * ey), n2)
        v = (kk * ex - v[0], kk * ey - v[1])
        z = p
        if z == z0 and v == v0 and L == L0:
            return hits, nD, nH, [int(Q[0]), int(Q[1])]


def run_room(room):
    tris = [mb.verts(k) for k in sorted(room)]
    cl.TRIANGLES = tris
    cl.ROOM = set(room)
    cnt = Counter()
    for t in tris:
        for a in range(3):
            cnt[tuple(sorted((t[a], t[(a + 1) % 3])))] += 1
    walls = [e for e, n in cnt.items() if n == 1]
    res, mism = {}, 0
    for th in [(1, 1), (2, 1)]:
        d = cl.run_direction(th)
        assert d["strip_weighted_sum"] == [0, 0]
        for c in d["cores"]:
            x0 = F(c["start_x_on_D"])
            got = second_tracer(room, walls, (x0, 2 - x0), tuple(c["start_velocity"]), th)
            mism += got != (c["wall_hits"], c["D_hits"], c["H_hits"], c["Q"])
        res[str(th)] = [c["Q"] for c in d["cores"]]
    return res, mism


def main():
    bands = json.load(open(f"mirror_bands_R{R}.json"))["bands"]
    out, totals = [], Counter()
    for bi, b in enumerate(bands):
        pool = IDPool()
        x, cls = base_cnf(pool)
        fixed_in = [mb.key(F(sum(p[0] for p in t), 3), F(sum(p[1] for p in t), 3)) for t in map(lambda t: [tuple(q) for q in t], b["tris_in"])]
        fixed_out = [mb.key(F(sum(p[0] for p in t), 3), F(sum(p[1] for p in t), 3)) for t in map(lambda t: [tuple(q) for q in t], b["tris_out"])]
        s = Solver(name="cd15", bootstrap_with=cls)
        for k in fixed_in:
            s.add_clause([x[k]])
        for k in fixed_out:
            if k in BOXSET:
                s.add_clause([-x[k]])
        rows, rng, iters = [], random.Random(bi), 0
        while len(rows) < NC:
            ph = [-x[k] for k in BOX] if not rows else [x[k] if rng.random() < 0.5 else -x[k] for k in BOX]
            s.set_phases(ph)
            if not s.solve():
                break
            iters += 1
            model = set(l for l in s.get_model() if l > 0)
            room = {k for k in BOX if x[k] in model}
            cs = cuts(room, x)
            if cs:
                for c in cs:
                    s.add_clause(c)
                continue
            ok, info = independent_check(room)
            assert ok, info
            res, mism = run_room(room)
            mirror = all(q == [0, 0] for q in res["(1, 1)"])
            loaded21 = sum(q != [0, 0] for q in res["(2, 1)"])
            rows.append({"n_tri": len(room), "boundary_len": len(info), "mirror_11": mirror,
                         "cores_21": len(res["(2, 1)"]), "loaded_21": loaded21, "Q21": res["(2, 1)"],
                         "Q11": res["(1, 1)"], "mismatches": mism,
                         "tris": [mb.verts(k) for k in sorted(room)]})
            totals["completions"] += 1
            totals["mirror_fail"] += not mirror
            totals["blind_21"] += loaded21 == 0
            totals["mismatches"] += mism
            s.add_clause([-x[k] for k in room] + [x[k] for k in BOX if k not in room])
        totals["bands_completed"] += bool(rows)
        totals["bands_uncompletable"] += not rows
        out.append({"band": bi, "completions": rows, "sat_rounds": iters})
        json.dump({"R": R, "pad": PAD, "nc": NC, "totals": totals, "bands": out}, open(f"mirror_complete_R{R}.json", "w"))
        print(f"band {bi}: completions={len(rows)} sizes={[r['n_tri'] for r in rows]} "
              f"loaded21={[r['loaded_21'] for r in rows]} mirror={all(r['mirror_11'] for r in rows)} "
              f"mism={sum(r['mismatches'] for r in rows)} rounds={iters}", flush=True)
    json.dump({"R": R, "pad": PAD, "nc": NC, "totals": totals, "bands": out}, open(f"mirror_complete_R{R}.json", "w"))
    print("totals", dict(totals))
    sys.exit(1 if totals["mismatches"] or totals["mirror_fail"] else 0)


if __name__ == "__main__":
    main()
