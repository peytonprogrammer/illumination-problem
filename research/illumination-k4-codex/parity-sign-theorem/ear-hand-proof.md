# A hand opening mechanism for one ear family

[done] Explicit unfolding argument and exact interval certificate.
[done] Independent mathematical/code review by Opus; reviewed without executing.
[waiting on Claude] Independent numerical replay in a separate output copy.

A legal ray must avoid every polygon vertex, including a tangential passage through a reflex vertex. Reflections occur only in wall interiors.

## The family and the claim

Use the counterclockwise polygon with the following vertices, numbered 0 through 24:

```text
0:(0,0)    1:(1,0)    2:(1,1)    3:(2,2)    4:(1,2)
5:(1,3)    6:(2,4)    7:(1,4)    8:(1,5)    9:(2,6)
10:(1,6)   11:(1,7)   12:(0,8)   13:(0,7)   14:(-1,7)
15:(-2,6)  16:(-1,6)  17:(-1,5)  18:(0,5)  19:(0,3)
20:(-1,3)  21:(-2,2)  22:(-1,2)  23:(-1,1)  24:(0,1)
```

Keep the marks S=(0,2), T=(0,6). Move only vertices 5,6,7 to

    C_e=(1,3+2 e),  U_e=(2-e,4+e),  V_e=(1,4+e).

Every other vertex stays fixed. Equivalently, the two changed supporting lines are

    wall5: y-x=2+2 e,    wall6: y=4+e.

Wall i joins vertex i to vertex i+1, modulo25. The family is strictly simple for -1/2<e<1: the changed boundary remains a right-hand protrusion between heights2 and5, its edges have positive length, and it meets no other boundary arc. Both marks remain interior.

**Claim.** At e=0 the marks are dark by the parity obstruction. For every sufficiently small nonzero e they illuminate each other. The exact interval checker proves the quantitative statement for

    0<|e|<=1/1000.

The opening mechanism below is a hand argument using two specified reflection words. The stated numerical interval additionally uses the accompanying exact inequality certificate.

## The two moving mirrors have a simple effect

Write H_b for reflection in y=b, V_a for reflection in x=a, D_d for reflection in y-x=d, and A_c for reflection in x+y=c:

    H_b(x,y)=(x,2 b-y),       V_a(x,y)=(2 a-x,y),
    D_d(x,y)=(y-d,x+d),      A_c(x,y)=(c-y,c-x).

Composition is written XY=X composed with Y. Direct substitution gives

    H_(b+e) D_(d+2 e)(x,y)=(y-d-2 e,2 b-d-x).

Thus this consecutive mirror pair shifts its developed image by exactly (-2 e,0). This is the source of the sign in the proof. No gradient or linear-program calculation is used.

## Positive e: the line passes above the moving corner

Use the word

    23,20,2,3,0,24 | 6,5,18,7,16,10,12,11.

The bar marks passage through C_0 in the limiting path; it is not a reflection there. The prefix and suffix developments are

    Phi_+=H_1 D_4 D_0 H_2 H_0 V_0,
    Psi_+=H_(4+e) D_(2+2 e) V_0 V_1 V_(-1) V_1 V_0 A_8.

Multiplication gives

    Phi_+(x,y)=(-x-4,-y-6),
    Psi_+(x,y)=(6-2 e-x,20-y).

In the physical corner frame, the source and target images are therefore

    S'=Phi_+^(-1)(S)=(-4,-8),
    T'=Psi_+(T)=(6-2 e,14).

The chord S'T' crosses x=1 at height

    y=-8+110/(10-2 e).

Its height above C_e is exactly

    y-(3+2 e)=e(1+2 e)/(5-e)>0              for 0<e<1.

Its slope is 11/(5-e)>1. Locally the exterior of the polygon at C_e is the sector to the right of x=1 and below y=x+2+2 e. The chord crosses x=1 above C_e and continues more steeply upward than that diagonal wall, so it avoids this exterior sector.

At e=0 every other reflection in this word is in a wall interior, and every other intervening segment stays in the room away from vertices; the limiting bounce points are listed below. Near C_0 only walls4 and5 meet the limiting corner; away from that corner all the listed conditions are strict. These finitely many strict conditions persist for small e. Thus the chord folds to a legal connection for all sufficiently small positive e.

The full target image is (-10+2 e,-20). The initial direction is therefore (-10+2 e,-22); the path is aimed at the moved target image, rather than keeping the old direction fixed.

## Negative e: a corner reflection becomes an ordinary reflection

Use the shorter word

    6,5,18,7 | 16,11,17,14.

