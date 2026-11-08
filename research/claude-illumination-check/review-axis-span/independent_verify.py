"""Independent exact re-check of Section 6 (axis-span claim) on frozen inputs.

Reads only the copied frozen JSON files in this directory. It does not import
or execute the Codex checker, the twist-action generator, or any builder.
No room, ray, direction, word, cylinder, or orbit is discovered.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib, json

here = Path(__file__).resolve().parent
pins = {
    'coupling.json': '9f81b7bf93b258958fa3d6347631e50f8165e57ad32166547431a3be9ed26bec',
    'twist-action.json': 'b500e3b59ba262a81655d60441f31d6c7da74e022d308761f171cc7459f81e27',
    'twist-pf.json': '0bbe693ff7e0e3e9a47541a253027cb433e6b301b52c152a469289356c71fd92',
}
for name, h in pins.items():
    got = hashlib.sha256((here / name).read_bytes()).hexdigest()
    if got != h:
        raise SystemExit(f'hash mismatch for {name}: {got}')
C = json.loads((here / 'coupling.json').read_text())
A = json.loads((here / 'twist-action.json').read_text())
PF = json.loads((here / 'twist-pf.json').read_text())
report = {}

def check(cond, msg):
    if not cond:
        raise SystemExit('FAIL: ' + msg)

# ---------------------------------------------------------------- bindings
W = C['walls']; dim = C['offset_dimension']
check(W == 25 and dim == W + 4, 'dimension')
Vt = [tuple(map(F, p)) for p in C['room']['vertices']]
N = [tuple(map(F, n)) for n in C['offset_normals']]
base = [F(x) for x in C['offset_base_point']]
S, T = [tuple(map(F, p)) for p in C['room']['marked']]
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
# Wall i runs from vertex i to vertex i+1 and lies on the line N[i].p = c_i.
for i in range(W):
    a, b = Vt[i], Vt[(i + 1) % W]
    check(dot(N[i], a) == base[i] == dot(N[i], b), f'wall {i} offset binding')
    check(dot(N[i], (b[0] - a[0], b[1] - a[1])) == 0, f'wall {i} normal')
check(base[W:] == [S[0], S[1], T[0], T[1]], 'mark columns 25..28 are (Sx,Sy,Tx,Ty)')
area2 = sum(Vt[i][0] * Vt[(i + 1) % W][1] - Vt[(i + 1) % W][0] * Vt[i][1] for i in range(W))
check(area2 > 0, 'counterclockwise room')
# The supplied normal points into the room (interior lies on the left).
for i in range(W):
    a, b = Vt[i], Vt[(i + 1) % W]
    left = (-(b[1] - a[1]), b[0] - a[0])
    check(dot(left, N[i]) > 0, f'wall {i} inward normal')
report['room_area'] = str(area2 / 2)
report['pocket_walls'] = {'wall1': [C['room']['vertices'][1], C['room']['vertices'][2]],
                          'wall4': [C['room']['vertices'][4], C['room']['vertices'][5]],
                          'wall20': [C['room']['vertices'][20], C['room']['vertices'][21]],
                          'normals_1_4_20': [C['offset_normals'][i] for i in (1, 4, 20)],
                          'c1_c4_c20': [str(base[i]) for i in (1, 4, 20)]}

# ------------------------------------------------- independent neck form
def unit(k):
    return [F(int(j == k)) for j in range(dim)]

def vertex_form(k):
    """Cramer's rule for vertex k = line(k-1) cap line(k), as two forms in c."""
    a, b = N[k - 1], N[k]
    det = a[0] * b[1] - a[1] * b[0]
    check(det != 0, 'adjacent walls nonparallel')
    ua, ub = unit((k - 1) % W), unit(k)
    x = [(b[1] * p - a[1] * q) / det for p, q in zip(ua, ub)]
    y = [(-b[0] * p + a[0] * q) / det for p, q in zip(ua, ub)]
    return x, y

