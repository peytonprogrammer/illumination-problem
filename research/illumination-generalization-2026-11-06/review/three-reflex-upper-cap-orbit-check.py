"""UC01 independent cap-orbit selection and prescribed actual-wall checks."""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd,floor
import ast,json,hashlib
HERE=Path(__file__).parent;REQUEST=HERE.parent/'construction/three-reflex-upper-cap-orbit-review-request.json'
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
 e,P,L,N,b,c,h,H=params;e=Q(e);s,u=map(Q,S);t,v=map(Q,T);a=P*e;A=N*e;B=L*e;C=2*H-h-u;D=2*H-u-v;g1=h-c;d2=c-v;tau=Q(tau)
 X=s+C*tau;m=floor(X/(2*A));z1=X-(2*m+1)*A
 k=floor((z1+g1*tau+e)/(2*e));z2=z1+g1*tau-2*e*k
 return dict(C=C,D=D,indices=[m,k],residuals=[z1,z2],E=z2+d2*tau)
def physical(label,params,S,T,tau,selector_member=True):
 e,P,L,N,b,c,h,H=params;e=Q(e);s,u=map(Q,S);t,v=map(Q,T);tau=Q(tau);A=N*e;a=P*e
 assert 0<b<c<h<u<H and 0<s<A and (N-L)*e<t<A and 0<v<c and N>P+L
 ch=chart(params,S,T,tau);z1,z2=ch['residuals'];assert abs(z1)<e and abs(z2)<e and fold(ch['E'],L*e)==A-t
 f=H-u;roofphase=s+f*tau;singular=(roofphase/A).denominator==1
 if singular:
  assert fold(s+2*f*tau,A)==s
  duration=ch['D']-2*f;assert duration==u-v
  velocity=(-tau,-Q(1));roof_required=False
 else:
  duration=ch['D'];velocity=(tau,Q(1));roof_required=True
 polygon=[(a,b),(a,h),((N-1)*e,h),((N-1)*e,c),((N-L)*e,c),((N-L)*e,0),(A,0),(A,H),(0,H),(0,b)]
 ray=replay(polygon,(s,u),(t,v),tau,duration,velocity,roof_required)
 if not singular:assert ray['roof']['time']==f
 return dict(label=label,parameters=params,S=S,T=T,slope=tau,selector_member=selector_member,formal_roof_phase=roofphase,roof_corner_suffix_used=singular,retained_duration=duration,**ch,**ray)
def select(params,S,T,preset_q=None):
 e,P,L,N,b,c,h,H=params;e=Q(e);s,u=map(Q,S);t,v=map(Q,T);A=N*e;z=A-t;C=2*H-h-u;D=2*H-u-v;n=C/2;d=D/2
 assert N%2 and L>=2 and L&(L-1)==0 and h%2==0 and c%2 and u.denominator==v.denominator==1 and int(u)%2==int(v)%2==0
 assert n.denominator==d.denominator==1 and d>n>=1
 n=int(n);d=int(d);G=gcd(n,N*d);period=N*d//G;spacing=2*e*G/d;assert G<=n<d and spacing<2*e
 tau0=(A+z-s)/(2*d);X0=s+C*tau0
 ell=floor((A-X0)/spacing+Q(1,2));Y=X0+spacing*ell;assert abs(Y-A)<e
 q0=(ell*pow(n//G,-1,period))%period if preset_q is None else preset_q
 def slope(q):return tau0+e*q/d
 ch=chart(params,S,T,slope(q0));assert abs(ch['residuals'][0])<e
 returned=chart(params,S,T,slope(q0+period));assert returned['residuals'][0]==ch['residuals'][0]
 return_delta=e*N/G;right_delta=(h-c)*return_delta;assert (right_delta/(2*e)).denominator!=1
 flip=abs(ch['residuals'][1])==e;q=q0+period if flip else q0;mid=slope(q);ch=chart(params,S,T,mid);assert abs(ch['residuals'][1])<e
 m,k=ch['indices'];J=(ch['E']-z)/(2*e);assert J.denominator==1 and J==q-N*m-k
 coefficient=N*(c-v);assert coefficient.denominator==1 and gcd(int(coefficient),L)==1
 p=(-int(J)*pow(int(coefficient),-1,L))%L
 final=mid+2*e*N*p;end=chart(params,S,T,final)
 assert end['residuals']==ch['residuals'] and end['indices']==[m+C*p,k+(h-c)*N*p]
 assert end['E']==ch['E']+2*e*coefficient*p and (J+coefficient*p)%L==0
 return dict(n=n,d=d,G=G,Q=period,spacing=spacing,nearest_ell=ell,q0=q0,q=q,cap_return_used=flip,cap_return_slope=return_delta,right_return_delta=right_delta,p=p,J=J,final_slope=final)
A=(4,1,4,7,2,3,4,12);B=(2,3,4,9,1,3,4,9);D=(2,2,4,9,1,3,6,15)
rows=[]
for label,params,S,T,preset,expected in [
 ('author-A-near-roof',A,(2,10),(20,2),0,Q(1025,6)),
 ('author-B-active-right-corner',B,(2,6),(14,2),0,Q(20)),
 ('author-C-nontrivial-G',A,(2,6),(20,2),0,Q(1361,8)),
 ('own-nearest-A',A,(2,10),(20,2),None,None),
 ('own-even-P-G-not-dividing-N',D,(2,8),(14,2),None,None)]:
 sel=select(params,S,T,preset)
 if expected is not None:assert sel['final_slope']==expected
 rows.append(dict(selection=sel,**physical(label,params,S,T,sel['final_slope'])))
assert rows[1]['selection']['cap_return_used'] and rows[1]['selection']['q']==45
assert rows[2]['selection']['G']==7
assert rows[4]['selection']['G']==2 and rows[4]['selection']['right_return_delta']==27
rows.append(physical('own-native-conditional-roof-corner',(12,1,4,7,2,3,4,12),(6,6),(38,2),41,False))
assert rows[-1]['roof_corner_suffix_used'] and rows[-1]['reflections']==5
assert request_hash==hashlib.sha256(REQUEST.read_bytes()).hexdigest()
out=dict(status='PASS_UC01_INDEPENDENT_ALL_UPPER_SELECTION_AND_GENUINE_WALL_CONTROLS',source_pins_before=before,source_pins_after=pins(),request_sha256=request_hash,rows=rows,cases=len(rows),reflections=sum(r['reflections'] for r in rows),wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_pins_before','source_pins_after']}))
