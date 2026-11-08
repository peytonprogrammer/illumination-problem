# A supporting-line formulation of the sign theorem

[done] General algebraic lemmas and one exact frozen-data control.
[waiting on Claude] Independent mathematical review requested.
The positivity theorem remains open.

## 1. Eliminate artificial independence of corner motion

Fix a strictly simple polygon's cyclic wall directions, with no consecutive parallel walls. Choose a fixed normal n_i for each wall and write its supporting line as n_i dot x=h_i. The adjacent-normal matrices are invertible. In a neighborhood of the base polygon its vertices are exactly

    c_i=B_i h,
    n_(i-1) dot c_i=h_(i-1), n_i dot c_i=h_i.

The matrices B_i are constant. Reflection words and their admissible side continuations are fixed when interpreting the affine formulas optically; the algebra by itself does not make an arbitrary word a valid event. Positivity of wall lengths and absence of nonincident contacts are open conditions, so (h,s,t) is a local chart of dimension W+4. It has no closure constraint: intersecting the cyclic supporting lines closes the polygon automatically. This is equivalent to the earlier W+6 edge-length/mark chart with two closure equations. The corner is no longer an independent variable.

Reflection in wall i has fixed linear part and offset-linear translation:

    r_i(x)=R_i x+b_i(h),
    R_i=Id-2 n_i n_i^T/|n_i|^2,
    b_i(h)=2h_i n_i/|n_i|^2.

Let a fixed one-corner event have wall word i_1,...,i_m. Define prefix maps

    F_j(x)=O_j x+B_j(h), O_0=Id, B_0=0,
    O_j=O_(j-1) R_(i_j),
    B_j=B_(j-1)+O_(j-1)b_(i_j).

These maps are affine in h, not approximations.

Choose r from the actual first corner-contact position in the replayed word. The actual developed corner affine form, not merely a coincidental equality at the base point, determines the split. The checker now records that actual contact and verifies its affine form under the old/new chart pullback. Alternative base-coincident split positions are recorded separately from affine-equivalent ones. Put

    C(h,s)=F_r(c)-s,
    A(h,s,t)=F_m(t)-s.

At the parity event, A=2w and C=w for primitive nonzero w. The exported signed functional is f=sigma det(A,C). Its derivative is

    g(delta)=sigma det(w,delta E), E=2C-A.

This uses the previously audited exported-side convention in ../isolation-review/findings.md §4 and the established one-corner lit-side implication; it does not derive that implication anew.

## 2. Exact first-half-minus-second-half wall identity

Expanding the prefix shifts gives

    E=2O_r c-O_m t-s
       + sum_(j<=r) O_(j-1)b_(i_j)
       - sum_(j>r) O_(j-1)b_(i_j).

The common prefix of the full target map is present twice in the corner image and once in the target image, leaving coefficient +1. The suffix appears only in the target image, leaving -1. Thus the identity follows directly from the affine prefix recurrence.

For wall-hit j let epsilon_j be +1 before the split and -1 after it. Its contribution to the scalar event row is

    sigma * 2 epsilon_j det(w,O_(j-1)n_(i_j))/|n_(i_j)|^2 * delta h_(i_j).

The explicit corner contribution becomes a load on its TWO incident wall offsets by substituting c=B_c h. The remaining mark terms are -sigma det(w,delta s) and -sigma det(w,O_m delta t).

This is the complete coupling in one chart. It does not permit independently varying c while freezing its incident walls. The separate local and wall contributions depend on the split convention: moving r past a reflection incident to c can transfer a term between them. Only their sum is intrinsic to this event row. All numerical split values below use the actual first-contact convention.

If n_i=J d_i for a primitive wall tangent d_i and v_j=O_(j-1)^T w, orthogonality gives

    det(w,O_(j-1)n_i)=det(O_(j-1)) dot(v_j,d_i).

So the wall-load sign involves the tangential velocity and reflection parity. It is not an unsigned incidence count. The +/− split at the corner adds another sign. There is no immediate local positivity principle in this formula.

## 3. Paired-side cancellation lemma

Consider two admissible events at the same incoming primitive direction w, opposite exported sides +1/-1, and the SAME developed corner affine form C. This common-form hypothesis holds when the events share their pre-corner itinerary; incident reflections at c fix c identically and may be moved across the split without changing its image.

Let their developed target differences be A_+, A_-. Then

    g_+ + g_- = det(w,delta(A_- - A_+)).

