"""Check stored balances in original length coordinates, with no chart code or LP."""
from pathlib import Path
from fractions import Fraction as F
import json
import math

ROOT = Path(__file__).resolve().parent
INP = ROOT / 'inputs/holdouts'


def rank(rows):
    basis = {}
    for row in rows:
        row = list(map(F, row))
        for pivot, b in sorted(basis.items()):
            if row[pivot]:
                x = row[pivot]
                row = [u-x*v for u, v in zip(row, b)]
        p = next((i for i, v in enumerate(row) if v), None)
        if p is not None:
            x = row[p]
            basis[p] = [v/x for v in row]
    return len(basis)


def check_balance(rows, indices, weights, closure):
    weights = list(map(F, weights))
    assert len(indices) == len(set(indices)) == len(weights)
    assert all(w > 0 for w in weights)
    residual = [sum(w*rows[i][c] for i, w in zip(indices, weights)) for c in range(len(rows[0]))]
    # Closure equations have independent x/y tangents; solve their two coefficients.
    a = next(i for i, v in enumerate(closure[0]) if v)
    b = next(i for i, v in enumerate(closure[1])
             if closure[0][a]*v != closure[0][i]*closure[1][a])
    det = closure[0][a]*closure[1][b]-closure[0][b]*closure[1][a]
    x = (residual[a]*closure[1][b]-residual[b]*closure[1][a])/det
    y = (closure[0][a]*residual[b]-closure[0][b]*residual[a])/det
    assert residual == [x*u+y*v for u, v in zip(*closure)]
    return rank([rows[i] for i in indices] + closure)-2


def main():
    repairs = json.loads((ROOT / 'repair-structure.json').read_text())['cases']
    cones = {r['tag']: r for r in json.loads((ROOT / 'ear-family.json').read_text())['cases']}
    checks = []
    for record in repairs:
        tag = record['tag']
        room = json.loads((INP / (tag+'.json')).read_text())
        rows = [list(map(F, r)) for r in json.loads((INP / ('funcs-'+tag+'-R12.json')).read_text())['funcs']]
        events = json.loads((INP / ('events-'+tag+'-R12.json')).read_text())['rows']
        assert len(rows) == len(events)
        v = room['vertices']
        W = len(v)
        dirs = []
        for a, b in zip(v, v[1:]+v[:1]):
            x, y = b[0]-a[0], b[1]-a[1]
            length = math.gcd(abs(x), abs(y))
            dirs.append((x//length, y//length))
        closure = [[F(0), F(0)] + [F(d[a]) for d in dirs] + [F(0)]*4 for a in (0, 1)]
        base_lengths = []
        for i, d in enumerate(dirs):
            edge = [v[(i+1)%W][k]-v[i][k] for k in (0, 1)]
            base_lengths.append(F(sum(d[k]*edge[k] for k in (0, 1)), sum(x*x for x in d)))
        tx = [F(1), F(0)]+[F(0)]*W+[F(1), F(0), F(1), F(0)]
        ty = [F(0), F(1)]+[F(0)]*W+[F(0), F(1), F(0), F(1)]
        scale = list(map(F, v[0]))+base_lengths+[F(x) for p in room['marked'] for x in p]
        assert rank([tx, ty, scale]) == 3
        assert all(sum(x*y for x, y in zip(row, sym)) == 0 for row in rows for sym in (tx, ty, scale))
        assert all(sum(x*y for x, y in zip(c, sym)) == 0 for c in closure for sym in (tx, ty, scale))
        cert = record['single_diagonal_exact_certificate']
        assert cert is not None
        axis = [i for i, e in enumerate(events) if any(sorted(abs(e['corner'][k]-p[k]) for k in (0, 1)) == [0, 1] for p in room['marked'])]
        assert cert['indices'][:-1] == axis
        assert cert['indices'][-1] == cert['index']
        corner = events[cert['index']]['corner']
        assert corner == cert['corner']
        assert any(sorted(abs(corner[k]-p[k]) for k in (0, 1)) == [1, 1] for p in room['marked'])
        r = check_balance(rows, cert['indices'], cert['weights'], closure)
        assert r == W+1 == cert['rank']
        cone = cones[tag]
        Z = cone['forced_zero_rows']
        if Z:
            zero_rank = check_balance(rows, Z, cone['exact_positive_stress'], closure)
        else:
            assert cone['exact_positive_stress'] == []
            zero_rank = 0
        assert zero_rank == cone['forced_zero_rank']
        assert W+1-zero_rank == cone['cone_dimension_mod_symmetries']
        # Independently map the stored deformation to physical vertex velocities,
        # then to the original length chart. Check relative interior exactly.
        h = list(map(F, cone['exact_relative_interior_direction']))
        normals = [(-d[1], d[0]) for d in dirs]
        velocity = []
        for i in range(W):
            a, b = normals[(i-1)%W], normals[i]
            det = a[0]*b[1]-a[1]*b[0]
            velocity.append(((h[(i-1)%W]*b[1]-a[1]*h[i])/det,
                             (a[0]*h[i]-h[(i-1)%W]*b[0])/det))
        lengths = []
        for i, d in enumerate(dirs):
            diff = [velocity[(i+1)%W][k]-velocity[i][k] for k in (0, 1)]
            value = sum(d[k]*diff[k] for k in (0, 1))/sum(x*x for x in d)
            assert diff == [value*x for x in d]
            lengths.append(value)
        old_delta = list(velocity[0])+lengths+h[W:]
        assert len(old_delta) == W+6
        assert h[W:W+2] == [0, 0] and sum(lengths) == 0
        assert all(sum(x*y for x, y in zip(c, old_delta)) == 0 for c in closure)
        values = {i: sum(x*y for x, y in zip(rows[i], old_delta)) for i in axis}
        assert all(value >= 0 for value in values.values())
        assert [i for i in axis if values[i] == 0] == Z
        assert any(value > 0 for value in values.values())
        checks.append({'tag': tag, 'repair_rank_mod_closure': r, 'forced_zero_rank_mod_closure': zero_rank})
        print(tag+' PASS', flush=True)
    out = {'status': 'EXACT_PASS', 'cases_checked': len(checks), 'checks': checks,
           'scope': 'Independent original-coordinate positive-stress, quotient-rank, axis/diagonal membership and exact relative-interior checks. Optical validity still inherits frozen packets.'}
    (ROOT / 'repair-verify.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'checks'}, indent=2), flush=True)


if __name__ == '__main__':
    main()
