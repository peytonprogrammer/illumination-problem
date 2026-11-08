"""Exact controls of prescribed formulas. No direction or room discovery."""
from fractions import Fraction as F
from pathlib import Path
import json


def fold(x, w):
    x %= 2 * w
    return x if x <= w else 2 * w - x


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def inside(p, polygon):
    x, y = p
    hits = 0
    for a, b in zip(polygon, polygon[1:] + polygon[:1]):
        if cross(sub(p, a), sub(b, a)) == 0:
            if min(a[0], b[0]) <= x <= max(a[0], b[0]) and min(a[1], b[1]) <= y <= max(a[1], b[1]):
                return False
        if (a[1] > y) != (b[1] > y):
            ix = a[0] + (y-a[1]) * (b[0]-a[0]) / (b[1]-a[1])
            hits += ix > x
    return hits % 2 == 1


def controls(d, g, a):
    hm, hp = a + g, a + 2*g
    poly = [(0,-hm),(2*d,-hm),(2*d,0),(3*d,0),(3*d,g),
            (2*d,g),(2*d,g+hp),(0,g+hp),(0,g),(d,g),(d,0),(0,0)]
    poly = [tuple(map(F,p)) for p in poly]
    source, target = (d,-a), (d,g+a)
    assert inside(source,poly) and inside(target,poly)
    if a == 3*g/2:
        m = None
        bounces = [(9*d/4,g),(11*d/4,0),(3*d,g/2),
                   (11*d/4,g),(9*d/4,0)]
    else:
        z = (a+3*g/2)/(3*g)
        m = 1 if z < 1 else z.numerator // z.denominator + 1
        assert z < m < 2*z
        q = 2*m*d/(a+3*g/2)
        X = (3-2*m)*d
        e, p = 3*d-3*q*g/2, 3*d-q*g/2
        assert d < e < 2*d and 2*d < p < 3*d
        assert X+q*a == e and fold(X,2*d) == d
        lower = [(fold(2*d*j,2*d),-a+(2*d*j-X)/q)
                 for j in range(-m,2) if X < 2*d*j < e]
        assert len(lower) == m-1
        upper = [(x,g-y) for x,y in reversed(lower)]
        bounces = lower + [(p,g),(3*d,g/2),(p,0)] + upper
        assert len(bounces) == 2*m+1
    path = [source] + bounces + [target]
    edges = list(zip(poly,poly[1:]+poly[:1]))
    for i, (p0,p1) in enumerate(zip(path,path[1:])):
        v = sub(p1,p0)
        assert v != (0,0)
        assert inside(((p0[0]+p1[0])/2,(p0[1]+p1[1])/2),poly)
        contacts = []
        for e0,e1 in edges:
            w = sub(e1,e0)
            den = cross(v,w)
            if den == 0:
                assert cross(sub(e0,p0),v) != 0, 'unexpected wall glide'
                continue
            t = cross(sub(e0,p0),w)/den
            u = cross(sub(e0,p0),v)/den
            if 0 < t <= 1 and 0 <= u <= 1:
                assert t == 1 and 0 < u < 1, 'earlier wall or corner'
                contacts.append((e0,e1))
        if i == len(path)-2:
            assert not contacts
        else:
            assert len(contacts) == 1
            e0,e1 = contacts[0]
            reflected = (-v[0],v[1]) if e0[0] == e1[0] else (v[0],-v[1])
            outgoing = sub(path[i+2],p1)
            assert cross(reflected,outgoing) == 0
            assert sum(x*y for x,y in zip(reflected,outgoing)) > 0
        # Actual target must not occur on an earlier segment.
        if i < len(path)-2 and cross(sub(target,p0),v) == 0:
            component = 0 if v[0] else 1
            t = (target[component]-p0[component])/v[component]
            assert not 0 < t <= 1
    return {"d":str(d),"g":str(g),"a_over_g":str(a/g),
            "m":m,"reflections":len(bounces),"passed":True}


if __name__ == '__main__':
    ratios = list(map(F,['1/100','1/2','149/100','3/2','151/100','3','10','100']))
    cases = [controls(d,g,r*g)
             for d in map(F,['1/3','1','7/2'])
             for g in map(F,['2/5','1','3']) for r in ratios]
    # Algebraic controls of the hand monotone obstruction, all residue classes.
    residues = []
    for r in range(8):
        entry = fold(1+F(r,2),F(2))
        allowed = 1 < entry < 2
        assert allowed == (r in (1,3))
        if allowed:
            v = r if r == 1 else -r
            assert v % 4 == 1
            assert 1+fold(F(1,2)+v,F(2)) == F(5,2)
        residues.append({"r_mod_8":r,"first_portal_allowed":allowed})
    result = {"status":"PASS","purpose":"prescribed-formula controls only",
              "case_count":len(cases),"wall_contacts_checked":sum(c['reflections'] for c in cases),
              "maximum_control_reflections":max(c['reflections'] for c in cases),
              "cases":cases,"monotone_residue_controls":residues,
              "limits":"Finite rational controls do not prove the arbitrary-real theorem or independent review."}
    dest = Path(__file__).with_name('check.json')
    dest.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('cases','monotone_residue_controls')}))
