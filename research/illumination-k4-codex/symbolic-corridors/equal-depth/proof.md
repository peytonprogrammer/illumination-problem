# Equal-depth illumination across a two-portal corridor

Codex01a18403, 6 November 2026. Complete parent hand argument; independent
review pending. No universal wall-minimum claim.

## Statement and scope

For positive real d,g,h_-,h_+, let P be the union

    [0,2d] × [-h_-,0], [d,3d] × [0,g], [0,2d] × [g,g+h_+].

For every 0<s,t<2d and 0<a<min(h_-,h_+), the actual interior points
S=(s,-a), T=(t,g+a) admit a finite corner-avoiding specular connection.
The room is a strictly simple orthogonal twelve-wall polygon. The theorem
allows arbitrary real dimensions and independently varying s,t. It does not
cover unequal depths or all interior point placements in this room.

Missing implication addressed: compatible endpoint lifts must cross BOTH
open portals, with matching position and velocity, even on rational phase
orbits. Success criterion is a legal actual-target connection for every
parameter in the statement. The strongest objection is missing a rational
orbit or a boundary equality. Sections 4–7 cover these explicitly.

## 1. Reduce the horizontal endpoint region

If s,t>d, their direct segment lies in the common vertical strip and works.
If s<=d<t, use the L-shaped subroom

    R=([0,2d]×[-h_-,0]) union ([d,2d]×[0,g+h_+]).

Both endpoints are interior to R. The arbitrary-real L theorem in
`../../single-boundary-blocker/l-monotone-proof.md` supplies a connection
using only horizontal-wall reflections (and monotone in x). Every horizontal
wall of R lies on an actual horizontal wall of P: bottom, upper right, and
the lower left ledge. Artificial vertical walls of R are never contacted.
Thus that trajectory is legal in P. If t<=d<s, reverse and reflect y about
g/2 to apply the same argument. Consequently only s,t<=d remain.

Reflecting y about g/2 and reversing the path exchanges s,t and h_-,h_+.
We may assume 0<t<=s<=d. Rescale x by 1/d and y by 1/g. Independent positive
axis scaling preserves the specular law on axis-aligned mirrors: each
reflection flips exactly one velocity component, and diagonal scaling
commutes with those flips. Hence use d=g=1 below, with a now meaning a/g.
Write

    alpha=a/(2a+1), 0<alpha<1/2; D=s-t, 0<=D<1.

## 2. Four exact folding charts

Let F(x)=F_2(x): reduce x modulo4 to r in [0,4), and return r for r<=2,
or 4-r for r>=2. For u in {0,2}, epsilon in {+1,-1}, M an integer, set

    L=u+epsilon*t+4M,
    X(y)=s+(L-s)(y+a)/(2a+1),
    E1=X(0)=(1-alpha)s+alpha*epsilon*t+alpha*(u+4M),
    E2=X(1)=alpha*s+(1-alpha)*epsilon*t+(1-alpha)*(u+4M).

Choose a row of this table; intervals are residues modulo4, strictly open.

|u|E1 interval|E2 interval|c|
|--|--|--|--|
|0|(1,2)|(1,2)|1|
|0|(2,3)|(2,3)|3|
|2|(1,2)|(0,1)|1|
|2|(2,3)|(3,4)|3|

Fold X by F(X) below0, 1+F(X-c) between0 and1, and F(X-u) above1.
The neighboring maps agree in both value AND derivative at both portals.
For example, at residues in (2,3), F(X)=4-r and 1+F(X-3)=4-r;
for u=2 at the second portal r in (3,4), both middle and upper maps give
r-2. The other two interval pairs follow directly from F's definition.
All portal values lie in (1,2), so avoid every portal endpoint.
The endpoints are F(s)=s and F(L-u)=F(epsilon*t+4M)=t.

Each interior fold kink reflects at an actual vertical side wall of its
rectangle. Its height lies strictly within that band, so cannot be a corner.
If L=s there are no kinks and the same matched maps give a direct vertical
path. Otherwise there are finitely many transverse crossings, because X has
finite range. Physical y increases strictly from -a to1+a, so neither outer
horizontal wall nor any earlier encounter with T is possible. This proves
that every successful chart is an actual finite legal trajectory, regardless
of the number of vertical bounces.

## 3. A nonempty phase window for every irrational alpha

Choose u=2, epsilon=-1. Then E1+E2=D+2+4M. If

    E1 mod4 is in (1+D,2),

then E2 mod4 is in (D,1), a subset of (0,1). The u=2,c=1 chart works.
The window length is 1-D>0, including D=0. For irrational alpha,
E1/4 modulo1 is an irrational rotation with increment alpha, so enters this
open interval. An elementary density proof: pigeonhole N+1 fractional
multiples into N equal bins to find a nonzero integer n with 0<||n alpha||<1/N;
choose its sign to get a positive step delta<1/N. Successive j*delta up to
floor(1/delta) have circular gaps at most delta, and are all integer multiples
of alpha modulo1. Taking N sufficiently large hits any given open interval,
including after translating by the constant term of E1/4. Integers of either
sign are allowed in the charts. Every resulting M is finite.

## 4. Rational alpha: even denominators

Let alpha=p/q be reduced, with 0<p<q/2. The orbit E1 mod4 is a translated
q-point grid of spacing4/q, since multiplication by p permutes residues modq.
An open interval longer than4/q necessarily contains a grid point; select
its index by rounding and invert p moduloq.

