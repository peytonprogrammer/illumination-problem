"""Task 1: try to refute the Direction 1 claims with exact arithmetic.

(a) The first primitive piece of every A-to-A segment has a C point at its midpoint.
(b) Tiling vertices on a primitive A-to-A segment: C only at t=1/2, B only at
    t in {1/3, 2/3}, no A. So B never needs to block.
(c) The pinwheel: 12 walls, six 270-degree C corners, six 30-degree tips.
Plus controls for the darkness shooter in check_room.py.
"""
import json, itertools
from fractions import Fraction as F
from math import gcd
from check_room import label, add, scale, E1, E2, check, analyze, darkness

N = 60
out = {}

# (a) + (b)
stats = dict(primitive=0, nonprimitive=0, B_at_thirds=0, no_B=0, fails=[])
for a in range(-N, N+1):
    for b in range(-N, N+1):
        if (a, b) == (0, 0): continue
        d = add(scale(a, E1), scale(b, E2)); k = gcd(a, b)
        if k == 1:
            stats['primitive'] += 1
            # every tiling vertex lies in (1/6)L, so only t = j/6 can carry one;
            # for small vectors also scan t = j/60 as an independent sanity check
            den = 60 if max(abs(a), abs(b)) <= 6 else 6
            hits = {}
            for j in range(1, den):
                t = F(j, den); l = label(scale(t, d))
                if l: hits[t] = l
            Cs = [t for t, l in hits.items() if l == 'C']; Bs = sorted(t for t, l in hits.items() if l == 'B'); As = [t for t, l in hits.items() if l == 'A']
            if Cs != [F(1, 2)] or As or Bs not in ([], [F(1, 3), F(2, 3)]):
                stats['fails'].append((a, b, {str(t): l for t, l in hits.items()}))
            if Bs: stats['B_at_thirds'] += 1
            else: stats['no_B'] += 1
        else:
            stats['nonprimitive'] += 1
            # first C point along the segment is at t = 1/(2k)
            first = None
            for j in range(1, 6*k):
                t = F(j, 6*k)
                if label(scale(t, d)) == 'C': first = t; break
            if first != F(1, 2*k): stats['fails'].append((a, b, 'first C at', str(first)))
out['midpoint_claim'] = dict(bound=N, **{k: v for k, v in stats.items() if k != 'fails'}, failures=stats['fails'][:5], PASS=not stats['fails'])

# (1/2)L/L classes are exactly the three edge-midpoint classes
mids = {label(scale(F(1, 2), v)) for v in [E1, E2, add(E1, E2)]}
out['half_lattice_classes_are_C'] = mids == {'C'}


# (c) pinwheel and its 63 siblings
def lat(i, j): return add(scale(i, E1), scale(j, E2))
O = (0, 0)
P = [lat(1, 0), lat(0, 1), lat(-1, 1), lat(-1, 0), lat(0, -1), lat(1, -1)]
M = [scale(F(1, 2), p) for p in P]; M = [tuple(int(c) for c in m) for m in M]
G = [tuple(int(c) for c in scale(F(1, 3), add(P[m], P[(m+1) % 6]))) for m in range(6)]
star = []
for m in range(6):
    star += [(O, M[m], G[m]), (O, M[(m+1) % 6], G[m])]
variants = {}
for choice in itertools.product((0, 1), repeat=6):
    # choice 0: tile (P_m, M_m, G_m); choice 1: tile (P_m, M_m, G_{m-1})
    extra = [(P[m], M[m], G[m] if c == 0 else G[(m-1) % 6]) for m, c in enumerate(choice)]
    try:
        info, _ = analyze(star + extra)
        variants[''.join(map(str, choice))] = dict(walls=info['walls'], transparent_C=len(info['transparent_C']), angles=info['angle_histogram'])
    except AssertionError as e:
        variants[''.join(map(str, choice))] = dict(error=str(e))
pin = star + [(P[m], M[m], G[m]) for m in range(6)]
info = check(dict(tiles=[[list(p) for p in t] for t in pin]), bound=20)
out['pinwheel'] = dict(tiles=[[list(p) for p in t] for t in pin], walls=info['walls'], angle_histogram=info['angle_histogram'],
                       corners=info['corners'], transparent_C=info['transparent_C'], C_tile_counts=info['C_tile_counts'],
                       flat_B=info['flat_B'], interior_A=info['interior_A'], shots_from_O=info['dark_tests'])
out['pinwheel_variants_wall_counts'] = sorted({(v.get('walls'), v.get('transparent_C')) for v in variants.values()}, key=str)
out['pinwheel_variants'] = variants

# Control: a lit room (all tiles with A vertex in a hex of radius 2) must show open shots.
tiles = []
for i in range(-3, 4):
    for j in range(-3, 4):
        for tri in [((i, j), (i+1, j), (i, j+1)), ((i+1, j), (i+1, j+1), (i, j+1))]:
            if all(max(abs(x), abs(y), abs(x+y)) <= 2 for x, y in tri):
                v = [lat(*q) for q in tri]; g = tuple(int(c) for c in scale(F(1, 3), add(add(v[0], v[1]), v[2])))
                for p, q in itertools.combinations(v, 2):
                    m = tuple(int(c) for c in scale(F(1, 2), add(p, q)))
                    tiles += [(p, m, g), (q, m, g)]
ctrl = check(dict(tiles=[[list(p) for p in t] for t in tiles], S=[0, 0], T=[12, 0]), bound=12)
out['control_lit_hexagon'] = dict(walls=ctrl['walls'], transparent_C=len(ctrl['transparent_C']),
                                  open_from_S=ctrl['dark_tests']['[0, 0]']['open_count'],
                                  directions=ctrl['dark_tests']['[0, 0]']['directions'], verdict=ctrl['verdict'])

json.dump(out, open('verify-claims.json', 'w'), indent=1, default=str)
print(json.dumps({k: v for k, v in out.items() if k not in ('pinwheel_variants',)}, indent=1, default=str)[:6000])
