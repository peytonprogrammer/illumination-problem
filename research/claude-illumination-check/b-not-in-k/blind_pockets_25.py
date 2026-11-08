"""All D4 direction classes with |theta|^2 <= 25 at the 62 pockets where (2,1) is blind.

Fixed-room check approved by Daniel on 2026-11-02. The pockets are exactly those
with no loaded (2,1) core in existing_rooms_21.json; the direction list is the
one used for the Section 33 room. Same pocket placement, tracer, and second
tracer as existing_rooms_21.py.
"""
import json
import sys
from fractions import Fraction as F
import importlib.util

spec = importlib.util.spec_from_file_location("er", "existing_rooms_21.py")
er = importlib.util.module_from_spec(spec)
spec.loader.exec_module(er)
cl = er.cl

DIRECTIONS = [(1, 0), (1, 1), (2, 1), (3, 1), (3, 2), (4, 1), (4, 3)]


def main():
    rooms = {f"study{k}": json.loads(l) for k, l in enumerate(open(er.SEED + "study.jsonl"))}
    rooms |= {f"res{k}": json.loads(l) for k, l in enumerate(open(er.SEED + "res_rooms.jsonl"))}
    blind = [p for p in json.load(open("existing_rooms_21.json"))["pockets"] if p["loaded"] == 0]
    out, mismatches = [], 0
    for p in blind:
        V = [tuple(x) for x in rooms[p["room"]]["V"]]
        B, A, C = [tuple(x) for x in p["pocket_BAC"]]
        f = er.to_s33(B, A, C)
        V2 = [f(x) for x in V]
        tris = er.triangles(V2)
        assert len(tris) == er.shoelace2(V2)
        cl.TRIANGLES = tris
        cl.ROOM = {cl.key(F(sum(q[0] for q in t), 3), F(sum(q[1] for q in t), 3)) for t in tris}
        pts = er.unit_points(V2)
        W = [tuple(sorted(s)) for s in zip(pts, pts[1:] + pts[:1])]
        row = {"room": p["room"], "pocket_BAC": p["pocket_BAC"], "directions": {}}
        for th in DIRECTIONS:
            d = cl.run_direction(th)
            er.THETA = th
            for c in d["cores"]:
                x0 = F(c["start_x_on_D"])
                got = er.second_trace(W, V2, (x0, 2 - x0), tuple(c["start_velocity"]))
                mismatches += got != (c["wall_hits"], c["D_hits"], c["H_hits"], c["Q"])
            assert d["strip_weighted_sum"] == [0, 0]
            qs = [c["Q"] for c in d["cores"]]
            row["directions"][str(th)] = {"cores": len(qs), "loaded": sum(q != [0, 0] for q in qs),
                                          "odd": sum(q[0] % 2 != 0 for q in qs), "Q": qs}
        out.append(row)
        print(p["room"], p["pocket_BAC"], " ".join(
            f"{k}:{v['loaded']}/{v['cores']}{'*' if v['odd'] else ''}" for k, v in row["directions"].items()), flush=True)
    json.dump({"pockets": out, "second_tracer_mismatches": mismatches}, open(sys.argv[1], "w"), indent=1, default=str)
    first = {}
    for r in out:
        hit = next((k for k, v in r["directions"].items() if v["loaded"]), None)
        first[hit] = first.get(hit, 0) + 1
    print("pockets", len(out), "first loaded direction:", first)
    print("second tracer mismatches", mismatches)
    sys.exit(1 if mismatches else 0)


if __name__ == "__main__":
    main()
