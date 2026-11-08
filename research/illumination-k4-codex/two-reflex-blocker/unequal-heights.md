# Unequal-height U-room connections

[in progress] 2026-11-01. Separate tools-disabled Opus accepts the main §2 theorem; its correction to the original §3 scope is incorporated. The new §5 matching reduction was added after that review and awaits independent checking. Theory and prescribed exact constructions only; no ray/direction/word/room discovery searches. Keep the room symmetric with arm width a, passage width M, lower height c and arm height H. Put A=2a+M and marks s=(x,y_s),t=(A-x,y_t), where0<x<a and c<y_s,y_t<H.

## 1. Exact matching equations for strict single-crossing one-bottom paths

Choose arm phases independently, giving lengths

    L=a +/- x + 2na, R=a +/- x + 2ma, n,m>=0.

Unfold the sole bottom reflection by joining source height y_s to target height -y_t. Set

    S=y_s+y_t, D=L+M+R, beta=S/D,
    q_s=y_s-beta L, q_t=-y_t+beta R.

Thus q_s-q_t=M beta>0. In the physical room the portal heights are |q_s| and |q_t|. A strict one-bottom path crossing the passage once, in this arm-phase family, exists exactly when:

- 0<|q_s|<c and0<|q_t|<c;
- if the left phase has an earlier inner-wall encounter, q_s+2a beta>c;
- if the right phase has an earlier inner-wall encounter, -q_t+2a beta>c;
- at every outer-wall encounter the developed height is nonzero. It suffices to check the closest outer encounter: q_s+a beta!=0 on the left, q_t-a beta!=0 on the right, when they exist.

Proof. Before reaching its portal the left arm's nearest earlier inner encounter has developed height q_s+2a beta. Because q_s in(-c,c), this is greater than-c; for its absolute value to exceed c it must exceed+c. All earlier inner encounters are higher. The right arm has the reversed test. With an earlier inner encounter present, all outer encounters further back are positive on the left and negative on the right; only the closest outer encounter could otherwise coincide with the bottom. Within each arm the absolute developed height stays below its mark height or c, hence below H. In the passage the developed height runs monotonically from q_s to q_t inside(-c,c). Its zero may be in either arm or in the passage. The folds match at both strict portals and obey reflection. Conversely every strict path with these arm phases, a single passage crossing and exactly one bottom hit has this unfolding and must satisfy those collision tests.

A portal zero q_s=0 or q_t=0 is omitted deliberately: the physical point(a,0) or(a+M,0) is smooth, so such cases may be valid but are outside this strict parameterization. This is not an exclusion of those paths.

## 2. Quantitative unequal-height extension with disjoint paths

Write

    y=(y_s+y_t)/2, delta=(y_s-y_t)/2, d=|delta|, h=M/2.

Assume d>0 and

    d<c,
    a(c-d)(y-c-d) > y h d.                         (U)

The mark assumptions already imply y>c+d. Then there are two corner-free connections with disjoint boundary-contact sets. Every single boundary blocker is therefore avoidable. All parameters are real. This is a sufficient condition; its failure is not evidence of a dark pair or an essential blocker.

### Choose two arm lengths

Set

    B=yh/(c-d)-h,     U=y(h+2a)/(c+d)-h.

Condition(U) is equivalent to U>B+2a. Take the first length of each phase a-x+2na and a+x+2na strictly above B. Both belong to(B,B+2a], are distinct and differ by less than2a, so both are below U. For each chosen length use the same phase/length in the right arm: R=L.

With beta=y/(L+h) and w=yh/(L+h), the developed portal heights are

    q_s=delta+w,       q_t=delta-w.

Since L>B, w<c-d, and both absolute portal heights are less than c. A zero portal is permitted for this theorem: it is a smooth bottom point in the physical U, and there is no vertical reflection there. Strict portal controls are used except where a fixture intentionally checks that smooth coincidence.

### Validity and corners

The nearest earlier inner encounters, when present, have signed left/right-backward heights

    delta+y(h+2a)/(L+h),    -delta+y(h+2a)/(L+h).

