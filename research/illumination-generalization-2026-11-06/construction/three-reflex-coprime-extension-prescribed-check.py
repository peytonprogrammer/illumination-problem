"""CE01 formula construction on fixed controls, not optical discovery."""
from fractions import Fraction as Q
from math import gcd, floor, ceil
from pathlib import Path
from itertools import combinations
import ast
import json

HERE=Path(__file__).parent
BASE=HERE.parent
ns={'Q':Q,'F':Q}
sources=[(BASE/'review/resumed-exact-check.py',
          {'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}),
         (BASE/'review/three-reflex-tr01-independent-check.py',
          {'point','L_vertical','L_horizontal','U_opposite','U_path'})]
for source,names in sources:
    tree=ast.parse(source.read_text())
    exec(compile(ast.Module(body=[n for n in tree.body
                                 if isinstance(n,ast.FunctionDef) and n.name in names],
                            type_ignores=[]),str(source),'exec'),ns)
fold=ns['fold']


def geometry(a,N,L,b,c,h,H):
    a=Q(a)
    assert isinstance(N,int) and isinstance(L,int) and L>=2 and N>=L+2
    assert all(isinstance(z,int) for z in (b,c,h,H)) and 0<b<c<h<H
    assert gcd(2*(H-h),N)==1
    l,w,A=(N-L)*a,(N-1)*a,N*a
    P=[(a,Q(b)),(a,Q(h)),(w,Q(h)),(w,Q(c)),(l,Q(c)),
       (l,Q(0)),(A,Q(0)),(A,Q(H)),(Q(0),Q(H)),(Q(0),Q(b))]
    ns['simple'](P)
    return a,l,w,A,P


def select(a,N,L,b,c,h,H,S,T):
    a,l,w,A,P=geometry(a,N,L,b,c,h,H)
    s,u=map(Q,S);t,v=map(Q,T)
    assert 0<s<a and b<u<=h and l<t<A and 0<v<c
    assert u.denominator==v.denominator==1
    assert ns['location'](P,(s,u))==ns['location'](P,(t,v))==1
    d0,G,g1,d2=int(h-u),2*(H-h),h-c,int(c-v)
    assert gcd(N*d2,L)==1
    D=d0+G+g1+d2;z=A-t
    choices=[];bad_rows=[]
    for q in range(D):
        tau=(A+z-s+2*a*q)/D
        events=[s+d0*tau,s+(d0+G)*tau-A,s+(D-d2)*tau-A]
        bad=[(x-a)%(2*a)==0 for x in events]
        bad_rows.append(bad)
        if not any(bad):choices.append((q,tau))
    assert choices
    equal_blocks=d0==G==g1==d2
    if equal_blocks and any(x[1] for x in bad_rows):
        assert not any(x[0] for x in bad_rows)
    q,tau=choices[0]
    n=floor((s+d0*tau+a)/(2*a));z0=s+d0*tau-2*n*a
    X0=z0+G*tau
    offset=(X0-A+a)%(2*a)
    assert 0<offset<2*a
    desired=A-a+offset
    shift=(desired-X0)/(2*a)
    assert shift.denominator==1
    M=(int(shift)*pow(G,-1,N))%N
    tau+=2*a*M;n+=d0*M
    X=z0+G*tau
    m=(X-desired)/(2*A)
    assert m.denominator==1
    m=int(m);z1=X-(2*m+1)*A
    k=floor((z1+g1*tau+a)/(2*a));z2=z1+g1*tau-2*k*a
    assert abs(z0)<a and abs(z1)<a and abs(z2)<a
    J=(z2+d2*tau-z)/(2*a)
    assert J.denominator==1
    J=int(J);p=(-J*pow(N*d2,-1,L))%L
    tau+=2*a*N*p;n+=N*d0*p;m+=G*p;k+=N*g1*p
    J+=N*d2*p
    assert J%L==0
    final0=s+d0*tau-2*n*a
    final1=final0+G*tau-(2*m+1)*A
    final2=final1+g1*tau-2*k*a
    assert (final0,final1,final2)==(z0,z1,z2)
    E=z2+d2*tau
    assert E==z+2*L*a*(J//L)
    return {'tau':tau,'q':q,'D':D,'cap_M':M,'target_shift_p':p,
            'indices':[n,m,k,J//L],'residuals':[z0,z1,z2],
            'equal_four_heights':equal_blocks,
            'bad_class_counts':[sum(row[i] for row in bad_rows) for i in range(3)],
            'target_phase':E}


def replay(label,a,N,L,b,c,h,H,S,T):
    a,l,w,A,P=geometry(a,N,L,b,c,h,H)
    S=tuple(map(Q,S));T=tuple(map(Q,T));s,u=S;t,v=T
    sel=select(a,N,L,b,c,h,H,S,T)
    tau=sel['tau'];z0,z1,z2=sel['residuals']
    e1,e2,end=2*H-h,2*H-c,2*H-v
    bands=[]
    if u<h:bands.append((u,Q(h),a,s,False))
    bands.extend([(Q(h),Q(e1),A,z0,False),
                  (Q(e1),Q(e2),a,z1,True),
                  (Q(e2),Q(end),L*a,z2,True)])
    events={u,Q(H),end}
    for begin,stop,width,phase,mirror in bands:
        events.update((begin,stop))
        for i in range(floor(phase/width)-1,
                       ceil((phase+tau*(stop-begin))/width)+2):
            eta=begin+(i*width-phase)/tau
            if begin<eta<stop:events.add(eta)
    def at(eta):
        xs=[]
        for begin,stop,width,phase,mirror in bands:
            if begin<=eta<=stop:
                x=fold(phase+tau*(eta-begin),width)
                xs.append(A-x if mirror else x)
        assert xs and len(set(xs))==1
        return (xs[0],min(eta,2*H-eta))
    times=sorted(events);path=[at(eta) for eta in times]
    assert path[0]==S and path[-1]==T
    result=ns['path_check'](P,path)
    velocities=[]
    for i,(p,q) in enumerate(zip(path,path[1:])):
        dt=times[i+1]-times[i]
        vel=((q[0]-p[0])/dt,(q[1]-p[1])/dt)
        assert abs(vel[0])==tau and abs(vel[1])==1
        theta=(t-p[0])/vel[0]
        if i<len(path)-2:
            assert not(0<theta<=dt and p[1]+theta*vel[1]==v)
        velocities.append(vel)
    for i,p in enumerate(path[1:-1],1):
        contacts=[(x,y) for x,y in ns['edges'](P) if ns['on'](x,y,p)]
        vx,vy=velocities[i-1]
        expected=((-vx,vy) if contacts[0][0][0]==contacts[0][1][0]
                  else (vx,-vy)) if contacts else (vx,vy)
        assert velocities[i]==expected
    roof=[p for p in path if p[1]==H]
    assert len(roof)==1 and 0<roof[0][0]<A
    return {'label':label,'geometry':[a,l,w,A,b,c,h,H],
            'L':L,'N':N,'S':S,'T':T,'selection':sel,'path':path,**result}


def whole_control():
    a,N,L,b,c,h,H=4,5,3,1,4,5,6
    a,l,w,A,P=geometry(a,N,L,b,c,h,H)
    # Explicit complete list of native marks for this one fixed room.
    marks=[(2,2),(2,4),(10,2),(12,2),(14,2),(16,2),(18,2),(18,4)]
    assert all(ns['location'](P,p)==1 for p in marks)
    def inG(p):return p[0]<a or p[1]>=h or(p[0]>w and p[1]>=c)
    def inR(p):return (l<p[0]<A and 0<p[1]<c)or(w<p[0]<A and 0<p[1]<H)
    rows=[]
    for i,(S,T) in enumerate(combinations(marks,2)):
        S=tuple(map(Q,S));T=tuple(map(Q,T))
        if inG(S) and inG(T):
            path=ns['U_path'](a,w,A,H-h,H-b,H,
                              (S[0],H-S[1]),(T[0],H-T[1]))
            path=[(x,H-y) for x,y in path];method='protected G'
        elif inR(S) and inR(T):
            path=ns['L_horizontal'](A-l,A-w,c,H,
                                    (A-S[0],S[1]),(A-T[0],T[1]))
            path=[(A-x,y) for x,y in path];method='protected R'
        else:
            if S[0]>=a:S,T=T,S
            row=replay('native-terminal-'+str(i),a,N,L,b,c,h,H,S,T)
            row['method']='CE01 terminal';rows.append(row);continue
        assert path[0]==S and path[-1]==T
        result=ns['path_check'](P,path)
        rows.append({'method':method,'S':S,'T':T,'path':path,**result})
    assert len(rows)==28 and sum(r['method']=='CE01 terminal' for r in rows)==10
    return {'geometry':[a,l,w,A,b,c,h,H],'marks':marks,'pair_count':len(rows),
            'terminal_pairs':10,'rows':rows,
            'reflections':sum(r['reflections'] for r in rows),
            'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows)}


if __name__=='__main__':
    fixtures=[
        ('even-d2-low',4,5,3,1,4,5,6,(2,2),(10,2)),
        ('even-d2-high',4,5,3,1,4,5,6,(2,4),(14,2)),
        ('target-on-w',4,5,3,1,4,5,6,(2,2),(16,2)),
        ('source-on-h',4,5,3,1,4,6,7,(2,6),(10,2)),
        ('equal-block-cap-nonempty',4,5,3,1,4,6,7,(2,4),(10,2)),
        ('equal-block-cap-empty',4,5,3,1,4,6,7,(2,4),(14,2)),
        ('rational-x-equal-block',Q(3,2),7,3,1,4,6,7,(Q(1,7),4),(Q(67,11),2)),
        ('L5-cap-height2',4,7,5,2,6,10,12,(2,8),(10,4)),
        ('L7-even-d2-four',4,9,7,1,8,11,12,(2,10),(14,4)),
        ('L4-odd-d2',4,7,4,1,7,10,11,(2,8),(14,2)),
        ('L9-nonprime',4,11,9,1,4,7,8,(2,6),(10,2)),
    ]
    rows=[replay(*f) for f in fixtures]
    whole=whole_control()
    out={'status':'PASS_PRESCRIBED_CE01','terminal_controls':rows,'whole_native_control':whole,
         'terminal_control_count':len(rows),'terminal_control_reflections':sum(r['reflections'] for r in rows),
         'terminal_control_wall_guards':sum(r['wall_leg_guards'] for r in rows),
         'nonzero_final_L_corrections':sum(r['selection']['target_shift_p']>0 for r in rows),
         'formula_guard_reuse':'Read-only AST of frozen reviewer finite-wall predicates and protected U/L formulas; not independent implementation or proof acceptance.',
         'discovery_search_used':False,'whole_r3_complete':False,'whole_goal_complete':False}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('terminal_controls','whole_native_control')}))
    print(json.dumps({k:v for k,v in whole.items() if k not in ('rows','marks')} ,default=str))
