# Arbitrary upper depth: a literal-preservation obstruction

Reviewer hand result for reciprocal challenge. This refutes a particular extension of UP01/UP02's selector, not illumination or all possible seeds. No room/ray discovery, numerical census, new engine, or clock was used.

## Claim being challenged

For a jointly strict first-cap/left-loop seed with cap phase off the endpoint class, can one always adjust the slope while preserving both literal first-entry residuals to reach the right cap mouth, as in UP01, at arbitrary native upper depth?

**No.** There is a variable family of genuine original rooms and target-compatible jointly strict seeds for which every such adjustment, even allowing real slope increments rather than just the author's integer grid, leaves the cap phase unchanged modulo its full physical period. It never enters the right mouth. This is a restriction on a repair map starting from the displayed seed; another seed or another itinerary remains possible.

## Exact preservation lattice

Write upper depth dp=2j, f=h-b, and slope increment Delta. Keeping the literal initial residual zpre while changing its actual fold index forces

    dp*Delta in 2A Z.

Keeping the literal left-loop residual z0 once zpre is fixed forces

    2f*Delta in 2a Z.

For a=Pe,A=Ne and gcd(P,N)=1 these equalities hold simultaneously exactly when

    Delta/e in (NP/gcd(Nf,Pj)) Z.

This is an equality of additive subgroups of the reals. To verify it, set Delta/e=N*k/j=P*m/f and solve Nf*k=Pj*m in integers; the least positive solution gives NP/gcd(Nf,Pj). The result does not assume Delta/e is an integer. Requiring the target q grid can only shrink this group further.

The cap phase then changes by C*Delta=2epsilon*Delta modulo 2A. Its orbit must be computed using this subgroup; UP01's spacing-2e conclusion is not automatic once dp=2N*ell is removed.

## A full parametric failure of this repair map

For every odd integer N>=7 take

    e=4, P=1, L=4, a=4, A=4N,
    l=4(N-4), w=4(N-1),
    b=2,c=3,h=4,H=N+5,
    S=(2,6), T=(4N-8,2).

All required original ordered inequalities hold. The polygon has exactly the prescribed strictly simple ten-wall ordered-spiral boundary. S,T are distinct even-even interior points. N>P+L; h is even, c is odd; epsilon=N+1 and gcd(P*epsilon,N)=1. Thus this family retains the other odd-width UP02 conditions and drops only the source-depth congruence dp=2N*ell. Here dp=2, f=2 and gcd(2N,1)=1, so every real increment preserving both residuals is

    Delta=4N*k, k integer.

Consequently C*Delta=2(N+1)*4N*k is an integer multiple of 2A=8N: the cap phase is frozen modulo its full period.

The developed duration is D=2(N+5), z=A-t=8. Choose the integer target-grid seed

    q=N^2+(9N-3)/2,
    tau=(A+z-s+2e*q)/D=4N-3/(N+5).

Put d=N+5>=12. The actual first cap index is npre=1 and its literal residual is

    zpre=s+2tau-2A=2-6/d,

strictly in (0,4). After the left loop of duration 4, the actual left index is nleft=2N, with literal residual

    z0=zpre+4tau-2a*(2N)=2-18/d,

strictly in (0,4). These are simultaneous genuine first-entry and return-mouth guards on one actual initial branch.

The cap phase X=z0+2(N+1)tau reduces modulo 2A to

    X = -4+6/d (mod 8N).

Since -4<X<-3, X is not in the forbidden cap-boundary class A+e=4N+4 modulo 2e=8: N odd makes that class zero modulo 8, whereas this rational phase is nonintegral. Thus the seed satisfies exactly the preliminary guards that UP01/UP02 repair after their first selection.

But the right cap mouth requires

    X in (4N-4,4N+4) modulo 8N.

Our phase is in (8N-4,8N-3) modulo 8N, disjoint from that opening. Every real slope increment preserving both literal earlier residuals leaves this same phase. No weighted period, larger multiple, additional right flip, or target correction within this preserving subgroup repairs the cap passage from this seed.

## Physical and logical qualifications

The band expression before the failed cap exit describes genuine original mirrors only. At the descending h contact this seed returns through the left opening, so it does not enter the right arm as the claimed five-band route would require. The obstruction is the absence of the specified right-entry guard, not a fabricated illegal continuation or proof of darkness. We do not assert that these rooms are dark, that every target-compatible seed fails, or that no different mirror word works.

UP01 and UP02 retain their exact original hypotheses and are unaffected. The challenge is to arbitrary-depth extension by selecting a preliminarily good seed and then insisting that both literal earlier phases remain fixed. A positive arbitrary-depth proof must either select a seed already in a reachable cap coset, prove joint selection of the correct coset, allow controlled changes of both earlier residuals within their physical windows, or use a different itinerary. The two-event noncoverage proof alone does not provide that stronger joint condition.
