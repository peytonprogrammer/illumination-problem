"""Lemma H configurations of the 10 door pairs at r = 3 (metric-free part).

Rooms use gaps 2, so position types are lattice points (read-only import of
d57 tools). For each door pair, frame, and order, prints the Lemma H data
(a, b, p, q, d) in the canonical frame (corridor point T above, viewer S below),
the far end of T's corridor, and the side of S away from the door."""
import sys, json
sys.path.insert(0, '../d57-witness-mining-r3/tools')
from rooms import Room
import newlemmas as nl
from newlemmas import Geo, SYMS

DOOR = [(119, (1, 1), (3, 5)), (122, (1, 3), (3, 1)), (122, (1, 4), (3, 1)),
        (1238, (1, 5), (3, 1)), (1238, (1, 5), (4, 1)), (971, (1, 1), (3, 5)),
        (971, (1, 1), (4, 5)), (971, (1, 1), (5, 5)), (1275, (3, 7), (5, 3)),
        (719, (1, 1), (3, 5))]

def far_end(o, p, q, T):
    """Top of T's corridor: first row e >= t2 where run [p, q) stops. Returns (e, kind)."""
    c = o.cells
    e = T[1]
    while all((x, e) in c for x in range(p, q)) and (p - 1, e) not in c and (q, e) not in c: e += 1
    above = [(x, e) in c for x in range(p, q)]
    kind = 'dead-end' if not any(above) else ('open' if all(above) else 'partial')
    side = ((p - 1, e) in c, (q, e) in c)
    return e, kind, side

def behind(o, a, b, S):
    """Rows below S: is the line y = s2 - ... a full wall across [a, b)? Walk down
    from S while the row run equals [a, b)."""
    c = o.cells
    y = S[1] - 1
    while y >= 0 and all((x, y) in c for x in range(a, b)) and (a - 1, y) not in c and (b, y) not in c: y -= 1
    below = [(x, y) in c for x in range(a, b)] if y >= 0 else [False] * (b - a)
    kind = 'wall' if not any(below) else ('open' if all(below) else 'partial')
    return y + 1, kind

if __name__ == '__main__':
    rows = {r['mask']: r for r in json.load(open('../d57-witness-mining-r3/tools/cert_r3.json'))}
    for mask, S, T in DOOR:
        r = rows[mask]
        R = Room(r['nx'], r['ny'], mask, [2] * r['nx'], [2] * r['ny'])
        g = Geo(R.cells, R.W, R.H)
        print(f"== {mask} {r['shape']} S={S} T={T}")
        for sym in SYMS:
            o = g.tr(sym)
            for nm, A, B in (('ST', S, T), ('TS', T, S)):
                a, b = g.tp(sym, A), g.tp(sym, B)
                for cfg in nl.H_configs(o, a, b):
                    ca, cb, p, q, d = cfg
                    e, kind, side = far_end(o, p, q, b)
                    c0, bk = behind(o, ca, cb, a)
                    print(f"  sym={sym} order={nm} viewer={a} corr={b} chan=[{ca},{cb}] door=[{p},{q}]@{d} "
                          f"corr_top={e} {kind} {side} chan_back={c0} {bk}")
