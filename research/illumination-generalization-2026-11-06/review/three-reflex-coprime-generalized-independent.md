# CE01 independent review

The final pinned proof is independently ACCEPTED at its exact stated scope. The acceptance receipt is in `three-reflex-coprime-generalized-independent.json`; the candidate records the development of the claim before verification. The final proof's sections1 and7 explicitly remove the equal-block exclusion and broaden the native corollary. This review audits those final statements, not a silent extrapolation from the earlier candidate.

## Quantified statement under review

Let L>=2,N>=L+2 be integers, a>0 rational, A=Na,w=(N-1)a,l=(N-L)a. Let b,c,h,H be integers with 0<b<c<h<H and gcd(2(H-h),N)=1. For rational actual interior S=(s,u),T=(t,v), require 0<s<a,b<u<=h,l<t<A,0<v<c and integral u,v. Put d2=c-v and assume gcd(Nd2,L)=1. The proof claims a finite one-roof actual S-to-T ray for all these inputs, including equal developed heights and even d2.

Its whole-native-pair corollary takes integral a>=1, odd L>=3, odd N>=L+2 with gcd(N,L)=1, c=4,b in{1,2,3}, integral h>4,H=h+1. Every distinct actual interior even-even pair in this entire family illuminates. These are unbounded variable-size ten-wall classes, not all W10/r3 or r<=8.

## 1. Geometry and inherited hypotheses: ACCEPT

N>=L+2 and L>=2 give l>=2a>a, l<w<A and R=a,B=La>a. The original strictly ordered TR01 geometry and all its protected U/L hypotheses therefore hold. The new bottom width changes the inner-bottom wall to the genuine x=l interval below c; it does not change the source, cap or right-band mirror intervals. Integral h,H give positive EVEN G=2(H-h). Coprimality with G implies N is odd even though the statement need not list that redundant condition.

## 2. Full forbidden-class selection, including the equal case: ACCEPT

The exact grid tau_q=(A+z-s+2aq)/D leaves each bad event empty or one residue class modulo D/gcd(t_i,D), with t1=d0,t2=d0+G,t3=D-d2. This remains valid for rational a,s,z: one subtracts any existing solution rather than assuming an integral constant. A zero t1 has no bad event. The nonzero times are distinct and in(0,D).

The independently accepted three-class density/CRT classification leaves only repeated period2, triple period3 or (2,4,4). The first two are impossible for distinct times; the last forces d0=G=g1=d2=lambda. Here the proof correctly uses the correlated physical offsets. If the cap event is nonempty, s+z-A=2ar for an integer r. The source phase is then `[s+A+a(r+q)]/2`. A source bad event would imply `s/a+N+r+q=2 (mod4)`, impossible for 0<s/a<1. Thus at least one of the cap/source bad classes is empty. With a cap class the remaining density is at most3/4; without it the other two have total density at most1/2. The equal case cannot cover. This agrees with the separately accepted equal-block addendum; the author proof independently contains the needed argument and does not depend on a pending supplement.

All bad classes are D-periodic, so a permissible q exists among0,...,D-1. Its grid slope is positive because A+z-s>A-a>0. No period/reflection cutoff is inferred.

## 3. Coprime cap placement and modulo-L actual target: ACCEPT

The source residual stays unchanged under tau->tau+2aM because d0 is integral. The cap phase increments by2aGM modulo2Na. Its N orbit points are precisely one spacing-2a coset. The excluded second event ensures that coset misses both endpoints of the open width2a cap window, so it has exactly one point strictly inside. The right residual's excluded third event stays excluded under the same shift since its time is integral and A=Na. Both source and right phases are preserved in their correct original chart, not chosen independently.

After cap/right matching, E=z2+d2*tau=z+2aJ with integral J. The bottom fold now has period2La, so the old parity repair is correctly replaced by J=0 modulo L. A further slope shift2aN changes the center indices by Nd0,G,Ng1 and preserves all three residuals EXACTLY. It changes J by Nd2. Under gcd(Nd2,L)=1, the modular inverse gives a unique correction p in0,...,L-1. The resulting E=z modulo2La, and 0<z<La gives the same actual t=A-z. This is the full actual bottom period, not merely its projection modulo2a.

The gcd hypothesis is a sufficient hypothesis for this uniform correction. This review does not claim it is necessary for illumination, or that failure makes any pair dark.

