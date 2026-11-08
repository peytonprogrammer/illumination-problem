"""Exact dual control from frozen gradients. Numerical LP proposes, exact fractions verify."""
from pathlib import Path
from fractions import Fraction as F
import json
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parent
j=json.loads((ROOT/'coupling.json').read_text());W=j['walls'];dim=W+4
room=j['room'];normals=[tuple(n) for n in j['offset_normals']]
rows=[tuple(map(F,e['offset_gradient'])) for e in j['events']]
local=[tuple(map(F,e['local_corner_and_marks_gradient'])) for e in j['events']]
walls=[tuple(map(F,e['first_minus_second_wall_gradient'])) for e in j['events']]
unit=lambda k:tuple(F(i==k) for i in range(dim))
dot=lambda a,b:sum(x*y for x,y in zip(a,b))
def vertexform(c):
    p=(c-1)%W;a=normals[p];b=normals[c];det=a[0]*b[1]-a[1]*b[0]
    return (tuple((F(b[1])*unit(p)[k]-F(a[1])*unit(c)[k])/det for k in range(dim)),
            tuple((-F(b[0])*unit(p)[k]+F(a[0])*unit(c)[k])/det for k in range(dim)))
vs=[vertexform(c) for c in range(W)];length=(F(0),)*dim
for c,d in enumerate(zip(normals,room['vertices'])):
    dx=room['vertices'][(c+1)%W][0]-room['vertices'][c][0];dy=room['vertices'][(c+1)%W][1]-room['vertices'][c][1]
    import math
    g=math.gcd(abs(dx),abs(dy));d=(dx//g,dy//g);nn=d[0]*d[0]+d[1]*d[1]
    length=tuple(length[k]+sum(F(d[a],nn)*(vs[(c+1)%W][a][k]-vs[c][a][k]) for a in (0,1)) for k in range(dim))
# Set source translation to zero and total primitive edge-length variation to zero.
gauge=[unit(W),unit(W+1),length]
marks=room['marked']
axis=[i for i,e in enumerate(j['events']) if any(sorted(abs(e['corner'][a]-p[a]) for a in (0,1))==[0,1] for p in marks)]
assert axis
scales=[max(map(abs,rows[i])) for i in axis]
M=np.array([[float(v/s) for v in rows[i]] for i,s in zip(axis,scales)])
G=np.array([[float(v) for v in row] for row in gauge])
r=linprog(-M.sum(axis=0),A_ub=-M,b_ub=np.zeros(len(axis)),A_eq=G,b_eq=np.zeros(len(gauge)),bounds=[(-1,1)]*dim,method='highs')
assert r.success and -r.fun>1e-6
# Recover the proposed LP vertex as an exact rational solution.
eq=[list(row)+[F(0)] for row in gauge]
for i,value in zip(axis,M@r.x):
    if abs(value)<1e-8:eq.append(list(rows[i])+[F(0)])
for c,value in enumerate(r.x):
    if abs(abs(value)-1)<1e-8:eq.append(list(unit(c))+[F(1 if value>0 else -1)])
piv=[];k=0
for c in range(dim):
    pivot=next((p for p in range(k,len(eq)) if eq[p][c]),None)
    if pivot is None:continue
    eq[k],eq[pivot]=eq[pivot],eq[k];v=eq[k][c];eq[k]=[x/v for x in eq[k]]
    for p in range(len(eq)):
        if p!=k and eq[p][c]:
            v=eq[p][c];eq[p]=[x-v*y for x,y in zip(eq[p],eq[k])]
    piv.append(c);k+=1
assert len(piv)==dim,('nonunique LP vertex',len(piv))
delta=tuple(eq[k][-1] for k in range(dim))
assert all(dot(g,delta)==0 for g in gauge)
values=[dot(row,delta) for row in rows]
assert all(values[i]>=0 for i in axis)
assert any(values[i]>0 for i in axis)
negative=[i for i,v in enumerate(values) if v<0]
assert negative
# Prior fixed repair-corner data, chosen before this control.
repair=(1,3)
repair_negative=[i for i in negative if tuple(j['events'][i]['corner'])==repair]
assert repair_negative
rescued=[i for i in axis if dot(local[i],delta)<0 and values[i]>=0]
def detail(i):
 e=j['events'][i]
 return {'index':i,'corner':e['corner'],'direction':e['direction'],'side':e['side'],
         'local_value':str(dot(local[i],delta)),'wall_value':str(dot(walls[i],delta)),
         'coupled_value':str(values[i]),'prefix_hits':e['prefix_hits'],'all_hits':e['all_hits']}
out={'status':'EXACT_PASS','tag':j['tag'],'offset_deformation':list(map(str,delta)),
     'vertex_deformations':[[str(dot(row,delta)) for row in p] for p in vs],
     'mark_deformations':list(map(str,delta[W:])),
     'gauge':'Source fixed and total primitive edge-length variation zero',
     'axis_rows':len(axis),'axis_strictly_positive':sum(values[i]>0 for i in axis),
     'axis_zero':sum(values[i]==0 for i in axis),'axis_negative':0,
     'all_rows_negative':len(negative),'repair_corner':repair,
     'repair_negative_events':[detail(i) for i in repair_negative],
     'axis_local_terms_rescued_by_wall_terms':[detail(i) for i in rescued],
     'all_negative_events':[detail(i) for i in negative],
     'scope':'One exact infinitesimal deformation satisfying all SAVED axis-event inequalities, cut off by saved diagonal events. Not a dark deformation and not an exhaustive optical event set.'}
(ROOT/'dual-control.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('vertex_deformations','axis_local_terms_rescued_by_wall_terms','all_negative_events','offset_deformation')},indent=2))
