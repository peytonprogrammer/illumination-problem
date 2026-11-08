# LJ04: a target-residue transport that preserves the source and cap windows

Independent review pending. This concerns P1 with potentially wider right arm K; it is distinct from the peer's unequal-box theorem requiring Gamma<=P. General r3/r<=8 remains open.

## 1. Precise lower-pair hypotheses and strict initial joint covering

Use exactly candidate.md's original ordered spiral, actual endpoint guards and parities. Let alpha=(h-u)/2>0,beta=H-h>0,f=(h-v)/2>0,d=alpha+beta+f, z=A-t,g1=h-c odd,d2=c-v odd. Suppose f is odd; alpha,beta are arbitrary positive integers.

Use q=i+Nm+j and tau=(A+z-s+2eq)/(2d). Define source residualz0=s+2alpha*tau-2ei and cap residualz1=z0+2beta*tau-(2m+1)A. The actual right residual after centering with period2Ke is z2=z1+g1tau-2Kek, giving
 E=z2+d2tau=z+2eJ, J=j-Kk.

Temporarily IGNORE the target congruence moduloL; the exact original target root remains retained in this identity. At fixedm0 the two integer residual generators are precisely LJ03's P1 basis
 vi=(2e/d)(-(beta+f),-f), vj=(2e/d)(alpha,alpha+beta).

Their signs, determinant and half-open rounding proof do not refer to the physical right width. Thus they yield simultaneously |z0|<e and |z1|<e<=Ke. No source residue assumption or capgcd is used. This is an actual strict source/cap candidate; it is not yet a complete target match.

## 2. Positive nullreturns enforce the missing target residue

Put M=gcd(Nalpha,beta,Nf). Since N and f are odd, M is odd. The positive integral nullincrements
 di=Nalpha/M, dm=beta/M, dj=Nf/M, dq=Nd/M
preserve BOTH literal source/cap residuals and increase slope by eN/M. They are exactly the P1 joint-box kernel, independent of K. Take finitely many to make i,m,q nonnegative and tau>0, identifying actual source/cap indices. The integer dj is ODD.

Set Lambda=lcm(N,K) and Gamma=gcd(Lambda*d2,L). Since N,d2 are odd and Lpower2 with K<L,
 Gamma=2^nu2(K), which divides K.

Because dj is odd, it is invertible modulo Gamma. Choose a finite ell in0..Gamma-1 with j+dj*ell=0modGamma, and perform that many additional nullsteps. Indices and slope stay nonnegative/positive. Both earlier literal guards remain unchanged. Now the ACTUAL right-centering index k gives J=j-Kk divisible by Gamma, irrespective of k.

The current candidate may hit the true right-corner class R modulo2R. Compare it to a further BLOCK of Gamma nullsteps. That block preserves jmodGamma and both source/cap residuals. Its right-prephase change divided by2Ke is
 g1*(eN/M)*Gamma/(2Ke)=g1N/[2(K/Gamma)M].

Here K/Gamma is an integer and g1N is odd; the denominator is an even integer. The ratio is not integral. Thus the two candidates cannot both lie in the corner class. Choose the safe one and recenter its actual right phase. We now have strict |z0|<e,|z1|<Ke,|z2|<Ke AND integerJ divisible byGamma, with actual nonnegative folds.

No different slopes are concatenated: these are algebraic choices made before the final ray is emitted.

## 3. Full actual target and original optical guards

Increase the one common slope by2eLambda*p. Source/cap/right index increments are2alpha*Lambda*p,2beta*Lambda*p/N,g1*Lambda*p/K, all integers. Every literal residual remains identical. The target index increases byLambda*d2*p. Definition ofGamma makes Lambda*d2/Gamma a unit moduloL/Gamma, so choose finite0<=p<L/Gamma making J+Lambda*d2*p divisible by L.

The final phase E equals+z modulo2Le and the bottom fold reaches exactly actualt=A-z. The source is genuinely upward in its left band of width e; there is no floor hit. Its ascending h abscissa is |z0|<e. The actual descending right-mouth abscissa is A-|z1|>w>e. Therefore a final singular roof is impossible by the usual exact folding symmetry, which would equate those abscissae. It is an ordinary true roof reflection.

Only the genuine left walls below h, full outer cap walls above h, right walls of width Ke, and bottom walls of width Le are used. Strict residuals exclude all actual reflex corners; zero residuals are single ordinary smooth outer-wall reflections. Positions and signed velocities match at every physical passage. Before h, x<=e<l<t excludes actualT even at its height. Cap/right heights exceedv; the final bottom descent first reachesv at its end. Finite positive slope and finite widths give a legal finite actual S-to-T specular trajectory.

## 4. Whole native family with arbitrary right width and many lower levels

Take e any positive INTEGER,Nodd,Lpower2>=2,ANY1<=K<L,N>1+L,P1. Let b be1or2,c3,h=4m for ANY positive integerm, and H ANY integer>h. These are strict ordered original ten-wall rooms. Every native bottom mark has v2, so f=(h-v)/2=2m-1 is odd. Every native residual left source withu<h satisfies the lower lemma, whatever its actual even height and whatever cap depth beta.

At u=h oru>h, accepted UJ01 applies because its target divisor Gamma=2^nu2(K) dividesK. The exact protectedTR01/TR05 placement join and reversal cover every complementary pair. Thus EVERY distinct actual native pair illuminates throughout this whole family, with unbounded h, widths, cap depth and reflection count and NO gcd conditions involving cap depth. Even right width K2 with P1<Gamma is included and is outside the peer's new Gamma<=P box scope.

General f even, unequal source widthsP>1, even N, other parities/normal forms/turn types andr4..8 remain open. The sufficient fodd hypothesis is not asserted necessary for illumination. This is another partial optical theorem, not completion of the native goal.

## 5. Prescribed check

The sole declared input has alpha1,beta6,f3,d10,Gamma2,M3. It explicitly needs the target-residue transport: the initial rounded j1 is ODD and not target-compatible modulo2. One nullstep has dj9 and changes slope by12, producing j10 and actual final root151/10. Its actual right index5 givesJ0 and exactT24,2; source/cap guards stay1/5,7/5. The checker validates actual input domains first. No discovery, engine, census, fitting, newclock, worker or git-state mutation.
