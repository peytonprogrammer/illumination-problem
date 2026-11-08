"""Independent fixed-witness audit. No search or author code execution.

Each triangle is intersected with each prescribed open path leg by rational
half-plane clipping. Requiring every intersecting incident triangle protects
the full neighborhood of every point on that leg, including mesh vertices.
Bounce neighborhoods are proved separately by complete half-plane occupancy.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[1] / "illumination-k4-codex"
READS = {}


def read(relative):
    p = BASE / relative
    READS[relative] = hashlib.sha256(p.read_bytes()).hexdigest()
    return json.loads(p.read_text())


def add(a, b): return tuple(x + y for x, y in zip(a, b))
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def mul(a, x): return tuple(x * v for v in a)
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def det(a, b): return a[0] * b[1] - a[1] * b[0]
def triangle(t): return tuple(sorted(tuple(F(v) for v in p) for p in t))
def decode(ts): return {triangle(t) for t in ts}
def points(ps): return [tuple(F(v) for v in p) for p in ps]
def fraction_pairs(ps): return [tuple(F(*v) for v in p) for p in ps]


DIR = [(1, 0), (1, 1), (0, 1), (-1, 1),
       (-1, 0), (-1, -1), (0, -1), (1, -1)]
CENTERS = {"L": (-2, 0), "B": (0, -2), "D": (2, -2),
           "R": (4, 0), "E": (4, 2), "Tc": (2, 4), "N": (0, 2)}


def fan(center, sectors=range(8)):
    if isinstance(center, str): center = CENTERS[center]
    return {triangle([center, add(center, DIR[i]),
                      add(center, DIR[(i + 1) % 8])]) for i in sectors}


H = set().union(*(fan(c) for c in [(0, 0), (2, 0), (2, 2)]))
LOCAL = H | set().union(*(fan(c) for c in CENTERS))


def oriented(t):
    a, b, c = t
    return (a, b, c) if det(sub(b, a), sub(c, a)) > 0 else (a, c, b)


def contains(t, p):
    t = oriented(t)
    return all(det(sub(t[(i + 1) % 3], t[i]), sub(p, t[i])) >= 0
               for i in range(3))


def clip(t, a, b):
    """Closed parameter interval of a + s(b-a) in the closed triangle."""
    t = oriented(t)
    lo, hi = F(0), F(1)
    for i in range(3):
        edge = sub(t[(i + 1) % 3], t[i])
        alpha = det(edge, sub(a, t[i]))
        beta = det(edge, sub(b, a))
        if beta > 0: lo = max(lo, -alpha / beta)
        elif beta < 0: hi = min(hi, -alpha / beta)
        elif alpha < 0: return None
        if lo > hi: return None
    return lo, hi


def tiling_for(P):
    # Any incident triangle center is within one coordinate unit of the path.
    xs, ys = list(zip(*P))
    return set().union(*(fan((x, y))
        for x in range(2 * (min(xs).__floor__() // 2 - 1),
                       2 * (max(xs).__ceil__() // 2 + 2), 2)
        for y in range(2 * (min(ys).__floor__() // 2 - 1),
                       2 * (max(ys).__ceil__() // 2 + 2), 2)))


def reflection(v, tangent):
    return sub(mul(tangent, 2 * dot(v, tangent) / dot(tangent, tangent)), v)


def mirror_direction(before, p, after):
    vin, vout = sub(p, before), sub(after, p)
    candidates = []
    for w in [(1, 0), (0, 1), (1, 1), (1, -1)]:
        r = reflection(vin, w)
        if det(r, vout) == 0 and dot(r, vout) > 0:
            candidates.append(tuple(F(x) for x in w))
    assert len(candidates) == 1, (p, candidates)
    return candidates[0]


def on_segment(p, a, b):
    return det(sub(p, a), sub(b, a)) == 0 and dot(sub(p, a), sub(p, b)) <= 0


def support(P):
    tiles = tiling_for(P)
    required, forbidden, legs, mirrors = set(), set(), [], []
    for a, b in zip(P, P[1:]):
        crossings = []
        for t in tiles:
            interval = clip(t, a, b)
            if interval is not None:
                lo, hi = interval
                if hi > 0 and lo < 1:
                    required.add(t)
                    crossings.append([t, lo, hi])
        legs.append(crossings)
    for before, p, after in zip(P, P[1:], P[2:]):
        tangent = mirror_direction(before, p, after)
        side = det(tangent, sub(before, p))
        assert side * det(tangent, sub(after, p)) > 0
        for t in tiles:
            if not contains(t, p): continue
            signs = [det(tangent, sub(q, p)) for q in t]
            assert min(signs) >= 0 or max(signs) <= 0, (p, t)
            centroid_side = sum(signs)
            assert centroid_side
            (required if side * centroid_side > 0 else forbidden).add(t)
        mirrors.append((p, tangent))
    assert not required & forbidden
    return required, forbidden, legs, mirrors


def first_target(P):
    assert all(not on_segment(P[-1], a, b) for a, b in zip(P[:-2], P[1:-1]))


def sigma(p): return (2 - p[1], 2 - p[0])
def sigma_tiles(ts): return {triangle([sigma(p) for p in t]) for t in ts}


def witness(P, minimum, maximum):
    assert P[0] == (0, 0) and P[-1] == (2, 2)
    assert minimum <= maximum
    u, z, legs, mirrors = support(P)
    assert u <= minimum, ("missing support", u - minimum)
    assert not z & maximum, ("removed mirror", z & maximum)
    # Marks are interior, rather than merely contained in one incident tile.
    for p in [P[0], P[-1]]:
        assert {t for t in tiling_for(P) if contains(t, p)} <= minimum
    first_target(P)
    ur, zr, _, _ = support(P[::-1])
    assert (ur, zr) == (u, z)
    PS = [sigma(p) for p in P[::-1]]
    us, zs, _, _ = support(PS)
    assert (us, zs) == (sigma_tiles(u), sigma_tiles(z))
    first_target(PS)
    q = P[-1]
    for p, tangent in mirrors[::-1]:
        q = add(p, reflection(sub(q, p), tangent))
    assert det(sub(q, P[0]), sub(P[1], P[0])) == 0
    assert dot(sub(q, P[0]), sub(P[1], P[0])) > 0
    return {"reflections": len(P) - 2, "required": sorted(u),
            "forbidden": sorted(z), "unfolded_target": q,
            "triangle_clip_counts_per_leg": [len(x) for x in legs],
            "mirror_tangents": [v for _, v in mirrors],
            "first_target_reverse_sigma": "PASS"}


def intersections(a, b, c, d):
    v, w = sub(b, a), sub(d, c)
    denominator = det(v, w)
    if denominator:
        t = det(sub(c, a), w) / denominator
        s = det(sub(c, a), v) / denominator
        return [t] if 0 <= t <= 1 and 0 <= s <= 1 else []
    if det(sub(c, a), v): return []
    axis = 0 if v[0] else 1
    ts = sorted([(c[axis] - a[axis]) / v[axis],
                 (d[axis] - a[axis]) / v[axis]])
    lo, hi = max(F(0), ts[0]), min(F(1), ts[1])
    return [lo, hi] if lo <= hi else []


def boundary(tiles):
    counts = Counter()
    for t in tiles:
        t = oriented(t)
        for i in range(3): counts[(t[i], t[(i + 1) % 3])] += 1
    edges = {e for e, n in counts.items() if counts[(e[1], e[0])] == 0}
    assert all(n == 1 for n in counts.values())
    outgoing, incoming = defaultdict(list), defaultdict(list)
    for a, b in edges: outgoing[a].append(b); incoming[b].append(a)
    assert set(outgoing) == set(incoming)
    assert all(len(outgoing[p]) == len(incoming[p]) == 1 for p in outgoing)
    start = min(outgoing)
    cycle, p = [], start
    while p not in cycle:
        cycle.append(p); p = outgoing[p][0]
    assert p == start and len(cycle) == len(edges), "multiple cycles or boundary contact"
    V = [p for i, p in enumerate(cycle)
         if det(sub(p, cycle[i - 1]), sub(cycle[(i + 1) % len(cycle)], p))]
    for i in range(len(V)):
        for j in range(i + 1, len(V)):
            if j == i + 1 or (i == 0 and j == len(V) - 1): continue
            assert not intersections(V[i], V[(i + 1) % len(V)],
                                     V[j], V[(j + 1) % len(V)])
    return V, len(edges)


def physical(P, V):
    walls = []
    for index, (a, b) in enumerate(zip(P, P[1:])):
        hits = []
        for c, d in zip(V, V[1:] + V[:1]):
            hits.extend((t, c, d) for t in intersections(a, b, c, d) if t > 0)
        if index == len(P) - 2:
            assert not hits
        else:
            assert len(hits) == 1 and hits[0][0] == 1, (index, hits)
            _, c, d = hits[0]
            assert b not in V and on_segment(b, c, d)
            reflected = reflection(sub(b, a), sub(d, c))
            assert det(reflected, sub(P[index + 2], b)) == 0
            assert dot(reflected, sub(P[index + 2], b)) > 0
            walls.append((c, d))
    first_target(P)
    return walls


def angle_at(tiles, p):
    total = 0
    for t in tiles:
        if p not in t: continue
        a, b = [sub(q, p) for q in t if q != p]
        total += 90 if dot(a, b) == 0 else 45
    return total


def inherited_dispatch(minimum, maximum, forbidden):
    """Recheck fixed inherited witnesses rather than trusting PASS labels."""
    zero = read("zero-surplus-L/cover-check.json")
    old_guards = read("third-surplus-review/independent-review/guard-extension-check.json")
    receipt = read("surplus-four-local/e2-e1-b1/critical-B-check.json")
    named = {r["name"]: r for r in receipt["whole_envelopes"]}
    paths = {
        "one_sigma": fraction_pairs(zero["paths"]["one_sigma"]["path"]),
        "four_sigma": fraction_pairs(zero["paths"]["four_sigma"]["path"]),
        "sigma_centeredB3": fraction_pairs(old_guards["forcing_paths"]["sigma_centeredB3"]["path"]),
        "sigma_outerB2": fraction_pairs(old_guards["forcing_paths"]["sigma_outerB2"]["path"]),
    }
    force_results = {}
    expected = {
        "force_E4": (H, LOCAL - fan("E", [4]), 1),
        "force_L0_Eordinary": (H | fan("E", [4]),
            (LOCAL - fan("E") - fan("L", [0])) | fan("E", [4]), 4),
        "force_L0_Ecenter": (H | fan("E", [3, 4]),
            (LOCAL - fan("E") - fan("L", [0])) | fan("E", [3, 4]), 3),
        "force_L0_Eouter": (H | fan("E", [4, 5]),
            (LOCAL - fan("E") - fan("L", [0])) | fan("E", [4, 5]), 2),
    }
    for name, (mi, ma, count) in expected.items():
        row = named[name]
        assert (decode(row["minimum"]), decode(row["maximum"])) == (mi, ma)
        force_results[name] = witness(paths[row["path"]], mi, ma)
        assert force_results[name]["reflections"] == count
    prior = read("fourth-surplus-review/mixed-e2-e1/joined-four-check.json")
    four, six = points(prior["path"]), points(prior["six_path_complement"]["path"])
    D23 = fan("D", [2, 3])
    other = set().union(*(fan(k) for k in ["L", "R", "E", "N"]))
    four_result = witness(four, minimum | D23, minimum | D23 | other | fan("Tc", [6]))
    six_result = witness(six, minimum | D23 | fan("Tc", [5]),
                         minimum | D23 | other | fan("Tc", [5]))
    assert (four_result["reflections"], six_result["reflections"]) == (4, 6)
    assert (len(four_result["required"]), len(four_result["forbidden"])) == (15, 3)
    assert (len(six_result["required"]), len(six_result["forbidden"])) == (14, 4)
    # All possible ordinary caps after E4/L0 forcing, using unions as an
    # overapproximation rather than assembling/enumerating completed rooms.
    ordinary = {"L": [0], "D": [1, 2], "R": [3, 4], "E": [4],
                "Tc": [5, 6], "N": [0, 5, 6, 7]}
    root_windows = {"L": [[7, 0], [0, 1]], "D": [[0, 1], [1, 2], [2, 3]],
                    "R": [[2, 3], [3, 4], [4, 5]],
                    "E": [[3, 4], [4, 5]],
                    "Tc": [[4, 5], [5, 6], [6, 7]],
                    "N": [[4, 5], [5, 6], [6, 7], [7, 0], [0, 1]]}
    dispatch = []
    for root, windows in root_windows.items():
        others = set().union(*(fan(k, ss) for k, ss in ordinary.items() if k != root))
        for window in windows:
            label = root + "".join(map(str, window))
            upper = minimum | fan(root, window) | others
            if label == "L70":
                assert forbidden & upper
                dispatch.append({"partner": label, "status": "EXPLICITLY_EXCLUDED"})
            elif label == "D23":
                dispatch.append({"partner": label, "status": "RECHECKED_FOUR_SIX_TC_SPLIT"})
            else:
                assert minimum <= upper <= maximum, label
                dispatch.append({"partner": label, "status": "NEW_FIVE_SUPPORT_CONTAINMENT"})
    assert len(dispatch) == 18
    return {"short_forcing_witnesses": force_results,
            "D23_Tc_empty_or_6": four_result, "D23_Tc_5": six_result,
            "symbolic_partner_dispatch": dispatch,
            "upstream_assumptions": "The established local two-root/root-window/ordinary-cap classification; not a fresh proof of the global classification."}


def main():
    raw = read("surplus-four-local/O3-R23-search/room.json")
    candidate = read("surplus-four-local/O3-R23-search/result.json")
    author = read("surplus-four-local/O3-R23-search/verification.json")
    P = points([(0, 0), (-1, F(-2, 5)), (1, F(-6, 5)), (0, F(-8, 5)),
                (1, -2), (F(2, 7), F(-16, 7)), (2, 2)])
    assert P == [tuple(F(*v) for v in p) for p in candidate["candidate"]["path"]]
    room = decode(raw["triangles"])
    assert room == H | set().union(*(fan(k, ss) for k, ss in raw["spec"].items()))
    V, atomic = boundary(room)
    assert len(V) == 20 and set(V) == set(map(tuple, raw["vertices"]))
    walls = physical(P, V)
    physical(P[::-1], V)
    physical([sigma(p) for p in P[::-1]], [sigma(p) for p in V])
    vertices = {p for t in room for p in t}
    As = {p for p in vertices if p[0] % 2 == 0 and p[1] % 2 == 0}
    fullA = {p for p in As if angle_at(room, p) == 360}
    assert fullA == {(0, 0), (2, 0), (2, 2)}
    J = sum(angle_at(room, p) == 360 for p in vertices - As)
    sN = sum(angle_at(room, p) == 180 for p in vertices - As)
    assert (J, sN) == (2, 4)
    assert angle_at(room, (1, -2)) == 180 and (1, -2) not in V
    assert angle_at(room, (0, -2)) == 135
    minimum = H | fan("B", [7, 0, 1])
    maximum = minimum | (fan("L") - fan("L", [7])) | (fan("D") - fan("D", [3, 4]))
    maximum |= set().union(*(fan(k) for k in ["R", "E", "Tc", "N"]))
    assert minimum <= room <= maximum
    new = witness(P, minimum, maximum)
    assert decode(new["required"]) == decode(author["whole_support"]["required"])
    assert decode(new["forbidden"]) == fan("L", [7]) | fan("D", [3, 4]) | fan("B", [2, 6])
    assert len(new["required"]) == 11 and len(new["forbidden"]) == 5
    assert new["unfolded_target"] == (-10, -4)
    dispatch = inherited_dispatch(minimum, maximum, decode(new["forbidden"]))
    # Check the fixed rational root against every stated contact formula.
    d = F(2, 5)
    assert F(1, 3) < d < F(3, 7)
    assert P[1:-1] == [(-1, -d), (1, -3*d), (0, -4*d), (1, -5*d),
                         ((6*d-2)/(1+d), -8*d/(1+d))]
    assert 10*d-2 == 2 and 0 < 7*d-2 < 1 and 1 < 9*d-2 < 3
    # Mutation controls: the engine must reject a non-specular contact and
    # an envelope that allows filling any one of the five protected tiles.
    mutation_failures = []
    corrupt = P.copy(); corrupt[3] = (F(0), F(-7, 5))
    try: witness(corrupt, minimum, maximum)
    except AssertionError: mutation_failures.append("non_specular_contact")
    else: raise AssertionError("failed to detect changed contact")
    for tile in decode(new["forbidden"]):
        try: witness(P, minimum, maximum | {tile})
        except AssertionError: mutation_failures.append("filled_mirror_mate")
        else: raise AssertionError("failed to detect lost mirror")
    result = {"verdict": "NEW_FIVE_REFLECTION_OPTICAL_LEMMA_PASS",
              "geometry": {"tiles": len(room), "maximal_walls": len(V),
                           "atomic_boundary_edges": atomic, "J": J, "sN": sN,
                           "full_A": sorted(fullA), "smooth_C_angle": 180,
                           "avoided_O3_apex_angle": 135},
              "path": P, "finite_mirrors": walls, "new_lemma": new,
              "family_dispatch": dispatch,
              "mutation_controls_rejected": mutation_failures,
              "source_sha256": READS,
              "limits": "Fixed supplied path and room only; no discovery or author-code execution."}
    (OUT / "check.json").write_text(json.dumps(result, indent=2, default=str) + "\n")
    print("PASS: frozen polygon, finite first walls, specularity, first T, reverse/sigma, 11U/5Z; four forcing paths and D23 four/six rechecked; 18 symbolic partner windows with L70 excluded; 6 mutation rejections.")


if __name__ == "__main__": main()
