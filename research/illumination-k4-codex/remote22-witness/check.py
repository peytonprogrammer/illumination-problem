"""Verify only the peer's prescribed direction in the frozen remote22 room."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib
import json
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'inputs'))
from exact import run
from boundary_replay import replay, on, sub, cross, dot
from illumination_geometry import check, edges_of, owners_of, label, check_fan_angles

def main():
    raw=json.loads((ROOT/'inputs/remote22-residue-check.json').read_text())
    V=[tuple(p) for p in json.loads((ROOT/'inputs/one-room-geometry.json').read_text())['vertices']]
    S,T=(0,0),(2,2)
    ts=[tuple(sorted(map(tuple,t))) for t in raw['triangles']]
    geom=check({'triangles':ts,'marked':[S,T],'require_simple':True},strict=False)
    assert geom['walls']==20 and geom['tiles']==34
    assert sorted(geom['interior_A'])==[(0,0),(2,0),(2,2)]
    assert len(geom['transparent_vertices'])==6
    # Every atomic union boundary edge belongs to exactly one supplied wall;
    # squared lengths against primitive lattice directions certify full coverage.
    boundary=[e for e,os in owners_of(ts).items() if len(os)==1]
    E=list(zip(V,V[1:]+V[:1])); covered=Counter()
    for a,b in boundary:
        js=[j for j,(c,d) in enumerate(E) if on(a,c,d) and on(b,c,d)]
        assert len(js)==1
        covered[js[0]]+=max(abs(b[k]-a[k]) for k in (0,1))
    assert all(covered[j]==max(abs(d[k]-c[k]) for k in (0,1)) for j,(c,d) in enumerate(E))
    d,P=run(V,S,T,B=50,dirs=[(10,-13)])
    assert d==(10,-13) and P is not None
    assert replay(V,S,T,P)==14
    peer=json.loads((ROOT/'inputs/peer-path.json').read_text())
    peerP=[tuple(F(*q) for q in p) for p in peer['path']]
    assert P==peerP,'independently traced coordinates differ from peer'
    contacts=[]
    for i,p in enumerate(P[1:-1],1):
        js=[j for j,(a,b) in enumerate(E) if on(p,a,b)]
        assert len(js)==1 and p not in V
        j=js[0];a,b=E[j];w=sub(b,a);vin=sub(p,P[i-1]);vout=sub(P[i+1],p)
        # Normal-component sign flips; tangent component keeps its sign/ratio.
        reflected=tuple(vin[k]-2*cross(w,vin)*(-w[1],w[0])[k]/dot(w,w) for k in (0,1))
        assert cross(reflected,vout)==0 and dot(reflected,vout)>0
        contacts.append({'bounce':i,'wall_zero_based':j,'point':[str(q) for q in p]})
    reverse=replay(V,T,S,list(reversed(P)));assert reverse==14
    controls={}
    for name,changed in [('moved_bounce',[*P[:4],(P[4][0]+F(1,100),P[4][1]),*P[5:]]),('omitted_bounce',P[:5]+P[6:]),('corner_contact',[P[0],tuple(V[3]),*P[2:]]),('wrong_target',P[:-1]+[(F(2),F(201,100))])]:
        try:replay(V,S,T,changed)
        except (AssertionError,ValueError):controls[name]='REJECTED'
        else:raise AssertionError(('corrupt path accepted',name))
    result={'status':'PASS','scope':'Single prescribed room and supplied direction; no optical search or orbit traversal. Same-agent independent replay, not an audit of the entire remote22 reduction.',
        'geometry':geom,'boundary_matches_triangle_union':True,'direction':d,'reflections':14,
        'source':S,'target':T,'path':[[str(q) for q in p] for p in P],'contacts':contacts,
        'peer_coordinates_match':True,'reverse_replay':'PASS','negative_controls':controls,
        'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'inputs').glob('*')) if p.is_file()}}
    (ROOT/'check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','direction','reflections','boundary_matches_triangle_union','peer_coordinates_match','reverse_replay','negative_controls')},indent=2))
if __name__=='__main__':main()
