"""Exact one-sided portal cycles at the single saved slope 43/33."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import sys

directions = Path(__file__).resolve().parents[2] / "illumination-generalization-2026-11-06/fable/directions-2026-11-09"
sys.path.insert(0, str(directions / "d112-review-gluing"))
from chamber import Irregular, leg, rect_poly, shoot_room

left = [(0,0),(1,0),(1,-3),(3,-3),(3,0),(5,0),(5,4),(3,4),(3,48),(1,48),(1,4),(0,4)]
right = rect_poly(9,13,-1,5)
room = left[:6] + [(5,1),(9,1),(9,-1),(13,-1),(13,5),(9,5),(9,2),(5,2)] + left[6:]
slope = F(43,33)
source, target = (2,47), (10,3)
launches = list(product((1,-1), repeat=2))


def first_phase(polygon, mouth_x, start, signs):
    result = leg(polygon, (mouth_x,1,2), [], start, slope, *signs)
    height, _, vertical_sign = result["exit"]
    return vertical_sign * (height-1) % 2


def traverse(phase):
    phase = (phase+4*slope) % 2
    return 1+min(phase,2-phase), 1 if phase<1 else -1


def cycle(initial):
    phase = initial
    sequence = []
    seen = set()
    while phase not in seen:
        seen.add(phase)
        sequence.append(round(33*phase) % 66)
        y, sy = traverse(phase)
        right_exit = first_phase(right, 9, (9,y), (1,sy))
        y, sy = traverse(right_exit)
        phase = first_phase(left, 5, (5,y), (-1,sy))
    assert phase == initial
    return sequence


def main():
    target_phases = [int(33*first_phase(right,9,target,signs)) for signs in launches]
    assert target_phases == [65,41,5,43]
    for side in (-1,1):
        hist = Counter()
        for sx,sy in launches:
            start = (source[0], source[1]+sy*F(side,132))
            seq = cycle(first_phase(left,5,start,(sx,sy)))
            assert 935 % len(seq) == 0
            for a,b in product(seq,target_phases):
                hist[(a+172+b)%66] += 935//len(seq)
            print(side,(sx,sy),seq)
        print("all-target counts at 0 and 4:",hist[0],hist[4])
    for sx,sy in launches:
        try:
            shoot_room(room,source,(33*sx,43*sy),target,maxev=4000)
        except Irregular as exc:
            assert str(exc).startswith("vertex")
            print("critical", (sx,sy), exc)
        else:
            raise AssertionError("unexpected regular connection")


if __name__ == "__main__":
    main()
