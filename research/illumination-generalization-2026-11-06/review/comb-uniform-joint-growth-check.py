"""Prescribed uniform-separation formula controls; no discovery or peer execution."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
from math import gcd,lcm
import json,hashlib,types
R=Path(__file__).resolve().parent
# Load only definitions from our frozen R31 checker, never its top-level writer.
source=(R/'comb-unequal-depth-first-witness-check.py').read_text().split('\nrows=[]',1)[0]
m=types.ModuleType('r31_definitions');m.__dict__['__file__']=str(R/'comb-unequal-depth-first-witness-check.py');exec(compile(source,m.__dict__['__file__'],'exec'),m.__dict__)
effort=json.loads((R/'comb-uniform-joint-growth-effort.json').read_text());m.effort=effort

def uniform(c,u,v,ds,dt,bs,bt,Mmin):
    c,u,v,ds,dt,bs,bt,Mmin=map(Q,(c,u,v,ds,dt,bs,bt,Mmin));assert Mmin>0 and c>0 and min(ds,dt)>0 and 0<bs<u and 0<bt<v
    den=lcm(u.denominator,v.denominator);g=Q(gcd(int(u*den),int(v*den)),den);p=int(u/g);q=int(v/g);U=u*v/g;P=2*g
    Delta=ds-dt;z=Delta/(2*c);a=1+z;b=-1+z
    low=min(0,a*u)+min(0,b*v);high=max(0,a*u)+max(0,b*v);W=high-low;assert W>=P
    primitive=None
    if W>P:mu=(W-P)/4
    else:
        if u==g and (v==g or z==1):primitive='source';shift=2*bs
        else:assert v==g and z==-1;primitive='target';shift=2*bt
        mu=min(shift,P-shift)/4
    rho=min(u,v)*mu/W;A=max(abs((Delta-2*c)/2),abs(-(Delta+2*c)/2));tmin=Mmin/(2*c)
    eta=min(tmin/2,rho/(2*(A+1)))
    Lbar=max(U/eta+1,4*max(u,v)/tmin+1)
    return dict(c=c,u=u,v=v,ds=ds,dt=dt,bs=bs,bt=bt,Mmin=Mmin,g=g,p=p,q=q,U=U,period=P,Delta=Delta,z=z,a=a,b=b,low=low,high=high,W=W,mu=mu,rho=rho,eta=eta,tmin=tmin,Lbar=Lbar,primitive=primitive)

def at_height(d,H):
    H=Q(H);assert H>=d['u']+d['v']+d['Mmin'];ss=st=1
    if d['W']>d['period']:signs=[(1,1)]
    elif d['primitive']=='source':signs=[(1,1),(-1,1)]
    else:signs=[(1,1),(1,-1)]
    found=None
    for ss,st in signs:
        delta=ss*d['bs']-st*d['bt'];C=delta+d['z']*H
        n=int((C-(d['low']+d['mu']))//d['period']);f=C-d['period']*n
        if d['low']+d['mu']<=f<=d['high']-d['mu']:
            found=(ss,st,delta,n,f);break
    assert found is not None
    ss,st,delta,n,f=found;theta=(f-d['low'])/d['W']
    rs=d['u']*theta if d['a']>=0 else d['u']*(1-theta)
    rt=d['v']*theta if d['b']>=0 else d['v']*(1-theta)
    assert min(rs,d['u']-rs,rt,d['v']-rt)>=d['rho']
    t0=(H-rs-rt)/(2*d['c']);assert t0>=d['tmin']
    gg,alpha,beta=m.egcd(d['p'],d['q']);assert gg==1
    ks0=alpha*n;kt0=-beta*n
    C0=H-ss*d['bs']-st*d['bt']+2*d['u']*ks0+2*d['v']*kt0
    return {**d,'H':H,'ss':ss,'st':st,'delta':delta,'n':n,'rs0':rs,'rt0':rt,'tau0':t0,'ks0':ks0,'kt0':kt0,'C0':C0,'D0':d['ds']+d['dt']+2*d['c'],'L0':d['Lbar']}

controls=[(4,2,2,4,4,1,1,2),(4,2,3,1,5,1,1,2),(4,2,4,10,2,1,1,2),(4,4,2,2,10,1,1,2)]
rows=[]
for args in controls:
    d=uniform(*args);L=Q(-((-d['Lbar'])//1))+Q(1,3)
    for add in (Q(0),Q(1,7),Q(17)):
        assert datetime.now(timezone.utc)<datetime.fromisoformat(effort['deadline_utc'])
        H=d['u']+d['v']+d['Mmin']+add;selected=at_height(d,H);result=m.construct(selected,L)
        assert min(result['portal_offsets'][0],d['u']-result['portal_offsets'][0],result['portal_offsets'][1],d['v']-result['portal_offsets'][1])>d['rho']/2
        rows.append({'parameters':args,'H':H,'H_independent_Lbar':d['Lbar'],'uniform_mu':d['mu'],'uniform_rho':d['rho'],'result':result})
# Huge-height controls check the EXACT algebra and integer positivity without
# materializing the enormous finite contact list. They are not path replays.
algebra=[]
for args in controls:
    d=uniform(*args);L=d['Lbar']+Q(1,3)
    for add in (Q(10**6),Q(10**12)+Q(1,11)):
        x=at_height(d,d['u']+d['v']+d['Mmin']+add);den=x['D0']+2*L
        h=int((((den*x['tau0']-x['C0'])/(4*x['U']))+Q(1,2))//1);ks=x['ks0']+x['q']*h;kt=x['kt0']+x['p']*h
        tau=(x['C0']+4*x['U']*h)/den
        rs=x['ss']*x['bs']+(L+x['ds'])*tau-2*x['u']*ks
        rt=x['st']*x['bt']+(L+x['dt'])*tau-2*x['v']*kt
        assert 0<rs<x['u'] and 0<rt<x['v'] and rs+rt+2*x['c']*tau==x['H'] and min(ks,kt)>=0 and abs(tau-x['tau0'])<x['eta']
        algebra.append({'H':x['H'],'L':L,'windings':[ks,kt],'strict_portals':[rs,rt]})
out={'status':'TWELVE_ACTUAL_PATHS_AND_EIGHT_HUGE_HEIGHT_ALGEBRA_CONTROLS_PASS','actual_path_controls':len(rows),'algebra_only_controls':len(algebra),'total_reflections':sum(r['result']['reflections'] for r in rows),'total_wall_leg_guards':sum(r['result']['wall_leg_guards'] for r in rows),'rows':rows,'algebra_only':algebra,'source_sha256':{'comb-unequal-depth-first-witness-check.py':hashlib.sha256((R/'comb-unequal-depth-first-witness-check.py').read_bytes()).hexdigest(),'resumed-exact-check.py':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest()},'whole_goal_complete':False,'discovery':False,'limits':'Uniform-H hand proof is separate. Huge-height arithmetic controls do not materialize or replay trajectories.'}
(R/'comb-uniform-joint-growth-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('rows','algebra_only','source_sha256')}))
