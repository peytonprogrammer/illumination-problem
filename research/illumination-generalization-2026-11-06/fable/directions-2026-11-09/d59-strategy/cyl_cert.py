"""d59 third test: are the lighting paths of named lit pairs cylinder certificates?

For each lighting direction found by lattice_trace (|p|, |q| <= H), follow the leaf through
S in both senses until it returns to S's state (closed regular leaf -> S lies in an open
cylinder of that direction, so S and T share a cylinder) or dies at a corner (S lies on a
saddle connection).  Named rooms only.  Run: python3 -B cyl_cert.py
"""
import json
from pathlib import Path
from lattice_trace import trace, lighting, load, cells_from_vertices, D, status

HERE = Path(__file__).resolve().parent


def leaf_closed(cells, S, p, q, maxsteps=100000):
    """True if the leaf from S in direction (p, q) returns to S without meeting a corner."""
    # target that is never reached: 0 => periodic with no corner (closed regular leaf),
    # negative => the leaf meets a corner (S lies on a saddle connection).
    r = trace(cells, S, (10 ** 9, 10 ** 9), p, q, maxsteps)
    return r == 0


rooms = D / 'd41-two-param-cover' / 'rooms'
cases = [('r20a W=20', load(rooms / 'r20a.txt'), (1, 3), (3, 5)),
         ('dumb12', load(rooms / 'dumb12.txt'), (2, 2), (6, 2)),
         ('dumb12', load(rooms / 'dumb12.txt'), (1, 2), (7, 2))]
out = []
for name, cells, S, T in cases:
    L = lighting(cells, S, T, 15)
    rows = []
    for h, p, q, steps in L:
        fwd = leaf_closed(cells, S, p, q)
        bwd = leaf_closed(cells, S, -p, -q)
        rows.append((h, p, q, steps, fwd and bwd))
    ncyl = sum(1 for r in rows if r[4])
    rec = dict(room=name, S=S, T=T, lighting=len(rows), on_closed_leaf=ncyl,
               first=[r for r in rows][:10], first_closed=[r for r in rows if r[4]][:5])
    print(json.dumps(rec))
    out.append(rec)
json.dump(out, open(HERE / 'cyl_cert.json', 'w'), indent=1)
