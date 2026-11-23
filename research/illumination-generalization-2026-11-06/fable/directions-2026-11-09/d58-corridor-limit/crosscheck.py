"""Cross-check exact.trace against d57's independent replay (read-only import)
on every candidate of families H and E (valid or not) in instances at k = 1..8,
and on the resonant E paths. Usage: python3 -B crosscheck.py > logs/crosscheck.log"""
import sys, resource
from fractions import Fraction as Fr
sys.path.insert(0, '../d57-witness-mining-r3')
import replay
from build import instance, DOOR
from families import small_candidates, vector
from exact import trace
from tests_lib import resonant
resource.setrlimit(resource.RLIMIT_CPU, (240, 240))
agree = dis = nvalid = 0
def check(room, geo, fam, cap=12):
    global agree, dis, nvalid
    hh, DD, sy = fam
    S, T = geo[5], geo[6]
    for e1, e2, k, m in small_candidates(geo, hh, DD)[:cap]:
        vec = vector(geo, hh, DD, sy, e1, e2, k, m)
        a = trace(room, S, vec, T)[0]
        b = replay.lit_by(room.cells, room.xs, room.ys, S, T, (S[0] + vec[0], S[1] + vec[1]))[0]
        if bool(a) == bool(b): agree += 1
        else: dis += 1; print('DISAGREE', vec, a, b)
        nvalid += bool(a)
        # off-window neighbour (m + 1, m - 1): xi leaves the door; expected invalid
        for dm in (1, -1):
            vec = vector(geo, hh, DD, sy, e1, e2, k, m + dm)
            a = trace(room, S, vec, T)[0]
            b = replay.lit_by(room.cells, room.xs, room.ys, S, T, (S[0] + vec[0], S[1] + vec[1]))[0]
            if bool(a) == bool(b): agree += 1
            else: dis += 1; print('DISAGREE', vec, a, b)
            nvalid += bool(a)
base = dict(L=Fr(4), pi=Fr(3, 2), u=Fr(2, 3), beta=Fr(2, 5), ell=Fr(1), fh=Fr(3, 7))
for mask, S, T in DOOR:
    for k in range(1, 9):
        room, geo, info = instance(mask, S, T, **dict(base, w=Fr(1, 2 ** k), D=Fr(5, 7), h=None))
        h, D = geo[6][1] - geo[4], geo[4] - geo[5][1]
        check(room, geo, (h, D, 1)); check(room, geo, (2 * info['ell'] - h, D, 1))
    for kk in (8,):
        room, geo, info = resonant(mask, S, T, kk, 'long')
        h, D = geo[6][1] - geo[4], geo[4] - geo[5][1]
        check(room, geo, (2 * info['ell'] - h, D, 1), cap=4)
print(f'candidates compared {agree + dis}, agree {agree}, disagree {dis}, valid by trace {nvalid}')
