# Independent acceptance of the corner-fixing vertical twist reduction

Codex01a1a00f, 6 November 2026.

Verdict: ACCEPT the pinned vertical-twist.md without mathematical correction.
In a room with rational normalized a,b,h_-,h_+, every allowed outer pair
illuminates whenever at least one normalized horizontal mark s,t is irrational.
Combined with the previously accepted height reductions, the full objective
now remains only when ALL SIX ratios a/g,b/g,h_-/g,h_+/g,s/d,t/d are
rational. That class is unbounded and is not closed by this review.

## 1. Four copies, all eight annuli and forbidden regular points

Normalize d=g=1 by positive axis scaling, which preserves axis specularity.
The four reflected copies labeled(x-sign,y-sign) have translation edge
gluings: reflecting an edge changes the corresponding sign, and signed
Cartesian coordinates on the two copies differ by a constant translation
along that edge. Thus a geodesic avoiding ALL vertex preimages folds to an
ordinary corner-avoiding billiard path. Convex corner preimages can be regular
on this surface; avoiding only cone singularities would be insufficient.
The peer explicitly retains every vertex lift as forbidden.

At fixed physical x in(0,1), the lower and upper vertical billiards are
separate intervals(-h_-,0) and(1,1+h_+), with closed unfolded vertical
circumferences2h_- and2h_+. At x in(1,2) the interval is
(-h_-,1+h_+), circumference2(h_-+1+h_+); at x in(2,3) it is(0,1),
circumference2. For each interval there are two x-sign copies; the two
y-sign halves close into its single vertical annulus. These are exactly
eight open unit-width annuli after cutting every lifted integer-x line.
Their area8(h_-+1+h_+) equals four times the polygon area. More than
an area check is used: the fixed-x interval classification directly covers
every non-cut surface point, so no component or smaller boundary cylinder
has been lost. Cutting a larger cylinder into artificial unit strips is legal.

All four circumferences are positive rationals. Taking L as the lcm of
their reduced numerators makes L/C integral for every C. L is a positive
integer and is even because C=2 is included.

On signed j<X<j+1 the map(X,[Y])->(X,[Y+L(X-j)]) has inverse with
-L. It fixes BOTH boundary circles pointwise, since the shifts are0,L,
respectively, and L is divisible by that annulus's C. Boundary segments may
be identified to different annuli with different C; pointwise identity on
all of them still makes the quotient map well-defined and invertible.

At a regular cut point take one translation chart with transverse coordinate
xi=X-X_boundary. On either side the map is locally(xi,Y)->(xi,Y+L xi):
the extra0 or L is a full number of local vertical periods. Hence derivatives
agree across original mirror cuts AND artificial subdivisions, regardless
of different circumferences or chart-origin translations. Original vertical
mirror gluings change signed X by an even integer; all cut fibers remain
integer-x in those charts. Horizontal mirror gluings merely translate Y.
Thus this is a genuine globally affine surface automorphism with derivative
[[1,0],[L,1]], not a collection of incompatible cylinder maps.

Each polygon vertex in each signed representation lies on an integer-x cut.
Every incident boundary arc is fixed pointwise; as X approaches its boundary,
the displacement modulo C tends to0. This gives a continuous extension at
all vertices, as does the inverse. Consequently the map fixes EVERY forbidden
vertex preimage, including regular convex corners. It cannot send an allowed
geodesic through a forbidden regular lift on transport back.

## 2. Endpoint motion and simultaneous returns

For a physical left-chamber x=s, the identity-copy shift is ell L s modulo
2h_-. Subtracting the integer j from signed X changes the shift only by
an integer number of full vertical periods. In the upper chamber the
identity x-sign target shifts by ell L t; the x-sign eta target shifts by
eta ell L t modulo2h_+. At a net return small enough to stay within the
same chamber and same y-sign copy, depths therefore become
 a'=a-delta_s, b'=b+eta delta_t.
The x coordinate is unchanged, including its x-sign label.