VF = [vertex_form(k) for k in range(W)]
for k in range(W):
    check((dot(VF[k][0], base), dot(VF[k][1], base)) == Vt[k], f'vertex form {k}')

def wall_point_form(i, t):
    """Point at fraction t along wall i, transported with the wall endpoints."""
    a, b = VF[i], VF[(i + 1) % W]
    return [[(1 - t) * p + t * q for p, q in zip(a[z], b[z])] for z in (0, 1)]

lower = wall_point_form(1, F(1, 2))   # on wall 1, below B
upper = wall_point_form(4, F(1, 2))   # on wall 4, above C
check(lower[0] == [-x for x in unit(1)], 'x on wall 1 is -c1')
check(upper[0] == [-x for x in unit(4)], 'x on wall 4 is -c4')

def neck_form(start, end):
    """b0 = crosscut start->end in copy I, then end->start in copy V=(x,y)->(-x,y)."""
    dx = [e - s for s, e in zip(start[0], end[0])]
    dy = [e - s for s, e in zip(start[1], end[1])]
    # hol = Delta - V Delta = (2 dx, 0)
    return [2 * x for x in dx], [F(0)] * dim

def nonzero(row):
    return {j: str(x) for j, x in enumerate(row) if x}

up_neck = neck_form(lower, upper)      # Section 6 orientation: lower -> upper
dn_neck = neck_form(upper, lower)      # 31.1 orientation: boundary of U
report['neck_b0_x_form_lower_to_upper'] = nonzero(up_neck[0])
report['neck_b0_x_form_upper_to_lower_31_1'] = nonzero(dn_neck[0])

# Hit-formula cross-check: crossing wall k out of copy g adds 2 g n_k/|n_k|^2 per unit c_k.
Vm = ((F(-1), F(0)), (F(0), F(1)))
Im = ((F(1), F(0)), (F(0), F(1)))
mv = lambda M, v: tuple(dot(r, v) for r in M)
def hit(g, k):
    n = N[k]; s = 2 / dot(n, n); v = mv(g, n)
    return {k: (s * v[0], s * v[1])}
# Upper->lower in copy I exits through wall 1; return in copy V exits through wall 4.
h31 = {}
for d in (hit(Im, 1), hit(Vm, 4)):
    for k, v in d.items():
        h31[k] = v
check(h31 == {1: (F(-2), F(0)), 4: (F(2), F(0))}, 'hit formula, 31.1 orientation')
check(nonzero(dn_neck[0]) == {1: '-2', 4: '2'}, 'Cramer and hit formula agree')

# 31.1 orientation check: <b0,z> = sign det(b0', z') must be +1 for z entering U.
# In copy I, U (pocket side) lies east of the crosscut; entry direction is (1,0).
det2 = lambda a, b: a[0] * b[1] - a[1] * b[0]
check(det2((0, -1), (1, 0)) == 1 and det2((0, 1), (1, 0)) == -1, 'orientation')
report['b0_direction_in_identity_copy_per_31_1'] = 'south: upper flank (wall 4) to lower flank (wall 1)'

# ---------------------------------------------------------- core forms
cp = A['core_period_derivatives']
check(len(cp['horizontal']) == 20 and len(cp['vertical']) == 20, '20 + 20 cores')
cores = []
for orient in ('horizontal', 'vertical'):
    for core in cp[orient]:
        check(len(core) == 2 and all(len(r) == dim for r in core), 'core shape')
        check(all(isinstance(x, str) for r in core for x in r), 'string entries')
        cores.append((orient, [[F(x) for x in r] for r in core]))
