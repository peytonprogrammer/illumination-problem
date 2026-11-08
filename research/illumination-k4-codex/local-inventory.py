"""Exact integer fan-inventory feasibility; no positions, rays, or room claims.

Build local patterns from the existing canonical triangle/fan helpers. Couple
their multiplicities by triangle incidences, Euler, and boundary-edge colors.
Every simple room induces one feasible inventory; the converse is not claimed.
"""
import argparse
import hashlib
import json
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sys.path.insert(0, str(BASE))
from ortools.sat.python import cp_model
from illumination_geometry import patch, label, owners_of, local_sectors


def local_rows():
    result = {}
    for kind, p in [('A', (0, 0)), ('B', (1, 1)), ('C', (1, 0))]:
        ts = sorted(t for t in patch(p[0]-2, p[0]+2, p[1]-2, p[1]+2) if p in t)
        expected = 4 if kind == 'C' else 8
        assert len(ts) == expected
        patterns = {}
        for mask in range(1, 1 << len(ts)):
            chosen = [t for i, t in enumerate(ts) if mask >> i & 1]
            own = owners_of(chosen)
            opened = {e for e, ids in own.items() if len(ids) == 2}
            sectors, full = local_sectors(chosen, p, opened)
            if not full and len(sectors) != 1:
                continue
            smooth = not full and sectors == [4]
            stubs = Counter(label(e[0] if e[1] == p else e[1])
                            for e, ids in own.items() if p in e and len(ids) == 1)
            assert sum(stubs.values()) == (0 if full else 2)
            row = dict(kind=kind, tiles=len(chosen), full=int(full), smooth=int(smooth),
                       corner=int(not full and not smooth),
                       charge=(0 if full else 3 if smooth else sectors[0]) if kind == 'A' else 0,
                       stubs={k: stubs[k] for k in 'ABC'})
            key = json.dumps(row, sort_keys=True)
            patterns.setdefault(key, dict(row, representative_mask=mask))
        result[kind] = list(patterns.values())
        assert sum(r['full'] for r in result[kind]) == 1
    return result


def physical_inventory(room, rows):
    """Control from a saved physical room, with an independent fan-angle check."""
    from illumination_geometry import check, check_fan_angles
    geometry = check(room, strict=False)
    assert geometry['simple_polygon']
    ts = [tuple(sorted(map(tuple, t))) for t in room['triangles']]
    own = owners_of(ts)
    opened = {e for e, ids in own.items() if len(ids) == 2}
    counts = {kind: [0]*len(rows[kind]) for kind in 'ABC'}
    for p in {p for t in ts for p in t}:
        sectors, full = local_sectors(ts, p, opened)
        other_sectors, other_full = check_fan_angles(ts, p, own, opened)
        assert (sorted(sectors), full) == (sorted(other_sectors), other_full)
        smooth = not full and sectors == [4]
        kind = label(p)
        stubs = Counter(label(e[0] if e[1] == p else e[1])
                        for e, ids in own.items() if p in e and len(ids) == 1)
        values = dict(kind=kind, tiles=sum(p in t for t in ts), full=int(full),
                      smooth=int(smooth), corner=int(not full and not smooth),
                      charge=(0 if full else 3 if smooth else sectors[0]) if kind == 'A' else 0,
                      stubs={c: stubs[c] for c in 'ABC'})
        matching = [j for j, r in enumerate(rows[kind])
                    if all(r[key] == value for key, value in values.items())]
        assert len(matching) == 1
        counts[kind][matching[0]] += 1
    def total(kind, field):
        return sum(c*r[field] for c, r in zip(counts[kind], rows[kind]))
    values = (total('A', 'full'), total('B', 'full')+total('C', 'full'),
              total('B', 'smooth')+total('C', 'smooth'), total('A', 'charge'), len(ts))
    return values, counts, geometry


