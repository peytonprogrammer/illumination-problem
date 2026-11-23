"""Replay reversal.md's prescribed DB55 branch at d75's saved length 451."""
from fractions import Fraction as F
from math import gcd

length = 451
slope = F(-37, 8)
source_x, source_y = 1, 1
entrance, exit_x, mirror = 5, 5 + length, 10 + length
target_x = 6 + length


def fold(height, bottom, top):
    width = top - bottom
    residue = (height - bottom) % (2 * width)
    return bottom + min(residue, 2 * width - residue)


left = fold(source_y + (entrance-source_x)*slope, 0, 5)
# At the first mouth the chamber development is in (-20,-15),
# where folding has positive derivative. Continue at the same signed slope.
assert source_y + (entrance-source_x)*slope == F(-35, 2)
mid_x = source_x + F(mirror-source_x + mirror-target_x, 2)
mid_y = fold(left + (mid_x-entrance)*slope, 2, 3)
exit_phase = left + length*slope
right = fold(exit_phase, 2, 3)
assert (exit_phase-2) % 2 < 1  # positive fold derivative
wall = fold(right + (mirror-exit_x)*slope, 0, 5)
end = fold(right + (mirror-exit_x + mirror-target_x)*slope, 0, 5)
assert gcd(5,length) == 1 and gcd(5,2) == 1
assert (left,mid_x,mid_y,right,wall,end) == (F(5,2),233,2,F(21,8),F(1,2),1)
print('area',50+length,'mouths',left,right,'mirror height',wall,'target',(target_x,end))
print('regular midpoint',(mid_x,mid_y),'half developed displacement',(mid_x-source_x,(mid_x-source_x)*slope))
