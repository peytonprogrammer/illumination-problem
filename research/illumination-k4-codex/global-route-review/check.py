"""Full-star support accounting and reanalysis of fixed certificates only."""
from pathlib import Path
from itertools import combinations
from collections import Counter
from fractions import Fraction
import json
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parent;I=ROOT/'inputs'

def neigh(F):return {(x+dx,y+dy) for x,y in F for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))}
def connected(F):
    seen={(0,0)}
    while True:
        add={p for p in F-seen if any(abs(p[0]-q[0])+abs(p[1]-q[1])<=2 for q in seen)}
        if not add:return seen==F
        seen|=add

def canon(F):
    out=[]
    for swap in (False,True):
        for sx in (-1,1):
            for sy in (-1,1):
                pts=[(sx*(y if swap else x),sy*(x if swap else y)) for x,y in F]
                xx=min(x for x,y in pts);yy=min(y for x,y in pts)
                out.append(tuple(sorted((x-xx,y-yy) for x,y in pts)))
    return min(out)

D=sorted((x,y) for x in range(-6,7) for y in range(-6,7) if 0<abs(x)+abs(y)<=6)
hist=Counter(); minima=set(); tested=0
for triple in combinations(D,3):
    tested+=1;F={(0,0),*triple}
    if not connected(F):continue
    b=len(neigh(F)-F);hist[b]+=1
    if b==8:minima.add(canon(F))
assert tested==95284 and min(hist)==8
caps={str(k):{str(i):(21-4*i+2*k)//2 for i in (2,3,4)} for k in (4,5,6)}
assert caps['5']=={'2':11,'3':9,'4':7}
old=json.loads((I/'support-check.json').read_text())
assert old['support_cases']==22 and old['marked_pairs']==31
support=dict(all_triples=tested,overlap_connected_rooted_sets=sum(hist.values()),boundary_histogram=dict(sorted(hist.items())),
    minimum_boundary=8,minimal_boundary_shapes=[list(F) for F in sorted(minima)],
    partial_or_missing_caps=caps,k5_four_full_stars_excluded=True,k5_reuses_22_supports_31_pairs=True)
print(json.dumps(dict(support_summary={k:v for k,v in support.items() if k!='minimal_boundary_shapes'})),flush=True)

def floats(rows):return np.array([[float(Fraction(x)) for x in row] for row in rows])
def rank(M):return int(np.linalg.matrix_rank(M,tol=1e-7)) if len(M) else 0
def positive(M):
    if not len(M):return False
    p=linprog(np.zeros(len(M)),A_eq=M.T,b_eq=np.zeros(M.shape[1]),bounds=[(1,None)]*len(M),method='highs')
    assert p.status in (0,2),(p.status,p.message)
    return p.status==0

counts=Counter();holdouts=[];rows=[];axis_rank=0;angle_checks=0
for f in sorted(I.glob('funcs-parity-*-R12.json')):
    tag=f.name[len('funcs-'):-len('-R12.json')]
    data=json.loads(f.read_text());room=json.loads((I/(tag+'.json')).read_text());events=json.loads((I/('events-'+tag+'-R12.json')).read_text())['rows']
    G=floats(data['funcs']);C=floats(data['clos']);target=data['target'];assert len(G)==len(events)
    Q,_=np.linalg.qr(C.T);P=G-(G@Q)@Q.T
    marks=room['marked'];vertices=room['vertices']
    assert sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(vertices,vertices[1:]+vertices[:1]))>0
    axis_pts={(x+dx,y+dy) for x,y in marks for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))}
    assert len(axis_pts)==8
    for c in axis_pts:
        j=next(j for j,p in enumerate(vertices) if tuple(p)==c)
        prev=vertices[j-1];nxt=vertices[(j+1)%len(vertices)]
        u=(c[0]-prev[0],c[1]-prev[1]);v=(nxt[0]-c[0],nxt[1]-c[1])
        assert u[0]*v[0]+u[1]*v[1]==0 and u[0]*v[1]-u[1]*v[0]<0
        angle_checks+=1
    masks={}
    for label,ms in [('s',marks[:1]),('t',marks[1:]),('both',marks)]:
        for kind in ('ring','axis','diag'):
            selected=[]
            for e in events:
                yes=False
                for m in ms:
                    d=[abs(e['corner'][i]-m[i]) for i in (0,1)]
                    yes|=max(d)==1 if kind=='ring' else sorted(d)==[0,1] if kind=='axis' else d==[1,1]
                selected.append(yes)
            masks[kind+'-'+label]=np.array(selected)
    outcomes={}
    for label in ('ring-both','axis-both','diag-both','ring-s','ring-t'):
        M=P[masks[label]];rk=rank(M);ok=rk>=target and positive(M)
        counts[label]+=ok;outcomes[label]=ok
        if label=='axis-both':axis_rank+=rk>=target
    fixes=[]
    if not outcomes['axis-both']:
        for m in marks:
            for dx,dy in ((1,1),(1,-1),(-1,1),(-1,-1)):
                c=(m[0]+dx,m[1]+dy)
                mk=masks['axis-both']|np.array([tuple(e['corner'])==c for e in events])
                if rank(P[mk])>=target and positive(P[mk]):fixes.append(c)
        assert fixes,(tag,'unrepaired')
        holdouts.append(dict(tag=tag,diagonal_repairs=fixes))
    rows.append(dict(tag=tag,outcomes=outcomes))
assert len(rows)==327 and axis_rank==327 and len(holdouts)==34
assert counts=={'ring-both':327,'axis-both':293,'diag-both':43,'ring-s':72,'ring-t':35}
# Exact derivative controls for the proposed corner/wall decomposition.
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
differentials=0
for w in ((1,0),(0,1),(1,1),(2,-1)):
    A=(2*w[0],2*w[1]);C=w
    for dc in ((1,0),(0,1),(2,-1),(-1,2)):
        for da in ((0,0),(1,0),(0,1),(1,-1)):
            for sigma in (-1,1):
                plus=cross(tuple(A[i]+da[i] for i in (0,1)),tuple(C[i]+dc[i] for i in (0,1)))
                minus=cross(tuple(A[i]-da[i] for i in (0,1)),tuple(C[i]-dc[i] for i in (0,1)))
                derivative=Fraction(sigma*(plus-minus),2)
                expected=sigma*cross(w,tuple(2*dc[i]-da[i] for i in (0,1)))
                assert derivative==expected
                differentials+=1
assert cross((2,0),(0,1))==2 and cross((1,0),(0,1))==1

result=dict(status='PASS',support=support,exact_event_differential_checks=differentials,ring_numerical_reproduction=dict(rooms=len(rows),counts=dict(counts),axis_full_rank=axis_rank,
    exact_axis_corner_angle_checks=angle_checks,axis_holdouts=holdouts,scope='floating QR/rank/LP reproduction; no new exact subset positive-span certificates'),
    scope='full-star support accounting and fixed saved-event reanalysis only; no room or optical discovery')
(ROOT/'check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(status='PASS',ring_counts=dict(counts),holdouts=len(holdouts))),flush=True)
