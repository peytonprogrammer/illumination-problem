"""Prescribed proof replay: verify every saved strict chart and continuous cover."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd,lcm
import json,hashlib,time,signal
B=Path(__file__).parent
# This fixed verification is bounded too; no search restart or clock alteration.
started=time.time()
def timeout(*_):raise TimeoutError('840 second prescribed replay bound')
signal.signal(signal.SIGALRM,timeout);signal.setitimer(signal.ITIMER_REAL,840)
def hnorm(p):
    div=gcd(gcd(abs(p[0]),abs(p[1])),abs(p[2]));assert div and p[2]
    p=tuple(x//div for x in p);return tuple(-x for x in p) if p[2]<0 else p

def value(g,p):return g[0]*p[0]+g[1]*p[1]+g[2]*p[2]
def clip(P,g):
    out=[]
    for C,D in zip(P,P[1:]+P[:1]):
        c,d=value(g,C),value(g,D)
        if c>=0:out.append(C)
        if c*d<0:out.append(hnorm(tuple(c*y-d*x for x,y in zip(C,D))))
    return list(dict.fromkeys(out))
def valid(P):return P and max(p[0] for p in P)>0 and max(p[1] for p in P)>0

def subtract(P,gs):
    if any(max(value(g,p) for p in P)<=0 for g in gs):return [P]
    if all(min(value(g,p) for p in P)>0 for g in gs):return []
    result=[];R=P
    for g in gs:
        Q=clip(R,tuple(-x for x in g))
        if valid(Q):result.append(Q)
        R=clip(R,g)
        if not R:break
    return result

def guards(room,clause):
    a,A,b,Bb=map(F,room['rectangle']);U,V=[(a,b),(A,b),(a,Bb),(A,Bb)][clause['sheet']]
    D=lcm(U.denominator,V.denominator);p=int(U*D);r=int(V*D)
    info=clause['chart'];ell=info['mode'];assert ell in (1,3);q=p+r+ell*D
    assert room['q'+str(ell)][clause['sheet']]==q
    u,eps,M,c=[info[n] for n in ['u','eps','M','c']]
    assert u in (0,2) and eps in (1,-1) and c in (1,3) and 0<=M<q
    l0=1 if c==1 else 2;l1={(0,1):1,(0,3):2,(2,1):0,(2,3):3}[u,c]
    intervals=[(0,l0,info['shifts'][0]),(ell,l1,info['shifts'][1])]
    if ell==3:
        for j,(lo,k) in enumerate(info['inner'],1):
            assert lo in ((2,3) if c==1 else (0,1));intervals.append((j,lo,k))
    gs=[]
    for j,lo,k in intervals:
        n=p+j*D;v=(q-n,eps*n,n*(u+4*M));gs.extend([(v[0],v[1],v[2]-q*(lo+4*k)),(-v[0],-v[1],q*(lo+1+4*k)-v[2])])
    assert [list(g) for g in gs]==clause['guards']
    return gs

def main():
    raw=(B/'residual-rooms.json').read_bytes();roomdata=json.loads(raw);rooms=roomdata['rooms'];proof=json.loads((B/'residual-optical.json').read_text())
    assert proof['status']=='COMPLETE_CONTINUOUS_ONE_THREE_PASS_COVER'
    assert proof['input_sha256']==hashlib.sha256(raw).hexdigest()
    assert len(rooms)==roomdata['room_count']==len(proof['certificates'])==22538
    count=0;three=0
    for i,(room,cert) in enumerate(zip(rooms,proof['certificates'])):
        assert room['id']==cert['room_id']==i
        pieces=[[(0,0,1),(1,0,1),(1,1,1),(0,1,1)]];used3=False
        for clause in cert['clauses']:
            gs=guards(room,clause);count+=1;used3|=clause['chart']['mode']==3
            out={}
            for P in pieces:
                for Q in subtract(P,gs):out[tuple(sorted(set(Q)))]=Q
            pieces=list(out.values())
        assert not pieces,('NONEMPTY_CERTIFICATE_COMPLEMENT',i)
        three+=used3
    out={'status':'PASS_ALL_FROZEN_CONTINUOUS_COVER_CERTIFICATES','rooms':len(rooms),'prescribed_chart_clauses':count,'rooms_using_three_pass':three,'elapsed_seconds':time.time()-started,'source_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ['residual-rooms.json','residual-optical.py','residual-optical.json','residual-optical-proof.md']},'independent_review':False,'scope':'Only frozen optical certificates; upstream support/algebra/margins require independent review.'}
    (B/'residual-optical-replay.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
