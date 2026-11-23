"""Does the corridor-limit lemma (Lemma H, and E which extends it) apply to the
22-wall dark pair? Vertices R22 from ../d38-review/check_named.py, S = (0, 0),
T = (2, 2). Cells are doubled so the points are lattice points of a gap-2 room,
the setting of newlemmas.H_configs. For each of the 8 frames and both orders,
reports the Lemma H hypotheses one by one."""
import sys
sys.path.insert(0, '../d57-witness-mining-r3/tools')
import newlemmas as nl
from newlemmas import Geo, SYMS

R22 = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1), (5, 1),
       (5, 0), (3, 0), (3, 1), (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2), (0, -2), (0, -1)]

def inside(px, py, poly):
    c = False
    for k in range(len(poly)):
        (x1, y1), (x2, y2) = poly[k], poly[(k + 1) % len(poly)]
        if (y1 > py) != (y2 > py) and px < x1 + (py - y1) * (x2 - x1) / (y2 - y1): c = not c
    return c

ox, oy = 1, 3
cells = set()
for x in range(-1, 5):
    for y in range(-3, 3):
        if inside(x + .5, y + .5, R22):
            for dx in (0, 1):
                for dy in (0, 1):
                    cells.add((2 * (x + ox) + dx, 2 * (y + oy) + dy))
g = Geo(cells, 12, 12)
S0, T0 = (2 * (0 + ox), 2 * (0 + oy)), (2 * (2 + ox), 2 * (2 + oy))
assert g.npt(*S0) == 4 and g.npt(*T0) == 4
print('cells', len(cells) // 4, 'S', S0, 'T', T0)
total = 0
for sym in SYMS:
    o = g.tr(sym)
    for nm, A, B in (('S viewer', S0, T0), ('T viewer', T0, S0)):
        a, b = g.tp(sym, A), g.tp(sym, B)
        if a[1] >= b[1]:
            print(sym, nm, 'fails: corridor point not above viewer'); continue
        p, q, dlow = nl.corridor_up(o, b)
        ca, cb, top = nl.channel_up(o, a)
        reflex = (o.npt(p, dlow) == 3, o.npt(q, dlow) == 3)
        cfgs = list(nl.H_configs(o, a, b))
        total += len(cfgs)
        why = []
        if not (ca <= p and cb >= q): why.append(f'channel [{ca},{cb}] does not contain door [{p},{q}]')
        if not (a[1] < dlow <= top): why.append(f'door line {dlow} not in (viewer {a[1]}, channel top {top}]')
        print(sym, nm, 'viewer', a, 'corr pt', b, f'corridor [{p},{q}] mouth {dlow} reflex ends {reflex}',
              f'channel [{ca},{cb}] up to {top}', 'configs', cfgs, '; '.join(why))
print('Lemma H configurations in all frames:', total)