Pigeonhole N^2+1 multiples into N^2 boxes gives a nonzero integer ell
with both signed normalized return errors arbitrarily small. Rational L
and rational circumferences imply that an irrational horizontal mark has
an irrational normalized rotation, so a nonzero ell cannot make its error
zero. For increasingly fine boxes, a fixed finite set of nonzero indices
cannot supply arbitrarily small errors; arbitrarily small nonzero returns
are indeed available. Choose their magnitudes smaller than all relevant
original positive wall clearances, and, later, any additional fixed
rational-lattice threshold. The chosen image points are then in the SAME
intended copies, not just somewhere in the folded polygon.

A source return delta_s at irrational s is irrational: it is nonzero integer
ell times rational L times s, minus an integer multiple of rational2h_-.
The analogous fact holds for t. This justifies the needed new irrational
depths without any numerical approximation.

## 3. Transport and endpoint-copy control

Applying A^-ell to a straight geodesic changes its chart velocity by the
same inverse shear in every translation chart; it remains a straight
geodesic. All vertex preimages are fixed, so every original forbidden point
is avoided. A finite segment with interior endpoints and no forbidden
vertex has finitely many crossings of the finite original mirror seams.
It has positive clearance from their endpoints; transversal crossings cannot
accumulate away from an endpoint. Coinciding with a seam would require either
an endpoint on that seam or passage through a seam endpoint, both excluded.
Thus its fold is an ordinary FINITE original-room billiard path. If it meets
actual T before the selected final lift, take the prefix ending at the first
encounter. A global reflection bound is not required.

The twist does NOT generally commute with the reflection deck maps. The
argument must therefore connect the actual selected image target lift.
The three cases in the peer proof do this correctly:

- One horizontal mark rational: use reflection/reversal to make s irrational,
  t rational. A power ell0 makes ell0 L t divisible by2h_+, fixing ALL
  four target lifts, including their y-sign variants. Integer-cut target
  t=1 is fixed pointwise as well. Along multiples of ell0 a small irrational
  source return exists. The accepted depth theorem connects that image source
  to the target; whichever lift it reaches is fixed, so inverse transport
  reaches the ORIGINAL target.
- Both irrational and1,s,t rationally independent: after any nonzero small
  simultaneous return, a'=rational-ell L s and b'=rational+ell L t
  remain independent together with1. Any integer phase relation would imply
  an integer relation among1,a',b', hence among1,s,t. The generic foundation
  consequently gives the SPECIFIC common chart with u=0,epsilon=+1 and
  target lift t+4M. Its upper horizontal fold derivative is+1 and its y
  never reflects. Its endpoint is exactly the identity-sign target copy,
  which is A^ell applied to the original identity target lift.
- Both irrational but rationally affine dependent: the next section verifies
  the preselected x-sign eta target. No arbitrary later choice of lift is
  substituted for it.

## 4. Dependent irrational marks, exact rational lattice and primitive relation

If1,s,t have rank2 while both marks are irrational, their unique affine
relation has t=eta(p/q)s+mu, with positive coprime p,q, eta=+/-1 and
rational mu. Neither irrational coefficient can vanish, so these possibilities
exhaust the case. Both irrational marks are strictly less than1 after the
L reduction.

For the small signed returns,
 p delta_s-eta q delta_t
 =-eta ell L q mu-2p h_- k_s+eta2q h_+ k_t.
All three coefficients are rational and have a common denominator D independent
of ell,k_s,k_t. Taking the simultaneous errors so small that the left side
has magnitude<1/D forces it to be EXACTLY0. This uses a discrete rational
lattice, not a limiting argument. Therefore eta delta_t=(p/q)delta_s and
 R=p a'+q b'=p a+q b>0 is rational.

Both transformed depths are irrational and positive. With
H'=[(q-p)a'+q+R]/q, a rational alpha or beta would make a' rational,
unless the respective constant q+R or p+R vanished; both are positive.
This argument also covers p=q, where H'=1+R is rational but both phases
are still irrational. The needed orbit is therefore a rank-one irrational
orbit, possibly with disconnected closure, not a finite rational orbit.

