"""Exact controls for hand-derived unbounded rectangle and affine obstructions."""
from fractions import Fraction as F
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
def square_types(w,h):
    interior=[(x,y) for x in range(1,w) for y in range(1,h)]
    smooth=[(x,y) for x in range(w+1) for y in range(h+1) if ((x in (0,w))+(y in (0,h))==1)]
    I=sum(x%2==y%2==0 for x,y in interior);J=len(interior)-I
    sA=sum(x%2==y%2==0 for x,y in smooth);sN=len(smooth)-sA
    corners=[(0,0),(w,0),(w,h),(0,h)];Q=3*sA+2*sum(x%2==y%2==0 for x,y in corners)
    assert 2*w*h==8*I+Q+sA and 4==2+6*I+Q-2*J-sN
    return I,J,sA,sN,Q
def main():
    controls=0
    for n in range(2,43):
        I,J,sA,sN,Q=square_types(2*n,2*n);assert (I,J,sN)==((n-1)**2,3*n*n-2*n,4*n);assert J+sN==3*n*n+2*n;controls+=1
        I,J,sA,sN,Q=square_types(4,2*n+1);assert (I,J,sA,sN,Q)==(n,5*n,2*n+1,2*n+5,6*n+7);assert J+sN==7*n+5;controls+=1
    # A=diag(2,1), diagonal mirror tangent(1,1): input(1,0) reflects to(0,1).
    # Transported input(2,0) reflects at image tangent(2,1) to(6/5,8/5),
    # which is not parallel to the transported outgoing(0,1).
    v=(F(2),F(0));t=(F(2),F(1));tt=sum(x*x for x in t);ref=tuple(2*sum(a*b for a,b in zip(v,t))/tt*x-y for x,y in zip(t,v))
    assert ref==(F(6,5),F(8,5)) and ref[0]!=0
    out={'status':'PRESCRIBED_EXACT_CONTROLS_PASS','rectangle_controls':controls,'affine_mirror_counterexample':{'map':'diag(2,1)','original_wall_tangent':[1,1],'original_incoming':[1,0],'original_reflected':[0,1],'mapped_incoming':[2,0],'mapped_actual_reflection':list(map(str,ref)),'mapped_expected_direction':[0,1]},'scope':'Supports universal rectangle count formulas and affine rigidity hand proofs; no dark pair or uncapped theorem claimed.'}
    (HERE/'bridge-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
