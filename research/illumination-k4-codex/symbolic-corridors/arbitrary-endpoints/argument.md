# Arbitrary endpoint coordinates: a finite resonance reduction

Codex01a18403, 6 November 2026. Parent hand argument. Independent review
pending. This is a partial endpoint extension, not all-pair illumination.

## Fixed family and scope

Retain the twelve-wall room in ../proof.md:

    P = [0,2d]×[-h_-,0] ∪ [d,3d]×[0,g] ∪ [0,2d]×[g,g+h_+],

where all dimensions are positive. Consider actual interior points

    S=(s,-a), T=(t,g+b),
    0<s,t<2d, 0<a<h_-, 0<b<h_+.

The horizontal coordinates are unrestricted. No equality between a and b
is assumed. Set H=a+g+b, α=a/H, β=(a+g)/H.

**Proposition.** If S and T have no legal finite trajectory reflecting only
at vertical walls, then there are integers m,n,r, with (m,n)≠(0,0),
|m|,|n|≤32 and |r|≤64, satisfying

    mα+nβ=r,
    equivalently (m+n-r)a - rb + (n-r)g = 0.                 (1)

In particular, outside this FINITE union of planes in (a,b,g), every choice
of horizontal endpoint coordinates s,t illuminates by the explicit strip
formula below. Equation (1) is necessary for failure of this mechanism;
it is not sufficient for darkness, or even for failure of this mechanism.

Each plane is proper: all three coefficients in (1) vanish only when
m=n=r=0. Many listed triples describe the same plane; no enumeration or
claim about a number of distinct exceptional planes is needed.

## Attempt 1: compose the three foldings, retaining their common chart

Let F_w be the triangular folding map defined in ../proof.md. For an integer
M≥0 use the straight developed line

    X_M(y)=s+q_M(y+a),
    q_M=(t-s+4dM)/H,     -a≤y≤g+b.

Fold it as follows:

    lower: x=F_(2d)(X_M(y)),
    middle: x=d+F_(2d)(X_M(y)-d),
    upper: x=F_(2d)(X_M(y)).

The folds agree in position AND derivative wherever X modulo 4d belongs
to the open interval (d,2d). Thus it suffices that BOTH

    (s+α(t-s))/(4d) + Mα  modulo 1 lies in (1/4,1/2),
    (s+β(t-s))/(4d) + Mβ  modulo 1 lies in (1/4,1/2).       (2)

At y=-a, the lower folding gives actual s. At y=g+b, the developed
coordinate is t+4dM and the upper folding gives actual t. If (2) holds,
both portal crossings have d<x<2d and continuous velocity. Crossings of
the vertical fold lines strictly inside a band are smooth wall-interior
reflections. No horizontal wall is reached within a band, because y
increases strictly. No corner is reached at a portal because of (2).
There are finitely many fold-line crossings for any finite M.

For q_M=0 a successful line is simply a legal vertical segment; it has no
side-wall contacts. Otherwise every side-wall contact is transverse.
The target cannot occur earlier: its y coordinate is attained only at the
end. The outer horizontal boundaries are beyond the two marks.

This proves a SUFFICIENT criterion. Other chart transitions, target images
and trajectories can work when (2) fails. Do not replace sufficiency by
necessity in subsequent uses.

The strongest objection to an unconditional composition argument is real:
the previous packet gives a room/pair for which no vertical-wall-only
trajectory exists. It has a=b=g/2 and satisfies (1) with m=n=r=1.
Therefore Attempt 1 cannot establish all-pair illumination in this family.

## Attempt 2: reduce every failure of (2) to a bounded integer relation

The goal of this attempt is a necessary arithmetic obstruction, not another
list of successful rays. A finite obstruction list in (a,b,g) would replace
an unbounded collection of bounce words for the nonexceptional branch.

Write c=(3/8,3/8), and set

    f(u)=cos^64(πu),
    ρ=cos²(π/8)=(2+√2)/4,
    B(x,y)=f(x-3/8)f(y-3/8).

Functions are periodic modulo one. They satisfy 0≤f≤1. Outside the open
square O=(1/4,1/2)², one coordinate has circle distance at least 1/8 from
3/8, hence

    B(x,y)≤ρ^32.                                         (3)

The Fourier expansion of f is FINITE, with frequencies -32,…,32:

    f(u)=2^-64 Σ_(j=-32)^32 binom(64,32+j) exp(2πiju).

