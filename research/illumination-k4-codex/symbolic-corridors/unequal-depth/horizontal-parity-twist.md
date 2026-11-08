# A rational endpoint-depth subclass by a horizontal affine shear

Codex01a18403. Candidate hand theorem; independent review required.

Normalize d=g=1 by positive diagonal scaling. Suppose h_-,h_+,a,b are rational. Let delta>0 be the positive rational gcd of h_-,1,h_+: each height divided by delta is an integer, with gcd one. If both s,t are strictly less than 1 and either a/delta or b/delta has an even denominator in lowest terms, the endpoints illuminate. More generally the precise arithmetic criterion below handles one centered horizontal mark when the endpoint of maximal denominator exponent is noncentered. This is an unbounded rational subclass, not the full theorem.

## The affine map and forbidden points

Use the standard four-copy translation unfolding of the orthogonal room. Cut at every lift of a horizontal band boundary. At each physical height strictly within one band, the horizontal billiard runs across an interval of width 2, reflecting at its two actual side walls. Its double is a horizontal cylinder of circumference 4. There are two y-sign copies for each of the three bands, hence six open annuli, with transverse widths h_-,1,h_+. Their total area is 8(h_-+1+h_+), the area of the four-copy unfolding. They exhaust the surface except the cut fibers.

An annulus can have signed transverse interval (Y0,Y1), with Y1-Y0 equal to its band's height. For a positive integer n set L=4n/delta, and define

    H(X,Y)=(X+L(Y-Y0),Y), with X modulo 4.

At either boundary the displacement is a multiple of 4, so every cut boundary is fixed pointwise. The maps glue across actual and artificial cuts, with the same derivative [[1,L],[0,1]] in every translation chart. Their inverses use -L. Thus H is an affine homeomorphism. Every polygon vertex lift is on a cut, so H fixes all singular vertices AND all regular convex-corner lifts. It preserves the full forbidden set, not only the conical singularities.

Offsets in horizontal cylinder coordinates do not alter the displacement formula. At physical height y, signed coordinate is Y=tau*y plus a chart translation. Relative to any signed band boundary, the difference is tau*(y-y_boundary). All original horizontal boundary heights -h_-,0,1,1+h_+ have L times their height in 4Z. Thus the displacement is congruent to tau*L*y modulo 4. In an x-sign sigma copy, physical horizontal folding consequently has argument x+sigma*tau*L*y modulo 4, relative to the actual chamber's interval. Source and target lie in intervals [0,2].

## Mapping whole endpoint fibers, rather than choosing an ending copy

If La=2r and Lb=2q for integers r,q, every one of the four lifts of S maps to a lift of the SAME physical point

    S'=(s,-a) if r is even, and S'=(2-s,-a) if r is odd.

Indeed its horizontal displacement is either +2r or -2r modulo 4. These agree modulo 4, and the period-4 triangular fold sends x+2 to 2-x. For T, Ly=L(1+b) is congruent to Lb modulo 4, since L is a multiple of 4. Hence all target lifts map to one physical point T', with horizontal coordinate t or 2-t according to the parity of q. Vertical coordinates are unchanged. The four lifts remain distinct because H is injective; therefore H maps each entire endpoint fiber ONTO the corresponding new fiber.

If r is odd and s<1, S' lies strictly in the common column 1<x<2. The accepted actual-mirror L-subroom theorem connects S' to T', at arbitrary interior depths. Lift that physical path starting at any H(S) lift. Its ending lift is in the full T' fiber, which equals H of the full T fiber. Apply H inverse to obtain an original connection. H fixes every forbidden vertex lift. Folding back gives a finite ordinary corner-free specular path. An earlier actual target visit can be used as the endpoint.

The same argument works if q is odd and t<1. Existing results already handle s>1 or t>1, and s=t=1. If one mark equals 1 and only that mark has odd r or q, the shear does NOT move it into the open common column. The criterion in the statement therefore needs the refinement below; an even-depth denominator at a centered mark alone does not establish the result by this argument.

## Precise arithmetic criterion (the proved candidate)

Assume 0<s,t<=1, with at least one strict inequality. Put

    r0=2a/delta, q0=2b/delta.

There is a useful shear if an integer n>0 makes nr0,nq0 integers, with nr0 odd and s<1, OR nq0 odd and t<1. Let D be the lcm of the reduced denominators of r0,q0. This occurs exactly when D*r0 is odd at a noncentered source, or D*q0 is odd at a noncentered target. Any admissible n is a multiple of D, and an even integer cannot become odd by multiplication. Conversely n=D suffices whenever the condition holds.

Equivalently, among the endpoints whose depth/delta has maximal 2-adic denominator exponent, that exponent must be positive and at least one endpoint attaining it must be noncentered. If both s,t<1, the initial even-denominator condition is sufficient without further qualification. A centered endpoint uniquely attaining the maximal exponent is NOT covered by this proof.

For the equivalence, a depth with even reduced denominator 2^e*v, v odd, gives twice-depth denominator exponent e-1 and odd numerator. A depth with odd denominator gives twice-depth an even numerator. Multiplying by the lcm clears odd factors without changing these parity conclusions: exactly the endpoints of maximal positive e acquire odd integer displacement halves.

## What remains

The candidate theorem is the precise arithmetic criterion, including its noncentered-mark requirement. The opening even-denominator summary applies when both marks are strictly left of center. No conclusion is claimed for a centered endpoint uniquely carrying the largest exponent, or when both normalized depths have odd denominators. No reflection bound or complete rational classification follows.

Prescribed controls in horizontal-parity-check.py check the complete endpoint fibers and original physical rays obtained by inverse transport of fixed straight connections in the common column. They are exact checks of the stated mechanism, not parameter or direction discovery. Independent review is required before adding this candidate to accepted coverage.
