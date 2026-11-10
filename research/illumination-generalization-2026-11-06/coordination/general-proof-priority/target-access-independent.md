# Independent target-access and source-matching audit

Decision: **ACCEPT BD01, NG01, BT01–BT03 and GT01 at their stated literal-path scopes. ACCEPT MS01/MS02, FG01 and SC01 as scoped continuity limitations and conditional matching criteria.** The actual source-to-target theorem remains OPEN. A branch/entry-state qualification below is important when an earlier target hit precedes a later corner.

The ten original peer proof/receipt files were read in full and pinned before validation. The prescribed tests use the existing reviewer exact first-hit and full finite-wall path-check functions, not a separate numerical engine. The mathematical derivations below are independent hand checks, with the shared unfolding/fold foundations disclosed. This is internal AI review, not formal verification or external expert review.

## 1. Independent backward construction proves GT01 directly

Use the original integral ordered room with 0<a<l<w<A, 0<b<c<h<H, and actual integer target T=(t,v), l<t<A, 0<v<c. Let G=h-c, B=A-l, R=A-w, P=2*lcm(a,A,R,B), tau=P+epsilon and 0<epsilon<1/(2H).

It is clearest to start AT ACTUAL T and trace a reversed ray, rather than assume any original-source access. When a rectangular leg travels an integer vertical distance, the P part of its horizontal phase is a full period. At its next integer-height section only the epsilon drift remains. Between sections all ordinary vertical-wall bounces remain present. A true vertex could occur at a section/floor endpoint; the following strict bounds exclude those contacts.

**If l<t<w:** launch backward from T with positive horizontal velocity and either vertical sign. Its potential upward c contacts occur at the integer times

    D_(m,sigma)=2cm+c+sigma*v, sigma=-1,+1.

Before exiting to the right, the sampled slow x coordinate is t+epsilon*D. Select the first integer m for which this exceeds w. For each sign there is exactly one strict exit state with

    0 < epsilon*D_(m,sigma)-(w-t) < 2c*epsilon,

unless an exact alignment makes the exit x=w or the preceding contact x=w. Those are true reflex failures. The two alignment expressions differ by v/c, which lies strictly between zero and one. They cannot both be integers, so at least one vertical-sign choice has a strict exit. Positivity of w-t and 2c*epsilon<1 imply m is positive; no negative duration or free return count is used.

Every preceding c contact has x in (t,w), hence reflects on the genuine underside. Every floor contact is strictly between t and w+2c*epsilon, which is below A because 2c*epsilon<1<=R. None can reach the left corner x=l. Thus this is one exact corner-free trajectory from T to a strict upward c-mouth state. Extend backward through the real right strip to h. Its additional x displacement is G*epsilon, and the total excess beyond w is less than (2c+G)*epsilon=(h+c)*epsilon<1<=R. The h state is therefore strict. Reversing the whole path yields the required NEGATIVE/downward target-bound cap state, with the original target exact. There is no unknown S in this construction.

**If t=w:** the target is an ordinary interior bottom point, not the corner (w,c). The same backward launches leave through c immediately, with x=w+(c-v)*epsilon or w+(c+v)*epsilon. Their h positions are w+(h-v)*epsilon and w+(h+v)*epsilon. Both are strict and corner-free; no limiting argument is required.

**If w<t<A:** the integer margins t-w and A-t are at least one. For each physical forward horizontal sign eta=+/-1 and direct/floor duration F=h-v or h+v, use x_h=t-eta*F*epsilon. Every cap/c/floor section position differs from t by less than one and remains strictly in (w,A). Separate 2R and 2B period cancellation gives the same physical sign at the seam and actual T at the end. The original finite-wall continuation is ordinary throughout. These four sufficient states are not asserted to exhaust all right-target routes.

This independently proves GT01 for EVERY stated target and EVERY real epsilon in the stated interval. It is target-side access only, and does not assume a previously illuminated pair. Integral geometry and target coordinates are essential to the integer-time cancellation and unit margins; arbitrary real geometry is not covered.

## 2. Last-bottom necessity and complete gate relation

For a legal full ray stopped at its FIRST T with l<t<w, take its last downward bottom entry (x_e,c). Before T every upward c contact must reflect on the underside; otherwise another right-strip/cap passage would intervene. With m such reflections, the duration is D=2mc+c+sigma*v, strictly less than 2c(m+1).

