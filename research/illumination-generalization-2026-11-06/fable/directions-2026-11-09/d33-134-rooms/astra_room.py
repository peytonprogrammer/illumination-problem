"""Astra's 17-wall, 40-tile (1,3,4) room (d32-fold-minimum/astra-r2.md).
Geom frame = Astra frame rotated by pi/8 and scaled by r, so C_j -> r zeta^(2j+1).
M = 0 carries the half-octagon (C at zeta^1,3,5,7); S = 2 r zeta, T = 2 r zeta^5."""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'd7-review'))
from geom import Triangle, Tile, Room, star
from shoot import Tracer, find_path_mid
tri = Triangle(8, 3); F = tri.F
S = F.smul(2, F.mul(F.z(1), tri.r)); T = F.smul(2, F.mul(F.z(5), tri.r))
H = [Tile(tri, +1, k, F.zero) for k in (0, 2, 4, 6)] + [Tile(tri, -1, k, F.zero) for k in (2, 4, 6, 8)]
tiles = H + star(tri, S) + star(tri, T)
room = Room(tri, tiles); ok = room.analyze(); print('valid', ok, getattr(room, 'err', None))
f = lambda p: tuple(round(x, 4) for x in (F.cval(p).real, F.cval(p).imag))
print('tiles', len(tiles), 'W', room.W, room.summary(), 'clean', room.clean)
print('interior A', [f(p) for p in room.interiorA])
print('transparent C', [(f(p), 'int' if p not in room.bset else 'flat') for p in room.transparentE])
tr = Tracer(room); t0 = time.time()
for d in range(0, 5):
    r = tr.find_path(S, T, d); print('depth', d, r['found'], r['tried'], round(time.time() - t0), 's', flush=True)
    if r['found']: print('reflections', len(r['walls_hit']), 'walls', r['walls_hit'], 'image', f(r['image'])); break
else:
    for d in range(1, 4):
        r = find_path_mid(tr, S, T, room.transparentE, d); print('mid', d, r['found'], r['tried'], flush=True)
        if r['found']: print('reflections', len(r['walls_hit']), 'mid', f(r['mid'])); break
