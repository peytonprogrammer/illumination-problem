"""Pinhole chains: j+1 square chambers DxD in a row, joined by 1x1 corridors that sit
alternately on the bottom and top wall line. r = 2j, W = 4j + 4.
usage: gen_chain.py j D [j D ...] -> one room per line"""
import sys
a = list(map(int, sys.argv[1:]))
for j, D in zip(a[::2], a[1::2]):
    c = set()
    for k in range(j + 1):
        x0 = k * (D + 1)
        c |= {(x0 + x, y) for x in range(D) for y in range(D)}
        if k < j: c.add((x0 + D, 0 if k % 2 == 0 else D - 1))
    print(len(c), " ".join("%d %d" % p for p in sorted(c)))
