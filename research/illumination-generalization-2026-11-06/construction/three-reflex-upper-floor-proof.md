# UP01: positive upper-source entry, actual floor return and full target

Independent review pending. All parameters are the original-room parameters from the candidate, with precise N>P+L. No width-a reflection is used aboveh. FR01 supplies intuition only; upper-source transfer and joint availability are proved here explicitly.

## 1. Parameters and the actual five bands

Let a=Pe,A=Ne,R=e,B=Le, P odd>=5,Nodd,N>P+L,L a power of2,e positive integral. Take integer0<b<c<h<H,h even,codd,epsilon=H-h andgcd(P*epsilon,N)=1. Actual native S=(s,u) has0<s<a,u=h+2N*ell<H for integerell>=1. Actual native bottom T=(t,v) hasl<t<A,0<v<c. Set
 dpre=u-h=2N*ell,
 dleft=2(h-b), C=2epsilon, g1=h-c odd,d2=c-v odd,
 D=dpre+dleft+C+g1+d2 even,z=A-t,
 a0=P/gcd(P,h-b) odd.
Thus gcd(epsilon*a0,N)=1. All durations are positive; dpre<epsilon is exactlyu<H.

At finite positive horizontal slope tau start with vertical velocity-1 and use these ORIGINAL bands:

1. Initial cap descent, durationdpre: x=F_A(s+tau*w), y=u-w. At its endpoint require s+dpre*tau=2A*npre+zpre with |zpre|<a. The even cap center is necessary for the LEFT opening, not the right one.
2. Left-arm loop, durationdleft: x=F_a(zpre+tau*wleft), with y descending fromh tob and ascending back toh. At its endpoint put zpre+dleft*tau=2a*nleft+z0 and require |z0|<a.
3. Roof cap, durationC: x=F_A(z0+tau*wcap), ascendh->H then descendH->h. At its endpoint require z0+C*tau=(2m+1)A+z1 with |z1|<e.
4. Right arm, durationg1: x=A-F_e(z1+tau*wright). Center its endpoint z2 with |z2|<e.
5. Bottom, durationd2: x=A-F_Le(z2+tau*wbottom). Require final F_Le(z2+d2*tau)=z.

Each adjoining fold agrees in actual value and signed derivative near a strict interface. All vertical mirrors in band1 are0/A and all in band2 are0/a belowh; none is invented aboveh. The other bands retain their original walls. A zero residual is a smooth outer-wall reflection, not a true corner. Roof corners are excluded by symmetry: they would identify the ascending left h mouth x<a with the descending right h mouth x>A-e, which are disjoint.

## 2. Exact-S repair if the formal floor is a corner

The left floor occurs at full elapsed u-b=dpre+h-b. Its phase in the left chart is zpre+tau*(h-b). If this equalsj*a, no actual path may traverse that corner. At the second h passage the left phase becomes2ja-zpre, hence its centered residual is EXACTLYz0=-zpre, because|zpre|<a.

After another cap ascent of durationdpre<epsilon, the phase is
 -zpre+tau*dpre=-s+2A*npre.
Its fold is EXACT actuals, with actual horizontal velocity-tau and vertical velocity+1, and its height isu. Thus the formal curve returns to original actualS at elapsed2(u-b), BEFORE the roof. Delete the entire corner-containing prefix and emit the regular remaining suffix from S. It reaches the original target under the later strict guards and never traverses the discarded corner. If the floor is ordinary, retain the whole path. Apply this dichotomy only to the FINAL slope; no preservation of a preliminary floor's regularity is assumed.

Initial-cap heights are>=h>v. Every left-loop visit to heightv hasx<=a<l<t. Cap/right heights exceedv, and the bottom reachesv only at its end. Therefore the resulting actual path reaches FIRST actualT. All durations, widths and slope are finite, so it has finitely many original specular reflections.

## 3. FOUR choices jointly enter left and avoid later source/cap endpoints

Start with the full target-compatible grid
 tau_q=(A+z-s+2eq)/D, q>=0 integer.
Its numerator is positive. The UNFOLDED first-cap endpoint
 Ypre(q)=s+dpre*tau_q
is increasing and unbounded with stepdelta=2e*dpre/D<2e. Choose an integer npre>=0 with
 Upre=2A*npre+a>Ypre(0)+4delta.
Let q* be the first integer withYpre(q*)>=Upre; thenq*>4. Its four predecessors satisfy
 Upre-4delta<Ypre(q*-i)<Upre, i1..4.
Because4delta<8e<2Pe (P>=5), ALL four lie in the SAME strict left-entry window(2A*npre-a,2A*npre+a). This fixes their actual initial fold index npre. No later adjustment is allowed to break this entry.

At fixed npre the actual left-loop endpoint is bad precisely when
 s+(dpre+dleft)*tau_q-2A*npre=Pe modulo2Pe.
