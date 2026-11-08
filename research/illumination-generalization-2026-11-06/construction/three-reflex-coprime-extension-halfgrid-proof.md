# LC04 proof: two target images restore a missing half-grid

Independent review pending. Original-room notation is LC04 candidate. This proof uses the offset first-crossing lemma proved in LC03 sections2--4, itself an explicit generalization of peer-originated and independently accepted LC01R. Review of LC03 remains a separate prerequisite; no acceptance is inferred here.

## Quantifiers and the new target condition

Let P,K,L,N be positive integers,K<L,N>P+L; e>0 rational, integer0<b<c<h<H, actual rational S=(s,u),T=(t,v) with integer u,v in the original terminal ranges. Let d0,C,g1,d2,D,z and Lambda retain their definitions. Set g=gcd(Lambda*d2,L). Assume
 g|P, K=g, z/e=(g/2)*(2ell+1) for some integer ell.
Here0<z<Le forces ell>=0. We allow K1. No new lower bound on size, aspect, height or reflection length is imposed.

Define eprime=eg/2, Pprime=2P/g>=2, Kprime=2. Then a=Pprime*eprime and Ke=Kprime*eprime. Original A/eprime need not be integral. We will choose half-integral original q when g is odd; only the eventual target congruence needs an integer index.

## One common physical cap branch and a legal index

Let tau_max=(A+z-s+2e(g-1))/D and B=a+C*tau_max, rho=2eprime*(d0+C)/D<2eprime. Choose integer m>=0 with U=(2m+1)A+Ke>B+4rho. Set r as the least nonnegative residue Nm modulo g AFTER choosing this m. For all j>=0 use
 q_j=r+(g/2)*j,
 tau_j=(A+z-s+2e*q_j)/D.
The uniform B bounds X(0) for any r, avoiding circularity of the residue/window choice.

Below h the source fold has actual width Pprime*eprime. Its forward increment before centering is2eprime*d0/D<2a; source resets decrease X. Its bad-index period is Pprime*D/gcd(d0,Pprime*D)>Pprime>=2. The right sufficient event is
 s+(D-d2)*tau_j-(2m+1)A=Ke modulo2eprime.
This has period D/gcd(D-d2,D)>=2. Because g|P and K=g, removed source periods2Pe are multiples2eprime=eg, and actual right periods2Ke are also such multiples. Avoiding the sufficient event excludes the actual right reflex corner.

All hypotheses of the offset first-crossing choice lemma hold with these Pprime,Kprime and arbitrary fixed offsets. It supplies a positive j at strict source/cap/right residuals in this SAME cap branch. In detail: if right period2, forward step<eprime and four predecessors fit; the source period>=3 cannot kill both survivors. Otherwise both periods>=3; if last two are bad, the source reset makes the third predecessor fit and avoid both classes. No source-period2 case occurs since Pprime>=2. At/above h there is no source band; two predecessors fit and the single right class leaves one. These arguments use integer j, not integrality of q. A zero residual is a smooth outer-wall reflection.

## The half-integer index selects the target image

The exact initial phase identity remains valid for REAL q:
 E=z+2eJ, J=q-Pn-Nm-Kk.
Since r-Nm is divisibleg, Pn and Kk are multiplesg, and q=r+g*j/2,
 J belongs to g*(Z+j/2).
Thus there are exactly two cases.

* j even: J is an integer multiple ofg. Use the positive target image and target index I=J.
* j odd: J need not be integral. Instead use the negative target image:
 E=-z+2eI, I=J+z/e.
Because z/e=g*(ell+1/2), I is an INTEGER multiple ofg. This addition is essential; applying an integer congruence directly to half-integral J would be invalid.

In either case solve
 I/g+(Lambda*d2/g)*p=0 modulo L/g
with0<=p<L/g, or p0 if L/g1. The coefficient is invertible by the definition ofg. Add2eLambda*p to the slope. All source/cap/right indices shift integrally and every literal signed residual is unchanged. E then equals +z or -z modulo2Le according to the already selected case. The bottom triangular fold is even, so BOTH alternatives give F_Le(E)=z and actual target abscissa A-z=t.

One final positive finite slope defines the whole path. No two directional trajectories are spliced. Choosing an unfolded image is not changing the physical target, since the final fold calculation verifies actual t. This is precisely the mechanism absent from the failed positive-integer-grid control.

## Full original optical guards

The source/cap/right/bottom charts are the accepted original-room charts. Their strict residuals match phase position and signed velocity, excluding every original reflex corner at a passage. Roof corners for lower sources contradict disjoint ascending/descending mouths. For an upper source, only the accepted EXACT-S descending suffix may be kept if its formal roof contact is singular; the discarded corner is never traversed. Ordinary smooth zero contacts remain legal. Height separation gives first actual T, and positive finite widths/slope give finitely many wall contacts.

The theorem proves the stated terminal-pair class. It does not assert every native pair satisfies the half-odd target offset, does not prove all K1 rooms, and does not close all r3 or r<=8. When the two image grids coincide instead of interlacing at a half-step, this proof gives no selection lemma. The peer's countercontrol is compatible with this distinction.

## Four prescribed hand calibrations, before execution

A. Peer K1 geometry e4,P3,K1,L4,N9,b1c3h5H7,S6,6,T30,2. Here g1,z/e3/2,eprime2. Choose m0,r0,U40,first j*8. Select j7/q7/2: tau32/3,z1=2,z2=-2/3,E10,J1/2,I2 (negative image). Correction p2 gives tau464/3,E154=-6 mod32,actualT30,2. This is a different explicit witness from the peer's460/3.

B. Same room, lower S6,4: d01,C4,D8. Choose m1,r0,U112,first j*43. Select j42/q21: tau51/2,z0=15/2,z1=3/2,z2=-7/2,E22,J2 (positive image). Correction p2 gives339/2,E166=6 mod32,actualT30,2.

C. Same room, mouth S6,5: d00,C4,D7. Choose m1,r0,U112,first j*38. Select j37/q37/2: tau184/7,z1=22/7,z2=-2/7,E26,J5/2,I4 (negative image). No correction p0; actualT30,2. This rational endpoint control tests the mouth convention; S6,5 is not native even-even, so it is a terminal theorem control only.

D. A g2 native case: e2,P2,K2,L4,N7,b1c3h6H9,S2,4,T8,2. Here Lambda14,g2,z/e3. Choose m1,r1,U46,first j*17. Select j15/q16: tau41/6,z0=-1/3,z1=-4/3,z2=19/6,E10,J1,I4 (negative image); p0 reaches actualT8,2. LC03's reducedK>=2 condition fails because K/g1, while LC04's paired images supply the missing half-step.

No discovery search, new clock, census, worker, engine or git-state change. Fixed arithmetic checks corroborate, never prove universal quantifiers by sampling.
