#!/usr/bin/env python3
"""runs_poly.py -- run lines of a lattice polygon (orthogonal or 45-degree walls).
A horizontal lattice line y = c (strictly inside the room's y-range, c not the row of S or T)
carries a run iff no polygon vertex lies on it and every edge crossing it is vertical; then the
room meets the open strip c-1 < y < c+1 in a product (intervals) x (c-1, c+1), so the two cell
rows there are identical.  Columns likewise.  Also reports lines with no vertex at all."""
def runs(poly, S, T):
    out = {}
    for ax in (0, 1):
        o = 1 - ax
        vals = [p[o] for p in poly]
        skip = {S[o], T[o]}
        runl, novert = [], []
        for c in range(min(vals) + 1, max(vals)):
            if c in skip: continue
            if any(p[o] == c for p in poly): continue
            novert.append(c)
            ok = True
            for a, b in zip(poly, poly[1:] + poly[:1]):
                if (a[o] - c) * (b[o] - c) < 0 and a[ax] != b[ax]: ok = False
            if ok: runl.append(c)
        out["rows" if ax == 0 else "cols"] = (runl, novert)
    return out
