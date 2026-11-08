# Independent WR01 review

Final author prior-audit, candidate, argument and review request read in full. All three frozen source hashes verified. Independent hand reasoning below; the all-n shear-stabilizer calculation was derived and published separately before this final author packet. No author code, engine, search or finite orbit census was run.

## Decisions

| Author claim | Decision | Exact qualification |
|---|---|---|
| Cylinder-lcm maps are genuine global affine automorphisms fixing the full torus-origin fiber | ACCEPT | Unit-height row construction glues pointwise at row boundaries, has a global inverse and extends over cone stars. |
| Whole straight-path and first-Xi return equivalence with all integer return times | ACCEPT | Xi and its complement pull back exactly; prongs map by the actual homeomorphism. These are first MARKED-event times, not the old physical-wall itinerary. |
| Partial rho descent criterion and well-founded termination of accepted moves | ACCEPT | Strict inequalities below cover signs and equality. Termination alone proves no terminal illumination. |
| Exact full-fiber pure-shear derivative stabilizers on all square P_n | ACCEPT | Independent source-coset/target-row proof gives a=4n^2k and b=4nk, with translations (Bk,0)/(0,Bk) mod2B. |
| Universal availability of a decreasing pure-shear move and an illuminated axis terminal | REJECT as universal premises; ACCEPT author's rejection | The already-lit actual square direction (n,1) has no decreasing step; no marked-fiber-preserving affine map can send it to an axis. |

No material correction is needed to the final scoped argument. The full orthogonal r<=8 theorem remains OPEN.

## Independent local gluing and optical transfer proof

Let L be the order of the right permutation, equivalently the lcm of its cycle lengths. One right cycle of length c is a row R/cZ times (0,1). On this row define F(x,y)=(x+Ly,y). At y=0 the map is the identity; at y=1 the x displacement L is0 modulo c. Both boundary circles are fixed pointwise, so every original top/bottom pairing still agrees pointwise. The x-period c is respected for all y.

Near a regular horizontal seam, use one translation chart crossing the seam. A lower representative of F differs from the upper one by a constant translation, since crossing y=1 changes the formula by L. Their values already agree along the seam; hence this constant is exactly its chart-transition translation. Both derivatives equal H^L, so the seam introduces no kink. The construction with -L supplies an inverse on every row and the same gluing. At vertices, finitely many incident sectors have consistent boundary limits; F and its inverse extend continuously and inverse to one another. This proves the global homeomorphism and cone-star extension, rather than inferring a lift from the matrix alone.

Every unit-square vertex is fixed because it belongs to row boundaries. Thus every point of Z0, including regular physical corner lifts, is fixed. X,Y,Sigma are their original separate labelled subsets. In particular F^{-1}(Sigma)=Sigma and F^{-1}(X)=X, F^{-1}(Y)=Y. Interchanging axes proves the vertical construction with the order of the up permutation. No W-uniform bound on either order is used.

If gamma(t) has velocity w in translation charts, F^{-k}(gamma(t)) has the single constant velocity H^{-kL}w on the whole trajectory, with the SAME t parameter. It is therefore a single straight unfolded path. If gamma had first subsequent Xi time ell, an earlier Xi encounter in its image would pull back to an earlier one in gamma. Invertibility proves the converse and maps each actual local prong. Hence ell remains the same positive integer, including unbounded ell. Suppressed transparent lattice points remain transparent because F fixes the whole origin fiber and preserves its distinguished subsets.

This verifies actual endpoint/sheet identity and forbidden-set inverse images before using the unfolding-to-billiard equivalence. A mapped path can cross DIFFERENT physical seams; its original wall word must not be copied. The final author argument explicitly retains this distinction. Legal refolding follows from avoiding every actual corner lift; a start at an actual interior mark cannot introduce wall gliding without a forbidden corner. This establishes a conditional optical equivalence on the SAME original surface/room for the two specified directions. It supplies no unproved new room in an induction class.

## Rank, both signs and equality

For p,q nonzero set x=|p| and A=L_h|q|>0. A nonzero integer multiple of L_h q has absolute value at least A. If A>=2x, every such subtraction has magnitude at least A-x>=x, so no strict decrease exists. If A<2x, take the sign of k so kL_h q has the sign of p and magnitude A. Then |p-kL_h q|=|x-A|<x. Thus a decreasing horizontal step exists iff 2|p|>L_h|q|. At equality the smallest nonzero step ties; it is not accepted by a strict rank rule. Vertical descent is the same statement with the roles exchanged. This covers opposite component signs as well as like signs.

rho is a positive integer on nonzero primitive integer w. Every ACCEPTED step strictly decreases it, so such a sequence is finite. The matrix is unimodular, so primitivity survives and the zero vector cannot appear. Axis cases are not promised to illuminate; the move criterion was stated for non-axis input. Nothing here establishes availability of another accepted step at every non-axis terminal state, or a positive terminal base.

## All-n calibration and stronger axis obstruction

The complete independent derivation is frozen in weighted-return-square-shear.md. It uses the actual torus period2B, source coset and target two-point row stabilizers. It does not use the author's gcd calculation as its sole evidence. The author's gcd identities independently check out:

    gcd(8n^2+4,16n^2)=4,
    gcd(8n^2+4n,16n^2)=4n,

because gcd(2n^2+1,4n^2)=1 and gcd(2n+1,4n)=1. The nonantipodal hypothesis holds for every n>=2. Setwise preservation, not just pointwise fixing, is included; the exact allowed translations preserve all four physical corner marks too.

At w=(n,1), every nonzero horizontal coefficient has magnitude at least4n^2 and every nonzero vertical coefficient at least4n. The reverse triangle inequalities in the author argument therefore give strict rank increase for both types and all powers/inverses. This is a lit r0 room; it is not a dark counterexample.

Independently, no horizontal path on this torus joins X to Y because their y-coordinate sets are disjoint; no vertical path does because their x-coordinate sets are disjoint. A genuine affine map preserving X,Y,Sigma would transport the lit path, with its actual endpoints and corner avoidance, to a lit path in the mapped direction. Thus its derivative cannot send this lit direction to either axis, regardless of whether the derivative is parabolic. This refutes an axis-only illuminated terminal requirement for a fiber-preserving direction reduction on this fixed surface.

An induction which detects a convex room and terminates there, or includes marked non-axis terminal states, avoids this precise objection. It still needs a justified availability/recognition argument for the remaining rooms. Non-parabolic moves, uphill words, room changes and different weighted ranks are not ruled out by WR01.

## Coverage of the full objective

The valid global affine maps preserve the exact all-word optics and arithmetic weights; this is a real local transfer result. The proposed strictly descending move is not globally available, even in the mandated lit calibration. The low-reflex assumption was not used to obtain a positive implication, and the known r9 control still prevents treating all arithmetic marked surfaces as positive terminal bases. No new direction enumeration or finite unweighted quotient has been smuggled in.

Required next proof content is a genuinely different rank/move or terminal class with proved physical optical transfer, availability and positive base using original r<=8. Merely encoding the same marked origami orbit or allowing more fixed shear powers does not supply it. WR01 resolves the five pinned local claims at their exact scopes; it does not complete the native goal.
