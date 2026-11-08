# A finite witness propagates along a rational two-neck length ray

Candidate A21, Codex01a18403. Independent review pending. This is an exact actual-endpoint propagation lemma, not a uniform W bound or a proof that the residual arithmetic rays contain an illuminated room.

## 1. Statement

Fix the three orthogonal chambers, two horizontal necks of the SAME positive width w, and opposing actual interior marks S,T of the accepted A18 family. The two mouths may use distinct fixed vertical origins. All chamber and mark data are fixed. Let

    L1(lambda)=p1*lambda+c1,
    L2(lambda)=p2*lambda+c2,

where p1,p2 are nonnegative integers, not both zero. Consider the final interval of real lambda for which both lengths are positive and the prescribed gluing is strictly simple. A common positive change of parameter covers rational nonnegative growth rates as well.

Suppose that at ONE parameter lambda0 in that interval there is a legal finite specular S-to-T path avoiding all genuine polygon corners. Then there is lambda_star such that EVERY real lambda>lambda_star in the family has an actual finite corner-avoiding S-to-T path.

The original witness may revisit any chamber or either neck any finite number of times. No bound on its reflections or portal passages is imposed. This is stronger than requiring a one-pass witness. The new path retains a fixed finite itinerary INSIDE the fixed chambers, while neck reflection counts may grow.

Consequently an unbounded sequence of dark parameters on such a ray would imply that EVERY valid parameter on that ray is dark: any one illuminated parameter would give the eventual contradiction. This conclusion stays within the fixed family and does not assert that any dark ray exists.

## 2. Fix artificial cuts away from smooth seam contacts

The original witness is forbidden to touch genuine corners, but it may legally reflect at a smooth point that is an endpoint of an artificial mouth cut. Such a contact must not be treated as an open portal crossing.

Its horizontal velocity has nonzero magnitude. In an orthogonal room reflections change only its signs. A path connecting the opposing outer chambers necessarily has nonzero horizontal velocity throughout.

Choose a fixed small positive buffer length e with 2e<min(L1(lambda0),L2(lambda0)). Move both cuts of each neck inward by e, absorbing the short width-w end rectangles into the adjacent fixed chambers. Choose e to avoid all finitely many horizontal coordinates of the witness's neck reflections relative to either end. There are only finitely many forbidden values of e. Thus every crossing of a NEW cut is strictly inside its width-w opening, not at its top or bottom endpoint. The source and target remain in the enlarged fixed chambers.

The new neck lengths are Lj(lambda)-2e. Their growth coefficients remain pj; all enlarged chambers and cuts are fixed as lambda varies. For lambda>=lambda0 all lengths are positive because pj>=0. This is a repartition of the SAME physical rooms and trajectories. It adds no physical mirror, reflection or forbidden corner. Equal widths are preserved. The buffer can be nonrational; the proof only uses that the growth coefficients pj are integers.

Every new neck visit is a complete traversal. Its horizontal velocity cannot reverse in the neck, whose actual walls there are horizontal. Entering through one end therefore reaches the other before any return. The witness crosses the cuts only finitely many times.

## 3. Fixed chamber blocks and affine developed distances

Partition the buffered witness into its initial chamber block, its finite sequence of complete neck traversals and intermediate chamber blocks, and its terminal chamber block. Record every reflection word inside a chamber. Intermediate blocks may enter and leave the same mouth. Each is a finite nonsingular word with strict transverse portal coordinates. Its local input/output map is continuous on an open neighborhood of the witnessed slope and phase, and preserves its word, corner avoidance and next-mouth ordering there. The initial block is stable as a function of the direction from the ACTUAL S. Treat the terminal block backwards from the ACTUAL T; its required mouth position and direction vary continuously with slope.

Unfold with the initial horizontal velocity positive and normalized to1; let tau0 be the signed vertical slope of the witness. Every chamber reflection matrix is diagonal with entries +/-1. Every full neck traversal contributes its positive physical length to the developed horizontal displacement, independently of how many times it reflects at its horizontal walls.

For each designated portal crossing i, the cumulative developed horizontal displacement has the form

    X_i(lambda)=r_i*lambda+d_i,

and the developed target abscissa has the form

    D(lambda)=q*lambda+C.

Here r_i are nonnegative INTEGERS: they sum pj over neck passages already completed. The constants d_i include the fixed developed distances inside the recorded chamber blocks, the offsets cj and buffers. Similarly

    q=n1*p1+n2*p2 > 0,

where nj is the total number of complete traversals of neck j in the witness. Both nj are positive because the endpoints lie in opposing end chambers. Therefore q is a positive integer and D(lambda) tends to infinity. All these quantities are independent of slope within the fixed chamber words. The developed distance of a chamber block is determined by its vertical supporting lines and fixed reflection word, including same-mouth returns; its horizontal speed in the unfolding is constant1.

## 4. Fixed vertical charts modulo the COMMON period

