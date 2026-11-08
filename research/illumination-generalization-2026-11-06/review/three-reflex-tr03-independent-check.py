"""Independent exact prescribed TR03 audit. No author code execution or search."""
from fractions import Fraction as Q
from pathlib import Path
from math import floor, ceil
import ast, hashlib, json

HERE = Path(__file__).parent
REQUEST = HERE.parent / 'construction/three-reflex-review-request-03.json'
request = json.loads(REQUEST.read_text())

def pins():
    rows = []
    for p in request['source_pins']:
        actual = hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()
        assert actual == p['sha256'], p
        rows.append(dict(p, actual=actual, passed=True))
    return rows

before = pins()
# Reuse only our earlier independent finite geometric predicates.
tree = ast.parse((HERE / 'resumed-exact-check.py').read_text())
names = {'vec','det','dot','edges','on','location','intersect','simple','path_check'}
scope = {'Q': Q}
exec(compile(ast.Module(body=[f for f in tree.body if isinstance(f,ast.FunctionDef)
    and f.name in names],type_ignores=[]),'<independent-geometric-predicates>','exec'),scope)

def fold(x, w):
    # Different algebraic expression for distance to 2wZ.
    return abs(x - 2*w*floor((x+w)/(2*w)))

def partition_roots(offset, coefficient, width, lo, hi):
    """Pull back odd width multiples to the requested slope interval."""
    ends = sorted((offset+coefficient*lo, offset+coefficient*hi))
    out = []
    for j in range(floor((ends[0]/width-1)/2)-1,
                   ceil((ends[1]/width-1)/2)+2):
        root = ((2*j+1)*width-offset)/coefficient
        if lo < root < hi:
            out.append(root)
    return out

