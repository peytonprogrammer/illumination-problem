"""Build the dark-rooms worksheet for Peyton: worksheet.tex with exact TikZ figures, set by LuaLaTeX with a
florilegium margin (theme florilegium-theme-rooms.lua) in the florilegium-tex Docker image.

Every numeric answer in the answer key is asserted from the room data before the PDF is built.
vendor/florilegium is github.com/kevinraymond/florilegium at commit 231f5eb (v1.3), unmodified.
Build the image once: docker build -t florilegium-tex vendor/florilegium/tools
"""
import math
import os
import re
import shutil
import subprocess
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
PX = 0.75                                     # bp per unit of the figure sizes below (CSS px)

INK, GRID, FAINT = "#1f2937", "#d6dae1", "#eef0f3"
WALL, RAY, GHOST = "#1e3a8a", "#dc2626", "#9ca3af"
ROOM, STAR = "#eef2ff", "#fde68a"
P0C, P1C, P2C = "#dbeafe", "#dcfce7", "#fef3c7"

# ---------------------------------------------------------------- geometry data

ROOM22 = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1), (5, 1), (5, 0),
          (3, 0), (3, 1), (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2), (0, -2), (0, -1)]
STAIR = [(-1, 0), (1, 0), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2), (0, -2), (0, -1), (-1, -1)]
P_SQUARES = [(-1, -1), (0, -1), (0, -2), (1, -2), (1, -3)]          # lower-left corners of P's squares
P1_SQUARES = [(x, -y - 1) for x, y in P_SQUARES]                      # (x, y) -> (x, -y)
P2_SQUARES = [(4 - x - 1, -y - 1) for x, y in P_SQUARES]              # (x, y) -> (4 - x, -y)

# The published rooms, from the coordinates in Wikimedia Commons file Tokarsky_Castro_illumination_problem.svg
# (Cmglee, 2012), divided by 10 with y flipped. S = (2, -2) and T = (6, -2) in both.
TOKARSKY26 = [(0, -2), (1, -2), (1, -3), (2, -3), (2, -4), (3, -3), (4, -3), (4, -4), (5, -3), (6, -3), (6, -4),
              (7, -3), (7, -2), (8, -2), (8, -1), (7, -1), (6, 0), (6, -1), (5, -1), (5, -2), (3, -2), (3, -1),
              (2, -1), (2, 0), (1, 0), (1, -1)]
CASTRO24 = [(0, -2), (1, -3), (2, -3), (2, -4), (3, -3), (4, -4), (4, -3), (5, -3), (6, -4), (6, -3), (7, -3),
            (8, -2), (7, -2), (7, -1), (6, 0), (6, -1), (5, -1), (5, -2), (3, -2), (3, -1), (2, -1), (2, 0),
            (1, -1), (1, -2)]
PUBLISHED_ST = ((2, -2), (6, -2))


def kind(p):
    x, y = p
    if x % 2 == 0 and y % 2 == 0:
        return "A"
    if x % 2 and y % 2:
        return "B"
    return "C"


def tiles_of_squares(squares):
    """Each unit square splits into two tiles along its A-B diagonal; return tiles as vertex triples."""
    out = []
    for x, y in squares:
        c = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
        a = next(p for p in c if kind(p) == "A")
        b = next(p for p in c if kind(p) == "B")
        others = [p for p in c if p not in (a, b)]
        out += [(a, b, others[0]), (a, b, others[1])]
    return out


def ledger(squares, corners):
    """N, W, I, J, s_A, s_N, Q for a room given by unit squares and its corner list."""
    tiles = tiles_of_squares(squares)
    count = {}
    for t in tiles:
        for p in t:
            count.setdefault(p, {"A": 0, "B": 0, "C": 0})
            count[p][kind(p)] += 1
    full = {"A": 8, "B": 8, "C": 4}
    led = dict(N=len(tiles), W=len(corners), I=0, J=0, sA=0, sN=0, Q=0)
    for p, c in count.items():
        n = c[kind(p)]
        if n == full[kind(p)]:
            led["I" if kind(p) == "A" else "J"] += 1
        elif p in corners:
            led["Q"] += n if kind(p) == "A" else 0
        elif kind(p) == "A":
            led["sA"] += 1
            led["Q"] += 3
        else:
            led["sN"] += 1
    return led


def outside_neighbors(cells):
    cells = set(cells)
    nb = {(x + dx, y + dy) for x, y in cells for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))}
    return nb - cells


def trace(poly, start, d, limit=30):
    """Follow light in an axis-parallel room until it hits a corner.

    Returns the path points and, for each piece of the path, the map (sx, tx, sy, ty) that unfolds it:
    x -> sx * x + tx, y -> sy * y + ty.
    """
    edges = list(zip(poly, poly[1:] + poly[:1]))
    corners = {(Fr(x), Fr(y)) for x, y in poly}
    p, d = (Fr(start[0]), Fr(start[1])), (Fr(d[0]), Fr(d[1]))
    pts, maps = [p], [(1, 0, 1, 0)]
    for _ in range(limit):
        hits = []
        for u, v in edges:
            ax = 0 if u[0] == v[0] else 1                   # 0: vertical wall x = c, 1: horizontal wall y = c
            if d[ax] == 0:
                continue
            t = (u[ax] - p[ax]) / d[ax]
            q = [p[0] + t * d[0], p[1] + t * d[1]]
            q[ax] = Fr(u[ax])
            if t > 0 and min(u[1 - ax], v[1 - ax]) <= q[1 - ax] <= max(u[1 - ax], v[1 - ax]):
                hits.append((t, tuple(q), ax))
        t, q, ax = min(hits)
        pts.append(q)
        if q in corners:
            return pts, maps
        sx, tx, sy, ty = maps[-1]
        maps.append((-sx, 2 * q[0] * sx + tx, sy, ty) if ax == 0 else (sx, tx, -sy, 2 * q[1] * sy + ty))
        d = (-d[0], d[1]) if ax == 0 else (d[0], -d[1])
        p = q
    raise ValueError("no corner reached")


def apply(m, p):
    sx, tx, sy, ty = m
    return (sx * p[0] + tx, sy * p[1] + ty)


