"""Exact prescribed checks of the interval/Bezout first-witness construction."""
from fractions import Fraction as Q
from math import gcd,lcm
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,importlib.util
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');own=importlib.util.module_from_spec(sp);sp.loader.exec_module(own)
effort=json.loads((R/'comb-unequal-depth-first-witness-effort.json').read_text())
def deadline():assert datetime.now(timezone.utc)<datetime.fromisoformat(effort['deadline_utc'])
def egcd(a,b):
    if not b:return a,1,0
    g,x,y=egcd(b,a%b);return g,y,x-(a//b)*y

def prepare(c,H,u,v,ds,dt,bs,bt):
    c,H,u,v,ds,dt,bs,bt=map(Q,(c,H,u,v,ds,dt,bs,bt))
    assert c>0 and H>u+v and ds>0 and dt>0 and 0<bs<u and 0<bt<v
    den=lcm(u.denominator,v.denominator);g=Q(gcd(int(u*den),int(v*den)),den);p=int(u/g);q=int(v/g);U=u*v/g;period=2*g
    Delta=ds-dt;z=Delta/(2*c);a=1+z;b=-1+z
    low=min(0,a*u)+min(0,b*v);high=max(0,a*u)+max(0,b*v);width=high-low
    assert width>=period
    choices=[];picked=None
    for ss,st in ((1,1),(1,-1),(-1,1),(-1,-1)):
        delta=ss*bs-st*bt;C=delta+z*H;n=int((C-low)//period);f=C-period*n
        if f==low and width>period:n-=1;f+=period
        choices.append({'signs':[ss,st],'n':n,'f':f,'strict':low<f<high})
        if low<f<high:
            theta=(f-low)/width
            rs=u*theta if a>=0 else u*(1-theta)
            rt=v*theta if b>=0 else v*(1-theta)
            picked=(ss,st,delta,n,rs,rt);break
    assert picked is not None
    ss,st,delta,n,rs,rt=picked;assert 0<rs<u and 0<rt<v
    tau0=(H-rs-rt)/(2*c);assert a*rs+b*rt==delta+z*H-period*n and tau0>0
    gg,alpha,beta=egcd(p,q);assert gg==1 and alpha*p+beta*q==1
    ks0=alpha*n;kt0=-beta*n;assert 2*u*ks0-2*v*kt0==period*n
    C0=H-ss*bs-st*bt+2*u*ks0+2*v*kt0;D0=ds+dt+2*c
    ass=(Delta-2*c)/2;att=-(Delta+2*c)/2
    eta=min(tau0/2,rs/(2*(abs(ass)+1)),(u-rs)/(2*(abs(ass)+1)),rt/(2*(abs(att)+1)),(v-rt)/(2*(abs(att)+1)))
    ceil=lambda z:-((-z)//1)
    hmin=max(0,int(ceil(Q(-ks0,q))),int(ceil(Q(-kt0,p))))
    dbound=max(2*U/eta+1,(abs(C0)+4*U*(hmin+1))/tau0+1)
    L0=max(Q(0),(dbound-D0)/2)
    return dict(c=c,H=H,u=u,v=v,ds=ds,dt=dt,bs=bs,bt=bt,g=g,p=p,q=q,U=U,Delta=Delta,ss=ss,st=st,delta=delta,n=n,rs0=rs,rt0=rt,tau0=tau0,eta=eta,ks0=ks0,kt0=kt0,C0=C0,D0=D0,L0=L0,choices=choices,width=width,period=period)

def construct(d,L,lo=5):
    deadline();L=Q(L);assert L>=d['L0'];c,H,u,v,ds,dt,bs,bt=(d[k] for k in ('c','H','u','v','ds','dt','bs','bt'))
    den=d['D0']+2*L;h=int(((den*d['tau0']-d['C0'])/(4*d['U'])+Q(1,2))//1)
    ks=d['ks0']+d['q']*h;kt=d['kt0']+d['p']*h;assert min(ks,kt)>=0
    tau=(d['C0']+4*d['U']*h)/den;assert abs(tau-d['tau0'])<d['eta']
    Ds=ds+L;Dt=dt+L;rs=d['ss']*bs+Ds*tau-2*u*ks;rt=d['st']*bt+Dt*tau-2*v*kt
    assert 0<rs<u and 0<rt<v and rs+rt+2*c*tau==H and tau>0
    N=d['period']*d['n'];assert rs==(H+d['delta']-N+(d['Delta']-2*c)*tau)/2
    assert rt==(H-d['delta']+N-(d['Delta']+2*c)*tau)/2
    def tooth(D,b,w,k,sg):
        return [(c+D,b)]+[(c+D-(j*w-sg*b)/tau,w if j%2 else Q(0)) for j in range(1 if sg==1 else 0,2*k+1)]
    lower=tooth(Ds,bs,u,ks,d['ss']);upper=tooth(Dt,bt,v,kt,d['st'])
    assert all(x>c for x,y in lower[1:]+upper[1:])
    path=[(x,y+lo) for x,y in lower+[(Q(0),rs+c*tau)]+[(x,H-y) for x,y in reversed(upper)]]
    hg=H+10;teeth=[(Q(0),Q(2),c+L+3),(Q(lo),Q(lo)+u,c+Ds+5),(Q(lo)+H-v,Q(lo)+H,c+Dt+5),(H+8,hg,c+L+6)]
    poly=[(Q(0),Q(0)),(teeth[0][2],Q(0))]
    for j,(bottom,top,right) in enumerate(teeth):
        poly.append((right,top))
        if j<3:
            nxt=teeth[j+1];assert top<nxt[0];poly.extend([(c,top),(c,nxt[0]),(nxt[2],nxt[0])])
    poly.append((Q(0),hg));own.simple(poly)
    check=own.path_check(poly,path);expect=2*ks+2*kt+1+(d['ss']==-1)+(d['st']==-1);assert check['reflections']==expect
    assert all(not own.on(a,b,path[-1]) for a,b in zip(path[:-2],path[1:-1]))
    return {'L':L,'signs':[d['ss'],d['st']],'h':h,'windings':[ks,kt],'tau':tau,'portal_offsets':[rs,rt],**check,'path':path}
rows=[]
parameters=[(4,10,2,2,4,4,1,1),(4,20,2,3,1,5,1,1),(4,16,2,4,10,2,1,1),(4,16,4,2,2,10,1,1),(4,6,2,2,6,2,1,1),(3,15,Q(3,2),Q(9,4),Q(5,3),Q(7,2),Q(1,2),Q(5,4))]
for args in parameters:
    deadline();d=prepare(*args);L=Q(-((-d['L0'])//1))+Q(1,3)
    result=construct(d,L);rows.append({'parameters':args,'L0':d['L0'],'interval_width':d['width'],'period':d['period'],'phase_choices':d['choices'],'result':result})
assert rows[2]['interval_width']==rows[2]['period'] and rows[2]['result']['signs']!=[1,1]
assert rows[3]['interval_width']==rows[3]['period'] and rows[3]['result']['signs']!=[1,1]
assert rows[4]['interval_width']==rows[4]['period'] and rows[4]['result']['signs']!=[1,1]
mixed=[]
c=Q(4);L=Q(13);D=L+2;lo=Q(17);w=Q(4);bt=Q(1);hg=Q(26)
teeth=[(Q(0),Q(2),Q(20)+L),(Q(5),Q(7),Q(19)+L),(lo,lo+w,c+D+5),(Q(24),hg,Q(21)+L)]
poly=[(Q(0),Q(0)),(teeth[0][2],Q(0))]
for j,(_,top,right) in enumerate(teeth):
    poly.append((right,top))
    if j<3:
        nxt=teeth[j+1];poly.extend([(c,top),(c,nxt[0]),(nxt[2],nxt[0])])
poly.append((Q(0),hg));own.simple(poly)
for xs,ys in ((Q(4),Q(6)),(Q(2),Q(25))):
    C=c+xs;t0=(lo+w/2-ys)/C;den=D+C
    k=int((((den*t0+ys-lo-bt)/(2*w))+Q(1,2))//1)
    image=lo+bt+2*w*k;tau=(image-ys)/den;portal=ys+C*tau
    assert D>C and lo<portal<lo+w and tau!=0
    point=(Q(0),ys+xs*tau);assert 0<point[1]<hg
    events=[]
    for j in range(int((min(portal,image)-lo)//w)-1,int((max(portal,image)-lo)//w)+2):
        y=lo+j*w
        if min(portal,image)<y<max(portal,image):
            x=(y-ys)/tau-xs;assert c<x<c+D
            yy=lo+(w if j%2 else 0);events.append((x,yy))
    path=[(xs,ys),point]+sorted(events)+[(c+D,lo+bt)]
    guard=own.path_check(poly,path);mixed.append({'source':(xs,ys),'target':path[-1],'tau':tau,'portal':portal,'path':path,**guard})
seam=[(c,Q(6)),(Q(0),Q(13)),(c,Q(20))]
seam_guard=own.path_check(poly,seam)
out={'status':'ALL_SIX_BEZOUT_AND_THREE_SPINE_CONTROLS_PASS','rows':rows,'spine_controls':mixed,'seam_control':{'path':seam,**seam_guard},'total_reflections':sum(r['result']['reflections'] for r in rows)+sum(r['reflections'] for r in mixed)+seam_guard['reflections'],'total_wall_leg_guards':sum(r['result']['wall_leg_guards'] for r in rows)+sum(r['wall_leg_guards'] for r in mixed)+seam_guard['wall_leg_guards'],'discovery':False,'whole_goal_complete':False,'source_sha256':{'resumed-exact-check.py':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest()},'scope':'Supplied formula controls at explicit rational cutoff, including primitive-width equality sign changes, arbitrary unequal depths/heights, rational L. General all-real-L quantifier follows from hand proof.'}
(R/'comb-unequal-depth-first-witness-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('rows','spine_controls','seam_control','source_sha256')}))
