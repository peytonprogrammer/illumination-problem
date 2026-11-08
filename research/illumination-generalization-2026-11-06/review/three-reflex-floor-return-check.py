"""Independent FR01 selector and six prescribed actual-wall controls."""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd,floor
import ast,hashlib,json
HERE=Path(__file__).parent;AUTHOR=HERE.parent/'construction';REQUEST=AUTHOR/'three-reflex-floor-return-review-request.json'
def pins():
 items=json.loads(REQUEST.read_text())['source_pins']
 for p in items:assert hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'],p
 return items
before=pins();request_hash=hashlib.sha256(REQUEST.read_bytes()).hexdigest()
helpers={'__file__':str(HERE/'three-reflex-coprime-wide-check.py'),'__name__':'own_floor_geometry'}
exec(compile((HERE/'three-reflex-coprime-wide-check.py').read_text().split('\ndef geometry(')[0],'<own-existing-predicates>','exec'),helpers)
ns=helpers['ns'];fold=ns['fold']
txt=(HERE/'three-reflex-coprime-independent-check.py').read_text();tree=ast.parse(txt);f=next(f for f in tree.body if isinstance(f,ast.FunctionDef) and f.name=='replay_actual')
code=ast.get_source_segment(txt,f).replace('def replay_actual(P,S,T,slope,D):','def replay_actual(P,S,T,slope,D,initial_velocity,expected_floor=None):').replace('velocity=(slope,Q(1))','velocity=initial_velocity')
code=code.replace('assert len(roofs)==len(horizontal)==1',"assert len(roofs)==1\n    if expected_floor is None:assert len(horizontal)==1\n    else:\n        floors=[e for e in horizontal if e['point'][1]==expected_floor]\n        assert len(horizontal)==2 and len(floors)==1\n        assert floors[0]['time']==S[1]-expected_floor")
rns={'Q':Q,'ns':ns};exec(compile(code,'<own-earliest-wall-with-prescribed-floor-itinerary>','exec'),rns);replay=rns['replay_actual']
def physical(label,e,P,K,L,N,b,c,h,H,S,T,tau):
 e=Q(e);tau=Q(tau);s,u=map(Q,S);t,v=map(Q,T);a=P*e;A=N*e;R=K*e;B=L*e
 assert 0<b<c<h<H and 0<s<a and b<u<=h and A-B<t<A and 0<v<c
 d=h+u-2*b;C=2*(H-h);g1=h-c;d2=c-v;D=d+C+g1+d2;f=u-b
 n=floor((s+d*tau+a)/(2*a));z0=s+d*tau-2*a*n;X=z0+C*tau;m=floor(X/(2*A));z1=X-(2*m+1)*A;k=floor((z1+g1*tau+R)/(2*R));z2=z1+g1*tau-2*R*k;E=z2+d2*tau
 assert abs(z0)<a and abs(z1)<R and abs(z2)<R and fold(E,B)==A-t
 assert ((z0+(H-h)*tau)/A).denominator!=1
 floorx=fold(s+f*tau,a);singular=floorx in (0,a)
 if singular:
  assert fold(s+2*f*tau,a)==s and 2*f<=d
  duration=D-2*f;velocity=(-tau,Q(1));expected_floor=None
 else:
  assert 0<floorx<a;duration=D;velocity=(tau,-Q(1));expected_floor=Q(b)
 polygon=[(a,b),(a,h),(A-R,h),(A-R,c),(A-B,c),(A-B,0),(A,0),(A,H),(0,H),(0,b)]
 result=replay(polygon,(s,u),(t,v),tau,duration,velocity,expected_floor)
 assert result['roof']['time']==(H-u if singular else d+H-h)
 return dict(label=label,parameters=(e,P,K,L,N,b,c,h,H),source=S,target=T,slope=tau,residuals=(z0,z1,z2),final_E=E,floor_x=floorx,floor_corner_suffix_used=singular,formal_duration=D,retained_duration=duration,**result)
