"""Symbolic replay of hand-specified continuations, without direction search.

Run: uv run --offline --with sympy python later-passes-check.py
The listed walls come from the hand derivation; no wall/ray/word selection,
numerical tracing, room assignments or guard-archive lookup occurs here.
"""
from pathlib import Path
import json
import sympy as s

HERE = Path(__file__).resolve().parent
r,h = s.symbols('r h', positive=True)
sim = s.factor
vec = lambda p: tuple(s.expand(s.cancel(v)) for v in p)
domain = None
positive_times = 0

def positive_on_interval(expr,lo,hi):
    """Exact signs of factored linear polynomials over an open interval."""
    num,den = s.fraction(s.cancel(expr))
    for poly in (num,den):
        _,factors = s.factor_list(poly,r)
        for factor,power in factors:
            assert s.degree(factor,r) == 1, factor
            a,b = factor.subs(r,lo),factor.subs(r,hi)
            assert a*b >= 0 and (a != 0 or b != 0), (expr,lo,hi)
    # All factors have no interior root/pole; its sign is its one-sided
    # endpoint limit. This is algebra, not a numerical direction sample.
    value = s.limit(expr,r,lo,dir='+')
    if value == 0:
        value = s.limit(expr,r,hi,dir='-')
    assert value > 0, (expr,lo,hi,value)

def advance(p,v,wall,reflect=False):
    global positive_times
    A,B,C = wall
    t = sim((C-A*p[0]-B*p[1])/(A*v[0]+B*v[1]))
    if domain is not None:
        positive_on_interval(t,*domain)
        positive_times += 1
    q = vec((p[0]+t*v[0],p[1]+t*v[1]))
    if reflect:
        scale = sim(2*(A*v[0]+B*v[1])/(A*A+B*B))
        v = vec((v[0]-scale*A,v[1]-scale*B))
    return q,v

def hits(p,v,walls):
    for wall in walls:
        p,v = advance(p,v,wall,True)
    return p,v

X = lambda x: (1,0,s.Rational(x))
Y = lambda y: (0,1,s.Rational(y))
LD = (-1,1,2)   # y=x+2; L+ and T- diagonal
ED = (-1,1,-2)  # y=x-2
ND = (1,1,2)   # y=2-x
DD = (1,1,0)   # y=-x
L3 = [LD,Y(0),LD]
E3 = [ED,Y(2),ED]
N3 = [ND,Y(2),ND]
D3 = [DD,X(2),DD]
D4 = D3+[X(2)]
T3 = [LD,X(2),LD]
T4 = [X(2),LD,X(2),LD]

# Complete descending-entry response for 0<h<1, 0<r<1 in
# triangle 0<=X<=Y<=1, mouth X=0, entry velocity(1,-r).
diag = (1,-1,0)
local = []
for count,walls,exit_y,out_v in (
    (1,[diag],h/r,(-r,1)),
    (2,[diag,Y(1)],2-h/r,(-r,-1)),
    (3,[diag,Y(1),diag],h-2*r,(-1,-r))):
    p,v = hits((0,h),(1,-r),walls)
    p,v = advance(p,v,X(0))
    assert p == vec((0,exit_y)) and v == out_v
    local.append({'reflections':count,'exit_height':str(exit_y),'velocity':list(map(str,v))})

# A steep cap entry can have FOUR hits, despite the earlier three-hit
# branch. Two strict subbranches meet at an excluded apex collision h=r.
bottom_diag = (1,-1,1)  # y=x-1
four_hit = []
for walls in ([bottom_diag,X(0),bottom_diag,X(0)],
              [X(0),bottom_diag,X(0),bottom_diag]):
    p,v = hits((h,0),(-r,-1),walls)
    p,v = advance(p,v,Y(0))
    assert p == (2*r-h,0) and v == (r,1)
    four_hit.append({'wall_order':['diagonal' if w == bottom_diag else 'vertical' for w in walls],
        'exit_x':'2r-h','velocity':['r','1']})

# Specified L/E/N prefix, including exact portal exits.
domain = (s.Rational(1,7),s.Rational(2,13))
p,v = hits((0,0),(-1,r),L3)
p,v = advance(p,v,X(-1))
assert p == (-1,3*r) and v == (1,r)
p,v = hits(p,v,E3)
p,v = advance(p,v,X(3))
assert p == (3,9*r) and v == (-1,r)
p,v = hits(p,v,N3)
p,v = advance(p,v,X(1))
assert p == (1,13*r) and v == (1,r)
p,v = hits(p,v,[X(3),X(1),X(3)])
assert p == (3,19*r) and v == (-1,r)
upper_p,upper_v = p,v

# Left roof first descent, shared by three floor-response cases.
domain = (s.Rational(1,7),s.Rational(3,20))
p,v = hits(upper_p,upper_v,[LD])
p,v = advance(p,v,Y(2))
assert p == (22*r-2,2) and v == (r,-1)
left_p,left_v = p,v

rows = {}
def save(name,p2,p3,expected2,expected3,lo,hi):
    assert sim(p2[0]-expected2) == 0 and p2[1] == 2
    assert sim(p3[0]-expected3) == 0 and p3[1] == 2
    # All these endpoint expressions are affine in r. Their exact open
    # ranges therefore follow from endpoint values, with no sampling.
    ranges = []
    for expr in (expected2,expected3):
        ends = sorted((expr.subs(r,lo),expr.subs(r,hi)))
        assert not (ends[0] < 2 < ends[1])
        assert sim(s.diff(expr,r,2)) == 0
        ranges.append(list(map(str,ends)))
    rows[name] = {'interval':list(map(str,(lo,hi))),
        'second_height2_x':str(expected2),'third_height2_x':str(expected3),
        'open_x_ranges':ranges,'target_hit':'NO on these specified passages'}

