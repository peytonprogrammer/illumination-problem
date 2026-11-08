"""Audit local equivalence, support reduction, controls, and both exclusions."""
import itertools
import json
from pathlib import Path
from illumination_geometry import (patch, owners_of, local_sectors,
                                   check_fan_angles, check)
from illumination_cover import D4, mat
from illumination_family_bound import (counts, mandatory_cells, support,
                                       NEIGHBORS, TARGETS_UNDER_24)
from verify_illumination_family import formulation, control_primal
from search_illumination_family import build_model
from ortools.sat.python import cp_model

BASE = Path(__file__).parent


def connected(cells):
    first = min(cells)
    seen, todo = {first}, [first]
    for x, y in todo:
        for dx, dy in NEIGHBORS:
            p = x+dx, y+dy
            if p in cells and p not in seen:
                seen.add(p)
                todo.append(p)
    return seen == set(cells)


def normalize_target(p):
    return tuple(sorted(map(abs, p), reverse=True))


def support_audit():
    checked = 0
    observed_targets = set()
    # Enumerate every attachment of the remaining <=3 A cells to the mandatory
    # cells for all symmetry representatives through Manhattan separation 8.
    # Any final connected graph has a breadth-first attachment order of this form.
    for x in range(1, 9):
        for y in range(x+1):
            if not 2 <= x+y <= 8:
                continue
            full, required = mandatory_cells((x, y))
            extra = 9-len(required-full)
            levels = {frozenset(required)}
            for depth in range(extra+1):
                for cells in levels:
                    if not connected(cells):
                        continue
                    checked += 1
                    assert x+y <= 4
                    observed_targets.add((x, y))
                    assert cells <= support((x, y))['allowed']
                if depth < extra:
                    levels = {cells | {p} for cells in levels for a, b in cells
                              for dx, dy in NEIGHBORS
                              if (p := (a+dx, b+dy)) not in cells}
    assert observed_targets == set(TARGETS_UNDER_24)
    return checked


def main():
    legal = patch(-2, 4, -2, 4)
    local_checks = 0
    for p in [(0, 0), (1, 1), (1, 0)]:
        incident = [t for t in legal if p in t]
        for bits in itertools.product((0, 1), repeat=len(incident)):
            selected = [t for t, bit in zip(incident, bits) if bit]
            owners = owners_of(selected)
            opened = {e for e, os in owners.items() if len(os) == 2}
            angular, full = local_sectors(selected, p, opened)
            fans, interior = check_fan_angles(selected, p, owners, opened)
            assert (sorted(angular), full) == (fans, interior)
            local_checks += 1
    room = json.loads((BASE/'illumination-search-simple-unrestricted.json').read_text())
    original_counts = counts(room)
    assert original_counts['walls'] == 24
    assert original_counts['boundary_A_charge'] == 10
    transforms = 0
    for g in D4:
        for swap in (False, True):
            def transform(p):
                x, y = mat(g, p)
                return x+12, y-8
            changed = dict(triangles=[tuple(map(transform, t)) for t in room['triangles']],
                           marked=list(map(transform, room['marked'])), require_simple=True)
            if swap:
                changed['marked'].reverse()
            assert counts(changed) == original_counts
            assert check(changed)['simple_polygon']
            transforms += 1
    model, ts, variables, _, _ = build_model((2, 0), 24)
    chosen = {tuple(sorted(map(tuple, t))) for t in room['triangles']}
    for t, variable in zip(ts, variables):
        model.add(variable == int(t in chosen))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10
    assert solver.solve(model) == cp_model.OPTIMAL
    assert control_primal(formulation((2, 0), 24), room) == 24
    cp = json.loads((BASE/'family-under24-summary.json').read_text())
    other = json.loads((BASE/'family-independent-summary.json').read_text())
    assert cp['status'] == other['status'] == 'EXCLUDED'
    assert {tuple(r['target_A_cell']) for r in cp['cases']} == set(TARGETS_UNDER_24)
    assert all(r['status'] == 'INFEASIBLE' and r['max_walls'] == 23 for r in cp['cases'])
    for target in TARGETS_UNDER_24:
        result = next(r for r in other['results'] if tuple(r['target_A_cell']) == target
                      and r['integer'])
        assert result['status'] == 'OPTIMAL' and result['objective'] >= 24
    checked = support_audit()
    result = dict(status='PASS', local_masks_checked=local_checks,
                  connected_A_cell_supports_checked=checked,
                  transformed_24_wall_controls=transforms,
                  cp_fixed_24_wall_control='PASS', exact_one_hot_primal_control='PASS',
                  cp_infeasible_cases=7, independent_scip_exclusions=7,
                  scope='Family-wide computer-assisted exclusion, not general polygon optimality or a formal UNSAT proof.')
    (BASE/'family-final-audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
