"""Independent twist arithmetic and exact prescribed original-room paths.
No peer code imports/execution, candidate directions or room discovery.
"""
from fractions import Fraction as F
from pathlib import Path
from math import gcd,lcm
from importlib.util import spec_from_file_location,module_from_spec
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sp=spec_from_file_location('own_field',BASE/'arbitrary-endpoints-independent/check.py')
G=module_from_spec(sp);sp.loader.exec_module(G);K=G.K

# The ray tracer needs only affine pairs c+r*sqrt(2), not field division.
def rat(x):return F(x),F(0)
def add(x,y):return x[0]+y[0],x[1]+y[1]
def neg(x):return -x[0],-x[1]
def sub(x,y):return add(x,neg(y))
def scale(c,x):return c*x[0],c*x[1]
def sign(x):
    a,b=x
    if not b:return (a>0)-(a<0)
    if not a:return (b>0)-(b<0)
    if a>=0 and b>=0:return 1
    if a<=0 and b<=0:return -1
    d=a*a-2*b*b;assert d!=0
    return (1 if d>0 else -1)*(1 if a>0 else -1)
def cmp(x,y):return sign(sub(x,y))
def between(z,lo,hi,strict=False):
    l,h=cmp(z,rat(lo)),cmp(z,rat(hi))
    return l>0 and h<0 if strict else l>=0 and h<=0

def interior(p):
    x,y=p
    return ((between(x,0,2,True) and between(y,-2,0,True)) or
            (between(x,1,3,True) and between(y,0,1,True)) or
            (between(x,0,2,True) and between(y,1,3,True)) or
            (y==rat(0) and between(x,1,2,True)) or
            (y==rat(1) and between(x,1,2,True)))

POLY=[(0,-2),(2,-2),(2,0),(3,0),(3,1),(2,1),(2,3),(0,3),(0,1),(1,1),(1,0),(0,0)]

def trace(source,target,v,limit):
    point=source;vx,vy=v;initial=(vx,vy);elapsed=rat(0);edges=[]
    assert interior(source) and interior(target)
    # All unfolded supporting mirror lines remain at integer coordinates.
    # A finite time horizon crosses at most |vx|T+|vy|T+4 such lines.
    bound=((abs(vx)+abs(vy))*limit).__floor__()+4
    for step in range(bound+1):
        hits=[]
        for i,(a,b) in enumerate(zip(POLY,POLY[1:]+POLY[:1])):
            axis=0 if a[0]==b[0] else 1
            speed=vx if axis==0 else vy
            if not speed:continue
            dt=scale(1/speed,sub(rat(a[axis]),point[axis]))
            if sign(dt)<=0:continue
            other=1-axis;coordinate=add(point[other],scale(vy if other==1 else vx,dt))
            lo,hi=sorted((a[other],b[other]))
            if between(coordinate,lo,hi):hits.append((dt,i,axis,coordinate in (rat(lo),rat(hi))))
        assert hits
        dt,i,axis,corner=hits[0]
        for event in hits[1:]:
            if cmp(event[0],dt)<0:dt,i,axis,corner=event
        assert sum(x[0]==dt for x in hits)==1 and not corner
        tt=scale(1/vy,sub(target[1],point[1])) if vy else scale(1/vx,sub(target[0],point[0]))
        reached=(sign(tt)>0 and cmp(tt,dt)<0 and add(point[0],scale(vx,tt))==target[0] and add(point[1],scale(vy,tt))==target[1])
        if reached:
            elapsed=add(elapsed,tt);assert cmp(elapsed,rat(limit))<=0
            middle=(add(point[0],scale(vx/2,tt)),add(point[1],scale(vy/2,tt)));assert interior(middle)
            return {'contacts':len(edges),'time':list(map(str,elapsed)),'final_velocity':[vx,vy],'edge_word':edges,'finite_integer_line_bound':bound}
        assert cmp(add(elapsed,dt),rat(limit))<0,'actual target absent at proved transport time'
        middle=(add(point[0],scale(vx/2,dt)),add(point[1],scale(vy/2,dt)));assert interior(middle)
        point=(add(point[0],scale(vx,dt)),add(point[1],scale(vy,dt)));elapsed=add(elapsed,dt)
        edges.append(i)
        if axis==0:vx=-vx
        else:vy=-vy
    raise AssertionError('derived integer-line crossing bound exceeded')

def twist_point(x,y,sx,sy,low,high,L,power):
    height=high-low;C=2*height;X=sx*x;j=X.__floor__()
    Z=y-low if sy==1 else C-(y-low)
    w=(Z+power*L*(X-j))%C
    assert w not in (0,height),'prescribed arithmetic control lies on mirror seam'
    return (x,low+w,sx,1) if w<height else (x,low+C-w,sx,-1)

