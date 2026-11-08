"""Prescribed R45 formula controls, exact rational original-wall replay; no discovery."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def polygon(D,mu,G,w,f,roof):
    p=[(0,0),(1,0)]
    for lo,hi in [(mu-3,mu-1),(mu+1,mu+3)]:p.extend([(1,lo),(D+2,lo),(D+2,hi),(1,hi)])
    p.extend([(1,G),(0,G)])
    if roof is not None:p.extend([(-roof,G),(-roof,G-2),(0,G-2)])
    p.extend([(0,mu+2),(-w,mu+2),(-w,mu),(0,mu),(0,2),(-f,2),(-f,0)])
    # Remove only collinear vertices on literal rectangle-union boundary.
    while True:
        drop=next((i for i in range(len(p)) if g.det(g.vec(p[i-1],p[i]),g.vec(p[i],p[(i+1)%len(p)]))==0),None)
        if drop is None:break
        p.pop(drop)
    return [tuple(map(Q,z)) for z in p]
def control(D,mu,G,w,f,roof):
    den=w+(5 if D<2 else 6);lower=[Q(2,7),Q(1,4),Q(2,9)][D];upper=[Q(2,5),Q(1,3),Q(1,4)][D]
    j=int((lower*den/2)//1)+1;k=j-1;tau=Q(2*j,den);assert lower<tau<upper
    S=(Q(1+D),Q(mu-2));T=(Q(1+D),Q(mu+2));B=3 if D==0 else D+1
    path=[S,(Q(D+2),mu-2+tau)]
    path += [(Q(x),mu-2+(D+3+i)*tau) for i,x in enumerate([0,1,0,1])]
    P1=mu-2+(D+7)*tau;P2=mu+2-B*tau;A=P1-mu
    assert P1+2*w*tau==P2+4*k
    path.append((Q(0),P1));events={Q(w),Q(2*w)}
    for n in range(int(A//2)+1,int((A+2*w*tau)//2)+1):
        r=(2*n-A)/tau
        if 0<r<2*w:events.add(r)
    assert len(events)==2*k+2
    for r in sorted(events):path.append((-r if r<=w else r-2*w,mu+g.fold(A+tau*r,Q(2))))
    assert path[-1]==(0,P2)
    if D==0:path.append((Q(2),mu+2-tau))
    path.append(T);p=polygon(D,mu,G,Q(w),Q(f),None if roof is None else Q(roof));g.simple(p)
    assert len(p)==(18 if roof is None else 20)
    assert not any(g.on(a,b,T) for a,b in zip(path[:-2],path[1:-1]))
    res=g.path_check(p,path);assert res['reflections']==(7 if D==0 else 6)+2*k
    return {'D':D,'mu':mu,'G':G,'w':w,'f':str(f),'roof':str(roof),'j':j,'k':k,'tau':str(tau),'polygon':p,'path':path,**res}
rows=[]
for D,cut in enumerate([13,20,67]):
    for mu,G,roof in [(4,8,None),(4,10,Q(1,3)),(5,10,10001),(27,56,7001),(28,56,Q(7,4))]:
        for w in [cut,cut+1,cut+73]:rows.append(control(D,mu,G,w,Q(100003,7),roof))
out={'status':'R45_PRESCRIBED_FORMULAS_PASS','discovery':False,'rows':rows,'paths':len(rows),'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'whole_goal_complete':False,'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['minimal-depth-shuttle-proof.md','resumed-exact-check.py']}}
(R/'minimal-depth-shuttle-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_sha256']}))
