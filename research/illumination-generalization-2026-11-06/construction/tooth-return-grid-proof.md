# A54: all four-band A0/A1 rooms at common depths one and two

Author proof complete, pending independent review. The universal canonical45 W<=21 objective remains OPEN. All discovery and prescribed checks belong to the original effort starting 06:57:28Z with deadline 07:11:28Z; no restart renews that deadline.

## 1. Exact quantified statement

For any integers h>=3, D in {1,2}, and independently arbitrary integers a,b>=1, take core [0,1]x[0,G], selected RIGHT teeth [1,D+2]x[1,3] and [1,D+2]x[2h+1,2h+3], and LEFT teeth [-a,0]x[h,h+2] and [-b,0]x[Y2,Y2+2]. Use either

- A0: G=2h+4, Y2=h+4;
- A1: any integer d>=1, G=2h+d+4, Y2=h+d+2.

Then the actual interior marks S=(1+D,2), T=(1+D,2h+2) illuminate. Every room is a strictly simple 20-wall disk. The statement concerns this selected pair; additional interior A points in wide teeth are permitted. It assumes no upper bound on a,b,h,d, diameter, or transparent exceptions. Translation makes the points A points when appropriate, but the actual optical assertion needs no parity designation.

This closes the entire A0/A1 four-band region left by A51 for these two minimal selected widths. It is not an all-comb or universal polygon theorem. Equal depth zero remains separate, as do other residual comb patterns.

## 2. Actual one-tooth-return construction

Put t=2h+2. Work in either the ordinary target chart tc=t or the actual upper-end reflected target chart tc=2G-t. Set H=(tc-2)/2, an integer. The chosen opposite tooth in this chart has bottom Y equal either to its actual bottom or its reflected bottom 2G-Y_actual-2. Only a tooth copy lying between the developed endpoints is used.

Choose integers n>=0 and l,r>=1, and an open rational interval I=(L,U) of positive slopes satisfying the following STRICT physical guards throughout I. Define C=2-2n and B=tc+2n.

1. |D*tau-2n|<1.
2. Both entry C+(D+2l-1)tau and exit B-(D+2r-1)tau are strictly in (Y,Y+2).
3. For j=1,...,2l-2, the point at height C+(D+j)tau is a smooth actual core side mirror after end folding: odd j is the left side, even j the right side.
4. For j=1,...,2r-2 the analogous reverse-side heights B-(D+j)tau satisfy the same guard.

The guards in 3–4 mean avoidance of EVERY closed copied tooth band on that side and of the core-end corner level G. All these heights are in (0,2G). Left/right band lists in that developed range are exactly their two original bands plus their two reflections in G. An open core crossing of y=G has 0<x<1 and gives a genuine smooth roof reflection. No side contact at G is allowed.

Let w be the chosen actual opposite tooth width. Choose k>=0 and

    tau = (H+2n+2k)/(w+D+l+r-1) in I.                 (1)

The source starts with velocity (-1,(-1)^n*tau) and travels its actual horizontal depth D to the mouth. In height-two phase coordinates it runs from phase 1 to 1+(-1)^n D*tau. Guard 1 folds this to actual portal ordinate 2+D*tau-2n=C+D*tau with UPWARD exit velocity. There are exactly n smooth horizontal contacts, each at horizontal depth strictly between 0 and D, before the unused far wall. There is no mouth reflection.

Follow 2l-1 core legs to the chosen left tooth entry. Let A=C+(D+2l-1)tau-Y and A'=B-(D+2r-1)tau-Y, both in (0,2). Equation (1) is exactly

    A+2w*tau = A'+4k.                                (2)

Develop an actual excursion of horizontal length 2w: move left to the genuine far wall at depth w, reflect once there, and return to the same mouth. Fold its increasing height phase A+tau*u modulo 4 into [0,2]. Equation (2) yields UPWARD exit velocity and precisely 2k ordinary horizontal contacts. The only possible new corner is a simultaneous far/horizontal collision, equivalent to

    F = A+w*tau = H+2-Y+2k+(l-r)tau being EVEN integer. (3)

Exclude (3). Then all far and horizontal contacts are strict physical wall points. This construction folds only inside a closed rectangular tooth, never periodically through its open mouth.

After exit, take the 2r-1 guarded core legs to target portal B-D*tau=tc-(D*tau-2n), then append the reversed source prefix reflected by y -> 2+tc-y. It reaches the ORIGINAL selected target after global end folding. The selected widths D+1 exceed all prefix depths. Other opposite widths are unused and can vary independently. Truncate at an earlier actual T if there is one. Before end folding the reflection count is 2n+2k+2l+2r-3; roof crossings add ordinary reflections.

