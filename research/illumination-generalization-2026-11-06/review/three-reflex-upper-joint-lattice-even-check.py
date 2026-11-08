"""UJ02 independent cap-orbit selection and prescribed actual-wall checks."""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd,floor,ceil,lcm
import ast,json,hashlib
HERE=Path(__file__).parent;REQUEST=HERE.parent/'construction/three-reflex-upper-joint-lattice-even-review-request.json'
def pins():
 rows=[]
 for item in json.loads(REQUEST.read_text())['source_pins']:
  digest=hashlib.sha256(Path(item['path']).read_bytes()).hexdigest();assert digest==item['sha256'],item
  rows.append(dict(item,actual=digest,passed=True))
 return rows
before=pins();request_hash=hashlib.sha256(REQUEST.read_bytes()).hexdigest()
helpers={'__file__':str(HERE/'three-reflex-coprime-wide-check.py'),'__name__':'own_uc01_geometry'}
exec(compile((HERE/'three-reflex-coprime-wide-check.py').read_text().split('\ndef geometry(')[0],'<own-geometry-predicates>','exec'),helpers)
ns=helpers['ns'];fold=ns['fold'];txt=(HERE/'three-reflex-coprime-independent-check.py').read_text();tree=ast.parse(txt);f=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='replay_actual')
code=ast.get_source_segment(txt,f).replace('def replay_actual(P,S,T,slope,D):','def replay_actual(P,S,T,slope,D,initial_velocity,roof_required):').replace('velocity=(slope,Q(1))','velocity=initial_velocity')
code=code.replace('assert len(roofs)==len(horizontal)==1','assert len(roofs)==len(horizontal)==int(roof_required)').replace('roof=roofs[0]','roof=roofs[0] if roofs else None')
rns={'Q':Q,'ns':ns};exec(compile(code,'<own-earliest-wall-roof-or-exact-S-suffix>','exec'),rns);replay=rns['replay_actual']
def chart(params,S,T,tau):
 e,P,K,L,N,b,c,h,H=params;e=Q(e);s,u=map(Q,S);t,v=map(Q,T);A=N*e;R=K*e;C=2*H-h-u;D=2*H-u-v;tau=Q(tau)
 m=floor((s+C*tau)/(2*A));z1=s+C*tau-(2*m+1)*A
 k=floor((z1+(h-c)*tau+R)/(2*R));z2=z1+(h-c)*tau-2*R*k
 return dict(C=C,D=D,indices=[m,k],residuals=[z1,z2],E=z2+(c-v)*tau)
def physical(label,params,S,T,tau):
 e,P,K,L,N,b,c,h,H=params;e=Q(e);s,u=map(Q,S);t,v=map(Q,T);a=P*e;A=N*e;R=K*e;tau=Q(tau)
 assert 1<=K<L and N>P+L and 0<b<c<h<=u<H and 0<s<A and (N-L)*e<t<A and 0<v<c
 if u==h:assert 0<s<a
 ch=chart(params,S,T,tau);z1,z2=ch['residuals'];assert abs(z1)<R and abs(z2)<R and fold(ch['E'],L*e)==A-t
 roofphase=s+(H-u)*tau;singular=(roofphase/A).denominator==1
 if singular:
  assert u>h and fold(s+2*(H-u)*tau,A)==s
  duration=ch['D']-2*(H-u);assert duration==u-v
  velocity=(-tau,-Q(1));roof_required=False
 else:duration=ch['D'];velocity=(tau,Q(1));roof_required=True
 polygon=[(a,b),(a,h),((N-K)*e,h),((N-K)*e,c),((N-L)*e,c),((N-L)*e,0),(A,0),(A,H),(0,H),(0,b)]
 result=replay(polygon,(s,u),(t,v),tau,duration,velocity,roof_required)
 return dict(label=label,parameters=params,S=S,T=T,slope=tau,formal_roof_phase=roofphase,roof_corner_suffix_used=singular,retained_duration=duration,**ch,**result)
def bezout(a,b):
 oldr,r=a,b;olds,s=1,0;oldt,t=0,1
 while r:
  q=oldr//r;oldr,r=r,oldr-q*r;olds,s=s,olds-q*s;oldt,t=t,oldt-q*t
 assert olds*a+oldt*b==oldr
 return oldr,olds,oldt

def v2(n):
 assert n>0
 result=0
 while n%2==0:result+=1;n//=2
 return result

