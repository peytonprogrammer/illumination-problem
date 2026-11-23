"""Task 1: validate the decider before any perturbation run.

V1  22-wall room, all 8 regular lattice points: full orbit (DONE); only the
    four cross pairs {(0,0),(4,0)} x {(2,2),(2,-2)} are dark, as in the record;
    the result equals the copied reference decider ref/room_model.illumination.
V2  per-state check on the 22-wall room: in every orbit state, the set of
    (source, source) meetings of the horizontal scan equals the union of the
    room-level billiard rays from each source in the four sign variants of the
    tracked direction M^-1 (1,0).
V3  34-wall orthogonal room: run the orbit with a state cap; report.
V4  31 orthogonal lit controls (30 k7 models + W18 control): marks lit, each
    witness certified by both tracers, N_min does not separate the marks.
V5  per-state check (as V2) on the states scanned for 5 lit controls.
Every lit witness in V1 and V4 is certified by certify.certify (two tracers).
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "ref"))

import room_model as RM  # noqa: E402
from certify import certify  # noqa: E402
from decider import decide, regular_points  # noqa: E402
from nmin import class_report, group_info  # noqa: E402
from room import (cells_from_triangles, cells_from_vertices, is_strictly_simple,  # noqa: E402
                  status, summary)
from tracer import ray_reach  # noqa: E402

OUT = {}


def per_state_check(cells, sources, trace):
    """Rays start at interior sources only (a ray from a flat wall point may
    run along the wall, which the room tracer does not model)."""
    bad = 0
    starts = [s for s in sources if status(cells, s) == "interior"]
    for (a, b, c, d), seen in trace:
        dirn = (d, -c)
        seen = {(s, t) for (s, t) in seen if s in starts}
        exp = set()
        for s in starts:
            for sx in (1, -1):
                for sy in (1, -1):
                    if (dirn[0] == 0 and sx == -1) or (dirn[1] == 0 and sy == -1):
                        continue
                    for t in ray_reach(cells, s, (sx * dirn[0], sy * dirn[1]), sources):
                        exp.add((s, t))
        if exp != seen:
            bad += 1
    return bad


def certify_all(cells, res):
    fails = [p for p in res["lit"] if certify(cells, p[0], p[1], res["witness"][p]) is None]
    return fails


def v1_v2():
    c22 = cells_from_vertices(RM.Q22)
    regs = regular_points(c22)
    t = time.time()
    res = decide(c22, regs, verbose=True)
    dark = sorted({tuple(sorted((p, q))) for p in regs for q in regs if p != q and (p, q) not in res["lit"]})
    ref = RM.illumination(set(c22), regs, verbose=False)
    ref_lit = {(p, q) for p in regs for q in ref[p] if q != p}
    fails = certify_all(c22, res)
    bad = per_state_check(c22, regs, res["trace"])
    OUT["V1"] = {"status": res["status"], "states": res["states"], "dark_pairs": dark,
                 "equals_reference_decider": ref_lit == res["lit"],
                 "uncertified_witnesses": len(fails), "seconds": round(time.time() - t, 1)}
    OUT["V2"] = {"states_checked": len(res["trace"]), "mismatches": bad}
    exp_dark = sorted(tuple(sorted(x)) for x in [((0, 0), (2, 2)), ((0, 0), (2, -2)),
                                                  ((4, 0), (2, 2)), ((4, 0), (2, -2))])
    ok = res["status"] == "DONE" and dark == exp_dark and ref_lit == res["lit"] and not fails and bad == 0
    OUT["V1"]["pass"] = ok
    print("V1/V2", OUT["V1"], OUT["V2"], flush=True)
    return ok


def v3(cap):
    h = json.load(open(os.path.join(HERE, "ref", "historical34-room.json")))
    c34 = cells_from_triangles(h["triangles"])
    S, T = (2, 0), (6, 0)
    rep = class_report(c34, S)
    t = time.time()
    res = decide(c34, [S, T], cap=cap)
    OUT["V3"] = {"summary": {k: v for k, v in summary(c34, S).items() if k != "transparent"},
                 "nmin_degree": rep["degree"], "separated": rep["separated"][(S, T)],
                 "orbit_status": res["status"], "states": res["states"],
                 "lit_found": len(res["lit"]), "seconds": round(time.time() - t, 1)}
    print("V3", OUT["V3"], flush=True)
    return res["status"] == "DONE" and not res["lit"]


def lit_controls():
    d = os.path.join(HERE, "ref", "k7-models")
    for f in sorted(os.listdir(d)):
        m = json.load(open(os.path.join(d, f)))
        yield f, frozenset(map(tuple, m["cells"])), [tuple(x) for x in m["marks"]]
    c = json.load(open(os.path.join(HERE, "ref", "k7-controls.json")))["controls"][0]
    yield "k7-control-W18", frozenset(map(tuple, c["cells"])), [tuple(x) for x in c["geometry"]["interior_A"]]


def v4_v5():
    rows, ok, nchecked, bad_states = [], True, 0, 0
    for name, cells, marks in lit_controls():
        assert is_strictly_simple(cells) and all(status(cells, m) == "interior" for m in marks)
        S, T = marks
        rep = class_report(cells, S)
        verbose = nchecked < 5
        res = decide(cells, [S, T], wanted=[(S, T)], verbose=verbose)
        lit = (S, T) in res["lit"] or (T, S) in res["lit"]
        fails = certify_all(cells, res)
        if verbose:
            bad_states += per_state_check(cells, [S, T], res["trace"])
            nchecked += 1
        g = group_info(cells)
        row = {"room": name, "W": summary(cells, S)["W"], "k": rep["k"], "lit": lit,
               "status": res["status"], "states": res["states"],
               "witness": res["witness"].get((S, T)) or res["witness"].get((T, S)),
               "certified": lit and not fails, "nmin_degree": rep["degree"],
               "separated": rep["separated"][tuple(sorted((S, T)))], "primitive": g["primitive"]}
        rows.append(row)
        ok &= row["lit"] and row["certified"] and not row["separated"]
    OUT["V4"] = {"rooms": len(rows), "all_lit_certified_unseparated": ok, "rows": rows}
    OUT["V5"] = {"rooms_checked": nchecked, "state_mismatches": bad_states}
    print("V4", len(rows), ok, "V5", OUT["V5"], flush=True)
    return ok and bad_states == 0


if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 4_000_000
    a = v1_v2()
    b = v4_v5()
    c = v3(cap)
    OUT["pass"] = {"V1_V2": a, "V4_V5": b, "V3_orbit_complete_dark": c}
    json.dump(OUT, open(os.path.join(HERE, "validate.json"), "w"), indent=1, default=str)
    print("PASS" if a and b else "FAIL", OUT["pass"])
