# TR01: genuine-wall optical coverage in ordered three-reflex spirals

Quantified positive candidate, published before checks. Parameters are arbitrary real numbers satisfying

    0<a<l<w<A,  0<b<c<h<H.

Let P have CCW boundary

    (a,b),(a,h),(w,h),(w,c),(l,c),
    (l,0),(A,0),(A,H),(0,H),(0,b).

Equivalently P is the union of the closed rectangles [0,a]x[b,H], [0,A]x[h,H], [w,A]x[0,H], [l,A]x[0,c]. Its three reflexes are consecutive, so its gap type is (1,1,8). Integral parameters and actual even-even marks are target-class members; arbitrary-real parameters are allowed in this candidate.

Define the actual-interior set

    G = int(P) intersect ({x<a} union {y>=h} union {x>w and y>=c}),

and the L subroom

    R = ([l,A]x[0,c]) union ([w,A]x[c,H]).

Claim: every distinct actual interior S,T illuminates in ORIGINAL P if either (i) both belong to G, or (ii) both are strictly interior to R. Original-room endpoints on artificial subroom boundaries are NOT silently included in (ii).

Mechanism: for (i) use the accepted U construction in Q=[0,a]x[b,H] union [0,A]x[h,H] union [w,A]x[0,H], via y->H-y. Its right-arm traces stay no lower than the right endpoint, hence at least c; its only artificial vertical wall x=w below c is never contacted. Other placements use the accepted L charts from that U theorem with only genuine vertical reflections. For (ii) use the accepted horizontal-reflection-only L theorem; every horizontal R wall is a genuine P wall.

Success criterion: prove actual finite S-to-T trajectories under these full metric and endpoint conditions, including y=h,c seams, with all artificial-cut and genuine-corner guards. Strongest objection: the accepted whole W8 theorem alone does NOT guarantee avoidance of artificial mirrors; the specific accepted constructions must supply that avoidance. R-boundary points are not interior L endpoints.

This is a partial optical theorem for one ordered spiral class, not all metrics of gap type (1,1,8), not all endpoint placements, and not the full r3 or r<=8 theorem. No discovery search or clock begins; hand transfer proof only.
