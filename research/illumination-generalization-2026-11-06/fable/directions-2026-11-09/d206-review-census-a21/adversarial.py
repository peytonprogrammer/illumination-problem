"""Hand-made near-dark cases and the 22-wall control against verify_plane.c."""
import subprocess, math, json
from tracer import Room
def vp(cells, s, d, m, t):
    q = [len(cells)] + [c + 1 for xy in cells for c in xy] + [s[0]+1, s[1]+1, d[0], d[1], m, t[0]+1, t[1]+1]
    return ' '.join(map(str, q))
out = {}
# 1. L room (4x4 minus top-right 2x2): straight segment (3,1)->(1,3) passes reflex corner (2,2).
L = [(x, y) for x in range(4) for y in range(4) if not (x >= 2 and y >= 2)]
R = Room(L)
cases = [(L, (3, 1), (-1, 1), 2, (1, 3)),    # through reflex corner: must be 0
         (L, (1, 3), (1, -1), 2, (3, 1)),    # reverse: must be 0
         (L, (1, 1), (1, 1), 1, (2, 2)) if False else (L, (2, 1), (-1, 1), 1, (1, 2)),  # legit: must be 1
        ]
# 2. 3x3 square, diagonal into convex corner (3,3) then "back" to (1,1)/(2,2): must be 0
Sq = [(x, y) for x in range(3) for y in range(3)]
cases += [(Sq, (1, 1), (1, 1), 4, (1, 1)) if False else (Sq, (2, 2), (1, 1), 2, (2, 2)) if False else (Sq, (1, 2), (1, 1), 2, (1, 2)),
          (Sq, (1, 1), (1, 1), 3, (2, 2))]
# 3. 2x? corridor: grazing path along a wall line is impossible from interior; axis bounce legit
cases += [(Sq, (1, 1), (0, 1), 3, (1, 2))]
queries = [vp(*c) for c in cases]
tr = []
for cells, s, d, m, t in cases:
    ok, first, end = Room(cells).trace(s, d, m)
    tr.append(int(ok and end == t))
got = list(map(int, subprocess.run(['./vp_harness'], input='\n'.join(queries)+'\n', capture_output=True, text=True).stdout.split()))
out['hand_cases'] = [dict(case=str(c[1:]), verify_plane=g, tracer=e) for c, g, e in zip(cases, got, tr)]
# 4. Control: 22-wall area-15 room, pair (1,3)-(3,5). All primitive directions p+q<=40, all m<=600.
C = [(0,2),(0,3),(1,1),(1,2),(1,3),(1,4),(2,0),(2,1),(2,4),(2,5),(3,4),(3,5),(4,3),(4,4),(5,3)]
RC = Room(C)
from rooms import walls, has_hole, has_pinch
out['control_room'] = dict(walls=walls(set(C)), hole=has_hole(tuple(C)), pinch=has_pinch(set(C)), marks=sorted(RC.marks))
S, T = (1, 3), (3, 5)
dirs = [(sx*p, sy*q) for s in range(1, 41) for p in range(s+1) for q in [s-p] if math.gcd(p, q) == 1 for sx in (1, -1) for sy in (1, -1)]
dirs = sorted(set(dirs))
qs = []
for d in dirs:
    for a, b in ((S, T), (T, S)):
        for m in range(1, 61):
            qs.append(vp(C, a, d, m, b))
got = list(map(int, subprocess.run(['./vp_harness'], input='\n'.join(qs)+'\n', capture_output=True, text=True).stdout.split()))
out['control_verify_plane'] = dict(queries=len(got), accepted=sum(got))
# tracer: every direction with p+q<=40, both orientations, up to time 60: first time hitting target?
hits = 0
for d in dirs:
    for a, b in ((S, T), (T, S)):
        ok, first, end = RC.trace(a, d, 60, b)
        if first is not None: hits += 1
out['control_tracer'] = dict(rays=2*len(dirs), tmax=60, reached_target_before_corner=hits)
print(json.dumps(out, indent=1))
