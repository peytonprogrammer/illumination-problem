"""Reconstruct and check Wolecki's Figure 1 on its integer triangle grid."""
import collections
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

root = ET.parse(Path(__file__).with_name('wolecki-22.svg')).getroot()
triangles = []
scale = 56.69363
for element in root.iter('{http://www.w3.org/2000/svg}path'):
    if element.get('fill-opacity') != '.1':
        continue
    tokens = re.findall(r'[MHVZ]|-?\d+(?:\.\d+)?', element.get('d'))
    points = []
    i = 0
    command = None
    x = y = 0
    while i < len(tokens):
        if tokens[i] in {'M', 'H', 'V', 'Z'}:
            command = tokens[i]
            i += 1
        if command == 'Z':
            break
        if command == 'M':
            x, y = float(tokens[i]), float(tokens[i+1])
            i += 2
        elif command == 'H':
            x = float(tokens[i]); i += 1
        elif command == 'V':
            y = float(tokens[i]); i += 1
        point = (round(x / scale), round(y / scale))
        assert max(abs(x / scale - point[0]), abs(y / scale - point[1])) < 1e-6
        points.append(point)
    assert len(points) == 3
    lengths = sorted((a[0]-b[0])**2+(a[1]-b[1])**2 for a,b in zip(points,points[1:]+points[:1]))
    assert lengths == [1,1,2]
    triangles.append(tuple(points))
assert len({tuple(sorted(t)) for t in triangles}) == len(triangles)

edges = collections.defaultdict(list)
incident = collections.Counter()
for index, triangle in enumerate(triangles):
    incident.update(triangle)
    for a,b in zip(triangle,triangle[1:]+triangle[:1]):
        edges[tuple(sorted((a,b)))].append(index)
assert all(len(v) <= 2 for v in edges.values())
adjacency = collections.defaultdict(set)
for a,b in (e for e,owners in edges.items() if len(owners) == 1):
    adjacency[a].add(b); adjacency[b].add(a)
print("boundary degree exceptions", {str(k):sorted(v) for k,v in adjacency.items() if len(v)!=2})

interior_a = sorted(p for p in incident if p not in adjacency)
wall_paths = [p for p in root.iter('{http://www.w3.org/2000/svg}path') if p.get('stroke') == '#b39999']
assert len(wall_paths) == 22
assert interior_a == [(0,0),(2,2)]
assert all(incident[p] == 8 for p in interior_a)
assert all(p in adjacency for p in incident if not(p[0]%2 == 0 and p[1]%2 == 0))
# Check the triangles have connected interior by shared-edge adjacency.
graph = collections.defaultdict(set)
for owners in edges.values():
    if len(owners) == 2:
        a,b = owners; graph[a].add(b); graph[b].add(a)
seen = {0}; pending = [0]
while pending:
    for b in graph[pending.pop()]:
        if b not in seen:
            seen.add(b); pending.append(b)
assert len(seen) == len(triangles)
result = dict(triangles=len(triangles), drawn_wall_segments=len(wall_paths),
    atomic_boundary_edges=sum(len(o)==1 for o in edges.values()),
    interior_A=interior_a,
    boundary_degree_exceptions={str(k):len(v) for k,v in adjacency.items() if len(v)!=2},
    euler=len(incident)-len(edges)+len(triangles),
    caveat='Integer reconstruction from rounded SVG. Connected interior verified. Boundary has a point contact at (2,0), so do not silently classify it as a Jordan polygon. No new bound proved.')
print(json.dumps(result,indent=2))
