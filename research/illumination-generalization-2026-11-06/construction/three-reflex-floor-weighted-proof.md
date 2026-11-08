# FR02: weighted source period removes the floor-height equality

Independent review pending. Physical dependency: FR01 section1 original floor-prefix/EXACT-S-suffix transfer. It is reused only for b<u<=h; no left-arm walls are invented aboveh. FR01's initial native arithmetic family remains frozen.

## 1. Statement

Original ordered spiral a=Pe,A=Ne,R=e,B=Le; integersP>=1,N>P+L,Nodd,L=2^j,integer e>=1,integer0<b<c<h<H,h even,codd. Actual native S=(s,u),b<u<=h,0<s<Pe; native bottom targetT=(t,v) in the usual strict ranges. Let
 d=h+u-2b (positive even), epsilon=H-h,
 g1=h-c odd, d2=c-v odd,
 C=2epsilon, D=d+C+g1+d2 even,
 a0=P/gcd(P,d/2).
Assume a0odd andgcd(epsilon*a0,N)=1. Claim: actualS illuminates actualT, with a retained ordinary floor or the exact-S suffix if its formal floor is a corner.

## 2. First choose a source-safe and cap-nonboundary seed

For integerq>=0 set tau_q=(A+z-s+2eq)/D>0,z=A-t. Actual source-bad is s+d*tau=Pe modulo2Pe. Its q solutions are empty or a single class with period
 pS=P*D/gcd(d,P*D)>P>=1.
Cap-boundary bad is s+(d+C)*tau=(N+1)e modulo2e. Its period is
 pC=D/gcd(d+C,D)>=2,
since0<d+C<D. If pS2, then P1 and d=D/2, as follows from PD/2<=d<D and exact gcd. If pC2, then d+C=D/2. Both cannot occur since C>0. Thus two possible bad classes have periods>=2 and cannot both have period2. Their densities sum to at most1/2+1/3<1. They cannot cover all integers. Both periods divide the COMMON periodP*D (not necessarilyD), so a seed can be chosen finitely in0..P*D-1 avoiding both.

After actual source centering, literal |z0|<Pe. Since removed2Pe*n is a multiple2e, X0=z0+C*tau is also not on the cap boundary class A+e modulo2e. This statement excludes endpoints, not merely a nearest-point error bound.

## 3. Weighted source-preserving cap rotation and a safe right exit

Set ell=(d/2)/gcd(P,d/2), an integer. Increasing slope by e*a0*M changes the actual source index by ell*M, leaving literal z0 unchanged. The cap phase increases by2e*epsilon*a0*M. Asgcd(epsilon*a0,N)=1, modulo2Ne the N candidates cover the entire coset of spacing2e. The open interval(A-e,A+e) has exactly this length and has no coset point at its endpoints. Choose0<=M0<N whose phase is strictly inside it, obtaining literal |z1|<e at some actual odd cap center.

The alternative M0+N increases cap phase by2A*epsilon*a0; cap index changes by epsilon*a0 and z1 stays IDENTICAL. The two right phases differ by g1*e*a0*N, an odd multiple ofe. Thus they cannot both equal the actual corner class e modulo2e. Select a safe M in{M0,M0+N}, giving strict |z2|<e. All source/cap/right folds retain actual signed derivative matching. No corner-bad seed is propagated as a ray.

Because D is even, the weighted shift e*a0*M changes the initial grid index by D*a0*M/2, an integer. Thus
 E=z+2eJ,
 J=q+D*a0*M/2-Pn-Nm-k
is integral. Portal strictness alone is not target matching.

## 4. Preserve all guards while reaching the complete actual target

The FINAL slope period2e*a0*N*p changes source/cap/right indices by
 2ell*N*p, 2epsilon*a0*p, g1*a0*N*p.
Each is integral; every literal residual z0,z1,z2 is unchanged. E changes by2e*a0*N*d2*p, so J changes by a0*N*d2*p. The latter coefficient is odd and coprime to Lpower2. Choose0<=p<L withJ+a0*N*d2*p=0 moduloL. The full original bottom fold reaches actual t.

FR01 section1 now supplies a legal actual path for the FINAL slope: retain the entire path only if the floor is ordinary; otherwise delete the formal prefix and emit the regular suffix from exactlyS before its ascending h passage. Roof corners are excluded by disjoint mouths. All strict original passages and signed velocities remain matched, and first actualT follows from height/abscissa separation. One finite positive slope and finitely many original reflections suffice.

## 5. Complete lower-source native corollary

Suppose Podd andgcd(P*epsilon,N)=1 in addition to the original Nodd/Lpower2/h even/codd hypotheses. For EVERY actual native source inb<u<=h, d is even and a0 divides the odd integerP. Therefore a0odd andgcd(epsilon*a0,N)=1. The theorem applies to EVERY native bottom target and EVERY such source, with no fixed source ordinate, cap-depth bound or reflection bound. P and N may be composite.

FR01 is recovered atd=2P andepsilon1, wherea01, including evenP. The general theorem therefore also retains pair-specific evenP cases witha0odd. The full lower-source corollary is new scope beyond a fixed d=2P equality; its physical mechanism is the previously introduced original floor return.

Upper-cap terminal sources u>h, incompatible cap/source arithmetic, other spiral metrics/forms and the remaining r3/r<=8 cases remain OPEN. A weighted period alone is not claimed to prove those cases, and the stronger whole-room goal is not complete.

## 6. Two prescribed arithmetic controls before execution

A. e4,P3,K1,L4,N11,b1c3h6H8,S8,4,T36,2. Here d8,C4,g1=3,d2=1,D16,epsilon2,a03, so the old d=2P equality fails. q0 gives tau11/4,z06,X17. CapM6 gives tau299/4,X305,capcenter308,z1-3,rightz2-11/4,E72,J8. Already target-divisible, p0 reaches actualT36,2. Floor x31/4 is ordinary.

B. Retain FR01's necessary right-flip control e2,P2,K1,L4,N7,b1c3h4H5,S2,2,T10,2. Herea01. q0,capM2 hits a true right corner; M9 gives tau20,z1=z20,E20,J4,p0,actualT10,2. This is a prescribed replay of an existing control, not another discovery or new evidence count.

No discovery, new clock, engine, census, fitting, worker or git mutation. Quantifiers come from the proof; these controls only check arithmetic and actual endpoint identities.
