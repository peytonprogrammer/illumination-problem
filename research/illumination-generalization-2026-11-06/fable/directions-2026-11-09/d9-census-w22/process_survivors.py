"""Decide every survivor of the shooting filter, then analyse every dark pair.

Survivors are read from runs/<dir>/job-*.sv.  For each survivor pair:
  1. orbitc (C, complete SL(2,Z) orbit) with the two endpoints as sources;
  2. if orbitc says DARK: orbit.py (Python twin, independent code path) and
     d2-factor-audit/room_model.illumination (another agent's decider) must
     both say DARK;
  3. dark pairs: vertices (boundary walk of d3-review/surface.py), W, r, area,
     k, monodromy group order and block systems (room_model), B_min / N_min
     separation (room_model closure), and equivalence to the known 22-wall
     room up to the 8 lattice symmetries.
usage: python3 process_survivors.py runs/a20 > survivors.log
writes survivors.json and dark_rooms.json in the current directory.
"""
import glob
import json
import subprocess
import sys

HERE = sys.path[0]
sys.path.insert(1, HERE + "/../d2-factor-audit")
sys.path.insert(2, HERE + "/../d3-review")
import room_model as rm                                   # noqa: E402
from surface import boundary_cycle                        # noqa: E402
from orbit import decide                                  # noqa: E402
from check_enum_small import canon, boundary_walls        # noqa: E402

Q22_CELLS = rm.cells_from_vertices(rm.Q22)


def around(cells, p):
    x, y = p
    return sum(c in cells for c in ((x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)))


def orbitc(cells, sources, cap=20_000_000):
    line = (f"{len(cells)} " + " ".join(f"{x} {y}" for x, y in sorted(cells))
            + f" | {len(sources)} " + " ".join(f"{x} {y}" for x, y in sources))
    out = subprocess.run([HERE + "/orbitc", str(cap)], input=line + "\n",
                         capture_output=True, text=True, check=True).stdout.split("\n")
    st = out[0].split()
    res = {}
    for ln in out[1:]:
        f = ln.split()
        if len(f) == 5:
            res[frozenset(((int(f[0]), int(f[1])), (int(f[2]), int(f[3]))))] = f[4]
    return int(st[1]), st[3] == "1", res


def analyse(cells, S, T):
    pts = rm.lattice_points(cells)
    origin = S
    cl, idx, lam, rho, the = rm.pillow_model(cells, origin)
    gens = (lam, rho, the)
    n = len(cl)
    cp = rm.class_perms(lam, rho, the)
    seeds = [c for k in ("C1", "B", "C2") for c in rm.cycles(cp[k]) if len(c) == 2]
    bmin = rm.closure_partition(n, gens, seeds)
    bid = {a: b for b, blk in enumerate(bmin) for a in blk}

    def blocks_at(p):
        return {bid[idx[c]] for c in rm.around(cells, p)}
    sep = not (blocks_at(S) & blocks_at(T))
    order = rm.group_order(gens, n, cap=3_000_000)
    systems = rm.all_block_systems(n, gens)
    k = sum(1 for p in pts if rm.cls(p, origin) != "A" and rm.status(cells, p) in ("smooth", "interior"))
    verts, _ = boundary_cycle(cells)
    r = sum(1 for p in pts if rm.status(cells, p) == "reflex")
    return {
        "cells": sorted(cells), "S": S, "T": T, "area": len(cells), "W": boundary_walls(cells),
        "r": r, "k": k, "vertices": verts,
        "monodromy_order": order, "block_system_sizes": sorted(len(p[0]) for p in systems),
        "B_min_blocks": len(bmin), "B_min_block_sizes": sorted({len(b) for b in bmin}),
        "N_min_separates": sep,
        "equivalent_to_known_22_wall_room": canon(cells) == canon(Q22_CELLS),
    }


def main():
    rdir = sys.argv[1]
    surv = []
    for f in sorted(glob.glob(rdir + "/job-*.sv")):
        for line in open(f):
            a, b = line.split("|")
            h = list(map(int, a.split()))
            v = list(map(int, b.split()))
            cells = {(v[i], v[i + 1]) for i in range(0, len(v), 2)}
            surv.append({"job_file": f.split("/")[-1], "rid": h[0], "area": h[1], "W": h[2], "r": h[3],
                         "S": (h[4], h[5]), "T": (h[6], h[7]), "sep_c": h[8], "k_c": h[9],
                         "nblk_c": h[10], "cells": cells})
    print(f"survivors: {len(surv)}")
    dark = []
    for s in surv:
        cells, S, T = s["cells"], s["S"], s["T"]
        ns, complete, res = orbitc(cells, [S, T])
        v1 = res[frozenset((S, T))]
        s["orbitc"] = {"states": ns, "complete": complete, "verdict": v1}
        line = f"room {s['job_file']}:{s['rid']} area {s['area']} W {s['W']} pair {S}-{T}: orbitc {v1} ({ns} states)"
        if v1 == "DARK":
            assert complete
            reach, ns2, comp2 = decide(cells, [S, T])
            v2 = "LIT" if T in reach[S] else "DARK"
            ref = rm.illumination(cells, [S, T], verbose=False)
            v3 = "LIT" if T in ref[S] else "DARK"
            s["orbit_py"] = {"states": ns2, "complete": comp2, "verdict": v2}
            s["room_model"] = v3
            line += f"; orbit.py {v2} ({ns2} states); room_model {v3}"
            if v2 == v3 == "DARK":
                info = analyse(cells, S, T)
                info["shoot_sep"] = s["sep_c"]
                info["shoot_k"] = s["k_c"]
                dark.append(info)
                line += (f"; N_min separates {info['N_min_separates']}; k {info['k']};"
                         f" equivalent to known room {info['equivalent_to_known_22_wall_room']}")
        print(line, flush=True)
    for s in surv:
        s["cells"] = sorted(s["cells"])
    json.dump(surv, open("survivors.json", "w"), indent=1, default=list)
    json.dump(dark, open("dark_rooms.json", "w"), indent=1, default=list)
    print(f"dark pairs (all three deciders): {len(dark)}")


if __name__ == "__main__":
    main()
