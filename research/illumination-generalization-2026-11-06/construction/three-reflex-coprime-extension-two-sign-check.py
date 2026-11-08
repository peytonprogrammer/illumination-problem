"""CE02 prescribed two-sign constructor with unchanged CE01 physical replay."""
from fractions import Fraction as Q
from pathlib import Path
from math import gcd, floor
import importlib.util
import json

HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('frozen_ce01',HERE/'three-reflex-coprime-extension-prescribed-check.py')
ce=importlib.util.module_from_spec(spec)
spec.loader.exec_module(ce)  # Main-only writes do not execute on import.
FORCED_Q=None


def select_two(a,N,L,b,c,h,H,S,T):
    a,l,w,A,P=ce.geometry(a,N,L,b,c,h,H)
    s,u=map(Q,S);t,v=map(Q,T)
    assert 0<s<a and b<u<=h and l<t<A and 0<v<c
    assert u.denominator==v.denominator==1
    d0,G,g1,d2=int(h-u),2*(H-h),h-c,int(c-v)
    z=A-t;r=z/a
    assert gcd(N*d2,L)==2 and r.denominator==1 and int(r)%2
    r=int(r);D=d0+G+g1+d2
    choices=[]
    for q in range(D):
        tau=(A+z-s+2*a*q)/D
        phases=[s+d0*tau,s+(d0+G)*tau-A,s+(D-d2)*tau-A]
        if all((x-a)%(2*a)!=0 for x in phases):choices.append((q,tau))
    assert choices
    if FORCED_Q is None:q,tau=choices[0]
    else:
        matches=[x for x in choices if x[0]==FORCED_Q]
        assert len(matches)==1
        q,tau=matches[0]
    n=floor((s+d0*tau+a)/(2*a));z0=s+d0*tau-2*n*a
    X0=z0+G*tau;offset=(X0-A+a)%(2*a)
    assert 0<offset<2*a
    desired=A-a+offset;shift=(desired-X0)/(2*a)
    assert shift.denominator==1
    M=(int(shift)*pow(G,-1,N))%N
    tau+=2*a*M;n+=d0*M
    X=z0+G*tau;m=(X-desired)/(2*A)
    assert m.denominator==1
    m=int(m);z1=X-(2*m+1)*A
    k=floor((z1+g1*tau+a)/(2*a));z2=z1+g1*tau-2*k*a
    assert abs(z0)<a and abs(z1)<a and abs(z2)<a
    J=(z2+d2*tau-z)/(2*a)
    assert J.denominator==1
    J=int(J);initialJ=J
    sign=1 if J%2==0 else -1
    C=0 if sign==1 else -r
    modulus=L//2
    p=0 if modulus==1 else (((C-J)//2)*pow((N*d2)//2,-1,modulus))%modulus
    tau+=2*a*N*p;n+=N*d0*p;m+=G*p;k+=N*g1*p
    J+=N*d2*p
    final0=s+d0*tau-2*n*a
    final1=final0+G*tau-(2*m+1)*A
    final2=final1+g1*tau-2*k*a
    assert (final0,final1,final2)==(z0,z1,z2)
    E=z2+d2*tau
    j=(J+(r if sign==-1 else 0))//L
    assert E==sign*z+2*L*a*j
    assert ce.fold(E,L*a)==z
    return {'tau':tau,'q':q,'D':D,'cap_M':M,'target_shift_p':p,
            'indices':[n,m,k,j],'residuals':[z0,z1,z2],
            'target_sign':sign,'initial_J':initialJ,'target_phase':E,'target_r':r}


# Only the selector changes in memory; all original finite-wall/velocity/
# first-target guards in the pinned CE01 replay execute without modification.
ce.select=select_two


def run(label,a,N,L,b,c,h,H,S,T,forced=None):
    global FORCED_Q
    FORCED_Q=forced
    try:
        row=ce.replay(label,a,N,L,b,c,h,H,S,T)
    finally:FORCED_Q=None
    if label=='prescribed-negative-image':
        assert row['selection']['tau']==29
        assert row['selection']['initial_J']==7
        assert row['selection']['target_sign']==-1
    return row


def native_column():
    a,N,L,b,c,h,H=4,5,2,1,4,5,6
    a,l,w,A,P=ce.geometry(a,N,L,b,c,h,H)
    marks=[(2,2),(2,4),(14,2),(16,2),(18,2),(18,4)]
    T=(Q(16),Q(2));rows=[]
    for source in marks:
        S=tuple(map(Q,source))
        if S==T:continue
        if S[0]<a:
            row=run('column-terminal',a,N,L,b,c,h,H,S,T)
            row['method']='CE02 terminal';rows.append(row)
        else:
            path=ce.ns['L_horizontal'](A-l,A-w,c,H,
                                       (A-S[0],S[1]),(A-T[0],T[1]))
            path=[(A-x,y) for x,y in path]
            assert path[0]==S and path[-1]==T
            result=ce.ns['path_check'](P,path)
            rows.append({'method':'protected R','S':S,'T':T,'path':path,**result})
    assert len(rows)==5 and sum(x['method']=='CE02 terminal' for x in rows)==2
    return {'marks':marks,'target':T,'source_count':5,'new_terminal_sources':2,'rows':rows}


if __name__=='__main__':
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
        ('d2-six',4,7,4,1,8,10,11,(2,6),(16,2)),
    ]
    rows=[run(*f) for f in fixtures];column=native_column()
    out={'status':'PASS_PRESCRIBED_CE02','rows':rows,'native_column_control':column,
         'terminal_controls':len(rows),'actual_reflections':sum(x['reflections'] for x in rows),
         'wall_leg_guards':sum(x['wall_leg_guards'] for x in rows),
         'negative_target_images':sum(x['selection']['target_sign']==-1 for x in rows),
         'nonzero_reduced_orbit_corrections':sum(x['selection']['target_shift_p']>0 for x in rows),
         'reuse':'Pinned CE01 geometry/physical replay and historical guards reused read-only; selector replaced in memory as disclosed. No assertions removed. Not independent acceptance.',
         'discovery_search_used':False,'whole_r3_complete':False,'whole_goal_complete':False}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('rows','native_column_control')}))
