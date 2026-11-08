"""Exact matrix/parity checks for a fixed whole-room similarity; no search."""
from pathlib import Path
from fractions import Fraction as Q
import json
R=Path(__file__).resolve().parent
F=((1,1),(1,-1));Finv=((Q(1,2),Q(1,2)),(Q(1,2),Q(-1,2)))
I=((1,0),(0,1))
def mul(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def transpose(a):return tuple(zip(*a))
def apply(a,p):return tuple(sum(a[i][k]*p[k] for k in range(2)) for i in range(2))
assert mul(transpose(F),F)==((2,0),(0,2)) and mul(F,Finv)==mul(Finv,F)==I
# Reflections in diagonals through0 are x/y exchanges with sign, conjugating to axial flips.
for D in [((0,1),(1,0)),((0,-1),(-1,0))]:
 C=mul(mul(F,D),Finv)
 assert C in [((1,0),(0,-1)),((-1,0),(0,1))]
axial=[(0,0),(8,0),(8,4),(4,4),(4,8),(0,8)]
Sax=(6,2);Tax=(2,6)
diagonal=[apply(Finv,p) for p in axial];S=apply(Finv,Sax);T=apply(Finv,Tax)
assert S==(4,2) and T==(4,-2)
assert all(x.denominator==y.denominator==1 for x,y in diagonal+[S,T])
assert all(apply(F,p)==q for p,q in zip(diagonal,axial))
for a,b in zip(diagonal,diagonal[1:]+diagonal[:1]):
 dx,dy=b[0]-a[0],b[1]-a[1]
 assert abs(dx)==abs(dy)>0
 support=a[0]-a[1] if dx==dy else a[0]+a[1]
 assert support%2==0
assert all(x%2==y%2==0 for x,y in [S,T,apply(F,S),apply(F,T)])
out={'status':'PASS_EXACT_ORTHOGONAL_FRAME_NORMALIZATION','F':F,'Finv':[[str(x) for x in row] for row in Finv],'FtF':[[2,0],[0,2]],'existing_axial_L':axial,'prescribed_diagonal_L':[[str(x),str(y)] for x,y in diagonal],'actual_diagonal_S':list(map(str,S)),'actual_diagonal_T':list(map(str,T)),'roundtrips_exact':True,'all_diagonal_supports_even':True,'new_search_or_census':False,'whole_goal_complete':False}
(R/'geometric-reduction-orthogonal-normalization.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