Its limiting corner is the fixed point K=(-1,6). This time wall16 is an intended reflection whose limiting contact is K. The developments are

    Phi_-=H_(4+e) D_(2+2 e) V_0 V_1,
    Psi_-=V_(-1) A_8 H_5 D_8,

so

    Phi_-(x,y)=(y-2-2 e,8-x),
    Psi_-(x,y)=(-x-8,16-y).

The corner-frame source and target images are

    S'=(6,2+2 e),    T'=(-8,10).

Their chord crosses x=-1 at exactly

    (-1,6+e).

For -1<e<0 this point lies strictly inside wall16, which runs from (-1,6) to (-1,5). Folding at this vertical mirror reflects the path back toward the room interior. The potentially forbidden corner passage has become a legal smooth-wall reflection.

Near K only walls15 and16 meet the limiting corner. All other contacts in this word are strict at e=0 and persist for small e. Hence sufficiently small negative e also gives a connection. The full developed target is (8-2 e,16), so the initial direction is (8-2 e,14).

## The reusable local opening rule

Suppose an analogous ear corner moves from c to c+(0,2 e). Assume a limiting one-corner itinerary has fixed prefix image of the source c-(p,q), while its suffix begins with the moving H,D pair above and then uses fixed supporting lines. If its target image at e=0 is c+(p,q), the moving target image is c+(p-2 e,q).

At the vertical line through c, the chord clears the moved corner by

    e(q-2 p+2 e)/(p-e).

For q>2 p>0 this is positive for sufficiently small positive e, and the chord is steeper than the diagonal ear wall. Provided the remaining limiting itinerary is strict away from that corner, this constructs an actual connecting path. The example has p=5,q=11. This local rule is one-sided; the negative-e proof uses the different corner-to-wall-interior reflection mechanism.

More generally, replace the images by c-(p1,q1) and c+(p2,q2), where p1,p2>0 and q1/p1=q2/p2. The same calculation gives clearance 2 e(q1-p1-p2+2 e)/(p1+p2-2 e). Thus q1>p1+p2 is a sufficient one-sided slope condition under the same itinerary hypotheses. Midpoint symmetry is not needed for this local calculation.

This rule explains the sign from mirror geometry. It does not prove that an arbitrary ear in an arbitrary parity room admits the required return itinerary or the slope q>2 p. That existence step remains open.

## Base-path arithmetic and the quantitative interval

Substituting the e=0 polygon into the two developments gives these physical bounce points:

|Positive-e word: wall and point|Negative-e word: wall and point|
|---|---|
|23: (-5/11,1)|6: (8/7,4)|
|20: (-5/4,11/4)|5: (16/11,38/11)|
|2: (3/2,3/2)|18: (0,30/7)|
|3: (14/11,2)|7: (1,34/7)|
|0: (4/11,0)|16: (-1,6), the limiting corner|
|24: (0,4/5)|11: (10/11,78/11)|
|6: (16/11,4)|17: (-2/7,5)|
|5: (13/8,29/8)|14: (-14/11,74/11)|
|18: (0,48/11)||
|7: (1,53/11)||
|16: (-1,63/11)||
|10: (1,73/11)||
|12: (0,78/11)||
|11: (5/8,59/8)||

The positive-e limiting path additionally passes through C_0=(1,3) between its contacts with walls24 and6. No other vertex occurs. In the negative-e word K is its only vertex contact. These facts and the strict wall-interior contacts can be checked against the listed polygon edges.

`ear-hand-check.py` certifies the complete intervals 0<e<=1/1000 and -1/1000<=e<0, not sampled parameters. It uses the two fixed words, unfolds the moved target, and proves:

- Positive time between consecutive contacts and the final target arrival.
- Every intended reflection lies strictly inside its wall.
- No segment intersects any other wall before the next intended contact.
- The polygon stays simple and both marks stay interior.

All conditions reduce to rational polynomials. A polynomial with first nonzero term a_r u^r is positive on 0<u<=rho when a_r exceeds the sum of the absolute higher coefficients times their powers of rho. This coefficient bound proves each inequality, including arbitrarily near u=0. The output contains 578 segment/wall exclusions in total: 361 for positive e and 217 for negative e. It contains 275 nonadjacent-edge separation certificates for each parameter sign. Mark interiority follows from interiority at e=0, continuous deformation through simple polygons, and the certified absence of mark/boundary contact, which keeps the winding number constant. The checker pins both frozen input hashes before evaluating any geometry.

At e=0, reflections preserve the even-even lattice class and every other integer point in the closed polygon is a corner. Unfolding a connection would force an intermediate non-even-even integer point, hence a corner. This is the original parity obstruction. The result here is a concrete two-sided opening of that dark parameter value within this one-parameter family; it is not the general sign theorem.
