"""Complete decision for one primitive direction in simple canonical rooms.

A first-arrival connecting ray uses <=r*J+(r/2)*S exceptional vertices,
counting visits, where r=|D4*d|, J are interior B/C exceptions and S smooth
boundary B/C exceptions. Its primitive unfolding duration is twice its visit
count. Crossing the four canonical grid-line families then bounds reflections.
This does not bound primitive directions or decide all-direction darkness.
"""
from math import gcd
from illumination_geometry import check,label,owners_of,check_fan_angles
from illumination_cover import D4,mat
from illumination_paths import trace
from illumination_sector_paths import verify


def parameters(data,direction):
    d=tuple(direction)
    if len(d)!=2 or any(type(v) is not int for v in d) or not any(d):raise ValueError('nonzero integer direction required')
    divisor=gcd(*map(abs,d));d=tuple(v//divisor for v in d)
    geometry=check(data,strict=False)
    if not geometry['simple_polygon'] or data.get('slits'):raise ValueError('simple canonical polygon without slits required')
    if any(label(tuple(p))!='A' or tuple(p) not in geometry['interior_A'] for p in data['marked']):raise ValueError('distinct interior A marks required')
    ts=[tuple(sorted(map(tuple,t))) for t in data['triangles']];owners=owners_of(ts);opens={e for e,os in owners.items() if len(os)==2}
    interior=smooth=0
    for p in geometry['transparent_vertices']:
        sizes,full=check_fan_angles(ts,tuple(p),owners,opens)
        assert full or sizes==[4]
        interior+=full;smooth+=not full
    orbit=len({mat(g,d) for g in D4});assert orbit in (4,8)
    visit_bound=orbit*interior+(orbit//2)*smooth
    duration_bound=2*visit_bound
    crossing_rate=abs(d[0])+abs(d[1])+max(map(abs,d))
    return dict(direction=d,interior_exceptions=interior,smooth_exceptions=smooth,velocity_orbit=orbit,
                exception_visit_bound=visit_bound,primitive_duration_bound=duration_bound,
                reflection_bound=duration_bound*crossing_rate)


def decide_direction(data,direction):
    bounds=parameters(data,direction)
    if not bounds['exception_visit_bound']:
        return dict(status='NOT_ILLUMINATED_IN_DIRECTION',reason='no transparent non-A vertex for the first odd lattice step',bounds=bounds)
    witness=trace(data,bounds['direction'],bounds['reflection_bound'])
    if witness['status']=='illuminated':
        verify(data,witness)
        assert witness['bounces']<=bounds['reflection_bound']
        return dict(status='ILLUMINATED',witness=witness,bounds=bounds)
    assert witness['status'] in ('corner','periodic','limit'),witness
    return dict(status='NOT_ILLUMINATED_IN_DIRECTION',reason=witness['status'] if witness['status']!='limit' else 'first-arrival reflection bound exceeded',bounds=bounds,trace_status=witness['status'])
