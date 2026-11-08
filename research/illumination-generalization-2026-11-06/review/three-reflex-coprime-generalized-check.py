"""Independent CE01 finite selector and actual-wall replay on prescribed inputs."""
from fractions import Fraction as Q
from pathlib import Path
from math import gcd,floor,ceil
from itertools import combinations
import ast,hashlib,json

HERE=Path(__file__).parent
AUTHOR=HERE.parent/'construction'
REQUEST=AUTHOR/'three-reflex-coprime-extension-review-request.json'
def capture():
    if REQUEST.exists():
        requested=json.loads(REQUEST.read_text())['source_pins']
    else:
        requested=[dict(path=str(AUTHOR/name),sha256=hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest())
            for name in ['three-reflex-coprime-extension-candidate.md',
                         'three-reflex-coprime-extension-proof.md',
                         'three-reflex-coprime-extension-prescribed-check.py',
                         'three-reflex-coprime-extension-prescribed-check.json']]
    rows=[]
    for item in requested:
        actual=hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()
        assert actual==item['sha256'],item
        rows.append(dict(item,actual=actual,passed=True))
    return rows
before=capture()

ns={'Q':Q,'F':Q}
tree=ast.parse((HERE/'resumed-exact-check.py').read_text())
names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
exec(compile(ast.Module(body=[f for f in tree.body if isinstance(f,ast.FunctionDef)
    and f.name in names],type_ignores=[]),'<reviewer-geometric-predicates>','exec'),ns)
tree=ast.parse((HERE/'three-reflex-coprime-independent-check.py').read_text())
fixed={'Q':Q,'ns':ns}
exec(compile(ast.Module(body=[f for f in tree.body if isinstance(f,ast.FunctionDef)
    and f.name=='replay_actual'],type_ignores=[]),'<reviewer-one-prescribed-ray>','exec'),fixed)

def parameters(a,N,L,b,c,h,H):
    a=Q(a)
    assert a>0 and isinstance(N,int) and isinstance(L,int) and L>=2 and N>=L+2
    assert all(isinstance(x,int) for x in (b,c,h,H)) and 0<b<c<h<H
    assert gcd(2*(H-h),N)==1
    assert N%2==1  # Implied by coprimality with the even G, not an extra hypothesis.
    l,w,A=(N-L)*a,(N-1)*a,N*a
    P=[(a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b)]
    ns['simple'](P)
    return a,l,w,A,P

