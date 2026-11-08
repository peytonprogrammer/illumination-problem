"""Two hand-derived five/eight-reflection paths; no discovery search."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import runpy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / "triangle-composition/check.json"
CAPS = ROOT / "zero-surplus-L/guard-incidence-check.json"
GUARD = ROOT / "lower-bound-proof-audit/full-replay/guard-checker.py"
fixture = json.loads(SOURCE.read_text())["controls"]["unresolved_Bquarter"]
vertices = [tuple(map(F, p)) for p in fixture["vertices"]]
room = {tuple(sorted(map(tuple, t))) for t in fixture["triangles"]}
path = [(F(0), F(0)), (F(1), F(-4, 3)), (F(1, 2), F(-2)),
        (F(0), F(-4, 3)), (F(3), F(8, 3)), (F(11, 4), F(3)),
        (F(2), F(2))]
sub = lambda a, b: (a[0]-b[0], a[1]-b[1])
cross = lambda a, b: a[0]*b[1]-a[1]*b[0]
dot = lambda a, b: a[0]*b[0]+a[1]*b[1]


def interior(p, walls):
    inside = False
    for a, b in walls:
        e, v = sub(b, a), sub(p, a)
        assert cross(e, v) or not (min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
                                      and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))
        if (a[1] > p[1]) != (b[1] > p[1]):
            x = a[0] + (p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])
            if p[0] < x:
                inside = not inside
    return inside


def verify_boundary(path, vertices):
    walls = list(zip(vertices, vertices[1:]+vertices[:1]))
    assert interior(path[0], walls) and interior(path[-1], walls)
    for prev, p, nxt in zip(path, path[1:], path[2:]):
        matches = [(a, b) for a, b in walls
                   if cross(sub(b, a), sub(p, a)) == 0
                   and 0 < dot(sub(p, a), sub(b, a)) < dot(sub(b, a), sub(b, a))]
        assert len(matches) == 1, ("non-strict contact", p)
        a, b = matches[0]
        e, v, out = sub(b, a), sub(p, prev), sub(nxt, p)
        reflected = tuple(2*dot(v, e)*e[k]/dot(e, e)-v[k] for k in [0, 1])
        assert cross(reflected, out) == 0 and dot(reflected, out) > 0
    for p, q in zip(path, path[1:]):
        assert interior(tuple((p[k]+q[k])/2 for k in [0, 1]), walls)
        v = sub(q, p)
        for a, b in walls:
            w, ap = sub(b, a), sub(a, p)
            den = cross(v, w)
            if den:
                t, s = cross(ap, w)/den, cross(ap, v)/den
                assert not (0 < t < 1 and 0 <= s <= 1), ("earlier wall", p, q, a, b)
            elif cross(ap, v) == 0:
                aa, bb = dot(ap, v)/dot(v, v), dot(sub(b, p), v)/dot(v, v)
                assert max(min(aa, bb), F(0)) >= min(max(aa, bb), F(1))

def polygon(triangles):
    edges = set()
    for triangle in triangles:
        a,b,c = triangle
        if cross(sub(b,a),sub(c,a)) < 0:
            b,c = c,b
        for u,v in [(a,b),(b,c),(c,a)]:
            if (v,u) in edges:
                edges.remove((v,u))
            else:
                edges.add((u,v))
    outgoing = {a:b for a,b in edges}
    assert len(outgoing) == len(edges)
    assert len(set(outgoing.values())) == len(outgoing)
    start = min(outgoing)
    cycle = [start]
    p = outgoing[start]
    while p != start:
        assert p not in cycle
        cycle.append(p)
        p = outgoing[p]
    assert len(cycle) == len(edges)
    return [p for i,p in enumerate(cycle)
            if cross(sub(p,cycle[i-1]),sub(cycle[(i+1)%len(cycle)],p))]


def ledger(triangles, vertices):
    points = set().union(*map(set,triangles))
    Q = J = sN = 0
    fullA = []
    for p in points:
        m = sum(p in t for t in triangles)
        if p[0]%2 == p[1]%2 == 0:
            if m == 8:
                fullA.append(p)
            else:
                Q += 3 if m == 4 else m
        elif p[0]%2 == p[1]%2 == 1:
            J += m == 8
            sN += m == 4
        else:
            J += m == 4
            sN += m == 2
    assert set(fullA) == {(0,0),(2,0),(2,2)}
    result = dict(W=len(vertices),Q=Q,J=J,sN=sN,k=J+sN,Delta=Q+sN-8)
    assert result['W'] == 20 and result['k'] == 6 and result['Delta'] == 4
    return result


checker = runpy.run_path(str(GUARD))
H = set().union(*(checker["incident"](tuple(map(F, p)))
                  for p in [(0, 0), (2, 0), (2, 2)]))
square = {tuple(sorted(t)) for t in [((0, -2), (1, -2), (1, -1)),
                                     ((0, -2), (0, -1), (1, -1))]}
caps = {n: tuple(sorted(map(tuple, t)))
        for n, t in json.loads(CAPS.read_text())["cap_options"].items()}
room8 = (room - {caps['T-']}) | {caps['T+']}
vertices8 = [tuple(map(F,p)) for p in polygon(room8)]
path8 = [(F(0),F(0)),(F(1),F(-5,4)),(F(2,5),F(-2)),
         (F(0),F(-3,2)),(F(3),F(9,4)),(F(2),F(7,2)),
         (F(20,9),F(34,9)),(F(2),F(18,5)),(F(3),F(14,5)),(F(2),F(2))]
rows = {}
geometry = {}
for name,P,V,R,direction,parameter,interval,target in [
    ('five',path,vertices,room,[3,-4],'3/4',['5/7','5/6'],'x=8-8d at y=2'),
    ('eight',path8,vertices8,room8,[4,-5],'4/5',['7/9','5/6'],'x=12-8/d at y=2')]:
    verify_boundary(P,V)
    # Replay backwards too, using the same physical boundary predicates.
    verify_boundary(list(reversed(P)),V)
    U,Z = checker['path_requirements'](P)
    assert U <= R and not Z & R
    required = H | square | ({caps['T+']} if name == 'eight' else set())
    assert U <= required
    blockers = sorted(n for n,t in caps.items() if t in Z)
    assert blockers == (['B-','E+','T+'] if name == 'five' else ['B-','E+','T-'])
    rows[name] = dict(reflections=len(P)-2,initial_direction=direction,
                     path=[[str(x) for x in p] for p in P],
                     required_triangles=sorted(U),forbidden_triangles=sorted(Z),
                     required_outside_core=sorted(U-H),ordinary_cap_blockers=blockers,
                     parameter=parameter,open_itinerary_interval=interval,
                     target_formula=target,fixture_ledger=ledger(R,V),
                     reverse_boundary_check='PASS')
    geometry[name] = dict(vertices=[[str(x) for x in p] for p in V],triangles=sorted(R),
                          ledger=rows[name]['fixture_ledger'])
result = dict(status='PASS',scope='Two hand-derived fixed paths and two specifically prescribed controls. Independent physical boundary/interior/reflection checks and reused universal tile guards; no room/direction/word scan.',
              paths=rows,inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in [SOURCE,CAPS,GUARD]})
(HERE/'bottom-square-check.json').write_text(json.dumps(result,indent=2)+'\n')
(HERE/'bottom-square-geometry.json').write_text(json.dumps(geometry,indent=2)+'\n')
print('PASS: five/eight reflections, actual endpoints, strict first hits, reverse replay, exact guards, W20/k6/Delta4')
