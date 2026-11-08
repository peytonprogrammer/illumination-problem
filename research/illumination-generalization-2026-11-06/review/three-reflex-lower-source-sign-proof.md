# LS01: both actual source directions remove the lower cap-parity restriction

Independent reciprocal review pending. Retain the ordered equal-arm family a=Pe,R=Pe,A=Ne,B=Le,l=A-B,w=A-a with positive integers P<L, L a power of two, N>P+L, and nu2(N)=nu2(P)+1. Let e>0 be rational; let integer heights satisfy 0<b<c<h<H, h even and c odd. Actual rational-horizontal terminal marks S=(s,u),T=(t,v) satisfy 0<s<a,b<u<h,l<t<A,0<v<c, with even integer u,v. Claim: every such LOWER terminal pair illuminates for ANY positive integral cap depth beta=H-h, including odd beta. There is no bound on metrics, reflection count or horizontal residues. Mouth and upper sources require separate accepted theorems.

## Two strict source/cap seeds from the original source

Put alpha=(h-u)/2>0,f=(h-v)/2>0,d=alpha+beta+f,g1=h-c,d2=c-v. All are positive integers, with g1,d2 odd and 2f=g1+d2. For sigma in {+1,-1}, use the actual source fold F_a(sigma*s+tau*w). At w=0 this is the SAME actual x=s and its initial horizontal velocity has sign sigma. Both have upward vertical velocity. Only true left-strip walls are used before h.

For each sign set m=0 and use the exact half-open construction with

    lambda_sigma=-sigma*s/(2a)-alpha*N/(2P*beta),
    mu=z/(2a)-f*N/(2P*beta), z=A-t,
    i_sigma=-floor(lambda_sigma+1/2), j=-floor(mu+1/2),
    q_sigma=P*i_sigma+P*j,
    tau_sigma=(A+z-sigma*s+2e*q_sigma)/(2d).

The same j works for both signs. The accepted half-open source/cap basis has both negative first-column components and positive second-column components. Thus its component sums force BOTH literal residuals strictly inside (-a,a), including half-integer ties. This argument is independent of the sign of the source phase, N parity and beta parity. The residuals are

    z0_sigma=sigma*s+2alpha*tau_sigma-2a*i_sigma,
    z1_sigma=z0_sigma+2beta*tau_sigma-A,
    r_sigma=z1_sigma+g1*tau_sigma.

These preliminary algebraic roots may have negative indices/time; actual positive representatives are selected below before any ray is emitted.

## Exact two-sign separation of the right-corner phase

Because lambda_plus=lambda_minus-s/a and 0<s/a<1, common floor rounding gives

    Delta_i=i_plus-i_minus in {0,1}.

Direct subtraction gives

    tau_plus-tau_minus=(-s+a*Delta_i)/d,
    z1_plus-z1_minus=(2f/d)*(s-a*Delta_i),
    r_plus-r_minus=(d2/d)*(s-a*Delta_i).

The last difference is NONZERO because 0<s<a. Moreover its absolute value is strictly smaller than a*d2/d<2a, since d2<2f<2d. Two genuine right-corner phases are both a modulo 2a and therefore differ by an integer multiple of 2a. Our difference is nonzero with absolute value less than 2a, so the two seeds cannot both be corner-bad. At least one has all three strict guards.

This is a finite exact two-choice argument for every offset, not density or a claim that an arbitrary old right phase can be repaired.

## Restore physical positivity and retain the safe choice

Let H0=gcd(Nalpha,Pbeta,Nf). The positive integral null increments are

    (di,dm,dj)=(Nalpha,Pbeta,Nf)/H0,
    dq=PNd/H0, Delta_tau=ePN/H0.

They preserve BOTH literal source/cap residuals. If the right phase ratio g1N/(2H0) is an integer, positive null shifts preserve the right phase modulo the genuine full period. Choose the safe source sign above and take a finite nonnegative number of nulls to make i,m,q nonnegative. Since A+z-sigma*s>0, tau is then positive. The actual centered right k is automatically nonnegative since r=z1+g1*tau>-a. Thus the safe phase remains strict and physical.

