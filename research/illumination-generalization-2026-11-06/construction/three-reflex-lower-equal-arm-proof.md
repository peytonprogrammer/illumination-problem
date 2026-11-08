# LJ03: strict half-open source/cap covering for equal-width outer arms

Independent review pending. This strengthens LJ01_BOX and LJ02_DIVISIBILITY through a stricter choice of fundamental domain; those frozen sufficient theorems are preserved. It does not prove allr3/r<=8.

## 1. Quantifiers and the exact endpoint-compatible lattice

Original ordered spiral: positive integersP,N,L with1<=P<L,N>P+L,Nodd,Lpower2>=2; K=P. Take rational e>0, a=R=Pe,A=Ne,B=Le,l=A-B,w=A-R,integer0<b<c<h<H,h even,codd. Actual rationalhorizontalS=(s,u),T=(t,v) satisfy0<s<a,b<u<h,l<t<A,0<v<c andu,v are even integers. No condition is imposed on Pparity, capheight, their gcds, or horizontal endpoint residues.

Put alpha=(h-u)/2>0,beta=H-h>0,f=(h-v)/2>0,d=alpha+beta+f, g1=h-c odd,d2=c-v odd,z=A-t. These are positive integers except rationalhorizontalz. Choose integer i,m,j, initially unrestricted, and
 q=Pi+Nm+Pj,
 tau=(A+z-s+2eq)/(2d),
 z0=s+2alpha*tau-2Pe*i,
 z1=z0+2beta*tau-(2m+1)A.

At actual right indexk, z2=z1+g1tau-2Pe*k, giving complete targetidentity
 E=z2+d2tau=z+2eJ, J=q-Pi-Nm-Pk=P(j-k).

All indices must become actual, and all passages strict, before emitting a ray. The first source band is upward fromu toh; there is NO floor reflection.

## 2. One half-open fundamental domain lies STRICTLY inside both passage windows

Fixm=0. Let r0=(s+2alpha*tau0,s+2(alpha+beta)*tau0-A) at i=j=0. Changingi orj changes residualvector by
 vi=(2eP/d)(-(beta+f),-f),
 vj=(2eP/d)(alpha,alpha+beta).

Their determinant -4e^2*P^2*beta/d is nonzero. Expressr0 uniquely as lambda*vi+mu*vj. Define I=floor(lambda+1/2), J0=floor(mu+1/2), and choose i=-I,j=-J0,m0. Then
 (z0,z1)=a0*vi+b0*vj,
 a0=lambda-I, b0=mu-J0,
 with BOTH a0,b0 in[-1/2,1/2).

This half-open convention is essential: the excluded endpoint is+1/2 in BOTH coefficients. Every component ofvi is strictlynegative; every component ofvj is strictlypositive. For each componentr, therefore,
 -(|vi_r|+vj_r)/2 < a0*vi_r+b0*vj_r < (|vi_r|+vj_r)/2.

For the upper bound, -a0<=1/2 whileb0<1/2, so positivity ofvj makes it strict. For the lower bound, a0<1/2 whileb0>=-1/2, so negativity ofvi makes it strict. Both component absolute sums are exactly2Pe, sincealpha+beta+f=d. Hence
 |z0|<Pe, |z1|<Pe=R.

This proves simultaneous STRICT source/cap entry for EVERY nominated offset, even at simultaneous half-integer ties. There is no residual corner exception and no need to assume beta*s/e nonintegral. In the older closed centered domain, only two box vertices could be problematic; the chosen half-open domain excludes the problematic opposite-sign half endpoints directly. Nearest-point rounding here is an exact finite algebraic construction, not a search or density premise.

## 3. Positive physical indices and one right-corner repair

Set H0=gcd(Nalpha,Pbeta,Nf). The positive integral increments
 di=Nalpha/H0, dm=Pbeta/H0, dj=Nf/H0
have q incrementPNd/H0 and slope incrementDelta_tau=ePN/H0. Each is integral by definition. They annihilate BOTH literal residuals:
 2alpha*Delta_tau=2Pe*di,
 2beta*Delta_tau=2Ne*dm.

Choose finitely many such positive shifts to makei,m,q nonnegative (a maximum of their ceiling thresholds and0). Then tau>0 since A+z-s>0. Strict residuals identifyi as the actual source index andm as the actual odd-A cap-center index. No negative-time curve or independent covering sheet is retained.

The right prephase changes under one more such shift by g1ePN/H0. Dividing by the TRUE full right period2Pe gives
 g1N/(2H0),
