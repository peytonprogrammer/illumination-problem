"""Independent exact check of the prescribed 26.13 event, plus the fixed 26.9/26.10 events.

No imports from the Codex tree. No room, ray, direction, word, cylinder or orbit
search: every segment, mirror and leaf option below is copied from the text.
"""
from fractions import Fraction as F
from math import atan2, pi, gcd
import json, sys

def P(x, y): return (F(x), F(y))
def add(a, b): return (a[0]+b[0], a[1]+b[1])
def sub(a, b): return (a[0]-b[0], a[1]-b[1])
def mul(k, a): return (k*a[0], k*a[1])
def dot(a, b): return a[0]*b[0]+a[1]*b[1]
def cross(a, b): return a[0]*b[1]-a[1]*b[0]
def is_lattice(p): return p[0].denominator == 1 and p[1].denominator == 1
def kind(p):
    x, y = int(p[0]), int(p[1])
    return 'A' if x % 2 == 0 and y % 2 == 0 else 'B' if x % 2 and y % 2 else 'C'

# ---------- canonical tiles ----------
def tri(*pts): return frozenset((int(x), int(y)) for x, y in pts)
def cell_tiles(i, j):
    sq = [(i, j), (i+1, j), (i+1, j+1), (i, j+1)]
    a = [q for q in sq if q[0] % 2 == 0 and q[1] % 2 == 0][0]
    b = [q for q in sq if q[0] % 2 and q[1] % 2][0]
    return [frozenset((a, b, c)) for c in sq if c not in (a, b)]
def center(t): return [q for q in t if q[0] % 2 == 0 and q[1] % 2 == 0][0]
def in_closed(p, t):
    v = [P(*q) for q in t]
    s = [cross(sub(v[(k+1) % 3], v[k]), sub(p, v[k])) for k in range(3)]
    return all(c >= 0 for c in s) or all(c <= 0 for c in s)
def in_open(p, t):
    v = [P(*q) for q in t]
    s = [cross(sub(v[(k+1) % 3], v[k]), sub(p, v[k])) for k in range(3)]
    return all(c > 0 for c in s) or all(c < 0 for c in s)
def tiles_at(p):
    import math
    ix, iy = math.floor(p[0]), math.floor(p[1])
    out = set()
    for i in (ix-1, ix):
        for j in (iy-1, iy):
            for t in cell_tiles(i, j):
                if in_closed(p, t): out.add(t)
    return out
def angle_units(t, q):
    """Angle of tile t at its vertex q, in 45-degree units (C vertex is the right angle)."""
    return 2 if kind(P(*q)) == 'C' else 1

# ---------- fan-tree tile status under a hypothesis set ----------
FULL = {(0, 0), (4, 0)}
LEAVES = {  # center: parent direction (unit vector from leaf center to its C point)
    (-2, 0): (1, 0), (0, 2): (0, -1), (0, -2): (0, 1), (2, 2): (0, -1),
    (6, 0): (-1, 0), (4, 2): (0, -1), (4, -2): (0, 1)}
def leaf_tiles(a, side, m):
    d = LEAVES[a]; c = (a[0]+d[0], a[1]+d[1]); e = (c[0]+side[0], c[1]+side[1])
    t1 = frozenset((a, c, e)); t2 = frozenset((a, e, (a[0]+side[0], a[1]+side[1])))
    return [t1] if m == 1 else [t1, t2]
def status(t, hyp):
    """'present', 'absent' or 'optional' for tile t given leaf hypotheses.
    hyp maps leaf center -> (set of allowed sides, set of allowed m)."""
    a = center(t)
    if a in FULL: return 'present'
    if a == (2, 0): return 'present' if all(q[1] >= 0 for q in t) else 'absent'
    if a not in LEAVES: return 'absent'
    sides, ms = hyp[a]
    options = [leaf_tiles(a, s, m) for s in sides for m in ms]
    hits = [t in o for o in options]
    return 'present' if all(hits) else 'absent' if not any(hits) else 'optional'

