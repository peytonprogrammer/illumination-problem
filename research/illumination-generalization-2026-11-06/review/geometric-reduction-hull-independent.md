# GR-author-02: independent review of global geometric availability

Verdict: **ACCEPT the geometric H/V/C1 reduction system, with the full room and endpoint hypotheses.** This proves geometric availability and a well-founded reflex decrease, not existential optical transfer or illumination. The durable goal remains unfinished.

Read both frozen GR-author-01 and02 requests and all their pinned files. The eight distinct source-file hashes match before and after the independent controls. The author checker was not run. Own prescribed controls are geometric-reduction-hull-independent-check.py/json; they deterministically construct horizontal and vertical band hulls of five already specified polygons, never enumerate rooms or rays.

## 1. Strict simple disk, lattice and actual endpoints — ACCEPT

List all vertex heights. For every open band between consecutive heights inside the y-support, a horizontal section of D is a constant finite union of positive-length intervals with integer endpoints. Connectivity of the open interior implies that the y-support has no gap. Across any internal critical height, a path inside the old room from below to above supplies an open neighborhood of a crossing point. Consequently the two adjacent band sections, and hence their interval hulls, overlap in positive length. This uses actual interior connectivity; point contacts alone would not suffice.

Glue the finitely many closed hull band rectangles. Positive overlap gives a connected interior and left/right step boundaries with no pinches at interfaces. A hole would have an open horizontal slice missing between occupied portions, contradicting the interval sections. The explicit left and right chains plus top and bottom edges form a Jordan polygon; merging collinear edges gives its maximal walls. The construction therefore yields a finite strictly simple orthogonal disk. All x-extrema and y-breaks are original integer coordinates, so it stays in the canonical tiling class.

Original D is contained in the hull, including its critical-level boundary points by closure of its interior. Thus both original actual interior marks stay interior, remain distinct and retain even-even coordinates. No assumptions about marks lying away from a rectangulation seam are needed for these enlargements. Exchanging x,y proves the same facts for V(D).

## 2. Horizontal charge, cap reuse and simultaneous heights — ACCEPT with an independent wall-injection proof

For original maximal horizontal walls let C,M,R be the counts having0,1,2 reflex endpoints, respectively. Every corner belongs to exactly one such wall, so

    c=2C+M,  r=2R+M,  C=R+2.

Instead of relying only on a chosen charge for each moving extremum, the following proves the required inequality by entire output walls.

**Wall lemma.** Every maximal horizontal wall of H(D) contains, along its relative interior, one ENTIRE original horizontal wall with fewer than two reflex endpoints. Distinct output walls receive distinct original walls.

First, an original horizontal wall W has old interior on one side of its support and old exterior on the other. Immediately on the exterior side, the generic old section has no points with x strictly between W's endpoints. Its interval hull either covers W's entire open x-interval (because old components occur on both sides) or covers none of it. An interval endpoint cannot fall strictly inside W: it would be an endpoint of a nonempty old section there, contradicting the exterior neighborhood on that side. Thus W's entire relative interior is either exposed on the hull or covered; it cannot be split between two exposed hull walls.

Next, take an output horizontal wall J. For an internal left or right envelope jump, the old interval achieving the relevant extremum extends a positive distance into J on the occupied side of that critical height. On the other side the hull is absent there. Hence an original horizontal boundary interval occurs within J. For the global bottom/top wall this is even more direct: an old extreme cap lies inside it. By the preceding paragraph this original maximal wall is exposed WHOLE within J.

An original R-R wall cannot be exposed: immediately on its old exterior side there are old interior intervals beyond BOTH endpoints, by the two reflex sectors. Horizontal hull completion bridges the gap and covers the wall. Therefore the chosen old wall is of type C or M. Distinct output horizontal walls cannot share a positive-length exposed old wall, yielding an injection into the C+M old non-R-R walls.

Every strictly simple orthogonal polygon with r_h reflex corners has r_h+2 maximal horizontal walls. Therefore

    r(H(D))+2 <= C+M = R+2+M,
    r(H(D)) <= M+R = r(D)-R.

This also resolves cap reuse: a cap cannot supply two distinct output walls, because its entire relative interior has one exposure status. It automatically treats multiple old walls at the same height. Their disjoint relative interiors remain separate objects; no perturbation of heights, room or marks is used. A new bridging wall may incorporate several old exposed walls, which only strengthens the injection bound.

