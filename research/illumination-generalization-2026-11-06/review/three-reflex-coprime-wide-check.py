"""Independent prescribed CE03 selector and original-wall replay. No discovery."""
from fractions import Fraction as Q
from pathlib import Path
from math import gcd,floor
from itertools import combinations
import ast,json,hashlib
HERE=Path(__file__).parent;AUTHOR=HERE.parent/'construction';REQUEST=AUTHOR/'three-reflex-coprime-extension-wide-review-request.json'
def capture():
    files=['candidate.md','proof.md']
    pins=json.loads(REQUEST.read_text())['source_pins'] if REQUEST.exists() else [{'path':str(AUTHOR/('three-reflex-coprime-extension-wide-'+f)),'sha256':hashlib.sha256((AUTHOR/('three-reflex-coprime-extension-wide-'+f)).read_bytes()).hexdigest()} for f in files]
    for p in pins:assert hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'],p
    return pins
before=capture()
ns={'Q':Q,'F':Q};tree=ast.parse((HERE/'resumed-exact-check.py').read_text());names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
exec(compile(ast.Module(body=[f for f in tree.body if isinstance(f,ast.FunctionDef) and f.name in names],type_ignores=[]),'<reviewer-geometry>','exec'),ns)
text=(HERE/'three-reflex-coprime-independent-check.py').read_text();tree=ast.parse(text)
f=next(f for f in tree.body if isinstance(f,ast.FunctionDef) and f.name=='replay_actual')
source=ast.get_source_segment(text,f).replace('def replay_actual(P,S,T,slope,D):','def replay_actual(P,S,T,slope,D,initial_velocity=None,expected_roofs=1):').replace('velocity=(slope,Q(1))','velocity=initial_velocity or (slope,Q(1))').replace('len(roofs)==len(horizontal)==1','len(roofs)==len(horizontal)==expected_roofs').replace('roof=roofs[0]','roof=roofs[0] if roofs else None')
rns={'Q':Q,'ns':ns};exec(compile(source,'<reviewer-prescribed-ray-with-suffix>','exec'),rns)
def geometry(a,N,K,L,b,c,h,H):
    a=Q(a);A=N*a;w=(N-K)*a;l=(N-L)*a
    assert a>0 and 1<=K<L and N>=L+2 and 0<b<c<h<H
    P=[(a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b)]
    ns['simple'](P);return a,l,w,A,P

