"""Static applicability of ten already retained implications, no discovery."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import runpy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sources = {
    "index": HERE / "inherited-two-unit-support.json",
    "B6": ROOT / "first-surplus-review/bottom-residual-check.json",
    "exchange": ROOT / "first-surplus-review/square-exchange-check.json",
    "zero": ROOT / "zero-surplus-L/cover-check.json",
    "five": ROOT / "second-surplus-review/five-path-check.json",
    "caps": ROOT / "zero-surplus-L/guard-incidence-check.json",
    "fixture": ROOT / "triangle-composition/check.json",
    "checker": ROOT / "lower-bound-proof-audit/full-replay/guard-checker.py",
}
data = {k: json.loads(p.read_text()) for k,p in sources.items() if k != "checker"}
checker = runpy.run_path(str(sources["checker"]))
decode = lambda raw: [tuple(F(*c) for c in p) for p in raw]
base_B6 = decode(data["B6"]["path"])
sigma_reverse = lambda P: [(2-y,2-x) for x,y in reversed(P)]
paths = {
    "B6": base_B6,
    "sigma_B6": sigma_reverse(base_B6),
    "L11": decode(data["exchange"]["paths"]["L_thirteen"]["path"]),
    "E11": decode(data["exchange"]["paths"]["E_thirteen"]["path"]),
    "sigma13": decode(data["zero"]["paths"]["thirteen_sigma"]["path"]),
    "five": decode(data["five"]["five_path"]),
}
tri = lambda raw: {tuple(sorted(map(tuple,t))) for t in raw}
fixture = data["fixture"]["controls"]["unresolved_Tcenter"]
room = tri(fixture["triangles"])
caps = {n: tuple(sorted(map(tuple,t))) for n,t in data["caps"]["cap_options"].items()}
H = set().union(*(checker["incident"](tuple(map(F,p))) for p in [(0,0),(2,0),(2,2)]))
D = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]


def fan(center, indices):
    x,y = center
    return {tuple(sorted((center,(x+D[i][0],y+D[i][1]),
                          (x+D[(i+1)%8][0],y+D[(i+1)%8][1])))) for i in indices}


root = fan((-2,0),[7,0,1,2])
leaf = fan((-2,2),[6])
roof = fan((2,4),[5,6])
present = H | root | leaf | roof | {caps['B+'],caps['E-']}
allowed = H | root | leaf | roof | set(caps.values())
forced_absent = {caps['B-'],caps['E+']}
assert present <= room and not forced_absent & room
assert room <= allowed
results = {}
for name,P in paths.items():
    assert P[0] == (0,0) and P[-1] == (2,2)
    U,Z = checker['path_requirements'](P)
    impossible_need = (U-allowed) | (U & forced_absent)
    fixed_mirror_removed = Z & present
    assert impossible_need or fixed_mirror_removed
    results[name] = dict(status='INAPPLICABLE_TO_EVERY_ROOM_IN_THIS_RESIDUAL_CLASS',
                        reflections=len(P)-2,
                        impossible_required=sorted(impossible_need),
                        forbidden_already_present=sorted(fixed_mirror_removed))
implications = {}
for name,row in data['index']['implications'].items():
    key = row['path']
    implications[name] = dict(path=key,status=results[key]['status'])
assert len(implications) == 10 and len(results) == 6
out = dict(status='PASS',scope='Ten retained implication names, six unique retained fixed paths. Static incompatibility proof, NOT darkness or failure of all paths. No source archive, room assignment or direction search.',
           paths=results,implications=implications,
           prefix_only_roof_return=dict(target_image=[6,6],parameter='6/7',
                                       first_floor_contact=['0','-1'],status='ACTUAL_CORNER'),
           inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in sources.values()})
(HERE/'centered-roof-check.json').write_text(json.dumps(out,indent=2)+'\n')
(HERE/'centered-roof-geometry.json').write_text(json.dumps(dict(
    source='triangle-composition/check.json:unresolved_Tcenter',
    vertices=fixture['vertices'],triangles=fixture['triangles'],ledger=fixture['ledger']),indent=2)+'\n')
print('PASS: all ten retained implications statically inapplicable (six unique paths); no darkness claim')