This is an independent justification of the author's claimed estimate. It avoids assuming that counting an exposed endpoint alone has already supplied a unique global charge. The author's conclusion needs no correction.

## 3. A changed horizontal hull has R>0 — ACCEPT

If R=0, then C=2. A global lowest horizontal boundary cap and a global highest cap are necessarily convex-convex, and these are distinct because the room has positive height. Thus the two available caps are exhausted by global bottom/top events. No internal cap can create or terminate a section component, and no R-R wall can split or merge components. Mixed walls only move one endpoint. Local events at the same height occur on disjoint boundary intervals, so their count changes add; strict simplicity excludes an unrecorded pinch connection.

Starting with the one interval just above the unique bottom cap, all generic sections remain single intervals up to the top. Hence horizontal completion is unchanged. The contrapositive gives H(D)!=D => R>=1, and the estimate in section2 gives strict reflex decrease. If generic sections are already intervals, there is no additional critical-level change: the original disk is the closure of those band interiors. The vertical analogue follows identically.

## 4. Both-axis convexity gives the fully isolated C1 rectangle — ACCEPT

If both kinds of generic sections are intervals, no horizontal R-R wall exists: the two exterior-side intervals at its reflex endpoints would form a disconnected section. Likewise no vertical R-R wall exists. Therefore every reflex corner has convex neighbors on both incident edges.

Choose one and put its local geometry in the C1 coordinates C=(0,0), A=(0,H), B=(L,0), H,L>0, with interior west of AC and south of CB. For each0<y<H, the horizontal section contains AC as its right endpoint; it has no D point at x>0. For each0<x<L, the vertical section has CB as its top endpoint; it has no D point at y>0. These statements exclude the open rectangle and the open top/right replacement sides, including isolated boundary contacts there.

For rigor at V=(L,H), the two forbidden strips also settle the connectivity issue. The open interior of D cannot meet the closures of either forbidden strip: any such interior point would have a small ball meeting the strip. If V were in D, closed-polygon regularity would give interior points arbitrarily near it. The southwest, northwest and southeast neighborhoods of V are excluded by the two strips, leaving only the northeast quadrant. But the northeast allowed component x>L,y>H is separated from the old interior near C (west/south of the strips). An interior path cannot connect those components without crossing a forbidden strip or its boundary; a corner-only connection is not interior connectivity. Contradiction. Thus V cannot contact D either.

All C1 isolation hypotheses are satisfied. Its already independently checked geometric proof removes exactly one reflex corner and preserves the actual marks and strict lattice disk.

## 5. Global geometric induction — ACCEPT; optical induction — OPEN

For every nonconvex room, either H changes it and strictly lowers r, or V does, or both sections are convex and an isolated C1 move is available. Every move preserves the geometric target class and literal S,T. Repeating such moves terminates by the nonnegative integer r, with a rectangle at r=0. The direct interior segment proves the actual convex base.

This is a complete GEOMETRIC reduction system with no area, diameter, support or exception bound. It repairs C1-only availability, including the reviewer's r3 spiral and the author's r4 control. It does NOT prove that a ray in the final rectangle lifts through any of these changes. The fixed known22 C1 fill already shows that unrestricted existential transfer can fail; restricting original r<=8 remains a substantive unproved hypothesis. The exact remaining task is an existential optical theorem for an available choice of these moves on every original r<=8 room, or a different direct path mechanism. Merely naming that theorem is not proof progress on it.

## 6. Independent prescribed evidence and limits

Own band-boundary construction checks both axes on five predeclared existing polygons: known22, reviewer r3 spiral, author r4 no-C1 control, reviewer L and the prescribed square. Ten exact controls pass strict simplicity, integer supports, actual mark interiority, positive band overlap, the wall injection, the charge bound, idempotence and strict decrease whenever changed. Results include:

| Input | r | r(H) | r(V) |
|---|---:|---:|---:|
| known22 |9|8|8|
| reviewer spiral |3|1|2|
| author no-C1 control |4|0|4 (unchanged)|
| reviewer L |1|1 (unchanged)|1 (unchanged)|
| square |0|0 (unchanged)|0 (unchanged)|

These are corroborating controls. The universal geometric proof is in sections1-5, not an inference from ten examples. Known22 remains outside original r<=8. No author checker, new room/orbit/ray census, coefficient fitting, workers, frozen-source modification or native accounting change occurred. All eight distinct source pins match after verification. This independently accepted geometric milestone does not complete the reviewer goal or the universal orthogonal theorem; the general diagonal-wall canonical45 case remains separate and open.
