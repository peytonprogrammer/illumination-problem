"""Prescribed exact Q(sqrt2) original-room transport controls; no ray search."""
from fractions import Fraction as F
from dataclasses import dataclass
from pathlib import Path
import json
B=Path(__file__).parent

@dataclass(frozen=True)
class Q2:
    a:F=F(0)
    b:F=F(0)
    def __post_init__(self):
        object.__setattr__(self,'a',F(self.a));object.__setattr__(self,'b',F(self.b))
    def __add__(self,y):
        y=cv(y);return Q2(self.a+y.a,self.b+y.b)
    __radd__=__add__
    def __neg__(self):return Q2(-self.a,-self.b)
    def __sub__(self,y):return self+-cv(y)
    def __rsub__(self,y):return cv(y)+-self
    def __mul__(self,y):
        y=cv(y);return Q2(self.a*y.a+2*self.b*y.b,self.a*y.b+self.b*y.a)
    __rmul__=__mul__
    def __truediv__(self,y):
        y=cv(y);den=y.a*y.a-2*y.b*y.b;assert den
        return self*Q2(y.a/den,-y.b/den)
    def sign(self):
        if not self.b:return (self.a>0)-(self.a<0)
        if not self.a:return (self.b>0)-(self.b<0)
        if self.a>0 and self.b>0:return 1
        if self.a<0 and self.b<0:return -1
        z=self.a*self.a-2*self.b*self.b;assert z
        return (1 if z>0 else -1)*(1 if self.a>0 else -1)
    def __lt__(self,y):return (self-cv(y)).sign()<0
    def __le__(self,y):return (self-cv(y)).sign()<=0
    def __gt__(self,y):return (self-cv(y)).sign()>0
    def __ge__(self,y):return (self-cv(y)).sign()>=0
    def __eq__(self,y):
        try:y=cv(y)
        except (ValueError,TypeError):return False
        return self.a==y.a and self.b==y.b
    def rec(self):return [str(self.a),str(self.b)]

def cv(x):return x if isinstance(x,Q2) else Q2(F(x),F(0))
def mod4(x):
    while x<0:x=x+4
    while x>=4:x=x-4
    return x

def trace(source,target,velocity,limit):
    poly=[(0,-2),(2,-2),(2,0),(3,0),(3,1),(2,1),(2,3),(0,3),(0,1),(1,1),(1,0),(0,0)]
    point=tuple(map(cv,source));target=tuple(map(cv,target))
    vx,vy=map(F,velocity);elapsed=cv(0);contacts=[]
    for step in range(20000):
        # Every edge is checked; no wall-word guess or numeric tolerance.
        candidates=[]
        for i,(A,C) in enumerate(zip(poly,poly[1:]+poly[:1])):
            vertical=A[0]==C[0]
            if vertical:
                if not vx:continue
                tau=(A[0]-point[0])/vx
                if tau<=0:continue
                z=point[1]+vy*tau;low,high=sorted((A[1],C[1]))
            else:
                if not vy:continue
                tau=(A[1]-point[1])/vy
                if tau<=0:continue
                z=point[0]+vx*tau;low,high=sorted((A[0],C[0]))
            if low<=z<=high:candidates.append((tau,i,vertical,z==low or z==high))
        assert candidates
        first=min(candidates,key=lambda x:x[0]);tau,i,vertical,corner=first
        if vy:
            tt=(target[1]-point[1])/vy
            if 0<tt<tau and point[0]+vx*tt==target[0]:
                assert elapsed+tt<=limit
                return {'contacts':len(contacts),'first_target_time':(elapsed+tt).rec(),
                        'contact_edges':contacts,'target_reached':True}
        assert not corner,'prescribed transport unexpectedly reaches a corner'
        assert sum(x[0]==tau for x in candidates)==1
        assert elapsed+tau<limit,'target missing by the proved affine-image parameter time'
        point=(point[0]+vx*tau,point[1]+vy*tau);elapsed+=tau
        contacts.append(i)
        if vertical:vx=-vx
        else:vy=-vy
    raise AssertionError('coding guard; no proof of finite trajectory accepted')

def main():
    s=Q2(0,F(1,2));delta=40*s-28
    assert 0<delta<F(1,2)
    a1=F(1,2)-delta;b1=1+delta;assert a1+b1+1==F(5,2)
    out=[]
    for eta,M,v in [(1,15,F(24)),(-1,13,F(102,5))]:
        t=s if eta==1 else 1-s
        assert 0<s<1 and 0<t<1
        Ltarget=eta*t+4*M
        assert (Ltarget-s)/F(5,2)==v
        E1=s+a1*v;E2=s+(a1+1)*v
        assert 1<mod4(E1)<2 and 1<mod4(E2)<2
        res=trace((s,F(-1,2)),(t,F(2)),(v,1-40*v),F(5,2))
        out.append({'eta':eta,'twist_power':2,'L_twist':20,'M':M,
                    'original_velocity':[str(v),str(1-40*v)],'source_x':s.rec(),'target_x':t.rec(),
                    'transformed_a':a1.rec(),'transformed_b':b1.rec(),
                    'portal_residues':[mod4(E1).rec(),mod4(E2).rec()],**res})
    result={'status':'PASS','actual_paths':len(out),'total_contacts':sum(x['contacts'] for x in out),
            'arithmetic':'Exact rational coefficients of1,sqrt2; signs by integer-square comparisons',
            'method':'Two explicitly prescribed affine-transport directions; full actual-polygon nearest-wall tracing',
            'scope':'Controls support hand surface map and selected ending-copy argument; not full theorem by samples',
            'independent_review':False,'records':out}
    (B/'twist-check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}))
    print(json.dumps([{k:v for k,v in r.items() if k!='contact_edges'} for r in out]))

if __name__=='__main__':main()
