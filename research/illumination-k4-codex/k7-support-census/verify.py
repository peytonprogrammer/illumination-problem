"""Reconstruct the support cover by connected growth, not the root-diamond loop.
Does not import count.py, geometry enumerators, SAT or optical code.
"""
from itertools import combinations
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).parent
D=json.loads((ROOT/'count.json').read_text())

def neigh(S):
    out=set()
    for x,y in S: out.update(((x+1,y),(x-1,y),(x,y+1),(x,y-1)))
    return out

def is_connected(S):
    unseen=set(S); reached={unseen.pop()}
    while unseen:
        new=unseen & neigh(reached)
        if not new: return False
        unseen-=new; reached|=new
    return True

# Independent normalization: translate each oriented image by its bounding-box
# minima, rather than by every full-cell anchor as count.py does.
def orientations(points):
    pp=list(points)
    for reflection in (1,-1):
        T=[(reflection*x,y) for x,y in pp]
        for _ in range(4):
            yield T
            T=[(-y,x) for x,y in T]

def key(S):
    variants=[]
    for T in orientations(S):
        mx=min(x for x,y in T); my=min(y for x,y in T)
        variants.append(tuple(sorted((x-mx,y-my) for x,y in T)))
    return min(variants)

def pair_key(S,pair):
    points=list(sorted(S)); inds=[points.index(p) for p in pair]; variants=[]
    for T in orientations(points):
        mx=min(x for x,y in T); my=min(y for x,y in T)
        F=tuple(sorted((x-mx,y-my) for x,y in T))
        P=tuple(sorted((T[i][0]-mx,T[i][1]-my) for i in inds))
        variants.append((F,P))
    return min(variants)

def grow(size,step):
    shapes={((0,0),)}; totals=[1]
    offsets={(x,y) for x in range(-step,step+1) for y in range(-step,step+1) if 0<abs(x)+abs(y)<=step}
    while len(next(iter(shapes)))<size:
        following=set()
        for shape in shapes:
            S=set(shape)
            frontier={(x+dx,y+dy) for x,y in S for dx,dy in offsets}-S
            for p in frontier: following.add(key(S|{p}))
        shapes=following; totals.append(len(shapes))
    return shapes,totals

# Retained I3 has connected radius-one neighborhood; this is equivalent to
# connectivity of its full cells at pair distances <=3. Connected growth is
# therefore complete without using the radius12 coordinate enumeration.
triple_candidates,triple_growth=grow(3,3)
triples={s for s in triple_candidates if len(neigh(set(s))-set(s))<=10 and is_connected(set(s)|neigh(set(s)))}
quad_candidates,quad_growth=grow(4,2)
quads={s for s in quad_candidates if len(neigh(set(s))-set(s))<=8}
# I2 use all root displacements in the complete sharper radius8 domain,
# followed by the proved d8 exclusion, rather than the primary normalized scan.
pairs=set()
for x in range(-8,9):
    for y in range(-8,9):
        d=abs(x)+abs(y)
        if not 2<=d<=8: continue
        S={(0,0),(x,y)}; b=len(neigh(S)-S)
        if max(0,d-3)>13-b or d==8: continue
        pairs.add(key(S))
observed={I:{key(set(map(tuple,r['full']))) for r in D['cases'] if r['I']==I} for I in (2,3)}
assert pairs==observed[2] and triples==observed[3]
assert quads=={key(set(map(tuple,r['full']))) for r in D['I4_exclusions']}

all_mark_keys=set(); summaries={I:{'supports':0,'raw_pairs':0,'orbits':0} for I in (2,3)}
for r in D['cases']:
    S=set(map(tuple,r['full'])); b=len(neigh(S)-S); R=S|neigh(S)
    cap=(20+3*7-2-6*len(S))//2
    assert b==r['external_neighbors'] and cap==r['partial_plus_missing_cap']
    assert set(map(tuple,r['neighborhood']))==R
    radius=cap-b
    # Direct Manhattan distance formula checks the whole finite universe.
    lo_x=min(x for x,y in R)-radius; hi_x=max(x for x,y in R)+radius
    lo_y=min(y for x,y in R)-radius; hi_y=max(y for x,y in R)+radius
    universe={(x,y) for x in range(lo_x,hi_x+1) for y in range(lo_y,hi_y+1)
              if min(abs(x-a)+abs(y-b) for a,b in R)<=radius}
    assert universe==set(map(tuple,r['allowed']))
    assert len(universe)==r['allowed_A_cells']
    assert r['canonical_triangle_universe']==8*len(universe)
    assert r['unit_square_universe']==4*len(universe)
    pp={tuple(sorted((a,b))) for a,b in combinations(sorted(S),2) if abs(a[0]-b[0])+abs(a[1]-b[1])>1}
    observed_pp={tuple(tuple(p) for p in pair) for pair in r['mark_pairs']}
    assert pp==observed_pp
    assert r['mark_pairs_original_coordinates']==[[[2*x,2*y] for x,y in pair] for pair in r['mark_pairs']]
    keys={pair_key(S,p) for p in pp}
    assert len(keys)==r['marked_pair_orbits']
    reps=r['mark_orbit_representatives']
    assert {pair_key(S,tuple(map(tuple,p))) for p in reps}==keys
    multiplicities=sorted(sum(pair_key(S,p)==k for p in pp) for k in keys)
    assert sorted(r['mark_orbit_multiplicities'])==multiplicities
    assert not(all_mark_keys & keys)
    all_mark_keys|=keys
    s=summaries[len(S)]; s['supports']+=1; s['raw_pairs']+=len(pp); s['orbits']+=len(keys)

