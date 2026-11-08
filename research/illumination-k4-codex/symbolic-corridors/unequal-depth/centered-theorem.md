# Every centered outer pair illuminates, at arbitrary depths

Codex01a18403, 6 November 2026. Parent theorem for independent review.
No rationality or commensurability restriction. No uniform reflection bound.

## Statement

In P=[0,2d]×[-h_-,0] union[d,3d]×[0,g] union[0,2d]×[g,g+h_+],
for all positive dimensions and all 0<a<h_-,0<b<h_+, the actual points
S=(d,-a), T=(d,g+b) admit a finite corner-avoiding specular connection.
The source/target horizontal coordinates are fixed to their chamber centers.
This does not prove the arbitrary-horizontal-endpoint goal.

Positive diagonal scaling reduces d=g=1. Set H=a+1+b,
alpha=a/H, beta=(a+1)/H, so 0<alpha<beta<1.

## 1. A complete centered vertical-path criterion

For integer n set L=1+2n, X(y)=1+2n(y+a)/H. Its portal values are
E1=1+2n alpha and E2=1+2n beta. The four already accepted compatible
charts have lower F2(X), middle1+F2(X-c), upperF2(X-u), with

    (c,u; E1mod4,E2mod4):
    (1,0;(1,2),(1,2)), (3,0;(2,3),(2,3)),
    (1,2;(1,2),(0,1)), (3,2;(2,3),(3,4)).

Every odd L maps to actual target x=1 under either upper shift u=0 or2.
The first portal is legal exactly when sin(pi n alpha)>0 and
cos(pi n alpha)!=0. Its middle shift is c=1 when the cosine is positive,
and c=3 when it is negative. For that chosen c, the second portal is legal
for some u exactly when cos(pi n alpha)cos(pi n beta)>0 and
sin(pi n beta)!=0. Replace n by -n if necessary to make the first sine
positive; cosine signs and sine nonvanishing are unchanged. Therefore a
successful chart exists if and only if some integer n has

    C_n = cos(pi n alpha) sin²(pi n alpha)
          cos(pi n beta) sin²(pi n beta) > 0.                 (1)

For completeness relative to ALL vertical-only paths: physical y increases
at constant positive speed; unfold vertical mirrors fixing the source chart.
Every target image is odd, since all mirror lines have integer x. Hence its
unfolded line has precisely L=1+2n. The lower fold is F2. Strict entry fixes
c=1 or3 modulo4 by matching value and velocity; strict exit fixes u=0 or2.
There are no other chart possibilities. Thus (1) is also necessary for this
mechanism. Sufficiency alone is enough for the main illumination theorem.

Every successful chart is finite and legal by the accepted strip lemma:
matching portal values and derivatives, strict portal coordinates, only
actual smooth vertical-wall contacts, actual endpoint and positive y motion.

## 2. Finite Fourier reduction to four exceptional lines

Suppose alpha,beta are not1/2. Then C_1!=0. Identity

    cos x sin²x = (cos x-cos3x)/4

gives

    C_n = [cos(nπα)cos(nπβ) + cos(3nπα)cos(3nπβ)
           -cos(nπα)cos(3nπβ) -cos(3nπα)cos(nπβ)]/16.

Each product expands into exponentials of frequencies(m alpha+k beta)/2,
with (|m|,|k|) in{(1,1),(3,3),(1,3),(3,1)}. Its Cesaro average is its
constant-modulo-integer coefficient: all nonintegral geometric averages
vanish. The first two products have nonnegative coefficients. A NEGATIVE
coefficient contributes to the average only on one of these four lines:

    beta=3alpha, 3alpha+beta=2,
    alpha+3beta=2, 3beta-alpha=2.                            (2)

These exhaust the possibilities: a negative product has frequencies
(3alpha±beta)/2 or(alpha±3beta)/2; use0<alpha<beta<1 to list the even
integer sums/differences. For example 3alpha-beta<2alpha<2, so its only
even integer can be0, and alpha-3beta lies between-3 and0, admitting only-2.
Outside(2), the mean of C_n is consequently nonnegative.

For a nonzero finite exponential sequence, the Cesaro mean of its squared
absolute value is strictly positive. To prove this, group equal frequencies
modulo integers first; orthogonality of the finite geometric averages gives
sum|coefficient|². It is positive because C_1!=0, so not all grouped
coefficients vanish. If every C_n<=0, its real bound |C_n|<=1 gives
C_n²<=-C_n. Averaging then forces a positive squared mean to be at most
the negative of a nonnegative mean, impossible. Thus some C_n>0 outside(2).
This step also works when positive-frequency resonances increase the mean.

## 3. The four lines reduce to one angle and a finite table

