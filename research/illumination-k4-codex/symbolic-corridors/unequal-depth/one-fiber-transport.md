# One coalesced endpoint fiber suffices for affine transport

Codex01a18403. Candidate theorem, independent review required. This extends the frozen horizontal-parity packet; it does not change that packet.

## The lifting observation

Let pi:X->P be the standard four-copy unfolding projection. Let H be an affine homeomorphism fixing every polygon-vertex preimage, including regular convex-corner lifts. Suppose H maps the ENTIRE fiber pi^-1(S) onto pi^-1(S'), for one interior physical S'. Choose any v in pi^-1(T) such that T'=pi(H(v)) is interior. If actual S',T' illuminate, actual S,T illuminate.

Take a physical S'-to-T' corner-free connection. Lift it BACKWARDS starting from the prescribed lift H(v) of its target. All regular mirror seam crossings lift uniquely. Its starting point belongs to pi^-1(S'), which by hypothesis equals H(pi^-1(S)). Apply H inverse. The result connects a lift of original S to v, avoids every forbidden vertex lift, and folds to a finite original connection. An earlier actual target visit can be used. No fixed initial copy was prescribed in the physical problem. No assumption that H commutes with the deck reflections is made.

The observation needs coalescence of just ONE endpoint's whole fiber. It does not require the other endpoint's four images to have the same physical projection. It also does not permit a boundary T' in the present statement.

## Horizontal shear specialization

Use the six horizontal annuli and H of slope L=4n/delta constructed in horizontal-parity-twist.md, where delta=gcd(h_-,1,h_+). Put A=a/delta and B=b/delta. Let n0 be the reduced denominator of 2A. For every integer k, H with n=n0*k maps the full S fiber to one interior S', with horizontal position s or 2-s according to the parity of 2nA.

Choose the original identity lift v of T. Its image projects to

    T'_x=F_2(t+4nB),  T'_y=1+b,

since L is a multiple of 4 and the target height is 1+b. As k varies, t+4n0*k*B modulo 4 runs through a uniform cyclic grid of order

    N = denominator(n0*B) = den(B)/gcd(n0,den(B)).

If one grid point projects strictly into (1,2), then T' is an interior common-column mark. The accepted L-subroom theorem connects it to S', whatever the latter's horizontal position. The lifting observation proves original illumination.

There is a second sufficient condition: if 2n0*A is odd and s<1, take k=1, so S' is strictly in the common column. It suffices to choose ANY T-image lift whose projection is interior. When t<1 at least one of the images F_2(t+4n0B), F_2(t-4n0B) is interior: if both were in {0,2}, their two arguments would be even integers, forcing t to be an integer. Thus this condition proves illumination whenever s,t<1. We do not use it when t=1 without a separate interior-image check.

## Exact circle-grid obstruction, all denominators

Let 0<t<=1. The order-N uniform grid t+4j/N modulo 4 has a point in (1,2) or (2,3), equivalently a fold strictly in (1,2), except precisely:

- N=1 (the original point stays left of or at center);
- N=2 and t=1;
- N=3 and t=2/3;
- N=4 and t=1.

For N>=5, spacing 4/N<1 forces a point in the interval (1,2). For N=2, t+2 works whenever t<1. For N=4, t+1 works whenever t<1. At t=1 both grids consist of excluded boundary values. For N=3, an interval of length 2 contains a grid point, since spacing is 4/3. If every point in (1,3) is forbidden, the only such point is 2. The grid must then be {2/3,2,10/3}; its only starting value in (0,1] is t=2/3. Conversely that grid indeed has no strict common-column image.

These are failures of this shear reduction, not darkness assertions.

## Consequence for both strictly left horizontal marks

Assume 0<s,t<1. Write q=den(A), r=den(B) in lowest terms.

If q or r is even, pick that endpoint as the coalesced source. Its n0 is half the even denominator and 2n0 times its depth ratio is odd. The second sufficient condition proves illumination, with no divisibility condition on the other endpoint's depth.

Otherwise q,r are odd. Then n0=q when fixing S, and the target grid order is r/gcd(q,r). Reversing endpoints gives source grid order q/gcd(q,r). If q!=r, at least one order exceeds 1. They cannot both equal 3: dividing both denominators by their gcd would make them equal, whereas these quotients are coprime. The only unclosed distinct-denominator cases therefore have one order equal to 1 and the other equal to 3, with the endpoint on the latter orbit having horizontal coordinate 2/3. Equivalently:

    r=3q and t=2/3, OR q=3r and s=2/3.

Thus, for both strictly left marks, this candidate reduction leaves only EQUAL ODD depth denominators, or a denominator ratio 3 with the larger-denominator endpoint horizontally at 2/3. Existing accepted equal-depth, centered, portal-chart and fixed-room results may still cover particular members of those sets. These arithmetic sets are NOT claimed dark.

If one horizontal mark equals 1, use the general order-N criterion above, not the simplified both-strictly-left consequence. In particular order 2 or 4 may leave that centered endpoint fixed or on smooth walls. The full goal remains open, and no uniform reflection bound is claimed.

## Prescribed exact controls and remaining dependencies

one-fiber-check.py checks the circle-grid exceptions at prescribed orders and exact breakpoint/interior representatives. Those controls do not replace the elementary all-N proof. It also pulls back five prescribed direct common-column paths where the target fiber DOES split into different physical positions; the old requirement of two coalesced fibers fails in these controls. Original all-edge rational tracing verifies the resulting physical paths.

The geometric dependencies are the six-annulus horizontal shear, the accepted common-column L-subroom reduction, and the four-copy unfolding correspondence. Independent review must challenge backwards lifting from an arbitrary selected target image, full source-fiber surjectivity, and the two small-orbit exclusions involving wall images. No finite-orbit sampling is substituted for a theorem.