Proof: g_+=det(w,2delta C-delta A_+) and g_-=-det(w,2delta C-delta A_-). Add them. The explicit corner term, source term, and common pre-corner shift cancel. What remains compares two target-image continuations after the corner. Wall offsets in the two suffixes still matter; the cancellation does not erase them.

The sum uses positive coefficients, so it is a valid consequence of the original two LINEARIZED darkness inequalities. A negative paired sum forces at least one original event negative. It is therefore a useful sufficient obstruction, not a replacement for every original event.

These paired loop rows have zero source-coordinate coefficients and are invariant under translating the room and target together, while leaving the source independent. They also annihilate uniform scale of the room and target. Hence in the W+4 chart they have at least five independent kernel directions (two source motions, two room-plus-target translations, one room-plus-target scaling), giving rank at most W-1. The full sign theorem needs rank W+1 modulo actual family symmetries for a room with diagonal walls. Paired loops alone necessarily lose at least two needed dimensions.

This rank bound is structural, not a sampling claim. It prevents mistaking the cancellation lemma itself for a complete positivity argument.

## 4. Exact control: why the diagonal can matter

An axis row means an event whose physical corner is at coordinate distance (plus-or-minus1,0) or (0,plus-or-minus1) from either mark. The frozen room parity-W25-24 has 25 walls and 167 supplied event rows. All167 replay with their supplied direction and side; the new offset-chart rows pull back EXACTLY to the previously exported rows modulo the old closure equations. They annihilate the two translations and uniform scale exactly.

An LP proposes a normalized deformation; exact active-equation reconstruction then verifies it with fractions. The source is fixed, total primitive wall length has zero variation, and the target moves by (0,1/13). All102SAVEDaxis-corner rows are nonnegative:94zero and8strictlypositive. This is a tangent-cone control for the saved subset, not a dark deformation or an exhaustive statement about all possible axis events.

Fifteen saved rows are negative in total; six are at the previously identified diagonal repair corner (1,3). For example:

| Incoming direction | Side | Local corner-and-mark value | Wall-hit value | Coupled value |
|---|---:|---:|---:|---:|
|(-5,-11)|+1|132/13|-145/13|-1|
|(7,-3)|+1|83/13|-96/13|-1|
|(7,-3)|-1|-69/13|-9/13|-6|

With the stated split convention, the first two would point the wrong way if the wall terms were discarded. The (7,-3) pair has total -7; its explicit corner/source/common-prefix terms cancel by Lemma3, so its negative obstruction is also a target-image loop obstruction.

There are19opposite-side pairs in this saved packet. All19satisfy the exact cancellation identity. Their loop rows have exact rank17, below the structural maximum24 and below the full-event rank26. A floating LP finds no strictly positive dependence for these19rows; this numerical observation is not used as a proof. The rank deficit alone proves the saved paired loops cannot supply the full certificate.

## 5. A complete ear-mode explanation in this fixed packet

The exact dual control simplifies after subtracting uniform scale about the source and rescaling. Its only nonzero wall offsets are

    delta h_5=2, delta h_6=-1.

Its only moving vertices are

    (1,3) -> displacement (0,2),
    (2,4) -> displacement (-1,1),
    (1,4) -> displacement (0,1).

Both marks and all eight axis corners remain fixed. This changes a single triangular protrusion; the description is in the deformation chart and does not claim the deformed room stays dark.

For the94axis rows zero on this mode, the checker constructs STRICTLY POSITIVE rational weights whose weighted row sum is exactly zero, and verifies exact rank25. Their common kernel therefore has dimension4: the three true symmetry directions plus this one ear mode eta. Any deformation satisfying all102savedaxis inequalities must make each of the94zero-stress rows vanish. It thus belongs to that kernel. The other8axis rows evaluate positively on eta (values10,18,6,14,16,10,22,24), forcing its coefficient to be nonnegative.

Consequently the ENTIRE linearized cone of the saved102axis rows, modulo symmetries, is exactly the nonnegative ray generated by this ear motion. This is stronger than checking one LP-proposed direction.

The single saved diagonal event at c=(1,3), direction(-5,-11), side+1, has value-2 on eta. Adding it forces the ear coefficient to be nonpositive as well, hence zero. Thus one diagonal EVENT, not all events at a diagonal corner, completes the saved axis cone in this room.

The positive balance can be constructed explicitly. Take one positive-axis row a and the negative-diagonal row d. Set alpha=-g_d(eta)>0 and beta=g_a(eta)>0. Then H=alpha*g_a+beta*g_d annihilates eta and all symmetries, so lies in the span of the94zero rows. Express -H in those rows with signed coefficients. Add a sufficiently large multiple of their strictly positive zero stress to make every coefficient positive. The result is a96-row strictly positive rational balance of exact rank26, all checked in ear-control.json.

