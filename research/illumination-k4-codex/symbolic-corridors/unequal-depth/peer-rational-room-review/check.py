"""Independent7-clause continuous square cover; own guards/geometry/slabs."""
from pathlib import Path
from fractions import Fraction as F
from math import lcm
import json,hashlib
B=Path(__file__).parent
P=B.parents[1]/'unequal-depth-independent/rational-room-audit'
A,b,hm,hp=F(1,2),F(1),F(3,4),F(5,4)
VERTICES=[(F(0),F(0)),(F(1),F(0)),(F(1),F(1)),(F(0),F(1))]
BOX={(0,1):((1,2),(1,2)),(0,3):((2,3),(2,3)),(2,1):((1,2),(0,1)),(2,3):((2,3),(3,4))}
def val(g,s,t):return g[0]*s+g[1]*t+g[2]
def norm(g):
    x=next(v for v in g if v);return tuple(v/x for v in g)
def fold(x):
    r=x%4;return r if r<=2 else 4-r

def derive(row):
    low,up=row['lc'],row['uc'];a0=2*hm-A if low else A;b0=2*hp-b if up else b
    H=a0+1+b0;u,eps,M,c=row['u'],row['eps'],row['M'],row['c']
    gs0=[tuple(map(F,g)) for g in row['guards']];gs=[]
    for i,(time,I) in enumerate(zip([a0/H,(a0+1)/H],BOX[u,c])):
        E=(1-time,time*eps,time*(u+4*M))
        k=(E[2]-I[0]-gs0[2*i][2])/4
        assert k.denominator==1
        gs.extend([(E[0],E[1],E[2]-I[0]-4*k),(-E[0],-E[1],I[1]+4*k-E[2])])
    assert gs==gs0
    caps=[];times=[a0/H,(a0+1)/H]
    for gamma,isupper in ([( (a0-hm)/H,False)] if low else [])+([((a0+1+hp)/H,True)] if up else []):
        times.append(gamma);E=(1-gamma,gamma*eps,gamma*(u+4*M)-(u if isupper else 0))
        lo,hi=min(val(E,*v) for v in VERTICES),max(val(E,*v) for v in VERTICES)
        for j in range(-((-lo/2).__floor__()),(hi/2).__floor__()+1):caps.append((E[0],E[1],E[2]-2*j))
    assert lcm(*(x.denominator for x in times))==row['period']
    return {'source_index':row['source_index'],'lc':low,'uc':up,'u':u,'eps':eps,'M':M,'c':c,'guards':gs,'bad':caps}

def sub(A,B):return tuple(x-y for x,y in zip(A,B))
def cross(v,w):return v[0]*w[1]-v[1]*w[0]
def inside(P,poly):
    x,y=P;count=0
    for C,D in zip(poly,poly[1:]+poly[:1]):
        if cross(sub(P,C),sub(D,C))==0 and all(min(c,d)<=p<=max(c,d) for c,d,p in zip(C,D,P)):return False
        if (C[1]>y)!=(D[1]>y):count+=C[0]+(y-C[1])*(D[0]-C[0])/(D[1]-C[1])>x
    return count%2==1