Thus (1), the interval guards, and the explicit exclusion (3) give a finite actual witness, not merely a correspondence or a prescribed witness transfer.

## 3. A whole-width tail from one strict interval

Let A_w=w+D+l+r-1. The slopes (1) form an arithmetic grid of step 2/A_w. If l!=r and A_w>4/(U-L), the interval contains TWO consecutive grid slopes. Their far phases differ by 2(l-r)/A_w, whose absolute value lies strictly between 0 and 2: A_w>|l-r| follows from w>0,D>=0 and l,r>=1. Therefore both phases cannot be even integers. At least one of these two candidates is legal.

If l=r and H+2-Y is odd, the far phase is always odd. One grid slope suffices under A_w>2/(U-L). If l=r and H+2-Y is even, discard the profile; it always hits a far corner.

A valid grid point automatically has k>=0: from (2), 4k=A+2w*tau-A'>-2, so integral k cannot be negative. Our explicit selection also enforces k>=0. A sufficient INTEGER tail threshold is

    N = max(1, floor(K/(U-L))-(D+l+r-1)+1),
    K=4 for l!=r and K=2 for l=r with odd constant phase.

For every w>=N, choose the first grid point strictly above L and the next, retaining a clean candidate; their strict upper bounds follow from the displayed grid-spacing inequality. These are formulas for all unbounded widths, not sampled extrapolations.

For a finite width w<N, the exact table retains an explicit n,l,r,k,tau whose interval and far phase pass all guards. If none of the retained profiles supplies it, that width is listed as uncovered by THIS construction. Such a label is never a darkness verdict.

## 4. Complete h>=5 cover

Accepted A51, common-depth-zigzag-proof.md, already covers A0 h>=9 and A1 h>=15,d>=1 OR h>=5,d>=6; its m=2/m=4 strict inequalities also cover the complement of its explicitly stated residual strip. Thus the ONLY h>=5 vertical rows requiring new optics are

    A0: h=5,6,7,8;
    A1: d1:h5..6; d2:h5..8; d3:h6..10;
        d4:h8..12; d5:h10..14.

For BOTH D1 and D2, the exact end-chart table supplies a valid whole-width tail for EACH opposite tooth in EVERY one of these rows. The table is tooth-return-grid-end-check.json, rows keyed by (kind,h,d,D), with each targets entry containing its tail profile and every retained finite-prefix witness. The actual all-slope guard verifier checks the affine image of the ENTIRE open slope interval against every closed copied band and the roof corner, not only a midpoint sample. For an affine image interval (u,v), disjointness from a closed band [a,b] is verified by v<=a or u>=b; endpoint equality is allowed only at an excluded slope endpoint.

Consequently an unresolved width pair in a row must lie in the Cartesian product of its two explicit uncovered-width lists. Across the stated h>=5 rows this product has EXACTLY 308 members, fixed before discovery in tooth-return-grid-large-inputs.json. ALL 308 have complete actual certificates in tooth-return-grid-large-seeds.json. For each original polygon the exact physical trace checks the first target, every finite wall intersection, unique smooth reflection, and no corner contact. Thus the width tails, explicit finite-prefix paths, and these precisely enumerated isolated pairs exhaust ALL independent integers a,b. No finite candidate bound is used to infer darkness.

The retained exact guards and actual controls are in tooth-return-grid-physical-check.json. The validator definitions are reused from an accepted helper; this is NOT independent review. The peer must independently check the interval arithmetic and isolated certificates.

## 5. Low-height local paths remove vertical tails

### h3,D1: A0 and ALL A1 d>=2, arbitrary a,b

The SAME actual path, initially (-2,5), is

S=(2,2), (8/5,3), (2/5,0), (0,1), (1,7/2), (0,6),
(6/5,9), (2,7), (14/5,9), (3,17/2), (12/5,7), T=(2,8).

Its only left-side core mirrors are y=1 and y=6. It enters NEITHER opposite tooth. The lower opening is [3,5]; the upper opening begins at 7 in A0 and at d+5>=7 in A1. All selected contacts lie strictly on their actual walls, including the far reflection at (3,17/2). All heights are <=9, below every actual roof in this class. Therefore the exact same path works for ALL a,b and every d>=2. The local cap used for discovery had an artificial roof y10 as a REJECTION boundary; no path touched it. This is a direct all-wall guard, not general illumination monotonicity.

