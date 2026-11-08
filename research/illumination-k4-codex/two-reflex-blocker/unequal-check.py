"""Prescribed exact unequal-height constructions; no candidate or ray search."""
from fractions import Fraction as F
from pathlib import Path
import runpy,contextlib,io,json
root=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()): base=runpy.run_path(str(root/'check.py'))
fold=base['fold']; verify_path=base['verify_path']; first_length=base['first_length']

def events(a,x,phase,n):
    if phase=='minus': return [(j*a-x,a if j%2 else F(0)) for j in range(1,2*n+1)]
    return [(x+j*a,F(0) if j%2==0 else a) for j in range(2*n+1)]

def one_bottom(a,M,x,ys,yt,H,c,L,R,phaseL,nL,phaseR,nR):
    D=L+M+R; beta=(ys+yt)/D; A=2*a+M
    qs=ys-beta*L; qt=-yt+beta*R
    assert abs(qs)<c and abs(qt)<c
    left=events(a,x,phaseL,nL); right=events(a,x,phaseR,nR)
    if nL: assert qs+2*a*beta>c
    if nR: assert -qt+2*a*beta>c
    path_events=[(d,px,abs(ys-beta*d)) for d,px in left]
    path_events += [(D-d,A-px,abs(ys-beta*(D-d))) for d,px in right]
    bottom_d=ys/beta
    assert all(d!=bottom_d for d,px,py in path_events)
    if bottom_d<L:
        px=fold(x+(1 if phaseL=='minus' else -1)*bottom_d,a)
    elif bottom_d<=L+M: px=a+bottom_d-L
    else: px=A-fold(x+(1 if phaseR=='minus' else -1)*(D-bottom_d),a)
    path_events.append((bottom_d,px,F(0))); path_events.sort()
    path=[(x,ys)]+[(px,py) for d,px,py in path_events]+[(A-x,yt)]
    incidences=verify_path(path,a,M,H,c)
    return path,dict(beta=str(beta),q_source=str(qs),q_target=str(qt),bottom_x=str(px),
        reflections=len(path)-2,wall_incidence_checks=incidences,portal_bottom=qs==0 or qt==0)

fixtures=[
    ('right-arm-bottom',F(2),F(1),F(1),F(11,20),F(9,20),F(1),F(1,10)),
    ('left-arm-bottom',F(2),F(1),F(1),F(9,20),F(11,20),F(1),F(1,10)),
    ('wide-passage',F(1),F(2),F(1,2),F(21,10),F(19,10),F(3),F(1)),
    ('thin-passage',F(2),F(1),F(1),F(40001,100000),F(39999,100000),F(1),F(1,1000)),
    ('long-notch',F(3,2),F(40),F(2,7),F(9001,10000),F(8999,10000),F(2),F(1,20)),
    ('smooth-portal-bottom',F(2),F(1),F(1),F(24,55),F(4,11),F(1),F(1,10))]
results=[]
for label,a,M,x,ys,yt,H,c in fixtures:
    y=(ys+yt)/2; delta=(ys-yt)/2; d=abs(delta); h=M/2
    margin=a*(c-d)*(y-c-d)-y*h*d
    assert 0<d<c and margin>0
    B=y*h/(c-d)-h; U=y*(h+2*a)/(c+d)-h
    assert U>B+2*a
    paths=[]; details=[]
    for phase in ('minus','plus'):
        L,n=first_length(a,x,B,phase)
        assert B<L<=B+2*a<U
        path,info=one_bottom(a,M,x,ys,yt,H,c,L,L,phase,n,phase,n)
        assert info['bottom_x']==str(a+h+delta*(L+h)/y)
        paths.append(path);details.append(dict(length=str(L),**info))
    assert not(set(paths[0][1:-1])&set(paths[1][1:-1]))
    results.append(dict(label=label,inequality_margin=str(margin),paths=details))

# A complete modular obstruction to a bottom contact in the passage, plus a
# fixed one-bottom connection whose bottom contact is inside the right arm.
a=F(2);M=F(1,100);x=F(1);ys=F(1,3);yt=F(2,3);H=F(1);c=F(1,1000)
assert -M*ys>-F(1,3) and M*yt<F(1,3)
# Positive odd lengths have R-2L odd, hence absolute Delta at least1/3.
path,info=one_bottom(a,M,x,ys,yt,H,c,F(115),F(231),'plus',28,'plus',57)
assert F(info['q_source'])==F(101,103803) and F(info['q_target'])==F(98,103803)
assert a+M<F(info['bottom_x'])<2*a+M
# Frozen repeated-crossing construction supplied by the separate reviewer.
L=F(133269);R=F(266939);k=100;A=2*a+M;B=M+2*k*A
D=L+R+B;beta=(ys+yt)/D;N=120303003
qs=ys-beta*L;qt=-yt+beta*R
assert D==F(40101001,100) and beta==F(100,40101001)
assert qs==F(120301,N) and qt==-F(120302,N)
assert 0<qs<c and 0<-qt<c
assert qs+2*a*beta>c and -qt+2*a*beta>c
# Monotonic arm heights mean these nearest-contact tests cover the entire arms.
assert qs+a*beta>0 and qt-a*beta<0
outer_checks=0
for j in range(1,2*k+1):
    dd=j*A-a
    assert 0<dd<B
    yy=abs(qs-beta*dd)
    assert 0<yy<c
    outer_checks+=1
crossing_checks=0
for j in range(2*k+1):
    if j%2==0:
        begin=j*A;end=begin+M
    else:
        begin=(j+1)*A-a-(a+M);end=begin+M
    assert 0<=begin<end<=B
    assert abs(qs-beta*begin)<c and abs(qs-beta*end)<c
    crossing_checks+=1
assert qs-beta*(100*A)==F(1,N) and qs-beta*(100*A+M)==-F(2,N)
bottom_dd=qs/beta
bottom_x=fold(a+bottom_dd,A)
assert bottom_x==F(601,300) and a<bottom_x<a+M
repeated=dict(L=str(L),R=str(R),k=k,beta=str(beta),bottom_x=str(bottom_x),
    outer_contact_checks=outer_checks,passage_crossing_checks=crossing_checks,status='PASS')

result=dict(status='PASS',method='fixed formula evaluations, exact polygon intersections and complete parity argument; no search',
    disjoint_pair_fixtures=results,passage_obstruction_bypass=info,repeated_crossing_control=repeated,
    total_wall_incidence_checks=sum(z['wall_incidence_checks'] for r in results for z in r['paths'])+info['wall_incidence_checks'])
(root/'unequal-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
