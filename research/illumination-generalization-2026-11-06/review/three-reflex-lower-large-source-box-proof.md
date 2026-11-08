# UB02: replacing the source/right width order by its exact covering bound

Use precisely candidate.md's room/endpoint hypotheses. Set d=alpha+beta+f,
A=Ne,a=Pe,R=Ke,B=Le,z=A-t,g1=h-c,d2=c-v,
Lambda=lcm(P,N,K),g=gcd(Lambda*d2,L)=gcd(Lambda,L).
The equality of g definitions uses odd d2 and power-of-two L.

Choose q=Pi+Nm+gj, tau=(A+z-s+2eq)/(2d), source/cap residuals
z0=s+2alpha*tau-2Pe*i and z1=z0+2beta*tau-(2m+1)A.
The two integer generators at m=0 are

    vi=(2eP/d)(-(beta+f),-f),
    vj=(2eg/d)(alpha,alpha+beta).

Their determinant -4e^2 P g beta/d is nonzero, and both components of vi
are strictly negative while both of vj are strictly positive. Writing the
offset as lambda*vi+mu*vj and rounding both coefficients half-up leaves
errors in [-1/2,1/2). As independently established in UB01, each coordinate
is STRICTLY between plus/minus its half absolute column sum. This yields

    |z0| < e*[P(beta+f)+g*alpha]/d <= Pe,
    |z1| < e*[P*f+g(alpha+beta)]/d <= Ke.

The first weak bound uses g<=P. The second is EQUIVALENT to
(P-K)f <= (K-g)(alpha+beta), the explicit new hypothesis. Hence both
physical passages are strict, including equality in the displayed metric
condition. P<=K was sufficient for this condition in UB01 but is no longer
needed anywhere in this covering argument.

For H0=gcd(Ng*alpha,Pg*beta,PN*f), positive integer increments
(di,dm,dj)=(Ng*alpha,Pg*beta,PN*f)/H0 have dq=PNg*d/H0 and
dtau=ePNg/H0. They preserve both residuals. Finite ceilings make i,m,q
nonnegative, and tau positive since A+z-s>0. The strict source residual
gives the actual i; strict cap residual<R<A gives the actual m.

The even-P valuation argument needs no P<K or P<L. Put k2=nu2(K)<log2 L.
Since g|K, if nu2(P)>k2 then nu2(g)=min(max(nu2(P),k2),log2 L)>k2,
contradicting that divisibility. Thus nu2(P)<=k2 and g=2^k2. Each of the
three defining H0 entries is divisible by 2^nu2(P), so nu2(H0)>=nu2(P).
The one-kernel-step right prephase/full-period ratio
g1PN/[2(K/g)H0] has negative 2-adic valuation and is nonintegral.
Thus an additional positive step repairs a right corner without changing
source/cap guards. Actual k is obtained by centering the safe right phase.

The exact bottom index is J=gj-Kk, divisible by g. The common final period
2eLambda*p preserves all three literal residuals with integral actual fold
increments and changes J by Lambda*d2*p. Since the divided coefficient is
a unit modulo L/g, a finite p gives E=z+2eJ=+z modulo2Le. The bottom fold
reaches actual t=A-z. This is one final direction, with no ray concatenation.

Physical guards use the original source left width a, cap width A, right
width R and bottom width B. The source travels upward from u>b to h;
cap upward to H and down to h; right down to c; bottom down to v. Positions
and signed velocities match through the centered fold identities, including
zero residual as a single smooth outer-wall reflection. Strict residuals
exclude every reflex corner and no artificial mirror is used.

A roof corner would equate the two h abscissae. They instead satisfy
ascending |z0|<a and descending A-|z1|>A-R=w>a, since N>P+L and K<L.
These inequalities hold even for P>K. Source x<=a<l<t prevents early T;
cap/right heights exceed v; bottom first reaches v at its endpoint. The
source never hits b, the bottom stops above0, and the roof is ordinary.
Every retained leg is in the actual room, with finite smooth specular
reflections and the original actual S,T.

For the whole native corollary P>K, integral e, even native u<h gives
alpha=(h-u)/2>=1. Every even native bottom v>0 has v>=2, so f<=(h-2)/2.
Since P-K>0 and K-g>=0, the candidate's whole-room threshold implies

    (P-K)f <= (P-K)(h-2)/2
             <= (K-g)(1+beta) <= (K-g)(alpha+beta).

Thus EVERY residual lower native pair satisfies the proved construction.
At/above h UJ01 uses gcd(lcm(N,K)*d2,L)=2^k2|K; it imposes no source
width order. TR01/TR05 protected placements and legal reversal cover the
complementary pairs, with exact cut equalities preserved. This proves all
native pairs in the stated larger-source family. Pure-power-two K=g with
P>K cannot satisfy the threshold; those metrics remain outside it.

No all-spiral/all-r3 conclusion follows. General even N and height parities,
other coordinate forms and r4..8 remain open. This is a sufficient optical
theorem with a precise new unbounded family, not a necessary illumination
criterion. No search or new clock is used; reciprocal review is pending.
