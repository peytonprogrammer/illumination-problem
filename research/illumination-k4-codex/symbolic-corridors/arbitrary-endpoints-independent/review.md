# Independent review of the finite-resonance corridor foundation

Codex01a1a00f, 6 November 2026.

Verdict: ACCEPT the finite-resonance implication and the stated sufficient
placement criteria in arbitrary-endpoints/argument.md. ACCEPT its complete
equal-depth/equal-horizontal-coordinate subfamily, including the claimed
vertical-only obstruction at its exceptional placement. No mathematical
correction is required. This verdict is partial with respect to the NEW
unequal-depth goal: it does not establish the general unequal-depth theorem.

## Exact statement and quantifiers

Let all d,g,h_-,h_+ be positive. The room is the union
[0,2d]×[-h_-,0], [d,3d]×[0,g], [0,2d]×[g,g+h_+]. Its twelve boundary
segments form a simple orthogonal polygon; the overlaps at y=0,g are
strict open portals d<x<2d. Take S=(s,-a), T=(t,g+b), with 0<s,t<2d,
0<a<h_-, 0<b<h_+, H=a+g+b, alpha=a/H and beta=(a+g)/H.

The accepted implication is: absence of a legal finite vertical-wall-only
connection implies m alpha+n beta=r for some nonzero pair (m,n),
|m|,|n|<=32 and integer |r|<=64. Equivalently,
(m+n-r)a-rb+(n-r)g=0. Every listed plane is proper: its b coefficient
first forces r=0, its g coefficient forces n=0, then its a coefficient
forces m=0 if all coefficients vanish. Thus the sufficient nonresonant
branch has finitely many exceptional planes independent of s,t. No assertion
that all points on a plane fail, or that any are dark, is made or accepted.

## Common chart and actual geometry

For integer M>=0 let L=t+4dM and X(y)=s+(L-s)(y+a)/H. Use
F_(2d)(X), d+F_(2d)(X-d), F_(2d)(X) in the lower/middle/upper bands.
For X residue r in (d,2d), both adjacent formulas have value r and
derivative +1 at either portal. This is an identity on the whole OPEN
interval, so it matches physical velocity, not only portal position.
The two inequalities in argument.md are precisely these residue conditions.

The source maps to s and the final image maps to t. Fold kinks inside a
band occur only on that band's actual vertical sides, strictly away from
horizontal boundary endpoints; their horizontal velocity changes sign and
their positive vertical velocity is unchanged. The strict portal interval
excludes a kink at either junction and excludes every portal corner.
All intermediate noncontact points are interior. Even with negative
horizontal slope, the y coordinate increases, so every band is traversed
once, the outer horizontal walls are avoided and actual T is reached only
at the final y. The zero horizontal slope branch is a legal vertical
segment when its portal tests pass. Each finite M gives finitely many
transverse contacts otherwise. These arguments prove a sufficient criterion.
If there is no vertical-wall-only connection, every M in this chart must
fail; this one-way implication is exactly what the contraposition needs.

## Finite Fourier argument

cos^64(pi u) is periodic modulo one, nonnegative, at most one, with
coefficients 2^-64 binom(64,32+j) for -32<=j<=32. This follows directly
by expanding (exp(i pi u)+exp(-i pi u))^64/2^64, with frequency index
j=k-32; symmetry of the binomial coefficients permits the displayed sign.
Its constant coefficient is C=binom(64,32)/2^64, and the sum of the
positive coefficients is one.

Shift each factor by 3/8 and take the product B on the two-torus. Outside
O=(1/4,1/2)^2, at least one coordinate has CIRCLE distance at least 1/8
from 3/8. cos^2(pi u) decreases with this distance on [0,1/2], so
0<=B<=rho^32, rho=(2+sqrt(2))/4. Boundaries of O are included in this
upper bound. The shifted Fourier coefficients retain their absolute values;
B has support in [-32,32]^2, constant C^2 and total absolute coefficient
sum one. There are 4,225 frequencies, including 4,224 nonzero ones.

If none of those nonzero frequencies has m alpha+n beta integral,
every associated finite geometric average tends to zero. This is true
also for negative m,n and for every initial phase. The finite Fourier sum
therefore has limiting average C^2 without invoking any infinite-series
interchange, general equidistribution theorem or rational independence
beyond the finitely many stated frequencies.

For C_k=binom(2k,k)/4^k the ratio is (2k+1)/(2k+2).
The squared inequality needed to propagate C_k>=1/(2 sqrt(k)) reduces
exactly to (2k+1)^2>4k(k+1), whose difference is 1. Starting at k=1
proves C^2>=1/128 for k=32. sqrt(2)<10/7 gives rho<6/7, and the
independent integer check verifies 128*6^32<7^32. Hence
rho^32<1/128<=C^2. An orbit avoiding O would have every finite average
at most rho^32, contradicting that limit. Some finite nonnegative M
satisfies both strict portal inequalities.

Contraposition yields the claimed frequency relation. Because alpha,beta
are strictly between zero and one, |m alpha+n beta|<64 for a nonzero
pair in the box. The inclusive |r|<=64 bound is safe. Substitution gives
the displayed plane relation with the correct b and g signs.

The explicit finite bound is valid as well: the geometric-series numerator
has magnitude at most 2 and denominator magnitude 2|sin(pi theta)|,
so the normalized average is at most 1/(N eta), where eta is the strictly
positive minimum over the FINITE nonzero support. The shifted coefficient
absolute sum is one, bounding the nonconstant contribution by 1/(N eta).
Thus C^2-1/(N eta)>rho^32 forces entry for some M<N. This bound is
parameter dependent; neither this proof nor the controls give a uniform
reflection bound.

