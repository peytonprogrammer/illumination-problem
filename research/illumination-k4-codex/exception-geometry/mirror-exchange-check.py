"""Static two-path cover check for the hand-classified zero-surplus family.
No room/cap-assignment enumeration, ray generation, or solving.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('exact_saved_guard',HERE.parent/'persisted-replay/audit.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
centers=((0,0),(2,0),(2,2))
core=frozenset().union(*(a.incident(tuple(map(F,c))) for c in centers))
options=set()
for x,y in centers:
    for dx,dy in ((1,0),(0,1),(-1,0),(0,-1)):
        external=(x+2*dx,y+2*dy)
        if external in centers:continue
        C=(x+dx,y+dy)
        for sign in (-1,1):
            B=(C[0]-sign*dy,C[1]+sign*dx)
            options.add(tuple(sorted((external,C,B))))
assert len(options)==16
by_center={}
for tri in options:
    A=next(p for p in tri if p[0]%2==p[1]%2==0)
    by_center.setdefault(A,set()).add(tri)
assert len(by_center)==7 and len(by_center[0,2])==4
assert all(len(ts)==2 for c,ts in by_center.items() if c!=(0,2))
cap=lambda *p:tuple(sorted(p))
ref_caps=frozenset((
 cap((-2,0),(-1,0),(-1,1)),cap((0,-2),(0,-1),(1,-1)),
 cap((4,2),(3,2),(3,1)),cap((2,4),(2,3),(1,3)),
))
base=core|ref_caps
sigma=lambda p:(2-p[1],2-p[0])
maptris=lambda tris:frozenset(tuple(sorted(sigma(p) for p in t)) for t in tris)
assert maptris(core)==core and maptris(ref_caps)==ref_caps

source=HERE.parent.parent/'claude-illumination-check/k6-run/cases/I3_00_01_10-pair0/guards.jsonl'
manifest=json.loads((HERE.parent/'lower-bound-proof-audit/full-replay/manifest.json').read_text())
expected=next(g['sha256'] for g in manifest['guards'] if Path(g['path'])==source.resolve())
assert hashlib.sha256(source.read_bytes()).hexdigest()==expected
with source.open() as f:
    rec=next(json.loads(line) for i,line in enumerate(f,1) if i==60)
a.check_record(rec,tuple(rec['q']),False)
p=tuple((-F(*v[1]),F(*v[0])) for v in rec['path'])
p_sigma=tuple(sigma(v) for v in reversed(p))
assert p[0]==p_sigma[0]==(0,0) and p[-1]==p_sigma[-1]==(2,2)
need,z=a.path_requirements(p);need2,z2=a.path_requirements(p_sigma)
assert maptris(need)==need2 and maptris(z)==z2
assert need<=base and need2<=base and not z&base and not z2&base

# Equality permits at most one triangle in each of the four already
# occupied outer cells, so their opposite choices cannot be added.
occupied_centers={next(v for v in t if v[0]%2==v[1]%2==0) for t in ref_caps}
same_cell_excluded=frozenset(t for c in occupied_centers for t in by_center[c])-ref_caps
# Equality forbids smooth B points. With fixed L+ and T-, these two caps
# would make (-1,1) or (1,3) smooth and hence are unavailable.
Nb_minus=cap((-1,1),(0,1),(0,2))
Nr_plus=cap((0,2),(1,2),(1,3))
no_smooth_B_excluded=frozenset((Nb_minus,Nr_plus))
remaining=frozenset(options)-ref_caps-same_cell_excluded-no_smooth_B_excluded
Nb_plus=cap((0,1),(0,2),(1,1))
Nr_minus=cap((0,2),(1,1),(1,2))
assert z&remaining=={Nb_plus}
assert z2&remaining=={Nr_minus}
assert Nb_plus!=Nr_minus
assert next(v for v in Nb_plus if v[0]%2==v[1]%2==0)==(0,2)
assert next(v for v in Nr_minus if v[0]%2==v[1]%2==0)==(0,2)

# The only equality-compatible two-triangle fan in that cell fills the
# missing quadrant of the midpoint B, making the direct path legal.
bridge_room=base|{Nb_plus,Nr_minus}
B=(F(1),F(1))
assert a.incident(B)<=bridge_room
need_direct,z_direct=a.path_requirements(((F(0),F(0)),(F(2),F(2))))
assert need_direct<=bridge_room and not z_direct
receipt={
 'status':'PASS','guard_source':str(source.resolve()),'guard_line':60,'guard_sha256':expected,
 'classified_half_side_triangles':len(options),'external_A_cells':len(by_center),
 'original_path_reflections':len(p)-2,'reflected_path_reflections':len(p_sigma)-2,
 'core_invariant':True,'reference_caps_invariant':True,
 'path_sets_transform_exactly':True,
 'original_only_possible_blocker':Nb_plus,'reflected_only_possible_blocker':Nr_minus,
 'blockers_share_A_center':[0,2],
 'both_blockers_make_midpoint_interior':True,'direct_bridge_check':'PASS',
 'unavailable_same_cell_choices':sorted(same_cell_excluded),
 'unavailable_smooth_B_choices':sorted(no_smooth_B_excluded),
 'required_original_outside_core':sorted(need-core),
 'required_reflected_outside_core':sorted(need2-core),
 'scope':'Static independent recomputation of two fixed path implications and sixteen half-side incidences, plus one supplied direct-bridge implication. All-room completeness rests on the separate hand slack/fan classification. No cap-assignment census or ray discovery.'}
(HERE/'mirror-exchange-check.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ('unavailable_same_cell_choices','unavailable_smooth_B_choices','required_original_outside_core','required_reflected_outside_core')},indent=2))
