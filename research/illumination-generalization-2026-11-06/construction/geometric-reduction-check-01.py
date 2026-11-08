"""Exact prescribed geometry only. No ray, room, direction or orbit discovery."""
from pathlib import Path
from fractions import Fraction as F
import datetime, hashlib, json

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().with_suffix('.json')
OLD = [(-1,-1),(0,-1),(0,-2),(1,-2),(1,-3),(2,-3),(2,-1),
       (1,-1),(1,1),(3,1),(3,0),(5,0),(5,1),(4,1),(4,2),
       (3,2),(3,3),(1,3),(1,2),(0,2),(0,1),(-1,1)]
FILLED = [(-1,-2)] + OLD[3:]
PRUNED = OLD[:11]+[(4,0)]+OLD[14:]
S,T = (0,0),(2,2)
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def on(a,b,p):
    return cross(sub(b,a),sub(p,a))==0 and all(min(a[i],b[i])<=p[i]<=max(a[i],b[i]) for i in [0,1])
def hit(a,b,c,d):
    vals=[cross(sub(b,a),sub(p,a)) for p in [c,d]]
    oth=[cross(sub(d,c),sub(p,c)) for p in [a,b]]
    if vals[0]*vals[1]<0 and oth[0]*oth[1]<0: return True
    return any(on(a,b,p) for p in [c,d]) or any(on(c,d,p) for p in [a,b])
def where(poly,p):
    edges=list(zip(poly,poly[1:]+poly[:1]))
    if any(on(a,b,p) for a,b in edges): return 'boundary'
    right=sum(a[0]>p[0] and min(a[1],b[1])<p[1]<=max(a[1],b[1]) for a,b in edges if a[0]==b[0])
    return 'interior' if right%2 else 'exterior'
def cells(poly):
    return {(x,y) for x in range(-2,6) for y in range(-4,4)
            if where(poly,(F(2*x+1,2),F(2*y+1,2)))=='interior'}
def geometry(poly):
    edges=list(zip(poly,poly[1:]+poly[:1])); turns=[]
    for i,(a,b) in enumerate(edges):
        assert a!=b and (a[0]==b[0] or a[1]==b[1])
        turn=cross(sub(b,a),sub(poly[(i+2)%len(poly)],b)); assert turn
        turns.append(turn)
        for j,(c,d) in enumerate(edges):
            if j>i and j not in [(i+1)%len(poly)] and not (i==0 and j==len(poly)-1):
                assert not hit(a,b,c,d),(a,b,c,d)
    area=F(sum(cross(a,b) for a,b in edges),2); assert area>0
    perimeter=sum(abs(a[0]-b[0])+abs(a[1]-b[1]) for a,b in edges)
    inside=[]; smooth=[]
    for x in range(-2,6):
        for y in range(-4,4):
            state=where(poly,(x,y))
            if state=='interior': inside.append((x,y))
            elif state=='boundary' and (x,y) not in poly: smooth.append((x,y))
    J=sum(x%2!=0 or y%2!=0 for x,y in inside)
    sn=sum(x%2!=0 or y%2!=0 for x,y in smooth)
    assert len(inside)==area-F(perimeter,2)+1
    assert all(where(poly,p)=='interior' for p in [S,T])
    return {'vertices':poly,'W':len(poly),'r':sum(t<0 for t in turns),
            'area':int(area),'boundary_lattice_count':perimeter,
            'interior_lattice_points':inside,'smooth_lattice_points':smooth,
            'J':J,'s_N':sn,'k':J+sn,'strict_simple':True,'actual_marks_interior':True}
if __name__=='__main__':
    rows={name:geometry(poly) for name,poly in [('known22',OLD),('C1_corner_filled',FILLED),('peer_ear_pruned',PRUNED)]}
    assert (rows['known22']['W'],rows['known22']['r'],rows['known22']['k'])==(22,9,4)
    assert (rows['C1_corner_filled']['W'],rows['C1_corner_filled']['r'],rows['C1_corner_filled']['k'])==(20,8,6)
    assert (rows['peer_ear_pruned']['W'],rows['peer_ear_pruned']['r'],rows['peer_ear_pruned']['k'])==(20,8,5)
    assert cells(FILLED)==cells(OLD)|{(-1,-2)}
    assert cells(OLD)==cells(PRUNED)|{(4,0)}
    # Separate hand-specified availability control, not a search or catalogue.
    teeth=[(0,0),(20,0),(20,12),(16,12),(16,4),(12,4),
           (12,12),(8,12),(8,4),(4,4),(4,12),(0,12)]
    ts=[cross(sub(teeth[i],teeth[i-1]),sub(teeth[(i+1)%12],teeth[i])) for i in range(12)]
    reflex=[i for i,t in enumerate(ts) if t<0]
    assert len(reflex)==4 and all(ts[i-1]<0 or ts[(i+1)%12]<0 for i in reflex)
    assert where(teeth,(2,10))==where(teeth,(18,10))=='interior'
    deps=[ROOT/'illumination-k4-codex/restricted-theorem-note/theorem.txt',
          ROOT/'illumination-generalization-2026-11-06/construction/baseline-and-gap.md',
          ROOT/'illumination-k4-codex/preprint-review-codex/revised.tex']
    out={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'scope':'Prescribed exact geometry, not a search or a new darkness proof',
         'rows':rows,'C1_fill_cell':[-1,-2],
         'availability_control':{'polygon':teeth,'r':4,'W':12,'marks':[[2,10],[18,10]],'no_reflex_has_two_convex_neighbors':True},
         'source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in deps},
         'darkness_inherited_from_accepted_known22_hand_proof':True,
         'filled_and_pruned_illumination_inherited_from_accepted_W21_k6':True,
         'whole_goal_complete':False}
    OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:{q:v[q] for q in ['W','r','area','J','s_N','k']} for k,v in rows.items()},indent=2))