scalar = [r for _, core in cores for r in core]
check(len(scalar) == 80, '80 scalar rows')
eq_4_20 = all(r[4] == r[20] for r in scalar)
zero_rows = sum(1 for r in scalar if not any(r))
off_axis_zero = all(not any(core[1]) if o == 'horizontal' else not any(core[0]) for o, core in cores)
mark_cols_zero = all(r[j] == 0 for r in scalar for j in range(W, dim))
nz4 = [(i, o) for i, (o, core) in enumerate(cores) for r in core if r[4] or r[20]]
report['scalar_rows'] = 80
report['col4_equals_col20_all_80'] = eq_4_20
report['identically_zero_scalar_rows'] = zero_rows
report['horizontal_y_rows_and_vertical_x_rows_all_zero'] = off_axis_zero
report['mark_columns_25_28_zero_in_all_rows'] = mark_cols_zero
report['cores_with_nonzero_col4_or_col20'] = [
    {'core': i, 'orientation': o, 'row': nonzero(cores[i][1][0 if o == 'horizontal' else 1])}
    for i, o in nz4]
check(eq_4_20, 'col4 == col20 in all 80 rows')

# Translation and Euler-scale identities, and binding to the twist-pf ledger.
tx = [n[0] for n in N] + [F(1), F(0), F(1), F(0)]
ty = [n[1] for n in N] + [F(0), F(1), F(0), F(1)]
for _, core in cores:
    for r in core:
        check(dot(r, tx) == 0 and dot(r, ty) == 0, 'translation invariance')
hp = [dot(core[0], base) for o, core in cores if o == 'horizontal']
vp = [dot(core[1], base) for o, core in cores if o == 'vertical']
check(all(dot(core[1], base) == 0 for o, core in cores if o == 'horizontal'), 'horizontal y period 0')
check(all(dot(core[0], base) == 0 for o, core in cores if o == 'vertical'), 'vertical x period 0')
room = next(r for r in PF['rooms'] if r['tag'] == C['tag'])
report['base_x_periods_of_horizontal_cores'] = sorted(int(x) for x in hp)
report['twist_pf_row_widths'] = sorted(room['row_widths'])
report['base_y_periods_of_vertical_cores'] = sorted(int(x) for x in vp)
report['twist_pf_column_lengths'] = sorted(room['column_lengths'])
report['periods_match_ledger'] = (sorted(hp) == sorted(map(F, room['row_widths']))
                                  and sorted(vp) == sorted(map(F, room['column_lengths'])))
report['ledger_square_total'] = room['squares']

# ------------------------------------------------- exact elimination (RREF)
def rref(rows):
    rows = [list(r) for r in rows]
    piv = []; r0 = 0; ncol = len(rows[0]) if rows else 0
    for col in range(ncol):
        p = next((i for i in range(r0, len(rows)) if rows[i][col]), None)
        if p is None:
            continue
        rows[r0], rows[p] = rows[p], rows[r0]
        s = rows[r0][col]; rows[r0] = [x / s for x in rows[r0]]
        for i in range(len(rows)):
            if i != r0 and rows[i][col]:
                f = rows[i][col]; rows[i] = [x - f * y for x, y in zip(rows[i], rows[r0])]
        piv.append(col); r0 += 1
    return rows[:r0], piv

def in_span(rows, v):
    return len(rref(rows + [v])[1]) == len(rref(rows)[1])

def kernel(rows, n):
    R, piv = rref(rows)
    free = [j for j in range(n) if j not in piv]
    out = []
    for f in free:
        v = [F(0)] * n; v[f] = F(1)
        for r, p in zip(R, piv):
            v[p] = -r[f]
        out.append(v)
    return out

vec = [core[0] + core[1] for _, core in cores]          # 40 forms in R^58
hx = [core[0] for o, core in cores if o == 'horizontal']
vy = [core[1] for o, core in cores if o == 'vertical']
report['rank_vector_forms_R58'] = len(rref(vec)[1])
report['rank_scalar_rows_R29'] = len(rref(scalar)[1])
report['rank_horizontal_x_rows'] = len(rref(hx)[1])
report['rank_vertical_y_rows'] = len(rref(vy)[1])
report['horizontal_and_vertical_row_spaces_equal'] = (
    len(rref(hx + vy)[1]) == len(rref(hx)[1]) == len(rref(vy)[1]))