which is not an integer becauseg1N is odd. Thus the current seed and its next nulltranslate cannot both hit the right-corner classR modulo2R. Pick a safe one, retainingboth earlier literalstrictguards and actual nonnegativeindices. Its centered actual rightresidual satisfies|z2|<R. No halfperiod or fixedreflectionbound is asserted.

## 4. Full original target correction for odd OR even armwidthfactorP

LetLambda=lcm(P,N), Gamma=gcd(Lambda*d2,L). SinceN,d2 areodd andLpower2, nu2(Lambda*d2)=nu2(P). BecauseP<L, nu2(P)<log2L, so
 Gamma=2^nu2(P), which DIVIDES P.

The selected seed hasJ=P(j-k), thusGamma dividesJ even whenP iseven. Increase the common slope by2eLambda*p. Actual source/cap/right indexincrements are
 2alpha*Lambda*p/P,
 2beta*Lambda*p/N,
 g1*Lambda*p/P,
all integers, preservingeveryliteralstrictresidual. J increasesbyLambda*d2*p. Bydefinition,Lambda*d2/Gamma is a unitmoduloL/Gamma. Choosefinitep in0..L/Gamma-1 satisfying
 J/Gamma+(Lambda*d2/Gamma)p=0 moduloL/Gamma.

The final bottomphaseE is+z modulo2Le. ThusF_Le(E)=z andactual endpointabscissa isA-z=t. One FINALslope defines the entire path; no changeofdirection between selected phases or target-sheet substitution occurs.

## 5. Original walls, roof, signed velocity and first target

The upward source band uses the true left walls x=0,a between actual u>b and h. Strict z0 gives a regular actual h entry, matching the position and signed velocity of the full cap chart F_A(z0+tau*wC). The cap rises to H and descends to h. The genuine right and bottom charts are A-F_R(z1+tau*wR) and A-F_B(z2+tau*wB). At zero residuals there is one ordinary smooth outer vertical reflection, not a corner or artificial mirror.

A singular roof at the FINAL slope would equate the ascending and descending h abscissae. The former is |z0|<a and the latter is A-|z1|>A-R=w>a, because N>P+L and P<L. This is a contradiction. Thus the only horizontal reflection is an ordinary actual roof contact. Every h/c reflex corner is excluded by strict source/cap/right guards. No synthetic wall above h is used.

The source band may cross the target height, but then x<=a<l<t, so actual T is not reached there. Cap and right heights exceed v. The final bottom descent first reaches v at its end. A positive finite slope and finite widths give finitely many ordinary original-wall reflections. Both actual endpoints are preserved and every open leg lies in the original room.

## 6. Whole native equal-arm family with arbitrary cap depth

Now take e any positive INTEGER, while P,N,L,b,c,h,H satisfy section1. Apply the accepted TR01/TR05 protected placement join to EVERY pair of distinct actual native even-even marks. Its exact residual is S in (0,a)x(b,H) against T in (l,A)x(0,c), up to reversal.

For u<h, LJ03 applies with no additional arithmetic. For u=h or u>h, accepted UJ01 applies with K=P,N odd,Lpower2: its target divisor is Gamma=2^nu2(P), which divides P=K exactly as proved above. Its actual mouth and upper-cap guards retain the SAME S,T. Every complementary placement is already covered by the original-wall-protected paths. Legal reversal exchanges labels.

Therefore EVERY distinct actual native pair illuminates in this ENTIRE equal-arm ordered-spiral family, with ANY integer P<L (odd or even), arbitrary source height, cap depth, size and reflection length, subject to the explicit N odd, h even/c odd, Lpower2 and normal-form geometry. No gcd involving cap height is needed. Both odd and even cap depths are included. This subsumes the BOX1/BOX2 native families and fills pure-power-two equal-arm cases outside the previous strict cover arguments.

General unequal arms, other N or height parity data, other normal forms, other reflex-gap words and r4..8 remain OPEN. This is not a universal22-wall minimum or completion of the full native goal.

## 7. Two prescribed exact controls

Use ONLY candidate.md's two fixed inputs. Control A has BOTH basis coefficients=-1/2 and tests consistent half-open ties explicitly; its cap depth18 shares factor9 with N9. Control B uses EVEN P=K2 with cap depth6 sharing factor3 with N9, testing the complete Gamma2 target residue. The checker validates actual source/target domains BEFORE any formulas. Exact controls corroborate; the quantified proof comes from sections1--6. No discovery, engine, census, fitting, new clock, worker, frozen edit or git mutation.
