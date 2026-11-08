# AP01 independent review — ACCEPT the stated parity-free weighted-box and whole-family theorems

All seven requested claims are ACCEPTED, without correction to the author packet. This proves the stated actual lower-pair weighted-box theorem and upper companion for arbitrary INTEGER heights. It also proves the whole native P<=K family under the full per-target divisor conditions, including the explicit unequal-arm/even-N/odd-h family. It does not remove all arithmetic or metric hypotheses, prove all r3 rooms, or finish r<=8.

## Integer times and strict source/cap covering

I independently expand the root with raw integer times A0=h-u,C0=2(H-h),F0=h-v,D=A0+C0+F0. The source/cap offset is exactly [((C0+F0)*sigma*s+A0*(A+z))/D, (F0*(sigma*s-A)+(A0+C0)*z)/D]. Multiplying the displayed integer-index basis by lambda_sigma=-sigma*s/(2eP)-A0*N/(2P*C0) and mu=z/(2eg)-F0*N/(2g*C0) reproduces this offset. Its determinant is -4e^2*P*g*C0/D, nonzero. No half-integer gcd or lost factor of two is used.

The negative/positive basis columns and the SAME half-open rounding yield strict bounds in BOTH coordinates, even at ties. The source bound follows from g<=P, and the cap bound from PF0+g(A0+C0)<=KD. Both weak equalities are permitted because the preceding half-open inequalities are strict.

## Two actual source directions and physical positivity

Only lambda changes between +s and -s, by -s/a. Therefore j is the SAME and Delta_i belongs to {0,1}. Direct subtraction gives Delta_r=2d2*(s-a*Delta_i)/D, which is nonzero. The weighted metric bound gives PF0<KD because g(A0+C0)>0; d2<F0. Hence abs(Delta_r)<2R. Both phases cannot be the true right-corner class R modulo 2R. This establishes existence of a simultaneous strict source/cap/right seed at every offset with no parity premise.

The author's Hlow kernel has exact positive integer increments, with q change PNgD/Hlow and slope change 2ePNg/Hlow. Its full-period/non-full-period cases correctly distinguish preservation from repair. Independently, g|K|Lambda allows an even simpler positivity kernel: increase slope by 2eLambda, with increments i=A0Lambda/P,m=C0Lambda/N,j=F0Lambda/g,q=D*Lambda,k=g1Lambda/K. These are positive integers, preserve ALL literal signed residuals, and retain the complete root grid. This alternative is used in my checker after selecting a safe seed. It supplies an independent positivity argument rather than relying on the author's implementation.

## Upper lattice and the exact proper-divisor condition

In units e/D, vm=(-2NF,-2Nd2),vj=(2Cg,2g(C+g1)) and determinant -4Ng*g1*D are correct. With Hup=gcd(NF,Cg), Bezout yields a column step 2Hup. The primitive zero-x integer kernel (Cg/Hup,NF/Hup) gives EXACT vertical fiber 2Ng*g1*D/Hup. This proves actual integer preimages and the full lattice, not a covolume proxy.

If 2Hup<KD, two adjacent strict cap columns exist. A non-full-period fiber can repair a corner. A full-period fiber cannot hide both columns: their common bad phase would force their y-projection gcd divisible by 2KD, but that positive gcd is at most 2g(C+g1)<2KD. Positivity retains the chosen physical class.

When g<K, the integer divisibility g|K is essential: it gives 2g<=K, hence 2Hup<=2Cg<=CK<KD. The mere real inequality g<K would not suffice. The author explicitly uses the correct divisor implication.

In the remaining permitted branch g=K=P and 2Hup>=KD, CP/Hup is a positive integer below two; it equals one. Thus Hup=CP,C>=F. Both original source images have nearest strict cap residuals of size at most Ca/(C+F)<a. Their nearest j values differ by 0 or -1 because Fs/(Ca) is strictly between zero and one, including C=F. For B0=2(C+g1)/D, 1<B0<2 and 2d2/D=2-B0. The right-phase difference is in (0,1) or (-2,0) in units a, so cannot be an even integer. The paired-source proof therefore covers equality as well as the critical branch even when C,F are ODD. This raw-time argument is stronger than silently applying an integer-n theorem to n=C/2.

