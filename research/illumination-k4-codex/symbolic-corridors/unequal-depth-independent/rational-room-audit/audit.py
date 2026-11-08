"""One fixed rational room: exact continuous four-cap-chart audit."""
from fractions import Fraction as F
from pathlib import Path
from math import lcm
from itertools import product
import json,time,hashlib
HERE=Path(__file__).resolve().parent
EFF=json.loads((HERE/'effort.json').read_text());DEADLINE=EFF['deadline_epoch']
DOMAIN=[(F(0),F(0)),(F(1),F(0)),(F(1),F(1)),(F(0),F(1))]
BOXES=[(0,1,(1,2),(1,2)),(0,3,(2,3),(2,3)),(2,1,(1,2),(0,1)),(2,3,(2,3),(3,4))]

def guard():
    if time.time()>=DEADLINE:raise TimeoutError('original aggregate840s deadline')
def value(g,p):return g[0]*p[0]+g[1]*p[1]+g[2]
def area(P):return abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(P,P[1:]+P[:1])))
def clip(P,L,sign=1):
    out=[]
    for a,b in zip(P,P[1:]+P[:1]):
        x,y=sign*value(L,a),sign*value(L,b)
        if x>=0:out.append(a)
        if x*y<0:
            z=x/(x-y);out.append(tuple(u+z*(v-u) for u,v in zip(a,b)))
    clean=[]
    for p in out:
        if not clean or p!=clean[-1]:clean.append(p)
    if len(clean)>1 and clean[0]==clean[-1]:clean.pop()
    return clean if len(clean)>=3 and area(clean)>0 else []
def center(P):return tuple(sum(p[k] for p in P)/len(P) for k in (0,1))
def norm(g):
    z=next(a for a in g if a);return tuple(a/z for a in g)
def transform(alpha,u,eps,M):return 1-alpha,alpha*eps,alpha*(u+4*M)
def periodic_shifts(E,I):
    lo,hi=min(value(E,p) for p in DOMAIN),max(value(E,p) for p in DOMAIN)
    return [k for k in range(((lo-I[1])/4).__floor__()-1,((hi-I[0])/4).__floor__()+2) if lo<I[1]+4*k and hi>I[0]+4*k]
def strict_guards(E,I,k):return [(E[0],E[1],E[2]-I[0]-4*k),(-E[0],-E[1],I[1]+4*k-E[2])]

def enumerate_clauses():
    a,b,hm,hp=map(F,['1/2','1','3/4','5/4']);cs=[];sheets=[]
    for lc,uc in product((0,1),repeat=2):
        A=2*hm-a if lc else a;B=2*hp-b if uc else b;H=A+1+B
        alpha,beta=A/H,(A+1)/H
        caps=[]
        if lc:caps.append(((A-hm)/H,0))
        if uc:caps.append(((A+1+hp)/H,1))
        Q=lcm(*(x.denominator for x in [alpha,beta]+[c[0] for c in caps]))
        sheets.append({'lc':lc,'uc':uc,'period':Q})
        for u,c,I,J in BOXES:
            for eps in (1,-1):
                for M in range(Q):
                    guard();E1,E2=transform(alpha,u,eps,M),transform(beta,u,eps,M)
                    for k1,k2 in product(periodic_shifts(E1,I),periodic_shifts(E2,J)):
                        gs=strict_guards(E1,I,k1)+strict_guards(E2,J,k2)
                        P=DOMAIN
                        for g in gs:
                            P=clip(P,g)
                            if not P:break
                        if not P or not all(value(g,center(P))>0 for g in gs):continue
                        bad=[]
                        for gamma,upper in caps:
                            E=transform(gamma,u,eps,M)
                            if upper:E=(E[0],E[1],E[2]-u)
                            lo,hi=min(value(E,p) for p in P),max(value(E,p) for p in P)
                            for j in range(-((-lo/2).__floor__()),(hi/2).__floor__()+1):
                                L=(E[0],E[1],E[2]-2*j)
                                if min(value(L,p) for p in P)<=0<=max(value(L,p) for p in P):bad.append(L)
                        cs.append({'lc':lc,'uc':uc,'u':u,'c':c,'eps':eps,'M':M,'period':Q,'guards':gs,'cap_bad_lines':bad})
    return cs,sheets