def arithmetic():
    roundtrips=vertices=0;fixtures=[]
    for hm,hp in [(F(2),F(2)),(F(3,4),F(5,4)),(F(1,3),F(7,5))]:
        cs=[2*hm,2*hp,2*(hm+1+hp),F(2)];L=lcm(*(c.numerator for c in cs))
        assert all((F(L)/c).denominator==1 for c in cs) and L%2==0
        strips=[(0,-hm,F(0)),(0,F(1),1+hp),(1,-hm,1+hp),(2,F(0),F(1))]
        assert 2*sum(2*(hi-lo) for j,lo,hi in strips)==8*(hm+1+hp)
        for j,lo,hi in strips:
            C=2*(hi-lo)
            assert F(L)%C==0 and F(0)%C==0
            for sx in (1,-1):
                for sy in (1,-1):
                    original=(F(j)+F(1,3),lo+(hi-lo)*F(2,7),sx,sy)
                    for power in (1,-1,2,7):
                        moved=twist_point(*original,lo,hi,L,power)
                        restored=twist_point(*moved,lo,hi,L,-power)
                        assert restored==original;roundtrips+=1
        polygon=[(0,-hm),(2,-hm),(2,0),(3,0),(3,1),(2,1),(2,1+hp),(0,1+hp),(0,1),(1,1),(1,0),(0,0)]
        for x,y in polygon:
            for sx in (1,-1):
                for sy in (1,-1):assert (sx*x).denominator==1 if isinstance(sx*x,F) else isinstance(sx*x,int);vertices+=1
        fixtures.append({'hm':str(hm),'hp':str(hp),'L':L,'circumferences':list(map(str,cs))})
    # Prescribed simultaneous pigeonhole return for Q-independent1,s,t.
    s=K((0,F(1,2),0,0));t=K((0,0,F(1,2),0));N=20;seen={};return_record=None
    for j in range(N*N+1):
        phases=((5*j*s)%1,(5*j*t)%1);bucket=tuple((N*x).__floor__() for x in phases)
        if bucket in seen:
            k,previous=seen[bucket];ell=j-k
            ds,dt=(4*(phases[i]-previous[i]) for i in (0,1))
            assert -K(F(1,5))<ds<K(F(1,5)) and -K(F(1,5))<dt<K(F(1,5))
            aa=K(F(1,2))-ds;bb=1+dt
            assert 0<aa<2 and 0<bb<2 and aa.c[1]!=0 and aa.c[2]==0 and bb.c[1]==0 and bb.c[2]!=0
            return_record={'N':N,'ell':ell,'source_delta':str(ds),'target_delta':str(dt)};break
        seen[bucket]=(j,phases)
    assert return_record is not None
    primitive=0
    for p,q in [(1,1),(1,2),(2,1),(2,3),(3,2)]:
        for R in map(F,['1/3','1','3/2','2']):
            k=R.denominator;num=R.numerator;m=k*p+num;n=-k*q-num;r=-k*q
            assert gcd(gcd(m,abs(n)),abs(r))==1
            width=abs(m)+abs(n)
            assert width>=5 or (p,q,k,num,width)==(1,1,1,1,4)
            primitive+=1
    return roundtrips,vertices,fixtures,return_record,primitive

def main():
    names=['unequal-depth/vertical-twist.md','unequal-depth/twist-check.py','unequal-depth/twist-check.json','unequal-depth-independent/phase-lines-acceptance.json','arbitrary-endpoints-independent/acceptance.json']
    pins={r:hashlib.sha256((BASE/r).read_bytes()).hexdigest() for r in names}
    ar=arithmetic();s=(F(0),F(1,2));delta=40*K((0,F(1,2),0,0))-28
    assert 0<delta<K(F(1,2));rows=[];contactsum=0
    for eta,M,v in [(1,15,F(24)),(-1,13,F(102,5))]:
        targetx=s if eta==1 else (F(1),F(-1,2))
        a1=K(F(1,2))-delta;b1=1+delta;H=a1+1+b1
        assert H==K(F(5,2))
        ss=K((s[0],s[1],0,0));tt=K((targetx[0],targetx[1],0,0))
        assert (eta*tt+4*M-ss)/H==v
        assert 1<(ss+a1*v)%4<2 and 1<(ss+(a1+1)*v)%4<2
        source=(s,rat(F(-1,2)));target=(targetx,rat(2));velocity=(v,1-40*v)
        out=trace(source,target,velocity,F(5,2))
        assert out['time']==['5/2','0']
        assert out['final_velocity']==[eta*v,velocity[1]],'wrong unfolded target copy'
        reverse=trace(target,source,tuple(-x for x in out['final_velocity']),F(5,2))
        assert reverse['contacts']==out['contacts']
        contactsum+=2*out['contacts']
        rows.append({'eta':eta,'M':M,'velocity':list(map(str,velocity)),'contacts_forward':out['contacts'],'contacts_reverse':reverse['contacts'],'first_target_time':out['time'],'target_copy_parity':[eta,1],'edge_word_sha256':hashlib.sha256(json.dumps(out['edge_word']).encode()).hexdigest()})
    parent=json.loads((BASE/'unequal-depth/twist-check.json').read_text())
    for own,p in zip(rows,parent['records']):
        assert own['contacts_forward']==p['contacts'] and own['eta']==p['eta']
        assert own['edge_word_sha256']==hashlib.sha256(json.dumps(p['contact_edges']).encode()).hexdigest()
    for rel,h in pins.items():assert hashlib.sha256((BASE/rel).read_bytes()).hexdigest()==h,rel
    pins['unequal-depth-independent/twist-check.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out={'status':'INDEPENDENT_TWIST_CONTROLS_PASS','annulus_roundtrips':ar[0],'vertex_representations_on_fixed_cuts':ar[1],'circumference_fixtures':ar[2],'Q_independent_return':ar[3],'primitive_relation_controls':ar[4],'prescribed_actual_paths':4,'total_wall_contacts':contactsum,'source_sha256':pins,'records':rows,'limits':'Exact prescribed controls plus complete hand review, not proof by sampling. No peer imports/execution or direction discovery. General fully rational case remains open.'}
    (HERE/'twist-check.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','records')}))
    print(json.dumps(rows))
if __name__=='__main__':main()
