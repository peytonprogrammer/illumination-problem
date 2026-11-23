# An effective denominator bound from one rational source

Let P be a strictly simple orthogonal polygon with integral vertices, and fix a rational interior source S. For each horizontal unit row take every contiguous run of cells separately. Let Lh be the lcm of twice their lengths, and define Lv by columns. Write den for the positive reduced denominator, including den(0)=1. Put

    A = Lh den(S_y),   B = Lv den(S_x),   D = 4AB max(A,B).

**Theorem.** Every distinct interior target dark from S is rational and has simultaneous denominator N = lcm(den(T_x),den(T_y)) at most D. This gives an explicit finite list of candidate points in the bounded polygon. No restriction on area or reflex count is needed. For a lattice source the only inputs are the two strip periods.

## Proof

Use the connected four-copy translation unfolding of the room, marking all physical vertex lifts as forbidden in the interior of a trajectory. Fix one lift of S and one of T. Local unit-grid coordinates in this unfolding agree with physical coordinates up to signs and integral translations, preserving the coordinate denominators. On each unfolded horizontal unit strip, use coordinates along its circumference W and across its height 1. Here W is twice the length of its physical run. The map H adds A times the transverse coordinate to the longitudinal coordinate modulo W. It fixes both boundary edges pointwise since W divides A. The strip maps glue to an affine automorphism with common horizontal shear derivative, including across regular edges, and fix the forbidden set. Define V by the analogous vertical construction with B. This is the strip twist of [d16](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d16-real-to-rational/reduction.md). H fixes the chosen lift of S even in a strip interior because A times its transverse fraction is a multiple of W. Likewise V fixes S. On coordinates modulo the unit grid these maps are integral unimodular shears. Thus each preserves the simultaneous denominator N of every rational target.

Suppose the current target lift has transverse denominator q = den(y) > 2A. In its horizontal strip write a = A/W. For y with reduced fractional numerator coprime to q, H advances by a rotation of order h = q/gcd(q,a). The orbit points have equal spacing

    delta = W/h = W gcd(q,a)/q <= A/q < 1/2.

Every specified open unit tile on this strip contains at least two consecutive orbit points at this height, even if the starting point is on a vertical grid edge. Take two such samples in increasing order in the tile, with longitudinal denominators b1 and b2. Their difference is delta, hence den(delta) divides lcm(b1,b2). Since h divides W den(delta) and q divides a h, we obtain q dividing A den(delta). At the first sample the simultaneous denominator equals the original N. Consequently

    N = lcm(b1,q) divides A lcm(b1,b2).

If both samples had longitudinal denominator at most 2B, this would give N <= 4AB². Therefore whenever N > D we can place the target in *any chosen tile* on its horizontal strip with den(x) > 2B, ready to move vertically. Interchanging axes gives the vertical-to-horizontal statement, since D also bounds 4BA².

Initially at least one axis is available, since den(y) <= 2A and den(x) <= 2B together give N <= 4AB. Use an available shear to enter an open tile if necessary. Follow an edge-adjacency path in the unfolding to a tile incident to S. Each horizontal or vertical edge step uses the corresponding strip. If the available axis differs from the required axis, use it to land in the *same* tile with the other axis available. The tile graph is connected because the unfolded surface is connected and removing finitely many vertices preserves path connectivity. This proves we can place T in the interior of the chosen tile. The segment from S to this point has open interior in that tile and misses all forbidden vertices. Its endpoints are distinct since the applied maps fix S and are injective. Pull the segment back by the inverse affine composition and fold to P. This is a valid illuminating billiard path.

For an irrational target, start with an irrational transverse coordinate on one of the two axes. Its strip rotation is dense, and at most one iterate has rational longitudinal coordinate, since differences between distinct iterates are irrational modulo the integral circumference. Thus every chosen tile admits an iterate with an irrational coordinate transverse to the next axis. The same tile-by-tile argument finishes. This part also follows from d16 for a fixed rational source.

## R22 arithmetic control

For S=(0,0) in R22, the archived cell list gives strip circumferences 2, 4 and 8 on each axis. Thus A=B=8 and D=2048. We sharpen the cutoff by asking exactly which orders can fail the sufficient steering test. Initially both coordinates can fail readiness only at orders lcm(i,j) with i,j <= 16. There are 70 such orders and the maximum is 240. At a later horizontal stall, all samples in a specified open unit interval have denominator at most 16. Its first two fractional positions u and v must therefore be on the list of low-denominator fractions. Their gap is delta=v-u, and u <= delta since the predecessor is outside the interval or on its boundary. All further samples below 1 must also have low denominator. For each surviving gap and each W, require h=W/delta integral and q=h gcd(q,A/W)>16. Then the only possible order at that sample is lcm(q,den(u)). The vertical test is identical.

The union of initial failures and both axis stall sets contains **74 orders, all at most 240**. Every other order is lit by the proof. This union is a necessary condition for darkness, and many of its orders are lit as well. The known dark target (2,2) has order 1 and survives. The separate R22 uniqueness proof gives the sharp bound 1 there.

Run [denominator-control.py](denominator-control.py) with Python 3. A second calculation enumerates q directly up to 128, justified by 1/16 <= u <= delta <= 8/q, and obtains exactly the same stall sets. [Exact output](denominator-control.txt). Both checks use strip periods and rational arithmetic only.

## Remaining quantifier

For a *fixed* room and rational source, enumerate N <= D and the finitely many points of (1/N) Z² in its interior. Any surviving pair can be handed to an exact rational marked-pair decision procedure after clearing denominators. The candidate list alone does not certify these pairs. As S varies over rational nonlattice points, A and B can grow together. Nor are strip periods bounded by the wall count. The next question is whether a dark pair forces an absolute bound on the *smaller* endpoint order in a fixed room. Such a bound would combine with this theorem, using reversibility, to leave finitely many rational pairs with both endpoints free.
