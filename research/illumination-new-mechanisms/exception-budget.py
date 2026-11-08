"""Necessary exception budgets; no rays, room solver, or orbit search.

Full A cells form a finite subset F of Z². Its external vertex boundary is
the four-neighbor set minus F. Components in the distance-at-most-two graph
have disjoint external boundaries, so connected shapes and integer partitions
give the exact minimum boundary for |F| <= 4, with no coordinate window.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIDES = ((1, 0), (-1, 0), (0, 1), (0, -1))
OVERLAP = tuple((x, y) for x in range(-2, 3) for y in range(-2, 3)
                if 0 < abs(x) + abs(y) <= 2)


def normalize(points):
    points = set(points)
    ax, ay = min(points)
    return tuple(sorted((x-ax, y-ay) for x, y in points))


def boundary(shape):
    return {(x+dx, y+dy) for x, y in shape for dx, dy in SIDES} - set(shape)


def main():
    shapes = {((0, 0),)}
    connected_min = {}
    all_min = {0: 0}
    certificates = []
    for size in range(1, 5):
        connected_min[size] = min(len(boundary(s)) for s in shapes)
        all_min[size] = min(connected_min[j] + all_min[size-j]
                            for j in range(1, size+1))
        witness = next(s for s in sorted(shapes)
                       if len(boundary(s)) == connected_min[size])
        certificates.append(dict(full_cells=size, overlap_connected_shapes=len(shapes),
                                 connected_min=connected_min[size],
                                 arbitrary_set_min=all_min[size], witness=witness))
        if size < 4:
            shapes = {normalize((*s, (x+dx, y+dy))) for s in shapes
                      for x, y in s for dx, dy in OVERLAP
                      if (x+dx, y+dy) not in s}

    # Universal Q >= 4-s_N yields I <= floor((17+2k)/6) at W<=23.
    # For k=4,5,6 this is at most four, covered by the exact boundary minima.
    rows = []
    for k in (4, 5, 6):
        imax = (17+2*k)//6
        assert imax <= 4
        for interior_a in range(2, imax+1):
            for interior_bc in range(k+1):
                smooth_bc = k-interior_bc
                credit = 2*interior_bc+smooth_bc
                values = []
                for walls in range(3, 24):
                    charge = walls-2-6*interior_a+credit
                    if charge < max(0, all_min[interior_a]-smooth_bc):
                        continue
                    for smooth_a in range(charge//3+1):
                        triangles = 8*interior_a+charge+smooth_a
                        regular = 8*interior_a+4*smooth_a+8*interior_bc+4*smooth_bc
                        assert regular == 4*(triangles-walls+2)
                        values.append(dict(W=walls, Q=charge, s_A=smooth_a,
                                           N=triangles, R=regular))
                row = dict(k=k, I=interior_a, J=interior_bc, s_N=smooth_bc,
                           universal_wall_lower=2+6*interior_a+all_min[interior_a]-2*k,
                           necessary_tuple_count=len(values),
                           status='arithmetic_survivor' if values else 'excluded_by_necessary_bounds')
                if values:
                    row['ranges'] = {name: [min(v[name] for v in values),
                                            max(v[name] for v in values)]
                                     for name in ('W', 'Q', 's_A', 'N', 'R')}
                    row['tuples'] = values
                rows.append(row)
    result = dict(scope='Necessary arithmetic bounds only; not per-vertex or polygon feasibility, illumination, or darkness.',
                  completeness='All finite full-cell sets of size <=4 via overlap components; exact k=4,5,6 budget relaxations at W<=23.',
                  full_cell_boundary_certificates=certificates, budgets=rows)
    (HERE/'exception-budget.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(boundary_minima=all_min, shape_counts=[c['overlap_connected_shapes'] for c in certificates],
                          surviving_I={k: sorted({r['I'] for r in rows if r['k']==k and r['necessary_tuple_count']})
                                       for k in (4, 5, 6)}), indent=2))


if __name__ == '__main__':
    main()
