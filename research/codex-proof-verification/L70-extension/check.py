"""Independent audit of the fixed L70 six-path and its stated scope.

Uses only our previously authored rational triangle-clipping primitives.
No author code, discovery search, or completed-room enumeration.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import runpy

OUT = Path(__file__).resolve().parent
ENGINE = OUT.parent / "O3-five/check.py"
g = runpy.run_path(str(ENGINE))
BASE = OUT.parents[1] / "illumination-k4-codex"
fan, H = g["fan"], g["H"]
decode, witness, angle = g["decode"], g["witness"], g["angle_at"]
sources = {}


def read(relative):
    p = BASE / relative
    sources[relative] = hashlib.sha256(p.read_bytes()).hexdigest()
    return json.loads(p.read_text())


def witness_with_source_revisit(P, minimum, maximum):
    """A legal billiard may pass its initial mark again before reaching T.

    Verify the whole forward witness and reversed geometry, but do not claim
    the full reverse reaches its target for the first time only at its end.
    The valid first-target reverse is checked separately as the four suffix.
    """
    u, z, legs, mirrors = g["support"](P)
    assert u <= minimum and not z & maximum
    g["first_target"](P)
    ur, zr, _, _ = g["support"](P[::-1])
    assert (ur, zr) == (u, z)
    ps = [g["sigma"](p) for p in P[::-1]]
    us, zs, _, _ = g["support"](ps)
    assert (us, zs) == (g["sigma_tiles"](u), g["sigma_tiles"](z))
    q = P[-1]
    for p, tangent in mirrors[::-1]:
        q = g["add"](p, g["reflection"](g["sub"](q, p), tangent))
    return {"reflections": len(P)-2, "required": sorted(u), "forbidden": sorted(z),
            "unfolded_target": q, "triangle_clip_counts_per_leg": [len(x) for x in legs],
            "mirror_tangents": [v for _, v in mirrors],
            "forward_first_T": "PASS", "reverse_sigma_geometry": "PASS",
            "reverse_first_target": "Use the verified four-reflection suffix; full eleven revisits S."}


def audit_N7(O3L70):
    receipt = read("surplus-four-local/L70-N7-search/verification.json")
    raw = read("surplus-four-local/L70-N7-search/room.json")
    found = read("surplus-four-local/L70-N7-search/result.json")
    eleven = g["points"]([
        (0, 0), (F(-1, 4), -1), (F(-3, 4), 1), (F(-6, 5), F(-4, 5)),
        (3, F(1, 4)), (0, 1), (F(-4, 3), F(2, 3)),
        (F(-8, 5), F(-2, 5)), (3, F(3, 4)),
        (F(2, 3), F(4, 3)), (F(1, 2), 2), (F(2, 5), F(8, 5)), (2, 2)])
    nine = g["points"]([
        (0, 0), (F(-1, 4), -1), (F(-3, 4), 1), (F(-6, 5), F(-4, 5)),
        (F(18, 5), F(2, 5)), (F(7, 2), 0), (F(10, 3), F(2, 3)),
        (F(2, 3), F(4, 3)), (F(1, 2), 2), (F(2, 5), F(8, 5)), (2, 2)])
    full_other = set().union(*(fan(k) for k in ["D", "E", "Tc"]))
    base = H | fan("L", [7, 0]) | fan("N", [7])
    min11 = base
    max11 = base | (fan("B") - fan("B", [2])) | full_other
    max11 |= (fan("R") - fan("R", [3])) | fan("N", [1, 2, 3, 4])
    min9 = base | fan("R", [3])
    max9 = min9 | (fan("B") - fan("B", [2])) | full_other
    max9 |= fan("R", [0, 1, 5, 6, 7]) | fan("L", [1, 2, 3, 4, 5]) | fan("N", [1, 2, 3, 4])
    outputs = {}
    for name, P, mi, ma, counts, image in [
        ("eleven", eleven, min11, max11, (22, 7), (-6, -24)),
        ("nine", nine, min9, max9, (21, 7), (-4, -16))]:
        author = receipt[name]
        assert P == g["points"](author["path"])
        assert (mi, ma) == (decode(author["minimum"]), decode(author["maximum"]))
        result = witness_with_source_revisit(P, mi, ma) if name == "eleven" else witness(P, mi, ma)
        assert (len(result["required"]), len(result["forbidden"])) == counts
        assert decode(result["required"]) == decode(author["required"])
        assert decode(result["forbidden"]) == decode(author["forbidden"])
        assert result["unfolded_target"] == image
        outputs[name] = result
    assert decode(outputs["eleven"]["forbidden"]) == fan("L", [1, 6]) | fan("B", [2]) | fan("R", [3]) | fan("N", [0, 5, 6])
    assert decode(outputs["nine"]["forbidden"]) == fan("L", [6]) | fan("B", [2]) | fan("R", [2, 4]) | fan("N", [0, 5, 6])
    room = decode(raw["triangles"])
    assert room == H | set().union(*(fan(k, ss) for k, ss in raw["spec"].items()))
    assert len(room) == 33 and min11 <= room <= max11
    V, atomic = g["boundary"](room)
    assert len(V) == 20 and set(V) == set(map(tuple, raw["vertices"]))
    walls = g["physical"](eleven, V)
    assert eleven == g["fraction_pairs"](found["candidate"]["path"])
    verts = {p for t in room for p in t}
    nonA = {p for p in verts if not (p[0] % 2 == p[1] % 2 == 0)}
    assert {p for p in verts - nonA if angle(room, p) == 360} == {(0, 0), (2, 0), (2, 2)}
    assert sum(angle(room, p) == 360 for p in nonA) == 3
    assert sum(angle(room, p) == 180 for p in nonA) == 3
    assert angle(room, (0, 1)) == 180 and (F(0), F(1)) not in V
    ceiling = [(a, b) for a, b in zip(V, V[1:] + V[:1])
               if g["on_segment"]((F(0), F(1)), a, b)]
    assert len(ceiling) == 1 and set(ceiling[0]) == {(-1, 1), (1, 1)}
    assert angle(min11, (-1, 0)) == 360
    assert g["on_segment"]((-1, 0), eleven[2], eleven[3])
    # The eleven-reflection witness visits actual S a second time in the
    # open leg from its seventh to eighth bounce. Keep its supplied suffix.
    assert g["on_segment"]((F(0), F(0)), eleven[7], eleven[8])
    four = [eleven[0]] + eleven[8:]
    min4 = H | fan("N", [7])
    max4 = g["LOCAL"] - fan("R", [3]) - fan("N", [0, 6])
    four_result = witness(four, min4, max4)
    assert (len(four_result["required"]), len(four_result["forbidden"])) == (9, 3)
    assert decode(four_result["forbidden"]) == fan("R", [3]) | fan("N", [0, 6])
    assert four_result["unfolded_target"] == (8, 2)
    g["physical"](four, V)
    g["physical"](four[::-1], V)
    g["physical"]([g["sigma"](p) for p in four[::-1]], [g["sigma"](p) for p in V])
    assert max11 <= max4
    outputs["four_suffix"] = four_result
    # Direct hand formulas at the unique target-matching root.
    d = F(1, 4)
    assert F(5, 21) < d < F(6, 23) and F(3, 13) < d < F(4, 15)
    common = [(-d, F(-1)), (-3*d, F(1)),
              (-6*d/(1+d), (4*d-2)/(1+d))]
    assert eleven[1:4] == nine[1:4] == common
    N11 = 6 - 22*d
    eleven_formula = common + [(F(3), 9*d-2), (12-3/d, F(1)),
        ((2-12*d)/(1-d), (4-14*d)/(1-d)),
        ((2-16*d)/(1+d), (14*d-4)/(1+d)),
        (F(3), 19*d-4),
        (N11/(1-d), 2-N11/(1-d)), (N11, F(2)),
        (N11/(1+d), 2-N11/(1+d))]
    assert eleven[1:-1] == eleven_formula and 24*d-4 == 2
    N9 = 4 - 14*d
    nine_formula = common + [(6*(1-d)/(1+d), 4-6*(1-d)/(1+d)),
        (6-10*d, F(0)), ((6-14*d)/(1-d), (10*d-2)/(1-d)),
        (N9/(1-d), 2-N9/(1-d)), (N9, F(2)),
        (N9/(1+d), 2-N9/(1+d))]
    assert nine[1:-1] == nine_formula and 16*d-2 == 2
    assert F(1, 5) < d < F(2, 7) and 8*d == 2
    n4 = 2 - 6*d
    assert four[1:-1] == [(F(3), 3*d), (n4/(1-d), 2-n4/(1-d)),
                           (n4, F(2)), (n4/(1+d), 2-n4/(1+d))]
    # Exact whole dispatch: ordinary N7 excludes the other N caps. R3
    # versus R4/empty is exhaustive. All D/Tc support may be present.
    o3N7 = O3L70 | fan("N", [7])
    assert min9 <= o3N7 | fan("R", [3]) <= max9
    assert o3N7 | fan("R", [3]) | full_other <= max9
    assert min11 <= o3N7 | fan("R", [4]) | full_other <= max11
    assert min11 <= o3N7 | full_other <= max11
    assert min4 <= o3N7 | fan("R", [4]) | full_other <= max4
    assert min4 <= o3N7 | full_other <= max4
    for name in ["findings.txt", "verify.py", "coverage.txt"]:
        p = BASE / "surplus-four-local/L70-N7-search" / name
        sources[str(p.relative_to(BASE))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return {"paths": outputs, "frozen_eleven_room": {
        "tiles": 33, "walls": 20, "atomic_edges": atomic, "J": 3, "sN": 3,
        "smooth_ceiling": 180, "interior_L_portal": 360, "finite_mirrors": walls},
        "whole_dispatch": "N7 absent: six or missing-E4 one. N7 and ordinary R3: nine. N7 and R4/empty: FOUR (suffix of supplied eleven). All D/Tc choices allowed. Entire local O3/L70 <=9.",
        "four_suffix_path": four,
        "review_improvement": "Original eleven remains legal, but revisits S after bounce7. Its final four reflections suffice; full reverse/sigma must stop at the earlier target."}


def main():
    parent = read("surplus-four-local/O3-L70-hand/check.json")
    P = g["points"]([
        (0, 0), (F(-12, 7), F(-2, 7)), (F(-8, 5), F(2, 5)),
        (F(16, 5), F(6, 5)), (F(10, 3), 2),
        (F(24, 7), F(10, 7)), (1, F(11, 6)), (2, 2)])
    assert P == g["points"](parent["path"])
    minimum = H | fan("L", [7, 0]) | fan("E", [4])
    maximum = minimum | set().union(*(fan(k) for k in ["B", "D", "R", "Tc"]))
    maximum |= fan("N", [0, 1, 2, 3, 4, 5, 6])
    assert (minimum, maximum) == (decode(parent["whole_support"]["minimum"]),
                                  decode(parent["whole_support"]["maximum"]))
    result = witness(P, minimum, maximum)
    u, z = decode(result["required"]), decode(result["forbidden"])
    assert len(u) == 15 and len(z) == 5
    assert u == decode(parent["whole_support"]["required"])
    assert z == fan("L", [1, 6]) | fan("E", [3, 5]) | fan("N", [7])
    assert result["unfolded_target"] == (-12, -2)
    d = F(1, 6)
    assert F(1, 7) < d < F(2, 11)
    formulas = [
        (-2 / (1 + d), -2 * d / (1 + d)),
        ((4 * d - 2) / (1 - d), 2 * d / (1 - d)),
        ((2 + 4 * d) / (1 - d), 6 * d / (1 - d)),
        (2 + 8 * d, F(2)),
        ((2 + 12 * d) / (1 + d), 10 * d / (1 + d)),
        (F(1), 11 * d)]
    assert P[1:-1] == formulas and 12 * d == 2
    # All contacts are strict inside the claimed finite sides.
    assert -2 < P[1][0] < -1 and -2 < P[2][0] < -1
    assert all(3 < P[i][0] < 4 for i in [3, 4, 5])
    assert 1 < P[6][1] < 2
    assert g["on_segment"]((F(2), F(1)), P[2], P[3])
    incident = {t for t in g["tiling_for"](P) if g["contains"](t, (2, 1))}
    assert incident <= H and angle(H, (2, 1)) == 360
    # Ordinary caps cannot add forbidden tiles, except N7 explicitly.
    O3L70 = H | fan("B", [7, 0, 1]) | fan("L", [7, 0]) | fan("E", [4])
    ordinary_other = fan("D", [1, 2]) | fan("R", [3, 4]) | fan("Tc", [5, 6])
    nonN7_upper = O3L70 | ordinary_other | fan("N", [0, 5, 6])
    assert minimum <= O3L70 <= nonN7_upper <= maximum
    assert z & fan("N", [7])
    # A separate inherited six-path covers ordinary Tc5 even when N7 exists.
    previous = read("fourth-surplus-review/mixed-e2-e1/joined-four-check.json")
    oldP = g["points"](previous["six_path_complement"]["path"])
    Tc5_minimum = O3L70 | fan("Tc", [5])
    Tc5_maximum = Tc5_minimum | fan("D", [1, 2]) | fan("R", [3, 4])
    Tc5_maximum |= fan("N", [0, 5, 6, 7])
    prior_result = witness(oldP, Tc5_minimum, Tc5_maximum)
    # Derive the fixed local non-A angle coefficients symbolically; do not
    # assemble cap assignments or polygons.
    single_caps = {"D1": fan("D", [1]), "D2": fan("D", [2]),
        "R3": fan("R", [3]), "R4": fan("R", [4]),
        "Tc5": fan("Tc", [5]), "Tc6": fan("Tc", [6]),
        "N0": fan("N", [0]), "N5": fan("N", [5]),
        "N6": fan("N", [6]), "N7": fan("N", [7])}
    vertices = {p for t in O3L70 | set().union(*single_caps.values()) for p in t}
    coefficients = {}
    full_nonA = []
    for p in vertices:
        if p[0] % 2 == 0 and p[1] % 2 == 0:
            continue
        fixed = angle(O3L70, p)
        contributions = {name: angle(ts, p) for name, ts in single_caps.items() if angle(ts, p)}
        coefficients[str(tuple(map(int, p)))] = {"fixed": fixed, "caps": contributions}
        # A single cell supplies at most one ordinary cap, so maximize its
        # contribution per cell, not independently per Boolean variable.
        cell_max = sum(max([v for k, v in contributions.items()
                            if k.rstrip("01234567") == cell] or [0])
                       for cell in ["D", "R", "Tc", "N"])
        assert fixed == 360 or fixed + cell_max < 360, p
        if fixed == 360: full_nonA.append(p)
        if p[0] % 2 != p[1] % 2:
            # Non-A side midpoints already accounted for by M are excluded
            # from b; the only exterior fixed smooth midpoint is (1,-2).
            if p == (1, -2):
                assert fixed == 180 and not contributions
            elif fixed != 360 and angle(H, p) != 180:
                assert fixed + cell_max < 180, p
            continue
        if p == (-1, 1):
            assert fixed == 135 and contributions == {"N5": 45}
        elif p == (1, 3):
            assert fixed == 90 and contributions == {"Tc5": 45, "N0": 45}
        elif p == (3, -1):
            assert fixed == 90 and contributions == {"D1": 45, "R4": 45}
        else:
            assert fixed > 180 or fixed + cell_max < 180, p
    assert set(full_nonA) == {(-1, 0), (1, 0), (2, 1)}
    assert angle(O3L70, (1, -2)) == 180
    # Under the inherited two-root identity n=J+1, J=3 forces n=4.
    # E4 and residual N7 occupy two ordinary slots: Tc + D + R = 2.
    # With old Tc5 already covered, remaining Tc empty implies D=R=1;
    # remaining Tc6 implies D+R=1. This is algebra, not cap enumeration.
    assert len(full_nonA) + 1 - 2 == 2
    # Both direct N7 terminal substitutions need d=1/7, where Eentry is
    # already a genuine corner, not a candidate for replay.
    singular = F(1, 7)
    assert 14 * singular == 2 and 4 - 14 * singular == 2
    assert (F(3), 7 * singular) == (3, 1)
    assert angle(O3L70, (3, 1)) == 225
    assert angle(single_caps["R3"], (3, 1)) == 45
    assert angle(single_caps["R4"], (3, 1)) == 0
    N7 = audit_N7(O3L70)
    rejected_mutations = 0
    for tile in z:
        try: witness(P, minimum, maximum | {tile})
        except AssertionError: rejected_mutations += 1
        else: raise AssertionError("lost mirror was not detected")
    for name in ["argument.txt", "check.py", "coverage.txt"]:
        p = BASE / "surplus-four-local/O3-L70-hand" / name
        sources[str(p.relative_to(BASE))] = hashlib.sha256(p.read_bytes()).hexdigest()
    payload = {"verdict": "ACCEPT_PARENT_AND_TIGHTEN_WHOLE_LOCAL_O3_L70_TO_NINE",
        "independent_six_path": result,
        "crossing_2_1": {"angle": 360, "incident_triangles_in_H": len(incident)},
        "Tc5_inherited_six_rechecked": prior_result,
        "symbolic_angle_coefficients": coefficients,
        "J": 3, "b_formula": "1 + N5 + Tc5*N0 + D1*R4",
        "N7_extension": N7,
        "remaining_scope": "No remaining local two-root O3/L70 cases under the inherited class. Six/nine/FOUR complement gives <=9, improving the parent <=11.",
        "mirror_mutations_rejected": rejected_mutations,
        "source_sha256": sources,
        "own_engine_sha256": hashlib.sha256(ENGINE.read_bytes()).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "limits": "Whole LOCAL two-root O3/L70 <=9 accepted; joining our prior independently reviewed O3-except-L70 <=6 gives local O3 <=9. Upstream local root classification inherited. No author execution, search, new room or workers."}
    (OUT / "check.json").write_text(json.dumps(payload, indent=2, default=str) + "\n")
    print("PASS: SIX15U5Z/NINE21U7Z/ELEVEN22U7Z/FOURsuffix9U3Z; frozen11 geometry; four firstT/reverse/sigma; full ordinaryR split => whole LOCAL O3/L70 <=9; original eleven revisitsS; 5 mutation rejections.")


if __name__ == "__main__": main()
