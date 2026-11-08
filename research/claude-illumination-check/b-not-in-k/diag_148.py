"""Diagonal (1,1) cores at the 148 pockets where (2,1) is loaded.

Fixed-room check approved by Daniel on 2026-11-02. Pockets: those with a loaded
(2,1) core in existing_rooms_21.json. Direction: (1,1) only. Counts the diagonal
mirror rooms, where every diagonal core is blind. Same placement and tracers as
existing_rooms_21.py.
"""
import json
import sys
from fractions import Fraction as F
import importlib.util

spec = importlib.util.spec_from_file_location("er", "existing_rooms_21.py")
er = importlib.util.module_from_spec(spec)
spec.loader.exec_module(er)
cl = er.cl
TH = (1, 1)

rooms = {f"study{k}": json.loads(l) for k, l in enumerate(open(er.SEED + "study.jsonl"))}
rooms |= {f"res{k}": json.loads(l) for k, l in enumerate(open(er.SEED + "res_rooms.jsonl"))}
loaded = [p for p in json.load(open("existing_rooms_21.json"))["pockets"] if p["loaded"] > 0]
out, mismatches = [], 0
er.THETA = TH
for p in loaded:
    V = [tuple(x) for x in rooms[p["room"]]["V"]]
    f = er.to_s33(*[tuple(x) for x in p["pocket_BAC"]])
    V2 = [f(x) for x in V]
    tris = er.triangles(V2)
    assert len(tris) == er.shoelace2(V2)
    cl.TRIANGLES = tris
    cl.ROOM = {cl.key(F(sum(q[0] for q in t), 3), F(sum(q[1] for q in t), 3)) for t in tris}
    pts = er.unit_points(V2)
    W = [tuple(sorted(s)) for s in zip(pts, pts[1:] + pts[:1])]
    d = cl.run_direction(TH)
    for c in d["cores"]:
        x0 = F(c["start_x_on_D"])
        got = er.second_trace(W, V2, (x0, 2 - x0), tuple(c["start_velocity"]))
        mismatches += got != (c["wall_hits"], c["D_hits"], c["H_hits"], c["Q"])
    assert d["strip_weighted_sum"] == [0, 0]
    qs = [c["Q"] for c in d["cores"]]
    row = {"room": p["room"], "pocket_BAC": p["pocket_BAC"], "cores": len(qs),
           "loaded": sum(q != [0, 0] for q in qs), "odd": sum(q[0] % 2 != 0 for q in qs), "Q": qs,
           "Q21": p["Q"], "D_hits": [c["D_hits"] for c in d["cores"]], "hits": [c["wall_hits"] for c in d["cores"]]}
    out.append(row)
    print(f"{p['room']:>8} {p['pocket_BAC']} diag cores={row['cores']} loaded={row['loaded']} odd={row['odd']} "
          f"D={row['D_hits']} hits={row['hits']} Q21={p['Q']}", flush=True)
json.dump({"pockets": out, "second_tracer_mismatches": mismatches}, open(sys.argv[1], "w"), indent=1, default=str)
mirror = [r for r in out if r["loaded"] == 0]
print("pockets", len(out), "diagonal mirror pockets", len(mirror), "rooms", sorted({r["room"] for r in mirror}))
print("second tracer mismatches", mismatches)
sys.exit(1 if mismatches else 0)
