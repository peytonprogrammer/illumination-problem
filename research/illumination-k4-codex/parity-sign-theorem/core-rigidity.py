"""Exact axis-core length information, using only frozen cellulations."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import json,hashlib
if not __debug__:raise RuntimeError('Do not strip certificate assertions with -O')
B=Path(__file__).resolve().parent
PINNED_INPUTS = {'coupling.json': '9f81b7bf93b258958fa3d6347631e50f8165e57ad32166547431a3be9ed26bec', 'twist-action.json': 'b500e3b59ba262a81655d60441f31d6c7da74e022d308761f171cc7459f81e27', 'inputs/holdouts/selection.json': '2676f153625dcc05c8e4753e377c3997230d773525d5f261b4c99858dd158b3a', 'inputs/twist_origami.py': 'cd1b19c002c1d234d6f0d29ad46250e6f409ff14cea509c488ec4b1b34bdf19e'}
for name,digest in PINNED_INPUTS.items():
    assert hashlib.sha256((B/name).read_bytes()).hexdigest()==digest, ('input changed',name)
_frozen_selection=json.loads((B/'inputs/holdouts/selection.json').read_text())
_frozen_packet=''.join(e['tag']+':'+hashlib.sha256((B/'inputs/holdouts'/f"{e['tag']}.json").read_bytes()).hexdigest()+'\n' for e in _frozen_selection)
assert hashlib.sha256(_frozen_packet.encode()).hexdigest()=='8dc5f3bb506a4f26f27d8f95e0208798d6fc7d14365d9bc1e71973521696959d'
ns={'__name__':'frozen_builder','__file__':str(B/'inputs/twist_origami.py')}
source=(B/'inputs/twist_origami.py').read_text()
exec(compile(source.replace('return r,u,lab,sstart','return r,u,lab,sstart,tris,sqs,sq'),str(B/'inputs/twist_origami.py'),'exec'),ns)

def echelon(rows):
    bs={}
    for original in rows:
        row=list(map(F,original))
        for k,v in sorted(bs.items()):
            if row[k]:
                a=row[k];row=[x-a*y for x,y in zip(row,v)]
        k=next((j for j,x in enumerate(row) if x),None)
        if k is not None:
            a=row[k];bs[k]=[x/a for x in row]
    return bs

def kernel(rows,dim):
    bs=echelon(rows);out=[]
    for f in range(dim):
        if f in bs:continue
        v=[F(j==f) for j in range(dim)]
        for k,row in sorted(bs.items(),reverse=True):v[k]=-sum(row[j]*v[j] for j in range(k+1,dim))
        assert all(sum(x*y for x,y in zip(row,v))==0 for row in rows)
        out.append(v)
    return out

def cycles(p):
    todo=set(range(len(p)));out=[]
    while todo:
        s=min(todo);c=[]
        while s in todo:todo.remove(s);c.append(s);s=p[s]
        assert s==c[0];out.append(c)
    return out

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mm(A,v):return tuple(dot(row,v) for row in A)
def cross(a,b):return a[0]*b[1]-a[1]*b[0]

def core_data(room):
    V=list(map(tuple,room['vertices']));W=len(V)
    dirs=[]
    for a,b in zip(V,V[1:]+V[:1]):
        x,y=sub(b,a);d=gcd(abs(x),abs(y));dirs.append((x//d,y//d))
    assert any(x*y==0 for x,y in dirs) and any(x*y!=0 for x,y in dirs), 'D4 family required for reported symmetry counts'
    normals=[(-y,x) for x,y in dirs];offsets=[dot(n,p) for n,p in zip(normals,V)]
    unit=lambda k:tuple(F(j==k) for j in range(W));zero=(F(0),)*W
    forms=[]
    for i in range(W):
        a,b=normals[i-1],normals[i];d=cross(a,b);assert d
        forms.append((tuple((b[1]*unit((i-1)%W)[j]-a[1]*unit(i)[j])/d for j in range(W)),tuple((-b[0]*unit((i-1)%W)[j]+a[0]*unit(i)[j])/d for j in range(W))))
    r,u,lab,s0,tris,sqs,sq=ns['build'](V,*map(tuple,room['marked']))
    pf={}
    for p in {p for tri in tris for p in tri}:
        if p in V:pf[p]=forms[V.index(p)];continue
        for i,a in enumerate(V):
            b=V[(i+1)%W];d=sub(b,a)
            if cross(sub(p,a),d)==0 and dot(sub(p,a),sub(p,b))<=0:
                k=0 if d[0] else 1;t=F(p[k]-a[k],d[k])
                pf[p]=tuple(tuple((1-t)*x+t*y for x,y in zip(forms[i][z],forms[(i+1)%W][z])) for z in (0,1));break
        else:pf[p]=(zero,zero)
    def edge(s,axis):
        values=[]
        for ti,g in sqs[s]:
            tri=tris[ti];pts=[mm(g,p) for p in tri];low=min(p[1-axis] for p in pts)
            for k,p in enumerate(pts):
                q=pts[(k+1)%3]
                if p[1-axis]==q[1-axis]==low and abs(p[axis]-q[axis])==1:
                    a,b=tri[k],tri[(k+1)%3]
                    if q[axis]<p[axis]:a,b=b,a
                    f=tuple(sub(pf[b][z],pf[a][z]) for z in (0,1))
                    values.append(tuple(tuple(sum(g[z][l]*f[l][j] for l in (0,1)) for j in range(W)) for z in (0,1)))
        assert values and all(v==values[0] for v in values);return values[0]
    he=[edge(s,0) for s in range(len(r))];ve=[edge(s,1) for s in range(len(r))]
    for s in range(len(r)):
        assert all(he[s][z][j]+ve[r[s]][z][j]-he[u[s]][z][j]-ve[s][z][j]==0 for z in (0,1) for j in range(W))
    rows=[]
    for axis,p,edges in ((0,r,he),(1,u,ve)):
        for c in cycles(p):
            f=[tuple(sum(edges[s][z][j] for s in c) for j in range(W)) for z in (0,1)]
            assert not any(f[1-axis])
            assert dot(f[axis],offsets)==len(c)
            assert all(dot(f[axis],[n[z] for n in normals])==0 for z in (0,1))
            rows.append(f[axis])
    return rows,normals,offsets,forms

selection=json.loads((B/'inputs/holdouts/selection.json').read_text());assert len(selection)==34
records=[];inputs=[];frozen_first=None
for entry in selection:
    path=B/'inputs/holdouts'/f"{entry['tag']}.json";inputs.append(path);room=json.loads(path.read_text())
    rows,normals,offsets,forms=core_data(room);W=len(normals);r=len(echelon(rows));ker=kernel(rows,W)
    result={'tag':room['tag'],'walls':W,'axis_core_length_rows':len(rows),'axis_length_rank':r,'wall_axis_isoperiodic_dimension':len(ker),
        'wall_axis_isoperiodic_mod_translation':len(ker)-2,'with_marks_mod_translation_dimension':len(ker)+2,'seed_class_lower_bound_for_axis_isoperiodic_detection':(len(ker)+3)//2}
    records.append(result);print(json.dumps(result),flush=True)
    if entry['tag']=='parity-W25-24':frozen_first=(room,rows,normals,offsets,forms,ker)
room,rows,normals,offsets,forms,ker=frozen_first
C=json.loads((B/'coupling.json').read_text());W=len(normals);dim=W+4
assert room['vertices']==C['room']['vertices'] and normals==list(map(tuple,C['offset_normals']))
# Compare the separately built core rows against the earlier action packet.
action=json.loads((B/'twist-action.json').read_text())
old=[list(map(F,f[axis][:W])) for axis,name in ((0,'horizontal'),(1,'vertical')) for f in action['core_period_derivatives'][name]]
assert list(map(list,rows))==old
assert all(not any(F(x) for x in row[W:]) for name in ('horizontal','vertical') for f in action['core_period_derivatives'][name] for row in f)
E=[]
for e in C['events']:
    E.append([tuple(F(a)-2*F(b)+F(j==W+k) for j,(a,b) in enumerate(zip(e['target_image_forms'][k],e['corner_image_forms'][k]))) for k in (0,1)])
# Hold marks fixed: isolate an actual wall change invisible to all axis lengths.
tx=[F(n[0]) for n in normals];ty=[F(n[1]) for n in normals]
witness=None
for v in ker:
    if len(echelon([tx,ty,v]))==3:
        drift=[dot(row[:W],v) for row in E[0]]
        if any(drift):witness=(v,drift);break
assert witness is not None
v,drift=witness
assert all(dot(row,v)==0 for row in rows)
assert len(echelon([tx,ty,offsets,v]))==4
# Conditional vector defect detection on the period-preserving subspace,
# including four freely moving mark coordinates.
full_basis=[list(v)+[F(0)]*4 for v in ker]+[[F(0)]*W+[F(i==j) for i in range(4)] for j in range(4)]
restricted=[[dot(row,v) for v in full_basis] for event in E for row in event]
restricted_rank=len(echelon(restricted))
fulltx=tx+[F(1),F(0),F(1),F(0)];fullty=ty+[F(0),F(1),F(0),F(1)]
fullscale=list(map(F,C['offset_base_point']))
assert len(echelon([fulltx,fullty,fullscale]))==3
assert all(dot(row,v)==0 for event in E for row in event for v in (fulltx,fullty,fullscale))
assert len(echelon(full_basis))==len(full_basis)
assert restricted_rank==len(full_basis)-2
# Literal pocket slide from the proof, not a witness chosen by kernel order.
slide=[F(0)]*dim;slide[2]=-1;slide[3]=1
assert all(dot(row,slide[:W])==0 for row in rows)
assert len(echelon([fulltx,fullty,fullscale,slide]))==4
assert [dot(row,slide) for row in E[0]]==[0,0]
assert [dot(row,slide) for row in E[1]]==[-1,-1]
assert [[dot(row,slide[:W]) for row in f] for f in forms]==[[0,-1] if i in (2,3,4) else [0,0] for i in range(W)]
e1=C['events'][1]; dx,dy=e1['direction'];ex,ey=[dot(row,slide) for row in E[1]]
slide_gradient=-F(e1['side'])*(dx*ey-dy*ex);assert slide_gradient==-17

# Select saved seed classes by exact block rank on that residual space.
blocks=[[[dot(row,v) for v in full_basis] for row in event] for event in E]
chosen=[]; selected_rows=[]; current=0
while current<restricted_rank:
    gains=[(len(echelon(selected_rows+block)),i) for i,block in enumerate(blocks) if i not in chosen]
    newrank,idx=max(gains,key=lambda t:(t[0],-t[1]));assert newrank>current
    chosen.append(idx);selected_rows+=blocks[idx];current=newrank
# Give a concrete flex invisible to the entire orbit of the first seed.
zero_core_rows=[list(row)+[F(0)]*4 for row in rows]
one_seed_kernel=kernel(zero_core_rows+E[0],dim)
fulltx=tx+[F(1),F(0),F(1),F(0)];fullty=ty+[F(0),F(1),F(0),F(1)]
blind=None
for z in one_seed_kernel:
    if len(echelon([fulltx,fullty,z]))<3:continue
    for i,event in enumerate(E):
        value=[dot(row,z) for row in event]
        if any(value):blind=(z,i,value);break
    if blind is not None:break
assert blind is not None
witness_receipt={'tag':room['tag'],'wall_variation':list(map(str,v)),'marks_fixed':True,'all_axis_core_period_derivatives_zero':True,
    'independent_of_translation_and_scale':True,'saved_event0_vector_defect_change':list(map(str,drift)),
    'axis_isoperiodic_subspace_dimension_with_marks':len(full_basis),'saved_vector_defect_rank_on_subspace':restricted_rank,
    'minimal_block_count_lower_bound':(len(full_basis)-1)//2,'saved_blocks_selected':chosen,'selected_block_count':len(chosen),'selected_block_rank':current,
    'one_seed_orbit_blind_variation':list(map(str,blind[0])),'detecting_other_saved_seed':blind[1],'other_seed_vector_defect':list(map(str,blind[2])),
    'one_seed_orbit_blind_dimension_mod_translation':len(one_seed_kernel)-2,
    'explicit_pocket_slide':{'variation':list(map(str,slide)),'moved_vertices':[2,3,4],'vertex_velocity':['0','-1'],'seed0_defect':['0','0'],'seed1_defect':['-1','-1'],'seed1_signed_gradient':str(slide_gradient)},
    'scope':'Prescribed infinitesimal changes and fixed seed forms, not darkness or absence of other corner events.'}
summary={'rooms':len(records),'axis_lengths_fail_wall_rigidity_in':sum(r['wall_axis_isoperiodic_mod_translation']>0 for r in records),
    'axis_length_rank_range':[min(r['axis_length_rank'] for r in records),max(r['axis_length_rank'] for r in records)],
    'wall_kernel_mod_translation_range':[min(r['wall_axis_isoperiodic_mod_translation'] for r in records),max(r['wall_axis_isoperiodic_mod_translation'] for r in records)]}
inputs += [B/'inputs/holdouts/selection.json',B/'inputs/twist_origami.py',B/'coupling.json',B/'twist-action.json']
out={'status':'EXACT_AXIS_LENGTH_RIGIDITY_AUDIT_PASS','summary':summary,'rooms':records,'fixed_room_witness':witness_receipt,
    'input_sha256':{str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
    'scope':'Only frozen cellulation and saved event forms. No new optical discovery. Shows why axis period lengths alone cannot prove the required corner-event rigidity.'}
(B/'core-rigidity.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(summary,indent=2));print(json.dumps(witness_receipt,indent=2))
