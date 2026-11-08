# UC01: complete cap orbit, a nontrivial return, and ALL upper-source depths

Independent review pending. This reverses the earlier selection order: first choose an actual right-cap entry from the complete exact target grid, then use one exact cap return to avoid the actual right corner. No initial left-floor excursion is used.

## 1. Quantified upper-source theorem

Use the original ordered strictly simple ten-wall spiral a=Pe,l=(N-L)e,w=(N-1)e,A=Ne, with integerN>P+L,L>=2 and positive rational e. SupposeN is odd,L a power of2,integer0<b<c<h<H,h even,codd. Let actual rational horizontal marksS=(s,u),T=(t,v) have
 0<s<A, h<u<H, u EVENinteger,
 l<t<A, 0<v<c, v EVENinteger.
No parity assumption on horizontal coordinates is needed for this upper-source lemma. Its native even-even case is included. No restriction onP parity, cap depth gcd or source depth moduloN is imposed.

Set z=A-t in(0,Le),g1=h-c odd,d2=c-v odd,
 C=2H-h-u=2n>0,
 D=C+g1+d2=2H-u-v=2d,
where integersd>n>=1. Choose on the exact full-target grid
 tau_q=(A+z-s+2eq)/(2d), q>=0integer.
The numerator is positive because s<A and z>0.

The physical cap curve isx=F_A(s+tau*w), y ascending fromu toH then descending toh, with total durationC. The right arm isx=A-F_e(z1+tau*w_R), durationg1; the bottom isx=A-F_Le(z2+tau*w_B), durationd2. Their positions AND signed derivatives agree when |z1|<e and|z2|<e. Only genuine cap/right/bottom walls are used.

## 2. The complete cap orbit ALWAYS enters the open right mouth

The cap phase is
 X(q)=s+C*tau_q=X(0)+(2e*n/d)q.
LetG=gcd(n,N*d),Q=N*d/G. SinceG<=n<d, G/d<1. The rational phase generator has exact periodQ modulo2A=2Ne, and its coset spacing is
 2e*G/d < 2e.
The open cap right-mouth interval has length2e, so it contains a point of EVERY such coset, with strictness, regardless of offset.

For a completely explicit construction choose an integerell nearest to
 (A-X(0))*d/(2e*G).
ThenY=X(0)+(2e*G/d)*ell satisfies |Y-A|<=e*G/d<e. The inverse ofn/G moduloQ exists becausegcd(n/G,Q)=1. Solve
 (n/G)*q0=ell moduloQ,
with0<=q0<Q. NowX(q0)-Y is an integer multiple2A. ThereforeX(q0)=(2m+1)A+z1, with literal z1=Y-A strictly between-eande. BecauseX(q0)>0 the actual cap indexm is nonnegative. No open-recurrence premise, bounded direction list or presumed favorable endpoint phase is used.

## 3. An exact cap RETURN cannot fix the right-corner class

Increase q0 by the exact cap periodQ. The slope increases by
 Delta_tau=(e/d)*Q=e*N/G.
The cap phase increases byC*Delta_tau=2A*(n/G), an integer number of actual cap periods, so z1 is IDENTICAL. Its right pre-fold phaseY_R=z1+g1*tau increases by
 e*g1*N/G.
This is NOT an integer multiple of the actual right period2e: equality would make the odd integerg1*N divisible by the even integer2G, impossible. Thus ifq0 gives the true right-corner class e modulo2e, q0+Q does not. Ifq0 is already safe, retain it. In either case the chosen centered residual|z2|<e is strict. At most one cap return is used for selection; this is not a uniform optical reflection bound.

The change may be a rational fraction of a right period; no claim of a literal half-period is needed. Only its proved nonintegrality modulo the full actual right period is used.

## 4. Reach the FULL actual target while preserving both strict portals

For the selected integerq and actual cap/right indicesm,k,
 E=z2+d2*tau
  =s+D*tau-(2m+1)A-2e*k
  =z+2eJ, J=q-N*m-k INTEGER.
A positive finite slope increase2e*N*p changes cap/right indices byC*p andg1*N*p, both integers, preserving z1,z2 LITERALLY. It changes J byN*d2*p, odd and therefore a unit moduloLpower2. Choose0<=p<L with
 J+N*d2*p=0 moduloL.
