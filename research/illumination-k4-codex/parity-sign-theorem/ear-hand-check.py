"""Uniform exact verification of two fixed words in an ear deformation family.

No directions or reflection words are searched. Every inequality is proved on
0 < u <= 1/1000 by a rational coefficient bound, including u arbitrarily near 0.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import hashlib

if not __debug__:
    raise RuntimeError('Exact verification requires assertions; do not use -O.')

ROOT = Path(__file__).resolve().parent
PINNED_INPUT_HASHES = {'inputs/room.json': '4e9d566118d1bb8d9f81f12255abe14da7f67028b0d8b63789b081a145c3e805', 'coupling.json': '9f81b7bf93b258958fa3d6347631e50f8165e57ad32166547431a3be9ed26bec'}
for name, digest in PINNED_INPUT_HASHES.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, (
        "frozen input changed", name)
RHO = F(1, 1000)
ROOM = json.loads((ROOT/'inputs/room.json').read_text())
SAVED = json.loads((ROOT/'coupling.json').read_text())
WORDS = {
    1: (50, [23, 20, 2, 3, 0, 24, 6, 5, 18, 7, 16, 10, 12, 11]),
    -1: (105, [6, 5, 18, 7, 16, 11, 17, 14]),
}


def poly(a):
    a = list(map(F, a))
    while len(a) > 1 and not a[-1]:
        a.pop()
    return tuple(a)


P0 = poly([0])
P1 = poly([1])
add = lambda a, b: poly([(a[i] if i < len(a) else 0)+(b[i] if i < len(b) else 0) for i in range(max(len(a), len(b)))])
scale = lambda c, a: poly([c*x for x in a])
sub = lambda a, b: add(a, scale(-1, b))


def mul(a, b):
    c = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for k, y in enumerate(b):
            c[i+k] += x*y
    return poly(c)


def positive(a, strict=True):
    """A proof on (0,rho], never a sampled sign test."""
    leading = next((i for i, x in enumerate(a) if x), None)
    if leading is None:
        return None if strict else {'coefficients': a, 'identically_zero': True}
    remainder = sum(abs(a[i])*RHO**(i-leading) for i in range(leading+1, len(a)))
    if a[leading] > remainder:
        return {'coefficients': a, 'leading_order': leading,
                'leading_coefficient': a[leading], 'tail_bound': remainder}
    return None


def rational(num, den):
    if positive(den):
        return num, den
    assert positive(scale(-1, den)), ('denominator not bounded away from zero', den)
    return scale(-1, num), scale(-1, den)


def difference(a, b):
    return sub(mul(a[0], b[1]), mul(b[0], a[1]))


def mm(A, B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in (0, 1)) for j in (0, 1)) for i in (0, 1))


def mv(A, v):
    return tuple(add(scale(A[i][0], v[0]), scale(A[i][1], v[1])) for i in (0, 1))


I = ((F(1), F(0)), (F(0), F(1)))
NORMALS = [tuple(map(F, n)) for n in SAVED['offset_normals']]
BASE = [tuple(map(F, v)) for v in ROOM['vertices']]
assert ROOM['vertices'] == SAVED['room']['vertices'] and ROOM['marked'] == SAVED['room']['marked']
assert len(BASE) == 25 and ROOM['marked'] == [[0, 2], [0, 6]]
SOURCE, TARGET = [tuple(poly([x]) for x in p) for p in ROOM['marked']]
DOT = lambda a, b: sum(x*y for x, y in zip(a, b))
NORMAL_CHOICES = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]


def separation(A, B):
    for n in NORMAL_CHOICES:
        receipts = [positive(add(scale(n[0], sub(b[0], a[0])), scale(n[1], sub(b[1], a[1])))) for a in A for b in B]
        if all(receipts):
            return {'normal': n, 'inequalities': receipts}
    raise AssertionError(('no uniform strict separator', A, B))


def inside(point):
    winding = 0
    x, y = point
    for a, b in zip(BASE, BASE[1:]+BASE[:1]):
        cross = (b[0]-a[0])*(y-a[1])-(b[1]-a[1])*(x-a[0])
        if a[1] <= y < b[1] and cross > 0:
            winding += 1
        elif b[1] <= y < a[1] and cross < 0:
            winding -= 1
    return winding != 0


def on_boundary(point):
    x, y = point
    for a, b in zip(BASE, BASE[1:]+BASE[:1]):
        if ((b[0]-a[0])*(y-a[1]) == (b[1]-a[1])*(x-a[0])
                and min(a[0], b[0]) <= x <= max(a[0], b[0])
                and min(a[1], b[1]) <= y <= max(a[1], b[1])):
            return True
    return False


def parity_control():
    closed = []
    for x in range(-2, 3):
        for y in range(9):
            if inside((x, y)) or on_boundary((x, y)):
                closed.append((x, y))
                if x % 2 or y % 2:
                    assert (x, y) in BASE
    for n, a, b in zip(NORMALS, BASE, BASE[1:]+BASE[:1]):
        d = (b[0]-a[0], b[1]-a[1])
        assert DOT(n, d) == 0 and n[0]*d[1]-n[1]*d[0] < 0
        nn = DOT(n, n)
        shift = [2*DOT(n, a)*v/nn for v in n]
        assert all(v.denominator == 1 and int(v) % 2 == 0 for v in shift)
        R = [F(i == k)-2*n[i]*n[k]/nn for i in (0, 1) for k in (0, 1)]
        assert all(v.denominator == 1 for v in R)
    assert all(inside(p) and not on_boundary(p) for p in ROOM['marked'])
    return {'closed_integer_points': len(closed),
            'non_even_even_points_all_corners': sum(x % 2 != 0 or y % 2 != 0 for x, y in closed),
            'even_even_preserving_reflections': len(NORMALS)}


def check(sign):
    index, word = WORDS[sign]
    assert SAVED['events'][index]['word'] == word
    W = len(BASE)
    offsets = [poly([DOT(n, v), sign*(2 if i == 5 else -1 if i == 6 else 0)]) for i, (n, v) in enumerate(zip(NORMALS, BASE))]
    vertices = []
    for i in range(W):
        a, b = NORMALS[(i-1)%W], NORMALS[i]
        det = a[0]*b[1]-a[1]*b[0]
        vertices.append((scale(1/det, sub(scale(b[1], offsets[(i-1)%W]), scale(a[1], offsets[i]))),
                         scale(1/det, sub(scale(a[0], offsets[i]), scale(b[0], offsets[(i-1)%W])))))
    directions = [(n[1], -n[0]) for n in NORMALS]
    lengths = [scale(1/DOT(d, d), add(scale(d[0], sub(vertices[(i+1)%W][0], vertices[i][0])),
                                     scale(d[1], sub(vertices[(i+1)%W][1], vertices[i][1])))) for i, d in enumerate(directions)]
    assert all(positive(length) for length in lengths)
    assert vertices[5] == (poly([1]), poly([3, 2*sign]))
    assert vertices[6] == (poly([2, -sign]), poly([4, sign]))
    assert vertices[7] == (poly([1]), poly([4, sign]))
    assert all(vertices[i] == tuple(poly([x]) for x in BASE[i]) for i in range(W) if i not in (5, 6, 7))
    topology = []
    for i in range(W):
        for k in range(i+1, W):
            if k == i+1 or (i == 0 and k == W-1):
                continue
            topology.append({'edges': [i, k], **separation([vertices[i], vertices[(i+1)%W]], [vertices[k], vertices[(k+1)%W]])})
    marks = []
    for point in ROOM['marked']:
        assert inside(point)
        form = tuple(poly([x]) for x in point)
        marks.append([separation([form], [vertices[i], vertices[(i+1)%W]]) for i in range(W)])
    reflectors = []
    for n, h in zip(NORMALS, offsets):
        nn = DOT(n, n)
        R = tuple(tuple(F(a == b)-2*n[a]*n[b]/nn for b in (0, 1)) for a in (0, 1))
        shift = tuple(scale(2*n[a]/nn, h) for a in (0, 1))
        reflectors.append((R, shift))
    O, B = I, (P0, P0)
    states = [(O, B)]
    for wall in word:
        R, shift = reflectors[wall]
        mapped = mv(O, shift)
        B = tuple(add(B[k], mapped[k]) for k in (0, 1))
        O = mm(O, R)
        states.append((O, B))
    target_image = tuple(add(mv(O, TARGET)[k], B[k]) for k in (0, 1))
    A = tuple(sub(target_image[k], SOURCE[k]) for k in (0, 1))
    expected = (poly([-10, 2*sign]), poly([-20])) if sign == 1 else (poly([8, -2*sign]), poly([16]))
    assert target_image == expected
    current = (P0, P1)
    hits = []
    exclusion_count = 0
    for stage, (O, B) in enumerate(states):
        Ot = tuple(zip(*O))

        def intersection(wall):
            n, h, d = NORMALS[wall], offsets[wall], directions[wall]
            N = tuple(sum(O[k][a]*n[a] for a in (0, 1)) for k in (0, 1))
            numerator = add(h, add(scale(N[0], sub(B[0], SOURCE[0])), scale(N[1], sub(B[1], SOURCE[1]))))
            denominator = add(scale(N[0], A[0]), scale(N[1], A[1]))
            tau = rational(numerator, denominator)
            num, den = tau
            global_point_num = tuple(add(mul(sub(SOURCE[k], B[k]), den), mul(A[k], num)) for k in (0, 1))
            physical_num = mv(Ot, global_point_num)
            along = scale(1/DOT(d, d), add(scale(d[0], sub(physical_num[0], mul(vertices[wall][0], den))),
                                           scale(d[1], sub(physical_num[1], mul(vertices[wall][1], den)))))
            remaining = sub(mul(lengths[wall], den), along)
            return tau, along, remaining, physical_num

        intended = word[stage] if stage < len(word) else None
        if intended is not None:
            next_tau, along, remaining, point_num = intersection(intended)
            at_start, at_end = positive(along), positive(remaining)
            assert at_start and at_end, ('bounce not strictly inside edge', sign, stage, intended, along, remaining)
            hits.append({'stage': stage, 'wall': intended, 'tau': next_tau,
                         'physical_point_numerators': point_num,
                         'edge_start_clearance': at_start, 'edge_end_clearance': at_end})
        else:
            next_tau = (P1, P1)
        order = positive(difference(next_tau, current))
        assert order, ('nonpositive segment length', sign, stage)
        checks = []
        for wall in range(W):
            if wall == intended:
                continue
            tau, along, remaining, _ = intersection(wall)
            options = [('at_or_before_start', scale(-1, difference(tau, current)), False),
                       ('at_or_after_end', difference(tau, next_tau), False),
                       ('outside_before_edge', scale(-1, along), True),
                       ('outside_after_edge', scale(-1, remaining), True)]
            for reason, condition, strict in options:
                proof = positive(condition, strict=strict)
                if proof is not None:
                    checks.append({'wall': wall, 'reason': reason, 'proof': proof})
                    break
            else:
                raise AssertionError(('unexcluded wall', sign, stage, wall, options))
        exclusion_count += len(checks)
        if intended is not None:
            hits[-1]['segment_order'] = order
            hits[-1]['other_wall_exclusions'] = checks
        else:
            terminal = {'segment_order': order, 'wall_exclusions': checks}
        current = next_tau
    return {'sign': sign, 'saved_index': index, 'word': word, 'target_image': target_image,
            'rho': RHO, 'bounces': hits, 'terminal': terminal,
            'uniform_segment_wall_exclusions': exclusion_count,
            'nonadjacent_edge_separations': len(topology), 'topology_receipts': topology,
            'marks_stay_interior_receipts': marks}


out = {'status': 'EXACT_UNIFORM_PASS', 'parameter_interval': '-1/1000 <= epsilon <= 1/1000, epsilon nonzero',
       'base_parity_control': parity_control(),
       'cases': [check(1), check(-1)],
       'input_hashes': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                        for name in ('inputs/room.json', 'coupling.json')},
       'scope': 'Two prescribed saved words, exact inequalities over complete open parameter intervals, no sampled directions or trajectory discovery. No general parity sign theorem.'}
(ROOT/'ear-hand-check.json').write_text(json.dumps(out, indent=2, default=str)+'\n')
for case in out['cases']:
    print(json.dumps({k: case[k] for k in ('sign', 'saved_index', 'word', 'target_image', 'rho', 'uniform_segment_wall_exclusions', 'nonadjacent_edge_separations')}, default=str))
print(out['status'])
