"""Independent congruence selector and prescribed actual first-hit replay.

No author code execution, direction discovery, room census, or old clock reuse.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import gcd, floor, ceil
from itertools import combinations
import ast,hashlib,json

HERE=Path(__file__).parent
REQUEST=Path('.context/codex-proof-verification/specialist-ideas/terminal-resumption-2026-11-07/review-request.json')
request=json.loads(REQUEST.read_text())
def pin_check():
    rows=[]
    for item in request['source_pins']:
        actual=hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()
        assert actual==item['sha256'],item
        rows.append(dict(item,actual=actual,passed=True))
    return rows
before=pin_check()
old=ast.parse((HERE/'resumed-exact-check.py').read_text())
names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
ns={'Q':Q,'F':Q}
exec(compile(ast.Module(body=[f for f in old.body if isinstance(f,ast.FunctionDef)
    and f.name in names],type_ignores=[]),'<reviewer-pure-geometry>','exec'),ns)

def choose(a,N,b,c,h,H,S,T):
    a=Q(a);s,u=map(Q,S);t,v=map(Q,T)
    assert a>0 and N>=5 and N%2 and all(isinstance(i,int) for i in (b,c,h,H))
    assert 0<b<c<h<H and gcd(2*(H-h),N)==1
    assert 0<s<a and b<u<=h and (N-2)*a<t<N*a and 0<v<c
    assert u.denominator==v.denominator==1 and int(c-v)%2==1
    d0,G,g1,d2=int(h-u),2*(H-h),h-c,int(c-v)
    D=d0+G+g1+d2;A=N*a;z=A-t
    times=(d0,d0+G,D-d2)
    bad_residues=[[] for _ in times];good=[]
    for q in range(D):
        slope=(A+z-s+2*a*q)/D
        values=(s+times[0]*slope,s+times[1]*slope-A,s+times[2]*slope-A)
        bad=[(x-a)/(2*a)==floor((x-a)/(2*a)) for x in values]
        for i,hit in enumerate(bad):
            if hit:bad_residues[i].append(q)
        if not any(bad):good.append(q)
    assert good
    # Choose the LAST permissible q rather than the coordinator's first.
    q=good[-1];slope0=(A+z-s+2*a*q)/D
    for time,forbidden in zip(times,bad_residues):
        if time==0:
            assert not forbidden
        elif forbidden:
            modulus=D//gcd(time,D)
            assert modulus>=2
            assert forbidden==list(range(forbidden[0],D,modulus))
    n0=floor((s+d0*slope0+a)/(2*a));z0=s+d0*slope0-2*n0*a
    assert abs(z0)<a
    X0=z0+G*slope0
    assert (X0/(2*a)).denominator!=1  # N odd makes cap endpoints this coset.
    target_cell=(N-1)//2
    # Direct modular inverse, no M enumeration or phase search.
    M=(pow(G,-1,N)*(target_cell-floor(X0/(2*a))))%N
    slope=slope0+2*a*M
    X=z0+G*slope;m=floor(X/(2*A));z1=X-(2*m+1)*A
    assert abs(z1)<a
    n=n0+d0*M
    k=floor((z1+g1*slope+a)/(2*a));z2=z1+g1*slope-2*k*a
    assert abs(z2)<a
    J=(z2+d2*slope-z)/(2*a);assert J.denominator==1
    shifted=bool(int(J)%2)
    initial_residuals=(z0,z1,z2)
    if shifted:
        slope+=2*a*N;n+=N*d0;m+=G;k+=N*g1
    residuals=(s+d0*slope-2*n*a,
        s+d0*slope-2*n*a+G*slope-(2*m+1)*A,
        s+d0*slope-2*n*a+G*slope-(2*m+1)*A+g1*slope-2*k*a)
    assert residuals==initial_residuals and all(abs(x)<a for x in residuals)
    E=z2+d2*slope
    assert ns['fold'](E,2*a)==z
    assert ((E-z)/(4*a)).denominator==1
    return dict(q=q,D=D,good_q=len(good),forbidden=bad_residues,
        forbidden_moduli=[D//gcd(time,D) if time else None for time in times],
        cap_M=M,parity_shift=shifted,slope=slope,indices=[n,m,k],residuals=residuals)

def replay_actual(P,S,T,slope,D):
    """Check the ONE prescribed ray against earliest intersections of actual walls."""
    P=[tuple(map(Q,p)) for p in P];S=tuple(map(Q,S));T=tuple(map(Q,T))
    ns['simple'](P);assert ns['location'](P,S)==ns['location'](P,T)==1
    walls=ns['edges'](P);position=S;velocity=(slope,Q(1));elapsed=Q(0)
    path=[S];events=[]
    while elapsed<D:
        x,y=position;vx,vy=velocity;hits=[]
        for left,right in walls:
            dt=(left[0]-x)/vx if left[0]==right[0] else (left[1]-y)/vy
            p=(x+dt*vx,y+dt*vy)
            if dt>0 and ns['on'](left,right,p):hits.append((dt,p,left,right))
        assert hits
        hit=min(hits,key=lambda e:e[0]);dt,p,left,right=hit
        target_dt=(T[0]-x)/vx
        if target_dt>0 and y+target_dt*vy==T[1] and target_dt<dt:
            elapsed+=target_dt;path.append(T);break
        assert elapsed+dt<D,'Target must be reached before or at its proved developed time'
        assert p not in P
        assert sum(e[0]==dt for e in hits)==1
        elapsed+=dt;path.append(p);events.append(dict(point=p,time=elapsed))
        velocity=(-vx,vy) if left[0]==right[0] else (vx,-vy)
        position=p
    assert path[-1]==T and elapsed==D
    result=ns['path_check'](P,path)
    assert len(events)==result['reflections']
    roofs=[e for e in events if e['point'][1]==max(p[1] for p in P)]
    horizontal=[e for e in events if any(l[1]==r[1] and ns['on'](l,r,e['point']) for l,r in walls)]
    assert len(roofs)==len(horizontal)==1
    return dict(path=path,events=events,actual_target_time=elapsed,roof=roofs[0],**result)

def terminal(label,a,N,b,c,h,H,S,T):
    selection=choose(a,N,b,c,h,H,S,T);a=Q(a);l,w,A=(N-2)*a,(N-1)*a,N*a
    P=[(a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b)]
    return dict(label=label,geometry=[a,l,w,A,b,c,h,H],S=S,T=T,selection=selection,
        **replay_actual(P,S,T,selection['slope'],selection['D']))

fixtures=[
 ('same-height',4,5,1,5,7,8,(2,2),(14,2)),
 ('rising-target',4,5,1,5,7,8,(2,2),(18,4)),
 ('falling-target',4,5,1,5,7,8,(2,6),(14,2)),
 ('target-w',4,5,1,5,7,8,(2,4),(16,2)),
 ('source-h',6,7,2,7,10,11,(4,10),(32,6)),
 ('composite-N',8,9,3,9,12,13,(6,8),(58,4)),
 ('cap-depth-two',4,5,1,5,10,12,(2,8),(18,2)),
 ('rational-horizontal-marks',Q(3,2),7,1,5,8,9,(Q(1,101),6),(Q(21,2)-Q(1,103),4)),
 ('long-arm',4,5,1,5,40,41,(2,38),(14,2)),
]
rows=[terminal(*fixture) for fixture in fixtures]

# Read-only reuse of previously independently verified protected U/L formulas.
old=ast.parse((HERE/'three-reflex-tr01-independent-check.py').read_text())
names={'point','L_vertical','L_horizontal','U_opposite','U_path'}
exec(compile(ast.Module(body=[f for f in old.body if isinstance(f,ast.FunctionDef)
    and f.name in names],type_ignores=[]),'<reviewer-protected-U-L>','exec'),ns)
a,l,w,A,b,c,h,H=map(Q,(4,12,16,20,1,5,7,8))
P=[(a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b)]
R=[(l,0),(A,0),(A,H),(w,H),(w,c),(l,c)]
marks=[(Q(x),Q(y)) for y in range(0,int(H)+1,2) for x in range(0,int(A)+1,2)
       if ns['location'](P,(Q(x),Q(y)))==1]
def G(p):return p[0]<a or p[1]>=h or (p[0]>w and p[1]>=c)
def inR(p):return ns['location'](R,p)==1
whole=[]
for S,T in combinations(marks,2):
    if G(S) and G(T):
        method='protected-U'
        path=ns['U_path'](a,w,A,H-h,H-b,H,(S[0],H-S[1]),(T[0],H-T[1]))
        path=[(x,H-y) for x,y in path]
    elif inR(S) and inR(T):
        method='protected-L'
        path=ns['L_horizontal'](A-l,A-w,c,H,(A-S[0],S[1]),(A-T[0],T[1]))
        path=[(A-x,y) for x,y in path]
    else:
        method='new-terminal'
        X,Y=(S,T) if S[0]<a else (T,S)
        witness=terminal('whole-room-terminal',4,5,1,5,7,8,X,Y)
        path=witness['path'] if X==S else list(reversed(witness['path']))
    # Earliest actual T gives a legal prefix for the inherited protected cases.
    for i,(p,q) in enumerate(zip(path,path[1:])):
        if ns['on'](p,q,T):
            path=path[:i+1]+[T];break
    assert path[0]==S and path[-1]==T
    result=ns['path_check'](P,path)
    whole.append(dict(S=S,T=T,method=method,**result))
assert len(marks)==10 and len(whole)==45
assert sum(r['method']=='new-terminal' for r in whole)==18
L=(A-w)/(2*c);dv=L/(ceil(L*h/(2*a))+ceil(L*h/(2*(A-w)))+3)
Lh=(H-h)/(2*a);dh=Lh/(ceil(Lh*w/(2*c))+ceil(Lh*w/(2*(H-h)))+3)
assert c+2*A/dv==505 and a+2*H/dh==644
out=dict(status='PASS_INDEPENDENT_COPRIME_SELECTOR_AND_ACTUAL_FIRST_HITS',
    source_pins_before=before,source_pins_after=pin_check(),
    request_sha256=hashlib.sha256(REQUEST.read_bytes()).hexdigest(),terminal_rows=rows,
    terminal_cases=len(rows),terminal_reflections=sum(r['reflections'] for r in rows),
    terminal_wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),
    native_points=marks,whole_room_rows=whole,pair_count=len(whole),new_terminal_pairs=18,
    whole_reflections=sum(r['reflections'] for r in whole),
    whole_wall_leg_guards=sum(r['wall_leg_guards'] for r in whole),
    old_height_threshold=505,old_width_threshold=644,
    own_selector='last permissibleq; capM via modularinverse; independent actual earliestwall intersections',
    author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('source_pins_before','source_pins_after','terminal_rows','native_points','whole_room_rows')}))
