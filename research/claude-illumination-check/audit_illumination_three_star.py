"""Independent finite-domain fan audit of the unique three-star equality case.

No CP-SAT model, connectivity constraints, Euler equation, or wall formula is
used here. Seven partial cells each contain exactly one of their eight tiles.
"""
import itertools
import json
from pathlib import Path
from illumination_family_bound import NEIGHBORS, triangles_in_cells
from illumination_geometry import label, owners_of, check_fan_angles


def run():
    full = {(0, 0), (1, 0), (0, 1)}
    partial = sorted({(x+dx, y+dy) for x, y in full for dx, dy in NEIGHBORS}-full)
    fixed = triangles_in_cells(full)
    choices = [triangles_in_cells({p}) for p in partial]
    points = {p for t in fixed+sum(choices, []) for p in t}
    constraints = []
    for p in sorted(points):
        ids = [i for i, ts in enumerate(choices) if any(p in t for t in ts)]
        present = [t for t in fixed if p in t]
        allowed = []
        for values in itertools.product(range(8), repeat=len(ids)):
            ts = present+[choices[i][v] for i, v in zip(ids, values) if p in choices[i][v]]
            owners = owners_of(ts)
            opened = {e for e, os in owners.items() if len(os) == 2}
            angles, interior = check_fan_angles(ts, p, owners, opened)
            if len(angles) > 1:
                continue
            if label(p) != 'A' and (interior or 4 in angles) and p not in {(1, 0), (0, 1)}:
                continue
            allowed.append(values)
        constraints.append((ids, allowed))
    nodes = 0
    def search(assigned):
        nonlocal nodes
        nodes += 1
        for ids, allowed in constraints:
            if not any(all(i not in assigned or assigned[i] == value for i, value in zip(ids, row)) for row in allowed):
                return 0
        if len(assigned) == len(partial):
            return 1
        i = next(i for i in range(len(partial)) if i not in assigned)
        return sum(search(assigned | {i: v}) for v in range(8))
    solutions = search({})
    result = dict(status='PASS' if solutions == 0 else 'FEASIBLE', solutions=solutions,
                  partial_cells=partial, full_cells=sorted(full), local_constraints=len(constraints),
                  search_nodes=nodes, method='Independent fan tables and exhaustive singleton-cell CSP')
    Path(__file__).with_name('two-three-star-independent.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))

if __name__ == '__main__':
    run()
