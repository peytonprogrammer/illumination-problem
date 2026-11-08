"""Fixed arithmetic certificates only; no candidate or trajectory search."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
from math import gcd
import importlib.util
import json

C = F(comb(64,32),2**64)
assert C*C >= F(1,128)
assert 128*6**32 < 7**32
assert F(10,7)**2 > 2

# Prescribed positive root enclosures, verified by squaring rational bounds.
al, au = F(14142,10000), F(14143,10000)
bl, bu = F(17320,10000), F(17321,10000)
assert al*al < 2 < au*au and bl*bl < 3 < bu*bu
Hl, Hu = 1+al+bl, 1+au+bu
ql, qu = 49/Hu, 49/Hl
E1l, E1u = F(1,2)+ql*al, F(1,2)+qu*au
E2l, E2u = F(1,2)+ql*(1+al), F(1,2)+qu*(1+au)
assert 17 < E1l < E1u < 18
assert 29 < E2l < E2u < 30
assert F(1,2)+49 == F(3,2)+4*12

# All fold-line locations are prescribed by the certified portal intervals.
lower = list(range(2,17,2))
middle = list(range(19,30,2))
upper = list(range(30,49,2))
assert len(lower) == 8 and len(middle) == 6 and len(upper) == 10
assert all(F(1,2) < x < E1l for x in lower)
assert all(E1u < x < E2l for x in middle)
assert all(E2u < x < F(99,2) for x in upper)

# Reuse only our frozen packet's pure geometry helpers; importing it does
# not execute its __main__ writer. This is not an independent review.
spec = importlib.util.spec_from_file_location('own_corridor_helpers',Path(__file__).parents[1]/'check.py')
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)
fold, sub, cross, inside = helpers.fold, helpers.sub, helpers.cross, helpers.inside


def equal_pair(p, den, horizontal):
    d, g = F(1), F(1)
    alpha = F(p,den)
    a = alpha/(1-2*alpha)
    s = horizontal
    if den == 4 and s == d:
        control = helpers.controls(d,g,a)
        return {'p':p,'q':den,'s':str(s),'mechanism':'three middle contacts',
                'contacts':control['reflections'],'passed':True}
    if den >= 5:
        v = (s+2*alpha*(d-s))/(4*d)
        z = den*(F(1,4)-v)
        j = z.numerator//z.denominator+1
        M = (j*pow(p,-1,den)) % den
        assert F(1,4) < (v+M*alpha)%1 < F(1,2)
    elif den == 3:
        M = 0 if s > d else 1
    else:
        assert den == 4
        M = 0 if s > d else 1
    H = 2*a+g
    L = 2*d-s+4*d*M
    slope = (L-s)/H
    assert slope != 0
    E = s+slope*a
    E2 = s+slope*(a+g)
    residue = E % (4*d)
    assert d < residue < 3*d and residue != 2*d
    shift = d if residue < 2*d else 3*d
    fm = lambda X:d+fold(X-shift,2*d)
    fu = lambda X:fold(X-2*d,2*d)
    assert fold(E,2*d) == fm(E) and d < fm(E) < 2*d
    assert fm(E2) == fu(E2) and d < fm(E2) < 2*d
    assert fu(L) == s
    def derivative(X, offset):
        u = (X-offset) % (4*d)
        assert u not in (0,2*d)
        return 1 if u < 2*d else -1
    assert derivative(E,0) == derivative(E,shift)
    assert derivative(E2,shift) == derivative(E2,2*d)
    events = []
    for ya,yb,offset,ff in [(-a,F(0),F(0),lambda X:fold(X,2*d)),
                            (F(0),g,shift,fm),(g,g+a,2*d,fu)]:
        xa,xb = s+slope*(ya+a),s+slope*(yb+a)
        lo,hi = sorted((xa,xb))
        jlo = ((lo-offset)/(2*d)).__floor__()-1
        jhi = ((hi-offset)/(2*d)).__floor__()+2
        for j in range(jlo,jhi+1):
            X = offset+2*d*j
            if lo < X < hi:
                y = -a+(X-s)/slope
                assert ya < y < yb
                events.append((ff(X),y))
    events.sort(key=lambda point:point[1])
    path = [(s,-a)]+events+[(s,g+a)]
    hm,hp = a+1,a+2
    poly = [(0,-hm),(2*d,-hm),(2*d,0),(3*d,0),(3*d,g),
            (2*d,g),(2*d,g+hp),(0,g+hp),(0,g),(d,g),(d,0),(0,0)]
    poly = [tuple(map(F,P)) for P in poly]
    edges = list(zip(poly,poly[1:]+poly[:1]))
    assert inside(path[0],poly) and inside(path[-1],poly)
    for i,(A,B) in enumerate(zip(path,path[1:])):
        v = sub(B,A)
        assert v != (0,0) and B[1]>A[1]
        assert inside(((A[0]+B[0])/2,(A[1]+B[1])/2),poly)
        contacts = []
        for C,D in edges:
            w = sub(D,C)
            divisor = cross(v,w)
            if not divisor:
                assert cross(sub(C,A),v) != 0
                continue
            t = cross(sub(C,A),w)/divisor
            u = cross(sub(C,A),v)/divisor
            if 0 < t <= 1 and 0 <= u <= 1:
                assert t == 1 and 0 < u < 1
                contacts.append((C,D))
        if i == len(path)-2:
            assert not contacts
        else:
            assert len(contacts) == 1
            C,D = contacts[0]
            assert C[0] == D[0], 'only vertical-wall contacts in this branch'
            reflected = (-v[0],v[1])
            outgoing = sub(path[i+2],B)
            assert cross(reflected,outgoing) == 0
            assert sum(x*y for x,y in zip(reflected,outgoing)) > 0
    return {'p':p,'q':den,'s':str(s),'M':M,'contacts':len(events),'passed':True}


equal_controls = [equal_pair(p,q,s)
                  for q in (3,4,5,7,8,11)
                  for p in range(1,(q+1)//2) if gcd(p,q) == 1
                  for s in map(F,['1/100','1/2','1','3/2','199/100'])]

result = {
    'status':'PASS',
    'purpose':'fixed arithmetic certificates; no discovery search',
    'finite_frequency_box':[-32,32],
    'constant_coefficient_squared_ge':'1/128',
    'threshold_bound_lt':'1/128',
    'integer_inequality_128_times_6_pow_32_lt_7_pow_32':True,
    'fixed_control':{'d':'1','g':'1','a':'sqrt(2)','b':'sqrt(3)',
                     's':'1/2','t':'3/2','M':12,
                     'first_portal_interval':list(map(str,[E1l,E1u])),
                     'second_portal_interval':list(map(str,[E2l,E2u])),
                     'lower_contacts':8,'middle_contacts':6,'upper_contacts':10,
                     'total_contacts':24},
    'limits':'Does not verify the full proof independently or close resonance cases.'
}
result['equal_pair_prescribed_controls'] = {
    'cases':len(equal_controls),
    'wall_contacts':sum(c['contacts'] for c in equal_controls),
    'maximum_contacts':max(c['contacts'] for c in equal_controls),
    'records':equal_controls
}
Path(__file__).with_name('check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k != 'equal_pair_prescribed_controls'}))
print(json.dumps({k:v for k,v in result['equal_pair_prescribed_controls'].items() if k != 'records'}))
