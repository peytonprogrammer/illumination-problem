#!/usr/bin/env python3
"""Prescribed exact checks of A10 formulas; no candidate direction search."""
from fractions import Fraction as Q
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, signal, time
ROOT=Path(__file__).resolve().parent
EFFORT=ROOT/'centered-T-effort.json'
eff=json.loads(EFFORT.read_text())
deadline=datetime.fromisoformat(eff['aggregate_deadline_utc']).timestamp()
remaining=deadline-time.time()
if remaining<=0: raise SystemExit('Original aggregate deadline expired')
signal.alarm(max(1,int(remaining)))

def near(x):
    k=x.numerator//x.denominator
    return min((k,k+1),key=lambda n:(abs(x-n),n))
def fold(x,a): return a-abs((x+a)%(4*a)-2*a)
def bad_roof(z,a): return z/a==int(z/a) and int(z/a)%2!=0

def construct(a,c,h,S,T):
    s,ys=S;t,yt=T;d=yt-c;D=c-ys
    assert D>0 and 0<d<h and -a<t<a
    if d>D:
        v=d;z0=-v*s/D
        opts=[]
        for residue in (t,2*a-t):
            k=near((z0-residue)/(4*a));opts.append(residue+4*k*a)
        X=min(opts,key=lambda z:(abs(z-z0),z))
        assert abs(X-z0)<(1+v/D)*a
        chart='direct';candidates=1
    else:
        v=2*h-d;assert v>2*D
        z0=-v*s/D;center0=a if t>=0 else 3*a
        C=center0+4*a*near((z0-center0)/(4*a));u=a-abs(t)
        opts=[C-u,C+u]
        good=[]
        for X0 in opts:
            assert fold(X0,a)==t
            assert abs(X0-z0)<(1+v/D)*a
            B=((v-h)*s+(D+h)*X0)/(D+v)
            if not bad_roof(B,a):good.append(X0)
        assert good
        X=good[0];chart='roof';candidates=2
    q=(v*s+D*X)/(D+v)
    assert -a<q<a
    return (X-s,c+v-ys),chart,q,candidates

def trace(L,R,a,c,h,S,T,V):
    verts=[(L,Q(0)),(R,Q(0)),(R,c),(a,c),(a,c+h),(-a,c+h),(-a,c),(L,c)]
    edges=list(zip(verts,verts[1:]+verts[:1]))
    p=S;vx,vy=V;hits=0;roof_hits=0
    bound=20+int(abs(vx)/a)*4
    for step in range(bound):
        opts=[]
        for A,B in edges:
            if A[0]==B[0]:
                if vx==0:continue
                tt=(A[0]-p[0])/vx
                yy=p[1]+tt*vy
                if tt>0 and min(A[1],B[1])<=yy<=max(A[1],B[1]):opts.append((tt,(A[0],yy),'v'))
            else:
                if vy==0:continue
                tt=(A[1]-p[1])/vy
                xx=p[0]+tt*vx
                if tt>0 and min(A[0],B[0])<=xx<=max(A[0],B[0]):opts.append((tt,(xx,A[1]),'h'))
        assert opts,('no wall',p,V)
        tw=min(z[0] for z in opts)
        dx,dy=T[0]-p[0],T[1]-p[1]
        if dx*vy==dy*vx:
            tt=dx/vx if vx else dy/vy
            if 0<tt<tw:return hits,roof_hits
        active=[z for z in opts if z[0]==tw]
        wallpoint=active[0][1]
        assert wallpoint not in verts,('corner',S,T,V,wallpoint)
        assert len(active)==1,('multiple wall',active)
        p=wallpoint;hits+=1
        if p[1]==c+h:roof_hits+=1
        if active[0][2]=='v':vx=-vx
        else:vy=-vy
    raise AssertionError(('reflection guard exhausted',S,T,V,bound))

rooms=[]
for a,L,R in [(Q(1),Q(-3),Q(4)),(Q(2,3),Q(-5,3),Q(7,3)),(Q(3,2),Q(-8),Q(2))]:
    for c in (Q(1),Q(5,3)):
        for ratio in (Q(3,2),Q(2),Q(5)):
            rooms.append((L,R,a,c,c*ratio))
counts={'rooms':len(rooms),'paths':0,'direct_chart':0,'roof_chart':0,'contacts':0,'axis_targets':0,'q_zero':0,'roof_contacts':0,'two_candidate_roof_rejections':0}
examples=[]
for L,R,a,c,h in rooms:
    srcx=[L+( -a-L)*Q(i,4) for i in (1,2,3)]+[a+(R-a)*Q(i,4) for i in (1,2,3)]
    for s in srcx:
      for ys in (c/7,c/3,2*c/3,6*c/7):
       for t in (-4*a/5,-a/3,Q(0),a/4,5*a/6):
        for d in (h/11,h/3,2*h/3,10*h/11):
            if time.time()>=deadline:raise SystemExit('Original aggregate deadline reached')
            S=(s,ys);T=(t,c+d)
            V,chart,q,n=construct(a,c,h,S,T)
            hits,roofhits=trace(L,R,a,c,h,S,T,V)
            assert roofhits<=int(chart=='roof') # first actual T can occur before intended roof event
            counts['paths']+=1;counts[chart+'_chart']+=1;counts['contacts']+=hits;counts['roof_contacts']+=roofhits
            counts['axis_targets']+=t==0;counts['q_zero']+=q==0
            if len(examples)<8:examples.append({'S':list(map(str,S)),'T':list(map(str,T)),'V':list(map(str,V)),'chart':chart,'q':str(q),'reflections':hits})
signal.alarm(0)
out={'status':'PASS','kind':'exact checks of prescribed proof formulas, no direction or room discovery','counts':counts,'examples':examples,'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),ROOT/'centered-T-proof.md']},'ended_utc':datetime.now(timezone.utc).isoformat(),'within_original_effort_deadline':time.time()<deadline,'whole_goal_complete':False}
(ROOT/'centered-T-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out['counts'],indent=2))