p,v = hits(left_p,left_v,[Y(-1)])
p2,_ = advance(p,v,Y(2))
p,v = hits(p,v,[Y(3)])
p3,_ = advance(p,v,Y(2))
save('left_roof_Dminus_absent',p2,p3,28*r-2,30*r-2,s.Rational(1,7),s.Rational(3,20))

domain = (s.Rational(1,7),s.Rational(4,27))
p,v = hits(left_p,left_v,D3)
p,v = advance(p,v,Y(-1))
assert p == (27*r-2,-1) and v == (r,1)
p2,_ = advance(p,v,Y(2))
p,v = hits(p,v,[Y(3)])
p3,_ = advance(p,v,Y(2))
save('left_roof_Dminus_three_hits',p2,p3,30*r-2,32*r-2,s.Rational(1,7),s.Rational(4,27))

domain = (s.Rational(4,27),s.Rational(3,20))
p,v = hits(left_p,left_v,D4)
p,v = advance(p,v,Y(-1))
assert p == (6-27*r,-1) and v == (-r,1)
p2,_ = advance(p,v,Y(2))
p,v = hits(p,v,T3+[X(1)])
p3,_ = advance(p,v,Y(2))
save('left_roof_Dminus_four_hits',p2,p3,6-30*r,34*r-4,s.Rational(4,27),s.Rational(3,20))

# Right-roof return through E and N; N has two or three hits depending
# on the strict branch threshold 5/33. No numeric r is selected.
domain = (s.Rational(3,20),s.Rational(2,13))
p,v = hits(upper_p,upper_v,[Y(3),X(1),X(3),X(1)])
p,v = advance(p,v,X(3))
assert p == (3,6-27*r) and v == (1,-r)
p,v = hits(p,v,E3)
p,v = advance(p,v,X(3))
assert p == (3,6-29*r) and v == (-1,-r)
p,v = advance(p,v,X(1))
assert p == (1,6-31*r)
n_entry,n_velocity = p,v
domain = (s.Rational(5,33),s.Rational(2,13))
p,v = hits(p,v,[ND,Y(2)])
p,v = advance(p,v,X(1))
assert p == (1,34-5/r) and v == (r,-1)
n2_p,n2_v = p,v

p,v = hits(n2_p,n2_v,[Y(-1)])
assert p == (35*r-4,-1)
p2,_ = advance(p,v,Y(2))
p,v = hits(p,v,T4)
p,v = advance(p,v,Y(3))
assert p == (8-41*r,3) and v == (-r,-1)
p3,_ = advance(p,v,Y(2))
save('right_roof_Ntwo_Dminus_absent',p2,p3,38*r-4,8-42*r,s.Rational(5,33),s.Rational(2,13))

p,v = hits(n2_p,n2_v,D3)
p,v = advance(p,v,Y(-1))
assert p == (37*r-4,-1) and v == (r,1)
p2,_ = advance(p,v,Y(2))
p,v = hits(p,v,[Y(3)])
p3,_ = advance(p,v,Y(2))
save('right_roof_Ntwo_Dminus_present',p2,p3,40*r-4,42*r-4,s.Rational(5,33),s.Rational(2,13))

domain = (s.Rational(3,20),s.Rational(5,33))
p,v = hits(n_entry,n_velocity,N3)
p,v = advance(p,v,X(1))
assert p == (1,6-33*r) and v == (1,-r)
p,v = advance(p,v,X(3))
assert p == (3,6-35*r)
# R+ is the cap conv{(3,0),(3,1),(4,0)}, not the E/N orientation.
arrival_p,arrival_v = p,v
p,v = hits(p,v,[(1,1,4),Y(0),(1,1,4)])
p,v = advance(p,v,X(3))
assert p == (3,6-37*r) and v == (-1,-r)
p,v = advance(p,v,X(-1))
assert p == (-1,6-41*r)
present_next = tuple(map(str,p))
p,v = arrival_p,(-1,-r)  # exposed vertical mirror flips the x velocity
p,v = advance(p,v,X(-1))
assert p == (-1,6-39*r)
absent_next = tuple(map(str,p))
arrival = {'interval':['3/20','5/33'],'point':['3','6-35r'],
    'height_open_range':['23/33','3/4'], 'next_boundary_choice':'R+ present or absent',
    'Rplus_present_next_left_contact':present_next,
    'Rplus_absent_next_left_contact':absent_next}
assert 6-35*s.Rational(5,33) == s.Rational(23,33)
assert 6-35*s.Rational(3,20) == s.Rational(3,4)

out = {'status':'PASS','method':'Symbolic substitution into specified wall sequences, no numeric direction samples or itinerary selection.',
    'strict_positive_flight_times_over_intervals':positive_times,
    'descending_cap_map':local,'steep_four_hit_cap_map':four_hit,
    'five_prescribed_continuations':rows,
    'remaining_three_hit_northwest_branch':arrival,
    'limits':'Hand interval/portal proof supplies itinerary validity. No entire-family illumination or dark example established; later passes remain open.'}
(HERE/'later-passes-check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: five local return-map identities, five prescribed later continuations and R+ split; no direction samples.')
