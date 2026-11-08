"""LJ03 independently selected exact equal-arm physical witnesses, no search."""
from pathlib import Path
from fractions import Fraction as Q
from math import floor,ceil,gcd,lcm
import ast,json,hashlib
HERE=Path(__file__).parent
REQUEST=HERE.parent/'construction/three-reflex-lower-equal-arm-review-request.json'
def pins():
    rows=[]
    for pin in json.loads(REQUEST.read_text())['source_pins']:
        actual=hashlib.sha256(Path(pin['path']).read_bytes()).hexdigest()
        assert actual==pin['sha256'],pin
        rows.append(dict(pin,actual=actual,passed=True))
    return rows
before=pins(); request_hash=hashlib.sha256(REQUEST.read_bytes()).hexdigest()
ns={'Q':Q,'F':Q};txt=(HERE/'resumed-exact-check.py').read_text()
names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
exec(compile(ast.Module(body=[n for n in ast.parse(txt).body if isinstance(n,ast.FunctionDef)
    and n.name in names],type_ignores=[]),'<own-pure-geometry>','exec'),ns)
txt=(HERE/'three-reflex-coprime-independent-check.py').read_text()
fn=next(n for n in ast.parse(txt).body if isinstance(n,ast.FunctionDef) and n.name=='replay_actual')
rns={'Q':Q,'ns':ns};exec(compile(ast.get_source_segment(txt,fn),'<own-earliest-wall>','exec'),rns)

def check(label,e,P,N,L,b,c,h,H,S,T,expected=None):
    e=Q(e);s,u=map(Q,S);t,v=map(Q,T);a=P*e;A=N*e;R=a;B=L*e;z=A-t
    assert P<L and N>P+L and N%2 and h%2==0 and c%2 and L&(L-1)==0
    assert 0<b<c<h<H and 0<s<a and b<u<h and A-B<t<A and 0<v<c
    al=int((h-u)/2);be=H-h;f=int((h-v)/2);d=al+be+f
    assert Q(h-u,2)==al>0 and Q(h-v,2)==f>0
    # Independent direct elimination, not the author's inverse matrix formula.
    la=-s/(2*a)-Q(al*N,2*P*be)
    mu=z/(2*a)-Q(f*N,2*P*be)
    i=-floor(la+Q(1,2));j=-floor(mu+Q(1,2));m=0
    errors=(la+i,mu+j)
    assert all(-Q(1,2)<=x<Q(1,2) for x in errors)
    q=P*i+N*m+P*j;hh=gcd(gcd(N*al,P*be),N*f)
    di,dm,dj=N*al//hh,P*be//hh,N*f//hh;dq=P*di+N*dm+P*dj
    shift=max(0,ceil(Q(-i,di)),ceil(Q(-m,dm)),ceil(Q(-q,dq)))
    i+=di*shift;m+=dm*shift;j+=dj*shift;q+=dq*shift
    def state():
        tau=(A+z-s+2*e*q)/(2*d)
        x=s+2*al*tau-2*a*i;y=x+2*be*tau-(2*m+1)*A
        assert abs(x)<a and abs(y)<R and tau>0 and min(i,m,q)>=0
        assert floor((s+2*al*tau+a)/(2*a))==i
        assert floor((x+2*be*tau)/(2*A))==m
        k=floor((y+(h-c)*tau+R)/(2*R));w=y+(h-c)*tau-2*R*k
        return tau,x,y,k,w
    tau,x,y,k,w=state();repair=abs(w)==R
    if repair:i+=di;m+=dm;j+=dj;q+=dq;tau,x,y,k,w=state()
    assert abs(w)<R and Q((h-c)*N,2*hh).denominator>1
    J=P*(j-k);Lam=lcm(P,N);Gamma=gcd(Lam*int(c-v),L)
    assert P%Gamma==0 and J%Gamma==0
    mod=L//Gamma;p=0 if mod==1 else (-J//Gamma*pow(Lam*int(c-v)//Gamma,-1,mod))%mod
    final=tau+2*e*Lam*p
    fi=i+2*al*Lam*p//P;fm=m+2*be*Lam*p//N;fk=k+(h-c)*Lam*p//P
    assert s+2*al*final-2*a*fi==x
    assert x+2*be*final-(2*fm+1)*A==y
    assert y+(h-c)*final-2*R*fk==w
    assert ns['fold'](w+(c-v)*final,B)==z
    roof=x+be*final;assert (roof/A).denominator>1
    if expected is not None:assert final==expected
    polygon=[(a,b),(a,h),(A-R,h),(A-R,c),(A-B,c),(A-B,0),(A,0),(A,H),(0,H),(0,b)]
    result=rns['replay_actual'](polygon,(s,u),(t,v),final,2*d)
    return dict(label=label,parameters=[e,P,N,L,b,c,h,H],S=S,T=T,
       coefficients=[la,mu],errors=errors,positive_steps=shift,right_repair=repair,
       Gamma=Gamma,J=J,p=p,final_slope=final,indices=[fi,fm,fk],
       residuals=[x,y,w],roof_phase=roof,**result)

# Author's two fixed controls; an additional identical B geometry with a
# prescribed target t=12 exercises a nonzero final full-target correction.
fixtures=[
 ('simultaneous-half-ties',4,1,9,4,1,3,8,26,(2,6),(34,2),Q(9,11)),
 ('even-P-equal-arm',2,2,9,4,1,3,6,12,(2,4),(14,2),Q(14,9)),
 ('even-P-nonzero-target-correction',2,2,9,4,1,3,6,12,(2,4),(12,2),None)]
rows=[check(*x) for x in fixtures]
assert rows[0]['errors']==(-Q(1,2),-Q(1,2))
assert rows[-1]['p']>0
assert request_hash==hashlib.sha256(REQUEST.read_bytes()).hexdigest()
out=dict(status='PASS_LJ03_HALF_OPEN_EQUAL_ARM_ACTUAL_REPLAY',source_pins_before=before,
 source_pins_after=pins(),request_sha256=request_hash,rows=rows,cases=len(rows),
 reflections=sum(r['reflections'] for r in rows),wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),
 author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_pins_before','source_pins_after']}))
