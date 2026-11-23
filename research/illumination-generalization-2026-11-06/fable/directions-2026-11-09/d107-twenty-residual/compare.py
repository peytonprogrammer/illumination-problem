"""D107: compare cert2's own residual for one room with the room's saved boxes.

Usage: python3 -B compare.py ROOMFILE RESIDUAL BOXES NAME

Checks, all in exact integer arithmetic:
  1. The open tile pairs in the residual equal the tile pairs named in BOXES.
  2. Every residual product f x W lies in closed tiles, and some box of its tile pair
     covers it: every vertex at the end in tile a is within r/65536 (max-norm) of
     corner ca of tile a, and likewise for tile b. Corner index k means
     (x + (k & 1), y + (k >> 1)), as in D103.
  3. Reports the per-box maximum displacement that the residual actually reaches.
The census code and census residual are not read; BOXES is the object being compared.
"""
import sys
from fractions import Fraction as F

U = 65536
roomf, resf, boxf, name = sys.argv[1:5]
v = list(map(int, open(roomf).read().split()))
cells = [(v[2 + 2 * i], v[3 + 2 * i]) for i in range(v[0])]
boxes = {}
for l in open(boxf):
    a, b, ca, cb, r = map(int, l.split())
    boxes.setdefault((a, b), []).append((ca, cb, r))


def poly(tok):
    t = list(map(int, tok.split()))
    return [(t[i], t[i + 1], t[i + 2]) for i in range(0, len(t), 3)]


def corner(c, k):
    x, y = cells[c]
    return x + (k & 1), y + (k >> 1)


def disp(P, c, k):  # exact max-norm displacement of polygon P from corner k of tile c
    X0, Y0 = corner(c, k)
    return max(max(abs(F(X, d) - X0), abs(F(Y, d) - Y0)) for X, Y, d in P)


def in_tile(P, c):
    x, y = cells[c]
    return all(x * d <= X <= (x + 1) * d and y * d <= Y <= (y + 1) * d for X, Y, d in P)


open_pairs = set(); nprod = 0; bad = []; reach = {}
for line in open(resf):
    if line.startswith('PAIR '):
        t = line.split()
        if int(t[7]) > 0:
            open_pairs.add((int(t[1]), int(t[2])))
        continue
    if not line.startswith('PROD '):
        continue
    head, fs, ws = line.split('|')
    _, a, b, src = head.split(); a, b, src = int(a), int(b), int(src)
    f, W = poly(fs), poly(ws); nprod += 1
    tgt = b if src == a else a
    if not (in_tile(f, src) and in_tile(W, tgt)):
        bad.append(('outside tile', line[:80])); continue
    # ends: (polygon, tile) at tile a and at tile b; for a == b try both orders
    orders = [(f, W)] if a != b else [(f, W), (W, f)]
    if a != b and src == b:
        orders = [(W, f)]
    ok = False
    for Pa, Pb in orders:
        for ca, cb, r in boxes.get((a, b), []):
            da, db = disp(Pa, a, ca), disp(Pb, b, cb)
            if da <= F(r, U) and db <= F(r, U):
                ok = True
                key = (a, b, ca, cb, r); m = reach.get(key, (0, 0))
                reach[key] = (max(m[0], da), max(m[1], db))
                break
        if ok:
            break
    if not ok:
        bad.append(('uncovered', line[:100]))

box_pairs = set(boxes)
print(f'{name}: residual open pairs {len(open_pairs)}, box tile pairs {len(box_pairs)}, '
      f'same set {open_pairs == box_pairs}, products {nprod}, uncovered {len(bad)}')
if open_pairs != box_pairs:
    print('  only in residual:', sorted(open_pairs - box_pairs))
    print('  only in boxes:', sorted(box_pairs - open_pairs))
for b in bad[:5]:
    print('  BAD', *b)
unused = [k for (a, b), L in boxes.items() for (ca, cb, r) in L if (a, b, ca, cb, r) not in reach]
print(f'  boxes used {len(reach)}, boxes never needed {len(unused)}')
tight = sum(1 for (a, b, ca, cb, r), (da, db) in reach.items() if -(-max(da, db) * U // 1) == r)
print(f'  boxes whose radius equals ceil(65536 * reached displacement): {tight} of {len(reach)}')
for (a, b, ca, cb, r), (da, db) in sorted(reach.items())[:4]:
    print(f'  box {a} {b} {ca} {cb} r={r}/65536: reached {da} and {db}')
print('RESULT', name, 'PASS' if (open_pairs == box_pairs and not bad) else 'FAIL')
