"""Prescribed exact A32 proof controls; no peer imports or discovery."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def polygon(c,bands,ymin,ymax):
    p=[(Q(0),ymin),(c,ymin)]
    for lo,hi,right in bands:p.extend([(c,lo),(right,lo),(right,hi),(c,hi)])
    p.extend([(c,ymax),(Q(0),ymax)])
    p=[z for i,z in enumerate(p) if i==0 or z!=p[i-1]]
    while any(g.det(g.vec(p[i-1],z),g.vec(z,p[(i+1)%len(p)]))==0 for i,z in enumerate(p)):
        p=[z for i,z in enumerate(p) if g.det(g.vec(p[i-1],z),g.vec(z,p[(i+1)%len(p)]))!=0]
    g.simple(p);return p

def prefix(c,D,u,tau,n):
    sign=1 if n%2==0 else -1;k=n//2;r=sign*u/2+D*tau-2*u*k;assert 0<r<u
    p=[(c+D,u/2)]
    for j in range(1 if sign==1 else 0,2*k+1):
        x=c+D-(j*u-sign*u/2)/tau;assert c<x<c+D
        p.append((x,u if j%2 else Q(0)))
    p.append((c,r));return p,r

def two(c,u,v,H,Ds,Dt):
    c,u,v,H,Ds,Dt=map(Q,(c,u,v,H,Ds,Dt));A=Ds+Dt+2*c;t=Q(0);outputs=[]
    for iteration in range(10000):
        ns=int((Ds*t/u+Q(1,2))//1);nt=int((Dt*t/v+Q(1,2))//1)
        nxt=(H-(u+v)/2+u*ns+v*nt)/A;assert t<=nxt<=H/(2*c)
        if nxt==t:break
        outputs.append(t);t=nxt
    else:raise AssertionError('prescribed iteration guard')
    assert t>0 and (Ds*t/u+Q(1,2)).denominator!=1 and (Dt*t/v+Q(1,2)).denominator!=1
    p,rs=prefix(c,Ds,u,t,ns);q,rt=prefix(c,Dt,v,t,nt)
    assert rs+rt+2*c*t==H
    path=p+[(Q(0),rs+c*t)]+[(x,H-y) for x,y in reversed(q)]
    bands=[(Q(0),u,c+Ds+1),(u+(H-u-v)/3,u+2*(H-u-v)/3,c+2),(H-v,H,c+Dt+Q(1,2))]
    V=polygon(c,bands,Q(-1),H+1);result=g.path_check(V,path);assert result['reflections']==ns+nt+1
    # Actual target occurs on no earlier leg.
    assert not any(g.on(a,b,path[-1]) for a,b in zip(path[:-2],path[1:-1]))
    return {'parameters':[c,u,v,H,Ds,Dt],'slope':t,'iterations':iteration,'parities':[ns%2,nt%2],**result}

def mixed(xs,ys,D):
    c=Q(3);lo=Q(7);u=Q(2);xs,ys,D=map(Q,(xs,ys,D));C=c+xs
    low=((lo-ys)*(C+D)/C+ys-lo-u/2)/u
    n=int(low//1)+1;t=(lo+u/2+u*n-ys)/(C+D);z=ys+C*t;assert lo<z<lo+u
    image=lo+u/2+u*n;events=[]
    for j in range(int((min(z,image)-lo)//u)-1,int((max(z,image)-lo)//u)+2):
        y=lo+j*u
        if min(z,image)<y<max(z,image):
            x=(y-ys)/t-xs;assert c<x<c+D
            events.append((x,lo+(u if j%2 else 0)))
    path=[(xs,ys),(Q(0),ys+xs*t),(c,z)]+sorted(events)+[(c+D,lo+u/2)]
    bands=[(Q(1),Q(3),Q(5)),(lo,lo+u,c+D+1),(Q(12),Q(14),Q(6))];V=polygon(c,bands,Q(0),Q(15))
    return {'source':path[0],'target':path[-1],'n':n,'slope':t,**g.path_check(V,path)}
rows=[two(*args) for args in [(1,2,2,7,Q(1,10),Q(1,20)),(1,2,3,9,1,2),(2,1,4,13,7,3),(3,4,1,15,2,11),(1,3,5,12,9,8),(2,3,2,9,Q(2,3),Q(7,4)),(1,2,2,50,10,10),(Q(3,2),Q(5,3),Q(7,4),11,Q(1,4),12)]]
rows += [mixed(*args) for args in [(1,1,Q(1,10)),(3,2,1),(2,14,Q(1,7)),(3,13,4)]]
V=polygon(Q(3),[(Q(1),Q(3),Q(5)),(Q(7),Q(9),Q(6)),(Q(12),Q(14),Q(6))],Q(0),Q(15))
rows.append({'seam':True,**g.path_check(V,[(Q(3),Q(2)),(Q(0),Q(5)),(Q(3),Q(8))])})
out={'status':'THIRTEEN_PRESCRIBED_ACTUAL_PATHS_PASS','rows':rows,'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'scope':'Exact rational formula controls; arbitrary-real theorem audited by hand. No search or peer code execution.','whole_goal_complete':False,'source_sha256':{'resumed-exact-check.py':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest()}}
(R/'midheight-comb-independent-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
