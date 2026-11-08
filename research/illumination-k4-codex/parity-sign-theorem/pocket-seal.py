"""Prescribed finite D4 arrival-state and cone-index checks, no trajectories."""
from fractions import Fraction as F
from pathlib import Path
import json
B=Path(__file__).resolve().parent
D4=[((1,0),(0,1)),((0,-1),(1,0)),((-1,0),(0,-1)),((0,1),(-1,0)),((1,0),(0,-1)),((-1,0),(0,1)),((0,1),(1,0)),((0,-1),(-1,0))]
def ap(g,v):return tuple(sum(g[i][j]*v[j] for j in (0,1)) for i in (0,1))
def inv(g):return ((g[0][0],g[1][0]),(g[0][1],g[1][1]))
checks=[]
for q,w in [((1,1),(1,3)),((1,1),(3,5)),((1,2),(1,2)),((1,2),(2,1)),((1,2),(2,3))]:
    incoming={ap(inv(g),w) for g in D4 if tuple(x%2 for x in ap(g,q))==tuple(x%2 for x in w)}
    incoming={v for v in incoming if v[0]>0}
    pairs={tuple(sorted((v,(v[0],-v[1])))) for v in incoming}
    assert all((v[0],-v[1]) in incoming for v in incoming)
    expected=2 if q==(1,1) else 1
    assert len(pairs)==expected and len(incoming)==2*expected
    checks.append({'q':q,'w':w,'incoming_states':sorted(incoming),'reversal_pairs':len(pairs)})
# Lambda = theta coefficient plus pi coefficient, in exact rational arithmetic.
def cone(k,beta):
    a,c=beta
    return (a,c+F(5*k-1,4)) if k%2==0 else (-a,F(5*k+6,4)-c)
source=cone(0,(1,F(1)))
assert source==(1,F(3,4))
cases=[('+','+',6,(1,F(1,2)),7,3),('+','-',3,(-1,F(3,2)),3,3),('-','+',7,(-1,F(1,2)),9,1),('-','-',2,(1,F(3,2)),3,3)]
table=[]
for sign,eps,k,beta,expected,small in cases:
    end=cone(k,beta)
    assert end[0]==source[0]
    turn=end[1]-source[1]
    assert turn==expected and min(turn,10-turn)==small
    table.append({'first_y_sign':sign,'second_y_sign':eps,'directed_pi':str(turn),'minimum_pi':str(min(turn,10-turn))})
# Prescribed algebra controls for the finite multiple-corner proposition.
def det(v,z):return v[0]*z[1]-v[1]*z[0]
def add(v,z):return tuple(v[i]+z[i] for i in (0,1))
def scale(c,v):return tuple(c*x for x in v)
w=(3,1)
vp=(5,-2)
opening=[]
for j,cp in [(1,(1,2)),(3,(-3,4))]:
    v0=scale(4,w)
    c0=scale(j,w)
    # Quadratic determinant's linear coefficient, without optical tracing.
    direct=det(vp,c0)+det(v0,cp)
    defect=add(scale(j,vp),scale(-4,cp))
    assert direct==-det(w,defect)
    opening.append({'j':j,'target_derivative':vp,'corner_derivative':cp,
                    'defect':defect,'area_linear_coefficient':direct})
quadrants=[]
a,b=2,4
for sx,sy in [(1,1),(1,-1),(-1,1),(-1,-1)]:
    p0,q0=w
    n=sx*(1 if q0>0 else -1)*(abs(p0)+abs(q0)+1)
    px=p0+a*n*q0
    m=sy*(1 if px>0 else -1)*(abs(q0)+abs(px)+1)
    qy=q0+b*m*px
    assert sx*px>0 and sy*qy>0 and abs(qy)>abs(px)>0
    quadrants.append({'desired_signs':[sx,sy],'horizontal_power':n,
                      'vertical_power':m,'result':[px,qy]})
out={'status':'EXACT_SEALED_STATE_AND_CONE_ALGEBRA_PASS','arrival_controls':checks,'cone_table':table,
     'multiple_corner_algebra':opening,'prescribed_quadrant_controls':quadrants,
     'scope':'Five prescribed D4/parity arrival-state sets, four exact cone-index cases, two determinant identities, and four prescribed shear-quadrant controls only. No billiard tracing, ray, room, direction, word, cylinder or origami discovery.',
     'portal_avoiding_connection_exists':None,'portal_avoiding_existence_status':'NOT_PROVED_OR_DISPROVED','universal_one_corner_event_proved':False}
(B/'pocket-seal.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='arrival_controls'},indent=2))