Let k be the reduced denominator of R and w=kR its positive coprime
numerator. A phase relation is exactly
 (m+n-r)a'-r b'+n-r=0.
Its irrational coefficient forces q(m+n-r)+pr=0. Coprime p,q give
m+n-r=p h,r=-q h for an integer h; the rational part then forces
m=h(p+R),n=-h(q+R). The least positive admissible h is k. Thus the
primitive relation is
 (m,n,r)=(kp+w,-kq-w,-kq).
A common divisor divides kp and kq, hence k, and also w. Since gcd(k,w)=1,
the triple is primitive. Its normal alone need not be coprime; the already
accepted full-component closure proof is essential.

The box width is k(p+q)+2w. Since p+q>=2,k>=1,w>=1, it is>=5
except precisely p=q=k=w=1. In every larger-width case, the accepted
open-box image lemma supplies a common chart for u=0 and the PRESELECTED
sign epsilon=eta. Its length>4 attains every phase residue; this reasoning
does not need an independent ordering of the two horizontal marks.

In the sole width4 case R=1 and(m,n,r)=(2,-2,-1). The common-box
image is(-2,2), while C=s-eta t lies in(-1,1) for eta=+1, or in(0,2)
for eta=-1. It is strictly inside, including all affine relations compatible
with the two irrational marks. The disconnected closure is fully included
by the previously accepted lemma. No endpoint equality was removed silently.

The common upper fold derivative at eta t+4M is eta; with no horizontal
reflections, its y-sign is positive. Hence the reached copy is precisely
x-sign eta/y-positive, fixed BEFORE choosing the chart. This image point
is A^ell(T^eta), because its depth is b+eta delta_t. Inverse transport
therefore reaches a lift of ORIGINAL T. This closes the last irrational
horizontal case.

## 5. Independent reproducible checks and limitations

Run `python3 .context/illumination-k4-codex/symbolic-corridors/unequal-depth-independent/twist-check.py`.
No peer program is imported or executed. The checker independently verifies:

- Three rational circumference fixtures with L=20,30,574; all eight annuli,
  area exhaustion, boundary-period divisibility,192forward/inverse annulus
  round trips and144signed vertex representations on fixed cuts.
- A prescribed N=20 simultaneous pigeonhole return for
  s=sqrt(2)/2,t=sqrt(3)/2, giving ell=15 and strict same-copy clearances;
 20primitive phase/width arithmetic controls, including the width4 exception.
- The TWO explicitly prescribed original-room transport directions
  (24,-959) and(102/5,-815), with s=sqrt(2)/2 and t respectively s or1-s,
  a=1/2,b=1,h_-=h_+=2. An independent affine quadratic-pair nearest-wall
  tracer checks every actual edge with exact integer-square sign comparisons.
  It reaches actual T first at time5/2, after respectively1,110and933smooth
  contacts, and independently checks both reverse paths:4,086contacts total.
  Final velocity parity gives the intended target copies(+,+) and(-,+).

The tracer has a proved control-specific time bound, not a guessed reflection
cutoff: all supporting mirror lines have integer coordinates even after
unfolding, so the time horizon crosses at most |vx|T+|vy|T+4 such lines.
It validates original polygon paths rather than just transformed endpoint
equations. The edge words also match the parent receipts after independent
tracing. These controls support the full hand surface/return/copy proof above;
they do not prove the arbitrary-irrational theorem by sampling.

All three parent hashes match the frozen request. Prior proof/review inputs
are preserved. The full native goal is STILL OPEN for all six normalized
parameters rational, unbounded denominators, unequal depths and noncentered
left-left marks. The width ratio d/g remains arbitrary positive real under
axis scaling. The separate fixed-rational-room continuous certificate is
awaiting peer review and is not substituted for the universal rational class.
No darkness, all-interior-pair, other-family or universal wall-minimum
claim is made here.
