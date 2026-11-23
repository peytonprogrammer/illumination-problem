"""Shared helpers for d11 Python scripts: tile conversion, record rooms, d6 decider.

Tile (i, j, h): square [i,i+1]x[j,j+1], "/" diagonal if i+j even, "\\" if odd;
h = 0 lower tile, h = 1 upper tile (see enum45.c).
"""
import ast
import json
import subprocess
import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
DIRS = HERE.parent.parent   # d55 copy: lib/ is one level deeper
CTX = HERE.parents[4]
assert CTX.name == '.context', CTX
D4 = DIRS / 'd4-monodromy-blocks'
D6 = DIRS / 'd6-hurwitz-census'


def tile_verts(i, j, h):
    if (i + j) % 2 == 0:
        return [(i, j), (i + 1, j), (i + 1, j + 1)] if h == 0 else [(i, j), (i, j + 1), (i + 1, j + 1)]
    return [(i, j), (i + 1, j), (i, j + 1)] if h == 0 else [(i + 1, j), (i + 1, j + 1), (i, j + 1)]


def tri_to_ijh(tri):
    tri = [tuple(p) for p in tri]
    i = min(p[0] for p in tri)
    j = min(p[1] for p in tri)
    for h in (0, 1):
        if sorted(tile_verts(i, j, h)) == sorted(tri):
            return (i, j, h)
    raise ValueError('not a canonical45 tile: %r' % (tri,))


def point_in_polygon(pt, poly):
    x, y = pt
    inside = False
    m = len(poly)
    for k in range(m):
        (x1, y1), (x2, y2) = poly[k], poly[(k + 1) % m]
        if (y1 > y) != (y2 > y):
            xc = Fr(x1) + (y - y1) * Fr(x2 - x1, y2 - y1)
            if xc > x:
                inside = not inside
    return inside


def tiles_from_polygon(poly):
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    out = []
    for i in range(min(xs), max(xs)):
        for j in range(min(ys), max(ys)):
            for h in (0, 1):
                v = tile_verts(i, j, h)
                c = (Fr(sum(p[0] for p in v), 3), Fr(sum(p[1] for p in v), 3))
                if point_in_polygon(c, poly):
                    out.append((i, j, h))
    return out


def tiles_from_squares(squares):
    return [(i, j, h) for (i, j) in squares for h in (0, 1)]


def boundary(tiles):
    """Boundary walk.  Returns dict(simple, W_cycle, corners, interior points, cycle).

    W_cycle counts turning vertices along every boundary cycle with multiplicity
    (a pinch point visited twice counts twice)."""
    from collections import Counter
    ec = Counter()
    for t in tiles:
        v = tile_verts(*t)
        for k in range(3):
            ec[frozenset((v[k], v[(k + 1) % 3]))] += 1
    bnd = [tuple(sorted(e)) for e, c in ec.items() if c == 1]
    inc = {}
    for e in bnd:
        for p in e:
            inc.setdefault(p, []).append(e)
    verts = {p for t in tiles for p in tile_verts(*t)}
    interior = sorted(p for p in verts if p not in inc)
    simple = all(len(es) == 2 for es in inc.values())
    # walk cycles: at a vertex with 4 edges, continue along the edge that keeps the room on the left
    # (only needed for the pinched validation room); count turns with multiplicity
    used = set()
    cycles = []
    W = 0
    for e0 in bnd:
        if e0 in used:
            continue
        # orient e0 with the room on its left
        a, b = e0
        if not _room_left(tiles, a, b):
            a, b = b, a
        cyc = [a]
        cur, nxt = a, b
        used.add(e0)
        while True:
            cyc.append(nxt)
            cands = [e for e in inc[nxt] if e not in used]
            outs = [(e[0] if e[1] == nxt else e[1]) for e in cands]
            outs = [q for q in outs if _room_left(tiles, nxt, q)]
            if not outs:
                break
            # choose the sharpest left turn consistent with the room on the left: smallest ccw angle from reverse
            q = min(outs, key=lambda q: _ccw_angle_key(cur, nxt, q))
            used.add(tuple(sorted((nxt, q))))
            cur, nxt = nxt, q
        cycles.append(cyc)
    for cyc in cycles:
        pts = cyc[:-1]
        m = len(pts)
        for k in range(m):
            p0, p1, p2 = pts[k - 1], pts[k], pts[(k + 1) % m]
            if (p1[0] - p0[0]) * (p2[1] - p1[1]) - (p1[1] - p0[1]) * (p2[0] - p1[0]) != 0:
                W += 1
    corners = sorted({p for p, es in inc.items() if len(es) != 2 or _turn(es, p)})
    return dict(simple=simple and len(cycles) == 1, W_cycle=W, n_cycles=len(cycles), corners=corners,
                interior=interior, cycle=cycles[0] if cycles else [])