def covers(c,p):return all(value(g,p)>0 for g in c['guards']) and all(value(g,p)!=0 for g in c['cap_bad_lines'])

def direct_validate_absence(p,sheets):
    s,t=p;a,b,hm,hp=map(F,['1/2','1','3/4','5/4']);tests=0;valid=[]
    for row in sheets:
        lc,uc,Q=row['lc'],row['uc'],row['period'];A=2*hm-a if lc else a;B=2*hp-b if uc else b;H=A+1+B
        for u,c,I,J in BOXES:
            for eps in (1,-1):
                for M in range(Q):
                    tests+=1;D=u+eps*t+4*M-s
                    E1=(s+A*D/H)%4;E2=(s+(A+1)*D/H)%4
                    if not I[0]<E1<I[1] or not J[0]<E2<J[1]:continue
                    if lc and (s+(A-hm)*D/H)%2==0:continue
                    if uc and (s+(A+1+hp)*D/H-u)%2==0:continue
                    valid.append((lc,uc,u,c,eps,M))
    assert not valid
    return {'complete_period_chart_tests':tests,'valid_candidates':valid}

def main():
    cs,sheets=enumerate_clauses();print(json.dumps({'stage':'clauses','retained':len(cs),'periods':sheets}),flush=True)
    lines=sorted({norm(g) for c in cs for g in c['guards']+c['cap_bad_lines'] if g[0] or g[1]})
    polys=[DOMAIN]
    print(json.dumps({'stage':'arrangement','lines':len(lines)}),flush=True)
    for i,L in enumerate(lines):
        guard();out=[]
        for P in polys:
            guard()
            out.extend(Q for Q in (clip(P,L),clip(P,L,-1)) if Q)
        polys=out
        if i%10==0:print(json.dumps({'line':i+1,'polygons':len(polys),'elapsed':time.time()-EFF['started_epoch']}),flush=True)
    reps=set()
    for P in polys:
        reps.add(center(P))
        for a,b in zip(P,P[1:]+P[:1]):
            reps.add(a);reps.add(tuple((x+y)/2 for x,y in zip(a,b)))
    bad=[];cnt=0;selected={}
    for p in sorted(reps):
        guard()
        if not 0<p[0]<=1 or not 0<p[1]<=1:continue
        cnt+=1
        hit=next((j for j,c in enumerate(cs) if covers(c,p)),None)
        if hit is None:
            bad.append({'s':str(p[0]),'t':str(p[1]),'independent_period_validation':direct_validate_absence(p,sheets)})
        else:selected[hit]=selected.get(hit,0)+1
    out={'status':'FIXED_ROOM_CAP_COVER_PROVED' if not bad else 'FIXED_ROOM_CAP_MECHANISM_FAILURES_VALIDATED','parameters':EFF['parameters'],'domain':EFF['endpoint_domain'],'retained_clauses':len(cs),'sheets':sheets,'arrangement_lines':len(lines),'open_faces':len(polys),'admissible_sign_cells':cnt,'uncovered':bad,'selected_clause_counts':selected,'elapsed_seconds_including_setup':time.time()-EFF['started_epoch'],'clauses':cs,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'One prescribed rational room and four specified cap-sheet families only. Continuous sign-cell proof includes edges/vertices/cap-corner exclusions. No darkness or universal commensurable conclusion.'}
    def serial(x):
        if isinstance(x,F):return str(x)
        raise TypeError(type(x).__name__)
    (HERE/'result.json').write_text(json.dumps(out,default=serial,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('clauses','selected_clause_counts','uncovered')}),flush=True)
    if bad:print(json.dumps({'first_failure':bad[0],'failed_sign_cells':len(bad)}),flush=True)
if __name__=='__main__':main()
