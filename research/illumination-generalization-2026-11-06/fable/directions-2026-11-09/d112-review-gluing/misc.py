"""D112 claims 4-5 side checks: reflex counts r = r_A + r_B + 4, and the DB55 truncation example."""
import sys
from fractions import Fraction as F
from pathlib import Path
from chamber import reflex_count
from glue import sealed
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'd110-review-length'))
from geom import room

for name in ('DBas', 'DB55', 'DBw2'):
    for L in (4, 21):
        R = room(name, L)
        A, _, B, _ = sealed(R)
        r, W = reflex_count(R['V']); rA, WA = reflex_count(A); rB, WB = reflex_count(B)
        print(f"{name} L={L}: room r={r} W={W}; sealed chambers r={rA},{rB} W={WA},{WB}; r = rA+rB+4: {r == rA + rB + 4}")

# DB55 left square, (1,1), slope 3/10 moving right and up; developed heights at vertical-wall visits
y0, s = F(1), F(3, 10)
visits = [(j, y0 + s * (4 + 5 * j)) for j in range(11)]
print("first x=5 hit height:", visits[0][1], "; corner among j=0..10:", any((Y / 5).denominator == 1 for _, Y in visits))
Y = visits[10][1]
r = Y % 10
print("developed height after 5 more x=5 visits:", Y, "-> folds to", r if r < 5 else 10 - r, "going", "up" if r < 5 else "down")
print("developed heights:", [str(Y) for _, Y in visits])
