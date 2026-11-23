# A bounded target orbit at arbitrarily large marked valency

**Route B, theorem for review.** The stabilizer of a specified source lift need not have a growing orbit on **either** lift of a nondirect, same-parity target, even in normalized BBBB rooms with r=6 and marked valency d≥n−8. In the D69 staircase with symmetrically stretched ends, both target orbits have size at most two, independently of area. For the very same pair, reversing the roles gives an orbit of size at least m/gcd(m,3), where n=2m²+6. This refutes an unconditional one-way lower bound and gives a two-way necessary condition for darkness. It does not produce a dark pair.

## The symmetry responsible for the small orbits

Use the orientation-preserving affine automorphism group G of the quadratic room double Q, preserving the forbidden corners as a set. The derivative is defined modulo ±I. This group, rather than its derivative image alone, acts on specified points. Let K be the kernel of that projective derivative. It is normal in G. The following description allows K to be read off the room itself.

Every k in K is holomorphic on the smooth compactification Q, a Riemann sphere. The mirror exchanging the physical room copies fixes a circle containing all the corners. A Möbius map in K permutes those corners and therefore preserves this circle: it is the unique generalized circle through any three of them. It commutes with the mirror, since the conjugated reflection fixes the same circle pointwise. Consequently it descends to a Euclidean symmetry of the physical room. On each open copy its physical derivative is constant: in half-translation coordinates it is ±I, and folding the opposite copy changes one coordinate sign. Thus the physical derivative is diagonal with entries ±1. The descent is injective because the other lift of the identity is antiholomorphic. Conversely, an axis-sign symmetry lifts uniquely with positive orientation, keeping the two halves if orientation preserving and switching them otherwise; its derivative on Q is ±I. All these Euclidean symmetries fix the room's area centroid, so there is at most one per sign choice. Hence K is a subgroup of the group of four diagonal sign choices. This also identifies the kernel when some symmetries shift the pillowcase parity classes; no assumption that K fixes each base pole is needed.

In particular, if the only nonidentity axis-sign symmetry is the physical half-turn δ, its lift is central in G. For a center in the room interior, the fixed set of this lift consists of precisely the two lifts of the center. The lift preserves each half and restricts to the physical rotation there. The unordered pair of fixed points is G-invariant. Both points have G-orbit size at most two, before even fixing the source. More generally, for any K the orbit of a point of Fix(k), k≠1, is contained in the union of the fixed sets of the conjugates of k in K. Each such nonidentity Möbius involution has two fixed points, giving a bound of six across all three possible involutions. Also G_s · (k s) lies in K s. These describe specific bounded-orbit exceptions without any claim that they exhaust the exceptions.

## D69 staircase, with the same physical pair in both bounds

Use the symmetric end stretches in D69's st279 construction, writing m for the resulting end-square side (m=2 in cov279, 4 in st279b and 5 in st279). The four horizontal bands have the following vertical ranges and horizontal intervals; take the closure of their union.

| height range | horizontal range |
|---|---|
| (0,m) | [0,m] |
| (m,m+1) | [m−1,m+2] |
| (m+1,m+2) | [m,m+3] |
| (m+2,2m+2) | [m+2,2m+2] |

These are the original rows after inserting m−2 extra copies of each outermost row and column. For every integer m≥2 consecutive bands overlap in positive length, and both ends of each interval shift strictly right at each of the three interfaces. The boundary is simple, with two reflexes per interface. The unit shifts at the middle interface and the exposed unit-high sides give the separate wall-length gcds one. The area is 2m²+6. For m≥3 the end square alone contains all four interior parities. For the large-area range the archived proper-factor bound also excludes proper canonical factors (n>8r). The half-turn around C=(m+1,m+1) interchanges the ends. Neither axis reflection preserves the room: it takes (0,0) to a missing corner of its bounding box. Thus K has order two. [D69 builder, COV279 and stretch](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d69-bbbb/decomp.py) · [Proper-factor bound and room classes](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d66-pair-level/README.md)

