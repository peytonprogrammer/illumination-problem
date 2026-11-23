"""d101: exact checks for Q07 (normalization) and Q08 (Lemma MP).

Independent tracer (written here; does not import d8 tracer.py or room.py).
Rooms are sets of unit cells named by lower-left corner. All arithmetic is exact.

Part A: 200 random saved witnesses from d8-perturbation-test/results.jsonl (named
         rooms R22-L1-*, R34-*, ...). For each, trace the witness, then check
         (1) D = 0 mod 2, (2) the point at half length is a lattice point,
         (3) it is interior or smooth. Also Q07: the same path in the room scaled
         by (2, 3) ends at the scaled T, legally, with the same wall/corner events.
Part B: non-circular search in R22 and all 29 single edits R22-L1-* (d8):
         for same-class pairs of regular (interior or smooth) lattice points, trace every D with max|D_i| <= BOUND
         (odd components included) and check MP on every lighting path found.
Run: python3 -B mp_check.py > mp_check.log
"""
import json
import random
import sys
from fractions import Fraction as F
from math import floor, ceil, gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent / "d8-perturbation-test" / "results.jsonl"
HALF = F(1, 2)
BOUND = 12


def kind(cells, p):
    x, y = p
    ll, lr, ul, ur = ((x - 1, y - 1) in cells, (x, y - 1) in cells,
                      (x - 1, y) in cells, (x, y) in cells)
    k = ll + lr + ul + ur
    if k == 2 and ((ll and ur) or (lr and ul)):
        return "pinch"
    return {0: "outside", 1: "convex", 2: "smooth", 3: "reflex", 4: "interior"}[k]


class Bad(Exception):
    pass


def trace(cells, S, D):
    """Billiard flow from lattice point S with velocity D for unit time.
    Returns (end, half_point, events) or raises Bad on a corner/pinch hit or an
    illegal start. events lists (kind, point) for every wall reflection."""
    x, y = F(S[0]), F(S[1])
    vx, vy = F(D[0]), F(D[1])
    if kind(cells, S) not in ("interior", "smooth"):
        raise Bad("start not regular")
    if vx != 0 and vy != 0:
        c = (S[0] if vx > 0 else S[0] - 1, S[1] if vy > 0 else S[1] - 1)
        if c not in cells:
            raise Bad("start leaves room")
    elif kind(cells, S) != "interior":
        raise Bad("axis-parallel start on a wall")
    t, half, events = F(0), None, []
    while True:
        cand = []
        if vx != 0:
            nx = floor(x) + 1 if vx > 0 else ceil(x) - 1
            cand.append((nx - x) / vx)
        if vy != 0:
            ny = floor(y) + 1 if vy > 0 else ceil(y) - 1
            cand.append((ny - y) / vy)
        dt = min(cand)
        if half is None and t + dt >= HALF:
            half = (x + vx * (HALF - t), y + vy * (HALF - t))
        if t + dt >= 1:
            end = (x + vx * (1 - t), y + vy * (1 - t))
            if end[0].denominator == 1 and end[1].denominator == 1:
                if kind(cells, (int(end[0]), int(end[1]))) not in ("interior", "smooth"):
                    raise Bad("ends at corner")
            return end, half, events
        t += dt
        x, y = x + vx * dt, y + vy * dt
        xi, yi = x.denominator == 1, y.denominator == 1
        if xi and yi:
            p = (int(x), int(y))
            k = kind(cells, p)
            if k == "interior":
                continue
            if k != "smooth":
                raise Bad("corner " + k)
            X, Y = p
            horiz = ((X - 1, Y - 1) in cells) == ((X, Y - 1) in cells)
            if horiz:
                if vy == 0:
                    raise Bad("runs along wall")
                vy = -vy
            else:
                if vx == 0:
                    raise Bad("runs along wall")
                vx = -vx
            events.append(("smooth", p))
            if vx != 0 and vy != 0:
                c = (X if vx > 0 else X - 1, Y if vy > 0 else Y - 1)
                if c not in cells:
                    raise Bad("reflection leaves room")
        elif xi:
            c = (int(x) if vx > 0 else int(x) - 1, floor(y))
            if c not in cells:
                vx = -vx
                events.append(("v", (x, y)))
        elif yi:
            c = (floor(x), int(y) if vy > 0 else int(y) - 1)
            if c not in cells:
                vy = -vy
                events.append(("h", (x, y)))
        else:
            raise Bad("no crossing")


