"""R35 prescribed actual branch-safe transits and returns, no discovery."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
eff=json.loads((R/'two-sided-star-effort.json').read_text())
def deadline():assert datetime.now(timezone.utc)<datetime.fromisoformat(eff['deadline_utc'])
def polygon(c,left,right,ymin,ymax):
    p=[(Q(0),ymin),(c,ymin)]
    for lo,hi,w in right:p.extend([(c,lo),(c+w,lo),(c+w,hi),(c,hi)])
    p.extend([(c,ymax),(Q(0),ymax)])
    for lo,hi,w in reversed(left):p.extend([(Q(0),hi),(-w,hi),(-w,lo),(Q(0),lo)])
    p=[z for i,z in enumerate(p) if i==0 or z!=p[i-1]]
    if p[-1]==p[0]:p.pop()
    while any(g.det(g.vec(p[i-1],z),g.vec(z,p[(i+1)%len(p)]))==0 for i,z in enumerate(p)):
        p=[z for i,z in enumerate(p) if g.det(g.vec(p[i-1],z),g.vec(z,p[(i+1)%len(p)]))!=0]
    g.simple(p);return p

def prefix(D,u,t,n):
    k=n//2;sgn=1 if n%2==0 else -1;r=sgn*u/2+D*t-2*u*k;assert 0<r<u
    path=[(D,u/2)]
    for j in range(1 if sgn==1 else 0,2*k+1):
        x=D-(j*u-sgn*u/2)/t;assert 0<x<D;path.append((x,u if j%2 else Q(0)))
    return path+[(Q(0),r)],r

def transit(c,u,v,H,Ds,Dt,lower_side,lo):
    deadline();A=c+Ds+Dt;t=Q(0);bound=int(Ds*H/(c*u)+Q(1,2))+int(Dt*H/(c*v)+Q(1,2))+3
    assert H>(u+v)/2
    for j in range(bound):
        ns=int((Ds*t/u+Q(1,2))//1);nt=int((Dt*t/v+Q(1,2))//1);nxt=(H-(u+v)/2+u*ns+v*nt)/A
        assert t<=nxt<=H/c
        if nxt==t:break
        t=nxt
    else:raise AssertionError('finite matching did not terminate')
    ps,rs=prefix(Ds,u,t,ns);pt,rt=prefix(Dt,v,t,nt);assert rs+rt+c*t==H
    if lower_side=='left':path=[(-x,lo+y) for x,y in ps]+[(c+x,lo+H-y) for x,y in reversed(pt)]
    else:path=[(c+x,lo+y) for x,y in ps]+[(-x,lo+H-y) for x,y in reversed(pt)]
    return path,{'slope':t,'iterations':j,'counts':[ns,nt]}
rows=[]
for c,u,v,H,Ds,Dt,side in [(3,2,2,6,1,4,'left'),(1,4,5,5,Q(1,9),Q(7,3),'right'),(2,7,2,6,5,Q(1,7),'left'),(Q(3,2),Q(4,3),Q(7,2),8,Q(7,4),Q(1,5),'right')]:
    c,u,v,H,Ds,Dt=map(Q,(c,u,v,H,Ds,Dt));lo=Q(3);path,data=transit(c,u,v,H,Ds,Dt,side,lo)
    sb=(lo,lo+u,Ds+1);tb=(lo+H-v,lo+H,Dt+1)
    left=[sb] if side=='left' else[tb];right=[tb] if side=='left' else[sb]
    V=polygon(c,left,right,Q(0),lo+H+3);result=g.path_check(V,path);assert result['reflections']==sum(data['counts'])
    rows.append({'kind':'opposite','overlapping_bands':H<u+v,**data,**result})
# Fixed same-side controls with an actual open opposite mouth at the old mirror point.
for c,D,u,d,m,v,w in [(3,1,2,4,6,2,4),(1,Q(1,9),3,5,9,Q(3,2),Q(1,7)),(2,8,4,7,12,5,2),(3,1,2,4,6,2,20)]:
    c,D,u,d,m,v,w=map(Q,(c,D,u,d,m,v,w));lo=m-d-u/2;H=d+(u+v)/2
    half,data=transit(c,u,v,H,D,w,'right',lo);assert half[-1]==(-w,m)
    path=half+[(x,2*m-y) for x,y in reversed(half[:-1])]
    left=[(m-v/2,m+v/2,w)];right=[(m-d-u/2,m-d+u/2,D+1),(m+d-u/2,m+d+u/2,D+2)]
    if u==v==2 and d==4:right.insert(1,(m-1,m+1,D+3))
    V=polygon(c,left,right,Q(0),m+d+u/2+1);res=g.path_check(V,path)
    assert res['reflections']==2*sum(data['counts'])+1
    assert not any(g.on(a,b,path[-1]) for a,b in zip(path[:-2],path[1:-1]))
    rows.append({'kind':'actual_far_wall_return','polygon_walls':len(V),'old_mirror_is_open_mouth':g.location(V,(Q(0),m))==1,'source':path[0],'target':path[-1],'far_wall':half[-1],**data,**res})
assert all(r['old_mirror_is_open_mouth'] for r in rows if r['kind']=='actual_far_wall_return')
assert rows[4]['polygon_walls']==20 and rows[4]['source']==(4,2) and rows[4]['target']==(4,10)
out={'status':'EIGHT_PRESCRIBED_ACTUAL_TRANSITS_AND_RETURNS_PASS','rows':rows,'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'discovery':False,'whole_goal_complete':False,'source_sha256':{'resumed-exact-check.py':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest()}}
(R/'two-sided-star-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
