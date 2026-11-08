"""LJ01 five prescribed Euclidean constructions and existing actual-wall replay.
No discovery, room sweep, new tracing engine, or author code execution.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd,floor,ceil,lcm
import ast,json,hashlib
HERE=Path(__file__).parent
ns={'Q':Q,'F':Q};geometry_tree=ast.parse((HERE/'resumed-exact-check.py').read_text())
geometry_names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
exec(compile(ast.Module(body=[f for f in geometry_tree.body if isinstance(f,ast.FunctionDef) and f.name in geometry_names],type_ignores=[]),'<existing-own-pure-geometry>','exec'),ns)
fold=ns['fold'];txt=(HERE/'three-reflex-coprime-independent-check.py').read_text();tree=ast.parse(txt);fn=next(f for f in tree.body if isinstance(f,ast.FunctionDef) and f.name=='replay_actual')
code=ast.get_source_segment(txt,fn).replace('def replay_actual(P,S,T,slope,D):','def replay_actual(P,S,T,slope,D,initial_velocity,expected_floor=None):').replace('velocity=(slope,Q(1))','velocity=initial_velocity')
code=code.replace('assert len(roofs)==len(horizontal)==1',"assert len(roofs)==1\n    if expected_floor is None:assert len(horizontal)==1\n    else:\n        floors=[e for e in horizontal if e['point'][1]==expected_floor]\n        assert len(horizontal)==2 and len(floors)==1\n        assert floors[0]['time']==S[1]-expected_floor")
rns={'Q':Q,'ns':ns};exec(compile(code,'<existing-own-floor-roof-or-suffix-replay>','exec'),rns);replay=rns['replay_actual']
def bezout2(a,b):
 aa,bb=abs(a),abs(b);r0,r1=aa,bb;s0,s1=1,0;t0,t1=0,1
 while r1:q=r0//r1;r0,r1=r1,r0-q*r1;s0,s1=s1,s0-q*s1;t0,t1=t1,t0-q*t1
 return r0,s0*(1 if a>=0 else -1),t0*(1 if b>=0 else -1)
def bezout_list(values):
 gg=0;coeff=[0]*len(values)
 for i,value in enumerate(values):
  ng,x,y=bezout2(gg,value);coeff=[x*v for v in coeff];coeff[i]+=y;gg=ng
 assert sum(x*y for x,y in zip(values,coeff))==gg
 return gg,coeff

def data(params,S,T,tau):
 e,P,K,L,N,b,c,h,H=params;e=Q(e);s,u=map(Q,S);t,v=map(Q,T);a=P*e;A=N*e;R=K*e
 r=(h+u-2*b)/2;n=H-h;f=(h-v)/2;d=r+n+f
 ni=floor((s+2*r*tau+a)/(2*a));z0=s+2*r*tau-2*a*ni
 mi=floor((z0+2*n*tau)/(2*A));z1=z0+2*n*tau-(2*mi+1)*A
 ki=floor((z1+(h-c)*tau+R)/(2*R));z2=z1+(h-c)*tau-2*R*ki
 return dict(indices=[ni,mi,ki],residuals=[z0,z1,z2],E=z2+(c-v)*tau,r=r,n=n,f=f,d=d)
def physical(label,params,S,T,tau):
 e,P,K,L,N,b,c,h,H=params;e=Q(e);s,u=map(Q,S);t,v=map(Q,T);a=P*e;A=N*e;R=K*e;tau=Q(tau)
 assert 0<b<c<h<H and b<u<=h and 0<s<a and (N-L)*e<t<A and 0<v<c and 1<=K<L and N>P+L
 dd=data(params,S,T,tau);z0,z1,z2=dd['residuals'];assert abs(z0)<a and abs(z1)<R and abs(z2)<R and fold(dd['E'],L*e)==A-t
 formalD=2*dd['d'];floorx=fold(s+(u-b)*tau,a);singular=floorx in(0,a)
 assert ((z0+(H-h)*tau)/A).denominator!=1
 if singular:
  assert fold(s+2*(u-b)*tau,a)==s and 2*(u-b)<=2*dd['r']
  duration=formalD-2*(u-b);velocity=(-tau,Q(1));floor=None
 else:duration=formalD;velocity=(tau,-Q(1));floor=Q(b)
 polygon=[(a,b),(a,h),((N-K)*e,h),((N-K)*e,c),((N-L)*e,c),((N-L)*e,0),(A,0),(A,H),(0,H),(0,b)]
 ray=replay(polygon,(s,u),(t,v),tau,duration,velocity,floor)
 return dict(label=label,parameters=params,S=S,T=T,slope=tau,floor_x=floorx,floor_corner_suffix_used=singular,formal_duration=formalD,retained_duration=duration,**dd,**ray)
def select(params,S,T,fixed=None):
 e,P,K,L,N,b,c,h,H=params;e=Q(e);s,u=map(Q,S);t,v=map(Q,T);A=N*e;z=A-t
 assert P%2 and N%2 and h%2==0 and c%2 and all(x.denominator==1 and int(x)%2==0 for x in (u,v))
 r=(h+u-2*b)/2;n=H-h;f=(h-v)/2;d=r+n+f;assert all(Q(x).denominator==1 and x>0 for x in (r,n,f,d));r,n,f,d=map(int,(r,n,f,d))
 Lam=lcm(P,N,K);d2=int(c-v);g=gcd(Lam*d2,L);assert K%g==0
 H0=gcd(gcd(P*N*f,P*g*n),N*g*r);Hx=gcd(gcd(P*(n+f),N*r),g*r);assert H0<K*Hx
 vectors=[(-P*(n+f),-P*f),(N*r,-N*f),(g*r,g*(r+n))]
 xs=[x for x,y in vectors];ys=[y for x,y in vectors];hx,wcoeff=bezout_list(xs);assert hx==Hx
 yw=sum(y*c for y,c in zip(ys,wcoeff))
 fiber_triples=[];fiber_values=[]
 for i,(x,y) in enumerate(vectors):
  mult=x//Hx;assert x==mult*Hx
  coeff=[-mult*w for w in wcoeff];coeff[i]+=1
  assert sum(xx*c for xx,c in zip(xs,coeff))==0
  yy=sum(y*c for y,c in zip(ys,coeff));fiber_triples.append(coeff);fiber_values.append(yy)
 Fy,fcoeff=bezout_list(fiber_values);assert Fy*Hx==d*H0
 fibercoeff=[sum(c*row[i] for c,row in zip(fcoeff,fiber_triples)) for i in range(3)]
 assert sum(x*c for x,c in zip(xs,fibercoeff))==0 and sum(y*c for y,c in zip(ys,fibercoeff))==Fy
 C0=(n+f)*s+r*A+r*z;C1=f*(s-A)+(r+n)*z
 wx=floor(-C0/(2*e*Hx)+Q(1,2));wy=floor(-(C1/(2*e)+wx*yw)/Fy+Q(1,2))
 triple=[wx*w+wy*ff for w,ff in zip(wcoeff,fibercoeff)];ni,mi,j=triple
 if fixed is not None:ni,mi,j=fixed
 q=P*ni+N*mi+g*j
 z0=(C0+2*e*sum(x*c for x,c in zip(xs,(ni,mi,j))))/d;z1=(C1+2*e*sum(y*c for y,c in zip(ys,(ni,mi,j))))/d
 assert abs(z0)<P*e and abs(z1)<K*e
 if fixed is None:assert abs(z0)<=e*Hx/d<P*e and abs(z1)<=e*H0/Hx<K*e
 sn=r*N*g//H0;sm=n*P*g//H0;sj=f*P*N//H0;sq=P*sn+N*sm+g*sj
 assert all(x>0 for x in (sn,sm,sj,sq)) and H0*sq==P*N*g*d
 raw=(ni,mi,j,q);shift=max(0,ceil(Q(-ni,sn)),ceil(Q(-mi,sm)),ceil(Q(-q,sq)))
 ni+=sn*shift;mi+=sm*shift;j+=sj*shift;q+=sq*shift
 assert min(ni,mi,q)>=0
 def tau(q):return (A+z-s+2*e*q)/(2*d)
 dt=data(params,S,T,tau(q));assert dt['indices'][:2]==[ni,mi] and dt['residuals'][:2]==[z0,z1]
 ret=data(params,S,T,tau(q+sq));assert ret['residuals'][:2]==[z0,z1]
 return_slope=e*P*N*g/H0;assert tau(q+sq)-tau(q)==return_slope and ((h-c)*return_slope/(2*K*e)).denominator!=1
 repair=abs(dt['residuals'][2])==K*e
 if repair:ni+=sn;mi+=sm;j+=sj;q+=sq;dt=data(params,S,T,tau(q))
 assert abs(dt['residuals'][2])<K*e
 ki=dt['indices'][2];J=q-P*ni-N*mi-K*ki;assert J%g==0 and J==g*j-K*ki and dt['E']==z+2*e*J
 modulus=L//g;coefficient=Lam*d2//g;p=0 if modulus==1 else (-J//g*pow(coefficient,-1,modulus))%modulus
 final=tau(q)+2*e*Lam*p;end=data(params,S,T,final)
 assert end['residuals']==dt['residuals'] and end['E']==dt['E']+2*e*Lam*d2*p
 increments=[Q(2*r*Lam*p,P),Q(2*n*Lam*p,N),Q((h-c)*Lam*p,K)];assert all(x.denominator==1 for x in increments)
 assert end['indices']==[int(x+y) for x,y in zip(dt['indices'],increments)] and (J+Lam*d2*p)%L==0
 return dict(r=r,n=n,f=f,d=d,g=g,H0=H0,Hx=Hx,Fy=Fy,vectors=vectors,wcoeff=wcoeff,fibercoeff=fibercoeff,raw_triple=raw,positive_shift=shift,selected_triple=(ni,mi,j,q),right_repair=repair,J=J,p=p,final_slope=final)
A=(4,1,4,8,11,2,3,6,7);C=(2,3,4,8,13,2,3,6,7)
fixtures=[('A-P1-lower',A,(2,4),(16,2),None),('B-P1-mouth',A,(2,6),(16,2),None),('C-P3-H06-lower',C,(2,4),(12,2),None),('D-P3-mouth',C,(2,6),(12,2),None),('E-native-floor-corner-suffix',A,(2,4),(18,2),(13,0,1))]
rows=[]
for label,params,S,T,fixed in fixtures:
 sel=select(params,S,T,fixed);rows.append(dict(selection=sel,**physical(label,params,S,T,sel['final_slope'])))
assert rows[2]['selection']['H0']==6 and rows[0]['selection']['Hx']==3
assert rows[-1]['slope']==17 and rows[-1]['residuals']==[0,-10,9] and rows[-1]['E']==26 and rows[-1]['floor_corner_suffix_used'] and rows[-1]['retained_duration']==8
out=dict(status='PASS_LJ01_FIVE_PRESCRIBED_EUCLIDEAN_SOURCE_CAP_CONSTRUCTIONS_AND_GENUINE_WALLS',rows=rows,cases=len(rows),reflections=sum(x['reflections'] for x in rows),wall_leg_guards=sum(x['wall_leg_guards'] for x in rows),author_code_executed=False,discovery_search_used=False,independent_peer_review='pending',whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
