"""Exact prescribed cup-form constraints; no surfaces or optical paths."""
from fractions import Fraction as F
from pathlib import Path
import json

b=Path(__file__).resolve().parent
pairs=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
R=[[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]]
K=[[1,0,0,0],[0,-1,0,0],[0,0,1,0],[0,0,0,-1]]
def transpose(a):return list(map(list,zip(*a)))
def mul(a,c):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*c)] for row in a]
def rank(a):
    a=[[F(x) for x in row] for row in a];k=0
    for j in range(len(a[0])):
        i=next((i for i in range(k,len(a)) if a[i][j]),None)
        if i is None:continue
        a[k],a[i]=a[i],a[k];d=a[k][j];a[k]=[v/d for v in a[k]]
        for i in range(len(a)):
            if i!=k:
                d=a[i][j];a[i]=[x-d*y for x,y in zip(a[i],a[k])]
        k+=1
    return k
bases=[]
for i,j in pairs:
    B=[[0]*4 for _ in range(4)];B[i][j]=1;B[j][i]=-1;bases.append(B)
constraints=[]
for transform,sign in [(R,1),(K,-1)]:
    images=[mul(mul(transpose(transform),B),transform) for B in bases]
    for i in range(4):
        for j in range(4):constraints.append([im[i][j]-sign*B[i][j] for im,B in zip(images,bases)])
# area'(0)=B(x1,y0)+B(x0,y1)=-B12+B03; area''/2=B23.
constraints += [[0,0,1,-1,0,0],[0,0,0,0,0,1]]
assert rank(constraints)==5
assert all(sum(row[j]*[1,0,0,0,0,0][j] for j in range(6))==0 for row in constraints)
W=[[0,8,0,0],[-8,0,0,0],[0,0,0,0],[0,0,0,0]]
assert rank(W)==2
V=[[0]*6 for _ in range(6)]
for i,j,v in [(0,1,8),(2,4,1),(3,5,1)]:V[i][j]=v;V[j][i]=-v
assert rank(V)==6 and [row[:4] for row in V[:4]]==W
# Removing either symmetry permits a nondegenerate4dimensional pencil.
withoutK=[[0,8,1,0],[-8,0,0,1],[-1,0,0,0],[0,-1,0,0]]
withoutR=[[0,8,0,1],[-8,0,1,0],[0,-1,0,0],[-1,0,0,0]]
assert rank(withoutK)==rank(withoutR)==4
assert mul(mul(transpose(R),withoutK),R)==withoutK
assert mul(mul(transpose(K),withoutR),K)==[[-x for x in row] for row in withoutR]
assert withoutK[0][3]-withoutK[1][2]==withoutK[2][3]==0
assert withoutR[0][3]-withoutR[1][2]==withoutR[2][3]==0
out={'status':'PRESCRIBED_D4_CUP_RADICAL_ALGEBRA_PASS',
'free_skew_form_entries':len(pairs),'independent_constraints':rank(constraints),
'only_free_pair':'B(x0,y0)=area>0','both_symmetries_necessary_countercontrols':True,'pencil_dimension':4,'restricted_cup_rank':2,
'radical_dimension':2,'minimum_symplectic_extension_dimension':6,
'reviewed_orbit_closure_rank_lower_bound':3,
'imported_theorem':{'url':'https://arxiv.org/pdf/1209.2854','version':'v2','theorem':'1.4','claim':'Projected real absolute tangent of an affine invariant manifold is symplectic.'},
'scope':'Fixed4dimensional symmetry/area constraint calculation and6dimensional symplectic extension. No actual surface, orbit, room, ray, direction or event search. Geometric application accepted by tools-disabled Opus review; this checker verifies only the prescribed cup algebra.',
'independent_review':'TOOLS_DISABLED_OPUS_ACCEPTED_EXIT0; primary Theorem1.4 independently read; geometry and proof reviewed, no copied code execution claimed','goal_complete':False,'discovery_runs':0}
(b/'pocket-rank3.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