R, L, U, D = (1, 0), (-1, 0), (0, 1), (0, -1)
ANY = ({R, L, U, D}, {1, 2})
def perp(a):  # both admissible portal sides for leaf a
    d = LEAVES[a]; return {(-d[1], d[0]), (d[1], -d[0])}

# ---------- forcing table (text 26.13 lines 2929-2941, 26.9 line 2632) ----------
def angle_at(p, tiles): return sum(angle_units(t, p) for t in tiles if p in t)
def base_tiles():
    ts = [t for i in range(-1, 5) for j in range(-1, 1) for t in cell_tiles(i, j)
          if center(t) in FULL]
    ts += [t for i in (1, 2) for t in cell_tiles(i, 0) if center(t) == (2, 0)]
    ts += [frozenset({(6, 0), (5, 0), (5, 1)})]  # literal upper end pocket
    return ts
forcing = {}
def contrib(p, a, side, m): return angle_at(p, leaf_tiles(a, side, m))
base = base_tiles()
# (5,1): literal 225 degrees = 5 units
forcing['B(5,1) Tup options'] = {f'{s},{m}': angle_at((5, 1), base)+contrib((5, 1), (4, 2), s, m)
                                 for s in (R, L) for m in (1, 2)}
# (3,1) with Tup = right m2
forcing['B(3,1) N options'] = {f'{s},{m}': angle_at((3, 1), base)+contrib((3, 1), (4, 2), R, 2)+contrib((3, 1), (2, 2), s, m)
                               for s in (R, L) for m in (1, 2)}
# (1,1) with N right (either m)
forcing['B(1,1) Sup options'] = {f'{s},{m},N{mn}': angle_at((1, 1), base)+contrib((1, 1), (2, 2), R, mn)+contrib((1, 1), (0, 2), s, m)
                                 for s in (R, L) for m in (1, 2) for mn in (1, 2)}
# (-1,1) with Sup right (either m), Sleft upper
forcing['B(-1,1) Sleft-upper options'] = {f'm{m},Sup{ms}': angle_at((-1, 1), base)+contrib((-1, 1), (0, 2), R, ms)+contrib((-1, 1), (-2, 0), U, m)
                                          for m in (1, 2) for ms in (1, 2)}
# 26.9: (5,-1) with Tdown right
forcing['B(5,-1) Tdown-right options'] = {f'm{m}': angle_at((5, -1), base)+contrib((5, -1), (4, -2), R, m) for m in (1, 2)}
# Only tree centers can touch these B points: list the A neighbours not in the tree.
tree = FULL | {(2, 0)} | set(LEAVES)
for p in [(5, 1), (3, 1), (1, 1), (-1, 1), (5, -1)]:
    nb = {(p[0]+dx, p[1]+dy) for dx in (-1, 1) for dy in (-1, 1)}
    forcing[f'nontree A neighbours of {p}'] = sorted(nb - tree)
f = forcing
assert f['B(5,1) Tup options'] == {f'{R},1': 4, f'{R},2': 5, f'{L},1': 3, f'{L},2': 3}
assert all(v == 4 for k, v in f['B(3,1) N options'].items() if k.startswith(str(L)))
assert all(v in (5, 6) for k, v in f['B(3,1) N options'].items() if k.startswith(str(R)))
assert all(v == 4 for k, v in f['B(1,1) Sup options'].items() if k.startswith(str(L)))
assert all(v in (5, 6) for k, v in f['B(1,1) Sup options'].items() if k.startswith(str(R)))
assert all(v == (3 if k.startswith('m1') else 4) for k, v in f['B(-1,1) Sleft-upper options'].items())
assert f['B(5,-1) Tdown-right options'] == {'m1': 3, 'm2': 4}