This is an exact finite certificate for the chosen room and saved packet. The subsequent frozen34-room audit RULES OUT extrapolating this literal ear geometry to all holdouts. Only one of the26one-dimensional saved cones is this triangular-ear mode; eight other holdouts have full-dimensional saved cones. It does NOT establish that unsaved axis events permit any of these motions.

## 6. Precise remaining theorem

After substituting the coupled corner terms into wall offsets, prove that actual admissible event rows generate all dual directions modulo the actual symmetry kernel. A sufficient finite form is full quotient rank plus strictly positive weights lambda_e with

    sum_e lambda_e g_e=0.

That weighted identity must balance each wall offset and each mark coordinate. It cannot be obtained from a cancellation that discards the wall suffixes or the needed mark directions.

For an infinite event family, the exact target remains: every nonsymmetry delta has some admissible g_e(delta)<0. Strict negativity gives an open cover of the unit quotient sphere and hence a finite subcover, PROVIDED the one-corner illumination implication persists locally. The algebra above supplies no such global signed balance by itself.

Next proof target: identify a reversible or cycle-balance construction that combines target-image loop constraints with the missing mark-control directions, using actual admissible continuations. The example above is a fixed exact test any proposed balance must explain. No new ray search is justified merely by this reformulation.

## Scope

All geometric statements concern a fixed cyclic direction family near a strictly simple base room. No arbitrary-angle isolation, all-parity-room positivity, extension to the non-parity22construction, or degeneration exclusion is claimed. The8-axis-plus1diagonal conjecture remains an observed finite-family pattern.

## 7. A stronger finite pattern: one diagonal event suffices

The exact holdout audit in ear-family.json separates the34previously frozen cases into26one-dimensional axis cones and8full-dimensional axis cones, after quotienting translations and scale. The eight full-dimensional cases have W=26, so their quotient dimension is27. A strictly feasible rational vector proves that every saved axis inequality can be strict there. This is a finite-packet statement: an omitted axis event could change that cone.

The displacement class does not entirely explain the split:

| Mark displacement up to D4 | One-dimensional saved cone | Full-dimensional saved cone |
|---|---:|---:|
|(0,4)|23|0|
|(2,4)|3|8|

repair-structure.json gives a strictly positive rational stress on ALL saved axis rows plus ONE saved diagonal event in EACH of the34cases. Each augmented packet has exact rank W+1. repair-verify.py independently checks those balances and ranks directly in the original W+6length chart, modulo its two closure covectors; it does not use the supporting-line conversion or an LP.

This strengthens the earlier empirical statement, which allowed all events at one diagonal corner. Here a diagonal event means a midpoint event whose physical corner differs from a mark by (plus-or-minus1,plus-or-minus1). It does not extend the327-room census or prove a general geometric statement.

## 8. The one-event repair lemma

Let V be the room deformation space after quotienting its true symmetry kernel. Let a_1,...,a_m be the saved axis covectors and d one diagonal event covector. Suppose a_i span V*, and there exist strictly positive rational numbers lambda_i and mu such that

    sum_i lambda_i a_i + mu d = 0.

Then d is strictly negative on every nonzero vector of the axis cone C={v:a_i(v)>=0 for all i}.

Proof. If v is nonzero, full rank makes some a_i(v) nonzero. Inside C, at least one is therefore strictly positive, so

    d(v)=-(1/mu) sum_i lambda_i a_i(v)<0.

Consequently C intersect {d>=0}={0}. This does not depend on the dimension of C. Conversely, for a FINITE axis family, if C is pointed and d<0 on C minus {0}, then -d lies in the interior of cone{a_i}; it can be written using strictly positive coefficients on all a_i. One justification: negativity is uniform on the compact set C intersect the unit sphere, so -d has an open dual-cone neighborhood. Subtract a sufficiently small positive multiple of sum_i a_i and remain in the dual cone, then use the finite cone's duality representation. This converse is elementary polyhedral duality, not a new billiard theorem.

The34stored certificates verify the forward lemma's hypotheses. Their full augmented rank and positive balance also imply axis rank W+1, because the balance expresses d in the axis span. Thus one diagonal event opposes ALL saved-axis-feasible nonsymmetry motions in each case, including each27-dimensional cone. It is not merely negative on the particular LP direction used to discover it.

