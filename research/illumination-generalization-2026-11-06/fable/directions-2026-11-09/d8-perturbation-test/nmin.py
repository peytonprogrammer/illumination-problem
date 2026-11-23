"""Monodromy of DP -> unit pillowcase, the finest parity factor N_min, and
separation of lattice points by N_min (definitions of d2-factor-audit/audit.md,
section 3.1). Uses the copied, unmodified reference code in ref/.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "ref"))
import room_model as RM          # noqa: E402  (pillow_model, class_perms, closure_partition, quotient)
import d4_monodromy as D4        # noqa: E402  (group order, minimal blocks)
from enum_targets import cycles  # noqa: E402

from room import around, cls, lattice_points, status  # noqa: E402


def model(cells, origin):
    """Monodromy data with A class = origin + 2Z^2."""
    cells = set(cells)
    cl, idx, lam, rho, the = RM.pillow_model(cells, origin)
    n = len(cl)
    cp = RM.class_perms(lam, rho, the)
    # consistency: cycles of sigma_X <-> lattice points of class X by status
    pts = lattice_points(cells)
    for X, perm in cp.items():
        lens = sorted(len(c) for c in cycles(perm))
        exp = []
        for p in pts:
            if cls(p, origin) != X:
                continue
            st = status(cells, p)
            exp += {"convex": [1], "smooth": [2], "interior": [2, 2], "reflex": [3]}[st]
        assert lens == sorted(exp), (X, lens, sorted(exp))
    seeds = [c for X in ("C1", "B", "C2") for c in cycles(cp[X]) if len(c) == 2]
    gens = (lam, rho, the)
    bmin = RM.closure_partition(n, gens, seeds)
    bid, (ql, qr, qt) = RM.quotient(bmin, gens)
    acyc = {}
    for c in cycles(ql):
        for b in c:
            acyc[b] = min(c)

    def image(p):
        """Images in N_min (A-point ids) of the DP lifts of a regular A point p."""
        cs = around(cells, p)
        ox, oy = origin
        ev = [c for c in cs if (c[0] - ox + c[1] - oy) % 2 == 0]
        od = [c for c in cs if (c[0] - ox + c[1] - oy) % 2 == 1]
        lifts = [ev, od] if status(cells, p) == "interior" else [ev + od]
        out = []
        for lift in lifts:
            im = {acyc[bid[idx[c]]] for c in lift}
            assert len(im) == 1, (p, im)
            out.append(im.pop())
        return frozenset(out)

    return {"n": n, "gens": gens, "bmin": bmin, "image": image, "seeds": seeds}


def is_primitive(gens, n):
    for x in range(1, n):
        if len(D4.min_block_partition([0, x], gens, n)) > 1:
            return False
    return True


def group_info(cells):
    """|G| and primitivity of the sheet monodromy (independent of the origin)."""
    m = model(cells, (0, 0))
    gens = tuple(tuple(g) for g in m["gens"])
    prim = is_primitive(gens, m["n"])
    order, method = D4.group_order(gens, m["n"], prim)
    return {"order": order, "order_method": method, "primitive": prim}


def class_report(cells, origin):
    """N_min data for the class of `origin` and separation for its interior points."""
    m = model(cells, origin)
    pts = sorted(p for p in lattice_points(cells) if cls(p, origin) == "A" and status(cells, p) == "interior")
    img = {p: m["image"](p) for p in pts}
    transparent = sorted(p for p in lattice_points(set(cells))
                         if cls(p, origin) != "A" and status(cells, p) in ("interior", "smooth"))
    sep = {}
    for i, p in enumerate(pts):
        for q in pts[i + 1:]:
            sep[(p, q)] = not (img[p] & img[q])
    return {"degree": len(m["bmin"]), "k": len(transparent), "transparent": transparent,
            "points": pts, "separated": sep}
