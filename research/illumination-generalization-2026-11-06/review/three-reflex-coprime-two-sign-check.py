"""CE02 independent prescribed algebra and earliest actual-wall replay; no discovery."""
from fractions import Fraction as Q
from pathlib import Path
from math import gcd,floor
import ast,json,hashlib
HERE=Path(__file__).parent
AUTHOR=HERE.parent/'construction'
REQUEST=AUTHOR/'three-reflex-coprime-extension-two-sign-review-request.json'
def capture():
    pins=json.loads(REQUEST.read_text())['source_pins'] if REQUEST.exists() else [
        {'path':str(AUTHOR/('three-reflex-coprime-extension-two-sign-'+s)),
         'sha256':hashlib.sha256((AUTHOR/('three-reflex-coprime-extension-two-sign-'+s)).read_bytes()).hexdigest()}
        for s in ['candidate.md','proof.md','check.py','check.json']]
    for pin in pins:
        assert hashlib.sha256(Path(pin['path']).read_bytes()).hexdigest()==pin['sha256'],pin
    return pins
before=capture()
ns={'Q':Q,'F':Q}
tree=ast.parse((HERE/'resumed-exact-check.py').read_text());names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
exec(compile(ast.Module(body=[f for f in tree.body if isinstance(f,ast.FunctionDef) and f.name in names],type_ignores=[]),'<reviewer-pure-geometry>','exec'),ns)
replayns={'Q':Q,'ns':ns}
tree=ast.parse((HERE/'three-reflex-coprime-independent-check.py').read_text())
exec(compile(ast.Module(body=[f for f in tree.body if isinstance(f,ast.FunctionDef) and f.name=='replay_actual'],type_ignores=[]),'<reviewer-prescribed-ray>','exec'),replayns)
def ray(label,a,N,L,b,c,h,H,S,T,q_fixed=None):
    a=Q(a);s,u=map(Q,S);t,v=map(Q,T);A=N*a;l=(N-L)*a;w=(N-1)*a
    assert L>=2 and N>=L+2 and a>0 and 0<b<c<h<H
    assert all(isinstance(i,int) for i in (N,L,b,c,h,H))
    assert 0<s<a and b<u<=h and l<t<A and 0<v<c and u.denominator==v.denominator==1
    d0,G,g1,d2=int(h-u),2*(H-h),h-c,int(c-v);D=d0+G+g1+d2;z=A-t;r=z/a
    assert gcd(G,N)==1 and gcd(N*d2,L)==2 and r.denominator==1 and int(r)%2==1
    good=[]
    for q in range(D):
        tau=(A+z-s+2*a*q)/D
        if all(((p-a)/(2*a)).denominator!=1 for p in (s+d0*tau,s+(d0+G)*tau-A,s+(D-d2)*tau-A)):good.append(q)
    q=good[-1] if q_fixed is None else q_fixed
    assert q in good
    tau=(A+z-s+2*a*q)/D;n=floor((s+d0*tau+a)/(2*a));z0=s+d0*tau-2*a*n
    X=z0+G*tau;M=(pow(G,-1,N)*((N-1)//2-floor(X/(2*a))))%N
    tau+=2*a*M;n+=d0*M
    X=z0+G*tau;m=floor(X/(2*A));z1=X-(2*m+1)*A
    k=floor((z1+g1*tau+a)/(2*a));z2=z1+g1*tau-2*a*k
    assert all(abs(p)<a for p in (z0,z1,z2))
    J=(z2+d2*tau-z)/(2*a);assert J.denominator==1;J=int(J)
    # Solve the compatible one of the two exact target-image equations.
    sign=1 if J%2==0 else -1
    rhs=(sign-1)*r/2-J
    assert rhs.denominator==1 and int(rhs)%2==0
    modulus=L//2
    p=0 if modulus==1 else (int(rhs)//2*pow(N*d2//2,-1,modulus))%modulus
    initialJ=J;tau+=2*a*N*p;n+=N*d0*p;m+=G*p;k+=N*g1*p
    z0new=s+d0*tau-2*a*n;z1new=z0new+G*tau-(2*m+1)*A;z2new=z1new+g1*tau-2*a*k
    assert (z0new,z1new,z2new)==(z0,z1,z2)
    E=z2+d2*tau
    assert ((E-sign*z)/(2*L*a)).denominator==1 and ns['fold'](E,L*a)==z
    P=[(a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b)]
    result=replayns['replay_actual'](P,(s,u),(t,v),tau,D)
    if label=='prescribed-negative-image':assert tau==29 and initialJ==7 and sign==-1
    return dict(label=label,source=S,target=T,q=q,slope=tau,D=D,initial_J=initialJ,target_sign=sign,target_shift=p,**result)
fixtures=[
 ('prescribed-negative-image',4,5,2,1,4,5,6,(2,4),(16,2),1),
 ('positive-image',4,5,2,1,4,5,6,(2,2),(16,2)),
 ('equal-four-heights',4,5,2,1,4,6,7,(2,4),(16,2)),
 ('source-on-h',4,5,2,1,4,6,7,(2,6),(16,2)),
 ('L4-off-center-r3',4,7,4,1,4,5,6,(2,2),(16,2)),
 ('L4-off-center-r1',4,7,4,1,4,5,6,(2,4),(24,2)),
 ('L6-r5',4,11,6,1,4,7,8,(2,6),(24,2)),
 ('L10-r3',4,13,10,1,4,7,8,(2,4),(40,2)),
 ('rational-horizontal',Q(3,2),5,2,1,4,6,7,(Q(1,7),4),(6,2)),
 ('d2-four',4,11,6,1,6,9,10,(2,8),(24,2)),
 ('d2-six',4,7,4,1,8,10,11,(2,6),(16,2))]
rows=[ray(*f) for f in fixtures]
tree=ast.parse((HERE/'three-reflex-tr01-independent-check.py').read_text());names={'point','L_vertical','L_horizontal','U_opposite','U_path'}
exec(compile(ast.Module(body=[f for f in tree.body if isinstance(f,ast.FunctionDef) and f.name in names],type_ignores=[]),'<reviewer-protected-formulas>','exec'),ns)
P=[(4,1),(4,5),(16,5),(16,4),(12,4),(12,0),(20,0),(20,6),(0,6),(0,1)]
marks=[(x,y) for x in range(0,21,2) for y in range(0,7,2) if ns['location'](P,(x,y))==1]
assert set(marks)=={(2,2),(2,4),(14,2),(16,2),(18,2),(18,4)}
column=[];T=(Q(16),Q(2))
for S in marks:
    if S==T:continue
    if S[0]<4:
        result=ray('column-terminal',4,5,2,1,4,5,6,S,T);method='CE02'
    else:
        path=ns['L_horizontal'](Q(8),Q(4),Q(4),Q(6),(20-Q(S[0]),Q(S[1])),(20-T[0],T[1]))
        path=[(20-x,y) for x,y in path]
        for i,(x,y) in enumerate(zip(path,path[1:])):
            if ns['on'](x,y,T):path=path[:i+1]+[T];break
        result=ns['path_check'](P,path);method='protected-L'
    column.append(dict(result,source=S,method=method))
out=dict(status='PASS_INDEPENDENT_CE02_EXACT_TARGET_SIGNS_AND_FIRST_HITS',source_pins_before=before,source_pins_after=capture(),request_present=REQUEST.exists(),rows=rows,column=column,terminal_cases=len(rows),terminal_reflections=sum(x['reflections'] for x in rows),terminal_wall_guards=sum(x['wall_leg_guards'] for x in rows),negative_images=sum(x['target_sign']==-1 for x in rows),column_sources=len(column),column_reflections=sum(x['reflections'] for x in column),column_wall_guards=sum(x['wall_leg_guards'] for x in column),author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('source_pins_before','source_pins_after','rows','column')}))
