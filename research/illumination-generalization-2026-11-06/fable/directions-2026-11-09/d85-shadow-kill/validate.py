"""Cross-check shadow.shoot against d8-perturbation-test/tracer.trace (Fractions)."""
import json, random, sys
from fractions import Fraction as Fr
import shadow
from tracer import trace

rooms = json.load(open('../d8-perturbation-test/rooms.json'))
byid = {r['id']: {tuple(c) for c in r['cells']} for r in rooms}
cases = [('R22', byid['R22-base'], (0, 0)), ('R22-L1-005', byid['R22-L1-005'], (0, 0)),
         ('cross7', shadow.cross(7), (0, 0)), ('cross7', shadow.cross(7), (6, 1)),
         ('U2k2', shadow.U2(2), (1, 1)), ('U2k2', shadow.U2(2), (14, 6))]
random.seed(85)
n = agree = 0
for name, C, S in cases:
    for _ in range(400):
        Dx, Dy = 2 * random.randint(-25, 25), 2 * random.randint(-25, 25)
        if (Dx, Dy) == (0, 0):
            continue
        mine = shadow.shoot(C, S, Dx, Dy)
        try:
            end, ok, _ = trace(C, S, (Dx, Dy))
            ref = (int(end[0]), int(end[1])) if ok else None
        except (RuntimeError, AssertionError):
            ref = None
        n += 1; agree += mine == ref; legal = globals().get("legal", 0) + (ref is not None); globals()["legal"] = legal
        if mine != ref:
            print('MISMATCH', name, S, (Dx, Dy), mine, ref)
print(f'{agree}/{n} agree, {legal} legal in the reference tracer')
