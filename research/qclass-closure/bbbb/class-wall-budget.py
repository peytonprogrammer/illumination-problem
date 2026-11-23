"""Read only the twelve archived parity-W24 polygons and two named orthogonal controls."""
import json
import re
from collections import Counter
from pathlib import Path

context = Path(__file__).resolve().parents[2]
colors = [(0, 0), (1, 1), (0, 1), (1, 0)]


def parity(point):
    return tuple(x % 2 for x in point)


def incident(vertices, selected):
    return {j for j, p in enumerate(vertices)
            if p in selected or vertices[(j+1) % len(vertices)] in selected}


def site(vertices, p):
    """Exact winding-number test with an explicit boundary case."""
    x, y = p
    winding = 0
    for (a, b), (c, d) in zip(vertices, vertices[1:] + vertices[:1]):
        cross = (c-a)*(y-b) - (d-b)*(x-a)
        if cross == 0 and min(a,c) <= x <= max(a,c) and min(b,d) <= y <= max(b,d):
            return 'boundary'
        winding += (b <= y < d and cross > 0) - (d <= y < b and cross < 0)
    return 'interior' if winding else 'outside'


for i in range(12):
    path = context / f'illumination-k4-codex/global-route-review/inputs/parity-W24-{i}.json'
    vertices = [tuple(v) for v in json.loads(path.read_text())['vertices']]
    counts = Counter(map(parity, vertices))
    assert [counts[c] for c in colors] == [7, 8, 5, 4]
    for x in range(min(p[0] for p in vertices), max(p[0] for p in vertices)+1):
        for y in range(min(p[1] for p in vertices), max(p[1] for p in vertices)+1):
            if parity((x,y)) != (0,0) and site(vertices,(x,y)) != 'outside':
                assert (x,y) in vertices
    odd = incident(vertices, {v for v in vertices if parity(v)==(1,1)})
    mixed = incident(vertices, {v for v in vertices if sum(parity(v))==1})
    assert (len(odd), len(mixed), len(odd & mixed), len(odd | mixed)) == (16,17,9,24)
print('W24-0 through W24-11 (including Castro -5): 16 + 17 - 9 = 24 incident walls each')

paper = context / 'illumination-publication/repository/preprints/twenty-two-wall/manuscript.tex'
outline = next(line for line in paper.read_text().splitlines()
               if line.startswith(r'  \draw[outline,very thick] (-1,-1)--(0,-1)--'))
vertices = [tuple(map(int,coords)) for coords in re.findall(r'\((-?\d+),(-?\d+)\)', outline)]
stops = {(0,-1),(0,1),(1,-2),(1,-1),(1,1),(1,2),(3,1),(3,2),(4,1)}
edges = [incident(vertices, {v for v in stops if parity(v)==c}) for c in colors[1:]]
assert list(map(len,edges)) == [4,6,6] and len(set.union(*edges)) == 16
print('R22: 9 indispensable reflex stops, 16 distinct incident walls')

columns = [range(6), (2,3), (2,3), range(6), range(6), (2,3), (2,), range(3)]
cells = {(x,y) for x, col in enumerate(columns) for y in col}
stars = Counter((x+i,y+j) for x,y in cells for i,j in [(0,0),(0,1),(1,0),(1,1)])
print('cov4181 stars by parity, ordered convex / smooth / reflex / interior')
for c in colors:
    print(c,[sum(parity(p)==c and n==j for p,n in stars.items()) for j in range(1,5)])
