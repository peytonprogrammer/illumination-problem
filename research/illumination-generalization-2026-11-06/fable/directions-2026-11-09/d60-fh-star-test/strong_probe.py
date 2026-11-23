"""STRONG reading on one distinct-image pair: dumb12 S=(1,1), T=(1,2) (class d), full orbit.
Run: python3 -B strong_probe.py"""
import time
from fh_star import run_pair_factor, points_of, D, load, room_tuple, d4
cells = load(D / 'd41-two-param-cover' / 'rooms' / 'dumb12.txt')
S, T = (1, 1), (1, 2)
room, t = room_tuple(cells, S)
_, LS = points_of(room, t, S, S)
y, LT = points_of(room, t, T, S)
P = [P for P in d4.all_block_systems(list(t), len(t[0])) if 1 < len(P) < len(t[0])]
for part in P:
    st = run_pair_factor(t, LS, LT, y, part)
    print(S, T, 'abcd'[y], len(part), 'blocks', st, 'CPU %.2f' % time.process_time())