zero = [F(0)] * dim
targets = {
    'b0_sec6': up_neck[0] + up_neck[1],
    'b1_sec6': up_neck[1] + up_neck[0],      # quarter turn: (0, 2(c1-c4))
    'b0_31_1': dn_neck[0] + dn_neck[1],
    'b1_31_1': dn_neck[1] + dn_neck[0],
}
report['target_in_vector_period_image'] = {k: in_span(vec, t) for k, t in targets.items()}
report['neck_x_row_in_scalar_span'] = in_span(scalar, up_neck[0])

K = kernel(scalar, dim)
report['scalar_kernel_dimension'] = len(K)
delta = [F(0)] * dim; delta[4] = F(-1); delta[20] = F(1)
report['sparse_delta_kills_all_80_rows'] = all(dot(r, delta) == 0 for r in scalar)
report['sparse_delta_in_computed_kernel'] = in_span(K, delta)
d_sec6 = dot(up_neck[0], delta); d_31 = dot(dn_neck[0], delta)
report['dhol_b0_delta_sec6_orientation'] = [str(d_sec6), '0']
report['dhol_b0_delta_31_1_orientation'] = [str(d_31), '0']
report['dhol_a_beta0_b_beta1_delta_31_1'] = f'({2 * d_31}a, {2 * d_31}b)'
# Every other kernel vector with marks fixed: does the neck functional vanish on all?
report['neck_functional_nonzero_on_kernel'] = any(dot(up_neck[0], k) for k in K)

# ------------------------------------------- deformation legitimacy check
def room_at(eps):
    c = [b + eps * d for b, d in zip(base, delta)]
    pts = [(dot(VF[k][0], c), dot(VF[k][1], c)) for k in range(W)]
    return c, pts

def seg_cross(p1, p2, q1, q2):
    o = lambda a, b, c: (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    d1, d2, d3, d4 = o(q1, q2, p1), o(q1, q2, p2), o(p1, p2, q1), o(p1, p2, q2)
    if ((d1 > 0) != (d2 > 0)) and d1 and d2 and ((d3 > 0) != (d4 > 0)) and d3 and d4:
        return True
    on = lambda a, b, c: o(a, b, c) == 0 and min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= c[1] <= max(a[1], b[1])
    return on(q1, q2, p1) or on(q1, q2, p2) or on(p1, p2, q1) or on(p1, p2, q2)

def inside(pts, p):
    wn = 0
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        cr = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
        if cr == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]):
            return 'boundary'
        if a[1] <= p[1] < b[1] and cr > 0:
            wn += 1
        elif b[1] <= p[1] < a[1] and cr < 0:
            wn -= 1
    return wn

deform = {}
for eps in (F(-1, 2), F(-1, 10), F(1, 10), F(1, 2)):
    c, pts = room_at(eps)
    ok_dir = True
    for i in range(W):
        e0 = (Vt[(i + 1) % W][0] - Vt[i][0], Vt[(i + 1) % W][1] - Vt[i][1])
        e1 = (pts[(i + 1) % W][0] - pts[i][0], pts[(i + 1) % W][1] - pts[i][1])
        ok_dir &= det2(e0, e1) == 0 and dot(e0, e1) > 0   # same direction, positive length
    simple = not any(seg_cross(pts[i], pts[(i + 1) % W], pts[j], pts[(j + 1) % W])
                     for i in range(W) for j in range(W)
                     if j not in (i, (i - 1) % W, (i + 1) % W))
    deform[str(eps)] = {'edges_same_direction_positive_length': ok_dir, 'simple': simple,
                        'S_winding': inside(pts, S), 'T_winding': inside(pts, T),
                        'moved_vertices': {k: [str(pts[k][0]), str(pts[k][1])] for k in range(W) if pts[k] != Vt[k]}}
    check(ok_dir and simple and inside(pts, S) == 1 and inside(pts, T) == 1, f'deformation at {eps}')
report['deformation_checks'] = deform

(here / 'independent_verify.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
