# Every remaining c2 dark thin comb reduces to five explicit families

A42 structural candidate, pending independent review. Classification is not an illumination proof and does not complete the universal goal. The reduction below is NECESSARY for actual darkness; none of its normal forms is asserted dark.

## Domain and normalization

Let P be an integer two-sided rectangular-spine comb with core width2, every tooth width1 and height2, positive gaps on each side, opposite-side overlap allowed, and at most21 maximal straight walls. Suppose two distinct ACTUAL interior A points are dark.

The accepted A39 placement argument still applies: all possible A points outside the strict core are middle-row seams; core/core, core/seam and opposite-seam pairs are directly visible. A possible dark pair therefore lies on the same seam, in two different teeth. If the global core's left coordinate were odd, both seams would have odd x and all A points would be strict-core, an immediate contradiction. Thus the core's left coordinate is even. Reflect horizontally about its middle if needed, and order endpoints vertically. Normalize it to [0,2]x[0,G], with actual S=(2,s),T=(2,t),0<s<t<G.

Set h=(t-s)/2, mu=(s+t)/2. A38 and the actual zero-depth chart twists in A39 force

    h,mu,G all divisible by2.                              (1)

This step is OPTICAL and is independently accepted in A39's proof before its c>=3 counting step; that counting step is not being imported for c2. In each of the four actual end charts, failure of2|H_* gives a real shifted seam path. Darkness therefore forces(1), and then s=mu-h,t=mu+h are even. Since the original actual A ordinates are even, the translating global bottom is even as well. The normalization is an actual A-preserving integer translation and isometry.

Both selected teeth are NONFLUSH: their centers s,t and G are even, while their edges are odd, excluding an edge at0 orG. The four physical levels

    h,mu,G-mu,G-h                                           (2)

must all be opposite-side mouth endpoints by A38. There are at least three distinct levels in(2). Every one is even. A blocking opposite tooth therefore has even band edges and has no actual A midpoint. There must be at least TWO such blocking teeth.

## Wall budget and possible blocker types

Use the exact accepted charge W=4+4N+2F. Since W is even and at most21,

    2N+F<=8.                                               (3)

The selected two nonflush teeth use4 units of(3), leaving at most4 for ALL other teeth. On the opposite side at most one tooth is floor-flush and one ceiling-flush. A height2 tooth cannot be flush at both ends because the two selected separated teeth imply G>4.

Cover at least three distinct levels with height2 mouth endpoints. The only budget possibilities are:

A. TWO nonflush blocking teeth, cost4; no other tooth can exist.
B. ONE nonflush and ONE flush blocking tooth, cost3; at most one additional flush tooth could exist before checking geometry.
C. ONE nonflush and TWO flush blocking teeth, cost4; no other tooth can exist.

Two flush teeth alone have only the two eligible interior endpoints2,G-2 and cannot cover at least three levels. Three blocking teeth of any other type exceed the remaining budget; four or more also exceed it. If a third tooth is not needed for the endpoint cover, it still consumes the same budget and is included as the possible extra flush in B. Thus the case list does not silently remove unused attachments.

All normal forms below have the selected right teeth [2,3]x[s-1,s+1] and[2,3]x[t-1,t+1]; every listed opposite band denotes a left tooth[-1,0] over that band. There are NO additional teeth after the following case analysis.

## A. Two nonflush blockers

Let q=min(s,G-t)>=2 and d=|s-(G-t)|>=0. Both are even. The sorted levels(2) are

    h, h+q, h+q+d, h+2q+d.                                (4)

For d0 there are three distinct levels; for d>0 there are four. A height2 blocker can cover two distinct levels only when their difference is2. With two blockers covering three or four levels, at least one must cover a pair. In(4), q>=2 and d is nonnegative even. For four distinct levels each blocker must cover two; disjoint positive-gap bands can only pair the two lower and the two upper levels. Hence q=2. For three levels a paired adjacent difference is q, so again q=2. A nonadjacent pair cannot work: its difference is at least4.

Reflect y if necessary to arrange s=q=2. Then

    t=2h+2, G=2h+d+4.

If d>0, each blocker covers two levels and its band is forced. This gives normal form A1:

    h EVEN>=2, d EVEN>=2,
    core height G=2h+d+4,
    S=(2,2), T=(2,2h+2),
    right bands [1,3], [2h+1,2h+3],
    left bands [h,h+2], [h+d+2,h+d+4].                    (A1)

