"""Slide load Q for every cylinder core in fixed directions of the Section 33 room.

Fixed-room check approved by Daniel on 2026-11-02. The room is the single
prescribed assembly of pocket-detection.md Section 33, in that section's
coordinates: pocket A=(2,0), C=(1,0), B=(1,1); moving mirrors D_t: x+y=2+t and
H_t: y=t. No room, ray, direction, word, or orbit discovery is done: the
direction list is fixed below, and every core meeting a moving mirror is found
by tracing one midpoint per height-1/|theta| strip on D.
"""
import json
import math
import sys
from fractions import Fraction as F

DIRECTIONS = [(1, 0), (1, 1), (2, 1), (3, 1), (3, 2), (4, 1), (4, 3)]  # all D4 classes with |theta|^2 <= 25


def fan(center, k_list):
    """Canonical triangles k of the A star at center, counterclockwise from +x."""
    cx, cy = center
    ring = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0)]
    out = []
    for k in k_list:
        a, b = ring[k], ring[k + 1]
        out.append(((cx, cy), (cx + a[0], cy + a[1]), (cx + b[0], cy + b[1])))
    return out


TRIANGLES = (
    fan((-4, 0), range(8)) + fan((0, 0), range(8)) + fan((-2, 0), range(4))
    + [((-2, 2), (-2, 1), (-1, 1)), ((2, 0), (1, 0), (1, 1)),
       ((0, 2), (0, 1), (1, 1)), ((0, 2), (1, 1), (1, 2)),
       ((0, -2), (0, -1), (1, -1)), ((-6, 0), (-5, 0), (-5, 1)),
       ((-4, 2), (-4, 1), (-3, 1)), ((-4, -2), (-4, -1), (-5, -1))]
)


def key(x, y):
    i, j = math.floor(x), math.floor(y)
    if (i - j) % 2 == 0:
        d = (x - y) - (i - j)
    else:
        d = (x + y) - (i + j + 1)
    assert d != 0
    return (i, j, d > 0)


ROOM = {key(F(sum(v[0] for v in t), 3), F(sum(v[1] for v in t), 3)) for t in TRIANGLES}

# Line families: 0 vertical x=c, 1 horizontal y=c, 2 x-y=c (c even), 3 x+y=c (c even).
REFLECT = {0: ((-1, 0), (0, 1)), 1: ((1, 0), (0, -1)), 2: ((0, 1), (1, 0)), 3: ((0, -1), (-1, 0))}


def matmul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def matvec(a, v):
    return (a[0][0] * v[0] + a[0][1] * v[1], a[1][0] * v[0] + a[1][1] * v[1])


I2 = ((1, 0), (0, 1))
D4 = [((1, 0), (0, 1)), ((-1, 0), (0, 1)), ((1, 0), (0, -1)), ((-1, 0), (0, -1)),
      ((0, 1), (1, 0)), ((0, -1), (1, 0)), ((0, 1), (-1, 0)), ((0, -1), (-1, 0))]


def next_crossing(z, v):
    """Smallest t>0 at which z+tv meets a canonical edge line; returns (t, family)."""
    best = None
    vals = [(z[0], v[0], 1), (z[1], v[1], 1), (z[0] - z[1], v[0] - v[1], 2), (z[0] + z[1], v[0] + v[1], 2)]
    for fam, (f, df, step) in enumerate(vals):
        if df == 0:
            continue
        if df > 0:
            target = (math.floor(f / step) + 1) * step
        else:
            target = (math.ceil(f / step) - 1) * step
        t = F(target - f) / df
        if best is None or t < best[0]:
            best = (t, fam, False)
        elif t == best[0]:
            best = (t, fam, True)
    assert not best[2], "trajectory meets a lattice point"
    return best[0], best[1]


def line_const(fam, p):
    return [p[0], p[1], p[0] - p[1], p[0] + p[1]][fam]


def moving(fam, p):
    if fam == 3 and p[0] + p[1] == 2 and 1 < p[0] < 2:
        return "D"
    if fam == 1 and p[1] == 0 and 1 < p[0] < 2:
        return "H"
    return None


A_LOAD = {"D": (1, 1), "H": (0, 2)}


def trace_to_D(z, v):
    """From a point on D leaving into the pocket, trace to the next D hit."""
    hits = []
    mid = (z[0] + F(1, 1000000) * v[0], z[1] + F(1, 1000000) * v[1])
    assert key(*mid) in ROOM
    steps = 0
    while True:
        steps += 1
        assert steps < 10 ** 6
        t1, fam = next_crossing(z, v)
        p = (z[0] + t1 * v[0], z[1] + t1 * v[1])
        t2, _ = next_crossing(p, v)
        beyond = (p[0] + t2 / 2 * v[0], p[1] + t2 / 2 * v[1])
        if key(*beyond) in ROOM:
            z = p
            continue
        mv = moving(fam, p)
        hits.append((fam, line_const(fam, p), mv, p, v))
        r = REFLECT[fam]
        v = matvec(r, v)
        z = p
        if mv == "D":
            return z, v, hits


