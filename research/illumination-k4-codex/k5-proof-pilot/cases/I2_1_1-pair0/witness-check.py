"""Exact independent physical verification of one peer-supplied witness; no search."""
from pathlib import Path
from fractions import Fraction as F
import ast, json, importlib.util, hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('audit',ROOT.parent/'persisted-replay/audit.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
source=HERE/'inputs-classify.out'
raw=source.read_text()
path=[tuple(map(F,p)) for p in ast.literal_eval(next(l[5:] for l in raw.splitlines() if l.startswith('path ')))]
packet=json.loads((ROOT/'inputs/pilot/I2_1_1-pair0/vertices.json').read_text());vertices=[tuple(map(F,p)) for p in packet['vertices']]
edges=list(zip(vertices,vertices[1:]+vertices[:1]))
sub=audit.sub;cross=audit.cross;dot=audit.dot

def inside(p):
    # Winding number, exact and valid for concave polygons.
    winding=0
    for a,b in edges:
        z=cross(sub(b,a),sub(p,a))
        assert not(z==0 and min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1])),('point on boundary',p)
        if a[1]<=p[1]<b[1] and z>0:winding+=1
        if b[1]<=p[1]<a[1] and z<0:winding-=1
    return winding!=0

assert path[0]==tuple(packet['marked'][0]) and path[-1]==tuple(packet['marked'][1])
assert inside(path[0]) and inside(path[-1])
checks=0
for a,b in zip(path,path[1:]):
    d=sub(b,a);assert d!=(0,0)
    for u,v in edges:
        e=sub(v,u);den=cross(d,e)
        if den:
            t=cross(sub(u,a),e)/den;s=cross(sub(u,a),d)/den
            assert not(0<t<1 and 0<=s<=1),('intermediate boundary',a,b,u,v,t,s)
        elif cross(sub(u,a),d)==0:
            j=0 if d[0] else 1;lo,hi=sorted(((u[j]-a[j])/d[j],(v[j]-a[j])/d[j]))
            assert max(lo,F(0))>=min(hi,F(1)),('wall gliding',a,b,u,v)
        checks+=1
    assert inside(tuple((a[k]+b[k])/2 for k in (0,1)))
for prev,p,nxt in zip(path,path[1:],path[2:]):
    assert p not in vertices,('corner hit',p)
    walls=[(a,b) for a,b in edges if cross(sub(b,a),sub(p,a))==0 and min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1])]
    assert len(walls)==1,(p,walls)
    a,b=walls[0];e=sub(b,a);incoming=sub(p,prev);outgoing=sub(nxt,p)
    reflected=tuple(2*dot(incoming,e)*e[k]-dot(e,e)*incoming[k] for k in (0,1))
    assert cross(reflected,outgoing)==0 and dot(reflected,outgoing)>0
    assert cross(e,sub(prev,p))*cross(e,sub(nxt,p))>0
need,forbid=audit.path_requirements(tuple(path))
room=json.loads((ROOT/'inputs/pilot/I2_1_1-pair0/residual-room.json').read_text());room=room.get('room',room)
record=dict(U=sorted(need),Z=sorted(forbid),path=[[[c.numerator,c.denominator] for c in p] for p in path],room=room['triangles'],q=[2,2])
receipt=audit.check_record(record,(2,2),True)
(HERE/'guard.json').write_text(json.dumps(record,indent=2)+'\n')
result=dict(status='PASS',physical_segments=len(path)-1,physical_reflections=len(path)-2,segment_wall_checks=checks,used_triangles=len(need),absent_triangles=len(forbid),source_sha256=hashlib.sha256(raw.encode()).hexdigest(),guard_receipt=receipt,scope='One supplied fixed path and universal exact tile guard; no optical search.')
(HERE/'witness-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