## Complete target and all original optics

For actual centered k, E=z+2e(gj-Kk). Its J is already g-divisible because g|K. At a common full-period shift, all raw-time fold increments are integral and every signed residual stays unchanged. J changes by Lambda*d2, whose quotient by g is a unit modulo L/g by the FULL definition of g. A finite nonnegative correction yields E=z modulo the TRUE period 2Le and the original actual T. No missing-bit repair, parity shorthand, independent target sheet or direction concatenation is used.

The source image -s is the same actual S with negative initial horizontal velocity. All lower left-strip, full cap, right-strip and bottom mirrors are genuine original finite walls under the ordered geometry. Strict portal residuals exclude true h/c corners and zeros are ordinary outer-wall contacts. Disjoint source/right h abscissae exclude lower and mouth roof corners. For upper S, any singular FINAL roof prefix is removed only at the exact-original-S descending return before the cap exit. That argument is independent of height parity. First-T follows from source x<=a<l<t, retained cap/right heights above v and the bottom's first arrival at v. Finiteness and signed interface velocity matching are preserved throughout.

## Whole native scope and explicit families

For P<=K and EVERY actual native bottom height v, the assumptions g_v<=P and g_v|K imply the lower metric condition automatically. Upper g_v<K is handled by the proper-divisor branch; if g_v=K then g_v<=P<=K forces g_v=P=K, covered by paired sources. All source heights and target heights are therefore covered, and the accepted TR01/TR05 protected placement and reversal give EVERY distinct native pair. If no native bottom height exists, the residual terminal cross case is empty and the protected coverage already suffices. No bound on area, support, reflections or cap depth is introduced.

For c=3,b=1 or 2, v=2 is the sole native bottom height, so g0=gcd(lcm(P,N,K),L)<=P,g0|K suffice. The displayed P5,K6,L8,N18 family satisfies these with g0=2. For equal arms, gcd(N,L)|P gives gcd(lcm(P,N),L)=gcd(P,L)|P prime by prime. For c odd,L dyadic,nu2(N)<=nu2(P), every d2 is odd so g_v is the two-part of P and divides P. All these assertions allow h ODD; no old h-even premise is inherited. The P>K pairwise theorem remains conditional on its metric bound and is not promoted to a whole family.

## Independent prescribed replay and corrected test input

My checker implements raw integer times, both source images, exact Bezout column representatives, and the independent full-period positivity kernel. It runs NO author code. Three fixed inputs pass 570 actual reflections and 5730 finite wall/leg guards: lower and upper odd-h unequal-arm controls P5,K6,N18,L8,e2,b1,c3,h5,H7,S=(2,4) or (2,6),T=(26,2); and critical equality with ODD C=F=3, e4,P=K1,N11,L4,b1,c3,h5,H7,S=(2,6),T=(34,2).

The third control's positive source seed tau14,z1=0 hits the right corner. Its negative source seed 44/3 has z1=-2,z2=10/3; a nonzero complete target-period correction gives final 308/3,E106=10 modulo32 and actual T34,2. This directly checks the raw odd-time critical branch and actual negative initial velocity. My earlier proposed N5 input was discarded by the domain assertion N=P+L before a ray was traced; it is not counted as evidence. This was an own test-input error, not an author finding.

All fourteen source pins and the request hash match before and after. No material correction remains. These exact replays corroborate the independent quantified hand proof, not formal verification or a finite numerical cover. No discovery, new clock, engine, census, fitting, worker, frozen edit or git-state change was used. Uncovered full-divisor/metric cases, larger source widths without all-pair bounds, other normal forms/types, all r3 and r4..8 remain open.
