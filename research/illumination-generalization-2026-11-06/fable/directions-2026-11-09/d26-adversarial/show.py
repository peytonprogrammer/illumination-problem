"""ASCII picture of rooms. usage: show.py < lines 'A x y ...' (optionally prefixed 'ROOM ')"""
import sys
for line in sys.stdin:
    v = list(map(int, line.replace("ROOM", "").split())); c = set(zip(v[1::2], v[2::2]))
    w = max(x for x, _ in c) + 1; h = max(y for _, y in c) + 1
    for y in range(h - 1, -1, -1): print("".join("#" if (x, y) in c else "." for x in range(w)))
    print()