If the ratio is nonintegral, choose either source sign, restore positivity, then if necessary take one additional null to repair a true right corner. The preceding strict source/cap guards remain unchanged. In both branches there is a physical strict three-guard seed.

## Odd block transport works for ODD beta as well

Write p=nu2(P), so nu2(N)=p+1. Every term in H0 is divisible by 2^p, even if beta is odd. Therefore nu2(H0)>=p. Set D0=gcd(g1N,2H0),B0=2H0/D0. Since g1 is odd,

    nu2(D0)=min(p+1,1+nu2(H0))=p+1.

A block of B0 positive nulls preserves all three literal signed residuals, with actual increments delta_j=2Nf/D0 and delta_k=g1N/D0. Their difference is the positive odd integer delta_M=N*d2/D0. It is integral because D0 divides both 2Nf and g1N. No assumption D0|N is made.

For either source sign the exact target identity is E=z+2eJ,J=P(j-k); sigma*s cancels from the root equation. The target divisor is Gamma=gcd(lcm(P,N)*d2,L)=2^min(p+1,log2(L)), and rho=Gamma/2^p=2. Odd delta_M permits a finite nonnegative block count giving J divisible by Gamma. The usual common period 2e*lcm(P,N) then changes J by lcm(P,N)*d2. Its quotient by Gamma is a unit modulo L/Gamma, so a finite nonnegative correction makes J divisible by L. E_final=z modulo TRUE period 2Le, reaching the original actual T. Every selection specifies one FINAL signed slope.

## All actual optical guards

Negative source phase is the original S with negative initial vx, not another physical point. During the upward source stage, its true strip folds stay in 0<=x<=a with y>b. At h strict z0 gives matching F_A(z0) position and horizontal derivative in the genuine full cap. Strict z1 and z2 match the right and bottom charts with the same signed velocity. Zero residuals are ordinary smooth outer-wall contacts. No fake portal mirror is inserted.

A true roof corner at the final slope would equate the ascending and descending h abscissae. The former is strictly less than a and the latter strictly greater than w>a, a contradiction. Thus the lower one-roof path is ordinary for either initial horizontal sign. All h/c true corners are excluded by strict guards. Source-stage x<=a<l<t excludes an early T; cap/right heights exceed v; the bottom first reaches v at its last point. Finite widths, slope and developed time give finitely many ordinary true-wall reflections. This proves actual illumination under the stated lower-pair quantifiers.

## Whole-family consequence, conditional only on independent acceptance

Accepted EA07, reciprocally accepted UE01 and independently accepted SS01 jointly cover ALL upper/mouth terminal sources at this same one-step valuation gap, with no restriction on beta. If LS01 is independently accepted, TR01/TR05 protected placement and reversal therefore yield EVERY distinct actual native even-even pair in the entire ordered equal-arm family for ANY positive cap depth beta. This removes the even-beta condition from the prior whole family. General larger opposite valuation gaps, unequal arms, different height parities, other shapes, all r3 and r4..8 remain open.

## Prescribed exact evidence

Own checker three-reflex-lower-source-sign-check.py has two fixed lower inputs with e4,P1,N6,L4,b1,c3,h6,S=(2,4),T=(12,2). At beta1, Delta_i=0 and the selected negative initial branch reaches T at signed slope -47/4. At beta5, Delta_i=1 and the selected negative branch reaches T at signed slope -595/8 after nonzero block and full-period corrections. Both cap depths are ODD and outside EA06's sufficient beta divisibility. Exact first-wall replays check all actual mirrors, all corners and first-target arrival. A third row separately validates SS01's upper negative-source branch; it is not another LS01 lower sample. No author code, search, new clock, census, engine, fitting, worker, frozen edit or git mutation was used.