Its solution set is empty or one q class with period
 pS=P*D/gcd(dpre+dleft,P*D)>P>=5,
since0<dpre+dleft<D. It can remove at mostONE of these four consecutive indices.

The cap-boundary bad event is
 s+(dpre+dleft+C)*tau_q=(N+1)e modulo2e.
Its period is pC=D/gcd(dpre+dleft+C,D)>=2, since the time isD-g1-d2 strictly between0andD. It removes at mostTWO of four consecutive indices. Source/initial fold removals are multiples2e, so this is the correct boundary event even with varying nleft. Together at mostthree candidates are removed. At least oneq has strict initial left entry, strict left-loop exitz0, AND a cap phase X0=z0+C*tau not on the endpoint class A+e modulo2e. This proves joint availability, not three separate conditional equations.

## 4. Preserve BOTH entries while selecting cap and right exit

Increase the selected slope by e*a0*M for integerM>=0. The first-cap endpoint changes by
 dpre*e*a0*M=2A*(ell*a0*M),
so initial npre increases byell*a0*M and literal zpre is unchanged. The left-loop phase then changes by2(h-b)*e*a0*M, an integer multiple2Pe because a0=P/gcd(P,h-b). Thus literal z0 is ALSO unchanged.

The roof-cap phase increases by2e*epsilon*a0*M. Modulo2A, gcd(epsilon*a0,N)=1 gives the entire coset with spacing2e. The OPEN right-entry interval(A-e,A+e) has this length. Its endpoints were excluded, so exactly one representative lies strictly inside. Choose0<=M0<N reaching it, with actual cap indexm and literal strictz1.

The alternative M0+N preserves BOTH earlier residuals and z1, increasing m byepsilon*a0. Its right pre-fold phase differs by g1*e*a0*N, an odd multiple ofe. At most one of the two choices can be the actual right-corner classe modulo2e. Select a safeM, with literal strictz2. Hence all FOUR actual passage guards now hold jointly.

D is even, so addinge*a0*M increases the original q grid index by D*a0*M/2, an integer. The complete seed identity is
 E=z+2eJ,
 J=q+D*a0*M/2-N*npre-P*nleft-N*m-k.
Here npre,nleft,m,k are the actual fold indices AFTER the M shift. None is discarded or treated as an independent sheet choice.

## 5. Match the original target with all four guards unchanged

The final slope increase2e*a0*N*p changes the first-cap/left-loop/roof-cap/right indices by
 dpre*a0*p,
 2(h-b)*a0*N*p/P,
 2epsilon*a0*p,
 g1*a0*N*p,
respectively. Every increment is integral and every literal zpre,z0,z1,z2 is unchanged. E increases by2e*a0*N*d2*p and J by a0*N*d2*p. The latter is odd and coprime to Lpower2. Select0<=p<L givingJ+a0*N*d2*p=0 moduloL. This reaches exactly actualt after the entire bottom fold.

Apply sections1--2 at this FINAL slope. The source is the original upper-capS, the initial cap uses its full physical width, all corner and first-hit guards are genuine, and target attainment is exact. No mixed directions are concatenated, no artificial wall is reflected from, and no bounded word/direction search is used.

## 6. Exact scope

This is a positive upper-source terminal-pair theorem for the stated family, with source depthu-h a positive multiple2N andPodd>=5. It does not supply arbitrary upper-depth availability, arbitrary narrow arms or every room pair. FR02 covers a different lower-source family; their union is not all ordered spirals. The remaining r3 and r<=8 goal remains OPEN.

## 7. Prescribed arithmetic controls before execution

A. e2,P5,K1,L4,N11,b1c3h4H27,S4,26,T18,2. Hereepsilon23,ell1,a05,dpre22,dleft6,C46,D76. Choose first-entry npre1,Upre54,q*38 andq37. Then tau85/38,zpre175/19,z0=50/19,X2005/19. CapM9 yields tau3505/38,z1=-9/19,z2=-9/38,E92,J22. Finalp2 gives tau20225/38,E532,J132,actualT18,2. Finalindices npre266,nleft160,m556,k133. This nontrivially tests BOTH preserved entry phases and weighted a05.

B. e2,P5,K1,L4,N11,b1c5h6H29,S4,28,T18,2. Hereepsilon23,ell1,a01,dpre22,dleft10,C46,D82. Choose first-entry npre1,Upre54,q*42 andq41. Then tau93/41,zpre406/41,z0=-304/41,X3974/41. CapM3 yields tau339/41,z1=-44/41,z2=-33/41,E24,J5. Finalp3 gives tau5751/41,E420,J104,actualT18,2. Both floor contacts are ordinary; the general exact-S corner-suffix branch is proved symbolically, not inferred from these controls.

No discovery search or new clock/engine/census/worker/git mutation. Fixed prescribed checks corroborate this quantified hand argument; independent review remains required.
