"""Evaluate prescribed, adjacent two-tail twists algebraically on the named cross7."""
from collections import Counter
from itertools import combinations, permutations, product
from math import gcd, lcm
from pathlib import Path
import sys

archive = Path(__file__).resolve().parents[2] / 'illumination-generalization-2026-11-06/fable/directions-2026-11-09'
sys.path.insert(0,str(archive/'d10-mechanisms'))
import roomtools as rt

cells = {(x,y) for x in range(-7,7) for y in range(-7,7) if -2<=x<2 or -2<=y<2}
sites = sorted(p for p in rt.lattice_points(cells) if rt.status(cells,p)== 'interior')
nominal = (0,0)
room,g = rt.room_tuple(cells,nominal)
parts = [p for p in rt.d4.all_block_systems(g,96) if len(p) in (24,48)]
assert sorted(map(len,parts))==[24,48,48,48]
# One sheet per physical cell in lexicographic cell order, independent of origin.
def location(i):
    return room.tiles[room.faces[room.sheets[i]][0]]['key']


def partition_name(p):
    here = next(b for b in p if room.sheet_index[room.sheets[0]] in b)
    return str(len(p))+' '+str(sorted(location(i) for i in here))


def pair_keys(h):
    lookup = {v:(i,j,len(c)) for i,c in enumerate(rt.cycles(h)) for j,v in enumerate(c)}
    def key(x,y):
        i,j,n = lookup[x]
        l,k,m = lookup[y]
        return i,l,(j-k)%gcd(n,m)
    return key


def component_labels(a,d):
    labels = list(range(len(a)))
    for perm in (a,d):
        for cycle in rt.cycles(perm):
            old = {labels[i] for i in cycle}
            rep = min(old)
            labels = [rep if v in old else v for v in labels]
    return labels


def pencil_components(a, d, h, regular=False):
    """Entry (i,j) encodes all powers connecting the A-vertices of i and j."""
    orbits = rt.cycles(h)
    period = lcm(*(len(c) for c in orbits))
    full = (1 << period) - 1
    a_cycles, d_cycles = rt.cycles(a), rt.cycles(d)
    ai = {x:k for k,c in enumerate(a_cycles) for x in c}
    di = {x:k for k,c in enumerate(d_cycles) for x in c}
    size = len(a_cycles)
    incident = [[0]*len(d_cycles) for _ in a_cycles]
    for orbit in orbits:
        n = len(orbit)
        repetition = full // ((1 << n) - 1)
        for j,x in enumerate(orbit):
            for k,y in enumerate(orbit):
                if regular and (len(a_cycles[ai[x]]) != 2 or len(d_cycles[di[y]]) != 2):
                    continue
                incident[ai[x]][di[y]] |= repetition << ((k-j)%n)
    paths = [[0]*size for _ in a_cycles]
    for i in range(size):
        paths[i][i] = full
        for j in range(i):
            for left,right in zip(incident[i],incident[j]):
                paths[i][j] |= left & right
            paths[j][i] = paths[i][j]
    for k in range(size):
        for i in range(size):
            step = paths[i][k]
            if step:
                for j in range(size):
                    paths[i][j] |= step & paths[k][j]
    baseline = component_labels(a,d)
    assert regular or all(bool(paths[ai[i]][ai[j]] & 1)==(baseline[i]==baseline[j])
               for i in ai for j in ai)
    return lambda i,j: paths[ai[i]][ai[j]]


totals = {}
for blocks in parts+[[[i] for i in range(96)]]:
    name = partition_name(blocks)
    where = {i:b for b,block in enumerate(blocks) for i in block}
    counts = Counter()
    legal_pairs = set()
    for origin in product(range(2),repeat=2):
        rm,t = rt.room_tuple(cells,origin)
        assert all(tuple(a+b for a,b in zip(rm.tiles[rm.faces[f][0]]['key'],origin))==location(i)
                   for i,f in enumerate(rm.sheets))
        assert rt.d4.is_block_system(blocks,t)
        perms = [rt.induced(v,blocks) for v in t]
        pts = [p for p in sites if tuple(v%2 for v in p)==origin]
        marks = {p:{where[i] for lift in rt.lifts(rm,t,p,origin) for i in lift} for p in pts}
        for d in (1,2,3):
            base = component_labels(perms[0],perms[d])
            rules = []
            pencils = []
            cut = []
            for e in (d-1,d+1):
                if e not in (1,2,3): continue
                lo,hi = sorted((e,d))
                h = rt.mul(perms[lo],perms[hi])
                pencils.append(pencil_components(perms[0],perms[d],h))
                if len(blocks)==96:
                    cut.append(pencil_components(perms[0],perms[d],h,regular=True))
                key = pair_keys(h)
                accepted = {key(i,j) for c in rt.cycles(perms[d]) for i,j in permutations(c,2)}
                rules.append((key,accepted))
            for s,u in combinations(pts,2):
                counts['rows'] += 1
                pairs = list(product(marks[s],marks[u]))
                if cut and any(test(i,j) for test in cut for i,j in pairs):
                    legal_pairs.add((s,u))
                    counts["legal rows"] += 1
                if any(base[i]==base[j] for i,j in pairs):
                    counts['base'] += 1
                elif any(key(i,j) in acc for key,acc in rules for i,j in pairs):
                    counts['twist extra'] += 1
                else:
                    if any(test(i,j) for test in pencils for i,j in pairs):
                        counts['longer component'] += 1
                    else:
                        counts['miss'] += 1
                        print('residual',len(blocks),origin,d,s,u)
    assert counts['rows']==574*3
    if legal_pairs:
        counts["legal pairs"]=len(legal_pairs)
    totals[name]=counts
    print(name,dict(counts))