def family(label,e,P,L,N,b,c,h,H,S,T,q):
 e=Q(e);s,u=map(Q,S);t,v=map(Q,T);a=P*e;A=N*e;z=A-t;d=h+u-2*b;C=2*(H-h);g1=h-c;d2=c-v;D=d+C+g1+d2
 assert e.denominator==1 and N>P+L and N%2 and L>1 and L&(L-1)==0 and h%2==0 and c%2 and H==h+1 and d==2*P and D%2==0
 assert all(x.denominator==1 and int(x)%2==0 for x in (s,u,t,v))
 good=[]
 assert D.denominator==1
 for index in range(int(D)):
  tau=(A+z-s+2*e*index)/D
  if ((s+d*tau-a)/(2*a)).denominator!=1 and ((s+(d+C)*tau-(N+1)*e)/(2*e)).denominator!=1:good.append(index)
 assert good and q in good
 tau0=(A+z-s+2*e*q)/D;n=floor((s+d*tau0+a)/(2*a));z0=s+d*tau0-2*a*n;X0=z0+2*tau0
 offset=(X0-(A-e))%(2*e);assert 0<offset<2*e
 desired=A-e+offset;shift=(desired-X0)/(2*e);assert shift.denominator==1
 M0=int(shift)%N
 def residual(M):
  tau=tau0+e*M;X=z0+2*tau;m=floor(X/(2*A));z1=X-(2*m+1)*A;Y=z1+g1*tau;k=floor((Y+e)/(2*e));z2=Y-2*e*k
  assert abs(z1)<e
  return tau,m,z1,k,z2
 trial=residual(M0);failed=abs(trial[4])==e
 M=M0+N if failed else M0;tau,m,z1,k,z2=residual(M);assert abs(z2)<e
 n+=M;J=(z2+d2*tau-z)/(2*e);assert J.denominator==1
 assert gcd(N*int(d2),L)==1;p=(-int(J)*pow(N*int(d2),-1,L))%L
 final=tau+2*e*N*p
 assert s+d*final-2*a*(n+2*N*p)==z0 and z0+2*final-(2*(m+2*p)+1)*A==z1 and z1+g1*final-2*e*(k+N*g1*p)==z2
 result=physical(label,e,P,1,L,N,b,c,h,H,S,T,final)
 return dict(q=q,cap_M0=M0,cap_M=M,N_flip_used=failed,target_shift=p,initial_target_J=int(J),**result)
rows=[
 family('author-A-native-mouth',4,3,4,9,1,3,4,5,(8,4),(28,2),0),
 family('author-B-native-lower',4,3,4,9,1,3,6,7,(8,2),(28,2),1),
 family('author-C-mandatory-N-flip',2,2,4,7,1,3,4,5,(2,2),(10,2),0),
 physical('author-D-conditional-corner-suffix',4,3,1,4,9,1,3,4,5,(8,4),(Q(88,3),2),Q(172,3)),
 physical('own-native-conditional-corner-suffix',4,3,1,4,9,1,3,4,5,(6,4),(26,2),22),
 physical('accepted-K1R01-ordinary-floor-repair',4,3,1,3,8,1,3,4,5,(8,4),(24,2),Q(76,5))]
assert [r['slope'] for r in rows[:3]]==[Q(1158,5),Q(695,3),20]
assert rows[2]['N_flip_used'] and rows[2]['cap_M0']==2 and rows[2]['cap_M']==9
assert rows[3]['floor_corner_suffix_used'] and rows[4]['floor_corner_suffix_used'] and not rows[5]['floor_corner_suffix_used']
assert request_hash==hashlib.sha256(REQUEST.read_bytes()).hexdigest()
out=dict(status='PASS_INDEPENDENT_FR01_NATIVE_SELECTION_AND_SINGULAR_FLOOR_SUFFIX',source_pins_before=before,source_pins_after=pins(),request_sha256=request_hash,rows=rows,cases=len(rows),reflections=sum(r['reflections'] for r in rows),wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_pins_before','source_pins_after']}))
