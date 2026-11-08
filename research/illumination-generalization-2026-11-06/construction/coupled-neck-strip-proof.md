# Two-neck illumination outside finitely many affine strips

Candidate A19, Codex01a18403. Independent review pending. This is a quantitative strengthening of the frozen A18 candidate and is conditional on its geometric splice lemma. It does not prove the cap-free W<=21 objective.

## 1. Fixed beam and exact target reduction

Use precisely the fixed three-chamber/equal-width geometry of `coupled-neck-irrational-proof.md`, Sections 1--4. In particular the actual source and target, the mouths, the finite end words and a legal first-transit middle word are fixed. Write their constants as

    w,a,b,d > 0,
    I=(u,v), delta=v-u>0,
    J an open circular arc of length ell in (0,1/2),
    D=L1+L2+a+b+d,
    rho=(L1+a)/D,
    tau_N=(K+2wN)/D,
    phi_N=alpha/(2w)+(K/(2w)+N)*rho modulo 1.

The exact geometric implication used here is: any INTEGER N with tau_N in I and phi_N in J gives a finite actual corner-avoiding S-to-T path. No target image or intermediate mouth phase is chosen independently of N. All conclusions below are conditional on independent acceptance of that implication.

Fix an integer Q>4/ell and constants

    C = 4wQ/delta,
    D0 = 8w/delta.

If D>D0 and the actual S,T fail to illuminate, then there are integers 1<=q<=Q and 0<=p<=q with

    |q(L1+a)-pD| <= C.                                      (1)

Equivalently, every sufficiently long room outside the finite UNION of strips (1) illuminates. The constants depend on one fixed chamber/mark beam; there is no W-uniform bound.

## 2. A finite mesh from Dirichlet pigeonholing

For every rho in (0,1), there are 1<=q<=Q and an integer p with

    gamma=|q*rho-p| < 1/Q.                                  (2)

For completeness, put the Q+1 fractional parts of 0,rho,...,Q*rho into Q equal half-open subintervals of [0,1). Two lie in the same subinterval. Subtracting their indices gives (2). Since 0<q*rho<q and the error is <1/Q<1, the integer p lies between 0 and q.

If gamma=0, (1) holds with zero left side, so there is nothing more to prove for this pair p,q. Suppose gamma>0. Put k=floor(1/gamma). The circle points

    0, q*rho, 2q*rho, ..., kq*rho modulo 1

have maximum circular gap at most gamma: up to reflection they are the equally spaced points 0,gamma,...,k*gamma on one turn, with remaining gap 1-k*gamma<=gamma. A duplicate endpoint, when 1/gamma is an integer, does not change this bound. In particular their maximum gap is <ell because gamma<1/Q<ell/4.

These mesh points are contained among the consecutive orbit points of indices 0,...,m, where m=q*k. Adding the other orbit points cannot increase the largest gap. Hence the first m+1 consecutive orbit points meet EVERY translate of J. Every translated block of m+1 consecutive indices has this same property. Crucially this is a finite net, without any claim that rho is irrational or that an infinite orbit is dense.

## 3. Fit the mesh inside the actual slope window

For the pair p,q supplied by (2), suppose the affine deviation is greater than C. Then

    D*gamma=|q(L1+a)-pD|>C,
    m=q*floor(1/gamma)<=q/gamma<=QD/(D*gamma)<D*delta/(4w).

The OPEN real interval of permitted integers N, namely

    ((D*u-K)/(2w), (D*v-K)/(2w)),

has length H=D*delta/(2w). Since D>D0, H>4. Therefore

    m+2 < H/2+2 < H.

Any open real interval of length greater than m+2 contains a block of m+1 consecutive integers strictly inside it. On that block, the values phi_N are a translate of the finite orbit net from Section 2. One therefore lies in J, while its slope tau_N lies strictly in I. The geometric implication in Section 1 produces an actual legal illuminating path.

Its contrapositive proves (1) for every physically dark pair. Failure of this one beam is also confined to these strips, but membership in a strip does not prove that the beam fails or that the pair is dark.

## 4. What is stronger than A18

