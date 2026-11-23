"""Exact LIT/DARK decider for lattice points of an orthogonal lattice room.

Model: the 4-fold unfolding X of the room, a square-tiled translation surface
with one square per (cell, sheet). Its lattice points are the lifts of room
lattice points. Polygon vertices (convex and reflex) are blocked; every other
lattice point is regular. A billiard path between lattice points S and T is a
straight segment in X of rational slope from a lift of S to a lift of T that
meets no blocked point. The C program `orbit` explores the whole SL(2,Z) orbit
of the decorated surface, so every primitive direction is scanned once as the
horizontal direction of some state. DARK therefore means: no direction and no
length works. LIT comes with a witness vector that `tracer.py` re-checks.
"""
import os
import subprocess

from room import lattice_points, status

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "orbit")


def build():
    src = os.path.join(HERE, "orbit.c")
    if not os.path.exists(BIN) or os.path.getmtime(BIN) < os.path.getmtime(src):
        subprocess.run(["cc", "-O2", "-o", BIN, src], check=True)


def origami(cells):
    """Squares (cell, sx, sy); developing +x is room direction sx, +y is sy."""
    sq = [(c, sx, sy) for c in sorted(cells) for sx in (1, -1) for sy in (1, -1)]
    idx = {s: k for k, s in enumerate(sq)}
    h, v, ll = [], [], []
    for (c, sx, sy) in sq:
        i, j = c
        nb = (i + sx, j)
        h.append(idx[(nb, sx, sy)] if nb in cells else idx[(c, -sx, sy)])
        nb = (i, j + sy)
        v.append(idx[(nb, sx, sy)] if nb in cells else idx[(c, sx, -sy)])
        ll.append((i + (1 if sx < 0 else 0), j + (1 if sy < 0 else 0)))
    assert sorted(h) == list(range(len(sq))) and sorted(v) == list(range(len(sq)))
    return sq, h, v, ll


def decide(cells, sources, wanted=(), cap=4_000_000, verbose=False):
    """Illumination among `sources` (regular lattice points of the room).

    wanted: unordered pairs of sources; the search stops early once all are lit.
    Returns dict with
      lit       set of ordered pairs (s, t) found lit (with witness)
      witness   pair -> developing vector (DX, DY) of a legal path s -> t
      states    number of orbit states stored
      status    'DONE'  : the whole orbit was scanned, so every pair not in
                          `lit` is DARK (complete decision)
                'EARLY' : every wanted pair is lit; other pairs undecided
                'CAP'   : state cap reached; pairs not in `lit` undecided
      trace     (verbose only) list of (matrix, set of (s, t) seen) per state
    """
    build()
    cells = set(cells)
    for p in sources:
        assert status(cells, p) in ("interior", "smooth"), p
    sq, h, v, ll = origami(cells)
    sid = {p: k for k, p in enumerate(sources)}
    lab = []
    for p in ll:
        if p in sid:
            lab.append(sid[p])
        elif status(cells, p) in ("convex", "reflex"):
            lab.append(-1)
        else:
            lab.append(-2)
    n = len(sq)
    wl = [(sid[a], sid[b]) for a, b in wanted]
    inp = f"{n} {len(sources)} {cap} {1 if verbose else 0}\n" + \
        f"{len(wl)} " + " ".join(f"{a} {b}" for a, b in wl) + "\n" + \
        " ".join(map(str, h)) + "\n" + " ".join(map(str, v)) + "\n" + \
        " ".join(map(str, lab)) + "\n"
    out = subprocess.run([BIN], input=inp, capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"orbit failed: {out.stderr}")
    res = {"lit": set(), "witness": {}, "states": None, "status": None, "trace": []}
    for line in out.stdout.split("\n"):
        f = line.split()
        if not f:
            continue
        if f[0] == "LIT":
            s, t, steps, dx, dy = map(int, f[1:])
            pair = (sources[s], sources[t])
            res["lit"].add(pair)
            res["witness"][pair] = (steps * dx, steps * dy)
        elif f[0] == "ST":
            res["trace"].append((tuple(map(int, f[1:])), set()))
        elif f[0] == "R":
            res["trace"][-1][1].add((sources[int(f[1])], sources[int(f[2])]))
        elif f[0] == "STATES":
            res["states"] = int(f[1])
        elif f[0] in ("DONE", "EARLY", "CAP"):
            res["status"] = f[0]
    assert res["status"] is not None
    return res


def regular_points(cells):
    return sorted(p for p in lattice_points(cells) if status(cells, p) in ("interior", "smooth"))
