"""Independent CE04 exact selector and prescribed original-wall rays; no discovery."""
from fractions import Fraction as Q
from pathlib import Path
from math import gcd,lcm,floor
import ast,json,hashlib
HERE=Path(__file__).parent;AUTHOR=HERE.parent/'construction';REQUEST=AUTHOR/'three-reflex-coprime-extension-sourcewide-review-request.json'
def capture():
    pins=json.loads(REQUEST.read_text())['source_pins'] if REQUEST.exists() else [{'path':str(AUTHOR/('three-reflex-coprime-extension-sourcewide-'+s)),'sha256':hashlib.sha256((AUTHOR/('three-reflex-coprime-extension-sourcewide-'+s)).read_bytes()).hexdigest()} for s in ['candidate.md','proof.md','check.py']]
    for p in pins:assert hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'],p
    return pins
before=capture()
# Only own previously checked pure geometry and one-ray first-hit replay.
helpers={'__file__':str(HERE/'three-reflex-coprime-wide-check.py'),'__name__':'own_prescribed_geometry'}
source=(HERE/'three-reflex-coprime-wide-check.py').read_text().split('\ndef geometry(')[0]
exec(compile(source,'<own-ray-predicates>','exec'),helpers)
ns=helpers['ns'];replay=helpers['rns']['replay_actual']
def ray(label,e,P,K,L,N,b,c,h,H,S,T,q_fixed=None):
    e=Q(e);s,u=map(Q,S);t,v=map(Q,T);a=P*e;A=N*e;l=(N-L)*e;w=(N-K)*e
    assert e>0 and all(isinstance(x,int) for x in (P,K,L,N,b,c,h,H)) and P>=1 and 2<=K<L and P<N-L and 0<b<c<h<H
    assert 0<s<a and b<u<H and l<t<A and 0<v<c and u.denominator==v.denominator==1
    d0=max(int(h-u),0);C=2*(H-h) if u<=h else int(2*H-h-u);g1=h-c;d2=int(c-v);D=d0+C+g1+d2;z=A-t
    delta=gcd(P*C,N);Lam=lcm(P,N,K);assert delta<K and gcd(Lam*d2,L)==1
    good=[]
    for q in range(D):
        tau=(A+z-s+2*e*q)/D
        phases=[(s+(D-d2)*tau-A,K*e)]+([(s+d0*tau,P*e)] if u<h else [])
        if all(((x-end)/(2*e)).denominator!=1 for x,end in phases):good.append(q)
    assert good;q=good[-1] if q_fixed is None else q_fixed;assert q in good
    tau0=(A+z-s+2*e*q)/D;n=floor((s+d0*tau0+a)/(2*a)) if u<=h else 0;z0=s+d0*tau0-2*a*n
    X0=z0+C*tau0;point=(A-X0)/(2*e*delta);nearest=floor(point)+(point-floor(point)>Q(1,2))
    M=nearest*pow(P*C//delta,-1,N//delta)%(N//delta)
    tau=tau0+2*e*P*M;n+=d0*M
    X=z0+C*tau;m=floor(X/(2*A));z1=X-(2*m+1)*A
    k=floor((z1+g1*tau+K*e)/(2*K*e));z2=z1+g1*tau-2*k*K*e
    assert abs(z0)<a and abs(z1)<K*e and abs(z2)<K*e
    J=(z2+d2*tau-z)/(2*e);assert J.denominator==1;initialJ=int(J)
    p=(-int(J)*pow(Lam*d2,-1,L))%L
    tau+=2*e*Lam*p;n+=(Lam//P)*d0*p;m+=(Lam//N)*C*p;k+=(Lam//K)*g1*p
    assert s+d0*tau-2*a*n==z0 and z0+C*tau-(2*m+1)*A==z1 and z1+g1*tau-2*k*K*e==z2
    E=z2+d2*tau;J=(E-z)/(2*e);assert J.denominator==1 and int(J)%L==0 and ns['fold'](E,L*e)==z
    Pgon=[(a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b)]
    singular=u>h and ((s+(H-u)*tau)/A).denominator==1
    if singular:
        assert ns['fold'](s+2*(H-u)*tau,A)==s
        duration=u-v;velocity=(-tau,Q(-1));roofs=0
    else:duration=D;velocity=(tau,Q(1));roofs=1
    result=replay(Pgon,(s,u),(t,v),tau,duration,velocity,roofs)
    if label=='hand-calibration-A':assert q==0 and M==1 and p==0 and tau==15 and J==4
    if label=='hand-calibration-B':assert q==0 and M==6 and p==2 and tau==Q(244,3) and J==81 and z1==0
    if label=='source-seam-strong-guard-identically-bad':assert u==h and ((s-a)/(2*e)).denominator==1
    return dict(label=label,source=S,target=T,parameters=(e,P,K,L,N,b,c,h,H),q=q,M=M,target_shift=p,Lambda=Lam,cap_gcd=delta,slope=tau,initialJ=initialJ,finalJ=int(J),residuals=(z0,z1,z2),singular_prefix_discarded=singular,**result)
fixtures=[
 ('hand-calibration-A',2,3,3,4,11,1,3,5,7,(2,4),(18,2),0),
 ('hand-calibration-B',1,2,2,3,7,1,4,5,6,(1,4),(5,2),0),
 ('source-seam-strong-guard-identically-bad',2,3,3,4,11,1,3,5,7,(2,5),(18,2)),
 ('upper-cap-same-original-room',2,3,3,4,11,1,3,5,7,(2,6),(18,2))]
rows=[ray(*f) for f in fixtures]
out=dict(status='PASS_INDEPENDENT_CE04_PRESCRIBED_ACTUAL_WALLS',source_pins_before=before,source_pins_after=capture(),request_present=REQUEST.exists(),rows=rows,cases=len(rows),reflections=sum(x['reflections'] for x in rows),wall_leg_guards=sum(x['wall_leg_guards'] for x in rows),author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_pins_before','source_pins_after','rows')}))