def _turn(es, p):
    q1 = es[0][0] if es[0][1] == p else es[0][1]
    q2 = es[1][0] if es[1][1] == p else es[1][1]
    return (q1[0] - p[0]) * (q2[1] - p[1]) - (q1[1] - p[1]) * (q2[0] - p[0]) != 0


def _room_left(tiles, a, b):
    """True if the tile on the left of the directed edge a->b is in the room."""
    mx = Fr(a[0] + b[0], 2)
    my = Fr(a[1] + b[1], 2)
    dx, dy = b[0] - a[0], b[1] - a[1]
    pt = (mx - Fr(dy, 10), my + Fr(dx, 10))
    ts = set(map(tuple, tiles))
    i, j = int(pt[0] // 1), int(pt[1] // 1)
    for h in (0, 1):
        if (i, j, h) in ts:
            v = tile_verts(i, j, h)
            if _in_tri(pt, v):
                return True
    return False


def _in_tri(pt, v):
    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    d = [cr(v[k], v[(k + 1) % 3], pt) for k in range(3)]
    return all(x > 0 for x in d) or all(x < 0 for x in d)


def _ccw_angle_key(prev, cur, q):
    import math
    a1 = math.atan2(prev[1] - cur[1], prev[0] - cur[0])
    a2 = math.atan2(q[1] - cur[1], q[0] - cur[0])
    return (a2 - a1) % (2 * math.pi)


def room_line(tiles, W):
    return '%d %d %s' % (len(tiles), W, ' '.join('%d %d %d' % t for t in tiles))


def worksheet_constants():
    tree = ast.parse((D4 / 'inputs' / 'peyton-worksheet-build.py.txt').read_text())
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in ('TOKARSKY26', 'CASTRO24', 'PUBLISHED_ST', 'ROOM22'):
                out[node.targets[0].id] = ast.literal_eval(node.value)
    return out


WOLECKI22 = [(-2, 0), (-1, 0), (-1, -1), (0, -2), (0, -1), (1, -1), (1, 0), (2, 0), (1, 1), (2, 1), (2, 0), (3, 1),
             (3, 2), (4, 2), (3, 3), (2, 3), (2, 4), (1, 3), (1, 2), (0, 2), (0, 1), (-1, 1)]


def d6_decide(tiles, marks, max_states=200000):
    """d6's pure-braid Hurwitz decider on the triangle pull-back (independent code, read in place)."""
    sys.path.insert(0, str(D6))
    import d4_monodromy as d4
    import validate_rooms as vr
    tris = [tuple(map(tuple, tile_verts(*t))) for t in tiles]
    room = d4.Room('r', 'tri', tris, [tuple(m) for m in marks])
    r = vr.decide_room(room, vr.tri_tuple(room), max_states=max_states)
    return dict(verdict=r['verdict'], basis=r['verdict_basis'],
                states=[c['orbit_states'] for c in r['components']],
                complete=[c['complete'] for c in r['components']],
                k=[c['k_transparent'] for c in r['components']])


def d4_blocks(tiles, marks):
    """d4's block-system analysis in the triangle framework (read in place)."""
    sys.path.insert(0, str(D4))
    import monodromy as m4
    tris = [tuple(map(tuple, tile_verts(*t))) for t in tiles]
    room = m4.Room('r', 'tri', tris, [tuple(m) for m in marks])
    out = m4.analyse_room(room, full_group=True)
    return dict(order=out.get('order'), primitive=out['primitive'], degree=out['degree'],
                ledger=out['ledger'],
                block_systems=[dict(size=b['block_size'], parity=b['parity_property'], sep=b['phiS_disjoint_phiT'])
                               for b in out['block_systems']])