The globally 1-Lipschitz triangular fold, together with integer D and 2B-period cancellation, gives

    w-t < x_e-t <= epsilon*D < 2c*epsilon*(m+1).

Therefore m>=floor((w-t)/(2c*epsilon)), including integral equality of the quotient. In particular m>=1 under epsilon<1/(2c). This proves BD01 independently of all earlier history.

A positive horizontal entry cannot have its first upward c contact on the underside: its forward folded distance to x=w is at least R, whereas the slow step is only Delta=2c*epsilon<1<=R. Thus its entry sign must be negative. Its first c contact is then x_e-Delta, giving the necessary strict gate w<x_e<w+Delta. This is NG01, including the smooth-wall convention at x_e=A, which cannot satisfy the thin gate.

Write r=x_e-l, y=t-l, W=w-l. The sampled unfolded phase is -r+epsilon*D'. Before the next right exit, ceiling samples move by Delta and cannot skip over the right window, since Delta<R. Thus the final target phase is one of -y,+y without an extra 2B winding. For each target-image sign kappa and vertical-arrival sign sigma,

    epsilon*(2mc+c+sigma*v)=r+kappa*y,
    0 < epsilon*(2mc+c+sigma*v)-(W+kappa*y) < Delta.

For fixed (kappa,sigma) the step in m is exactly Delta, so at most one m is admitted, and exact floor alignments admit none. The count is at most four signed entry states, with duplicates allowed.

The negative-image branches reach T before the slow phase crosses zero. All preceding underside/floor positions are strict and they are corner-free. The positive-image branches cross zero before the nominated target; they require r/(c*epsilon) not integral. Otherwise a genuine l-floor or l-underside corner occurs before that nominated visit. The ordinary finite-wall/corner guards in BT01–BT03 are sufficient and necessary for the specified literal episodes. The two safe negative-image alignment expressions cannot fail together, proving their pointwise nonemptiness as well.

### Earlier T versus an invalid later branch

Corner filtering applies to a nominated continuation, not automatically to the incoming state. An entry may share a safe earlier target branch and a corner-invalid later postturn branch. Keep the earlier legal hit. This is consistent with the peer packet's explicit earlier-T truncation and union of branches, but must be retained in any implementation or junction interpretation.

The eighth prescribed control demonstrates this exactly. In the old K1R01 room, epsilon=1/16 and x_h=225/8 with the negative/downward germ first reaches actual T=(24,2) at time66. Its continued trajectory reaches the corner (20,0) at time130, before its nominated later postturn target time194. My initial check incorrectly expected the whole ray to fail before any target; I corrected that expectation, retained the same prescribed ray, and verified its continuation from first T to the corner. This is not a counterexample to GT01 or the qualified literal-branch statements.

Likewise FG01's discussion of opposite-arrival-sign junctions must not be interpreted as deleting a state that already reaches T via the safe branch. Its monotonicity proof allows all branch lines, even before corner filtering, and therefore does not depend on that stronger interpretation.

## 3. Continuity and matching criteria

MS01 is valid for the two safe target families. Their distinct affine slopes have positive discrete separation; on a compact positive-epsilon interval only finitely many branches fit the thin gate. A continuous selector must keep one branch index locally, hence globally on the connected interval. No fixed m covers epsilon approaching zero. Pointwise access therefore supplies no global continuous selector.

FG01 validly extends this limitation to all four literal final-bottom families. In reciprocal coordinate z=1/epsilon the normalized entry coordinate q lies in (0,2c), on locally finitely many lines of slopes -(W-y) or -(W+y), both at most -(w-t)<0. Every continuous selection, including legal switches, obeys

    q(z2)-q(z1) <= -(w-t)*(z2-z1).

The open gate then implies (w-t)*(z2-z1)<2c for included endpoints. An open interval can have diameter EQUAL to the bound, so the peer's nonstrict diameter qualification is correct. This does not exclude an isolated rational match or disconnected parameter choices by the source.

MS02's whole-word source identity is also correct. For a fixed finite regular prefix ending at a negative/downward h-state, integer heights imply integer vertical duration D_S, and composition of actual wall reflections gives x_S=C-epsilon*D_S with integer C. A safe target branch is x_T=t+epsilon*D_T. Their unique possible root is (C-t)/(D_S+D_T), rational and admissible only inside BOTH strict physical guard domains. Native parity makes C and t even, but does not establish guard availability.