Both exceed c because L<U. Earlier inner encounters are higher. The nearest outer encounters have signed heights delta+y(h+a)/(L+h) and -delta+y(h+a)/(L+h). Both are positive, since

    y(h+a)/(L+h) > ((h+a)/(h+2a))(c+d) > (c+d)/2 > d.

Thus the bottom hit occurs after the last left outer-wall encounter and before the first right outer-wall encounter, with no bottom/outer-corner coincidence. Arm heights never exceed their corresponding mark heights or c, so no roof is touched. Each path is valid with exactly one horizontal reflection, at a smooth point of the bottom wall. If that bottom hit lies at a portal, both folding formulas produce the ordinary bottom-wall reflection, with no horizontal-velocity reversal; this partition endpoint is not a room corner.

### No shared boundary contact

At a left vertical contact the remaining arm length r is an odd multiple of a on the outer wall or a positive even multiple of a on the inner wall, and the height is

    v=delta+y(h+r)/(L+h).

On the right it is v=-delta+y(h+r)/(L+h). These are signed heights before the unique bottom hit in each arm's backward orientation; the preceding positivity proves they equal physical heights.

If both paths hit the same left wall point, then

    r1-r2=((v-delta)/y)(L1-L2).

The coefficient is(h+r)/(L+h) in(0,1); r1-r2 belongs to2aZ, whereas0<|L1-L2|<2a. This is impossible. Replace delta by-delta for the right wall. Different physical walls cannot supply an identical point.

The bottom hit has physical horizontal coordinate

    x_B(L)=a+h+delta(L+h)/y.

This formula is valid also when the bottom hit lies in an arm: the preceding outer-encounter positivity puts it within the central stretch with positive horizontal velocity. Since delta!=0 and L1!=L2, the two bottom hits are distinct. There are no other horizontal contacts. Thus their entire boundary-contact sets are disjoint.

### Scope and size of the sufficient region

Equivalently(U) reads

    a c(y-c)-y(a+h)d+a d^2>0.

At d=0 the left side is strictly positive; this gives an explicit range of unequal heights around every previous symmetric configuration. The extension works for every horizontal mark position0<x<a and every real room dimension satisfying(U), with no arithmetic restriction. It makes the earlier qualitative stability result constructive and gives two paths for genuinely unequal heights. Equal heights require the existing third notch path because both bottom hits coincide.

For a concrete scale, set a=1,M=2,c=1,H=3 and mean height y=2. Condition(U) reduces to d^2-4d+1>0, so every half-difference0<d<2-sqrt(3) is covered, for every0<x<1. The total height difference may approach4-2sqrt(3), approximately0.536 passage-height units. This is an explicit sufficient range, not an optimal threshold.

## 3. A genuine obstruction to the narrower passage-bottom family

Take a=2,x=1,H=1,c=1/1000,M=1/100,y_s=1/3,y_t=2/3. Every available L and R is a positive odd integer. A bottom hit strictly in the passage would require q_s>0>q_t. Let

    Delta=R y_s-L y_t=(R-2L)/3.

The two signs are equivalent to

    -M y_s < Delta < M y_t.

But R-2L is odd, so |Delta|>=1/3, while the interval is(-1/300,1/150). Impossible for every arm length, not just a bounded set. This forbids one bottom reflection in the passage within the single-passage-crossing family, with arbitrary vertical arm reflections before and after it. It does not forbid a bottom reflection in an arm, repeated passage crossings with vertical outer-wall reflections in the lower strip, or additional horizontal reflections.

Indeed prescribe L=115 and R=231, both in the plus phase. Then

    beta=100/34601,
    q_s=101/103803,     q_t=98/103803.

Both are positive and below1/1000; the unique bottom hit is inside the right arm. The earlier-inner and outer tests above are strict. This fixed exact construction avoids the passage-family obstruction without invoking roof or notch reflections. It is a prescribed formula evaluation, not a discovered-ray search.

## 4. Repeated passage crossings supply another parameter

