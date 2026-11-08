"""Counts and complete support reduction for exactly one B/C exception."""
from illumination_geometry import check, owners_of, check_fan_angles, label
from illumination_cover import D4, mat
from illumination_family_bound import support

TARGETS = tuple((x, y) for d in range(2, 7) for x in range((d+1)//2, d+1)
                if (y := d-x) <= x)


def counts(data):
    geometry = check(data, strict=False)
    assert geometry['simple_polygon']
    ts = [tuple(map(tuple, t)) for t in data['triangles']]
    owners = owners_of(ts)
    opens = {e for e, os in owners.items() if len(os) == 2}
    I = J = sA = sN = K = 0
    used_A = set()
    for p in {p for t in ts for p in t}:
        angles, full = check_fan_angles(ts, p, owners, opens)
        if label(p) == 'A':
            used_A.add(p)
            if full:
                I += 1
            elif angles == [4]:
                sA += 1
            else:
                assert len(angles) == 1
                K += angles[0]
        elif full:
            J += 1
        elif angles == [4]:
            sN += 1
    Q, E, W = 3*sA+K, 2*J+sN, geometry['walls']
    assert W == 2+6*I+Q-E
    assert len(ts) <= 4*(W-2+E)//3
    result = dict(walls=W, interior_A=I, interior_nonA=J,
                  smooth_boundary_nonA=sN, charge=Q, defect_credit=E,
                  triangles=len(ts), used_A_cells=len(used_A))
    if W <= 23 and J+sN == 1:
        assert I == 2 and Q <= 9+E and len(ts) <= 30
        source, target = map(tuple, data['marked'])
        displacement = tuple(target[k]-source[k] for k in (0, 1))
        normalized = tuple(sorted(map(abs, displacement), reverse=True))
        t = tuple(v//2 for v in normalized)
        assert sum(t) <= 6
        g = next(g for g in D4 if mat(g, displacement) == normalized)
        cells = {tuple(v//2 for v in mat(g, (p[0]-source[0], p[1]-source[1])))
                 for p in used_A}
        if sum(t) == 1:
            result['forced_direct_illumination'] = True
        else:
            assert cells <= support(t, 11)['allowed']
        result['normalized_A_cell_target'] = t
    return result


def three_vertex_boundary_check():
    """Check the small grid lemma used to exclude I=3.

    A disconnected distance-2 overlap graph has >=4+6=10 external neighbors.
    If connected, all three points are within distance four of one root.
    """
    from itertools import combinations
    from illumination_family_bound import NEIGHBORS
    diamond = [(x, y) for x in range(-4, 5) for y in range(-4, 5)
               if abs(x)+abs(y) <= 4 and (x, y) != (0, 0)]
    minimum, checked = 99, 0
    for a, b in combinations(diamond, 2):
        full = {(0, 0), a, b}
        seen, todo = {(0, 0)}, [(0, 0)]
        for p in todo:
            for q in full-seen:
                if sum(abs(p[k]-q[k]) for k in (0, 1)) <= 2:
                    seen.add(q)
                    todo.append(q)
        if seen != full:
            continue
        boundary = {(x+dx, y+dy) for x, y in full for dx, dy in NEIGHBORS}-full
        minimum = min(minimum, len(boundary))
        assert len(boundary) >= 7
        checked += 1
    return dict(connected_triples_checked=checked, minimum_external_neighbors=minimum)
