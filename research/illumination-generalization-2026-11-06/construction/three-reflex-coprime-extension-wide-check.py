"""CE03 fixed arithmetic selectors and exact original-wall replay; no discovery."""
from fractions import Fraction as Q
from pathlib import Path
from math import gcd, floor, ceil
from itertools import combinations
import importlib.util
import json

HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('ce01_guard_library',HERE/'three-reflex-coprime-extension-prescribed-check.py')
old=importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
ns=old.ns
fold=old.fold


def geometry(a,N,K,L,b,c,h,H):
    a=Q(a)
    assert isinstance(N,int) and isinstance(K,int) and isinstance(L,int)
    assert 1<=K<L and N>=L+2 and a>0
    assert all(isinstance(z,int) for z in (b,c,h,H)) and 0<b<c<h<H
    l,w,A=(N-L)*a,(N-K)*a,N*a
    P=[(a,Q(b)),(a,Q(h)),(w,Q(h)),(w,Q(c)),(l,Q(c)),
       (l,Q(0)),(A,Q(0)),(A,Q(H)),(Q(0),Q(H)),(Q(0),Q(b))]
    ns['simple'](P)
    return a,l,w,A,P


def select(a,N,K,L,b,c,h,H,S,T,forced=None):
    a,l,w,A,P=geometry(a,N,K,L,b,c,h,H)
    s,u=map(Q,S);t,v=map(Q,T)
    assert 0<s<a and b<u<H and l<t<A and 0<v<c
    assert u.denominator==v.denominator==1
    assert ns['location'](P,(s,u))==ns['location'](P,(t,v))==1
    lower=u<=h
    d0=int(max(h-u,0));C=int(2*(H-h) if lower else 2*H-h-u)
    g1=h-c;d2=int(c-v);D=d0+C+g1+d2;z=A-t;R=K*a
    assert D==2*H-u-v and gcd(N*K*d2,L)==1
    delta=gcd(C,N)
    assert delta==1 if K==1 else delta<K
    choices=[]
    for q in range(D):
        tau=(A+z-s+2*a*q)/D
        bad=[]
        if lower:bad.append((s+d0*tau-a)%(2*a)==0)
        if K==1:bad.append((s+(d0+C)*tau-A-a)%(2*a)==0)
        bad.append((s+(D-d2)*tau-A-R)%(2*a)==0)
        if not any(bad):choices.append((q,tau))
    assert choices
    if forced is None:q,tau=choices[0]
    else:
        picked=[x for x in choices if x[0]==forced[0]]
        assert len(picked)==1
        q,tau=picked[0]
    n=floor((s+d0*tau+a)/(2*a)) if lower else 0
    z0=s+d0*tau-2*n*a
    assert abs(z0)<a
    X0=z0+C*tau
    r=floor((A-X0)/(2*a*delta)+Q(1,2))
    modulus=N//delta
    M=(r*pow(C//delta,-1,modulus))%modulus
    if forced is not None:M=forced[1]
    assert 0<=M<modulus
    tau+=2*a*M
    if lower:n+=d0*M
    X=z0+C*tau;m=floor(X/(2*A));z1=X-(2*m+1)*A
    k=floor((z1+g1*tau+R)/(2*R));z2=z1+g1*tau-2*k*R
    assert abs(z1)<R and abs(z2)<R
    J=(z2+d2*tau-z)/(2*a)
    assert J.denominator==1
    J=int(J);p=(-J*pow(N*K*d2,-1,L))%L
    tau+=2*a*N*K*p
    if lower:n+=N*K*d0*p
    m+=K*C*p;k+=N*g1*p;J+=N*K*d2*p
    f0=s+d0*tau-2*n*a
    f1=f0+C*tau-(2*m+1)*A
    f2=f1+g1*tau-2*k*R
    assert (f0,f1,f2)==(z0,z1,z2) and J%L==0
    assert z2+d2*tau==z+2*L*a*(J//L)
    return {'q':q,'D':D,'tau':tau,'lower_source':lower,'cap_flight':C,
            'cap_gcd':delta,'cap_M':M,'target_shift_p':p,
            'indices':[n,m,k,J//L],'residuals':[z0,z1,z2]}


def replay(label,a,N,K,L,b,c,h,H,S,T,forced=None):
    a,l,w,A,P=geometry(a,N,K,L,b,c,h,H)
    S=tuple(map(Q,S));T=tuple(map(Q,T));s,u=S;t,v=T
    sel=select(a,N,K,L,b,c,h,H,S,T,forced)
    tau=sel['tau'];z0,z1,z2=sel['residuals']
    lower=sel['lower_source'];e1,e2,end=2*H-h,2*H-c,2*H-v
    cap_begin=Q(h) if lower else u
    bands=[]
    if lower and u<h:bands.append((u,Q(h),a,s,False))
    bands.extend([(cap_begin,Q(e1),A,z0,False),
                  (Q(e1),Q(e2),K*a,z1,True),
                  (Q(e2),Q(end),L*a,z2,True)])
    roof_phase=z0+tau*(H-cap_begin)
    singular=roof_phase%A==0
    if lower:assert not singular
    start=2*H-u if singular else u
    if singular:assert not lower and H<start<e1
    events={start,end}
    if start<H<end:events.add(Q(H))
    for begin,stop,width,phase,mirror in bands:
        if start<=begin<=end:events.add(begin)
        if start<=stop<=end:events.add(stop)
        for j in range(floor(phase/width)-1,
                       ceil((phase+tau*(stop-begin))/width)+2):
            eta=begin+(j*width-phase)/tau
            if max(start,begin)<eta<min(end,stop):events.add(eta)
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
    assert len(roof)==(0 if singular else 1)
    assert all(0<p[0]<A for p in roof)
    if label=='wider-singular-roof-suffix':
        assert singular and tau==18 and start==8
    if label=='narrow-singular-roof-suffix':
        assert singular and tau==27 and start==8
    return {'label':label,'geometry':[a,l,w,A,b,c,h,H],
            'N':N,'K':K,'L':L,'S':S,'T':T,'selection':sel,'path':path,
            'singular_roof_discarded':singular,'actual_start_eta':start,**result}


def first_target(path,T):
    out=[path[0]]
    for p,q in zip(path,path[1:]):
        dx,dy=q[0]-p[0],q[1]-p[1]
        theta=(T[0]-p[0])/dx if dx else (T[1]-p[1])/dy
        if 0<theta<=1 and (p[0]+theta*dx,p[1]+theta*dy)==T:
            out.append(T);return out
        out.append(q)
    raise AssertionError('Actual target missing')


def whole_room():
    a,N,K,L,b,c,h,H=4,5,2,3,1,4,5,7
    a,l,w,A,P=geometry(a,N,K,L,b,c,h,H)
    marks=[(2,2),(10,2),(12,2),(14,2),(16,2),(18,2),
           (2,4),(14,4),(16,4),(18,4),
           (2,6),(4,6),(6,6),(8,6),(10,6),(12,6),(14,6),(16,6),(18,6)]
    assert len(marks)==19 and all(ns['location'](P,p)==1 for p in marks)
    def inG(p):return p[0]<a or p[1]>=h or(p[0]>w and p[1]>=c)
    def inR(p):return (l<p[0]<A and 0<p[1]<c)or(w<p[0]<A and 0<p[1]<H)
    def bottom(p):return l<p[0]<A and 0<p[1]<c
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
            if bottom(S):S,T=T,S
            assert bottom(T)
            if S[0]<a:
                row=replay('whole-native-terminal-'+str(i),a,N,K,L,b,c,h,H,S,T)
                row['method']='CE03 terminal';rows.append(row);continue
            assert a<=S[0]<=w and h<S[1]<H
            U=ns['U_path'](H-h,H-c,H,A-w,A,A-l,
                            (H-S[1],A-S[0]),(H-T[1],A-T[0]))
            path=[(A-y,H-x) for x,y in U];method='protected rotated U TR05'
        assert path[0]==S and path[-1]==T
        path=first_target(path,T)
        result=ns['path_check'](P,path)
        rows.append({'method':method,'S':S,'T':T,'path':path,**result})
    assert len(rows)==171
    assert sum(x['method']=='CE03 terminal' for x in rows)==15
    assert sum(x['method']=='protected rotated U TR05' for x in rows)==25
    return {'geometry':[a,l,w,A,b,c,h,H],'marks':marks,'pair_count':len(rows),
            'terminal_pairs':15,'TR05_upper_cap_pairs':25,'rows':rows,
            'reflections':sum(x['reflections'] for x in rows),
            'wall_leg_guards':sum(x['wall_leg_guards'] for x in rows)}


if __name__=='__main__':
    fixtures=[
        ('wider-lower-thin',4,5,2,3,1,4,5,6,(2,4),(10,2)),
        ('wider-singular-roof-suffix',4,5,2,3,1,4,5,7,(2,6),(10,2),(4,1)),
        ('wider-upper-ordinary',4,5,2,3,1,4,5,7,(2,6),(14,2)),
        ('noncoprime-lower-cap',4,8,3,5,1,4,5,6,(2,4),(14,2)),
        ('noncoprime-upper-cap',4,9,4,5,1,4,5,7,(2,6),(18,2)),
        ('narrow-upper-odd-c',4,5,1,2,1,5,7,9,(2,8),(14,2)),
        ('narrow-source-on-h',4,5,1,3,1,4,6,8,(2,6),(10,2)),
        ('narrow-singular-roof-suffix',4,7,1,5,1,4,5,7,(1,6),(26,1),(6,2)),
        ('long-thick-cap',4,11,3,5,1,4,7,11,(2,10),(26,2)),
        ('power2L-oddK',4,7,3,4,1,5,7,9,(2,8),(14,2)),
        ('rational-horizontal',Q(3,2),7,2,3,1,4,5,7,(Q(1,7),6),(Q(67,11),2)),
    ]
    rows=[replay(*f) for f in fixtures];whole=whole_room()
    out={'status':'PASS_PRESCRIBED_CE03','terminal_controls':rows,'whole_native_control':whole,
         'terminal_control_count':len(rows),'terminal_reflections':sum(x['reflections'] for x in rows),
         'terminal_wall_guards':sum(x['wall_leg_guards'] for x in rows),
         'singular_roof_suffixes':sum(x['singular_roof_discarded'] for x in rows),
         'noncoprime_cap_controls':sum(x['selection']['cap_gcd']>1 for x in rows),
         'guard_reuse':'Read-only frozen CE01 reviewer-predicate/U/L library; new formulas and guards explicit. Not independent acceptance.',
         'discovery_search_used':False,'whole_r3_complete':False,'whole_goal_complete':False}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('terminal_controls','whole_native_control')}))
    print(json.dumps({k:v for k,v in whole.items() if k not in ('rows','marks')},default=str))
