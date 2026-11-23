"""Shooter sanity checks: no legal path joins interior A points in clean rooms; controls are lit.

For each room, candidate targets X are the A-class vertices of all images of the base tile
under at most DEPTH side reflections (no planarity filter), within RADIUS of the source.
Every legal path that crosses fewer than DEPTH - 2n tile edges ends on such an X.
"""
import json
import sys
from collections import Counter

from rooms import Geo, analyze, shoot, a_images
from build import two_star, arc_family


def run(name, g, tiles, depth, radius, expect_dark):
    rep = analyze(g, tiles)
    ints = rep['interior_A']
    res = Counter()
    first_block = Counter()
    shots = 0
    for S in ints:
        base_pts = a_images(g, depth, radius + abs(g.cx(S)))
        for X in base_pts:
            if X == S or abs(g.cx(X) - g.cx(S)) > radius:
                continue
            for T in ints:
                shots += 1
                out = shoot(g, rep, S, X, T)
                res[out[0]] += 1
                if out[0] == 'BLOCKED':
                    first_block[out[1]] += 1
    dark = res['LIT'] == 0
    row = dict(room=name, n=g.n, b=g.b, walls=rep['walls'], tiles=rep['tiles'], clean=rep['clean'],
               interior_A=len(ints), depth=depth, radius=radius, shots=shots, outcomes=dict(res),
               first_block_class=dict(first_block), dark_in_range=dark, expected_dark=expect_dark,
               PASS=(dark == expect_dark))
    print(json.dumps(row))
    return row


if __name__ == '__main__':
    out = []
    # positive controls (not clean): lit
    g = Geo(6, 2)
    out.append(run("control: 30-60-90 hexagon star (C flat), S to S", g, g.star(g.base), 40, 14.0, False))
    g = Geo(8, 3)
    out.append(run("control: 22.5-67.5-90 octagon star (C flat), S to S", g, g.star(g.base), 13, 12.0, False))
    g = Geo(8, 2)
    ts = two_star(g)
    t1 = g.reflect_tile(g.reflect_tile(g.base, 2), 0)       # pair on the other side of P
    extra = [t1, g.reflect_tile(t1, 2)]
    out.append(run("control: (1,2,5) two-star room with P made interior (8 tiles)", g, ts + extra, 13, 10.0, False))
    # clean rooms: dark
    out.append(run("(1,2,5) two-star room, 32 walls", g, ts, 14, 10.0, True))
    g = Geo(6, 2)
    out.append(run("30-60-90 arc-family room, 27 walls", g, arc_family(g)[0]['tileset'], 40, 16.0, True))
    g = Geo(10, 3)
    out.append(run("(1,3,6) arc room, 42 walls", g, arc_family(g)[0]['tileset'], 14, 10.0, True))
    json.dump(out, open('shoot-checks.json', 'w'), indent=1)
    print("ALL_PASS", all(r['PASS'] for r in out))