### h3,D2: A0 and ALL A1 d>=2

For every a>=2 use section 2 with the ACTUAL lower tooth Y3, tc8, H3, n1,l1,r2 and any slope

    1<tau=(5+2k)/(a+4)<7/5.

The grid step 2/(a+4)<2/5 guarantees such an integer k; take k=floor((a-1)/2)+1. Its far phase is 2+2k-tau, noninteger. The source portal is 2tau; entry is 3tau in (3,21/5); exit is 10-5tau in (3,5). The remaining right mirror is 10-4tau in (22/5,6), between selected bands, and the remaining left mirror is 10-3tau in (29/5,7), strictly below the upper opening and above the lower opening. All actual prefixes are strict. Thus no opposite upper tooth or roof is used, uniformly in b and d>=2.

Only a1 remains. The actual 19-reflection (-3,-4) local cap path is stored in tooth-return-grid-cap.json. Its only left core mirrors outside its chosen lower tooth are y=2/3,2,6; it stays at height<=9, uses only the actual width-one lower tooth and selected width-three teeth, and never touches the rejected artificial roof. Thus it too works in A0 and every A1 d>=2, for ALL b. The complete coordinates and exact guards are stored, not inferred from failed searches.

### h4,D2: A0 and ALL A1 d>=2, arbitrary a,b

The SAME actual path, initially (-1,3), is

S=(3,2), (8/3,3), (2,1), (4/3,3), (1/3,0), (0,1),
(1,4), (0,7), (4/3,11), (2,9), (8/3,11), T=(3,10).

Its only left core mirrors are y1 and y7. The opposite openings are [4,6] and an upper band beginning at 8 in A0 or at d+6>=8 in A1. It enters NEITHER opposite tooth. All selected contacts are strict and heights<=11 lie below the actual roof. Hence it works for ALL a,b. Four identical local cap outputs at a1/2/4/8 are controls, not four isolated proof dependencies.

### h4,D1: ALL A1 d>=3, arbitrary a,b

For every a>=2 use the lower tooth Y4, tc10, H4, n0,l2,r3 and

    2/3<tau=(4+2k)/(a+5)<1.

One grid point exists since 2/(a+5)<1/3. Its far phase is 2+2k-tau, noninteger. Source portal is 2+tau, entry 2+4tau in (14/3,6), and exit 10-6tau in (4,6). The first left mirror 2+2tau is below4; subsequent left mirrors 10-4tau and 10-2tau lie in (6,22/3) and (8,26/3), respectively, below9. Every right turn is strictly in (3,9). The unused upper opening begins at d+6>=9. All selected arms and developed core segments have height<=11, below the actual roof.

For a1 use n0,l2,r4,k0,tau4/7. The entry is30/7, exit38/7, and far phase6/7. The left core mirrors are22/7,46/7,54/7,62/7, all outside [4,6] and below9. The right mirrors are strictly between3 and9. This single actual profile likewise works for every b and d>=3. Thus the entire unbounded vertical tail is covered, not merely the sampled d3..6 rows.

## 6. Exact remaining low rows

The all-slope/end-chart tables close A0 h4,D1 and A1 h4,d1,D1/2 for every a,b: at least one opposite-tooth profile has NO uncovered width after its explicit finite-prefix formulas. A1 h4,d2,D1 has uncovered widths {2,3,4,8} for BOTH teeth; the 16 Cartesian members have exact actual certificates in tooth-return-grid-seeds.json.

For A1 h3,d1, the two uncovered-width products are

- D1: a in {1,2,3,4,5,6,7,8}, b in {1,2,4,5,7,8,10,13,16}: 72 members.
- D2: a in {1,2,3,5,6,8,9}, b in {1,2,3,5,6,7,8,11,12,13,17,18,23}: 91 members.

All 163 have exact actual certificates in tooth-return-grid-small-seeds.json. That file also contains 11 redundant h4,D2 controls rendered unnecessary by the stronger explicit path above; they are not needed to fill a proof gap. The remaining low-row slope intervals and finite-prefix witnesses have their own exact all-slope guard and actual control verification in tooth-return-grid-low-physical-check.json.

This exhausts h3, h4, every h>=5 residual row, and every A51 large region for BOTH depths. No other h,d,a,b value in the exact statement remains. Every use of an end chart folds to original S,T and every tooth excursion uses a real far reflection. Selected-width D+1, integer opposite widths, and the stated four-band geometry remain hypotheses. Independent peer acceptance is required; universal W21, all-comb closure, and arbitrary endpoint/minimum-wall claims remain OPEN.
