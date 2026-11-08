# TR06: test a precise unbounded-period iteration premise

Hand candidate, before prescribed verification. This is a proposed algorithmic
premise for TR02, not a new claimed illumination theorem.

Keep the original ordered spiral and lower-left / bottom placements of TR02.
Put d0=h-u, g0=2(H-h), g1=h-c, d2=c-v, D=d0+g0+g1+d2,
R=A-w, B=A-l, z=A-t. Fix source and target signs positive.

For a trial tau>0, use nearest signed periods successively:

    n=floor((s+d0*tau+a)/(2a)), z0=s+d0*tau-2na;
    m=floor((z0+g0*tau)/(2A)), z1=z0+g0*tau-(2m+1)A;
    k=floor((z1+g1*tau+R)/(2R)), z2=z1+g1*tau-2kR;
    j=floor((z2+d2*tau-z+B)/(2B)).

Restrict the trial domain to strict |z0|<a, |z1|<R, |z2|<R.
The target root associated to these periods is

    F(tau)=[2na+(2m+1)A+2kR+2jB+z-s]/D.

Candidate premise to assess: F is nondecreasing on this admissible domain,
so a U-style finite monotone fixed-point iteration might apply with
unbounded bottom periods. A fixed point in this domain would give the
TR02 actual target equation. Monotonicity alone would still need an
invariant admissible interval and finite termination; neither is assumed.

Strongest objection: when k increases by1, z2 decreases by2R. Nearest
target rounding can then decrease j by1. The numerator jump is
2R-2B<0. The bounded success criterion is to settle this exact premise
with full strict portal guards, not infer a general impossibility for
every possible matching algorithm or for illumination.

No new discovery effort is proposed. The following hand challenge uses
two prescribed rational slopes at one already defined spiral geometry.
It does not restart the reviewer's closed fixed-input TR02 search.
