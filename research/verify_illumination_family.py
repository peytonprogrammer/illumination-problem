"""Independent fan formulation and LP/MIP check of the finite exclusion.

Uses fan angles rather than angular slots, one-hot fan variables rather than
CP-SAT tables, and GLOP/SCIP rather than CP-SAT. Connectivity is relaxed;
W - boundary_A_charge = 14 remains a necessary condition for the family.
"""
from fractions import Fraction
import json
from pathlib import Path
from ortools.linear_solver import pywraplp
from illumination_geometry import owners_of, check_fan_angles, label
from illumination_family_bound import support, triangles_in_cells, TARGETS_UNDER_24

BASE = Path(__file__).parent


def formulation(target, wall_budget=23, transparent_budget=0):
    bounded = support(target, wall_budget-14+2*transparent_budget)
    ts = triangles_in_cells(bounded['allowed'])
    points = sorted({p for t in ts for p in t})
    full = {(2*x, 2*y) for x, y in bounded['full']}
    costs, charge = [0]*len(ts), [0]*len(ts)
    credits, bads = [0]*len(ts), [0]*len(ts)
    equations = []
    vertex_rows = []
    for p in points:
        ids = [i for i, t in enumerate(ts) if p in t]
        rows = []
        for mask in range(1 << len(ids)):
            selected = [ts[i] for j, i in enumerate(ids) if mask >> j & 1]
            owners = owners_of(selected)
            opened = {e for e, os in owners.items() if len(os) == 2}
            angles, interior = check_fan_angles(selected, p, owners, opened)
            if len(angles) > 1 or (label(p) == 'A' and interior != (p in full)):
                continue
            bad = int(label(p) != 'A' and (interior or 4 in angles))
            if bad and not transparent_budget:
                continue
            w = int(bool(angles) and angles[0] != 4)
            q = 0
            if label(p) == 'A' and angles:
                q = 3 if angles[0] == 4 else angles[0]
            index = len(costs)
            costs.append(w)
            charge.append(q)
            bads.append(bad)
            credits.append((2 if interior else 1) if bad else 0)
            rows.append((index, mask))
        equations.append(({index: 1 for index, _ in rows}, 1))
        for bit, i in enumerate(ids):
            terms = {index: 1 for index, mask in rows if mask >> bit & 1}
            terms[i] = -1
            equations.append((terms, 0))
        vertex_rows.append((p, ids, rows))
    equations.append(({i: w-q+e for i, (w, q, e) in enumerate(zip(costs, charge, credits))
                       if w-q+e}, 14))
    if transparent_budget:
        equations.append(({i: v for i, v in enumerate(bads) if v}, transparent_budget))
    return dict(triangles=ts, costs=costs, charge=charge,
                equations=equations, vertex_rows=vertex_rows)


def exact_dual_bound(form, dual):
    """For Ax=b, 0<=x<=1: b*y + sum(min(0,c-A^T*y))."""
    reduced = list(map(Fraction, form['costs']))
    bound = Fraction(0)
    assert len(dual) == len(form['equations'])
    for (terms, rhs), weight in zip(form['equations'], dual):
        bound += rhs*weight
        for i, coefficient in terms.items():
            reduced[i] -= coefficient*weight
    return bound+sum(min(Fraction(0), value) for value in reduced)


def control_primal(form, room):
    selected = {tuple(sorted(map(tuple, t))) for t in room['triangles']}
    assert selected <= set(form['triangles'])
    values = [int(t in selected) for t in form['triangles']]
    values += [0]*(len(form['costs'])-len(values))
    for p, ids, rows in form['vertex_rows']:
        mask = sum(values[i] << j for j, i in enumerate(ids))
        matches = [index for index, bits in rows if bits == mask]
        assert len(matches) == 1, (p, mask)
        values[matches[0]] = 1
    for terms, rhs in form['equations']:
        assert sum(coefficient*values[i] for i, coefficient in terms.items()) == rhs
    return sum(c*v for c, v in zip(form['costs'], values))


