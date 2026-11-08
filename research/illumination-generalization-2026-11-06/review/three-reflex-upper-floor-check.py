"""UP01 independent algebra and prescribed original-wall verification.
Fixed inputs only; no author code execution or discovery effort.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd,floor,ceil
import ast,hashlib,json
HERE=Path(__file__).parent
REQUEST=HERE.parent/'construction/three-reflex-upper-floor-review-request.json'
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
def select(params,S,T,q_override=None):
 e,P,L,N,b,c,h,H=params;e=Q(e);s,u=map(Q,S);t,v=map(Q,T);a=P*e;A=N*e;z=A-t
 dp=u-h;dl=2*(h-b);C=2*(H-h);g1=h-c;d2=c-v;D=dp+dl+C+g1+d2;a0=P//gcd(P,h-b)
 assert P>=5 and P%2 and N%2 and N>P+L and L>=2 and L&(L-1)==0 and e.denominator==1
 assert h%2==0 and c%2 and gcd(P*(H-h),N)==1 and dp>0 and dp%(2*N)==0 and u<H
 assert all(x.denominator==1 and int(x)%2==0 for x in (s,u,t,v))
 base=(A+z-s)/D;delta=2*e*dp/D;Y0=s+dp*base
 ip=floor((Y0+4*delta-a)/(2*A))+1;U=2*A*ip+a;star=ceil((U-Y0)/delta)
 assert U>Y0+4*delta and star>4 and Y0+(star-1)*delta<U<=Y0+star*delta
 candidates=[]
 for q in range(star-4,star):
  tau=base+2*e*q/D;ch=chart(e,P,L,N,b,c,h,H,S,T,tau)
  assert ch['indices'][0]==ip and abs(ch['residuals'][0])<a
  left_bad=abs(ch['residuals'][1])==a
  cap_bad=(s+(dp+dl+C)*tau-(N+1)*e)%(2*e)==0
  candidates.append(dict(q=q,left_bad=left_bad,cap_bad=cap_bad))
 assert sum(x['left_bad'] for x in candidates)<=1 and sum(x['cap_bad'] for x in candidates)<=2
 good=[x['q'] for x in candidates if not x['left_bad'] and not x['cap_bad']]
 assert good
 q=good[0] if q_override is None else q_override;assert q in good
 tau0=base+2*e*q/D;ch0=chart(e,P,L,N,b,c,h,H,S,T,tau0);zp,z0=ch0['residuals'][:2];X=z0+C*tau0
 # Direct modular inverse: target the unique open representative of this 2e coset.
 residue=(X-(A-e))%(2*e);assert 0<residue<2*e
 target=A-e+residue;units=(target-X)/(2*e);assert units.denominator==1
 M0=(int(units)*pow((H-h)*a0,-1,N))%N
 tau=tau0+e*a0*M0;ch=chart(e,P,L,N,b,c,h,H,S,T,tau)
 assert ch['residuals'][:2]==[zp,z0] and abs(ch['residuals'][2])<e
 flip=abs(ch['residuals'][3])==e;M=M0+N if flip else M0
 tau=tau0+e*a0*M;ch=chart(e,P,L,N,b,c,h,H,S,T,tau)
 assert abs(ch['residuals'][3])<e
 J=(ch['E']-z)/(2*e);assert J.denominator==1
 ip,il,im,ik=ch['indices'];assert J==q+D*a0*M/2-N*ip-P*il-N*im-ik
 coefficient=a0*N*int(d2);assert gcd(coefficient,L)==1
 p=(-int(J)*pow(coefficient,-1,L))%L
 final=tau+2*e*a0*N*p;chf=chart(e,P,L,N,b,c,h,H,S,T,final)
 assert chf['residuals']==ch['residuals']
 increments=[dp*a0*p,Q(2*(h-b)*a0*N*p,P),2*(H-h)*a0*p,g1*a0*N*p]
 assert all(Q(x).denominator==1 for x in increments)
 assert chf['indices']==[int(x+y) for x,y in zip(ch['indices'],increments)]
 assert chf['E']==ch['E']+2*e*coefficient*p and (J+coefficient*p)%L==0
 return dict(q=q,qstar=star,npre_seed=ch0['indices'][0],four_candidates=candidates,a0=a0,M0=M0,M=M,N_flip_used=flip,p=p,J=J,final_slope=final)
A=(2,5,4,11,1,3,4,27);B=(2,5,4,11,1,5,6,29)
rows=[]
for label,params,S,T,q,expected in [
 ('author-A',A,(4,26),(18,2),37,Q(20225,38)),
 ('author-B',B,(4,28),(18,2),41,Q(5751,41)),
 ('own-seed-A',A,(4,26),(18,2),None,None),
 ('own-seed-B',B,(4,28),(18,2),None,None)]:
 sel=select(params,S,T,q)
 if expected is not None:assert sel['final_slope']==expected
 rows.append(dict(selection=sel,**physical(label,params,S,T,sel['final_slope'],True)))
# Prescribed CONDITIONAL upper-floor singular fixture, not a UP01 arithmetic member.
# Exact phase computation fixed before replay: zp48,z0-48,z1=16,z2=0,E176.
rows.append(physical('own-upper-corner-suffix',(32,3,4,9,8,24,32,40),(4,34),(208,16),22,False))
assert rows[-1]['residuals']==[48,-48,16,0] and rows[-1]['E']==176 and rows[-1]['floor_corner_suffix_used']
assert rows[0]['indices']==[266,160,556,133] and rows[1]['indices']==[70,71,146,35]
assert request_hash==hashlib.sha256(REQUEST.read_bytes()).hexdigest()
out=dict(status='PASS_UP01_INDEPENDENT_ARITHMETIC_AND_ACTUAL_WALL_REPLAY',source_pins_before=before,source_pins_after=pins(),request_sha256=request_hash,rows=rows,cases=len(rows),reflections=sum(r['reflections'] for r in rows),wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_pins_before','source_pins_after']}))
