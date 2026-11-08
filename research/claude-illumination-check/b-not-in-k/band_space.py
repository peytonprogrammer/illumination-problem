"""Space test for closed mirror bands (part of the approved enumeration, Section 11). Flood-fill from the
pocket across every edge whose far triangle isn't decided out. A band can complete to a room with two
interior A marks only if this region reaches two A points with all eight triangles reachable. A region
that stays inside the band box and has fewer than two such points can't complete in any box."""
import json
import sys
from fractions import Fraction as F
import importlib.util

s = importlib.util.spec_from_file_location("mb", "mirror_bands.py")
mb = importlib.util.module_from_spec(s)
s.loader.exec_module(mb)
R = int(sys.argv[1])
mb.R = R


def nbrs(k):
    v = mb.verts(k)
    out = []
    for a in range(3):
        e = {v[a], v[(a + 1) % 3]}
        for p in e:
            for k2 in mb.tris_at(p):
                if k2 != k and e <= set(mb.verts(k2)):
                    out.append(k2)
    return set(out)


cen = lambda t: mb.key(F(sum(p[0] for p in t), 3), F(sum(p[1] for p in t), 3))
bands = json.load(open(f"mirror_bands_R{R}.json"))["bands"]
res = {"closed_no_space": 0, "open_or_space": 0}
rows = []
for b in bands:
    out = {cen([tuple(q) for q in t]) for t in b["tris_out"]}
    start = mb.key(F(4, 3), F(1, 3))
    seen, stack, escaped = {start}, [start], False
    while stack and not escaped:
        k = stack.pop()
        for k2 in nbrs(k):
            if k2 in out or k2 in seen:
                continue
            if not mb.in_box(k2):
                escaped = True
                break
            seen.add(k2)
            stack.append(k2)
    fans = sum(1 for p in {p for k in seen for p in mb.verts(k)}
               if mb.ptype(p) == "A" and all(k in seen for k in mb.tris_at(p)))
    ok = escaped or fans >= 2
    res["open_or_space" if ok else "closed_no_space"] += 1
    rows.append({"escaped": escaped, "region": len(seen), "full_fan_slots": fans})
json.dump({"R": R, "summary": res, "bands": rows}, open(f"band_space_R{R}.json", "w"))
print(R, res)
