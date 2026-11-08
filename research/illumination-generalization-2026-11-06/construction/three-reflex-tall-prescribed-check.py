"""Exact prescribed TR03 formula replay; no room/direction/word discovery."""
from fractions import Fraction as F
from pathlib import Path
from math import ceil, floor
import json


def wave(x, width):
    r = x % (2 * width)
    return min(r, 2 * width - r)


def phases(geometry, source, target, forced=None):
    a, ell, w, A, b, c, h, H = map(F, geometry)
    s, u = map(F, source)
    t, v = map(F, target)
    assert 0 < a < ell < w < A and 0 < b < c < h < H
    assert ell < t < A and 0 < v < c
    lower = u < h
    assert (0 < s < a and b < u < h) if lower else (h <= u < H and 0 < s <= w)
    R, B = A - w, A - ell
    L = R / (2 * c)
    Ns = ceil(L * h / (2 * a)) + 1
    Nr = ceil(L * h / (2 * R)) + 1
    delta = L / (Ns + Nr + 1)
    z, d, e = A - t, c - v, h - v
    D = 2 * H - u - v
    interval = None
    if forced is None:
        assert H >= c + 2 * A / delta
        left = max(F(0), (z - R) / d)
        lo, hi = left + L / 2, left + 3 * L / 2
        assert 0 < lo < hi < (z + R) / d
        bad = set()
        if lower:
            d0 = h - u
            for n in range(floor((s + d0 * lo - a) / (2 * a)) - 1,
                           ceil((s + d0 * hi - a) / (2 * a)) + 2):
                q = ((2 * n + 1) * a - s) / d0
                if lo < q < hi:
                    bad.add(q)
        source_count = len(bad)
        right_bad = set()
        for j in range(floor((z - e * hi - R) / (2 * R)) - 1,
                       ceil((z - e * lo - R) / (2 * R)) + 2):
            q = (z - (2 * j + 1) * R) / e
            if lo < q < hi:
                right_bad.add(q)
        assert source_count <= Ns and len(right_bad) <= Nr
        bad.update(right_bad)
        endpoints = [lo] + sorted(bad) + [hi]
        alpha, beta = max(zip(endpoints, endpoints[1:]), key=lambda x: x[1] - x[0])
        assert beta - alpha >= delta
        mid = (alpha + beta) / 2
        n = floor((s + mid * (h - u) + a) / (2 * a)) if lower else 0
        k = -floor((z - mid * e + R) / (2 * R))
        C = (2 * n * a if lower else 0) + A + 2 * k * R + z - s
        m = floor((D * alpha - C) / (2 * A)) + 1
        tau = (C + 2 * m * A) / D
        assert alpha < tau < beta and 2 * A / D < delta
        interval = [alpha, beta]
    else:
        tau, n, k, m = map(F, forced)
        assert all(q.denominator == 1 for q in [n, k, m])
        n, k, m = map(int, [n, k, m])
    z1, z2 = z - tau * e + 2 * k * R, z - tau * d
    assert abs(z1) < R and abs(z2) < R and tau > 0
    assert tau * D == (2 * n * a if lower else 0) + (2 * m + 1) * A + 2 * k * R + z - s
    bands = []
    eta1, eta2, end = 2 * H - h, 2 * H - c, 2 * H - v
    if lower:
        z0 = s + tau * (h - u) - 2 * n * a
        assert abs(z0) < a
        assert z0 + tau * 2 * (H - h) - (2 * m + 1) * A == z1
        bands += [(u, h, a, s, False), (h, eta1, A, z0, False)]
        roof_phase = z0 + tau * (H - h)
        assert roof_phase % A != 0
    else:
        assert s + tau * (eta1 - u) - (2 * m + 1) * A == z1
        bands += [(u, eta1, A, s, False)]
        roof_phase = s + tau * (H - u)
    bands += [(eta1, eta2, R, z1, True), (eta2, end, B, z2, True)]
    assert z1 + tau * (h - c) - 2 * k * R == z2
    assert z2 + tau * d == z
    singular = roof_phase % A == 0
    start = 2 * H - u if singular else u
    if singular:
        assert not lower and u > h and H < start < eta1
    events = {start, end}
    if start < H < end:
        events.add(H)
    for begin, stop, width, phase, mirrored in bands:
        if start <= begin <= end:
            events.add(begin)
        if start <= stop <= end:
            events.add(stop)
        for j in range(floor(phase / width) - 1,
                       ceil((phase + tau * (stop - begin)) / width) + 2):
            eta = begin + (j * width - phase) / tau
            if max(start, begin) < eta < min(end, stop):
                events.add(eta)
    def point(eta):
        for begin, stop, width, phase, mirrored in bands:
            if begin <= eta <= stop:
                x = wave(phase + tau * (eta - begin), width)
                return (A - x if mirrored else x, eta if eta <= H else 2 * H - eta)
        raise AssertionError(eta)
    timed = [(eta, point(eta)) for eta in sorted(events)]
    assert timed[0][1] == (s, u) and timed[-1][1] == (t, v)
    polygon = [(a,b),(a,h),(w,h),(w,c),(ell,c),(ell,0),(A,0),(A,H),(0,H),(0,b)]
    refs, checks = validate(polygon, timed, (s, u), (t, v))
    return {'geometry': list(map(F, geometry)), 'source':[s,u], 'target':[t,v],
            'tau': tau, 'n': n, 'k': k, 'm': m, 'delta':delta,
            'selected_component':interval, 'singular_roof_discarded':singular,
            'legal_start_eta':start, 'reflections':refs, 'finite_wall_checks':checks,
            'status':'PASS'}


