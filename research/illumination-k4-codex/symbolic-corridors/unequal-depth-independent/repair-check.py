"""Independent actual-wall checks of the prescribed midpoint repair."""
from fractions import Fraction as F
from pathlib import Path
from importlib.util import spec_from_file_location,module_from_spec
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
spec=spec_from_file_location('own_frozen_geometry',BASE/'arbitrary-endpoints-independent/check.py')
G=module_from_spec(spec);spec.loader.exec_module(G)

def check(d,g,a,lo,up,scalar=F):
    b=a+g;hm=a+lo;hp=b+up
    R=(2*d,hp-a);C=(2*d-d*b/hp,g+hp)
    P=[(d,-a),R,C,(d,g+b)]
    assert g<R[1]<g+hp and d<C[0]<2*d
    e1=d+d*a/hp;e2=d+d*b/hp
    assert d<e1<2*d and d<e2<2*d
    assert G.sub(R,P[0])==(d,hp)
    assert G.sub(C,R)==(-d*b/hp,b)
    assert G.sub(P[-1],C)==(-d*(hp-b)/hp,-(hp-b))
    assert G.verify(P,d,g,a,b,d,d,hm,hp,scalar)==2
    Q=[(x,g-y) for x,y in P[::-1]]
    assert G.verify(Q,d,g,b,a,d,d,hp,hm,scalar)==2
    return {'d':str(d),'g':str(g),'a':str(a),'lower_clearance':str(lo),'upper_clearance':str(up),'actual_paths':2,'contacts':4}

def main():
    names=['unequal-depth/midpoint-repair.md','unequal-depth/midpoint-check.py','unequal-depth/midpoint-check.json','arbitrary-endpoints-independent/check.py','unequal-depth-independent/midpoint-review.md']
    pins={n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in names}
    rows=[check(d,g,a,lo,up) for d,g in [(F(1),F(1)),(F(2,7),F(11,3)),(F(9),F(1,11))] for a in [F(1,10000),F(1,2),F(1),F(37)] for lo in [F(1,10**8),F(3)] for up in [F(1,10**8),F(1,3),F(100)]]
    K=G.K
    rows.append(check(K((0,1,0,0)),K((0,0,1,0)),K((0,0,0,1)),K(F(1,10**8)),K(F(1,10**8)),K))
    for n,h in pins.items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
    pins['unequal-depth-independent/repair-check.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out={'status':'PASS','actual_paths':2*len(rows),'wall_contacts':4*len(rows),'exact_irrational_paths':2,'smallest_prescribed_cap_clearance':'1/100000000','source_sha256':pins,'records':rows,'limits':'Prescribed formula checks only. General positive-real inequalities hand-reviewed. No peer execution, discovery or darkness claim.'}
    (HERE/'repair-check.json').write_text(json.dumps(out,indent=2)+'\n')
    print({k:v for k,v in out.items() if k not in ('records','source_sha256')})
if __name__=='__main__':main()
