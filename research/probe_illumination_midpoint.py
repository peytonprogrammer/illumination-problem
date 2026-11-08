"""Small actual-room pilot: periodically repeated rectangular holes."""
import itertools,json,time
from pathlib import Path
from illumination_geometry import patch,check,owners_of,edge
from illumination_cover import build
from illumination_midpoint import vertex_data,components,half_turns,inspect_turn,translations
BASE=Path(__file__).parent

def run(nx,ny):
    started=time.monotonic();holes=[(4*i+1,4*i+3,4*j+1,4*j+3) for i in range(nx) for j in range(ny)]
    ts=[t for t in patch(0,4*nx,0,4*ny) if not any(all(a<=x<=b and c<=y<=d for x,y in t) for a,b,c,d in holes)]
    owners=owners_of(ts);boundary={p for e,o in owners.items() if len(o)==1 for p in e};points=sorted({p for t in ts for p in t}-boundary);marks=[p for p in points if p[0]%2==p[1]%2==0]
    assert len(marks)>=2
    data=dict(triangles=ts,marked=marks[:2]);g=check(data,strict=False);cover=build(data);vd=vertex_data(cover);vphys={v:cover['physical'][items[0][0]][items[0][1]] for v,items in enumerate(vd['members'])};points=set(points)
    candidate_vertices={v for v,p in vphys.items() if p in points};covered=set();required=set();counts=[];turn_records=[]
    for group in components(cover['H'],cover['V']):
        vertices={vd['ids'][i][q] for i in group for q in range(4)}&candidate_vertices
        required|=set(itertools.permutations(vertices,2))
        turns=half_turns(cover['H'],cover['V'],group);admissible=0
        for f in turns:
            r=inspect_turn(cover,vd,group,f)
            if not r['admissible']:continue
            admissible+=1;action={vd['ids'][i][q]:vd['ids'][f[i]][(q+2)%4] for i in group for q in range(4)}
            covered.update((v,action[v]) for v in vertices if action[v] in vertices and action[v]!=v)
            turn_records.append(r)
        counts.append(dict(squares=len(group),translations=len(translations(cover['H'],cover['V'],group)),half_turns=len(turns),admissible_half_turns=admissible))
    found=[];partial=[]
    for p,q in itertools.combinations(sorted(points),2):
        pairs={(a,b) for a,b in required if vphys[a]==p and vphys[b]==q}
        hit=len(pairs&covered)
        if pairs and hit==len(pairs):found.append((p,q))
        if hit:partial.append(dict(source=p,target=q,covered=hit,required=len(pairs)))
    r=dict(room_family='rectangular holes in rectangular room',nx=nx,ny=ny,walls=g['walls'],holes=len(holes),interior_lattice_points=len(points),physical_point_pairs=len(points)*(len(points)-1)//2,components=counts,fully_covered_pairs=found,partially_covered_pairs=partial,seconds=time.monotonic()-started)
    (BASE/f'midpoint-holes-{nx}x{ny}-room.json').write_text(json.dumps(data,indent=2)+'\n');(BASE/f'midpoint-holes-{nx}x{ny}-result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True);return r

if __name__=='__main__':
    results=[run(nx,ny) for nx,ny in [(3,1),(4,1),(2,2)]]
    (BASE/'midpoint-inverse-pilot.json').write_text(json.dumps(dict(status='complete',rooms=results,scope='Three periodic orthogonal rooms; all distinct interior integer-grid point pairs. A missing certificate is not illumination.'),indent=2)+'\n')