def model_for(k, rows, tuples):
    m = cp_model.CpModel()
    nmax = 4*(21+2*k)//3
    variables = {}
    for kind, patterns in rows.items():
        variables[kind] = [m.new_int_var(0, nmax+2, f'{kind}{j}') for j in range(len(patterns))]

    def total(kind, field):
        return sum(v*r[field] for v, r in zip(variables[kind], rows[kind]))

    I = m.new_int_var(2, (17+2*k)//6, 'I')
    J = m.new_int_var(0, k, 'J')
    sn = m.new_int_var(0, k, 's_N')
    Q = m.new_int_var(0, 9+2*k, 'Q')
    N = m.new_int_var(1, nmax, 'N')
    W = m.new_int_var(3, 23, 'W')
    sa = total('A', 'smooth')
    m.add(I == total('A', 'full'))
    m.add(J == total('B', 'full')+total('C', 'full'))
    m.add(sn == total('B', 'smooth')+total('C', 'smooth'))
    m.add(J+sn == k)
    m.add(Q == total('A', 'charge'))
    for kind in 'ABC':
        m.add(N == total(kind, 'tiles'))
    m.add(W == sum(total(kind, 'corner') for kind in 'ABC'))
    m.add(W == 2+6*I+Q-2*J-sn)
    m.add(N == 8*I+Q+sa)
    boundary_vertices = sum(sum(variables[kind])-total(kind, 'full') for kind in 'ABC')
    m.add(N == 2*(I+J)+boundary_vertices-2)
    m.add(N >= W+6)
    for a, b in [('A', 'B'), ('A', 'C'), ('B', 'C')]:
        from_a = sum(v*r['stubs'][b] for v, r in zip(variables[a], rows[a]))
        from_b = sum(v*r['stubs'][a] for v, r in zip(variables[b], rows[b]))
        m.add(from_a == from_b)
        interior_edges = m.new_int_var(0, nmax, 'interior_'+a+b)
        m.add(N-from_a == 2*interior_edges)
    projection = [I, J, sn, Q, N]
    m.add_allowed_assignments(projection, tuples)
    return m, projection, variables


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seconds', type=float, default=2)
    ap.add_argument('--max-k', type=int, default=12)
    args = ap.parse_args()
    assert args.max_k >= 4
    start = time.monotonic()
    budget_path = BASE/'illumination-new-mechanisms/exception-budget.json'
    budgets = json.loads(budget_path.read_text())
    rows = local_rows()
    result = dict(status='RUNNING', scope='Exact local fan-inventory feasibility only; not embedded polygon feasibility or darkness.',
                  local_rows=rows, tables=[], controls=[], inputs_sha256={})
    for p in [Path(__file__), budget_path, BASE/'illumination_geometry.py']:
        result['inputs_sha256'][str(p.relative_to(BASE))] = hashlib.sha256(p.read_bytes()).hexdigest()

    def save():
        result['seconds'] = time.monotonic()-start
        p = HERE/'table.json'
        tmp = p.with_suffix('.tmp')
        tmp.write_text(json.dumps(result, indent=2)+'\n')
        tmp.replace(p)

    save()
    saved = json.loads((BASE/'three-triples/peer-2-0-control.json').read_text())['room']
    rectangle = dict(triangles=patch(0, 4, 0, 6), marked=[[2, 2], [2, 4]], slits=[])
    for name, room in [('saved_peer_control', saved), ('rectangle_k23', rectangle)]:
        values, counts, geometry = physical_inventory(room, rows)
        control_model, _, variables = model_for(values[1]+values[2], rows, [values])
        for kind in 'ABC':
            for v, c in zip(variables[kind], counts[kind]):
                control_model.add(v == c)
        solver = cp_model.CpSolver()
        status = solver.solve(control_model)
        assert status in (cp_model.FEASIBLE, cp_model.OPTIMAL), name
        result['controls'].append(dict(name=name, values=values, walls=geometry['walls'],
                                       status=solver.status_name(status)))
    save()
    print(json.dumps(dict(event='physical_controls_pass', controls=result['controls'])), flush=True)
    for k in range(4, args.max_k+1):
        candidates = set()
        for i in range(2, (17+2*k)//6+1):
            bmin = {2: 6, 3: 7, 4: 8}.get(i, 4)
            for j in range(k+1):
                sn = k-j
                for w in range(3, 24):
                    q = w-2-6*i+2*j+sn
                    if q < max(0, bmin-sn):
                        continue
                    for sa in range(q//3+1):
                        n = 8*i+q+sa
                        assert n >= w+6
                        candidates.add((i, j, sn, q, n))
        if k <= 6:
            previous = {(r['I'], r['J'], r['s_N'], v['Q'], v['N'])
                        for r in budgets['budgets'] if r['k'] == k
                        for v in r.get('tuples', [])}
            assert candidates == previous
        candidates = sorted(candidates)
        model, projection, variables = model_for(k, rows, candidates)
        table = dict(k=k, arithmetic_candidates=len(candidates), cells=[])
        result['tables'].append(table)
        for index, values in enumerate(candidates):
            model.clear_assumptions()
            # A fresh clone keeps each query independent while preserving the fixed inventory model.
            query = model.clone()
            for var, value in zip(projection, values):
                query.add(query.get_int_var_from_proto_index(var.index) == value)
            solver = cp_model.CpSolver()
            solver.parameters.num_search_workers = 1
            solver.parameters.max_time_in_seconds = args.seconds
            status = solver.solve(query)
            cell = dict(zip(('I', 'J', 's_N', 'Q', 'N'), values))
            cell['W'] = 2+6*values[0]+values[3]-2*values[1]-values[2]
            cell['status'] = solver.status_name(status)
            if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
                cell['inventory'] = {kind: [int(solver.value(query.get_int_var_from_proto_index(v.index)))
                                           for v in variables[kind]] for kind in 'ABC'}
                # Evaluate all physical inventory equations from the extracted integer witness.
                counts = cell['inventory']
                def total(kind, field):
                    return sum(c*r[field] for c, r in zip(counts[kind], rows[kind]))
                assert all(total(kind, 'tiles') == cell['N'] for kind in 'ABC')
                assert sum(total(kind, 'corner') for kind in 'ABC') == cell['W']
                assert total('A', 'full') == cell['I']
                assert total('B', 'full')+total('C', 'full') == cell['J']
                assert total('B', 'smooth')+total('C', 'smooth') == cell['s_N']
                assert total('A', 'charge') == cell['Q']
                for a, b in [('A', 'B'), ('A', 'C'), ('B', 'C')]:
                    ea = sum(c*r['stubs'][b] for c, r in zip(counts[a], rows[a]))
                    eb = sum(c*r['stubs'][a] for c, r in zip(counts[b], rows[b]))
                    assert ea == eb and 0 <= ea <= cell['N'] and (cell['N']-ea)%2 == 0
                interior = cell['I']+cell['J']
                boundary = sum(sum(counts[t])-total(t, 'full') for t in 'ABC')
                assert cell['N'] == 2*interior+boundary-2
            table['cells'].append(cell)
            if (index+1)%100 == 0:
                save()
                print(json.dumps(dict(k=k, done=index+1, total=len(candidates),
                                      statuses=dict(Counter(c['status'] for c in table['cells'])))), flush=True)
        table['statuses'] = dict(Counter(c['status'] for c in table['cells']))
        save()
        print(json.dumps(dict(k=k, done=len(candidates), statuses=table['statuses'])), flush=True)
    result['status'] = 'COMPLETE' if all(c['status'] != 'UNKNOWN' for t in result['tables'] for c in t['cells']) else 'INCOMPLETE'
    save()


if __name__ == '__main__':
    main()