The final bottom phase is+z modulo2Le, soF_Le(E)=z and the actual last point ist=A-z. This is the original physical target, at one common final slope, not another point over a covering projection. Cap-return selection and final target correction are complete before emitting the actual ray; no trajectories of different slopes are concatenated.

## 5. Roof, true corners, actual source and first target

The only unguarded formal corner is a roof endpoint. If s+tau*(H-u) is a multipleA, the folded cap symmetry gives
 F_A(s+2tau*(H-u))=F_A(-s)=s.
At elapsed2(H-u) the formal descending curve returns to EXACT actualS. Sinceu>h, this occurs strictly before its right h passage. Delete the entire formal prefix including the corner and emit only this regular descending suffix from originalS with its actual signed horizontal/vertical velocity. No physical trajectory traverses the discarded corner. If the roof is ordinary, retain the full cap curve. Apply this dichotomy at the FINAL slope, not at a preliminary seed.

All right h/c reflex corners are excluded by strict |z1|,|z2|<e. A zero residual gives a smooth genuine outer-wall reflection. Every retained open cap/right/bottom segment stays in the original polygon, with no artificial mirror. Cap/right heights exceedv; the descending bottom reachesv only at its final time. Therefore this is first actualT. Positive finite slope and widths give finitely many ordinary original-wall reflections.

## 6. Whole-room native corollary via the accepted exact placement join

Now take e positive integral,P ODD,Nodd,N>P+L,K1,Lpower2>=2,integer0<b<c<h<H,h even,codd andgcd(P*(H-h),N)=1. All native interior marks are actual even-even points.

The independently accepted TR01/TR05 original-room placement reduction leaves only pairs, up to reversal, with
 S in(0,a)x(b,H), T in(l,A)x(0,c).
Their exact artificial-cut/mouth equalities are retained in that accepted reduction. Forb<u<=h use independently accepted FR02: d=h+u-2b is even,a0=P/gcd(P,d/2) divides oddP andgcd((H-h)*a0,N)=1. Thus every such actual lower/mouth source connects to every native bottom target. Forh<u<H use UC01, whose upper-source hypotheses hold for the SAME original pair with no extra depth condition. Every complementary placement is already covered by TR01/TR05, and legal ray reversal covers exchanged labels.

Therefore EVERY distinct native interior pair illuminates in this entire quantified ten-wall room family, with arbitrary source heights, cap depth, size and reflection length subject to its explicit arithmetic conditions. P,N may be composite. This is the first all-source join here at right-widthK1; earlier lower-source, depth-congruence and coset-width restrictions do not survive in this joined family.

This does NOT prove all ordered spirals, allr3, arbitrary polygons orr<=8. OddN, h even/codd and the lower-branch cap/source arithmetic are real remaining hypotheses. The N8 K1R01 whole-one-roof obstruction violates oddN; the N9,h5 positive-grid obstruction violates oddg1. Both accepted controls remain valid and are not counterexamples to this theorem.

## 7. Three prescribed controls before execution

A. Existing reviewer near-roof input:e4,P1,K1,L4,N7,b2c3h4H12,S2,10,T20,2. n5,d6,G1,Q42. q0 gives tau17/6,z1=7/3,z2=-17/6,J-1. Finalp3 gives1025/6,J20,actualT20,2. This is a one-roof path; a separate floor-itinerary search is unnecessary for proving existence on this pair.

B. An ACTIVE right-corner repair: e2,P3,K1,L4,N9,b1c3h4H9,S2,6,T14,2. n4,d5,G1,Q45. q0 gives tau2,z1=0 and rightY2 TRUEcorner. Useq45, slope20, capm4,z1=0,rightk5,z2=0,J4. Finalp0 reaches actualT14,2 with smooth cap/right zero residuals. Only the latter ray is retained.

C. Nontrivial capG: sameN7room as A, sourceS2,6,T20,2. n7,d8,G7,Q8. q0 gives17/8,z1=15/4,z2=-17/8,J-1. Finalp3 gives1361/8,J20,actualT20,2. This checks the rational orbit spacing2eG/d and cap-return formula withG>1.

These controls are prescribed formula verifications, not a census or discovery search. The quantified proof above supplies the all-depth existence assertion. No new engine, worker, clock or git mutation. Independent audit of the complete upper theorem AND the whole-room join is required before acceptance.
