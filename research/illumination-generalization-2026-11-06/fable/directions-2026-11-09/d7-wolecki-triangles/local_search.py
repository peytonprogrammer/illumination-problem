"""Randomized hill-climb that tries to beat the proved lower bounds (falsification test).

Start from a valid room with two interior A points. Moves: add the mirror tile across a
boundary edge, or remove a tile outside the two stars. A move is kept if the room stays a
strictly simple clean room with the same two interior A points and the wall count does not
grow by more than `slack` above the best seen. Reports the smallest wall count seen.
"""
import json
import random
import sys
from collections import defaultdict

from rooms import Geo, Invalid, analyze, any_overlap
from build import arc_family, two_star


def climb(g, start, steps, seed, slack=2):
    rng = random.Random(seed)
    rep = analyze(g, start)
    assert rep['clean'] and len(rep['interior_A']) >= 2
    stars = set(rep['interior_A'][:2])
    cur, curw = list(rep['tileset']), rep['walls']
    best, bestw = cur[:], curw
    tried = accepted = 0
    for _ in range(steps):
        tiles = set(cur)
        if rng.random() < 0.6:
            t = rng.choice(cur)
            u = g.reflect_tile(t, rng.randrange(3))
            if u in tiles or any_overlap(g, [u], cur):
                continue
            cand = cur + [u]
        else:
            movable = [t for t in cur if t[0] not in stars]
            if not movable:
                continue
            t = rng.choice(movable)
            cand = [x for x in cur if x != t]
        tried += 1
        try:
            r = analyze(g, cand)
        except Invalid:
            continue
        if not r['clean'] or not stars <= set(r['interior_A']):
            continue
        if r['walls'] <= bestw + slack:
            cur, curw = cand, r['walls']
            accepted += 1
            if curw < bestw:
                best, bestw = cand[:], curw
    return bestw, best, tried, accepted


if __name__ == '__main__':
    out = []
    for spec in sys.argv[1:]:
        n, b, steps, seeds = map(int, spec.split(','))
        g = Geo(n, b)
        starts = []
        fam = arc_family(g)
        if fam:
            starts.append(('arc', fam[0]['tileset']))
        try:
            r2 = analyze(g, two_star(g))
            if r2['clean'] and len(r2['interior_A']) >= 2:
                starts.append(('two_star', two_star(g)))
        except Invalid:
            pass
        for name, st in starts:
            w0 = analyze(g, st)['walls']
            res = [climb(g, st, steps, s) for s in range(seeds)]
            bw = min(r[0] for r in res)
            row = dict(n=n, b=b, c=g.c, start=name, start_walls=w0, steps=steps, seeds=seeds,
                       best_walls=bw, valid_moves_tried=sum(r[2] for r in res), accepted=sum(r[3] for r in res))
            print(json.dumps(row), flush=True)
            out.append(row)
        json.dump([r for r in out if (r['n'], r['b']) == (n, b)],
                  open('local-search-%d-%d.json' % (n, b), 'w'), indent=1)
