"""Orthogonal lattice rooms as sets of unit cells (named by lower-left corner).

Geometry only: point status, strict simplicity, walls, parity classes, and the
single local modifications used by the perturbation test. Integer arithmetic.
"""
from collections import deque


def around(cells, p):
    """Cells around lattice point p, in the order ll, lr, ul, ur."""
    x, y = p
    return [c for c in ((x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)) if c in cells]


def status(cells, p):
    x, y = p
    ll, lr = (x - 1, y - 1) in cells, (x, y - 1) in cells
    ul, ur = (x - 1, y) in cells, (x, y) in cells
    n = ll + lr + ul + ur
    if n == 0:
        return "outside"
    if n == 1:
        return "convex"
    if n == 3:
        return "reflex"
    if n == 4:
        return "interior"
    if (ll and ur) or (lr and ul):
        return "pinch"
    return "smooth"


def lattice_points(cells):
    return {(i + a, j + b) for (i, j) in cells for a in (0, 1) for b in (0, 1)}


def cls(p, origin=(0, 0)):
    """Parity class relative to origin: 'A', 'C1' (odd, even), 'B', 'C2' (even, odd)."""
    a, b = (p[0] - origin[0]) % 2, (p[1] - origin[1]) % 2
    return {(0, 0): "A", (1, 0): "C1", (1, 1): "B", (0, 1): "C2"}[(a, b)]


def boundary_edges(cells):
    """Unit boundary edges as ((x0,y0),(x1,y1)) with the room on the left."""
    out = []
    for (i, j) in cells:
        if (i, j - 1) not in cells:
            out.append(((i, j), (i + 1, j)))
        if (i + 1, j) not in cells:
            out.append(((i + 1, j), (i + 1, j + 1)))
        if (i, j + 1) not in cells:
            out.append(((i + 1, j + 1), (i, j + 1)))
        if (i - 1, j) not in cells:
            out.append(((i, j + 1), (i, j)))
    return out


def is_strictly_simple(cells):
    """Edge-connected, no pinch point, boundary one simple closed curve."""
    if not cells:
        return False
    cells = set(cells)
    start = next(iter(cells))
    seen = {start}
    dq = deque([start])
    while dq:
        i, j = dq.popleft()
        for nb in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if nb in cells and nb not in seen:
                seen.add(nb)
                dq.append(nb)
    if len(seen) != len(cells):
        return False
    for p in lattice_points(cells):
        if status(cells, p) == "pinch":
            return False
    edges = boundary_edges(cells)
    nxt = {}
    for a, b in edges:
        if a in nxt:
            return False
        nxt[a] = b
    a0 = edges[0][0]
    a, steps = a0, 0
    while True:
        a = nxt[a]
        steps += 1
        if a == a0:
            break
    return steps == len(edges)


def vertex_cycle(cells):
    """Polygon vertices (convex and reflex corners) in counter-clockwise order."""
    edges = boundary_edges(cells)
    nxt = {a: b for a, b in edges}
    pts = [p for p in nxt if status(cells, p) in ("convex", "reflex")]
    start = min(pts)
    out, a = [], start
    while True:
        if status(cells, a) in ("convex", "reflex"):
            out.append(a)
        a = nxt[a]
        if a == start:
            break
    return out


def walls(cells):
    """Maximal wall segments (v_k, v_{k+1}) of the boundary, counter-clockwise."""
    vs = vertex_cycle(cells)
    return [(vs[k], vs[(k + 1) % len(vs)]) for k in range(len(vs))]


def summary(cells, origin=(0, 0)):
    pts = sorted(lattice_points(cells))
    st = {p: status(cells, p) for p in pts}
    conv = sum(1 for p in pts if st[p] == "convex")
    refl = sum(1 for p in pts if st[p] == "reflex")
    assert conv - refl == 4, (conv, refl)
    interior = [p for p in pts if st[p] == "interior"]
    transparent = [p for p in pts if cls(p, origin) != "A" and st[p] in ("interior", "smooth")]
    return {
        "W": conv + refl, "r": refl, "area": len(cells),
        "interior": interior,
        "transparent": transparent, "k": len(transparent),
    }


