"""Convert the record's 34-wall orthogonal room (triangles) to unit cells."""
import json
from collections import Counter


def load34(path="inputs/historical34-room.json"):
    d = json.load(open(path))
    cnt = Counter()
    for tri in d["triangles"]:
        xs = [p[0] for p in tri]
        ys = [p[1] for p in tri]
        assert max(xs) - min(xs) == 1 and max(ys) - min(ys) == 1
        cnt[(min(xs), min(ys))] += 1
    assert all(v == 2 for v in cnt.values()), "not a union of unit cells"
    return set(cnt), [tuple(p) for p in d["marked"]]