The separate Opus reviewer accepted the main theorem but found that my initial obstruction wording omitted this family. Correction incorporated: §3 excludes only a single passage crossing. This omission does not affect §2's explicit constructions.

After entering the lower rectangle at x=a, unfold the horizontal reflections at its two outer walls. To leave through the right portal moving right after2k+1 passage crossings, use effective passage length

    B_k=M+2kA,     k>=0.

Replace D by L+R+B_k in the slope formula. The physical lower-strip path is x=F_A(a+d), y=|q_s-beta*d| for0<=d<=B_k, where F_A is triangular-wave folding into[0,A]. It may hit the outer bottom corners if its unique zero falls exactly at an outer-wall crossing. That coincidence must be excluded separately.

### Prescribed counterexample to the overbroad obstruction wording

In the §3 room use L=133269 in the minus phase, R=266939 in the plus phase and k=100. Then D=40101001/100,beta=100/40101001. Put N=120303003. The entry/exit heights are

    q_s=120301/N, q_t=-120302/N,
    q_s+4beta=121501/N>c,
    -q_t+4beta=121502/N>c.

Both portal heights are below c. The201passage traversals and200outer-wall bounces all stay below c; none of those outer bounces has height0. On the101st passage crossing the developed heights are+1/N and-2/N, so the single bottom hit is strictly inside the passage, at physical x=601/300. This is a frozen construction supplied by the reviewer and checked by exact formulas, not a discovery search. The long arms' nearest-contact inequalities certify all their earlier contacts without listing hundreds of thousands of bounces.

## 5. A general matching reduction via downward jumps

The extra parameter also resolves portal matching abstractly for arbitrary y_s,y_t>c, leaving a specific corner-coincidence issue.

Fix either arm phase on each side. For tau>0 let L(tau) be the first available left arm length strictly above(y_s-c)tau, and R(tau) the first right length strictly above(y_t-c)tau. Their remainders ell_s=L-(y_s-c)tau and ell_t=R-(y_t-c)tau lie in(0,2a], with equality only at a phase jump. Define

    G(tau)=(y_s+y_t)tau-L(tau)-R(tau)
          =2c*tau-ell_s-ell_t.

Between phase jumps G is linear with positive slope y_s+y_t. At each jump it moves DOWN by2a or4a. Since the remainders are bounded, G tends to infinity. Choose tau0>2a/c. For any prescribed B>G(tau0), G attains B at some tau>tau0 lying strictly between jumps. Indeed G eventually exceeds B, and a first upward transition past B cannot occur at a downward jump; on a finite interval there are only finitely many jumps. Thus an open linear segment contains a solution.

At that solution use beta=1/tau. The two portal heights are

    u=c-ell_s/tau, v=c-ell_t/tau,

strictly in(0,c), and u+v=B/tau. Their nearest earlier inner encounters have heights c+(2a-ell_s)/tau and c+(2a-ell_t)/tau, strictly above c. Arm contacts therefore avoid all corners and enter the passage for the first time as required. Taking B=B_k for sufficiently large k produces this algebraic candidate for EVERY pair of heights in the stated room geometry.

At this stage of the reduction, admissibility still appeared to require a lower-strip corner check; the companion proof below now resolves it. The potential coincidence is at x=0 or x=A. It occurs at developed horizontal coordinate

    X=a+u*tau=a+y_s*tau-L.

The subsequent proof in `all-heights.md` resolves this corner issue: bounded arm remainders put X strictly between kA+M/2 and(k+1)A-M/2. It also gives a finite monotone iteration and permits unequal arm widths/heights. A singleton-removal theorem additionally needs alternatives with no shared boundary contact. The main §2 sufficient-region theorem already supplies those alternatives there; this reduction identifies a concrete next obstruction outside that region.

## Next unresolved step

The companion `all-heights.md` resolves bottom/outer-corner avoidance and all-height matching; its opposite-arm proof is now accepted by a separate symbolic Opus reviewer; live peer review is pending. Next control common boundary contacts. The new integer k and the possibility of bottom hits in an arm are both required in the general matching model. The current sufficient region does not establish universal unequal-height singleton removal.
