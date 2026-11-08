# ET01: positive flat-wall transfer, with a low-reflex availability obstruction

Author HAND proof, pending independent review. Candidate was published in endpoint-transfer-candidate-01.md after endpoint-transfer-prior-audit.md. No search, census, engine, worker or frozen edit.

## 1. Exact local physical theorem

Use the candidate's ACTUAL original D, full L-corridor Q, actual reflex C=(A,H), and actual interior marks

    S=(A+a,H-b), T=(A-c,H+d),
    a,b,c,d>0, ad=bc,
    0<a<R-A, 0<b<H, 0<c<A, 0<d<U-H.

The singular straight connection S-C-T is replaced by a path with one reflection at the physical floor y0. The hypotheses int(Q) subset int(D) and an actual smooth floor are essential; no artificial reflector is introduced.

Put u=H-b>0, v=H+d>0, D0=u+v=2H+d-b>0. Reflect ACTUAL T to Tstar=(A-c,-v). The straight S-to-Tstar line reaches y0 at positive parameter u/D0<1. Its abscissa is

    q=(v*(A+a)+u*(A-c))/D0
      = A+(v*a-u*c)/D0.

Because the weights are strictly positive,

    0<A-c<q<A+a<R.

Thus Qfloor=(q,0) is strictly inside the ACTUAL smooth floor segment. This is an endpoint image arising from that actual physical reflection, not an independently chosen cover point.

The reflected outgoing leg Qfloor-to-T intersects the interface yH at

    x_H = (d*q+H*(A-c))/(H+d)
        = A+(ad+bc-2H*c)/D0
        = A-2c*(H-b)/D0,                      (1)

where the final equality uses the corner-degenerate condition ad=bc. Hence x_H<A strictly. Moreover

    x_H-(A-c)=c*(b+d)/D0>0,

so0<A-c<x_H<A. The outgoing leg passes through the INTERIOR of the original corridor mouth; it misses the actual reflex corner C rather than continuing through a singular sector.

## 2. All signed optical and first-hit guards

Let m=(a+c)/D0>0. The incoming source-to-floor velocity is proportional to(-m,-1); the outgoing floor-to-target velocity is proportional to(-m,+1). Their horizontal component agrees, their vertical component reverses, and normalization by sqrt(1+m^2) gives one speed. There is no direction change except this single specular reflection.

The entire source-to-floor leg, except its final floor contact, lies strictly in the lower rectangle of Q: its endpoints have0<x<R and0<=y<H, with positive source height and strict x bounds. From Qfloor to the strict interface point(x_H,H), the open leg also lies inside that lower rectangle. From(x_H,H) to actualT it lies strictly inside the upper rectangle, with0<x<A andH<y<U. The interface point itself is interior to the union Q because0<x_H<A.

By int(Q) subset int(D), no other true D wall or corner can interrupt any open leg. Qfloor is the sole boundary contact and is a genuine smooth physical wall point. Both flight lengths are positive. The initial leg cannot reach T because all of its heights are below H while T_y>H; the final straight leg first attains actualT at its endpoint. Thus S->Qfloor->T is a legal finite actual point-to-point path.

The initial direction differs from that of the singular straight S-C-T candidate, as permitted. The actual S,T never change. In an unfolding, the unique floor word yields the same Tstar above; no alternate sheet is silently substituted and no mixed-direction concatenation is used.

This proves ET01 for arbitrary finite offsets satisfying its geometric hypotheses, with no epsilon limit or word search. It does not prove every developed corner-degenerate source/target prefix can be placed in such a full corridor.

## 3. The tentative A8 availability claim is FALSE already at r2

Consider the original strictly simple orthogonal lattice room

    D_notch=([2,8]x[0,4]) union ([0,4]x[2,8]),
    S=(6,2), T=(2,6), C=(4,4).

Its ordered boundary is

    (2,0),(8,0),(8,4),(4,4),
    (4,8),(0,8),(0,2),(2,2).