On each line(2), one coordinate theta has the other congruent to +3theta
or -3theta modulo2. Choose theta=alpha on the first two lines and theta=beta
on the last two. Consequently C_n equals

    cos(pi n theta)sin²(pi n theta)
    cos(3pi n theta)sin²(3pi n theta).                     (3)

If theta is irrational, its integer multiples modulo2 enter(0,1/6).
This follows from the elementary pigeonhole circle-density argument used in
the accepted equal-depth proof. At such a multiple both cosines are positive
and both sines nonzero, so C_n>0.

If theta=p/q is reduced, the orbit modulo2 is a uniform grid with spacing
G/q, G=gcd(p,2q)<=2. For q>=13 its smallest positive residue is strictly
less than1/6, proving the same result. It is therefore enough to check q<=12.
Exclude alpha or beta=1/2 here, since they are handled separately below.
The following complete finite table lists theta:witness n. A dash means no
positive value over its full period2q. Fractions not listed are excluded by
0<alpha<beta<1, theta reduced, or a coordinate equal to1/2.

|line|theta:witness n|
|--|--|
|beta=3alpha|1/4:–;1/5:–;1/7:1;2/7:3;1/8:1;1/9:1;2/9:4;1/10:1;3/10:3;1/11:1;2/11:5;3/11:4;1/12:1|
|3alpha+beta=2|2/5:–;3/7:2;3/8:3;4/9:2;4/11:3;5/11:2;5/12:5|
|alpha+3beta=2|3/5:–;4/7:2;5/8:3;5/9:2;6/11:2;7/11:3;7/12:5|
|3beta-alpha=2|3/4:–;4/5:–;5/7:3;6/7:1;7/8:1;7/9:4;8/9:1;7/10:3;9/10:1;8/11:4;9/11:5;10/11:1;11/12:1|

Each entry is an exact residue sign check, not a numerical trigonometric
approximation: cos(pi x) is positive at xmod2 in[0,1/2) or(3/2,2),
negative in(1/2,3/2), zero at1/2,3/2; sin(pi x)=0 exactly at integer x.
For dash entries, check n=0,...,2q-1, the entire period. The four lines
together yield only these three phase exceptions:

    (alpha,beta)=(1/4,3/4),(1/5,3/5),(2/5,4/5).

The executable finite certificate contains all40 rows and their complete
parameter filters; no extrapolation from a large-denominator search is used.

If alpha=1/2, every integer n has either its sine or its cosine zero, so
C_n=0. The same holds for beta=1/2. By Section1 no vertical-only path exists
on these lines. Combining the finite table with Section2 proves an exact
classification: centered vertical-only failure occurs precisely at

    a=b+1, b=a+1,
    or (a,b)=(1/2,1/2),(1/2,1),(1,1/2).

For the three isolated exceptions all C_n<=0 by the table, so none satisfies
(1); on every other allowed depth pair some C_n>0.

## 4. Actual horizontal-reflection repairs

For b=a+1 use the TWO-reflection formula in midpoint-repair.md, already
sent for independent review:

    S -> (2,h_+-a) -> (2-b/h_+,1+h_+) -> T.

It works for every h_+>b and h_->a, with both contacts in actual smooth
walls. Reflect y and reverse to cover a=b+1. This repair needs exterior
cap mirrors, whose clearance may be arbitrarily small.

For each of the three isolated depth pairs set v=4/(a+b+3),

    e=1+av, f=1+bv, p=e+v, p'=f+v, eta=1-(3-p)/v.

Their exact values are:

|a,b|v|e,f|p,p'|eta|
|--|--|--|--|--|
|1/2,1/2|1|3/2,3/2|5/2,5/2|1/2|
|1/2,1|8/9|13/9,17/9|7/3,25/9|1/4|
|1,1/2|8/9|17/9,13/9|25/9,7/3|3/4|

In every row,1<e,f<2,2<p,p'<3,0<eta<1 and p+p'+v=6.
The actual path is

    S -> (p,1) -> (3,eta) -> (p',0) -> T,

crossing portals at(e,0),(f,1). Its directions are(v,1),(v,-1),
(-v,-1),(-v,1). Thus exactly three actual smooth-wall reflections occur;
no exterior horizontal mirror is reached, so arbitrary outer clearances suffice.

Rescaling back to d,g preserves legality. This proves illumination for
EVERY centered depth pair in the theorem.

## Verification limits and next obligation

centered-check.py verifies the exact finite table after the hand reduction,
its chart choices and the three repair guard rows. Prescribed physical checks
also verify actual walls and corners. Independent review of this new theorem
is required before acceptance. It does not settle independent s,t, and it
uses no inference of darkness from a failed mechanism or a finite ray cutoff.
