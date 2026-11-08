# Independent two-sided-return review

Decision: **ACCEPT A, B, their conditional combination, and the prescribed fixed-ray replay at the stated scopes.** No material correction to the packet is needed. The general ordered/r3/r<=8 illumination goals remain OPEN. This is one bounded review; the existing native goal was observed BLOCKED and was not resumed, replaced, completed or reset.

The request, test/proofs and checker/evidence were read in full. I independently checked A/B by hand, read the accepted WR01 proof and independent review, and reread the original LR01 overshoot and K1R01 four-reflection witness. The prescribed exact replay reused the existing reviewer geometry and earliest-wall functions, with only their old single-roof scope assertion omitted. No coordinator checker, historical main block, discovery code, direction scan, new room, worker or engine was run. Shared proof and computational dependencies are disclosed below.

## A — ACCEPT: endpoint-fixing normalization conditional on an existing ray

For a generic horizontal height, the ordered room has components of widths B=A-l, a, R=A-w or A. Moving horizontally in the four-copy unfolding crosses each physical component and its reflected copy before returning to the same sheet/germ. Its unit-row cycle length is twice the component width. The possible lengths therefore divide

    P = 2*lcm(a,A,R,B).

For a generic vertical column, the physical components have heights H-b, beta=H-h, c or H. For l<x<w there are TWO separate components, of heights c and beta; they cannot be replaced by their combined height. Their doubled lengths divide

    Q = 2*lcm(H-b,beta,c,H).

All boundaries and these lengths are integral. Thus the row/column permutation orders divide P/Q. This does not assume that every maximal geometric cylinder has height one. Accepted WR01 constructs the affine maps on unit rows/columns, fixing their boundaries pointwise and extending with a global inverse across seams and cone stars. Taking the appropriate integer powers yields H_P and V_Q, fixing the ENTIRE integer-vertex fiber pointwise. In particular every actual source lift, target lift and forbidden corner lift is fixed, and the inverse forbidden sets agree exactly.

Applying either map to the WHOLE unfolded segment preserves its selected actual endpoints and legality. Refolding reconstructs a possibly different physical wall word. It would be wrong to shear a Euclidean vector while copying the old reflection itinerary, or to concatenate differently directed pieces. The packet does neither.

To check signs, first select the initial source copy as the canonical physical chart; the four-copy symmetry permits that selection for any existing actual ray. Its nonzero developed displacement is an integer vector, so use an integer direction (p,q). A horizontal ray cannot connect these terminal marks: if u!=v the heights differ; if u=v, then b<u=v<c and the source and target lie in distinct horizontal components (0,a) and (l,A). Hence q!=0. Choose an integer k with p0=p+kPq>0. After H_P^k, then V_Q^n, then H_P, the derivative gives

    q_n = q+nQp0,
    w_n = (p0+Pq_n, q_n),
    tau_n = P+p0/q_n.

For sufficiently large positive n, q_n>0, so the actual source signs in that chart are (+,+), epsilon_n=p0/q_n>0, and epsilon_n tends to zero. All maps still fix the chosen source and target points on the surface. This proves that every ALREADY-LIT terminal pair has successful full paths arbitrarily close to P from above. It gives no starting path for an unknown pair, no universal existence implication, and no success at epsilon=0.

## B — ACCEPT: all first-N physical circuits and target-height guards

Assume a legal native-source ray with tau=P+epsilon reaches its FIRST downward R mouth. Earlier corner failure would disqualify that ray. LR01 gives the initial actual state

    (w+rho,h), vx=+tau, vy=-1,
    0<rho<2beta*epsilon.

This includes either source horizontal sign and lower/mouth/upper terminal placement. In the upper case the initial descending h phase is still in L under the smallness bound, so a direct initial R entry is not silently substituted. Before the first R entry the ray cannot reach the bottom target.

Here is the independent fold calculation used for every subsequent leg. In a real strip [L,L+W], start on its positive horizontal branch at x and travel an INTEGER vertical distance z. Because P is a multiple of 2W, the endpoint phase x-L+z(P+epsilon) reduces to x-L+z*epsilon modulo 2W. If that residual stays strictly between 0 and W, the actual endpoint is x+z*epsilon and its horizontal velocity is again positive. This conclusion includes all intervening ordinary vertical reflections; it does not remove them from the physical trajectory.

Apply this successively to the actual right, bottom, right and cap strips. From the j-th downward R entry x=w+rho+2Hj*epsilon, the successive offsets from that entry at c down, floor 0, c up, h up, roof H, and h down are respectively

    G*epsilon, h*epsilon, (h+c)*epsilon,
    2h*epsilon, (h+H)*epsilon, 2H*epsilon.

