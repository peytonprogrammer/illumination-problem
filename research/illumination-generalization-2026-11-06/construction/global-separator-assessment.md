# B02: a darkness-derived cone separator and its exact limitation

Original effort 2026-11-07 08:17:33–08:31:33 UTC, not renewed. Universal theorem OPEN. Candidate hand lemmas below require independent review. No optical search, implementation, census or room-family expansion.

## 1. Premises retain the complete original pair

Let P be any qualifying canonical45 W<=21 room, with distinct actual interior A marks S,T. Let M be its connected minimal reflection unfolding, q=4 or8, and let X,Y be the disjoint complete q-point physical lift fibers of S,T. Let Z be ONLY the genuine cone zeros of M, excluding removable physical corner lifts. The accepted cone-only full-fiber argument says: a straight Z-avoiding connection between ANY X and ANY Y supplies a legal finite physical connection between the ORIGINAL S,T, after deleting removable-corner retracing excursions. It may change the endpoint sheet, which is why the entire physical fibers are essential.

Thus actual darkness implies absence of every such X-to-Y segment. No global reversing symmetry, base factor, fixed word or quotient necessity is assumed.

## 2. Primary-source triangulation input

Nguyen, *Triangulations and volume form on moduli spaces of flat surfaces*, arXiv:1002.3279, Lemma3.3 (PDF page index8), provides a geodesic triangulation with vertex set equal to any prescribed finite set containing all cone points. His flat-surface convention explicitly permits angle2pi regular marks. Apply it with V=Z union X union Y on the closed connected translation surface M. Here genus>=1 and at least8 regular marks avoid empty-mark exceptional situations. Only this triangulation-existence statement is imported. Source: https://arxiv.org/pdf/1002.3279 .

Repeated vertices in an abstract triangle and loop edges may occur on a surface. Each open triangle is a flat embedded Euclidean triangle; no extra vertices are introduced. Denote one such triangulation by D.

## 3. Necessary cone separator, derived from darkness

Under darkness D has no X-Y edge, since its interior avoids V and hence Z. Consequently no triangle contains both an X vertex and a Y vertex.

Let K contain every vertex of Z and every edge of D whose two endpoints lie in Z. Every connected component of M minus K contains marks from AT MOST ONE of X,Y.

Proof: label each open triangle X if it has an X vertex, Y if it has a Y vertex, and neutral otherwise. A neutral triangle has only Z vertices, so all its edges belong to K. If two triangles are joined across an edge outside K, that edge has an X or Y endpoint. Both incident triangles then have the SAME label. At an X vertex every incident triangle has label X, and similarly for Y. A path in M minus K can therefore be perturbed off the finite triangulation vertices other than X,Y, and it cannot change from an X triangle to a Y triangle. There are no remaining Z vertices to pass through. This proves the assertion, including components meeting regular marked vertices.

This is a genuine consequence of actual darkness for arbitrary qualifying geometry. It does NOT say the converse: optical trajectories may cross K freely at regular edge interiors.

## 4. Wall-dependent complexity without a metric bound

Write g for the genus and z=|Z|. A closed triangulation with z+2q vertices has

    E=6g-6+3z+6q = 3(2g-2+z)+6q,
    F=4g-4+2z+4q.

If a true zero has angle2pi*m, then sum_Z m=2g-2+z. The total prong count over ALL physical corner lifts, including regular ones, is q(W-2)/2 by the accepted angle sum. Therefore

    E <= 3q(W+2)/2 <=276,   F<=184.

In particular K has at most276 edges, independent of k and all lattice lengths. This bound is deliberately conservative. No bound on its holonomy vectors, embedding type relative to the physical mirror seams, or necessary reflection count follows. Compared with the earlier directionwise92-edge skeleton this is a different, multi-direction geometric separator, but bounded combinatorial complexity alone is not universal optical progress.

When Z is empty, K is empty and M is connected, contradicting separation of nonempty X,Y. This recovers only the already familiar torus case, not a new wall threshold.

## 5. A stronger local optical obstruction across a separator edge