def star_cells(squares):
    """Group unit squares by the A star that holds them. Star (2X, 2Y) becomes cell (X, Y)."""
    cells = {}
    for x, y in squares:
        cells.setdefault(((x + 1) // 2, (y + 1) // 2), []).append((x, y))
    full = {c for c, sq in cells.items() if len(sq) == 4}
    return full, set(cells) - full


SHAPES = {
    "one cell": [(0, 0)], "domino": [(0, 0), (1, 0)], "diagonal pair": [(0, 0), (1, 1)],
    "line of 3": [(0, 0), (1, 0), (2, 0)], "L of 3": [(0, 0), (1, 0), (0, 1)],
    "I": [(0, 0), (1, 0), (2, 0), (3, 0)], "O": [(0, 0), (1, 0), (0, 1), (1, 1)],
    "T": [(0, 0), (1, 0), (2, 0), (1, 1)], "S": [(0, 0), (1, 0), (1, 1), (2, 1)],
    "L": [(0, 0), (0, 1), (0, 2), (1, 0)],
}


def check_tokarsky(room, walls, marks):
    """Tokarsky's lemma for the 45-degree tiling: if a simple room is a union of tiles and every B or C point in it
    (inside or on the boundary) is a corner, then no light path joins two inside A points. Checks those conditions."""
    n = len(room)
    assert n == walls and len(set(room)) == n
    for i in range(n):
        (ax, ay), (bx, by), (cx, cy) = room[i - 1], room[i], room[(i + 1) % n]
        assert (bx - ax) * (cy - by) != (by - ay) * (cx - bx), "three corners in a line"
        dx, dy = cx - bx, cy - by
        k = max(abs(dx), abs(dy))
        assert dx in (0, k, -k) and dy in (0, k, -k)
        for j in range(k):                      # each unit step is a tile edge
            p = (bx + dx // k * j, by + dy // k * j)
            q = (p[0] + dx // k, p[1] + dy // k)
            if dx and dy:
                assert {kind(p), kind(q)} == {"A", "B"}, ("diagonal off the tiling", p, q)

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def on_seg(p, a, b):
        return cross(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])

    edges = [(room[i], room[(i + 1) % n]) for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if j == i + 1 or (i == 0 and j == n - 1):
                continue
            (a, b), (c, d) = edges[i], edges[j]
            d1, d2, d3, d4 = cross(c, d, a), cross(c, d, b), cross(a, b, c), cross(a, b, d)
            assert not ((d1 > 0) != (d2 > 0) and d1 and d2 and (d3 > 0) != (d4 > 0) and d3 and d4), "edges cross"
            assert not any(on_seg(p, *e) for p, e in ((a, edges[j]), (b, edges[j]), (c, edges[i]), (d, edges[i]))), "edges touch"
    def inside(m):                              # ray casting to the right
        hit = False
        for a, b in edges:
            if (a[1] > m[1]) != (b[1] > m[1]) and m[0] < a[0] + (m[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1]):
                hit = not hit
        return hit

    xs, ys = [p[0] for p in room], [p[1] for p in room]
    for x in range(min(xs), max(xs) + 1):
        for y in range(min(ys), max(ys) + 1):
            m = (x, y)
            if kind(m) != "A" and (inside(m) or any(on_seg(m, *e) for e in edges)):
                assert m in room, ("B or C point that isn't a corner", m)
    for m in marks:
        assert kind(m) == "A" and inside(m) and not any(on_seg(m, *e) for e in edges)


def check_answers():
    check_tokarsky(TOKARSKY26, 26, PUBLISHED_ST)
    check_tokarsky(CASTRO24, 24, PUBLISHED_ST)
    # Q1: light from (1,1) in direction (1,1) in [0,4]x[0,2] hits (2,2), then (4,0).
    assert (1 + 1, 1 + 1) == (2, 2) and (2 + 2, 2 - 2) == (4, 0)
    # Q7: segment (1,1)->(5,3) meets y=2 at x=3 and x=4 at y=2.5; folded back to y=1.5.
    assert Fr(1) + Fr(4) * Fr(1, 2) == 3 and Fr(1) + Fr(2) * Fr(3, 4) == Fr(5, 2)
    # Q13: lattice points of the staircase.
    sq = P_SQUARES
    pts = {(x + dx, y + dy) for x, y in sq for dx in (0, 1) for dy in (0, 1)}
    assert len(pts) == 12 and pts - set(STAIR) == {(0, 0), (2, -2)}
    # Q19-Q20 and Q25: the 22-wall room.
    squares = P_SQUARES + P1_SQUARES + P2_SQUARES
    assert len(set(squares)) == 15
    led = ledger(squares, set(ROOM22))
    assert led == dict(N=30, W=22, I=2, J=0, sA=2, sN=4, Q=12), led
    assert led["W"] == 2 + 6 * led["I"] + led["Q"] - 2 * led["J"] - led["sN"]
    turns = [(ROOM22[i][0] - ROOM22[i - 1][0]) * (ROOM22[(i + 1) % 22][1] - ROOM22[i][1])
             - (ROOM22[i][1] - ROOM22[i - 1][1]) * (ROOM22[(i + 1) % 22][0] - ROOM22[i][0]) for i in range(22)]
    convex = sum(t < 0 for t in turns)          # the list runs clockwise
    assert (convex, 22 - convex) == (13, 9)
    # Q14/Q16 figure: from a in direction (3, -4), light bounces at (2, -8/3) and (7/4, -3), stops at the
    # corner (1, -2), and unfolds to the straight segment from a to (3, -4).
    pts, maps = trace(STAIR, (0, 0), (3, -4))
    assert pts[1:] == [(2, Fr(-8, 3)), (Fr(7, 4), -3), (1, -2)] and apply(maps[-1], pts[-1]) == (3, -4)
    # Q21: the straight path, the left-wall bounce, and the top-wall try stop at (1,1), (0,1), (1,2).
    for d, n, end in (((1, 1), 0, (1, 1)), ((-2, 1), 1, (0, 1)), ((1, 2), 0, (1, 2))):
        pts, _ = trace(ROOM22, (0, 0), d)
        assert len(pts) - 2 == n and pts[-1] == end, (d, pts)
    assert trace(ROOM22, (0, 0), (-2, 1))[0][1] == (-1, Fr(1, 2))
    # Part 7 figure: the room's stars. Two full cells, b = 6 outside neighbors; three are partly in the room
    # (A corners), and three are empty, and their shared sides have midpoints E1 to E4.
    full, partial = star_cells(P_SQUARES + P1_SQUARES + P2_SQUARES)
    assert full == {(0, 0), (1, 1)} and partial == {(0, 1), (0, -1), (2, 1), (2, 0), (1, -1)}
    nb = outside_neighbors(full)
    assert len(nb) == 6 and nb & partial == {(0, 1), (0, -1), (2, 1)}
    # The shared side of stars (2X, 2Y) and (2fx, 2fy) has midpoint (X + fx, Y + fy).
    assert {(X + fx, Y + fy) for X, Y in nb - partial for fx, fy in full
            if abs(X - fx) + abs(Y - fy) == 1} == {(-1, 0), (1, 0), (2, 1), (2, 3)}   # E1, E2, E3, E4
    # Q34 figure: L of 3 grows by r = 2, then by c + 1 = 3, to m + r + c + 1 = 8 cells.
    S = set(SHAPES["L of 3"])
    step1 = S | {(x + 1, y) for x, y in S}
    step2 = step1 | {(x, y + 1) for x, y in step1}
    assert (len(step1 - S), len(step2 - step1), len(step2)) == (2, 3, 8)
    # Q23-Q24: small rooms.
    sq1 = [(-1, -1), (0, -1), (-1, 0), (0, 0)]
    assert ledger(sq1, {(-1, -1), (1, -1), (1, 1), (-1, 1)}) == dict(N=8, W=4, I=1, J=0, sA=0, sN=4, Q=0)
    sq2 = [(x, y) for x in range(-1, 3) for y in (-1, 0)]
    assert ledger(sq2, {(-1, -1), (3, -1), (3, 1), (-1, 1)}) == dict(N=16, W=4, I=2, J=1, sA=0, sN=8, Q=0)
    # Q27-Q28: outside-neighbor counts.
    b = {k: len(outside_neighbors(v)) for k, v in SHAPES.items()}
    assert b == {"one cell": 4, "domino": 6, "diagonal pair": 6, "line of 3": 8, "L of 3": 7,
                 "I": 10, "O": 8, "T": 8, "S": 8, "L": 9}, b
    return led


# ---------------------------------------------------------------- TikZ helper

def C(c):
    """A TikZ color for "white" or a #rrggbb string."""
    if c == "white":
        return "white"
    r, g, b = (int(c[i:i + 2], 16) for i in (1, 3, 5))
    return f"{{rgb,255:red,{r};green,{g};blue,{b}}}"


def style(stroke=None, w=None, fill=None, dash=None, arrow=None, extra=""):
    o = []
    if stroke and stroke != "none":
        o.append(f"draw={C(stroke)}, line width={w * PX:.2f}bp")
    if fill and fill != "none":
        o.append(f"fill={C(fill)}")
    if dash:
        on, off = dash.split()
        o.append(f"dash pattern=on {float(on) * PX:.2f}bp off {float(off) * PX:.2f}bp")
    if arrow:
        a = 4.2 * w
        o.append(f"-{{Triangle[length={a:.1f}bp, width={a:.1f}bp]}}")
    if extra:
        o.append(extra)
    return "[" + ", ".join(o) + "]"


def label(t):
    """Figure text: LaTeX, with the primes that Latin Modern lacks set in math."""
    return t.replace("′", "$'$")


class Fig:
    """A window x0..x1 by y0..y1 of the plane, s px per unit with pad px around it, drawn in TikZ.
    Like the old SVG version, it clips what falls outside the window."""

    def __init__(self, x0, x1, y0, y1, s=34, pad=16):
        self.x0, self.x1, self.y0, self.y1, self.s, self.pad = x0, x1, y0, y1, s, pad
        self.items = []

    def P(self, p, dx=0, dy=0):
        """A point in bp, y up; dx and dy are px offsets, dy down as in SVG."""
        return (PX * (self.pad + (p[0] - self.x0) * self.s + dx), PX * (self.pad + (p[1] - self.y0) * self.s - dy))

    def at(self, p, dx=0, dy=0):
        a, b = self.P(p, dx, dy)
        return f"({a:.2f},{b:.2f})"

    def grid(self, color=GRID, w=0.7):
        for x in range(math.ceil(self.x0), math.floor(self.x1) + 1):
            self.seg((x, self.y0), (x, self.y1), color, w)
        for y in range(math.ceil(self.y0), math.floor(self.y1) + 1):
            self.seg((self.x0, y), (self.x1, y), color, w)

    def poly(self, pts, fill="none", stroke=INK, w=1.6, dash=None):
        cmd = "\\path" + style(stroke, w, fill, dash, extra="line join=round")
        self.items.append(cmd + " " + " -- ".join(self.at(p) for p in pts) + " -- cycle;")

    def seg(self, p, q, stroke=INK, w=1.4, dash=None, arrow=None):
        self.path([p, q], stroke, w, dash, arrow)

    def path(self, pts, stroke=RAY, w=2, dash=None, arrow=None):
        cmd = "\\path" + style(stroke, w, dash=dash, arrow=arrow, extra="line cap=round, line join=round")
        self.items.append(cmd + " " + " -- ".join(self.at(p) for p in pts) + ";")

    def arc(self, p, start, end, r, stroke=RAY, w=2):
        """An arc that starts at p, with radius r px, from angle start to angle end in degrees."""
        self.items.append("\\path" + style(stroke, w, extra="line cap=round")
                          + f" {self.at(p)} arc[start angle={start}, end angle={end}, radius={r * PX:.2f}bp];")

    def dot(self, p, r=3.6, fill=INK, stroke="none", w=1.3):
        self.items.append("\\path" + style(stroke, w, fill) + f" {self.at(p)} circle[radius={r * PX:.2f}bp];")

    def square_mark(self, p, r=2.6, fill="#6b7280"):
        self.items.append("\\path" + style(fill=fill) + f" {self.at(p, -r, r)} rectangle {self.at(p, r, -r)};")

    def cross(self, p, r=5, color=RAY, w=2.2):
        self.items.append("\\path" + style(color, w, extra="line cap=round")
                          + f" {self.at(p, -r, -r)} -- {self.at(p, r, r)} {self.at(p, -r, r)} -- {self.at(p, r, -r)};")

    def text(self, p, t, dx=0, dy=0, size=12, anchor="start", color=INK, italic=False, weight="normal", halo=False):
        font = f"\\fontsize{{{size * PX:.1f}}}{{{size * PX * 1.2:.1f}}}\\selectfont\\sffamily"
        font += "\\bfseries" if weight == "bold" else ""
        font += "\\itshape" if italic else ""
        o = [f"anchor={dict(start='base west', middle='base', end='base east')[anchor]}", f"text={C(color)}", f"font={font}"]
        o.append("fill=white, fill opacity=0.85, text opacity=1, inner sep=1pt" if halo else "inner sep=0pt")
        self.items.append(f"\\node[{', '.join(o)}] at {self.at(p, dx, dy)} {{{label(t)}}};")

    def glyph(self, p, t, sx=1, sy=1, size=15, color=INK):
        """A letter drawn mirrored (sx or sy = -1) or turned (both -1), to show what a map does."""
        font = f"\\fontsize{{{size * PX:.1f}}}{{{size * PX:.1f}}}\\selectfont\\sffamily\\bfseries"
        self.items.append(f"\\begin{{scope}}[shift={{{self.at(p)}}}, xscale={sx}, yscale={sy}]"
                          f"\\node[transform shape, inner sep=0pt, text={C(color)}, font={font}] {{{t}}};\\end{{scope}}")

    def rect(self, x, y, w, h, fill, stroke="none", sw=0):
        self.items.append("\\path" + style(stroke, sw, fill) + f" {self.at((x, y))} rectangle {self.at((x + w, y + h))};")

    def tikz(self):
        W = PX * (2 * self.pad + (self.x1 - self.x0) * self.s)
        H = PX * (2 * self.pad + (self.y1 - self.y0) * self.s)
        return ("\\begin{tikzpicture}[x=1bp, y=1bp]"
                f"\\path[use as bounding box] (0,0) rectangle ({W:.2f},{H:.2f});\\clip (0,0) rectangle ({W:.2f},{H:.2f});\n"
                + "\n".join(self.items) + "\n\\end{tikzpicture}")


def axis_labels(f, xs, ys, size=9):
    for x in xs:
        f.text((x, f.y0), str(x).replace("-", "−"), dy=12, size=size, anchor="middle", color="#6b7280")
    for y in ys:
        f.text((f.x0, y), str(y).replace("-", "−"), dx=-5, dy=3, size=size, anchor="end", color="#6b7280")


def lattice_marks(f, pts):
    for p in pts:
        k = kind(p)
        if k == "A":
            f.dot(p, 3.4, INK)
        elif k == "B":
            f.dot(p, 3.4, "white", INK, 1.3)
        else:
            f.square_mark(p, 2.4)


def draw_tiles(f, squares, color="#9aa5b8"):
    for a, b, _ in tiles_of_squares(squares):
        f.seg(a, b, color, 0.8)


def box(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def panels(*items, gap=30):
    """Side-by-side pictures, bottom-aligned, each with a small label under it (\\panel in worksheet.tex)."""
    return f"\\hspace{{{gap * PX:.1f}bp}}".join(f"\\panel{{{pic}}}{{{text}}}" for pic, text in items)


# ---------------------------------------------------------------- figures

def fig_rules():
    f = Fig(-0.6, 6.6, -0.7, 3.4, s=28, pad=12)
    f.poly([(0, 0), (6, 0), (6, 3), (0, 3)], ROOM, WALL, 2.4)
    f.grid(FAINT)
    f.poly([(0, 0), (6, 0), (6, 3), (0, 3)], "none", WALL, 2.4)
    f.path([(1, 1), (5, 3), (6, 2.5), (4.2, 1.6)], RAY, 2.2, arrow="red")
    f.path([(1, 1), (0.05, 0.05)], GHOST, 2, dash="5 4")
    f.cross((0, 0), 6, GHOST)
    f.text((0, 0), "stops at a corner", dx=10, dy=16, size=11, color="#6b7280")
    f.dot((1, 1), 4.2, INK)
    f.text((1, 1), "S", dx=-14, dy=4, size=14, weight="bold")
    f.dot((4, 1.5), 4.2, INK)
    f.text((4, 1.5), "T", dx=-6, dy=18, size=14, weight="bold")
    return f.tikz()


def fig_blank_rect():
    f = Fig(-0.4, 4.4, -0.5, 2.4, s=32, pad=12)
    f.grid(FAINT)
    f.poly([(0, 0), (4, 0), (4, 2), (0, 2)], "none", WALL, 2.4)
    axis_labels(f, range(0, 5), range(0, 3))
    f.dot((1, 1), 4, INK)
    f.text((1, 1), "(1, 1)", dx=-8, dy=18, size=11)
    f.seg((1, 1), (1.45, 1.45), INK, 1.6, arrow="ink")
    return f.tikz()


def fig_unfold():
    f = Fig(-0.4, 8.4, -0.4, 2.5, s=34, pad=12)
    f.poly([(0, 0), (4, 0), (4, 2), (0, 2)], ROOM, WALL, 2.4)
    f.poly([(4, 0), (8, 0), (8, 2), (4, 2)], "none", "#7c8db5", 1.6, "6 4")
    f.text((6, 2), "mirror copy", dy=-6, size=11, anchor="middle", color="#6b7280")
    f.text((2, 2), "room", dy=-6, size=11, anchor="middle", color="#6b7280")
    s, t, tp, hit = (1, 0.5), (2, 1.5), (6, 1.5), (4, 1.1)
    f.seg(hit, tp, RAY, 1.6, "5 4")
    f.path([s, hit, (2.15, 1.47)], RAY, 2.2, arrow="red")
    for p, name, dx in ((s, "S", -14), (t, "T", -14), (tp, "T′", 8)):
        f.dot(p, 4.2, INK)
        f.text(p, name, dx=dx, dy=5, size=14, weight="bold")
    return f.tikz()


def fig_tiling():
    f = Fig(-1.4, 5.4, -1.4, 4.4, s=31, pad=12)
    f.rect(1, 1, 2, 2, STAR)
    f.grid(GRID, 0.9)
    sq = [(x, y) for x in range(-1, 5) for y in range(-1, 4)]
    draw_tiles(f, sq, "#8792a8")
    lattice_marks(f, [(x, y) for x in range(-1, 6) for y in range(-1, 5)])
    axis_labels(f, range(-1, 6), range(-1, 5))
    return f.tikz()


def fig_stair():
    f = Fig(-1.6, 2.6, -3.6, 0.7, s=34, pad=12)
    f.grid(FAINT)
    f.poly(STAIR, ROOM, WALL, 2.4)
    axis_labels(f, range(-1, 3), range(-3, 1))
    for p, name, dx, dy in (((0, 0), "a", -4, -9), ((2, -2), "b", 9, 4)):
        f.dot(p, 4.6, RAY)
        f.text(p, name, dx=dx, dy=dy, size=15, weight="bold", color=RAY, italic=True)
    return f.tikz()


def fig_room22(labels=True, tiles=False):
    f = Fig(-1.8, 5.8, -3.6, 3.8, s=36, pad=12)
    f.grid(FAINT)
    for sqs, col in ((P_SQUARES, P0C), (P1_SQUARES, P1C), (P2_SQUARES, P2C)):
        for x, y in sqs:
            f.rect(x, y, 1, 1, col if labels else ROOM)
    if tiles:
        draw_tiles(f, P_SQUARES + P1_SQUARES + P2_SQUARES)
        sq = P_SQUARES + P1_SQUARES + P2_SQUARES
        lattice_marks(f, sorted({(x + dx, y + dy) for x, y in sq for dx in (0, 1) for dy in (0, 1)}))
    f.poly(ROOM22, "none", WALL, 2.6)
    axis_labels(f, range(-1, 6), range(-3, 4))
    if labels:
        f.seg((-1, 0), (1, 0), "#475569", 1.6, "5 4")
        f.seg((2, 1), (2, 3), "#475569", 1.6, "5 4")
        f.text((1.5, -2.5), "P0", dx=2, size=12, anchor="middle", weight="bold", color="#1d4ed8")
        f.text((0.5, 1.5), "P1", size=12, anchor="middle", dy=4, weight="bold", color="#15803d")
        f.text((4.5, 0.5), "P2", size=12, anchor="middle", dy=4, weight="bold", color="#b45309")
        for p, name, dx, dy in (((-1, 0), "E1", -22, 4), ((1, 0), "E2", 6, 14), ((2, 1), "E3", 4, 14),
                                ((2, 3), "E4", 4, -6)):
            f.dot(p, 3.4, "white", "#475569", 1.6)
            f.text(p, name, dx=dx, dy=dy, size=10.5, color="#475569")
        for p, name in (((0, 0), "S"), ((2, 2), "T")):
            f.dot(p, 4.4, RAY)
            f.text(p, name, dx=7, dy=-6, size=14, weight="bold", color=RAY)
    return f.tikz()


def fig_history():
    def room(poly, st, x0, x1, y0, y1):
        f = Fig(x0, x1, y0, y1, s=20, pad=8)
        f.grid(FAINT)
        f.poly(poly, ROOM, WALL, 2.2)
        for p, name in zip(st, "ST"):
            f.dot(p, 3.8, RAY)
            f.text(p, name, dx=6, dy=-5, size=12, weight="bold", color=RAY)
        return f.tikz()
    return panels((room(TOKARSKY26, PUBLISHED_ST, -0.3, 8.3, -4.3, 0.3), "(a) Tokarsky, 1995: 26 walls"),
                  (room(CASTRO24, PUBLISHED_ST, -0.3, 8.3, -4.3, 0.3), "(b) Castro, 1997: 24 walls"),
                  (room(ROOM22, ((0, 0), (2, 2)), -1.3, 5.3, -3.3, 3.3), "(c) Your room: 22 walls"))


def fig_small_rooms():
    a = Fig(-1.7, 1.7, -1.7, 1.7, s=40, pad=10)
    a.grid(FAINT)
    sq1 = [(-1, -1), (0, -1), (-1, 0), (0, 0)]
    for x, y in sq1:
        a.rect(x, y, 1, 1, ROOM)
    draw_tiles(a, sq1)
    a.poly([(-1, -1), (1, -1), (1, 1), (-1, 1)], "none", WALL, 2.4)
    lattice_marks(a, [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1)])
    a.text((0, 1), "(a)", dy=-10, size=12, anchor="middle", weight="bold")
    b = Fig(-1.7, 3.7, -1.7, 1.7, s=40, pad=10)
    b.grid(FAINT)
    sq2 = [(x, y) for x in range(-1, 3) for y in (-1, 0)]
    for x, y in sq2:
        b.rect(x, y, 1, 1, ROOM)
    draw_tiles(b, sq2)
    b.poly([(-1, -1), (3, -1), (3, 1), (-1, 1)], "none", WALL, 2.4)
    lattice_marks(b, [(x, y) for x in range(-1, 4) for y in (-1, 0, 1)])
    b.text((1, 1), "(b)", dy=-10, size=12, anchor="middle", weight="bold")
    return a.tikz() + f"\\hspace{{{36 * PX}bp}}" + b.tikz()


def cell_fig(cells, x0, x1, y0, y1, mark_neighbors=False, s=24, title=None):
    f = Fig(x0, x1, y0, y1, s=s, pad=8)
    f.grid(GRID, 0.8)
    for x, y in cells:
        f.rect(x, y, 1, 1, "#6366f1", "#4338ca", 0.8)
    if mark_neighbors:
        for x, y in outside_neighbors(cells):
            f.dot((x + 0.5, y + 0.5), 4.2, "#f59e0b")
    return f"\\panel{{{f.tikz()}}}{{{title}}}" if title else f.tikz()


def fig_star_shrink():
    squares = P_SQUARES + P1_SQUARES + P2_SQUARES
    full, partial = star_cells(squares)
    a = Fig(-3.4, 5.4, -3.4, 5.4, s=18, pad=8)
    a.grid(FAINT)
    for x, y in squares:
        a.rect(x, y, 1, 1, ROOM)
    for X, Y in full:
        a.rect(2 * X - 1, 2 * Y - 1, 2, 2, "#c7d2fe")
    draw_tiles(a, squares, "#b6bfd0")
    for c in range(-3, 6, 2):
        a.seg((c, -3.4), (c, 5.4), "#818cf8", 1.1)
        a.seg((-3.4, c), (5.4, c), "#818cf8", 1.1)
    a.poly(ROOM22, "none", WALL, 2.2)
    for X, Y in full | partial:
        a.dot((2 * X, 2 * Y), 3.2, INK)
    for p in ((-1, 0), (1, 0), (2, 1), (2, 3)):
        a.square_mark(p, 3.6, "#f59e0b")
    b = Fig(-1.6, 3.1, -1.6, 3.1, s=32, pad=8)
    for X, Y in partial:
        b.rect(X, Y, 1, 1, "#e0e7ff")
    for X, Y in full:
        b.rect(X, Y, 1, 1, "#6366f1")
    b.grid(GRID, 0.9)
    for X, Y in outside_neighbors(full):
        b.dot((X + 0.5, Y + 0.5), 5, "#f59e0b")
    b.text((0.5, 0.5), "S", dy=5, size=13, anchor="middle", color="white", weight="bold")
    b.text((1.5, 1.5), "T", dy=5, size=13, anchor="middle", color="white", weight="bold")
    return panels((a.tikz(), "(a) Your room, cut into stars"), (b.tikz(), "(b) Each star shrunk to one cell"), gap=48)


def fig_expansion():
    S = set(SHAPES["L of 3"])
    step1 = S | {(x + 1, y) for x, y in S}
    step2 = step1 | {(x, y + 1) for x, y in step1}

    def grid_of(layers):
        f = Fig(-0.5, 3.5, -0.5, 3.5, s=24, pad=6)
        for cells, color in layers:
            for x, y in cells:
                f.rect(x, y, 1, 1, color)
        f.grid(GRID, 0.9)
        return f.tikz()

    s0 = grid_of([(S, "#6366f1")])
    s1 = grid_of([(S, "#6366f1"), (step1 - S, "#86efac")])
    s2 = grid_of([(S, "#6366f1"), (step1 - S, "#86efac"), (step2 - step1, "#fdba74")])
    c = Fig(-0.2, 5.2, -0.2, 5.2, s=26, pad=6)
    for x in range(5):
        for y in range(5):
            if (x + y) % 2 == 0:
                c.rect(x, y, 1, 1, "#cbd5e1")
    c.grid("#94a3b8", 0.9)
    c.rect(2, 2, 1, 1, "#6366f1")
    for x, y in ((1, 2), (3, 2), (2, 1), (2, 3)):
        c.dot((x + 0.5, y + 0.5), 5, "#f59e0b")
    c.poly([(1.5, 2.5), (2.5, 3.5), (3.5, 2.5), (2.5, 1.5)], "none", "#b45309", 1.6, "4 3")
    c.seg((0.5, 0.5), (1.5, 1.5), INK, 1.6, arrow="ink")
    c.text((1.5, 1.5), "u", dx=4, dy=12, size=13, italic=True, weight="bold", halo=True)
    c.seg((0.5, 4.5), (1.5, 3.5), INK, 1.6, arrow="ink")
    c.text((1.5, 3.5), "v", dx=4, dy=-4, size=13, italic=True, weight="bold", halo=True)
    return panels((s0, "(a) $S$: $m = 3$, $r = 2$, $c = 2$"),
                  (s1, "add the right shift: 2 new"),
                  (s2, "add the up shift: 3 new"),
                  (c.tikz(), "(b) a dark cell's 4 neighbors"), gap=22)


def fig_cells_blank():
    rows = []
    row1 = [("one cell", (-1, 2, -1, 2)), ("domino", (-1, 3, -1, 2)), ("diagonal pair", (-1, 3, -1, 3)),
            ("line of 3", (-1, 4, -1, 2)), ("L of 3", (-1, 3, -1, 3))]
    row2 = [("I", (-1, 5, -1, 2)), ("O", (-1, 3, -1, 3)), ("T", (-1, 4, -1, 3)), ("S", (-1, 4, -1, 3)),
            ("L", (-1, 3, -1, 4))]
    for row in (row1, row2):
        rows.append("\\hspace*{\\fill}" + "\\hfill".join(
            cell_fig(SHAPES[name], *box, s=21, title=name if len(name) > 1 else f"{name} shape") for name, box in row)
            + "\\hspace*{\\fill}")
    return "\\par\\medskip\n".join(rows)


def fig_turnaround():
    f = Fig(-0.9, 1.9, -1.2, 1.2, s=56, pad=10)
    f.rect(-0.9, 0, 1.9, 1.2, P1C)
    f.rect(-0.9, -1.2, 1.9, 1.2, P0C)
    f.seg((-0.9, 0), (1, 0), "#475569", 1.6, "5 4")
    f.seg((1, -1.2), (1, 1.2), WALL, 3)
    f.text((1, 1.2), "wall x = 1", dx=6, dy=14, size=11, color=WALL)
    f.path([(0.2, 0.8), (0.97, 0.03)], RAY, 2.2, arrow="red")
    f.dot((1, 0), 4, "white", "#475569", 1.8)
    f.text((1, 0), "E2", dx=7, dy=4, size=11, color="#475569")
    f.text((-0.6, 0.6), "P1", size=12, weight="bold", color="#15803d")
    f.text((-0.6, -0.6), "P0", size=12, weight="bold", color="#1d4ed8")
    g = Fig(-0.9, 1.9, -1.2, 1.2, s=56, pad=10)
    g.grid(FAINT)
    g.poly(STAIR, P0C, WALL, 3)
    g.dot((1, 0), 4.4, INK)
    g.text((1, 0), "corner (1, 0) of P", dx=-6, dy=-10, size=11, anchor="end", color=INK)
    return panels((f.tikz(), "(a) In your room"), (g.tikz(), "(b) Folded into $P$: draw both directions here"))


def fig_lroom():
    f = Fig(-0.3, 4.3, -0.3, 4.3, s=25, pad=10)
    L = [(0, 0), (4, 0), (4, 2), (2, 2), (2, 4), (0, 4)]
    f.poly(L, ROOM, WALL, 2.4)
    f.grid(FAINT)
    f.poly(L, "none", WALL, 2.4)
    f.seg((0.5, 0.5), (1.94, 1.94), GHOST, 2, "5 4")
    f.cross((2, 2), 6, GHOST)
    f.path([(0.4, 0.6), (2, 2.2), (1.05, 3.15)], RAY, 2, arrow="red")
    f.path([(0.6, 0.4), (2.2, 2), (3.15, 1.05)], RAY, 2, arrow="red")
    f.text((2, 2), "inner corner", dx=10, dy=-8, size=11, color="#6b7280")
    return f.tikz()


def fig_mirror_copies():
    f = Fig(-0.5, 8.5, -2.5, 4.5, s=27, pad=12)
    f.grid(FAINT)
    f.poly(box(0, 0, 4, 2), ROOM, WALL, 2.4)
    for x, y, label in ((0, 2, "(a)"), (0, -2, "(b)"), (4, 2, "(c)")):
        f.poly(box(x, y, x + 4, y + 2), "none", "#7c8db5", 1.6, "6 4")
        f.text((x, y + 2), label, dx=5, dy=15, size=11, color="#6b7280", weight="bold")
    axis_labels(f, range(0, 9), range(-2, 5))
    for p, name in (((1, 1), "S"), ((3, 1), "T")):
        f.dot(p, 4.2, INK)
        f.text(p, name, dx=-14, dy=5, size=14, weight="bold")
    return f.tikz()


def fig_number_line():
    f = Fig(-0.5, 8.5, -1.3, 1.5, s=30, pad=8)
    f.seg((-0.3, 0), (8.3, 0), INK, 1.4)
    for x in range(9):
        f.seg((x, -0.1), (x, 0.1), INK, 1.2)
        f.text((x, 0), str(x), dy=20, size=10.5, anchor="middle", color="#6b7280")
    f.seg((3, -0.35), (3, 1.3), "#7c3aed", 1.8, "5 4")
    f.text((3, 1.3), "mirror at c = 3", dy=-4, size=11, anchor="middle", color="#7c3aed")
    for a, b in ((1, 3), (3, 5)):
        f.seg((a, 0.5), (b, 0.5), "#475569", 1.2)
        f.seg((a, 0.4), (a, 0.6), "#475569", 1.2)
        f.seg((b, 0.4), (b, 0.6), "#475569", 1.2)
        f.text(((a + b) / 2, 0.5), "c − x", dy=-5, size=10.5, anchor="middle", color="#475569")
    for x, label in ((1, "x"), (5, "2c − x")):
        f.dot((x, 0), 4.4, RAY)
        f.text((x, 0), label, dy=36, size=11.5, anchor="middle", color=RAY, weight="bold")
    return f.tikz()


def fig_lattice_questions():
    a = Fig(-1.4, 4.4, -2.4, 3.9, s=27, pad=10)
    a.grid(GRID, 0.9)
    draw_tiles(a, [(x, y) for x in range(-1, 4) for y in range(-2, 3)], "#a3acbf")
    a.seg((-1, 3), (4, -2), "#7c3aed", 2.4)
    a.text((-1, 3), "x + y = 2", dx=-4, dy=-9, size=11, color="#7c3aed", weight="bold")
    lattice_marks(a, [(x, y) for x in range(-1, 5) for y in range(-2, 4)])
    a.seg((3, 2), (0.1, -0.9), RAY, 1.6, "4 3", arrow="red")
    a.text((3, 2), "(3, 2)", dx=7, dy=-7, size=10.5, color=RAY, halo=True)
    a.text((0, -1), "(0, −1)", dx=-7, dy=14, size=10.5, anchor="end", color=RAY, halo=True)
    b = Fig(-0.5, 4.5, -0.5, 8.5, s=18, pad=14)
    b.grid(GRID, 0.8)
    b.seg((0, 0), (4, 8), RAY, 2)
    for p in ((0, 0), (4, 8)):
        b.dot(p, 3.6, INK)
    axis_labels(b, range(0, 5), range(0, 9, 2))
    return panels((a.tikz(), "(a) Question 11"), (b.tikz(), "(b) Question 12"), gap=48)


def fig_unfold_P():
    pts, maps = trace(STAIR, (0, 0), (3, -4))
    a = Fig(-1.5, 2.5, -3.5, 0.5, s=34, pad=12)
    a.grid(FAINT)
    a.poly(STAIR, ROOM, WALL, 2.4)
    a.path(pts, RAY, 2)
    a.cross(pts[-1], 6, RAY)
    a.text(pts[-1], "(1, −2)", dx=-8, dy=15, size=11, anchor="end", color=RAY)
    a.dot((0, 0), 4.4, RAY)
    a.text((0, 0), "a", dx=-4, dy=-9, size=14, color=RAY, weight="bold", italic=True)
    axis_labels(a, range(-1, 3), range(-3, 1))
    b = Fig(-1.5, 5.5, -6.5, 0.5, s=24, pad=12)
    b.grid(FAINT)
    for m, name in zip(maps, ("P", "copy 1", "copy 2")):
        poly = [apply(m, v) for v in STAIR]
        b.poly(poly, ROOM if name == "P" else "none", WALL if name == "P" else "#7c8db5", 2 if name == "P" else 1.6,
               None if name == "P" else "6 4")
        b.text(apply(m, (-0.5, -0.5)), name, dy=4, size=9.5, anchor="middle", color="#475569",
               italic=name == "P", weight="bold", halo=True)
    b.seg((0, 0), (3, -4), RAY, 2)
    for q, m in zip(pts[1:-1], maps[1:]):
        b.dot(apply(m, q), 3, "white", RAY, 1.4)
    b.dot((0, 0), 4.4, RAY)
    b.text((0, 0), "a", dx=-4, dy=-9, size=14, color=RAY, weight="bold", italic=True)
    b.dot((3, -4), 4.4, RAY)
    b.text((3, -4), "(3, −4)", dx=8, dy=14, size=11, color=RAY, halo=True)
    axis_labels(b, range(-1, 6), range(-6, 1))
    return panels((a.tikz(), "(a) The real path in $P$"), (b.tikz(), "(b) The same path, unfolded"), gap=40)


def fig_halving():
    f = Fig(-0.6, 12.6, -8.6, 0.6, s=15, pad=14)
    f.grid(FAINT)
    f.seg((0, 0), (12, -8), RAY, 2)
    f.dot((0, 0), 4.2, INK)
    f.text((0, 0), "a = (0, 0)", dx=8, dy=-4, size=11)
    for p, label in (((3, -2), "z = (3, −2)"), ((6, -4), "B/2 = (6, −4)")):
        f.dot(p, 4.2, RAY)
        f.text(p, label, dx=9, dy=-3, size=11, color=RAY)
    f.dot((12, -8), 4.2, INK)
    f.text((12, -8), "B = (12, −8)", dx=-10, dy=4, size=11, anchor="end")
    return f.tikz()


def fig_copies():
    def panel(copy, img, sx, sy, mark):
        f = Fig(-1.5, 5.5, -3.5, 3.5, s=20, pad=10)
        f.grid(FAINT)
        for x, y in P_SQUARES:
            f.rect(x, y, 1, 1, P0C)
        for x, y in copy[0]:
            f.rect(x, y, 1, 1, copy[1])
        f.poly(STAIR, "none", WALL, 2)
        f.poly([img(v) for v in STAIR], "none", WALL, 2)
        mark(f)
        f.glyph((-0.5, -0.5), "F")
        f.glyph(img((-0.5, -0.5)), "F", sx, sy)
        f.text((0.5, -2.6), "P", size=12, anchor="middle", weight="bold", italic=True, color="#1d4ed8")
        return f.tikz()

    def mirror(f):
        f.seg((-1.5, 0), (5.5, 0), "#7c3aed", 1.8, "6 4")
        f.text((5.5, 0), "mirror", dx=-4, dy=-6, size=10.5, anchor="end", color="#7c3aed")
        f.text((0.5, 2.6), "P1", size=12, anchor="middle", weight="bold", color="#15803d")

    def center(f):
        f.seg((-0.5, -0.5), (4.5, 0.5), "#7c3aed", 1.4, "4 3")
        f.dot((2, 0), 4, "#7c3aed")
        f.text((2, 0), "center (2, 0)", dx=6, dy=16, size=10.5, color="#7c3aed")
        f.text((3.5, 1.6), "P2", size=12, anchor="middle", weight="bold", color="#b45309")

    a = panel((P1_SQUARES, P1C), lambda v: (v[0], -v[1]), 1, -1, mirror)
    b = panel((P2_SQUARES, P2C), lambda v: (4 - v[0], -v[1]), -1, -1, center)
    return panels((a, "(a) $P$1: reflect across the $x$-axis"),
                  (b, "(b) $P$2: a half turn around (2,~0)"), gap=40)


def fig_three_tries():
    def panel(x0, x1, y1, img=None, wall=None, tp=None):
        f = Fig(x0, x1, -3.5, y1, s=16, pad=8)
        f.grid(FAINT)
        if img:
            f.poly([img(v) for v in ROOM22], "none", "#7c8db5", 1.4, "5 4")
        f.poly(ROOM22, ROOM, WALL, 2)
        if wall:
            f.seg(*wall, "#7c3aed", 3)
        for p, name in (((0, 0), "S"), ((2, 2), "T")):
            f.dot(p, 3.6, RAY)
            f.text(p, name, dx=5, dy=-5, size=11, weight="bold", color=RAY)
        if tp:
            f.dot(tp, 3.6, "white", RAY, 1.6)
            f.text(tp, "T′", dx=5, dy=-5, size=11, weight="bold", color=RAY)
        return f.tikz()

    a = panel(-1.5, 5.5, 3.5)
    b = panel(-5.5, 5.5, 3.5, lambda v: (-2 - v[0], v[1]), ((-1, -1), (-1, 1)), (-4, 2))
    c = panel(-1.5, 5.5, 5.5, lambda v: (v[0], 6 - v[1]), ((1, 3), (3, 3)), (2, 4))
    return panels((a, "(a) straight"), (b, "(b) mirror across $x = -1$"), (c, "(c) mirror across $y = 3$"),
                  gap=22)


def fig_timeline():
    col = "#475569"
    H = 132 + 46
    f = Fig(0, 520, -H, 0, s=1, pad=0)
    P = lambda x, y: (x, -y)                   # px, y down, as the layout below was drawn
    rows = (28, 72, 132)
    ax, cx, bx = 40, 330, 470
    f.seg(P(ax, rows[0]), P(cx, rows[0]), RAY, 2.2, arrow="red")
    f.arc(P(cx, rows[0]), 90, -90, 22)
    f.seg(P(cx, rows[1]), P(ax + 6, rows[1]), RAY, 2.2, "7 4", arrow="red")
    f.seg(P(ax, rows[1] + 8), P(ax, rows[2] - 8), col, 1.4, "2 4")
    f.seg(P(ax, rows[2]), P(bx, rows[2]), RAY, 2.2, arrow="red")
    f.path([P(ax, rows[2] + 12), P(ax, rows[2] + 20), P(bx, rows[2] + 20), P(bx, rows[2] + 12)], col, 1.2)
    for y in rows:
        f.dot(P(ax, y), 4.4, INK)
        f.text(P(ax, y), "a", dx=-10, dy=5, size=14, anchor="end", italic=True, weight="bold")
    mid = (rows[0] + rows[1]) / 2
    f.dot(P(cx + 22, mid), 4.4, INK)
    f.text(P(cx + 32, mid), "corner: turns around", dy=4, size=11.5)
    f.text(P((ax + cx) / 2, rows[0]), "route \\textit{R}", dy=-8, size=11.5, anchor="middle")
    f.text(P((ax + cx) / 2, rows[1]), "\\textit{R} backward", dy=-8, size=11.5, anchor="middle")
    f.text(P(ax + 10, (rows[1] + rows[2]) / 2), "maybe more round trips, each back to \\textit{a}", dy=4, size=11,
           color=col)
    f.dot(P(bx, rows[2]), 4.4, INK)
    f.text(P(bx, rows[2]), "b", dx=10, dy=5, size=14, italic=True, weight="bold")
    f.text(P((ax + bx) / 2, rows[2]), "the shorter path: from the last visit to \\textit{a} to the first visit to \\textit{b}",
           dy=36, size=11.5, anchor="middle", color=col)
    return f.tikz()


def lualatex():
    """Run LuaLaTeX twice (for the figure references) in the florilegium-tex image, with florilegium on the path."""
    cmd = ["docker", "run", "--rm", "-u", f"{os.getuid()}:{os.getgid()}", "-e", "HOME=/tmp",
           "-e", "TEXINPUTS=.:./vendor/florilegium:", "-e", "LUAINPUTS=.:./vendor/florilegium:",
           "-v", f"{HERE}:/work", "-w", "/work", "florilegium-tex",
           "lualatex", "-interaction=nonstopmode", "-halt-on-error", "-output-directory=build", "worksheet.tex"]
    for _ in range(2):
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            raise SystemExit(r.stdout[-3000:])
    log = (HERE / "build" / "worksheet.log").read_text(errors="replace")
    problems = re.findall(r"Missing character: .*|LaTeX Warning: Reference .* undefined.*|Overfull \\hbox.*", log)
    assert not problems, problems


def main():
    check_answers()
    figs = {
        "rules": fig_rules(), "blank": fig_blank_rect(), "lroom": fig_lroom(),
        "unfold": fig_unfold(), "mirrors": fig_mirror_copies(), "numline": fig_number_line(),
        "tiling": fig_tiling(), "latticeqs": fig_lattice_questions(), "stair": fig_stair(),
        "unfoldp": fig_unfold_P(), "halving": fig_halving(), "copies": fig_copies(),
        "room": fig_room22(), "tries": fig_three_tries(), "turn": fig_turnaround(),
        "timeline": fig_timeline(), "small": fig_small_rooms(),
        "roomtiles": fig_room22(labels=False, tiles=True), "shrink": fig_star_shrink(),
        "shapes": fig_cells_blank(), "expansion": fig_expansion(), "history": fig_history(),
    }
    # Every figure appears once in worksheet.tex, through \\fig or \\sidefig, which also label it fig:<key>.
    tex = re.sub(r"(?m)^%.*$", "", (HERE / "worksheet.tex").read_text())
    used = re.findall(r"\\(?:side)?fig\{(\w+)\}", tex)
    assert sorted(used) == sorted(figs), (sorted(used), sorted(figs))
    (HERE / "figs").mkdir(exist_ok=True)
    (HERE / "build").mkdir(exist_ok=True)
    for k, v in figs.items():
        (HERE / "figs" / f"{k}.tex").write_text(v + "\n")
    lualatex()
    pdf = HERE / "dark-rooms-worksheet.pdf"
    shutil.copy(HERE / "build" / "worksheet.pdf", pdf)
    print("wrote", pdf, pdf.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
