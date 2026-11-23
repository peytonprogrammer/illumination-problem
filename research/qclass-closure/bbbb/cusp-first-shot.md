# Counting first shots over an unmarked cusp

For a fixed primitive class there is a first-shot test which does not take an already lit pair as input. One cusp of the room **with its physical corners marked but without the endpoints marked** can certify a first shot for a prescribed pair. Its contribution can be computed on the finite endpoint orbit, or bounded by an inequality about the distribution of that orbit across straight leaves. Getting a positive contribution universally in BBBB remains open.

## Count the pairs on the leaves before marking the endpoints

Work on the translation unfolding. Let G consist of the orientation-preserving affine automorphisms preserving the physical stop set and having derivative in Γ(2). All such maps preserve primitive parity. Fix particular lifts s,t of the two marks. The sets X=Gs, Y=Gt and Ω=G(s,t) are finite: after fixing a corner as a reference modulo the grid, these affine maps preserve the finite integral grid fiber. Equivalently, explicitly restrict to maps preserving that fiber. Let v represent a chosen G-cusp of the desired parity. Partition X∪Y by the actual corner-cut unoriented leaves in direction v. Count a tip-free closed leaf as one part. On a critical leaf cut at *each* physical stop and keep the resulting open intervals separately. Membership in different parallel leaves of one cylinder is a failure for this direction. Denote the parts by i and their intersections with X and Y by X_i and Y_i.

The exact numerator for that cusp is

    E_v = Σ_i |Ω ∩ (X_i × Y_i)|.

It is positive iff that cusp gives a legal shot for (s,t). Indeed a contributing pair (gs,gt) lies on one corner-free interval or circle. The straight subarc between them pulls back by g⁻¹ to one legal segment in the required class. Conversely push any witness in the cusp to v. This is an unmarked-room cusp test with moving endpoints, equivalent to keeping the endpoints fixed and moving the direction. For physical marks take the union over lift choices. The partition is computable from the row cycles and stop colors without tracing prospective rays. The group Ω and its incidences are independent of whether the pair is known to be lit.

There is also a counting interpretation for pair-marked cusps. Let G_v stabilize the unoriented v-line. Pair-marked cusps above this room cusp correspond bijectively to G_v-orbits on Ω (double cosets). In particular E_v counts the successful cusps *weighted by the size of their endpoint orbits*. Counting each cusp once changes those weights but leaves the existence test unchanged. This explains why seeing no mixed cusp in d149 validates invariance yet supplies no positivity theorem. [d149 review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d149-review-cyclicsep/review.md)

## A sufficient inequality that uses no first shot

Choose (x,y) uniformly from Ω. Its marginals are uniform on X and Y, by transitivity on each. Put p_i=|X_i|/|X| and q_i=|Y_i|/|Y|. Let ρ be the largest absolute correlation of mean-zero unit-variance functions of x and y, or zero if either marginal is constant. Equivalently it is the operator norm of the conditional-expectation map on centered functions. Then

    E_v/|Ω| ≥ Σ_i p_i q_i − ρ √[(1−Σ_i p_i²)(1−Σ_i q_i²)].

For each i subtract p_i and q_i from the two leaf indicators. Their covariance is bounded below by minus ρ times the product of their standard deviations. Sum over i and use Cauchy–Schwarz. Thus a strictly positive right side proves a first shot for the given lifts. This uses the joint marked action, not the possibly different sheet monodromy. It requires no direction-residue periodicity.

For example, if X=Y has m>1 points and the affine action is two-transitive there, Ω for distinct lifts consists of all ordered distinct pairs. The exact numerator simplifies to Σ_i |X_i|(|X_i|−1). Any one leaf with two points of X then suffices. In general neither marginal transitivity nor a long cylinder gives the needed conclusion: the orbit can couple marks on different leaves with probability one. A product of marginal counts alone would miss that possibility. In particular ρ can be one if the target is determined by the source, even with uniform marginals. The inequality is sufficient only; a nonpositive bound need not mean the exact numerator is zero.

## A first shot from the saved cross subdegree

A simpler bound can be useful when a stabilizer orbit is dense. Work equally on the half-translation double, using unoriented lines. One may use any group preserving the specified primitive parity, even if it exchanges the other two. If |Y|=m and |G_s t|=d, any one corner-free leaf interval through s containing more than m−d distinct members of Y meets G_s t. Pull the resulting segment back by an element fixing s. This proves a shot to t in that parity without knowing which orbit element is met.

For the seven-unit cross, use the full orientation-preserving affine group of the corner-marked half-double from d91. It preserves the diagonal parity: the four reflex corners have site 00 and the only site without any physical corner is 11. The integral affine action on the parity torus must fix both sites, hence its linear part fixes their difference. Use the d91 pair with s over (6,0), t over (0,6). The unique orbit Y of size 40 contains both endpoint lifts in question; the target subdegree is 36. Thus four misses are possible.

Follow the reference diagonal from (6,0) to the smooth lower wall at (4,−2), then to the smooth vertical wall at (−2,4). Before leaving that second wall, the interval already contains lifts of the five distinct positions (6,0), (4,−2), (2,0), (0,2), (−2,4), endpoints included. Both contacts are regular, so the interval extends a little at both ends. The d91 orbit map puts all five in the unique size-40 orbit. Its displayed map uses one lift; the other is its physical mirror, which normalizes the full affine group and therefore preserves the unique orbit of that size. Five exceeds 40−36. This supplies a diagonal-class first shot to the specified target by the pigeonhole argument, before the reference trace visits its physical position. The same bound applies to any target in that suborbit. This is a demonstration of the counting criterion, not a new illumination verdict for the cross. [d91 orbit map and subdegrees](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d91-review-stabilizers/fullG_b7.log) · [geometry of the diagonal interval](every-direction.md)

## Remaining theorem

The new condition is for a *specified* pair and class. A uniform proof would need to force positive overlap on at least one room cusp for every relevant Ω. The universal canonical relations concern the sheet action and currently give no bound on ρ for the affine endpoint action or on the same-leaf incidences. The large index measured by d149 concerns the pair-marked action; the reformulation does not assert that computing the room cusp or endpoint orbit is cheap. No cusp or direction search was run.

The quantitative target is to bound the number |Y|−|G_s t| of missing target images against occupancy of a *single legal leaf* through s. The cross calculation succeeds using the full group preserving its diagonal parity; it cannot be transferred unchanged to either axial class, which that group may exchange. For sparse target suborbits the exact joint count, rather than the cardinality bound, would be needed.
