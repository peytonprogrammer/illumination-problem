"""Tasks 2-3: enumerate perturbed rooms and decide every same-class interior pair.

Usage:
  python3 -B perturb.py enumerate            # writes rooms.json
  python3 -B perturb.py run [CAP] [WORKERS]  # writes results.jsonl (resumable)

Verdict methods for a pair of interior lattice points of one class:
  LIT  / witness     a developing vector certified by two independent tracers
  DARK / orbit       the whole SL(2,Z) orbit was scanned (complete decision)
  DARK / separation  N_min separates the pair (proved lemma, audit 1.3); the
                     orbit stopped early after all non-separated pairs were lit
  UNDECIDED          not separated, no witness, orbit cap reached
"""
import json
import os
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "ref"))

import room_model as RM  # noqa: E402
from certify import certify  # noqa: E402
from decider import build, decide  # noqa: E402
from nmin import class_report, group_info  # noqa: E402
from room import (cells_from_triangles, cells_from_vertices, cls, lattice_points,  # noqa: E402
                  perturbations, status, summary, vertex_cycle)


def bases():
    c22 = cells_from_vertices(RM.Q22)
    h = json.load(open(os.path.join(HERE, "ref", "historical34-room.json")))
    c34 = cells_from_triangles(h["triangles"])
    return {"R22": (c22, [(0, 0), (2, 2)]), "R34": (c34, [(2, 0), (6, 0)])}


def enumerate_rooms():
    rooms = []
    for name, (base, marks) in bases().items():
        lvl1 = perturbations(base, marks)
        seen = {base} | set(lvl1)
        lvl2 = {}
        for c1, d1 in lvl1.items():
            for c2, d2 in perturbations(c1, marks).items():
                if c2 in seen:
                    continue
                lvl2.setdefault(c2, f"{d1[0]} + {d2[0]}")
        rooms.append({"id": f"{name}-base", "base": name, "level": 0, "moves": "",
                      "marks": marks, "cells": sorted(base)})
        for i, (c, d) in enumerate(sorted(lvl1.items(), key=lambda x: sorted(x[0]))):
            rooms.append({"id": f"{name}-L1-{i:03d}", "base": name, "level": 1, "moves": " | ".join(d),
                          "marks": marks, "cells": sorted(c)})
        for i, (c, d) in enumerate(sorted(lvl2.items(), key=lambda x: sorted(x[0]))):
            rooms.append({"id": f"{name}-L2-{i:04d}", "base": name, "level": 2, "moves": d,
                          "marks": marks, "cells": sorted(c)})
        print(name, "level1", len(lvl1), "level2", len(lvl2), flush=True)
    json.dump(rooms, open(os.path.join(HERE, "rooms.json"), "w"))
    return rooms


def analyse(args):
    room, cap = args
    t0 = time.time()
    cells = frozenset(map(tuple, room["cells"]))
    marks = [tuple(m) for m in room["marks"]]
    S, T = marks
    sm = summary(cells, S)
    interior = sm["interior"]
    g = group_info(cells)
    classes = {}
    for p in interior:
        classes.setdefault(cls(p), []).append(p)
    pairs, unsep = [], []
    class_rows = {}
    for key, pts in sorted(classes.items()):
        rep = class_report(cells, pts[0])
        class_rows[key] = {"origin": pts[0], "k": rep["k"], "transparent": rep["transparent"],
                           "nmin_degree": rep["degree"], "points": pts}
        for (p, q), sep in sorted(rep["separated"].items()):
            pairs.append({"p": p, "q": q, "class": key, "separated": sep,
                          "marks": {p, q} == {S, T}})
            if not sep:
                unsep.append((p, q))
    res = decide(cells, interior, wanted=unsep, cap=cap if unsep else min(cap, 300_000)) \
        if len(interior) >= 2 else None
    for pr in pairs:
        p, q = pr["p"], pr["q"]
        w = None
        if res is not None:
            w = res["witness"].get((p, q))
            if w is not None:
                ws = certify(cells, p, q, w)
            else:
                w = res["witness"].get((q, p))
                ws = certify(cells, q, p, w) if w is not None else None
        if w is not None:
            pr["verdict"], pr["method"] = ("LIT", "witness") if ws else ("LIT?", "uncertified")
            pr["witness"] = w
        elif res["status"] == "DONE":
            pr["verdict"], pr["method"] = "DARK", "orbit"
        elif pr["separated"]:
            pr["verdict"], pr["method"] = "DARK", "separation"
        else:
            pr["verdict"], pr["method"] = "UNDECIDED", res["status"]
    out = {k: room[k] for k in ("id", "base", "level", "moves", "marks", "cells")}
    out.update({"W": sm["W"], "r": sm["r"], "area": sm["area"], "vertices": vertex_cycle(cells),
                "interior": interior, "k_marks": sm["k"], "transparent_marks": sm["transparent"],
                "group_order": g["order"], "group_order_method": g["order_method"],
                "primitive": g["primitive"], "classes": class_rows,
                "orbit_status": res["status"] if res else None,
                "orbit_states": res["states"] if res else 0,
                "pairs": pairs, "seconds": round(time.time() - t0, 2)})
    return out


def run(cap, workers):
    build()
    rooms = json.load(open(os.path.join(HERE, "rooms.json")))
    path = os.path.join(HERE, "results.jsonl")
    done = set()
    if os.path.exists(path):
        for line in open(path):
            done.add(json.loads(line)["id"])
    todo = [(r, cap) for r in rooms if r["id"] not in done]
    print(f"{len(rooms)} rooms, {len(todo)} to do", flush=True)
    with open(path, "a") as f, Pool(workers) as pool:
        for k, out in enumerate(pool.imap_unordered(analyse, todo)):
            f.write(json.dumps(out, default=list) + "\n")
            f.flush()
            if k % 50 == 0:
                print(k, out["id"], out["orbit_status"], out["orbit_states"], out["seconds"], flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "enumerate":
        enumerate_rooms()
    else:
        cap = int(sys.argv[2]) if len(sys.argv) > 2 else 3_000_000
        workers = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        run(cap, workers)