## 4. Physical ray, walls, corners and first target: ACCEPT

The source/cap/right gluing is unchanged from the independently accepted core. At the final portal |z2|<a<La makes both adjacent folds locally A minus the same absolute value; hence signed velocities match even at zero residual. Source u=h simply omits its zero-duration source band, with z0=s. There is one common absolute slope throughout, and only the physical roof reverses the vertical velocity.

All open-band mirrors are on the original finite intervals x=0,a in the source band above b; x=0,A above h; x=w,A between c,h; and x=l,A below c. Strict residual bounds avoid the genuine reflex vertices, ledges and any artificial cut. A roof cusp would give identical coordinates at the two h-level cap mouths, contradicting their ranges [0,a) and(w,A]. Thus the roof is smooth. Finite parameters give finitely many contacts without a uniform bound.

The nominated endpoint is the actual T. On ascent any possible visit to its height v has x<a<t because l>=2a; cap heights exceed v. On descent height equals v only at the end. No earlier T, wrong endpoint fiber, singular continuation, direction concatenation or changed physical room is used.

## 5. Entire even-displacement native family: ACCEPT

For c=4, every actual native bottom point has even ordinate v=2, so d2=2. Odd L and gcd(N,L)=1 imply gcd(2N,L)=1. H=h+1 contains no integer interior cap level, so every actual native left-terminal source has integral u<=h. G=2 is coprime to odd N. All native residual terminal pairs therefore satisfy the new lemma. The resonance h=6,u=4 is INCLUDED by the proof's equal-case argument.

Protected TR01 covers every other native pair using its already reviewed original-wall guards. There are no unhandled native open-cap marks; h-level seam marks are included exactly. Label reversal is a regular reversible ray. The proof consequently covers every distinct actual native pair for all dimensions in its stated family, independently of the prescribed finite controls.

## 6. Entire power-of-two native family: ACCEPT

For L=2^r, integer r>=1, N odd>=L+2, c odd and H=h+1, each native even v makes d2=c-v odd. Thus Nd2 is odd and coprime to L. The terminal lemma applies; the same protected TR01 coverage and absent native open-cap levels give every native pair. Integral a>=1 and all strict integral height orders remain required. This is a separate sufficient whole-family corollary, not arbitrary bottom multipliers.

## Independent prescribed verification

Run `python3 -B .context/illumination-generalization-2026-11-06/review/three-reflex-coprime-generalized-check.py`.

No author/coordinator code executes. The checker uses the last permissible q, a different direct cap modular-inverse convention, the exact final modulo-L inverse, and the reviewer-owned actual earliest-wall replay. Eleven prescribed terminal controls pass with1882 actual reflections and18930 wall/leg guards. They exercise equal-block cap-nonempty/cap-empty cases, u=h, t=w, rational widths/marks, a two-unit cap, even d2, odd d2, and composite multipliers L=9 and N=9.

In the one prescribed room `(a,l,w,A;b,c,h,H)=(4,8,16,20;1,4,5,6)`, the checker independently enumerates the complete eight native interior marks. All28 unordered pairs pass,10 by the new terminal mechanism, with622 reflections and6540 wall/leg guards. The room fails the former H>=404 and A>=484 sufficient conditions. Different reflection totals from the author are expected because different valid arithmetic selectors are used. No sample proves the quantifiers; they are supported by the hand proof above.

## Remaining limits and next step

No correction is needed in the final proof's stated generalization. It still requires commensurate widths R=a,B=La,A=Na, integral developed heights, cap coprimality, target-step coprimality and the specified terminal source range u<=h. General real marks, arbitrary spiral metrics, upper-left terminal sources with u>h, other r3 types and r4..8 remain open.

A concrete next arithmetic gap is gcd(Nd2,L)>1. For a FIXED already selected q and cap phase, the allowed preserving shifts hit the actual positive target image if and only if gcd(Nd2,L) divides J. The same path may still be obtainable by another initial q, target image sign or an enlarged actual phase mechanism; none is proved here. A coverage theorem must make those choices jointly rather than label the failed sufficient gcd condition darkness. This remains a genuinely missing existence step, not a reason to restart old cutoffs.

## Final pin reconciliation

All 16 CE01 source pins passed before and after the independent replay. The final request and candidate explicitly include both native corollaries and the equal-block repair. No material finding remains at these scopes. The full r3/r<=8 target remains open.
