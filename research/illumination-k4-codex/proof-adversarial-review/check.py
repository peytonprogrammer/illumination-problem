"""Exact fixed-geometry audit, independently reconstructed from the attached PDF.

Uses only Python's standard library; performs no ray or room search.
"""
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent
PDF = ROOT.parents[1] / 'attachments/qkhk3S/proof-to-send.pdf'
text = subprocess.check_output(['pdftotext', '-layout', str(PDF), '-'], text=True)
coordinates = lambda s: [tuple(map(int, p)) for p in re.findall(r'\((-?\d+),\s*(-?\d+)\)', s)]
start = text.index('(-1,-1)')
cycle = coordinates(text[start:text.index('Dashed seams', start)])
start = text.index('lower-left corners are')
cells = set(coordinates(text[start:text.index('Its two smooth', start)]))
assert len(cycle) == 22 and len(cells) == 5


def boundary(cells):
    edges = set()
    for x, y in cells:
        vertices = [(x,y), (x+1,y), (x+1,y+1), (x,y+1)]
        for a, b in zip(vertices, vertices[1:] + vertices[:1]):
            if (b,a) in edges:
                edges.remove((b,a))
            else:
                edges.add((a,b))
    outgoing, incoming = defaultdict(list), Counter()
    for a, b in edges:
        outgoing[a].append(b)
        incoming[b] += 1
    assert all(len(v) == 1 for v in outgoing.values())
    assert all(n == 1 for n in incoming.values())
    a = min(outgoing)
    vertices = []
    while a not in vertices:
        vertices.append(a)
        a = outgoing[a][0]
    assert a == vertices[0] and len(vertices) == len(edges)
    # Unit grid edges can cross only at their endpoints. The preceding degree,
    # uniqueness, and single-cycle checks establish a simple boundary, no holes.
    corners = []
    signs = {}
    for i, b in enumerate(vertices):
        a, c = vertices[i-1], vertices[(i+1) % len(vertices)]
        cross = (b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])
        if cross:
            corners.append(b)
            signs[b] = cross
    return vertices, corners, signs


def census(cells):
    incidence = Counter()
    for x,y in cells:
        for dx,dy in [(0,0),(1,0),(0,1),(1,1)]:
            incidence[(x+dx,y+dy)] += 1
    vertices, corners, signs = boundary(cells)
    interior = {v for v,n in incidence.items() if n == 4}
    assert set(incidence) == set(vertices) | interior
    return {
        'unit_squares': len(cells),
        'perimeter': len(vertices),
        'walls': len(corners),
        'convex_corners': sorted(v for v,s in signs.items() if s > 0),
        'reflex_corners': sorted(v for v,s in signs.items() if s < 0),
        'smooth_integer_points': sorted(set(vertices) - set(corners)),
        'interior_integer_points': sorted(interior),
    }


copies = [cells, {(x,-y-1) for x,y in cells}, {(3-x,-y-1) for x,y in cells}]
assert all(not (copies[i] & copies[j]) for i,j in [(0,1),(0,2),(1,2)])
q = set.union(*copies)
pv, pc, ps = boundary(cells)
qv, qc, qs = boundary(q)
assert len(qc) == 22
k = qc.index(cycle[0])
assert qc[k:] + qc[:k] == cycle
cp, cq = census(cells), census(q)
assert len(cp['convex_corners']) == 7 and len(cp['reflex_corners']) == 3
assert cp['interior_integer_points'] == []
assert cp['smooth_integer_points'] == [(0,0), (2,-2)]
assert cq['interior_integer_points'] == [(0,0), (2,2)]


def intersection_bounds(a,b):
    x0, y0 = max(a[0],b[0]), max(a[1],b[1])
    x1, y1 = min(a[0]+1,b[0]+1), min(a[1]+1,b[1]+1)
    return (x0,y0,x1,y1) if x0 <= x1 and y0 <= y1 else None


pair_contacts = {}
for i,j in [(0,1),(0,2),(1,2)]:
    contacts = sorted({v for a in copies[i] for b in copies[j]
                       if (v := intersection_bounds(a,b)) is not None})
    if (i,j) == (0,1):
        assert all(y0 == y1 == 0 and -1 <= x0 <= x1 <= 1 for x0,y0,x1,y1 in contacts)
        assert (-1,0,0,0) in contacts and (0,0,1,0) in contacts
    elif (i,j) == (1,2):
        assert all(x0 == x1 == 2 and 1 <= y0 <= y1 <= 3 for x0,y0,x1,y1 in contacts)
        assert (2,1,2,2) in contacts and (2,2,2,3) in contacts
    else:
        assert not contacts
    pair_contacts[f'{i}-{j}'] = contacts


maps = [lambda v:v, lambda v:(v[0],-v[1]), lambda v:(4-v[0],-v[1])]
corner_preimages = defaultdict(list)
for i, f in enumerate(maps):
    for v in pc:
        w = f(v)  # Each map is its own inverse.
        corner_preimages[w].append({'copy':i,'base_corner':v,'type':'convex' if ps[v]>0 else 'reflex'})
endpoints = {(-1,0), (1,0), (2,1), (2,3)}
assert set(corner_preimages) == set(qc) | endpoints
assert all(len(corner_preimages[v]) == 1 for v in qc)
assert all(len(corner_preimages[v]) == 2 for v in endpoints)
assert all(a['type']=='convex' for v in endpoints for a in corner_preimages[v])
assert all(v in qc for v,items in corner_preimages.items() if any(a['type']=='reflex' for a in items))
assert endpoints <= set(cq['smooth_integer_points'])

# Diagonal matrices represented by their diagonal entries. This is a symbolic
# identity for every velocity, not a finite numerical direction sample.
mul = lambda *ms: tuple(__import__('math').prod(m[k] for m in ms) for k in range(2))
derivatives = [(1,1),(1,-1),(-1,-1)]
seam_checks = []
for i,j,seam,wall,ends in [(0,1,(1,-1),(-1,1),[(-1,0),(1,0)]),
                            (1,2,(-1,1),(1,-1),[(2,1),(2,3)])]:
    for a,b in [(i,j),(j,i)]:
        assert mul(derivatives[b], derivatives[a]) == seam
        assert mul(derivatives[b], wall, derivatives[a]) == (-1,-1)
        seam_checks.append({'from':a,'to':b,'ordinary_seam_matrix':seam,
                            'endpoint_matrix':(-1,-1),'endpoints':ends})
mark_preimages = {name: sorted({f(v) for f in maps}) for name,v in [('a',(0,0)),('b',(2,-2))]}
assert mark_preimages == {'a':[(0,0),(4,0)],'b':[(2,-2),(2,2)]}

result = {'status':'PASS','pdf_sha256':sha256(PDF.read_bytes()).hexdigest(),
          'source':'Coordinates extracted directly from attached PDF; no prior geometry or checker imports.',
          'base':cp,'room':cq,'cycle_matches_pdf':True,'pair_contacts':pair_contacts,
          'base_corner_incidences':sum(map(len,corner_preimages.values())),
          'room_corner_preimages':len(qc),
          'endpoint_preimages':{str(v):corner_preimages[v] for v in sorted(endpoints)},
          'symbolic_seam_transitions':seam_checks,'mark_preimages':mark_preimages,
          'scope':'Finite geometry and symbolic reflection identities only; analytic proof reviewed separately.'}
(ROOT/'check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
