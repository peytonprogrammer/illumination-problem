"""Exact cell incidence audit on the 34 frozen rooms; no trajectory operations."""
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

B = Path(__file__).resolve().parent

def cls(p):
    return (p[0] & 1) + (p[1] & 1)

def triangles(vertices):
    def inside(x, y):
        value = False
        for (ax, ay), (bx, by) in zip(vertices, vertices[1:] + vertices[:1]):
            if (ay > y) != (by > y) and x < ax + F(y - ay) * (bx - ax) / (by - ay):
                value = not value
        return value
    result = []
    for x in range(min(p[0] for p in vertices), max(p[0] for p in vertices)):
        for y in range(min(p[1] for p in vertices), max(p[1] for p in vertices)):
            square = [(x,y), (x+1,y), (x+1,y+1), (x,y+1)]
            k = next(i for i,p in enumerate(square) if cls(p) == 0)
            a, b = square[k], square[(k+2) % 4]
            for c in (square[(k+1) % 4], square[(k+3) % 4]):
                if inside(F(a[0]+b[0]+c[0], 3), F(a[1]+b[1]+c[1], 3)):
                    result.append((a,b,c))
    return result

def audit(room):
    tris = triangles(list(map(tuple, room['vertices'])))
    stars = defaultdict(list)
    edges = defaultdict(list)
    for i, tri in enumerate(tris):
        stars[tri[0]].append(i)
        for j in range(3):
            edges[frozenset((tri[j], tri[(j+1)%3]))].append(i)
    indeg = Counter()
    outdeg = Counter()
    undirected = defaultdict(list)
    portals = []
    for edge, indices in edges.items():
        if len(indices) != 2 or sorted(cls(p) for p in edge) != [1,2]:
            continue
        c = next(p for p in edge if cls(p) == 1)
        centers = [tris[i][0] for i in indices]
        counts = [sum(tris[i][2] == c for i in stars[a]) for a in centers]
        assert sorted(counts) == [1,2], (room['tag'], edge, counts)
        source, target = centers[counts.index(2)], centers[counts.index(1)]
        outdeg[source] += 1
        indeg[target] += 1
        undirected[source].append(target)
        undirected[target].append(source)
        portals.append({'C': c, 'B':next(p for p in edge if cls(p) == 2), 'from': source, 'to': target})
    seen = set()
    stack = [next(iter(stars))]
    while stack:
        a = stack.pop()
        if a not in seen:
            seen.add(a)
            stack.extend(undirected[a])
    assert len(seen) == len(stars) and len(portals) == len(stars)-1
    cut_rows = []
    for portal in portals:
        source, target = tuple(portal['from']), tuple(portal['to'])
        upstream = {source}
        queue = [source]
        for a in queue:
            for c in undirected[a]:
                if frozenset((a,c)) == frozenset((source,target)):
                    continue
                if c not in upstream:
                    upstream.add(c)
                    queue.append(c)
        c, bp = tuple(portal['C']), tuple(portal['B'])
        up_c = sum(tri[0] in upstream and tri[2] == c for tri in tris)
        down_c = sum(tri[0] not in upstream and tri[2] == c for tri in tris)
        assert (up_c, down_c) == (2,1)
        up_b = sum(tri[0] in upstream and tri[1] == bp for tri in tris)
        down_b = sum(tri[0] not in upstream and tri[1] == bp for tri in tris)
        assert up_b > 0 and down_b > 0
        cut_rows.append({'C':c, 'B':bp, 'up_C_triangles':up_c,
                         'down_C_triangles':down_c, 'up_B_triangles':up_b,
                         'down_B_triangles':down_b, 'downstream_raw':down_b != 4})
    fan_rows = []
    for a, indices in sorted(stars.items()):
        m = len(indices)
        q = sum(len(edges[frozenset((a, tris[i][1]))]) == 1 for i in indices)
        c_counts = Counter(tris[i][2] for i in indices)
        h = sum(n == 2 for n in c_counts.values())
        e = sum(n == 1 for n in c_counts.values())
        full = m == 8
        assert h == outdeg[a]
        assert indeg[a] <= e
        if full:
            assert q == e == indeg[a] == 0 and h == 4
        else:
            assert 2*h == m-2+q and e == 2-q
        fan_rows.append({'A': a, 'triangles': m, 'AB_ends': q,
                         'internal_C': h, 'endpoint_C': e,
                         'in': indeg[a], 'out': outdeg[a], 'full': full})
    I = sum(r['full'] for r in fan_rows)
    D = sum(r['AB_ends'] for r in fan_rows)
    V = len(stars)
    full_centers = [tuple(r['A']) for r in fan_rows if r['full']]
    full_pairs = []
    for i,a in enumerate(full_centers):
        for c in full_centers[i+1:]:
            distance = max(abs(a[j]-c[j]) for j in (0,1))
            assert distance >= 4
            full_pairs.append({'A1':a, 'A2':c, 'chebyshev_distance':distance})
    sources = sum(r['in'] == 0 for r in fan_rows)
    mergers = sum(r['in'] == 2 for r in fan_rows)
    sinks = [r for r in fan_rows if r['out'] == 0]
    assert len(tris)+D+2*I == 4*V-2
    assert mergers == sources-1 and sources >= I
    assert all(r['AB_ends'] == 0 for r in fan_rows if r['in'] == 2)
    assert all((r['triangles'],r['AB_ends']) in [(1,1),(2,0)] for r in sinks)
    right_mergers = []
    for fan in fan_rows:
        if fan['in'] != 2 or fan['triangles'] != 2:
            continue
        a = tuple(fan['A'])
        own = [tris[i] for i in stars[a]]
        bp = own[0][1]
        assert all(tri[1] == bp for tri in own)
        incoming = [tuple(edge['from']) for edge in portals if tuple(edge['to']) == a]
        assert len(incoming) == 2
        assert not all(len(stars[c]) == 8 for c in incoming)
        counts = [sum(tris[i][1] == bp for i in stars[c]) for c in incoming]
        assert all(n in (1,2) for n in counts) and sum(counts) >= 3
        b_order = sum(tri[1] == bp for tri in tris)
        assert b_order in (5,6,7)
        if b_order == 5:
            incident_centers = {tri[0] for tri in tris if tri[1] == bp}
            assert len(incident_centers) == 3
            assert all(len(stars[c]) > 1 for c in incident_centers)
        right_mergers.append({'A':a, 'B':bp, 'incoming_B_counts':counts,
                              'B_angle_pi_over_4':b_order,
                              'sector_window_pi_over_4':sum(counts)-2})
    s,t = map(tuple, room['marked'])
    assert len(stars[s]) == len(stars[t]) == 8
    prev = {s: None}
    queue = [s]
    for a in queue:
        for b in undirected[a]:
            if b not in prev:
                prev[b] = a
                queue.append(b)
    path = [t]
    while path[-1] != s:
        path.append(prev[path[-1]])
    path.reverse()
    arrows = {(tuple(r['from']),tuple(r['to'])) for r in portals}
    path_mergers = [path[i] for i in range(1,len(path)-1)
                    if (path[i-1],path[i]) in arrows and (path[i+1],path[i]) in arrows]
    assert path_mergers
    return {'tag': room['tag'], 'T':len(tris), 'D_AB_segments':D,
            'I':I, 'V':V, 'E':len(portals), 'sources':sources,
            'mergers':mergers, 'sinks':len(sinks),
            'mark_path':path, 'mark_path_mergers':path_mergers,
            'fans':fan_rows, 'portals':portals, 'portal_cuts':cut_rows, 'right_angle_mergers':right_mergers, 'full_fan_pairs':full_pairs}