def select(params,S,T,preset=None):
 e,P,K,L,N,b,c,h,H=params;e=Q(e);s,u=map(Q,S);t,v=map(Q,T);A=N*e;R=K*e;z=A-t;C=2*H-h-u;D=2*H-u-v
 assert L>=2 and L&(L-1)==0 and v2(N)<=v2(K) and h%2==0 and c%2 and u.denominator==v.denominator==1 and int(u)%2==int(v)%2==0
 n=C/2;d=D/2;assert n.denominator==d.denominator==1 and 0<n<d;n=int(n);d=int(d);f=d-n
 Lam=lcm(N,K);d2=int(c-v);g=gcd(Lam*d2,L);assert K%g==0
 H0=gcd(n*g,N*f);V=f*(s-A)+n*z
 assert g==2**v2(K) and v2(H0)==min(v2(n)+v2(K),v2(N)+v2(f)) and v2(H0)>=v2(N)
 ell=floor(-V/(2*e*H0)+Q(1,2));hh,x,y=bezout(n*g,N*f);assert hh==H0
 j=x*ell;m=-y*ell;q=N*m+g*j
 raw=(j,m,q);dm=n*g//H0;dj=N*f//H0;dq=N*dm+g*dj;assert dq==N*g*d//H0
 shift=max(0,ceil(Q(-m,dm)),ceil(Q(-q,dq)))
 j+=dj*shift;m+=dm*shift;q+=dq*shift
 if preset is not None:j,m=preset;q=N*m+g*j;shift=None
 assert m>=0 and q>=0
 def slope(q):return (A+z-s+2*e*q)/(2*d)
 tau=slope(q);ch=chart(params,S,T,tau)
 residual=(V+2*e*(n*g*j-N*f*m))/d
 assert abs(residual)<R and ch['indices'][0]==m and ch['residuals'][0]==residual
 if preset is None:assert abs(residual)<=e*H0/d<e*g<=R
 returned=chart(params,S,T,slope(q+dq));assert returned['residuals'][0]==residual
 delta=e*N*g/H0;assert slope(q+dq)-tau==delta and (delta*(h-c)/(2*R)).denominator!=1
 repair=abs(ch['residuals'][1])==R
 if repair:
  j+=dj;m+=dm;q+=dq;tau=slope(q);ch=chart(params,S,T,tau)
 assert abs(ch['residuals'][1])<R and ch['residuals'][0]==residual and ch['indices'][0]==m
 J=q-N*m-K*ch['indices'][1];assert J==g*j-K*ch['indices'][1] and J%g==0 and ch['E']==z+2*e*J
 modulus=L//g;coefficient=Lam*d2//g;assert gcd(coefficient,modulus)==1
 p=0 if modulus==1 else (-J//g*pow(coefficient,-1,modulus))%modulus
 final=tau+2*e*Lam*p;end=chart(params,S,T,final)
 assert end['residuals']==ch['residuals'] and end['E']==ch['E']+2*e*Lam*d2*p
 capinc=Q(C*Lam*p,N);rightinc=Q((h-c)*Lam*p,K);assert capinc.denominator==rightinc.denominator==1
 assert end['indices']==[int(m+capinc),int(ch['indices'][1]+rightinc)] and (J+Lam*d2*p)%L==0
 return dict(valuation_N=v2(N),valuation_K=v2(K),valuation_H0=v2(H0),right_return_ratio=(h-c)*delta/(2*K*e),n=n,d=d,f=f,Lambda=Lam,g=g,H0=H0,ell=ell,raw_bezout=raw,positive_shift=shift,j=j,m=m,q=q,homogeneous_steps=(dj,dm,dq),right_repair=repair,return_slope=delta,J=J,p=p,final_slope=final)
fixtures=[
 ('author-even-N10-active-right-corner',(2,1,2,4,10,2,3,4,12),(2,10),(14,2),(0,0),Q(6)),
 ('own-even-N10-native-mouth',(2,2,2,4,10,2,3,4,12),(2,4),(14,2),None,None),
 ('own-strict-H0-valuation-quarter-period',(2,2,2,4,10,1,3,6,15),(2,8),(14,2),None,None)]
rows=[]
for label,params,S,T,preset,expected in fixtures:
 sel=select(params,S,T,preset)
 if expected is not None:assert sel['final_slope']==expected
 rows.append(dict(selection=sel,**physical(label,params,S,T,sel['final_slope'])))
assert rows[0]['selection']['right_repair'] and rows[0]['selection']['q']==12
assert rows[-1]['selection']['valuation_H0']>rows[-1]['selection']['valuation_N'] and rows[-1]['selection']['right_return_ratio']==Q(15,4)
assert request_hash==hashlib.sha256(REQUEST.read_bytes()).hexdigest()
out=dict(status='PASS_UJ02_EVEN_N_VALUATION_EXTENSIONS_AND_GENUINE_ORIGINAL_WALLS',source_pins_before=before,source_pins_after=pins(),request_sha256=request_hash,rows=rows,cases=len(rows),reflections=sum(r['reflections'] for r in rows),wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_pins_before','source_pins_after']}))
