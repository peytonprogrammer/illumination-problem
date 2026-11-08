"""Paired-side corner elimination on frozen affine event forms."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import json
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parent
j=json.loads((ROOT/'coupling.json').read_text());dim=j['offset_dimension'];W=j['walls']
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def rank(rows):
    A=[list(map(F,row)) for row in rows];k=0
    for c in range(dim):
        p=next((i for i in range(k,len(A)) if A[i][c]),None)
        if p is None:continue
        A[k],A[p]=A[p],A[k];v=A[k][c];A[k]=[x/v for x in A[k]]
        for i in range(k+1,len(A)):
            if A[i][c]:v=A[i][c];A[i]=[x-v*y for x,y in zip(A[i],A[k])]
        k+=1
    return k

groups=defaultdict(dict)
for e in j['events']:
    key=(tuple(e['direction']),tuple(e['corner']))
    assert e['side'] not in groups[key],('duplicate saved event key',key,e['side'])
    groups[key][e['side']]=e
out=[];rows=[]
for key,sides in sorted(groups.items()):
    if set(sides)!={-1,1}:continue
    plus,minus=sides[1],sides[-1]
    Cplus=[[F(x) for x in row] for row in plus['corner_image_forms']]
    Cminus=[[F(x) for x in row] for row in minus['corner_image_forms']]
    assert Cplus==Cminus,key
    gp=list(map(F,plus['offset_gradient']));gm=list(map(F,minus['offset_gradient']));row=tuple(a+b for a,b in zip(gp,gm))
    Tp=[[F(x) for x in r] for r in plus['target_image_forms']];Tm=[[F(x) for x in r] for r in minus['target_image_forms']]
    w=key[0]
    expected=tuple(w[0]*(Tm[1][k]-Tp[1][k])-w[1]*(Tm[0][k]-Tp[0][k]) for k in range(dim))
    assert row==expected and row[W]==row[W+1]==0
    rows.append(row)
    out.append({'direction':key[0],'corner':key[1],'plus_index':plus['index'],'minus_index':minus['index'],'loop_gradient':list(map(str,row)),
                'corner_forms_cancel':True,'source_coefficients_cancel':True})
assert rows
M=np.array([[float(v/max(map(abs,row))) for v in row] for row in rows if any(row)])
lp=linprog(np.ones(len(M)),A_eq=M.T,b_eq=np.zeros(dim),bounds=[(1,None)]*len(M),method='highs')
assert lp.status in (0,2)
result={'status':'PASS','tag':j['tag'],'paired_sides':len(rows),'nonzero_loop_rows':len(M),
        'exact_full_rank':rank([e['offset_gradient'] for e in j['events']]),
        'exact_loop_rank':rank(rows),'structural_max_loop_rank':W-1,
        'loop_positive_dependence_float':lp.status==0,
        'loop_positive_dependence_scope':'Numerical exploration only; not an exact positive certificate.',
        'paired_events':out,
        'scope':'Exact paired-gradient identity on fixed side pairs. A sufficient sign theorem for all rooms remains open; source-fixed paired loops alone cannot control moving source relative to room and target.'}
(ROOT/'sign-identity.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='paired_events'},indent=2))