def ray(label,a,N,K,L,b,c,h,H,S,T,forced_q=None):
    a,l,w,A,P=geometry(a,N,K,L,b,c,h,H);s,u=map(Q,S);t,v=map(Q,T)
    assert 0<s<a and b<u<H and l<t<A and 0<v<c and u.denominator==v.denominator==1
    d0=max(int(h-u),0);C=2*(H-h) if u<=h else int(2*H-h-u);g1=h-c;d2=int(c-v);D=d0+C+g1+d2;z=A-t
    delta=gcd(C,N);assert gcd(N*K*d2,L)==1 and (delta==1 if K==1 else delta<K)
    good=[]
    for q in range(D):
        tau=(A+z-s+2*a*q)/D
        if K>1:phases=[(s+(D-d2)*tau-A,K*a)]+([(s+d0*tau,a)] if u<h else [])
        elif u>h:phases=[(s+C*tau-A,a),(s+(C+g1)*tau-A,a)]
        else:phases=[(s+d0*tau,a),(s+(d0+C)*tau-A,a),(s+(D-d2)*tau-A,a)]
        if all(((x-end)/(2*a)).denominator!=1 for x,end in phases):good.append(q)
    assert good;q=good[-1] if forced_q is None else forced_q;assert q in good
    tau=(A+z-s+2*a*q)/D
    n=floor((s+d0*tau+a)/(2*a)) if u<=h else 0
    z0=s+d0*tau-2*n*a;X0=z0+C*tau
    if K>1:
        value=(A-X0)/(2*a*delta);nearest=floor(value)+(value-floor(value)>Q(1,2))
        M=(pow(C//delta,-1,N//delta)*nearest)%(N//delta)
    else:
        # Window cell convention works for even N also.
        offset=(X0-A+a)%(2*a);assert 0<offset<2*a
        desired=A-a+offset;shift=(desired-X0)/(2*a);assert shift.denominator==1
        M=int(shift)*pow(C,-1,N)%N
    tau+=2*a*M;n+=d0*M;X=z0+C*tau;m=floor(X/(2*A));z1=X-(2*m+1)*A
    k=floor((z1+g1*tau+K*a)/(2*K*a));z2=z1+g1*tau-2*k*K*a
    assert abs(z0)<a and abs(z1)<K*a and abs(z2)<K*a
    J=(z2+d2*tau-z)/(2*a);assert J.denominator==1
    p=(-int(J)*pow(N*K*d2,-1,L))%L
    tau+=2*a*N*K*p;n+=N*K*d0*p;m+=K*C*p;k+=N*g1*p
    assert s+d0*tau-2*n*a==z0 and z0+C*tau-(2*m+1)*A==z1 and z1+g1*tau-2*k*K*a==z2
    assert ns['fold'](z2+d2*tau,L*a)==z
    singular=u>h and ((s+(H-u)*tau)/A).denominator==1
    if singular:
        eta=2*H-u;assert H<eta<2*H-h and ns['fold'](s+2*(H-u)*tau,A)==s
        duration=u-v;velocity=(-tau,Q(-1));roofs=0
    else:duration=D;velocity=(tau,Q(1));roofs=1
    result=rns['replay_actual'](P,(s,u),(t,v),tau,duration,velocity,roofs)
    if label=='declared-singular-suffix':assert q==4 and M==1 and tau==18 and singular
    return dict(label=label,source=S,target=T,q=q,cap_M=M,target_shift=p,cap_gcd=delta,slope=tau,singular_prefix_discarded=singular,**result)

fixtures=[
 ('declared-singular-suffix',4,5,2,3,1,4,5,7,(2,6),(10,2),4),
 ('noncoprime-cap-gcd3',4,9,4,5,1,4,8,11,(2,6),(18,2)),
 ('source-at-h',4,5,2,3,1,4,6,8,(2,6),(10,2)),
 ('K1-upper-cap',4,11,1,4,1,5,8,11,(2,10),(30,2)),
 ('K1-even-N-upper-cap',4,8,1,5,1,4,5,7,(2,6),(14,2)),
 ('rational-marks',Q(3,2),7,2,3,1,4,6,8,(Q(1,7),7),(Q(67,11),2))]
rows=[ray(*f) for f in fixtures]
tree=ast.parse((HERE/'three-reflex-tr01-independent-check.py').read_text());names={'point','L_vertical','L_horizontal','U_opposite','U_path'}
exec(compile(ast.Module(body=[f for f in tree.body if isinstance(f,ast.FunctionDef) and f.name in names],type_ignores=[]),'<reviewer-protected-U-L>','exec'),ns)
a,l,w,A,P=geometry(4,5,2,3,1,4,5,7);b,c,h,H=1,4,5,7
right=[(l,0),(A,0),(A,H),(w,H),(w,c),(l,c)]
marks=[(Q(x),Q(y)) for x in range(0,int(A)+1,2) for y in range(0,H+1,2) if ns['location'](P,(Q(x),Q(y)))==1]
assert len(marks)==19
def G(p):return p[0]<a or p[1]>=h or (p[0]>w and p[1]>=c)
whole=[]
for S,T in combinations(marks,2):
    if G(S) and G(T):
        method='TR01-U';path=[(x,H-y) for x,y in ns['U_path'](a,w,A,H-h,H-b,H,(S[0],H-S[1]),(T[0],H-T[1]))]
    elif ns['location'](right,S)==ns['location'](right,T)==1:
        method='TR01-L';path=[(A-x,y) for x,y in ns['L_horizontal'](A-l,A-w,c,H,(A-S[0],S[1]),(A-T[0],T[1]))]
    else:
        X,Y=(S,T) if S[0]<a or S[1]>h else (T,S)
        assert l<Y[0]<A and 0<Y[1]<c
        if X[0]<a:
            method='CE03';result=ray('whole-terminal',4,5,2,3,b,c,h,H,X,Y);path=result['path']
        else:
            method='TR05';assert a<=X[0]<=w and h<X[1]<H
            path=[(A-yp,H-xp) for xp,yp in ns['U_path'](H-h,H-c,H,A-w,A,A-l,(H-X[1],A-X[0]),(H-Y[1],A-Y[0]))]
        if X!=S:path=list(reversed(path))
    for i,(left,last) in enumerate(zip(path,path[1:])):
        if ns['on'](left,last,T):path=path[:i+1]+[T];break
    assert path[0]==S and path[-1]==T
    whole.append(dict(S=S,T=T,method=method,**ns['path_check'](P,path)))
assert len(whole)==171 and sum(x['method']=='CE03' for x in whole)==15 and sum(x['method']=='TR05' for x in whole)==25
out=dict(status='PASS_INDEPENDENT_CE03_ORIGINAL_WALLS_AND_SOURCE_SUFFIX',source_pins_before=before,source_pins_after=capture(),request_present=REQUEST.exists(),rows=rows,whole_rows=whole,terminal_cases=len(rows),terminal_reflections=sum(x['reflections'] for x in rows),terminal_wall_guards=sum(x['wall_leg_guards'] for x in rows),singular_suffix_controls=sum(x['singular_prefix_discarded'] for x in rows),native_marks=marks,whole_pair_count=171,whole_terminal_pairs=15,whole_TR05_pairs=25,whole_reflections=sum(x['reflections'] for x in whole),whole_wall_guards=sum(x['wall_leg_guards'] for x in whole),author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_pins_before','source_pins_after','rows','whole_rows','native_marks')}))
