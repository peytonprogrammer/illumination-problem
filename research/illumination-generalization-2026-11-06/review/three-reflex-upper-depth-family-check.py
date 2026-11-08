"""UDPA01 independent algebra and prescribed original-wall verification.
Fixed inputs only; no author code execution or discovery effort.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd,floor,ceil
import ast,hashlib,json
HERE=Path(__file__).parent
REQUEST=HERE.parent/'construction/three-reflex-upper-depth-family-review-request.json'
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
def family(N,r):
 assert N>=7 and N%2 and 1<=r<=7
 k=next(k for k in (2,3,4,5) if (k-r-1)%4==0);d=N+5
 q=N*N+4*N+Q(k-r-9,4);assert q.denominator==1
 tau0=4*N-2+Q(k,d);params=(4,1,4,N,2,3,4,N+5);S=(2,6);T=(4*N-2*r,2)
 seed=chart(*params,S,T,tau0)
 wanted=[-2+Q(2*k,d),-2+Q(6*k,d),2*k-6-Q(2*k,d),2*k-4-Q(k,d) if k<=4 else -2-Q(5,d)]
 assert seed['residuals']==wanted
 indicator=int(k==5)
 assert seed['indices']==[1,2*N-1,N,(N-1)//2+indicator]
 J=Q(2*N+k-r-3,4)-indicator;assert J.denominator==1 and seed['E']==2*r+8*J
 assert tau0==Q(4*N+2*r-2+8*q,2*d)
 p=(-int(J)*pow(N,-1,4))%4;final=tau0+8*N*p;ch=chart(*params,S,T,final)
 assert ch['residuals']==wanted and ch['E']==seed['E']+8*N*p and (J+N*p)%4==0
 assert ch['indices']==[1+2*p,2*N-1+4*N*p,N+2*(N+1)*p,(N-1)//2+indicator+N*p]
 floorx=2+Q(4*k,d);assert 2<floorx<4
 ray=physical('N'+str(N)+'-r'+str(r)+'-k'+str(k),params,S,T,final,True)
 assert ray['floor_x']==floorx and not ray['floor_corner_suffix_used']
 return dict(r=r,k=k,q=q,p=p,J=J,**ray)
# The four exact controls were declared before any execution; no parameter sweep.
rows=[family(7,4),family(9,2),family(7,1),family(7,3)]
assert rows[0]['slope']==Q(1661,12)
assert {r['k'] for r in rows}=={2,3,4,5}
assert request_hash==hashlib.sha256(REQUEST.read_bytes()).hexdigest()
out=dict(status='PASS_UDPA01_INDEPENDENT_EXPLICIT_ALL_K_FORMULA_AND_ORIGINAL_WALLS',source_pins_before=before,source_pins_after=pins(),request_sha256=request_hash,rows=rows,cases=len(rows),reflections=sum(r['reflections'] for r in rows),wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_pins_before','source_pins_after']}))
