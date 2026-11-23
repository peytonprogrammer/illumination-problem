"""D113 claim 3: odd crosses P_b. Room data, supporting-line gaps, and an exhaustive check over
reflex-vertex rectangles for a separating corridor with two genuine mouths. python3 -B cross.py"""
from fractions import Fraction as F
from itertools import combinations
from geo import rect, summary
from jump import cells as dbas_cells


def cross(b):
    return rect(-b, b, -2, 2) | rect(-2, 2, -b, b)


def corridors(C, refl):
    """Rectangles [c1,c2]x[y0,y1] (horizontal) with four reflex corners, open mouths, wall long sides.
    Vertical corridors: run on the transposed room."""
    R = set(refl); out = []
    xs = sorted({x for x, _ in R}); ys = sorted({y for _, y in R})
    for c1, c2 in combinations(xs, 2):
        for y0, y1 in combinations(ys, 2):
            if not all(p in R for p in ((c1, y0), (c1, y1), (c2, y0), (c2, y1))): continue
            inside = all((x, y) in C for x in range(c1, c2) for y in range(y0, y1))
            walls = all((x, y0 - 1) not in C and (x, y1) not in C for x in range(c1, c2))
            mouths = all((c1 - 1, y) in C and (c2, y) in C for y in range(y0, y1))
            out.append(((c1, c2, y0, y1), inside, walls, mouths))
    return out


def report(name, C):
    info = summary(C)
    print(f'== {name}: W={info["W"]} r={info["r"]} area={info["area"]} gcd_h={info["gcd_h"]} gcd_v={info["gcd_v"]} '
          f'no corner-only class={info["no_corner_only_class"]}')
    print('   classes', {c: v for c, v in sorted(info['classes'].items())})
    V = info['V']
    for ax, name_ in ((0, 'x'), (1, 'y')):
        lines = sorted({v[ax] for v in V}); gaps = [b - a for a, b in zip(lines, lines[1:])]
        span = lines[-1] - lines[0]
        print(f'   {name_}-support {lines} gaps {gaps} max/min ratio {F(max(gaps), min(gaps))} normalized gaps {[str(F(g, span)) for g in gaps]}')
    T = {(y, x) for x, y in C}
    for lab, CC, rf in (('horizontal', C, info['reflex']), ('vertical', T, [(y, x) for x, y in info['reflex']])):
        cand = corridors(CC, rf)
        good = [c for c in cand if all(c[1:])]
        print(f'   {lab}: {len(cand)} reflex rectangles; (inside, wall sides, open mouths) = '
              f'{[(c[0], c[1], c[2], c[3]) for c in cand]}; genuine corridors {[c[0] for c in good]}')


if __name__ == '__main__':
    report('control DBas (L=4)', dbas_cells(0)[0])
    for b in (7, 9, 41):
        report(f'P_{b}', cross(b))
        assert summary(cross(b))['area'] == 16 * b - 16
