# UJ01: a joint integer lattice supplies a physical cap entry AND target compatibility

Independent review pending. This is a positive unbounded-metric upper-source theorem, not a complete r3 or r<=8 result. UC01's K1 cap orbit is a special case; UJ01 changes the selection problem to include the cap index in the target congruence. No numerical experiment is used in the existence proof.

## 1. Quantifiers and optical chart

Use exactly candidate geometry and endpoint hypotheses. Put R=Ke,B=Le,A=Ne,z=A-t in(0,B),g1=h-c odd,d2=c-v odd. C=2H-h-u=2n>0,D=2H-u-v=2d, f=d-n=(h-v)/2>0. All n,d,f are positive integers and n<d. Set Lambda=lcm(N,K),g=gcd(Lambda*d2,L), and assume g|K. No assumption that g divides N or P is made.

The original cap chart is x=F_A(s+tau*w), rising from u to H and descending to h, duration C. At the right h exit require s+Ctau=(2m+1)A+z1 with |z1|<R. Then right chart x=A-F_R(z1+tau*wR), duration g1, exits with z1+g1tau=2Rk+z2, |z2|<R. Bottom chart x=A-F_B(z2+tau*wB), duration d2, ends at height v. Triangular folds agree in position AND signed derivative at both portals, including z1=0 or z2=0 as genuine smooth outer-wall reflections. Only real polygon walls are reflected.

## 2. A two-variable lattice gives a strict cap entry in the required target class

Restrict the full-target root grid to
 q=Nm+gj,  tau=(A+z-s+2eq)/(2d), with integers j,m initially unrestricted.

Then, by direct expansion,
 z1=s+2n*tau-(2m+1)A
   =[V+2e(ngj-Nfm)]/d,
 V=f(s-A)+nz.

Put H0=gcd(ng,Nf)>0. The attainable integer values ngj-Nfm are exactly H0 times the integers by Bezout. Choose integer ell nearest -V/(2eH0). Thus |V+2eH0ell|<=eH0. Since H0<=ng and n<d,
 |z1|<=eH0/d<eg<=eK=R.

This gives strictness even if the nearest-integer choice ties. Choose any integer Bezout solution (j0,m0) to ngj0-Nfm0=H0ell. This is existence of a finite integer solution, not a density/recurrence assertion. It works with rational horizontal positions and arbitrary rational e.

## 3. Make the selected cap center physical and avoid the true right corner

All solutions along the following positive homogeneous shift have the SAME literal z1:
 m -> m+(ng/H0)t,
 j -> j+(Nf/H0)t,
 q -> q+(Ngd/H0)t.

Each displayed increment is a positive integer. For q this follows from Ngd/H0=N*(ng/H0)+g*(Nf/H0). Thus choose a finite integer t>=0 large enough that m>=0 and q>=0. Explicitly max(0,ceil(-m0/(ng/H0)),ceil(-q0/(Ngd/H0))) suffices. Then tau>0 because A+z-s>0. The cap index is now an actual nonnegative unfolding index and its literal residual remains strict. No negative-time ray or fictitious cap center remains.

One additional homogeneous shift increases slope by Delta_tau=eNg/H0 and preserves z1. Its change in the right prephase divided by the actual full right period2Ke is
 g1*Delta_tau/(2Ke)=g1*N/[2(K/g)H0].

The numerator is odd; the denominator is even. Hence this is NOT an integer. If the current right prephase is the true corner class R modulo2R, the next one is not. Otherwise retain the current one. Select one of these two physical solutions; its centered right residual |z2|<R is strict. The test occurs before any trajectory is emitted. No claim that the increment is a half-period, nor a bounded reflection count, is used.

## 4. Match the full actual target without losing either strict passage

For the selected q,m and right fold index k,
 E=z2+d2tau=s+Dtau-(2m+1)A-2Kek
  =z+2eJ,
 J=q-Nm-Kk=gj-Kk.

