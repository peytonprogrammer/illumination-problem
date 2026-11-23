"""R22 fixed-source cutoff using only strip widths and rational interval arithmetic."""
from fractions import Fraction
from itertools import combinations, groupby
import json
from math import gcd, lcm
from pathlib import Path

root = Path(__file__).resolve().parents[2]
archive = next(root.glob('illumination-generalization*/fable/directions*/d8-perturbation-test/rooms.json'))
room = next(r for r in json.loads(archive.read_text()) if r['id'] == 'R22-base')
cells = room['cells']


def periods(axis):
    result = set()
    for line in {p[1-axis] for p in cells}:
        values = sorted(p[axis] for p in cells if p[1-axis] == line)
        for _, run in groupby(enumerate(values), lambda pair: pair[1]-pair[0]):
            result.add(2 * len(list(run)))
    return sorted(result)


def stalled_orders(widths, shear, next_limit):
    # A stalled open tile has at least two orbit points when q > 2*shear.
    # Its first two fractional positions must both have small denominators.
    low = sorted({Fraction(i, d) for d in range(2, next_limit+1) for i in range(1, d)})
    orders = set()
    for u, v in combinations(low, 2):
        gap = v-u
        if u > gap:  # predecessor would also be in the open tile
            continue
        p = v+gap
        while p < 1 and p.denominator <= next_limit:
            p += gap
        if p < 1:
            continue
        for w in widths:
            h = w/gap
            if h.denominator != 1:
                continue
            a = shear//w
            for g in range(1,a+1):
                if a%g:
                    continue
                q = h.numerator*g
                if q > 2*shear and gcd(q,a) == g:
                    orders.add(lcm(q,u.denominator))
    return orders


widths, heights = periods(0), periods(1)
A, B = lcm(*widths), lcm(*heights)
start = {lcm(i,j) for i in range(1,2*B+1) for j in range(1,2*A+1)}
hstop = stalled_orders(widths,A,2*B)
vstop = stalled_orders(heights,B,2*A)
possible = start | hstop | vstop
print('horizontal and vertical strip circumferences:',widths,heights)
print('shears:',A,B,'general cutoff:',4*A*B*max(A,B))
print('initial small-coordinate orders:',len(start),'maximum:',max(start))
print('horizontal stalled orders:',sorted(hstop))
print('vertical stalled orders:',sorted(vstop))
print('combined possible orders:',len(possible),'maximum:',max(possible))
print('known dark target order retained:',1 in possible)
assert 1 in possible and A == B == 8


def check_by_transverse_denominator(widths, shear, limit):
    # At a stall the first sample u >= 1/limit satisfies u <= gap <= shear/q.
    result = set()
    for q in range(2*shear+1, shear*limit+1):
        for w in widths:
            gap = Fraction(w*gcd(q,shear//w),q)
            for d in range(2,limit+1):
                for i in range(1, int(gap*d)+1):
                    u = Fraction(i,d)
                    position = u
                    while position < 1 and position.denominator <= limit:
                        position += gap
                    if position >= 1:
                        result.add(lcm(q,u.denominator))
    return result


assert hstop == check_by_transverse_denominator(widths,A,2*B)
assert vstop == check_by_transverse_denominator(heights,B,2*A)
print('cross-check by transverse denominator: identical order sets')