Suppose a Z-Z edge has, as its incident triangles, one with opposite vertex x in X and one with opposite vertex y in Y. Develop the two triangles across that edge, putting its endpoints at(0,0),(L,0), L>0, and writing

    x=(u,v), v>0; y=(r,-s), s>0.

The straight x-y chord meets the shared support at

    c=(s*u+v*r)/(v+s).

If 0<c<L, the two portions of that chord lie in the open convex triangles and meet the common edge strictly inside it. Their union is an actual straight Z-avoiding X-Y segment. Cone-only full-fiber transfer then illuminates the ORIGINAL physical S,T. Coincident abstract edge endpoints on M cause no problem: the chord stays away from those endpoints and uses only the two face interiors and the regular interior of the edge.

Hence actual darkness forces, at EVERY such neighboring X/Y pair,

    s*u+v*r <=0  OR  s*u+v*r >=L(v+s).       (*).

This is a finite metric condition for a FIXED triangulation, not just graph separation. Equality corresponds to a forbidden cone hit. If the developed two-triangle quadrilateral is strictly convex, (*) is impossible and there is a legal connection. Conversely no direct two-triangle route follows from a failed crossing gate.

For the first branch c<=0, the two face angles at the left cone endpoint sum to at least pi; for c>=L the analogous right sum is at least pi. This follows from the elementary criterion for the alternative diagonal of two Euclidean triangles to cross their common edge. The same follows by comparing the polar angles of(u,v) and(r,-s) about the designated endpoint.

Each participating triangle has exactly one Z-Z edge, so different neighboring X/Y interface edges consume disjoint face corners. Charging pi at the blocking endpoint gives ONLY an UPPER bound on the number of these interfaces by twice the available total cone multiplicity. It yields no lower bound on W. Neutral triangles can also separate colored regions without ANY immediately neighboring X/Y triangles, making the local test vacuous there.

## 6. Peer's qualifying test defeats bare separation

Peer R59 proposes the already independently accepted illuminated14-wall branched-diagonal room R58, with actual S=(-998,0),T=(0,8). The straight proper crosscut from(-2,2) to(2,-2) has true reflex endpoints and interior in the central square. Its full preimage in M is a cone-to-cone geodesic graph separating EVERY X lift from EVERY Y lift: a path avoiding that preimage would project to a path in the physical disk avoiding the proper crosscut, contrary to planar separation.

The independently checked actual996-bounce trajectory crosses the cut transversely at(-8/5,8/5), on its final leg. Thus even a full-fiber, physically descending, canonical14-wall cone separator is compatible with actual illumination. This does not refute the one-way necessary lemma. It refutes using the separator ALONE as a wall-count or darkness certificate. The peer's frozen R59 report must be independently checked before its receipt is inherited; the geometric calculation here is also directly inspectable from the R58 boundary and final line y=4x+8.

Local source-target triangles may detect some crossings, but there is no argument that an arbitrary separating triangulation has an immediately flippable X/Y pair. Neutral triangles and same-color chains are not eliminated by Euler counts. Flipping through many triangulations introduces unbounded period/embedding data. A bare appeal to flip connectivity would only re-express the original geodesic-existence problem.

## 7. Assessment and unresolved implication

The valid forward statement is: actual darkness forces a bounded cone-saddle separator in EVERY prescribed marked geodesic triangulation, together with (*) at every adjacent source-target interface. This preserves all actual fibers and covers diagonal and branched rooms without extra geometry assumptions.

The requested stronger implication remains unproved: that EVERY canonical45 W<=21 physical quotient and original pair must violate this condition somewhere, perhaps after a bounded, justified change of triangulation. Neither E<=276, angle charging, nor the existence of a graph cut establishes it. The R59 calibration proves why the weakest proposed reduction must be abandoned. No all-word counterexample or new universal illuminated family is claimed.

Do not invest in a triangulation enumeration or flip engine on this evidence. Continue this route ONLY if a new physical-quotient/metric argument forces an actual X-Y chord rather than another bounded graph description. The elementary separator lemma may be a useful dependency, but it is not counted as a substantive advance toward22minimality by itself. Native objective and accounting remain unfinished.
