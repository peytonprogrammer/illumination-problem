"""Learn a lighting certificate (U, Z) from one room, for the enumerator's pruning.

The exact decider (exact-dark/claude_origami_dark.py) returns a shear word, which gives a
direction. The direction is folded into an exact billiard path, and Claude's checker
accepts the path in this room. The certificate then records what the path needs:
- U: every tile meeting an open segment of the path (tile interior, both tiles of an
  edge, or every tile around a vertex it passes through);
- at a reflection inside an edge: the incoming tile in U, the tile across in Z;
- at a reflection at a vertex (a smooth boundary point): ring tiles on the incoming side of
  the mirror line in U, the rest in Z.
Any room containing U and avoiding Z contains the same valid path, so it's lit.
"""
import math
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent), str(HERE.parent/'exact-dark'), str(HERE.parent/'refolding')]
from claude_lit_certs import around, segment_tiles
from claude_origami_dark import decide
from claude_verify_lit import direction, fold
from claude_unfold import G, app
from claude_ray_guard_check import check_path


def centroid(t):
    return (F(sum(v[0] for v in t), 3), F(sum(v[1] for v in t), 3))


def certificate(path):
    U, Z = set(), set()
    for a, b in zip(path, path[1:]):
        U |= segment_tiles(a, b)
    for prev, p, nxt in zip(path, path[1:], path[2:]):
        din = (p[0]-prev[0], p[1]-prev[1]); dout = (nxt[0]-p[0], nxt[1]-p[1])
        # mirror normal n is parallel to dout/|dout| - din/|din|; only the sign of (c - p)·n is used
        ni = din[0]**2+din[1]**2; no = dout[0]**2+dout[1]**2
        n = (dout[0]/math.sqrt(no) - din[0]/math.sqrt(ni), dout[1]/math.sqrt(no) - din[1]/math.sqrt(ni))
        ring = around(*p)
        for t in ring:
            c = centroid(t)
            side = (float(c[0]-p[0])*n[0] + float(c[1]-p[1])*n[1])
            # dout - din = -2 (din·m) m, so n points into the room (the incoming side)
            (U if side > 0 else Z).add(t)
    return U, Z


def light(room_tiles, q, cap=200000):
    """Return (U, Z, path) for marks (0,0), q, or (None, status) if no lit direction is found."""
    tri = [[list(v) for v in t] for t in room_tiles]
    res = decide(dict(triangles=tri, marked=[[0, 0], list(q)]), cap=cap)
    if res['status'] != 'lit':
        return None, res
    v = direction(res['word'])
    room = frozenset(tuple(sorted(map(tuple, t))) for t in room_tiles)
    for g in G:
        pts = fold(sorted(room), set(), (0, 0), tuple(q), app(g, v))
        if not pts:
            continue
        path = [[[c.numerator, c.denominator] for c in p] for p in pts]
        ok, why, _ = check_path(room, path, [(0, 0), tuple(q)])
        if ok:
            U, Z = certificate(pts)
            assert U <= room and not (Z & room), 'certificate disagrees with the room'
            return (U, Z, pts), res
    return None, dict(status='fold_failed', word=res['word'])
