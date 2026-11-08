# Exact affine bridge for orthogonal wall data

Candidate hand lemma for independent peer review. This sharpens the scope report; it does not prove the uncapped canonical theorem.

## Statement

Let P be a finite strictly simple orthogonal polygon with nonempty interior, expressed in an orthonormal wall frame. Let X and Y be its finite sets of vertex x and y coordinates. Fix x0 in X and y0 in Y. An invertible global affine map that preserves ordinary Euclidean reflection at every wall can send all vertices to rational coordinates if and only if

    dim_Q span_Q {x-x0 : x in X}=1,
    dim_Q span_Q {y-y0 : y in Y}=1.

Equivalently, there are positive real alpha,beta with all vertex differences x-x0 in alpha Q and y-y0 in beta Q. The criterion concerns wall vertices; endpoints may be arbitrary distinct real interior points.

Conditional consequence: if the uncapped canonical45 W<=21 theorem holds, then EVERY polygon in this orthogonal class with W<=21 illuminates EVERY distinct interior pair. No exception-count, diameter, aspect-ratio, endpoint rationality, or denominator bound is needed.

## Necessity and sufficiency of the coordinate criterion

A nondegenerate bounded orthogonal polygon has both horizontal and vertical nonzero edges. If A preserves reflection at every wall, the accepted mirror-conjugacy lemma gives A e1 perpendicular to A e2. Put a=A e1 and b=A e2. Every horizontal polygon edge of length ell has rational image displacement ell a; every vertical edge of signed length m has rational image displacement m b. Fix one nonzero horizontal edge ell0 and one vertical edge m0. A nonzero coordinate of the rational vector ell0 a shows that ell/ell0 is rational for every horizontal edge: both numerator and denominator are rational in that coordinate. Likewise every vertical edge length is a rational multiple of m0. Summing edge increments around the connected boundary shows that all x-x0 are rational multiples of ell0, and all y-y0 are rational multiples of m0. Nonempty interior makes both ranks exactly one. This argument even works for arbitrary invertible A without the mirror hypothesis; rational image edges in each parallel family already force the ratio condition.

Conversely, translate by (-x0,-y0), then apply diag(1/alpha,1/beta). All vertices become rational. The two original wall directions remain perpendicular, so conjugation by this diagonal map preserves Euclidean specular reflection at every horizontal or vertical wall. It sends every finite legal billiard path, with its actual endpoints and actual wall contacts, bijectively to a legal path in the image polygon. Corners, strict interior points, transversality, and maximal straight wall count are preserved. The inverse map has the same properties. Anisotropic scaling is allowed here because there are exactly the two perpendicular mirror directions.

## Conditional optical consequence for arbitrary endpoints

Normalize the walls as above. Suppose there is a dark interior pair. In the normalized rational-coordinate orthogonal room, the independently accepted arithmetic endpoint lemma, WITH its citation/projection supplement, implies that both endpoints have rational coordinates. Apply the common even-denominator similarity to all vertices and this actual pair. The resulting room is a canonical45 triangle disk, with the same W and a distinct interior A pair; darkness is preserved by both maps. This contradicts the hypothesized uncapped theorem. Thus every original real interior pair illuminates, conditional exactly as stated.

The k<=6 theorem cannot replace the uncapped premise: normalization and endpoint denominator clearing can increase k without bound. No affine deformation of a dark pair into rational data is assumed; the endpoint rationality theorem is used only AFTER walls are exactly rationalized by a reflection-preserving bijection.

## Examples and boundaries

Every rectangle, with arbitrary positive real width and height, satisfies this coordinate condition. More generally it includes orthogonal rooms whose horizontal vertex spacings are rational multiples of one alpha and vertical spacings rational multiples of a possibly incommensurable beta. For example [0,2]x[0,sqrt(2)] union [0,1]x[0,2sqrt(2)] is covered by alpha=1,beta=sqrt(2). It need not be similar to a rational-coordinate polygon: perpendicular displacements of lengths 1 and sqrt(2) have irrational length ratio, whereas rational perpendicular vectors have rational ratio of lengths. Affine scaling rationalizes it exactly.

The previously reviewed six-wall room [0,2]x[0,1] union [0,1]x[0,1+sqrt(2)] fails the y condition: its vertical increments include 1 and sqrt(2), with irrational ratio. It cannot be rationalized by any invertible affine map. This matches the earlier parallel-edge obstruction.

Adding a third nonparallel wall direction changes the mirror constraint: the accepted rigidity lemma forces every globally reflection-preserving affine map to be a similarity. The independent-axis criterion must not be used for a mixed axis/diagonal octilinear room.

Review targets: necessity for arbitrary placements/orientations of rational output; reflection conjugation and actual pair preservation; use of the arithmetic endpoint lemma only on normalized rational walls; quantifiers and k-cap limitation; the claimed strict extension beyond similarity-rational orthogonal walls.