def physical(s,t,row):
    a0=2*hm-A if row['lc'] else A;b0=2*hp-b if row['uc'] else b;H=a0+1+b0
    L=row['u']+row['eps']*t+4*row['M'];v=(L-s)/H;assert v
    X=lambda y:s+v*(y+a0)
    event=[]
    for ya,yb,offset,add in [(-a0,F(0),0,0),(F(0),F(1),row['c'],1),(F(1),1+b0,row['u'],0)]:
        lo,hi=sorted((X(ya),X(yb)))
        for j in range(((lo-offset)/2).__floor__()-1,((hi-offset)/2).__floor__()+2):
            x=F(offset+2*j)
            if lo<x<hi:
                y=-a0+(x-s)/v;event.append((y,add+fold(x-offset)))
    if row['lc']:event.append((-hm,fold(X(-hm))))
    if row['uc']:event.append((1+hp,fold(X(1+hp)-row['u'])))
    event.sort()
    Y=lambda y:-2*hm-y if y<-hm else 2*(1+hp)-y if y>1+hp else y
    path=[(s,-A)]+[(x,Y(y)) for y,x in event]+[(t,1+b)]
    target=path[-1];trimmed=False
    for i,(C,D) in enumerate(zip(path,path[1:])):
        vec=sub(D,C)
        if cross(sub(target,C),vec)==0:
            j=0 if vec[0] else 1;tau=(target[j]-C[j])/vec[j]
            if 0<tau<=1:
                trimmed=i<len(path)-2 or tau<1
                path=path[:i+1]+[target];break
    poly=[(0,-hm),(2,-hm),(2,0),(3,0),(3,1),(2,1),(2,1+hp),(0,1+hp),(0,1),(1,1),(1,0),(0,0)]
    poly=[tuple(map(F,p)) for p in poly]
    assert inside(path[0],poly) and inside(path[-1],poly)
    for i,(C,D) in enumerate(zip(path,path[1:])):
        v0=sub(D,C);assert v0!=(0,0)
        assert inside(tuple((x+y)/2 for x,y in zip(C,D)),poly)
        hits=[]
        for E,G in zip(poly,poly[1:]+poly[:1]):
            w=sub(G,E);det=cross(v0,w)
            if not det:
                if cross(sub(E,C),v0)==0:
                    j=0 if v0[0] else 1;lo,hi=sorted(((E[j]-C[j])/v0[j],(G[j]-C[j])/v0[j]));assert hi<=0 or lo>=1
                continue
            tau=cross(sub(E,C),w)/det;u=cross(sub(E,C),v0)/det
            if 0<tau<=1 and 0<=u<=1:
                assert tau==1 and 0<u<1;hits.append((E,G))
        if i==len(path)-2:assert not hits
        else:
            assert len(hits)==1
            E,G=hits[0];r=(-v0[0],v0[1]) if E[0]==G[0] else (v0[0],-v0[1]);out=sub(path[i+2],D)
            assert cross(r,out)==0 and sum(x*y for x,y in zip(r,out))>0
    return len(path)-2,trimmed

def main():
    request=json.loads((P/'review-request.json').read_text())
    for name,digest in request['source_sha256'].items():assert hashlib.sha256((P/name).read_bytes()).hexdigest()==digest
    saved=json.loads((P/'result.json').read_text());ids=sorted(map(int,saved['selected_clause_counts']))
    assert ids==[0,1,2,4,5,8,18]
    cs=[]
    for i in ids:
        row=saved['clauses'][i];row['source_index']=i;cs.append(derive(row))
    lines={norm(g) for c in cs for g in c['guards']+c['bad'] if g[0] or g[1]}
    lines|={(F(1),F(0),F(0)),(F(1),F(0),F(-1)),(F(0),F(1),F(0)),(F(0),F(1),F(-1))}
    lines=sorted(lines);xs={F(0),F(1)}
    for i,(a,b,c) in enumerate(lines):
        if b==0 and a and 0<=-c/a<=1:xs.add(-c/a)
        for A,Bb,C in lines[i+1:]:
            det=a*Bb-b*A
            if det:
                x=(b*C-c*Bb)/det
                if 0<=x<=1:xs.add(x)
    z=sorted(xs);points=[]
    for s in sorted(xs|{(a+b)/2 for a,b in zip(z,z[1:])}):
        if not s:continue
        ys={F(0),F(1)}
        for a,b,c in lines:
            if b:
                t=-(a*s+c)/b
                if 0<=t<=1:ys.add(t)
        z=sorted(ys)
        for t in sorted(ys|{(a+b)/2 for a,b in zip(z,z[1:])}):
            if t:points.append((s,t))
    records=[]
    for s,t in points:
        hit=next((r for r in cs if all(val(g,s,t)>0 for g in r['guards']) and all(val(g,s,t)!=0 for g in r['bad'])),None)
        assert hit is not None,('uncovered',s,t)
        contacts,trimmed=physical(s,t,hit)
        records.append({'s':str(s),'t':str(t),'clause':hit['source_index'],'contacts':contacts,'early_target_trim':trimmed})
    out={'status':'INDEPENDENT_FIXED_ROOM_COVER_ACCEPTED','selected_clauses':ids,'arrangement_lines':len(lines),
         'admissible_sign_cells_and_actual_paths':len(records),'wall_contacts':sum(r['contacts'] for r in records),
         'early_target_trims':sum(r['early_target_trim'] for r in records),'source_sha256':request['source_sha256'],
         'records':records,'scope':'ONE fixed rational vertical parameter room, all real0<s,t<=1; L reduction covers rest. No general rational theorem.'}
    (B/'check.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','records')}))
if __name__=='__main__':main()
