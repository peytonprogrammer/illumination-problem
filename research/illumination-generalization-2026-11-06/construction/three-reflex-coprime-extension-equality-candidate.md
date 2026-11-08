# CE05: strict cap windows at equality of orbit spacing

Predeclared hand candidate; CE03/CE04 frozen and unchanged.
Use CE04 ordered spiral geometry with e>0 rational, integers
2<=K<L, P<N-L and K dividing P. Integral strict heights and actual
terminal marks/ordinates are as in CE04. Put delta=gcd(P*C,N).
Replace CE04's delta<K condition by

    delta=K, gcd(lcm(P,N,K)*d2,L)=1.

Claim: actual S/T illuminate, with all original physical guards.
New ingredient: use the ACTUAL source/cap/right endpoint congruences
modulo2Pe and2Ke. Their three periods are all>=3, and the cap/right
periods cannot both equal3, so their densities sum to less than1.
This avoids a tie at the exact cap aperture and yields a strict return.
K|P and delta=K imply K|N; the removed source/cap periods therefore
preserve the genuine right/cap endpoint congruences. Without that
compatibility, the density argument is not justified.

Success: prove noncover, strict equality-case cap selection and the
original optical transfer. Strongest objection: source folding can alter
the endpoint residue; divisibility must be checked before counting.
No discovery search is proposed; hand proof and three prescribed
formula calibrations only. New files equality-{candidate.md,proof.md,
check.py,check.json,review-request.json} are owned by this author.

Whole native family: e integral,P=K=q,2<=q<L,N=q*M with M prime>L,
positive integral cap depth epsilon with2epsilon<M,ordered integer
0<b<c<h,H=h+epsilon. Either c4,Lodd,gcd(q,L)=1, or codd,Lpower2,qodd.
Both complete native families are claimed, using TR01/TR05 for all
other placements. Full spiral/r3/r<=8 remains open.
