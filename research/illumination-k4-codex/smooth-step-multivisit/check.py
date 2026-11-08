"""Exact state/reflection identities and one prescribed outside-scope path.
No ray, direction, word or room enumeration/discovery.
"""
from pathlib import Path
from fractions import Fraction as F
import json
B=Path(__file__).resolve().parent

def mul(M,v):return tuple(sum(M[i][j]*v[j] for j in (0,1)) for i in (0,1))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def negative(v):return tuple(-x for x in v)

def main():
 Rx=((-1,0),(0,1));Ry=((1,0),(0,-1));I=((1,0),(0,1))
 cases=[]
 # Sign vectors represent coefficients of formal independent nonzero p,q.
 for axis,R in [(0,Rx),(1,Ry)]:
  for tangent in (-1,1):
   outgoing=[0,0];outgoing[axis]=-1;outgoing[1-axis]=tangent;outgoing=tuple(outgoing)
   other=list(outgoing);other[1-axis]*=-1;other=tuple(other)
   assert mul(R,other)==negative(outgoing)
   assert mul(R,outgoing)!=negative(outgoing)
   cases.append(dict(wall_normal_axis=axis,outgoing_signs=outgoing,other_outgoing_signs=other,other_arrival_is_negative_start=True))
 # A reversal at a vertical/horizontal regular wall forces a zero component.
 Rx_plus_I=tuple(tuple(Rx[i][j]+I[i][j] for j in (0,1)) for i in (0,1))
 Ry_plus_I=tuple(tuple(Ry[i][j]+I[i][j] for j in (0,1)) for i in (0,1))
 assert Rx_plus_I==((0,0),(0,2)) and Ry_plus_I==((2,0),(0,0))
 # In each axial case only one outgoing velocity remains at a transverse wall.
 axial=[dict(normal_axis=axis,unique_outgoing=tuple(-1 if i==axis else 0 for i in (0,1))) for axis in (0,1)]
 # Fixed 45-degree triangular control showing why orthogonality is essential.
 # Room: 0<y<x<2. Prescribed path, not a traced/discovered trajectory.
 S=(F(7,4),F(3,4));Z=(F(2),F(1));C=(F(3,2),F(3,2));T=(F(3,2),F(1,2))
 path=[S,Z,C,Z,T];velocities=[(1,1),(-1,1),(1,-1),(-1,-1)]
 swap=((0,1),(1,0))
 for v0,v1,R in zip(velocities,velocities[1:],[Rx,swap,Rx]):assert mul(R,v0)==v1
 for a,b,v in zip(path,path[1:],velocities):
  leg=sub(b,a);assert not cross(leg,v) and dot(leg,v)>0
  midpoint=tuple((a[j]+b[j])/2 for j in (0,1));assert 0<midpoint[1]<midpoint[0]<2
 assert all(p not in [(0,0),(2,0),(2,2)] for p in path)
 assert Z[0]==2 and 0<Z[1]<2 and C[0]==C[1] and 0<C[0]<2
 for a,b in zip(path[:-2],path[1:-1]):
  assert cross(sub(T,a),sub(b,a)) or dot(sub(T,a),sub(T,b))>0
 result=dict(status='PASS',symbolic_nonaxial_state_cases=cases,normal_reversal_matrices=[Rx_plus_I,Ry_plus_I],axial_cases=axial,outside_orthogonal_control=dict(room='triangle 0<y<x<2',path=[[str(x) for x in p] for p in path],same_smooth_point_visited_twice=True,midpoint_collision='normal reflection in diagonal x=y',first_target_arrival=True),scope='Algebraic controls only. Continuous uniqueness/time-reversal proof is in findings.md; no numerical trajectory search proves the theorem.')
 (B/'check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
