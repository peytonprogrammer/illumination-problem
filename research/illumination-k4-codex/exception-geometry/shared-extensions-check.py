"""Three specified shared extensions and two specified budget repairs.
No room/direction/word enumeration, solver, or ray generation.
"""
import ast
from collections import Counter
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
# Reuse the existing pure fixed-triangle geometry functions, avoiding its
# top-level writes and optional renderer.
geometry=HERE/'darkness-fixed-check.py'
parsed=ast.parse(geometry.read_text())
ns={'Counter':Counter}
for n in parsed.body:
    if isinstance(n,ast.Assign):
        for t in n.targets:
            if isinstance(t,ast.Name) and t.id in ('CENTERS','CAPS'):
                ns[t.id]=ast.literal_eval(n.value)
functions=[n for n in parsed.body if isinstance(n,ast.FunctionDef) and n.name in ('cross','kind','star','ledger')]
exec(compile(ast.Module(body=functions,type_ignores=[]),str(geometry),'exec'),ns)
base=frozenset(t for c in ns['CENTERS'] for t in ns['star'](c))|frozenset(tuple(sorted(t)) for t in ns['CAPS'])
ledger=ns['ledger']

spec=importlib.util.spec_from_file_location('exact_guard_replay',HERE.parent/'persisted-replay/audit.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
canon=lambda triangles:frozenset(tuple(sorted(map(tuple,t))) for t in triangles)
own=json.loads((HERE/'cap-continuation-check.json').read_text())
peer=json.loads((HERE.parent/'cap-return-review/verify.json').read_text())
old_forbidden=(canon(own['forbidden']),canon(peer['forbidden_tiles']))
shared=old_forbidden[0]&old_forbidden[1]
assert len(shared)==3
extensions={
 'A_left':tuple(sorted(((-2,0),(-1,-1),(-1,0)))),
 'B_bottom':tuple(sorted(((-1,-1),(0,-2),(0,-1)))),
 'C_roof':tuple(sorted(((-1,1),(0,1),(0,2)))),
}
assert set(extensions.values())==shared
repair=tuple(sorted(((1,-1),(2,-2),(2,-1))))
rooms={name:base|{t} for name,t in extensions.items()}
rooms.update({name+'_repair':rooms[name]|{repair} for name in ('A_left','B_bottom')})
rows={}
for name,room in rooms.items():
    counted=ledger(sorted(room))
    rows[name]={'ledger':counted,'triangles_added':sorted(room-base),
       'within_W21_k6':counted['W']<=21 and counted['k']<=6,
       'invalidates_old_paths':[bool(room&z) for z in old_forbidden]}
assert [(rows[t]['ledger']['W'],rows[t]['ledger']['k']) for t in ('A_left','B_bottom','C_roof')]==[(15,7),(15,7),(17,6)]
assert all(rows[t]['within_W21_k6'] for t in ('A_left_repair','B_bottom_repair','C_roof'))
assert all(all(row['invalidates_old_paths']) for row in rows.values())

source=HERE.parent.parent/'claude-illumination-check/k6-run/cases/I3_00_01_10-pair0/guards.jsonl'
manifest=json.loads((HERE.parent/'lower-bound-proof-audit/full-replay/manifest.json').read_text())
frozen=next(r for r in manifest['guards'] if Path(r['path'])==source.resolve())
source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
assert source_hash==frozen['sha256']
eligible=('A_left_repair','B_bottom_repair','C_roof')
# Inverse of the previously established map (x,y)->(-y,x).
lookup_rooms={name:frozenset(tuple(sorted((y,-x) for x,y in tri)) for tri in rooms[name]) for name in eligible}
counts=Counter();selected={}
for index,line in enumerate(source.open(),1):
    rec=json.loads(line);used=canon(rec['U']);absent=canon(rec['Z'])
    for name,room in lookup_rooms.items():
        if used<=room and not absent&room:
            counts[name]+=1
            key=(len(rec['path'])-2,index)
            if name not in selected or key<selected[name][0]:
                selected[name]=(key,rec)

# Separate physical-polygon verification for each supplied selected path.
def boundary_check(path,cycle):
    c=audit.cross;s=audit.sub
    cycle=list(map(tuple,cycle))
    corners=[p for i,p in enumerate(cycle) if c(s(p,cycle[i-1]),s(cycle[(i+1)%len(cycle)],p))]
    walls=list(zip(corners,corners[1:]+corners[:1]))
    def on(p,u,v):
        return c(s(p,u),s(v,u))==0 and all(min(u[k],v[k])<=p[k]<=max(u[k],v[k]) for k in (0,1))
    def inside(p):
        assert not any(on(p,u,v) for u,v in walls)
        hits=0
        for u,v in walls:
            if (u[1]>p[1])!=(v[1]>p[1]):
                x=F(u[0])+F(p[1]-u[1],v[1]-u[1])*(v[0]-u[0])
                hits+=x>p[0]
        return bool(hits%2)
    for prev,p,nxt in zip(path,path[1:],path[2:]):
        support=[(u,v) for u,v in walls if on(p,u,v) and p not in (u,v)]
        assert len(support)==1
        u,v=support[0];t=s(v,u);d=s(p,prev);e=s(nxt,p)
        reflected=tuple(2*audit.dot(d,t)*t[k]-audit.dot(t,t)*d[k] for k in (0,1))
        assert c(reflected,e)==0 and audit.dot(reflected,e)>0
    assert inside(path[0]) and inside(path[-1])
    for p,q in zip(path,path[1:]):
        d=s(q,p)
        assert inside(tuple((p[k]+q[k])/2 for k in (0,1)))
        for u,v in walls:
            e=s(v,u);den=c(d,e)
            if den:
                t=F(c(s(u,p),e),den);ucoord=F(c(s(u,p),d),den)
                assert not (0<t<1 and 0<=ucoord<=1)
            elif c(s(u,p),d)==0:
                k=0 if d[0] else 1
                lo,hi=sorted((F(u[k]-p[k],d[k]),F(v[k]-p[k],d[k])))
                assert max(lo,F(0))>=min(hi,F(1))
    return {'status':'PASS','maximal_walls':len(walls),'open_legs':len(path)-1,'smooth_bounces':len(path)-2}

for name in eligible:
    rows[name]['matching_saved_guards']=counts[name]
    if name not in selected:
        rows[name]['optical_status']='No matching record in this one frozen file; no darkness verdict.'
        continue
    (n,index),rec=selected[name]
    guard_result=audit.check_record(rec,tuple(rec['q']),False)
    path=tuple((-F(*p[1]),F(*p[0])) for p in rec['path'])
    assert path[0]==(0,0) and path[-1]==(2,2)
    need,absent=audit.path_requirements(path)
    assert need<=rooms[name] and not absent&rooms[name]
    polygon=boundary_check(path,rows[name]['ledger']['boundary_cycle'])
    assert polygon['maximal_walls']==rows[name]['ledger']['W']
    rows[name]['optical_status']='LIT: one saved path passes exact triangle and actual-boundary verification.'
    rows[name]['witness']={'source_line':index,'reflections':n,'guard_check':guard_result,'boundary_check':polygon,
       'path':[[[v.numerator,v.denominator] for v in p] for p in path],
       'required':sorted(need),'forbidden':sorted(absent),'original_record':rec}
corner=(-1,1)
assert sum(corner in t for t in base)==3
assert sum(corner in t for t in rooms['C_roof'])==4
roof_path=rows['C_roof']['witness']['path']
assert [[-1,1],[1,1]] in roof_path[1:-1]
rows['C_roof']['new_smooth_B_used']={'point':corner,'old_triangle_fan':3,'new_triangle_fan':4,'bounce':6}

result={'status':'PASS','source_file':str(source.resolve()),'source_sha256':source_hash,
        'pure_geometry_source_sha256':hashlib.sha256(geometry.read_bytes()).hexdigest(),
        'shared_triangles':sorted(shared),'repair_triangle':repair,'base_ledger':ledger(sorted(base)),
        'rooms':rows,'scope':'Three prescribed one-triangle additions and two prescribed single-triangle repairs; one frozen library lookup and exact replay of selected saved paths. No room/direction/word discovery, solver or global shortestness claim.'}
(HERE/'shared-extensions-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({name:{'W':row['ledger']['W'],'k':row['ledger']['k'],'I':row['ledger']['I'],'Q':row['ledger']['Q'],
   'matching_saved_guards':row.get('matching_saved_guards'),'reflections':row.get('witness',{}).get('reflections'),
   'source_line':row.get('witness',{}).get('source_line'),'optical_status':row.get('optical_status')} for name,row in rows.items()},indent=2))
