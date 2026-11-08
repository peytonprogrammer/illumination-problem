# Ear deletion: exact geometry, complexity and availability conditions

Independent reviewer continuation, Codex01a1a00f. This complements the P1/P2 controls in geometric-reduction-prerequisites.md. It does not assert optical transfer or global reduction availability.

## E1. A strict full-side rectangular ear has a controlled geometric deletion

Let Q be the closed region of a finite strictly simple orthogonal lattice room. Let E be a nondegenerate closed axis-aligned lattice rectangle. Assume all of the following, explicitly:

1. Q and E have disjoint interiors, and Q intersect E is EXACTLY one full side J of E, a nonzero segment in the boundary of Q.
2. The relative interior of J lies in one maximal straight boundary wall of Q. At each endpoint of J the Q interior angle is90 or180 degrees; no Q reflex vertex lies there.
3. D=Q union E has a strictly simple boundary, with no extra contacts. Equivalently the local interior sectors on J and its endpoints form the indicated single polygonal region and the remainder has no touching components.
4. Both actual endpoints S,T lie strictly inside Q. A sufficient condition given interior endpoints of D is that neither lies in the CLOSED ear E.

Then deletion D->Q preserves the orthogonal lattice disk class and the actual distinct interior even-even marks. Every boundary segment remains a canonical tiling edge. There is no fractional chord or parity normalization issue for this specific operation.

Let j be the number of endpoints of J having Q angle180. At each such endpoint, adding E contributes90 more degrees, so it creates a reflex270 corner. At a Q-angle90 endpoint, adding E changes90 to180, removing a convex corner but adding no reflex. The two free outer corners of E are convex. All other corners of Q persist. Therefore

    r(D) = r(Q) + j,     j in {0,1,2}.

This proves r cannot increase on deletion, but strict decrease is NOT automatic. In terms of maximal walls, W(D)-W(Q)=2j by the orthogonal turning equation. Any r-induction must require j>=1, or separately handle j=0.

The lexicographic pair (r, area) is an alternative well-founded measure on this lattice class: both entries are nonnegative integers, r never increases, and area(Q)=area(D)-area(E) is strictly smaller. An orthogonal integer-vertex polygon has integer area, for example by decomposition at its finitely many x-coordinates into integer-height rectangles. Lexicographic order on N x N is well-founded: r can decrease only finitely often, and once r is constant area cannot decrease infinitely. This remains a geometry-only reduction until illumination transfer is independently proved.

This statement concerns an ear attached along a FULL rectangle side, not a rectangular chamber joined through a proper subsegment with two overhangs, an ear meeting two walls, a slit collapse, or a corridor surgery with extra contacts. Such operations need their own angle and topology calculations.

## E2. A mark on an open mouth can be an actual interior point

Use Q=[0,8]x[0,4] and E=[4,8]x[4,8], glued along J=[4,8]x{4}. Their union D has boundary

    (0,0),(8,0),(8,8),(4,8),(4,4),(0,4).

It is a six-wall strictly simple orthogonal lattice room with r=1. S=(6,4) lies in the relative interior of J and is strictly INTERIOR to D: a ball of radius less than2 lies inside the union, with Q below the seam and E above it. T=(2,2) is also a distinct actual interior even-even point.

Deleting E leaves S on the boundary of Q, so the transformed pair fails the induction domain, even though S is not in the OPEN ear interior. Thus a test that rejects only endpoints strictly inside an ear is insufficient. It must also reject actual marks on the mouth and any surviving seam points that become boundary. This is an exact domain failure, not a broken-ray argument.

For this operation j=1: the mouth endpoint(4,4) lies in the interior of Q's top wall and becomes reflex in D; endpoint(8,4) is a Q convex corner and becomes smooth. Thus r(D)=r(Q)+1 as E1 predicts. The endpoint condition is an independent requirement beyond complexity decrease.

## E3. Global ear availability is a quantified geometric theorem

A valid local deletion lemma does not prove that an admissible ear exists. Even ignoring optics, one must quantify over the marked room, not choose a decomposition whose cuts avoid marks without proving such a decomposition exists.

A limited sufficient counting statement is available: suppose a decomposition into chambers has a tree adjacency graph with at least three leaves, and the CLOSED leaf ears (including their mouths) are pairwise disjoint. At most two of these ears can contain one of S,T. Therefore at least one closed leaf ear is endpoint-free. If it also satisfies E1's attachment and angle conditions, it is geometrically deletable with the stated measure. This conditional count is valid even when a mark lies on a mouth because closed ears are counted.

Its hypotheses are substantial. A path-shaped decomposition has only two leaves, and both may contain endpoints, as P1 already exhibits. More generally a thin corridor with both endpoints in terminal chambers need not have an unused terminal ear. Intersecting closed mouths require a separate bound on how many ears one endpoint can protect. A tree of chambers alone is not a certificate that the needed rectangles, disjoint closed ears or strict reflex decrease exist.

The area alternative does not repair endpoint loss: a smaller room with an original mark on its boundary is outside the induction domain. Conversely endpoint preservation does not repair missing strict r decrease. These guards must be proved separately before discussing optical transfer.

## E4. Exact transfer premise still absent

For D=Q union E, a legal path in Q that avoids J and its endpoints, with every contact on an unchanged wall interior and open legs inside D, transfers literally. However existence of SOME ray in Q does not imply existence of one avoiding J. P2 shows that even a smooth artificial bounce on J need not be replaced by a matching single-ear excursion without a precise compatibility condition.

A proposed induction must prove an existence-level replacement result: either select a Q witness with the required avoidance/compatibilities, or construct another legal path in D whose actual start and target agree with S,T. A failure of one chosen word or ear excursion does not reject that stronger possibility. No such global existence theorem has been proved in these prerequisite notes.

The independent next challenge is the author's specific quantified surgery and its claimed existence-level transfer. In its absence, E1-E3 supply checkable constraints and exact domain countercontrols, not a complete solution or a reason to declare the native goal finished.

## E5. Endpoint-protected leaves also occur beyond the small base cases

One fixed hand-constructed control has four rectangular chambers

    R_j=[4j,4j+4]x[4j,4j+6],  j=0,1,2,3,

joined consecutively along width2 vertical mouths. Its boundary is

    (0,0),(4,0),(4,4),(8,4),(8,8),(12,8),(12,12),(16,12),
    (16,18),(12,18),(12,14),(8,14),(8,10),(4,10),(4,6),(0,6).

This is a strictly simple orthogonal canonical disk with16walls, r=6, area96. Its actual interior even-even pair S=(2,2),T=(14,16) lies in the two terminal chambers. This particular exact chamber graph is a path, whose only leaves both contain endpoints; deleting either terminal chamber loses its actual mark. The example lies beyond the accepted W<=8/r<=2 base, so protected leaves are not confined to the r1 base-control phenomenon.

This does not exclude another decomposition, a different subroom, nonterminal surgery or direct illumination. Indeed its actual endpoints connect directly: y=(7x-2)/6 crosses x=4,8,12 at heights13/3,9,41/3, strictly inside mouths(4,6),(8,10),(12,14). Within each chamber the affine height lies strictly between its horizontal walls, and crossings lie inside the union. Thus the example is LIT. The claimed failure is only that endpoint-free leaf availability cannot be inferred from this room's tree decomposition alone.

The two controls are independently reproducible with geometric-reduction-ear-conditions-check.py/json. They are prescribed hand constructions, not outputs of a room census or optical search. The r6 control is a general-availability discriminator, not an attempt to extend a comb catalogue.
