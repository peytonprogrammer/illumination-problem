"""LJ04 independent exact nulltransport and original-wall replay, no search."""
from pathlib import Path
from fractions import Fraction as Q
from math import floor,ceil,gcd,lcm
import ast,json,hashlib
HERE=Path(__file__).parent
REQ=HERE.parent/'construction/three-reflex-lower-small-source-review-request.json'
def pins():
 rows=[]
 for p in json.loads(REQ.read_text())['source_pins']:
  actual=hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()
  assert actual==p['sha256'];rows.append(dict(p,actual=actual,passed=True))
 return rows
before=pins();request_hash=hashlib.sha256(REQ.read_bytes()).hexdigest()
ns={'Q':Q,'F':Q};text=(HERE/'resumed-exact-check.py').read_text()
names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
exec(compile(ast.Module(body=[n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)
 and n.name in names],type_ignores=[]),'<own-pure-geometry>','exec'),ns)
text=(HERE/'three-reflex-coprime-independent-check.py').read_text()
fn=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name=='replay_actual')
rns={'Q':Q,'ns':ns};exec(compile(ast.get_source_segment(text,fn),'<own-earliest-original-wall>','exec'),rns)
e=Q(4);N=9;K=2;L=4;b=1;c=3;h=8;H=14;S=(Q(2),Q(6));T=(Q(24),Q(2))
s,u=S;t,v=T;A=N*e;R=K*e;B=L*e;z=A-t
assert 0<e<A-B<A-R<A and 0<b<c<h<H and 0<s<e and b<u<h and A-B<t<A and 0<v<c
alpha=int((h-u)/2);beta=H-h;f=int((h-v)/2);d=alpha+beta+f
assert f%2 and N%2 and (h-c)%2 and int(c-v)%2
la=-s/(2*e)-Q(alpha*N,2*beta);mu=z/(2*e)-Q(f*N,2*beta)
i=-floor(la+Q(1,2));j=-floor(mu+Q(1,2));m=0;q=i+N*m+j
M=gcd(gcd(N*alpha,beta),N*f);di,dm,dj=N*alpha//M,beta//M,N*f//M;dq=di+N*dm+dj
assert M%2 and dj%2 and dq==N*d//M
positive=max(0,ceil(Q(-i,di)),ceil(Q(-m,dm)),ceil(Q(-q,dq)))
i+=di*positive;m+=dm*positive;j+=dj*positive;q+=dq*positive
Lam=lcm(N,K);Gamma=gcd(Lam*int(c-v),L);assert K%Gamma==0 and j%Gamma!=0
ell=(-j*pow(dj,-1,Gamma))%Gamma
i+=di*ell;m+=dm*ell;j+=dj*ell;q+=dq*ell
assert j%Gamma==0
tau=(A+z-s+2*e*q)/(2*d)
x=s+2*alpha*tau-2*e*i;y=x+2*beta*tau-(2*m+1)*A
assert abs(x)<e and abs(y)<e<=R and min(i,m,q)>=0 and tau>0
k=floor((y+(h-c)*tau+R)/(2*R));w=y+(h-c)*tau-2*R*k
block_ratio=Q((h-c)*N,2*(K//Gamma)*M);assert block_ratio.denominator>1
if abs(w)==R:
 i+=di*Gamma;m+=dm*Gamma;j+=dj*Gamma;q+=dq*Gamma
 tau=(A+z-s+2*e*q)/(2*d)
 assert s+2*alpha*tau-2*e*i==x and x+2*beta*tau-(2*m+1)*A==y
 k=floor((y+(h-c)*tau+R)/(2*R));w=y+(h-c)*tau-2*R*k
assert abs(w)<R
J=j-K*k;assert J%Gamma==0
mod=L//Gamma;p=0 if mod==1 else (-J//Gamma*pow(Lam*int(c-v)//Gamma,-1,mod))%mod
final=tau+2*e*Lam*p
assert ns['fold'](w+(c-v)*final,B)==z
assert (final,x,y,w,i,m,k,j,q)==(Q(151,10),Q(1,5),Q(7,5),-Q(31,10),4,2,5,10,32)
assert ell==1 and p==0
polygon=[(e,b),(e,h),(A-R,h),(A-R,c),(A-B,c),(A-B,0),(A,0),(A,H),(0,H),(0,b)]
replay=rns['replay_actual'](polygon,S,T,final,2*d)
out=dict(status='PASS_LJ04_INDEPENDENT_NULLTRANSPORT_ACTUAL_RAY',source_pins_before=before,
 source_pins_after=pins(),request_sha256=request_hash,coefficients=[la,mu],M=M,
 Gamma=Gamma,null_indices=[di,dm,dj],target_null_steps=ell,block_return_ratio=block_ratio,
 final_slope=final,residuals=[x,y,w],indices=[i,m,k],j=j,J=J,**replay,
 author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['source_pins_before','source_pins_after','path','events']},default=str))
