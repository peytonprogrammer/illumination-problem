# Independent guard for a pillowcase-cover optical argument

This is a precise necessary guard, derived before inspecting a peer pillowcase implementation. It is not a finding that the peer has made the mistake described here, and it supplies no low-wall exclusion.

## 1. Interior A marks need not lie over primitive torus two-torsion

Take the canonical orthogonal rectangle

    P=[0,10]x[0,12], S=(2,2), T=(4,4).

Both marks are distinct strictly interior A points. The minimal four-copy unfolding M is the rectangular torus with full absolute period lattice

    Lambda=20Z x 24Z.

Its primitive torus covering has degree1. The normalized coordinates of S on this torus are (1/10,1/12), of order60. Those of T are (1/5,1/6), of order30. Neither is two-torsion, since doubling does not give an integer vector in these normalized coordinates. The actual corner lifts, in contrast, ARE the four two-torsion points.

Thus an argument cannot silently replace the arithmetic torus used to make all integer/A marks lie over0 by the primitive period torus while preserving that property. This counterexample is convex and illuminated directly. It is a counterexample only to the normalization assumption.

For this same room the development map modulo Z^2 has degree480 and DOES send all its A marks to0. This is a different torus cover. Both are valid, but they have different degrees and different marked fibers. A further mark-compatible quotient can also be chosen; its degree must be tracked rather than called primitive automatically.

## 2. Exact orthogonal odd-ramification accounting

Let an orthogonal polygon have r reflex corners, g=r+1, W=2r+4. Let M cover a torus E by a degree-D translation map using a lattice invariant under the canonical half-turn, with a fixed actual corner as origin. Set Q=M/<rho> and B=E/<-I>. The accepted canonical half-turn quotient makes Q a sphere. The induced map

    h:Q -> B

has degree D; both vertical maps in the commutative square have degree2. B is a sphere with four cone points of angle pi.

Every actual corner lift maps to two-torsion in E. At a convex corner, the induced local degree of h is1; at a reflex corner it is3. At any OTHER point over a cone point of B, the point of Q is regular and h has local degree2. There is no other branching: away from corner lifts the map M->E is locally a translation, and the two quotient maps have only their specified half-turn fixed points as branch points.

Let n_j be the total number of local-degree-j preimages over the four cone values of B. Then

    n1=r+4, n3=r,
    n1+2n2+3n3=4D,
    n2=2D-2r-2=2(D-g).

Riemann-Hurwitz independently gives n2+2n3=2D-2, the same identity. In particular D>=g. This is topology/ramification, not darkness.

If the chosen cover ALSO sends both actual endpoint Gamma orbits to torus two-torsion (for example the common integer arithmetic torus), the two distinct interior physical marks give four distinct regular points of Q over these cone values, each of local degree2. THEN n2>=4 and D>=g+2. This last inequality does NOT apply to the primitive cover unless the endpoint hypothesis is proved there. The degree1 rectangle above is an exact counterexample to the unqualified inequality.

## 3. What an optical proof would still need

The additional degree2 points are regular in Q. They are not forbidden physical corners, and they cannot be treated as absorbers. Their number is unbounded at fixed W, even after choosing a primitive period torus in suitable L families. Suppressing them is a representation choice, not an optical stopping rule.

Physical darkness is an absence of geodesics between two distinct endpoint orbits, not a ramification count by itself. Any odd-ramification proof must retain the actual marked preimages and show how a legal segment reaches one of the actual target lifts. Neither n2=2(D-g), D>=g, nor a finite branching type supplies that connection alone.

This guard concerns orthogonal rooms only. Mixed-direction N=4 quotient genus and local orders need their own accounting. No counterexample to illumination, no primitive-degree bound, and no claim that the peer made an unqualified endpoint assertion is supplied.
