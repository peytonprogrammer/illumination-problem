"""Finite support bounds for strict simple canonical 45-degree rooms.

All A coordinates here are divided by two (cell centers form Z^2).
Every triangle belongs to the unique A-centered square cell containing it.
"""
from illumination_geometry import label, owners_of, check_fan_angles, check, patch

NEIGHBORS = ((1, 0), (-1, 0), (0, 1), (0, -1))
TARGETS_UNDER_24 = ((1, 1), (2, 0), (2, 1), (3, 0),
                    (2, 2), (3, 1), (4, 0))


def mandatory_cells(target):
    full = {(0, 0), tuple(target)}
    required = full | {(x+dx, y+dy) for x, y in full for dx, dy in NEIGHBORS}
    assert not any((x+dx, y+dy) in full for x, y in full for dx, dy in NEIGHBORS)
    return full, required


def support(target, partial_budget=9):
    full, required = mandatory_cells(target)
    partial_required = len(required-full)
    extra_budget = partial_budget-partial_required
    assert extra_budget >= 0
    allowed = set(required)
    for _ in range(extra_budget):
        allowed |= {(x+dx, y+dy) for x, y in allowed for dx, dy in NEIGHBORS}
    return dict(full=full, mandatory=required, allowed=allowed,
                partial_required=partial_required, extra_budget=extra_budget)


def triangles_in_cells(cells):
    return sorted({t for x, y in cells for t in patch(2*x-1, 2*x+1, 2*y-1, 2*y+1)})


def counts(data):
    """Independent geometric check of the identities used in the bound."""
    result = check(data)
    assert result['simple_polygon']
    ts = [tuple(map(tuple, t)) for t in data['triangles']]
    owners = owners_of(ts)
    opens = {e for e, o in owners.items() if len(o) == 2}
    vertices = {p for t in ts for p in t}
    full, smooth, charge, used = [], [], 0, set()
    for p in sorted(vertices):
        if label(p) != 'A':
            continue
        used.add((p[0]//2, p[1]//2))
        angles, interior = check_fan_angles(ts, p, owners, opens)
        if interior:
            full.append(p)
        else:
            assert len(angles) == 1
            k = angles[0]
            if k == 4:
                smooth.append(p)
                charge += 3
            else:
                charge += k
    W, N, I, a4 = result['walls'], len(ts), len(full), len(smooth)
    assert W == 2+6*I+charge
    assert N == 2*I+a4+W-2
    assert N <= (4*(W-2))//3
    assert I <= (W-6)//6
    # Each full A forces all four adjacent A cells to be nonempty and nonfull.
    interior = {(x//2, y//2) for x, y in full}
    for x, y in interior:
        for dx, dy in NEIGHBORS:
            q = (x+dx, y+dy)
            assert q in used and q not in interior
    return dict(walls=W, triangles=N, interior_A=I, smooth_boundary_A=a4,
                boundary_A_charge=charge, used_A_cells=len(used))
