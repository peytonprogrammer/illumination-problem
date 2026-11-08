"""Exact algebra on prescribed marks, not a direction or room search."""
from fractions import Fraction as F
from math import gcd,lcm
from pathlib import Path
from itertools import product
import json
ROOT=Path(__file__).resolve().parent
s=(F(12,7),F(16,7));t=(F(9,2),F(2));z=(F(3),F(4))
det=lambda u,v:u[0]*v[1]-u[1]*v[0]
den=lambda p:lcm(*(c.denominator for c in p))
assert den(s)==7 and den(t)==2 and gcd(den(s),den(t))==1
# Direct segment lies in the existing L room's open convex lower window.
assert all(0<p[0]<6 and 0<p[1]<3 for p in (s,t))
v=(39,-4)
sub_t_s=(t[0]-s[0],t[1]-s[1])
assert sub_t_s==(F(v[0],14),F(v[1],14)) and gcd(*v)==1
assert det(v,s)==96
# Check the fixed torus endpoint image numerators; no directions are generated.
rows=[]
for ex,ey in product((-1,1),repeat=2):
    Q=(ex*t[0],ey*t[1]);D=14
    u=(D*(Q[0]-s[0]),D*(Q[1]-s[1]))
    assert all(c.denominator==1 for c in u)
    assert gcd(gcd(int(u[0]),int(u[1])),2*D)==1
    rows.append({'target_image':Q,'common_denominator':D,'endpoint_numerator':u,
                 'primitive_coset_gcd':1,'clean_segment_lemma_hypothesis':True})
# Exact coprime-denominator intersection identity for the theorem's mechanism.
# If a/7=b/2, then 2a=7b; gcd(2,7)=1 forces 7|a and 2|b.
assert gcd(7,2)==1
out={'status':'PASS','source':s,'target':t,'blocker':z,'source_denominator':7,
     'target_denominator':2,'direct_primitive_direction':v,
     'direct_determinant':det(v,s),'direct_bypass':True,
     'all_connecting_directions_good':False,
     'all_connecting_directions_bad':True,
     'universal_argument':'For any integer direction v connecting P to Q+2lambda, det(v,P)=det(v,Q)+2 det(v,lambda) lies in (1/7)Z intersect (1/2)Z = Z. Applies to every reflected target image and source sign choice.',
     'fixed_endpoint_controls':rows,
     'scope':'Refutes unconditional good-direction existence for connected interior pairs; does not refute a conditional claim assuming a globally essential blocker, or the denominator clean-segment lemma.'}
(ROOT/'check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps(out,indent=2,default=str))
