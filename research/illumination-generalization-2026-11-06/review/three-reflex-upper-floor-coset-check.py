"""UP03 independent algebra and prescribed original-wall verification.
Fixed inputs only; no author code execution or discovery effort.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd,floor,ceil
import ast,hashlib,json
HERE=Path(__file__).parent
REQUEST=HERE.parent/'construction/three-reflex-upper-floor-coset-review-request.json'
def pins():
 result=[]
 for item in json.loads(REQUEST.read_text())['source_pins']:
  h=hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()
  assert h==item['sha256'],item
  result.append(dict(item,actual=h,passed=True))
 return result
before=pins();request_hash=hashlib.sha256(REQUEST.read_bytes()).hexdigest()
# Reuse reviewer-owned exact geometric predicates, not author arithmetic.
helpers={'__file__':str(HERE/'three-reflex-coprime-wide-check.py'),'__name__':'own_upper_geometry'}
exec(compile((HERE/'three-reflex-coprime-wide-check.py').read_text().split('\ndef geometry(')[0],'<own-existing-predicates>','exec'),helpers)
ns=helpers['ns'];fold=ns['fold']
txt=(HERE/'three-reflex-coprime-independent-check.py').read_text();tree=ast.parse(txt)
f=next(f for f in tree.body if isinstance(f,ast.FunctionDef) and f.name=='replay_actual')
code=ast.get_source_segment(txt,f).replace('def replay_actual(P,S,T,slope,D):','def replay_actual(P,S,T,slope,D,initial_velocity,expected_floor=None):').replace('velocity=(slope,Q(1))','velocity=initial_velocity')
code=code.replace('assert len(roofs)==len(horizontal)==1',"assert len(roofs)==1\n    if expected_floor is None:assert len(horizontal)==1\n    else:\n        floors=[e for e in horizontal if e['point'][1]==expected_floor]\n        assert len(horizontal)==2 and len(floors)==1\n        assert floors[0]['time']==S[1]-expected_floor")
rns={'Q':Q,'ns':ns};exec(compile(code,'<own-earliest-wall-upper-floor>','exec'),rns);replay=rns['replay_actual']
def chart(e,P,L,N,b,c,h,H,S,T,tau):
 e=Q(e);s,u=map(Q,S);t,v=map(Q,T);tau=Q(tau)
 a=P*e;A=N*e;dp=u-h;dl=2*(h-b);C=2*(H-h);g1=h-c;d2=c-v;D=dp+dl+C+g1+d2
 ip=floor((s+dp*tau+A)/(2*A));zp=s+dp*tau-2*A*ip
 il=floor((zp+dl*tau+a)/(2*a));z0=zp+dl*tau-2*a*il
 im=floor((z0+C*tau)/(2*A));z1=z0+C*tau-(2*im+1)*A
 ik=floor((z1+g1*tau+e)/(2*e));z2=z1+g1*tau-2*e*ik
 return dict(indices=[ip,il,im,ik],residuals=[zp,z0,z1,z2],E=z2+d2*tau,D=D,durations=[dp,dl,C,g1,d2])
def physical(label,params,S,T,tau,theorem_member):
 e,P,L,N,b,c,h,H=params;e=Q(e);s,u=map(Q,S);t,v=map(Q,T);tau=Q(tau);a=P*e;A=N*e
 assert 0<b<c<h<u<H and 0<s<a and (N-L)*e<t<A and 0<v<c and N>P+L
 d=chart(e,P,L,N,b,c,h,H,S,T,tau);zp,z0,z1,z2=d['residuals'];dp,dl,C,g1,d2=d['durations'];D=d['D']
 assert abs(zp)<a and abs(z0)<a and abs(z1)<e and abs(z2)<e and fold(d['E'],L*e)==A-t
 assert ((z0+(H-h)*tau)/A).denominator!=1
 f=u-b;floorx=fold(zp+(h-b)*tau,a);singular=floorx in(0,a)
 if singular:
  assert z0==-zp and fold(z0+dp*tau,A)==s and (z0+dp*tau+s)%(2*A)==0
  duration=D-2*f;velocity=(-tau,Q(1));expected_floor=None
 else:
  duration=D;velocity=(tau,-Q(1));expected_floor=Q(b)
 polygon=[(a,b),(a,h),((N-1)*e,h),((N-1)*e,c),((N-L)*e,c),((N-L)*e,0),(A,0),(A,H),(0,H),(0,b)]
 result=replay(polygon,(s,u),(t,v),tau,duration,velocity,expected_floor)
 assert result['roof']['time']==(H-u if singular else dp+dl+H-h)
 return dict(label=label,parameters=params,source=S,target=T,slope=tau,theorem_member=theorem_member,floor_x=floorx,floor_corner_suffix_used=singular,retained_duration=duration,**d,**result)
def select(params,S,T,initial_center,threshold_skip):
 e,P,L,N,b,c,h,H=params;e=Q(e);s,u=map(Q,S);t,v=map(Q,T);a=P*e;A=N*e;z=A-t
 dp=u-h;dl=2*(h-b);C=2*(H-h);g1=h-c;d2=c-v;D=dp+dl+C+g1+d2
 deltaN=N//gcd(N,int(dp/2));aP=P//gcd(P,h-b);a0=aP*deltaN
 assert P%2 and N%2 and N>P+L and L>=2 and L&(L-1)==0
 assert h%2==0 and c%2 and gcd(P*(H-h),N)==1 and P>=deltaN+4
 assert all(x.denominator==1 and int(x)%2==0 for x in (s,u,t,v))
 base=(A+z-s)/D;dy=2*e*dp/D;Y0=s+dp*base
 ip=initial_center;lo=2*A*ip-a;hi=2*A*ip+a
 start=floor((lo-Y0)/dy)+1;end=ceil((hi-Y0)/dy)-1
 assert start>0 and end>=start
 def tau(q):return base+2*e*q/D
 def X(q):
  ch=chart(e,P,L,N,b,c,h,H,S,T,tau(q));return ch['residuals'][1]+C*tau(q)
 Xstart=X(start);Xend=X(end);rho=2*e*(dp+dl+C)/D;spacing=2*e*deltaN
 assert tau(end)-tau(start)>=2*a/dp-4*e/D
 assert Xend-Xstart>C*(2*a/dp-4*e/D)-2*a>2*a-4*e>=spacing+4*e>spacing+2*rho
 j=floor((Xstart+2*rho-A-e)/spacing)+1+threshold_skip;U=A+e+spacing*j
 assert Xstart+2*rho<U<=Xend
 values=[(q,X(q)) for q in range(start,end+1)]
 assert all(abs(s+dp*tau(q)-2*A*ip)<a for q,x in values)
 jumps=[q for (q0,x0),(q,x) in zip(values,values[1:]) if x<x0]
 assert all(x-x0<=rho for (q0,x0),(q,x) in zip(values,values[1:]))
 cross=next(q for q,x in values if x>=U);q=cross-1
 assert cross>start+2 and U-2*e<X(q)<U
 ch0=chart(e,P,L,N,b,c,h,H,S,T,tau(q));zp,z0=ch0['residuals'][:2]
 assert abs(zp)<a and abs(z0)<a
 z1=X(q)-(A+spacing*j);assert abs(z1)<e
 quotient=N//deltaN;M0=(-j*pow((H-h)*aP,-1,quotient))%quotient
 t0=tau(q);mid=t0+e*a0*M0;ch=chart(e,P,L,N,b,c,h,H,S,T,mid)
 assert ch['residuals'][:3]==[zp,z0,z1]
 flip=abs(ch['residuals'][3])==e;M=M0+quotient if flip else M0
 mid=t0+e*a0*M;ch=chart(e,P,L,N,b,c,h,H,S,T,mid);assert abs(ch['residuals'][3])<e
 J=(ch['E']-z)/(2*e);assert J.denominator==1
 ip,il,im,ik=ch['indices'];assert J==q+D*a0*M/2-N*ip-P*il-N*im-ik
 coefficient=aP*N*int(d2);p=(-int(J)*pow(coefficient,-1,L))%L
 final=mid+2*e*aP*N*p;chf=chart(e,P,L,N,b,c,h,H,S,T,final)
 assert chf['residuals']==ch['residuals'] and chf['E']==ch['E']+2*e*coefficient*p
 assert (J+coefficient*p)%L==0
 inc=[dp*aP*p,Q(2*(h-b)*aP*N*p,P),2*(H-h)*aP*p,g1*aP*N*p]
 assert all(Q(x).denominator==1 for x in inc)
 assert chf['indices']==[int(x+y) for x,y in zip(ch['indices'],inc)]
 return dict(deltaN=deltaN,aP=aP,a0=a0,block=[start,end],Xstart=Xstart,Xend=Xend,rho=rho,threshold=U,qcross=cross,q=q,backward_jumps=jumps,M0=M0,M=M,N_flip_used=flip,p=p,seed_J=J,final_slope=final)
params=(2,7,4,15,1,3,4,15);S=(4,14);T=(26,2);rows=[]
for label,center,skip in [('author-control',1,0),('own-next-cap-threshold',1,1),('own-next-initial-branch',2,0)]:
 sel=select(params,S,T,center,skip);ray=physical(label,params,S,T,sel['final_slope'],True)
 rows.append(dict(selection=sel,**ray))
assert rows[0]['slope']==Q(4053,4) and rows[0]['indices']==[169,217,371,254]
assert rows[0]['selection']['block']==[35,62] and 37 in rows[0]['selection']['backward_jumps']
assert rows[0]['selection']['threshold']==116 and rows[0]['selection']['qcross']==46 and rows[0]['selection']['q']==45
assert request_hash==hashlib.sha256(REQUEST.read_bytes()).hexdigest()
out=dict(status='PASS_UP03_INDEPENDENT_JOINT_CAP_COSET_SELECTION_AND_ORIGINAL_WALLS',source_pins_before=before,source_pins_after=pins(),request_sha256=request_hash,rows=rows,cases=len(rows),reflections=sum(r['reflections'] for r in rows),wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_pins_before','source_pins_after']}))
