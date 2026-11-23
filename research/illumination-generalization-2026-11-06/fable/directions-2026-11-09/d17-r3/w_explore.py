import sys
from rooms import Room, shoot
# W pentomino, mask 94 `#../##./.##`, scaled by q. A=[0,q]x[q,3q], J=[q,2q]x[q,2q], B=[q,3q]x[0,q]
for q in (2, 3, 4, 5):
    R = Room(3, 3, 94, [q] * 3, [q] * 3)
    print("q", q, R.shape(), "interior pts", len(R.interior_points()))
    for (S, T) in (((1, 2 * q), (2 * q, 1)), ((1, 2 * q), (2 * q, q - 1)), ((q - 1, 2 * q), (2 * q, q - 1)), ((1, 2*q+1), (2*q+1, 1))):
        r = shoot(R, S, T, 60)
        print("  S", S, "T", T, "types", R.ptype(S), R.ptype(T), "->", None if r is None else (r[0], r[1], r[2], len(r[3])))