Take S=(m−1,m−1), T=C. Both are interior, of the same parity. Their direct chord hits the reflex at (m,m), where the southeast quadrant is missing. For m≥8 one has n≥120, so d≥n−8 by the reviewed large-area theorem. For either lift s of S, both lifts of T have G_s-orbit size at most two by the symmetry argument. [Reviewed valency dichotomy](eight-sheet.md)

For the reverse direction construct one affine map with the same derivative everywhere. On the double of an open horizontal band of width w the horizontal coordinate is circular of period 2w: follow the physical interval on one room copy and return along the other. Choose ordinate y above the lower band edge. Apply (x,y) ↦ (x+6y,y) in each completed band. On the end bands the top shift 6m is divisible by 2m. On either middle band the top shift 6 is its full circumference. All boundary circles are fixed pointwise. The maps glue to a homeomorphism with the indicated common shear derivative: changes of half-translation chart are ±I plus a translation, and equal boundary values and equal derivatives give a single affine germ across every regular seam. The inverse uses −6. The map fixes both lifts t of T on the middle interface. At either s the shift on its circumference-2m leaf is 6(m−1), so its orbit under this map has exactly

    2m / gcd(2m,6(m−1)) = m / gcd(m,3)

points. This yields the claimed lower bound for G_t · s. No ray, word, room or direction search enters either result.

## A two-way test from any certified parabolic

Let F be any affine automorphism of the corner-marked double, and write u,v for the finite F-periods of s,t. Then

    |G_s · t| ≥ v/gcd(u,v),       |G_t · s| ≥ u/gcd(u,v).

Indeed F^u fixes s and its cycle on t has the first stated length. Exchange the points for the second. In a horizontal band decomposition the formulas are checkable from the corners: choose a common shear λ for which λH_i is divisible by the circumference C_i in each band. The period of an interior point of relative height h is the reduced denominator of λh/C_i. Boundary points are fixed for this choice. The same construction works in any integral straightened chart where the cylinder bands and endpoint heights are certified.

If the Q pair is dark, reversibility and the ordinary shadow bound B(r) bound **both** stabilizer orbits. Thus for every such F both numerator and denominator of the reduced period ratio u/v are at most B(r). If either exceeds B(r), that lift pair is lit and so is the physical pair. This conclusion is ordinary illumination; the argument does not prescribe its midpoint parity. For the staircase it proves illumination of the specified pair once m/gcd(m,3)>B(6), though B(6) has no evaluated numerical value. [Ordinary shadow theorem and limits](shadow-budget.md)

## Why kernel symmetries alone cannot defeat both lift choices

For a fixed source lift s, suppose both lifts t and ιt of the same physical T belong to K s, where ι is the physical mirror. Two elements taking s to these opposite sheets induce physical axis-sign symmetries taking S to T. Their quotient fixes S and exchanges halves, so its physical action is an axis reflection through S. The sign symmetries commute (take the centroid as origin), hence T lies on the same fixed axis. The intersection of the room interior with this axis is an interval. Indeed a Riemann map from the disk to the simply connected room sending 0 to S pulls the reflection back to an antiholomorphic disk involution fixing 0, whose fixed set is a diameter. Its image is exactly the room's interior fixed set, which is therefore connected on that straight line. Thus S and T are directly visible. For a nondirect pair at least one lift choice always escapes K s. Likewise, among interior physical points only the rotation center can have a Q lift fixed by a nonidentity element of K: an axis reflection exchanges halves. Therefore for distinct interior marks one can orient the pair so the target escapes the interior fixed-point exception, and for nondirect marks also choose its lift outside the source's K-orbit. This removes the two kernel-based explanations simultaneously; it does not bound suborbits of points outside them.

**Remaining obstruction.** For a universal orbit-size proof one now needs a large suborbit in at least one orientation and for at least one lift choice, or a separate way to light the bounded cases. Even the two-way period test has a precise blind spot: if t=k s with k central in G, then the two points have identical periods under every F, and G_s fixes t and G_t fixes s. This does not automatically identify the other physical target lift. The staircase center example does not disprove the two-way proposal. High sheet-monodromy valency alone is insufficient for the original one-way proposal, including after allowing both target lifts. The universal same-parity reachability statement remains open.
