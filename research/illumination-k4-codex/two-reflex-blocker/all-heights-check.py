"""Finite formula construction for fixed U-room inputs; no optical search."""
from pathlib import Path
from fractions import Fraction as F
import runpy,contextlib,io,json
root=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()): base=runpy.run_path(str(root/'check.py'))
fold=base['fold'];verify=base['verify_path']

def first(T,ell,period):
    n=max(0,(T-ell)//period+1)
    return ell+n*period,n

def construct(a,b,M,c,HL,HR,xs,ys,xt,yt):
    A=a+M+b; S=ys+yt; t0=2*max(a,b)/c+1
    k=max(0,(2*c*t0-M)//(2*A)+1)
    B=M+2*k*A; upper=(B+2*a+2*b)/(2*c)
    assert B>2*c*t0 and upper>t0
    t=t0; iterations=0
    _,nbound=first((ys-c)*upper,a-xs,2*a)
    _,mbound=first((yt-c)*upper,xt,2*b)
    bound=nbound+mbound+3
    while True:
        L,n=first((ys-c)*t,a-xs,2*a)
        R,m=first((yt-c)*t,xt,2*b)
        next_t=(L+R+B)/S
        iterations+=1
        assert t<=next_t<=upper and iterations<=bound
        if next_t==t:break
        t=next_t
    ls=L-(ys-c)*t; lt=R-(yt-c)*t
    assert 0<ls<2*a and 0<lt<2*b
    u=ys-L/t; v=yt-R/t
    assert 0<u<c and 0<v<c and u+v==B/t
    assert u+2*a/t>c and v+2*b/t>c
    X=a+u*t
    assert k*A+M/2<X<(k+1)*A-M/2
    bottom_x=fold(X,A)
    assert M/2<bottom_x<A-M/2
    D=L+B+R; z=b-xt
    events=[]
    for j in range(1,2*n+1):
        d=j*a-xs
        events.append((d,a if j%2 else F(0),ys-d/t))
    for j in range(1,2*m+1):
        back=j*b-z
        events.append((D-back,a+M if j%2 else A,yt-back/t))
    for j in range(1,2*k+1):
        dd=j*A-a
        assert 0<dd<B
        events.append((L+dd,A if j%2 else F(0),abs(u-dd/t)))
    events.append((L+u*t,bottom_x,F(0)))
    events.sort()
    assert len({d for d,px,py in events})==len(events)
    path=[(xs,ys)]+[(px,py) for d,px,py in events]+[(a+M+xt,yt)]
    checks=verify(path,a,M,HL,c,right_width=b,right_height=HR)
    assert sum(py==0 for px,py in path[1:-1])==1
    return dict(k=k,fixed_point_iterations=iterations,tau=str(t),L=str(L),R=str(R),
        source_remainder=str(ls),target_remainder=str(lt),bottom_x=str(bottom_x),
        reflections=len(path)-2,wall_incidence_checks=checks)

fixtures=[
    ('former-single-crossing-obstruction',2,2,F(1,100),F(1,1000),1,1,1,F(1,3),1,F(2,3)),
    ('unequal-marks',2,2,1,F(1,10),1,1,F(1,3),F(1,5),F(7,4),F(4,5)),
    ('unequal-arms',1,3,2,F(1,2),2,4,F(1,7),F(3,2),F(11,4),F(7,2)),
    ('both-on-passage-height',1,2,1,F(1,2),2,3,F(1,3),F(1,2),F(7,4),F(1,2)),
    ('one-on-passage-height',1,2,1,F(1,2),2,3,F(1,3),F(1,2),F(7,4),F(5,2)),
    ('wide-notch',1,2,40,F(1,3),2,5,F(3,4),F(4,3),F(1,3),F(13,3))]
results=[]
for label,*parameters in fixtures:
    info=construct(*map(F,parameters))
    results.append(dict(label=label,**info))
result=dict(status='PASS',method='finite monotone matching formula on six fixed inputs; exact polygon verification, no optical search',fixtures=results,
    total_wall_incidence_checks=sum(z['wall_incidence_checks'] for z in results))
(root/'all-heights-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
