"""Independent determinant expansion and exact rank/stress check; no path tracing."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
if not __debug__:raise RuntimeError('Do not strip verification assertions with -O')
B=Path(__file__).resolve().parent
D=json.loads((B/'coupling.json').read_text());C=json.loads((B/'twist-action.json').read_text())
assert C['generator_sha256']==hashlib.sha256((B/'twist-action.py').read_bytes()).hexdigest()
for name,digest in C['input_sha256'].items():
    assert hashlib.sha256((B/name).read_bytes()).hexdigest()==digest
W=D['walls'];dim=W+4;point=list(map(F,D['offset_base_point']))
assert C['summary']['horizontal_shear']==C['summary']['vertical_shear']==48
vertices=[tuple(map(F,p)) for p in D['room']['vertices']]
for p in map(tuple,D['room']['marked']):
    inside=False
    for a,b in zip(vertices,vertices[1:]+vertices[:1]):
        cross=(p[0]-a[0])*(b[1]-a[1])-(p[1]-a[1])*(b[0]-a[0])
        between=sum((p[j]-a[j])*(p[j]-b[j]) for j in (0,1))<=0
        assert cross or not between, 'mark on boundary'
        if (a[1]>p[1])!=(b[1]>p[1]) and p[0]<a[0]+F(p[1]-a[1],b[1]-a[1])*(b[0]-a[0]):inside=not inside
    assert inside, 'mark outside room'
rows=[];weights=[]
for record in C['orbit_stress_certificate']:
    e=D['events'][record['saved_index']];a=C['events'][record['saved_index']]
    forms=[list(map(F,row)) for row in e['target_image_forms']]
    corner=[list(map(F,row)) for row in e['corner_image_forms']]
    E=[[forms[k][j]-2*corner[k][j]+F(j==W+k) for j in range(dim)] for k in (0,1)]
    target=[sum(x*y for x,y in zip(row,point)) for row in forms]
    source=point[W:W+2];w=[(x-y)/2 for x,y in zip(target,source)]
    direction=record['twist'];n=F(record['power']);shear=F(C['summary'][direction+'_shear'])
    increment=[list(map(F,row)) for row in a[direction]['period_derivative']]
    image_w=[w[0]+n*shear*w[1],w[1]] if direction=='horizontal' else [w[0],w[1]+n*shear*w[0]]
    image_E=[[E[k][j]+n*increment[k][j] for j in range(dim)] for k in (0,1)]
    actual=[-F(e['side'])*(image_w[0]*image_E[1][j]-image_w[1]*image_E[0][j]) for j in range(dim)]
    assert actual==list(map(F,record['row']))
    weights.append(F(record['weight']));rows.append(actual)
assert len(rows)==52 and min(weights)>0
assert all(sum(weight*row[j] for weight,row in zip(weights,rows))==0 for j in range(dim))
# Separate Gauss-Jordan implementation, using columns and all other rows.
A=[row[:] for row in rows];pivot=0
for col in range(dim):
    pick=next((i for i in range(pivot,len(A)) if A[i][col]),None)
    if pick is None:continue
    A[pivot],A[pick]=A[pick],A[pivot];v=A[pivot][col]
    A[pivot]=[x/v for x in A[pivot]]
    for i in range(len(A)):
        if i!=pivot and A[i][col]:
            v=A[i][col];A[i]=[x-v*y for x,y in zip(A[i],A[pivot])]
    pivot+=1
assert pivot==W+1==26
normals=[list(map(F,n)) for n in D['offset_normals']]
tx=[n[0] for n in normals]+[F(1),F(0),F(1),F(0)]
ty=[n[1] for n in normals]+[F(0),F(1),F(0),F(1)]
scale=point
for row in rows:
    assert all(sum(x*y for x,y in zip(row,v))==0 for v in (tx,ty,scale))
assert tx[W:]==[1,0,1,0] and ty[W:]==[0,1,0,1]
assert source!=point[W+2:W+4] # scale independent of the translations
result={'status':'EXACT_ORBIT_DETERMINANT_AND_STRESS_PASS','expanded_rows':len(rows),'rank':pivot,'positive_weights':len(weights),'minimum_weight':str(min(weights)),
    'source_sha256':{name:hashlib.sha256((B/name).read_bytes()).hexdigest() for name in ('twist-action.py','twist-action.json','coupling.json')},
    'scope':'Independent determinant expansion, Gauss-Jordan rank and stress only. Inherits recorded annulus increments and affine-event transfer hypotheses.'}
(B/'twist-verify.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