def construct(label,a,N,L,b,c,h,H,S,T):
    a,l,w,A,P=parameters(a,N,L,b,c,h,H)
    s,u=map(Q,S);t,v=map(Q,T)
    assert 0<s<a and b<u<=h and l<t<A and 0<v<c
    assert u.denominator==v.denominator==1
    d0,G,g1,d2=int(h-u),2*(H-h),h-c,int(c-v)
    assert gcd(N*d2,L)==1
    D=d0+G+g1+d2;z=A-t
    good=[];forbidden=[[] for _ in range(3)]
    for q in range(D):
        tau=(A+z-s+2*a*q)/D
        phase=(s+d0*tau,s+(d0+G)*tau-A,s+(D-d2)*tau-A)
        bad=[((p-a)/(2*a)).denominator==1 for p in phase]
        if not any(bad):good.append(q)
        for i,bad_event in enumerate(bad):
            if bad_event:forbidden[i].append(q)
    assert good
    if d0==G==g1==d2 and forbidden[1]:assert not forbidden[0]
    q=good[-1]
    tau0=(A+z-s+2*a*q)/D
    n0=floor((s+d0*tau0+a)/(2*a));z0=s+d0*tau0-2*n0*a
    X0=z0+G*tau0
    assert (X0/(2*a)).denominator!=1
    M=(pow(G,-1,N)*((N-1)//2-floor(X0/(2*a))))%N
    tau1=tau0+2*a*M
    n=n0+d0*M
    X=z0+G*tau1;m=floor(X/(2*A));z1=X-(2*m+1)*A
    k=floor((z1+g1*tau1+a)/(2*a));z2=z1+g1*tau1-2*k*a
    assert all(abs(z)<a for z in (z0,z1,z2))
    J=(z2+d2*tau1-z)/(2*a);assert J.denominator==1
    # Exact residue solution, not a sweep of candidate final slopes.
    p=(-int(J)*pow(N*d2,-1,L))%L
    tau=tau1+2*a*N*p
    n+=N*d0*p;m+=G*p;k+=N*g1*p
    actual0=s+d0*tau-2*n*a
    actual1=actual0+G*tau-(2*m+1)*A
    actual2=actual1+g1*tau-2*k*a
    assert (actual0,actual1,actual2)==(z0,z1,z2)
    E=z2+d2*tau
    assert ((E-z)/(2*L*a)).denominator==1 and ns['fold'](E,L*a)==z
    result=fixed['replay_actual'](P,(s,u),(t,v),tau,D)
    return dict(label=label,a=a,N=N,L=L,geometry=[a,l,w,A,b,c,h,H],S=S,T=T,
        q=q,cap_M=M,target_shift=p,source_residuals=(z0,z1,z2),slope=tau,
        forbidden=forbidden,equal_blocks=d0==G==g1==d2,**result)

fixtures=[
 ('even-low',4,5,3,1,4,5,6,(2,2),(10,2)),
 ('even-high',4,5,3,1,4,5,6,(2,4),(14,2)),
 ('target-w',4,5,3,1,4,5,6,(2,2),(16,2)),
 ('source-h',4,5,3,1,4,6,7,(2,6),(10,2)),
 ('equal-cap-nonempty',4,5,3,1,4,6,7,(2,4),(10,2)),
 ('equal-cap-empty',4,5,3,1,4,6,7,(2,4),(14,2)),
 ('rational-equal',Q(3,2),7,3,1,4,6,7,(Q(1,7),4),(Q(67,11),2)),
 ('L5-depth2',4,7,5,2,6,10,12,(2,8),(10,4)),
 ('L7-even-four',4,9,7,1,8,11,12,(2,10),(14,4)),
 ('L4-odd',4,7,4,1,7,10,11,(2,8),(14,2)),
 ('L9-composite',4,11,9,1,4,7,8,(2,6),(10,2)),
]
rows=[construct(*f) for f in fixtures]

tree=ast.parse((HERE/'three-reflex-tr01-independent-check.py').read_text())
names={'point','L_vertical','L_horizontal','U_opposite','U_path'}
exec(compile(ast.Module(body=[f for f in tree.body if isinstance(f,ast.FunctionDef)
    and f.name in names],type_ignores=[]),'<reviewer-protected-U-L>','exec'),ns)
a,l,w,A,P=parameters(4,5,3,1,4,5,6);b,c,h,H=1,4,5,6
R=[(l,0),(A,0),(A,H),(w,H),(w,c),(l,c)]
marks=[(Q(x),Q(y)) for x in range(0,int(A)+1,2) for y in range(0,H+1,2)
       if ns['location'](P,(Q(x),Q(y)))==1]
assert set(marks)=={(2,2),(2,4),(10,2),(12,2),(14,2),(16,2),(18,2),(18,4)}
def G(p):return p[0]<a or p[1]>=h or (p[0]>w and p[1]>=c)
whole=[]
for S,T in combinations(marks,2):
    if G(S) and G(T):
        method='protected-U'
        path=ns['U_path'](a,w,A,H-h,H-b,H,(S[0],H-S[1]),(T[0],H-T[1]))
        path=[(x,H-y) for x,y in path]
    elif ns['location'](R,S)==ns['location'](R,T)==1:
        method='protected-L'
        path=ns['L_horizontal'](A-l,A-w,c,H,(A-S[0],S[1]),(A-T[0],T[1]))
        path=[(A-x,y) for x,y in path]
    else:
        method='CE01-terminal';X,Y=(S,T) if S[0]<a else (T,S)
        witness=construct('whole-prescribed',4,5,3,1,4,5,6,X,Y)
        path=witness['path'] if X==S else list(reversed(witness['path']))
    for i,(left,right) in enumerate(zip(path,path[1:])):
        if ns['on'](left,right,T):path=path[:i+1]+[T];break
    assert path[0]==S and path[-1]==T
    whole.append(dict(S=S,T=T,method=method,**ns['path_check'](P,path)))
assert len(whole)==28 and sum(row['method']=='CE01-terminal' for row in whole)==10
Lv=(A-w)/(2*c);dv=Lv/(ceil(Lv*h/(2*a))+ceil(Lv*h/(2*(A-w)))+3)
Lh=(H-h)/(2*a);dh=Lh/(ceil(Lh*w/(2*c))+ceil(Lh*w/(2*(H-h)))+3)
assert c+2*A/dv==404 and a+2*H/dh==484
out=dict(status='PASS_INDEPENDENT_CE01_SELECTOR_ACTUAL_FIRST_HITS',source_pins_before=before,
    source_pins_after=capture(),request_present=REQUEST.exists(),
    terminal_rows=rows,terminal_cases=len(rows),terminal_reflections=sum(r['reflections'] for r in rows),
    terminal_wall_guards=sum(r['wall_leg_guards'] for r in rows),
    whole_native_points=marks,whole_rows=whole,whole_pair_count=len(whole),whole_terminal_pairs=10,
    whole_reflections=sum(r['reflections'] for r in whole),whole_wall_guards=sum(r['wall_leg_guards'] for r in whole),
    old_height_threshold=404,old_width_threshold=484,
    author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['source_pins_before','source_pins_after','terminal_rows','whole_native_points','whole_rows']}))