def affine_hol(itinerary, t):
    """Translation part of A_1 o ... o A_N with moving mirrors at slide t."""
    lin, trans = I2, (F(0), F(0))
    for fam, c, mv in itinerary:
        if mv == "D":
            c = c + t
        elif mv == "H":
            c = c + t
        r = REFLECT[fam]
        b = [(2 * c, 0), (0, 2 * c), (c, -c), (c, c)][fam]
        tb = matvec(lin, b)
        trans = (trans[0] + tb[0], trans[1] + tb[1])
        lin = matmul(lin, r)
    return lin, trans


def d_states(theta):
    p, q = theta
    vels = {(sx * a, sy * b) for a, b in [(p, q), (q, p)] for sx in (1, -1) for sy in (1, -1)}
    states = []
    for a, b in sorted(vels):
        if a + b >= 0:
            continue
        c = -(a + b)
        for k in range(c):
            x = 1 + F(2 * k + 1, 2 * c)
            states.append(((x, 2 - x), (a, b)))
    return states


def frame_to(theta, w):
    for g in D4:
        if matvec(g, w) == theta:
            return g
    raise AssertionError


def run_direction(theta):
    states = d_states(theta)
    seen = set()
    cores = []
    for s0 in states:
        if (s0[0], s0[1]) in seen:
            continue
        L0 = frame_to(theta, s0[1])
        L = L0
        z, v = s0
        Q = [0, 0]
        nD = nH = 0
        itinerary = []
        visited = []
        length_steps = 0
        while True:
            visited.append((z, v))
            z, v, hits = trace_to_D(z, v)
            for fam, c, mv, pt, vin in hits:
                if mv:
                    ld = matvec(L, A_LOAD[mv])
                    Q[0] += ld[0]
                    Q[1] += ld[1]
                    nD += mv == "D"
                    nH += mv == "H"
                itinerary.append((fam, c, mv))
                L = matmul(L, REFLECT[fam])
            length_steps += len(hits)
            if (z, v) == s0 and L == L0:
                break
            assert length_steps < 10 ** 6
        for st in visited:
            seen.add(st)
        lin1, tr1 = affine_hol(itinerary, 1)
        lin0, tr0 = affine_hol(itinerary, 0)
        assert lin1 == I2
        q_affine = matvec(L0, (tr1[0] - tr0[0], tr1[1] - tr0[1]))
        hol = matvec(L0, tr0)
        assert tuple(Q) == tuple(q_affine), (Q, q_affine)
        assert (Q[0] - nD) % 2 == 0 and (Q[1] - nD) % 2 == 0, "parity rule fails"
        assert hol[0] * theta[1] - hol[1] * theta[0] == 0, "holonomy not along theta"
        cores.append({
            "start_x_on_D": str(s0[0][0]), "start_velocity": s0[1],
            "D_states_per_period": len(set(visited)), "billiard_traversals": len(visited) // len(set(visited)),
            "wall_hits": len(itinerary), "D_hits": nD, "H_hits": nH,
            "hol": [str(hol[0]), str(hol[1])], "Q": Q,
        })
    total = [sum(c["Q"][0] for c in cores), sum(c["Q"][1] for c in cores)]
    return {"theta": theta, "D_strip_states": len(states), "cores": cores,
            "loaded_cores": sum(1 for c in cores if c["Q"] != [0, 0]),
            "strip_weighted_sum": total}


def room_facts():
    edges = {}
    for t in TRIANGLES:
        for i in range(3):
            e = tuple(sorted((t[i], t[(i + 1) % 3])))
            edges[e] = edges.get(e, 0) + 1
    boundary = [e for e, n in edges.items() if n == 1]
    return {"triangles": len(TRIANGLES), "distinct_triangles": len(ROOM), "area": len(TRIANGLES) / 2,
            "boundary_edges": len(boundary)}


def main():
    out = {"room": room_facts(), "directions": []}
    for theta in DIRECTIONS:
        out["directions"].append(run_direction(theta))
    json.dump(out, open(sys.argv[1], "w"), indent=1, default=str)
    print(json.dumps(out["room"]))
    for d in out["directions"]:
        print(f"theta={d['theta']} strips_on_D={d['D_strip_states']} cores_meeting_D={len(d['cores'])} "
              f"loaded={d['loaded_cores']} sum={d['strip_weighted_sum']}")
        for c in d["cores"]:
            print(f"   x0={c['start_x_on_D']:>6} w0={c['start_velocity']} strips={c['D_states_per_period']} "
                  f"trav={c['billiard_traversals']} hits={c['wall_hits']} D={c['D_hits']} H={c['H_hits']} "
                  f"hol={c['hol']} Q={c['Q']}")


if __name__ == "__main__":
    main()
