"""Complete support constants and equality patterns for two B/C exceptions."""
from itertools import combinations
from illumination_family_bound import NEIGHBORS, support, triangles_in_cells
from illumination_transparent_bound import counts
from illumination_cover import D4, mat

TARGETS = tuple((x, d-x) for d in range(2, 5) for x in range((d+1)//2, d+1))


def canonical(cells):
    variants = []
    for g in D4:
        transformed = [mat(g, p) for p in cells]
        for origin in transformed:
            variants.append(tuple(sorted((p[0]-origin[0], p[1]-origin[1]) for p in transformed)))
    return min(variants)


def equality_patterns():
    diamond = [(x, y) for x in range(-4, 5) for y in range(-4, 5)
               if 0 < abs(x)+abs(y) <= 4]
    patterns = set()
    checked = 0
    for a, b in combinations(diamond, 2):
        full = {(0, 0), a, b}
        seen, todo = {(0, 0)}, [(0, 0)]
        for p in todo:
            for q in full-seen:
                if sum(abs(p[k]-q[k]) for k in (0, 1)) <= 2:
                    seen.add(q); todo.append(q)
        if seen != full:
            continue
        boundary = {(x+dx, y+dy) for x, y in full for dx, dy in NEIGHBORS}-full
        assert len(boundary) >= 7
        if len(boundary) == 7:
            patterns.add(canonical(full))
        checked += 1
    return dict(checked=checked, patterns=sorted(patterns))


def validate_counts(room):
    c = counts(room)
    assert c['interior_nonA']+c['smooth_boundary_nonA'] == 2
    assert c['walls'] <= 23 and c['triangles'] <= 33
    assert c['used_A_cells'] <= 15
    assert c['interior_A'] in (2, 3)
    if c['interior_A'] == 2:
        from illumination_cover import D4, mat
        source, target = map(tuple, room['marked'])
        delta = tuple(target[k]-source[k] for k in (0, 1))
        norm = tuple(sorted(map(abs, delta), reverse=True))
        normalized = tuple(v//2 for v in norm)
        assert sum(normalized) <= 4
        g = next(g for g in D4 if mat(g, delta) == norm)
        cells = {tuple(v//2 for v in mat(g, (p[0]-source[0], p[1]-source[1])))
                 for t in room['triangles'] for p in map(tuple, t) if p[0]%2 == p[1]%2 == 0}
        assert len(cells)-2 <= 9
        if sum(normalized) >= 2:
            bounded = complete_support(normalized)
            missing = len(bounded['mandatory']-cells)
            assert len(cells)-2+missing <= 9
            assert cells <= bounded['allowed']
        c['normalized_A_cell_target'] = normalized
    return c


def complete_support(target):
    """Q >= sum partial graph degrees >= 2P-6+m implies P+m <= 9."""
    assert tuple(target) in TARGETS
    return support(target, 9)


def degree_lemma():
    from illumination_geometry import local_sectors, owners_of
    ts = triangles_in_cells({(0, 0)})
    checked = 0
    for mask in range(1, 255):
        selected = [t for i, t in enumerate(ts) if mask >> i & 1]
        owners = owners_of(selected)
        opened = {e for e, os in owners.items() if len(os) == 2}
        sizes, full = local_sectors(selected, (0, 0), opened)
        if len(sizes) != 1:
            continue
        charge = 3 if sizes[0] == 4 else sizes[0]
        sides = {(axis, value) for t in selected for axis in (0, 1) for value in (-1, 1)
                 if sum(p[axis] == value for p in t) == 2}
        assert charge >= len(sides)
        checked += 1
    return dict(partial_fan_masks_checked=checked, maximum_partial_cells=9,
                maximum_partial_plus_missing=9, maximum_mark_distance=4,
                target_cases=len(TARGETS))


def audit_cell_graph(room):
    """Recompute the degree inequalities from actual shared tile edges."""
    from illumination_geometry import owners_of, label
    c = validate_counts(room)
    assert c['interior_A'] == 2
    ts = [tuple(map(tuple, t)) for t in room['triangles']]
    centers = [next(p for p in t if label(p) == 'A') for t in ts]
    cells = set(centers)
    links = {tuple(sorted((centers[ids[0]], centers[ids[1]])))
             for ids in owners_of(ts).values()
             if len(ids) == 2 and centers[ids[0]] != centers[ids[1]]}
    full = set(map(tuple, room['marked']))
    required = {(x+2*dx, y+2*dy) for x, y in full for dx, dy in NEIGHBORS}-full
    missing = len(required-cells)
    degrees = {p: sum(p in edge for edge in links) for p in cells}
    seen = {next(iter(cells))}
    while True:
        added = {q for edge in links if any(p in seen for p in edge) for q in edge}-seen
        if not added:
            break
        seen |= added
    assert seen == cells
    assert len(links) >= len(cells)-1
    assert sum(degrees[p] for p in full) <= 8-missing
    partial_degrees = sum(degrees[p] for p in cells-full)
    assert c['charge'] >= partial_degrees >= 2*(len(cells)-2)-6+missing
    assert len(cells)-2+missing <= 9
    return dict(cells=len(cells), edges=len(links), missing=missing,
                charge=c['charge'], partial_degree_sum=partial_degrees)
