# Reaching a fixed preimage and reaching the target sheet

**Verdict.** A prescribed regular preimage of an involution-fixed point over the source site can be unreachable from a prescribed source lift even in the named 2-by-4 rectangle. There is a second, independent obstruction. A reachable regular preimage can send *every* doubled path through it to the wrong physical point. These statements concern the proposed reachability argument. Neither example has a physically dark pair.

## An unreachable preimage with four walls

Translate the [archived 2-by-4 rectangle](../../illumination-per-class-census/rectangle.py) to [0,2] × [0,4]. Its translation unfolding X is the torus with period lattice Λ_X = 4ℤ × 8ℤ. Physical corner lifts are exactly 2ℤ × 4ℤ modulo Λ_X. Use the proper degree-two quotient Y with lattice 2ℤ × 8ℤ and the base torus with lattice 2ℤ × 2ℤ. All maps are the natural projections. Use representatives

    s = (1,1),       m = (−1,−1),       t = (−3,−3).

The three points project to the same base site p. The physical marks are the distinct same-parity interior lattice points (1,1) and (1,3). On Y the involution e(z)=2m−z exchanges the distinct images of s and t and fixes the image of m. Upstairs m is regular. Yet every segment from s to m develops to a segment ending at −s+(4i,8j). Its midpoint is (2i,4j), a forbidden corner lift, for every pair of integers i,j. This is exhaustive in every direction.

Here m is the opposite lift of the *source's own physical point*. The statement about a prescribed lift includes it. This example does not refute a claim restricted to preimages at different physical points, or a claim requiring existence of one reachable preimage somewhere in the fiber. Allowing a choice of source lift also changes the quantifier. The physical marks in the example are directly visible.

## A reachable preimage that never returns the requested target

On any rectangular unfolding, for tori X → Y with period lattices Λ_X ⊆ Λ_Y, a segment from s through m doubled in time ends at 2m−s modulo Λ_X, independent of winding. For the quotient involution exchanging f(s), f(t), the difference

    δ = 2m−s−t ∈ Λ_Y / Λ_X

is the exact sheet discrepancy whenever e fixes f(m). Doubling through m ends at the specified t if and only if δ=0. Corner avoidance on the second leg is an additional requirement. For an arbitrary translation cover the corresponding sheet test is transport along the particular image path, rather than addition in a lattice quotient.

For an explicit control in the same room take Λ_Y=4ℤ × 4ℤ, a proper degree-two quotient. Take the base lattice (½ℤ) × ℤ so all three points project to p. Let

    s=(½,1),        m=(1,2),        t=(3/2,7),        e(z)=2m−z on Y.

All three physical positions are distinct and interior. The straight segment from s to m lies inside the room. The images of s and t on Y are distinct and exchanged by e. Doubling the segment ends at (3/2,3), while t represents the physical target (3/2,1). Their difference (0,−4) is nonzero in Λ_Y/Λ_X. Every other arrival at this same m from this same s, if continued legally for the same time, has the same wrong endpoint. The physical target is itself directly visible from the source. This example uses rational marks and a refined base; the first example already uses integer marks. The defect occurs on an unbranched cover, without a seam or a singular midpoint.

## The corrected reachability statement

Write α for a regular straight leg from s to m and β for a regular straight leg from t to that same lift m on X, with the same travel time. Impose f(β(u))=e(f(α(u))) at every time u. Then α followed by the reverse of β is a legal shot from s to t: their velocities agree at the join because the derivative of e is −I. Conversely any legal s-to-t shot supplies just such legs, by reversal and uniqueness on Y. Equivalently the two legs must reach a **diagonal** point (m,m) from (s,t) in the correspondence f(y)=e(f(x)), avoiding forbidden points in *both* projections. For one prescribed primitive class the legs must also have that developed direction class. Merely lighting m by an unspecified direction would not establish lighting in every class.

This gives a structural follow-on even without assuming the conjectured converse. In an unbranched torus quotient the eligible midpoints for a specified pair form the four solutions of 2m=s+t on X. Other fixed preimages can be discarded exactly by δ. On a general cover the two-leg test replaces the discrepancy. A dark pair separates every such legal trajectory from the diagonal, even when that diagonal contains regular points over p. That fact provides neither the existence of an exchanging quotient involution nor the claim that all of its fixed preimages there are forbidden. The proposed per-class classification for all rooms with at most 20 walls therefore does not follow.

## What R22 actually does at a seam

The proved map folds three physical copies onto a five-square staircase. Its two marks land at distinct smooth wall sites a=(0,0) and b=(2,−2). On an ordinary staircase trajectory between them, unfolding gives a nonzero displacement B with both coordinates even. Dividing B by the highest common power of two gives an intermediate lattice point with an odd coordinate. Refolding preserves coordinate parity, and every such staircase site is a vertex. The argument can use a point other than the temporal midpoint.

The four exceptional smooth upstairs sites are (−1,0), (1,0), (2,1), and (2,3). They are all outside the even-even source class. A physical wall reflection there reverses the *entire folded velocity*. Truncate a proposed folded trajectory from its last visit to a before its first arrival at b. Its first exceptional reversal would retrace to a. It cannot encounter b along the retraced part because that would give an earlier visit to b. With reversals eliminated, the ordinary parity argument applies. The complete physical fibers are {S,(4,0)} over a and {(2,−2),T} over b. In particular the source parity has regular representatives. Calling any of them an involution-fixed preimage requires specifying an exchanging involution on a particular translation quotient. The staircase proof supplies no such involution, and does not establish an empty regular fixed fiber over p. [R22 manuscript, folding and reversal proofs](../../illumination-publication/repository/preprints/twenty-two-wall/manuscript.tex)

**Open question.** For a hypothetical dark physical pair, is there a class-dependent quotient witnessing separation, or a seam invariant of a different kind? Replacing first-leg reachability by two-leg reachability in a given quotient is an exact reformulation of lighting for those lifts. It is not a proof of that existence assertion.