## Placement statements and inherited hypotheses

Same-band segments lie in a convex rectangle and avoid its boundary except
possibly an endpoint on an interior portal. A segment from an open portal
to an interior point of an adjacent rectangle has its open segment in that
rectangle's interior. Two portal points connect through the common strip.
For an outer/middle pair the unfolded target t+4dM folds by
 d+F_(2d)(t-d)=t because d<t<3d. There is one free portal condition,
so the same finite argument using a single factor f works if no
k alpha is integral for 1<=k<=32. Its constant C exceeds rho^32,
as C>=C^2>rho^32. A starting portal in the nonadjacent-outer case
already lies strictly in the common chart; only the other portal varies.
Reflection in a horizontal line and endpoint reversal gives the remaining
orientation. These are sufficient criteria; the resonant cases remain open
within this packet. No illumination monotonicity or artificial-wall lemma
is required for any of these statements.

## Equal-coordinate/equal-depth appendix

The alternate upper fold F_(2d)(X-2d) sends its target lift
2d-s+4dM to s. The portal phase sum is 2d+4dM. If the first residue
lies in (d,2d), the second lies in (0,d) and the middle offset is d.
If it lies in (2d,3d), the second lies in (3d,4d) and the middle offset
is 3d. In each case the two adjoining affine functions AND derivatives
agree on the entire open residue interval. The physical portals lie
strictly in (d,2d). The same actual-wall/finite/first-arrival argument
therefore applies.

The initial normalized phase v lies strictly between alpha/2 and
(1-alpha)/2. For irrational alpha, pigeonhole gives a positive k with
nonzero signed step of magnitude delta<1/N modulo one. Positive multiples
j k alpha for 0<=j<=floor(1/delta) give a circle mesh of gap at most
delta, with either sign of step. Translating this mesh by v hits any
open interval longer than delta. Consequently some nonnegative M hits
either permitted interval; a negative-index recurrence is unnecessary.

For reduced alpha=p/q in (0,1/2), q>=3. At q>=5 the exact floor formula
j=floor(q(1/4-v))+1 makes v+j/q strictly greater than 1/4 and at most
1/4+1/q<1/2. Choosing M congruent to j p^-1 modulo q preserves that
residue, even when j is negative. The q=3 prescriptions give residues
(s+2d)/3 in (d,4d/3) for s>d, or 2d+s/3 in (2d,7d/3] for s<=d.
For q=4 the two strict noncentral branches likewise lie in (d,2d).
All equality s=d cases are explicitly assigned; the q=4 center uses the
three actual contacts (5d/2,g), (3d,g/2), (5d/2,0), whose portals are
7d/4. Directions change respectively in the y,x,y components, and all
three contacts are strictly inside actual walls. Arbitrary positive
horizontal/vertical scaling preserves component sign changes and hence
the specular law at these axis-aligned walls.

I also independently checked the cited NO-vertical-only obstruction rather
than accepting a failed common chart as such a result. Normalize d=g=1,
a=b=1/2,s=t=1. Any vertical-only path has constant positive vertical
velocity. Reflections in integer-x mirrors send target x=1 to an odd
integer. Thus its developed slope r is integral. Even r misses the first
open portal. Odd r can enter it only in classes 1 or 3 modulo 8, both
at x=3/2, with entering middle slope v congruent to 1 modulo 4.
The next physical y=1 coordinate is 1+F_2(1/2+v)=5/2, on the ledge.
That requires a horizontal reflection, contradicting a vertical-only path.
This is independent of the outer clearances. The three-contact path is a
positive connection, so the obstruction is not darkness.

Only the fold definition and this three-contact/obstruction subsection of
the older symmetric proof are dependencies here; the older repetition-count
and five-contact formulas are unnecessary to this verdict. The complete
later equal-depth theorem already has a separate frozen acceptance, which
this review preserves rather than reopens or silently extends.

## Reproducible independent checks and limits

Run `python3 .context/illumination-k4-codex/symbolic-corridors/arbitrary-endpoints-independent/check.py`.
It imports or executes no peer code. It checks the exact binomial and integer
threshold arithmetic and three whole-interval affine chart identities.
It builds 48 prescribed unequal-depth common-chart paths, one zero-slope
path, 145 prescribed modular diagonal paths, and one prescribed irrational
path: 195 actual-wall paths and 2,099 wall contacts, all passing.

The irrational control uses the independent exact field Q(sqrt(2),sqrt(3)),
with four rational coefficients, conjugate-product inversion and adaptive
rational sign enclosures verified by integer square roots. No floating-point
trajectory claim is used. Its band contact counts are exactly 8,6,10, with
the actual S and T and strict portal velocities checked. Linear independence
of 1,sqrt(2),sqrt(3) follows by isolating one radical and squaring, treating
zero coefficients separately; it removes all nonzero frequency relations
for that example, not merely those in the bounded box.

The physical checker checks interior marks, first intersections with ALL
actual polygon edges, strict mirror interiors, boundary nonoverlap,
positive specularity, segment interior points and no earlier target hit.
These counts are controls of prescribed formulas, not a sampled proof,
discovery effort, valid-room census or universal reflection bound. Arbitrary
real parameters are justified by the hand arguments above.

No proof finding remains for this foundation packet. General unequal depths
ON the exceptional planes remain unproved by it. No acceptance of a later
unequal-depth replacement, all interior pairs, arbitrary twelve-wall rooms,
universal wall minimality follows. This is independent AI review,
not formal verification or external expert refereeing.
