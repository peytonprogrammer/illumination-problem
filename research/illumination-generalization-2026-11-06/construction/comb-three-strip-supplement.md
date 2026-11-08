# Three independent strip parameters: finite possible-dark remainder

A31 supplement under its SAME original05:33:48Z deadline. Conditional on independent acceptance of the frozen uniform independent-depth supplement; its first review was still pending at authoring. The literal two-strip join has already been independently accepted. No finite remainder entry is decided by this statement.

## Exact family

Start with a fixed rational comb, actual marks strictly in two different EQUAL-height teeth of height u, with fixed offsets0<b_s,b_t<u and fixed positive horizontal depths d_s,d_t. Their right ends have fixed positive margins beyond the marks. Select one tooth-free bare-spine gap BETWEEN these teeth, of positive initial width G. The spine width is c>0.

Independently extend ONLY the source tooth right end and actual source abscissa by2n_s, and ONLY the target tooth right end and actual target abscissa by2n_t. Insert2m vertically into the selected bare gap, translating exactly its upper bands, marks and spine top. Other tooth widths are fixed. Let n_s,n_t,m range independently over all nonnegative integers.

As in comb-two-strip-join.md, the three insertions commute and preserve strict simplicity, every positive segment and the maximal wall count. Coincidence or crossing of different teeth's right-end x levels creates no boundary contact because their vertical bands stay separated. Integer canonical input and even-even actual marks remain canonical/A throughout. The selected separation is H=H0+2m>=2u+M_min for M_min=H0-2u>0. No k, support, area, diameter or interior-point cap is assumed.

## The region with two large independent depths

The uniform independent-depth theorem supplies a computable rational D0 depending only on c,u,M_min,b_s,b_t, valid for ALL m and all extra tooth configurations. Define

    N_s=max(0,ceil((D0-d_s)/2)),
    N_t=max(0,ceil((D0-d_t)/2)).

Every entry with n_s>=N_s AND n_t>=N_t illuminates, for every m>=0. This is an entire two-depth orthant, not an inference from eventuality on rays.

## Each small source coordinate is an actual perpendicular two-neck family

Fix one integer i<N_s and set n_s=i. Cut the bare vertical gap into two rational retained collars and a positive core of length G/3, exactly as in the accepted two-strip join. Independently choose two vertical cuts inside the TARGET tooth at x=c+epsilon_1 and c+epsilon_2, where

    0<epsilon_1<epsilon_2<min(d_t,R_t-c).

The target horizontal core has width u and positive initial length epsilon_2-epsilon_1. Its length becomes epsilon_2-epsilon_1+2n_t; its right chamber and actual target translate by2n_t. The vertical core has width c and length G/3+2m. It lies in the bare spine x<=c, whereas the horizontal core lies at x>c, so the two are disjoint.

After these two cuts there are EXACTLY three fixed capped chamber disks for this fixed i:

1. the lower spine component with the source tooth at its fixed n_s=i and actual S;
2. the upper spine component with the fixed stub of the target tooth and every other upper tooth;
3. the target tooth's right rectangle containing the actual T, beyond its horizontal core.

The lower/upper components are joined by the vertical core, and the upper/right components by the horizontal core. Other teeth are parts of fixed chambers; they do not become additional varying necks. Piece interiors are disjoint, their only contacts are intended smooth relative-interior mouths, and the actual union is the SPECIFIED comb for EVERY n_t,m>=0. There is no omitted cap mirror, crossing slab or unintended tooth contact. Both actual marks lie strictly inside the two OUTER chambers of this three-node chain. This remains true at n_t=m=0 because both initial cores and collars are positive.

Rotate/reflect/reverse the chain if necessary to match the accepted horizontal/vertical order convention. The independently accepted effective perpendicular-neck theorem, with its reviewed wrapped-chamber correction, now applies literally. It does NOT require a previously discovered path: hold one neck fixed and use the accepted rational first-mouth one-neck algorithm on the other to obtain an actual reference witness; source/target separation forces that witness through BOTH varying necks. A path traversing both orthogonal cores has nonzero horizontal AND vertical velocity magnitudes. The rational algorithm supplies an exact finite rational-direction witness when the lengths are rational. The accepted quantitative joint-tail construction and finitely many fixed-coordinate first-mouth tails then compute a finite possible-dark rectangle R_i in(n_t,m).

The cap endpoints, including smooth subdivision points, are excluded by the first-mouth procedure. Every joined reflection is on an actual nonmouth chamber wall or an actual neck sidewall. All endpoint and full-word guards are inherited through this exact decomposition; no selected target lift replaces actual T. There is no unproved generic-path existence or phase-search premise.

## The symmetric finite collection of small target coordinates

For each integer j<N_t fix n_t=j, and instead cut the SOURCE tooth's horizontal core. The same argument, reversing actual source/target when needed, gives an exact three-chamber perpendicular-neck family in(n_s,m), hence a computable finite possible-dark rectangle R'_j. Reversibility of an ordinary corner-avoiding path preserves its actual endpoints and every smooth contact.

## The complete finite union

Any possibly dark triple is in the finite set

    union_{0<=i<N_s} {(i,n_t,m):(n_t,m) in R_i}
      union
    union_{0<=j<N_t} {(n_s,j,m):(n_s,m) in R'_j}.             (1)

Indeed if neither small-coordinate condition holds, both depths exceed D0 and the uniform theorem applies. Otherwise the corresponding exact perpendicular-neck remainder includes every exception on that slice. Both unions have finitely many computable finite entries, with empty unions interpreted literally. Overlap does not matter. Taking coordinatewise maxima plus1 yields a finite bounding box if desired; the sharper finite union is enough.

The construction is a mathematical computability result using finitely many terminating rational procedures. None was run in this proof effort, and no840-second runtime promise follows. An actual timed run that did not finish would remain unfinished. Likewise a missing ray within a bounded search would not classify a member of(1) as dark.

## Proven implication and limits

Subject to acceptance of the cited uniform independent-depth theorem, EVERY member of the complete three-independent-parameter family outside(1) has a rigorously supplied actual legal trajectory. This closes the joint unbounded tail and witness-existence obligations for this particular disjoint-strip family, including shallow/deep mixed slices via actual neck geometry. It does not prove illumination of ANY unchecked entry in(1), decide all marked combs, permit changing tooth heights or many independent vertical gaps, cover diagonal-wall patterns, or complete the universal W<=21 goal.

The hypotheses are no stronger than those stated: fixed rational initial comb, two specified equal-height marked teeth, independent local horizontal insertions and one specified separating bare-spine vertical insertion. The universal minimum remains a separate open objective. No novelty or external refereeing claim is made.
