# A55: every A0/A1 four-band room illuminates its actual seam pair

Author proof complete, pending independent review. Original conservative effort start07:10Z/deadline07:24Z includes preliminary zero-arm algebra. The universal canonical45 W<=21 theorem remains OPEN.

## 1. Statement

Take the exact A0/A1 room geometry in A54 section1 with D=0: core[0,1]x[0,G], selected RIGHT teeth of width1 in bands[1,3] and[2h+1,2h+3], and LEFT teeth of independently arbitrary positive INTEGER widths a,b in bands[h,h+2] and[Y2,Y2+2]. Here h>=3 is an integer and either

    A0: G=2h+4, Y2=h+4;
    A1: d>=1 integer, G=2h+d+4, Y2=h+d+2.

The actual interior seam marks S=(1,2), T=(1,2h+2) illuminate for EVERY such input. There is no cap on a,b,h,d, lattice diameter or transparent exceptions. Every room has20 maximal walls. Additional actual A points elsewhere are permitted; this statement concerns the selected actual pair. Its translated canonical A-pair applications preserve the physical endpoints. It does not assert arbitrary real widths, all-comb closure, or universal wall minimality.

The proof closes the zero-depth region excluded from A54. Frozen A54 sources remain unchanged; its independently accepted general return construction is used only with the additional physical fold proved here.

## 2. Two legitimate endpoint charts for actual seam marks

An actual seam endpoint in a selected width-one tooth has two useful developed depths:

- E0: empty normal arm, remaining at the actual seam;
- E2: develop to depth2 and fold at the ACTUAL far depth1, returning to the original actual seam.

For E2 apply the A54 common-depth arm construction at virtual common depth2. Its actual depth map is r -> 1-|r-1| on0<=r<=2. Every INTERNAL r maps to positive actual depth; only the two arm endpoints map to the open mouth. The arm crosses its genuine far line once. From a midpoint, that far crossing is a corner precisely when tau is an ODD integer. Therefore we exclude those slopes. Every other horizontal contact is on a finite actual selected wall. The folded terminal point is originalS or originalT, and at the mouth the coordinate map is the identity, preserving core velocity matching. This is a specific actual far-reflection construction, not a general widening implication.

Both arms use the same E, either0 or2, in each retained profile. Let tc be t=2h+2 or2G-t, H=(tc-2)/2, n>=0, l,r>=1, C=2-2n, B=tc+2n. For E2 require|2tau-2n|<1. For E0 require n0, with no endpoint-phase restriction: both arms are empty and source portal2/target portaltc are the actual marks.

For a chosen copied LEFT tooth bottomY and actual widthw, the entry/exit phases are

    A=C+(E+2l-1)tau-Y,
    A'=B-(E+2r-1)tau-Y.

The exact matching grid is

    tau=(H+2n+2k)/(w+E+l+r-1), k>=0,
    A+2w*tau=A'+4k.                               (1)

The genuine opposite-tooth far phase is

    H+2-Y+2k+(l-r)tau.                             (2)

It must not be an EVEN integer. The same explicit core turns, actual rectangular excursion, roof unfolding, reflected reverse target completion and first-target truncation as A54 section2 apply. For E2 fold ONLY the two selected arms by the depth map above; do not fold the core or opposite tooth horizontally. The proof preserves the original S,T, not a selected endpoint lift.

## 3. Whole-width tails with all actual guards

Each retained profile has an open rational slope interval I whose ENTIRE affine contact images avoid all copied closed tooth bands and core-end cornerG, with strict tooth portals and strict selected phases when E2 is used. For E2 the interval is split at EVERY odd integer before selection, so all its slopes avoid the additional actual selected-far corners. For E0 there is no such exclusion.

The A54 grid argument is unchanged with virtual depth E: put A_w=w+E+l+r-1. If l!=r and A_w>4/length(I), two consecutive grid slopes fit strictly in I, and the opposite far phases differ by nonzero2(l-r)/A_w of absolute value<2. They cannot both be even integers. Both candidates already avoid every selected-far corner by interval construction. If l=r with odd H+2-Y, one grid slope suffices under A_w>2/length(I). Even constant profiles are discarded. The explicit integer threshold and first-two-grid-point selection are exactly A54 section3 with E replacing D.

Thus a finite table of strict profiles proves each ALL-w tail. For smaller positive INTEGER widths the table retains explicit legal slope/profile choices where available. The absence of a retained choice is only a mechanism gap, not darkness. Each unused opposite width remains arbitrary because every core mirror avoids its entire mouth and the only entered left tooth is the chosen one.

## 4. Complete finite vertical and width cover

Accepted A51 covers A0 h>=9 and the large A1 regions stated there. Its complete h>=5 complement is exactly

    A0 h5..8;
    A1 d1:h5..6, d2:h5..8, d3:h6..10,
       d4:h8..12, d5:h10..14.

Add the two remaining low-height rows A1h3d1 and A1h4d1. The exact table seam-four-band-chart-check.json contains EXACTLY these27 distinct vertical rows. Each has a valid WHOLE-width tail for BOTH opposite teeth, after combining the E0 normal and E2 actual-far profiles. Every retained all-slope interval is checked against both original and reflected side-band lists and the actual roof corner. The physical checker independently reconstructs original width-one selected teeth, inserts the ACTUAL far-wall crossing in each E2 arm, folds just those arms, and checks original seam arrival.