If q is even, p is odd. For (s,t)!=(1,1), choose u=0,epsilon=+1,M=q/2.
Modulo4, the portal values are

    E1=2+V, E2=2+W,
    V=(1-alpha)s+alpha*t, W=alpha*s+(1-alpha)*t.

Both V,W lie strictly between0 and1; thus use c=3. This includes s=1 or t=s
provided they are not both1. If s=t=1 and q>=6, the window in Section3 has
length1>4/q, so its q-point grid supplies a chart instead.
The only even denominator left is q=4,p=1, s=t=1: a=1/2. Its explicit path
has three reflections:

    (1,-1/2) → (5/2,1) → (3,1/2) → (5/2,0) → (1,3/2).

All three contacts are in smooth actual walls; each successive direction
flips exactly the component normal to that wall. The initial/final legs
cross the two open portals at x=7/4. No other wall is hit.

## 5. Rational alpha: q>=9

If D<1/2, the Section3 window has length1-D>1/2>4/q.
If D>=1/2, use u=0,epsilon=-1. Now E1+E2=D+4M. Choosing

    E1 mod4 in (2,2+D)

puts E2 mod4 in (2,2+D) too. This is the c=3 chart; its window length
D>=1/2>4/q. The finite grid argument therefore covers all q>=9, including
the equality D=1/2. Only odd denominators3,5,7 remain.

## 6. Denominator3: three explicit reflections

Here alpha=1/3 and a=1. Set v=(6-s-t)/5>0,

    e_s=s+v, e_t=t+v, p_s=s+2v, p_t=t+2v,
    eta=1-(3-p_s)/v.

For all 0<s,t<=1 (ordering is unnecessary here),

    1<e_s,e_t<2, 2<p_s,p_t<3, 0<eta<1.

For example 5e_s=4s-t+6 and 5p_s=3s-2t+12 give their strict bounds;
exchange s,t for the others. The eta bounds follow from p_s<3 and
p_s+v=(2s-3t+18)/5>3. Also p_s+p_t+v=6.
The full path, showing portals as well as reflections, is

    S → (e_s,0) → (p_s,1) → (3,eta)
      → (p_t,0) → (e_t,1) → T.

The first and final portal crossings are interior. The three reflections
are at (p_s,1),(3,eta),(p_t,0). Their successive directions are
(v,1),(v,-1),(-v,-1),(-v,1), so obey the specular law. The middle
legs lie in the central rectangle and first meet its horizontal edges on
the ledges, not the portals. The first/last legs stay inside the outer
rectangles. Strict inequalities exclude all corners.

## 7. Denominators5 and7: a finite hand dispatch

All choices below use exactly the Section2 charts. A guard (A,B,C) means
A*s+B*t+C>0. Positive factors are suppressed. The four guards enforce the
two translated open portal intervals. No limiting or equality ray is used.

|alpha|u|epsilon|M|c|four guards|
|--|--|--|--|--|--|
|1/5|2|-1|1|1|4s-t+1; -4s+t+4; s-4t+4; -s+4t+1|
|2/5|2|-1|1|3|3s-2t+2; -3s+2t+3; 2s-3t+3; -2s+3t+2|
|2/7|2|-1|5|3|5s-2t+2; -5s+2t+5; 2s-5t+5; -2s+5t+2|
|3/7|2|-1|5|1|4s-3t+3; -4s+3t+4; 3s-4t+4; -3s+4t+3|

Each row holds on the entire domain 0<t<=s<=1. To see the only potentially
small guards, use s<=1 and t<=s: for example -5s+2t+5>=2t>0,
2s-5t+5>=5-3t>=2, and -2s+5t+2>=5t>0. The other rows have the
same explicit bounds with their displayed coefficients; alternatively each
guard is nonnegative at the closed triangle vertices (0,0),(1,0),(1,1),
and any zero vertex/edge is excluded by t>0. Thus all are strictly positive.

For alpha=1/7, select among these three rows:

|condition|u|epsilon|M|c|four guards|
|--|--|--|--|--|--|
|s<6t|2|-1|3|3|6s-t; -6s+t+7; s-6t+7; -s+6t|
|s>=6t and 6s+t>2|0|+1|3|3|6s+t-2; -6s-t+9; s+6t+2; -s-6t+5|
|s>=6t and 6s+t<=2|2|+1|2|1|6s+t+3; -6s-t+4; s+6t+4; -s-6t+3|

In the first row, 6s-t>=5s>0, 7-6s+t>=1+t>0,
7+s-6t>=7-5t>=2, and the last guard is the strict dispatch condition.
In the second, t<=s/6<=1/6, so 6s+t<=37/6<9 and s+6t<=2s<=2<5;
the first guard is strict by dispatch, and the third is positive.
In the third, s+6t<=6s+t<=2 (since s>=t), so the second guard is at least2
and the fourth at least1; the other guards are positive. The equalities
s=6t and 6s+t=2 therefore belong to legal charts, not uncovered boundaries.
This closes every remaining rational case.

## 8. Verification and conclusion

Sections1–7 prove the stated theorem by hand, using the existing L theorem
only for one endpoint strictly in the common core. The affine audit in
`check.py` helped extract Section7, but its finite decomposition is not a
premise of this proof. `physical-check.py` checks prescribed chart paths
against every edge of the actual polygon with exact rational arithmetic.
These are arithmetic controls, not a proof by sampling. Neither program
constitutes independent review. Review remains requested separately.

Realignment: every equal-depth outer pair in this precise family is covered
at parent-proof level. Unequal depths, general interior pairs, arbitrary
orthogonal polygons, and the universal22-wall minimum remain open here.