def validate(poly, timed, source, target):
    walls = list(zip(poly, poly[1:] + poly[:1]))
    def on(p, a, b):
        return ((b[0]-a[0])*(p[1]-a[1]) == (b[1]-a[1])*(p[0]-a[0])
                and all(min(a[i], b[i]) <= p[i] <= max(a[i], b[i]) for i in [0,1]))
    def inside(p):
        if any(on(p,a,b) for a,b in walls):
            return False
        x,y=p
        return sum((a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]
                   for a,b in walls if a[1]!=b[1]) % 2 == 1
    assert inside(source) and inside(target)
    velocities=[]
    for i,((ea,p),(eb,q)) in enumerate(zip(timed,timed[1:])):
        dx,dy=q[0]-p[0],q[1]-p[1]
        assert eb>ea and dx and dy
        velocities.append((dx/(eb-ea),dy/(eb-ea)))
        assert inside(((p[0]+q[0])/2,(p[1]+q[1])/2))
        for a,b in walls:
            theta=(a[0]-p[0])/dx if a[0]==b[0] else (a[1]-p[1])/dy
            hit=(p[0]+theta*dx,p[1]+theta*dy)
            assert not (0<theta<1 and on(hit,a,b)), (i,hit,a,b)
        if i < len(timed)-2:
            theta=(target[0]-p[0])/dx
            assert not (0<theta<=1 and p[1]+theta*dy==target[1])
    refs=0
    for i,(_,p) in enumerate(timed[1:-1],1):
        assert p not in poly
        contacts=[(a,b) for a,b in walls if on(p,a,b)]
        vin,vout=velocities[i-1],velocities[i]
        if contacts:
            assert len(contacts)==1
            a,b=contacts[0]
            expected=(-vin[0],vin[1]) if a[0]==b[0] else (vin[0],-vin[1])
            assert vout==expected,(p,vin,vout)
            refs+=1
        else:
            assert vin==vout,(p,vin,vout)
    return refs, len(walls)*(len(timed)-1)


if __name__ == '__main__':
    G=(4,12,20,28,4,8,20,680)
    fixtures=[('left',G,(2,6),(14,2),None),
              ('upper',G,(10,24),(14,2),None),
              ('artificial-cut',G,(20,24),(14,2),None),
              ('h-seam',G,(2,20),(14,2),None),
              ('near-roof-and-c',G,(20,F(6799,10)),(14,F(79,10)),None),
              ('discarded-roof-corner',G,(20,664),(25,2),(F(1,2),0,0,6)),
              ('thin-real',(F(2,3),F(5,3),F(7,3),F(11,3),F(1,5),F(2,5),F(3,5),F(112,5)),
               (F(1,3),F(2,5)),(2,F(1,5)),None),
              ('short-roof-TR02-only',(4,12,20,28,4,8,20,28),(2,6),(14,2),(F(7,6),2,0,0))]
    results=[]
    for label,geometry,source,target,forced in fixtures:
        row=phases(geometry,source,target,forced)
        row['label']=label
        results.append(row)
    output={'status':'PASS','method':'Prescribed exact formula construction plus every finite original wall, vertex, velocity and first-target guard; no discovery.',
            'cases':results,'search_used':False,'whole_r3_complete':False,'whole_goal_complete':False}
    destination=Path(__file__).with_suffix('.json')
    destination.write_text(json.dumps(output,indent=2,default=str)+'\n')
    print(json.dumps({'status':'PASS','prescribed_cases':len(results),
                      'actual_reflections':sum(x['reflections'] for x in results),
                      'singular_roof_suffix_checked':any(x['singular_roof_discarded'] for x in results)}))