def light(cells, S, T, D):
    """Try the four sign choices of D; return (D_signed, half, events) or None."""
    for sx in (1, -1):
        for sy in (1, -1):
            if (sx < 0 and D[0] == 0) or (sy < 0 and D[1] == 0):
                continue
            Ds = (sx * D[0], sy * D[1])
            try:
                end, half, ev = trace(cells, S, Ds)
            except Bad:
                continue
            if end == (F(T[0]), F(T[1])):
                return Ds, half, ev
    return None


def scale_cells(cells, a, b):
    return {(a * i + u, b * j + v) for (i, j) in cells for u in range(a) for v in range(b)}


def corners(cells):
    pts = {(i + u, j + v) for (i, j) in cells for u in (0, 1) for v in (0, 1)}
    ks = [kind(cells, p) for p in pts]
    return ks.count("convex"), ks.count("reflex"), ks.count("pinch")


def wall_gcds(cells):
    """gcd of horizontal and of vertical maximal wall lengths."""
    pts = {(i + u, j + v) for (i, j) in cells for u in (0, 1) for v in (0, 1)}
    cs = [p for p in pts if kind(cells, p) in ("convex", "reflex")]
    gh = gv = 0
    rows, cols = {}, {}
    for p in cs:
        rows.setdefault(p[1], []).append(p[0])
        cols.setdefault(p[0], []).append(p[1])
    # consecutive corners on a line bound a wall or a gap; both lengths are
    # differences of corner coordinates, so their gcd equals the wall-length gcd
    # (every corner x-difference is a signed sum of horizontal wall lengths).
    for xs in rows.values():
        xs.sort()
        for u, v in zip(xs, xs[1:]):
            gh = gcd(gh, v - u)
    for ys in cols.values():
        ys.sort()
        for u, v in zip(ys, ys[1:]):
            gv = gcd(gv, v - u)
    return gh, gv


def mp_verdict(cells, S, T, Ds, half):
    even = Ds[0] % 2 == 0 and Ds[1] % 2 == 0
    lat = half[0].denominator == 1 and half[1].denominator == 1
    k = kind(cells, (int(half[0]), int(half[1]))) if lat else "nonlattice"
    M = (int(half[0]), int(half[1])) if lat else None
    return even, lat, k, M


def part_a(rows):
    rng = random.Random(101)
    pool = [(r, p) for r in rows for p in r.get("pairs", []) if p.get("witness")]
    sample = rng.sample(pool, 200)
    stats = {"traced": 0, "even": 0, "lattice": 0, "interior": 0, "smooth": 0,
             "M=S_or_T": 0, "fail": 0, "scaled_ok": 0, "scaled_events_match": 0,
             "W_kept": 0, "pinch_free_kept": 0, "gcd_scaled": 0}
    for r, p in sample:
        cells = set(map(tuple, r["cells"]))
        S, T, D = tuple(p["p"]), tuple(p["q"]), tuple(p["witness"])
        res = light(cells, S, T, D)
        if res is None:
            stats["fail"] += 1
            print("A FAIL witness not reproduced", r["id"], S, T, D)
            continue
        Ds, half, ev = res
        stats["traced"] += 1
        even, lat, k, M = mp_verdict(cells, S, T, Ds, half)
        stats["even"] += even
        stats["lattice"] += lat
        stats["interior"] += k == "interior"
        stats["smooth"] += k == "smooth"
        stats["M=S_or_T"] += M in (S, T)
        if not (even and lat and k in ("interior", "smooth")):
            print("A MP VIOLATION", r["id"], S, T, Ds, half, k)
        # Q07: scale by (2, 3); the path must map to a legal path with the same events.
        a, b = 2, 3
        sc = scale_cells(cells, a, b)
        S2, T2, D2 = (a * S[0], b * S[1]), (a * T[0], b * T[1]), (a * Ds[0], b * Ds[1])
        try:
            end2, half2, ev2 = trace(sc, S2, D2)
            if end2 == (F(T2[0]), F(T2[1])):
                stats["scaled_ok"] += 1
            mapped = [(a * F(q[0]), b * F(q[1])) for _, q in ev]
            if mapped == [(F(q[0]), F(q[1])) for _, q in ev2]:
                stats["scaled_events_match"] += 1
        except Bad as e:
            print("A SCALED FAIL", r["id"], e)
        c1, c3, pin = corners(cells)
        s1, s3, spin = corners(sc)
        stats["W_kept"] += (c1 + c3) == (s1 + s3)
        stats["pinch_free_kept"] += pin == spin == 0
        g0 = wall_gcds(cells)
        gs = wall_gcds(sc)
        stats["gcd_scaled"] += gs == (a * g0[0], b * g0[1])
    print("Part A (200 saved witnesses, seed 101):", json.dumps(stats))
    return stats