selection = json.loads((B/'inputs/holdouts/selection.json').read_text())
paths = [B/'inputs/holdouts'/f"{r['tag']}.json" for r in selection]
rows = [audit(json.loads(p.read_text())) for p in paths]
# This finite check covers each possible contiguous local angular sector,
# not rooms, event words or trajectory directions.
octants = [(0,0),(0,1),(1,1),(1,2),(2,2),(2,3),(3,3),(3,0)]
local = 0
for m in range(1,8):
    for start in range(8):
        chosen = [(start+j)%8 for j in range(m)]
        cs = Counter(octants[j][0] for j in chosen)
        bs = Counter(octants[j][1] for j in chosen)
        h = sum(n == 2 for n in cs.values())
        e = sum(n == 1 for n in cs.values())
        q = sum(n == 1 for n in bs.values())
        assert 2*h == m-2+q and e == 2-q
        local += 1
# B-star mask control: the merger occupies bits4,5; its two incoming
# neighbours supply bits3,6. This is a prescribed local incidence check.
right_masks = []
for mask in range(256):
    bits = [(mask >> j) & 1 for j in range(8)]
    if not all(bits[j] for j in (3,4,5,6)):
        continue
    if sum(bits[j] != bits[(j+1)%8] for j in range(8)) != 2:
        continue
    if sum(bits) == 4:
        continue
    left, right = bits[2]+bits[3], bits[6]+bits[7]
    assert sum(bits) in (5,6,7) and left+right >= 3
    right_masks.append({'mask':mask, 'B_triangles':sum(bits),
                        'incoming_counts':[left,right],
                        'window_pi_over_4':left+right-2})
assert len(right_masks) == 9
summary = {'frozen_rooms':len(rows), 'local_sectors':local,
           'full_fans':sum(r['I'] for r in rows),
           'portals':sum(r['E'] for r in rows),
           'all_count_identities_pass':True,
           'all_actual_mark_fan_paths_have_merger':True,
           'event_existence_proved':False,
           'portal_cut_audits':sum(len(r['portal_cuts']) for r in rows),
           'downstream_raw_cuts':sum(c['downstream_raw'] for r in rows for c in r['portal_cuts']),
           'all_upstream_cuts_create_smooth_C':True,
           'right_angle_merger_audits':sum(len(r['right_angle_mergers']) for r in rows),
           'prescribed_B_star_masks':len(right_masks),
           'full_fan_spacing_pair_audits':sum(len(r['full_fan_pairs']) for r in rows),
           'no_right_merger_has_two_full_incoming_fans':True}
out = {'status':'EXACT_DIRECTED_FAN_COUNTS_PASS', 'summary':summary,
       'rooms':rows, 'right_merger_local_masks':right_masks, 'input_sha256':{str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
       'scope':'Frozen cell incidence and 56 prescribed local sectors only. No unfolding permutations, billiard tracing, ray/event/word/direction discovery or orbit enumeration.'}
(B/'pocket-fan.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(summary,indent=2))
