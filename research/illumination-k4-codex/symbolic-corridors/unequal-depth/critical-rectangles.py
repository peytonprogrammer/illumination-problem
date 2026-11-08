"""Exact support-rectangle classification on the10critical lines; no billiard search."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,signal,time
B=Path(__file__).parent;E=json.loads((B/'critical-rectangles-effort.json').read_text());rows=[r for r in json.loads((B/'short-line-margin.json').read_text())['rows'] if r['closed_blind_pieces']]
def timeout(*_):raise TimeoutError('original critical-rectangle aggregate deadline')
signal.signal(signal.SIGALRM,timeout);signal.setitimer(signal.ITIMER_REAL,max(.001,E['deadline']-time.time()))

def solve(indices):
    mat=[]
    # Variables a,A,b,B and four corners (a,b),(A,b),(a,B),(A,B).
    for j,i in enumerate(indices):
        p,q,r=map(F,rows[i]['depth_line']);R=[F(0)]*5;R[j%2]=p;R[2+j//2]=q;R[4]=r;mat.append(R)
    pivots=[];r=0
    for c in range(4):
        j=next((j for j in range(r,4) if mat[j][c]),None)
        if j is None:continue
        mat[r],mat[j]=mat[j],mat[r];z=mat[r][c];mat[r]=[x/z for x in mat[r]]
        for j in range(4):
            if j!=r and mat[j][c]:
                z=mat[j][c];mat[j]=[x-z*y for x,y in zip(mat[j],mat[r])]
        pivots.append(c);r+=1
    if any(all(v==0 for v in R[:4]) and R[4] for R in mat):return None
    free=[i for i in range(4) if i not in pivots];expr=[]
    for i in range(4):
        if i in free:expr.append([F(int(i==j)) for j in free]+[F(0)])
        else:
            R=mat[pivots.index(i)];expr.append([-R[j] for j in free]+[R[4]])
    # a>0,b>0,A-a>0,B-b>0 are necessary and sufficient for a strict NE rectangle.
    inequalities=[expr[0],expr[2],[x-y for x,y in zip(expr[1],expr[0])],[x-y for x,y in zip(expr[3],expr[2])]]
    work=inequalities
    for _ in free:
        pos=[R for R in work if R[0]>0];neg=[R for R in work if R[0]<0];zero=[R[1:] for R in work if not R[0]]
        work=zero+[[x/P[0]-y/N[0] for x,y in zip(P[1:],N[1:])] for P in pos for N in neg]
    if any(R[0]<=0 for R in work):return None
    interval=None
    if len(free)==1:
        lows=[-R[1]/R[0] for R in inequalities if R[0]>0];highs=[-R[1]/R[0] for R in inequalities if R[0]<0]
        interval=[str(max(lows)) if lows else None,str(min(highs)) if highs else None]
    key=tuple(tuple(R) for R in mat[:r]);return key,free,expr,interval

def blind_at(row,P):
    for piece in row['closed_blind_pieces']:
        Q=[tuple(map(F,p)) for p in piece]
        if len(Q)==1 and Q[0]==P:return True
        if len(Q)==2:
            A,C=Q;v=(C[0]-A[0],C[1]-A[1]);w=(P[0]-A[0],P[1]-A[1])
            if v[0]*w[1]-v[1]*w[0]==0 and all(min(x,y)<=z<=max(x,y) for x,y,z in zip(A,C,P)):return True
    return False

def main():
    families={};points={};tested=0
    for indices in product(range(len(rows)),repeat=4):
        tested+=1;result=solve(indices)
        if result is None:continue
        key,free,expr,interval=result
        rec={'supporting_line_indices':list(indices),'relations':[rows[i]['relation'] for i in indices],
             'variable_order':['a','A','b','B'],'free_variables':free,
             'affine_expressions':[[str(x) for x in R] for R in expr],'open_parameter_interval':interval,
             'common_blind_boundary_points':[[str(x),str(y)] for x,y in [(F(0),F(0)),(F(1),F(0)),(F(0),F(1)),(F(1),F(1))] if all(blind_at(rows[i],(x,y)) for i in indices)]}
        if not free:points[key]=rec
        else:families[key]=rec
    out={'status':'COMPLETE10LINE_SUPPORT_RECTANGLE_CLASSIFICATION','assignments':tested,'critical_lines':[r['depth_line'] for r in rows],
         'positive_dimensional_families':list(families.values()),'isolated_points':list(points.values()),
         'family_count':len(families),'isolated_count':len(points),'dimension_counts':{str(d):sum(len(r['free_variables'])==d for r in families.values()) for d in (1,2,3)},
         'effort':E,'scope':'Support only; not actual vertical failure, illumination proof or darkness.'}
    (B/'critical-rectangles.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('positive_dimensional_families','isolated_points')}))
    print('commonblindfamilies',sum(bool(r['common_blind_boundary_points']) for r in families.values()))
if __name__=='__main__':main()
