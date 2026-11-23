"""Two independent exact checks of a lit witness S -> T with developing vector D.

check 1: tracer.certify, a room-level billiard tracer (reflections, Fractions).
check 2: ref/surface.py (d3-review's independent unfolding) Surface.segment for
         non-axis vectors; for axis-parallel vectors, a walk along the
         horizontal or vertical unit edges of the same independent unfolding.
A witness is accepted only when both checks pass for the same signed vector.
"""
import os
import sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "ref"))
import surface as SF  # noqa: E402

from tracer import certify as trace_certify  # noqa: E402


def axis_walk(cells, S, T, D):
    """Walk along unit edges of d3-review's unfolding (Surface.r / Surface.u)."""
    surf = SF.Surface(cells)
    DX, DY = D
    n = len(surf.sq)
    if DY == 0:
        perm = surf.r if DX > 0 else surf.ri
        steps = abs(DX)
    else:
        perm = surf.u if DY > 0 else surf.ui
        steps = abs(DY)
    for k in range(n):
        if surf.corner_room_point(k, 0, 0) != S:
            continue
        cur, ok = k, True
        for _ in range(steps):
            cur = perm[cur]
            if SF.point_type(cells, *surf.corner_room_point(cur, 0, 0)) in ("convex", "reflex"):
                ok = False
                break
        if ok and surf.corner_room_point(cur, 0, 0) == T:
            return True
    return False


def second_check(cells, S, T, Ds):
    if Ds[0] == 0 or Ds[1] == 0:
        return axis_walk(cells, S, T, Ds)
    surf = SF.Surface(cells)
    rp, ok, _ = surf.segment((Fr(S[0]), Fr(S[1])), Ds)
    return ok and rp == (Fr(T[0]), Fr(T[1]))


def certify(cells, S, T, D):
    """Return the signed vector certified by both checks, or None."""
    cells = set(cells)
    Ds = trace_certify(cells, S, T, D)
    if Ds is None:
        return None
    return Ds if second_check(cells, S, T, Ds) else None