Adding further valid events cannot invalidate these positive-span certificates. In particular, each of these34rooms already satisfies the full linearized sign statement, conditional on the saved rows' optical validity. Its full axis family has no additional kernel, and its feasible cone is a subset of the saved one, so the same single diagonal event still cuts it. Only the precise26/8axis-cone classification can change when more axis events are included.

## 9. Lift balances through a forced-zero face

There is a general version of the ear construction. Let Z be a set of covectors with a strictly positive zero stress. Put K=intersection_(z in Z) ker z. Any vector satisfying z(v)>=0 for all z in Z lies in K, since their positive weighted sum vanishes.

Suppose additional rows r_j, restricted to K, have a strictly positive zero stress nu_j, and their common kernel in K is exactly the true symmetry kernel. Then the complete rows admit a strictly positive zero stress with that same kernel.

Proof. H=sum_j nu_j r_j vanishes on K, hence belongs to span Z. Express -H=sum_z beta_z z with signed coefficients beta_z. Add a sufficiently large multiple of Z's strictly positive zero stress to the beta coefficients to make them all positive. The resulting balance is exact and positive on all rows. Its common kernel is the stated symmetry kernel by the hypothesis on K. Section5 is the one-dimensional quotient case of this lifting lemma.

This reduces26finite holdouts to a one-dimensional sign check. It supplies no such reduction for the other eight: their saved axis rows have no forced-zero face at all.

## 10. Sharpened open geometric target

The evidence now suggests trying to prove the following two statements for the full admissible axis family in an arbitrary parity room:

1. Characterize its common kernel and feasible cone; the finite packets suggest that the kernel is exactly the true family symmetry kernel.
2. For each nonsymmetry motion in that cone, construct an admissible non-axis midpoint event that is strictly negative on that motion. The event may depend on the motion. Compactness would then give a finite covering family.

The second statement would prove the sign theorem, regardless of whether the axis cone is a ray or has interior. An independent rank theorem is useful but is not necessary for this covering argument. Neither the suggested general kernel description nor the geometric event construction is proved. The finite calculations identify witnesses, not a method to construct an admissible event from the room geometry. That construction must explain the coupled wall loads from Section2; naming a dual cone does not solve it.

The single-event target is STRONGER than the sign theorem needs. For an elementary algebraic control, take axis rows (1,0),(0,1) and two additional rows (-1,0),(0,-1). Together they positively span the plane, with all four weights equal to1. Each additional row alone leaves an axis ray. Thus positive spanning by all diagonal events does not logically guarantee a single repairing event. This is not a polygon counterexample; it prevents treating the finite single-event pattern as an automatic consequence of the desired theorem. If geometry requires several diagonal events in larger rooms, the original sign theorem and face-lifting strategy remain viable.

The next structural task is to characterize geometric event covectors that cover the remaining axis cone. The single-event negative-dual-interior condition is a useful stronger pattern to test, not a required premise. The literal triangular-ear test and the universally one-dimensional explanation fail for the saved family; a broader local-wall-patch description has not been excluded.

## 11. Corner-frame midpoint identity

This identity was suggested in the second independent Opus review and re-derived here. It is algebraic; it supplies no new sign or existence claim.

Use the actual corner-contact split from Section1. Write the prefix as Phi(x)=O x+b, and factor the target development as F_m=Phi composed with Psi. Define two unfolded mark images in the corner's physical coordinate frame:

    S'=Phi^(-1)(s), T'=Psi(t), w_c=O^T w.

The definitions include all their wall-offset dependence. Since s=Phi(S') and F_m(t)=Phi(T'),

    E=2Phi(c)-Phi(T')-Phi(S')
     =O(2c-T'-S').

The prefix translations cancel exactly. O is constant in a fixed-direction family. Therefore

    g(delta)=sigma det(O) det(w_c,2delta c-delta S'-delta T').

At the base point c-S'=T'-c=w_c: the physical corner lies at the midpoint of the chord joining these two unfolded mark images. The functional measures its first-order transverse drift relative to that chord.

This is independent of moving an incident reflection across the split. If that reflection is r(x)=R x+q(h), then r(c)=c identically. The new prefix is Phi composed with r and the new suffix is r composed with Psi; consequently both S' and T' become r(S') and r(T'), and

    2c-r(S')-r(T')=R(2c-S'-T').

The new prefix linear part OR absorbs this R, leaving E unchanged because R squared is the identity.

Unlike an isolated local-corner term, this chord-drift expression is invariant under that split choice. It is NOT local in its wall dependence: both S' and T' depend on their entire unfolding words. A proof via chord drift must control those global dependencies, rather than freeze the unfolded mark images while moving the corner.