def part_b(rows):
    byid = {r["id"]: r for r in rows}
    r22 = {(-1, -1), (-1, 0), (0, -2), (0, -1), (0, 0), (0, 1), (1, -3), (1, -2),
           (1, 1), (1, 2), (2, 1), (2, 2), (3, 0), (3, 1), (4, 0)}
    ids = sorted(i for i in byid if i.startswith("R22-L1-"))
    rooms = [("R22", r22)] + [(i, set(map(tuple, byid[i]["cells"]))) for i in ids]
    vecs = [(u, v) for u in range(-BOUND, BOUND + 1) for v in range(-BOUND, BOUND + 1)
            if (u, v) != (0, 0)]
    tot = {"pairs": 0, "paths": 0, "odd_D_paths": 0, "viol": 0, "M_interior": 0,
           "M_smooth": 0, "M_is_endpoint": 0, "pairs_lit": 0, "diffclass_paths": 0,
           "diffclass_lattice_half": 0}
    for name, cells in rooms:
        pts = sorted({(i + u, j + v) for (i, j) in cells for u in (0, 1) for v in (0, 1)
                      if kind(cells, (i + u, j + v)) in ("interior", "smooth")})
        same = [(s, t) for s in pts for t in pts if s < t and (s[0] - t[0]) % 2 == 0
                and (s[1] - t[1]) % 2 == 0]
        diff = [(s, t) for s in pts for t in pts if s < t and not
                ((s[0] - t[0]) % 2 == 0 and (s[1] - t[1]) % 2 == 0)][:6]
        for S, T in same:
            tot["pairs"] += 1
            lit = False
            for D in vecs:
                try:
                    end, half, ev = trace(cells, S, D)
                except Bad:
                    continue
                if end != (F(T[0]), F(T[1])):
                    continue
                lit = True
                tot["paths"] += 1
                even, lat, k, M = mp_verdict(cells, S, T, D, half)
                tot["odd_D_paths"] += not even
                if not (even and lat and k in ("interior", "smooth")):
                    tot["viol"] += 1
                    print("B MP VIOLATION", name, S, T, D, half, k)
                tot["M_interior"] += k == "interior"
                tot["M_smooth"] += k == "smooth"
                tot["M_is_endpoint"] += M in (S, T)
            tot["pairs_lit"] += lit
            if name == "R22" and S == (0, 0) and T == (2, 2):
                print("B R22 dark pair (0,0)-(2,2) lit within bound:", lit)
        for S, T in diff:
            for D in vecs:
                try:
                    end, half, ev = trace(cells, S, D)
                except Bad:
                    continue
                if end == (F(T[0]), F(T[1])):
                    tot["diffclass_paths"] += 1
                    tot["diffclass_lattice_half"] += (half[0].denominator == 1
                                                     and half[1].denominator == 1)
        print("B room", name, "n =", len(cells), "same-class regular pairs =", len(same))
    print("Part B (|D|_inf <=", BOUND, "):", json.dumps(tot))
    return tot


def main():
    rows = [json.loads(l) for l in open(RESULTS)]
    # self-test: R22 dark pair has no lighting path with small D; a lit pair has one.
    r22 = {(-1, -1), (-1, 0), (0, -2), (0, -1), (0, 0), (0, 1), (1, -3), (1, -2),
           (1, 1), (1, 2), (2, 1), (2, 2), (3, 0), (3, 1), (4, 0)}
    c1, c3, pin = corners(r22)
    print("self-test R22: convex, reflex, pinch =", c1, c3, pin, "W =", c1 + c3)
    print("self-test R22 wall gcds =", wall_gcds(r22))
    part_a(rows)
    part_b(rows)


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
