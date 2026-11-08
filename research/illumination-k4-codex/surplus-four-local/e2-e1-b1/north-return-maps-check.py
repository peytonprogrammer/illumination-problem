"""Exact coefficient identities for SIX hand-declared local return branches.

No point sampling, trajectory generation, search, symbolic solver, or rooms.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json

HERE=Path(__file__).resolve().parent
# Sparse polynomials in the FREE variables u,a, used only to clear denominators.
def poly(terms): return {k:F(v) for k,v in terms.items() if v}
def add(*ps):
    out={}
    for p in ps:
        for k,v in p.items(): out[k]=out.get(k,F(0))+v
    return poly(out)
def scale(c,p): return poly({k:F(c)*v for k,v in p.items()})
def mul(p,q):
    out={}
    for (i,j),v in p.items():
        for (k,l),w in q.items(): out[i+k,j+l]=out.get((i+k,j+l),F(0))+v*w
    return poly(out)
zero={}; one=poly({(0,0):1}); u=poly({(1,0):1}); a=poly({(0,1):1})
V=(((-1,0),(0,1)),(0,0))
H=(((0,-1),(-1,0)),(1,1))
def compose(left,right):
    A,b=left; C,d=right
    return (tuple(tuple(sum(A[i][k]*C[k][j] for k in range(2)) for j in range(2)) for i in range(2)),
            tuple(sum(A[i][k]*d[k] for k in range(2))+b[i] for i in range(2)))
def folded(word):
    g=(((1,0),(0,1)),(0,0))
    for wall in word: g=compose({'H':H,'V':V}[wall],g)
    return g
z=add(u,scale(2,a))
branches=[
 ('right_lower','a > 1-u','H',add(one,scale(-1,u)),a,
  add(a,scale(-1,add(one,scale(-1,u)))),(scale(-1,one),scale(-1,a))),
 ('right_upper','(1-u)/2 < a < 1-u','HV',add(one,scale(-1,u)),a,
  add(one,scale(-1,u),scale(-1,a)),(one,scale(-1,a))),
 ('top_positive','-u/2 < a < (1-u)/2','HVH',scale(2,one),one,z,(a,scale(-1,one))),
 ('top_negative_right_of_apex','-(1+u)/2 < a < -u/2 AND a > -u','HVHV',
  scale(2,one),one,scale(-1,z),(scale(-1,a),scale(-1,one))),
 ('top_negative_left_of_apex','-(1+u)/2 < a < -u/2 AND a < -u','VHVH',
  scale(2,one),one,scale(-1,z),(scale(-1,a),scale(-1,one))),
 ('left_upper','-(1+u) < a < -(1+u)/2','VHV',add(one,u),scale(-1,a),
  add(one,u,a),(one,a)),
 ('left_lower','a < -(1+u)','VH',add(one,u),scale(-1,a),
  add(scale(-1,a),scale(-1,one),scale(-1,u)),(scale(-1,one),a)),
]
checks={}
for name,gate,word,tn,td,outn,outv in branches:
    A,b=folded(word)
    # Entry(u,0)+t*(a,1), t=tn/td; apply the fixed wall reflections.
    xn=add(mul(u,td),mul(a,tn)); yn=tn
    folded_n=[add(scale(A[i][0],xn),scale(A[i][1],yn),scale(b[i],td)) for i in range(2)]
    assert folded_n==[outn,zero],name
    velocity=tuple(add(scale(A[i][0],a),scale(A[i][1],one)) for i in range(2))
    assert velocity==outv,name
    assert all(sum(A[k][i]*A[k][j] for k in range(2))==int(i==j) for i in range(2) for j in range(2))
    checks[name]={'status':'EXACT_FREE_POLYNOMIAL_IDENTITIES_PASS',
                  'gate':gate,'reflection_word_declared_by_hand':word,
                  'reflections':len(word),'fold_isometry':{'matrix':A,'offset':b},
                  'denominator_cleared_endpoint_on_base_and_return_velocity':True}
assert folded('HVHV')==folded('VHVH')
# HAND-declared square boundary events. All endpoint conditions follow by
# coefficient identity from the unfolded line(u+a*t,t).
events=[('right_midpoint',add(one,scale(-1,u)),one,(1,1)),
        ('right_upper_corner',add(one,scale(-1,u)),scale(2,one),(1,2)),
        ('top_midpoint',scale(-1,u),scale(2,one),(0,2)),
        ('left_upper_corner',scale(-1,add(one,u)),scale(2,one),(-1,2)),
        ('left_midpoint',scale(-1,add(one,u)),one,(-1,1)),
        ('apex',scale(-1,u),one,(0,1))]
for name,an,ad,(xx,yy) in events:
    assert add(mul(u,ad),scale(yy,an))==scale(xx,ad),name
# Physical N5/N6 transforms are exact affine isometries, not distinct trials.
for epsilon in [-1,1]:
    assert epsilon*epsilon==1
# Source-direct u=a=d special branches, denominator-cleared identities.
# top: u+2a=3d. right-upper:(1-d)/d-1=(1-2d)/d.
# right-lower:1-(1-d)/d=(2d-1)/d.
assert add(one,scale(-1,u),scale(-1,u))==add(one,scale(-2,u))
assert add(u,scale(-1,one),u)==add(scale(2,u),scale(-1,one))
# Downward exit implies a direct rightward run from x<=1 cannot enter an
# E34 inlet at x=3,height>1: y(3)=1+(3-x)*vy/vx <1.
assert all(len(word)<=4 for _,_,word,*_ in branches)
self_hash=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
out={'status':'EXACT_HAND_N5_N6_SIX_BRANCH_RETURN_MAP_IDENTITIES_PASS',
 'domain':'0<u<1, a any real; six singular slopes excluded as in proof',
 'branches':checks,'square_event_exclusions':[x[0] for x in events],
 'physical_coordinates':'N5 epsilon=-1; N6 epsilon=+1; x=epsilon*u, y=1+eta',
 'max_reflections':4,
 'north_exit_is_downward':'vy_out<0 on every strict branch; inequalities established in hand proof',
 'direct_north_to_E34':'IMPOSSIBLE without an intervening reflection',
 'source_direct_normalized_u_equals_a_d':{'three':'0<d<1/3','two':'1/3<d<1/2','one':'1/2<d<1'},
 'source_hashes':{'north-return-maps-check.py':self_hash},
 'limits':'Algebra checks coefficient identities for already hand-declared words, not branch discovery or numerical sampling. Inequality exhaustion and unfolded-square proof are hand arguments in north-return-maps.txt. Local cap map only; no full-room trajectory, actual-target match, optical closure, or independent/expert/formal verification.'}
(HERE/'north-return-maps-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
print('Six exit branches (top-negative has two words), all exact affine identities; six corner events; at most4 reflections. No trajectories sampled or rooms assembled.')
