# LJ01: simultaneous lower-source and cap entry by a fundamental parallelogram

Independent review pending. This supplies a different joint existence argument for lower sources; it does not simply repeat the earlier source-preserving cap period. The native r3/r<=8 objective remains unfinished.

## 1. Quantifiers, actual geometry and target root

Use candidate.md's original ordered spiral with P=K1, Nodd,N>1+L,Lpower2>=2,e=2^E>=4,integer0<b<c<h<H,h even,c odd,beta=H-h odd. Put A=Ne,R=e,B=Le,l=A-B,w=A-e. The source is actual nativeS=(s,u),0<s<e,b<u<h, and actual nativebottomT=(t,v),l<t<A,0<v<c. In particular s is a positive even integer strictly below e, so s/e is a proper nonintegral dyadic rational. The horizontal target may have ANY native coordinate in the bottom, including z/e integer.

Write alpha=(h-u)/2>0,f=(h-v)/2>0,d=alpha+beta+f, g1=h-c odd,d2=c-v odd,z=A-t. All alpha,beta,f,d are positive integers. We use an initially upward left-arm / one-outer-roof / right / bottom itinerary; there is NO left-floor reflection. The source band lasts2alpha, cap2beta, rightg1,bottomd2, with total duration2d.

For integers i,m,j initially unrestricted set
 q=i+Nm+j,
 tau=(A+z-s+2eq)/(2d).

The intended actual source and cap residuals are
 z0=s+2alpha*tau-2ei,
 z1=z0+2beta*tau-(2m+1)A.

The target identity after actual right centering z2=z1+g1tau-2ek is
 E=z2+d2tau=z+2eJ, J=q-i-Nm-k=j-k.
Thus every such integer choice remains on the exact complete target root grid. Guard selection must precede the final modular target correction.

## 2. Cover BOTH source and cap windows simultaneously

At i=m=j=0 let tau0=(A+z-s)/(2d) and r0=(s+2alpha*tau0,s+2(alpha+beta)*tau0-A). Varying i,j at fixed m0 changes the residual vector by
 vi=(2e/d)(-(beta+f),-f),
 vj=(2e/d)(alpha,alpha+beta).

Their determinant is -4e^2*beta/d, which is nonzero. Express r0 uniquely as lambda*vi+mu*vj. Choose nearest integers I,J to lambda,mu, with ANY fixed tie convention. Set i=-I,j=-J,m=0. The resulting residual pair is
 r=(lambda-I)*vi+(mu-J)*vj,
with both coefficients in[-1/2,1/2]. Every component satisfies the closed bound e, because
 (e/d)((beta+f)+alpha)=e,
 (e/d)(f+(alpha+beta))=e.

Both components of vi are strictly negative and both of vj strictly positive. Therefore equality in EITHER component's bound requires the coefficients be exactly(-1/2,+1/2) or(+1/2,-1/2); those give respectively r=(e,e) or(-e,-e). Every other point of this fundamental parallelogram has BOTH residuals strictly inside(-e,e). There are no edge segments on the boundary of the box: only these two vertices. A closed covering argument alone is not enough; the next section excludes them at the actual native marks.

## 3. Native dyadic source and odd cap height exclude the two boundary vertices

Suppose z0=z1=epsilon*e with epsilon=+1 or-1. From the exact cap relation,
 2beta*tau=(2m+1)A,
so tau/e=(2m+1)N/(2beta).

The source relation then forces
 beta*s/e + alpha*(2m+1)N = (2i+epsilon)*beta.

The second term and right side are integers. Hence beta*s/e would be integral. This is impossible: s/e is a nonintegral dyadic rational and beta is odd, so multiplication by beta cannot remove its power-of-two denominator. Thus the chosen residual pair cannot be either box-boundary vertex. We have proved simultaneous strict |z0|<e and |z1|<e for a nominated target-compatible grid point.

No counting of sampled phases or numerical density is used. The argument applies to EVERY admissible alpha,f,odd beta and EVERY native source abscissa in this width, regardless of gcd(beta,N). It is not asserted when beta is even or s/e has odd denominator.

## 4. Turn the rounded algebra into physical nonnegative fold indices

Rounding may produce negative i,j,q. Put
 M=gcd(alpha*N,beta,N*f),
 di=alpha*N/M, dm=beta/M, dj=N*f/M.