SC01 adds a valid sufficient width test without assuming target continuity. Put alpha=C-w>0, L=w-t>0. A regular source component J in z has q_S=alpha*z-D_S-G in (0,2c). Its target-matching phase

    Theta=(alpha+L)*z-D_S-G

must meet one of the two residue classes c-v or c+v modulo2c. The largest gap between these paired classes is M=2max(v,c-v). If (alpha+L)*length(J)>M, its OPEN image interval contains a matching level. The root is rational, has m>=1, and both velocity signs and every prefix/tail guard agree. Equality alone is insufficient. A source word legal across its entire geometric gate satisfies the condition, indeed each individual target-arrival residue class is then met.

Under actual darkness every such source component must consequently have length at most M/(alpha+L), and its normalized q span is strictly less than M. These are valid necessary constraints, not a proof that a sufficiently wide source component exists. They cannot be summed into a corner bound without controlling repeated images and component overlaps.

## 4. Exact corroboration and source-side limitation

The EIGHT predeclared controls in the single old K1R01 room all pass the qualified expectations: two missing-alignment alternatives, an ordinary safe branch, the t=w case, both signs for a right-side target, a legal postturn branch, and the earlier-target/later-corner coincidence described above. The checker retains exact earliest-wall, corner, specular-law and full-segment guards under a genuine y-reflection. The old one-roof-only assertion is omitted because these paths intentionally have repeated floors. No new room or sampled direction family is used. The universal statements above rest on hand arguments, not eight samples.

The peer's new SG01 source-word example is separately tested by the SAME already accepted K1R01 ray. The coordinator check reconstructs its final negative cap state and ONE prescribed earlier-reflex image; it does not claim to independently reproduce a complete maximal-interval classification. The resulting upper bound is already enough to refute automatic width of that selected source word. Details and exact evidence are in target-access-source-cut-check.json.

The known prefix has D_S=3364, C=56, alpha=28 and q=28z-3365. Its geometric gate is z in (3365/28,3371/28). The predeclared earlier corner is physical (28,4), developed (461596,2408), at developed time2404 and z=601/5. It lies inside the nominated traversed-copy time interval at that parameter. If the fixed word were regular there, its segment would hit that true corner; if it failed earlier, it is already outside the same regular component. Either way the connected component through z0=1923/16 cannot extend across this parameter. Thus its matching phase span is at most

    32*(601/5-3365/28)=24/35 < M=4.

The sufficient SC01 width condition therefore fails for THIS successful prefix, although its particular matching root Theta=481 is valid. No different source word is excluded. This accepts SG01's selected-word limitation; the exact equality of its claimed maximal component to that interval is not needed for this independent conclusion and is not independently certified merely from one selected cut.

## 5. Final scope

**Positive accepted step:** every native bottom target has an exact legal target-bound cap state at every stated small epsilon, without assuming prior illumination. This is stronger than the earlier conditional twist normalization.

**Remaining gap:** for each unknown residual actual S,T, produce a source prefix meeting one of those states at the SAME epsilon, position and signed velocity, inside all true-corner guards. SC01 gives a sufficient quantitative source condition; its universal availability is unproved, and SG01 rules out assuming it for an arbitrary chosen successful prefix.

No new full room family, all-ordered proof, all-r3 proof, r<=8 proof, actual dark counterexample is supplied. Existing agent/native goal identities, accounting and clocks were not changed by this coordinator audit. Frozen peer proofs were not edited.

## FT01 reciprocal qualification

The subsequently delivered peer supplement `review/three-reflex-two-sided-first-target-qualification.md/.json` was read in full. Its independent junction algebra agrees: equality of preturn/postturn cap positions gives epsilon*(D_plus-D_minus)=2(t-l)>0. The safe visit precedes the slow left turn, which precedes the nominated postturn visit. At an opposite-arrival-sign junction the middle event is a true corner, but it is after the safe actual T. Accept FT01's qualification that a continuous parameter-STATE selection can pass through this successful shared state, while its later itinerary is invalid. Retain FG01's main all-four-line horizon bound and GT01/SC01. The earlier-T issue is reconciled without modifying any frozen source.