# ---------- hypothesis sets after forcing ----------
common = {(6, 0): ({U}, {1}), (4, 2): ({R}, {2}), (2, 2): ({R}, {1, 2}), (0, 2): ({R}, {1, 2}),
          (0, -2): (perp((0, -2)), {1, 2})}
H13 = dict(common); H13.update({(4, -2): ({L}, {1, 2}), (-2, 0): ({U}, {1})})
H09 = dict(common); H09.update({(4, -2): ({R}, {1}), (-2, 0): (perp((-2, 0)), {1, 2})})
H10 = dict(common); H10.update({(4, -2): ({L}, {1, 2}), (-2, 0): ({D}, {1, 2})})

# ---------- reflections ----------
def refl_lin(v, n): return sub(v, mul(2*dot(v, n)/dot(n, n), n))
def refl_pt(p, n, c): return sub(p, mul(2*(dot(n, p)-c)/dot(n, n), n))
Vx = lambda c: ((F(1), F(0)), F(c)); Hy = lambda c: ((F(0), F(1)), F(c))
Dm = lambda c: ((F(1), F(-1)), F(c)); Dp = lambda c: ((F(1), F(1)), F(c))

def check_leg(a, b, hyp, need):
    v = sub(b, a)
    for n in [(1, 0), (0, 1), (1, 1), (1, -1)]:
        assert cross(v, n) != 0, ('leg parallel to an edge family', a, b)
    cuts = {F(0), F(1)}
    for g, step in [(lambda p: p[0], 1), (lambda p: p[1], 1), (lambda p: p[0]+p[1], 2), (lambda p: p[0]-p[1], 2)]:
        ga, gb = g(a), g(b)
        if ga == gb: continue
        lo, hi = min(ga, gb), max(ga, gb)
        k = (int(lo) // step - 1) * step
        while k <= hi + step:
            s = (k - ga) / (gb - ga)
            if 0 < s < 1: cuts.add(s)
            k += step
    cuts = sorted(cuts)
    for s in cuts[1:-1]:
        q = add(a, mul(s, v)); assert not is_lattice(q), ('lattice point inside leg', q)
        for t in tiles_at(q): need.add(t)
    for s0, s1 in zip(cuts, cuts[1:]):
        q = add(a, mul((s0+s1)/2, v)); ts = [t for t in tiles_at(q) if in_open(q, t)]
        assert len(ts) == 1, ('midpoint not in a unique tile interior', q); need.add(ts[0])

def check_bounce(prev, h, nxt, mirror, hyp, need, forbid):
    n, c = mirror
    assert dot(n, h) == c and not is_lattice(h)
    vin, vout = sub(h, prev), sub(nxt, h)
    r = refl_lin(vin, n); assert cross(r, vout) == 0 and dot(r, vout) > 0, 'not specular'
    ts = list(tiles_at(h)); assert len(ts) == 2, ('hit not on a unit-edge interior', h)
    shared = ts[0] & ts[1]; assert len(shared) == 2
    e = [P(*q) for q in shared]; assert dot(n, e[0]) == c and dot(n, e[1]) == c, 'edge not on mirror'
    side = dot(n, prev) - c; assert side != 0 and (dot(n, nxt) - c) * side > 0
    for t in ts:
        cen = mul(F(1, 3), add(add(P(*list(t)[0]), P(*list(t)[1])), P(*list(t)[2])))
        (need if (dot(n, cen) - c) * side > 0 else forbid).add(t)
    return r

def run_event(name, S, first, fm, corner, corner_mirror, second, sm, Tm, hyp, u, slide_terms):
    need, forbid = set(), set()
    # w is the developed first half; legs are checked below to develop along w.
    w = sub(corner, S) if not fm else None
    for pts, mirrors in [(first, fm), (second, sm)]:
        for k in range(len(pts)-1):
            check_leg(pts[k], pts[k+1], hyp, need)
        for k in range(1, len(pts)-1):
            check_bounce(pts[k-1], pts[k], pts[k+1], mirrors[k-1], hyp, need, forbid)
    # corner germs and pi sector
    gin = sub(first[-2], corner); gout = sub(second[1], corner)
    n, c0 = corner_mirror
    assert dot(n, corner) == c0, 'corner flank does not pass through corner'
    dev_out = refl_lin(gout, n)
    assert cross(dev_out, gin) == 0 and dot(dev_out, gin) < 0, 'developed continuation not straight'
    # link at the corner from forced tiles
    st = {tuple(sorted(t)): status(t, hyp) for t in tiles_at(P(*corner))}
    assert 'optional' not in st.values(), ('corner link not forced', st)
    present = [t for t in tiles_at(P(*corner)) if status(t, hyp) == 'present']
    def ang(v): return atan2(float(v[1]), float(v[0])) % (2*pi)
    slots = set()
    for t in present:
        qs = [sub(P(*q), P(*corner)) for q in t if q != corner]
        a0, a1 = sorted(ang(q) for q in qs)
        if a1 - a0 > pi: a0, a1 = a1, a0 + 2*pi
        slots.add((round(a0/(pi/4)) % 8, round((a1-a0)/(pi/4))))
    occ = set()
    for s, k in slots:
        for j in range(k): occ.add((s+j) % 8)
    link_units = len(occ)
    # flank ray direction (unit along mirror) that bounds the link
    tdir = (n[1], -n[0])
    flank = [tdir, mul(-1, tdir)]
    # sector: angle from gin to flank inside link + angle from flank to gout inside link == pi
    def inside_link(theta):
        k = theta/(pi/4)
        return any(abs(k - s) < 1e-12 or abs(k - (s+1)) < 1e-12 or s < k < s+1 for s in occ) or \
               any(abs(k - 8 - s) < 1e-12 for s in occ)
    assert inside_link(ang(gin)) and inside_link(ang(gout)), 'germ outside physical link'
    def wall_ray(fd):
        k = round(ang(fd)/(pi/4)) % 8
        return (k in occ) != (((k-1) % 8) in occ)
    rays = [fd for fd in flank if wall_ray(fd)]
    assert len(rays) == 1, ('corner mirror line must give exactly one wall ray of the link', rays)
    flank_ray = rays[0]; fa = ang(flank_ray); best = []
    for orient in (+1, -1):
        a1 = (orient*(fa - ang(gin))) % (2*pi); a2 = (orient*(fa - ang(gout))) % (2*pi)
        ok = all(inside_link((ang(gin) + orient*s*a1) % (2*pi)) for s in [x/200 for x in range(201)]) and \
             all(inside_link((ang(gout) + orient*s*a2) % (2*pi)) for s in [x/200 for x in range(201)])
        if ok and abs(a1 + a2 - pi) < 1e-12: best.append((flank_ray, orient, a1, a2))
    assert len(best) == 1, ('need exactly one embedded pi sector across the wall ray', best)
    best = best[0]
    # development
    def dev(point, mirrors_before):
        for (nn, cc) in reversed(mirrors_before): point = refl_pt(point, nn, cc)
        return point
    def images(t):
        fm_t = [(mm[0], mm[1] + slide_terms.get(k_, 0)*t) for k_, mm in enumerate(fm)]
        cm = (corner_mirror[0], corner_mirror[1] + slide_terms.get('corner', 0)*t)
        sm_t = [(mm[0], mm[1] + slide_terms.get(('s', k_), 0)*t) for k_, mm in enumerate(sm)]
        tgt = dev(dev(dev(P(*Tm), sm_t), [cm]), fm_t)
        cor = dev(add(P(*corner), mul(t, u) if slide_terms.get('corner_moves') else P(0, 0)), fm_t)
        return tgt, cor
    (T0, C0), (T1, C1), (Tm1, Cm1) = images(F(0)), images(F(1)), images(F(-1))
    assert sub(T1, T0) == sub(T0, Tm1) and sub(C1, C0) == sub(C0, Cm1), 'not affine'
    if w is None: w = sub(C0, S)
    assert sub(C0, S) == w and sub(T0, C0) == w, 'halves unequal'
    assert gcd(int(w[0]), int(w[1])) == 1
    # developed velocity on every leg equals w (validates composition order)
    def legs_dev(pts, mirrors, extra):
        times = []
        for k in range(len(pts)-1):
            v = sub(pts[k+1], pts[k])
            for (nn, cc) in reversed(extra + mirrors[:k]): v = refl_lin(v, nn)
            assert cross(v, w) == 0 and dot(v, w) > 0, ('developed leg not along w', pts[k])
            times.append(dot(v, w)/dot(w, w))
        assert sum(times) == 1, ('halftime is not 1', times)
        return times
    t1 = legs_dev(first, fm, [])
    t2 = legs_dev(second, sm, fm + [corner_mirror])
    Tdot, Cdot = sub(T1, T0), sub(C1, C0)
    Q = sub(Tdot, mul(2, Cdot)); det = cross(w, Q)
    # forced-structure check: every needed tile forced present, every far-side tile forced absent
    st_need = {tuple(sorted(t)): status(t, hyp) for t in need}
    st_forbid = {tuple(sorted(t)): status(t, hyp) for t in forbid}
    bad = {k: v for k, v in st_need.items() if v != 'present'}
    bad.update({k: v for k, v in st_forbid.items() if v != 'absent'})
    assert not bad, (name, 'event uses unforced tiles', bad)
    return dict(w=w, first_durations=t1, second_durations=t2, developed_corner=C0, developed_target=T0, target_velocity=Tdot,
                corner_velocity=Cdot, Q=Q, det=det, corner_link_degrees=45*link_units,
                pi_sector=dict(flank_dir=flank_ray, orientation=best[1], arc1=best[2], arc2=best[3]),
                needed_tiles=len(need), forbidden_tiles=len(forbid))

S = P(0, 0); T = (4, 0)
results = {'forcing_table_45deg_units': {k: (v if isinstance(v, list) else {str(kk): vv for kk, vv in v.items()}) for k, v in forcing.items()}}

# 26.13 (lines 2946-2973)
results['26.13'] = run_event('26.13', S,
    [S, P(F(-9, 5), F(1, 5)), P(F(-16, 9), 0), P(F(-7, 4), F(1, 4)), P(5, 1)],
    [Dm(-2), Hy(0), Dm(-2)], P(5, 1), Dp(6),
    [P(5, 1), P(F(43, 9), -1), P(F(40, 9), 2), P(F(37, 9), -1), P(4, 0)],
    [Hy(-1), Hy(2), Hy(-1)], T, H13, P(0, 1), {'corner': 1, 'corner_moves': True})
# 26.9 (lines 2643-2669)
results['26.9'] = run_event('26.9', S,
    [S, P(5, 1)], [], P(5, 1), Dp(6),
    [P(5, 1), P(F(9, 2), F(-3, 2)), P(4, F(-8, 5)), P(F(13, 3), F(-5, 3)), P(4, 0)],
    [Dm(6), Vx(4), Dm(6)], T, H09, P(0, 1), {'corner': 1, 'corner_moves': True})
# 26.10 (lines 2724-2750); corner flank x=5 is fixed, C moves along it
results['26.10'] = run_event('26.10', S,
    [S, P(-1, F(2, 7)), P(F(3, 2), 1), P(5, 0)], [Vx(-1), Hy(1)], P(5, 0), Vx(5),
    [P(5, 0), P(3, F(-4, 7)), P(F(9, 2), -1), P(5, F(-6, 7)), P(3, F(-2, 7)), P(4, 0)],
    [Vx(3), Hy(-1), Vx(5), Vx(3)], T, H10, P(0, 1), {'corner_moves': True})

# Section 3 formula (2) cross-check for 26.13, both split conventions at the corner.
LP = lambda v: refl_lin(refl_lin(refl_lin(v, (1, -1)), (0, 1)), (1, -1))
aD = (F(1), F(1)); uu = P(0, 1)
after = add(LP(aD), mul(-2, LP(uu)))
before = add(mul(-1, LP(aD)), mul(-2, LP(refl_lin(uu, (1, 1)))))
assert after == before == results['26.13']['Q']
results['26.13']['formula2_split_after'] = after; results['26.13']['formula2_split_before'] = before
# corner frame values claimed at line 2977
wc, Qc = LP(results['26.13']['w']), LP(results['26.13']['Q'])
results['26.13']['corner_frame'] = dict(w=wc, Q=Qc, det=cross(wc, Qc))

# ---------- fixture (lines 2989-2991) independent rawness/simplicity ----------
fx = []
for i in range(-1, 5):
    for j in range(-1, 1):
        fx += [t for t in cell_tiles(i, j) if center(t) in FULL]
fx += [t for i in (1, 2) for t in cell_tiles(i, 0) if center(t) == (2, 0)]
for a, s, m in [((2, 2), R, 1), ((6, 0), U, 1), ((4, 2), R, 2), ((4, -2), L, 1),
                ((-2, 0), U, 1), ((0, 2), R, 1), ((0, -2), L, 1)]:
    fx += leaf_tiles(a, s, m)
fx = list(dict.fromkeys(fx))
edges = {}
for t in fx:
    q = sorted(t)
    for e in [(q[0], q[1]), (q[0], q[2]), (q[1], q[2])]:
        edges.setdefault(frozenset(e), []).append(t)
bnd = [e for e, o in edges.items() if len(o) == 1]
deg = {}
for e in bnd:
    for q in e: deg[q] = deg.get(q, 0) + 1
assert all(v == 2 for v in deg.values()), 'boundary vertex of degree != 2'
# one cycle
adj = {}
for e in bnd:
    a, b = tuple(e); adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
start = next(iter(adj)); seen = {start}; cur, prev = start, None
while True:
    nxt = [q for q in adj[cur] if q != prev][0] if prev is not None else adj[cur][0]
    if nxt == start: break
    seen.add(nxt); prev, cur = cur, nxt
assert len(seen) == len(adj), 'boundary is not one cycle'
verts = {q for t in fx for q in t}
angle = {q: sum(angle_units(t, q) for t in fx if q in t) for q in verts}
corners = [q for q in verts if q in deg and angle[q] != 4]
interior = [q for q in verts if q not in deg]
raw_bad = [q for q in verts if kind(P(*q)) != 'A' and (angle[q] in (4, 8) or q not in deg)]
assert not raw_bad and sorted(interior) == [(0, 0), (4, 0)]
results['fixture'] = dict(tiles=len(fx), walls=len(corners), boundary_edges=len(bnd),
                          angle_deg={str(q): 45*angle[q] for q in [(5, 1), (5, 0), (3, 1), (1, 1), (-1, 1), (5, 2)]},
                          euler=len(verts)-len(edges)+len(fx))
assert results['fixture']['tiles'] == 28 and results['fixture']['walls'] == 25 and results['fixture']['euler'] == 1
# fixture must realise H13 (each fixture tile forced or optional-present; no forced-absent tile used)
assert all(status(t, H13) != 'absent' for t in fx)

def ser(o):
    if isinstance(o, F): return str(o)
    if isinstance(o, tuple): return [ser(x) for x in o]
    if isinstance(o, dict): return {str(k): ser(v) for k, v in o.items()}
    if isinstance(o, list): return [ser(x) for x in o]
    return o
out = ser(results)
print(json.dumps(out, indent=1))
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else 'independent_check.json', 'w'), indent=1)
print('INDEPENDENT_CHECK_PASS')
