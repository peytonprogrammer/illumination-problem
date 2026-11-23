"""d72: weakened form W2 (chain of two cylinders through a regular lattice-point lift Z~):
some direction v1 has S~, Z~ in one open cylinder and some v2 has Z~, T~ in one open cylinder.
Directions max(|p|,|q|) <= H (a positive answer is exact; a negative one is H-bounded).
Usage: python3 -B chain.py H ROOM:Sx,Sy:Tx,Ty ..."""
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cyl  # noqa: E402

H = int(sys.argv[1])
rooms = dict(cyl.rooms())
for a in sys.argv[2:]:
    t0 = time.process_time()
    nm, s, t = a.split(':')
    S = tuple(map(int, s.split(',')))
    T = tuple(map(int, t.split(',')))
    O = cyl.Origami(set(map(tuple, rooms[nm])))
    N = len(O.sq)
    ss = [i for i in range(N) if O.ll[i] == S]
    ts = [i for i in range(N) if O.ll[i] == T]
    zS, zT = {}, {}
    for v in cyl.directions(H):
        r, u = cyl.act(O.r, O.u, cyl.word(*v))
        Dc = cyl.Decomp(O, r, u)
        for z in range(N):
            if O.marked[z]:
                continue
            if any(Dc.cc(x, z) for x in ss):
                zS.setdefault(z, v)
            if any(Dc.cc(z, y) for y in ts):
                zT.setdefault(z, v)
    common = sorted(set(zS) & set(zT))
    w = [(O.ll[z], O.sq[z][1], zS[z], zT[z]) for z in common[:3]]
    print(nm, S, T, 'Z reachable from S', len({O.ll[z] for z in zS}), 'from T', len({O.ll[z] for z in zT}),
          'chain lifts', len(common), 'examples (Z, sheet, v1, v2)', w, 'CPU %.1f s' % (time.process_time() - t0), flush=True)
