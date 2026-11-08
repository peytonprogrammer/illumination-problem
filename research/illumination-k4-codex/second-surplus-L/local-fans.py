"""Static local-fan verification for the hand Delta2 classification.

Only contiguous fans in seven fixed neighboring cells, plus the fourteen
single cross-cell joins used in the remote-cell exclusion. No room/cap-
assignment enumeration, path generation, source-guard lookup or solver.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
spec = importlib.util.spec_from_file_location('exact_geometry',ROOT/'persisted-replay/audit.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
full = {(0,0),(2,0),(2,2)}
external = sorted({(x+2*dx,y+2*dy) for x,y in full
    for dx,dy in ((1,0),(0,1),(-1,0),(0,-1))}-full)
assert len(external) == 7
core = set().union(*(a.incident(tuple(map(F,p))) for p in full))
rays = ((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1))
side = ((1,0),(0,1),(0,1),(-1,0),(-1,0),(0,-1),(0,-1),(1,0))
tri = lambda t:tuple(sorted(t))
def make(A,i):
    return tri((A,tuple(A[k]+rays[i][k] for k in (0,1)),
        tuple(A[k]+rays[(i+1)%8][k] for k in (0,1))))
bridge = {tri(((0,2),(0,1),(1,1))),tri(((0,2),(1,1),(1,2)))}
def cpoint(t):
    return next(p for p in t if p[0]%2 != p[1]%2)
def apoint(t):
    return next(p for p in t if p[0]%2 == p[1]%2 == 0)
def bpoint(t):
    return next(p for p in t if p[0]%2 == p[1]%2 == 1)

zero=[];unit=[];two_raw=[];two=[];rejected=[];direct=[]
for A in external:
    for m in range(1,8):
        for start in range(8):
            inds=[(start+j)%8 for j in range(m)]
            ts={make(A,i) for i in inds}
            paid={side[i] for i in inds
                if tuple(A[k]+2*side[i][k] for k in (0,1)) in full}
            d=len(paid);q=3 if m==4 else m;e=q-d
            if not (d and 0<=e<=2):
                continue
            row={'A':A,'m':m,'start':start,'q':q,'d':d,
                'excess':e,'triangles':sorted(ts)}
            if bridge<=ts:
                direct.append(row)
                continue
            if e==0:
                zero.append(row)
            if e==1:
                assert m==2 and d==1
                pair_count=Counter(side[i] for i in inds)
                row['type']='centered' if max(pair_count.values())==2 else 'quarter'
                unit.append(row)
            if e==2:
                assert d==1 and m in (3,4)
                outside_smooth=[]
                for c in {cpoint(t) for t in ts}:
                    # C belongs to exactly these two A cells. If neither
                    # is full and the fan supplies two quadrants, all other
                    # zero-excess single caps cannot supply more at C.
                    if not any(c in t for t in core) and sum(c in t for t in ts)==2:
                        outside_smooth.append(c)
                row['unavoidable_extra_smooth_C']=outside_smooth
                two_raw.append(row)
                if outside_smooth:
                    rejected.append(row)
                else:
                    assert max(Counter(side[i] for i in inds).values())>=2
                    row['type']='three_triangle_fan' if m==3 else 'smooth_A_rectangle'
                    assert sum(sum(c in t for t in core|ts)==4
                        for c in {cpoint(t) for t in ts}
                        if any(c in t for t in core)) == 1
                    two.append(row)

assert len(zero)==16
assert len(unit)==22 and Counter(r['type'] for r in unit)=={'centered':8,'quarter':14}
assert len(two_raw)==62 and len(rejected)==42
assert len(two)==20 and Counter(r['type'] for r in two)=={'three_triangle_fan':14,'smooth_A_rectangle':6}
assert sum(r['A']==(0,2) for r in two)==2
assert all(r['m']==3 for r in two if r['A']==(0,2))

# One remote q=1 fan can join the core only through the unused BC edge
# of a quarter unit fan. At that C, exactly two adjacent quadrants occur:
# an extra smooth boundary C, which would raise total surplus to >=3.
remote_joins=[]
for row in unit:
    if row['type']!='quarter':
        continue
    ts=set(row['triangles'])
    outside=next(t for t in ts if t not in {make(row['A'],i) for i in range(8)
        if tuple(row['A'][k]+2*side[i][k] for k in (0,1)) in full})
    c,b=cpoint(outside),bpoint(outside)
    middle=tuple(F(c[k]+b[k],2) for k in (0,1))
    adjacent=a.incident(middle)
    assert len(adjacent)==2 and outside in adjacent
    leaf=next(t for t in adjacent if t!=outside)
    B=apoint(leaf)
    assert B not in full
    assert not any(c in t for t in core)
    assert sum(c in t for t in ts|{leaf})==2
    # The two right-angle quadrants fill a half-plane (not a pinch).
    vertices=[p for t in (outside,leaf) for p in t if p!=c]
    rays_at_c={tuple(p[k]-c[k] for k in (0,1)) for p in vertices}
    assert len(rays_at_c)==3
    remote_joins.append({'parent_A':row['A'],'parent_start':row['start'],
        'leaf_A':B,'shared_C':c,'parent_outer_triangle':outside,'leaf_triangle':leaf,
        'minimum_surplus':3})
assert len(remote_joins)==14

# The one-two-triangle optical extension needs NO no-smooth-B premise:
# the B6 path handles absence of Nb-, while old sigma13 handles Nb- present.
caps={k:tri(map(tuple,t)) for k,t in json.loads((ROOT/'zero-surplus-L/guard-incidence-check.json').read_text())['cap_options'].items()}
labels={t:k for k,t in caps.items()}
old=json.loads((ROOT/'exception-geometry/zero-L-completion-check.json').read_text())['paths']['left_east_thirteen']
path=tuple(tuple(F(*v) for v in p) for p in old['path'])
u,z=a.path_requirements(path)
assert {labels[t] for t in u-core}=={'L+','E-'}
assert {labels[t] for t in z if t in labels}=={'L-','E+','T+','Nr-','Nr+'}
assert caps['Nb-'] not in z
# Once L+,E-,T- are forced, their cells are single, and Nb- is the
# one N cap. These are slot exclusions, not smooth-B exclusions.
assert not z&(core|{caps[k] for k in ('B-','B+','L+','E-','T-','Nb-')})

# Only supplied fixed paths and explicit local square substitutions follow.
# The centered-L3 path survives every second defect outside B/L cells.
left_source=json.loads((ROOT/'first-surplus-review/residual-cover-check.json').read_text())
lp=tuple(tuple(F(*v) for v in p) for p in left_source['path'])
lu,lz=a.path_requirements(lp)
assert {labels[t] for t in lu-core}=={'B+','L+','L-'}
assert {labels[t] for t in lz if t in labels}=={'B-'}
assert not any(set(row['triangles'])&lz for row in unit if row['A'] not in ((0,-2),(-2,0)))

bottom_source=json.loads((ROOT/'first-surplus-review/bottom-residual-check.json').read_text())
bp=tuple(tuple(F(*v) for v in p) for p in bottom_source['path'])
bu,bz=a.path_requirements(bp)
assert {labels[t] for t in bu-core}=={'B+','B-','T-'}
assert {labels[t] for t in bz if t in labels}=={'Nb-','T+'}
# Replace its top three hits by the one far-wall hit of a T square.
patched=bp[:4]+((F(5,3),F(4)),bp[-1])
pu,pz=a.path_requirements(patched)
top_outer=tri(((1,3),(1,4),(2,4)))
assert pu-core=={caps['B-'],caps['B+'],caps['T-'],top_outer}
assert {labels[t] for t in pz if t in labels}=={'Nb-'}
assert len(patched)-2==4

# Two outer square excursions on the original13 path compose independently.
original=json.loads((ROOT/'exception-geometry/zero-L-completion-check.json').read_text())['paths']['bottom_top_thirteen']
op=tuple(tuple(F(*v) for v in p) for p in original['path'])
double_square=op[:8]+((F(6,11),F(-2)),(F(18,11),F(4)),op[-1])
du,dz=a.path_requirements(double_square)
bottom_outer=tri(((0,-2),(1,-2),(1,-1)))
assert du-core=={caps['B+'],caps['T-'],bottom_outer,top_outer}
assert not dz&{bottom_outer,top_outer}
assert {labels[t] for t in dz if t in labels} <= {'B-','L-','T+','Nb-','Nb+'}
assert len(double_square)-2==9

# A pair of centered L/B fans necessarily creates an extra smooth B.
point=(-1,-1)
assert sum(point in t for t in core|{caps[k] for k in ('L-','L+','B-','B+')})==4

# Convex-B repairs for single e2 fans. There is no remote third cell.
forced_repairs={
    (-2,0):{(-1,-1):'B-',(-1,1):'Nb-'},
    (0,-2):{(-1,-1):'L-'},
    (2,4):{(1,3):'Nr+',(3,3):'E+'},
    (4,2):{(3,3):'T+'}}
critical={(-2,0),(0,-2),(2,4),(4,2)}
repair_rows=[]
for row in two:
    if row['A'] not in critical:
        continue
    ts=set(row['triangles']);repairs=[]
    for b,label in forced_repairs[row['A']].items():
        if sum(b in t for t in core|ts)==4:
            repairs.append(label)
    repair_rows.append({'A':row['A'],'type':row['type'],'start':row['start'],'forced_ordinary_caps':repairs})
assert len(repair_rows)==12
assert all(r['forced_ordinary_caps'] for r in repair_rows if r['type']=='smooth_A_rectangle')
remaining_single=[]
for row in two:
    if row['A'] not in critical or row['m']!=3:
        continue
    repair=next(r for r in repair_rows if r['A']==row['A'] and r['start']==row['start'])
    blockers={'B-','L-','E+','T+'}
    if set(repair['forced_ordinary_caps'])&blockers:
        continue
    remaining_single.append(row)
assert len(remaining_single)==4

result={'status':'PASS','external_A_cells':external,
    'unit_excess_nonbridge_local_types':unit,
    'two_excess_raw_neighbor_fans':len(two_raw),
    'two_excess_fans_requiring_extra_smooth_C':rejected,
    'one_two_excess_cell_allowed_fans':two,
    'remote_leaf_join_local_obstructions':remote_joins,
    'single_e2_critical_repairs':repair_rows,
    'remaining_single_e2_local_patterns':remaining_single,
    'fixed_square_substitutions':{'Bcenter_Touter_reflections':4,'Bouter_Touter_reflections':9,'status':'PASS'},
    'remaining_geometric_forms':['one of four active three-triangle fans','one centered and one outer active fan in two specific critical cells'],
    'W21_k6_necessary_budget_pairs':[[18,6],[20,5]],
    'scope':'Hand necessity/locality and optical lemmas plus static local fans only. No whole-room/cap-assignment enumeration or new optical discovery. No full Delta2 illumination theorem.'}
(HERE/'local-fans.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','unit_types':len(unit),
    'one_two_excess_cell_types':dict(Counter(r['type'] for r in two)),
    'remote_join_obstructions':len(remote_joins),'raw_two_excess_fans_excluded_by_smooth_C':len(rejected)},indent=2))
