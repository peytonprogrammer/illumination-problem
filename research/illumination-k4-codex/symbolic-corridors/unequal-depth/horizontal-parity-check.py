"""Prescribed rational horizontal-shear controls; no discovery search."""
from pathlib import Path
from fractions import Fraction as F
from math import lcm,gcd
import json
B=Path(__file__).parent

def fold(x):
    r=x%4
    return r if r<=2 else 4-r

def rgcd(values):
    den=lcm(*(x.denominator for x in values))
    return F(gcd(*(int(x*den) for x in values)),den)

def trace(s,t,a,b,hm,hp,vx,vy):
    poly=[(0,-hm),(2,-hm),(2,0),(3,0),(3,1),(2,1),(2,1+hp),(0,1+hp),(0,1),(1,1),(1,0),(0,0)]
    P=(s,-a);target=(t,1+b);elapsed=F(0);contacts=[]
    for _ in range(10000):
        events=[]
        for i,(A,C) in enumerate(zip(poly,poly[1:]+poly[:1])):
            vert=A[0]==C[0];j=0 if vert else 1;v=(vx,vy)
            if not v[j]:continue
            tau=(A[j]-P[j])/v[j]
            if tau<=0:continue
            q=P[1-j]+v[1-j]*tau;lo,hi=sorted((A[1-j],C[1-j]))
            if lo<=q<=hi:events.append((tau,i,vert,q==lo or q==hi))
        assert events
        first=min(events);tau,i,vert,corner=first
        tt=(target[1]-P[1])/vy if vy else (target[0]-P[0])/vx
        if 0<tt<tau and (P[0]+vx*tt,P[1]+vy*tt)==target:
            assert elapsed+tt<=1
            return {'wall_contacts':len(contacts),'edges':contacts,'time':str(elapsed+tt)}
        assert not corner,('corner',P,first)
        assert sum(e[0]==tau for e in events)==1
        assert elapsed+tau<1,('target missing',elapsed,tau)
        P=(P[0]+vx*tau,P[1]+vy*tau);elapsed+=tau;contacts.append(i)
        if vert:vx=-vx
        else:vy=-vy
    raise AssertionError('finite prescribed trajectory guard exceeded')

def main():
    # The transformed endpoints share the open common column in all controls.
    fixtures=[('1/2','1/4','1/2','1/2','2','2'),
              ('1/3','2/3','1/2','3/2','2','2'),
              ('1/2','3/2','1/2','1','2','2'),
              ('3/2','1/2','1','1/2','2','2'),
              ('1/3','2/3','1/4','1/4','3/2','5/2'),
              ('2/5','3/7','1/6','1/6','2','3')]
    rows=[];fiber_checks=0
    for raw in fixtures:
        s,t,a,b,hm,hp=map(F,raw)
        delta=rgcd([hm,F(1),hp]);r0=2*a/delta;q0=2*b/delta
        n=lcm(r0.denominator,q0.denominator);L=4*n/delta
        r=n*r0;q=n*q0;assert r.denominator==q.denominator==1
        ss=fold(s-L*a);tt=fold(t+L*(1+b));assert 1<ss<2 and 1<tt<2
        for x,y,image in [(s,-a,ss),(t,1+b,tt)]:
            for sigma in (-1,1):
                for tau in (-1,1):
                    assert fold(x+sigma*tau*L*y)==image
                    fiber_checks+=1
        for height in (hm,F(1),hp):assert L*height%4==0
        derivative_x=1 if int(r)%2==0 else -1
        vy=1+a+b;vx=derivative_x*(tt-ss)-L*vy
        result=trace(s,t,a,b,hm,hp,vx,vy)
        rows.append({'fixture':raw,'delta':str(delta),'n':n,'L':str(L),
                     'source_image':str(ss),'target_image':str(tt),
                     'original_velocity':[str(vx),str(vy)],**result})
    # Arithmetic controls include an uncovered centered-maximal-exponent case.
    arithmetic=[]
    for aa,bb,s,t,expected in [('1/2','1/3','1/2','1/4',True),
          ('1/2','1/3','1','1/4',False),('1/3','1/2','1/2','1',False),
          ('1/3','1/3','1/2','1/4',False),('1/4','1/2','1/2','1',True),
          ('1/2','1/2','1','1/4',True)]:
        a,b,s,t=map(F,(aa,bb,s,t));r0=2*a;q0=2*b;n=lcm(r0.denominator,q0.denominator)
        actual=(s<1 and int(n*r0)%2==1) or (t<1 and int(n*q0)%2==1)
        assert actual==expected
        arithmetic.append({'a':aa,'b':bb,'s':str(s),'t':str(t),'criterion':actual})
    out={'status':'PRESCRIBED_CONTROLS_PASS','physical_paths':len(rows),
         'endpoint_fiber_checks':fiber_checks,'wall_contacts':sum(x['wall_contacts'] for x in rows),
         'rows':rows,'arithmetic':arithmetic,'scope':'Candidate hand criterion only; no full rational coverage.'}
    (B/'horizontal-parity-check.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))
if __name__=='__main__':main()