A18 confines possible divergent failures to rational LIMIT ratios. This theorem confines them to a fixed ABSOLUTE distance from rational affine length relations. For example, consider fixed 0<p<q, fixed constants and lengths

    L1=p*M+sqrt(M),  L2=(q-p)*M,  M tending to infinity.

The ratio tends to p/q. For the reduced version of that ratio, the absolute deviation in (1) grows as a nonzero constant times sqrt(M), rather than staying bounded. Every other one of the finitely many rational ratios has deviation of order M. The rooms therefore illuminate for all sufficiently large M. The same conclusion holds with any perturbation tending to infinity but o(M), of either sign, with lengths remaining positive.

This is a new class of parameters compared with A18; it is not a larger fixture count. It still leaves bounded affine detunings near the finite rational relations.

## 5. Exact lattice consequence and residual problem

For orthogonal chambers and marks with INTEGER coordinates, all unfoldings in the fixed words have integer translations. Thus a,b,d are integers. If the neck lengths L1,L2 are integers as well, then

    c=q(L1+a)-pD

is an integer. In the dark case only the finite integer list |c|<=floor(C) remains. After expanding D, each residual relation is

    (q-p)*L1-p*L2 = c-(q-p)*a+p*(b+d),                       (3)

for integers 1<=q<=Q, 0<=p<=q, and |c|<=floor(C). All nonnegative integer solutions of each relation (3) form at most one arithmetic ray with primitive step

    (p/g, (q-p)/g),  g=gcd(p,q),

or an empty set, after choosing its first positive solution. The assertion includes p=0 and p=q: the relation fixes one length, while the other may grow. In particular those two endpoint-ratio cases do not produce a sequence in which BOTH lengths diverge. Nonreduced p,q can be retained harmlessly; reducing them can only decrease the denominator and deviation.

For any fixed rational lattice after a common similarity, the same conclusion holds with scaled integer constants. This is a finite reduction ONLY within this fixed three-chamber family. It neither bounds the number/geometry of chambers in arbitrary W<=21 disks nor proves illumination along any residual arithmetic ray. The fixed beam intervals can be shrunk to rational endpoints, if desired, making Q,C,D0 explicitly rational/integer once the finite words are known.

## 6. Recover the sharper denominator cutoff

The strip theorem initially permits denominators up to Q. A finite additional argument recovers A18's sharper cutoff q<=1/ell. Define

    eta = min {ell-1/j : 1<=j<=Q, j>1/ell} > 0,
    D1 = max(D0, 4C/eta, 4w*(Q+2)/delta).

The minimum exists because Q>4/ell. Suppose D>D1 and the strip produced in Section 3 has reduced ratio p'/q', with g=gcd(p,q), p'=p/g and q'=q/g. Its reduced absolute deviation is at most C/g<=C. If q'>1/ell, then

    |rho-p'/q'| <= C/(q'*D).

The first q' orbit points at the exact rational step p'/q' form a q'-grid. Moving to rho displaces each of these points by at most C/D in circular distance. The maximum gap is therefore at most

    1/q' + 2C/D < 1/q'+eta/2 < ell.

For this last inequality use eta<=ell-1/q'. These q' points form a finite net for every initial phase. The allowed slope interval has length D*delta/(2w)>2*(Q+2), and contains q' consecutive integers strictly inside it. The net again yields an actual legal path, contradicting darkness.

Consequently, for D>D1 every failure lies in one of the strips (1) with REDUCED p/q and q<=1/ell. This is precisely A18's finite rational set, now with a bounded absolute affine deviation, rather than an unspecified shrinking neighborhood. For integer data the finite residual arithmetic rays in Section 5 may therefore use this sharper denominator cutoff.

## 7. Verification and scope

This proof uses elementary finite pigeonholing and the frozen A18 geometric splice. No room, direction, word or ray discovery, numerical sample, external literature search or computational assertion is used. Constants deliberately have slack to preserve all open guards.

Independent review must check both the finite-mesh constants here and the actual endpoint-preserving splice upstream. The cap-free canonical45 W<=21 objective remains OPEN. Rational residual rays, moving/degenerating chamber or endpoint data, unequal/shrinking widths, diagonal chambers and a complete room decomposition remain unresolved.