There are exactly two reflex corners C=(4,4) and B=(2,2). Its two rectangles overlap in a positive-area square; the boundary has no self-contact or hole. Actual S,T are distinct even-even strict interior marks. The straight S-C-T segments lie in the two arms, with C their unique actual corner contact. In the ET notation a=b=c=d=2, so ad=bc exactly.

ANY full L-corridor of the ET type at C that contains BOTH marks strictly would need its left bound strictly below x2 and its lower floor strictly below y2. Its lower/right rectangle must also reach beyond S_x6, up to C_y4. Therefore B=(2,2) would be a STRICT INTERIOR point of that rectangle, although B is an actual boundary corner of D_notch. This contradicts int(Q) subset int(D_notch). The x/y-swapped version has the same obstruction, because the room, pair and B are symmetric under that swap. These exhaust the axial frames preserving the missing-NE quadrant at C.

Thus A8, which would guarantee this full-corridor transfer hypothesis at every such event in an r<=8 room, is false at originalr2. Repeated lifts are not involved: this obstruction uses precisely two DISTINCT physical reflex corners. It is an availability failure of this sufficient corridor, not a nonterminating transition cycle or an actual dark pair.

Indeed D_notch is illuminated by the smooth actual path

    (6,2) -> (5,0) -> (2,6).

The initial leg lies in[2,8]x[0,4]. Its outgoing leg crosses y2 atx4 and y4 atx3, then stays in[0,4]x[2,8] to T. All seams are strict interior and the sole floor hit5,0 is inside the true finite floor(2,8)x0. Velocities(-1,-2),(-1,+2) and their positive continuation toT prove specularity. It avoids B and C. A weaker path-specific clearance condition can succeed even when the full rectangular corridor does not.

## 4. Calibration against accepted controls

- r2/r4 arithmetic roots previously proved are smooth actual paths. Their prefix-component boundaries are not automatically matching events. For the saved six-reflection r4 branch, at its lower and upper endpoints the developed matching defect is respectively-43/25 and377/75, neither in32Z. Thus these specific endpoint collisions are NOT fixed-target matching degeneracies and ET01 must not be applied to them. Its interior97/253 root requires no repair. The r2 smooth1/53 root similarly requires none.
- Originalr9 known22 dark room has the blocked direct connection through C0=(1,1) between actual0,0 and2,2. The Euclidean frame(X,Y)=(x-1,1-y) maps its missing-SE quadrant to missingNE and swaps the labels if desired, giving source(1,-1),target(-1,1),corner0. Any full ET-type corridor containing these marks strictly would need left bound<-1 and floor<-1, making(-1,-1) an interior point of its lower rectangle. Its inverse image is original(0,2), an ACTUAL boundary corner in the accepted22-wall contour. Therefore this specified singular connection does not satisfy ET01's corridor hypothesis. No contradiction to its inherited darkness arises. This is a direct geometric hypothesis check, not a new darkness certificate or a positive r<=8 force.

## 5. Rank/cycle and completion consequences

The local ET01 transfer SURVIVES at its exact hypotheses and ends immediately at a legal actual ray. On this restricted edge class, a rank1 singular event goes directly to rank0 legal completion. Such edges cannot form a nonterminating cycle, since their destination is already a valid connection.

There is no COMPLETE transition system for arbitrary originalr<=8 events. A8's failure at r2 shows that missing ET01 edges cannot be declared to require nine distinct corners. It does NOT show an actual cycle with fewer than nine corners, and does not refute the universal illumination target or every broader physical transfer. No rank or nine-corner obstruction for an unproved larger graph is claimed.

Further work would need a genuinely broader physical transfer whose availability covers the missing collars and complicated source/target germs, or another actual-path mechanism. Simply adding path-specific legality as an unproved assumption, appealing to the accepted directionwise graph, or importing the old conditional convex-return existence would leave the global gap. Isolated endpoint repairs also do not address guarded intervals missing all roots strictly. The entire native objective remains unfinished.
