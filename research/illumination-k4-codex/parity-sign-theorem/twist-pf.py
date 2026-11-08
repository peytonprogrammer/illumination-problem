"""Exact cylinder mixing matrix checks, only frozen origamis and fixed controls."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,importlib.util
if not __debug__:raise RuntimeError('Verification requires no -O')
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('frozen_origami',B/'inputs/twist_origami.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

def cycles(p):
    unseen=set(range(len(p)));out=[];labels={}
    while unseen:
        x=min(unseen);c=[]
        while x in unseen:labels[x]=len(out);c.append(x);unseen.remove(x);x=p[x]
        assert x==c[0];out.append(c)
    return out,labels

def rank(rows):
    if not rows:return 0
    rows=[list(map(F,r)) for r in rows];p=0
    for j in range(len(rows[0])):
        i=next((i for i in range(p,len(rows)) if rows[i][j]),None)
        if i is None:continue
        rows[p],rows[i]=rows[i],rows[p];a=rows[p][j];rows[p]=[x/a for x in rows[p]]
        for i in range(p+1,len(rows)):
            a=rows[i][j]
            if a:rows[i]=[x-a*y for x,y in zip(rows[i],rows[p])]
        p+=1
        if p==len(rows):break
    return p


def mixing(r,u,tag,require_connected=True):
    assert sorted(r)==sorted(u)==list(range(len(r)))
    hs,hi=cycles(r);vs,vi=cycles(u);H,V=len(hs),len(vs)
    E=[[0]*V for _ in range(H)]
    for s in range(len(r)):E[hi[s]][vi[s]]+=1
    l=list(map(len,hs));m=list(map(len,vs))
    assert [sum(row) for row in E]==l
    assert [sum(E[i][j] for i in range(H)) for j in range(V)]==m
    A=[[sum(F(E[i][j]*E[k][j],l[i]*m[j]) for j in range(V)) for k in range(H)] for i in range(H)]
    assert all(sum(row)==1 and row[i]>0 and min(row)>=0 for i,row in enumerate(A))
    assert all(l[i]*A[i][j]==l[j]*A[j][i] for i in range(H) for j in range(H))
    assert all(sum(l[i]*A[i][j] for i in range(H))==l[j] for j in range(H))
    seen={0};todo=[0]
    for i in todo:
        for j,x in enumerate(A[i]):
            if x and j not in seen:seen.add(j);todo.append(j)
    connected=len(seen)==H
    zero_matrix=[[A[i][j]-F(i==j) for j in range(H)] for i in range(H)]
    kernel=H-rank(zero_matrix)
    if require_connected:assert connected and kernel==1
    # Basis z_j=e_j-(l_j/l_0)e_0 of the free horizontal zero-holonomy space.
    restricted=[]
    for j in range(1,H):
        z=[F(i==j)-F(l[j],l[0])*F(i==0) for i in range(H)]
        image=[sum(zero_matrix[i][k]*z[k] for k in range(H)) for i in range(H)]
        assert sum(l[i]*image[i] for i in range(H))==0
        restricted.append(image[1:])
    zero_restricted_rank=rank(restricted)
    if require_connected:assert zero_restricted_rank==H-1
    return {'tag':tag,'squares':len(r),'horizontal_rows':H,'vertical_columns':V,'intersection_matrix':E,
        'row_widths':l,'column_lengths':m,'stochastic_matrix':[[str(x) for x in row] for row in A],
        'connected':connected,'top_eigenspace_dimension':kernel,'zero_holonomy_restriction_rank':zero_restricted_rank,'zero_holonomy_dimension':H-1}

selection=json.loads((B/'inputs/holdouts/selection.json').read_text());assert len(selection)==34
records=[];files=[]
for item in selection:
    path=B/'inputs/holdouts'/f"{item['tag']}.json";files.append(path);room=json.loads(path.read_text())
    r,u,labels,start=module.build(list(map(tuple,room['vertices'])),*map(tuple,room['marked']))
    todo=[start];seen={start}
    for x in todo:
        for y in (r[x],u[x]):
            if y not in seen:seen.add(y);todo.append(y)
    # The34frozen diagonal-wall rooms have connected eight-copy unfoldings.
    assert len(seen)==len(r)
    record=mixing(r,u,item['tag']);records.append(record)
    print(json.dumps({k:v for k,v in record.items() if k not in ('intersection_matrix','row_widths','column_lengths','stochastic_matrix')}),flush=True)
controls=[mixing([0],[0],'unit_torus'),mixing([0,1],[1,0],'stacked_torus'),mixing([1,0,2],[2,1,0],'three_square_L')]
disconnected=mixing([0,1],[0,1],'disconnected_two_tori',False)
assert not disconnected['connected'] and disconnected['top_eigenspace_dimension']==2
assert disconnected['zero_holonomy_restriction_rank']==0
controls.append(disconnected)
summary={'rooms':len(records),'simple_top_modes':len(records),'invertible_zero_period_horizontal_restrictions':len(records),'total_horizontal_rows':sum(r['horizontal_rows'] for r in records),'total_vertical_columns':sum(r['vertical_columns'] for r in records),'prescribed_controls':len(controls)}
out={'status':'EXACT_CYLINDER_MIXING_PASS','summary':summary,'rooms':records,'controls':controls,
    'input_sha256':{str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files+[B/'inputs/holdouts/selection.json',B/'inputs/twist_origami.py']},
    'scope':'Finite cell-permutation/matrix checks only. General ordinary-rank-to-positive-span proof is in twist-positivity-reduction.md; ordinary full event rank for all parity rooms is not claimed.'}
(B/'twist-pf.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(summary,indent=2))