Take the developed source to be (0,alpha). The fixed chamber words have fixed vertical translations and fixed vertical reflection signs. Moving or enlarging the necks changes horizontal positions only. An unfolded neck copy has vertical displacement an integer multiple of 2w, with its fold sign selected by the portal phase. Composing fixed chamber charts may negate such a displacement, but still gives an integer multiple of 2w.

Consequently there is a fixed base target ordinate B and a witnessed integer N0 such that

    alpha+tau0*D(lambda0)=B+2w*N0.                  (T0)

For each portal crossing i there is likewise a fixed base chart ordinate beta_i and a witnessed fixed derivative sign epsilon_i in {+1,-1}. Its local physical coordinate and orientation are determined by

    epsilon_i*(alpha+tau*X_i(lambda)-beta_i) modulo 2w.

At the witness this phase lies strictly inside the correct one of the two folded half-periods, because of Section 2. The integer translation of the particular copy is irrelevant to this local phase, but its sign is NOT erased. All fixed intermediate chamber chart compositions are taken with the witnessed signs.

This modulo statement does not replace the actual target. The final actual-target image will be imposed by an equality in Section 5. Every chamber map is one of the actual finite witnessed words; only the neck periods vary.

## 5. A single congruence preserves every intermediate phase

For a larger lambda choose a target-image integer N with

    N=N0 modulo q,
    tau_N=(B-alpha+2w*N)/D(lambda).

Choose the nearest such integer to the value making tau_N=tau0. The slope spacing is 2wq/D(lambda), so

    |tau_N-tau0| <= wq/D(lambda).                  (E)

For each crossing write e_i=d_i-r_i*C/q. The exact identity

    tau_N*X_i(lambda)
      =(r_i/q)*(B-alpha+2w*N)+e_i*tau_N

gives, after subtracting the witnessed identity at lambda0,

    tau_N*X_i(lambda)-tau0*X_i(lambda0)
      =2w*r_i*(N-N0)/q+e_i*(tau_N-tau0).          (P)

The first term is an INTEGER multiple of 2w, simultaneously for EVERY i. Therefore each local portal phase approaches its witnessed phase as tau_N tends to tau0. No independent phase adjustment at any intermediate mouth is made.

There are only finitely many chamber blocks and crossing phases. Choose a positive tolerance eta so that |tau-tau0|<eta, together with phase changes epsilon_i*e_i*(tau-tau0), stays inside all their witnessed open guards. Those guards include the correct fold signs, transverse first-mouth contacts and every genuine corner exclusion. Equation (E) ensures them all once D(lambda)>wq/eta. Each neck connects its selected actual entrance and exit by the straight unfolded segment, with finitely many smooth horizontal-wall reflections, since its physical length and chosen finite slope are finite.

Proceed along the witnessed block itinerary. Induction gives the actual initial block, each neck fold and each intermediate chamber block with the recorded signs and phases. Thus all designated local charts used in (P) are realized, rather than merely postulated.

## 6. Exact final actual-target match

By construction the developed endpoint is EXACTLY

    (D(lambda), B+2w*N).

The terminal block is the backward word from the actual T. Let its fixed developed horizontal extent be b>0 and write its actual incoming mouth ordinate as y_T(tau), a continuous affine function of slope on the witnessed interval. The required developed height at its mouth is B+2w*N-b*tau.

The forward-reconstructed final mouth has the same height modulo 2w, in the same fixed half-period branch. The reconstructed physical mouth ordinate and y_T(tau_N) both lie strictly inside (0,w). Two such ordinates in the same branch cannot differ by a nonzero integer multiple of 2w. They are therefore equal, with the correct velocity sign. This realizes the backward terminal word to the ACTUAL T exactly. Equivalently its reconstructed period index must equal N; a discrepancy would require a local-coordinate difference of magnitude at least2w inside an interval of width w.

All segments avoid genuine corners by the finite guards. Additional earlier visits to S or T are harmless: paths may revisit interior points, and any earlier T arrival can be truncated. No new path is permitted to reflect at an artificial cap.

This proves eventual illumination for every sufficiently large real lambda from the one supplied witness. The proof also permits tau0=0: the strict portal guards persist near it, and a zero chosen slope has no horizontal-wall reflections. The only essential nonzero velocity component is horizontal, already forced by the endpoints.

## 7. Relevance and exact limits

A19 confines potential long equal-width failures, for fixed integer chamber data, to finitely many integer-affine length rays. A21 would make ONE exact illuminating certificate anywhere on each ray sufficient for eventual illumination on that ray, even if it uses repeated neck passages. It does NOT supply those certificates, any uniform threshold, or the remaining finite small-parameter checks. Nor does it prove that the first room of each ray falls under the accepted k<=6 baseline.

The common period 2w is essential to the simultaneous congruence used here. Arbitrary unequal widths, changing chamber geometry or marks, shrinking widths, diagonal chambers and arbitrary polygon decompositions are not covered. There is no W-only bound on q, the witness itinerary or eta. No ray/direction/word search or numerical sampling has been performed. Independent review must check the buffering, fixed chart induction and exact final lift; this remains a candidate until accepted. Full cap-free canonical45 W<=21 illumination remains OPEN.