def cells_from_vertices(verts):
    """Unit cells inside a simple orthogonal polygon given by its vertex cycle."""
    xs = [x for x, _ in verts]
    ys = [y for _, y in verts]
    out = set()
    m = len(verts)
    for i in range(min(xs), max(xs)):
        for j in range(min(ys), max(ys)):
            # ray to +x from cell centre (i+1/2, j+1/2), doubled to stay integral
            cx, cy = 2 * i + 1, 2 * j + 1
            inside = False
            for k in range(m):
                (x1, y1), (x2, y2) = verts[k], verts[(k + 1) % m]
                if x1 == x2 and (2 * y1 > cy) != (2 * y2 > cy) and 2 * x1 > cx:
                    inside = not inside
            if inside:
                out.add((i, j))
    return frozenset(out)


def cells_from_triangles(tris):
    """Orthogonal room given as half-square triangles: pair them into unit cells."""
    cnt = {}
    for t in tris:
        xs = [p[0] for p in t]
        ys = [p[1] for p in t]
        c = (min(xs), min(ys))
        assert max(xs) - c[0] == 1 and max(ys) - c[1] == 1
        cnt[c] = cnt.get(c, 0) + 1
    assert all(v == 2 for v in cnt.values()), "not an orthogonal room"
    return frozenset(cnt)


# ------------------------------------------------------------------ moves

def neighbours4(c):
    i, j = c
    return ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1))


def single_moves(cells):
    """Yield (description, new cells) for every single local modification.

    add:    one cell outside the room sharing an edge with the room
    remove: one cell of the room
    push:   move one wall (maximal segment) outward or inward by one unit
    Validity (strict simplicity, marks interior) is checked by the caller.
    """
    cells = frozenset(cells)
    outside = {nb for c in cells for nb in neighbours4(c) if nb not in cells}
    for c in sorted(outside):
        yield f"add{c}", cells | {c}
    for c in sorted(cells):
        yield f"remove{c}", cells - {c}
    for (a, b) in walls(cells):
        # room on the left of a->b; inside strip and outside strip of unit cells
        (x0, y0), (x1, y1) = a, b
        ins, outs = [], []
        if y0 == y1:                      # horizontal wall
            lo, hi = min(x0, x1), max(x0, x1)
            if x1 > x0:                   # moving +x: room above
                ins = [(i, y0) for i in range(lo, hi)]
                outs = [(i, y0 - 1) for i in range(lo, hi)]
            else:                         # moving -x: room below
                ins = [(i, y0 - 1) for i in range(lo, hi)]
                outs = [(i, y0) for i in range(lo, hi)]
        else:                             # vertical wall
            lo, hi = min(y0, y1), max(y0, y1)
            if y1 > y0:                   # moving +y: room on the left (x < x0)
                ins = [(x0 - 1, j) for j in range(lo, hi)]
                outs = [(x0, j) for j in range(lo, hi)]
            else:                         # moving -y: room on the right
                ins = [(x0, j) for j in range(lo, hi)]
                outs = [(x0 - 1, j) for j in range(lo, hi)]
        assert all(c in cells for c in ins) and not any(c in cells for c in outs), (a, b)
        yield f"push-out{a}{b}", cells | set(outs)
        yield f"push-in{a}{b}", cells - set(ins)


def valid_room(cells, marks):
    return is_strictly_simple(cells) and all(status(cells, m) == "interior" for m in marks)


def perturbations(cells, marks):
    """Distinct valid single modifications: dict cells -> list of descriptions."""
    out = {}
    for desc, new in single_moves(cells):
        new = frozenset(new)
        if new == cells or not valid_room(new, marks):
            continue
        out.setdefault(new, []).append(desc)
    return out
