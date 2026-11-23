# Nine individually necessary reflex stops in R22

**Result.** In the original 22-wall room, each of its nine physical reflex corners is the sole forbidden contact of a distinct route from S=(0,0) to T=(2,2). At that contact the two legs continue along the same physical straight line. Eight of the routes visit no intermediate lattice point other than their respective corner. The ninth visits three, disjoint from all eight. Consequently the minimum number of physical reflex stops that intercept every such route is **exactly nine** in R22. This improves the earlier count of 18 algebraic branches: the nine separate obstructions now have explicit trajectories.

## Definitions and certificates

Consider finite billiard routes that follow the ordinary reflection rule everywhere, with one relaxation: they may pass straight across a reflex corner when the incoming and outgoing open segments both lie inside the room there. Convex corners remain forbidden. Only nonaxial routes are needed for these certificates. A route has a *support*, the set of physical reflex corners it passes through. A route of empty support is a legal shot. For a dark pair every route in this relaxed family has nonempty support; the full set of reflex corners intercepts them all.

Each table row gives two exact checks in **unmodified R22**. Launch from S and backward from T with the indicated signed velocities, for the indicated numbers of primitive steps. Each leg stops at its first forbidden event, at the stated C. The two arriving velocities are exact negatives, so reversing the second leg gives straight continuation through C. No freedom to change direction at the corner is used.

| C | Launch from S | Launch from T | Step counts S,T | Archived D8 slope source |
|---|---|---|---|---|
| (0,−1) | (−8,11) | (8,−11) | 1,3 | R22-L2-0320 |
| (0,1) | (−2,1) | (−2,−1) | 1,1 | R22-L1-004 |
| (1,−2) | (7,−4) | (−7,−4) | 1,1 | R22-L1-027 |
| (1,−1) | (9,−5) | (−9,5) | 1,1 | R22-L2-0210 |
| (1,1) | (1,1) | (−1,−1) | 1,1 | R22-L1-008 |
| (1,2) | (3,2) | (3,2) | 1,1 | R22-L1-000 |
| (3,1) | (9,5) | (9,5) | 1,1 | R22-L2-0210 |
| (3,2) | (9,2) | (9,2) | 1,1 | R22-L2-0398 |
| (4,1) | (4,7) | (4,−7) | 1,1 | R22-L1-021 |

The original directions came from the saved D8 single- and double-edit records. We compared first-corner contacts in the unedited room using D72's square permutations, then verified each stated certificate with D8's independent rational-coordinate wall tracer. The standalone checker replays the nine fixed rows, verifies their slope provenance, the exact incoming velocities and every intermediate lattice hit. The large-step leg in the first row visits (2,1) and (2,−2) before reaching (0,−1) from T. Both are legal contacts. In that row the forbidden corner is **not the midpoint**. The other eight corners are exact midpoints. [Checker](corner-support.py) · [Output](corner-support.txt) · [D8 archive](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d8-perturbation-test/README.md)

Every blocking set of physical reflexes must contain C for the row supported on {C}. All nine together suffice because the original pair is dark. More strongly, even if arbitrary lattice points other than S,T can be declared blockers, at least nine are needed to intercept these nine relaxed routes. Their intermediate lattice-site sets are pairwise disjoint. This count makes no assertion about blockers at nonlattice points.

**A physical repair at each corner.** Fill a small axis-aligned square in the missing quadrant at C, with one vertex at C. For every row above, any side length 0<ε≤1/12 suffices to make its entire route legal. Indeed the original rays never enter the missing quadrant, and their straight continuation across C becomes interior. The only other way the edit could spoil a route is by removing a wall contact on one of the two short segments adjacent to C. On a vertical integer wall a distinct contact has ordinate differing from the integer corner ordinate by at least 1/|p| for primitive velocity (p,q); unfolding the integer walls proves this directly. On horizontal walls the analogous gap is at least 1/|q|. Here all absolute components are at most 11. The checker also replays each full shot at ε=1/12 by scaling the room by 12 and filling exactly one prescribed grid cell. These are local repairs, not reductions to fewer walls.

## What the single-class failure tells us

Label a nonaxial route by the parity class x of the first primitive lattice step from S. For same-parity endpoints of class a we have x≠a. Throughout such a route all lattice hits have parity either a or x: integer-wall reflections preserve parities, and the developed primitive line alternates the two classes. This partitions by primitive direction parity; an even-step half-path may have its midpoint back in a.

In cov4181 the marks have parity a=(0,1). For a relaxed route whose first primitive step has parity d=(0,0), every lattice hit lies in a or d. There are zero reflexes in d and just one in a, at (6,3). Thus the reflex support of any such route is empty or the singleton {(6,3)}. This statement alone allows a legal route with empty support, or an empty route family. Separately, D66's per-target test fails at d for all four lift pairs, despite seven regular algebraic candidates there. These two observations concern different tests. Neither assigns three physical reflexes to that class. The [shortest-path audit](shortest.md) allows broken metric routes with differing direction parities on successive legs. [D66 verdict](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d66-pair-level/README.md)

**A count that avoids double charging.** For a dark pair restrict attention to the relaxed nonaxial routes just defined. Choose a subset A of the source-parity reflexes. For each of the three remaining classes x, discard routes of class x whose support meets A. Let h_x(A) be the minimum number of x-parity reflexes needed to intercept all its remaining routes. An empty family costs zero; if a remaining route has no x-reflex, the cost is infinite. The exact minimum number of reflex stops for this route family is

    min_A ( |A| + sum over x≠a of h_x(A) ).

Indeed every candidate blocking set splits into its four parity subsets, and after its a-part is fixed each remaining route can only use its own x-part. Conversely, the union of A and the three class solutions blocks every route. This identity is about the geometry of actual relaxed routes, independent of marked algebraic valency. In R22 there are no a-class reflexes and the certificates give h_x(empty)=3 in each other class.

## Remaining implication

To derive a universal lower bound this way, one still needs to prove that simultaneous darkness forces the displayed minimum to be at least nine, or obtain the nine physical corners by some weaker argument. Nine routes with pairwise disjoint nonempty reflex supports suffice. R22 realizes the stronger singleton version; cov4181 rules out inferring three stops from one failed class. The [large-area midpoint count](midpoint-clearance.md) controls which lifts belong to an algebraic component, without producing those routes. No necessity theorem for all room shapes follows from the named examples.

The d82 reachability question asks for a legal path to a regular off-class midpoint among the counted candidates. Our nine R22 certificates describe paths in the relaxed model, each stopped by a reflex corner under the ordinary rules. None certifies a reached regular midpoint in the original room. Even a legal path with a source-class midpoint would prove illumination of its pair while leaving the stronger off-class assertion open. The corner-support count supplies a possible separate contradiction to darkness; the step from the off-class candidate budget to a legal witness remains open. [Corrected counting lemma and scope](midpoint-necessity.md)