def verify(label, geometry, S, T, prescribed=None):
    a,l,w,A,b,c,h,H = map(Q,geometry)
    s,u = map(Q,S); t,v = map(Q,T)
    assert 0<a<l<w<A and 0<b<c<h<H
    poly = [(a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b)]
    scope['simple'](poly)
    assert scope['location'](poly,(s,u)) == scope['location'](poly,(t,v)) == 1
    assert l<t<A and 0<v<c
    lower = u<h
    assert (0<s<a and b<u<h) if lower else (h<=u<H and 0<s<=w)
    R,B = A-w,A-l
    L = R/(2*c)
    Ns,Nr = ceil(L*h/(2*a))+1,ceil(L*h/(2*R))+1
    delta = L/(Ns+Nr+1)
    bound = c+2*A/delta
    z,d,e,D = A-t,c-v,h-v,2*H-u-v
    component = None
    if prescribed is None:
        assert H>=bound
        origin = max(Q(0),(z-R)/d)
        lo,hi = origin+L/2,origin+3*L/2
        assert 0<lo<hi<(z+R)/d and lo>=(z-R)/d
        source_bad = partition_roots(s,h-u,a,lo,hi) if lower else []
        right_bad = partition_roots(z,-e,R,lo,hi)
        assert len(source_bad)<=Ns and len(right_bad)<=Nr
        cuts = [lo]+sorted(set(source_bad+right_bad))+[hi]
        intervals = list(zip(cuts,cuts[1:]))
        # Select the LAST maximal gap to avoid inheriting the author selection.
        length = max(y-x for x,y in intervals)
        alpha,beta = [I for I in intervals if I[1]-I[0]==length][-1]
        assert beta-alpha>=delta and 2*A/D<delta
        probe = (2*alpha+beta)/3
        n = floor((s+probe*(h-u)+a)/(2*a)) if lower else 0
        k = -floor((z-probe*e+R)/(2*R))
        C = 2*n*a+A+2*k*R+z-s
        # Take the LAST root strictly below beta, independent of author's first-root choice.
        m = ceil((D*beta-C)/(2*A))-1
        tau = (C+2*m*A)/D
        assert alpha<tau<beta
        component = [alpha,beta]
    else:
        tau,n,k,m = prescribed
        tau = Q(tau)
    z0 = s+tau*(h-u)-2*n*a if lower else None
    z1,z2 = z-tau*e+2*k*R,z-tau*d
    assert tau>0 and abs(z1)<R and abs(z2)<R
    assert tau*D == 2*n*a+(2*m+1)*A+2*k*R+z-s
    if lower: assert abs(z0)<a
    eta1,eta2,end = 2*H-h,2*H-c,2*H-v
    # Each record is (lo,hi,width,affine constant,mirror x about A).
    bands = []
    if lower:
        bands.append((u,h,a,s-tau*u,False))
        bands.append((h,eta1,A,z0-tau*h,False))
    else:
        bands.append((u,eta1,A,s-tau*u,False))
    bands.extend([(eta1,eta2,R,z1-tau*eta1,True),
                  (eta2,end,B,z2-tau*eta2,True)])
    def value(band,eta):
        x = fold(tau*eta+band[3],band[2])
        return A-x if band[4] else x
    for left,right in zip(bands,bands[1:]):
        assert left[1]==right[0]
        assert value(left,left[1])==value(right,right[0])
    cap = bands[1] if lower else bands[0]
    singular = (tau*H+cap[3]) % A == 0
    start = 2*H-u if singular else u
    if singular:
        assert not lower and u>h and H<start<eta1
        assert value(cap,start)==s
    events = {start,end}
    if start<H<end: events.add(H)
    for lo,hi,width,offset,mirror in bands:
        left,right = max(start,lo),min(end,hi)
        if left>=right: continue
        events.update((left,right))
        for j in range(floor((tau*left+offset)/width)-1,
                       ceil((tau*right+offset)/width)+2):
            eta = (j*width-offset)/tau
            if left<eta<right: events.add(eta)
    def point(eta):
        candidates = [value(B,eta) for B in bands if B[0]<=eta<=B[1]]
        assert candidates and len(set(candidates))==1
        return candidates[0], min(eta,2*H-eta)
    times = sorted(events)
    path = [point(eta) for eta in times]
    assert path[0]==(s,u) and path[-1]==(t,v)
    geometric = scope['path_check'](poly,path)
    velocities = []
    for i,(p,q) in enumerate(zip(path,path[1:])):
        dt = times[i+1]-times[i]
        velocity = ((q[0]-p[0])/dt,(q[1]-p[1])/dt)
        assert abs(velocity[0])==tau and abs(velocity[1])==1
        velocities.append(velocity)
        if i<len(path)-2:
            cross = (t-p[0])/velocity[0]
            assert not (0<cross<=dt and p[1]+cross*velocity[1]==v)
    for i,p in enumerate(path[1:-1],1):
        walls = [(x,y) for x,y in scope['edges'](poly) if scope['on'](x,y,p)]
        incoming = velocities[i-1]
        expected = incoming
        if walls:
            x,y = walls[0]
            expected = (-incoming[0],incoming[1]) if x[0]==y[0] else (incoming[0],-incoming[1])
        assert velocities[i]==expected
    return dict(label=label,geometry=geometry,source=S,target=T,slope=tau,indices=[n,k,m],
        delta=delta,height_bound=bound,at_height_equality=H==bound,component=component,
        singular_roof_discarded=singular,actual_elapsed=end-start,path=path,**geometric)

G = (4,12,20,28,4,8,20,680)
fixtures = [
    ('left',G,(2,6),(14,2),None),
    ('upper',G,(10,24),(14,2),None),
    ('cut',G,(20,24),(14,2),None),
    ('seam-h',G,(2,20),(14,2),None),
    ('near-roof-c',G,(20,Q(6799,10)),(14,Q(79,10)),None),
    ('singular-suffix',G,(20,664),(25,2),(Q(1,2),0,0,6)),
    ('thin-real',(Q(2,3),Q(5,3),Q(7,3),Q(11,3),Q(1,5),Q(2,5),Q(3,5),Q(112,5)),(Q(1,3),Q(2,5)),(2,Q(1,5)),None),
    ('short-explicit-only',(4,12,20,28,4,8,20,28),(2,6),(14,2),(Q(7,6),2,0,0)),
    ('near-left-floor-target-side',G,(Q(1,101),Q(405,101)),(Q(1213,101),Q(1,101)),None),
    ('near-roof-outer-target',G,(Q(2019,101),Q(68679,101)),(Q(2827,101),Q(807,101)),None),
]
rows = [verify(*fixture) for fixture in fixtures]
after = pins()
out = dict(status='PASS_INDEPENDENT_TR03_PRESCRIBED_REPLAY',rows=rows,
    source_pins_before=before,source_pins_after=after,
    request_sha256=hashlib.sha256(REQUEST.read_bytes()).hexdigest(),
    reflections=sum(r['reflections'] for r in rows),
    wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),
    search_used=False,author_code_executed=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('rows','source_pins_before','source_pins_after')}))