Every parameter choice is an actual strict room; opposite-side bands may overlap. All four teeth are nonflush and W=20.

If d0, the three levels are h,h+2,h+4. A blocker covering the lower pair is[h,h+2]; its partner must use h+4 as its LOWER endpoint, since[h+2,h+4] would touch the first band, violating the positive gap. It is therefore[h+4,h+6]. Pairing the upper two instead gives the vertical reflection of this form. Nonflushness requires h>2, yielding A0:

    h EVEN>=4,
    core height G=2h+4,
    S=(2,2), T=(2,2h+2),
    right bands [1,3], [2h+1,2h+3],
    left bands [h,h+2], [h+4,h+6].                        (A0)

All four teeth are nonflush and W=20. The accepted A41 candidate, once its independent acceptance is reconciled, covers h>=6 in A0. It does not include h4. The h2 endpoint would be flush and belongs to case B, not A0.

## B. One nonflush and one flush blocker

By vertical reflection take the flush band to be[0,2]. Its only eligible interior candidate endpoint is2, so the smallest turning level is h=2. If all four levels were distinct, the remaining one nonflush tooth could not cover the other THREE. Thus mu=G/2 and there are exactly three levels2,G/2,G-2. The nonflush tooth must cover the latter two and has height2, forcing G/2-2=2 and G=8. This is the single normal form B:

    G=8, S=(2,2), T=(2,6),
    right bands [1,3], [5,7],
    left bands [0,2], [4,6].                              (B)

It has W=18. The remaining one unit of wall budget could only add a flush tooth. No such tooth is geometrically allowed: a left ceiling band[6,8] touches[4,6], and a second left floor band duplicates[0,2]; a right floor band[0,2] overlaps[1,3], while a right ceiling band[6,8] overlaps[5,7]. Same-side positive gaps exclude all four possibilities. Thus B has no hidden extra attachment.

## C. Both opposite flush blockers plus one nonflush

Both flush bands are[0,2] and[G-2,G]. Their only eligible interior endpoints force h=2 again. The remaining distinct inner levels mu,G-mu must be endpoints of the nonflush blocker.

If they differ, their difference must be2. After vertical reflection take mu=G/2-1. Since mu is even, G=10+4r,r>=0, where the lower bound follows from positive gaps and s=mu-2>0. This gives C1:

    r>=0 integer, G=10+4r, mu=G/2-1,
    S=(2,mu-2), T=(2,mu+2),
    right bands [mu-3,mu-1], [mu+1,mu+3],
    left bands [0,2], [mu,mu+2], [G-2,G].                 (C1)

If mu=G/2, then G is divisible by4. The inner level is one endpoint of the nonflush band; choose[mu,mu+2] up to vertical reflection. Positive separation from[G-2,G] forces mu+2<G-2, hence G>=12. This is C2:

    r>=0 integer, G=12+4r, mu=G/2,
    S=(2,mu-2), T=(2,mu+2),
    right bands [mu-3,mu-1], [mu+1,mu+3],
    left bands [0,2], [mu,mu+2], [G-2,G].                 (C2)

In both C cases N3,F2 and W=20; the wall budget allows no extra tooth. Each displayed parameter choice satisfies all same-side positive gaps. Opposite-side overlaps are permitted and are not omitted.

## What this proves and what it leaves open

Every possible dark pair in the complete stated c2 thin-comb W<=21 class is carried by an actual endpoint-preserving Euclidean isometry to ONE of A0,A1,B,C1,C2, with the ENTIRE room equal to that normal form. This is not only an embedding of a small subroom into a larger unknown room. There is no bound on h,d,r. All normal forms have exactly TWO actual interior A points: strict-core x1 is odd, selected right seam midpoints are the two marks, all blocking opposite tooth centers are odd, and unit-width teeth have no other integer interior x coordinate. This support count is derived from actual darkness and the budget, not assumed.

These are necessary cases only. An exact positive path on one sample does not close its family. A0,h>=6 has an independently reviewed six-residue continuation proof in the separate A41 packet; A0,h4, all A1, B,C1,C2 require explicit optical closure and independent review. Proving those closures would settle this c2 thin-comb class, not c1 combs, wider/taller teeth or arbitrary canonical45 polygons. The main goal remains OPEN.
