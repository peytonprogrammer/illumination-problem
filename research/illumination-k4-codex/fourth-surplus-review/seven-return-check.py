"""Review one supplied seven-reflection path and its static cap implication."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import runpy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
INPUT = ROOT / "triangle-composition/seven-path.json"
CAPS = ROOT / "zero-surplus-L/guard-incidence-check.json"
CHECKER = ROOT / "lower-bound-proof-audit/full-replay/guard-checker.py"
FANS = ROOT / "first-surplus-L/local-fans.json"
SHORT = ROOT / "zero-surplus-L/cover-check.json"
source = json.loads(INPUT.read_text())
path = [tuple(map(F, p)) for p in source["path"]]
assert path[0] == (0, 0) and path[-1] == (2, 2) and len(path) == 9
checker = runpy.run_path(str(CHECKER))
U, Z = checker["path_requirements"](path)
tri = lambda raw: {tuple(sorted(map(tuple, t))) for t in raw}
assert U == tri(source["required_triangles"])
assert Z == tri(source["forbidden_triangles"])
directions = [(1, 0), (1, 1), (0, 1), (-1, 1),
              (-1, 0), (-1, -1), (0, -1), (1, -1)]


def fan(center, sectors):
    x, y = center
    return {tuple(sorted((center, (x + directions[i][0], y + directions[i][1]),
                          (x + directions[(i + 1) % 8][0],
                           y + directions[(i + 1) % 8][1])))) for i in sectors}


H = set().union(*(fan(c, range(8)) for c in [(0, 0), (2, 0), (2, 2)]))
parent = fan((-2, 0), [7, 0, 1, 2])
leaf = fan((-2, 2), [6])
caps = {name: tuple(sorted(map(tuple, t)))
        for name, t in json.loads(CAPS.read_text())["cap_options"].items()}
forced = H | parent | leaf | {caps["B+"], caps["E-"], caps["T-"]}
assert U <= forced and not Z & forced
blocked = sorted(name for name, t in caps.items() if t in Z)
assert blocked == ["B-", "E+", "T+"]
assert Z - set(caps.values()) == {
    tuple(sorted(((-3, 1), (-2, 1), (-2, 2)))),
    tuple(sorted(((-2, 2), (-1, 1), (-1, 2)))),
    tuple(sorted(((0, -2), (1, -2), (1, -1)))),
}
# Two forbidden triangles are other remote sectors; the third is an outer
# B-fan triangle, impossible when that cell is an ordinary single cap.
assert not (Z - set(caps.values())) & (H | parent | leaf)

# Independently reconstruct the analytic contact formulas at prescribed d.
d = F(5, 6)
derived = [(F(0), F(0)), (2*d/(1+d), -2/(1+d)),
           (F(-2), 4*d-2), ((2-6*d)/(1+d), (6*d-2)/(1+d)),
           (F(-2), 6-4/d), (7*d-6, F(-1)),
           (F(3), 9/d-8), (12-11*d, F(3)), (12-12*d, F(2))]
assert derived == path and F(9, 11) < d < F(6, 7)
fan_threats = []
fan_safe = []
for item in json.loads(FANS.read_text())["potentially_dark_one_excess_fans"]:
    if item["A"] == [-2, 0]:
        continue  # The parent already occupies this cell; no separate fan here.
    overlap = tri(item["triangles"]) & Z
    record = {k: item[k] for k in ["A", "m", "start", "type"]}
    record["forbidden_overlap"] = sorted(overlap)
    (fan_threats if overlap else fan_safe).append(record)
assert len(fan_threats) == 7 and len(fan_safe) == 12
# At the centered-B threat, the only possible occupied triangles at this
# boundary B vertex are two core sectors, one root and one B-fan sector.
centered_B = fan((0, -2), [1, 2])
smooth_B = (-1, -1)
occupied_at_B = {t for t in H | parent | leaf | centered_B if smooth_B in t}
assert len(occupied_at_B) == 4
assert all(smooth_B not in t for t in caps.values() if t not in centered_B | parent)
short_rows = {}
for name in ["one", "one_sigma", "four"]:
    row = json.loads(SHORT.read_text())["paths"][name]
    short_path = [tuple(F(*c) for c in p) for p in row["path"]]
    short_U, short_Z = checker["path_requirements"](short_path)
    assert short_U == tri(row["required_tiles"])
    assert short_Z == tri(row["forbidden_tiles"])
    assert short_U <= H | {caps["B+"]}
    assert not short_Z & (H | parent | leaf)
    short_rows[name] = {"reflections": len(short_path)-2,
                        "forbidden": sorted(short_Z)}
result = {"status": "PASS", "reflections": 7,
          "scope": "One prescribed path; established exact guard implementation reused, independent hand itinerary/cap implication.",
          "ordinary_cap_blockers": blocked,
          "forced_caps": ["B+", "E-", "T-"],
          "parameter": "5/6", "sufficient_open_interval": ["9/11", "6/7"],
          "target_formula": "x=12-12d at y=2",
          "required_triangles": sorted(U), "forbidden_triangles": sorted(Z),
          "extra_unit_fan_threats": fan_threats,
          "extra_unit_fans_disjoint_from_forbidden": fan_safe,
          "centered_B_new_smooth_vertex": list(smooth_B),
          "centered_B_occupied_45degree_sectors": len(occupied_at_B),
          "retained_short_path_guards": short_rows,
          "inputs": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in [INPUT, CAPS, CHECKER, FANS, SHORT]}}
(HERE / "seven-return-check.json").write_text(json.dumps(result, indent=2) + "\n")
print("PASS: supplied seven-reflection path, exact guard agreement, arbitrary ordinary-cap implication")
