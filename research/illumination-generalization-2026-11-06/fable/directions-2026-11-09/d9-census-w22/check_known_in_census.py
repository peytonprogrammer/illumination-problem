"""Find the record's rooms inside the census output (area <= CERTMAX files).

For the known 22-wall room and every k7 model / W18 control with area <= 16,
find the census room with the same canonical form (8 lattice symmetries) and
print its W and pair verdicts.  Expected: the known room has exactly one pair
and it is unresolved (U, separated); every k7 room's pairs are lit (L).
usage: python3 check_known_in_census.py runs/a20 NJ
"""
import glob
import json
import sys

HERE = sys.path[0]
sys.path.insert(1, HERE + "/../d2-factor-audit")
import room_model as rm                     # noqa: E402
from check_enum_small import canon         # noqa: E402


def opn(path):
    """Open a text file, or its gzip-compressed copy path + '.gz'."""
    import gzip
    import os
    if not os.path.exists(path) and os.path.exists(path + ".gz"):
        return gzip.open(path + ".gz", "rt")
    return open(path)


def main():
    rdir, nj = sys.argv[1], int(sys.argv[2])
    want = {canon(rm.cells_from_vertices(rm.Q22)): "known 22-wall room"}
    for f in sorted(glob.glob("inputs/k7-models/model-*.json")):
        d = json.load(open(f))
        if len(d["cells"]) <= 16:
            want.setdefault(canon([tuple(c) for c in d["cells"]]), f.split("/")[-1])
    d = json.load(open("inputs/k7-controls.json"))
    for c in d["controls"]:
        if "cells" in c and len(c["cells"]) <= 16:
            want.setdefault(canon([tuple(x) for x in c["cells"]]), c["control"])
    found = {}
    for j in range(nj):
        cur = None
        for line in opn(f"{rdir}/job-{j}.out"):
            f = line.split()
            if not f or f[0] == "#":
                continue
            if f[0] == "R":
                v = list(map(int, f[5:]))
                key = canon([(v[i], v[i + 1]) for i in range(0, len(v), 2)])
                cur = key if key in want else None
                if cur:
                    found[cur] = {"job": j, "rid": f[1], "W": int(f[3]), "pairs": []}
            elif f[0] == "P" and cur:
                found[cur]["pairs"].append(" ".join(f[1:7]))
    for key, name in want.items():
        if key in found:
            r = found[key]
            print(f"{name}: census job {r['job']} room {r['rid']}, W {r['W']}, pairs: {r['pairs']}")
        else:
            print(f"{name}: NOT FOUND in census output")


if __name__ == "__main__":
    main()