Therefore J is an INTEGER divisible by g. This uses the actual cap m and actual right k; no projection target is substituted.

Increase tau by 2eLambda*p. The cap index increases by C*Lambda*p/N and the right index by g1*Lambda*p/K, both integers. Thus literal z1,z2 remain unchanged. E increases by2eLambda*d2*p, so J increases byLambda*d2*p. By the DEFINITION g=gcd(Lambda*d2,L), the coefficient Lambda*d2/g is invertible moduloL/g. Choose the finite p in0..L/g-1 solving
 J/g+(Lambda*d2/g)p=0 moduloL/g,
with p0 for modulus1.

The final E equals +z modulo2Le. Consequently F_B(E)=z and actual last abscissa is A-z=t. All stages are choices of ONE FINAL slope; different directions are never concatenated.

## 5. Complete original physical guards and roof repair

The cap section above h has full actual width A, regardless of P. The descending right section between c and h has exact width R, and the bottom below c has exact width B. Strict |z1|,|z2|<R excludes the actual h/c reflex corners. Each triangular fold uses its true vertical walls; no source-arm boundary is reflected above h. A zero residual denotes a smooth outer wall, not a vertex.

At the FINAL slope inspect s+(H-u)tau. If it is not a multiple of A, the sole roof reflection is ordinary. If it is a multiple of A and u>h, exact fold symmetry returns to original S at elapsed2(H-u), with descending vertical velocity and the exact signed horizontal velocity of the remaining curve. Since u>h this time is strictly before the cap exit C. Delete the whole formal prefix, including the singular roof hit, and emit ONLY the regular suffix from actual S. No corner is traversed.

At u=h the source is required to have0<s<a<w. A formal roof corner would imply F_A(s+Ctau)=s at the h return, while the strict right exit has F_A(s+Ctau)>w. This is impossible. Thus the mouth case has an ordinary roof, with no limit argument.

All retained cap/right portions have height>v. On the final descent through the bottom, y=v occurs only at the last time. Thus the reached point is first actual T. Positive finite widths and one finite slope give a finite number of smooth specular reflections; all open segments lie in the original room. These are the same physical charts independently accepted in UC01/CE08, with R substituted explicitly and no additional optical premise.

## 6. Whole native cap-only family, now including every right width

Take positive integral e, N odd, L=2^a>=2, ANY positive integers P,K with1<=K<L,N>P+L. Let b be positive even,c=b+1,h=b+2 and H any integer>h. The polygon retains all ten positive walls and the original strict metric order.

For every native terminal source in0<s<Pe,b<u<H, even u implies u>=h. For every native bottom target, even v and odd c imply d2 odd. Since N is odd, Lambda=lcm(N,K) has the same 2-adic valuation as K. Consequently
 g=gcd(Lambda*d2,L)=gcd(K,L),
which divides K. All UJ01 hypotheses hold, including u=h left-mouth marks. There is NO restriction on cap depth H-h, source width parity, upper depth, or the odd part of K. The accepted TR01/TR05 protected placement arguments and legal reversal cover every complementary pair in the SAME original room. Thus EVERY distinct actual native pair illuminates in this whole family.

The old CE08 cap-only corollary excluded K a pure power of two; this fills precisely those width classes and also gives the explicit general target-divisor sufficient condition. CE08/LC03 remain valid at their accepted scopes. General lower-source classes, even N, other height parities, arbitrary width ratios/spiral forms, seven other turn types and r4..8 remain OPEN. This theorem neither proves a 22-wall minimum nor supplies a dark counterexample.

## 7. Prescribed exact controls

Use exactly the four controls declared in candidate.md. They test pure-power-two widthsK2/K4, actual mouth equality u=h, and a non-power-two bottom L6 with target divisor g3 and nonzero final correction. Formula checks will be exact; independent physical replay belongs to the existing reviewer. No discovery, census, fitting, new engine, worker, clock or git mutation.