All are positive integers. A simultaneous increment(i,m,j)->(i+di,m+dm,j+dj) increases q by N*d/M, a positive integer since di+Ndm+dj=Nd/M. Hence it increases tau by eN/M. Both residuals remain IDENTICAL:
 2alpha*(eN/M)-2e*di=0,
 2beta*(eN/M)-2A*dm=0.

Choose a finite nonnegative number of these steps so that i,m,q are all nonnegative; the maximum of the three corresponding ceiling thresholds suffices. The source/cap residuals stay strict. Then tau>0 because A+z-s>0. Since |z0|<e, i is the actual source fold index of its positive phase; since |z1|<e<A, m is the actual cap index. No negative-time ray or algebraic sheet is retained.

The right prephase changes under one additional null step by g1eN/M. Its ratio to the actual full right period2e is g1N/(2M), a noninteger because g1N is odd. Therefore the current seed and its next null translate cannot BOTH be in the true right-corner class e modulo2e. Select a safe one and center its actual right phase; then |z2|<e. This one extra step preserves source and cap strictness, actual nonnegative indices and the integer target root.

## 5. Full actual target and all optical guards

The selected right indexk gives integerJ=j-k. Increase the common slope by2eN*p. Its actual source/cap/right index increments are2alpha*N*p,2beta*p,g1*N*p. Every literal residualz0,z1,z2 remains identical. The target index changes byN*d2*p. Since N,d2 are odd and Lpower2, choose finite0<=p<L with
 J+N*d2*p=0 moduloL.

The final phaseE equals+z modulo2Le, so the genuine bottom fold F_Le(E)=z and actual endpoint abscissa A-z=t. This is the original actual target with ONE final common slope throughout.

The original source chart F_e(s+tau*w0) rises from u to h, using only the genuine left wallsx0,e. Since u>b it never reaches the left floor or its corners. At h strictz0 gives the exact regular left mouth, and its signed derivative matches the cap chart F_A(z0+tau*wC). The cap uses the genuine outer walls and one actual roof atH, then descends to the regular right mouth given by strictz1. The right and bottom charts A-F_e(z1+tau*wR) andA-F_Le(z2+tau*wB) match exact position and signed velocity, with zero residuals denoting ordinary smooth outer-wall reflections.

A singular roof at the FINAL slope is impossible: symmetry would identify its ascending and descending h abscissae. The ascending one is |z0|<e, while the descending one is A-|z1|>A-e>e by the room's strict width order. Thus the sole roof contact is ordinary. Every h/c reflex corner is excluded by the strict source/cap/right guards; every retained open segment lies in the actual polygon. No artificial seam is reflected.

Before h, even if the ray crosses the target's height, x<=e<l<t, so it cannot reach actual T. Cap and right heights exceedv. The last bottom descent reachesv only at the final time. This proves first actual target, finite length and finitely many ordinary original-wall contacts. No uniform reflection bound is asserted.

## 6. Whole native room family without cap coprimality

Retain the entire room family from section1 with odd beta, but consider EVERY pair of distinct native interior marks. The independently accepted TR01/TR05 protected placement join leaves only actualS in(0,e)x(b,H) and bottomT in(l,A)x(0,c), up to reversal. If u<h, apply LJ01. If u=h or u>h, apply accepted UJ01 with K1,Nodd,Lpower2, for which g1targetdivisor=gcd(N*d2,L)=1. That upper/mouth theorem imposes no source height, cap-depth gcd or P parity condition. The same actual pair is retained in each branch, and the accepted complementary protected paths/reversal finish the join.

Therefore every distinct native pair illuminates in this whole unbounded family with e a power of two>=4, P=K1, Nodd,Lpower2, arbitrary ordered b<c<h with h even/codd, and ANY odd cap depth beta. In particular beta may share arbitrary odd factors with N. This removes the accepted FR02 whole-family condition gcd(beta,N)=1 at this explicit geometry/parity family. The earlier half-odd-target theorem is not used: all native targets are included.

GeneralP/K,e,evenbeta,other height parities/evenN,other spiral normal forms,other turn types andr4..8 remain OPEN. This is not completion of the full goal and does not prove a universal22-wall lower bound.

## 7. One prescribed exact calibration

Use candidate.md's single source/room/target, with beta3,N9 and z/e3. It lies outside FR02's coprime cap condition and LC04's half-odd target criterion. The stated coefficient rounding, seed and final slope will be checked exactly, with source/target interior-domain assertions BEFORE arithmetic. Independent actual-wall verification belongs to the existing peer. No discovery effort, new clock, engine, census, fitting, worker, frozen edit or git mutation is used.