Its constant coefficient is C=binom(64,32)/2^64. Therefore B has constant
coefficient C² and frequencies (m,n) with |m|,|n|≤32.

Suppose no nonzero frequency satisfies mα+nβ∈Z. For each such frequency,
the geometric-series formula gives

    lim_(N→∞) (1/N) Σ_(M=0)^(N-1) exp(2πiM(mα+nβ))=0.

As the Fourier sum is finite, the average of B along the sequence in (2)
converges to C², for EVERY initial phase determined by s and t.

We now check C²>ρ^32 without a numerical approximation. Set
C_k=binom(2k,k)/4^k. Induction gives C_k≥1/(2√k): it holds at k=1,
and

    C_(k+1)/C_k=(2k+1)/(2k+2) > √(k/(k+1)),

since (2k+1)²>4k(k+1). Thus C²=C_32²≥1/128. Also √2<10/7,
so ρ<6/7, and direct integer arithmetic gives

    128·6^32 < 7^32.

Consequently ρ^32<1/128≤C². If the entire sequence avoided O, (3) would
bound every term of its averages by ρ^32, contradicting their limit C².
Some finite M satisfies (2), producing the actual connection.

Contraposition proves a nonzero bounded frequency with mα+nβ=r∈Z.
Since 0<α,β<1 and |m|,|n|≤32, |r|<64; the stated inclusive bound 64
is a harmless overapproximation. Substitution gives (1).

### A geometry-dependent finite bound, not a wall-count cutoff

When there is no bounded frequency relation, set

    η=min |sin(π(mα+nβ))| > 0,

over the finitely many nonzero frequencies in the square above. A finite
geometric sum has average absolute value at most 1/(Nη). The sum of
absolute Fourier coefficients of B is one. Therefore its N-term average
is at least C²-1/(Nη). Taking

    N > 1/[η(C²-ρ^32)]

forces some M<N to satisfy (2). This bound depends on the endpoint depths
and can diverge near a resonance. It does not contradict, or replace, the
earlier obstruction to a reflection cutoff depending only on wall count.

## Other endpoint placements

Two marks in the same open rectangular band have a direct segment. A
point on an open portal and a point in either adjacent band also have a
direct segment, legal in the actual room.

For one mark in an outer band and the other in the middle, the SAME
common-chart construction has just one portal condition. For example, for
S=(s,-a), T=(t,c), 0<c<g, use H=a+c, α=a/H and target image t+4dM.
If no integer 1≤k≤32 satisfies kα∈Z, averaging f alone proves that the
portal condition holds for some M. Its average constant coefficient C
exceeds ρ^32 by the stronger inequality already proved. The upper-band
case follows by reflecting y and reversing endpoint labels.

For a mark on one portal and another in the nonadjacent outer band,
there is again one variable portal phase: the starting portal coordinate
already lies in (d,2d). The same one-dimensional criterion applies to
the remaining flight-height ratio. Both marks on the portals connect
directly through the common core.

These are sufficient statements for all placement TYPES. They do NOT
dispose of their resonant endpoint values. In particular, arbitrary-endpoint
illumination in P remains unproved here.

## Prescribed noncommensurable control

Take d=g=1, a=√2, b=√3, h_-=a+1, h_+=b+1,
s=1/2, t=3/2, and prescribe M=12. Then q=49/(1+√2+√3).
The two developed portal coordinates lie respectively in (17,18) and
(29,30), so both residues modulo four lie in (1,2). check.py certifies
these strict inequalities with rational enclosures whose squares bound
2 and 3. There are eight lower, six middle and ten upper side-wall
contacts, all in band interiors; the portal strictness excludes corners.
No candidate selection loop or direction scan is run.

For this control the bounded relation is absent even without coefficient
bounds: (m+n-r)√2-r√3+(n-r)=0 forces all three rational coefficients
to vanish. Linear independence of 1,√2,√3 follows by isolating a radical
and squaring: if a nonzero √2 coefficient and a nonzero constant both
occur, a square yields √2 rational; if either vanishes, irrationality of
√3 or √(3/2) yields the same contradiction. Hence m=n=r=0.

## Additional phase repair: equal depths and equal horizontal coordinates

There is a stronger complete special case inside the resonance plane a=b.
For EVERY 0<s<2d and 0<a<min(h_-,h_+), the pair

    S=(s,-a), T=(s,g+a)

