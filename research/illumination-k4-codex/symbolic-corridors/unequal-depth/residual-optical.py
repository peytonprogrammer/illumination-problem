"""Exact continuous strict-chart cover for the frozen finite room support."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd,lcm
from functools import lru_cache
from itertools import product
import json,time,signal,hashlib
B=Path(__file__).parent;EFF=json.loads((B/'residual-optical-effort.json').read_text())
def timeout(*_):raise TimeoutError('original residual optical 840-second aggregate deadline')
signal.signal(signal.SIGALRM,timeout);signal.setitimer(signal.ITIMER_REAL,max(.001,EFF['deadline']-time.time()))
SQUARE=[(0,0,1),(1,0,1),(1,1,1),(0,1,1)]
def primitive(p):
    z=gcd(gcd(abs(p[0]),abs(p[1])),abs(p[2]));p=tuple(v//z for v in p)
    return tuple(-v for v in p) if p[2]<0 else p

def value(g,p):return sum(x*y for x,y in zip(g,p))
def normalize(P):
    out=[]
    for p in P:
        if not out or p!=out[-1]:out.append(p)
    if len(out)>1 and out[0]==out[-1]:out.pop()
    return out

def clip(P,g):
    if not P:return []
    out=[]
    for C,D in zip(P,P[1:]+P[:1]):
        c,d=value(g,C),value(g,D)
        if c>=0:out.append(C)
        if (c<0<d) or (d<0<c):out.append(primitive(tuple(c*y-d*x for x,y in zip(C,D))))
    return normalize(out)
def admissible(P):return P and any(p[0]>0 for p in P) and any(p[1]>0 for p in P)
def subtract(P,gs):
    vals=[[value(g,p) for p in P] for g in gs]
    if any(max(v)<=0 for v in vals):return [P]
    if all(min(v)>0 for v in vals):return []
    out=[];R=P
    for g in gs:
        neg=clip(R,tuple(-x for x in g))
        if admissible(neg):out.append(neg)
        R=clip(R,g)
        if not R:break
    return out

def apply(pieces,gs):
    out={}
    for P in pieces:
        for R in subtract(P,gs):
            if admissible(R):out[tuple(sorted(set(R)))]=R
    return list(out.values())

def ranges(v,lo,hi,q):
    low=v[2]+min(0,v[0])+min(0,v[1]);high=v[2]+max(0,v[0])+max(0,v[1])
    for k in range(low//(4*q)-1,high//(4*q)+2):
        gs=((v[0],v[1],v[2]-q*(lo+4*k)),(-v[0],-v[1],q*(hi+4*k)-v[2]))
        if all(max(g[2],g[0]+g[2],g[1]+g[2],sum(g))>0 for g in gs):yield gs,k

def charts(U,V,mode):
    D=lcm(U.denominator,V.denominator);p=int(U*D);r=int(V*D);q=p+r+mode*D
    for M in range(q):
      for u,eps in product((0,2),(1,-1)):
        for c in (1,3):
          left=1 if c==1 else 2
          right={(0,1):1,(0,3):2,(2,1):0,(2,3):3}[u,c]
          endpoints=[]
          for j,lo in [(0,left),(mode,right)]:
            n=p+j*D;v=(q-n,eps*n,n*(u+4*M))
            endpoints.append(list(ranges(v,lo,lo+1,q)))
          for (g0,k0),(g1,k1) in product(*endpoints):
            gs=g0+g1
            info={'mode':mode,'u':u,'eps':eps,'M':M,'c':c,'shifts':[k0,k1]}
            if mode==1:yield gs,info;continue
            inner=[]
            for j in (1,2):
                n=p+j*D;v=(q-n,eps*n,n*(u+4*M));opts=[]
                for lo in ((2,3) if c==1 else (0,1)):
                    for gg,kk in ranges(v,lo,lo+1,q):opts.append((gg,lo,kk))
                inner.append(opts)
            for (ga,la,ka),(gb,lb,kb) in product(*inner):
                yield gs+ga+gb,dict(info,inner=[[la,ka],[lb,kb]])

def witness(P):
    return sum(F(p[0],p[2]) for p in P)/len(P),sum(F(p[1],p[2]) for p in P)/len(P)

def sanity():
    assert clip([(1,1,2)],(2,0,-1))==[(1,1,2)]
    assert apply([SQUARE],((1,0,0),(0,1,0)))==[]
    z=apply([SQUARE],((2,0,-1),));assert all(F(p[0],p[2])<=F(1,2) for P in z for p in P)
    # Preserve the diagonal segment when strict opposite halfplanes are subtracted.
    z=apply(apply([SQUARE],((1,-1,0),)),((-1,1,0),));assert z
    assert all(p[0]==p[1] for P in z for p in P)

progress={'rooms_completed':0,'clauses_applied':0,'three_pass_needed':0,'max_residual_pieces':1,'started':time.time()};records=[]
def save(state,extra=None):
    out={'status':state,'progress':progress,'certificates':records,'effort':EFF,'input_sha256':hashlib.sha256((B/'residual-rooms.json').read_bytes()).hexdigest()}
    if extra:out.update(extra)
    (B/'residual-optical.json').write_text(json.dumps(out,indent=2)+'\n')

def main():
    sanity();rooms=json.loads((B/'residual-rooms.json').read_text())['rooms']
    for room in rooms:
        a,A,b,Bb=map(F,room['rectangle']);pairs=[(a,b),(A,b),(a,Bb),(A,Bb)]
        pieces=[SQUARE];used=[]
        for mode in (1,3):
            if mode==3:progress['three_pass_needed']+=1
            for sheet in sorted(range(4),key=lambda j:room['q'+str(mode)][j]):
                for gs,info in charts(*pairs[sheet],mode):
                    nxt=apply(pieces,gs);progress['clauses_applied']+=1
                    if {tuple(sorted(set(P))) for P in nxt}!={tuple(sorted(set(P))) for P in pieces}:
                        used.append({'sheet':sheet,'guards':gs,'chart':info})
                    pieces=nxt;progress['max_residual_pieces']=max(progress['max_residual_pieces'],len(pieces))
                    if not pieces:break
                if not pieces:break
            if not pieces:break
        if pieces:
            s,t=witness(pieces[0]);assert 0<s<=1 and 0<t<=1
            save('UNCOVERED_BY_ONE_AND_THREE_PASS',{'failure':{'room':room,'s':str(s),'t':str(t),'pieces':pieces,'scope':'failure of these templates only; NOT darkness'}})
            print('FAIL',room['id'],room['rectangle'],s,t,flush=True);return
        records.append({'room_id':room['id'],'clauses':used});progress['rooms_completed']+=1
        if progress['rooms_completed']%100==0:
            (B/'residual-optical-progress.json').write_text(json.dumps(progress,indent=2)+'\n');print(json.dumps(progress),flush=True)
    save('COMPLETE_CONTINUOUS_ONE_THREE_PASS_COVER');print('COMPLETE',json.dumps(progress),flush=True)
if __name__=='__main__':
    try:main()
    except TimeoutError:save('ORIGINAL_DEADLINE_PARTIAL_PREFIX_ONLY');print('TIMEOUT',json.dumps(progress),flush=True)