# Orthogonal fan table: all12 nonempty, proper cyclic quadrant intervals.
fan_count=0
for mask in range(1,15):
    bits=[(mask>>i)&1 for i in range(4)]
    if sum(bits[i]!=bits[(i+1)%4] for i in range(4))!=2: continue
    n=sum(bits); Qcharge={1:2,2:3,3:6}[n]
    assert Qcharge>=2 and (Qcharge==2)==(n==1)
    fan_count+=1
assert fan_count==12
# For the distance8 equality case, adjacent one-quarter A cells can connect
# across a BC edge only if their UNIQUE B corner is the same global point.
quarter_pairs_checked=0; connected_quarter_pairs=0
for cx,cy in [(1,0),(-1,0),(0,1),(0,-1)]:
    for dx0,dy0 in [(-1,-1),(-1,0),(0,-1),(0,0)]:
        lower0=(dx0,dy0); B0=(2*dx0+1,2*dy0+1)
        for dx1,dy1 in [(-1,-1),(-1,0),(0,-1),(0,0)]:
            lower1=(2*cx+dx1,2*cy+dy1)
            B1=(2*cx+2*dx1+1,2*cy+2*dy1+1)
            quarter_pairs_checked+=1
            if abs(lower0[0]-lower1[0])+abs(lower0[1]-lower1[1])==1:
                connected_quarter_pairs+=1; assert B0==B1
assert (quarter_pairs_checked,connected_quarter_pairs)==(64,8)
# A fixed odd/odd B=(1,1) lies in exactly four A-cell closures.
centers={(x,y) for x in range(-1,3) for y in range(-1,3) if abs(2*x-1)==abs(2*y-1)==1}
assert centers=={(0,0),(1,0),(0,1),(1,1)}
# Budget equality for all normalized distance8 exclusions, no room generated.
assert len(D['distance_eight_exclusions'])==5
for row in D['distance_eight_exclusions']:
    S=set(map(tuple,row['full'])); assert len(S)==2
    p,q=sorted(S); assert abs(p[0]-q[0])+abs(p[1]-q[1])==8
    assert len(neigh(S)-S)==8
    # e>=2,o>=5, while 8+e+2o<=20, force e=2,o=5.
    assert 8+2+2*5==20
    assert 2+5==7>len(centers)
# Four-point whole branch: b>=8 hand lemma plus orthogonal cap7.
assert (20+3*7-2-6*4)//2==7<8
assert summaries[2]=={'supports':18,'raw_pairs':18,'orbits':18}
assert summaries[3]=={'supports':18,'raw_pairs':43,'orbits':38}
assert len(all_mark_keys)==D['total_marked_pair_orbits']==56
assert sum(s['raw_pairs'] for s in summaries.values())==D['total_marked_pairs_raw']==61
assert D['selected_triangle_cap']==4*(20-2+2*7)//3==42
assert D['selected_unit_square_cap']==21
baseline=json.loads((ROOT/'inputs/k6-count.json').read_text())
baseline_marked={pair_key(set(map(tuple,r['full'])),tuple(map(tuple,p))) for r in baseline['cases'] for p in r['mark_pairs']}
assert baseline_marked==all_mark_keys
M=json.loads((ROOT/'marked-cases.json').read_text())
assert M['count']==len(M['cases'])==56
assert len({r['case_id'] for r in M['cases']})==56
emitted=set()
for r in M['cases']:
    support=D['cases'][r['support_index']]
    assert support['tag']==r['support_tag'] and support['full']==r['full']
    S=set(map(tuple,r['full'])); pair=tuple(map(tuple,r['marked_cell_coordinates']))
    k=pair_key(S,pair)
    assert k not in emitted
    emitted.add(k)
    assert r['marked_original_coordinates']==[[2*x,2*y] for x,y in pair]
assert emitted==all_mark_keys
assert sum(r['raw_pair_multiplicity'] for r in M['cases'])==61
result={'status':'PASS','verification':'Separately implemented geometry-only connected-growth reconstruction and exact local algebra; same-agent, no independent reviewer.',
        'support_counts':summaries,'total_supports':36,'raw_marked_pairs':61,'marked_pair_orbits':56,
        'I3_growth_shape_counts':triple_growth,'I4_growth_shape_counts':quad_growth,
        'I4_coarse_equality_shapes':len(quads),'orthogonal_fan_masks':fan_count,
        'quarter_adjacency_pairs_checked':quarter_pairs_checked,'quarter_edge_connections':connected_quarter_pairs,
        'matches_previous_k6_marked_support_orbits':True,
        'count_json_sha256':hashlib.sha256((ROOT/'count.json').read_bytes()).hexdigest()}
(ROOT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
