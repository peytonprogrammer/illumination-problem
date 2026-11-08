# UB01: unequal source/right widths by target-compatible box covering

This proof uses exactly candidate.md's quantifiers. It is a partial optical
theorem pending independent reciprocal review, not full r3/r<=8 closure.

## 1. Compatible lattice and simultaneous strict guards

Let A=Ne,a=Pe,R=Ke,B=Le,z=A-t, alpha=(h-u)/2,beta=H-h,
f=(h-v)/2,d=alpha+beta+f,g1=h-c,d2=c-v. Positive alpha,beta,f,d
are integers and g1,d2 are odd. Set Lambda=lcm(P,N,K),
g=gcd(Lambda*d2,L). Since L is a power of two and d2 odd, this equals
candidate.md's g=gcd(Lambda,L). Hypotheses require g<=P and g|K.

Take unrestricted integer i,m,j and define

    q=Pi+Nm+gj,
    tau=(A+z-s+2eq)/(2d),
    z0=s+2alpha*tau-2Pe*i,
    z1=z0+2beta*tau-(2m+1)A.

At m=0 the two i,j generators are exactly vi,vj in candidate.md, by direct
expansion. Their determinant is -4e^2 P g beta/d, nonzero. For offset r0
at i=j=0, write r0=lambda*vi+mu*vj. Direct elimination gives

    lambda=-s/(2eP)-alpha*N/(2Pbeta),
    mu=z/(2eg)-f*N/(2gbeta).

Round BOTH with floor(x+1/2), negate to get i,j, and put m=0. Both errors
lie in [-1/2,1/2). Each component of vi is strictly negative, each of vj
strictly positive; its resulting absolute value is STRICTLY below half
their absolute sum, even at all simultaneous ties. Therefore

    |z0| < e*[P(beta+f)+g*alpha]/d <= Pe,
    |z1| < e*[P*f+g(alpha+beta)]/d <= Pe <= Ke.

The weak inequalities use g<=P and P<=K; alpha,beta,f>0 justifies strictness
in the half-open step. This is a covering proof for every target-compatible
offset, not a covolume or density argument.

## 2. Positive actual indices and the even-P right-return guard

Put H0=gcd(Ng*alpha,Pg*beta,PN*f). Its positive integer kernel increments are

    di=Ng*alpha/H0, dm=Pg*beta/H0, dj=PN*f/H0.

Substitution yields dq=PNg*d/H0 and dtau=ePNg/H0. Both literal residuals
are preserved because 2alpha*dtau=2Pe*di and 2beta*dtau=2Ne*dm.
The positive increments make i,m,q nonnegative after a finite maximum of
ceiling thresholds. Then tau>0 as A+z-s>0. Strict residuals give the actual
source index floor((s+2alpha*tau+a)/(2a))=i and cap index
floor((z0+2beta*tau)/(2A))=m; R<A follows from K<L<N.

Let p2=nu2(P),k2=nu2(K),ell=log2 L. Because K<L, k2<ell.
The explicit assumption g|K forces p2<=k2: otherwise
nu2(g)=min(max(p2,k2),ell)>k2. Hence g=2^k2 and nu2(g)>=p2.
All three entries Ng*alpha,Pg*beta,PN*f are divisible by 2^p2,
so nu2(H0)>=p2. The right prephase/full-period ratio for one kernel return is

    g1*dtau/(2Ke)=g1PN/[2(K/g)H0].

K/g is odd, and g1,N are odd. Its numerator has valuation p2 and denominator
valuation 1+nu2(H0)>p2. Thus the ratio is not an integer, including even P.
If the current prephase is the true-corner class R mod 2R, take one more
positive kernel step. It cannot remain in that class. Center the chosen
actual prephase, obtaining integer k and strict |z2|<R, where
z2=z1+g1*tau-2Ke*k. All earlier strict guards and physical indices persist.

## 3. Full actual target with the same slope

The exact final bottom phase is

    E=z2+d2*tau=z+2eJ, J=q-Pi-Nm-Kk=gj-Kk.

Both g|K and integrality of j,k are needed to conclude g|J. This does not
follow from g<=P; that distinction is retained explicitly. Increase the
common slope by 2eLambda*p. Source,cap,right actual index increments are
2alpha*Lambda*p/P,2beta*Lambda*p/N,g1*Lambda*p/K, all integers.
Thus z0,z1,z2 and their signed interface states stay literally identical.
J increases by Lambda*d2*p. By definition g=gcd(Lambda*d2,L), the divided
coefficient is invertible modulo L/g. Choose finite p in [0,L/g) solving
J/g+(Lambda*d2/g)p=0 modulo L/g (p=0 if L/g=1). Then E=+z mod 2Le,
F_B(E)=z and the final actual abscissa is A-z=t. No independently chosen
sheet or changing direction is introduced; this is one FINAL common slope.

## 4. Original finite walls, roof corner and first target

Use source chart F_a(s+tau*t), upward for duration 2alpha; cap chart
F_A(z0+tau*t), upward to H then downward to h for duration 2beta;
right A-F_R(z1+tau*t) down to c for g1; bottom A-F_B(z2+tau*t)
down to v for d2. At h the source ends at |z0| with signed derivative
sign(z0); this equals cap position/derivative. Cap ends at A-|z1| with
derivative -sign(z1), matching the right chart. The c seam likewise
matches the bottom chart in both position and velocity. Zero residuals
are ordinary reflections at a genuine outer vertical wall, counted once.

Source vertical contacts have b<y<=h and use x=0,a. Cap contacts above h
use x=0,A. Right contacts have c<=y<=h and use x=A-R,A. Bottom contacts
below c use x=A-B,A. Strict residuals exclude actual passage reflex corners;
all other true vertices can occur only at the floor/roof endpoints of these
bands. The source never touches b and the bottom stops at v>0.
A roof corner would identify the two h abscissae by reflection symmetry.
The ascending one is <a while the descending one is >A-R=w>a; impossible
by N>P+L and K<L. Thus the unique horizontal reflection is ordinary.

Before the cap the ray has x<=a<l<t, so it cannot hit T early, even at
target height. Cap/right heights exceed v. The bottom first attains v at
its last time. Every open segment lies inside the original polygon,
contacts satisfy the specular law and finite widths/slope/time give finitely
many reflections. It reaches the original actual T without a true corner.

## 5. Whole native family

For positive integral e, the protected TR01/TR05 constructions reduce all
other actual native pairs to terminal S in (0,a)x(b,H) against bottom T,
up to legal reversal. Lower u<h uses UB01. At u=h or u>h, apply UJ01:
its target divisor gcd(lcm(N,K)*d2,L)=2^k2 divides K. No P restriction or
cap-depth condition is needed there. This keeps the same actual S,T,
including native source on the artificial h cut. Thus EVERY distinct native
pair illuminates in candidate.md's full unequal-arm family.

It includes genuinely unequal P3,K6 and even P2,K6 at all vertical metrics
with h even,c odd,N odd,L power of two; no cap gcd is required. It excludes
P>K, g>P or g not dividing K, even N, other height parities and other
normal forms/turn types. Failure of this sufficient construction is not
darkness. All r3 and r<=8 remain open. No discovery effort or new clock is used.
