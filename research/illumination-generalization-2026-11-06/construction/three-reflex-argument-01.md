# TR01: partial optical theorem for an arbitrary-metric ordered spiral

Submitted for independent review. The statement and parameters are exactly those in three-reflex-candidate-01.md. This is a positive actual-room optical result on its stated endpoint classes, not completion of the (1,1,8), r3, or r<=8 objectives.

## Geometry and accepted dependencies

The strict parameter orders give the displayed Jordan boundary: its three right turns are at (a,h), (w,h), (w,c), and its seven other turns are left turns. Its maximal walls are positive and no nonadjacent ones meet. Thus it is a strictly simple ten-wall disk of gap type (1,1,8). The rectangle-union description follows by taking the open horizontal sections in the bands cut by 0,b,c,h,H. No unbounded-metric classification is inferred from one control.

Use the independently accepted arbitrary-real L theorem, including its two separate constructions reflecting only in vertical walls or only in horizontal walls. Also use the independently accepted U construction in all-heights.md, not just the bare all-pair eight-wall conclusion. We need these particular facts from that construction:

* For opposite arm endpoints, it has one common slope, one reflection in the base floor, and otherwise only vertical reflections. Each arm's heights run monotonically from its endpoint towards the base; no arm roof is contacted. Its base portion stays strictly below the arm portal level and its floor reflection avoids both base corners.
* If one endpoint is strictly in the base and the other in an arm, the proof uses the vertical-reflection-only L construction. It avoids the artificial horizontal cap of that L. Same-column and base-interior cases use direct segments when appropriate.
* Endpoints on the internal arm/base level belong to the corresponding arm. Opposite endpoints on that level use the U construction, not a segment along the notch wall.

All these statements, including finite contacts, exact target attainment, strict corner guards and unequal real metrics, were checked in all-real-U-dependency-review.md. No bound on reflection count is imported.

## Region G: transfer of the particular U construction

Remove the lower leftward extension of P and put

    Q=([0,a]x[b,H]) union ([0,A]x[h,H]) union ([w,A]x[0,H]).

Q is a U room after the isometry (x,y)->(x,H-y). Its arm widths are a and A-w, its notch width is w-a, its base height is H-h, and its two arm roofs in that chart have heights H-b and H. All are positive, with roofs above the base. G is contained in the interior of Q. In particular a mark with y=h is interior there only when x<a or x>w, exactly as in the accepted U endpoint convention.

The only open Q wall that is not a genuine P wall is

    x=w, 0<y<c.

Its endpoint (w,0) is likewise not a P corner. The Q bottom wall y=0, w<x<A, is a genuine part of P's bottom wall; all other Q walls are genuine P walls or their subsegments. The point (w,c) is a true P corner lying on Q's inner wall, so it must be avoided separately, not treated as smooth.

Apply the accepted U proof to the actual S,T in G. For opposite arms, its reflected vertical coordinate decreases from each arm mark towards the base; hence in the original coordinates each arm portion increases in height from its mark towards h and the base above h. The left arm stays at heights at least its endpoint height, strictly above b. The right arm stays at heights at least its endpoint height, which is at least c by membership in G. Every right inner-wall reflection has height STRICTLY above that endpoint height, because the endpoint is interior in horizontal position and the connecting velocity has nonzero vertical component. Consequently those contacts have y>c, even when the right endpoint has y=c. They avoid both the artificial wall below c and the actual corner (w,c).

The base excursion stays strictly above h in original coordinates. There every x in (0,A) belongs to the actual room, its x=0,A reflections are genuine smooth wall contacts, and its one y=H reflection is on the genuine top wall away from the endpoints. It never hits the notch floor y=h. The two transparent lateral portal states retain the original U position and signed velocity matching. No artificial reflection is inserted at an interface.

For a base-interior/arm pair, the proof's vertical-only L path is monotone in original height from the arm mark towards the base mark. If it is the right arm, exactly the same height lower bound excludes y<=c on x=w; if it is the left arm its inner wall is genuine throughout. Artificial horizontal L caps are avoided because there are no horizontal contacts in this construction. All its vertical contacts above h occur on the genuine outer walls. Direct subcases stay in the interior of Q and therefore in P, including their actual endpoint positions.

Endpoints at y=h are handled as arm endpoints in the U proof. If both are at y=h on opposite arms, the U construction goes strictly above h through its base instead of following the boundary notch. Same-arm level endpoints have a direct interior segment. If one endpoint has y>h, an endpoint at y=h in an arm is also strictly interior to the corresponding L subroom. Thus no endpoint limit or artificial-boundary extension is used.

All selected paths avoid every Q corner by the accepted proof. We have separately excluded the additional P corner (w,c), and no other P corner lies in an open part of Q visited by these paths. Every contact is therefore a genuine finite P wall contact with the inherited specular velocity and actual target. This proves part (i).

## Region R: horizontal-only L transfer

R is the L room

    ([l,A]x[0,c]) union ([w,A]x[c,H]).

Apply the accepted horizontal-reflection-only L construction to actual S,T strictly interior to R. Its possible horizontal mirrors are precisely

    y=0, l<x<A;
    y=c, l<x<w;
    y=H, w<x<A.

All are genuine P wall interiors. The artificial vertical part x=w, h<y<H is never a reflection contact. The true P corner (w,h) lies on that vertical cut and is likewise never touched: an interior L trajectory cannot cross its own boundary there, and its horizontal-only construction has no vertical-wall contacts. The L corners are excluded by the accepted theorem. The other P corners either coincide with these excluded corners or are outside the path region.

No endpoint on R's artificial boundary is included in this application. For strictly interior endpoints, the inherited path retains the actual endpoint identities, one consistent slope, finite length and all specular contacts. Thus it is an original P path and proves part (ii).

## Exact uncovered placement and metric scope

Within this ordered-parameter spiral subclass, G together with int(R) covers all actual interior points. An actual point outside G lies in the lowest chamber

    B={(x,y): l<x<A, 0<y<c},

and is strictly interior to R. Therefore a pair not covered by (i) or (ii) must, after exchanging its labels, have

    T in B,
    S in int(P) with [x_S<a OR (y_S>h and x_S<=w)].

Conversely these conditions do describe the uncovered pairs: S is in G but not int(R), while T is in int(R) but not G. This explicitly retains the artificial-boundary case x_S=w,y_S>h. It must not be dropped by calling S an interior L mark.

No claim is made for these cross-chamber pairs. Nor is the strict ordering b<c and a<l asserted to exhaust all metrics of the turn word. Other turn types and all other r3 placements remain unproved here. The stress control scaled from the earlier spiral, with a=4,l=12,w=20,A=28,b=4,c=8,h=20,H=28, S=(2,6),T=(14,2), lies in this uncovered set; an isolated witness does not close it.

The candidate proves a nontrivial unbounded real-metric optical subclass of genuine three-reflex original rooms by explicit genuine-mirror avoidance. It is not a generic enlargement monotonicity or corner/hull transfer. No discovery search, new clock, census, fitting, engine, worker or git-state change was used.