illuminates. Except when s=d and a=g/2, a vertical-wall-only connection
exists. That remaining pair has the three-contact path already proved
in the frozen packet, scaled to d and g. This is an existence statement;
it does not say those paths minimize reflections.

### Complementary folding chart

Put α=a/(2a+g)∈(0,1/2). Instead of the earlier target lift, use

    L_M=2d-s+4dM,
    q_M=(L_M-s)/(2a+g),
    E_M=s+α(2d-2s)+4dMα.

The first developed portal coordinate is E_M. The second portal coordinate
has sum 2d+4dM with the first, because the two portal times add to one.
It suffices that E_M modulo 4d belong to

    (d,3d) minus {2d}.                                    (4)

Use the original lower fold F_(2d)(X). If the first residue is in (d,2d),
use the middle fold d+F_(2d)(X-d); the second residue is then in (0,d).
If the first residue is in (2d,3d), use the middle fold
d+F_(2d)(X-3d); the second residue is then in (3d,4d).
In BOTH cases finish with the upper fold F_(2d)(X-2d).
At each portal the selected folds agree in value AND derivative, and give
a physical coordinate strictly between d and 2d. At the target the upper
fold gives F_(2d)(-s+4dM)=s. All other legality checks follow as for (2).

### Finding M for every depth

The initial normalized phase

    v=[s+2α(d-s)]/(4d)

lies strictly between α/2 and (1-α)/2. If α is irrational, the positive
integer orbit v+Mα is dense modulo one, so some M satisfies (4).
An elementary density proof suffices: pigeonhole N+1 multiples of α into
N equal intervals to obtain k>0 with 0<||kα||<1/N. Successive positive
multiples of kα move by that small signed distance; up to its reciprocal
they give a mesh on the circle with maximum gap at most that distance.
Take N large enough for the desired open interval. No reflection bound
independent of α is asserted.

If α=p/q in lowest terms, necessarily q≥3. For q≥5 choose

    j=floor(q(1/4-v))+1,
    M ≡ j p^(-1) (mod q),     0≤M<q.

Then v+j/q lies strictly above 1/4 and at most 1/4+1/q<1/2.
Since p is invertible modulo q, v+Mα has this same residue. Thus (4)
holds, with no trial-direction loop.

For q=3, α=1/3 and the unnormalized initial phase is (s+2d)/3.
Choose M=0 for s>d; choose M=1 for s≤d. The first choice is in
(d,4d/3); the second is in (2d,7d/3], and both satisfy (4).

For q=4, α=1/4 and the initial phase is (s+d)/2. Choose M=0 for
s>d, or M=1 for s<d. These give respectively (d,3d/2) and
(3d/2,2d). For s=d every residue is an integer multiple of d, so
this mechanism fails. Here α=1/4 is exactly a=g/2; use the three-
reflection path in ../proof.md instead. Its scaled form is

    (d,-g/2) → (5d/2,g) → (3d,g/2) → (5d/2,0) → (d,3g/2).

The no-vertical-only argument in that packet applies after rescaling
x by d and y by g. Such axis scalings preserve the specular law at
axis-aligned walls: the relevant velocity component changes sign before
and after scaling. Thus this exceptional placement actually needs a
horizontal reflection, as opposed to being an artifact of criterion (4).

This repairs a full equal-coordinate/equal-depth subfamily, not the whole
plane a=b with independently varying s and t. It also shows that the
five-reflection equality in the earlier symmetric construction was an
exception of that particular formula; a different chart can avoid it.
No frozen proof or its accepted/pending status is altered.

## Research realignment

What is proved at parent level: an actual common-chart connection criterion
and a finite union of depth-resonance planes containing every possible
failure of vertical-wall-only illumination between the outer bands.

What is additionally proved at parent level: all equal-depth, equal-horizontal-
coordinate pairs, with explicit modular selection for rational depth ratios
and a separate positive mechanism at the unique remaining placement.

What remains: repair exceptional pairs with independently varying horizontal coordinates and depths; reconcile the one-portal exceptions. No proof of darkness follows from a failed criterion. No numerical wall-count lower bound follows.

The two attempts have reached their stated bounded outcomes. Further ray
counts would not resolve the remaining universal implication. Independent
review should challenge this reduction before any exceptional-family effort.