def solve(target, integer=False, wall_budget=23, transparent_budget=0, exclusion_cap=None):
    form = formulation(target, wall_budget, transparent_budget)
    solver = pywraplp.Solver.CreateSolver('SCIP' if integer else 'GLOP')
    solver.SetTimeLimit(60000)
    # Binary triangle bits force every local fan weight to its unique matching
    # mask. Fan weights can therefore remain continuous without relaxing the
    # integer feasible geometry.
    variables = [solver.IntVar(0, 1, f'x{i}') if integer and i < len(form['triangles']) else solver.NumVar(0, 1, f'x{i}')
                 for i in range(len(form['costs']))]
    constraints = []
    for terms, rhs in form['equations']:
        constraint = solver.Constraint(rhs, rhs)
        for i, coefficient in terms.items():
            constraint.SetCoefficient(variables[i], coefficient)
        constraints.append(constraint)
    objective = solver.Objective()
    for i, coefficient in enumerate(form['costs']):
        if coefficient:
            objective.SetCoefficient(variables[i], coefficient)
    objective.SetMinimization()
    if exclusion_cap is not None:
        cap = solver.Constraint(-solver.infinity(), exclusion_cap)
        for i, coefficient in enumerate(form['costs']):
            if coefficient:
                cap.SetCoefficient(variables[i], coefficient)
    status = solver.Solve()
    names = {solver.OPTIMAL: 'OPTIMAL', solver.INFEASIBLE: 'INFEASIBLE',
             solver.FEASIBLE: 'FEASIBLE', solver.NOT_SOLVED: 'NOT_SOLVED',
             solver.ABNORMAL: 'ABNORMAL', solver.UNBOUNDED: 'UNBOUNDED'}
    result = dict(target_A_cell=target, engine=solver.SolverVersion(),
                  status=names.get(status, str(status)), integer=integer,
                  transparent_budget=transparent_budget,
                  exclusion_cap=exclusion_cap,
                  variables=len(variables), equations=len(constraints),
                  seconds=solver.WallTime()/1000)
    if exclusion_cap == 23 and status == solver.INFEASIBLE:
        result['excludes_integer_walls_under24'] = True
    if status == solver.OPTIMAL:
        result['objective'] = objective.Value()
        if integer:
            result['excludes_integer_walls_under24'] = objective.Value() > 23.5
        if not integer:
            dual = [Fraction(c.dual_value()).limit_denominator(1000000) for c in constraints]
            exact = exact_dual_bound(form, dual)
            result['exact_dual_bound'] = str(exact)
            result['excludes_integer_walls_under24'] = exact > 23
            if exact > 23:
                cert = dict(target_A_cell=target, dual=[str(v) for v in dual], bound=str(exact))
                path = BASE/f'family-exact-dual-{target[0]}-{target[1]}.json'
                path.write_text(json.dumps(cert, indent=2)+'\n')
    print(json.dumps(result), flush=True)
    return result


if __name__ == '__main__':
    results = []
    for target in TARGETS_UNDER_24:
        r = solve(target)
        results.append(r)
        if not r.get('excludes_integer_walls_under24'):
            results.append(solve(target, True))
    room = json.loads((BASE/'illumination-search-simple-unrestricted.json').read_text())
    assert control_primal(formulation((2, 0), 24), room) == 24
    summary = dict(status='EXCLUDED' if all(any(
        tuple(r['target_A_cell']) == target and r.get('excludes_integer_walls_under24')
        for r in results) for target in TARGETS_UNDER_24) else 'INCOMPLETE',
        results=results, known24_exact_primal_verified=True,
        note='LP bounds alone are insufficient; SCIP integer optima exclude <=23 in the bounded supports, not their higher objective values globally.')
    (BASE/'family-independent-summary.json').write_text(json.dumps(summary, indent=2)+'\n')