For each row take the Cartesian product of its two explicit uncovered INTEGER width lists. Across all27 rows this has EXACTLY82 members, fixed before discovery in seam-four-band-inputs.json. The full original-room actual paths for ALL82 are in seam-four-band-seeds.json. Their contours use G=2h+4 or2h+d+4 computed from EACH row, not a template roof. Every finite wall intersection, corner exclusion, ordinary reflection and first original target has been checked exactly. Known unit-width members reproduce older accepted lit cases and are not claimed as new discoveries.

For audit, the only nonempty products are:

|row|lower uncovered widths|upper uncovered widths|
|---|---|---|
|A0 h6|1|1|
|A1 h6 d2|1|1|
|A1 h8 d2|3|2|
|A1 h10 d3|1|1,2,8|
|A1 h8 d4|1|1,2,3,6|
|A1 h9 d4|1|1|
|A1 h10 d4|1,4|1|
|A1 h11 d4|1,2|1|
|A1 h12 d4|1|1,2|
|A1 h3 d1|1,2,3,5,6|1,2,3,5,6,7,8,11,12,13,17,18,23|

The width tails, explicit finite-prefix choices, and precisely these positive isolated certificates cover ALL a,b in the27 rows. Finite path controls do not establish the unbounded claim; the grid inequalities do. The accepted validator definitions are reused author-side, so these checks are not independent review.

## 5. All remaining low-height vertical parameters

### h3, lower widtha>=2: A0 and every A1 d>=2

Use E0,n0,l1,r2,Y3,tc8,H3 and

    tau=(3+2k)/(a+2) in(1,5/3),
    k=floor((a-1)/2)+1.

Since2/(a+2)<2/3 at EVERYa>=2, the displayed rounding gives a strict grid slope. The source arm is EMPTY and starts at actualS. Entry is2+tau in(3,11/3), exit8-3tau in(3,5), the remaining right mirror8-2tau lies in(14/3,6), and the remaining left mirror8-tau lies in(19/3,7). Hence both mirrors avoid the chosen lower mouth and every upper mouth beginning at7 or higher. The far phase2+2k-tau is noninteger. The final core leg reaches original seamT, with no target arm or mouth reflection. No end wall is used. This proves every a>=2 uniformly in b and all d>=2.

### h3, a1: the actual accepted local cap path

Use the literal path, the horizontal reflection of the accepted A48 h3 cap certificate,

(1,2),(0,2/3),(1/2,0),(1,2/3),(0,2),(1,10/3),
(-1/4,5),(-1,4),(-1/4,3),(1,14/3),(0,6),
(2,26/3),(7/4,9),(1,8).

Every leg has absolute slope4/3 and each turn obeys the ordinary axial law. The only opposite tooth entered is the ACTUAL lower width-one tooth[-1,0]x[3,5]. All its far/horizontal contacts are strict. Outside it, left core mirrors are2/3,2,6, below the upper opening beginning at7 or higher. The selected upper far point(2,26/3) and horizontal point(7/4,9) are strict. All heights<=9 lie below the actual A0 roof10 and every A1 roof atd>=2. Thus every b and d>=2 is covered by direct actual-wall guards. An artificial cap roof was only a rejection boundary, never a used mirror. No monotonicity assumption is involved.

Together these two mechanisms prove A0h3 and ALLA1h3d>=2. The d1 row was already covered by section4.

### h4: A0 and ALL A1 d>=2, arbitrary a,b

Use the literal actual path

    (1,2),(1/3,0),(0,1),(1,4),(0,7),(1,10).

It has four strict ordinary reflections, absolute slope3, and enters NEITHER opposite tooth. Its only left mirrors are1 and7, outside [4,6] and every upper opening beginning at8 or higher. The selected-side mirror4 is strictly between selected mouths[1,3] and[9,11]. The floor contact1/3 is a genuine smooth actual floor point. No roof is used, and originalT is reached at its interior seam. Hence all opposite widths and all d>=2 are irrelevant to the used geometry. A1h4d1 was already covered by section4.

The literal paths and h3 normal-return formulas have additional exact full-room controls in seam-four-band-caps-check.json, including d=1,000,000 and unequal widths. Their hand guards prove the arbitrary-parameter transfer; the controls only check prescribed instances.

## 6. Exhaustion and boundaries

A51 covers the large h regions. Section4 covers its entire h>=5 complement and both d1 low rows. Section5 covers A0h3/4 and A1h3/4 at every d>=2. Thus every h>=3, every A1d>=1, and ALL independent positive integer a,b in the statement have an actual finite legal S-to-T path. No width denominator cutoff or finite failed search is used as proof.

Together with independently accepted A54 (including mandatory F1 roof correction), this settles common D0/1/2 with minimal selected widthsD+1 in the A0/A1 model. The generic common-depth far-fold theorem R43 handles its own larger-depth/larger-selected-width hypotheses separately. Other comb patterns, arbitrary core widths, taller teeth and diagonal canonical45 rooms remain outside this packet. Universal W21 remains OPEN. Final acceptance of A55 requires explicit independent peer review of its new actual selected-far folds, all interval/product coverage and every finite original-room certificate.
