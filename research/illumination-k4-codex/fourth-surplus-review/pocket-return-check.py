"""Independent exact replay of five prescribed triangle-return controls.

No peer code imports, direction scans, or room generation. General validity
comes from the accompanying hand proof, not from these five evaluations.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "remote22-proof-review/pocket-return.txt"
CONTROLS = [
    (F(1, 3), F(2), F(1)),
    (F(4, 5), F(-3, 5), F(1)),
    (F(1, 4), F(-2), F(1)),
    (F(1, 3), F(1, 10), F(1)),
    (F(1, 3), F(0), F(1)),
]


def physical_return(x, a, b):
    point = (x, F(0))
    velocity = (a, b)
    time = F(0)
    contacts = []
    for _ in range(6):
        px, py = point
        vx, vy = velocity
        candidates = []
        if vx < 0:
            candidates.append((-px / vx, "left"))
        if vy < 0:
            candidates.append((-py / vy, "portal"))
        if vx + vy > 0:
            candidates.append(((1 - px - py) / (vx + vy), "diagonal"))
        candidates = [(t, wall) for t, wall in candidates if t > 0]
        assert candidates
        t = min(t for t, _ in candidates)
        walls = [wall for u, wall in candidates if u == t]
        point = (px + t * vx, py + t * vy)
        time += t
        assert len(walls) == 1, ("vertex", point)
        assert point not in ((0, 0), (1, 0), (0, 1))
        wall = walls[0]
        if wall == "portal":
            return point, velocity, time, contacts
        contacts.append((wall, point))
        velocity = (-vx, vy) if wall == "left" else (-vy, -vx)
    raise AssertionError("Five-reflection local bound exceeded")


def formula(x, a, b):
    ty = 2 / b
    tx = (1 - x) / a if a > 0 else (1 + x) / (-a) if a < 0 else None
    assert tx != ty
    if tx is None or ty < tx:
        z = x + a * ty
        assert z != 0 and abs(z) < 1
        return (abs(z), F(0)), ((1 if z > 0 else -1) * a, -b), ty
    z = 1 - b * tx
    assert z != 0 and abs(z) < 1
    return (abs(z), F(0)), (-(1 if z > 0 else -1) * b, -abs(a)), tx


rows = []
for x, a, b in CONTROLS:
    point, velocity, time, contacts = physical_return(x, a, b)
    assert (point, velocity, time) == formula(x, a, b)
    assert len(contacts) <= 5
    rows.append({"entry": str(x), "velocity": list(map(str, (a, b))),
                 "exit": list(map(str, point)),
                 "exit_velocity": list(map(str, velocity)), "time": str(time),
                 "contacts": [[wall, list(map(str, p))] for wall, p in contacts]})

result = {"status": "PASS", "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
          "scope": "Five supplied controls, independent physical triangle reflection code; no discovery.",
          "controls": rows}
(HERE / "pocket-return-check.json").write_text(json.dumps(result, indent=2) + "\n")
print("PASS: five prescribed controls; exact exit position, velocity, flight time and <=5 reflections")