Thus the next downward R entry has the claimed offset rho+2H(j+1)*epsilon. For 0<=j<N every offset from w is positive and at most rho+2HN*epsilon, strictly less than one under epsilon<1/(2beta+2HN). Since R is a positive integer, all listed events lie strictly in (w,A), including the R mouth, bottom-floor interior and outer-roof interior. They avoid x=w,A at all relevant strip endpoints. The c-up event is in the open right mouth, not on its closed underside; the h-down event is in R, not on the genuine shelf. No artificial horizontal mirror is used.

Between those events, the right strip has only its true vertical walls w,A; the bottom strip only l,A; and the cap only 0,A. A collision with a vertical-wall endpoint could occur only at one of the section/floor/roof heights, where the strict formulas already exclude it. Other integer heights introduce no hidden corner: in particular b has no bottom-chamber corner at l or A. The finite walls, all ordinary vertical bounces, both horizontal velocity signs along the intervening legs, and the matched positive outgoing signs at every section are therefore accounted for. The only horizontal reflections in these N circuits are the real floor and roof.

At target height v, the downward/upward bottom coordinates are

    w+rho+(2Hj+h-v)*epsilon,
    w+rho+(2Hj+h+v)*epsilon.

Their coefficients lie between 0 and 2HN for j<N because 0<v<c<h<H. Both coordinates are strictly in (w,w+1). Every native t is integral, so neither can be actual T. This is an actual physical induction, not extrapolation of the stopped first-R formula. It is conditional on reaching a legal first R state; it does not prove that state is available for an unknown pair.

## A+B — ACCEPT the quantifiers; no minimum over all slopes

For any already illuminated terminal pair and any N, A supplies a successful tau_n with epsilon_n satisfying B. That full path must reach the bottom target eventually, while B proves its first N full right-floor-cap circuits legal and target-free. Hence successful near-P directions exist with arbitrarily large right-return depth. This does not mean the pair needs arbitrarily many returns across ALL directions. The K1R01 pair retains its original four-reflection ray.

The conclusion also sharpens the limitation correctly: LR01 excludes its stopped first-R/tail class, not every complete near-period trajectory. Adding any FIXED number of right circuits cannot uniformly repair the near-period strategy. This is a mechanism limitation plus conditional normalization, not new general illumination coverage.

## Prescribed K1R01 replay — ACCEPT

The original accepted ray has canonical source velocity (16,3), parameter duration 2, and unfolded endpoint (40,10) over actual T=(24,2). Its terminal physical sheet has both signs negative. The integer-vertex-fixing twists preserve that endpoint point on the surface. Their derivatives give

    V_120(16,3) = (16,1923),
    H_192(16,1923) = (369232,1923).

The affine maps preserve the original path parameter, so at |vy|=1 the predicted duration is 2*1923=3846. The successful exact original-wall replay independently confirms:

| Prescribed quantity | Verified result |
| --- | --- |
| Actual first T time | 3846 |
| Ordinary reflections | 47,748 |
| Whole-path finite-wall leg guards | 477,490 |
| Downward / upward R entries | 97 / 96 |
| Actual bottom-floor contacts | 176 |
| First R position | 53848/1923 = 28+4/1923 |
| First ten circuits | Both bottom target-height visits in (28,29); signed h-section formulas agree |

The path digest agrees with the pinned coordinator path digest. The independently extracted first eleven downward R entries have positive horizontal sign and exactly the predicted progression. The first ten upward R entries and the corresponding twenty BOTTOM-chamber target-height visits agree with the hand formulas and signs. No true corner or earlier actual target hit occurs.

The source-arm and bottom-chamber crossings must be distinguished in postprocessing: there are 473 total visits to height 2, of which 353 are in the bottom chamber. The final target is reached downward before the next floor. Two initial postprocessing assertions counted these incorrectly; the physical replay passed each time. I corrected that postprocessing and reran the SAME prescribed ray, without changing room, direction, coefficient or physical guards. Final evidence and this limitation are recorded in the JSON.

Computational independence is bounded: this reruns the existing accepted REVIEWER earliest-wall and path-check functions, rather than a second numerical engine. The coordinator checker was read but not executed. Independent mathematical evidence is the A/B hand derivation above and the separate signed-section checks. No sample count is used to prove the general quantifiers.

## Integrity, native state and final scope

All three request pins and the six referenced proof/reviewer-source pins match before and after replay; final checks and the request digest are in `three-reflex-two-sided-return-independent.json`. Source and coordinator evidence files were not changed. Only these two new owned review outputs and the shared board were written.

The native goal remains the SAME blocked goal, with its full objective, history, accounting, budget waiver and old clocks preserved. This scoped review does not restart blocked no-progress loops. General ordered-spiral nonemptiness, all r3 and full r<=8 illumination remain OPEN, and no qualifying actual dark counterexample is supplied.
