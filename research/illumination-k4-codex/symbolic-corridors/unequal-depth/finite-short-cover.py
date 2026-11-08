"""Exact continuous square coverage, preserving strict-guard complement boundaries."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import time,json,signal
B=Path(__file__).parent;E=json.loads((B/'finite-short-cover-effort.json').read_text())
progress={'phase_pairs_passed':0,'q_completed':2,'clauses_applied':0,'max_residual_pieces':1}
def timeout(*_):raise TimeoutError('original continuous-cover aggregate deadline')
signal.signal(signal.SIGALRM,timeout);signal.setitimer(signal.ITIMER_REAL,max(.001,E['deadline']-time.time()))
def val(g,p):return g[0]*p[0]+g[1]*p[1]+g[2]
def norm(P):
    out=[]
    for p in P:
        if not out or p!=out[-1]:out.append(p)
    if len(out)>1 and out[0]==out[-1]:out.pop()
    return out

def clip(P,g):
    # Closed halfplane g>=0, valid for polygons, segments and points.
    if not P:return []
    out=[]
    for C,D in zip(P,P[1:]+P[:1]):
        c,d=val(g,C),val(g,D)
        if c>=0:out.append(C)
        if (c<0<d) or (d<0<c):
            z=c/(c-d);out.append((C[0]+z*(D[0]-C[0]),C[1]+z*(D[1]-C[1])))
    return norm(out)

def admissible(P):return P and any(p[0]>0 for p in P) and any(p[1]>0 for p in P)
def key(P):return tuple(sorted(set(P)))
def subtract(P,guards):
    # Outside an OPEN intersection is the UNION of closed guard-negations.
    if any(max(val(g,p) for p in P)<=0 for g in guards):return [P]
    if all(min(val(g,p) for p in P)>0 for g in guards):return []
    result=[];R=P
    for g in guards:
        outside=clip(R,tuple(-x for x in g))
        if admissible(outside):result.append(outside)
        R=clip(R,g)
        if not R:break
    return result

def guards(A,C,q):
    # All q target-image residues, both target signs, all4 compatible boxes.
    for M in range(q):
      for u in (0,2):
       for eps in (1,-1):
        for lo1,hi1,lo2,hi2 in ([(1,2,1,2),(2,3,2,3)] if u==0 else [(1,2,0,1),(2,3,3,4)]):
          x=(q-A,eps*A,A*(u+4*M));y=(q-C,eps*C,C*(u+4*M))
          extrema=lambda v:(v[2]+min(0,v[0])+min(0,v[1]),v[2]+max(0,v[0])+max(0,v[1]))
          xlo,xhi=extrema(x);ylo,yhi=extrema(y)
          for k in range(xlo//(4*q)-1,xhi//(4*q)+2):
            gx=[(x[0],x[1],x[2]-q*(lo1+4*k)),(-x[0],-x[1],q*(hi1+4*k)-x[2])]
            if any(max(g[2],g[0]+g[2],g[1]+g[2],sum(g))<=0 for g in gx):continue
            for l in range(ylo//(4*q)-1,yhi//(4*q)+2):
              gy=[(y[0],y[1],y[2]-q*(lo2+4*l)),(-y[0],-y[1],q*(hi2+4*l)-y[2])]
              if any(max(g[2],g[0]+g[2],g[1]+g[2],sum(g))<=0 for g in gy):continue
              yield tuple(gx+gy),(u,eps,M,k,l,lo1,lo2)

def verify_failure(A,C,q,s,t):
    for M in range(q):
      for u in (0,2):
       for eps in (1,-1):
        x=((q-A)*s+A*(u+eps*t+4*M))/q%4;y=((q-C)*s+C*(u+eps*t+4*M))/q%4
        c=1 if 1<x<2 else 3 if 2<x<3 else None
        if c is None:continue
        lo,hi={(0,1):(1,2),(0,3):(2,3),(2,1):(0,1),(2,3):(3,4)}[u,c]
        assert not lo<y<hi

def sanity():
    P=[(F(0),F(0)),(F(1),F(0)),(F(1),F(1)),(F(0),F(1))]
    assert subtract(P,[(1,0,1),(0,1,1)])==[]
    R=subtract(P,[(1,0,0),(0,1,0)])
    assert not any(admissible(z) for z in R)
    R=subtract(P,[(1,0,-F(1,2))]);assert R
    assert all(p[0]<=F(1,2) for z in R for p in z)
    assert clip([(F(1,2),F(1,2))],(1,0,-F(1,2)))==[(F(1,2),F(1,2))]

def main():
    sanity();normals=[(m,n) for m in range(-4,5) for n in range(-4,5) if 0<abs(m)+abs(n)<=4]
    for q in range(3,E['q_max']+1):
      for A in range(1,q-1):
       for C in range(A+1,q):
        if gcd(gcd(A,C),q)!=1 or any((m*A+n*C)%q==0 for m,n in normals):continue
        pieces=[[(F(0),F(0)),(F(1),F(0)),(F(1),F(1)),(F(0),F(1))]]
        for gs,info in guards(A,C,q):
            result={}
            for P in pieces:
                for R in subtract(P,gs):
                    if admissible(R):result[key(R)]=R
            pieces=list(result.values());progress['clauses_applied']+=1
            progress['max_residual_pieces']=max(progress['max_residual_pieces'],len(pieces))
            if not pieces:break
        if pieces:
            P=pieces[0];s=sum(p[0] for p in P)/len(P);t=sum(p[1] for p in P)/len(P)
            assert 0<s<=1 and 0<t<=1
            verify_failure(A,C,q,s,t)
            out={'status':'NORM4_FAILURE_PREMISE_REFUTED_BY_EXACT_CELL','phase':[A,C,q],'s':str(s),'t':str(t),
                 'a':str(F(A,C-A)),'b':str(F(q-C,C-A)),'failure_cell':[[str(x),str(y)] for x,y in P],
                 'progress':progress,'effort':E,'scope':'No original vertical-only chart; not four-cap failure or darkness.'}
            (B/'finite-short-cover.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));return
        progress['phase_pairs_passed']+=1
      progress['q_completed']=q
    out={'status':'ALL_CONTINUOUS_ENDPOINT_SQUARES_COVERED_WITHOUT_NORM4_RELATION','progress':progress,'effort':E,
         'scope':'Finite q<=100 exact coverage only; combine with lattice sampling after independent review. Short-relation room cases still open.'}
    (B/'finite-short-cover.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':
    try:main()
    except TimeoutError:
        out={'status':'ORIGINAL_DEADLINE_REACHED_PARTIAL_ONLY','progress':progress,'effort':E}
        (B/'finite-short-cover.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
