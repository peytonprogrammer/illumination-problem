"""Prescribed complete formula paths; no direction discovery or peer writes."""
from fractions import Fraction as Q
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py')
own=importlib.util.module_from_spec(spec);spec.loader.exec_module(own)
effort=json.loads((R/'protected-comb-witness-effort.json').read_text())
def check_deadline():assert datetime.now(timezone.utc)<datetime.fromisoformat(effort['deadline_utc'])
def comb(c,H,teeth):
    # Sorted closed tooth bands are disjoint, the first/last touch y0/H.
    assert teeth[0][0]==0 and teeth[-1][1]==H
    p=[(0,0),(teeth[0][2],0)]
    for j,(lo,hi,right) in enumerate(teeth):
        assert 0<=lo<hi<=H and right>c
        p.append((right,hi))
        if j+1<len(teeth):
            nxt=teeth[j+1];assert hi<nxt[0]
            p.extend([(c,hi),(c,nxt[0]),(nxt[2],nxt[0])])
    p.append((0,H));p=[tuple(map(Q,z)) for z in p];own.simple(p);return p

def floor_path(c,u,H,D,bs,bt):
    c,u,H,D,bs,bt=map(Q,(c,u,H,D,bs,bt));delta=abs(bs-bt)
    assert 0<bs<u and 0<bt<u and H>2*u and D>=c*(u+delta)/(u-delta)
    low=min(bs,bt);z=c*low+D*(H-delta)/2
    k=int(z//(2*u*c));tau=(H-bs-bt+4*u*k)/(2*(c+D))
    rs=bs+D*tau-2*u*k;rt=bt+D*tau-2*u*k
    assert 0<=min(rs,rt)<2*u*c/(c+D) and max(rs,rt)<u
    assert rs+rt+2*c*tau==H and tau>0 and k>=0
    S=(c+D,bs);T=(c+D,H-bt)
    lower=[S]+[(c+D-(j*u-bs)/tau,u if j%2 else Q(0)) for j in range(1,2*k+1)]
    # Upper segment is the y-reflected reverse of the analogous source-side
    # segment with depth bt; vertical speed agrees at the spine join.
    backwards=[(c+D,bt)]+[(c+D-(j*u-bt)/tau,u if j%2 else Q(0)) for j in range(1,2*k+1)]
    middle=(Q(0),rs+c*tau)
    path=lower+[middle]+[(x,H-y) for x,y in reversed(backwards)]
    assert path[-1]==T
    assert all(x>=c for x,y in lower[1:]+backwards[1:])
    return path,{'k':k,'tau':tau,'source_portal':rs,'target_portal_from_top':rt,'expected_reflections':4*k+1}

def U_path(c,H,us,ut,Ds,Dt,bs,bt):
    c,H,a,b,Ds,Dt,xs,bt=map(Q,(c,H,us,ut,Ds,Dt,bs,bt));xt=b-bt
    assert 0<xs<a and 0<xt<b and Ds>0 and Dt>0 and H>a+b
    M=H-a-b;ys=c+Ds;yt=c+Dt;S=ys+yt
    t0=1+2*max(a,b)/c;k=max(0,int((2*c*t0-M)//(2*H))+1);B=M+2*k*H
    assert B>2*c*t0
    def lengths(t):
        n=max(0,int((Ds*t-(a-xs))//(2*a))+1)
        m=max(0,int((Dt*t-xt)//(2*b))+1)
        return a-xs+2*n*a,xt+2*m*b,n,m
    t=t0;iterations=0
    while True:
        check_deadline();L,RR,n,m=lengths(t);nxt=(L+RR+B)/S;iterations+=1
        assert nxt>=t
        if nxt==t:break
        t=nxt
    es=L-Ds*t;et=RR-Dt*t;u=c-es/t;v=c-et/t
    assert 0<es<2*a and 0<et<2*b and 0<u<c and 0<v<c and u+v==B/t
    def fold(z,w):r=z%(2*w);return min(r,2*w-r)
    # Work in rotated U coordinates (X,Y)=(physical y,physical x).
    left_r=[Q(0)]+[j*a-xs for j in range(1,2*n+2) if 0<j*a-xs<L]+[L]
    left=[(fold(xs+r,a),ys-r/t) for r in left_r]
    assert left[-1]==(a,u)
    cuts={Q(0),B,u*t}
    for j in range(int(a//H)+1,int((a+B)//H)+1):
        d=j*H-a
        if 0<d<B:cuts.add(d)
    central=[(fold(a+d,H),abs(u-d/t)) for d in sorted(cuts)]
    right_r=[Q(0)]+[xt+j*b for j in range(0,2*m+1) if 0<xt+j*b<RR]+[RR]
    right=[(a+M+fold(xt-r,b),yt-r/t) for r in right_r]
    assert right[-1]==(a+M,v) and central[-1]==right[-1]
    rotated=left+central[1:]+list(reversed(right))[1:]
    path=[(Y,X) for X,Y in rotated]
    assert path[0]==(c+Ds,xs) and path[-1]==(c+Dt,H-bt)
    return path,{'tau':t,'central_turns_k':k,'iterations':iterations,'bottom_arm_index':n,'top_arm_index':m}

rows=[]
for n,m in ((0,0),(0,4),(2,7),(10,1)):
    check_deadline();H=Q(36+2*m);D=Q(4+2*n);right=Q(20+2*n)
    teeth=[(0,4,right),(8,12,right),(16+2*m,20+2*m,right),(24+2*m,28+2*m,right),(32+2*m,H,right)]
    poly=comb(Q(4),H,teeth);path,meta=floor_path(4,4,H,D,2,2)
    guards=own.path_check(poly,path);assert guards['reflections']==meta['expected_reflections']
    assert all(not own.on(a,b,path[-1]) for a,b in zip(path[:-2],path[1:-1]))
    rows.append({'kind':'joint_integer_floor','n':n,'m':m,**meta,**guards,'path':path})
# Unequal offsets at the sharp sufficient width, including smooth portal zero.
H=Q(12);poly=comb(Q(4),H,[(0,4,20),(5,7,15),(8,12,21)])
path,meta=floor_path(4,4,H,12,1,3);guards=own.path_check(poly,path)
assert meta['source_portal']==0 and guards['reflections']==meta['expected_reflections']
rows.append({'kind':'unequal_offset_sharp_width_smooth_zero',**meta,**guards,'path':path})
# The stronger protected-U transfer allows completely asymmetric real data,
# short source/target depths and independently sized intermediate teeth.
for c,H,us,ut,Ds,Dt,bs,bt in [(4,36,4,4,1,2,1,3),(Q(3,2),19,Q(5,2),3,Q(1,3),7,Q(7,4),Q(5,2)),(2,20,3,5,8,Q(1,2),Q(1,2),4)]:
    check_deadline();c,H,us,ut,Ds,Dt,bs,bt=map(Q,(c,H,us,ut,Ds,Dt,bs,bt))
    gap=H-us-ut;teeth=[(0,us,c+Ds+2),(us+gap/4,us+gap/3,c+7),(us+gap/2,us+2*gap/3,c+3),(H-ut,H,c+Dt+2)]
    poly=comb(c,H,teeth);path,meta=U_path(c,H,us,ut,Ds,Dt,bs,bt)
    guards=own.path_check(poly,path)
    assert all(not own.on(a,b,path[-1]) for a,b in zip(path[:-2],path[1:-1]))
    rows.append({'kind':'protected_U_asymmetric_actual_room',**meta,**guards,'path':path})
out={'status':'ALL_EIGHT_PRESCRIBED_ACTUAL_PATHS_PASS','rows':rows,'total_reflections':sum(r['reflections'] for r in rows),'total_wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'whole_goal_complete':False,'discovery':False,'source_sha256':{'resumed-exact-check.py':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest()},'scope':'Exact formula controls only; whole-parameter statements require the separate hand proof.'}
(R/'protected-comb-witness-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('rows','source_sha256')}))
