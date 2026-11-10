# A three-copy geometric proof for the 22-wall room

2026-10-31. Status: exact geometry checked; hand argument below sent to Claude
for independent review. This proof gives a hand alternative to the 2,592-state calculation on the
60-square physical unfolding, using a
parity lemma and two folds. No ray searches are used.

## The base staircase

Let P be the union of five closed unit squares with lower-left corners

    (-1,-1), (0,-1), (0,-2), (1,-2), (1,-3).

Mark a=(0,0) and b=(2,-2). They are smooth boundary points of P.
P has ten walls. Its complete integer-point census is:

- Seven convex right-angle corners.
- Three concave 270-degree corners.
- The two smooth marked boundary points a and b.
- No interior integer points.

In particular, every integer point of P other than a and b is a polygon corner.
Both marks have two even coordinates.

**Parity lemma.** No ordinary billiard trajectory connects a to b in P.

Suppose one did. Reflect P across each wall encountered to straighten the path.
Every wall is an integer horizontal or vertical line. Such reflections preserve
both coordinate parities of integer points. Therefore every unfolded image of b
has two even coordinates. Starting at a=(0,0), write the nonzero displacement to
that image as k(p,q), with p,q coprime integers. Since the displacement is even in
both coordinates, k is an even positive integer. The intermediate point (p,q)
occurs strictly before the target. It is an integer point with at least one odd
coordinate. Folding it back preserves parity, so it cannot be a or b. The census
says it must be a polygon corner. An ordinary billiard trajectory cannot pass
through that corner: contradiction.

This argument permits any number of ordinary wall reflections. A connecting
trajectory necessarily has rational direction because its unfolded endpoint has
integer coordinates; irrational directions cannot evade the argument.

## Allowing convex-corner continuation still cannot connect the marks

At a convex right-angle corner, unfolding permits a straight continuation. Its
physical projection reverses velocity and retraces the incoming trajectory.
Allow such retroreflection at any subset of convex corners; retain the rule
that concave corners stop trajectories.

Suppose a finite generalized trajectory connected a to b. Take the last visit
to a before the first arrival at b. If the remaining portion met a right-angle
corner, its first such encounter would reverse it along precisely the same
ordinary reflections back to a, before reaching anything new. This contradicts
the choice of the last visit to a. Thus the remaining portion contains no corner
continuations and is an ordinary trajectory from a to b. The parity lemma
excludes it.

The argument also applies when a and b lie on smooth boundary edges: ordinary
bounces on those edges are reversible. Compare Wolecki, *Illumination in Rational
Billiards*, Remark 2.2, for the same retracing principle at removable corners:
https://arxiv.org/html/1905.09358v3

## Assemble the actual room

Take three copies of P in the plane:

    P0 = P,
    P1 = {(x,-y) : (x,y) in P},
    P2 = {(4-x,-y) : (x,y) in P}.

Their square interiors are disjoint. Glue P0 to P1 along the full wall
[-1,1] x {0}, and P1 to P2 along {2} x [1,3]. These are the only shared edges.
The resulting union is exactly Claude's saved 15-square room.

The first seam makes S=(0,0) interior; the second makes T=(2,2) interior.
The boundary is simple and has no holes or point contacts. Starting with thirty
walls, the two glued pairs remove four walls. Four joins of exterior wall pairs
are straight and merge, removing four more: 30-4-4=22.

Fold the three copies onto P by

    f0(x,y)=(x,y),
    f1(x,y)=(x,-y),
    f2(x,y)=(4-x,-y).

These maps agree pointwise along each seam. Both copies adjacent to S send S to a;
both adjacent to T send T to b. There are also smooth boundary preimages of
the base marks: (4,0) maps to a and (2,-2) maps to b. Visits to these points
are ordinary visits to the corresponding base mark. If b were reached before T,
the path prefix would already contradict the base nonillumination lemma.
An axis-parallel path in the original room cannot connect S=(0,0) to T=(2,2):
horizontal and vertical reflections keep its zero velocity component zero. All
remaining possible directions have both components nonzero and cross the seams
transversely. Crossing a seam becomes an ordinary specular
reflection in a wall of P. An ordinary exterior-wall bounce also projects to an
ordinary reflection.

There are exactly four seam endpoints:

    (-1,0), (1,0), (2,1), (2,3).

Upstairs, they are smooth boundary points: two right-angle sectors join to form
a straight 180-degree sector. Downstairs, each maps to a convex right-angle
corner of P. A bounce at such an upstairs point can therefore project to the
retroreflection allowed in the preceding lemma. Locally, the actual wall
reflection composed with the perpendicular seam reflection is -I, reversing
both velocity components. Every preimage of a concave base corner is an actual
corner upstairs, so a valid upstairs path cannot pass through one.

Consequently, any valid upstairs billiard path from S to T would project to a
generalized path from a to b in P, using ordinary reflections and possibly convex
retroreflections. The strengthened parity lemma rules it out. Hence S and T do
not illuminate each other in the strictly simple 22-wall room.

**What the four exceptions do:** they are seam endpoints that become smooth
when the copies are joined. Folding turns their potentially dangerous bounces
into retracing events; they add no route between the base marks.

## Exact checks and relation to the finite certificate

`geometric-proof-check.py` checks the unit-cell union, disjoint copy interiors,
complete base integer-point census, two seams, agreement of fold maps, all four
exception fibers, concave-corner fibers, both marked-point images, and both wall
counts. It passes. Inputs and full geometry results are in
`geometric-proof-check.json`. Run:

    .context/illumination-venv/bin/python -B \
      .context/illumination-k4-codex/geometric-proof-check.py

The previously verified finite proof independently confirms the conclusion. Its
60-square surface maps with degree three onto the 20-square unfolding of P.
Four convex base corners must be allowed to continue because they have smooth
upstairs preimages. Even with every ambiguously blocked fiber made transparent,
the quotient closes in 72 states and stays dark. The geometric proof explains
why those transparent fibers remain harmless. The 72-state count belongs to the
20-square base quotient; the 2,592-state count belongs to the physical unfolding.

The earlier
<=3-exception theorem remains intact; this room has four exceptions.
