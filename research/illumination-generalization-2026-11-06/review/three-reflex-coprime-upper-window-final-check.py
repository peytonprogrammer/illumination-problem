"""Independent CE08 full residue-choice, actual-wall replay and frozen pins."""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd,lcm,floor
import json,hashlib
HERE=Path(__file__).parent;AUTHOR=HERE.parent/'construction'
REQUEST=AUTHOR/'three-reflex-coprime-extension-upperwindow-review-request.json'
def capture():
 pins=json.loads(REQUEST.read_text())['source_pins']
 for p in pins:assert hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'],p
 return pins
before=capture();request_hash=hashlib.sha256(REQUEST.read_bytes()).hexdigest()
# Import ONLY reviewer predicates and earliest-wall replay, never author code.
source=(HERE/'three-reflex-coprime-source-width-check.py').read_text().split('\ndef ray(')[0]
helpers={'__file__':str(HERE/'three-reflex-coprime-source-width-check.py'),'__name__':'own_ray_helpers'}
exec(compile(source,'<own-existing-pure-geometry>','exec'),helpers)
replay=helpers['replay'];fold=helpers['ns']['fold']
def ray(label,e,P,K,L,N,b,c,h,H,S,T,m=None,q=None):
 e=Q(e);s,u=map(Q,S);t,v=map(Q,T);a=P*e;A=N*e;w=A-K*e;l=A-L*e
 assert e>0 and all(isinstance(x,int) for x in (P,K,L,N,b,c,h,H)) and P>=1 and 2<=K<L and P<N-L and 0<b<c<h<H
 assert 0<s<a and h<=u<H and l<t<A and 0<v<c and u.denominator==v.denominator==1
 C=int(2*H-h-u);g1=h-c;d2=int(c-v);D=C+g1+d2;z=A-t;Lam=lcm(N,K);g=gcd(Lam*d2,L)
 assert K%g==0 and K*D>2*g*C
 B=s+C*(A+z-s)/D
 if m is None:m=max(0,floor((B+K*e-A)/(2*A))+1)
 lower=((2*m+1)*A-K*e-B)*D/(2*e*C);upper=lower+Q(K*D,C)
 first=N*m+g*(floor((lower-N*m)/g)+1)
 candidates=[first,first+g]
 assert all(lower<x<upper for x in candidates)
 pbad=K*D//gcd(C+g1,K*D);assert pbad>K>=g
 def data(q):
  tau=(A+z-s+2*e*q)/D;z1=s+C*tau-(2*m+1)*A
  Y=z1+g1*tau;k=floor((Y+K*e)/(2*K*e));z2=Y-2*K*e*k
  return tau,z1,Y,k,z2
 good=[x for x in candidates if ((data(x)[2]-K*e)/(2*K*e)).denominator!=1]
 assert good
 if q is None:q=next(x for x in good if x>=0)
 assert q>=0 and lower<q<upper and (q-N*m)%g==0
 tau,z1,Y,k,z2=data(q);assert abs(z1)<K*e and abs(z2)<K*e
 J=(z2+d2*tau-z)/(2*e);assert J.denominator==1 and int(J)%g==0
 initialJ=int(J);mod=L//g;p=0 if mod==1 else (-int(J)//g*pow(Lam*d2//g,-1,mod))%mod
 oldm=m;oldk=k;tau+=2*e*Lam*p;m+=(Lam//N)*C*p;k+=(Lam//K)*g1*p
 assert s+C*tau-(2*m+1)*A==z1 and z1+g1*tau-2*K*e*k==z2
 E=z2+d2*tau;J=(E-z)/(2*e);assert J.denominator==1 and int(J)%L==0 and fold(E,L*e)==z
 Pgon=[(a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b)]
 singular=u>h and ((s+(H-u)*tau)/A).denominator==1
 if singular:
  assert fold(s+2*(H-u)*tau,A)==s
  duration=u-v;velocity=(-tau,-Q(1));roofs=0
 else:duration=D;velocity=(tau,Q(1));roofs=1
 result=replay(Pgon,(s,u),(t,v),tau,duration,velocity,roofs)
 return dict(label=label,parameters=(e,P,K,L,N,b,c,h,H),source=S,target=T,q=q,cap_index=oldm,cap_interval=(lower,upper),two_indices=candidates,good_indices=good,bad_period=pbad,target_gcd=g,Lambda=Lam,initialJ=initialJ,target_shift=p,slope=tau,finalJ=int(J),residuals=(z1,z2),singular_prefix_discarded=singular,**result)
fixtures=[
 ('CE08-A',4,1,3,4,9,1,3,6,10,(2,8),(28,2),0,1),
 ('CE08-B-mouth',4,1,3,4,9,2,3,4,10,(2,4),(28,2),0,0),
 ('CE08-C-g2',4,1,6,8,11,2,3,4,10,(2,4),(28,2),0,2),
 ('CE08-D-corner-alternative',1,1,2,3,8,1,3,5,7,(Q(1,2),6),(Q(39,5),1),2,41),
 ('open-endpoint-equality',4,1,3,4,9,1,3,6,10,(3,8),(34,2),0,1),
 ('first-index-bad-second-good',4,1,3,4,9,1,3,6,10,(2,8),(Q(242,9),2),0,2)]
rows=[ray(*f) for f in fixtures]
expected=[(Q(221),28),(Q(3),0),(Q(7429,7),128),(Q(3137,70),45)]
assert [(r['slope'],r['finalJ']) for r in rows[:4]]==expected
assert rows[4]['cap_interval'][0]==0
# Author D: independent actual right-corner phase for discarded q42.
tau=Q(131,10);X=Q(1,2)+3*tau;z1=X-40;Y=z1+2*tau
assert 38<X<42 and Y==26 and (Y-2)%4==0
# C wrong target class: BOTH portals strict but no admissible final shift.
tau=Q(33,7);z1=2+12*tau-44;z2=z1+tau;J=(z2+tau-16)/8
assert abs(z1)<24 and abs(z2)<24 and J==1 and gcd(66,8)==2 and int(J)%2!=0
# Existing singular final-slope control, independently replayed retained suffix.
Pgon=[(4,1),(4,5),(12,5),(12,4),(8,4),(8,0),(20,0),(20,7),(0,7),(0,1)]
assert fold(Q(2)+2*Q(18),Q(20))==2
suffix=replay(Pgon,(Q(2),Q(6)),(Q(10),Q(2)),Q(18),Q(4),(-Q(18),-Q(1)),0)
rows.append(dict(label='singular-exact-S-suffix',slope=18,singular_prefix_discarded=True,**suffix))
assert request_hash==hashlib.sha256(REQUEST.read_bytes()).hexdigest()
out=dict(status='PASS_INDEPENDENT_CE08_FULL_RESIDUE_CHOICE_ACTUAL_RAYS',source_pins_before=before,source_pins_after=capture(),request_sha256=request_hash,rows=rows,cases=len(rows),reflections=sum(r['reflections'] for r in rows),wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),true_corner_alternative_q42=True,strict_portal_wrong_target_class_q1=True,author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('rows','source_pins_before','source_pins_after')}))
