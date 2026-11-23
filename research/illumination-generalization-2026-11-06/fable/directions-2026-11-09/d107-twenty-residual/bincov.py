"""D107: does the saved bin-pair list cover cert2's own residual for a bin-pair room?

Usage: python3 -B bincov.py ROOMFILE RESIDUAL GRID NAME

From cert2's products, build the forward bin relation F (side 0: f in tile a, W in tile b) and
the reverse relation R (side 1: f in b, W in a), using floor bins with the far side clamped
(16 x 16 per tile, u = 16*xbin + ybin), enclosing each polygon by its bounding-box bins.
A dark pair (S, T) has (bin S, bin T) in F and (bin T, bin S) in R, so it lies in F ∩ R^T.
Check: F ∩ R^T is inside the grid's PIX set (which the receipts cover, see pixchk.py).
Only distinct tiles are handled; the grid is read only as the object being compared.
"""
import sys

roomf, resf, gridf, name = sys.argv[1:5]
v = list(map(int, open(roomf).read().split()))
cells = [(v[2 + 2 * i], v[3 + 2 * i]) for i in range(v[0])]


def bins(tok, c):
    t = list(map(int, tok.split())); x0, y0 = cells[c]
    pts = [(t[i], t[i + 1], t[i + 2]) for i in range(0, len(t), 3)]
    def rng(k, o):
        lo = min(16 * (p[k] - o * p[2]) // p[2] for p in pts)
        hi = max(16 * (p[k] - o * p[2]) // p[2] for p in pts)
        assert 0 <= lo and hi <= 16
        return range(lo, min(hi, 15) + 1)
    return {16 * bx + by for bx in rng(0, x0) for by in rng(1, y0)}


F, R = {}, {}
for line in open(resf):
    if not line.startswith('PROD '):
        continue
    head, fs, ws = line.split('|')
    _, a, b, src = map(int, head.split()); assert a != b
    if src == a:
        s = F.setdefault((a, b), set())
        for u in bins(fs, a):
            for w in bins(ws, b):
                s.add((u, w))
    else:
        s = R.setdefault((a, b), set())
        for u in bins(fs, b):
            for w in bins(ws, a):
                s.add((w, u))  # transpose: (bin in a, bin in b)
pix = {}
for l in open(gridf):
    if l.startswith('PIX '):
        i, j, u, w = map(int, l.split()[1:]); pix.setdefault((i, j), set()).add((u, w))
need = {k: F[k] & R.get(k, set()) for k in F}
miss = sum(len(s - pix.get(k, set())) for k, s in need.items())
print(f'{name}: tile pairs with residual {sorted(need)}; F {sum(map(len, F.values()))}, '
      f'R {sum(map(len, R.values()))}, F∩R^T {sum(map(len, need.values()))}; '
      f'grid PIX {sum(map(len, pix.values()))} in {sorted(pix)}; F∩R^T outside PIX: {miss}')
print('RESULT', name, 'PASS' if miss == 0 else 'FAIL')
